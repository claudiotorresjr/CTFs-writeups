
rocket_blaster_xxx:     file format elf64-x86-64


Disassembly of section .init:

0000000000401000 <_init>:
  401000:	f3 0f 1e fa          	endbr64
  401004:	48 83 ec 08          	sub    $0x8,%rsp
  401008:	48 8b 05 e9 3f 00 00 	mov    0x3fe9(%rip),%rax        # 404ff8 <__gmon_start__@Base>
  40100f:	48 85 c0             	test   %rax,%rax
  401012:	74 02                	je     401016 <_init+0x16>
  401014:	ff d0                	call   *%rax
  401016:	48 83 c4 08          	add    $0x8,%rsp
  40101a:	c3                   	ret

Disassembly of section .plt:

0000000000401020 <.plt>:
  401020:	ff 35 62 3f 00 00    	push   0x3f62(%rip)        # 404f88 <_GLOBAL_OFFSET_TABLE_+0x8>
  401026:	f2 ff 25 63 3f 00 00 	bnd jmp *0x3f63(%rip)        # 404f90 <_GLOBAL_OFFSET_TABLE_+0x10>
  40102d:	0f 1f 00             	nopl   (%rax)
  401030:	f3 0f 1e fa          	endbr64
  401034:	68 00 00 00 00       	push   $0x0
  401039:	f2 e9 e1 ff ff ff    	bnd jmp 401020 <_init+0x20>
  40103f:	90                   	nop
  401040:	f3 0f 1e fa          	endbr64
  401044:	68 01 00 00 00       	push   $0x1
  401049:	f2 e9 d1 ff ff ff    	bnd jmp 401020 <_init+0x20>
  40104f:	90                   	nop
  401050:	f3 0f 1e fa          	endbr64
  401054:	68 02 00 00 00       	push   $0x2
  401059:	f2 e9 c1 ff ff ff    	bnd jmp 401020 <_init+0x20>
  40105f:	90                   	nop
  401060:	f3 0f 1e fa          	endbr64
  401064:	68 03 00 00 00       	push   $0x3
  401069:	f2 e9 b1 ff ff ff    	bnd jmp 401020 <_init+0x20>
  40106f:	90                   	nop
  401070:	f3 0f 1e fa          	endbr64
  401074:	68 04 00 00 00       	push   $0x4
  401079:	f2 e9 a1 ff ff ff    	bnd jmp 401020 <_init+0x20>
  40107f:	90                   	nop
  401080:	f3 0f 1e fa          	endbr64
  401084:	68 05 00 00 00       	push   $0x5
  401089:	f2 e9 91 ff ff ff    	bnd jmp 401020 <_init+0x20>
  40108f:	90                   	nop
  401090:	f3 0f 1e fa          	endbr64
  401094:	68 06 00 00 00       	push   $0x6
  401099:	f2 e9 81 ff ff ff    	bnd jmp 401020 <_init+0x20>
  40109f:	90                   	nop
  4010a0:	f3 0f 1e fa          	endbr64
  4010a4:	68 07 00 00 00       	push   $0x7
  4010a9:	f2 e9 71 ff ff ff    	bnd jmp 401020 <_init+0x20>
  4010af:	90                   	nop
  4010b0:	f3 0f 1e fa          	endbr64
  4010b4:	68 08 00 00 00       	push   $0x8
  4010b9:	f2 e9 61 ff ff ff    	bnd jmp 401020 <_init+0x20>
  4010bf:	90                   	nop
  4010c0:	f3 0f 1e fa          	endbr64
  4010c4:	68 09 00 00 00       	push   $0x9
  4010c9:	f2 e9 51 ff ff ff    	bnd jmp 401020 <_init+0x20>
  4010cf:	90                   	nop
  4010d0:	f3 0f 1e fa          	endbr64
  4010d4:	68 0a 00 00 00       	push   $0xa
  4010d9:	f2 e9 41 ff ff ff    	bnd jmp 401020 <_init+0x20>
  4010df:	90                   	nop

Disassembly of section .plt.sec:

00000000004010e0 <puts@plt>:
  4010e0:	f3 0f 1e fa          	endbr64
  4010e4:	f2 ff 25 ad 3e 00 00 	bnd jmp *0x3ead(%rip)        # 404f98 <puts@GLIBC_2.2.5>
  4010eb:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

00000000004010f0 <printf@plt>:
  4010f0:	f3 0f 1e fa          	endbr64
  4010f4:	f2 ff 25 a5 3e 00 00 	bnd jmp *0x3ea5(%rip)        # 404fa0 <printf@GLIBC_2.2.5>
  4010fb:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000401100 <alarm@plt>:
  401100:	f3 0f 1e fa          	endbr64
  401104:	f2 ff 25 9d 3e 00 00 	bnd jmp *0x3e9d(%rip)        # 404fa8 <alarm@GLIBC_2.2.5>
  40110b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000401110 <close@plt>:
  401110:	f3 0f 1e fa          	endbr64
  401114:	f2 ff 25 95 3e 00 00 	bnd jmp *0x3e95(%rip)        # 404fb0 <close@GLIBC_2.2.5>
  40111b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000401120 <fputc@plt>:
  401120:	f3 0f 1e fa          	endbr64
  401124:	f2 ff 25 8d 3e 00 00 	bnd jmp *0x3e8d(%rip)        # 404fb8 <fputc@GLIBC_2.2.5>
  40112b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000401130 <read@plt>:
  401130:	f3 0f 1e fa          	endbr64
  401134:	f2 ff 25 85 3e 00 00 	bnd jmp *0x3e85(%rip)        # 404fc0 <read@GLIBC_2.2.5>
  40113b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000401140 <fflush@plt>:
  401140:	f3 0f 1e fa          	endbr64
  401144:	f2 ff 25 7d 3e 00 00 	bnd jmp *0x3e7d(%rip)        # 404fc8 <fflush@GLIBC_2.2.5>
  40114b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000401150 <setvbuf@plt>:
  401150:	f3 0f 1e fa          	endbr64
  401154:	f2 ff 25 75 3e 00 00 	bnd jmp *0x3e75(%rip)        # 404fd0 <setvbuf@GLIBC_2.2.5>
  40115b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000401160 <open@plt>:
  401160:	f3 0f 1e fa          	endbr64
  401164:	f2 ff 25 6d 3e 00 00 	bnd jmp *0x3e6d(%rip)        # 404fd8 <open@GLIBC_2.2.5>
  40116b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000401170 <perror@plt>:
  401170:	f3 0f 1e fa          	endbr64
  401174:	f2 ff 25 65 3e 00 00 	bnd jmp *0x3e65(%rip)        # 404fe0 <perror@GLIBC_2.2.5>
  40117b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000401180 <exit@plt>:
  401180:	f3 0f 1e fa          	endbr64
  401184:	f2 ff 25 5d 3e 00 00 	bnd jmp *0x3e5d(%rip)        # 404fe8 <exit@GLIBC_2.2.5>
  40118b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

Disassembly of section .text:

0000000000401190 <_start>:
  401190:	f3 0f 1e fa          	endbr64
  401194:	31 ed                	xor    %ebp,%ebp
  401196:	49 89 d1             	mov    %rdx,%r9
  401199:	5e                   	pop    %rsi
  40119a:	48 89 e2             	mov    %rsp,%rdx
  40119d:	48 83 e4 f0          	and    $0xfffffffffffffff0,%rsp
  4011a1:	50                   	push   %rax
  4011a2:	54                   	push   %rsp
  4011a3:	45 31 c0             	xor    %r8d,%r8d
  4011a6:	31 c9                	xor    %ecx,%ecx
  4011a8:	48 c7 c7 fa 14 40 00 	mov    $0x4014fa,%rdi
  4011af:	ff 15 3b 3e 00 00    	call   *0x3e3b(%rip)        # 404ff0 <__libc_start_main@GLIBC_2.34>
  4011b5:	f4                   	hlt
  4011b6:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
  4011bd:	00 00 00 

00000000004011c0 <_dl_relocate_static_pie>:
  4011c0:	f3 0f 1e fa          	endbr64
  4011c4:	c3                   	ret
  4011c5:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
  4011cc:	00 00 00 
  4011cf:	90                   	nop

00000000004011d0 <deregister_tm_clones>:
  4011d0:	b8 10 50 40 00       	mov    $0x405010,%eax
  4011d5:	48 3d 10 50 40 00    	cmp    $0x405010,%rax
  4011db:	74 13                	je     4011f0 <deregister_tm_clones+0x20>
  4011dd:	b8 00 00 00 00       	mov    $0x0,%eax
  4011e2:	48 85 c0             	test   %rax,%rax
  4011e5:	74 09                	je     4011f0 <deregister_tm_clones+0x20>
  4011e7:	bf 10 50 40 00       	mov    $0x405010,%edi
  4011ec:	ff e0                	jmp    *%rax
  4011ee:	66 90                	xchg   %ax,%ax
  4011f0:	c3                   	ret
  4011f1:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
  4011f8:	00 00 00 00 
  4011fc:	0f 1f 40 00          	nopl   0x0(%rax)

0000000000401200 <register_tm_clones>:
  401200:	be 10 50 40 00       	mov    $0x405010,%esi
  401205:	48 81 ee 10 50 40 00 	sub    $0x405010,%rsi
  40120c:	48 89 f0             	mov    %rsi,%rax
  40120f:	48 c1 ee 3f          	shr    $0x3f,%rsi
  401213:	48 c1 f8 03          	sar    $0x3,%rax
  401217:	48 01 c6             	add    %rax,%rsi
  40121a:	48 d1 fe             	sar    %rsi
  40121d:	74 11                	je     401230 <register_tm_clones+0x30>
  40121f:	b8 00 00 00 00       	mov    $0x0,%eax
  401224:	48 85 c0             	test   %rax,%rax
  401227:	74 07                	je     401230 <register_tm_clones+0x30>
  401229:	bf 10 50 40 00       	mov    $0x405010,%edi
  40122e:	ff e0                	jmp    *%rax
  401230:	c3                   	ret
  401231:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
  401238:	00 00 00 00 
  40123c:	0f 1f 40 00          	nopl   0x0(%rax)

0000000000401240 <__do_global_dtors_aux>:
  401240:	f3 0f 1e fa          	endbr64
  401244:	80 3d dd 3d 00 00 00 	cmpb   $0x0,0x3ddd(%rip)        # 405028 <completed.0>
  40124b:	75 13                	jne    401260 <__do_global_dtors_aux+0x20>
  40124d:	55                   	push   %rbp
  40124e:	48 89 e5             	mov    %rsp,%rbp
  401251:	e8 7a ff ff ff       	call   4011d0 <deregister_tm_clones>
  401256:	c6 05 cb 3d 00 00 01 	movb   $0x1,0x3dcb(%rip)        # 405028 <completed.0>
  40125d:	5d                   	pop    %rbp
  40125e:	c3                   	ret
  40125f:	90                   	nop
  401260:	c3                   	ret
  401261:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
  401268:	00 00 00 00 
  40126c:	0f 1f 40 00          	nopl   0x0(%rax)

0000000000401270 <frame_dummy>:
  401270:	f3 0f 1e fa          	endbr64
  401274:	eb 8a                	jmp    401200 <register_tm_clones>

0000000000401276 <error>:
  401276:	f3 0f 1e fa          	endbr64
  40127a:	55                   	push   %rbp
  40127b:	48 89 e5             	mov    %rsp,%rbp
  40127e:	48 83 ec 10          	sub    $0x10,%rsp
  401282:	48 89 7d f8          	mov    %rdi,-0x8(%rbp)
  401286:	48 8b 45 f8          	mov    -0x8(%rbp),%rax
  40128a:	48 8d 15 77 0d 00 00 	lea    0xd77(%rip),%rdx        # 402008 <_IO_stdin_used+0x8>
  401291:	48 89 d1             	mov    %rdx,%rcx
  401294:	48 89 c2             	mov    %rax,%rdx
  401297:	48 8d 05 72 0d 00 00 	lea    0xd72(%rip),%rax        # 402010 <_IO_stdin_used+0x10>
  40129e:	48 89 c6             	mov    %rax,%rsi
  4012a1:	48 8d 05 70 0d 00 00 	lea    0xd70(%rip),%rax        # 402018 <_IO_stdin_used+0x18>
  4012a8:	48 89 c7             	mov    %rax,%rdi
  4012ab:	b8 00 00 00 00       	mov    $0x0,%eax
  4012b0:	e8 3b fe ff ff       	call   4010f0 <printf@plt>
  4012b5:	90                   	nop
  4012b6:	c9                   	leave
  4012b7:	c3                   	ret

00000000004012b8 <cls>:
  4012b8:	f3 0f 1e fa          	endbr64
  4012bc:	55                   	push   %rbp
  4012bd:	48 89 e5             	mov    %rsp,%rbp
  4012c0:	48 8d 05 5e 0d 00 00 	lea    0xd5e(%rip),%rax        # 402025 <_IO_stdin_used+0x25>
  4012c7:	48 89 c7             	mov    %rax,%rdi
  4012ca:	b8 00 00 00 00       	mov    $0x0,%eax
  4012cf:	e8 1c fe ff ff       	call   4010f0 <printf@plt>
  4012d4:	ba 00 00 00 00       	mov    $0x0,%edx
  4012d9:	be 00 00 00 00       	mov    $0x0,%esi
  4012de:	48 8d 05 45 0d 00 00 	lea    0xd45(%rip),%rax        # 40202a <_IO_stdin_used+0x2a>
  4012e5:	48 89 c7             	mov    %rax,%rdi
  4012e8:	b8 00 00 00 00       	mov    $0x0,%eax
  4012ed:	e8 fe fd ff ff       	call   4010f0 <printf@plt>
  4012f2:	90                   	nop
  4012f3:	5d                   	pop    %rbp
  4012f4:	c3                   	ret

00000000004012f5 <fill_ammo>:
  4012f5:	f3 0f 1e fa          	endbr64
  4012f9:	55                   	push   %rbp
  4012fa:	48 89 e5             	mov    %rsp,%rbp
  4012fd:	48 83 ec 30          	sub    $0x30,%rsp
  401301:	48 89 7d e8          	mov    %rdi,-0x18(%rbp)
  401305:	48 89 75 e0          	mov    %rsi,-0x20(%rbp)
  401309:	48 89 55 d8          	mov    %rdx,-0x28(%rbp)
  40130d:	be 00 00 00 00       	mov    $0x0,%esi
  401312:	48 8d 05 1a 0d 00 00 	lea    0xd1a(%rip),%rax        # 402033 <_IO_stdin_used+0x33>
  401319:	48 89 c7             	mov    %rax,%rdi
  40131c:	b8 00 00 00 00       	mov    $0x0,%eax
  401321:	e8 3a fe ff ff       	call   401160 <open@plt>
  401326:	89 45 fc             	mov    %eax,-0x4(%rbp)
  401329:	83 7d fc 00          	cmpl   $0x0,-0x4(%rbp)
  40132d:	79 19                	jns    401348 <fill_ammo+0x53>
  40132f:	48 8d 05 0a 0d 00 00 	lea    0xd0a(%rip),%rax        # 402040 <_IO_stdin_used+0x40>
  401336:	48 89 c7             	mov    %rax,%rdi
  401339:	e8 32 fe ff ff       	call   401170 <perror@plt>
  40133e:	bf 01 00 00 00       	mov    $0x1,%edi
  401343:	e8 38 fe ff ff       	call   401180 <exit@plt>
  401348:	b8 ef be ad de       	mov    $0xdeadbeef,%eax
  40134d:	48 39 45 e8          	cmp    %rax,-0x18(%rbp)
  401351:	74 3c                	je     40138f <fill_ammo+0x9a>
  401353:	48 8d 05 b6 0c 00 00 	lea    0xcb6(%rip),%rax        # 402010 <_IO_stdin_used+0x10>
  40135a:	48 89 c1             	mov    %rax,%rcx
  40135d:	48 8d 05 a4 0c 00 00 	lea    0xca4(%rip),%rax        # 402008 <_IO_stdin_used+0x8>
  401364:	48 89 c2             	mov    %rax,%rdx
  401367:	48 8d 05 a2 0c 00 00 	lea    0xca2(%rip),%rax        # 402010 <_IO_stdin_used+0x10>
  40136e:	48 89 c6             	mov    %rax,%rsi
  401371:	48 8d 05 08 0d 00 00 	lea    0xd08(%rip),%rax        # 402080 <_IO_stdin_used+0x80>
  401378:	48 89 c7             	mov    %rax,%rdi
  40137b:	b8 00 00 00 00       	mov    $0x0,%eax
  401380:	e8 6b fd ff ff       	call   4010f0 <printf@plt>
  401385:	bf 01 00 00 00       	mov    $0x1,%edi
  40138a:	e8 f1 fd ff ff       	call   401180 <exit@plt>
  40138f:	b8 be ba ad de       	mov    $0xdeadbabe,%eax
  401394:	48 39 45 e0          	cmp    %rax,-0x20(%rbp)
  401398:	74 43                	je     4013dd <fill_ammo+0xe8>
  40139a:	4c 8d 05 6f 0c 00 00 	lea    0xc6f(%rip),%r8        # 402010 <_IO_stdin_used+0x10>
  4013a1:	48 8d 05 60 0c 00 00 	lea    0xc60(%rip),%rax        # 402008 <_IO_stdin_used+0x8>
  4013a8:	48 89 c1             	mov    %rax,%rcx
  4013ab:	48 8d 05 5e 0c 00 00 	lea    0xc5e(%rip),%rax        # 402010 <_IO_stdin_used+0x10>
  4013b2:	48 89 c2             	mov    %rax,%rdx
  4013b5:	48 8d 05 fa 0c 00 00 	lea    0xcfa(%rip),%rax        # 4020b6 <_IO_stdin_used+0xb6>
  4013bc:	48 89 c6             	mov    %rax,%rsi
  4013bf:	48 8d 05 fa 0c 00 00 	lea    0xcfa(%rip),%rax        # 4020c0 <_IO_stdin_used+0xc0>
  4013c6:	48 89 c7             	mov    %rax,%rdi
  4013c9:	b8 00 00 00 00       	mov    $0x0,%eax
  4013ce:	e8 1d fd ff ff       	call   4010f0 <printf@plt>
  4013d3:	bf 02 00 00 00       	mov    $0x2,%edi
  4013d8:	e8 a3 fd ff ff       	call   401180 <exit@plt>
  4013dd:	b8 37 13 ad de       	mov    $0xdead1337,%eax
  4013e2:	48 39 45 d8          	cmp    %rax,-0x28(%rbp)
  4013e6:	74 43                	je     40142b <fill_ammo+0x136>
  4013e8:	4c 8d 05 21 0c 00 00 	lea    0xc21(%rip),%r8        # 402010 <_IO_stdin_used+0x10>
  4013ef:	48 8d 05 12 0c 00 00 	lea    0xc12(%rip),%rax        # 402008 <_IO_stdin_used+0x8>
  4013f6:	48 89 c1             	mov    %rax,%rcx
  4013f9:	48 8d 05 10 0c 00 00 	lea    0xc10(%rip),%rax        # 402010 <_IO_stdin_used+0x10>
  401400:	48 89 c2             	mov    %rax,%rdx
  401403:	48 8d 05 ac 0c 00 00 	lea    0xcac(%rip),%rax        # 4020b6 <_IO_stdin_used+0xb6>
  40140a:	48 89 c6             	mov    %rax,%rsi
  40140d:	48 8d 05 ec 0c 00 00 	lea    0xcec(%rip),%rax        # 402100 <_IO_stdin_used+0x100>
  401414:	48 89 c7             	mov    %rax,%rdi
  401417:	b8 00 00 00 00       	mov    $0x0,%eax
  40141c:	e8 cf fc ff ff       	call   4010f0 <printf@plt>
  401421:	bf 03 00 00 00       	mov    $0x3,%edi
  401426:	e8 55 fd ff ff       	call   401180 <exit@plt>
  40142b:	48 8d 05 84 0c 00 00 	lea    0xc84(%rip),%rax        # 4020b6 <_IO_stdin_used+0xb6>
  401432:	48 89 c6             	mov    %rax,%rsi
  401435:	48 8d 05 04 0d 00 00 	lea    0xd04(%rip),%rax        # 402140 <_IO_stdin_used+0x140>
  40143c:	48 89 c7             	mov    %rax,%rdi
  40143f:	b8 00 00 00 00       	mov    $0x0,%eax
  401444:	e8 a7 fc ff ff       	call   4010f0 <printf@plt>
  401449:	48 8b 05 d0 3b 00 00 	mov    0x3bd0(%rip),%rax        # 405020 <stdin@GLIBC_2.2.5>
  401450:	48 89 c7             	mov    %rax,%rdi
  401453:	e8 e8 fc ff ff       	call   401140 <fflush@plt>
  401458:	48 8b 05 b1 3b 00 00 	mov    0x3bb1(%rip),%rax        # 405010 <stdout@GLIBC_2.2.5>
  40145f:	48 89 c7             	mov    %rax,%rdi
  401462:	e8 d9 fc ff ff       	call   401140 <fflush@plt>
  401467:	eb 18                	jmp    401481 <fill_ammo+0x18c>
  401469:	0f b6 45 fb          	movzbl -0x5(%rbp),%eax
  40146d:	0f be c0             	movsbl %al,%eax
  401470:	48 8b 15 99 3b 00 00 	mov    0x3b99(%rip),%rdx        # 405010 <stdout@GLIBC_2.2.5>
  401477:	48 89 d6             	mov    %rdx,%rsi
  40147a:	89 c7                	mov    %eax,%edi
  40147c:	e8 9f fc ff ff       	call   401120 <fputc@plt>
  401481:	48 8d 4d fb          	lea    -0x5(%rbp),%rcx
  401485:	8b 45 fc             	mov    -0x4(%rbp),%eax
  401488:	ba 01 00 00 00       	mov    $0x1,%edx
  40148d:	48 89 ce             	mov    %rcx,%rsi
  401490:	89 c7                	mov    %eax,%edi
  401492:	e8 99 fc ff ff       	call   401130 <read@plt>
  401497:	48 85 c0             	test   %rax,%rax
  40149a:	7f cd                	jg     401469 <fill_ammo+0x174>
  40149c:	8b 45 fc             	mov    -0x4(%rbp),%eax
  40149f:	89 c7                	mov    %eax,%edi
  4014a1:	e8 6a fc ff ff       	call   401110 <close@plt>
  4014a6:	48 8b 05 73 3b 00 00 	mov    0x3b73(%rip),%rax        # 405020 <stdin@GLIBC_2.2.5>
  4014ad:	48 89 c7             	mov    %rax,%rdi
  4014b0:	e8 8b fc ff ff       	call   401140 <fflush@plt>
  4014b5:	48 8b 05 54 3b 00 00 	mov    0x3b54(%rip),%rax        # 405010 <stdout@GLIBC_2.2.5>
  4014bc:	48 89 c7             	mov    %rax,%rdi
  4014bf:	e8 7c fc ff ff       	call   401140 <fflush@plt>
  4014c4:	90                   	nop
  4014c5:	c9                   	leave
  4014c6:	c3                   	ret

00000000004014c7 <banner>:
  4014c7:	f3 0f 1e fa          	endbr64
  4014cb:	55                   	push   %rbp
  4014cc:	48 89 e5             	mov    %rsp,%rbp
  4014cf:	48 8d 05 32 0b 00 00 	lea    0xb32(%rip),%rax        # 402008 <_IO_stdin_used+0x8>
  4014d6:	48 89 c2             	mov    %rax,%rdx
  4014d9:	48 8d 05 d6 0b 00 00 	lea    0xbd6(%rip),%rax        # 4020b6 <_IO_stdin_used+0xb6>
  4014e0:	48 89 c6             	mov    %rax,%rsi
  4014e3:	48 8d 05 a6 0c 00 00 	lea    0xca6(%rip),%rax        # 402190 <_IO_stdin_used+0x190>
  4014ea:	48 89 c7             	mov    %rax,%rdi
  4014ed:	b8 00 00 00 00       	mov    $0x0,%eax
  4014f2:	e8 f9 fb ff ff       	call   4010f0 <printf@plt>
  4014f7:	90                   	nop
  4014f8:	5d                   	pop    %rbp
  4014f9:	c3                   	ret

00000000004014fa <main>:
  4014fa:	f3 0f 1e fa          	endbr64
  4014fe:	55                   	push   %rbp
  4014ff:	48 89 e5             	mov    %rsp,%rbp
  401502:	48 83 ec 20          	sub    $0x20,%rsp
  401506:	e8 bc ff ff ff       	call   4014c7 <banner>
  40150b:	48 c7 45 e0 00 00 00 	movq   $0x0,-0x20(%rbp)
  401512:	00 
  401513:	48 c7 45 e8 00 00 00 	movq   $0x0,-0x18(%rbp)
  40151a:	00 
  40151b:	48 c7 45 f0 00 00 00 	movq   $0x0,-0x10(%rbp)
  401522:	00 
  401523:	48 c7 45 f8 00 00 00 	movq   $0x0,-0x8(%rbp)
  40152a:	00 
  40152b:	48 8b 05 de 3a 00 00 	mov    0x3ade(%rip),%rax        # 405010 <stdout@GLIBC_2.2.5>
  401532:	48 89 c7             	mov    %rax,%rdi
  401535:	e8 06 fc ff ff       	call   401140 <fflush@plt>
  40153a:	48 8d 05 97 25 00 00 	lea    0x2597(%rip),%rax        # 403ad8 <_IO_stdin_used+0x1ad8>
  401541:	48 89 c7             	mov    %rax,%rdi
  401544:	b8 00 00 00 00       	mov    $0x0,%eax
  401549:	e8 a2 fb ff ff       	call   4010f0 <printf@plt>
  40154e:	48 8b 05 bb 3a 00 00 	mov    0x3abb(%rip),%rax        # 405010 <stdout@GLIBC_2.2.5>
  401555:	48 89 c7             	mov    %rax,%rdi
  401558:	e8 e3 fb ff ff       	call   401140 <fflush@plt>
  40155d:	48 8d 45 e0          	lea    -0x20(%rbp),%rax
  401561:	ba 66 00 00 00       	mov    $0x66,%edx
  401566:	48 89 c6             	mov    %rax,%rsi
  401569:	bf 00 00 00 00       	mov    $0x0,%edi
  40156e:	e8 bd fb ff ff       	call   401130 <read@plt>
  401573:	48 8d 05 e7 25 00 00 	lea    0x25e7(%rip),%rax        # 403b61 <_IO_stdin_used+0x1b61>
  40157a:	48 89 c7             	mov    %rax,%rdi
  40157d:	e8 5e fb ff ff       	call   4010e0 <puts@plt>
  401582:	b8 00 00 00 00       	mov    $0x0,%eax
  401587:	c9                   	leave
  401588:	c3                   	ret

0000000000401589 <setup>:
  401589:	f3 0f 1e fa          	endbr64
  40158d:	55                   	push   %rbp
  40158e:	48 89 e5             	mov    %rsp,%rbp
  401591:	b8 00 00 00 00       	mov    $0x0,%eax
  401596:	e8 1d fd ff ff       	call   4012b8 <cls>
  40159b:	5a                   	pop    %rdx
  40159c:	c3                   	ret
  40159d:	5e                   	pop    %rsi
  40159e:	c3                   	ret
  40159f:	5f                   	pop    %rdi
  4015a0:	c3                   	ret
  4015a1:	48 8b 05 78 3a 00 00 	mov    0x3a78(%rip),%rax        # 405020 <stdin@GLIBC_2.2.5>
  4015a8:	b9 00 00 00 00       	mov    $0x0,%ecx
  4015ad:	ba 02 00 00 00       	mov    $0x2,%edx
  4015b2:	be 00 00 00 00       	mov    $0x0,%esi
  4015b7:	48 89 c7             	mov    %rax,%rdi
  4015ba:	e8 91 fb ff ff       	call   401150 <setvbuf@plt>
  4015bf:	48 8b 05 4a 3a 00 00 	mov    0x3a4a(%rip),%rax        # 405010 <stdout@GLIBC_2.2.5>
  4015c6:	b9 00 00 00 00       	mov    $0x0,%ecx
  4015cb:	ba 02 00 00 00       	mov    $0x2,%edx
  4015d0:	be 00 00 00 00       	mov    $0x0,%esi
  4015d5:	48 89 c7             	mov    %rax,%rdi
  4015d8:	e8 73 fb ff ff       	call   401150 <setvbuf@plt>
  4015dd:	bf 12 13 00 00       	mov    $0x1312,%edi
  4015e2:	e8 19 fb ff ff       	call   401100 <alarm@plt>
  4015e7:	90                   	nop
  4015e8:	5d                   	pop    %rbp
  4015e9:	c3                   	ret

Disassembly of section .fini:

00000000004015ec <_fini>:
  4015ec:	f3 0f 1e fa          	endbr64
  4015f0:	48 83 ec 08          	sub    $0x8,%rsp
  4015f4:	48 83 c4 08          	add    $0x8,%rsp
  4015f8:	c3                   	ret

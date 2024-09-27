
main:     file format elf64-x86-64


Disassembly of section .interp:

0000000000000318 <.interp>:
 318:	2f                   	(bad)
 319:	6c                   	ins    BYTE PTR es:[rdi],dx
 31a:	69 62 36 34 2f 6c 64 	imul   esp,DWORD PTR [rdx+0x36],0x646c2f34
 321:	2d 6c 69 6e 75       	sub    eax,0x756e696c
 326:	78 2d                	js     355 <__abi_tag-0x37>
 328:	78 38                	js     362 <__abi_tag-0x2a>
 32a:	36 2d 36 34 2e 73    	ss sub eax,0x732e3436
 330:	6f                   	outs   dx,DWORD PTR ds:[rsi]
 331:	2e 32 00             	cs xor al,BYTE PTR [rax]

Disassembly of section .note.gnu.property:

0000000000000338 <.note.gnu.property>:
 338:	04 00                	add    al,0x0
 33a:	00 00                	add    BYTE PTR [rax],al
 33c:	20 00                	and    BYTE PTR [rax],al
 33e:	00 00                	add    BYTE PTR [rax],al
 340:	05 00 00 00 47       	add    eax,0x47000000
 345:	4e 55                	rex.WRX push rbp
 347:	00 02                	add    BYTE PTR [rdx],al
 349:	00 00                	add    BYTE PTR [rax],al
 34b:	c0 04 00 00          	rol    BYTE PTR [rax+rax*1],0x0
 34f:	00 03                	add    BYTE PTR [rbx],al
 351:	00 00                	add    BYTE PTR [rax],al
 353:	00 00                	add    BYTE PTR [rax],al
 355:	00 00                	add    BYTE PTR [rax],al
 357:	00 02                	add    BYTE PTR [rdx],al
 359:	80 00 c0             	add    BYTE PTR [rax],0xc0
 35c:	04 00                	add    al,0x0
 35e:	00 00                	add    BYTE PTR [rax],al
 360:	01 00                	add    DWORD PTR [rax],eax
 362:	00 00                	add    BYTE PTR [rax],al
 364:	00 00                	add    BYTE PTR [rax],al
	...

Disassembly of section .note.gnu.build-id:

0000000000000368 <.note.gnu.build-id>:
 368:	04 00                	add    al,0x0
 36a:	00 00                	add    BYTE PTR [rax],al
 36c:	14 00                	adc    al,0x0
 36e:	00 00                	add    BYTE PTR [rax],al
 370:	03 00                	add    eax,DWORD PTR [rax]
 372:	00 00                	add    BYTE PTR [rax],al
 374:	47                   	rex.RXB
 375:	4e 55                	rex.WRX push rbp
 377:	00 a0 69 be 97 b1    	add    BYTE PTR [rax-0x4e684197],ah
 37d:	80 0e 1f             	or     BYTE PTR [rsi],0x1f
 380:	e9 c5 b9 a1 6f       	jmp    6fa1bd4a <_end+0x6fa17d32>
 385:	a8 a6                	test   al,0xa6
 387:	38 11                	cmp    BYTE PTR [rcx],dl
 389:	04 7e                	add    al,0x7e
 38b:	cd                   	.byte 0xcd

Disassembly of section .note.ABI-tag:

000000000000038c <__abi_tag>:
 38c:	04 00                	add    al,0x0
 38e:	00 00                	add    BYTE PTR [rax],al
 390:	10 00                	adc    BYTE PTR [rax],al
 392:	00 00                	add    BYTE PTR [rax],al
 394:	01 00                	add    DWORD PTR [rax],eax
 396:	00 00                	add    BYTE PTR [rax],al
 398:	47                   	rex.RXB
 399:	4e 55                	rex.WRX push rbp
 39b:	00 00                	add    BYTE PTR [rax],al
 39d:	00 00                	add    BYTE PTR [rax],al
 39f:	00 03                	add    BYTE PTR [rbx],al
 3a1:	00 00                	add    BYTE PTR [rax],al
 3a3:	00 02                	add    BYTE PTR [rdx],al
 3a5:	00 00                	add    BYTE PTR [rax],al
 3a7:	00 00                	add    BYTE PTR [rax],al
 3a9:	00 00                	add    BYTE PTR [rax],al
	...

Disassembly of section .gnu.hash:

00000000000003b0 <.gnu.hash>:
 3b0:	02 00                	add    al,BYTE PTR [rax]
 3b2:	00 00                	add    BYTE PTR [rax],al
 3b4:	06                   	(bad)
 3b5:	00 00                	add    BYTE PTR [rax],al
 3b7:	00 01                	add    BYTE PTR [rcx],al
 3b9:	00 00                	add    BYTE PTR [rax],al
 3bb:	00 06                	add    BYTE PTR [rsi],al
 3bd:	00 00                	add    BYTE PTR [rax],al
 3bf:	00 00                	add    BYTE PTR [rax],al
 3c1:	00 81 00 00 00 00    	add    BYTE PTR [rcx+0x0],al
 3c7:	00 06                	add    BYTE PTR [rsi],al
 3c9:	00 00                	add    BYTE PTR [rax],al
 3cb:	00 00                	add    BYTE PTR [rax],al
 3cd:	00 00                	add    BYTE PTR [rax],al
 3cf:	00 d1                	add    cl,dl
 3d1:	65 ce                	gs (bad)
 3d3:	6d                   	ins    DWORD PTR es:[rdi],dx

Disassembly of section .dynsym:

00000000000003d8 <.dynsym>:
	...
 3f0:	10 00                	adc    BYTE PTR [rax],al
 3f2:	00 00                	add    BYTE PTR [rax],al
 3f4:	12 00                	adc    al,BYTE PTR [rax]
	...
 406:	00 00                	add    BYTE PTR [rax],al
 408:	5e                   	pop    rsi
 409:	00 00                	add    BYTE PTR [rax],al
 40b:	00 20                	add    BYTE PTR [rax],ah
	...
 41d:	00 00                	add    BYTE PTR [rax],al
 41f:	00 22                	add    BYTE PTR [rdx],ah
 421:	00 00                	add    BYTE PTR [rax],al
 423:	00 12                	add    BYTE PTR [rdx],dl
	...
 435:	00 00                	add    BYTE PTR [rax],al
 437:	00 7a 00             	add    BYTE PTR [rdx+0x0],bh
 43a:	00 00                	add    BYTE PTR [rax],al
 43c:	20 00                	and    BYTE PTR [rax],al
	...
 44e:	00 00                	add    BYTE PTR [rax],al
 450:	89 00                	mov    DWORD PTR [rax],eax
 452:	00 00                	add    BYTE PTR [rax],al
 454:	20 00                	and    BYTE PTR [rax],al
	...
 466:	00 00                	add    BYTE PTR [rax],al
 468:	01 00                	add    DWORD PTR [rax],eax
 46a:	00 00                	add    BYTE PTR [rax],al
 46c:	22 00                	and    al,BYTE PTR [rax]
	...

Disassembly of section .dynstr:

0000000000000480 <.dynstr>:
 480:	00 5f 5f             	add    BYTE PTR [rdi+0x5f],bl
 483:	63 78 61             	movsxd edi,DWORD PTR [rax+0x61]
 486:	5f                   	pop    rdi
 487:	66 69 6e 61 6c 69    	imul   bp,WORD PTR [rsi+0x61],0x696c
 48d:	7a 65                	jp     4f4 <__abi_tag+0x168>
 48f:	00 5f 5f             	add    BYTE PTR [rdi+0x5f],bl
 492:	6c                   	ins    BYTE PTR es:[rdi],dx
 493:	69 62 63 5f 73 74 61 	imul   esp,DWORD PTR [rdx+0x63],0x6174735f
 49a:	72 74                	jb     510 <__abi_tag+0x184>
 49c:	5f                   	pop    rdi
 49d:	6d                   	ins    DWORD PTR es:[rdi],dx
 49e:	61                   	(bad)
 49f:	69 6e 00 5f 5f 73 74 	imul   ebp,DWORD PTR [rsi+0x0],0x74735f5f
 4a6:	61                   	(bad)
 4a7:	63 6b 5f             	movsxd ebp,DWORD PTR [rbx+0x5f]
 4aa:	63 68 6b             	movsxd ebp,DWORD PTR [rax+0x6b]
 4ad:	5f                   	pop    rdi
 4ae:	66 61                	data16 (bad)
 4b0:	69 6c 00 6c 69 62 63 	imul   ebp,DWORD PTR [rax+rax*1+0x6c],0x2e636269
 4b7:	2e 
 4b8:	73 6f                	jae    529 <__abi_tag+0x19d>
 4ba:	2e 36 00 47 4c       	cs ss add BYTE PTR [rdi+0x4c],al
 4bf:	49                   	rex.WB
 4c0:	42                   	rex.X
 4c1:	43 5f                	rex.XB pop r15
 4c3:	32 2e                	xor    ch,BYTE PTR [rsi]
 4c5:	32 2e                	xor    ch,BYTE PTR [rsi]
 4c7:	35 00 47 4c 49       	xor    eax,0x494c4700
 4cc:	42                   	rex.X
 4cd:	43 5f                	rex.XB pop r15
 4cf:	32 2e                	xor    ch,BYTE PTR [rsi]
 4d1:	34 00                	xor    al,0x0
 4d3:	47                   	rex.RXB
 4d4:	4c                   	rex.WR
 4d5:	49                   	rex.WB
 4d6:	42                   	rex.X
 4d7:	43 5f                	rex.XB pop r15
 4d9:	32 2e                	xor    ch,BYTE PTR [rsi]
 4db:	33 34 00             	xor    esi,DWORD PTR [rax+rax*1]
 4de:	5f                   	pop    rdi
 4df:	49 54                	rex.WB push r12
 4e1:	4d 5f                	rex.WRB pop r15
 4e3:	64 65 72 65          	fs gs jb 54c <__abi_tag+0x1c0>
 4e7:	67 69 73 74 65 72 54 	imul   esi,DWORD PTR [ebx+0x74],0x4d547265
 4ee:	4d 
 4ef:	43 6c                	rex.XB ins BYTE PTR es:[rdi],dx
 4f1:	6f                   	outs   dx,DWORD PTR ds:[rsi]
 4f2:	6e                   	outs   dx,BYTE PTR ds:[rsi]
 4f3:	65 54                	gs push rsp
 4f5:	61                   	(bad)
 4f6:	62                   	(bad)
 4f7:	6c                   	ins    BYTE PTR es:[rdi],dx
 4f8:	65 00 5f 5f          	add    BYTE PTR gs:[rdi+0x5f],bl
 4fc:	67 6d                	ins    DWORD PTR es:[edi],dx
 4fe:	6f                   	outs   dx,DWORD PTR ds:[rsi]
 4ff:	6e                   	outs   dx,BYTE PTR ds:[rsi]
 500:	5f                   	pop    rdi
 501:	73 74                	jae    577 <__abi_tag+0x1eb>
 503:	61                   	(bad)
 504:	72 74                	jb     57a <__abi_tag+0x1ee>
 506:	5f                   	pop    rdi
 507:	5f                   	pop    rdi
 508:	00 5f 49             	add    BYTE PTR [rdi+0x49],bl
 50b:	54                   	push   rsp
 50c:	4d 5f                	rex.WRB pop r15
 50e:	72 65                	jb     575 <__abi_tag+0x1e9>
 510:	67 69 73 74 65 72 54 	imul   esi,DWORD PTR [ebx+0x74],0x4d547265
 517:	4d 
 518:	43 6c                	rex.XB ins BYTE PTR es:[rdi],dx
 51a:	6f                   	outs   dx,DWORD PTR ds:[rsi]
 51b:	6e                   	outs   dx,BYTE PTR ds:[rsi]
 51c:	65 54                	gs push rsp
 51e:	61                   	(bad)
 51f:	62                   	.byte 0x62
 520:	6c                   	ins    BYTE PTR es:[rdi],dx
 521:	65                   	gs
	...

Disassembly of section .gnu.version:

0000000000000524 <.gnu.version>:
 524:	00 00                	add    BYTE PTR [rax],al
 526:	02 00                	add    al,BYTE PTR [rax]
 528:	01 00                	add    DWORD PTR [rax],eax
 52a:	03 00                	add    eax,DWORD PTR [rax]
 52c:	01 00                	add    DWORD PTR [rax],eax
 52e:	01 00                	add    DWORD PTR [rax],eax
 530:	04 00                	add    al,0x0

Disassembly of section .gnu.version_r:

0000000000000538 <.gnu.version_r>:
 538:	01 00                	add    DWORD PTR [rax],eax
 53a:	03 00                	add    eax,DWORD PTR [rax]
 53c:	33 00                	xor    eax,DWORD PTR [rax]
 53e:	00 00                	add    BYTE PTR [rax],al
 540:	10 00                	adc    BYTE PTR [rax],al
 542:	00 00                	add    BYTE PTR [rax],al
 544:	00 00                	add    BYTE PTR [rax],al
 546:	00 00                	add    BYTE PTR [rax],al
 548:	75 1a                	jne    564 <__abi_tag+0x1d8>
 54a:	69 09 00 00 04 00    	imul   ecx,DWORD PTR [rcx],0x40000
 550:	3d 00 00 00 10       	cmp    eax,0x10000000
 555:	00 00                	add    BYTE PTR [rax],al
 557:	00 14 69             	add    BYTE PTR [rcx+rbp*2],dl
 55a:	69 0d 00 00 03 00 49 	imul   ecx,DWORD PTR [rip+0x30000],0x49        # 30564 <_end+0x2c54c>
 561:	00 00 00 
 564:	10 00                	adc    BYTE PTR [rax],al
 566:	00 00                	add    BYTE PTR [rax],al
 568:	b4 91                	mov    ah,0x91
 56a:	96                   	xchg   esi,eax
 56b:	06                   	(bad)
 56c:	00 00                	add    BYTE PTR [rax],al
 56e:	02 00                	add    al,BYTE PTR [rax]
 570:	53                   	push   rbx
 571:	00 00                	add    BYTE PTR [rax],al
 573:	00 00                	add    BYTE PTR [rax],al
 575:	00 00                	add    BYTE PTR [rax],al
	...

Disassembly of section .rela.dyn:

0000000000000578 <.rela.dyn>:
 578:	b8 3d 00 00 00       	mov    eax,0x3d
 57d:	00 00                	add    BYTE PTR [rax],al
 57f:	00 08                	add    BYTE PTR [rax],cl
 581:	00 00                	add    BYTE PTR [rax],al
 583:	00 00                	add    BYTE PTR [rax],al
 585:	00 00                	add    BYTE PTR [rax],al
 587:	00 40 11             	add    BYTE PTR [rax+0x11],al
 58a:	00 00                	add    BYTE PTR [rax],al
 58c:	00 00                	add    BYTE PTR [rax],al
 58e:	00 00                	add    BYTE PTR [rax],al
 590:	c0 3d 00 00 00 00 00 	sar    BYTE PTR [rip+0x0],0x0        # 597 <__abi_tag+0x20b>
 597:	00 08                	add    BYTE PTR [rax],cl
	...
 5a1:	11 00                	adc    DWORD PTR [rax],eax
 5a3:	00 00                	add    BYTE PTR [rax],al
 5a5:	00 00                	add    BYTE PTR [rax],al
 5a7:	00 08                	add    BYTE PTR [rax],cl
 5a9:	40 00 00             	rex add BYTE PTR [rax],al
 5ac:	00 00                	add    BYTE PTR [rax],al
 5ae:	00 00                	add    BYTE PTR [rax],al
 5b0:	08 00                	or     BYTE PTR [rax],al
 5b2:	00 00                	add    BYTE PTR [rax],al
 5b4:	00 00                	add    BYTE PTR [rax],al
 5b6:	00 00                	add    BYTE PTR [rax],al
 5b8:	08 40 00             	or     BYTE PTR [rax+0x0],al
 5bb:	00 00                	add    BYTE PTR [rax],al
 5bd:	00 00                	add    BYTE PTR [rax],al
 5bf:	00 d8                	add    al,bl
 5c1:	3f                   	(bad)
 5c2:	00 00                	add    BYTE PTR [rax],al
 5c4:	00 00                	add    BYTE PTR [rax],al
 5c6:	00 00                	add    BYTE PTR [rax],al
 5c8:	06                   	(bad)
 5c9:	00 00                	add    BYTE PTR [rax],al
 5cb:	00 01                	add    BYTE PTR [rcx],al
	...
 5d5:	00 00                	add    BYTE PTR [rax],al
 5d7:	00 e0                	add    al,ah
 5d9:	3f                   	(bad)
 5da:	00 00                	add    BYTE PTR [rax],al
 5dc:	00 00                	add    BYTE PTR [rax],al
 5de:	00 00                	add    BYTE PTR [rax],al
 5e0:	06                   	(bad)
 5e1:	00 00                	add    BYTE PTR [rax],al
 5e3:	00 02                	add    BYTE PTR [rdx],al
	...
 5ed:	00 00                	add    BYTE PTR [rax],al
 5ef:	00 e8                	add    al,ch
 5f1:	3f                   	(bad)
 5f2:	00 00                	add    BYTE PTR [rax],al
 5f4:	00 00                	add    BYTE PTR [rax],al
 5f6:	00 00                	add    BYTE PTR [rax],al
 5f8:	06                   	(bad)
 5f9:	00 00                	add    BYTE PTR [rax],al
 5fb:	00 04 00             	add    BYTE PTR [rax+rax*1],al
	...
 606:	00 00                	add    BYTE PTR [rax],al
 608:	f0 3f                	lock (bad)
 60a:	00 00                	add    BYTE PTR [rax],al
 60c:	00 00                	add    BYTE PTR [rax],al
 60e:	00 00                	add    BYTE PTR [rax],al
 610:	06                   	(bad)
 611:	00 00                	add    BYTE PTR [rax],al
 613:	00 05 00 00 00 00    	add    BYTE PTR [rip+0x0],al        # 619 <__abi_tag+0x28d>
 619:	00 00                	add    BYTE PTR [rax],al
 61b:	00 00                	add    BYTE PTR [rax],al
 61d:	00 00                	add    BYTE PTR [rax],al
 61f:	00 f8                	add    al,bh
 621:	3f                   	(bad)
 622:	00 00                	add    BYTE PTR [rax],al
 624:	00 00                	add    BYTE PTR [rax],al
 626:	00 00                	add    BYTE PTR [rax],al
 628:	06                   	(bad)
 629:	00 00                	add    BYTE PTR [rax],al
 62b:	00 06                	add    BYTE PTR [rsi],al
	...

Disassembly of section .rela.plt:

0000000000000638 <.rela.plt>:
 638:	d0 3f                	sar    BYTE PTR [rdi],1
 63a:	00 00                	add    BYTE PTR [rax],al
 63c:	00 00                	add    BYTE PTR [rax],al
 63e:	00 00                	add    BYTE PTR [rax],al
 640:	07                   	(bad)
 641:	00 00                	add    BYTE PTR [rax],al
 643:	00 03                	add    BYTE PTR [rbx],al
	...

Disassembly of section .init:

0000000000001000 <_init>:
    1000:	f3 0f 1e fa          	endbr64
    1004:	48 83 ec 08          	sub    rsp,0x8
    1008:	48 8b 05 d9 2f 00 00 	mov    rax,QWORD PTR [rip+0x2fd9]        # 3fe8 <__gmon_start__@Base>
    100f:	48 85 c0             	test   rax,rax
    1012:	74 02                	je     1016 <_init+0x16>
    1014:	ff d0                	call   rax
    1016:	48 83 c4 08          	add    rsp,0x8
    101a:	c3                   	ret

Disassembly of section .plt:

0000000000001020 <.plt>:
    1020:	ff 35 9a 2f 00 00    	push   QWORD PTR [rip+0x2f9a]        # 3fc0 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026:	ff 25 9c 2f 00 00    	jmp    QWORD PTR [rip+0x2f9c]        # 3fc8 <_GLOBAL_OFFSET_TABLE_+0x10>
    102c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    1030:	f3 0f 1e fa          	endbr64
    1034:	68 00 00 00 00       	push   0x0
    1039:	e9 e2 ff ff ff       	jmp    1020 <_init+0x20>
    103e:	66 90                	xchg   ax,ax

Disassembly of section .plt.got:

0000000000001040 <__cxa_finalize@plt>:
    1040:	f3 0f 1e fa          	endbr64
    1044:	ff 25 ae 2f 00 00    	jmp    QWORD PTR [rip+0x2fae]        # 3ff8 <__cxa_finalize@GLIBC_2.2.5>
    104a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .plt.sec:

0000000000001050 <__stack_chk_fail@plt>:
    1050:	f3 0f 1e fa          	endbr64
    1054:	ff 25 76 2f 00 00    	jmp    QWORD PTR [rip+0x2f76]        # 3fd0 <__stack_chk_fail@GLIBC_2.4>
    105a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .text:

0000000000001060 <_start>:
    1060:	f3 0f 1e fa          	endbr64
    1064:	31 ed                	xor    ebp,ebp
    1066:	49 89 d1             	mov    r9,rdx
    1069:	5e                   	pop    rsi
    106a:	48 89 e2             	mov    rdx,rsp
    106d:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
    1071:	50                   	push   rax
    1072:	54                   	push   rsp
    1073:	45 31 c0             	xor    r8d,r8d
    1076:	31 c9                	xor    ecx,ecx
    1078:	48 8d 3d ca 00 00 00 	lea    rdi,[rip+0xca]        # 1149 <main>
    107f:	ff 15 53 2f 00 00    	call   QWORD PTR [rip+0x2f53]        # 3fd8 <__libc_start_main@GLIBC_2.34>
    1085:	f4                   	hlt
    1086:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    108d:	00 00 00 

0000000000001090 <deregister_tm_clones>:
    1090:	48 8d 3d 79 2f 00 00 	lea    rdi,[rip+0x2f79]        # 4010 <__TMC_END__>
    1097:	48 8d 05 72 2f 00 00 	lea    rax,[rip+0x2f72]        # 4010 <__TMC_END__>
    109e:	48 39 f8             	cmp    rax,rdi
    10a1:	74 15                	je     10b8 <deregister_tm_clones+0x28>
    10a3:	48 8b 05 36 2f 00 00 	mov    rax,QWORD PTR [rip+0x2f36]        # 3fe0 <_ITM_deregisterTMCloneTable@Base>
    10aa:	48 85 c0             	test   rax,rax
    10ad:	74 09                	je     10b8 <deregister_tm_clones+0x28>
    10af:	ff e0                	jmp    rax
    10b1:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    10b8:	c3                   	ret
    10b9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

00000000000010c0 <register_tm_clones>:
    10c0:	48 8d 3d 49 2f 00 00 	lea    rdi,[rip+0x2f49]        # 4010 <__TMC_END__>
    10c7:	48 8d 35 42 2f 00 00 	lea    rsi,[rip+0x2f42]        # 4010 <__TMC_END__>
    10ce:	48 29 fe             	sub    rsi,rdi
    10d1:	48 89 f0             	mov    rax,rsi
    10d4:	48 c1 ee 3f          	shr    rsi,0x3f
    10d8:	48 c1 f8 03          	sar    rax,0x3
    10dc:	48 01 c6             	add    rsi,rax
    10df:	48 d1 fe             	sar    rsi,1
    10e2:	74 14                	je     10f8 <register_tm_clones+0x38>
    10e4:	48 8b 05 05 2f 00 00 	mov    rax,QWORD PTR [rip+0x2f05]        # 3ff0 <_ITM_registerTMCloneTable@Base>
    10eb:	48 85 c0             	test   rax,rax
    10ee:	74 08                	je     10f8 <register_tm_clones+0x38>
    10f0:	ff e0                	jmp    rax
    10f2:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    10f8:	c3                   	ret
    10f9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000001100 <__do_global_dtors_aux>:
    1100:	f3 0f 1e fa          	endbr64
    1104:	80 3d 05 2f 00 00 00 	cmp    BYTE PTR [rip+0x2f05],0x0        # 4010 <__TMC_END__>
    110b:	75 2b                	jne    1138 <__do_global_dtors_aux+0x38>
    110d:	55                   	push   rbp
    110e:	48 83 3d e2 2e 00 00 	cmp    QWORD PTR [rip+0x2ee2],0x0        # 3ff8 <__cxa_finalize@GLIBC_2.2.5>
    1115:	00 
    1116:	48 89 e5             	mov    rbp,rsp
    1119:	74 0c                	je     1127 <__do_global_dtors_aux+0x27>
    111b:	48 8b 3d e6 2e 00 00 	mov    rdi,QWORD PTR [rip+0x2ee6]        # 4008 <__dso_handle>
    1122:	e8 19 ff ff ff       	call   1040 <__cxa_finalize@plt>
    1127:	e8 64 ff ff ff       	call   1090 <deregister_tm_clones>
    112c:	c6 05 dd 2e 00 00 01 	mov    BYTE PTR [rip+0x2edd],0x1        # 4010 <__TMC_END__>
    1133:	5d                   	pop    rbp
    1134:	c3                   	ret
    1135:	0f 1f 00             	nop    DWORD PTR [rax]
    1138:	c3                   	ret
    1139:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000001140 <frame_dummy>:
    1140:	f3 0f 1e fa          	endbr64
    1144:	e9 77 ff ff ff       	jmp    10c0 <register_tm_clones>

0000000000001149 <main>:
    1149:	f3 0f 1e fa          	endbr64
    114d:	55                   	push   rbp
    114e:	48 89 e5             	mov    rbp,rsp
    1151:	48 83 ec 50          	sub    rsp,0x50
    1155:	89 7d bc             	mov    DWORD PTR [rbp-0x44],edi
    1158:	48 89 75 b0          	mov    QWORD PTR [rbp-0x50],rsi
    115c:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    1163:	00 00 
    1165:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
    1169:	31 c0                	xor    eax,eax
    116b:	c7 45 cc 02 00 00 00 	mov    DWORD PTR [rbp-0x34],0x2
    1172:	c6 45 cb 42          	mov    BYTE PTR [rbp-0x35],0x42
    1176:	48 c7 45 d0 41 42 43 	mov    QWORD PTR [rbp-0x30],0x434241
    117d:	00 
    117e:	48 c7 45 d8 00 00 00 	mov    QWORD PTR [rbp-0x28],0x0
    1185:	00 
    1186:	48 c7 45 e0 00 00 00 	mov    QWORD PTR [rbp-0x20],0x0
    118d:	00 
    118e:	48 c7 45 e8 00 00 00 	mov    QWORD PTR [rbp-0x18],0x0
    1195:	00 
    1196:	b8 00 00 00 00       	mov    eax,0x0
    119b:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
    119f:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    11a6:	00 00 
    11a8:	74 05                	je     11af <main+0x66>
    11aa:	e8 a1 fe ff ff       	call   1050 <__stack_chk_fail@plt>
    11af:	c9                   	leave
    11b0:	c3                   	ret

Disassembly of section .fini:

00000000000011b4 <_fini>:
    11b4:	f3 0f 1e fa          	endbr64
    11b8:	48 83 ec 08          	sub    rsp,0x8
    11bc:	48 83 c4 08          	add    rsp,0x8
    11c0:	c3                   	ret

Disassembly of section .rodata:

0000000000002000 <_IO_stdin_used>:
    2000:	01 00                	add    DWORD PTR [rax],eax
    2002:	02 00                	add    al,BYTE PTR [rax]

Disassembly of section .eh_frame_hdr:

0000000000002004 <__GNU_EH_FRAME_HDR>:
    2004:	01 1b                	add    DWORD PTR [rbx],ebx
    2006:	03 3b                	add    edi,DWORD PTR [rbx]
    2008:	30 00                	xor    BYTE PTR [rax],al
    200a:	00 00                	add    BYTE PTR [rax],al
    200c:	05 00 00 00 1c       	add    eax,0x1c000000
    2011:	f0 ff                	lock (bad)
    2013:	ff 64 00 00          	jmp    QWORD PTR [rax+rax*1+0x0]
    2017:	00 3c f0             	add    BYTE PTR [rax+rsi*8],bh
    201a:	ff                   	(bad)
    201b:	ff 8c 00 00 00 4c f0 	dec    DWORD PTR [rax+rax*1-0xfb40000]
    2022:	ff                   	(bad)
    2023:	ff a4 00 00 00 5c f0 	jmp    QWORD PTR [rax+rax*1-0xfa40000]
    202a:	ff                   	(bad)
    202b:	ff 4c 00 00          	dec    DWORD PTR [rax+rax*1+0x0]
    202f:	00 45 f1             	add    BYTE PTR [rbp-0xf],al
    2032:	ff                   	(bad)
    2033:	ff                   	(bad)
    2034:	bc                   	.byte 0xbc
    2035:	00 00                	add    BYTE PTR [rax],al
	...

Disassembly of section .eh_frame:

0000000000002038 <__FRAME_END__-0xa8>:
    2038:	14 00                	adc    al,0x0
    203a:	00 00                	add    BYTE PTR [rax],al
    203c:	00 00                	add    BYTE PTR [rax],al
    203e:	00 00                	add    BYTE PTR [rax],al
    2040:	01 7a 52             	add    DWORD PTR [rdx+0x52],edi
    2043:	00 01                	add    BYTE PTR [rcx],al
    2045:	78 10                	js     2057 <__GNU_EH_FRAME_HDR+0x53>
    2047:	01 1b                	add    DWORD PTR [rbx],ebx
    2049:	0c 07                	or     al,0x7
    204b:	08 90 01 00 00 14    	or     BYTE PTR [rax+0x14000001],dl
    2051:	00 00                	add    BYTE PTR [rax],al
    2053:	00 1c 00             	add    BYTE PTR [rax+rax*1],bl
    2056:	00 00                	add    BYTE PTR [rax],al
    2058:	08 f0                	or     al,dh
    205a:	ff                   	(bad)
    205b:	ff 26                	jmp    QWORD PTR [rsi]
    205d:	00 00                	add    BYTE PTR [rax],al
    205f:	00 00                	add    BYTE PTR [rax],al
    2061:	44 07                	rex.R (bad)
    2063:	10 00                	adc    BYTE PTR [rax],al
    2065:	00 00                	add    BYTE PTR [rax],al
    2067:	00 24 00             	add    BYTE PTR [rax+rax*1],ah
    206a:	00 00                	add    BYTE PTR [rax],al
    206c:	34 00                	xor    al,0x0
    206e:	00 00                	add    BYTE PTR [rax],al
    2070:	b0 ef                	mov    al,0xef
    2072:	ff                   	(bad)
    2073:	ff 20                	jmp    QWORD PTR [rax]
    2075:	00 00                	add    BYTE PTR [rax],al
    2077:	00 00                	add    BYTE PTR [rax],al
    2079:	0e                   	(bad)
    207a:	10 46 0e             	adc    BYTE PTR [rsi+0xe],al
    207d:	18 4a 0f             	sbb    BYTE PTR [rdx+0xf],cl
    2080:	0b 77 08             	or     esi,DWORD PTR [rdi+0x8]
    2083:	80 00 3f             	add    BYTE PTR [rax],0x3f
    2086:	1a 39                	sbb    bh,BYTE PTR [rcx]
    2088:	2a 33                	sub    dh,BYTE PTR [rbx]
    208a:	24 22                	and    al,0x22
    208c:	00 00                	add    BYTE PTR [rax],al
    208e:	00 00                	add    BYTE PTR [rax],al
    2090:	14 00                	adc    al,0x0
    2092:	00 00                	add    BYTE PTR [rax],al
    2094:	5c                   	pop    rsp
    2095:	00 00                	add    BYTE PTR [rax],al
    2097:	00 a8 ef ff ff 10    	add    BYTE PTR [rax+0x10ffffef],ch
	...
    20a5:	00 00                	add    BYTE PTR [rax],al
    20a7:	00 14 00             	add    BYTE PTR [rax+rax*1],dl
    20aa:	00 00                	add    BYTE PTR [rax],al
    20ac:	74 00                	je     20ae <__GNU_EH_FRAME_HDR+0xaa>
    20ae:	00 00                	add    BYTE PTR [rax],al
    20b0:	a0 ef ff ff 10 00 00 	movabs al,ds:0x10ffffef
    20b7:	00 00 
    20b9:	00 00                	add    BYTE PTR [rax],al
    20bb:	00 00                	add    BYTE PTR [rax],al
    20bd:	00 00                	add    BYTE PTR [rax],al
    20bf:	00 1c 00             	add    BYTE PTR [rax+rax*1],bl
    20c2:	00 00                	add    BYTE PTR [rax],al
    20c4:	8c 00                	mov    WORD PTR [rax],es
    20c6:	00 00                	add    BYTE PTR [rax],al
    20c8:	81 f0 ff ff 68 00    	xor    eax,0x68ffff
    20ce:	00 00                	add    BYTE PTR [rax],al
    20d0:	00 45 0e             	add    BYTE PTR [rbp+0xe],al
    20d3:	10 86 02 43 0d 06    	adc    BYTE PTR [rsi+0x60d4302],al
    20d9:	02 5f 0c             	add    bl,BYTE PTR [rdi+0xc]
    20dc:	07                   	(bad)
    20dd:	08 00                	or     BYTE PTR [rax],al
	...

00000000000020e0 <__FRAME_END__>:
    20e0:	00 00                	add    BYTE PTR [rax],al
	...

Disassembly of section .init_array:

0000000000003db8 <__frame_dummy_init_array_entry>:
    3db8:	40 11 00             	rex adc DWORD PTR [rax],eax
    3dbb:	00 00                	add    BYTE PTR [rax],al
    3dbd:	00 00                	add    BYTE PTR [rax],al
	...

Disassembly of section .fini_array:

0000000000003dc0 <__do_global_dtors_aux_fini_array_entry>:
    3dc0:	00 11                	add    BYTE PTR [rcx],dl
    3dc2:	00 00                	add    BYTE PTR [rax],al
    3dc4:	00 00                	add    BYTE PTR [rax],al
	...

Disassembly of section .dynamic:

0000000000003dc8 <_DYNAMIC>:
    3dc8:	01 00                	add    DWORD PTR [rax],eax
    3dca:	00 00                	add    BYTE PTR [rax],al
    3dcc:	00 00                	add    BYTE PTR [rax],al
    3dce:	00 00                	add    BYTE PTR [rax],al
    3dd0:	33 00                	xor    eax,DWORD PTR [rax]
    3dd2:	00 00                	add    BYTE PTR [rax],al
    3dd4:	00 00                	add    BYTE PTR [rax],al
    3dd6:	00 00                	add    BYTE PTR [rax],al
    3dd8:	0c 00                	or     al,0x0
    3dda:	00 00                	add    BYTE PTR [rax],al
    3ddc:	00 00                	add    BYTE PTR [rax],al
    3dde:	00 00                	add    BYTE PTR [rax],al
    3de0:	00 10                	add    BYTE PTR [rax],dl
    3de2:	00 00                	add    BYTE PTR [rax],al
    3de4:	00 00                	add    BYTE PTR [rax],al
    3de6:	00 00                	add    BYTE PTR [rax],al
    3de8:	0d 00 00 00 00       	or     eax,0x0
    3ded:	00 00                	add    BYTE PTR [rax],al
    3def:	00 b4 11 00 00 00 00 	add    BYTE PTR [rcx+rdx*1+0x0],dh
    3df6:	00 00                	add    BYTE PTR [rax],al
    3df8:	19 00                	sbb    DWORD PTR [rax],eax
    3dfa:	00 00                	add    BYTE PTR [rax],al
    3dfc:	00 00                	add    BYTE PTR [rax],al
    3dfe:	00 00                	add    BYTE PTR [rax],al
    3e00:	b8 3d 00 00 00       	mov    eax,0x3d
    3e05:	00 00                	add    BYTE PTR [rax],al
    3e07:	00 1b                	add    BYTE PTR [rbx],bl
    3e09:	00 00                	add    BYTE PTR [rax],al
    3e0b:	00 00                	add    BYTE PTR [rax],al
    3e0d:	00 00                	add    BYTE PTR [rax],al
    3e0f:	00 08                	add    BYTE PTR [rax],cl
    3e11:	00 00                	add    BYTE PTR [rax],al
    3e13:	00 00                	add    BYTE PTR [rax],al
    3e15:	00 00                	add    BYTE PTR [rax],al
    3e17:	00 1a                	add    BYTE PTR [rdx],bl
    3e19:	00 00                	add    BYTE PTR [rax],al
    3e1b:	00 00                	add    BYTE PTR [rax],al
    3e1d:	00 00                	add    BYTE PTR [rax],al
    3e1f:	00 c0                	add    al,al
    3e21:	3d 00 00 00 00       	cmp    eax,0x0
    3e26:	00 00                	add    BYTE PTR [rax],al
    3e28:	1c 00                	sbb    al,0x0
    3e2a:	00 00                	add    BYTE PTR [rax],al
    3e2c:	00 00                	add    BYTE PTR [rax],al
    3e2e:	00 00                	add    BYTE PTR [rax],al
    3e30:	08 00                	or     BYTE PTR [rax],al
    3e32:	00 00                	add    BYTE PTR [rax],al
    3e34:	00 00                	add    BYTE PTR [rax],al
    3e36:	00 00                	add    BYTE PTR [rax],al
    3e38:	f5                   	cmc
    3e39:	fe                   	(bad)
    3e3a:	ff 6f 00             	jmp    FWORD PTR [rdi+0x0]
    3e3d:	00 00                	add    BYTE PTR [rax],al
    3e3f:	00 b0 03 00 00 00    	add    BYTE PTR [rax+0x3],dh
    3e45:	00 00                	add    BYTE PTR [rax],al
    3e47:	00 05 00 00 00 00    	add    BYTE PTR [rip+0x0],al        # 3e4d <_DYNAMIC+0x85>
    3e4d:	00 00                	add    BYTE PTR [rax],al
    3e4f:	00 80 04 00 00 00    	add    BYTE PTR [rax+0x4],al
    3e55:	00 00                	add    BYTE PTR [rax],al
    3e57:	00 06                	add    BYTE PTR [rsi],al
    3e59:	00 00                	add    BYTE PTR [rax],al
    3e5b:	00 00                	add    BYTE PTR [rax],al
    3e5d:	00 00                	add    BYTE PTR [rax],al
    3e5f:	00 d8                	add    al,bl
    3e61:	03 00                	add    eax,DWORD PTR [rax]
    3e63:	00 00                	add    BYTE PTR [rax],al
    3e65:	00 00                	add    BYTE PTR [rax],al
    3e67:	00 0a                	add    BYTE PTR [rdx],cl
    3e69:	00 00                	add    BYTE PTR [rax],al
    3e6b:	00 00                	add    BYTE PTR [rax],al
    3e6d:	00 00                	add    BYTE PTR [rax],al
    3e6f:	00 a3 00 00 00 00    	add    BYTE PTR [rbx+0x0],ah
    3e75:	00 00                	add    BYTE PTR [rax],al
    3e77:	00 0b                	add    BYTE PTR [rbx],cl
    3e79:	00 00                	add    BYTE PTR [rax],al
    3e7b:	00 00                	add    BYTE PTR [rax],al
    3e7d:	00 00                	add    BYTE PTR [rax],al
    3e7f:	00 18                	add    BYTE PTR [rax],bl
    3e81:	00 00                	add    BYTE PTR [rax],al
    3e83:	00 00                	add    BYTE PTR [rax],al
    3e85:	00 00                	add    BYTE PTR [rax],al
    3e87:	00 15 00 00 00 00    	add    BYTE PTR [rip+0x0],dl        # 3e8d <_DYNAMIC+0xc5>
	...
    3e95:	00 00                	add    BYTE PTR [rax],al
    3e97:	00 03                	add    BYTE PTR [rbx],al
    3e99:	00 00                	add    BYTE PTR [rax],al
    3e9b:	00 00                	add    BYTE PTR [rax],al
    3e9d:	00 00                	add    BYTE PTR [rax],al
    3e9f:	00 b8 3f 00 00 00    	add    BYTE PTR [rax+0x3f],bh
    3ea5:	00 00                	add    BYTE PTR [rax],al
    3ea7:	00 02                	add    BYTE PTR [rdx],al
    3ea9:	00 00                	add    BYTE PTR [rax],al
    3eab:	00 00                	add    BYTE PTR [rax],al
    3ead:	00 00                	add    BYTE PTR [rax],al
    3eaf:	00 18                	add    BYTE PTR [rax],bl
    3eb1:	00 00                	add    BYTE PTR [rax],al
    3eb3:	00 00                	add    BYTE PTR [rax],al
    3eb5:	00 00                	add    BYTE PTR [rax],al
    3eb7:	00 14 00             	add    BYTE PTR [rax+rax*1],dl
    3eba:	00 00                	add    BYTE PTR [rax],al
    3ebc:	00 00                	add    BYTE PTR [rax],al
    3ebe:	00 00                	add    BYTE PTR [rax],al
    3ec0:	07                   	(bad)
    3ec1:	00 00                	add    BYTE PTR [rax],al
    3ec3:	00 00                	add    BYTE PTR [rax],al
    3ec5:	00 00                	add    BYTE PTR [rax],al
    3ec7:	00 17                	add    BYTE PTR [rdi],dl
    3ec9:	00 00                	add    BYTE PTR [rax],al
    3ecb:	00 00                	add    BYTE PTR [rax],al
    3ecd:	00 00                	add    BYTE PTR [rax],al
    3ecf:	00 38                	add    BYTE PTR [rax],bh
    3ed1:	06                   	(bad)
    3ed2:	00 00                	add    BYTE PTR [rax],al
    3ed4:	00 00                	add    BYTE PTR [rax],al
    3ed6:	00 00                	add    BYTE PTR [rax],al
    3ed8:	07                   	(bad)
    3ed9:	00 00                	add    BYTE PTR [rax],al
    3edb:	00 00                	add    BYTE PTR [rax],al
    3edd:	00 00                	add    BYTE PTR [rax],al
    3edf:	00 78 05             	add    BYTE PTR [rax+0x5],bh
    3ee2:	00 00                	add    BYTE PTR [rax],al
    3ee4:	00 00                	add    BYTE PTR [rax],al
    3ee6:	00 00                	add    BYTE PTR [rax],al
    3ee8:	08 00                	or     BYTE PTR [rax],al
    3eea:	00 00                	add    BYTE PTR [rax],al
    3eec:	00 00                	add    BYTE PTR [rax],al
    3eee:	00 00                	add    BYTE PTR [rax],al
    3ef0:	c0 00 00             	rol    BYTE PTR [rax],0x0
    3ef3:	00 00                	add    BYTE PTR [rax],al
    3ef5:	00 00                	add    BYTE PTR [rax],al
    3ef7:	00 09                	add    BYTE PTR [rcx],cl
    3ef9:	00 00                	add    BYTE PTR [rax],al
    3efb:	00 00                	add    BYTE PTR [rax],al
    3efd:	00 00                	add    BYTE PTR [rax],al
    3eff:	00 18                	add    BYTE PTR [rax],bl
    3f01:	00 00                	add    BYTE PTR [rax],al
    3f03:	00 00                	add    BYTE PTR [rax],al
    3f05:	00 00                	add    BYTE PTR [rax],al
    3f07:	00 1e                	add    BYTE PTR [rsi],bl
    3f09:	00 00                	add    BYTE PTR [rax],al
    3f0b:	00 00                	add    BYTE PTR [rax],al
    3f0d:	00 00                	add    BYTE PTR [rax],al
    3f0f:	00 08                	add    BYTE PTR [rax],cl
    3f11:	00 00                	add    BYTE PTR [rax],al
    3f13:	00 00                	add    BYTE PTR [rax],al
    3f15:	00 00                	add    BYTE PTR [rax],al
    3f17:	00 fb                	add    bl,bh
    3f19:	ff                   	(bad)
    3f1a:	ff 6f 00             	jmp    FWORD PTR [rdi+0x0]
    3f1d:	00 00                	add    BYTE PTR [rax],al
    3f1f:	00 01                	add    BYTE PTR [rcx],al
    3f21:	00 00                	add    BYTE PTR [rax],al
    3f23:	08 00                	or     BYTE PTR [rax],al
    3f25:	00 00                	add    BYTE PTR [rax],al
    3f27:	00 fe                	add    dh,bh
    3f29:	ff                   	(bad)
    3f2a:	ff 6f 00             	jmp    FWORD PTR [rdi+0x0]
    3f2d:	00 00                	add    BYTE PTR [rax],al
    3f2f:	00 38                	add    BYTE PTR [rax],bh
    3f31:	05 00 00 00 00       	add    eax,0x0
    3f36:	00 00                	add    BYTE PTR [rax],al
    3f38:	ff                   	(bad)
    3f39:	ff                   	(bad)
    3f3a:	ff 6f 00             	jmp    FWORD PTR [rdi+0x0]
    3f3d:	00 00                	add    BYTE PTR [rax],al
    3f3f:	00 01                	add    BYTE PTR [rcx],al
    3f41:	00 00                	add    BYTE PTR [rax],al
    3f43:	00 00                	add    BYTE PTR [rax],al
    3f45:	00 00                	add    BYTE PTR [rax],al
    3f47:	00 f0                	add    al,dh
    3f49:	ff                   	(bad)
    3f4a:	ff 6f 00             	jmp    FWORD PTR [rdi+0x0]
    3f4d:	00 00                	add    BYTE PTR [rax],al
    3f4f:	00 24 05 00 00 00 00 	add    BYTE PTR [rax*1+0x0],ah
    3f56:	00 00                	add    BYTE PTR [rax],al
    3f58:	f9                   	stc
    3f59:	ff                   	(bad)
    3f5a:	ff 6f 00             	jmp    FWORD PTR [rdi+0x0]
    3f5d:	00 00                	add    BYTE PTR [rax],al
    3f5f:	00 03                	add    BYTE PTR [rbx],al
	...

Disassembly of section .got:

0000000000003fb8 <_GLOBAL_OFFSET_TABLE_>:
    3fb8:	c8 3d 00 00          	enter  0x3d,0x0
	...
    3fd0:	30 10                	xor    BYTE PTR [rax],dl
	...

Disassembly of section .data:

0000000000004000 <__data_start>:
	...

0000000000004008 <__dso_handle>:
    4008:	08 40 00             	or     BYTE PTR [rax+0x0],al
    400b:	00 00                	add    BYTE PTR [rax],al
    400d:	00 00                	add    BYTE PTR [rax],al
	...

Disassembly of section .comment:

0000000000000000 <.comment>:
   0:	47                   	rex.RXB
   1:	43                   	rex.XB
   2:	43 3a 20             	rex.XB cmp spl,BYTE PTR [r8]
   5:	28 55 62             	sub    BYTE PTR [rbp+0x62],dl
   8:	75 6e                	jne    78 <__abi_tag-0x314>
   a:	74 75                	je     81 <__abi_tag-0x30b>
   c:	20 31                	and    BYTE PTR [rcx],dh
   e:	33 2e                	xor    ebp,DWORD PTR [rsi]
  10:	32 2e                	xor    ch,BYTE PTR [rsi]
  12:	30 2d 34 75 62 75    	xor    BYTE PTR [rip+0x75627534],ch        # 7562754c <_end+0x75623534>
  18:	6e                   	outs   dx,BYTE PTR ds:[rsi]
  19:	74 75                	je     90 <__abi_tag-0x2fc>
  1b:	33 29                	xor    ebp,DWORD PTR [rcx]
  1d:	20 31                	and    BYTE PTR [rcx],dh
  1f:	33 2e                	xor    ebp,DWORD PTR [rsi]
  21:	32 2e                	xor    ch,BYTE PTR [rsi]
  23:	30 00                	xor    BYTE PTR [rax],al

Disassembly of section .debug_aranges:

0000000000000000 <.debug_aranges>:
   0:	2c 00                	sub    al,0x0
   2:	00 00                	add    BYTE PTR [rax],al
   4:	02 00                	add    al,BYTE PTR [rax]
   6:	00 00                	add    BYTE PTR [rax],al
   8:	00 00                	add    BYTE PTR [rax],al
   a:	08 00                	or     BYTE PTR [rax],al
   c:	00 00                	add    BYTE PTR [rax],al
   e:	00 00                	add    BYTE PTR [rax],al
  10:	49 11 00             	adc    QWORD PTR [r8],rax
  13:	00 00                	add    BYTE PTR [rax],al
  15:	00 00                	add    BYTE PTR [rax],al
  17:	00 68 00             	add    BYTE PTR [rax+0x0],ch
	...

Disassembly of section .debug_info:

0000000000000000 <.debug_info>:
   0:	e5 00                	in     eax,0x0
   2:	00 00                	add    BYTE PTR [rax],al
   4:	05 00 01 08 00       	add    eax,0x80100
   9:	00 00                	add    BYTE PTR [rax],al
   b:	00 05 50 00 00 00    	add    BYTE PTR [rip+0x50],al        # 61 <__abi_tag-0x32b>
  11:	1d 2f 00 00 00       	sbb    eax,0x2f
  16:	00 00                	add    BYTE PTR [rax],al
  18:	00 00                	add    BYTE PTR [rax],al
  1a:	49 11 00             	adc    QWORD PTR [r8],rax
  1d:	00 00                	add    BYTE PTR [rax],al
  1f:	00 00                	add    BYTE PTR [rax],al
  21:	00 68 00             	add    BYTE PTR [rax+0x0],ch
	...
  2c:	00 00                	add    BYTE PTR [rax],al
  2e:	01 08                	add    DWORD PTR [rax],ecx
  30:	07                   	(bad)
  31:	13 00                	adc    eax,DWORD PTR [rax]
  33:	00 00                	add    BYTE PTR [rax],al
  35:	01 04 07             	add    DWORD PTR [rdi+rax*1],eax
  38:	18 00                	sbb    BYTE PTR [rax],al
  3a:	00 00                	add    BYTE PTR [rax],al
  3c:	01 01                	add    DWORD PTR [rcx],eax
  3e:	08 25 00 00 00 01    	or     BYTE PTR [rip+0x1000000],ah        # 1000044 <_end+0xffc02c>
  44:	02 07                	add    al,BYTE PTR [rdi]
  46:	00 00                	add    BYTE PTR [rax],al
  48:	00 00                	add    BYTE PTR [rax],al
  4a:	01 01                	add    DWORD PTR [rcx],eax
  4c:	06                   	(bad)
  4d:	27                   	(bad)
  4e:	00 00                	add    BYTE PTR [rax],al
  50:	00 01                	add    BYTE PTR [rcx],al
  52:	02 05 46 00 00 00    	add    al,BYTE PTR [rip+0x46]        # 9e <__abi_tag-0x2ee>
  58:	06                   	(bad)
  59:	04 05                	add    al,0x5
  5b:	69 6e 74 00 01 08 05 	imul   ebp,DWORD PTR [rsi+0x74],0x5080100
  62:	38 00                	cmp    BYTE PTR [rax],al
  64:	00 00                	add    BYTE PTR [rax],al
  66:	03 6b 00             	add    ebp,DWORD PTR [rbx+0x0]
  69:	00 00                	add    BYTE PTR [rax],al
  6b:	01 01                	add    DWORD PTR [rcx],eax
  6d:	06                   	(bad)
  6e:	2e 00 00             	cs add BYTE PTR [rax],al
  71:	00 07                	add    BYTE PTR [rdi],al
  73:	33 00                	xor    eax,DWORD PTR [rax]
  75:	00 00                	add    BYTE PTR [rax],al
  77:	01 03                	add    DWORD PTR [rbx],eax
  79:	05 58 00 00 00       	add    eax,0x58
  7e:	49 11 00             	adc    QWORD PTR [r8],rax
  81:	00 00                	add    BYTE PTR [rax],al
  83:	00 00                	add    BYTE PTR [rax],al
  85:	00 68 00             	add    BYTE PTR [rax+0x0],ch
  88:	00 00                	add    BYTE PTR [rax],al
  8a:	00 00                	add    BYTE PTR [rax],al
  8c:	00 00                	add    BYTE PTR [rax],al
  8e:	01 9c d7 00 00 00 04 	add    DWORD PTR [rdi+rdx*8+0x4000000],ebx
  95:	41 00 00             	add    BYTE PTR [r8],al
  98:	00 0e                	add    BYTE PTR [rsi],cl
  9a:	58                   	pop    rax
  9b:	00 00                	add    BYTE PTR [rax],al
  9d:	00 03                	add    BYTE PTR [rbx],al
  9f:	91                   	xchg   ecx,eax
  a0:	ac                   	lods   al,BYTE PTR ds:[rsi]
  a1:	7f 04                	jg     a7 <__abi_tag-0x2e5>
  a3:	de 00                	fiadd  WORD PTR [rax]
  a5:	00 00                	add    BYTE PTR [rax],al
  a7:	1a d7                	sbb    dl,bh
  a9:	00 00                	add    BYTE PTR [rax],al
  ab:	00 03                	add    BYTE PTR [rbx],al
  ad:	91                   	xchg   ecx,eax
  ae:	a0 7f 02 61 00 05 06 	movabs al,ds:0x5806050061027f
  b5:	58 00 
  b7:	00 00                	add    BYTE PTR [rax],al
  b9:	03 91 bc 7f 02 62    	add    edx,DWORD PTR [rcx+0x62027fbc]
  bf:	00 06                	add    BYTE PTR [rsi],al
  c1:	07                   	(bad)
  c2:	6b 00 00             	imul   eax,DWORD PTR [rax],0x0
  c5:	00 03                	add    BYTE PTR [rbx],al
  c7:	91                   	xchg   ecx,eax
  c8:	bb 7f 02 63 00       	mov    ebx,0x63027f
  cd:	07                   	(bad)
  ce:	07                   	(bad)
  cf:	dc 00                	fadd   QWORD PTR [rax]
  d1:	00 00                	add    BYTE PTR [rax],al
  d3:	02 91 40 00 03 66    	add    dl,BYTE PTR [rcx+0x66030040]
  d9:	00 00                	add    BYTE PTR [rax],al
  db:	00 08                	add    BYTE PTR [rax],cl
  dd:	6b 00 00             	imul   eax,DWORD PTR [rax],0x0
  e0:	00 09                	add    BYTE PTR [rcx],cl
  e2:	2e 00 00             	cs add BYTE PTR [rax],al
  e5:	00 1f                	add    BYTE PTR [rdi],bl
	...

Disassembly of section .debug_abbrev:

0000000000000000 <.debug_abbrev>:
   0:	01 24 00             	add    DWORD PTR [rax+rax*1],esp
   3:	0b 0b                	or     ecx,DWORD PTR [rbx]
   5:	3e 0b 03             	ds or  eax,DWORD PTR [rbx]
   8:	0e                   	(bad)
   9:	00 00                	add    BYTE PTR [rax],al
   b:	02 34 00             	add    dh,BYTE PTR [rax+rax*1]
   e:	03 08                	add    ecx,DWORD PTR [rax]
  10:	3a 21                	cmp    ah,BYTE PTR [rcx]
  12:	01 3b                	add    DWORD PTR [rbx],edi
  14:	0b 39                	or     edi,DWORD PTR [rcx]
  16:	0b 49 13             	or     ecx,DWORD PTR [rcx+0x13]
  19:	02 18                	add    bl,BYTE PTR [rax]
  1b:	00 00                	add    BYTE PTR [rax],al
  1d:	03 0f                	add    ecx,DWORD PTR [rdi]
  1f:	00 0b                	add    BYTE PTR [rbx],cl
  21:	21 08                	and    DWORD PTR [rax],ecx
  23:	49 13 00             	adc    rax,QWORD PTR [r8]
  26:	00 04 05 00 03 0e 3a 	add    BYTE PTR [rax*1+0x3a0e0300],al
  2d:	21 01                	and    DWORD PTR [rcx],eax
  2f:	3b 21                	cmp    esp,DWORD PTR [rcx]
  31:	03 39                	add    edi,DWORD PTR [rcx]
  33:	0b 49 13             	or     ecx,DWORD PTR [rcx+0x13]
  36:	02 18                	add    bl,BYTE PTR [rax]
  38:	00 00                	add    BYTE PTR [rax],al
  3a:	05 11 01 25 0e       	add    eax,0xe250111
  3f:	13 0b                	adc    ecx,DWORD PTR [rbx]
  41:	03 1f                	add    ebx,DWORD PTR [rdi]
  43:	1b 1f                	sbb    ebx,DWORD PTR [rdi]
  45:	11 01                	adc    DWORD PTR [rcx],eax
  47:	12 07                	adc    al,BYTE PTR [rdi]
  49:	10 17                	adc    BYTE PTR [rdi],dl
  4b:	00 00                	add    BYTE PTR [rax],al
  4d:	06                   	(bad)
  4e:	24 00                	and    al,0x0
  50:	0b 0b                	or     ecx,DWORD PTR [rbx]
  52:	3e 0b 03             	ds or  eax,DWORD PTR [rbx]
  55:	08 00                	or     BYTE PTR [rax],al
  57:	00 07                	add    BYTE PTR [rdi],al
  59:	2e 01 3f             	cs add DWORD PTR [rdi],edi
  5c:	19 03                	sbb    DWORD PTR [rbx],eax
  5e:	0e                   	(bad)
  5f:	3a 0b                	cmp    cl,BYTE PTR [rbx]
  61:	3b 0b                	cmp    ecx,DWORD PTR [rbx]
  63:	39 0b                	cmp    DWORD PTR [rbx],ecx
  65:	27                   	(bad)
  66:	19 49 13             	sbb    DWORD PTR [rcx+0x13],ecx
  69:	11 01                	adc    DWORD PTR [rcx],eax
  6b:	12 07                	adc    al,BYTE PTR [rdi]
  6d:	40 18 7c 19 01       	sbb    BYTE PTR [rcx+rbx*1+0x1],dil
  72:	13 00                	adc    eax,DWORD PTR [rax]
  74:	00 08                	add    BYTE PTR [rax],cl
  76:	01 01                	add    DWORD PTR [rcx],eax
  78:	49 13 00             	adc    rax,QWORD PTR [r8]
  7b:	00 09                	add    BYTE PTR [rcx],cl
  7d:	21 00                	and    DWORD PTR [rax],eax
  7f:	49 13 2f             	adc    rbp,QWORD PTR [r15]
  82:	0b 00                	or     eax,DWORD PTR [rax]
	...

Disassembly of section .debug_line:

0000000000000000 <.debug_line>:
   0:	55                   	push   rbp
   1:	00 00                	add    BYTE PTR [rax],al
   3:	00 05 00 08 00 2a    	add    BYTE PTR [rip+0x2a000800],al        # 2a000809 <_end+0x29ffc7f1>
   9:	00 00                	add    BYTE PTR [rax],al
   b:	00 01                	add    BYTE PTR [rcx],al
   d:	01 01                	add    DWORD PTR [rcx],eax
   f:	fb                   	sti
  10:	0e                   	(bad)
  11:	0d 00 01 01 01       	or     eax,0x1010100
  16:	01 00                	add    DWORD PTR [rax],eax
  18:	00 00                	add    BYTE PTR [rax],al
  1a:	01 00                	add    DWORD PTR [rax],eax
  1c:	00 01                	add    BYTE PTR [rcx],al
  1e:	01 01                	add    DWORD PTR [rcx],eax
  20:	1f                   	(bad)
  21:	01 00                	add    DWORD PTR [rax],eax
  23:	00 00                	add    BYTE PTR [rax],al
  25:	00 02                	add    BYTE PTR [rdx],al
  27:	01 1f                	add    DWORD PTR [rdi],ebx
  29:	02 0f                	add    cl,BYTE PTR [rdi]
  2b:	02 2f                	add    ch,BYTE PTR [rdi]
  2d:	00 00                	add    BYTE PTR [rax],al
  2f:	00 00                	add    BYTE PTR [rax],al
  31:	2f                   	(bad)
  32:	00 00                	add    BYTE PTR [rax],al
  34:	00 00                	add    BYTE PTR [rax],al
  36:	05 01 00 09 02       	add    eax,0x2090001
  3b:	49 11 00             	adc    QWORD PTR [r8],rax
  3e:	00 00                	add    BYTE PTR [rax],al
  40:	00 00                	add    BYTE PTR [rax],al
  42:	00 15 08 2e 05 06    	add    BYTE PTR [rip+0x6052e08],dl        # 6052e50 <_end+0x604ee38>
  48:	e5 05                	in     eax,0x5
  4a:	07                   	(bad)
  4b:	75 4b                	jne    98 <__abi_tag-0x2f4>
  4d:	05 09 08 e6 05       	add    eax,0x5e60809
  52:	01 59 02             	add    DWORD PTR [rcx+0x2],ebx
  55:	16                   	(bad)
  56:	00 01                	add    BYTE PTR [rcx],al
  58:	01                   	.byte 0x1

Disassembly of section .debug_str:

0000000000000000 <.debug_str>:
   0:	73 68                	jae    6a <__abi_tag-0x322>
   2:	6f                   	outs   dx,DWORD PTR ds:[rsi]
   3:	72 74                	jb     79 <__abi_tag-0x313>
   5:	20 75 6e             	and    BYTE PTR [rbp+0x6e],dh
   8:	73 69                	jae    73 <__abi_tag-0x319>
   a:	67 6e                	outs   dx,BYTE PTR ds:[esi]
   c:	65 64 20 69 6e       	gs and BYTE PTR fs:[rcx+0x6e],ch
  11:	74 00                	je     13 <__abi_tag-0x379>
  13:	6c                   	ins    BYTE PTR es:[rdi],dx
  14:	6f                   	outs   dx,DWORD PTR ds:[rsi]
  15:	6e                   	outs   dx,BYTE PTR ds:[rsi]
  16:	67 20 75 6e          	and    BYTE PTR [ebp+0x6e],dh
  1a:	73 69                	jae    85 <__abi_tag-0x307>
  1c:	67 6e                	outs   dx,BYTE PTR ds:[esi]
  1e:	65 64 20 69 6e       	gs and BYTE PTR fs:[rcx+0x6e],ch
  23:	74 00                	je     25 <__abi_tag-0x367>
  25:	75 6e                	jne    95 <__abi_tag-0x2f7>
  27:	73 69                	jae    92 <__abi_tag-0x2fa>
  29:	67 6e                	outs   dx,BYTE PTR ds:[esi]
  2b:	65 64 20 63 68       	gs and BYTE PTR fs:[rbx+0x68],ah
  30:	61                   	(bad)
  31:	72 00                	jb     33 <__abi_tag-0x359>
  33:	6d                   	ins    DWORD PTR es:[rdi],dx
  34:	61                   	(bad)
  35:	69 6e 00 6c 6f 6e 67 	imul   ebp,DWORD PTR [rsi+0x0],0x676e6f6c
  3c:	20 69 6e             	and    BYTE PTR [rcx+0x6e],ch
  3f:	74 00                	je     41 <__abi_tag-0x34b>
  41:	61                   	(bad)
  42:	72 67                	jb     ab <__abi_tag-0x2e1>
  44:	63 00                	movsxd eax,DWORD PTR [rax]
  46:	73 68                	jae    b0 <__abi_tag-0x2dc>
  48:	6f                   	outs   dx,DWORD PTR ds:[rsi]
  49:	72 74                	jb     bf <__abi_tag-0x2cd>
  4b:	20 69 6e             	and    BYTE PTR [rcx+0x6e],ch
  4e:	74 00                	je     50 <__abi_tag-0x33c>
  50:	47                   	rex.RXB
  51:	4e 55                	rex.WRX push rbp
  53:	20 43 31             	and    BYTE PTR [rbx+0x31],al
  56:	37                   	(bad)
  57:	20 31                	and    BYTE PTR [rcx],dh
  59:	33 2e                	xor    ebp,DWORD PTR [rsi]
  5b:	32 2e                	xor    ch,BYTE PTR [rsi]
  5d:	30 20                	xor    BYTE PTR [rax],ah
  5f:	2d 6d 74 75 6e       	sub    eax,0x6e75746d
  64:	65 3d 67 65 6e 65    	gs cmp eax,0x656e6567
  6a:	72 69                	jb     d5 <__abi_tag-0x2b7>
  6c:	63 20                	movsxd esp,DWORD PTR [rax]
  6e:	2d 6d 61 72 63       	sub    eax,0x6372616d
  73:	68 3d 78 38 36       	push   0x3638783d
  78:	2d 36 34 20 2d       	sub    eax,0x2d203436
  7d:	67 20 2d 66 61 73 79 	and    BYTE PTR [eip+0x79736166],ch        # 797361ea <_end+0x797321d2>
  84:	6e                   	outs   dx,BYTE PTR ds:[rsi]
  85:	63 68 72             	movsxd ebp,DWORD PTR [rax+0x72]
  88:	6f                   	outs   dx,DWORD PTR ds:[rsi]
  89:	6e                   	outs   dx,BYTE PTR ds:[rsi]
  8a:	6f                   	outs   dx,DWORD PTR ds:[rsi]
  8b:	75 73                	jne    100 <__abi_tag-0x28c>
  8d:	2d 75 6e 77 69       	sub    eax,0x69776e75
  92:	6e                   	outs   dx,BYTE PTR ds:[rsi]
  93:	64 2d 74 61 62 6c    	fs sub eax,0x6c626174
  99:	65 73 20             	gs jae bc <__abi_tag-0x2d0>
  9c:	2d 66 73 74 61       	sub    eax,0x61747366
  a1:	63 6b 2d             	movsxd ebp,DWORD PTR [rbx+0x2d]
  a4:	70 72                	jo     118 <__abi_tag-0x274>
  a6:	6f                   	outs   dx,DWORD PTR ds:[rsi]
  a7:	74 65                	je     10e <__abi_tag-0x27e>
  a9:	63 74 6f 72          	movsxd esi,DWORD PTR [rdi+rbp*2+0x72]
  ad:	2d 73 74 72 6f       	sub    eax,0x6f727473
  b2:	6e                   	outs   dx,BYTE PTR ds:[rsi]
  b3:	67 20 2d 66 73 74 61 	and    BYTE PTR [eip+0x61747366],ch        # 61747420 <_end+0x61743408>
  ba:	63 6b 2d             	movsxd ebp,DWORD PTR [rbx+0x2d]
  bd:	63 6c 61 73          	movsxd ebp,DWORD PTR [rcx+riz*2+0x73]
  c1:	68 2d 70 72 6f       	push   0x6f72702d
  c6:	74 65                	je     12d <__abi_tag-0x25f>
  c8:	63 74 69 6f          	movsxd esi,DWORD PTR [rcx+rbp*2+0x6f]
  cc:	6e                   	outs   dx,BYTE PTR ds:[rsi]
  cd:	20 2d 66 63 66 2d    	and    BYTE PTR [rip+0x2d666366],ch        # 2d666439 <_end+0x2d662421>
  d3:	70 72                	jo     147 <__abi_tag-0x245>
  d5:	6f                   	outs   dx,DWORD PTR ds:[rsi]
  d6:	74 65                	je     13d <__abi_tag-0x24f>
  d8:	63 74 69 6f          	movsxd esi,DWORD PTR [rcx+rbp*2+0x6f]
  dc:	6e                   	outs   dx,BYTE PTR ds:[rsi]
  dd:	00 61 72             	add    BYTE PTR [rcx+0x72],ah
  e0:	67 76 00             	addr32 jbe e3 <__abi_tag-0x2a9>

Disassembly of section .debug_line_str:

0000000000000000 <.debug_line_str>:
   0:	2f                   	(bad)
   1:	68 6f 6d 65 2f       	push   0x2f656d6f
   6:	63 6c 61 75          	movsxd ebp,DWORD PTR [rcx+riz*2+0x75]
   a:	64 69 6f 2f 44 6f 63 	imul   ebp,DWORD PTR fs:[rdi+0x2f],0x75636f44
  11:	75 
  12:	6d                   	ins    DWORD PTR es:[rdi],dx
  13:	65 6e                	outs   dx,BYTE PTR gs:[rsi]
  15:	74 73                	je     8a <__abi_tag-0x302>
  17:	2f                   	(bad)
  18:	43 54                	rex.XB push r12
  1a:	46 73 2d             	rex.RX jae 4a <__abi_tag-0x342>
  1d:	77 72                	ja     91 <__abi_tag-0x2fb>
  1f:	69 74 65 75 70 73 2f 	imul   esi,DWORD PTR [rbp+riz*2+0x75],0x742f7370
  26:	74 
  27:	72 61                	jb     8a <__abi_tag-0x302>
  29:	69 6e 69 6e 67 00 6d 	imul   ebp,DWORD PTR [rsi+0x69],0x6d00676e
  30:	61                   	(bad)
  31:	69                   	.byte 0x69
  32:	6e                   	outs   dx,BYTE PTR ds:[rsi]
  33:	2e 63 00             	cs movsxd eax,DWORD PTR [rax]

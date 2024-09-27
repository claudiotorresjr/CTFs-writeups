#include <stdio.h>

int main(int argc, char const *argv[])
{
	int i = 0;
	int j = 2;
	int k = 3;
	char a[4] = "abc";

	i = j + k;
	printf(argv[1]);

	printf("%40x\n", i);

	return 0;
}

// 0000000000001129 <main>:
//     1129:	f3 0f 1e fa          	endbr64
//     112d:	55                   	push   rbp
//     112e:	48 89 e5             	mov    rbp,rsp
//     1131:	89 7d dc             	mov    DWORD PTR [rbp-0x24],edi
//     1134:	48 89 75 d0          	mov    QWORD PTR [rbp-0x30],rsi
//     1138:	c7 45 e8 01 00 00 00 	mov    DWORD PTR [rbp-0x18],0x1
//     113f:	c7 45 ec 02 00 00 00 	mov    DWORD PTR [rbp-0x14],0x2
//     1146:	48 c7 45 f0 03 00 00 	mov    QWORD PTR [rbp-0x10],0x3
//     114d:	00 
//     114e:	c6 45 e7 41          	mov    BYTE PTR [rbp-0x19],0x41
//     1152:	48 8d 05 ab 0e 00 00 	lea    rax,[rip+0xeab]        # 2004 <_IO_stdin_used+0x4>
//     1159:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
//     115d:	b8 00 00 00 00       	mov    eax,0x0
//     1162:	5d                   	pop    rbp
//     1163:	c3                   	ret

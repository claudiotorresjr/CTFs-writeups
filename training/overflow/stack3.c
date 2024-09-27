#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// gcc -static -z execstack -z norelro -fno-stack-protector -o stack3 stack3.c -m32 -g
// objdump -t stack3 | grep win
// 080498f5 g     F .text  0000002b win
//
// 

void win(void)
{
	printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
	volatile int (*fp)();
	char buffer[64];

	fp = 0;

	gets(buffer);

	if (fp) {
		printf("calling function pointer, jumping to 0x%08x\n", fp);
		fp();
	}
}

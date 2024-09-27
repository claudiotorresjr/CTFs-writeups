#include <stdio.h>

void test(const int x, const int y)
{
	if (y > x) {
		printf("%d\n", y);
	}
}

int main(int argc, char *argv[])
{
	int a = 2;
	char b = 'B';
	char c[32] = "ABC\0";

	test(1, 4);
	return 0;
}

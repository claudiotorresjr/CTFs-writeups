// cripto do arkham - 2023
// use uma string de no maximo 25 caracteres para criptografar

#include <stdio.h>
#include <time.h>
#include <string.h>

int main(int argc, char *argv[])
{
	int count, x, y, z, lc, t, r;
	FILE *a;
    	FILE *output_file = fopen("flag.txt", "w");

	a = fopen(argv[1], "r");
	x = 34;
	y = 55;
	lc = 0;
	count = 0;

	while (!feof(a) || count < 10000000)
	{
		z = x + y;
		int r = fgetc(a);

		if (z == count)
		{
			fprintf(output_file, "%c", r);
			lc++;
			x = y;
			y = z;
		}
		count++;
	}

	fclose(a);
	fclose(output_file);
	return 0;
}

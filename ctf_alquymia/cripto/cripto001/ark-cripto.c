// cripto do arkham - 2023
// use uma string de no maximo 25 caracteres para criptografar

#include <stdio.h>
#include <time.h>
#include <string.h>

int main(int argc, char *argv[])
{
     int count, x, y, z, lc, t, r;
     FILE *a;
     srand(time(NULL));

     if(argc != 2)
     {
          printf("\nUse: ./ark-cripto [secret_message]\n");
          printf("Examples:\n");
          printf("./ark-cripto hello_arkham!\n\n");
          return 0;
     }

     a = fopen("teste.txt", "w");
     t = strlen(argv[1]);
     x = 34;
     y = 55;
     lc = 0;

     for(count = 0; count < 10000000; count++)
     {
          z = x + y;
          r = rand() % 127;
          if((count == z) && (lc < t))
          {
               fprintf(a, "%c", argv[1][lc]);
               lc++;
               x = y;
               y = z;
          }
          else
          {
               fprintf(a, "%c", r);
          }
     }

     fclose(a);
     return 0;
}

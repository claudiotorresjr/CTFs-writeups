// #include<stdio.h>
  
// int main()
// {
//   char s[4] = "ABCD";
//   int flag = 1;
//   int e;

//   printf("%s%nLearning ", s, &e);
//   printf("\nCount: %d\n", e);

//   printf("count de novo: %2$s\n", s, s, s, e);
//   printf("AAA%4c%3$n");
//   printf("\nCount: %d", flag);
 
//   return 0;
// }

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, const char **argv) {
    char s[264];
    unsigned int v4;

    while (1) {
        if (fgets(s, sizeof(s), stdin) == NULL) {
            break;
        }
        printf(s);
        
        if (strncmp(s, "quit", 4) == 0) {
            break;
        }
    }

    return 0;
}

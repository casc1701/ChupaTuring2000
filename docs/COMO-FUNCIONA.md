# Como funciona

## O tableau

O cabeçalho fixa as colunas:

```
  #  A B C D E ... Z
  1  P V G I J ...
```

(no arquivo as letras vêm coladas ou em grupos de 5; o espaço é só leitura humana.)

Para cifrar a 1ª letra `H`:

- linha = 1
- coluna = H = índice 7 (A=0)
- ciphertext = caractere na coluna 7 da linha 1

A 2ª letra usa a **linha 2**, e assim por diante. Não existe “somar 3 e dar a volta no alfabeto”. Cada posição tem o próprio alfabeto embaralhado.

## Por que permutação, não letras repetidas

Se a linha 1 fosse `AAAAA...`, qualquer plaintext mapearia para `A` e o decode não saberia de qual coluna veio. Uma permutação é uma bijeção: cada ciphertext de uma linha aponta para exatamente uma coluna, portanto para exatamente uma letra original.

`gen` constrói isso com Fisher–Yates:

```text
para i de 25 até 1:
    j = secrets.randbelow(i + 1)
    troca chars[i] com chars[j]
```

`secrets.randbelow` usa o CSPRNG do SO. `random.randrange` não.

`read_pad` recusa a linha se `len != 26` ou se o conjunto das letras não for exatamente `{A…Z}`.

## Relação com o OTP clássico

OTP de Vernam, letras:

```
C_i = (P_i + K_i) mod 26
```

`K_i` uniforme em `0..25` é um **deslocamento**. Também é uma permutação, mas só 26 das `26!` permutações possíveis (os 26 Césares).

Aqui `K_i` é uma permutação inteira. Há `log2(26!) ≈ 88.4` bits de chave por letra, contra `log2(26) ≈ 4.7` no aditivo. Os dois dão secrecy perfeita **por letra** se a chave for uniforme e de uso único. O extra não “quebra Turing mais”; só gasta mais tinta.

Referência: C. E. Shannon, “Communication Theory of Secrecy Systems”, *Bell System Technical Journal* 28(4), 1949.

## O que a mensagem perde no caminho

`clean()`:

1. upper
2. NFD, joga fora marcas combinantes (`Á` → `A`)
3. descarta tudo que não é A–Z (espaço, dígito, pontuação)

`ATAQUE AO AMANHECER` vira `ATAQUEAOAMANHECER` (17 letras → 17 linhas do pad).

## Encode vs decode no CLI

- `enc` escreve grupos de 5 e aceita `-o`.
- `dec` imprime contínuo e hoje não tem `-o` (redirecione o stdout: `> claro.txt`).

## Vários pads no mesmo arquivo

`gen --copies 2` empilha dois blocos `OTP 1/2` e `OTP 2/2`.  
`read_pad` concatena **todas** as linhas numeradas do arquivo, na ordem. Não escolha o bloco. Se for usar cópias independentes, grave arquivos separados.

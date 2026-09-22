# ChupaTuring2000

Toolkit didático de **cifra posicional** com um pad de permutações A–Z.

> Este repositório foi **vibecoded**: conversa + Grok + um script Python.
> Não passou por review formal de criptografia. Não use para segredo real.
> Detalhes em [docs/VIBECODED.md](docs/VIBECODED.md).

[Como funciona](docs/COMO-FUNCIONA.md) · [Aviso de vibecode](docs/VIBECODED.md) · [Segurança](SECURITY.md)

## O que é (e o que não é)

Apesar do apelido “OTP” no script, isto **não** é o one-time pad aditivo de Vernam/Shannon (`C = P + K mod 26`).

É um **caderno de substituições de uso único**:

- cada **linha** do pad = 1ª, 2ª, 3ª… letra da mensagem
- cada **coluna** A–Z = letra do plaintext
- a célula `(linha, coluna)` é o ciphertext

Cada linha **tem** de ser uma permutação completa de A–Z. Sem isso o decode é ambíguo.

Com permutações uniformes, geradas por `secrets`, usadas uma vez e nunca reaproveitadas, cada letra isolada ainda é informação-teoricamente opaca (qualquer plaintext de mesmo comprimento é compatível com *alguma* chave). O pedaço difícil continua sendo o de sempre: gerar, transportar e queimar o papel.

## Requisitos

- Python 3.10+
- biblioteca padrão apenas (`secrets`, `argparse`, `unicodedata`)

```bash
git clone https://github.com/casc1701/ChupaTuring2000.git
cd ChupaTuring2000
python otp_toolkit.py --help
```

## Uso

### 1. Gerar o pad

```bash
python otp_toolkit.py gen -n 50 --groups -o pad.txt
python otp_toolkit.py gen -n 50 --copies 2 -o pads.txt
```

Formato:

```
OTP 1/1  |  50x26  |  A-Z
  #  ABCDE FGHIJ KLMNO PQRST UVWXY Z
---  -------------------------------
  1  PVGIJ CAIPV PUPIB GYCSY RVVMX U
  2  PHKEF ISRTK NMRUQ TBQUX EAEUD X
```

Imprima **duas** cópias. Uma fica com você. A outra vai para o destinatário por um canal que você considera confiável. Depois de usar a linha, risque-a.

### 2. Cifrar

```bash
python otp_toolkit.py enc -p pad.txt -m examples/mensagem.txt
python otp_toolkit.py enc -p pad.txt -m examples/mensagem.txt -o cifra.txt
echo "ATAQUE AO AMANHECER" | python otp_toolkit.py enc -p pad.txt
```

Acentos caem (`Á`→`A`, `Ç`→`C`). Espaço e pontuação são descartados. O ciphertext sai em grupos de 5.

### 3. Decifrar

```bash
python otp_toolkit.py dec -p pad.txt -m cifra.txt
echo "IFMGP" | python otp_toolkit.py dec -p pad.txt
```

O decode imprime letras contínuas, sem grupos.

## Regras que quebram o brinquedo

1. Reusar o mesmo pad (ou a mesma linha) em duas mensagens.
2. Pad gerado com `random` em vez de `secrets`.
3. Linha que não é permutação de A–Z (o script recusa na leitura).
4. Mensagem mais longa que o número de linhas.
5. Guardar o pad no mesmo pen-drive que a cifra, no iCloud, no Discord.

## Por que o nome

Turing quebrou máquinas com estrutura. Um pad de permutações sem estrutura, usado uma vez, não deixa o que mastigar. O nome é piada. O paper sério é Shannon, *Communication Theory of Secrecy Systems* (BSTJ, 1949).

## Licença

MIT. Ver [LICENSE](LICENSE).

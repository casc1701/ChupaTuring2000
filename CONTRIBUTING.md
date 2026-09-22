# Contribuir

Patches pequenos e testáveis. Este repo é vibecoded; uma correção humana bem nomeada vale mais que mais vibe.

## Antes do PR

```bash
python otp_toolkit.py gen -n 5 --groups -o /tmp/pad.txt
echo "OLA" | python otp_toolkit.py enc -p /tmp/pad.txt | tee /tmp/c.txt
python otp_toolkit.py dec -p /tmp/pad.txt -m /tmp/c.txt
```

A última linha deve imprimir `OLA`.

Python 3.10+ sem dependências.

## O que ajuda

- `-o` no `dec`
- recusar arquivos com vários blocos `OTP x/y` sem um seletor
- testes em `tests/`
- aviso mais claro quando a linha do pad tem 26 caracteres mas não é permutação

## O que não ajuda

- reescrever em Rust “porque é mais sério”
- adicionar AES “para ficar moderno”
- commitar `pad.txt` usado

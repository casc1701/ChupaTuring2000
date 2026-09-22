# Isto foi vibecoded

**ChupaTuring2000** não nasceu de um RFC, nem de um laboratório, nem de um code review com três criptógrafos e um café ruim.

Nasceu de uma conversa.

1. Pedido de um gerador de one-time pads em Python.
2. Discussão sobre `secrets` vs `random`.
3. Discussão sobre Shannon e computadores quânticos.
4. Um cipher que lia o pad e a mensagem.
5. Ajuste do alfabeto, do `-o`, do formato em grupos de 5.
6. Este script final: cifra **posicional** com permutação por linha.
7. Este repositório, os docs e esta página — também gerados na mesma conversa, por Grok, na conta GitHub `casc1701`.

Isso se chama **vibe coding**: você descreve a intenção, o modelo escreve o código, vocês iteram até “parece certo”. É rápido. É honesto quanto à origem. Não é auditoria.

## O que o vibecode acertou (pelo que dá para ver no texto)

- `secrets.randbelow` no Fisher–Yates, não `random.shuffle`.
- Validação de permutação na leitura do pad (`set(row) == set(A-Z)`).
- Recusa de mensagem maior que o pad.
- Normalização de acento via `unicodedata`.
- CLI com subcomandos `gen` / `enc` / `dec` e `-o` no encode.

## O que o vibecode *não* garante

- Ausência de bugs de parsing em pads malformados ou com vários blocos `OTP 1/2`.
- Constante de tempo no `row.index` (irrelevante para um pad de papel; relevante se alguém expuser o processo).
- Política de destruição, transporte ou numeração de folhas.
- Que isto seja o OTP aditivo clássico. Não é. É um tableau de substituições.
- Qualquer uso operacional (governo, empresa, “minha vida depende disso”).

Se você for usar isto para aprender Shannon, ótimo.  
Se você for usar isto para esconder alguma coisa que dói perder, pare e vá para TLS + um protocolo estudado.

## Como ler este repo

Trate o código como **material didático versionado**, não como produto.  
Patches são bem-vindos; fé cega no commit inicial, não.

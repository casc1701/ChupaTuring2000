#!/usr/bin/env python3
"""
OTP Toolkit — gerador de pads + cifra/decifra posicional.

FORMATO DO PAD
--------------
    #  ABCDE FGHIJ KLMNO PQRST UVWXY Z
---  -------------------------------
  1  PVGIJ CAIPV PUPIB GYCSY RVVMX U
  2  PHKEF ISRTK NMRUQ TBQUX EAEUD X
  ...

Cada linha do pad corresponde à posição de uma letra na mensagem
(linha 1 -> 1ª letra, linha 2 -> 2ª letra, ...). A letra da mensagem
determina a COLUNA (A=1, B=2, ..., Z=26); o caractere nessa coluna,
dentro da linha correspondente, é o caractere cifrado.

REQUISITO CRÍTICO: cada linha do pad precisa ser uma PERMUTAÇÃO
completa de A-Z (26 letras distintas, sem repetição). Se uma letra
se repetir na linha, o decode fica ambíguo — múltiplas colunas
mapeiam para o mesmo caractere cifrado e a operação deixa de ser
inversível. Este script garante isso tanto na geração quanto na
leitura do pad (validação em read_pad).

USO
---
Gerar um pad:
    python otp_toolkit.py gen -n 50 -o pad.txt
    python otp_toolkit.py gen -n 50 -o pad.txt --groups
    python otp_toolkit.py gen -n 50 --copies 3 -o pads.txt

Codificar uma mensagem:
    python otp_toolkit.py enc -p pad.txt -m msg.txt
    echo "HELLO" | python otp_toolkit.py enc -p pad.txt

Decodificar uma mensagem:
    python otp_toolkit.py dec -p pad.txt -m cipher.txt
    echo "IFMGP" | python otp_toolkit.py dec -p pad.txt
"""

from __future__ import annotations

import argparse
import secrets
import string
import sys
import unicodedata

ALPHABET = string.ascii_uppercase
DEFAULT_LINES = 50
DEFAULT_WIDTH = len(ALPHABET)  # 26: A-Z


# --------------------------------------------------------------------------
# Utilidades comuns
# --------------------------------------------------------------------------

def clean(text: str) -> str:
    """Maiúsculas, remove acentos, mantém somente A-Z."""
    text = unicodedata.normalize("NFD", text.upper())
    return "".join(char for char in text if char in ALPHABET)


def group5(text: str) -> str:
    """Formata em grupos de 5 caracteres."""
    return " ".join(text[i : i + 5] for i in range(0, len(text), 5))


# --------------------------------------------------------------------------
# Geração de pad
# --------------------------------------------------------------------------

def secure_permutation(alphabet: str) -> str:
    """
    Retorna uma permutação aleatória e criptograficamente segura do
    alfabeto (Fisher-Yates usando secrets.randbelow — sem viés e sem
    repetição de caracteres).
    """
    chars = list(alphabet)
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


def render_pad(n_lines: int, grouped: bool) -> str:
    """
    Gera o corpo do pad. Sempre com width = 26 (A-Z), pois cada linha
    precisa ser uma permutação completa do alfabeto para o decode ser
    reversível — não faz sentido um width diferente de 26 aqui.
    """
    idx_w = max(3, len(str(n_lines)))
    header_letters = group5(ALPHABET) if grouped else ALPHABET

    lines = [f"{'#':>{idx_w}}  {header_letters}"]
    lines.append(f"{'-' * idx_w}  {'-' * len(header_letters)}")

    for i in range(1, n_lines + 1):
        row = secure_permutation(ALPHABET)
        body = group5(row) if grouped else row
        lines.append(f"{i:>{idx_w}}  {body}")

    return "\n".join(lines) + "\n"


def cmd_gen(args: argparse.Namespace) -> int:
    if args.lines < 1 or args.copies < 1:
        print("Parâmetros devem ser >= 1", file=sys.stderr)
        return 2

    blocks = []
    for c in range(1, args.copies + 1):
        title = f"OTP {c}/{args.copies}  |  {args.lines}x{DEFAULT_WIDTH}  |  A-Z"
        pad = render_pad(args.lines, args.groups)
        blocks.append(title + "\n" + pad)

    text = "\n".join(blocks)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Escrito: {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


# --------------------------------------------------------------------------
# Leitura de pad (com validação de permutação)
# --------------------------------------------------------------------------

def read_pad(filename: str) -> list[str]:
    """
    Lê o pad. Cada linha numerada precisa conter uma permutação
    completa de A-Z (26 letras distintas). Linhas com letras repetidas
    ou faltando são rejeitadas, pois tornariam o decode ambíguo.
    """
    pads = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.split()
            if len(parts) < 2:
                continue
            # Ignora cabeçalho, separador, título "OTP x/y", etc.
            if not parts[0].isdigit():
                continue
            row = clean("".join(parts[1:]))
            if len(row) != 26:
                raise ValueError(
                    f"Linha {parts[0]} do pad não possui 26 caracteres."
                )
            if set(row) != set(ALPHABET):
                raise ValueError(
                    f"Linha {parts[0]} do pad contém letras repetidas ou "
                    f"faltando — precisa ser uma permutação de A-Z. Gere "
                    f"o pad com este mesmo script (subcomando 'gen') para "
                    f"garantir isso."
                )
            pads.append(row)

    if not pads:
        raise ValueError("Nenhuma linha de pad encontrada.")
    return pads


# --------------------------------------------------------------------------
# Cifra / decifra
# --------------------------------------------------------------------------

def encode(message: str, pads: list[str]) -> str:
    """
    A posição da mensagem determina a linha do pad.
    A letra da mensagem determina a coluna (A=0, B=1, ..., Z=25).
    O caractere cifrado é pads[posição][coluna].
    """
    if len(message) > len(pads):
        raise ValueError(
            f"A mensagem possui {len(message)} letras, "
            f"mas o pad possui apenas {len(pads)} linhas."
        )
    result = []
    for position, letter in enumerate(message):
        row = pads[position]
        column = ALPHABET.index(letter)
        result.append(row[column])
    return "".join(result)


def decode(message: str, pads: list[str]) -> str:
    """
    A posição da mensagem cifrada determina a linha do pad.
    Como cada linha é uma permutação (sem repetição), row.index(letter)
    localiza a única coluna correspondente, e essa coluna determina a
    letra original.
    """
    if len(message) > len(pads):
        raise ValueError(
            f"A mensagem possui {len(message)} letras, "
            f"mas o pad possui apenas {len(pads)} linhas."
        )
    result = []
    for position, letter in enumerate(message):
        row = pads[position]
        column = row.index(letter)
        result.append(ALPHABET[column])
    return "".join(result)


def _read_message(args: argparse.Namespace) -> str:
    if args.message:
        with open(args.message, "r", encoding="utf-8") as file:
            return clean(file.read())
    # sem -m: lê da stdin (permite `echo "HELLO" | ... enc -p pad.txt`)
    return clean(sys.stdin.read())


def cmd_enc(args: argparse.Namespace) -> int:
    try:
        pads = read_pad(args.pad)
        message = _read_message(args)
        if not message:
            raise ValueError("A mensagem não contém letras A-Z.")
        result = encode(message, pads)
        result = group5(result)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as file:
                file.write(result + "\n")
            print(f"Escrito: {args.output}", file=sys.stderr)
        else:
            print(result)
    except (OSError, ValueError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1
    return 0


def cmd_dec(args: argparse.Namespace) -> int:
    try:
        pads = read_pad(args.pad)
        message = _read_message(args)
        if not message:
            raise ValueError("A mensagem não contém letras A-Z.")
        result = decode(message, pads)
        print(result)
    except (OSError, ValueError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="OTP Toolkit — gera pads e cifra/decifra mensagens (uso didático)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # gen
    p_gen = sub.add_parser("gen", help="gera um novo pad (linhas = permutações de A-Z)")
    p_gen.add_argument("-n", "--lines", type=int, default=DEFAULT_LINES, help="número de linhas (padrão: 50)")
    p_gen.add_argument("-o", "--output", help="arquivo de saída (padrão: stdout)")
    p_gen.add_argument("--groups", action="store_true", help="agrupar de 5 em 5 letras")
    p_gen.add_argument("--copies", type=int, default=1, help="quantos pads independentes gerar")
    p_gen.set_defaults(func=cmd_gen)

    # enc
    p_enc = sub.add_parser("enc", help="codifica uma mensagem")
    p_enc.add_argument("-p", "--pad", required=True, help="arquivo do pad")
    p_enc.add_argument("-m", "--message", help="arquivo da mensagem (padrão: stdin)")
    p_enc.add_argument("-o", "--output", help="arquivo de saída (padrão: stdout)")
    p_enc.set_defaults(func=cmd_enc)

    # dec
    p_dec = sub.add_parser("dec", help="decodifica uma mensagem")
    p_dec.add_argument("-p", "--pad", required=True, help="arquivo do pad")
    p_dec.add_argument("-m", "--message", help="arquivo da mensagem (padrão: stdin)")
    p_dec.set_defaults(func=cmd_dec)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

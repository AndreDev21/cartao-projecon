#!/usr/bin/env python3
"""Gera os QR codes do cartão a partir da URL final.

    pip install segno
    python3 gerar-qr.py https://exemplo.com/cartao/

Sai com: qr.svg (vetor/gráfica), qr-print.png (impressão) e qr.png (tela).
"""

import sys
import segno

URL_PADRAO = "https://www.projecon.pro.br/cartao/"
VERDE = "#84C225"
ESCURO = "#0c0e0a"


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else URL_PADRAO
    qr = segno.make(url, error="h")

    # vetor — mandar pra gráfica
    qr.save("qr.svg", scale=10, border=4, dark=ESCURO, light="#ffffff")

    # impressão: preto no branco lê melhor em qualquer leitor
    qr.save("qr-print.png", scale=20, border=4, dark="#000000", light="#ffffff")

    # tela / WhatsApp: cores da marca
    qr.save("qr.png", scale=16, border=4, dark=VERDE, light=ESCURO)

    print(f"QR gerado para: {url}")
    print("  qr.svg        vetor, gráfica")
    print("  qr-print.png  impressão / adesivo")
    print("  qr.png        tela, cores Projecon")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Cartão de visita CR80 (85,5 × 54 mm) com QR, na identidade da Projecon.

    pip install reportlab segno
    python3 gerar-cartao-pdf.py

Gera um PDF por URL de destino — cada um com duas páginas, frente e verso,
no tamanho exato do cartão. Frente: marca, nome, contatos e o QR.
Verso: logo, serviços e o site.

BLEED: gráfica costuma pedir 3mm de sangria. Põe BLEED = 3 e o fundo escuro
passa a vazar pra fora do corte; com 0 o PDF sai no tamanho final exato
(serve pra impressão caseira e pra adesivo).
"""

import os

import segno
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

CARD_W = 85.5 * mm
CARD_H = 54 * mm
BLEED = 0 * mm

BG = HexColor("#0c0e0a")
GREEN = HexColor("#84C225")
TEXT = white
BODY = HexColor("#cfd4c6")
MUTED = HexColor("#9aa38d")
DIM = HexColor("#6f7862")

LOGO = "img/logo-projecon.png"

NOME = "Nelson Martins"
CARGO = "PROJECON · CONSTRUÇÃO CIVIL"
TELEFONE = "(19) 99746-0391"
EMAIL = "projetos@projecon.pro.br"
SITE = "www.projecon.pro.br"
SERVICOS = "Obras · Reformas · Galpões · Obras Públicas"
TAGLINE = "CONSTRUINDO COM QUALIDADE, INOVAÇÃO E EXCELÊNCIA"

# (arquivo de saída, URL do QR, rótulo curto impresso abaixo do QR)
SAIDAS = [
    ("cartao-qr-github.pdf",
     "https://andredev21.github.io/cartao-projecon/",
     "andredev21.github.io/cartao-projecon"),
    ("cartao-qr-site.pdf",
     "https://www.projecon.pro.br/cartaodecontato/",
     "projecon.pro.br/cartaodecontato"),
]

for nome, arquivo in [
    ("Poppins", "fonts/Poppins-Regular.ttf"),
    ("Poppins-Medium", "fonts/Poppins-Medium.ttf"),
    ("Poppins-SemiBold", "fonts/Poppins-SemiBold.ttf"),
    ("Poppins-Bold", "fonts/Poppins-Bold.ttf"),
]:
    pdfmetrics.registerFont(TTFont(nome, arquivo))


def espacado(c, x, y, texto, espaco=0.35):
    """Texto com letter-spacing — o cargo e a tagline usam isso, igual ao site."""
    for ch in texto:
        c.drawString(x, y, ch)
        x += c.stringWidth(ch, c._fontname, c._fontsize) + espaco


def largura_espacada(c, texto, espaco=0.35):
    return sum(
        c.stringWidth(ch, c._fontname, c._fontsize) + espaco for ch in texto
    ) - espaco


def fundo(c):
    """Fundo escuro cobrindo página inteira (inclusive sangria) + faixa verde."""
    c.setFillColor(BG)
    c.rect(0, 0, CARD_W + 2 * BLEED, CARD_H + 2 * BLEED, stroke=0, fill=1)
    c.setFillColor(GREEN)
    c.rect(0, CARD_H + 2 * BLEED - 1 * mm, CARD_W + 2 * BLEED, 1 * mm, stroke=0, fill=1)


def frente(c, qr):
    fundo(c)
    x0, y0 = BLEED, BLEED
    pad = 5 * mm

    # --- QR à direita, sobre quadrado branco (a zona de silêncio é obrigatória) ---
    caixa = 30 * mm
    qx = x0 + CARD_W - pad - caixa
    qy = y0 + (CARD_H - caixa) / 2 + 1.5 * mm
    c.setFillColor(white)
    c.roundRect(qx, qy, caixa, caixa, 1.6 * mm, stroke=0, fill=1)
    inset = 0.8 * mm
    c.drawImage(qr, qx + inset, qy + inset, caixa - 2 * inset, caixa - 2 * inset,
                preserveAspectRatio=True, mask="auto")

    c.setFillColor(GREEN)
    c.setFont("Poppins-Medium", 4.6)
    rotulo = "APONTE A CÂMERA"
    c.drawCentredString(qx + caixa / 2, qy - 4.2 * mm, rotulo)

    # --- coluna da esquerda ---
    tx = x0 + pad
    logo_w = 21 * mm
    logo = ImageReader(LOGO)
    iw, ih = logo.getSize()
    logo_h = logo_w * ih / iw
    c.drawImage(logo, tx, y0 + CARD_H - pad - logo_h, logo_w, logo_h,
                preserveAspectRatio=True, mask="auto")

    y = y0 + CARD_H - pad - logo_h - 5.6 * mm
    c.setFillColor(TEXT)
    c.setFont("Poppins-SemiBold", 11)
    c.drawString(tx, y, NOME)

    y -= 4.2 * mm
    c.setFillColor(GREEN)
    c.setFont("Poppins-Medium", 4.8)
    espacado(c, tx, y, CARGO)

    y -= 2.6 * mm
    c.setStrokeColor(GREEN)
    c.setLineWidth(0.4)
    c.line(tx, y, tx + 14 * mm, y)

    y -= 4.6 * mm
    c.setFillColor(BODY)
    c.setFont("Poppins", 6.4)
    c.drawString(tx, y, TELEFONE)
    y -= 3.9 * mm
    c.drawString(tx, y, EMAIL)
    y -= 3.9 * mm
    c.setFillColor(MUTED)
    c.drawString(tx, y, SITE)

    c.showPage()


def verso(c, rotulo_url):
    fundo(c)
    x0, y0 = BLEED, BLEED
    meio = x0 + CARD_W / 2

    logo_w = 26 * mm
    logo = ImageReader(LOGO)
    iw, ih = logo.getSize()
    logo_h = logo_w * ih / iw
    c.drawImage(logo, meio - logo_w / 2, y0 + CARD_H - 6 * mm - logo_h,
                logo_w, logo_h, preserveAspectRatio=True, mask="auto")

    c.setFillColor(BODY)
    c.setFont("Poppins", 6.2)
    c.drawCentredString(meio, y0 + 18.5 * mm, SERVICOS)

    c.setFillColor(GREEN)
    c.setFont("Poppins-Medium", 6.4)
    c.drawCentredString(meio, y0 + 12.5 * mm, rotulo_url)

    c.setFillColor(DIM)
    c.setFont("Poppins", 3.9)
    largura = largura_espacada(c, TAGLINE, 0.3)
    espacado(c, meio - largura / 2, y0 + 6 * mm, TAGLINE, 0.3)

    c.showPage()


def gerar(arquivo, url, rotulo):
    png = arquivo.replace(".pdf", "-qr-tmp.png")
    # border=4: os 4 módulos de zona de silêncio que a norma exige.
    segno.make(url, error="h").save(png, scale=24, border=4,
                                    dark="#000000", light="#ffffff")

    c = canvas.Canvas(arquivo, pagesize=(CARD_W + 2 * BLEED, CARD_H + 2 * BLEED))
    c.setTitle(f"Nelson Martins — Projecon | cartão de visita ({rotulo})")
    c.setAuthor("Projecon — Projetos & Construções")
    frente(c, ImageReader(png))
    verso(c, rotulo)
    c.save()
    os.remove(png)  # o QR já está embutido no PDF
    print(f"{arquivo}  →  {url}")


if __name__ == "__main__":
    for arquivo, url, rotulo in SAIDAS:
        gerar(arquivo, url, rotulo)

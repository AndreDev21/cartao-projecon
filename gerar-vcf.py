#!/usr/bin/env python3
"""Gera o nelson-martins-projecon.vcf com a foto do logo embutida.

    python3 gerar-vcf.py

Mexer aqui e rodar de novo é mais seguro que editar o .vcf na mão — a foto
vira base64 dobrado em dezenas de linhas e qualquer quebra errada corrompe
o arquivo.
"""

import base64
from datetime import date

FOTO = "img/vcard-photo.jpg"
SAIDA = "nelson-martins-projecon.vcf"

CAMPOS = [
    "BEGIN:VCARD",
    "VERSION:3.0",
    "N:Martins;Nelson;;;",
    "FN:Nelson Martins",
    "ORG:Projecon — Projetos & Construções",
    "TITLE:Construção Civil, Reformas e Obras Públicas",
    "TEL;TYPE=CELL,VOICE:+5519997460391",
    "EMAIL;TYPE=INTERNET,WORK:projetos@projecon.pro.br",
    "URL:https://www.projecon.pro.br/",
    "ADR;TYPE=WORK:;;;Serra Negra;SP;;Brasil",
    "X-SOCIALPROFILE;TYPE=instagram:https://www.instagram.com/projeconprojetoseconstrucoes/",
    "X-SOCIALPROFILE;TYPE=facebook:https://www.facebook.com/people/Projecon-Obras-e-Projetos/61574794974703/",
    "X-SOCIALPROFILE;TYPE=linkedin:https://www.linkedin.com/in/nelson-martins-a87a73342",
    "NOTE:Projecon — Projetos & Construções (desde 2016). Obras residenciais\\, "
    "industriais\\, comerciais e públicas\\, reformas\\, ampliações\\, galpões "
    "pré-moldados\\, pisos industriais\\, praças e paisagismo\\, administração de "
    "obras. Serra Negra/SP — atendimento em todo o Brasil.",
]


def dobrar(linha):
    """RFC 2426: no máximo 75 caracteres por linha, continuação começa com espaço."""
    partes = [linha[:75]]
    resto = linha[75:]
    while resto:
        partes.append(" " + resto[:74])
        resto = resto[74:]
    return partes


def main():
    foto = base64.b64encode(open(FOTO, "rb").read()).decode()

    campos = CAMPOS + [
        "PHOTO;ENCODING=b;TYPE=JPEG:" + foto,
        f"REV:{date.today().isoformat()}T00:00:00Z",
        "END:VCARD",
    ]

    linhas = []
    for campo in campos:
        linhas.extend(dobrar(campo))

    with open(SAIDA, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(linhas) + "\r\n")

    print(f"{SAIDA} gerado ({len(linhas)} linhas)")


if __name__ == "__main__":
    main()

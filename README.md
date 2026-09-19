# Cartão de visitas digital — Nelson Martins / Projecon

Página única com a identidade visual do [projecon.pro.br](https://www.projecon.pro.br/):
verde `#84C225`, preto, Poppins/Roboto e o logo do capacete. Feita pra abrir num toque
de NFC ou leitura de QR — WhatsApp, site, redes e **Adicionar aos contatos** (`.vcf`).

```
index.html                      o cartão
nelson-martins-projecon.vcf     contato pra agenda (com foto do logo embutida)
gerar-qr.py                     gera os QR codes a partir da URL final
gerar-vcf.py                    regenera o .vcf (não edite o .vcf na mão)
img/logo-projecon.png           logo (versão pra fundo escuro, tirada do site)
img/banner.jpg                  foto de obra usada no topo do cartão
img/vcard-photo.png             marca quadrada usada como foto do contato
img/og.jpg                      preview ao compartilhar o link (WhatsApp, redes)
img/favicon.png                 ícone da aba
qr-print.png                    QR pra impressão/adesivo (preto no branco)
qr.svg                          QR vetor, pra gráfica
qr.png                          QR nas cores da marca, pra tela
```

## Publicar — GitHub Pages (atual)

URL de produção: **https://andredev21.github.io/cartao-projecon/**

Cria o repo `cartao-projecon` **público** no GitHub e:

```bash
git remote add origin git@github.com:AndreDev21/cartao-projecon.git
git branch -M main
git push -u origin main
```

Depois: Settings → Pages → Source `Deploy from a branch`, branch `main` / `root`.
Sobe em ~1 minuto.

Todos os caminhos do `index.html` são relativos, então a mesma pasta funciona em
qualquer subdiretório — GitHub Pages hoje, FTP depois, sem editar nada.

## Migrar pro FTP depois

Quando tiver acesso ao servidor da Projecon:

1. Sobe a pasta inteira pra `/cartao/` — o link vira `https://www.projecon.pro.br/cartao/`.
2. No `index.html`, troca `og:url` e `og:image` pra URL nova (são os dois únicos
   caminhos absolutos do arquivo — servem pro preview do WhatsApp).
3. **Não apaga o repo do GitHub.** Troca o `index.html` de lá por um redirect, senão
   todo QR já impresso e toda tag NFC já gravada morrem:

   ```html
   <!doctype html><meta charset="utf-8">
   <meta http-equiv="refresh" content="0; url=https://www.projecon.pro.br/cartao/">
   <link rel="canonical" href="https://www.projecon.pro.br/cartao/">
   ```

4. Regenera o QR com a URL nova (`python3 gerar-qr.py https://www.projecon.pro.br/cartao/`)
   e usa esse daí pra frente. Tag NFC não-travada você regrava por cima.

## Gerar o QR

Já estão gerados pra URL do GitHub Pages. Pra refazer com outra URL:

```bash
pip install segno
python3 gerar-qr.py https://www.projecon.pro.br/cartao/
```

Sai `qr-print.png` (impressão/adesivo, preto no branco — lê melhor),
`qr.svg` (vetor pra gráfica) e `qr.png` (tela, nas cores da marca).

## Gravar o cartão/adesivo NFC

Qualquer tag **NTAG213** serve (cartão PVC, adesivo redondo, chaveiro) — a URL é curta.

1. Instala **NFC Tools** (Android ou iPhone).
2. **Escrever → Adicionar um registro → URL / URI** (não "Texto", não "Aplicativo").
3. Cola a URL final e grava encostando a tag atrás do celular.
4. Confere que ficou **um registro só** e testa com a tela ligada e desbloqueada.

Registro de "Aplicativo/Chrome" manda pra Play Store no celular de quem não tem Chrome —
por isso só URL.

**Lock/Proteger** a tag só depois de testar: depois disso não regrava mais.

## Trocar dados

Tudo em texto puro, sem build:

| O quê | Onde |
|---|---|
| Telefone/WhatsApp | `index.html` (links `wa.me/` e `tel:`) e `nelson-martins-projecon.vcf` (`TEL:`) |
| Bio e serviços | `index.html` — `<p class="bio">` e os `<span class="chip">` |
| E-mail | adicionar em `index.html` (bloco `.meta`) e `EMAIL:` no `.vcf` |
| URL do preview | `og:url` e `og:image` no `<head>` do `index.html` |
| Redes sociais | `index.html` (bloco `.socials`) e `X-SOCIALPROFILE` no `.vcf` |

O `.vcf` é vCard 3.0 com a foto do logo embutida em base64 — entra na agenda do iPhone
e do Android já com imagem. Para mudar qualquer campo dele, edita o `gerar-vcf.py` e roda
`python3 gerar-vcf.py`. Editar o `.vcf` direto é pedir problema: a foto ocupa ~190 linhas
dobradas em base64 e uma quebra errada corrompe o arquivo inteiro.

## Dados que ainda faltam

- [ ] Telefone fixo (se tiver)
- [ ] CNPJ e endereço completo (se quiser no vCard)

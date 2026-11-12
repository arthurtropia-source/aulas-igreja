#!/usr/bin/env python3
"""Compara, página a página, um deck gerado pelo motor com o deck original (feito no Cowork).

  python3 ferramentas/comparar.py <original.html> <primeira> <última> <gerado.html> <pasta-saida>

- Recorta do original só as páginas pedidas (o resto do arquivo fica igual), para a numeração "n / total" bater.
- Compara o HTML de cada página (texto e estrutura) e fotografa as duas versões, inclusive cada passo dos mapas.
- Conta os pixels diferentes de cada par de fotos e grava, para cada página, a imagem original | gerada | diferença.
- Grava lado-a-lado.png (todas as páginas) e um resumo em comparacao.md.
"""
import base64
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))

from playwright.sync_api import sync_playwright  # noqa: E402

from navegador import Deck, folha_de_contato  # noqa: E402

JS_DIFF = """async ([a,b])=>{
 const ld=s=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=s;});
 const A=await ld(a),B=await ld(b);const w=A.width,h=A.height;
 const c=document.createElement('canvas');c.width=w*3+20;c.height=h;const x=c.getContext('2d');
 x.fillStyle='#141213';x.fillRect(0,0,c.width,h);x.drawImage(A,0,0);x.drawImage(B,w+10,0);
 const t=document.createElement('canvas');t.width=w;t.height=h;const y=t.getContext('2d');
 y.drawImage(A,0,0);const da=y.getImageData(0,0,w,h).data;y.drawImage(B,0,0);const db=y.getImageData(0,0,w,h).data;
 const out=y.createImageData(w,h);let n=0;
 for(let k=0;k<da.length;k+=4){const d=Math.abs(da[k]-db[k])+Math.abs(da[k+1]-db[k+1])+Math.abs(da[k+2]-db[k+2]);
   if(d>30){n++;out.data[k]=221;out.data[k+1]=51;out.data[k+2]=56;out.data[k+3]=255;}
   else{const g=255-(255-da[k])*0.15;out.data[k]=out.data[k+1]=out.data[k+2]=g;out.data[k+3]=255;}}
 y.putImageData(out,0,0);x.drawImage(t,2*w+20,0);
 return [n,c.toDataURL('image/png')];}"""


def recortar(original, ini, fim, destino):
    with open(original, encoding='utf-8') as f:
        h = f.read()
    a = h.index('<div id="palco">') + len('<div id="palco">')
    b = h.index('<div id="trilha">')
    slots = re.split(r'(?=<div class="slot">)', h[a:b])[1:]
    slots[-1] = slots[-1][:-len('</div>\n')]
    with open(destino, 'w', encoding='utf-8') as f:
        f.write(h[:a] + ''.join(slots[ini - 1:fim]) + '</div>\n' + h[b:])
    return slots[ini - 1:fim]


def paginas_html(caminho):
    with open(caminho, encoding='utf-8') as f:
        h = f.read()
    a = h.index('<div id="palco">') + len('<div id="palco">')
    b = h.index('<div id="trilha">')
    s = re.split(r'(?=<div class="slot">)', h[a:b])[1:]
    s[-1] = s[-1][:-len('</div>\n')]
    return s


def fotografar(html, pasta, prefixo):
    fotos = {}
    with Deck(html) as d:
        for i in range(len(d.paginas())):
            fotos[(i + 1, None)] = d.foto(i, os.path.join(pasta, f'{prefixo}-p{i + 1:02d}.png'))
        for i, passos in d.mapas():
            for s in range(passos + 1):
                d.ir_ao_passo(i, s)
                fotos[(i + 1, s)] = d.foto(i, os.path.join(pasta, f'{prefixo}-p{i + 1:02d}-passo-{s}.png'))
    return fotos


def main(args):
    if len(args) < 5:
        print(__doc__)
        return 1
    original, ini, fim, gerado, saida = args[0], int(args[1]), int(args[2]), args[3], args[4]
    os.makedirs(os.path.join(saida, 'fotos'), exist_ok=True)
    ref = os.path.join(saida, 'original-recortado.html')
    orig_pags = recortar(original, ini, fim, ref)
    ger_pags = paginas_html(gerado)
    html_igual = [i + 1 for i, (x, y) in enumerate(zip(orig_pags, ger_pags)) if x == y]

    fo = fotografar(ref, os.path.join(saida, 'fotos'), 'original')
    fg = fotografar(gerado, os.path.join(saida, 'fotos'), 'gerado')
    linhas = ['# Comparação página a página', '',
              f'- Original: `{original}`, páginas {ini} a {fim}', f'- Gerado: `{gerado}`', '',
              f'Páginas: original {len(orig_pags)} · gerado {len(ger_pags)}. HTML da página idêntico em {len(html_igual)} de {len(orig_pags)}.', '',
              '| Página | Passo do mapa | HTML idêntico | Pixels diferentes |', '|---|---|---|---|']
    pares, rot = [], []
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pg = nav.new_page()
        for chave in sorted(fo, key=lambda k: (k[0], -1 if k[1] is None else k[1])):
            if chave not in fg:
                linhas.append(f'| {chave[0]} | {chave[1] if chave[1] is not None else ""} | | **falta no gerado** |')
                continue
            ua = 'data:image/png;base64,' + base64.b64encode(open(fo[chave], 'rb').read()).decode()
            ub = 'data:image/png;base64,' + base64.b64encode(open(fg[chave], 'rb').read()).decode()
            n, url = pg.evaluate(JS_DIFF, [ua, ub])
            nome = f'p{chave[0]:02d}' + (f'-passo-{chave[1]}' if chave[1] is not None else '') + '-lado-a-lado.png'
            destino = os.path.join(saida, 'fotos', nome)
            with open(destino, 'wb') as f:
                f.write(base64.b64decode(url.split(',', 1)[1]))
            pares.append(destino)
            rot.append(f'p. {chave[0]}' + (f' · passo {chave[1]}' if chave[1] is not None else '') + f' · {n} px diferentes')
            igual = 'sim' if chave[0] in html_igual else 'não'
            linhas.append(f'| {chave[0]} | {chave[1] if chave[1] is not None else ""} | {igual} | {n} |')
        nav.close()
    folha_de_contato(pares, os.path.join(saida, 'lado-a-lado.png'), colunas=1, largura=1500, rotulos=rot, proporcao=720 / 3860)
    linhas += ['', 'Cada imagem em `fotos/*-lado-a-lado.png`: original | gerado | diferença (em vermelho o que mudou).']
    with open(os.path.join(saida, 'comparacao.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas) + '\n')
    print('\n'.join(linhas))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

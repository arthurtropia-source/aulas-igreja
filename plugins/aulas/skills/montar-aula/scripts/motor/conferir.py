#!/usr/bin/env python3
"""Conferências automáticas de um deck. Rodam sempre, depois de gerar.

  python3 conferir.py <pasta-da-aula>/aula-1.html

O que confere, página a página (em tamanho real, 1280 × 720):
  1. nada transborda: nenhum elemento sai pela direita ou por baixo da página, e o miolo não estoura;
  2. folga de pelo menos 10 px entre o título e o primeiro bloco;
  3. folga de pelo menos 24 px entre o conteúdo e a borda de baixo da página;
  4. o miolo é centralizado com "justify-content: safe center" (se o conteúdo crescer, ele desce em vez de subir para cima do título);
  5. nenhum cartão só com rótulo (cartão, lado do par ou passo de mapa sem texto).
E grava, na pasta conferencia/ ao lado do HTML:
  - uma foto de cada página (paginas/p01.png ...) e de cada passo dos mapas (mapas/p07-passo-0.png ...);
  - folha-de-contato.png (todas as páginas) e folha-dos-mapas.png (todos os passos), para a conferência visual.
Sai com código 1 se alguma conferência falhar.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from navegador import Deck, folha_de_contato  # noqa: E402

FOLGA_TITULO = 10
FOLGA_RODAPE = 24

JS_CONFERE = """([FT,FR])=>{
const out=[];
document.querySelectorAll('.pagina').forEach((pg,i)=>{
  const n=i+1, r=pg.getBoundingClientRect(), prob=[];
  // 1 e 3: transbordo e folga antes do rodapé (só nas páginas de texto; capas e mapas ocupam a página toda)
  const sl=pg.querySelector('.sl');
  const alvo=sl?[...sl.querySelectorAll('*')]:[...pg.querySelectorAll('*')].filter(e=>!e.closest('svg'));
  const fora=new Set(), justo=new Set();
  alvo.forEach(e=>{const q=e.getBoundingClientRect();if(!q.width&&!q.height)return;
    const nome=(e.className&&e.className.baseVal===undefined?e.className:e.tagName)||e.tagName;
    if(q.right>r.right+1||q.bottom>r.bottom+1||q.left<r.left-1)fora.add(nome);
    else if(sl&&q.bottom>r.bottom-FR+1)justo.add(nome);});
  if(fora.size)prob.push('transborda a página: '+[...fora].slice(0,3).join(', '));
  if(justo.size)prob.push('menos de '+FR+' px antes da borda de baixo: '+[...justo].slice(0,3).join(', '));
  const mi=pg.querySelector('.sl .miolo');
  if(mi&&mi.scrollHeight>mi.clientHeight+1)prob.push('o miolo estoura ('+(mi.scrollHeight-mi.clientHeight)+' px a mais)');
  // 2: folga sob o título
  const h=pg.querySelector('.sl > .t1, .sl > .t2');
  if(h&&mi&&mi.firstElementChild){const d=mi.firstElementChild.getBoundingClientRect().top-h.getBoundingClientRect().bottom;
    if(d<FT)prob.push('só '+Math.round(d)+' px entre o título e o primeiro bloco');}
  // 4: centralização segura
  if(mi&&!getComputedStyle(mi).justifyContent.includes('safe'))prob.push('miolo sem "safe center"');
  // 5: cartão só com rótulo
  pg.querySelectorAll('.card,.lado,.cap').forEach(c=>{
    const txt=[...c.querySelectorAll('.t,.d,li')].map(x=>x.textContent.trim()).join('');
    if(!txt)prob.push('cartão só com rótulo: "'+((c.querySelector('.k')||{}).textContent||'').trim()+'"');});
  pg.querySelectorAll('.ca').forEach(c=>{if(!c.textContent.trim())prob.push('passo da cadeia vazio');});
  if(prob.length)out.push([n,pg.dataset.titulo,prob]);
});
return out;}"""


def conferir(html, fotos=True):
    pasta = os.path.join(os.path.dirname(os.path.abspath(html)), 'conferencia')
    os.makedirs(os.path.join(pasta, 'paginas'), exist_ok=True)
    os.makedirs(os.path.join(pasta, 'mapas'), exist_ok=True)
    with Deck(html) as d:
        problemas = d.pg.evaluate(JS_CONFERE, [FOLGA_TITULO, FOLGA_RODAPE])
        n = len(d.paginas())
        fotos_pg, fotos_mapa, rot_mapa = [], [], []
        if fotos:
            for i in range(n):
                fotos_pg.append(d.foto(i, os.path.join(pasta, 'paginas', f'p{i + 1:02d}.png')))
            for i, passos in d.mapas():
                for s in range(passos + 1):
                    d.ir_ao_passo(i, s)
                    fotos_mapa.append(d.foto(i, os.path.join(pasta, 'mapas', f'p{i + 1:02d}-passo-{s}.png')))
                    rot_mapa.append(f'p. {i + 1} · ' + ('visão geral' if s == 0 else f'passo {s} de {passos}'))
                d.ir_ao_passo(i, 0)
    if fotos:
        folha_de_contato(fotos_pg, os.path.join(pasta, 'folha-de-contato.png'),
                         rotulos=[f'p. {k + 1}' for k in range(len(fotos_pg))])
        if fotos_mapa:
            folha_de_contato(fotos_mapa, os.path.join(pasta, 'folha-dos-mapas.png'), colunas=3, largura=520, rotulos=rot_mapa)
    return n, problemas, pasta


def main(args):
    if not args:
        print(__doc__)
        return 1
    html = args[0]
    n, problemas, pasta = conferir(html, fotos='--sem-fotos' not in args)
    print(f'{n} páginas conferidas em {html}')
    if not problemas:
        print('ok: nenhuma falha (transbordo, folga sob o título ≥ 10 px, folga antes do rodapé ≥ 24 px, safe center, cartão vazio)')
    for num, tit, probs in problemas:
        for p in probs:
            print(f'  FALHA p. {num} ({tit}): {p}')
    if '--sem-fotos' not in args:
        print(f'fotos e folha de contato: {pasta}')
    return 1 if problemas else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

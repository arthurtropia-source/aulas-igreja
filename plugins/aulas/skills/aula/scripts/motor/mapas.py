"""Página de mapa por passos (o "mapa narrativo").

O mapa-base é um SVG na pasta mapas/ da matéria ou da aula (litoral, regiões, cidades e a rota geral).
O mapa tem a cor do curso: mora na pasta do curso ou, para o curso que vem no plugin, em
cursos/<curso>/mapas/ dentro da skill (procurado por último).
A aula diz só a história: os passos, com a legenda, a cidade em foco e o trecho da rota de cada um.
As cidades são achadas pelo nome no próprio SVG; um ponto solto pode ser dado como "x,y".

No navegador (molde/deck.js): a seta avança o passo antes de mudar de página, o clique no mapa
também avança, o trecho do passo se desenha, a cidade pulsa e o mapa aproxima (zoom) até a área
do campo "zoom"; o tamanho dos rótulos se ajusta ao zoom pela variável --zf.
"""
import html as H
import os
import re

from formato import ErroFormato

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mapas')
VERMELHO = '#DD3338'
LEGENDA = {'linha': '<i></i>', 'tracejada': '<i class="d"></i>', 'preta': '<i class="k"></i>', 'ponto': '<b></b>'}
_pastas_extra = []


def procurar_em(pasta):
    """Pastas onde o gerador também procura mapas (a da aula e a da matéria)."""
    _pastas_extra[:] = [pasta, os.path.dirname(pasta)]


_pastas_do_curso = []


def mapas_do_curso(pasta):
    """A pasta mapas/ ao lado da identidade do curso (no plugin: cursos/<curso>/mapas/). Procurada por último."""
    _pastas_do_curso[:] = [pasta]


def abrir_mapa(nome, linha):
    for base in _pastas_extra + [PASTA] + _pastas_do_curso:
        for c in (os.path.join(base, 'mapas', nome + '.svg'), os.path.join(base, nome + '.svg')):
            if os.path.exists(c):
                with open(c, encoding='utf-8') as f:
                    return f.read().strip('\n')
    raise ErroFormato(linha, f'mapa "{nome}" não encontrado (ele fica em mapas/{nome}.svg, na pasta da matéria ou da aula)')


def cidades_do_svg(svg):
    out = {}
    for g in re.finditer(r'<g class="city[^"]*">(.*?)</g>', svg, re.S):
        c = re.search(r'<circle cx="([^"]+)" cy="([^"]+)"', g.group(1))
        t = re.search(r'<text[^>]*>(.*?)</text>', g.group(1), re.S)
        if c and t:
            out[t.group(1).strip()] = (c.group(1), c.group(2))
    return out


def _ponto(nome, cidades, linha):
    nome = nome.strip()
    if nome in cidades:
        return cidades[nome]
    m = re.match(r'^(-?[\d.]+)\s*,\s*(-?[\d.]+)$', nome)
    if m:
        return (m.group(1), m.group(2))
    raise ErroFormato(linha, f'cidade "{nome}" não está no mapa (nem é um ponto "x,y")')


def pagina_mapa(p, idx, ident):
    c = p.campos
    svg = abrir_mapa(c.get('mapa'), p.linha)
    cidades = cidades_do_svg(svg)
    zoom = c.get('zoom')
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1).split()
    zf = float(vb[2]) / float(zoom.split()[2])

    passos = [b for b in p.blocos if b.tipo == 'passo']
    if not passos:
        raise ErroFormato(p.linha, 'mapa sem nenhum "### passo"')
    caps, nomes, segs, focos = [], [], [], {}
    for i, b in enumerate(passos):
        f = b.campos()
        cid = f.get('cidade', '')
        if '=' in cid:  # "Vale = Colossos + Laodiceia + Hierápolis": foco em vários pontos
            nome, lista = [x.strip() for x in cid.split('=', 1)]
            focos.setdefault(nome, [_ponto(x, cidades, b.linha) for x in lista.split('+')])
            cid = nome
        elif cid:
            focos.setdefault(cid, [_ponto(cid, cidades, b.linha)])
        nomes.append(cid)
        k = 'Visão geral' if i == 0 else f'Passo {i} de {len(passos) - 1}'
        caps.append(f'<div class="cap" data-passo="{i}"><div class="k">{k}</div><div class="t">{f.get("título")}</div>'
                    f'<div class="d">{f.get("texto")}</div></div>')
        for campo, val in f.pares:
            if campo in ('trecho', 'trecho tracejado'):
                pts = [_ponto(x, cidades, b.linha) for x in val.split('>')]
                d = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
                da = ' stroke-dasharray="6 6"' if campo == 'trecho tracejado' else ''
                segs.append(f'<path class="seg" data-passo="{i}" d="{d}" fill="none" stroke="{VERMELHO}" stroke-width="3" '
                            f'stroke-linecap="round" stroke-linejoin="round"{da}/>')

    extra = ''.join(segs)
    for nome, pts in focos.items():
        extra += (f'<g class="foco" data-cidade="{nome}">' +
                  ''.join(f'<circle cx="{x}" cy="{y}" r="16" fill="none" stroke="{VERMELHO}" stroke-width="3"/>'
                          f'<circle cx="{x}" cy="{y}" r="6" fill="{VERMELHO}"/>' for x, y in pts) + '</g>')
    # ids únicos por página (o mesmo mapa pode aparecer mais de uma vez no deck)
    svg = re.sub(r'id="(m\d+)-arr"', lambda m: f'id="{m.group(1)}-arr-{idx}"', svg)
    svg = re.sub(r'url\(#(m\d+)-arr\)', lambda m: f'url(#{m.group(1)}-arr-{idx})', svg)
    svg = svg.replace('<svg ', '<svg id="mp%d" style="--zf:%.3f" ' % (idx, zf), 1)
    svg = svg.replace('</svg>', extra + '</svg>')

    leg = ''
    for l in c.todos('legenda'):
        tipo, txt = [x.strip() for x in l.split('|', 1)]
        leg += f'<span>{LEGENDA[tipo]}{txt}</span>'
    titulo = c.get('título', p.titulo)
    return (f'<div class="pg-mapa anim" data-passos="{len(passos) - 1}" data-cur="0" data-zoom="{zoom}" '
            f"data-cidades='{H.escape(str(nomes))}'>\n"
            f'    <div class="cab"><div><div class="rot">{c.get("rótulo", "")}</div><h2 class="t2">{titulo}</h2></div>'
            f'<img src="{ident.logo_escuro}" style="height:26px"></div>\n'
            f'    <div class="corpo-mapa"><div class="quadro">{svg}</div><div class="caps">{"".join(caps)}'
            f'<div class="dica">→ avança um passo · ← volta · clique no mapa também avança</div></div></div>\n'
            f'    <div class="leg">{leg}</div></div>')

#!/usr/bin/env python3
"""Converte páginas de um deck HTML antigo (feito no Cowork) para o formato de dados do motor (aula.md).

Uso:
  python3 ferramentas/html_para_aula.py <deck.html> <primeira> <última> <saida/aula.md> \
      [--mapa N=nome-do-mapa ...] [--cabecalho "campo: valor" ...]

- As páginas são contadas a partir de 1, como no sumário do deck.
- Cada bloco convertido é conferido na hora: o motor gera o HTML do bloco a partir do aula.md
  e ele precisa sair idêntico ao original. O que não sai idêntico vira um bloco "### html" (cópia literal)
  e é listado no fim, para virar tipo de bloco próprio depois.
- --mapa N=nome: extrai o SVG-base do mapa da página N para <matéria>/mapas/nome.svg (a matéria é a pasta acima da pasta da aula).
O texto nunca é reescrito: só muda de lugar (do HTML para o aula.md).
"""
import os
import re
import sys
from html.parser import HTMLParser

AQUI = os.path.dirname(os.path.abspath(__file__))
MOTOR = os.path.dirname(AQUI)
sys.path.insert(0, MOTOR)

import blocos  # noqa: E402
import formato  # noqa: E402
import mapas  # noqa: E402

PASTA_MAPAS = None  # definida no main: <matéria>/mapas/, ao lado da pasta da aula

VAZIAS = {'img', 'br', 'meta', 'input', 'hr', 'link'}


# ------------------------------------------------------------ árvore HTML que se reescreve igual
class No:
    def __init__(self, tag, attrs, pai, fecha=False):
        self.tag, self.attrs, self.pai, self.fecha = tag, attrs, pai, fecha
        self.filhos = []

    def a(self, k, padrao=None):
        for x, y in self.attrs:
            if x == k:
                return y
        return padrao

    def dado(self, k):
        """Atributo data-* com as entidades desfeitas (&quot; -> \")."""
        import html
        v = self.a(k)
        return html.unescape(v) if v is not None else None

    def cls(self):
        return (self.a('class') or '').split()

    def elementos(self):
        return [f for f in self.filhos if isinstance(f, No)]

    def html(self):
        return serial(self)

    def interno(self):
        return ''.join(serial(f) for f in self.filhos)


def serial(n):
    if isinstance(n, str):
        return n
    at = ''.join(f' {k}' if v is None else f' {k}="{v}"' if "'" in v or '"' not in v else f" {k}='{v}'" for k, v in n.attrs)
    if n.fecha:
        return f'<{n.tag}{at}/>'
    if n.tag in VAZIAS:
        return f'<{n.tag}{at}>'
    return f'<{n.tag}{at}>' + ''.join(serial(f) for f in n.filhos) + f'</{n.tag}>'


class Leitor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.raiz = No('raiz', [], None)
        self.cur = self.raiz

    def handle_starttag(self, t, a):
        n = No(t, self._attrs(), self.cur)
        self.cur.filhos.append(n)
        if t not in VAZIAS:
            self.cur = n

    def handle_startendtag(self, t, a):
        self.cur.filhos.append(No(t, self._attrs(), self.cur, fecha=True))

    def _attrs(self):
        # atributos como estão no texto (sem desfazer &#x27; etc.)
        txt = self.get_starttag_text()
        return [(m.group(1), m.group(3) if m.group(3) is not None else m.group(4))
                for m in re.finditer(r'\s([\w:-]+)(=(?:"([^"]*)"|\'([^\']*)\'))?', txt[txt.index(' '):] if ' ' in txt else '')]

    def handle_endtag(self, t):
        c = self.cur
        while c is not self.raiz and c.tag != t:
            c = c.pai
        if c is not self.raiz:
            self.cur = c.pai

    def handle_data(self, d):
        self.cur.filhos.append(d)

    def handle_entityref(self, name):
        self.cur.filhos.append(f'&{name};')

    def handle_charref(self, name):
        self.cur.filhos.append(f'&#{name};')


def arvore(h):
    p = Leitor()
    p.feed(h)
    return p.raiz


def achar(n, f):
    if isinstance(n, str):
        return None
    if f(n):
        return n
    for k in n.filhos:
        r = achar(k, f)
        if r is not None:
            return r


def todos(n, f, out=None):
    out = [] if out is None else out
    if isinstance(n, No):
        if f(n):
            out.append(n)
        for k in n.filhos:
            todos(k, f, out)
    return out


# ------------------------------------------------------------ texto -> marcação
def md(n, destaque='r'):
    """Conteúdo de um nó em texto do aula.md: <b> vira **, <i> vira *, <span class="r|hl"> vira ==."""
    out = ''
    for f in n.filhos:
        if isinstance(f, str):
            out += f
        elif f.tag == 'b' and not f.attrs:
            out += '**' + md(f, destaque) + '**'
        elif f.tag == 'i' and not f.attrs:
            out += '*' + md(f, destaque) + '*'
        elif f.tag == 'span' and f.attrs == [('class', destaque)]:
            out += '==' + md(f, destaque) + '=='
        else:
            out += serial(f)
    return out


def so_texto(n):
    return ''.join(f if isinstance(f, str) else so_texto(f) for f in n.filhos)


COR = {'red': 'vermelho', 'blk': 'preto', 'cz': 'cinza'}
MT = {'mt1': 'pequeno', 'mt': 'médio', 'mt2': 'grande'}


def cor_de(n, base):
    for c in n.cls():
        if c in COR:
            return COR[c]
    return None


def item_nomeado(campos, cor=None):
    linhas = []
    for i, (k, v) in enumerate(campos):
        linhas.append(('- ' if i == 0 else '  ') + f'{k}: {v}')
    if cor:
        linhas.append(f'  cor: {cor}')
    return linhas


def item_curto(valores, cor=None):
    if any('|' in v for v in valores):
        return None
    while valores and valores[-1] == '':
        valores = valores[:-1]
    s = '- ' + ' | '.join(valores)
    if cor:
        s += ' {' + cor + '}'
    return [s]


def filho(n, cls):
    for f in n.elementos():
        if cls in f.cls():
            return f


# ------------------------------------------------------------ blocos
def converter_bloco(n, titulo_pagina):
    """Devolve (cabeçalho do bloco, opções, linhas) ou None se não reconhece."""
    cl = n.cls()
    ops = []
    # espaço acima (classe mt* no próprio bloco)
    for c in cl:
        if c in MT:
            ops.append('acima ' + MT[c])
    st = n.a('style')
    if n.tag == 'div' and len(cl) == 1 and cl[0] in MT and not st and len(n.elementos()) == 1 and \
            not any(isinstance(f, str) and f.strip() for f in n.filhos):
        r = converter_bloco(n.elementos()[0], titulo_pagina)
        if r is None:
            return None
        t, o, l = r
        return t, ['acima ' + MT[cl[0]]] + o, l
    if n.tag == 'div' and not cl and st and re.match(r'^height:[\d.]+px$', st) and not n.filhos:
        return 'espaço', [st.split(':')[1]], []
    if n.tag == 'div' and len(cl) == 1 and cl[0] in MT and not st and not n.filhos:
        return 'espaço', [MT[cl[0]]], []
    if n.tag == 'div' and cl == ['versiculo'] and len(n.elementos()) == 1:
        cit = n.elementos()[0]
        m = re.match(r'^font-size:([\d.]+px);text-transform:none;font-weight:600;line-height:1.4$', cit.a('style') or '')
        if cit.cls() == ['cit'] and m:
            ref = filho(cit, 'ref')
            corpo = No('x', [], None)
            corpo.filhos = [f for f in cit.filhos if f is not ref]
            return 'versículo', ['longo ' + m.group(1)], [f'texto: {md(corpo, "hl")}', f'referência: {md(ref)}']
    if st and not (n.tag == 'p' and re.match(r'^margin-bottom:[\d.]+px$', st)) and not (n.tag == 'ol' and re.match(r'^counter-reset:n \d+$', st)) \
            and not (cl == ['tl'] and re.match(r'^height:[\d.]+px$', st)):
        return None
    if (n.tag == 'p' and cl and cl[0] in ('frase', 'corpo', 'nota')) or (n.tag == 'div' and cl and cl[0] == 'rot'):
        tipo = {'frase': 'frase', 'corpo': 'texto', 'nota': 'nota', 'rot': 'rótulo'}[cl[0]]
        if 'g' in cl:
            if tipo == 'frase' and titulo_pagina.lower().startswith('desafio'):
                tipo = 'desafio'
            else:
                ops.append('grande')
        if st:
            ops.append('abaixo ' + st.split(':')[1])
        return tipo, ops, [md(n)]
    if n.tag == 'div' and cl[:1] == ['cards']:
        aprend = 'aprend' in cl
        linhas = []
        for c in n.elementos():
            k, t, d = filho(c, 'k'), filho(c, 't'), filho(c, 'd')
            campos = []
            if aprend:
                campos = [('rótulo', md(k)), ('título', md(t))]
            else:
                if k is not None:
                    campos.append(('rótulo', md(k)))
                if t is not None:
                    campos.append(('título', md(t)))
                if d is not None:
                    campos.append(('texto', md(d)))
            linhas += item_nomeado(campos, cor_de(c, 'card'))
        if aprend:
            return 'aprendemos', ops, linhas
        ncol = [c[1:] for c in cl if re.match(r'^c\d$', c)][0]
        nitens = len(n.elementos())
        if ncol != str(nitens if nitens <= 5 else 3):
            ops.append('colunas ' + ncol)
        return 'cartões', ops, linhas
    if n.tag == 'ol' and 'num' in cl:
        if 'duas' in cl:
            ops.append('duas colunas')
        if 'compacta' in cl:
            ops.append('compacta')
        if st:
            ops.append('começa em %d' % (int(st.split()[-1]) + 1))
        linhas = []
        for li in n.elementos():
            d = li.elementos()[0]
            b = [x for x in d.elementos() if x.tag == 'b'][0]
            s = [x for x in d.elementos() if x.tag == 'span']
            campos = [('título', md(b))] + ([('texto', md(s[0]))] if s else [])
            linhas += item_curto([v for _, v in campos]) if len(campos) == 1 and '|' not in campos[0][1] else item_nomeado(campos)
        return 'lista', ops, linhas
    if n.tag == 'div' and cl == ['cadeia']:
        linhas = []
        for ca in n.elementos():
            b = [x for x in ca.elementos() if x.tag == 'b'][0]
            s = [x for x in ca.elementos() if x.tag == 'small']
            campos = [('título', md(b))] + ([('texto', md(s[0]))] if s else [])
            cor = cor_de(ca, 'ca')
            linhas += item_nomeado(campos, cor) if len(campos) > 1 else (item_curto([campos[0][1]], cor) or item_nomeado(campos, cor))
        return 'cadeia', ops, linhas
    if n.tag == 'div' and cl == ['par']:
        linhas = []
        for lado in n.elementos():
            k, t = filho(lado, 'k'), filho(lado, 't')
            campos = ([('rótulo', md(k))] if k is not None else []) + ([('título', md(t))] if t is not None else [])
            linhas += item_nomeado(campos, cor_de(lado, 'lado'))
            ul = [x for x in lado.elementos() if x.tag == 'ul'][0]
            linhas.append('  itens:')
            linhas += ['    - ' + md(li) for li in ul.elementos()]
        return 'par', ops, linhas
    if n.tag == 'div' and cl == ['faixa']:
        k = filho(n, 'k')
        b = [x for x in n.elementos() if x.tag == 'b'][0]
        return 'faixa', ops, [f'rótulo: {md(k)}', f'texto: {md(b)}']
    if n.tag == 'div' and cl == ['chamada']:
        sm = [x for x in n.elementos() if x.tag == 'small']
        corpo = No('x', [], None)
        corpo.filhos = [f for f in n.filhos if not (isinstance(f, No) and f.tag == 'small')]
        linhas = [f'texto: {md(corpo)}'] + ([f'nota: {md(sm[0])}'] if sm else [])
        return 'chamada', ops, linhas
    if n.tag == 'div' and cl == ['versiculo']:
        cit = n.elementos()[0]
        if 'g' in cit.cls():
            ops.append('grande')
        ref = filho(cit, 'ref')
        corpo = No('x', [], None)
        corpo.filhos = [f for f in cit.filhos if f is not ref]
        texto = md(corpo, 'hl')
        return 'versículo', ops, [f'texto: {texto}', f'referência: {md(ref)}']
    if n.tag == 'div' and cl == ['chips']:
        linhas = []
        for c in n.elementos():
            linhas += item_curto([md(c)], cor_de(c, 'chip')) or item_nomeado([('texto', md(c))], cor_de(c, 'chip'))
        return 'chips', ops, linhas
    if n.tag == 'div' and cl == ['semana']:
        linhas = []
        for d in n.elementos():
            v = [md(filho(d, x)) for x in ('d', 'r', 's') if filho(d, x) is not None]
            linhas += item_curto(v) or item_nomeado(list(zip(['dia', 'referência', 'nota'], v)))
        return 'leitura', ops, linhas
    if n.tag == 'div' and cl == ['ordem']:
        linhas = []
        for d in n.elementos():
            v = [md(filho(d, 'n')), md(filho(d, 'c')), md(filho(d, 't'))]
            cor = 'vermelho' if 'on' in d.cls() else None
            linhas += item_curto(v, cor) or item_nomeado(list(zip(['número', 'textos', 'título'], v)), cor)
        return 'ordem', ops, linhas
    if n.tag == 'div' and cl == ['tl']:
        if st != 'height:300px':
            ops.append('altura ' + st.split(':')[1])
        els = n.elementos()
        linhas = []
        for pt, ev in zip(els[0::2], els[1::2]):
            campos = [('data', md(filho(ev, 'd'))), ('título', md(filho(ev, 't'))), ('texto', md(filho(ev, 's'))),
                      ('ponto', pt.a('style').split(':')[1]), ('caixa', ev.a('style').split(':')[1])]
            linhas += item_nomeado(campos)
        return 'linha do tempo', ops, linhas
    if n.tag == 'table' and 'tb' in cl:
        if 'grande' in cl:
            ops.append('grande')
        th = todos(n, lambda x: x.tag == 'th')
        trs = todos(n, lambda x: x.tag == 'tr')[1:]
        todas_k = all(tr.elementos()[0].a('class') == 'k' for tr in trs)
        if todas_k:
            ops.append('rótulo na 1ª coluna')

        def cel(td, i):
            c = td.a('class') or ''
            if c == 'r':
                return '{vermelho} ' + md(td)
            if c == 'k' and not (todas_k and i == 0):
                return '{rótulo} ' + md(td)
            if c == 'b':
                return '{negrito} ' + md(td)
            return md(td)

        linhas = ['| ' + ' | '.join(cel(x, i) for i, x in enumerate(th)) + ' |', '|' + '---|' * len(th)]
        for tr in trs:
            linhas.append('| ' + ' | '.join(cel(x, i) for i, x in enumerate(tr.elementos())) + ' |')
        return 'tabela', ops, linhas
    return None


def texto_do_bloco(tipo, ops, linhas):
    cab = '### ' + tipo + (f' ({", ".join(ops)})' if ops else '')
    return [cab] + linhas


def conferir_bloco(linhas_md, original_html, versoes='embaixo'):
    tmp = '## x\n' + '\n'.join(linhas_md) + '\n'
    aula = _ler_texto(tmp)
    try:
        h = blocos.bloco(aula.paginas[0].blocos[0], versoes)
    except Exception:
        return False
    return h == original_html


def _ler_texto(txt):
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(txt)
        nome = f.name
    try:
        return formato.ler(nome)
    finally:
        os.unlink(nome)


# ------------------------------------------------------------ páginas
def converter_pagina(slot, num, mapas_pedidos, avisos, ident_nome, cab_aula):
    pg = slot.elementos()[0]
    titulo = pg.dado('data-titulo')
    out = ['', f'## {titulo}']
    campos = []
    corpo = []
    cl = pg.cls()
    secao = pg.dado('data-secao') or ''
    if 'capa' in cl:
        cap = achar(pg, lambda x: 'capa' in x.cls() and x is not pg)
        lock = achar(cap, lambda x: x.cls() == ['lock'])
        cartas = achar(cap, lambda x: x.cls() == ['cartas'])
        cita = achar(cap, lambda x: x.cls() == ['cita'])
        curso = achar(cap, lambda x: x.cls() == ['curso'])
        campos += [('tipo', 'capa do curso')]
        if md(curso) != ident_nome:
            campos.append(('curso', md(curso)))
        campos += [('título', md(lock)), ('cartas', ' | '.join(md(s) for s in cartas.elementos())), ('citação', md(cita))]
    elif achar(pg, lambda x: x.cls() == ['aula-capa']):
        ac = achar(pg, lambda x: x.cls() == ['aula-capa'])
        esq, dir_ = filho(ac, 'esq'), filho(ac, 'dir')
        ks = todos(esq, lambda x: x.cls() == ['k'])
        n = achar(esq, lambda x: x.cls() == ['n'])
        h1 = achar(dir_, lambda x: x.tag == 'h1')
        tex = achar(dir_, lambda x: x.cls() == ['tex'])
        vk = achar(dir_, lambda x: x.cls() == ['vk'])
        rot, cit = filho(vk, 'rot'), filho(vk, 'cit')
        campos += [('tipo', 'capa da aula'), ('número', md(n)), ('título', md(h1)), ('textos', md(tex))]
        r = md(rot)
        if r.startswith('Versículo-chave · '):
            campos.append(('referência', r[len('Versículo-chave · '):]))
        else:
            campos.append(('rótulo do versículo', r))
        campos.append(('versículo', md(cit, 'hl')))
        padrao_topo = f"{cab_aula.get('matéria')} · {cab_aula.get('aulas na matéria')} aulas"
        if md(ks[0]) != padrao_topo:
            campos.append(('topo', md(ks[0])))
        if md(ks[1]) != ident_nome:
            campos.append(('curso', md(ks[1])))
    elif achar(pg, lambda x: 'anim' in x.cls()):
        out_m = converter_mapa(pg, num, mapas_pedidos, avisos)
        campos = out_m[0]
        corpo = out_m[1]
        if secao:
            campos.insert(1, ('seção', secao))
        out += [f'{k}: {v}' for k, v in campos]
        return out + corpo
    else:
        sl = filho(pg, 'sl')
        if secao:
            campos.append(('seção', secao))
        for e in sl.elementos():
            if e.cls() == ['rot']:
                campos.append(('rótulo', md(e)))
            elif e.tag == 'h1' and e.cls() == ['t1']:
                campos.append(('título', md(e)))
            elif e.tag == 'h2' and e.cls() == ['t2']:
                campos.append(('título menor', md(e)))
        miolo = filho(sl, 'miolo')
        for b in miolo.elementos():
            try:
                r = converter_bloco(b, titulo)
            except Exception as e:  # estrutura inesperada: fica como html
                r = None
            if r is not None:
                linhas = texto_do_bloco(*r)
                if conferir_bloco(linhas, b.html()):
                    corpo += [''] + linhas
                    continue
                avisos.append(f'p. {num}: bloco "{r[0]}" não saiu idêntico; ficou como html')
            else:
                avisos.append(f'p. {num}: bloco <{b.tag} class="{b.a("class") or ""}"> sem tipo próprio; ficou como html')
            corpo += ['', '### html', b.html()]
        if any(isinstance(f, str) and f.strip() for f in miolo.filhos):
            avisos.append(f'p. {num}: texto solto no miolo (perdido na conversão!)')
    if 'capa' in cl or campos and campos[0][1] == 'capa da aula':
        if secao:
            campos.insert(1, ('seção', secao))
    padrao_ind = 'nao' if campos and campos[0][0] == 'tipo' and campos[0][1].startswith('capa') else 'sim'
    padrao_cab = 'nao' if campos and campos[0][0] == 'tipo' else 'sim'
    if pg.a('data-indice') != padrao_ind:
        campos.append(('sumário', 'não' if pg.a('data-indice') == 'nao' else 'sim'))
    if pg.a('data-cabecalho') != padrao_cab:
        campos.append(('cabeçalho', 'não' if pg.a('data-cabecalho') == 'nao' else 'sim'))
    if pg.a('data-tipo'):
        campos.append(('modo', pg.a('data-tipo')))
    out += [f'{k}: {v}' for k, v in campos]
    return out + corpo


def converter_mapa(pg, num, mapas_pedidos, avisos):
    a = achar(pg, lambda x: 'anim' in x.cls())
    rot = achar(a, lambda x: x.cls() == ['rot'])
    t2 = achar(a, lambda x: x.tag == 'h2')
    svg = achar(a, lambda x: x.tag == 'svg')
    nome = mapas_pedidos.get(num) or f'mapa-p{num}'
    # SVG-base: sem os trechos e focos da aula, sem id/estilo da página, marcador com id genérico
    base = No('svg', [x for x in svg.attrs if x[0] not in ('id', 'style')], None)
    base.filhos = [f for f in svg.filhos if not (isinstance(f, No) and (('seg' in f.cls()) or ('foco' in f.cls())))]
    txt = serial(base)
    txt = re.sub(r'id="(m\d+)-arr-\d+"', r'id="\1-arr"', txt)
    txt = re.sub(r'url\(#(m\d+)-arr-\d+\)', r'url(#\1-arr)', txt)
    destino = os.path.join(PASTA_MAPAS or os.path.join(MOTOR, 'mapas'), nome + '.svg')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, 'w', encoding='utf-8') as f:
        f.write(txt + '\n')
    cidades = mapas.cidades_do_svg(txt)
    por_coord = {}
    for k, v in cidades.items():
        por_coord.setdefault(v, k)

    def nome_ponto(x, y):
        return por_coord.get((x, y), f'{x},{y}')

    focos = {}
    for g in todos(svg, lambda x: 'foco' in x.cls()):
        pts = [(c.a('cx'), c.a('cy')) for c in g.elementos() if c.a('r') == '16']
        focos[g.a('data-cidade')] = pts
    segs = {}
    for s in todos(svg, lambda x: 'seg' in x.cls()):
        d = s.a('d')
        pts = re.findall(r'[ML](-?[\d.]+),(-?[\d.]+)', d)
        campo = 'trecho tracejado' if s.a('stroke-dasharray') else 'trecho'
        segs.setdefault(int(s.a('data-passo')), []).append(f'{campo}: ' + ' > '.join(nome_ponto(x, y) for x, y in pts))
    campos = [('tipo', 'mapa'), ('rótulo', md(rot)), ('mapa', nome), ('zoom', a.a('data-zoom'))]
    if md(t2) != pg.dado('data-titulo'):
        campos.append(('título', md(t2)))
    for sp in achar(a, lambda x: x.cls() == ['leg']).elementos():
        marca = sp.elementos()[0]
        tipo = {'i': {'': 'linha', 'd': 'tracejada', 'k': 'preta'}[marca.a('class') or ''], 'b': 'ponto'}[marca.tag]
        resto = No('x', [], None)
        resto.filhos = sp.filhos[1:]
        campos.append(('legenda', f'{tipo} | {serial(resto)[3:-4]}'))
    corpo = []
    usados = set()
    for cap in todos(a, lambda x: x.cls() == ['cap']):
        i = int(cap.a('data-passo'))
        cid = re.findall(r"'([^']*)'", a.a('data-cidades').replace('&#x27;', "'"))[i]
        corpo += ['', '### passo']
        if cid:
            pts = focos.get(cid, [])
            nomes = [nome_ponto(x, y) for x, y in pts]
            if (len(pts) == 1 and nomes[0] == cid) or cid in usados:
                corpo.append(f'cidade: {cid}')
            else:
                corpo.append(f'cidade: {cid} = ' + ' + '.join(nomes))
            usados.add(cid)
        corpo += ['título: ' + filho(cap, 't').interno(), 'texto: ' + filho(cap, 'd').interno()]
        corpo += segs.get(i, [])
    return campos, corpo


def main(argv):
    if len(argv) < 4:
        print(__doc__)
        return 1
    deck, ini, fim, saida = argv[0], int(argv[1]), int(argv[2]), argv[3]
    global PASTA_MAPAS
    PASTA_MAPAS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(saida))), 'mapas')
    pedidos, cab = {}, []
    resto = argv[4:]
    while resto:
        if resto[0] == '--mapa':
            n, nome = resto[1].split('=')
            pedidos[int(n)] = nome
        elif resto[0] == '--cabecalho':
            cab.append(resto[1])
        resto = resto[2:]
    with open(deck, encoding='utf-8') as f:
        h = f.read()
    corpo = h[h.index('<div id="palco">') + len('<div id="palco">'):h.index('<div id="trilha">')]
    raiz = arvore(corpo)
    slots = [x for x in raiz.elementos() if x.cls() == ['slot']]
    cab_aula = formato.Campos()
    for c in cab:
        k, v = c.split(': ', 1)
        cab_aula.add(k, v)
    ident_nome = 'Turma Especial'
    for c in cab:
        if c.startswith('nome do curso: '):
            ident_nome = c.split(': ', 1)[1]
    linhas = ['<!-- Conteúdo da aula, lido pelo motor (motor/README.md explica o formato). -->']
    linhas += [c for c in cab if not c.startswith('nome do curso: ')]
    avisos = []
    grupo = None
    for num in range(ini, fim + 1):
        s = slots[num - 1]
        g = s.elementos()[0].dado('data-aula') or ''
        if g != grupo and g:
            linhas += ['', f'# {g}']
        if g != grupo:
            grupo = g
        linhas += converter_pagina(s, num, pedidos, avisos, ident_nome, cab_aula)
    with open(saida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas) + '\n')
    print(f'ok: {saida} (páginas {ini} a {fim})')
    for a in avisos:
        print('  aviso:', a)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

"""Transforma as páginas e os blocos de uma aula em HTML, no molde do deck.

O HTML de cada tipo de bloco reproduz exatamente o que o motor do Cowork gerava
(referência: o deck final de Epístolas Paulinas II), para que as aulas antigas
saiam iguais quando refeitas por aqui.
"""
import html as H
import re

from formato import ErroFormato
import mapas

# espaço acima de um bloco: pequeno = 14 px, médio = 26 px, grande = 40 px
ESPACOS = {'pequeno': 'mt1', 'médio': 'mt', 'grande': 'mt2'}
CORES = {'vermelho': 'red', 'preto': 'blk', 'cinza': 'cz', None: ''}


def inline(s, destaque='r'):
    """Marcação dentro do texto: **negrito**, *itálico*, ==destaque em vermelho==.
    O resto passa como está (aceita HTML simples, como <br>)."""
    if s is None:
        return ''
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', s)
    s = re.sub(r'==(.+?)==', lambda m: f'<span class="{destaque}">{m.group(1)}</span>', s)
    return s


def attr(s):
    return H.escape(s or '', quote=True)


class Opcoes:
    def __init__(self, bloco):
        self.lista = bloco.opcoes
        self.bloco = bloco

    def tem(self, nome):
        return nome in self.lista

    def valor(self, prefixo):
        for o in self.lista:
            if o.startswith(prefixo + ' '):
                return o[len(prefixo) + 1:].strip()
        return None

    def espaco(self):
        v = self.valor('acima')
        if v is None:
            return ''
        if v not in ESPACOS:
            raise ErroFormato(self.bloco.linha, f'espaço "acima {v}": use pequeno, médio ou grande')
        return ESPACOS[v]


def cor(c, linha=0):
    if c not in CORES:
        raise ErroFormato(linha, f'cor "{c}": use vermelho, preto ou cinza')
    return CORES[c]


def _cls(*partes):
    return ' '.join(p for p in partes if p)


# ---------------------------------------------------------------- blocos
def b_texto(b, op, classe):
    tag = 'div' if classe == 'rot' else 'p'
    cl = [classe]
    if op.tem('grande'):
        cl.append('g')
    cl.append(op.espaco())
    st = ''
    abaixo = op.valor('abaixo')
    if abaixo:
        st = f' style="margin-bottom:{abaixo}"'
    return f'<{tag} class="{_cls(*cl)}"{st}>{inline(b.texto())}</{tag}>', False


def b_cartoes(b, op, extra=''):
    itens = b.itens(['rótulo', 'título', 'texto'])
    n = op.valor('colunas') or str(len(itens) if len(itens) <= 5 else 3)
    out = []
    for it in itens:
        h = f'<div class="card {cor(it.get("cor"), b.linha)}">'
        if 'rótulo' in it:
            h += f'<div class="k">{inline(it.get("rótulo"))}</div>'
        if 'título' in it:
            h += f'<div class="t">{inline(it.get("título"))}</div>'
        if 'texto' in it:
            h += f'<div class="d">{inline(it.get("texto"))}</div>'
        out.append(h + '</div>')
    return f'<div class="cards c{n} {extra}">' + ''.join(out) + '</div>', True


def b_aprendemos(b, op):
    itens = b.itens(['rótulo', 'título'])
    out = ''.join(f'<div class="card {cor(it.get("cor"), b.linha)}"><div class="k">{inline(it.get("rótulo"))}</div>'
                  f'<div class="t">{inline(it.get("título"))}</div></div>' for it in itens)
    return f'<div class="cards c2 aprend">{out}</div>', True


def b_lista(b, op):
    itens = b.itens(['título', 'texto'])
    duas = 'duas' if op.tem('duas colunas') else ''
    comp = 'compacta' if op.tem('compacta') else ''
    st = ''
    ini = op.valor('começa em')
    if ini:
        st = f' style="counter-reset:n {int(ini) - 1}"'
    lis = ''.join('<li><div><b>' + inline(it.get('título')) + '</b>' +
                  (f'<span>{inline(it.get("texto"))}</span>' if 'texto' in it else '') + '</div></li>' for it in itens)
    return f'<ol class="num {duas} {comp}"{st}>{lis}</ol>', True


def b_cadeia(b, op):
    itens = b.itens(['título', 'texto'])
    out = ''.join(f'<div class="ca {cor(it.get("cor"), b.linha)}"><b>{inline(it.get("título"))}</b>' +
                  (f'<small>{inline(it.get("texto"))}</small>' if 'texto' in it else '') + '</div>' for it in itens)
    return f'<div class="cadeia">{out}</div>', True


def b_par(b, op):
    itens = b.itens(['rótulo', 'título'])
    if len(itens) != 2:
        raise ErroFormato(b.linha, 'o bloco "par" tem exatamente dois lados')
    out = ''
    for it in itens:
        h = f'<div class="lado {cor(it.get("cor"), b.linha)}">'
        if 'rótulo' in it:
            h += f'<div class="k">{inline(it.get("rótulo"))}</div>'
        if 'título' in it:
            h += f'<div class="t">{inline(it.get("título"))}</div>'
        h += '<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in it.todos('item')) + '</ul>'
        out += h + '</div>'
    return f'<div class="par">{out}</div>', True


def b_faixa(b, op):
    c = b.campos()
    return f'<div class="faixa"><div class="k">{inline(c.get("rótulo"))}</div><b>{inline(c.get("texto"))}</b></div>', True


def b_chamada(b, op):
    c = b.campos()
    nota = c.get('nota')
    return f'<div class="chamada">{inline(c.get("texto"))}' + (f'<small>{inline(nota)}</small>' if nota else '') + '</div>', True


def b_versiculo(b, op, versoes):
    c = b.campos()
    g = 'g' if op.tem('grande') else ''
    texto = inline(c.get('texto'), 'hl')
    ref = c.get('referência')
    cmp_ = c.get('comparação')
    if cmp_:
        return versiculo_duas(texto, inline(cmp_, 'hl'), ref, g, op.valor('versões') or versoes), True
    longo = op.valor('longo')  # versículo de vários versos: letra menor, sem caixa-alta
    if longo:
        st = f' style="font-size:{longo};text-transform:none;font-weight:600;line-height:1.4"'
        return f'<div class="versiculo"><div class="cit"{st}>{texto}<span class="ref">{inline(ref)}</span></div></div>', True
    return f'<div class="versiculo"><div class="cit {g}">{texto}<span class="ref">{inline(ref)}</span></div></div>', True


def versiculo_duas(texto, cmp_, ref, g, versoes):
    """As duas versões na tela (BKJ 1611 principal + ARA de comparação).
    Três desenhos possíveis, escolhidos no campo 'versões na tela' da aula. Ainda não decidido."""
    if versoes == 'lado a lado':
        return (f'<div class="versiculo v2 ladoalado"><div class="col"><div class="ver">BKJ 1611</div><div class="cit {g}">{texto}</div></div>'
                f'<div class="col cmp"><div class="ver">ARA</div><div class="cit {g}">{cmp_}</div></div>'
                f'<span class="ref">{ref}</span></div>')
    if versoes == 'ao clicar':
        return (f'<div class="versiculo v2 clique"><div class="cit {g}">{texto}<span class="ref">{ref} · BKJ 1611</span></div>'
                f'<button class="vbtn" type="button">Comparar com a ARA</button>'
                f'<div class="cmp"><span class="ver">ARA</span>{cmp_}</div></div>')
    # padrão: a ARA menor, embaixo
    return (f'<div class="versiculo v2 embaixo"><div class="cit {g}">{texto}<span class="ref">{ref} · BKJ 1611</span></div>'
            f'<div class="cmp"><span class="ver">ARA</span>{cmp_}</div></div>')


def b_chips(b, op):
    itens = b.itens(['texto'])
    out = ''.join(f'<span class="{_cls("chip", cor(it.get("cor"), b.linha))}">{inline(it.get("texto"))}</span>' for it in itens)
    return f'<div class="chips">{out}</div>', True


def b_leitura(b, op):
    itens = b.itens(['dia', 'referência', 'nota'])
    out = ''.join(f'<div><div class="d">{inline(it.get("dia"))}</div><div class="r">{inline(it.get("referência"))}</div>' +
                  (f'<div class="s">{inline(it.get("nota"))}</div>' if 'nota' in it else '') + '</div>' for it in itens)
    return f'<div class="semana">{out}</div>', True


def b_ordem(b, op):
    itens = b.itens(['número', 'textos', 'título'])
    out = ''
    for it in itens:
        ab = '<div class="on">' if it.get('ativo') == 'sim' or it.get('cor') == 'vermelho' else '<div>'
        out += f'{ab}<div class="n">{inline(it.get("número"))}</div><div class="c">{inline(it.get("textos"))}</div><div class="t">{inline(it.get("título"))}</div></div>'
    return f'<div class="ordem">{out}</div>', True


def b_linha_do_tempo(b, op):
    itens = b.itens(['data', 'título', 'texto'])
    alt = op.valor('altura') or '300px'
    out = f'<div class="tl" style="height:{alt}">'
    for it in itens:
        out += (f'\n <div class="pt" style="left:{it.get("ponto")}"></div><div class="ev" style="left:{it.get("caixa")}">'
                f'<div class="d">{inline(it.get("data"))}</div><div class="t">{inline(it.get("título"))}</div><div class="s">{inline(it.get("texto"))}</div></div>')
    return out + '\n</div>', True


def b_tabela(b, op):
    linhas = [l.strip() for l in b.linhas if l.strip()]
    if len(linhas) < 2:
        raise ErroFormato(b.linha, 'tabela: cabeçalho, linha de separação (|---|) e linhas')

    def cels(l):
        l = l.strip()
        if l.startswith('|'):
            l = l[1:]
        if l.endswith('|'):
            l = l[:-1]
        return [c.strip() for c in l.split(' | ')] if ' | ' in l else [c.strip() for c in l.split('|')]

    def marca(c):
        m = re.match(r'^\{(rótulo|negrito|vermelho)\}\s*', c)
        return (m.group(1), c[m.end():]) if m else ('', c)

    rotulo = op.tem('rótulo na 1ª coluna')
    ths = ''
    for c in cels(linhas[0]):
        k, t = marca(c)
        ths += f'<th class="{"r" if k == "vermelho" else ""}">{inline(t)}</th>'
    trs = ''
    for l in linhas[2:]:
        tds = ''
        for i, c in enumerate(cels(l)):
            k, t = marca(c)
            cl = {'rótulo': 'k', 'negrito': 'b'}.get(k, 'k' if (rotulo and i == 0) else '')
            tds += f'<td class="{cl}">{inline(t)}</td>'
        trs += f'<tr>{tds}</tr>'
    gr = 'grande' if op.tem('grande') else ''
    return f'<table class="tb {gr}"><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table>', True


def b_espaco(b, op):
    alt = op.lista[0] if op.lista else '10px'
    if alt in ESPACOS:
        return f'<div class="{ESPACOS[alt]}"></div>', False
    return f'<div style="height:{alt}"></div>', False


def b_html(b, op):
    return '\n'.join(b.linhas).strip('\n'), False


def bloco(b, versoes):
    op = Opcoes(b)
    t = b.tipo
    if t in ('frase', 'desafio'):
        if t == 'desafio' and not op.tem('grande'):
            op.lista = op.lista + ['grande']
        h, envolve = b_texto(b, op, 'frase')
    elif t == 'texto':
        h, envolve = b_texto(b, op, 'corpo')
    elif t == 'nota':
        h, envolve = b_texto(b, op, 'nota')
    elif t == 'rótulo':
        h, envolve = b_texto(b, op, 'rot')
    elif t == 'cartões':
        h, envolve = b_cartoes(b, op)
    elif t == 'aprendemos':
        h, envolve = b_aprendemos(b, op)
    elif t == 'lista':
        h, envolve = b_lista(b, op)
    elif t == 'cadeia':
        h, envolve = b_cadeia(b, op)
    elif t == 'par':
        h, envolve = b_par(b, op)
    elif t == 'faixa':
        h, envolve = b_faixa(b, op)
    elif t == 'chamada':
        h, envolve = b_chamada(b, op)
    elif t == 'versículo':
        h, envolve = b_versiculo(b, op, versoes)
    elif t == 'chips':
        h, envolve = b_chips(b, op)
    elif t == 'leitura':
        h, envolve = b_leitura(b, op)
    elif t == 'ordem':
        h, envolve = b_ordem(b, op)
    elif t == 'linha do tempo':
        h, envolve = b_linha_do_tempo(b, op)
    elif t == 'tabela':
        h, envolve = b_tabela(b, op)
    elif t == 'espaço':
        h, envolve = b_espaco(b, op)
    elif t == 'html':
        h, envolve = b_html(b, op)
    else:
        raise ErroFormato(b.linha, f'tipo de bloco desconhecido: "{t}" (veja a lista no motor/README.md)')
    if envolve:
        mt = op.espaco()
        if mt:
            h = f'<div class="{mt}">{h}</div>'
    return h


# ---------------------------------------------------------------- páginas
def pagina(p, idx, aula, ident):
    c = p.campos
    tipo = c.get('tipo', 'normal')
    grupo = c.get('aula', p.grupo)
    automatico_nao = tipo in ('capa do curso', 'capa da aula', 'mapa')
    indice = c.get('sumário', 'não' if tipo in ('capa do curso', 'capa da aula') else 'sim')
    cab = c.get('cabeçalho', 'não' if automatico_nao else 'sim')
    classes = {'capa do curso': 'capa vermelha'}.get(tipo, '')
    fundo = c.get('fundo')
    if fundo:
        classes = _cls(classes, {'vermelho': 'vermelha', 'preto': 'preta'}[fundo])
    versoes = aula.campos.get('versões na tela', 'embaixo')

    if tipo == 'capa do curso':
        corpo = capa_curso(p, ident)
    elif tipo == 'capa da aula':
        corpo = capa_aula(p, aula, ident, versoes)
    elif tipo == 'mapa':
        corpo = mapas.pagina_mapa(p, idx, ident)
    elif tipo == 'normal':
        corpo = '<div class="sl">'
        if 'rótulo' in c:
            corpo += f'<div class="rot">{inline(c.get("rótulo"))}</div>'
        if 'título' in c:
            corpo += f'<h1 class="t1">{inline(c.get("título"))}</h1>'
        elif 'título menor' in c:
            corpo += f'<h2 class="t2">{inline(c.get("título menor"))}</h2>'
        corpo += '<div class="miolo">' + ''.join(bloco(b, versoes) for b in p.blocos) + '</div></div>'
    else:
        raise ErroFormato(p.linha, f'tipo de página desconhecido: "{tipo}"')

    sn = lambda v: 'nao' if v == 'não' else 'sim'
    return (f'<div class="slot"><div class="pagina {classes}" data-titulo="{attr(p.titulo)}" data-secao="{attr(c.get("seção", ""))}" '
            f'data-aula="{attr(grupo)}" data-tipo="{attr(c.get("modo", ""))}" data-indice="{sn(indice)}" data-cabecalho="{sn(cab)}">'
            f'{corpo}</div></div>')


def capa_curso(p, ident):
    c = p.campos
    cartas = ''.join(f'<span>{inline(x.strip())}</span>' for x in c.get('cartas', '').split('|') if x.strip())
    return (f'<div class="capa"><div class="box">\n <div class="topo"><div class="curso">{inline(c.get("curso", ident.nome))}</div>'
            f'<img src="{ident.logo_claro}" style="height:34px"></div>\n'
            f' <div><div class="lock">{inline(c.get("título"))}</div>\n  <div class="cartas">{cartas}</div></div>\n'
            f' <div class="cita">{inline(c.get("citação"))}</div>\n</div></div>')


def capa_aula(p, aula, ident, versoes):
    c = p.campos
    materia = aula.campos.get('matéria', '')
    total = aula.campos.get('aulas na matéria')
    topo = c.get('topo', f'{materia} · {total} aulas' if total else materia)
    vers = inline(c.get('versículo'), 'hl')
    cmp_ = c.get('comparação')
    rot = c.get('rótulo do versículo', 'Versículo-chave · ' + (c.get('referência') or ''))
    if cmp_:
        vk = (f'<div class="rot">{inline(rot)}</div><div class="cit">{vers}</div>'
              f'<div class="cmp"><span class="ver">ARA</span>{inline(cmp_, "hl")}</div>')
    else:
        vk = f'<div class="rot">{inline(rot)}</div><div class="cit">{vers}</div>'
    return (f'<div class="aula-capa">\n <div class="esq"><div><img src="{ident.logo_escuro}" style="height:30px">'
            f'<div class="k" style="margin-top:28px">{inline(topo)}</div></div>\n'
            f'  <div><div class="lab">Aula</div><div class="n">{inline(c.get("número"))}</div></div>\n'
            f'  <div class="k">{inline(c.get("curso", ident.nome))}</div></div>\n'
            f' <div class="dir"><h1>{inline(c.get("título"))}</h1><div class="tex">{inline(c.get("textos"))}</div>\n'
            f'  <div class="vk">{vk}</div></div>\n</div>')

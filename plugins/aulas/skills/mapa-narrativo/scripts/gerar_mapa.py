#!/usr/bin/env python3
"""Monta o mapa narrativo: um mapa que conta a aula passo a passo, cena a cena.

Uso (a partir da pasta da skill):
    python3 scripts/gerar_mapa.py <pasta-do-mapa>            # gera mapa.html
    python3 scripts/gerar_mapa.py <pasta-do-mapa> --svg      # gera também svg/cena-N.svg, um mapa parado por cena

A pasta do mapa tem:
    cenas.md      o roteiro de cenas (uma cena por "## "), onde se corrige. O cabeçalho aceita
                  "quadro: lon_min lat_min lon_max lat_max" para escolher a região do mapa
    lugares.csv   nome, lon, lat, destaque, cor, rótulo_dx, rótulo_dy, fonte
    rotas.md      (opcional) as rotas nomeadas, com os pontos de cada trecho
    regioes.csv   (opcional) os rótulos de região, mar e rio, com a faixa de zoom
Sai um arquivo só (mapa.html), com as fontes e o litoral dentro: abre sem internet, em qualquer computador.

Só Python 3, sem biblioteca. O motor recusa lugar que não está em lugares.csv e trecho de percurso
que não está na rota citada: o mapa não inventa caminho.
"""
import csv, json, math, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent

# Quadro padrão: o do mapa das Cartas Paulinas (Mediterrâneo oriental), 1200 x 760.
QUADRO_PADRAO = [8.9966, 30.2995, 40.7858, 46.0124]
LARGURA = 1200
ALTURA = 760
_P = {}


class Erro(Exception):
    pass


def _merc(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def configurar(quadro):
    """Mercator ajustada ao quadro, com 1200 px de largura."""
    global ALTURA
    lon0, lat0, lon1, lat1 = quadro
    if not (lon1 > lon0 and lat1 > lat0):
        raise Erro('quadro: precisa ser lon_min lat_min lon_max lat_max, com o máximo maior que o mínimo')
    k = LARGURA / math.radians(lon1 - lon0)
    ymax = _merc(lat1)
    ALTURA = round((ymax - _merc(lat0)) * k)
    _P.update(k=k, lon0=lon0, ymax=ymax, quadro=quadro)


def projetar(lon, lat):
    return [round((lon - _P['lon0']) * math.pi / 180 * _P['k'], 2), round((_P['ymax'] - _merc(lat)) * _P['k'], 2)]


def biblioteca_nomes():
    arq = AQUI / 'biblioteca' / 'lugares.csv'
    return {l['nome'] for l in csv.DictReader(open(arq, encoding='utf-8'))} if arq.exists() else set()


def ler_lugares(pasta):
    lugares = {}
    for l in csv.DictReader(open(pasta / 'lugares.csv', encoding='utf-8')):
        x, y = projetar(float(l['lon']), float(l['lat']))
        lugares[l['nome']] = {
            'n': l['nome'], 'x': x, 'y': y, 'chave': l['destaque'] == 'sim', 'cor': l['cor'] or None,
            'dx': float(l.get('rótulo_dx') or 8), 'dy': float(l.get('rótulo_dy') or 4), 'fonte': l['fonte']}
    return lugares


def ler_regioes(pasta):
    arq = pasta / 'regioes.csv'
    if not arq.exists():
        return []
    out = []
    for r in csv.DictReader(open(arq, encoding='utf-8')):
        x, y = projetar(float(r['lon']), float(r['lat']))
        out.append({'t': r['texto'], 'x': x, 'y': y, 'tipo': r['tipo'],
                    'z0': float(r['zoom_min']), 'z1': float(r['zoom_max'])})
    return out


def ponto(txt, lugares, onde):
    txt = txt.strip()
    m = re.fullmatch(r'\(\s*(-?[\d.]+)\s+(-?[\d.]+)\s*\)', txt)
    if m:
        return txt, projetar(float(m.group(1)), float(m.group(2)))
    if txt not in lugares:
        dica = ' Ele existe em biblioteca/lugares.csv: copie a linha para o lugares.csv deste mapa.' if txt in biblioteca_nomes() else \
            ' Acrescente a linha em lugares.csv com a longitude, a latitude e a fonte da coordenada (não invente).'
        raise Erro(f'{onde}: o lugar "{txt}" não está em lugares.csv.' + dica)
    return txt, [lugares[txt]['x'], lugares[txt]['y']]


def ler_rotas(pasta, lugares):
    rotas, atual = {}, None
    if not (pasta / 'rotas.md').exists():
        return rotas
    for n, linha in enumerate(open(pasta / 'rotas.md', encoding='utf-8'), 1):
        linha = linha.rstrip()
        if linha.startswith('## '):
            atual = linha[3:].strip()
            rotas[atual] = {'fonte': '', 'trechos': []}
        elif atual and ':' in linha and not linha.startswith('>'):
            campo, valor = linha.split(':', 1)
            campo = campo.strip()
            if campo == 'fonte':
                rotas[atual]['fonte'] = valor.strip()
            elif campo in ('terra', 'mar', 'estrada', 'tracejada', 'rio'):
                nomes = [p.strip() for p in valor.split('>')]
                for p in nomes:
                    ponto(p, lugares, f'rotas.md, linha {n}')
                rotas[atual]['trechos'].append({'tipo': campo, 'nomes': nomes})
    return rotas


def trecho_valido(rota, nomes):
    """O percurso tem de ser uma sequência contínua de um trecho da rota (em qualquer sentido)."""
    for t in rota['trechos']:
        for seq in (t['nomes'], t['nomes'][::-1]):
            for i in range(len(seq) - len(nomes) + 1):
                if seq[i:i + len(nomes)] == nomes:
                    return t['tipo']
    return None


def ler_cenas(pasta, lugares, rotas):
    texto = re.sub(r'<!--.*?-->', '', open(pasta / 'cenas.md', encoding='utf-8').read(), flags=re.S)
    cabeca, *blocos = re.split(r'^## ', texto, flags=re.M)
    meta = {}
    for linha in cabeca.splitlines():
        if ':' in linha:
            k, v = linha.split(':', 1)
            meta[k.strip()] = v.strip()
    cenas = []
    for bloco in blocos:
        linhas = bloco.splitlines()
        nome = linhas[0].strip()
        onde = f'cenas.md, cena "{nome}"'
        c = {'nome': nome, 'percursos': [], 'cartas': [], 'acender': []}
        for linha in linhas[1:]:
            if ':' not in linha:
                continue
            k, v = linha.split(':', 1)
            k, v = k.strip(), v.strip()
            if k == 'percurso':
                nome_rota, pts = v.split(':', 1)
                nome_rota = nome_rota.strip()
                if nome_rota not in rotas:
                    raise Erro(f'{onde}: a rota "{nome_rota}" não está em rotas.md')
                nomes = [p.strip() for p in pts.split('>')]
                tipo = trecho_valido(rotas[nome_rota], nomes)
                if not tipo:
                    raise Erro(f'{onde}: o trecho "{pts.strip()}" não está na rota "{nome_rota}"')
                c['percursos'].append({'rota': nome_rota, 'tipo': tipo, 'nomes': nomes,
                                       'pts': [ponto(p, lugares, onde)[1] for p in nomes]})
            elif k == 'carta':
                trajeto, rot = (v.split('|', 1) + [''])[:2]
                a, b = [p.strip() for p in trajeto.split('>')]
                c['cartas'].append({'a': ponto(a, lugares, onde)[1], 'b': ponto(b, lugares, onde)[1],
                                    'de': a, 'para': b, 'rot': rot.strip()})
            elif k == 'acender':
                c['acender'] = [p.strip() for p in v.split(',') if p.strip()]
                for p in c['acender']:
                    ponto(p, lugares, onde)
            elif k == 'duração':
                c['dur'] = float(v)
            else:
                c[k] = v
        c['cam'] = camera(c.get('câmera', 'geral'), lugares, onde)
        for campo in ('título', 'texto', 'fonte'):
            if not c.get(campo):
                raise Erro(f'{onde}: falta o campo "{campo}"')
        cenas.append(c)
    return meta, cenas


def camera(v, lugares, onde):
    """Devolve a caixa (x0, y0, x1, y1) que a cena precisa mostrar inteira."""
    if v == 'geral':
        return [0, 0, LARGURA, ALTURA]
    m = re.fullmatch(r'foco (.+?) ([\d.]+)', v)
    if m:
        _, (x, y) = ponto(m.group(1), lugares, onde)
        z = float(m.group(2))
        w, h = LARGURA / z, ALTURA / z
        return [x - w / 2, y - h / 2, x + w / 2, y + h / 2]
    m = re.fullmatch(r'enquadrar (.+?)(?: folga ([\d.]+))?', v)
    if m:
        pts = [ponto(p, lugares, onde)[1] for p in m.group(1).split(',')]
        f = float(m.group(2) or 1.3)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        w, h = max(max(xs) - min(xs), 20) * f, max(max(ys) - min(ys), 14) * f
        return [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
    raise Erro(f'{onde}: câmera "{v}" não reconhecida (use: geral · foco <lugar> <zoom> · enquadrar <lugar>, <lugar> [folga N])')



def caminho_terra():
    """O litoral (base/terra.json, lon/lat) projetado no quadro: só os polígonos que tocam o quadro."""
    dados = json.load(open(AQUI / 'base' / 'terra.json', encoding='utf-8'))
    lon0, lat0, lon1, lat1 = _P['quadro']
    folga = 2.0
    partes = []
    for aneis in dados['poligonos']:
        xs = [p[0] for p in aneis[0]]
        ys = [p[1] for p in aneis[0]]
        if max(xs) < lon0 - folga or min(xs) > lon1 + folga or max(ys) < lat0 - folga or min(ys) > lat1 + folga:
            continue
        for anel in aneis:
            pts, ultimo = [], None
            for lon, lat in anel:
                lat = max(min(lat, 84), -84)
                p = projetar(lon, lat)
                p = [round(p[0], 1), round(p[1], 1)]
                if p != ultimo:
                    pts.append(p)
                    ultimo = p
            if len(pts) >= 3:
                partes.append('M' + 'L'.join(f'{x},{y}' for x, y in pts) + 'Z')
    quadro_dados = dados['quadro']
    if lon0 < quadro_dados[0] or lat0 < quadro_dados[1] or lon1 > quadro_dados[2] or lat1 > quadro_dados[3]:
        raise Erro(f'o quadro {_P["quadro"]} passa da base de litoral {quadro_dados}. '
                   'Refaça a base com scripts/recortar_natural_earth.py (instruções no topo do script).')
    return ''.join(partes)


def ler_meta_quadro(pasta):
    texto = (pasta / 'cenas.md').read_text(encoding='utf-8')
    cabeca = re.split(r'^## ', texto, flags=re.M)[0]
    cabeca = re.sub(r'<!--.*?-->', '', cabeca, flags=re.S)
    for linha in cabeca.splitlines():
        if linha.startswith('quadro:'):
            try:
                return [float(v) for v in linha.split(':', 1)[1].split()]
            except ValueError:
                raise Erro('cenas.md: "quadro:" precisa de quatro números (lon_min lat_min lon_max lat_max)')
    return QUADRO_PADRAO


# ---------- SVG parado, um por cena ----------
def svg_cena(c, dados, terra, fontes):
    """Um mapa parado da cena (16:9, 1920 x 1080), para slide ou impressão."""
    x0, y0, x1, y1 = c['cam']
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w, h = x1 - x0, y1 - y0
    if w / h < 16 / 9:
        w = h * 16 / 9
    else:
        h = w * 9 / 16
    w = min(w, LARGURA)
    h = w * 9 / 16
    vx = min(max(cx - w / 2, 0), LARGURA - w)
    vy = min(max(cy - h / 2, 0), ALTURA - h)
    u = w / 1920                      # unidades do mapa por pixel de saída
    zoom = LARGURA / w
    esc = lambda t: t.replace('&', '&amp;').replace('<', '&lt;')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {w:.2f} {h:.2f}" width="1920" height="1080">',
         f'<style>{fontes}\ntext{{font-family:"Crimson Text",Georgia,serif}} .cz{{font-family:"Cinzel",Georgia,serif}}</style>',
         f'<defs><path id="costa" d="{terra}"/></defs>',
         f'<rect x="{vx - 10:.1f}" y="{vy - 10:.1f}" width="{w + 20:.1f}" height="{h + 20:.1f}" fill="#a3bbb5"/>',
         f'<use href="#costa" fill="none" stroke="#7b9893" stroke-opacity=".5" stroke-width="{4.5 * u:.3f}" stroke-linejoin="round"/>',
         f'<use href="#costa" fill="#efe2c2" fill-rule="evenodd" stroke="#5b4630" stroke-width="{1.3 * u:.3f}" stroke-linejoin="round"/>']
    for r in dados['regioes']:
        if r['z0'] <= zoom <= r['z1'] and vx <= r['x'] <= vx + w and vy <= r['y'] <= vy + h:
            estilo = ('font-style="italic" fill="#4f6a66"' if r['tipo'] == 'mar' else
                      'font-style="italic" fill="#4a6f93"' if r['tipo'] == 'rio' else
                      'class="cz" font-weight="600" fill="#6b5638" fill-opacity=".75"')
            o.append(f'<text x="{r["x"]}" y="{r["y"]}" text-anchor="middle" font-size="{(17 if r["tipo"] != "região" else 14) * 2.2 * u:.3f}" '
                     f'letter-spacing="{.3 * 17 * 2.2 * u:.2f}" {estilo}>{esc(r["t"])}</text>')
    estilos = {'terra': 'stroke="#7a1f12" stroke-width="{0}" stroke-dasharray="{1} {2}"',
               'mar': 'stroke="#24435f" stroke-width="{0}" stroke-dasharray="{1} {2}"',
               'estrada': 'stroke="#5a4a2a" stroke-width="{0}"',
               'tracejada': 'stroke="#7a1f12" stroke-width="{0}" stroke-dasharray="{1} {2}" stroke-opacity=".8"',
               'rio': 'stroke="#5f86ad" stroke-width="{0}"'}
    larg = {'terra': (4, .1, 9), 'mar': (2.6, 11, 7), 'estrada': (3.2, 0, 0), 'tracejada': (2.4, 6, 6), 'rio': (3, 0, 0)}
    for p in c['percursos']:
        a, b, d = larg[p['tipo']]
        atr = estilos[p['tipo']].format(f'{a * 2.2 * u:.3f}', f'{b * 2.2 * u:.3f}', f'{d * 2.2 * u:.3f}')
        pts = 'M' + 'L'.join(f'{x},{y}' for x, y in p['pts'])
        o.append(f'<path d="{pts}" fill="none" stroke-linecap="round" stroke-linejoin="round" {atr}/>')
    acesos = set(c['acender'])
    for l in dados['lugares']:
        if not (vx - 5 * u <= l['x'] <= vx + w + 5 * u and vy - 5 * u <= l['y'] <= vy + h + 5 * u):
            continue
        if not l['chave'] and zoom < 1.6 and l['n'] not in acesos:
            continue
        aceso = l['n'] in acesos
        cor = '#7a1f12' if aceso else '#2a1d10'
        s = 2.2 * u
        if l['chave']:
            o.append(f'<circle cx="{l["x"]}" cy="{l["y"]}" r="{6.5 * s:.3f}" fill="{l["cor"] or "#7a1f12"}" stroke="#2a1d10" stroke-width="{1.2 * s:.3f}"/>')
        else:
            o.append(f'<circle cx="{l["x"]}" cy="{l["y"]}" r="{3.8 * s:.3f}" fill="#f6ecd2" stroke="#2a1d10" stroke-width="{1.6 * s:.3f}"/>')
        if aceso:
            o.append(f'<circle cx="{l["x"]}" cy="{l["y"]}" r="{10 * s:.3f}" fill="none" stroke="#7a1f12" stroke-width="{2.2 * s:.3f}" stroke-opacity=".7"/>')
        tam = (18 if l['chave'] else 15) * s
        cls = ' class="cz"' if l['chave'] else ''
        o.append(f'<text x="{l["x"] + l["dx"] * 1.15 * s:.2f}" y="{l["y"] + (l["dy"] * 1.15 + (2 if l["dy"] > 0 else 0)) * s:.2f}" '
                 f'font-size="{tam:.3f}" font-weight="{700 if l["chave"] else 600}" fill="{cor}" paint-order="stroke" '
                 f'stroke="#efe2c2" stroke-width="{4 * s:.3f}" stroke-linejoin="round"{cls}>{esc(l["n"])}</text>')
    nota = 'Litorais: Natural Earth 10m (domínio público)' + (f' · {c["nota"]}' if c.get('nota') else '')
    o.append(f'<text x="{vx + 24 * u:.2f}" y="{vy + h - 18 * u:.2f}" font-size="{22 * u:.3f}" fill="#2a1d10" fill-opacity=".7" '
             f'paint-order="stroke" stroke="#efe2c2" stroke-width="{3 * u:.3f}">{esc(nota)}</text>')
    o.append(f'<rect x="{vx + 6 * u:.2f}" y="{vy + 6 * u:.2f}" width="{w - 12 * u:.2f}" height="{h - 12 * u:.2f}" fill="none" stroke="#5a401e" stroke-opacity=".8" stroke-width="{2 * u:.3f}"/>')
    o.append('</svg>')
    return '\n'.join(o)


def gerar(pasta, com_svg=False):
    pasta = Path(pasta)
    if not (pasta / 'cenas.md').exists() or not (pasta / 'lugares.csv').exists():
        raise Erro(f'a pasta {pasta} precisa ter cenas.md e lugares.csv (veja exemplo/)')
    configurar(ler_meta_quadro(pasta))
    lugares = ler_lugares(pasta)
    rotas = ler_rotas(pasta, lugares)
    meta, cenas = ler_cenas(pasta, lugares, rotas)
    dados = {
        'meta': meta, 'base': [LARGURA, ALTURA],
        'lugares': list(lugares.values()), 'regioes': ler_regioes(pasta),
        'rotas': {k: v['fonte'] for k, v in rotas.items()}, 'cenas': cenas,
    }
    terra = caminho_terra()
    fontes = (AQUI / 'molde' / 'fontes.css').read_text(encoding='utf-8')
    molde = (AQUI / 'molde' / 'viagem.html').read_text(encoding='utf-8')
    html = (molde
            .replace('/*FONTES*/', fontes)
            .replace('/*CSS*/', (AQUI / 'molde' / 'viagem.css').read_text(encoding='utf-8'))
            .replace('/*JS*/', (AQUI / 'molde' / 'viagem.js').read_text(encoding='utf-8'))
            .replace('__LITORAL__', terra)
            .replace('__CREDITO__', f' · {meta["crédito"]}' if meta.get('crédito') else '')
            .replace('__TITULO__', meta.get('título', 'Mapa narrativo'))
            .replace('/*DADOS*/', 'const DADOS=' + json.dumps(dados, ensure_ascii=False) + ';'))
    saida = pasta / 'mapa.html'
    saida.write_text(html, encoding='utf-8')
    total = sum(c.get('dur', 0) for c in cenas)
    print(f'{saida}: {len(cenas)} cenas, {len(lugares)} lugares, {total:.0f} s no modo automático')
    if com_svg:
        pasta_svg = pasta / 'svg'
        pasta_svg.mkdir(exist_ok=True)
        for i, c in enumerate(cenas, 1):
            (pasta_svg / f'cena-{i}.svg').write_text(svg_cena(c, dados, terra, fontes), encoding='utf-8')
        print(f'{pasta_svg}: {len(cenas)} mapas parados (cena-N.svg)')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 1:
        sys.exit(__doc__)
    try:
        gerar(args[0], '--svg' in sys.argv)
    except Erro as e:
        sys.exit(f'ERRO: {e}')

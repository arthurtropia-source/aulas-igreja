#!/usr/bin/env python3
"""Recorta o litoral da Natural Earth (camada ne_10m_land, GeoJSON) a um retângulo e grava base/terra.json.

Só é preciso rodar isto para REFAZER a base (por exemplo, para outra região do mundo).
O repositório já traz base/terra.json pronto (mundo bíblico), então quem só faz mapas não precisa disto.

Uso:
    python3 scripts/recortar_natural_earth.py ne_10m_land.geojson base/terra.json [lon_min lat_min lon_max lat_max]
O retângulo padrão é -12 8 62 48 (da Espanha à Pérsia, do sul da Turquia à Etiópia).

Onde baixar o arquivo (domínio público, ~10 MB):
    https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson
Só Python 3, sem biblioteca.
"""
import json
import sys


def recortar_anel(anel, x0, y0, x1, y1):
    """Sutherland-Hodgman contra o retângulo."""
    def dentro(p, lado):
        return (p[0] >= x0, p[0] <= x1, p[1] >= y0, p[1] <= y1)[lado]

    def cruza(a, b, lado):
        if lado < 2:
            x = x0 if lado == 0 else x1
            t = (x - a[0]) / (b[0] - a[0])
            return (x, a[1] + t * (b[1] - a[1]))
        y = y0 if lado == 2 else y1
        t = (y - a[1]) / (b[1] - a[1])
        return (a[0] + t * (b[0] - a[0]), y)

    pts = anel[:-1] if anel[0] == anel[-1] else anel
    for lado in range(4):
        if not pts:
            break
        novo = []
        for i, b in enumerate(pts):
            a = pts[i - 1]
            if dentro(b, lado):
                if not dentro(a, lado):
                    novo.append(cruza(a, b, lado))
                novo.append(b)
            elif dentro(a, lado):
                novo.append(cruza(a, b, lado))
        pts = novo
    return pts


def main():
    if len(sys.argv) not in (3, 7):
        sys.exit(__doc__)
    quadro = [float(v) for v in sys.argv[3:7]] if len(sys.argv) == 7 else [-12, 8, 62, 48]
    x0, y0, x1, y1 = quadro
    dados = json.load(open(sys.argv[1], encoding='utf-8'))
    poligonos = []
    for f in dados['features']:
        g = f['geometry']
        polis = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poli in polis:
            xs = [p[0] for p in poli[0]]
            ys = [p[1] for p in poli[0]]
            if max(xs) < x0 or min(xs) > x1 or max(ys) < y0 or min(ys) > y1:
                continue
            aneis = []
            for anel in poli:
                r = recortar_anel([tuple(p[:2]) for p in anel], x0, y0, x1, y1)
                if len(r) >= 3:
                    aneis.append([[round(x, 3), round(y, 3)] for x, y in r])
            if aneis:
                poligonos.append(aneis)
    saida = {
        'fonte': 'Natural Earth, camada ne_10m_land (1:10m), domínio público: naturalearthdata.com/about/terms-of-use/',
        'quadro': quadro,
        'poligonos': poligonos,
    }
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        json.dump(saida, f, ensure_ascii=False, separators=(',', ':'))
    print(f'{len(poligonos)} polígonos, quadro {quadro} -> {sys.argv[2]}')


if __name__ == '__main__':
    main()

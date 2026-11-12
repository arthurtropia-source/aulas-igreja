#!/usr/bin/env python3
"""Exporta um deck HTML para PDF (uma folha de 1280 × 720 por página). Só quando pedido.

  python3 pdf.py <pasta-da-aula>/aula-1.html
      -> aula-1/aula-1.pdf

Usa o CSS de impressão que corrigiu o deslocamento de 56 px (08/10/2026):
  .slot{height:720px;break-after:page} e .pagina{transform:none;margin:0}.
Os mapas por passos saem na visão geral (passo 0).
Depois de exportar, confira a primeira página do PDF: o topo da página tem de bater com o topo da folha.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from navegador import Deck  # noqa: E402


def exportar(html, destino=None):
    destino = destino or os.path.splitext(html)[0] + '.pdf'
    with Deck(html) as d:
        d.pg.emulate_media(media='print')
        d.pg.wait_for_timeout(300)
        # conferência do deslocamento: o topo da 1ª página tem de estar no 0
        topo = d.pg.evaluate("Math.round(document.querySelector('.pagina').getBoundingClientRect().top+scrollY)")
        d.pg.pdf(path=destino, width='1280px', height='720px', print_background=True)
        n = len(d.paginas())
    return destino, n, topo


def main(args):
    if not args:
        print(__doc__)
        return 1
    destino, n, topo = exportar(args[0], args[1] if len(args) > 1 else None)
    print(f'ok: {destino} ({n} páginas)')
    if topo != 0:
        print(f'  FALHA: a primeira página começa {topo} px abaixo do topo da folha (deslocamento)')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

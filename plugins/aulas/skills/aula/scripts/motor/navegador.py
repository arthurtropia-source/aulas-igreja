"""Funções comuns às conferências, à exportação de PDF e à comparação: abrir o HTML num Chromium
sem janela (Playwright), mostrar as páginas em tamanho real (1280 × 720, sem a escala da tela)
e fotografar cada página e cada passo dos mapas."""
import base64
import os
import pathlib

from playwright.sync_api import sync_playwright

# Mesmo CSS da exportação de PDF que corrigiu o deslocamento de 56 px (08/10/2026):
# a página sai do palco rolável, perde a escala e a margem de compensação, e cada slot vira uma folha.
CSS_IMPRESSAO = ('@page{size:1280px 720px;margin:0}html,body{margin:0;height:auto;overflow:visible}'
                 '#barra,#trilha,#sumario,#irpara,#aviso{display:none!important}'
                 '#palco{height:auto!important;overflow:visible!important;scroll-snap-type:none}'
                 '.slot{height:720px!important;break-after:page;page-break-after:always;display:block}'
                 '.pagina{transform:none!important;margin:0!important}')

ESPERA_PASSO_MS = 1400  # o trecho leva 1,1 s para se desenhar e o zoom 0,9 s


class Deck:
    def __init__(self, caminho):
        self.caminho = os.path.abspath(caminho)

    def __enter__(self):
        self._pw = sync_playwright().start()
        self.nav = self._pw.chromium.launch()
        self.pg = self.nav.new_page(viewport={'width': 1280, 'height': 720})
        self.pg.goto(pathlib.Path(self.caminho).as_uri(), wait_until='load')
        self.pg.evaluate('document.fonts.ready')
        self.pg.wait_for_timeout(600)
        self.pg.add_style_tag(content=CSS_IMPRESSAO)
        self.pg.wait_for_timeout(200)
        return self

    def __exit__(self, *a):
        self.nav.close()
        self._pw.stop()

    def paginas(self):
        return self.pg.query_selector_all('.pagina')

    def foto(self, i, destino):
        el = self.paginas()[i]
        el.scroll_into_view_if_needed()
        el.screenshot(path=destino)
        return destino

    def mapas(self):
        """Índices das páginas com mapa por passos e o número de passos de cada uma."""
        return self.pg.evaluate("""[...document.querySelectorAll('.pagina')].map((p,i)=>{
            const a=p.querySelector('.pg-mapa.anim');return a?[i,+a.dataset.passos]:null}).filter(Boolean)""")

    def ir_ao_passo(self, i, passo):
        self.pg.evaluate("""([i,s])=>{const a=document.querySelectorAll('.pagina')[i].querySelector('.pg-mapa.anim');
            while(+a.dataset.cur<s)a.__passo(1);while(+a.dataset.cur>s)a.__passo(-1);}""", [i, passo])
        self.pg.wait_for_timeout(ESPERA_PASSO_MS)


def folha_de_contato(fotos, destino, colunas=4, largura=400, rotulos=None, proporcao=720 / 1280):
    """Junta as fotos numa imagem só (feita no próprio navegador: não precisa de outra biblioteca)."""
    alt = int(largura * proporcao)
    cel = []
    for k, f in enumerate(fotos):
        with open(f, 'rb') as fh:
            b = base64.b64encode(fh.read()).decode()
        r = rotulos[k] if rotulos else os.path.splitext(os.path.basename(f))[0]
        cel.append(f'<figure><img src="data:image/png;base64,{b}"><figcaption>{r}</figcaption></figure>')
    html = ('<html><body style="margin:0;background:#141213;font:600 12px Arial;color:#fff">'
            f'<div style="display:grid;grid-template-columns:repeat({colunas},{largura}px);gap:10px;padding:10px">'
            + ''.join(cel) + '</div><style>figure{margin:0}img{width:%dpx;height:%dpx;display:block;outline:1px solid #444}'
            'figcaption{padding:4px 0 2px}</style></body></html>' % (largura, alt))
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pg = nav.new_page(viewport={'width': colunas * (largura + 10) + 10, 'height': 400})
        pg.set_content(html)
        pg.wait_for_timeout(200)
        pg.screenshot(path=destino, full_page=True)
        nav.close()
    return destino

#!/usr/bin/env python3
"""Gera o HTML de uma aula, ou o deck consolidado de uma matéria.

  python3 gerar.py <pasta-do-curso>/materias/<matéria>/aula-1
      -> aula-1/aula-1.html (a aula avulsa)
  python3 gerar.py --deck <pasta-do-curso>/materias/<matéria>
      -> <matéria>/deck-<matéria>.html (todas as aulas-N/aula.md, em ordem)
No Windows, "python" no lugar de "python3".

O HTML sai único e autossuficiente: CSS, JS, fontes, logos e mapas vão dentro do arquivo; abre sem internet.
Só usa a biblioteca padrão do Python.
"""
import base64
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import blocos  # noqa: E402
import formato  # noqa: E402
import mapas  # noqa: E402

# Os cursos que vêm dentro do plugin (0.2.0): a identidade e os mapas-base de cada um.
# Valem quando a pasta do curso não tem a própria identidade/ (ex.: a primeira utilização).
CURSOS_DO_PLUGIN = os.path.join(os.path.dirname(os.path.dirname(AQUI)), 'cursos')
CURSO_PADRAO = 'turma-especial'


class Identidade:
    def __init__(self, pasta):
        self.pasta = pasta
        info = formato.ler(os.path.join(pasta, 'identidade.md')).campos
        self.nome = info.get('nome')
        self.logo_escuro = self._datauri(info.get('logo escuro'))
        self.logo_claro = self._datauri(info.get('logo claro'))
        with open(os.path.join(pasta, info.get('fontes')), encoding='utf-8') as f:
            fontes = f.read().rstrip('\n')
        # as fontes entram embutidas (base64), para o arquivo abrir sem internet
        self.fontes = re.sub(r'url\(([^)]+\.woff2)\)', lambda m: 'url(data:font/woff2;base64,' + self._b64(m.group(1)) + ')', fontes)
        with open(os.path.join(pasta, info.get('tema')), encoding='utf-8') as f:
            self.tema = f.read()

    def _b64(self, rel):
        with open(os.path.join(self.pasta, rel), 'rb') as f:
            return base64.b64encode(f.read()).decode()

    def _datauri(self, rel):
        return 'data:image/svg+xml;base64,' + self._b64(rel)


def pasta_do_curso(aula, caminho):
    """Acha a identidade do curso subindo a partir da pasta da aula.

    Duas arrumações valem (mudança do plugin, 11/11/2026; o motor de origem só conhecia a segunda,
    presa à pasta onde ele morava):
      - pasta do curso:   <curso>/identidade/            (a aula fica em <curso>/materias/<matéria>/aula-N/)
      - pasta de cursos:  <raiz>/cursos/<curso>/identidade/   (o campo "curso" do aula.md diz qual)
    Se nenhuma das duas existe, vale o curso que vem no plugin (0.2.0, 12/11/2026):
      - <pasta-da-skill>/cursos/<curso>/identidade/  (sem o campo "curso", a Turma Especial)
    """
    curso = aula.campos.get('curso')
    pasta = os.path.dirname(os.path.abspath(caminho))
    while True:
        direta = os.path.join(pasta, 'identidade')
        if os.path.exists(os.path.join(direta, 'identidade.md')):
            return direta
        if curso:
            por_curso = os.path.join(pasta, 'cursos', curso, 'identidade')
            if os.path.exists(os.path.join(por_curso, 'identidade.md')):
                return por_curso
        acima = os.path.dirname(pasta)
        if acima == pasta:
            break
        pasta = acima
    padrao = os.path.join(CURSOS_DO_PLUGIN, curso or CURSO_PADRAO, 'identidade')
    if os.path.exists(os.path.join(padrao, 'identidade.md')):
        return padrao
    raise SystemExit('identidade do curso não encontrada: falta a pasta identidade/ (com identidade.md) '
                     'na pasta do curso, acima de ' + os.path.dirname(os.path.abspath(caminho)) +
                     ', e o plugin não traz o curso "' + (curso or CURSO_PADRAO) + '"')


def montar(aulas, ident, titulo):
    paginas = []
    for aula in aulas:
        mapas.procurar_em(os.path.dirname(aula.caminho))
        for p in aula.paginas:
            paginas.append(blocos.pagina(p, len(paginas), aula, ident))
    with open(os.path.join(AQUI, 'molde', 'esqueleto.html'), encoding='utf-8') as f:
        esq = f.read()
    with open(os.path.join(AQUI, 'molde', 'deck.css'), encoding='utf-8') as f:
        css = ident.tema + f.read()
    with open(os.path.join(AQUI, 'molde', 'deck.js'), encoding='utf-8') as f:
        js = (f'const LOGO_K="{ident.logo_escuro}",LOGO_W="{ident.logo_claro}",NOME_CURSO="{ident.nome}";' + f.read())
    # regras novas do motor (ex.: as duas versões da Bíblia), separadas do CSS e do JS herdados do Cowork
    with open(os.path.join(AQUI, 'molde', 'extra.css'), encoding='utf-8') as f:
        css += f.read()
    with open(os.path.join(AQUI, 'molde', 'extra.js'), encoding='utf-8') as f:
        js += f.read()
    out = esq
    for k, v in (('{{TITULO}}', titulo), ('{{FONTES}}', ident.fontes), ('{{CSS}}', css),
                 ('{{PAGINAS}}', ''.join(paginas) + '</div>\n'), ('{{JS}}', js)):
        out = out.replace(k, v, 1)
    return out, len(paginas)


def gerar_aula(pasta):
    arq = os.path.join(pasta, 'aula.md')
    aula = formato.ler(arq)
    ident = Identidade(pasta_do_curso(aula, arq))
    mapas.mapas_do_curso(os.path.join(os.path.dirname(ident.pasta), 'mapas'))
    html, n = montar([aula], ident, aula.campos.get('título do arquivo', 'Aula'))
    destino = os.path.join(pasta, os.path.basename(os.path.normpath(pasta)) + '.html')
    with open(destino, 'w', encoding='utf-8') as f:
        f.write(html)
    return destino, n


def gerar_deck(pasta_materia):
    pastas = sorted((d for d in os.listdir(pasta_materia) if re.match(r'^aula-\d+$', d)), key=lambda d: int(d.split('-')[1]))
    aulas = [formato.ler(os.path.join(pasta_materia, d, 'aula.md')) for d in pastas
             if os.path.exists(os.path.join(pasta_materia, d, 'aula.md'))]
    if not aulas:
        raise SystemExit('nenhuma aula-N/aula.md nesta pasta')
    ident = Identidade(pasta_do_curso(aulas[0], aulas[0].caminho))
    mapas.mapas_do_curso(os.path.join(os.path.dirname(ident.pasta), 'mapas'))
    html, n = montar(aulas, ident, aulas[0].campos.get('título do arquivo', 'Deck'))
    nome = os.path.basename(os.path.normpath(pasta_materia))
    destino = os.path.join(pasta_materia, f'deck-{nome}.html')
    with open(destino, 'w', encoding='utf-8') as f:
        f.write(html)
    return destino, n


def main(args):
    if not args:
        print(__doc__)
        return 1
    try:
        if args[0] == '--deck':
            destino, n = gerar_deck(args[1])
        else:
            destino, n = gerar_aula(args[0])
    except formato.ErroFormato as e:
        print('ERRO no aula.md,', e)
        return 2
    print(f'ok: {destino} ({n} páginas)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

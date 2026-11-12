"""Leitura do arquivo de conteúdo de uma aula (aula.md).

O formato (descrito no README do motor) é markdown com quatro níveis:
  linhas soltas no topo  -> dados da aula (campo: valor)
  # Nome                 -> grupo de páginas (a "aula" no sumário)
  ## Título no sumário   -> uma página; logo abaixo, os campos da página (campo: valor)
  ### tipo (opções)      -> um bloco da página; abaixo, o conteúdo do bloco

Não depende de nenhuma biblioteca fora do Python.
"""
import re


class Campos:
    """Lista ordenada de pares (campo, valor). Um campo pode repetir (ex.: legenda, trecho)."""

    def __init__(self):
        self.pares = []

    def add(self, k, v):
        self.pares.append((k, v))

    def get(self, k, padrao=None):
        for a, b in self.pares:
            if a == k:
                return b
        return padrao

    def todos(self, k):
        return [b for a, b in self.pares if a == k]

    def __contains__(self, k):
        return any(a == k for a, _ in self.pares)


class Bloco:
    def __init__(self, tipo, opcoes, linha):
        self.tipo = tipo
        self.opcoes = opcoes
        self.linha = linha
        self.linhas = []

    # ---- leituras do conteúdo ----
    def texto(self):
        """Conteúdo como texto corrido (linhas unidas por espaço)."""
        return ' '.join(l.strip() for l in self.linhas if l.strip())

    def campos(self):
        c = Campos()
        for l in self.linhas:
            if not l.strip():
                continue
            k, v = _campo(l)
            if k is None:
                raise ErroFormato(self.linha, f'no bloco "{self.tipo}", esperava "campo: valor" e veio: {l.strip()[:60]}')
            c.add(k, v)
        return c

    def itens(self, posicoes):
        """Itens de lista. Cada item começa com '- '.
        Formas aceitas:
          - a | b | c               (campos na ordem de `posicoes`)
          - texto simples           (primeiro campo)
          - campo: valor            (e as linhas seguintes, recuadas, com mais campos)
        Sublista (ex.: itens de um lado do par): linhas recuadas com '- ' depois de 'itens:'.
        Sufixo {vermelho} / {preto} / {cinza} no fim da primeira linha define a cor."""
        itens = []
        atual = None
        em_sub = None
        for l in self.linhas:
            if not l.strip():
                continue
            rec = len(l) - len(l.lstrip(' '))
            s = l.strip()
            if s.startswith('- ') and rec == 0:
                atual = Campos()
                itens.append(atual)
                em_sub = None
                s = s[2:].strip()
                s, cor = _cor(s)
                if cor:
                    atual.add('cor', cor)
                k, v = _campo(s, posicoes)
                if k is not None:
                    atual.add(k, v)
                elif ' | ' in s or s.endswith(' |') or s.startswith('| '):
                    for nome, val in zip(posicoes, [x.strip() for x in s.split('|')]):
                        if val:
                            atual.add(nome, val)
                else:
                    atual.add(posicoes[0], s)
                continue
            if atual is None:
                raise ErroFormato(self.linha, f'no bloco "{self.tipo}", cada item começa com "- ": {s[:60]}')
            if s.startswith('- ') and em_sub is not None:
                atual.add(em_sub, s[2:].strip())
                continue
            k, v = _campo(s, None)
            if k is None:
                raise ErroFormato(self.linha, f'no bloco "{self.tipo}", linha não reconhecida: {s[:60]}')
            if k == 'itens' and v == '':
                em_sub = 'item'  # "itens:" abre a sublista; cada "- " recuado vira um item
                continue
            em_sub = None
            atual.add(k, v)
        return itens


class Pagina:
    def __init__(self, titulo, grupo, linha):
        self.titulo = titulo
        self.grupo = grupo
        self.linha = linha
        self.campos = Campos()
        self.blocos = []


class Aula:
    def __init__(self, caminho):
        self.caminho = caminho
        self.campos = Campos()
        self.paginas = []


class ErroFormato(Exception):
    def __init__(self, linha, msg):
        super().__init__(f'linha {linha}: {msg}')


_CAMPO = re.compile(r'^([A-Za-zÀ-ÿ0-9][A-Za-zÀ-ÿ0-9 ]{0,30}):(?:\s(.*)|$)')
_COR = re.compile(r'\s*\{(vermelho|preto|cinza)\}\s*$')


def _campo(s, posicoes=None):
    """'campo: valor' -> (campo, valor). Só aceita campos conhecidos quando `posicoes` é dado,
    para não confundir texto que tem dois-pontos ('Atos 16:11') com um campo."""
    m = _CAMPO.match(s.strip())
    if not m:
        return None, None
    k = m.group(1).strip().lower()
    if posicoes is not None and k not in posicoes and k not in CAMPOS_DE_ITEM:
        return None, None
    return k, (m.group(2) or '').strip()


def _cor(s):
    m = _COR.search(s)
    if not m:
        return s, None
    return s[:m.start()], m.group(1)


CAMPOS_DE_ITEM = {'rótulo', 'título', 'texto', 'cor', 'itens', 'número', 'textos', 'data',
                  'ponto', 'caixa', 'dia', 'referência', 'nota', 'ativo'}


def ler(caminho):
    aula = Aula(caminho)
    grupo = ''
    pag = None
    bloco = None
    with open(caminho, encoding='utf-8') as f:
        linhas = f.read().split('\n')
    em_comentario = False
    for n, l in enumerate(linhas, 1):
        s = l.rstrip()
        # comentários <!-- ... --> são ignorados (notas para quem edita)
        if em_comentario:
            if '-->' in s:
                em_comentario = False
            continue
        if s.strip().startswith('<!--'):
            if '-->' not in s:
                em_comentario = True
            continue
        if s.startswith('### '):
            if pag is None:
                raise ErroFormato(n, 'bloco "###" fora de uma página "##"')
            cab = s[4:].strip()
            m = re.match(r'^(.*?)\s*\((.*)\)\s*$', cab)
            tipo, ops = (m.group(1), m.group(2)) if m else (cab, '')
            opcoes = [o.strip() for o in ops.split(',') if o.strip()]
            bloco = Bloco(tipo.strip().lower(), opcoes, n)
            pag.blocos.append(bloco)
            continue
        if s.startswith('## '):
            pag = Pagina(s[3:].strip(), grupo, n)
            aula.paginas.append(pag)
            bloco = None
            continue
        if s.startswith('# '):
            grupo = s[2:].strip()
            pag = None
            bloco = None
            continue
        if bloco is not None:
            bloco.linhas.append(s)
            continue
        if not s.strip():
            continue
        k, v = _campo(s)
        if k is None:
            raise ErroFormato(n, f'esperava "campo: valor": {s.strip()[:60]}')
        (pag.campos if pag is not None else aula.campos).add(k, v)
    return aula

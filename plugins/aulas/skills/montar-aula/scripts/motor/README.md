# Motor

O código que monta o HTML das aulas a partir do `aula.md`. É chamado pela skill `montar-aula`; os caminhos abaixo são a partir desta pasta. No Windows, `python` no lugar de `python3`.

| Para | Comando | Sai em |
|---|---|---|
| Gerar uma aula | `python3 gerar.py <pasta-da-aula>` | `aula-N/aula-N.html` |
| Gerar o deck da matéria (todas as aulas) | `python3 gerar.py --deck <pasta-da-matéria>` | `<matéria>/deck-<matéria>.html` |
| Conferir (sempre, depois de gerar) | `python3 conferir.py <arquivo.html>` | `conferencia/` ao lado do HTML |
| PDF (só quando pedido) | `python3 pdf.py <arquivo.html>` | `<arquivo>.pdf` |
| Converter páginas de um deck antigo | `python3 ferramentas/html_para_aula.py <deck.html> <1ª> <última> <aula.md> [--mapa N=nome] [--cabecalho "campo: valor"]` | o `aula.md` e, com `--mapa`, o SVG em `<matéria>/mapas/` |
| Comparar o gerado com o original | `python3 ferramentas/comparar.py <original.html> <1ª> <última> <gerado.html> <pasta>` | `comparacao.md` e `lado-a-lado.png` |

O HTML sai **único e autossuficiente**: CSS, JS, fontes, logos e mapas vão dentro do arquivo e ele abre sem internet. No navegador: setas ou rolagem passam as páginas; S abre o sumário; F põe em tela cheia; E liga a edição; num mapa por passos a seta avança o passo antes de mudar de página.

## O que o motor lê da pasta do curso
- **A identidade:** a pasta `identidade/` (com `identidade.md`, `tema.css`, `fontes.css`, `fontes/` e os logos). O motor a acha subindo a partir da pasta da aula.
- **O conteúdo:** `aula.md`, na pasta da aula. O formato está em `../../referencias/formato-do-aula-md.md`.
- **Os mapas-base:** `mapas/<nome>.svg`, na pasta da matéria ou da aula.

## Dependências
- **Gerar:** só o Python 3 (3.9 ou mais novo). Nenhuma biblioteca.
- **Conferir, PDF e comparar:** Playwright com o Chromium, instalados uma vez por computador:
  ```
  python3 -m pip install playwright
  python3 -m playwright install chromium
  ```

## As conferências (`conferir.py`)
Página a página, em tamanho real (1280 × 720). Saem como FALHA na tela e com código de saída 1:
1. **Nada transborda:** nenhum elemento sai da página, e o miolo não estoura.
2. **Folga sob o título** de pelo menos 10 px até o primeiro bloco.
3. **Folga antes do rodapé** de pelo menos 24 px.
4. **`justify-content: safe center`** no miolo: se o conteúdo crescer, ele desce em vez de subir por cima do título.
5. **Nenhum cartão só com rótulo** (cartão, lado de par ou passo de mapa sem texto).

E grava a **folha de contato** (`conferencia/folha-de-contato.png`) e a **folha dos mapas** (`folha-dos-mapas.png`), para a conferência visual.

## Arquivos
| Arquivo | O quê |
|---|---|
| `gerar.py` | Lê o `aula.md` e a identidade do curso e monta o HTML da aula ou do deck |
| `formato.py` | Lê o `aula.md` (grupos, páginas, campos, blocos, itens) |
| `blocos.py` | O HTML de cada tipo de página e de bloco |
| `mapas.py` | A página de mapa por passos |
| `molde/` | A casca do deck, o CSS (sem cores nem fontes, que são do curso) e o JS |
| `conferir.py` · `pdf.py` · `navegador.py` | As conferências, o PDF e o que os dois usam do navegador |
| `ferramentas/` | O conversor de deck antigo e a comparação página a página |

Origem, data e o que mudou em relação ao motor de origem: `../../../../ORIGEM.md`.

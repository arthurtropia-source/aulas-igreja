# O formato do `aula.md`

> Referência da skill `montar-aula`. Origem: o README do motor das aulas da Turma Especial (20/10/2026), trazido em 11/11/2026; exemplos trocados por neutros em 12/11/2026. É o arquivo onde o conteúdo da aula fica, separado da apresentação; o motor (`scripts/motor/gerar.py`) gera o HTML a partir dele.

## Por que este formato
**Por que markdown estruturado, e não JSON:** o texto das aulas é cheio de aspas, e no JSON cada aspa precisa de escape (`\"`). Uma aspa esquecida quebra o arquivo inteiro. No `aula.md`, cada página é um título, cada campo é `nome: valor` numa linha e cada bloco tem nome em português. Ele se lê em qualquer editor ou visualizador de markdown e se edita sem saber programar. O motor lê sem nenhuma biblioteca. O erro aponta a linha (`ERRO no aula.md, linha 42: ...`).

### Os quatro níveis
```
título do arquivo: Nome da matéria — slides          <- dados da aula, no topo
curso: turma-especial                                  <- o nome curto do curso (sem identidade/ na pasta, vale a da TE, que vem no plugin)
matéria: Nome da matéria
aulas na matéria: 4
versões na tela: embaixo                               <- desenho das duas versões da Bíblia (a decidir)

# Aula 1 · Título da aula                              <- grupo: o nome da aula no sumário e na barra

## Gancho                                              <- uma página; o texto é o título dela no sumário
seção: 1 · Abertura                                    <- campos da página
rótulo: Abertura
título: "Uma pergunta com a ==palavra-chave== em vermelho?"

### cartões (acima grande)                             <- um bloco, com opções entre parênteses
- rótulo: O rótulo pequeno do cartão
  título: "A frase do professor"
  cor: vermelho
```
**Marcação no texto:** `==assim==` fica em vermelho (no título) ou realçado (no versículo); `**assim**` em negrito; `*assim*` em itálico. HTML simples, como `<br>`, passa como está. `<!-- comentário -->` é ignorado.

### Campos da página
| Campo | O que faz |
|---|---|
| `tipo` | `normal` (padrão), `capa do curso`, `capa da aula` ou `mapa` |
| `seção` | O texto em vermelho no topo, à direita (e na barra) |
| `rótulo` / `título` / `título menor` | O rótulo vermelho, o título grande (t1) ou o título menor (t2) |
| `sumário: não` · `cabeçalho: não` | Tira a página do sumário ou o logo e o número do topo. As capas e os mapas já vêm assim. |
| `fundo` | `vermelho` ou `preto` (página de destaque) |
| `modo: aprofundar` | Marca a página como aprofundamento (o botão "Aprofundar" a esconde) |
| Capa do curso | `título` (com `<br>`), `cartas` (separadas por `\|`), `citação` |
| Capa da aula | `número`, `título`, `textos`, `referência`, `versículo` e `comparação` (ARA) |
| Mapa | `mapa` (o SVG-base), `zoom` (a área de aproximação, "x y largura altura"), `rótulo`, `legenda` (uma por linha: `linha \| texto`, `tracejada \| texto`, `preta \| texto` ou `ponto \| texto`) |

### Tipos de bloco
Opções comuns: `acima pequeno|médio|grande` (14, 26 ou 40 px de espaço acima do bloco). Cor de item: `cor: vermelho|preto|cinza`, ou `{vermelho}` no fim da linha do item.
| Bloco | Conteúdo | Opções |
|---|---|---|
| `frase` | Texto corrido, a frase de destaque | `grande`, `abaixo 22px` |
| `texto` · `nota` · `rótulo` | Texto corrido: o corpo, a nota pequena ou o rótulo vermelho no meio da página | |
| `cartões` | Itens com `rótulo`, `título` e `texto` | `colunas N` (o padrão é o número de cartões) |
| `lista` | A lista numerada: itens com `título` e `texto` | `compacta`, `duas colunas`, `começa em N` |
| `cadeia` | Os passos ligados por traço: itens com `título` e `texto` | |
| `par` | Os dois lados contrastados: `rótulo`, `título`, `cor` e `itens:` (sublista) | |
| `faixa` | `rótulo` e `texto` (a faixa cinza) | |
| `chamada` | `texto` e `nota` (o traço vermelho à esquerda) | |
| `versículo` | `texto` (BKJ 1611), `referência`, `comparação` (ARA, opcional) | `grande`, `longo 19px` (vários versos), `versões embaixo\|lado a lado\|ao clicar` |
| `chips` | Um item por etiqueta | |
| `tabela` | Tabela markdown (`\| a \| b \|`, a 2ª linha `\|---\|`); `{vermelho}` no cabeçalho, `{rótulo}` ou `{negrito}` na célula | `rótulo na 1ª coluna`, `grande` |
| `ordem` | A grade das aulas: `número \| textos \| título` | |
| `linha do tempo` | Itens com `data`, `título`, `texto`, `ponto` (posição %) e `caixa` (posição do texto) | `altura 300px` |
| `aprendemos` | Itens com `rótulo` e `título` (os quatro cartões de "O que aprendemos?") | |
| `desafio` | Texto corrido (a frase grande do desafio da semana) | |
| `leitura` | A semana de leitura: `dia \| referência \| nota` | |
| `espaço` | Espaço vazio | `10px`, ou `médio` |
| `html` | Cópia literal de HTML. É a saída para o que ainda não tem tipo; evite. | |
| `passo` (só no mapa) | `cidade`, `título`, `texto`, `trecho: A > B > C` e `trecho tracejado: ...` (repetíveis) | |

**Item de lista**, em três formas: `- texto simples` (o primeiro campo), `- a | b | c` (os campos na ordem da tabela) ou `- campo: valor` com mais campos nas linhas seguintes, recuados com dois espaços.

### Mapa por passos (página do tipo `mapa`)
O mapa-base (litoral, regiões, cidades e a rota geral) é um SVG na pasta `mapas/` **da matéria** (ou da aula), na pasta do curso. Os três mapas-base da Turma Especial (`segunda-viagem-missionaria`, `via-egnacia`, `vale-do-lico`) vêm no plugin, em `cursos/turma-especial/mapas/`, e o motor os acha sozinho. A aula diz só a história: um `### passo` por passo. O primeiro é a visão geral, sem cidade. Em cada passo, a legenda vem do texto do professor, a cidade em foco pulsa, o trecho se desenha e o mapa aproxima até a área do `zoom`. As cidades são achadas pelo nome no SVG. Um ponto fora de cidade é escrito `x,y`. O foco em várias cidades fica `cidade: Vale = Colossos + Laodiceia + Hierápolis` (nomes que existem no mapa `vale-do-lico`). O sumário marca a página com a etiqueta "Mapa interativo". Na impressão, sai a visão geral.

Para um mapa novo, use a skill `mapa-narrativo` (ela gera o mapa completo, com câmera, e um SVG parado por cena). O mapa por passos dentro do deck só existe hoje para os mapas-base que já estão na pasta do curso ou no plugin.

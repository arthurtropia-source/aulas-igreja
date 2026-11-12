A Turma Especial é a escola de discipulado da Igreja Mananciais. A identidade vive de três coisas e nada mais: vermelho, preto e branco; tipografia comprimida em caixa alta; e fotografia real de turma. Esta é a extração do folder TE 2027 — cores, tipos, marcas e padrões como estão no material impresso, prontos para reuso em documentos, mockups e peças novas.

## Conteúdo

Escreva em português do Brasil, em segunda pessoa quando se dirigir ao candidato ("o aluno é encorajado", "você deverá confirmar"). O tom é direto e vocacional: frases curtas, verbos no presente, nada de linguagem publicitária.

Títulos vão em CAIXA ALTA, sempre. Texto corrido vai em caixa normal. Nunca use emoji, nem em peça digital.

Prazos, idades e condições de inscrição aparecem em `corpo-forte` dentro do parágrafo — é o único destaque inline da marca: "Ter o Ensino Médio completo **ATÉ DEZEMBRO DE 2026**". Citação bíblica vai entre aspas em `titulo-bloco`, com a referência logo abaixo em `referencia`: "PORTANTO, IDE, ENSINAI A TODAS AS NAÇÕES…" / MATEUS 28.19.

O nome da escola se escreve Turma Especial por extenso no texto e TE nas marcas e no ano (TE 27, TE 2027).

## Cor

São três tintas. `vermelho-te` é a cor da marca e só ela carrega ênfase; `tinta` faz todo o resto do texto; `fundo` é papel branco. Não existe segunda cor de apoio — se uma peça pede mais uma área de cor, ela é `cinza-faixa`, e só como fundo de faixa.

Use `realce` para a palavra-chave do título duplo, para o nome do módulo, para os numerais de lista e para blocos inteiros de chamada. Nunca para texto corrido.

Página cheia de `vermelho-te` é reservada à capa e à contracapa, com o lockup em `sobre-realce`.

Sobre `faixa`, o folder impresso usa `sobre-faixa` (branco). Em tela isso dá 2,6:1 — troque por `preto-rico`, que dá 6,4:1 sobre o mesmo cinza nos dois temas (`tinta` não serve: no tema escuro ela vira branco). Em título de 24px ou mais o `realce` sobre `fundo` escuro fica em 3,6:1: é assim que o original faz, e é o limite — não desça o tamanho.

## Tipografia

Quatro famílias, cada uma com um trabalho:

`display` (Tusker Grotesk Super) abre seção com manchete. `comprimida` (Neumatic Compressed) faz a capa, o mural de valores e as chamadas numéricas. `sans` (Montserrat) faz títulos, texto e listas — é a família que carrega 90% do material. `marca` (Open Sans ExtraBold) existe só dentro do logotipo e não deve ser usada em texto.

Tusker Grotesk e Neumatic Compressed são licenciadas e não acompanham este sistema; instale os arquivos na máquina que for diagramar. Sem elas, a pilha cai em Oswald e Big Shoulders Display (Google Fonts), que preservam a proporção comprimida mas não são a marca — não aprove arte final com o fallback. Montserrat e Open Sans são abertas e podem ser carregadas do Google Fonts.

Escala: `titulo-pagina` uma vez por página, `titulo-secao` para as viradas de assunto, `titulo-bloco` para blocos curtos, `titulo-modulo` ao lado do selo. Texto em `corpo` nas páginas institucionais e `corpo-leve` nas páginas de imersão e processo seletivo. Listas de disciplina em `item-lista`; carga horária e numeração de módulo em `rotulo`.

Entrelinha do display comprimido é sempre menor que 1 — é o que produz o bloco sólido de texto do mural de valores.

## Espaço e forma

Margem lateral é `espaco-12`. Entre seções, `espaco-8`. Dentro de um bloco, `espaco-2` entre título e parágrafo.

Tudo é reto: `raio-reto` em foto, faixa, bloco de cor e capa. A única exceção é o selo de módulo, em `raio-selo`. Não existe sombra, gradiente ou borda arredondada na marca.

O currículo roda em duas colunas separadas por `espaco-12`. Texto institucional pode vir centralizado ou justificado, como no folder; listas sempre alinhadas à esquerda.

## Imagem

Fotografia é sempre real, da própria turma: adoração, formatura, convivência. Sem banco de imagens, sem pessoas posando para câmera em estúdio.

Corte retangular, sem cantos arredondados e sem filtro de cor. Foto pode sangrar até a borda superior da página ou entrar em grade de dois ou três blocos. Atrás de recorte, use `moldura-foto`.

Veja `assets/Fotografia` para os três cortes de referência extraídos do folder.

## Iconografia

A marca tem um ícone só: o livro aberto dentro de um círculo, usado como selo de módulo e como marcador de destaque na faixa. Ele existe em duas versões — círculo `vermelho-te` com livro branco, e o inverso — e não deve ser redesenhado nem substituído por biblioteca de ícones. Se uma peça nova precisar de outro símbolo, encomende no mesmo traço: silhueta cheia, sem contorno, dentro de círculo.

Os SVGs são de tinta fixa; `<img>` não herda cor. Escolha o arquivo pela versão, não por CSS.

## Logotipo

O lockup horizontal é o monograma TE em `marca`, com TURMA sobre ESPECIAL à direita, alinhados à altura do monograma. Use `assets/Logotipos/te-logo-horizontal-preto.svg` sobre fundo claro e a versão branca sobre `vermelho-te`, `preto-te` ou foto escura.

Assine toda peça no canto superior. Área de proteção: a altura do monograma TE em todos os lados. Não recomponha o lockup, não troque as fontes, não aplique o logotipo em vermelho.

O lockup vertical TE 27 é da capa e da contracapa do ano — não sirva de assinatura de página. Troque o ano a cada turma.

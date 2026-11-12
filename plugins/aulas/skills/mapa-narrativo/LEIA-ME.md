# Mapa narrativo: instalação e uso

Faz o mapa que conta uma aula passo a passo (a câmera anda, o percurso se desenha, o lugar se revela e o texto do professor aparece num box). É o mesmo estilo dos mapas das Cartas Paulinas. Funciona sozinho, no seu computador, sem internet.

## O que você precisa
- Um computador com **Python 3** (testado no 3.9). No Mac já costuma vir. No Windows, instale em python.org (marque "Add python to PATH").
- O Claude (Claude Code, ou o Cowork/Claude Desktop) **ou** nenhum: dá para fazer à mão, editando texto.

## Instalar (escolha um)
**A. Claude Code** (o jeito mais simples)
1. Copie a pasta `mapa-narrativo` inteira para dentro da pasta `.claude/skills/` do seu projeto (crie `.claude/skills/` se não existir). Para valer em todos os projetos, use `~/.claude/skills/`.
2. Abra o Claude nesse projeto e peça: **"faça o mapa da aula sobre a segunda viagem de Paulo"**. A skill entra sozinha e começa com as perguntas.

**B. Cowork ou Claude Desktop**
1. Compacte a pasta `mapa-narrativo` num `.zip` (a pasta, não só o conteúdo).
2. Nos ajustes do Claude, na parte de Skills (o nome do menu muda de versão), envie o `.zip`.
3. Peça o mapa do mesmo jeito. O arquivo `mapa.html` sai na pasta de trabalho que você deu ao Claude.

**C. Sem o Claude**
1. Copie a pasta `exemplo/` para um nome seu (ex.: `meu-mapa/`) e edite `cenas.md` e `lugares.csv` em qualquer editor de texto.
2. No terminal, dentro da pasta `mapa-narrativo`:
```
python3 scripts/gerar_mapa.py meu-mapa
```
3. Abra `meu-mapa/mapa.html` no navegador.

## Ver o exemplo agora
Abra `exemplo/mapa.html` no navegador (4 cenas da segunda viagem). Setas do teclado, espaço ou clique avançam; **A** liga o modo automático; **F** põe em tela cheia.

## O dia a dia
1. Diga ao Claude (ou escreva no `cenas.md`) **que ideia da aula o mapa explica** e **qual texto do professor vai nos boxes**. Só entra o que o professor disse.
2. O Claude propõe as cenas; o professor aprova.
3. O Claude monta a pasta do mapa e roda o gerador. Para mapas parados (slide ou impressão): acrescente `--svg` ao comando; saem `svg/cena-1.svg`, `cena-2.svg`…
4. Abra o `mapa.html`, passe cena por cena, corrija no `cenas.md` e gere de novo.

## O que tem na pasta
| O quê | Para quê |
|---|---|
| `SKILL.md` | As instruções que o Claude segue (o passo a passo e as regras) |
| `exemplo/` | Um mapa pronto para copiar e já gerado (`mapa.html`) |
| `scripts/gerar_mapa.py` | O gerador |
| `molde/` | O visual (cores, fontes embutidas, câmera) |
| `base/terra.json` | O litoral (Natural Earth), da Espanha à Pérsia |
| `biblioteca/` | 50 lugares do mundo de Paulo com coordenada aproximada, as rotas das viagens e rótulos de região, prontos para copiar |
| `LICENCAS.md` e `licencas/` | De onde vem cada ativo e sob que licença |
| `historia-e-regras.md` | Como esta skill nasceu e as regras que aprendeu |

## Limites
- O mapa se movimenta no navegador. Para **slide**, use o SVG de cada cena (pode inserir como imagem no PowerPoint ou Keynote; as fontes caem para Georgia fora do navegador) ou projete o `mapa.html` direto.
- A base cobre da Espanha à Pérsia e do sul da Turquia à Etiópia. Outra região: veja `base/LEIA-ME.md`.
- Não faz mapa de rua nem de cidade; é mapa de percurso e de lugares.

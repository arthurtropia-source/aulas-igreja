---
name: converter-aula
description: Converte uma aula que já existe, feita fora do formato (PowerPoint, PDF de slides, Google Slides, Canva ou HTML antigo), para o formato das aulas — o aula.md e a apresentação HTML — já no design da Turma Especial, mantendo o texto de cada slide como está. Use quando pedirem "põe esta aula no design da TE", "põe na paleta da TE", "transforma esse PDF em HTML", "passa esse PowerPoint para o formato da aula", "deixa essa apresentação com a cara da Turma Especial". Não use para montar aula a partir de texto-base ou gravação (skill aula-do-zero) nem para aula que já tem aula.md (skills corrigir-aula ou incluir-mapa). Em dúvida, comece pela skill aula.
---

# Converter uma aula pronta

> **A pasta comum** (motor, identidade da TE, mapas-base e referências) fica na skill `aula`, ao lado desta: `../aula/`. Os caminhos `aula/...` abaixo são a partir dela.

O conteúdo já foi aprovado por quem fez a aula: aqui não se seleciona nem se reescreve, **converte-se**. O design da TE vem sozinho, porque é o motor que desenha.

## 0. Condição de entrada (confira antes de tudo)
| Pergunta | Se não |
|---|---|
| A tarefa está na pasta do curso (`memoria.md` e `mapa-das-aulas.md` na pasta aberta)? | Siga a skill `aula` (corte 1) e pare |
| Chegou um arquivo de slides (PowerPoint, PDF de slides, Google Slides, Canva, HTML)? | Não é esta skill: volte à skill `aula` |
| A pasta da aula **ainda não** tem `aula.md`? | Já está no formato: volte à skill `aula` (corte 4) |

Leia antes: `aula/referencias/regras-de-fonte.md`, `aula/referencias/curso-turma-especial.md`, `aula/referencias/formato-do-aula-md.md`, `aula/referencias/biblia.md`; da pasta do curso, `memoria.md` e `passagem.md`.

## 1. Guardar o original
Em `materias/<matéria>/aula-N/fonte/`, intocado. Briefing: só três dados (matéria, número da aula e quem fez o original). Pergunte o que faltar.

## 2. Ler slide a slide (uma rota por formato)
| Formato | Como ler |
|---|---|
| HTML antigo da Turma Especial (feito no Cowork em 2026) | O conversor: `python3 aula/scripts/motor/ferramentas/html_para_aula.py <deck.html> <primeira> <última> <aula-N/aula.md>` (uso completo no topo do arquivo). Bloco que não sai idêntico vira `### html`: anote em `sugestoes/` |
| PowerPoint ou PDF de slides | As habilidades de PowerPoint e de PDF do próprio Claude. Não conseguiu ler: peça o PDF exportado |
| Google Slides ou Canva | Peça o PDF exportado (ou o PowerPoint) e siga a linha de cima |

## 3. Escrever o `aula.md`
Um slide original para uma página, **na mesma ordem**:
- o texto do slide entra **literal**; só se corta o que é nota ao professor ou emoji, e o corte vai para as pendências (não some em silêncio);
- o bloco se escolhe pelo que o slide faz (lista, cartões, par, versículo, linha do tempo); título em `título`, a palavra-chave em `==assim==`;
- capa: `tipo: capa da aula` (ou `capa do curso`, se for a abertura da matéria);
- versículo citado por inteiro: siga `biblia.md`; a ARA de comparação, se o original não traz, vai para as pendências, não se inventa;
- imagem do original: foto de pessoa só com o ok de quem responde pelo curso; imagem de terceiro só com a origem no `registro.md`. **Mapa do original:** não cole a imagem; anote no fim "mapa a incluir na p. N" (é a skill `incluir-mapa` que faz).
- slide que não cabe numa página: divida em duas e diga na tabela. Não diminua letra nem mexa no molde.

## 4. Gerar e conferir
`python3 aula/scripts/motor/gerar.py materias/<matéria>/aula-N` e depois a skill `conferir-aula`. Falha de transbordo se corrige no `aula.md` (dividir a página), nunca no molde.

## 5. Mostrar a tabela de correspondência junto da aula
```
| Slide original | Página nova | O que mudou |
| 1 | 1 (capa da aula) | — |
| 4 | 4 e 5 | dividido: texto longo demais para uma página |
```
Depois pergunte: "Quer incluir um mapa nesta aula?" Sim: skill `incluir-mapa`.

## 6. Registro
Siga `aula/referencias/registro.md`, com a entrada "aula pronta, convertida para o formato e o design da TE".

## Não fazer
- Não "melhorar" o texto, não acrescentar slide, não trocar a ordem. O que parece errado no original vai para as pendências.
- O validador de entendimento não é obrigatório aqui (a aula já foi dada ou aprovada assim). Só se pedirem.

## Pronto quando
`aula.md` e `aula-N.html` na pasta da aula · conferência sem falha (ou a de reserva, dita no registro) · tabela de correspondência mostrada · registro, `mapa-das-aulas.md` e `passagem.md` em dia.

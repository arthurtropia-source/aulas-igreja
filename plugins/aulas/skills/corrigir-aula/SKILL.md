---
name: corrigir-aula
description: Corrige uma aula que já está no formato (com aula.md) a pedido de quem usa — página apertada ou cortada, cartão a tirar ou trocar, versículo, título, ordem — mudando só o aula.md e gerando de novo, com o antes e depois de cada item. Use quando pedirem "corrige a página 7", "a página 3 está apertada", "tira esse cartão", "troca o versículo", "refaz a aula 2", "gera o deck da matéria", "gera o PDF da aula". Não use para aula que ainda não está no formato (skill converter-aula ou aula-do-zero) nem para incluir mapa (skill incluir-mapa). Em dúvida, comece pela skill aula.
---

# Corrigir uma aula

> **A pasta comum** (motor, identidade da TE, mapas-base e referências) fica na skill `aula`, ao lado desta: `../aula/`. Os caminhos `aula/...` abaixo são a partir dela.

## 0. Condição de entrada (confira antes de tudo)
| Pergunta | Se não |
|---|---|
| A tarefa está na pasta do curso? | Siga a skill `aula` (corte 1) e pare |
| A pasta da aula tem `aula.md`? | Não está no formato: volte à skill `aula` |
| O pedido diz **o quê** e **onde** (página ou trecho)? | Pergunte. Não adivinhe a página |

Leia antes: `aula/referencias/regras-de-fonte.md`, `aula/referencias/formato-do-aula-md.md`; o `registro.md` da aula e a `memoria.md` do curso.

## 1. Uma rota por tipo de pedido
| Pedido | O que fazer |
|---|---|
| Diagramação (apertada, cortada, encostada no rodapé) | Menos texto **do próprio professor**, outro bloco, ou dividir a página. Nunca diminuir letra nem mexer no molde |
| Conteúdo (tirar, trocar, reescrever) | Só com texto do professor. Se o pedido exige frase nova que ele não disse, não escreva: vai para as pendências do professor |
| Versículo | As versões de `aula/referencias/biblia.md`; texto da internet tem a fonte no registro e é conferido com a Bíblia impressa |
| Deck da matéria inteira | `python3 aula/scripts/motor/gerar.py --deck materias/<matéria>` |
| PDF (só quando pedido) | `python3 aula/scripts/motor/pdf.py <arquivo.html>` (pede o Playwright) |

## 2. Gerar, conferir e mostrar
`python3 aula/scripts/motor/gerar.py materias/<matéria>/aula-N`, depois a skill `conferir-aula`. Mostre o antes e depois **por item** pedido. Se o texto mudou muito, ofereça o validador de entendimento (`conferir-aula`).

## 3. Registro
Siga `aula/referencias/registro.md`. Preferência do professor ou regra do curso que apareceu na correção: `contexto/curso.md` ou `memoria.md`.

## Pronto quando
Cada item pedido feito e mostrado · conferência sem falha · registro em dia.

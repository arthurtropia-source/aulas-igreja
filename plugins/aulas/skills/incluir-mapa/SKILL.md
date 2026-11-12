---
name: incluir-mapa
description: Inclui numa aula que já está no formato (com aula.md) um mapa por passos dentro do slide, como nas Aulas 1, 5 e 7 de Epístolas Paulinas II — a cada passo destaca um trecho da rota e uma cidade, aproxima o zoom e põe a legenda com a frase do professor —, escolhendo os passos pelo que a aula precisa contar. Só sobre os mapas-base que existem (a segunda viagem missionária, o vale do Lico e a Via Egnácia). Use quando pedirem "inclui um mapa na aula", "põe o mapa da viagem na página N", "faz o mapa interativo dessa aula". Não use para aula que ainda não está no formato (antes, skill converter-aula ou aula-do-zero), nem para mapa de região sem mapa-base. Em dúvida, comece pela skill aula.
---

# Incluir um mapa por passos

> **A pasta comum** (motor, identidade da TE, mapas-base e referências) fica na skill `aula`, ao lado desta: `../aula/`. Os caminhos `aula/...` abaixo são a partir dela.

**O mapa não mostra tudo o que aconteceu: mostra o que a aula precisa contar.** Cada legenda é uma frase do professor.

## 0. Condição de entrada (confira antes de tudo)
| Pergunta | Se não |
|---|---|
| A tarefa está na pasta do curso? | Siga a skill `aula` (corte 1) e pare |
| A pasta da aula tem `aula.md`? | Não está no formato: primeiro `converter-aula` (aula pronta) ou `aula-do-zero` (texto-base). Diga isso e pare |
| A região do mapa está num mapa-base? Confira os SVG em `aula/cursos/turma-especial/mapas/` e em `mapas/` da matéria, na pasta do curso | Diga: "Ainda não há mapa-base para essa região; o mapa por passos só sai sobre os mapas que já existem." Escreva em `sugestoes/` (região, aula, para que serviria) e **pare**. Não desenhe nem invente um mapa-base |

Mapas-base hoje: `segunda-viagem-missionaria` (Atos 16–18, de Antioquia à Acaia), `vale-do-lico` (Colossos, Laodiceia, Hierápolis, Éfeso), `via-egnacia` (Roma, a Via Egnácia, Filipos, Trôade).

## 1. A ideia que o mapa explica (uma frase)
Leia o `briefing.md` da aula, se houver. Se ele não diz, pergunte: **que ideia da aula o mapa explica, e por que ela se explica melhor num mapa?** Sem resposta, o mapa não entra (`aula/referencias/didatica.md`).

## 2. Os passos (aprovar antes de gerar)
Monte a tabela e espere o ok:
```
| Passo | Cidade em foco | Trecho que se desenha | Legenda (frase do professor, com a página da fonte) |
| 0 | — (visão geral) | — | ... |
```
- O primeiro passo é a visão geral, sem cidade. De 3 a 7 passos; **um passo, uma ideia**.
- A legenda sai **só** do texto do professor que já está na aula ou na `fonte/`. Sem frase dele para um passo, o passo não entra.
- Só cidades que existem no mapa-base (os nomes estão no SVG). Foco em várias: `cidade: Vale = Colossos + Laodiceia + Hierápolis`.
- A rota vem de Atos e de atlas, não do professor: o mapa-base já traz.

## 3. Pôr a página no `aula.md`
Uma página `tipo: mapa` com `mapa: <nome-do-mapa-base>` e um `### passo` por passo, no lugar que a pessoa indicou (ou onde estava a imagem do mapa no original). O formato está em `aula/referencias/formato-do-aula-md.md`, seção do mapa por passos. Não mexa nas outras páginas.

## 4. Gerar e conferir
`python3 aula/scripts/motor/gerar.py materias/<matéria>/aula-N` e depois a skill `conferir-aula`. **Olhe a folha dos mapas** (`conferencia/mapas/`): em cada passo a cidade certa pulsa e a legenda cabe.

## 5. Registro
Siga `aula/referencias/registro.md`: "mapa por passos incluído na p. N (mapa-base X, K passos)".

## Pronto quando
Passos aprovados · página gerada e conferida, folha dos mapas olhada · registro em dia.

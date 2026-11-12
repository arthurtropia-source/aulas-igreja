---
name: aula
description: Porta de entrada de toda tarefa com aula de curso da igreja (por padrão, a Turma Especial). Confere a pasta e o que chegou, e manda para a skill certa — converter-aula (aula pronta em PowerPoint, PDF, slides ou HTML para o formato e o design da TE), incluir-mapa, corrigir-aula, aula-do-zero (texto-base ou gravação) ou conferir-aula. Use em qualquer pedido de aula ou slide: "põe esse texto-base em slides", "põe esta aula no design da TE", "transforma esse PDF em HTML", "inclui um mapa na aula", "corrige a página 7", "confere a aula", "monta a aula", "o que dá para fazer?". Guarda o que é comum a todas: o motor, a identidade da Turma Especial, os mapas-base e as regras.
---

# Aula: a porta de entrada

> **v0.3.0 (12/11/2026).** A antiga `montar-aula` foi dividida: esta skill decide **qual** tarefa é; cada tarefa tem a sua skill. A decisão é fixa (se isto, então aquilo), conferida nos arquivos. **Não escolha a rota pelo que parece mais provável:** siga o corte. O que não cabe em nenhuma rota é exceção: pergunte a quem pediu.

**A IA organiza, seleciona e ilustra; não acrescenta.** Vale para todas as skills de aula (`referencias/regras-de-fonte.md`).

## O corte (nesta ordem; a primeira resposta "sim" decide)

**Corte 1. A tarefa está na pasta do curso?** Confira: a pasta aberta (no Cowork, a pasta conectada; na aba Code, a pasta da sessão) tem `memoria.md` e `mapa-das-aulas.md`?
- **Não:** não monte pasta nem crie arquivos. Diga: "Esta tarefa não está na pasta do curso. Abra a pasta Turma Especial que você recebeu (no campo de mensagem, + > Adicionar pasta) e me peça de novo. Se você não tem essa pasta, peça a quem cuida do curso." **Pare.**
- **Sim:** se o `passagem.md` ainda não registra o aviso de atualização automática, dê o aviso (`referencias/aviso-de-atualizacao.md`). Siga.

**Corte 2. De que aula se trata?** Ache a pasta `materias/<matéria>/aula-N/` (o `mapa-das-aulas.md` diz onde está cada aula). Se o pedido não diz a matéria e o número, pergunte. Aula nova: crie a pasta com `fonte/` dentro e guarde ali o que chegou (arquivo anexado, ou texto colado salvo como `.md`).

**Corte 3. O que existe e o que chegou?** Confira nos arquivos:

| Situação | Rota |
|---|---|
| Existe `aula-N/aula.md` (a aula já está no formato) | **Corte 4** |
| Chegou uma **aula pronta de fora**: PowerPoint, PDF de slides, Google Slides, Canva ou HTML antigo | skill **`converter-aula`** |
| Chegou **material do professor que não é slide**: texto-base (a aula escrita) ou gravação/transcrição | skill **`aula-do-zero`** |
| Nenhum dos três | **Exceção:** peça o material e diga onde ele vai ficar (`fonte/`). Não comece nada |

PowerPoint ou PDF de slides **é sempre aula pronta** (texto mantido, `converter-aula`). Refazer do zero a partir de um PowerPoint só quando a pessoa pedir com essas palavras (decisão de 12/11/2026).

**Corte 4. A aula já está no formato. O que se quer?** Se o pedido não diz com clareza, **mostre a lista e deixe a pessoa escolher**; não deduza:
| Pedido | Rota |
|---|---|
| Incluir um mapa | skill **`incluir-mapa`** |
| Corrigir algo ("a página 7 está apertada", "tira esse cartão", "corrige o versículo") | skill **`corrigir-aula`** |
| Conferir, sem mudar nada | skill **`conferir-aula`** |
| Outro | **Exceção:** registre em `sugestoes/` e pergunte |

**Depois de `converter-aula`:** pergunte "Quer incluir um mapa nesta aula?" Sim: `incluir-mapa`. Não: entregue.

## Antes de qualquer rota, leia
- Desta skill: `referencias/regras-de-fonte.md` e `referencias/curso-turma-especial.md`.
- Da pasta do curso: `memoria.md`, `passagem.md` e, se a aula já existe, o `registro.md` dela. Se houver `AGENTS.md` ou `contexto/`, leia também: **o que está na pasta do curso vale por cima do que vem no plugin.**

## O que é comum a todas as skills de aula (mora aqui)
As outras skills leem estes arquivos na pasta desta skill, que fica ao lado delas (`../aula/` a partir de cada uma).

| Arquivo | O quê |
|---|---|
| `scripts/motor/` | O motor: `gerar.py` (aula.md → HTML), `conferir.py`, `pdf.py`, `ferramentas/html_para_aula.py` (HTML antigo da TE → aula.md). Comandos em `scripts/motor/README.md` |
| `cursos/turma-especial/` | A identidade da TE (logo, cores, fontes com as licenças, design system) e os mapas-base. Não se edita por pedido de aula |
| `referencias/regras-de-fonte.md` | Sempre: só a palavra do professor |
| `referencias/curso-turma-especial.md` | Sempre: o curso padrão e as regras da marca para slide |
| `referencias/formato-do-aula-md.md` | Os campos, os blocos e o mapa por passos do `aula.md` |
| `referencias/biblia.md` | As versões da Bíblia na tela |
| `referencias/didatica.md` | As perguntas do briefing e quando um elemento visual entra |
| `referencias/esqueleto-e-corte.md` | O princípio de corte e a sequência padrão da aula |
| `referencias/validador-de-entendimento.md` | O roteiro do agente que lê como aluno |
| `referencias/conferencia-de-reserva.md` | Quando o Playwright não roda (ex.: o Cowork) |
| `referencias/registro.md` | Como toda tarefa termina (registro, mapa das aulas, passagem, sugestões) |
| `referencias/pasta-do-curso.md` | Como a pasta do curso é arrumada |
| `referencias/aviso-de-atualizacao.md` | O aviso de atualização automática |

**A identidade:** sem `identidade/` na pasta do curso, a aula sai na da Turma Especial, que vem aqui; o motor a acha sozinho.

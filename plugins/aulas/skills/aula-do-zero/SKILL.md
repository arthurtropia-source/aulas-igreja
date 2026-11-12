---
name: aula-do-zero
description: Monta uma aula nova a partir da palavra do professor que não está em slides — o texto-base (a aula escrita por extenso) ou a gravação transcrita —, numa apresentação HTML no formato e no design da Turma Especial, com briefing, esqueleto aprovado, aula.md, conferência, validador de entendimento, marcação da fonte e registro. Use quando pedirem "põe esse texto-base em slides", "monta a aula a partir desse texto", "transforma essa gravação em aula", "faz os slides da aula X" com material do professor. Não use para aula que já existe em PowerPoint, PDF de slides ou HTML (skill converter-aula), nem para corrigir aula pronta (corrigir-aula), nem para criar aula sem material do professor. Em dúvida, comece pela skill aula.
---

# Aula do zero

> **A pasta comum** (motor, identidade da TE, mapas-base e referências) fica na skill `aula`, ao lado desta: `../aula/`. Os caminhos `aula/...` abaixo são a partir dela.

Transforma a palavra do professor numa apresentação. **A IA organiza, seleciona e ilustra; não acrescenta.** Tudo o que aparece na tela saiu do material do professor.

## 0. Condição de entrada (confira antes de tudo)
| Pergunta | Se não |
|---|---|
| A tarefa está na pasta do curso? | Siga a skill `aula` (corte 1) e pare |
| Há material do professor em `aula-N/fonte/` que **não** é slide (texto-base ou gravação/transcrição)? | Slide (PowerPoint, PDF de slides, HTML): skill `converter-aula`. Nada: peça o material e pare |
| A pasta da aula **ainda não** tem `aula.md`? | Já existe: skill `corrigir-aula` |

Leia antes: `aula/referencias/regras-de-fonte.md`, `aula/referencias/curso-turma-especial.md`; da pasta do curso, `memoria.md`, `passagem.md` e `contexto/` (vale por cima do plugin).

## 1. A entrada (uma rota por tipo)
| Entrada | O que se faz com o texto |
|---|---|
| **Texto-base** (a aula escrita) | Selecionar e organizar em slides, só com as palavras dele |
| **Gravação ou transcrição** | Primeiro o arquivo base, só com as palavras de quem falou, em 4 partes: ênfases (com o sinal de cada uma), marcos, estilo e esqueleto, com a marcação de tempo. Daí os slides. Sempre a transcrição completa, nunca um resumo automático |

A fonte fica intocada em `fonte/`.

## 2. Briefing
As perguntas de `aula/referencias/didatica.md` (ou de `contexto/didatica.md` da pasta do curso): natureza do conteúdo, objetivo, público, mensagem, objetivo final, lugar na cadeia, como o aluno deve compreender. Uma por vez, em linguagem simples. O que o material já responde, mostre e peça só a confirmação. Grave em `briefing.md`. **Não siga sem o briefing aprovado.**

## 3. Esqueleto (aprovar antes de qualquer design)
Leia `aula/referencias/esqueleto-e-corte.md`. A lista de slides, com o que entra em cada um e de que trecho do professor saiu.
- **Tópico frasal:** antes de cada slide, uma frase do que ele ensina. Slide sem essa frase não entra.
- **Elemento visual** só entra respondendo que ideia explica e por que se explica melhor assim. **Mapa:** marque "mapa na p. N" no esqueleto; ele entra no passo 6, pela skill `incluir-mapa`.
- **Valide contra a fonte:** cada item aponta para o trecho do professor. O que não bate (número que não fecha, seção anunciada e ausente, duas versões) vai para as pendências, não se resolve em silêncio.
- Grave em `materias/<matéria>/esqueleto.md` e **espere o ok**. Referência: 12 a 20 slides por aula.

## 4. Escrever o `aula.md`
Formato em `aula/referencias/formato-do-aula-md.md`. Regras do texto:
1. **Só a palavra do professor.** Literal, adaptação (sintetizado do texto dele) ou sugestão; sugestão só com o ok do professor.
2. **Complementar, nunca substituir.** Cartão sem contexto se completa com outra frase do próprio texto (quem, o quê, como, quando, onde).
3. **Professor e aluno recebem o mesmo material.** Nada de nota ao professor.
4. **Didático, não poético.**
5. **Sem termo chulo ou coloquial pesado:** a descrição concreta que o próprio professor dá.
6. **Versículo por inteiro na tela:** as versões de `aula/referencias/biblia.md`; título do professor com palavra diferente da do versículo não se corrige: vai para as pendências.
7. **Nome de pessoa** não entra em link, endereço nem nome de arquivo.
8. Bloco `html` é a última saída: se precisou, anote em `sugestoes/`.
9. **Design system da TE** (`aula/cursos/turma-especial/identidade/design-system/`; resumo em `curso-turma-especial.md`): as regras de conteúdo para slide. Conflito com o motor: não mexa no molde, anote em `sugestoes/`.

## 5. Gerar e conferir
`python3 aula/scripts/motor/gerar.py materias/<matéria>/aula-N` e a skill `conferir-aula`, **com o validador de entendimento** (obrigatório na aula do zero). Correções só com texto do professor.

## 6. Mapa (só se o esqueleto marcou)
Skill `incluir-mapa`.

## 7. Marcação da fonte
Numa cópia do texto do professor (nunca no original), marque as **ideias inteiras** que foram para os slides. Grave ao lado da fonte, com `-marcado` no nome.

## 8. Registro
Siga `aula/referencias/registro.md`.

## Pronto quando
`briefing.md` aprovado · esqueleto aprovado · `aula.md` e `aula-N.html` · conferência sem falha e folha de contato olhada · validador rodado, correções só com texto do professor · registro, `mapa-das-aulas.md` e `passagem.md` em dia. Sem todos, a aula está "em produção".

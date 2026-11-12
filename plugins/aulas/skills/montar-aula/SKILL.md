---
name: montar-aula
description: Monta a aula de um curso da igreja (por padrão, a Turma Especial, cuja identidade vem no plugin) a partir da palavra do professor (texto por extenso, gravação transcrita ou PowerPoint), numa apresentação HTML que o professor usa na aula e o aluno recebe para estudar; e põe na paleta da Turma Especial uma aula que já existe. Trabalha na pasta do curso que a pessoa recebeu pronta e conduz o briefing, o esqueleto aprovado, a montagem pelo motor, as conferências, o validador de entendimento e o registro. Use quando pedirem "monta a aula", "põe esse texto-base em slides", "faz os slides da aula X", "transforma essa gravação em aula", "põe esta aula na paleta da TE", "deixa essa apresentação com a cara da Turma Especial", "refaz a aula", "corrige a página N", "gera o deck da matéria" ou "gera o PDF da aula". Não use para criar aula sem material do professor.
---

# Montar aula

> **v0.2.1 (12/11/2026).** Escrita a partir do caminho que funcionou nas 8 aulas de Epístolas Paulinas II; ainda em calibração numa aula real. Desde a 0.2 a skill se basta sozinha: a identidade da Turma Especial, a didática, a Bíblia e as regras de fonte vêm dentro dela. A pasta do curso chega pronta a quem usa: a skill não monta pasta. Cada atrito encontrado vira uma linha em `sugestoes/` da pasta do curso (seção 10).

Transforma a palavra do professor numa apresentação. **A IA organiza, seleciona e ilustra; não acrescenta.** Tudo o que aparece na tela saiu do material do professor.

**Pronto significa**, na pasta da aula (`materias/<matéria>/aula-N/`):
1. `briefing.md` com as respostas do professor ou de quem responde pela aula;
2. `aula.md` com o conteúdo, e `aula-N.html` gerado pelo motor a partir dele;
3. `conferir.py` sem nenhuma FALHA e a folha de contato olhada página a página;
4. o validador de entendimento rodado, e as correções feitas só com texto do professor;
5. `registro.md` com o que foi pedido, o que mudou e as pendências para o professor;
6. a linha da aula atualizada em `mapa-das-aulas.md`, na raiz da pasta do curso.

Sem os seis, a aula está "em produção", não "pronta".

## 0. O corte: onde esta aula está
Confira nos arquivos, nesta ordem, e siga **uma** rota. Não presuma.

**Primeiro, a pasta.** A pasta aberta (no Cowork, a pasta conectada; na aba Code, a pasta da sessão) tem `memoria.md` e `mapa-das-aulas.md`?
- **Não:** a tarefa não está na pasta do curso. **Não monte pasta nem crie arquivos.** Diga, simples: "Esta tarefa não está na pasta do curso. Abra a pasta Turma Especial que você recebeu (no campo de mensagem, + > Adicionar pasta) e me peça de novo. Se você não tem essa pasta, peça a quem cuida do curso." E pare.
- **Sim:** é a pasta do curso. Se o `passagem.md` ainda não registra o aviso de atualização automática, dê o aviso (`referencias/aviso-de-atualizacao.md`).

**Depois, a rota.** Ache a pasta da aula (`materias/<matéria>/aula-N/`). Se ela não existe, pergunte a matéria e o número da aula, crie a pasta com `fonte/` dentro e guarde ali o material recebido (arquivo anexado ou texto colado no chat, salvo como `.md`).

| Pergunta (confere-se na pasta da aula) | Rota |
|---|---|
| O pedido é pôr na paleta da TE uma aula **que já existe** (feita fora do motor: PowerPoint, PDF de slides, Google Slides, Canva, HTML antigo)? **Sim** | **Rota D, paleta:** `referencias/paleta-da-te.md`. |
| Existe `aula.md`? **Sim** | **Rota A, ajustar:** vá à seção 7 (correções) e depois refaça as seções 5 e 6. |
| Não existe `aula.md`, mas existe material do professor em `fonte/`? **Sim** | **Rota B, montar:** seções 1 a 9, em ordem. |
| Não existe nenhum dos dois | **Rota C, parar:** peça o material do professor e diga onde ele vai ficar (`fonte/`). Não comece a aula sem ele. |

**Antes de qualquer rota, leia:** desta skill, `referencias/regras-de-fonte.md` e `referencias/curso-turma-especial.md`; da pasta do curso, `memoria.md`, `passagem.md` e, se a aula já existe, o `registro.md` dela. Se a pasta do curso tiver `AGENTS.md` ou `contexto/` (curso, didática, Bíblia), leia também: **o que está na pasta do curso vale por cima do que vem no plugin.**

**A identidade:** sem `identidade/` na pasta do curso, a aula sai na identidade da **Turma Especial**, que vem no plugin (`cursos/turma-especial/`); o motor a acha sozinho. Outro curso traz a própria `identidade/` (veja `referencias/pasta-do-curso.md`).

## 1. A entrada
Diga em uma linha qual é a entrada, porque ela muda o trabalho:

| Entrada | O que se faz com o texto |
|---|---|
| **Texto por extenso** (a aula escrita) | Selecionar e organizar em slides, só com as palavras dele |
| **Aula gravada** (gravação ou transcrição) | Primeiro o arquivo base, só com as palavras de quem falou, em 4 partes: ênfases (com o sinal de cada uma), marcos, estilo e esqueleto, com a marcação de tempo. Daí os slides. Use sempre a transcrição completa, nunca um resumo automático |
| **PowerPoint pronto** | Quase não mexer no texto; reorganizar o visual e criar os elementos que ajudam a explicar. **Ainda não foi feito nenhuma vez:** vá devagar e registre cada decisão |

A fonte fica intocada em `fonte/`. Aula do zero, sem material do professor: não é desta skill.

## 2. Briefing
Faça as perguntas de `referencias/didatica.md` (ou de `contexto/didatica.md` da pasta do curso, se existir) (natureza do conteúdo, objetivo, público, mensagem, objetivo final, lugar na cadeia, como o aluno deve compreender). Uma por vez, em linguagem simples. O que o material do professor já responde, mostre a resposta e peça só a confirmação. Grave em `briefing.md`. **Não siga sem o briefing aprovado.**

## 3. Esqueleto (aprovar antes de qualquer design)
Leia `referencias/esqueleto-e-corte.md` e monte o esqueleto: a lista de slides, com o que entra em cada um e de que trecho do professor saiu.
- **Tópico frasal:** antes de cada slide, escreva em uma frase o que ele quer ensinar. Slide sem essa frase não entra.
- **Elemento visual** (mapa, linha do tempo, comparação) só entra respondendo: que ideia ele explica e por que ela se explica melhor assim.
- **Valide contra a fonte:** cada item do esqueleto aponta para o trecho do professor. O que não bate no material (número que não fecha, seção anunciada e ausente, duas versões do mesmo trecho) **não se resolve em silêncio**: vai para a lista de pendências do professor.
- Grave em `materias/<matéria>/esqueleto.md` (ou na seção da aula, se o arquivo já existe) e **espere o ok**. Tamanho de referência: 12 a 20 slides por aula.

## 4. Escrever o `aula.md`
O formato está em `referencias/formato-do-aula-md.md`. Regras do texto:
1. **Só a palavra do professor.** Marque para você mesmo o que é literal, o que é adaptação (sintetizado do texto dele) e o que é sugestão. Sugestão só entra com o ok do professor.
2. **Complementar, nunca substituir.** Cartão sem contexto se completa com outra frase do próprio texto. Confira em cada cartão: quem, o quê, como, quando e onde.
3. **Professor e aluno recebem o mesmo material.** Nada de nota ao professor nem frase que soe como orientação a quem dá a aula ("o objetivo", "as partes", "o aluno precisa ouvir").
4. **Didático, não poético.** Imagem de efeito vira formulação direta.
5. **Sem termo chulo ou coloquial pesado**, mesmo que esteja no texto do professor: troque pela descrição concreta que ele mesmo dá.
6. **Versículo citado por inteiro na tela:** a versão principal e a de comparação são as de `referencias/biblia.md` (ou de `contexto/biblia.md` da pasta do curso, se existir). Texto bíblico tirado da internet tem a fonte registrada no `registro.md` e é conferido com a Bíblia impressa antes do PDF final. Se o título do professor usa uma palavra diferente da do versículo na tela, não corrija: vai para as pendências.
7. **Nome de pessoa** não entra em link, endereço nem nome de arquivo; professor com título é chamado com o título.
8. Bloco `html` é a última saída: se precisou dele, anote em `sugestoes/`.
9. **Design system do curso** (na Turma Especial, `cursos/turma-especial/identidade/design-system/` desta skill; em outro curso, `identidade/design-system/` da pasta dele, quando existir): é a fonte da marca. O resumo do que vale para slide está em `referencias/curso-turma-especial.md`. Siga as regras de conteúdo dele que valem para slide (caixa alta nos títulos, tom, onde vai o destaque, como se escreve o nome do curso, sem emoji) e use só os logotipos e ícones de lá. Se uma regra dele conflitar com o que o motor desenha (fonte, cor, contraste), **não mexa no molde**: anote em `sugestoes/` e avise. Fonte licenciada que não está na pasta não se baixa nem se substitui por conta própria.

## 5. Gerar e conferir (sempre os dois)
Os scripts ficam em `scripts/motor/`, dentro da pasta desta skill. No Windows, `python` no lugar de `python3`.
```
python3 <pasta-desta-skill>/scripts/motor/gerar.py <pasta-da-aula>
python3 <pasta-desta-skill>/scripts/motor/conferir.py <pasta-da-aula>/aula-N.html
```
- Para mostrar a aula a quem pediu, entregue o arquivo `aula-N.html` (ele abre em qualquer navegador, sem internet).
- `gerar.py` só precisa do Python 3.9 ou mais novo. Erro no `aula.md` vem com a linha: conserte o arquivo, não o motor.
- `conferir.py` precisa do Playwright com o Chromium (instalação em `scripts/motor/README.md`). **Se não estiver instalado, diga isso e pergunte antes de instalar.** Onde não dá para instalar (ex.: o Cowork), use a **conferência de reserva** (`referencias/conferencia-de-reserva.md`) e diga no `registro.md` que foi ela.
- Qualquer FALHA (transbordo, folga, cartão só com rótulo) se corrige no `aula.md` (menos texto, outro bloco, dividir a página) e gera-se de novo. Não mexa no molde para fazer caber.
- **Olhe a folha de contato** (`conferencia/folha-de-contato.png`) e, se houver mapa, a folha dos mapas. Conferência automática sem olhar não vale.
- Deck da matéria inteira: `gerar.py --deck <pasta-da-matéria>`. PDF: `pdf.py <arquivo.html>`, só quando pedido.

## 6. Validador de entendimento
Abra um agente separado, que não viu esta conversa, com o roteiro de `referencias/validador-de-entendimento.md`. Ele lê como um aluno de primeira vez e devolve, bloco a bloco, ALCANÇADO, PARCIAL ou NÃO ALCANÇADO, e até 10 correções. Se o ambiente não abre agente separado, diga isso no `registro.md` e faça a leitura você mesmo, seguindo o mesmo roteiro, deixando claro que não foi independente.

## 7. Correções
- Cada correção usa **só texto do professor**. Se o entendimento só fecha com frase nova, não escreva: vai para as pendências do professor.
- Pedido de correção de quem usa ("a página 7 está apertada", "tira esse cartão"): altere o `aula.md`, refaça as seções 5 e 6 se o texto mudou, e mostre o antes e depois por item.
- Preferência do professor ou regra do curso que apareceu na correção: registre na memória da pasta do curso (seção 9), não aqui.

## 8. Marcação da fonte
Numa cópia do texto do professor (nunca no original de `fonte/`), marque as **ideias inteiras** que foram para os slides, não palavras soltas. Serve para o professor ver o que entrou e para rastrear cada slide. Grave ao lado da fonte, com `-marcado` no nome.

## 9. Entrega e registro
1. `registro.md` da aula: o que o professor pediu, a entrada, o que mudou e por quê, o resultado das conferências e do validador, e a lista de **pendências para o professor**, numerada.
2. A linha da aula em `mapa-das-aulas.md`.
3. O que está em produção e o que espera resposta de professor: uma linha em `passagem.md`.
4. Lição de forma geral ("daqui pra frente faça assim"): `memoria.md` da pasta do curso, com a data. Regra do curso ou preferência de um professor: `contexto/curso.md`.
5. **Não envie nem publique nada.** Entregar ao professor é de quem responde pela aula.

## 10. O que esta skill ainda precisa aprender
Sempre que um passo daqui não servir, faltar ou atrapalhar, escreva uma linha em `sugestoes/` da pasta do curso (arquivo `AAAA-MM-DD-assunto.md`): o que aconteceu, em que aula e o que teria ajudado. Não corrija a skill por conta própria: a sugestão vira versão nova do plugin.

## Referências desta skill
| Arquivo | Quando ler |
|---|---|
| `referencias/aviso-de-atualizacao.md` | Seção 0: o aviso de atualização automática (uma vez por pasta) e como desligar |
| `referencias/regras-de-fonte.md` | Sempre: só a palavra do professor |
| `referencias/curso-turma-especial.md` | Sempre: o curso padrão e as regras da marca que valem para slide |
| `referencias/didatica.md` | Seção 2: as perguntas do briefing |
| `referencias/biblia.md` | Seção 4: as versões da Bíblia na tela |
| `referencias/paleta-da-te.md` | Rota D: pôr na paleta da TE uma aula que já existe |
| `referencias/conferencia-de-reserva.md` | Seção 5, quando o Playwright não roda |
| `referencias/esqueleto-e-corte.md` | Seção 3: o princípio de corte e a sequência padrão da aula |
| `referencias/formato-do-aula-md.md` | Seção 4: os campos, os blocos e a marcação do `aula.md` |
| `referencias/validador-de-entendimento.md` | Seção 6: o roteiro do agente validador |
| `referencias/pasta-do-curso.md` | Quando a pasta não estiver como esperado, ou para abrir uma matéria ou aula nova |
| `scripts/motor/README.md` | Comandos, dependências e conferências do motor |
| `cursos/turma-especial/` | A identidade (logo, cores, fontes com as licenças, design system) e os mapas-base da Turma Especial. Não se edita por pedido de aula: mudança de marca é versão nova do plugin |

# Validador de entendimento

> Referência comum das skills de aula (mora na skill `aula`; 0.3.0). Origem: o agente usado nas 8 aulas de Epístolas Paulinas II (out/2026), onde pegou falha real em 6 das 8. **Este roteiro foi reescrito a partir da descrição registrada em 20/10/2026;** o texto original do pedido está no histórico bruto daquela sessão e ainda não foi recuperado. Calibrar na primeira aula real.

## O que é
Um agente **independente**, que não viu a conversa da montagem. Não é revisor de texto nem de design: é um aluno que nunca viu a matéria, conferindo se o entendimento é alcançado.

## O que ele recebe
1. O `aula.md` da aula (o que está nos slides).
2. O trecho do material do professor que corresponde a esta aula (o que será dito).
3. O público, tirado do `briefing.md` (uma linha).
Nada mais: nem o raciocínio de quem montou, nem o esqueleto comentado.

## O pedido (copie e preencha)
```
Você é um aluno que vê esta matéria pela primeira vez. Público: <público do briefing>.
Você recebeu dois materiais: os slides de uma aula (aula.md) e o texto do professor para a mesma aula.
Não revise estilo nem design. Responda só se o entendimento é alcançado.

Parte A, só os slides: lendo apenas os slides, na ordem, o que você entende de cada bloco da aula?
Aponte onde um slide não se entende sozinho (falta quem, o quê, como, quando ou onde).

Parte B, slides com a fala: para cada bloco, combinando o slide com o texto do professor,
dê o veredito ALCANÇADO, PARCIAL ou NÃO ALCANÇADO, com uma frase de motivo.

Parte C, correções: no máximo 10, em ordem de importância. Cada correção usa SOMENTE
frases que estão no texto do professor: cite a frase e diga em que slide ela entra.
Se o entendimento só se resolveria com frase nova, escreva "pendência para o professor"
e não proponha texto.
```

## O que fazer com a resposta
- PARCIAL e NÃO ALCANÇADO viram correção (com texto do professor) ou pendência para o professor.
- Registre no `registro.md` da aula: o veredito por bloco e o que foi corrigido.
- Rode de novo só se a correção mudou a estrutura de um bloco.

## Modelo
Leitura com julgamento sobre texto: um modelo intermediário basta. Não precisa do maior.

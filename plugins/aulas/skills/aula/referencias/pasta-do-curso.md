# A pasta do curso

> Referência comum das skills de aula (mora na skill `aula`; 0.3.0). O plugin leva o método e a identidade da Turma Especial (o curso padrão); a pasta do curso leva tudo o que é do curso. Uma pasta por curso, numa conta da igreja.
>
> **A pasta chega pronta** a quem usa, entregue por quem cuida do curso: `AGENTS.md`, `CLAUDE.md`, `memoria.md`, `mapa-das-aulas.md`, `passagem.md`, `contexto/curso.md`, `sugestoes/`, `materias/` e `.claude/settings.json`. A skill não monta pasta; o resto abaixo nasce quando faz falta.

```
<curso>/
├── AGENTS.md, CLAUDE.md    o que é o curso, as regras e o que carregar
├── memoria.md              lições do curso, com data
├── passagem.md             o que está em produção e as pendências com professores
├── mapa-das-aulas.md       o índice: uma linha por aula
├── contexto/               curso.md, didatica.md, biblia.md, fluxo-de-producao.md
├── identidade/             só para outro curso: identidade.md, tema.css, fontes.css, fontes/, logos, licenças
├── materias/<matéria>/     esqueleto.md, mapas/ e aula-N/
└── sugestoes/              o que o método deveria aprender; vira versão do plugin
```

## Uma pasta de aula (`materias/<matéria>/aula-N/`)
| Arquivo | O quê |
|---|---|
| `fonte/` | A palavra do professor (texto, transcrição, PowerPoint), intocada |
| `briefing.md` | As respostas da didática, aprovadas antes de produzir |
| `aula.md` | O conteúdo da aula (o motor gera o HTML a partir dele) |
| `aula-N.html` | A aula gerada. Não se edita à mão |
| `conferencia/` | As fotos das conferências (refeitas a cada conferência) |
| `registro.md` | O que foi pedido, o que mudou e as pendências para o professor |

## Abrir uma matéria ou uma aula nova
- Matéria: `materias/<nome-curto-sem-acento>/`, com um `README.md` de uma linha (matéria, professor, fonte).
- Aula: `materias/<matéria>/aula-N/`, com `fonte/` dentro. O número é a ordem na matéria.
- Mapa-base de um mapa por passos: `materias/<matéria>/mapas/<nome>.svg`.

## A identidade (`identidade/identidade.md`)
```
nome: <nome do curso como aparece nos slides>
logo escuro: logo-preto.svg
logo claro: logo-branco.svg
fontes: fontes.css
tema: tema.css
```
O motor embute tudo no HTML. Fonte, logo ou imagem só entra em `identidade/` com a origem e a licença registradas ali.

**Design system oficial (opcional):** `identidade/design-system/`, com um `LEIA-ME.md` (de onde veio e a conferência da `identidade/` contra ele), as regras da marca, os tokens e os logotipos e ícones oficiais. Quando existe, é a fonte da marca: a `identidade/` que o motor lê é conferida contra ele.

**A Turma Especial não precisa de `identidade/` na pasta:** a dela vem no plugin (`cursos/turma-especial/identidade/`, com o design system). Se a pasta tiver uma `identidade/`, ela vale por cima da do plugin.

## Duas pessoas, dois computadores
Uma aula, uma pessoa por vez. Cada aula tem a própria pasta; os arquivos comuns (`memoria.md`, `mapa-das-aulas.md`, `passagem.md`) só ganham linhas.

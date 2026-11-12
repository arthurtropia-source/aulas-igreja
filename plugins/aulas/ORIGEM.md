# Origem de cada peça do plugin

Regra: nada entra no plugin sem a origem e a data marcadas aqui. Código e ativo de terceiro, além disso, com a licença.

## Motor (`skills/montar-aula/scripts/motor/`)
- **Origem:** a pasta de aulas da Turma Especial (`igreja/aulas/motor/`), no commit `95f773b` do repositório das aulas. Reconstruído em 20/10/2026 a partir do deck final de Epístolas Paulinas II. Código do próprio projeto; usa só a biblioteca padrão do Python (e o Playwright nas conferências).
- **Copiado em:** 11/11/2026.
- **Não veio:** `viagem/` (o gerador da "viagem pelo mapa", que a skill `mapa-narrativo` substitui) e `mapas/*.svg` (os três mapas-base de Epístolas Paulinas II: levam a cor do curso gravada e moram na pasta do curso, em `materias/<matéria>/mapas/`).
- **O que mudou em relação à origem** (o resto é idêntico, byte a byte):

| Arquivo | Mudança | Por quê |
|---|---|---|
| `gerar.py` | `pasta_do_curso` acha a identidade subindo a partir da pasta da aula (`<curso>/identidade/` ou `<raiz>/cursos/<curso>/identidade/`); saiu a constante `RAIZ` | Na origem, a identidade era procurada ao lado do motor. No plugin, o motor mora longe da pasta do curso |
| `mapas.py` | Só a mensagem de erro e o comentário do topo | O mapa-base agora fica na pasta da matéria |
| `ferramentas/html_para_aula.py` | Com `--mapa`, o SVG extraído vai para `<matéria>/mapas/`, e não para a pasta do motor | Idem |
| `navegador.py` | O endereço do arquivo é montado com `pathlib` (`as_uri`), e não com `'file://' + caminho` | O jeito antigo não monta endereço válido no Windows |
| `conferir.py`, `pdf.py`, `ferramentas/*.py` | Só os exemplos de uso no comentário do topo | Tiravam o caminho da pasta de origem |
| `README.md` | Reescrito para o plugin; o formato do `aula.md` foi para `skills/montar-aula/referencias/formato-do-aula-md.md` | |

- **Pontos ainda presos à Turma Especial** (não atrapalham a TE; saem antes do segundo curso que não use a identidade dela): a constante `VERMELHO = '#DD3338'` em `mapas.py` e o nome padrão `'Turma Especial'` no conversor `ferramentas/html_para_aula.py` (só usado para converter os decks antigos da TE).

## Skill `mapa-narrativo`: retirada na 0.2.1
Era a "viagem pelo mapa" (a aula inteira dentro de um mapa), empacotada em 11/11/2026. Saiu do plugin em 12/11/2026 por decisão de quem responde pelo plugin: o plugin leva só o mapa por passos dentro do slide (o motor da `montar-aula`).

## Skill `montar-aula` (`skills/montar-aula/`)
- **Origem:** escrita em 11/11/2026 a partir de `igreja/aulas/contexto/fluxo-de-producao.md` (o caminho que funcionou nas 8 aulas), de `igreja/aulas/propostas/2026-10-20-licoes-do-historico.md` (regras R1 a R10, T1 a T4 e a seção 5) e do `AGENTS.md` das aulas. Texto do próprio projeto.
- **Estado:** rascunho v0.1. Não rodou em aula real.

## 0.2.0 (12/11/2026): a Turma Especial como curso padrão
Decisão de 12/11/2026 (a identidade da TE vai para o plugin público, para que ele funcione sem pasta do curso pronta).

| Peça | Origem | Observação |
|---|---|---|
| `skills/montar-aula/cursos/turma-especial/identidade/` | A pasta de identidade das aulas da TE (`igreja/aulas/cursos/turma-especial/identidade/`), igual byte a byte | Fontes SIL OFL 1.1 com os textos da licença; logos da igreja (uso das aulas da TE) |
| `.../identidade/design-system/` | O design system oficial (folder TE 2027), sem as 3 fotos de turma | `LEIA-ME.md` reescrito para o plugin |
| `skills/montar-aula/cursos/turma-especial/mapas/` | Os três mapas-base de Epístolas Paulinas II (litoral Natural Earth, domínio público) | Levam o vermelho da TE |
| `referencias/regras-de-fonte.md`, `didatica.md`, `biblia.md`, `curso-turma-especial.md` | O `AGENTS.md` e o `contexto/` das aulas da TE | Sem nome de professor nem de pessoa |
| `paleta-da-te.md`, `conferencia-de-reserva.md` | Escritos em 12/11/2026 | |
| `referencias/aviso-de-atualizacao.md` | Escrito em 12/11/2026 (0.2.1), a partir da antiga primeira utilização | |
| `scripts/motor/gerar.py` e `mapas.py` | Mudança do plugin | Sem `identidade/` na pasta do curso, o motor usa `cursos/<curso>/` da skill (padrão: `turma-especial`); os mapas-base de lá entram por último na busca |

## O que o plugin não leva (e onde fica)
Nome de professor, de aluno ou de membro; fonte de aula; aula pronta; foto de pessoa; memória e lições do curso; identidade de outro curso: tudo na **pasta do curso**.

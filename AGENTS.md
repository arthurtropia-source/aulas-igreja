# Plugin das aulas: AGENTS.md

Área da frente `igreja/`. Aqui mora o **método** de produção de aulas, empacotado como plugin do Claude: as skills, o motor que monta a apresentação e, desde a 0.2.0, a identidade da **Turma Especial**, o curso padrão. Quem faz aula instala o plugin e trabalha numa **pasta do curso** (a skill monta o mínimo dela na primeira utilização); a melhoria feita aqui chega a todos por versão.

> Status: **em uso** desde 12/11/2026 (versão 0.2.0), **publicado** em `github.com/arthurtropia-source/aulas-igreja`, repositório público. Vai ser transferido para a conta da igreja. Nome do marketplace (`aulas-igreja`) e do plugin (`aulas`) provisórios.
> Origem: proposta aprovada em 11/11/2026 (no sistema de quem mantém o plugin). Esta área se basta sozinha: o que ela precisa daquela proposta está resumido aqui e no `README.md`.

## As três casas (a regra que sustenta tudo)
| | O que tem | Onde mora |
|---|---|---|
| **Método** | Skills, motor, moldes, conferências; e a identidade da Turma Especial (curso padrão, decisão de 12/11/2026) | **Este plugin.** Repositório público |
| **Curso** | Memória, professores, fontes, aulas, passagem; a identidade de outro curso | A pasta do curso, numa conta da igreja. **Nunca aqui** |
| **Conversa** | Conta do Claude de quem opera | Com a pessoa. Não guarda nada que importe |

## O que nunca entra nesta área
- Logo, cor ou fonte de um curso que não seja a Turma Especial; nome de professor, de aluno, de membro ou de quem mantém o plugin; foto de pessoa; texto, gravação ou PowerPoint de professor; aula pronta.
- Conteúdo de terceiro sem origem e licença registradas (`plugins/aulas/ORIGEM.md` e o `LICENCAS.md` de cada skill).
- Senha, chave ou acesso.
Antes de cada commit, confira: o repositório vai ser público.

## Onde fica cada coisa
| Caminho | O quê |
|---|---|
| `.claude-plugin/marketplace.json` | O catálogo (um plugin só) |
| `plugins/aulas/` | O plugin: `.claude-plugin/plugin.json` (a versão), `skills/` e `ORIGEM.md` (de onde veio cada peça) |
| `plugins/aulas/skills/montar-aula/` | A skill que conduz a aula; o motor fica em `scripts/motor/`, a Turma Especial em `cursos/turma-especial/` e a pasta mínima do curso em `modelo-da-pasta/` |
| `plugins/aulas/skills/mapa-narrativo/` | A skill do mapa por passos |
| `teste/` | A prova de cada versão (`provar.sh`) e os registros datados |
| `roteiros/` | Roteiros para pessoas (teste de dois computadores, instalação) |
| `CHANGELOG.md` | O que mudou em cada versão |

## Regras
- **Skill usa `scripts/`, nunca `bin/`:** `bin/` não instala no Cowork nem no chat.
- **Uma skill só para montar a aula.** Os passos ficam dentro dela; só se divide pelo teste do OS (regra de 04/11/2026).
- **Prova antes de versão:** nenhuma versão sobe sem `teste/provar.sh` passar (a Aula 1 de referência, gerada só a partir do `aula.md`, sem pasta do curso, tem de sair idêntica, byte a byte) e sem o registro gravado em `teste/`. A aula de referência não mora aqui (é texto de professor): fica com quem mantém o plugin.
- **Versão:** toda mudança que chega a quem usa sobe o campo `version` do `plugin.json` e ganha uma linha no `CHANGELOG.md`. Com a versão fixa, ninguém recebe mudança.
- **Correção vira regra na skill**, não na memória de uma conta. Preferência de um curso ou de um professor não sobe para cá: fica na memória da pasta do curso.
- **Nenhuma ação externa sem o ok de quem responde pelo plugin:** publicar o repositório, enviar o pacote a alguém, instalar no computador de outra pessoa.
- **Fonte da verdade até o piloto:** o motor e a skill `mapa-narrativo` ainda são desenvolvidos na pasta de aulas de origem (`igreja/aulas/`). Aqui há **cópias** datadas. Mudança de método feita lá é trazida para cá, e vice-versa, até a mudança da fonte da verdade (depois do piloto).
- Idioma: português do Brasil. Com professores e responsáveis: simples, sem termo técnico.

## Sessão
Uma versão por sessão. Comece pelo `CHANGELOG.md` e pelo último registro em `teste/`; termine com a prova rodada, o registro gravado e o `CHANGELOG.md` atualizado.

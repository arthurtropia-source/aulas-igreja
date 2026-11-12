# Aulas da igreja: plugin do Claude

O método de produção das aulas dos cursos da igreja, como plugin do Claude. Transforma a palavra do professor (texto, gravação ou PowerPoint) numa apresentação HTML, que o professor usa na aula e o aluno recebe para estudar. Traz a **Turma Especial** como curso padrão: a identidade dela (logo, cores, fontes e regras da marca) vem junto, e funciona sem nenhuma preparação.

> Versão 0.2.0 (12/11/2026). Em uso; em calibração nas primeiras aulas reais.

## O que vem
| Skill | O que faz |
|---|---|
| `montar-aula` | Na primeira vez, monta a pasta do curso. Depois: a aula a partir do material do professor (briefing, esqueleto aprovado, montagem, conferências, validador e registro), ou uma aula pronta posta na paleta da Turma Especial. Leva o motor que gera a apresentação |
| `mapa-narrativo` | O mapa que conta a aula passo a passo: um HTML que abre sem internet |

Pedidos que funcionam: "põe esse texto-base em slides", "põe esta aula na paleta da TE", "faz o mapa da aula", "corrige a página 7".

## Instalar
**No Cowork (app do Claude):** Personalizar > Plugins > adicionar catálogo pelo endereço `arthurtropia-source/aulas-igreja`, com a sincronização automática ligada, e instalar o plugin `aulas`. Ao abrir uma tarefa, escolha uma pasta do computador para o curso.

**Na aba Code (app do Claude) ou no terminal:** dentro da pasta do curso,
```
claude plugin marketplace add arthurtropia-source/aulas-igreja
claude plugin install aulas@aulas-igreja
```

**O que é preciso no computador:** Python 3.9 ou mais novo, para gerar as aulas (nenhuma biblioteca). Para as conferências automáticas e o PDF: Playwright com o Chromium (`python3 -m pip install playwright` e `python3 -m playwright install chromium`); sem eles, a skill usa a conferência de reserva.

## Atualização
O plugin se atualiza sozinho quando a sincronização do catálogo está ligada (Cowork) ou pela pasta do curso (`.claude/settings.json`, aba Code). A skill avisa na primeira utilização e diz como desligar.

## O que fica onde
- **Aqui (público):** o método e a identidade da Turma Especial.
- **Na pasta do curso (de quem usa):** professores, material dos professores, aulas, memória e lições do curso.
- **Nunca aqui:** nome de professor, de aluno ou de membro; foto de pessoa; texto de professor; aula pronta.

## Licenças
- As fontes (Big Shoulders Display, Oswald, Montserrat): SIL Open Font License 1.1, com os textos em `plugins/aulas/skills/montar-aula/cursos/turma-especial/identidade/licencas/` e `plugins/aulas/skills/mapa-narrativo/licencas/`.
- O litoral dos mapas: Natural Earth, domínio público.
- O logo e o selo da Turma Especial são da igreja: servem às aulas e peças da própria Turma Especial.
- O código e os textos do método: licença do repositório **a definir**.

## Para quem mantém
Regras: `AGENTS.md`. De onde veio cada peça: `plugins/aulas/ORIGEM.md`. O que mudou: `CHANGELOG.md`. Prova de cada versão: `teste/provar.sh` (a Aula 1 de referência, gerada sem pasta do curso, tem de sair idêntica).

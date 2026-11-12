# Aulas da igreja: plugin do Claude

O método de produção das aulas dos cursos da igreja, como plugin do Claude. Transforma a palavra do professor (texto, gravação ou PowerPoint) numa apresentação HTML, que o professor usa na aula e o aluno recebe para estudar. Traz a **Turma Especial** como curso padrão: a identidade dela (logo, cores, fontes e regras da marca) vem junto, e funciona sem nenhuma preparação.

> Versão 0.2.0 (12/11/2026). Em uso; em calibração nas primeiras aulas reais.

## O que vem
| Skill | O que faz |
|---|---|
| `aula` | A porta de entrada: confere a pasta e o que chegou e manda para a skill certa. Guarda o motor, a identidade da TE e as regras |
| `converter-aula` | Aula pronta (PowerPoint, PDF de slides, HTML antigo) para o formato e o design da TE, com o texto mantido |
| `incluir-mapa` | Mapa por passos dentro do slide, sobre os mapas-base |
| `corrigir-aula` | Correções pedidas numa aula que já está no formato; deck da matéria; PDF |
| `aula-do-zero` | Aula nova a partir do texto-base ou da gravação: briefing, esqueleto, aula, validador, registro |
| `conferir-aula` | A conferência das páginas e o validador de entendimento |

Pedidos que funcionam: "põe esse texto-base em slides", "põe esta aula no design da TE", "transforma esse PDF em HTML", "inclui um mapa na aula 3", "corrige a página 7", "confere a aula".

## Instalar
**No Cowork (app do Claude):** no campo de mensagem, **+ > Adicionar plugins**; depois **+ Adicionar > Adicionar marketplace**, cole `arthurtropia-source/aulas-igreja` no campo URL, deixe **Sincronizar automaticamente** ligado, clique em **Sincronizar** e, no plugin **Aulas**, em **Adicionar**. Para trabalhar, **+ > Adicionar pasta** e escolha a pasta do curso, que vem pronta de quem cuida do curso (o plugin não monta pasta). Passo a passo em `roteiros/instalar.md`.

**Na aba Code (app do Claude) ou no terminal:** dentro da pasta do curso,
```
claude plugin marketplace add arthurtropia-source/aulas-igreja
claude plugin install aulas@aulas-igreja
```

**O que é preciso no computador:** Python 3.9 ou mais novo, para gerar as aulas (nenhuma biblioteca). Para as conferências automáticas e o PDF: Playwright com o Chromium (`python3 -m pip install playwright` e `python3 -m playwright install chromium`); sem eles, a skill usa a conferência de reserva.

## Atualização
O plugin se atualiza sozinho quando a sincronização do catálogo está ligada (Cowork) ou pela pasta do curso (`.claude/settings.json`, aba Code). A skill avisa uma vez por pasta e diz como desligar.

## O que fica onde
- **Aqui (público):** o método e a identidade da Turma Especial.
- **Na pasta do curso (de quem usa):** professores, material dos professores, aulas, memória e lições do curso.
- **Nunca aqui:** nome de professor, de aluno ou de membro; foto de pessoa; texto de professor; aula pronta.

## Licenças
- As fontes (Big Shoulders Display, Oswald, Montserrat): SIL Open Font License 1.1, com os textos em `plugins/aulas/skills/aula/cursos/turma-especial/identidade/licencas/`.
- O litoral dos mapas: Natural Earth, domínio público.
- O logo e o selo da Turma Especial são da igreja: servem às aulas e peças da própria Turma Especial.
- O código e os textos do método: licença do repositório **a definir**.

## Para quem mantém
Regras: `AGENTS.md`. De onde veio cada peça: `plugins/aulas/ORIGEM.md`. O que mudou: `CHANGELOG.md`. Prova de cada versão: `teste/provar.sh` (a Aula 1 de referência, gerada sem pasta do curso, tem de sair idêntica).

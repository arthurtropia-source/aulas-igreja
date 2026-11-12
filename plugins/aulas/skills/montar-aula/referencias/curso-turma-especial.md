# O curso padrão: Turma Especial

> Referência da skill `montar-aula`. A Turma Especial (TE) é o curso que vem no plugin: a identidade dela está em `cursos/turma-especial/` (dentro desta skill) e vale sempre que a pasta do curso não tiver a própria `identidade/`. Origem: a pasta de aulas da TE (out/2026) e o design system oficial do folder TE 2027.

## O curso
- A escola de discipulado da igreja. **Público:** jovens. **Formato:** integral, de um a dois anos, como um seminário.
- **O nome nos slides é "Turma Especial"** por extenso no texto, e "TE" só nas marcas e no ano (TE 27). Nunca "Curso de Maturidade Espiritual", que é outro curso.
- A capa não precisa dizer "para jovens".
- **Nada de orientação ao professor na tela:** um professor pediu para tirar tudo o que soava como orientação a quem dá a aula, e a regra ficou para todas as aulas.
- Professores, matérias em andamento e preferências de cada professor ficam na **pasta do curso** (`contexto/curso.md`), nunca no plugin.

## A matéria de referência
Epístolas Paulinas II (1 e 2 Tessalonicenses, Colossenses e Filipenses), 8 aulas, out/2026. Foi a primeira matéria feita por este método. A Aula 1 é a prova do plugin: gerada de novo, tem de sair idêntica. Os três mapas-base dela (`segunda-viagem-missionaria`, `via-egnacia`, `vale-do-lico`) vêm no plugin, em `cursos/turma-especial/mapas/`, e servem a qualquer aula da TE que precise deles.

## A identidade (o que o motor aplica sozinho)
| Elemento | Valor |
|---|---|
| Vermelho (a única cor de ênfase) | `#dd3338` |
| Preto | `#231f20` · texto `#100f0d` |
| Cinza de faixa (só como fundo de faixa) | `#a2a2a1`; texto sobre ele em `#100f0d`, nunca branco |
| Títulos | Big Shoulders Display e Oswald, em caixa alta |
| Texto | Montserrat |
| Página | 1280 × 720, fundo branco; páginas de destaque em vermelho ou preto |
| Logo | O lockup horizontal TE (preto sobre claro, branco sobre vermelho ou preto), no canto superior |

As regras completas da marca estão em `cursos/turma-especial/identidade/design-system/README-oficial.md`. As que valem para slide:
- Títulos em CAIXA ALTA, sempre; texto corrido em caixa normal. **Nunca emoji.**
- O vermelho só para ênfase: a palavra-chave do título (`==assim==`), numerais de lista, blocos de chamada. Nunca para texto corrido.
- Tudo reto: sem sombra, gradiente nem canto arredondado.
- Citação bíblica entre aspas, com a referência logo abaixo.
- Use só os logos e o selo de módulo (livro no círculo) da pasta `design-system/`; não redesenhe nem troque por biblioteca de ícones.
- As fontes oficiais de título (Tusker Grotesk e Neumatic Compressed) são licenciadas e **não** vêm no plugin. Big Shoulders e Oswald são a queda prevista pelo próprio design system. Não baixe nem troque fonte por conta própria.
- Fotografia, quando houver, é sempre real da própria turma, e só com o ok de quem responde pelo curso. O plugin não traz foto nenhuma.

## Outro curso
Para outro curso da igreja, a pasta do curso traz a própria `identidade/` (veja `pasta-do-curso.md`) e o `aula.md` diz `curso: <nome-curto>`. Sem isso, a aula sai na identidade da TE.

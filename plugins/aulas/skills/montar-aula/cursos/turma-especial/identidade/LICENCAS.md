# Origem e licença das fontes da identidade

Regra: nenhuma fonte, imagem ou logo de terceiro entra nesta pasta sem a origem e a licença registradas aqui. Verificado em 11/11/2026.

| Fonte | Arquivos (`fontes/`) | Projeto e autores | Versão gravada no arquivo | Licença | Texto da licença |
|---|---|---|---|---|---|
| Big Shoulders Display (peso 800) | `big-shoulders-display-800-a.woff2`, `-b.woff2` | The Big Shoulders Project Authors, `github.com/xotypeco/big_shoulders` | 2.002 | SIL Open Font License 1.1 | `licencas/OFL-bigshouldersdisplay.txt` |
| Oswald (pesos 400, 500, 700) | `oswald-*-a.woff2`, `-b.woff2` (6 arquivos) | The Oswald Project Authors, `github.com/googlefonts/OswaldFont` | 4.103 | SIL Open Font License 1.1 | `licencas/OFL-oswald.txt` |
| Montserrat (pesos 300, 400, 500, 700, 800, 900) | `montserrat-*-a.woff2`, `-b.woff2` (12 arquivos) | The Montserrat Project Authors, `github.com/JulietaUla/Montserrat` | 9.000 | SIL Open Font License 1.1 | `licencas/OFL-montserrat.txt` |

## Como foi confirmado
- **A licença está gravada dentro de cada um dos 20 arquivos.** A tabela de nomes de cada `.woff2` foi lida em 11/11/2026 (com a biblioteca fontTools): os 20 trazem o aviso de direitos do projeto acima e o endereço da licença (`scripts.sil.org/OFL` ou `openfontlicense.org`).
- **Os textos das licenças** foram baixados em 11/11/2026 do repositório oficial do Google Fonts (`github.com/google/fonts`, pastas `ofl/bigshouldersdisplay`, `ofl/oswald` e `ofl/montserrat`, arquivo `OFL.txt`) e estão em `licencas/`.
- **De onde vieram os arquivos:** foram extraídos em 20/10/2026 do deck final de Epístolas Paulinas II (09/10/2026), onde estavam embutidos. De que serviço o deck os tirou **não está registrado**; os arquivos não são iguais, byte a byte, aos que o Google Fonts serve hoje (comparado em 11/11/2026), o que é esperado para versões e recortes diferentes das mesmas fontes. A identidade e a licença de cada arquivo estão confirmadas pelo que ele traz gravado.

## O que a licença permite
A SIL OFL 1.1 permite usar, copiar, embutir e redistribuir as fontes, inclusive dentro do HTML das aulas, desde que a fonte não seja vendida sozinha e que o aviso de direitos e o texto da licença acompanhem a redistribuição dos arquivos de fonte. Por isso `licencas/` acompanha esta pasta.

## O que não é de terceiro
`logo-preto.svg`, `logo-branco.svg` e os arquivos de `design-system/logotipos/` e `design-system/icones/` são a marca da Turma Especial, da igreja. Estão no plugin para que as aulas do curso saiam com ela; **não são de uso livre**: servem às aulas e peças da própria Turma Especial. `tema.css`, `fontes.css` e `design-system/tokens.json` foram escritos no projeto.

## No plugin
Esta pasta foi copiada para o plugin em 12/11/2026 (0.2.0), igual à de origem, mais o design system sem as fotos. As licenças OFL acompanham as fontes, como a licença pede.

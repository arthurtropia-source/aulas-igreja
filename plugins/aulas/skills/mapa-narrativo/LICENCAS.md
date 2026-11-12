# Fonte e licença de cada ativo

Regra: nenhum ativo de terceiro entra sem a origem e a licença registradas aqui. Verificado em 11/11/2026.

| Ativo | Onde está | Origem | Licença | Como foi confirmada |
|---|---|---|---|---|
| Litoral (polígonos de terra) | `base/terra.json` | Natural Earth, camada `ne_10m_land` (1:10m), arquivo GeoJSON do repositório `nvkelso/natural-earth-vector` (`geojson/ne_10m_land.geojson`), recortado ao quadro -12 8 62 48 por `scripts/recortar_natural_earth.py` | Domínio público. Citação opcional: "Made with Natural Earth." (já vai no rodapé do mapa) | Página oficial https://www.naturalearthdata.com/about/terms-of-use/, aberta em 11/11/2026: "All versions of Natural Earth raster + vector map data ... are in the public domain." |
| Fonte Cinzel (latin) | embutida em `molde/fontes.css` (base64) | Google Fonts, arquivo woff2 `fonts.gstatic.com/s/cinzel/v26/` · Projeto Cinzel (Natanael Gama) | SIL Open Font License 1.1 | Texto da licença baixado de `github.com/google/fonts/ofl/cinzel/OFL.txt`, guardado em `licencas/OFL-cinzel.txt` |
| Fonte Crimson Text (latin, 400, 400 itálico, 600) | embutida em `molde/fontes.css` (base64) | Google Fonts, `fonts.gstatic.com/s/crimsontext/v19/` · Projeto Crimson Text (Sebastian Kosch) | SIL Open Font License 1.1 | Idem, `licencas/OFL-crimsontext.txt` |
| Lugares, coordenadas, rotas e rótulos de região | `biblioteca/` e `exemplo/` | Extração do projeto das Cartas Paulinas (Cowork, 17/09/2026), que desprojetou os sete mapas daquela época; as rotas vêm de Atos e de atlas, não do material de um professor. Cada linha traz a fonte na coluna `fonte`. As posições dos rótulos de região são indicativas | Dado do próprio projeto da igreja | Registro em `historia-e-regras.md` |
| Visual (cores, textura de papel, moldura, rosa dos ventos, rolo da carta) | `molde/` | Desenhado dentro do projeto (SVG e CSS próprios), sem imagem de terceiro | Do próprio projeto | — |
| Textos dos boxes do exemplo | `exemplo/cenas.md` | Escritos para o exemplo; não são de nenhum professor | Do próprio projeto | — |

A licença OFL permite uso, cópia e redistribuição das fontes (inclusive embutidas num arquivo), desde que a própria fonte não seja vendida isoladamente; os textos das licenças acompanham a pasta.

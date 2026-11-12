# A base do litoral

`terra.json` guarda o litoral (só a terra) do mundo bíblico em longitude e latitude: da Espanha (-12) à Pérsia (62) e do sul da Turquia (lat 8) ao norte do Mar Negro (lat 48). Origem: Natural Earth 10m, domínio público (ver `../LICENCAS.md`).

## Quando precisa refazer
Só se o mapa for de uma região **fora** desse retângulo (por exemplo, a Índia ou o Atlântico Norte). Dentro dele, basta pôr `quadro: lon_min lat_min lon_max lat_max` no topo do `cenas.md`.

## Como refazer (uma vez)
1. Baixe o arquivo (cerca de 10 MB, domínio público): https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson
2. Na pasta da skill, rode, com o retângulo que quiser (lon_min lat_min lon_max lat_max):
```
python3 scripts/recortar_natural_earth.py ne_10m_land.geojson base/terra.json -20 -10 80 60
```
3. Gere o mapa de novo. O arquivo bruto de 10 MB não precisa ficar guardado: baixe de novo quando precisar.

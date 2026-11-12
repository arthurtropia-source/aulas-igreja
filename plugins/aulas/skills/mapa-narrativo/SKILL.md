---
name: mapa-narrativo
description: Faz o mapa que conta uma aula passo a passo (viagem de Paulo, rota de Atos, geografia de um livro bíblico), no nível dos mapas das Cartas Paulinas. A câmera se move, o percurso se desenha, o lugar se revela e o texto da aula aparece num box. Sai um HTML que abre em qualquer computador, sem internet, e mapas parados em SVG por cena para slide ou impressão. Use quando o professor ou a equipe pedir "faz o mapa da aula", "mapa da viagem de Paulo", "mapa interativo", "mapa por passos", "mapa para o slide", ou quando um mapa que já existe saiu feio. Não use para mapa sem história (ilustração solta) nem para pedir imagem escaneada.
---

# Mapa narrativo

Transforma o que o professor disse em um mapa que **conta a aula**. O mapa não mostra tudo o que aconteceu: mostra o que a aula precisa contar. O filtro é a ideia da aula e o público.

**Pronto significa:** um `mapa.html` conferido renderizado, com cada cena aprovada pelo professor, e, se foi pedido para slide ou impressão, os `svg/cena-N.svg`. Tudo na pasta do mapa.

## 0. Antes de qualquer coisa: o corte
Pergunte e espere a resposta (não presuma):
1. **Que ideia da aula o mapa explica?** (uma frase). Se o professor não sabe dizer, o mapa não entra: a aula se explica melhor de outro jeito.
2. **Qual é o texto do professor** que vai nos boxes? Sem texto dele, não há box: o mapa só leva o que o professor disse ou escreveu. Nada de explicação sua, de doutrina ou de citação inventada.
3. **Para quê:** apresentação na tela (HTML), slide (SVG), impressão, ou os três?

## 1. O esqueleto das cenas (aprovar antes de gerar)
Mostre uma tabela simples e espere o ok do professor: número da cena, que parte da aula ela conta, onde a câmera fica, que lugares acendem, que percurso se desenha, e de que frase do professor sai o box. Regra de bolso: **uma cena = uma ideia**; 5 a 9 cenas para uma aula; o box leva no máximo 3 frases do professor.

## 2. A pasta do mapa
Crie uma pasta por mapa (ex.: `mapas/segunda-viagem/`) com quatro arquivos. O `exemplo/` desta skill é o modelo para copiar.

| Arquivo | O quê |
|---|---|
| `cenas.md` | O roteiro, uma cena por `## `. As instruções estão no topo do arquivo do exemplo. É aqui que se corrige. |
| `lugares.csv` | Cada lugar com lon/lat, se é destaque, e **a fonte da coordenada**. |
| `rotas.md` | As rotas nomeadas, trecho a trecho (terra, mar, estrada, tracejada, rio), com a fonte. |
| `regioes.csv` | Rótulos de região, mar e rio, com a faixa de zoom em que aparecem. |

- **Lugares:** comece pela `biblioteca/lugares.csv` (50 lugares do mundo de Paulo; as coordenadas são aproximadas, com erro de poucos quilômetros: servem para mapa de aula, não para medir distância). Copie as linhas de que precisa. Lugar que não está lá: acrescente com longitude e latitude **de uma fonte que você possa citar** (atlas bíblico, Pleiades, Wikipédia) e escreva a fonte na coluna `fonte`. Não deduza coordenada de memória.
- **Rotas:** a biblioteca tem as rotas de Paulo (`biblioteca/rotas.md`: primeira, segunda e terceira viagens, viagem a Roma, Via Egnátia). A rota **não vem do professor**, vem de Atos e de atlas: o mapa diz isso numa nota ("Rota segundo Atos 15:36–18:22; contexto geográfico"). Rota que a fonte não traz: escreva "a confirmar" na nota, nunca invente.
- **Outra região do mundo** (Israel, Egito, Mesopotâmia): ponha no topo do `cenas.md` a linha `quadro: lon_min lat_min lon_max lat_max`. A base de litoral cobre da Espanha à Pérsia e do sul da Turquia à Etiópia (`-12 8 62 48`). Fora disso, veja `base/LEIA-ME.md`.

## 3. Gerar
```
python3 scripts/gerar_mapa.py <pasta-do-mapa>          # mapa.html
python3 scripts/gerar_mapa.py <pasta-do-mapa> --svg    # e svg/cena-N.svg (um mapa parado por cena)
```
No Windows, `python` no lugar de `python3`. Só Python 3.8 ou mais novo, sem instalar nada.
O gerador **recusa** lugar que não está em `lugares.csv`, percurso que não é um trecho contínuo da rota citada e cena sem título, texto ou fonte. Quando recusar, conserte o arquivo; não contorne.

## 4. Conferir renderizado (obrigatório)
Abra o `mapa.html` e passe cena por cena (→ avança, ← volta). Confira:
- cada lugar da cena aparece e o rótulo não cobre outro (se cobrir, ajuste `rótulo_dx` e `rótulo_dy` em `lugares.csv`);
- o percurso segue o caminho que o texto conta (e não cruza terra onde era mar);
- o texto do box é **literal** do professor e a `fonte` de cada cena diz de onde veio;
- a câmera mostra o que a cena precisa, nem mais nem menos (ajuste `câmera`);
- nada de termo chulo ou coloquial pesado no box, mesmo que esteja no texto do professor: troque pela descrição concreta que ele mesmo dá.
Depois mostre ao professor. **Professor e aluno recebem o mesmo mapa**: nada de nota ao professor nem frase que soe como orientação a quem dá a aula.

## 5. O que dá para mexer, e o que não
- **Mexe sempre:** o conteúdo da pasta do mapa (`cenas.md`, `lugares.csv`, `rotas.md`, `regioes.csv`).
- **Mexe só se o pedido for de visual:** `molde/viagem.css` (cores, tamanhos), `molde/viagem.html`. O visual atual (pergaminho, mar verde-azulado, rota carmesim, Cinzel e Crimson Text, névoa nos lugares ainda não visitados) é o que foi aprovado; mude com um motivo e mostre antes e depois.
- **Não mexe:** `base/terra.json` (o litoral) e `scripts/gerar_mapa.py`, a não ser para corrigir um defeito.

## 6. Atalhos do mapa na tela
→ ou espaço ou clique: avança · ← volta · A: modo automático (usa a duração de cada cena) · F: tela cheia · N: esconde a linha de fonte · `#5` no fim do endereço abre na cena 5. No celular em pé o box fica embaixo; deslizar também avança.

## 7. Ativos e licenças
Litoral: Natural Earth, domínio público. Fontes Cinzel e Crimson Text: licença SIL OFL, embutidas no HTML. Tudo registrado em `LICENCAS.md`. O mapa traz no rodapé "Litorais: Natural Earth 10m (domínio público)". Imagem, ícone ou fonte nova só entra com a origem e a licença registradas em `LICENCAS.md`; na dúvida, pergunte.

## 8. Como esta skill nasceu e o que ela aprendeu
Leia `historia-e-regras.md` antes de mudar o jeito de fazer. Correção que o professor fizer num mapa entra lá, com a data.

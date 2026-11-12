# Como esta skill nasceu e as regras que aprendeu

> Fonte: o histórico do projeto de aulas da Turma Especial no Cowork (setembro a outubro de 2026), recuperado e conferido em novembro de 2026. O que é fato do histórico vem marcado; o que é decisão de empacotamento vem marcado como tal.

## A história, em ordem
- **17/09/2026, os sete mapas das Cartas Paulinas.** O PDF de outro professor (190 slides) tinha sete mapas, todos imagens escaneadas de baixa resolução. Foram reconstruídos como SVG vetorial sobre o litoral da Natural Earth 10m (gerador em JavaScript com d3-geo, projeção Mercator). Escolhas visuais: terra cor de pergaminho, mar azul claro, rota carmesim, cidades das cartas em cor cheia, alto contraste. Cada mapa levou uma nota de rodapé dizendo que rotas e distâncias vêm de Atos e de atlas, não do material do professor. Saíram também uma galeria de revisão e um mapa interativo.
- **05 a 09/10/2026, o mapa por passos.** Na Aula 1 de Epístolas Paulinas II, o mapa virou interativo: cada passo destaca o trecho da rota, a cidade em foco e um zoom proporcional; o resto da rota esmaece; a seta avança o passo antes de mudar de página e o clique no mapa também avança. Foi o recurso mais elogiado. Entrou nas Aulas 5 (vale do Lico) e 7 (Via Egnátia), com uma etiqueta "Mapa interativo" no sumário.
- **20/10/2026, a regra central**: *o mapa não mostra tudo o que aconteceu, mostra o que a aula precisa contar.* O mapa da Aula 1 cobre a segunda viagem inteira, mas os passos destacam só o que serve à implantação da igreja de Tessalônica.
- **20/10/2026, a perda.** O gerador e o litoral recortado ficavam na pasta temporária do Cowork e sumiram quando ele reiniciou. Sobraram os HTML entregues. Lição: **o código e a base que produzem um mapa moram no repositório, nunca só na sessão.**
- **09/11/2026, a reconstrução.** A extração do projeto trouxe os sete mapas desprojetados (lugares, rotas, rótulos); com ela se refez o gerador e nasceu a "viagem pelo mapa", versão generalizada: roteiro de cenas em texto, câmera, névoa nos lugares ainda não visitados, percursos, cartas em voo, estilo de mapa antigo.
- **11/11/2026, esta skill** (decisão de empacotamento): a "viagem pelo mapa" virou a `mapa-narrativo`, agora com o quadro do mapa à escolha, o litoral guardado em longitude e latitude (`base/terra.json`), as fontes embutidas (funciona sem internet), a exportação de SVG parado por cena e a biblioteca de lugares e rotas.

## Regras que o histórico fixou
1. **Didática antes do visual.** Nenhum mapa entra sem responder: que ideia ele explica e por que ela se explica melhor assim.
2. **Só a palavra do professor.** O box leva o que o professor disse ou escreveu; nada acrescentado. Quando um box fica sem contexto, complete com outra frase do próprio texto dele, nunca com redação nova.
3. **Fidelidade da rota.** A rota, as estradas e as distâncias vêm de Atos e de atlas, não do professor. O mapa diz isso numa nota. Rota sem fonte: "a confirmar".
4. **Vetorial, nunca imagem escaneada.** A base é o litoral da Natural Earth.
5. **Professor e aluno recebem o mesmo material.** Sem nota ao professor dentro do mapa.
6. **Sem termo chulo ou coloquial pesado,** mesmo que esteja na fonte.
7. **Ver renderizado antes de entregar.**
8. **Mapa por passos, uma ideia por cena;** o filtro é o objetivo da aula e o público.
9. **Cada licença registrada.** Ver `LICENCAS.md`.

## O que ainda não está resolvido (honesto)
- O visual da "viagem pelo mapa" estava em aprovação na versão anterior; esta skill o herda sem mudar.
- O mapa não imprime os passos: no papel, use o SVG de cada cena (`--svg`).
- Os mapas das Cartas Paulinas de 17/09 eram SVG estáticos com a paleta clara do guia; o SVG parado desta skill usa a paleta do mapa narrativo (pergaminho e mar verde-azulado). É parecido, não idêntico.
- Coordenadas da biblioteca são aproximadas (desprojetadas de imagens, erro de poucos km). Se o professor precisar de precisão, confira no atlas e corrija a linha.
- Rios e lagos pequenos não estão na base (só a terra); rio entra como rota do tipo `rio`, em traçado esquemático.

## Correções do professor (acrescente aqui, com data)
- (nenhuma ainda)

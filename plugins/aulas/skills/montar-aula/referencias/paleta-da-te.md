# Rota D: pôr uma aula pronta na paleta da Turma Especial

> Referência da skill `montar-aula` (0.2.0). Para a aula que **já existe**, feita fora do motor (PowerPoint, Google Slides, PDF de slides, Canva, um HTML antigo), e que só precisa ganhar a identidade da TE. O conteúdo já foi aprovado por quem fez: aqui não se seleciona nem se reescreve, **converte-se**.

## O que muda em relação à rota B
| | Rota B (montar) | Rota D (paleta) |
|---|---|---|
| Entrada | Texto, gravação ou PowerPoint do professor, para selecionar | Uma aula pronta, slide a slide |
| Briefing | Completo | Só três dados: matéria, número da aula e quem fez o original |
| Texto | Selecionado e organizado | **Mantido como está**, slide a slide |
| Esqueleto | Aprovado antes | A tabela de correspondência (abaixo), mostrada junto com a aula gerada |

## Passos
1. **Guardar o original** em `materias/<matéria>/aula-N/fonte/`, intocado. Se veio pelo chat, salve o arquivo ali.
2. **Ler slide a slide.** PowerPoint, PDF ou imagem: leia com o que o ambiente tiver (as habilidades de PowerPoint e de PDF do próprio Claude servem). Se não conseguir ler um formato, peça o PDF exportado. HTML antigo da Turma Especial (feito no Cowork em 2026): use o conversor `scripts/motor/ferramentas/html_para_aula.py` (uso no topo do arquivo).
3. **Escrever o `aula.md`** (formato em `formato-do-aula-md.md`), um slide original para uma página, na mesma ordem:
   - o texto do slide entra **literal**; só se corta o que é nota ao professor ou emoji (vão para as pendências, para não sumir em silêncio);
   - escolha o bloco pelo que o slide faz (lista, cartões, par, versículo, linha do tempo); título em `título`, a palavra-chave em `==assim==`;
   - capa: `tipo: capa da aula` (ou `capa do curso` se for a abertura da matéria);
   - versículo citado por inteiro: siga `biblia.md` (a ARA de comparação, se o original não a traz, vai para as pendências, não se inventa);
   - **imagem do original:** foto de pessoa só com o ok de quem responde pelo curso; imagem de terceiro só com a origem registrada no `registro.md`. Mapa: use os mapas-base da TE (mapa por passos), não a imagem colada; região sem mapa-base fica com a imagem do original e uma linha em `sugestoes/`.
4. **Slide que não cabe** numa página: divida em duas e diga na tabela. Não diminua letra nem mexa no molde.
5. **Gerar e conferir** (seção 5 da skill).
6. **Mostrar a tabela de correspondência** junto da aula gerada:
   ```
   | Slide original | Página nova | O que mudou |
   | 1 | 1 (capa da aula) | — |
   | 4 | 4 e 5 | dividido: texto longo demais para uma página |
   ```
7. **Registro** (seção 9 da skill), com a entrada "aula pronta, convertida para a paleta da TE".

## O que não fazer
- Não "melhorar" o texto, não acrescentar slide, não trocar a ordem. Se algo parece errado no original, vai para as pendências.
- Não rodar o validador de entendimento como obrigatório: a aula já foi dada ou aprovada assim. Rode só se pedirem.

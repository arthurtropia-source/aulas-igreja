---
name: conferir-aula
description: Confere uma aula gerada (aula-N.html) antes de entregar — transbordo, folga sob o título e antes do rodapé, cartão vazio, mapa por passos — com o conferir.py (ou a conferência de reserva onde o Playwright não roda, como no Cowork), a folha de contato olhada página a página e, quando pedido ou na aula do zero, o validador de entendimento (um agente que lê como aluno de primeira vez). Use quando pedirem "confere a aula", "está tudo cabendo?", "valida se a aula se entende", e ao fim de converter-aula, incluir-mapa, corrigir-aula e aula-do-zero. Não muda o conteúdo por conta própria. Em dúvida, comece pela skill aula.
---

# Conferir uma aula

> **A pasta comum** (motor, identidade da TE, mapas-base e referências) fica na skill `aula`, ao lado desta: `../aula/`. Os caminhos `aula/...` abaixo são a partir dela.

## 0. Condição de entrada
| Pergunta | Se não |
|---|---|
| Existe `aula-N.html` gerado a partir do `aula.md` atual? | Gere: `python3 aula/scripts/motor/gerar.py materias/<matéria>/aula-N` (só precisa do Python 3.9+). Erro no `aula.md` vem com a linha: conserte o arquivo, não o motor |

## 1. A conferência (uma rota, conforme o ambiente)
**O Playwright com o Chromium está instalado?** (tente `python3 -c "import playwright"`)
- **Sim:** `python3 aula/scripts/motor/conferir.py materias/<matéria>/aula-N/aula-N.html`.
- **Não, e dá para instalar** (aba Code): pergunte antes; com o ok, `python3 -m pip install playwright` e `python3 -m playwright install chromium`, e rode a linha de cima.
- **Não, e não dá** (ex.: o Cowork): a **conferência de reserva**, `aula/referencias/conferencia-de-reserva.md`, dita no registro.

## 2. Falhas
Toda FALHA se corrige no `aula.md` (menos texto do professor, outro bloco, dividir a página) e gera-se de novo. **Não mexa no molde para fazer caber.** Falha que só se resolve com frase nova: leve à pessoa, não escreva.

## 3. Olhar
**Olhe a folha de contato** (`conferencia/folha-de-contato.png`) e, se houver mapa, a folha dos mapas. Conferência automática sem olhar não vale. Para mostrar a aula, entregue o `aula-N.html` (abre em qualquer navegador, sem internet).

## 4. Validador de entendimento (na aula do zero, ou quando pedirem)
Um agente separado, que não viu a conversa, com o roteiro de `aula/referencias/validador-de-entendimento.md`. Devolve, bloco a bloco, ALCANÇADO, PARCIAL ou NÃO ALCANÇADO, e até 10 correções. Sem agente separado no ambiente: diga isso no registro e faça a leitura você mesmo, pelo mesmo roteiro, deixando claro que não foi independente.

## Pronto quando
Nenhuma FALHA (ou a reserva feita e dita) · folha de contato olhada · validador rodado quando cabia · resultado no `registro.md` (`aula/referencias/registro.md`).

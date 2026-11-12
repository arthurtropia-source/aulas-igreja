# Changelog

## 0.3.0 (12/11/2026): uma porta de entrada e uma skill por tarefa
- **A `montar-aula` foi dividida** (decisão de 12/11/2026, com o viés determinístico: se isto, então aquilo). A porta de entrada **`aula`** confere a pasta e o que chegou e manda para a skill certa, sem o modelo escolher pela probabilidade: aula já no formato (lista fechada: incluir mapa, corrigir, conferir), aula pronta de fora (`converter-aula`) ou material do professor (`aula-do-zero`).
- **Cinco skills de tarefa**, cada uma com a condição de entrada, os passos e a linha de chegada: `converter-aula` (a antiga rota D, texto literal, design da TE), `incluir-mapa` (mapa por passos sobre os mapas-base; região nova: "ainda não"), `corrigir-aula`, `aula-do-zero` (texto-base ou gravação; a antiga rota B) e `conferir-aula` (conferência e validador).
- **PowerPoint ou PDF de slides é sempre aula pronta** (`converter-aula`); refazer do zero só quando pedido.
- O que é comum (motor, identidade da TE, mapas-base, regras) mora na skill `aula`; as outras leem `../aula/`. Motor sem mudança. Nova referência comum: `registro.md`. Saiu `paleta-da-te.md` (virou a `converter-aula`).

## 0.2.1 (12/11/2026): a pasta do curso chega pronta
- **`montar-aula`:** não monta mais a pasta do curso. Se a tarefa não está na pasta do curso, pede para abrir a pasta Turma Especial recebida (+ > Adicionar pasta) e para. Saíram `referencias/primeira-utilizacao.md` e `modelo-da-pasta/`; o aviso de atualização automática ficou em `referencias/aviso-de-atualizacao.md`, com os nomes reais dos menus do app.
- **Sai a skill `mapa-narrativo`** (a "viagem pelo mapa", a aula inteira dentro de um mapa). Fica só o mapa por passos dentro do slide, sobre os mapas-base. Mapa de região nova: a `montar-aula` diz que ainda não se faz e registra em `sugestoes/`. A prova deixa de gerar o exemplo do mapa.
- A pasta pronta é entregue por quem cuida do curso, fora deste repositório. Motor sem mudança (só um comentário).

## 0.2.0 (12/11/2026): o plugin se basta sozinho, com a Turma Especial como curso padrão
- **Identidade da Turma Especial dentro do plugin** (`montar-aula/cursos/turma-especial/`): logo, cores, as 3 fontes SIL OFL com as licenças, o design system oficial sem as fotos de turma, e os 3 mapas-base de Epístolas Paulinas II. Decisão de 12/11/2026, que muda a regra "público, só método".
- **Motor:** sem `identidade/` na pasta do curso, usa a do plugin (o curso do campo `curso`, padrão `turma-especial`); os mapas-base do plugin entram por último na busca. Pasta do curso com identidade própria continua valendo por cima.
- **`montar-aula` v0.2:** novo corte (primeiro a pasta, depois a rota); **primeira utilização** monta o mínimo da pasta do curso (`memoria.md`, `mapa-das-aulas.md`, `passagem.md`, `sugestoes/`, `materias/`, `.claude/settings.json`) com o aviso de atualização automática e como desligar; **rota D**, pôr uma aula pronta na paleta da TE; conferência de reserva quando o Playwright não roda.
- **Contexto nas referências:** `regras-de-fonte.md`, `didatica.md`, `biblia.md`, `curso-turma-especial.md`, sem nome de pessoa.
- Exemplos de aula real trocados por neutros em `formato-do-aula-md.md`; nomes de pessoa tirados dos textos.
- `teste/provar.sh` prova sem pasta do curso: só o `aula.md` numa pasta vazia.
- Prova: Aula 1 idêntica sem pasta do curso (registro em `teste/`).

## 0.1.2 (12/11/2026): teste da atualização automática
- Sem mudança de método. Versão subida para provar que a pasta do curso recebe a versão nova sozinha (registro em `teste/`).

## 0.1.1 (12/11/2026): design system do curso
- `montar-aula`: lê o design system oficial do curso quando ele existe em `identidade/design-system/` da pasta do curso, e segue as regras de conteúdo dele (regra 9 da seção 4). Conflito com o desenho do motor vai para `sugestoes/`, sem mexer no molde.
- `referencias/pasta-do-curso.md`: a pasta `identidade/design-system/` entra na arrumação da pasta do curso.
- O design system da Turma Especial **não** entra no plugin (o plugin é público e só leva método): foi para a pasta do curso. Motor sem mudança.
- Prova: Aula 1 idêntica (registro em `teste/`).

## 0.1.0 (11/11/2026): bancada, só local
- Primeira montagem. Não publicada.
- `montar-aula` v0.1 (rascunho): uma skill só, com o corte, o briefing, o esqueleto aprovado, a montagem pelo motor, as conferências, o validador de entendimento, a marcação da fonte e o registro. Ainda não rodou numa aula real.
- Motor copiado de `igreja/aulas/motor/` (commit `95f773b`), com quatro ajustes para funcionar fora da pasta de origem (lista em `plugins/aulas/ORIGEM.md`).
- `mapa-narrativo` v1 copiada sem alteração.
- Prova: a Aula 1 de Epístolas Paulinas II, gerada pelo plugin instalado numa pasta limpa, saiu idêntica à original (registro em `teste/`).

# Roteiro: o teste de dois computadores

> Para quem mantém o plugin. v1, 11/11/2026. Um passo de cada vez: só avance quando o "tem de aparecer" do passo aparecer. Se não aparecer, pare, anote na tabela do fim e me chame.

## O que este teste decide
**O corte:** no Cowork, com a pasta do curso no Drive em modo espelhado, a Aula 1 sai idêntica à original e uma linha gravada na memória chega inteira ao segundo computador, no Mac e no Windows?
- **Sim:** quem opera usa o **Cowork** (nada de Python a instalar).
- **Não:** quem opera usa a **aba Code**, com Python instalado no computador.

Tempo: uns 40 minutos no Mac e 40 no segundo computador.

## O que já está pronto no seu Mac
| O quê | Onde |
|---|---|
| A pasta do curso | `~/Documents/bancada-aulas-igreja/turma-especial/` (3 MB) |
| O plugin em zip | `<pasta do repositório>/entrega/aulas-0.1.1.zip` |
| O número que prova a Aula 1 (sha256) | começa com `722e03ae` e termina com `27e36` |

**Conta do Google para o teste:** qualquer uma sua serve (a pasta definitiva vai para uma conta da igreja, que ainda não existe). Não ponha a pasta numa conta de aluno.

---

## Parte 1: o Drive, no Mac
1. Abra o Google Drive para computador (ícone na barra de cima) > engrenagem > Preferências > Google Drive > marque **"Espelhar arquivos"**.
   **Tem de aparecer:** o Drive pede uma pasta no disco para o "Meu Drive" e começa a baixar. (Se o seu Drive for grande, isso ocupa disco: se não quiser espelhar tudo, me diga e trocamos por uma conta só para o teste.)
2. Copie a pasta `turma-especial` para dentro do "Meu Drive" (no Finder).
   **Tem de aparecer:** todos os arquivos com o visto verde de sincronizado.

## Parte 2: o Cowork, no Mac
3. No app do Claude, confira no canto a conta e o plano em que está. Anote na tabela.
4. No Cowork: Customize (Personalizar) > Plugins > enviar arquivo > escolha `aulas-0.1.1.zip`.
   **Tem de aparecer:** o plugin "aulas" na lista, com as skills `aula`, `converter-aula`, `incluir-mapa`, `corrigir-aula`, `aula-do-zero` e `conferir-aula` (desde a 0.3.0).
5. Abra uma tarefa nova no Cowork e conecte a pasta `turma-especial` **do Drive** (a do "Meu Drive", não a de Documentos).
6. Escreva:
   > Use a skill aula. Gere de novo a Aula 1 de Epístolas Paulinas II (só o passo de gerar) e me diga o sha256 do aula-1.html.

   **Tem de aparecer:** "18 páginas" e um sha256 que começa com `722e03ae` e termina com `27e36`.
   Se ele disser que não tem Python, ou o número for outro: pare e anote.
7. Escreva:
   > Agora rode a conferência (conferir.py) dessa aula.

   **Tem de aparecer:** "nenhuma falha". Se ele disser que falta o Playwright ou o Chromium, anote o que ele propôs e **não mande instalar** ainda. (Isso não reprova o Cowork; só diz que a conferência precisa de outro caminho.)
8. Escreva:
   > Acrescente no fim do memoria.md esta linha, sem mudar mais nada: "- 2026-11-11: linha de teste do Mac, com acento: ação, coração, é."

   **Tem de aparecer:** abra o `memoria.md` no Finder: a linha está no fim e o resto do arquivo está inteiro (a regra de 07/11 continua lá).

## Parte 3: o segundo computador (de preferência o Windows)
9. Instale o Google Drive para computador, entre com a mesma conta e marque **"Espelhar arquivos"**. Espere sincronizar.
   **Tem de aparecer:** a pasta `turma-especial` no disco, e o `memoria.md` com a linha de teste do Mac, com os acentos certos.
10. Leve o `aulas-0.1.1.zip` para esse computador (pelo próprio Drive, fora da pasta do curso) e repita os passos 3 a 6.
    **Tem de aparecer:** o mesmo sha256 (`722e03ae…27e36`).
11. Repita o passo 8 com a frase "linha de teste do Windows". Volte ao Mac, espere sincronizar e abra o `memoria.md`.
    **Tem de aparecer:** as duas linhas de teste, na ordem, e o arquivo inteiro. Nenhum arquivo com "cópia" ou "conflito" no nome dentro da pasta.

## Parte 4: só se o Cowork reprovar (passo 6, 8, 10 ou 11)
12. No mesmo computador, abra a aba Code do app do Claude na pasta `turma-especial` do Drive e escreva "que versão do Python tem aqui?".
    **Tem de aparecer:** Python 3.9 ou mais novo. No Windows, se não tiver: instale de python.org marcando "Add python to PATH" e repita.
13. A aba Code não aceita o zip: ela instala pelo endereço do repositório, que ainda não foi publicado. Aqui eu preciso do seu ok para publicar (decisão 1, abaixo) ou você copia a pasta `plugin-aulas` inteira para o computador e escreve na aba Code: "adicione o marketplace da pasta <caminho> e instale o plugin aulas".
14. Repita os passos 6, 8 e 11 na aba Code.

## Limpar depois
Tire as duas linhas de teste do `memoria.md`. Se quiser, volte o Drive para "Fazer streaming".

---

## O que anotar (me devolva esta tabela)
| | Mac | Segundo computador (qual: ______) |
|---|---|---|
| Conta e plano do Claude | | |
| 4. O plugin entrou pelo zip? | | |
| 6. Aula 1: o sha256 bateu? | | |
| 6. O Cowork tinha Python? | | |
| 7. A conferência rodou? Se não, o que faltou | | |
| 8 e 11. A linha da memória chegou inteira? | | |
| Arquivo de conflito na pasta? | | |
| Quanto tempo levou, e onde travou | | |

## Decisões que ficam com você
1. **Publicar o repositório do plugin no GitHub** (público, só método). Só é preciso para a aba Code em outro computador e para a atualização automática. Recomendo esperar o resultado das partes 1 a 3.
2. **O nome** do repositório, do catálogo e do plugin (hoje `plugin-aulas`, `aulas-igreja` e `aulas`, provisórios).

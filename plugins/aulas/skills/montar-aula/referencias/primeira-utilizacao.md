# Primeira utilização: montar a pasta do curso

> Referência da skill `montar-aula` (0.2.0). Quem usa o plugin pode chegar sem pasta nenhuma, só com o plugin instalado. A skill monta o mínimo para que nada do que importa fique na conversa: tudo fica num arquivo da pasta.

## 1. Qual é a pasta
- **Cowork:** a pasta que a pessoa conectou à tarefa. **Aba Code:** a pasta em que a sessão foi aberta.
- **Sem pasta conectada** (ou só a área temporária do Cowork): pare e peça uma, em linguagem simples:
  > "Para eu guardar as aulas e o que aprendermos, preciso de uma pasta no seu computador. Crie uma pasta (por exemplo, `Documentos/Turma Especial`) e escolha-a em *Trabalhar em uma pasta* no início da tarefa. Depois me peça de novo."
- Pasta que já tem `memoria.md` e `mapa-das-aulas.md`: já é a pasta de um curso. Pule para o passo 4 (o aviso), se ele ainda não foi dado.
- Pasta com outros arquivos que não são de curso: pergunte antes se é ali mesmo. Não espalhe arquivos na pasta de trabalho de alguém sem o ok.

## 2. O que se cria (copiado de `modelo-da-pasta/`, dentro desta skill)
| Arquivo | Para quê |
|---|---|
| `memoria.md` | As lições do curso ("daqui pra frente faça assim"), com data |
| `mapa-das-aulas.md` | O índice: uma linha por aula |
| `passagem.md` | O que está em produção e o que espera resposta de professor; o histórico |
| `sugestoes/` | O que o método deveria aprender; vira versão nova do plugin |
| `materias/` | Uma pasta por matéria e, dentro, uma por aula |
| `.claude/settings.json` | Na aba Code: liga o plugin nesta pasta e a atualização automática. No Cowork não tem efeito |

**Nunca sobrescreva** um arquivo que já existe: copie só o que falta. Não crie `identidade/`: a identidade da Turma Especial vem do plugin. Não crie `contexto/`: ele só nasce quando houver regra do curso ou de professor para guardar (`contexto/curso.md`).

Copiar com o terminal, se o ambiente tiver (troque `<skill>` pela pasta desta skill):
```
cp -Rn <skill>/modelo-da-pasta/. <pasta-do-curso>/
```
Sem terminal, crie cada arquivo com o mesmo conteúdo dos de `modelo-da-pasta/`.

## 3. Dizer onde fica cada coisa (três linhas, sem termo técnico)
> "Montei a pasta do curso: `memoria.md` guarda o que aprendermos, `mapa-das-aulas.md` é a lista das aulas e `passagem.md` é o que está em andamento. Cada aula fica em `materias/<matéria>/aula-N/`, com o material do professor em `fonte/`."

## 4. O aviso de atualização automática (uma vez por pessoa)
Diga, antes de seguir com o pedido:
> "Este método se mantém atualizado sozinho: quando há uma versão nova do plugin, o Claude a busca e aplica. Nada é instalado fora do Claude e nada da sua pasta é apagado. Para desligar: no Cowork, em *Personalizar > Plugins*, desligue a sincronização automática do catálogo `aulas-igreja`; na aba Code, me peça "desliga a atualização automática"."

Depois, uma linha no `passagem.md`, tabela **Histórico**: `| <data> | aviso de atualização automática dado |`. Se a linha já existe, não repita o aviso.

**Para desligar (a pedido):** na aba Code, troque `"autoUpdate": true` por `false` em `.claude/settings.json` da pasta e avise que vale para todos que usam a pasta. No Cowork, quem desliga é a própria pessoa, no menu de plugins (a skill não mexe nas configurações do app).

## 5. Seguir com o pedido
Volte ao corte da skill (seção 0) com a pasta pronta.

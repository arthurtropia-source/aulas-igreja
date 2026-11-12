# Aviso de atualização automática

> Referência da skill `montar-aula` (0.2.1). A pasta do curso chega pronta a quem usa: a skill não monta pasta. Este aviso é dado uma vez por pasta.

## O aviso (uma vez)
Se o `passagem.md` da pasta do curso ainda não registra o aviso, diga, antes de seguir com o pedido:
> "Este método se mantém atualizado sozinho: quando há uma versão nova do plugin, o Claude a busca e aplica. Nada é instalado fora do Claude e nada da sua pasta é apagado. Para desligar: no app, + > Adicionar plugins (janela de Plugins), desligue a sincronização automática do marketplace `aulas-igreja`; na aba Code, me peça "desliga a atualização automática"."

Depois, uma linha no `passagem.md`, tabela **Histórico**: `| <data> | aviso de atualização automática dado |`. Se já há linha de aviso, não repita.

## Para desligar (a pedido)
- **Aba Code:** troque `"autoUpdate": true` por `false` em `.claude/settings.json` da pasta do curso e avise que vale para todos que usam a pasta.
- **Cowork:** quem desliga é a própria pessoa, na janela de Plugins. A skill não mexe nas configurações do app.

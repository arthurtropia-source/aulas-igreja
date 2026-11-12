# Teste: atualização automática do plugin

**Data:** 12/11/2026 · **Pedido:** o plugin se manter atualizado sozinho no computador de quem usa, sem a pessoa fazer nada, com aviso na primeira utilização e um jeito de desligar.

## Como ficou
- **Não há programa agendado no computador da pessoa.** A atualização é do próprio Claude: a pasta do curso traz `.claude/settings.json` com o catálogo `aulas-igreja`, `"autoUpdate": true` e o plugin ligado. Quando o Claude abre nessa pasta, ele busca a versão nova e a aplica. É o mesmo desenho que o Business Creator usa.
- **Aviso e desligar:** o `AGENTS.md` da pasta do curso manda avisar na primeira conversa de cada pessoa (texto pronto) e registrar o aviso no `passagem.md`. Para desligar: `"autoUpdate": false` no arquivo, para todos, ou o menu de plugins do Claude, só para aquele computador.

## O que foi provado
| Prova | Resultado |
|---|---|
| Cópia nova da pasta do curso, com o `settings.json`, aberta numa sessão do Claude | O plugin entra ligado (0.1.1) sem comando nenhum |
| Versão subida para 0.1.2 no repositório; nova sessão na pasta | A sessão já mostrou 0.1.2, sem `update` nem reinstalar |

## O que não foi provado
- **Nesta bancada, o catálogo é uma pasta local:** o Claude lê o plugin direto da pasta, então ele já fica sempre em dia. Isso só vale no Mac de quem mantém o plugin.
- **No computador de outra pessoa, o catálogo tem de ser o repositório no GitHub** (`"source": "github"`). A atualização automática por esse caminho só se prova depois de publicar.
- **No Cowork, a pasta não liga o plugin sozinha.** A atualização é por catálogo ("Sync automatically" ao adicionar `owner/repo`). Plugin enviado por zip não se atualiza. Qual é o padrão dessa opção, a documentação não diz: a pessoa liga uma vez.
- **A confiança na pasta:** na primeira vez, o Claude pede para confiar na pasta e instalar o plugin. É um clique da pessoa e não dá para pular. É a trava do próprio Claude.

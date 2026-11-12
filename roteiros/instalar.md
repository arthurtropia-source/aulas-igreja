# Instalar o plugin das aulas

> Para quem vai fazer as aulas. v2, 12/11/2026 (plugin 0.2.0). Um passo de cada vez. Os nomes dos menus do app podem variar um pouco de versão para versão.
> **Nomes conferidos na tela real** (app do Claude em português, 12/11/2026) até o botão "Adicionar" do plugin. A geração da aula dentro do Cowork ainda não foi provada; a aba Code foi provada no Mac.

## Caminho 1: Cowork (o padrão)
1. Abra o app do Claude e vá ao **Cowork**.
2. No campo de mensagem, clique no **+** e em **Adicionar plugins** (abre Configurações > Plugins).
3. **+ Adicionar > Adicionar marketplace**. Clique no campo **URL**, cole `arthurtropia-source/aulas-igreja` e escolha **Usar "arthurtropia-source/aulas-igreja"**. Deixe **Sincronizar automaticamente** ligado e clique em **Sincronizar**.
4. No plugin **Aulas** (por aulas-igreja), clique em **Adicionar**. Feche a janela.
5. Crie no computador uma pasta para o curso (ex.: `Documentos/Turma Especial`).
6. No campo de mensagem do Cowork, **+ > Adicionar pasta** e escolha essa pasta. Peça: *"Monta a pasta do curso da Turma Especial e me diz onde fica cada coisa."*
7. Tem de aparecer: os arquivos `memoria.md`, `mapa-das-aulas.md`, `passagem.md` e as pastas `sugestoes/` e `materias/`, e o aviso de atualização automática.
8. Primeira aula: **+ > Fazer upload ou adicionar arquivos**, escolha o texto-base e peça *"Põe esse texto-base em slides."*

Se o Claude disser que não consegue rodar o Python ou gerar a aula: vá ao caminho 2.

## Caminho 2: aba Code (reserva)
1. Instale o Python 3 (python.org; no Windows, marque "Add Python to PATH").
2. No app do Claude, aba **Code**, abra uma sessão **na pasta do curso**.
3. Cole, uma linha por vez:
```
claude plugin marketplace add arthurtropia-source/aulas-igreja
claude plugin install aulas@aulas-igreja
```
   (ou peça ao Claude da sessão para rodar as duas linhas)
4. Abra uma sessão nova na mesma pasta e faça o pedido do passo 6 do caminho 1.

## Vídeo
Há um vídeo curto (telas ilustrativas, com legendas) que mostra o caminho 1. Quem mandou o plugin manda o vídeo junto.

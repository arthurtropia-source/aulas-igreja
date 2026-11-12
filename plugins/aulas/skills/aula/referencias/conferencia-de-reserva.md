# Conferência de reserva (quando o Playwright não roda)

> Referência comum das skills de aula (mora na skill `aula`; 0.3.0). A conferência automática (`conferir.py`) abre a aula num navegador sem tela (Playwright com o Chromium) e mede cada página. Onde isso não roda, vale esta reserva. Ela é mais fraca: diga no `registro.md` da aula que a conferência foi a de reserva.

## 1. Tentar a automática primeiro
Pergunte antes de instalar. Com o ok:
```
python3 -m pip install playwright
python3 -m playwright install chromium
```
Se instalar e rodar, use a conferência normal (skill `conferir-aula`) e pare aqui.

## 2. A reserva
1. **Gerar** com `gerar.py` (só precisa do Python) e ver a linha `ok: ... (N páginas)`.
2. **Conferir o texto contra os limites do molde**, no `aula.md`, página a página:
   - título com mais de ~60 caracteres, ou mais de 2 linhas: encurte com as palavras do professor ou divida a página;
   - mais de 4 cartões numa linha, ou cartão com mais de ~220 caracteres de texto: divida;
   - lista com mais de 6 itens: `compacta`, `duas colunas` ou duas páginas;
   - cartão só com rótulo, sem título nem texto: complete com o texto do professor ou tire.
3. **Olhar renderizado:** abra o `aula-N.html` (no Cowork, ele aparece para a pessoa; na aba Code, no navegador) e peça a quem pediu a aula para passar página por página (seta →) e apontar: texto cortado, texto encostado no rodapé, cartão vazio. Não declare a aula conferida antes dessa volta.
4. **Registrar** no `registro.md`: "conferência de reserva (sem Playwright)", o que foi checado e o que a pessoa apontou.

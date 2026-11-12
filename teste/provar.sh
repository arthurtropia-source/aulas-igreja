#!/bin/sh
# Prova de uma versão do plugin: a aula de referência, gerada pelo plugin SEM pasta do curso
# (só o aula.md numa pasta vazia), tem de sair idêntica (byte a byte)
# ao HTML de referência. Desde a 0.2.0 a identidade e os mapas-base da Turma Especial vêm do plugin.
#
# Uso:
#   sh teste/provar.sh <raiz-do-plugin> <aula.md-de-referência> <html-de-referência> [--conferir]
# Exemplo (plugin instalado, Aula 1 de Epístolas Paulinas II):
#   sh teste/provar.sh ~/.claude/plugins/cache/aulas-igreja/aulas/0.2.0 <caminho>/aula-1/aula.md <caminho>/aula-1/aula-1.html --conferir
#
# A aula de referência não mora no plugin (é texto de professor): fica com quem mantém o plugin.
# Sai com código 0 se tudo passou e 1 se algo diferiu.
set -u
PLUGIN=$1; AULAMD=$2; REF=$3; CONFERIR=${4:-}
PY=python3; command -v python3 >/dev/null 2>&1 || PY=python
MOTOR="$PLUGIN/skills/montar-aula/scripts/motor"
TMP=$(mktemp -d)
falhas=0
echo "plugin:      $PLUGIN (versão $(sed -n 's/.*"version": *"\(.*\)".*/\1/p' "$PLUGIN/.claude-plugin/plugin.json"))"
echo "python:      $($PY --version 2>&1)"
echo "pasta limpa: $TMP (sem pasta do curso: só o aula.md)"

# 1. a aula de referência, sem identidade/ nem mapas/ por perto
NOME=$(basename "$REF" .html)
mkdir -p "$TMP/materia/$NOME"
cp "$AULAMD" "$TMP/materia/$NOME/aula.md"
$PY "$MOTOR/gerar.py" "$TMP/materia/$NOME" || falhas=1
if cmp -s "$TMP/materia/$NOME/$NOME.html" "$REF"; then
  echo "1. aula:     IDÊNTICA à referência ($(wc -c < "$REF" | tr -d ' ') bytes, sha256 $(shasum -a 256 "$REF" | cut -c1-16)…)"
else
  echo "1. aula:     DIFERENTE da referência"; falhas=1
fi

# 2. as conferências do motor (pede Playwright com Chromium)
if [ "$CONFERIR" = "--conferir" ]; then
  if $PY "$MOTOR/conferir.py" "$TMP/materia/$NOME/$NOME.html"; then
    echo "2. conferir: sem falha"
  else
    echo "2. conferir: FALHOU (ou o Playwright não está instalado)"; falhas=1
  fi
else
  echo "2. conferir: não rodado (acrescente --conferir)"
fi

[ $falhas -eq 0 ] && echo "RESULTADO: PASSOU" || echo "RESULTADO: FALHOU"
exit $falhas

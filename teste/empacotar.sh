#!/bin/sh
# Monta o zip do plugin para instalar à mão (Cowork: Customize > Plugins > enviar zip).
# Sai em entrega/aulas-<versão>.zip. A pasta entrega/ não sobe ao git.
set -eu
cd "$(dirname "$0")/.."
V=$(sed -n 's/.*"version": *"\(.*\)".*/\1/p' plugins/aulas/.claude-plugin/plugin.json)
mkdir -p entrega
rm -f "entrega/aulas-$V.zip"
(cd plugins && zip -qr "../entrega/aulas-$V.zip" aulas -x '*.DS_Store' -x '*__pycache__*')
echo "ok: entrega/aulas-$V.zip ($(wc -c < "entrega/aulas-$V.zip" | tr -d ' ') bytes, $(unzip -l "entrega/aulas-$V.zip" | tail -1 | awk '{print $2}') arquivos)"

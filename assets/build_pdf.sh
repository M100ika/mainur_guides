#!/usr/bin/env bash
# Собирает PDF из markdown-гайда: pandoc -> HTML (+ фикс эмодзи в bold) -> Chrome headless -> PDF
# Использование: assets/build_pdf.sh guides/имя-файла.md
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MD_FILE="$1"
SLUG="$(basename "$MD_FILE" .md)"
TMP_HTML="$(mktemp --suffix=.html)"
OUT_PDF="$ROOT_DIR/pdf/$SLUG.pdf"

pandoc "$MD_FILE" \
  --standalone \
  --css="$ROOT_DIR/assets/style.css" \
  --embed-resources --resource-path="$ROOT_DIR" \
  -o "$TMP_HTML"

python3 "$ROOT_DIR/assets/fix_emoji_bold.py" "$TMP_HTML"

google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf="$OUT_PDF" \
  --no-pdf-header-footer --print-to-pdf-no-header \
  "file://$TMP_HTML"

rm -f "$TMP_HTML"
echo "Готово: $OUT_PDF"

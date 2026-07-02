#!/usr/bin/env python3
"""Оборачивает эмодзи в span с font-weight:normal.

Chrome headless не рендерит Noto Color Emoji внутри жирного текста
(заголовки h1-h3, **bold**) - эмодзи просто исчезают. Явный сброс
начертания для эмодзи-символов решает проблему.
"""
import re
import sys

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E6-\U0001F1FF"
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U00002190-\U000021FF"
    "\U00002B00-\U00002BFF"
    "\U0000FE0F"
    "\U0000200D"
    "]+"
)

CHECKBOX_CHECKED = re.compile(r'<input[^>]*type="checkbox"[^>]*\bchecked\b[^>]*>')
CHECKBOX_UNCHECKED = re.compile(r'<input[^>]*type="checkbox"[^>]*>')


def fix(html: str) -> str:
    html = EMOJI_PATTERN.sub(
        lambda m: f'<span style="font-weight:normal">{m.group(0)}</span>', html
    )
    html = CHECKBOX_CHECKED.sub("☑ ", html)
    html = CHECKBOX_UNCHECKED.sub("☐ ", html)
    return html


if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        html = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(fix(html))

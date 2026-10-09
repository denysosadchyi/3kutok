#!/usr/bin/env python3
"""Рахує WCAG-контраст пар «текст / фон» з concept/tokens.css.

Запуск: python3 concept/contrast.py — друкує markdown-таблицю.
Нове поєднання кольорів додаємо в PAIRS.
"""
import re
from pathlib import Path

TOKENS = Path(__file__).with_name("tokens.css").read_text(encoding="utf-8")
COLORS = dict(re.findall(r"--(color-[\w-]+):\s*(#[0-9a-fA-F]{6})", TOKENS))

# (текст, фон, що це, поріг: 4.5 — звичайний текст, 3.0 — іконки й великий текст)
PAIRS = [
    ("color-ink", "color-bg", "основний текст на фоні", 4.5),
    ("color-muted", "color-bg", "метадані на фоні", 4.5),
    ("color-ink", "color-surface", "текст у полі, чипі, блоці профілю", 4.5),
    ("color-muted", "color-surface", "підказка в полі (placeholder)", 4.5),
    ("color-on-ink", "color-ink", "текст головної кнопки", 4.5),
    ("color-verified", "color-bg", "текст «Номер підтверджено» на фоні", 4.5),
    ("color-verified", "color-surface", "позначка на поверхні", 4.5),
    ("color-on-ink", "color-verified", "галочка на зеленому колі", 3.0),
    ("color-success", "color-success-bg", "повідомлення про успіх", 4.5),
    ("color-error", "color-bg", "текст помилки під полем", 4.5),
    ("color-error", "color-error-bg", "банер помилки", 4.5),
    ("color-ink", "color-error-bg", "основний текст у банері помилки", 4.5),
    ("color-muted", "color-line", "текст кнопки disabled", 4.5),
    ("color-on-accent", "color-accent", "текст кнопки дії", 4.5),
    ("color-on-accent", "color-accent-hover", "кнопка під курсором", 4.5),
    ("color-link", "color-bg", "посилання й активний пункт меню на фоні", 4.5),
    ("color-link", "color-surface", "посилання на поверхні", 4.5),
    ("color-line", "color-ink", "час у моєму повідомленні чату", 4.5),
]


def luminance(hex_color):
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


if __name__ == "__main__":
    print("| Текст | Фон | Де | Коефіцієнт | Поріг | AA |")
    print("|---|---|---|---:|---:|:---:|")
    for fg, bg, where, need in PAIRS:
        r = ratio(COLORS[fg], COLORS[bg])
        print(f"| `{fg}` {COLORS[fg]} | `{bg}` {COLORS[bg]} | {where} | {r:.2f} | {need} | {'✓' if r >= need else '✗'} |")

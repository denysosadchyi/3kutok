#!/usr/bin/env python3
"""Збирає документацію дизайн-системи «Кутка»: сторінку на компонент,
showcase index.html і why.html.

Запуск: python3 design-system/docs/_build.py — перезаписує всі *.html у docs/.
Зміст сторінок — у _pages_*.py (дані) і _why.py, живі шматки — у _kit.py.
Згенеровані HTML руками не правити.

Сторінки підключають той самий ../index.css, що й екрани продукту: кожен
приклад — справжній компонент системи, не картинка й не копія коду.
Оформлення самої документації — лише docs.css (класи .doc-*), поведінка —
../theme.js (тема), docs.js (шторки, мітки анатомії).
"""

import re
from html import escape
from pathlib import Path

import _pages_shell
import _pages_cards
import _pages_forms
import _why
import _states
import _motion
import _patterns
import _tokens

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
WIREFRAMES = ROOT / "wireframes"

# Порядок груп = порядок сторінок у showcase і в пагінації
GROUPS = [
    ("Оболонка", "Каркас мобільного екрана: що стоїть зверху, що прокручується і що тримається знизу."),
    ("Навігація", "Як людина рухається між екранами й не губиться: шапки, нижнє меню, панель дії, шторка."),
    ("Картки й списки", "Чим екран наповнений: оголошення, людина, факти про побут і житло, фото."),
    ("Форми", "Чим людина діє: кнопки, фільтри-чипи, поля."),
    ("Зворотний зв’язок", "Що бачить людина, коли даних ще немає, вже немає або не вдалося їх отримати."),
    ("Чат", "Прямий контакт — третій крок core loop: контекст оголошення, повідомлення, поле вводу."),
]

PAGES = _pages_shell.PAGES + _pages_cards.PAGES + _pages_forms.PAGES
ORDER = {g: n for n, (g, _) in enumerate(GROUPS)}
PAGES.sort(key=lambda p: ORDER[p["group"]])  # стабільно: всередині групи — порядок модулів
BY_SLUG = {p["slug"]: p for p in PAGES}

ICONIFY = '<script src="https://cdn.jsdelivr.net/npm/iconify-icon@2.1.0/dist/iconify-icon.min.js"></script>'
THEME = ('<button class="chip theme-toggle" type="button" aria-pressed="false">'
         '<iconify-icon icon="solar:moon-linear" aria-hidden="true"></iconify-icon>Темна тема</button>')


def head(title, description):
    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="../index.css">
<link rel="stylesheet" href="docs.css">
{ICONIFY}
<script src="../theme.js"></script>
<script src="docs.js"></script>
<script src="../components/button.js" defer></script>
</head>
<body>
<a class="doc-skip" href="#main">До змісту</a>
"""


def nav(crumbs):
    items = "".join(crumbs)
    return f'<nav class="doc-nav" aria-label="Документація"><p class="doc-crumbs">{items}</p>{THEME}</nav>\n'


def screens_for(page):
    """Екрани wireframes/, де компонент справді стоїть (шукаємо клас у згенерованому HTML)."""
    cls = page.get("detect", page["api"])
    rx = re.compile(r'class="[^"]*(?<![\w-])' + re.escape(cls) + r'(?![\w-])')
    found = sorted(f.stem for f in WIREFRAMES.glob("*.html") if rx.search(f.read_text(encoding="utf-8")))
    return found


def facts(page):
    files = ", ".join(f'<a class="doc-link" href="../components/{f}"><code>components/{f}</code></a>' for f in page["files"])
    scr = screens_for(page)
    if scr:
        screens = ", ".join(f'<a class="doc-link" href="../../wireframes/{s}.html">{s}</a>' for s in scr)
    else:
        screens = "у вайрфреймах поки не стоїть"
    return ('<dl class="doc-facts">'
            f'<div><dt>Файл</dt><dd>{files}</dd></div>'
            f'<div><dt>Класи</dt><dd>{page["classes"]}</dd></div>'
            f'<div><dt>Де стоїть</dt><dd>{screens}</dd></div>'
            '</dl>')


def legend(items):
    out = []
    for n, title, note in items:
        small = f"<small>{note}</small>" if note else ""
        out.append(f'<li data-pin="{n}" tabindex="0"><span class="doc-legend__n" aria-hidden="true">{n}</span>'
                   f'<span class="doc-legend__text"><strong>{title}</strong>{small}</span></li>')
    return '<ol class="doc-legend" aria-label="Частини компонента">' + "".join(out) + "</ol>"


def variants(items):
    out = []
    for v in items:
        caption, html = v[0], v[1]
        mod = v[2] if len(v) > 2 and v[2] else ""
        m = "".join(f" doc-spec--{x}" for x in mod.split())
        out.append(f'<figure class="doc-spec{m}">{html}<figcaption>{caption}</figcaption></figure>')
    return '<div class="doc-variants">' + "".join(out) + "</div>"


def link_to(slug):
    p = BY_SLUG[slug]
    return f'<a class="doc-link" href="{slug}.html">{p["name"]}</a>'


def rules(page):
    do_title, do_html, do_cap = page["do"]
    dont_title, dont_html, dont_cap, instead_slug, instead_text = page["dont"]
    yes = ('<figure class="doc-rule">'
           f'<p class="doc-rule__verdict"><iconify-icon icon="solar:check-circle-linear" aria-hidden="true"></iconify-icon>Так: {do_title}</p>'
           f'{do_html}<figcaption>{do_cap}</figcaption></figure>')
    no = ('<figure class="doc-rule doc-rule--dont">'
          f'<p class="doc-rule__verdict"><iconify-icon icon="solar:close-circle-linear" aria-hidden="true"></iconify-icon>Ні: {dont_title}</p>'
          f'{dont_html}<figcaption>{dont_cap}'
          f'<p class="doc-instead">Натомість — {link_to(instead_slug)}: {instead_text}</p></figcaption></figure>')
    return f'<div class="doc-rules">{yes}{no}</div>'


def part(pid, title, lead, body):
    l = f'<p class="doc-lead">{lead}</p>' if lead else ""
    return f'<section class="doc-part" id="{pid}" aria-labelledby="{pid}-h"><h2 id="{pid}-h">{title}</h2>{l}{body}</section>\n'


def component_page(page, prev, nxt):
    a = page["anatomy"]
    w = page.get("widths")  # (вступ, html) — лише в компонентів з адаптивом (урок 10)
    mv = _motion.block(page["slug"], variants)  # «Рух» — лише в компонентів, що рухаються
    anatomy = f'<div class="doc-anatomy"><div class="doc-anatomy__live">{a["live"]}</div>{legend(a["legend"])}</div>'
    usage = f'<div class="doc-prose">{page["usage"]}<p class="doc-sources">Джерела: {page["sources"]}</p></div>'
    pager = '<nav class="doc-pager" aria-label="Сусідні компоненти">'
    pager += f'<a class="button button--secondary" href="{prev["slug"]}.html">← {prev["name"]}</a>' if prev else '<a class="button button--secondary" href="index.html">← Усі компоненти</a>'
    pager += f'<a class="button button--secondary" href="{nxt["slug"]}.html">{nxt["name"]} →</a>' if nxt else '<a class="button button--secondary" href="why.html">Чому система така →</a>'
    pager += "</nav>"
    return (head(f'{page["name"]} — дизайн-система «Кутка»', page["role_plain"] if "role_plain" in page else re.sub("<[^>]+>", "", page["role"]))
            + '<div class="doc">'
            + nav(['<a class="doc-link" href="index.html">Дизайн-система «Кутка»</a>', f'<span>{page["group"]}</span>'])
            + '<main id="main">'
            + f'<header class="doc-hero"><p class="doc-eyebrow">{page["group"]} · <code>.{page["api"]}</code></p>'
            + f'<h1>{page["name"]}</h1><p class="doc-lead">{page["role"]}</p>{facts(page)}</header>'
            + '<nav class="doc-toc" aria-label="Частини сторінки">'
            + '<a class="chip" href="#anatomy">Анатомія</a><a class="chip" href="#variants">Варіанти</a>'
            + ('<a class="chip" href="#widths">Три ширини</a>' if w else "")
            + '<a class="chip" href="#usage">Коли вживати</a><a class="chip" href="#rules">Правило й антиправило</a><a class="chip" href="#states">Стани</a>'
            + ('<a class="chip" href="#motion">Рух</a>' if mv else "") + '</nav>'
            + part("anatomy", "1. Анатомія", a.get("lead", "Живий компонент із системи. Наведи на рядок легенди — частина обведеться пунктиром."), anatomy)
            + part("variants", "2. Варіанти й розміри", page.get("variants_lead", "Усі варіанти з <code>ui/inventory.md</code>, поруч."), variants(page["variants"]))
            + (part("widths", "3. Три ширини", w[0], w[1]) if w else "")
            + part("usage", f"{3 + bool(w)}. Коли вживати", "", usage)
            + part("rules", f"{4 + bool(w)}. Правило і антиправило", "", rules(page))
            + part("states", f"{5 + bool(w)}. Стани", "", _states.block(page["slug"], variants))
            + (part("motion", f"{6 + bool(w)}. Рух", "", mv) if mv else "")
            + pager
            + "</main></div>\n</body>\n</html>\n")


def index_page():
    groups = []
    for g, intro in GROUPS:
        cards = []
        for p in [p for p in PAGES if p["group"] == g]:
            mod = "".join(f" doc-card__preview--{x}" for x in p.get("preview_mod", "").split())
            cards.append(f'<li class="doc-card"><div class="doc-card__preview{mod}" aria-hidden="true" inert>{p["preview"]}</div>'
                         f'<div class="doc-card__body"><h3 class="doc-card__name"><a href="{p["slug"]}.html">{p["name"]}</a></h3>'
                         f'<p class="doc-card__role">{p["card_role"]}</p><p class="doc-card__api"><code>.{p["api"]}</code></p></div></li>')
        gid = "g-" + str(ORDER[g])
        groups.append(f'<section class="doc-group" aria-labelledby="{gid}"><h2 id="{gid}">{g}</h2><p>{intro}</p>'
                      f'<ul class="doc-cards">{"".join(cards)}</ul></section>')
    n = len(PAGES)
    return (head("Дизайн-система «Кутка» — компоненти", "Showcase живих компонентів дизайн-системи «Кутка»: анатомія, варіанти, коли вживати, правило й антиправило.")
            + '<div class="doc">'
            + nav(['<span>Дизайн-система «Кутка»</span>'])
            + '<main id="main">'
            + '<header class="doc-hero"><p class="doc-eyebrow">Документація · design-system/</p>'
            + f'<h1>Компоненти «Кутка»</h1><p class="doc-lead">{n} компонентів, з яких зібрано всі екрани: пошук, оголошення, профіль, чат. '
            + 'Кожна картка й кожна сторінка малює компонент тим самим <code>design-system/index.css</code>, що й продукт, — '
            + 'якщо компонент зміниться, showcase зміниться разом із ним.</p></header>'
            + '<div class="doc-start"><strong>Новий у проєкті? Почни з «чому».</strong>'
            + '<p>Звідки взялися біла стіна з холодною сірою поверхнею, один кораловий колір, вага замість розміру й бирка з ціною — коротко, з посиланнями на джерела.</p>'
            + '<p><a class="button button--primary" href="why.html">Чому система така</a></p></div>'
            + '<section class="doc-group" aria-labelledby="how"><h2 id="how">Як читати сторінку компонента</h2>'
            + '<p>Сторінка має п’ять частин, завжди в одному порядку. <strong>Анатомія</strong> — живий компонент з пронумерованими частинами. '
            + '<strong>Варіанти й розміри</strong> — усе з <code>ui/inventory.md</code> поруч. <strong>Коли вживати</strong> — роль у продукті '
            + 'за <code>DESIGN.md</code> і <code>microcopy.md</code>. <strong>Правило й антиправило</strong> — доречне вживання і випадок, '
            + 'коли треба взяти інший компонент. <strong>Стани</strong> — наведення, натискання, фокус і вимкнене в обох темах.</p></section>'
            + "".join(groups)
            + '<section class="doc-group" aria-labelledby="more"><h2 id="more">Поруч</h2><div class="doc-prose"><ul>'
            + '<li><a class="doc-link" href="tokens.html">Токени</a> — усі значення з <code>tokens.css</code>: primitive, semantic-ролі кольору в обох темах, контраст пар.</li>'
            + '<li><a class="doc-link" href="patterns.html">Патерни</a> — композиції компонентів, що вже стоять на трьох і більше екранах, і коли їх брати.</li>'
            + '<li><a class="doc-link" href="../../ui/kit.html">Вітрина кіта</a> — усі компоненти на одній сторінці, як вони стоять на екрані.</li>'
            + '<li><a class="doc-link" href="../../DESIGN.md"><code>DESIGN.md</code></a> — правила й причини; <a class="doc-link" href="../../microcopy.md"><code>microcopy.md</code></a> — текст.</li>'
            + '<li><a class="doc-link" href="../../wireframes/listings.html">Екрани</a> — 16 вайрфреймів, зібраних із цього кіта.</li>'
            + '</ul></div></section>'
            + "</main></div>\n</body>\n</html>\n")


def why_page():
    return (head("Чому система така — дизайн-система «Кутка»", _why.DESCRIPTION)
            + '<div class="doc">'
            + nav(['<a class="doc-link" href="index.html">Дизайн-система «Кутка»</a>', '<span>Чому система така</span>'])
            + '<main id="main">' + _why.body(link_to)
            + '<nav class="doc-pager" aria-label="Далі"><a class="button button--secondary" href="index.html">← Усі компоненти</a>'
            + f'<a class="button button--secondary" href="{PAGES[0]["slug"]}.html">{PAGES[0]["name"]} →</a></nav>'
            + "</main></div>\n</body>\n</html>\n")


def patterns_page():
    return (head("Патерни — дизайн-система «Кутка»", _patterns.DESCRIPTION)
            + '<div class="doc">'
            + nav(['<a class="doc-link" href="index.html">Дизайн-система «Кутка»</a>', '<span>Патерни</span>'])
            + '<main id="main">' + _patterns.body(link_to)
            + '<nav class="doc-pager" aria-label="Далі"><a class="button button--secondary" href="index.html">← Усі компоненти</a>'
            + '<a class="button button--secondary" href="why.html">Чому система така →</a></nav>'
            + "</main></div>\n</body>\n</html>\n")


def tokens_page():
    return (head("Токени — дизайн-система «Кутка»", _tokens.DESCRIPTION)
            + '<div class="doc">'
            + nav(['<a class="doc-link" href="index.html">Дизайн-система «Кутка»</a>', '<span>Токени</span>'])
            + '<main id="main">' + _tokens.body()
            + '<nav class="doc-pager" aria-label="Далі"><a class="button button--secondary" href="index.html">← Усі компоненти</a>'
            + '<a class="button button--secondary" href="patterns.html">Патерни →</a></nav>'
            + "</main></div>\n</body>\n</html>\n")


def main():
    for old in OUT.glob("*.html"):
        old.unlink()
    for i, p in enumerate(PAGES):
        prev = PAGES[i - 1] if i else None
        nxt = PAGES[i + 1] if i + 1 < len(PAGES) else None
        (OUT / f'{p["slug"]}.html').write_text(component_page(p, prev, nxt), encoding="utf-8")
    (OUT / "index.html").write_text(index_page(), encoding="utf-8")
    (OUT / "why.html").write_text(why_page(), encoding="utf-8")
    (OUT / "patterns.html").write_text(patterns_page(), encoding="utf-8")
    (OUT / "tokens.html").write_text(tokens_page(), encoding="utf-8")
    print(f"docs: {len(PAGES)} компонентів + index.html + why.html + patterns.html + tokens.html")


if __name__ == "__main__":
    main()

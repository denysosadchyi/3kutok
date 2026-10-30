"""Зміст сторінки patterns.html — патерни дизайн-системи «Кутка».

Патерн — композиція наявних компонентів, що вже стоїть на трьох і більше
екранах wireframes/. Живий приклад — сам файл ../patterns/<slug>.html
(одне джерело: сторінка не копіює розмітку, а вставляє фрагмент). Екрани,
де патерн стоїть, шукаємо в згенерованих wireframes/*.html за класами
(need — усі мають бути, skip — жодного); менше трьох — збірка падає.

Виклик: _build.py → patterns_page() → body(link_to).
"""

import re
from pathlib import Path

from _kit import screen

DOCS = Path(__file__).resolve().parent
PATTERNS = DOCS.parent / "patterns"
WIREFRAMES = DOCS.parent.parent / "wireframes"

DESCRIPTION = ("Патерни «Кутка»: композиції наявних компонентів, що вже стоять на трьох і більше екранах, — "
               "живий приклад, екрани, складники і коли брати патерн, а коли окремі компоненти.")

# Клас компонента → сторінка документації, де він описаний
SLUG = {"chip-row": "chip", "card-list": "listing-card"}

ITEMS = [
    dict(
        slug="search-panel", name="Панель пошуку",
        need=["header", "chip-row", "results-meta"], skip=[],
        parts=["shell", "header", "chip-row", "chip", "sheet", "field", "button", "results-meta"],
        lead="Велика шапка «Результати пошуку» → ряд чипів, перший відкриває шторку фільтрів → підсумок. "
             "Під панеллю — що знайшлося: стрічка карток, стан або скелетони.",
        take=["екран показує результат пошуку за умовами людини;",
              "умови мають лишатися видимими й змінними за будь-якого результату — і коли карток 12, і коли 0, і коли пошук упав;",
              "підсумок міняється зі станом: «12 оголошень», «0 оголошень», «Фільтри збережено», «Завантажуємо оголошення»."],
        split=["потрібна лише шапка без фільтрів — бери <code>header</code>;",
               "чипи стоять не над результатами — <code>chip-row</code> і <code>sheet</code> окремо;",
               "сортування «Спершу нові» і кнопка теми — разові блоки <code>wireframes/screens.css</code>, у патерн не входять."],
    ),
    dict(
        slug="card-feed", name="Стрічка карток",
        need=["card-list", "listing-card"], skip=[],
        parts=["card-list", "listing-card", "price-tag", "skeleton"],
        lead="Список карток оголошень: фото з биркою ціни, назва-посилання, рядок фактів. "
             "Та сама картка і в пошуку, і в профілі автора; у завантаженні — скелетони в тій самій картці.",
        take=["показуєш одне чи кілька оголошень, і з кожного треба перейти в оголошення;",
              "оголошення людини в профілі — це теж стрічка, навіть з однієї картки: людина впізнає ту саму картку, що бачила в пошуку;",
              "дані ще вантажаться — скелетони стоять у <code>listing-card</code>, тож висота не стрибає."],
        split=["оголошення вже відкрите — <code>hero-photo</code> і <code>listing-title</code>;",
               "оголошення лише нагадує, про що розмова, — <code>chat-context</code>;",
               "підпис автора на фото в пошуку (<code>.card-author</code>) — разовий блок екрана, не частина патерна."],
    ),
    dict(
        slug="section-group", name="Розділ зі списком",
        need=["section-title", "group"], skip=[],
        parts=["section-title", "group", "verified-note", "person-row", "avatar"],
        lead="Заголовок розділу → згрупований список на сірій поверхні. Найчастіший зміст — «Що підтверджено» "
             "з рядком перевірки: він однаковий на всіх трьох екранах.",
        take=["на сторінці деталей кілька однорідних фактів або одна сутність — людина, перевірка, — і їм потрібна назва;",
              "факти «підпис — значення» — <code>dl.group</code>; рядки-елементи (людина, перевірка) — <code>ul.group</code>;",
              "«Що підтверджено» бери саме так, з обмеженням «Це означає лише…»: номер — не особа й не житло."],
        split=["факти йдуть одразу під назвою оголошення — <code>group</code> без заголовка, як «Співмешканці / Квартира / Комунальні»;",
               "у розділі немає даних — заголовок і текстовий блок про це (<code>.state-note</code> у profile-empty), не порожній <code>group</code>."],
    ),
    dict(
        slug="contact-frame", name="Деталі з контактом",
        need=["topbar__back", "topbar__action", "actionbar", "button--primary"], skip=[],
        parts=["shell", "topbar", "actionbar", "button", "skeleton"],
        lead="Компактна шапка «назад + ⋯» → вміст про кімнату чи людину → закріплена панель з однією кораловою дією "
             "«Написати Ірині». Скелетон тієї самої рамки — у listing-loading і profile-loading.",
        take=["екран показує одну пропозицію чи одну людину, і наступний крок core loop — написати їй;",
              "у ⋯ — «Заблокувати чи поскаржитися»: на кожному екрані, звідки можна почати контакт;",
              "в оголошенні шапка стоїть поверх фото: <code>topbar--over-photo</code> і <code>shell--photo-top</code>."],
        split=["дії на екрані немає або їх кілька — не <code>actionbar</code>: одна панель — одна дія;",
               "екран — стрічка: <code>header</code> і <code>tabbar</code>;",
               "розмова вже почалася — «Рамка чату»."],
    ),
    dict(
        slug="chat-frame", name="Рамка чату",
        need=["topbar--person", "chat-context", "composer"], skip=[],
        parts=["shell", "topbar", "avatar", "chat-context", "composer", "bubble", "state", "skeleton"],
        lead="Шапка з людиною → першим рядком оголошення, про яке розмова → повідомлення або стан → поле повідомлення. "
             "Між станами міняється лише середина.",
        take=["будь-який стан розмови з однією людиною про одне оголошення — історія, нова розмова, помилка, завантаження;",
              "поле не зникає навіть у помилці: чернетку збережено, а «Надіслати» неактивна, поки розмова не завантажилась;",
              "щит біля імені й «номер підтверджено» в контексті — той самий сигнал довіри, що й у «Що підтверджено»."],
        split=["потрібне лише поле вводу поза чатом — <code>composer</code>;",
               "оголошення показуєш поза розмовою — «Стрічка карток»;",
               "дата над повідомленнями й список <code>.messages</code> — разові блоки <code>wireframes/screens.css</code>."],
    ),
    dict(
        slug="screen-state", name="Стан замість екрана",
        need=["topbar__back", "state__actions"], skip=["tabbar", "actionbar", "composer"],
        parts=["shell", "topbar", "state", "button"],
        lead="Шапка лише з «назад» → стан на весь вільний екран → основна дія і вихід. Нижнього поясу немає: "
             "написати людині, коли сторінки немає, не можна.",
        take=["не вдалося показати саму сторінку — оголошення зняли, профіль чи оголошення не завантажилися;",
              "людині лишаються повтор і дорога назад; заголовок стану — <code>h1</code> сторінки;",
              "помилка — <code>state--error</code> з <code>role=\"alert\"</code>, зняте оголошення — звичайний <code>state</code>."],
        split=["дані зникли лише в частині екрана, а рамка працює, — став <code>state</code> усередину наявної рамки:",
               "у «Панель пошуку» (listings-empty, listings-error) — фільтри лишаються, їх і змінюють;",
               "у «Рамку чату» (chat-empty, chat-error) — поле й чернетка лишаються."],
    ),
]

NOT_PATTERNS = [
    ("Фото, галерея й назва оголошення", "<code>hero-photo</code> + <code>gallery</code> + <code>listing-title</code>",
     "listing, listing-loading — це один екран у двох станах, а не три екрани."),
    ("Шторка сортування", "<code>sheet</code> + <code>.sort-options</code>", "лише listings."),
    ("Голова профілю", "<code>profile-head</code>", "стоїть на трьох екранах профілю, але це один компонент, а не композиція."),
]


def _rx(cls):
    return re.compile(r'class="[^"]*(?<![\w-])' + re.escape(cls) + r'(?![\w-])')


def screens(item):
    found = []
    for f in sorted(WIREFRAMES.glob("*.html"), key=lambda p: p.stem):
        html = f.read_text(encoding="utf-8")
        if all(_rx(c).search(html) for c in item["need"]) and not any(_rx(c).search(html) for c in item["skip"]):
            found.append(f.stem)
    if len(found) < 3:
        raise SystemExit(f'patterns: «{item["name"]}» стоїть лише на {found} — патерн потребує трьох екранів')
    return found


def live(slug):
    """Фрагмент ../patterns/<slug>.html без коментарів; заголовки — h4, щоб не ламати структуру сторінки."""
    html = (PATTERNS / f"{slug}.html").read_text(encoding="utf-8")
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    html = re.sub(r"<(/?)h[123](?=[\s>])", r"<\1h4", html)
    html = "\n".join(line for line in html.splitlines() if line.strip())
    if not html.lstrip().startswith('<div class="shell'):
        html = f'<div class="shell"><div class="shell__main">{html}</div></div>'
    return screen(html, "tall")


def _ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def _part(item, link_to):
    s = item["slug"]
    scr = screens(item)
    where = ", ".join(f'<a class="doc-link" href="../../wireframes/{x}.html">{x}</a>' for x in scr)
    parts = ", ".join(link_to(SLUG.get(c, c)) for c in item["parts"])
    facts = ('<dl class="doc-facts">'
             f'<div><dt>Файл</dt><dd><a class="doc-link" href="../patterns/{s}.html"><code>patterns/{s}.html</code></a></dd></div>'
             f'<div><dt>Складники</dt><dd>{parts}</dd></div>'
             f'<div><dt>Де стоїть</dt><dd>{where}</dd></div></dl>')
    yes = ('<figure class="doc-rule"><p class="doc-rule__verdict">'
           '<iconify-icon icon="solar:check-circle-linear" aria-hidden="true"></iconify-icon>Бери патерн, коли</p>'
           f'<figcaption class="doc-prose">{_ul(item["take"])}</figcaption></figure>')
    no = ('<figure class="doc-rule"><p class="doc-rule__verdict">'
          '<iconify-icon icon="solar:widget-linear" aria-hidden="true"></iconify-icon>Бери окремі компоненти, коли</p>'
          f'<figcaption class="doc-prose">{_ul(item["split"])}</figcaption></figure>')
    return (f'<section class="doc-part" id="{s}" aria-labelledby="{s}-h"><h2 id="{s}-h">{item["name"]}</h2>'
            f'<p class="doc-lead">{item["lead"]}</p>'
            f'<div class="doc-anatomy"><div class="doc-anatomy__live">{live(s)}</div>'
            f'<div class="doc-anatomy__live">{facts}{yes}{no}</div></div></section>\n')


def body(link_to):
    toc = "".join(f'<a class="chip" href="#{i["slug"]}">{i["name"]}</a>' for i in ITEMS)
    hero = ('<header class="doc-hero"><p class="doc-eyebrow">Документація · <code>design-system/patterns/</code></p>'
            f'<h1>Патерни «Кутка»</h1><p class="doc-lead">{len(ITEMS)} композицій, що вже стоять на трьох і більше екранах. '
            'Патерн не має власних стилів: це наявні компоненти в перевіреному порядку. Живий приклад нижче — сам файл '
            'патерна, підключений до того самого <code>design-system/index.css</code>; екрани в «Де стоїть» сторінка '
            'знаходить у <code>wireframes/</code> за класами.</p></header>')
    how = ('<section class="doc-part" id="choose" aria-labelledby="choose-h"><h2 id="choose-h">Патерн чи окремі компоненти</h2>'
           '<div class="doc-prose">'
           '<p><strong>Бери патерн</strong>, коли екран робить ту саму роботу, що й екрани з «Де стоїть»: показує результат пошуку, '
           'одну пропозицію перед контактом, розмову або сторінку, якої не вдалося показати. Тоді порядок частин уже перевірено, '
           'і людина впізнає екран з першого погляду.</p>'
           '<p><strong>Бери окремі компоненти</strong>, коли робота інша, навіть якщо частини схожі. Не обрізай патерн до половини '
           'й не дописуй до нього нові класи: якщо частина не потрібна — це вже не той патерн, збирай з компонентів.</p>'
           '<p><strong>Новий патерн</strong> з’являється, коли та сама композиція стоїть на трьох екранах. Двох замало: '
           'це ще збіг, а не правило.</p></div></section>\n')
    rows = "".join(f"<li><strong>{n}</strong> — {what}: {why}</li>" for n, what, why in NOT_PATTERNS)
    nope = ('<section class="doc-part" id="not" aria-labelledby="not-h"><h2 id="not-h">Що не стало патерном</h2>'
            f'<div class="doc-prose"><p>Повторюється, але менше ніж на трьох екранах, або це один компонент.</p><ul>{rows}</ul></div></section>\n')
    return (hero + f'<nav class="doc-toc" aria-label="Патерни">{toc}</nav>' + how
            + "".join(_part(i, link_to) for i in ITEMS) + nope)

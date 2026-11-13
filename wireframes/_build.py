#!/usr/bin/env python3
"""Збирає HTML-вайрфрейми «Кутка» зі спільної мобільної оболонки.

Запуск: python3 wireframes/_build.py — перезаписує всі *.html у wireframes/.
Зміст екранів редагуємо тут, а не в згенерованих файлах.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent

# Темна тема — частина продукту з 2026-10-23
# (tokens.css, блок [data-theme="dark"]). Скрипт стоїть у <head>: ставить
# data-theme на <html> до першого рендера (без блимання), пам'ятає вибір у
# localStorage і синхронізує кнопки .theme-toggle (aria-pressed, іконка).
# Той самий текст скрипта — у ui/kit.html і ui/shell.html.
THEME_SCRIPT = """<script>
/* Темна тема (tokens.css, [data-theme="dark"]) — частина продукту з 2026-10-23 */
(function () {
  var KEY = "kutok-theme", root = document.documentElement;
  function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function apply(dark) {
    if (dark) root.setAttribute("data-theme", "dark"); else root.removeAttribute("data-theme");
    document.querySelectorAll(".theme-toggle").forEach(function (b) {
      b.setAttribute("aria-pressed", dark ? "true" : "false");
      var i = b.querySelector("iconify-icon");
      if (i) i.setAttribute("icon", dark ? "solar:sun-2-linear" : "solar:moon-linear");
    });
  }
  apply(saved() === "dark");
  document.addEventListener("DOMContentLoaded", function () { apply(saved() === "dark"); });
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".theme-toggle");
    if (!b) return;
    var dark = root.getAttribute("data-theme") !== "dark";
    apply(dark);
    try { localStorage.setItem(KEY, dark ? "dark" : "light"); } catch (err) {}
  });
  window.addEventListener("storage", function (e) { if (e.key === KEY) apply(e.newValue === "dark"); });
})();
</script>"""
# Кнопка теми — наявний клас кіта .topbar__action (поверх фото — кругла на
# затемненні, як ⋯), без нового компонента. Поруч з іншою дією — у кластері
# .topbar__end (components/topbar.css, B10).
THEME = '<button class="topbar__action theme-toggle" type="button" aria-pressed="false" aria-label="Темна тема"><iconify-icon icon="solar:moon-linear" aria-hidden="true"></iconify-icon></button>'


def end_slot(action=""):
    """Права комірка app bar: кнопка теми, а за нею — наявна дія (⋯), якщо є."""
    return f'<span class="topbar__end">{THEME}{action}</span>' if action else THEME


# Усі екрани зібрані з кіта компонентів (урок 7). Система підключається одним
# пакетом — ../design-system/index.css (tokens.css — primitive + semantic,
# components/index.css — компоненти, урок 9); screens.css — разові блоки. Іконки — iconify (Streamline Freehand
# і Solar linear). split.js — синхронно: слухає pagereveal до першого кадру
# (перешикування карток спліта лише через transform, split.css).
HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="../design-system/index.css">
<link rel="stylesheet" href="screens.css">
<script src="https://cdn.jsdelivr.net/npm/iconify-icon@2.1.0/dist/iconify-icon.min.js"></script>
<script src="../design-system/components/button.js" defer></script>
<script src="../design-system/components/split.js"></script>""" + "\n" + THEME_SCRIPT
# Класи вайрфреймів → модифікатори оболонки кіта. status-dark — лише позначка
# для хабу уроків (темний статус-бар над світлим скелетоном), стилів не має.
SHELL = {"has-tabbar": "shell--tabbar", "has-actionbar": "shell--actionbar", "has-composer": "shell--composer", "photo-top": "shell--photo-top", "status-dark": "status-dark", "has-split": "shell--split"}
# Тап за межами шторки (по затемненню) або Escape закриває її. Відкрита
# шторка модальна: решта сторінки inert, фокус — у панель; після закриття
# фокус вертається на тригер (урок 9, аудит). «Надіслати» вмикається, коли
# в полі є текст (форма з data-wait чекає на розмову і не вмикається).
SHEET_SCRIPT = """
<script>
document.addEventListener("toggle", function (e) {
  var d = e.target;
  if (!d.matches || !d.matches("details.sheet")) return;
  for (var n = d; n.parentElement && n !== document.body; n = n.parentElement) {
    Array.prototype.forEach.call(n.parentElement.children, function (el) {
      if (el !== n && el.tagName !== "SCRIPT") el.inert = d.open;
    });
  }
  if (d.open) {
    var first = d.querySelector(".sheet__panel a, .sheet__panel button, .sheet__panel input, .sheet__panel select");
    if (first) first.focus();
  } else {
    d.querySelector("summary").focus();
  }
}, true);
document.addEventListener("input", function (e) {
  var form = e.target.closest(".composer");
  if (!form || form.hasAttribute("data-wait")) return;
  form.querySelector(".composer__send").disabled = !e.target.value.trim();
});
document.addEventListener("click", function (e) {
  var sheet = e.target.closest("details.sheet[open]");
  if (sheet && !e.target.closest(".sheet__panel, summary")) sheet.open = false;
});
document.addEventListener("keydown", function (e) {
  if (e.key !== "Escape") return;
  document.querySelectorAll("details.sheet[open]").forEach(function (d) { d.open = false; });
});
</script>"""
TAB_ICONS = {"search": "search-magnifier", "chats": "messages-bubble-smile", "profile": "smiley-happy"}


def icon(name):
    """Велика іконка, мальована від руки: нижнє меню, стани."""
    return f'<iconify-icon icon="streamline-freehand:{name}" aria-hidden="true"></iconify-icon>'


def lin(name):
    """Маленька іконка — проста лінійна (Solar linear): чипи, позначки, рядки."""
    return f'<iconify-icon icon="solar:{name}-linear" aria-hidden="true"></iconify-icon>'


# Стрілки й ⋯ — теж Solar linear (урок 7, аудит: ручні SVG прибрано).
CHEVRON_LEFT = lin("alt-arrow-left")
CHEVRON_RIGHT = '<iconify-icon class="chevron" icon="solar:alt-arrow-right-linear" aria-hidden="true"></iconify-icon>'
MORE = lin("menu-dots")
# Позначка перевірки на аватарі — однаково на всіх екранах, з текстом для читачів екрана.
MARK = f'<span class="avatar__mark">{lin("check")}<span class="sr-only">Номер підтверджено</span></span>'
# ⋯ у шапці: заблокувати чи поскаржитися (C-19) — у профілі, оголошенні й чаті.
REPORT = f'<button class="topbar__action" type="button" aria-label="Заблокувати чи поскаржитися">{MORE}</button>'


# Фото — власний набір visuals/ (один колорит, промпт — visuals/README.md).
def visual(name):
    return f"../visuals/{name}.jpg"


IRYNA = visual("person-iryna")


def page(name, *, title, job, body, body_class="has-tabbar", tab="search"):
    shell = " ".join(["shell"] + [SHELL[c] for c in body_class.split()])
    tabs = [("search", "Пошук", "listings.html"), ("chats", "Чати", "chats.html"), ("profile", "Профіль", None)]
    items = []
    for key, label, href in tabs:
        current = ' aria-current="page"' if key == tab else ""
        inner = f'{icon(TAB_ICONS[key])}<span>{label}</span>'
        if href:
            items.append(f'<li><a class="tabbar__item" href="{href}"{current}>{inner}</a></li>')
        else:
            # Розділу ще немає: посилання без href (поза Tab) + aria-disabled — глушиться base.css
            items.append(f'<li><a class="tabbar__item" aria-disabled="true"{current}>{inner}</a></li>')
    tabbar = (
        '\n<nav class="tabbar" aria-label="Головна навігація"><ul class="tabbar__list">' + "".join(items) + "</ul></nav>"
        if "has-tabbar" in body_class
        else ""
    )
    html = f"""<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="wireframe-job" content="{job}">
<title>{title}</title>
{HEAD.strip()}
</head>
<body class="{shell}">
{body.strip()}{tabbar}{SHEET_SCRIPT}
</body>
</html>
"""
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")


def appbar(title, back_href=None, back_label="Назад", action="", over_photo=False, heading=True):
    back = (
        f'<a class="topbar__back" href="{back_href}" aria-label="Назад до {back_label}">{CHEVRON_LEFT}</a>'
        if back_href
        else "<span></span>"
    )
    tag = "h1" if heading else "p"
    head = f'<{tag} class="topbar__title">{title}</{tag}>' if title else "<span></span>"
    mod = " topbar--over-photo" if over_photo else ""
    return f'<header class="topbar{mod}">{back}{head}{end_slot(action)}</header>'


# ---------- Результати пошуку ----------

JOB_SEARCH = "Related 1 — звузити пошук до прийнятних варіантів"


def filters(district, budget, date, date_label):
    options = "".join(
        f'<option{" selected" if d == district else ""}>{d}</option>'
        for d in ["Усі райони", "Шевченківський", "Подільський", "Голосіївський", "Дніпровський"]
    )
    budget_label = f"{int(budget):,}".replace(",", " ")
    return f"""
<div class="chip-row"><div class="chip-row__track" tabindex="0" role="group" aria-label="Активні фільтри">
  <details class="sheet">
    <summary class="chip chip--selected">{lin("tuning-2")}Фільтри · 3</summary>
    <section class="sheet__panel" role="dialog" aria-modal="true" aria-labelledby="filters-title">
      <div class="sheet__grabber" aria-hidden="true"></div>
      <div class="sheet__head"><h2 class="sheet__title" id="filters-title">Фільтри</h2><a class="button button--text" href="listings.html">Скасувати</a></div>
      <form class="sheet__body" action="listings.html" method="get">
        <fieldset>
          <legend class="sr-only">Базові умови кімнати</legend>
          <div class="field"><label class="field__label" for="district">Район Києва</label><select class="input" id="district" name="district">{options}</select></div>
          <div class="field"><label class="field__label" for="budget">Бюджет до, грн/місяць</label><input class="input" id="budget" name="budget" type="number" inputmode="numeric" min="1000" step="500" value="{budget}"></div>
          <div class="field"><label class="field__label" for="move-in">Дата заїзду</label><input class="input" id="move-in" name="move-in" type="text" inputmode="none" readonly value="з {date_label} 2026"></div>
        </fieldset>
      </form>
      <div class="sheet__foot"><a class="button button--primary button--block" href="listings.html">Застосувати фільтри</a></div>
    </section>
  </details>
  <span class="chip">{district}</span>
  <span class="chip">до {budget_label} грн</span>
  <span class="chip">з {date_label}</span>
</div></div>"""


def search_head(sub, heading=True):
    tag = "h1" if heading else "p"
    return f'<header class="header"><div class="header__top">{THEME}<{tag} class="header__title">Результати пошуку</{tag}><p class="header__subtitle">{sub}</p></div></header>'


# Split-view (design-system/components/split.css, урок 10): перелік + деталь.
# Телефон — одна панель за раз (--detail відкриває деталь), на ширині — поруч:
# чат від --bp-tablet (--tablet), стрічка → оголошення від --bp-desktop.
# <main> — у поточній панелі, друга панель — div.shell__main.
def split(list_html, detail_html=None, mods=""):
    """detail_html=None — деталі немає (нічого не вибрано): перелік на всю ширину (--solo)."""
    if detail_html is None:
        mods = (mods + " split--solo").strip()
    m = f" {mods}" if mods else ""
    detail = f'<section class="split__pane split__pane--detail">{detail_html}\n</section>\n' if detail_html is not None else ""
    return (f'<div class="split{m}">\n<section class="split__pane split__pane--list" aria-label="Перелік">{list_html}\n</section>\n'
            f'{detail}</div>')


def nothing(what, name, text):
    """Права панель на ширині, коли нічого не вибрано (на телефоні її не видно)."""
    return f"""
<div class="shell__main">
<section class="state">
  <div class="state__icon">{icon(name)}</div>
  <h2 class="state__title">Обери {what} ліворуч</h2>
  <p class="state__text">{text}</p>
</section>
</div>"""



def card(title, price, meta, photo, href="listing.html", author=None):
    # Keep "з 1 жовтня" and "2 співмешканці" from breaking across lines.
    meta = " · ".join(part.replace(" ", "\u00a0") for part in meta.split(" · "))
    src, alt = photo
    who = ""
    if author:
        name, face = author
        who = (
            f'\n      <p class="card-author"><span class="avatar"><img src="{face}" alt="">'
            f'{MARK}</span>{name}</p>'
        )
    # Ціна — на бирці від ключа поверх фото (concept.html, «Бирка з ключем»).
    return f"""
  <li class="listing-card">
    <div class="listing-card__photo">
      <img src="{src}" alt="{alt}" loading="lazy">
      <p class="price-tag">{price}</p>{who}
    </div>
    <div class="listing-card__body">
      <h2 class="listing-card__title"><a class="listing-card__link" href="{href}">{title}</a></h2>
      <p class="listing-card__meta">{meta}</p>
    </div>
  </li>"""


# Фото за темою: кімната — інтер'єр, автор — портрет (visuals/README.md).
ROOM_PHOTOS = [
    (visual("room-lukianivska-bedroom"), "Світла спальня з ліжком, тумбою і настінною лампою"),
    (visual("room-tatarka-sofa"), "Світла кімната з диваном, комодом, торшером і рослиною"),
    (visual("room-kpi-armchair"), "Кімната з ліжком, теракотовим кріслом, торшером і робочим столом"),
]
AUTHORS = [
    ("Ірина", IRYNA),
    ("Марина", visual("person-maryna")),
    ("Оля", visual("person-olia")),
]


# Сортування — така сама шторка, як фільтри (тап по «Спершу нові»).
SORT_OPTIONS = ["Спершу нові", "Спершу дешевші", "Спершу дорожчі"]
SORT_SHEET = f"""<details class="sheet">
  <summary class="sort">Спершу нові{lin("alt-arrow-down")}</summary>
  <section class="sheet__panel" role="dialog" aria-modal="true" aria-labelledby="sort-title">
    <div class="sheet__grabber" aria-hidden="true"></div>
    <div class="sheet__head"><h2 class="sheet__title" id="sort-title">Сортування</h2><a class="button button--text" href="listings.html">Скасувати</a></div>
    <ul class="sort-options">{"".join(f'<li><a href="listings.html"{' aria-current="true"' if i == 0 else ''}>{o}{lin("check") if i == 0 else ""}</a></li>' for i, o in enumerate(SORT_OPTIONS))}</ul>
  </section>
</details>"""

SEARCH_FILTERS = filters("Шевченківський", "12000", "2026-10-01", "1 жовтня")

# Видача: 9 оголошень, кожне — своя сторінка (перше — listing.html, решта —
# listing-<slug>.html). Фото — лише з visuals/: нових кімнат у наборі поки п’ять,
# тож кадри повторюються (visuals/README.md — промпт для нових).
# (slug, назва, ціна, мета, фото, автор, ім’я в давальному, вік, співмешканці, кімнат, опис, підпис людини)
ROOM_COVERS = {
    "bedroom": ROOM_PHOTOS[0], "sofa": ROOM_PHOTOS[1], "armchair": ROOM_PHOTOS[2],
    "living": (visual("room-lukianivska-living"), "Кімната з диваном, рослинами й книжковою полицею"),
    "corner": (visual("room-lukianivska-corner"), "Кімната з кріслом, торшером і книжковою полицею"),
}
ROOMS = [
    ("lukianivska", "Кімната біля Лук’янівської", "10 500", "Шевченківський · 2 співмешканці · з 1 жовтня", "bedroom", 0, "Ірині", 29, "2 людини", 3,
     "Окрема кімната у трикімнатній квартирі. Комунальні платежі оплачуються окремо.", "Живе з одним співмешканцем"),
    ("tatarka", "Світла кімната на Татарці", "9 800", "Шевченківський · 1 співмешканка · з 5 жовтня", "sofa", 1, "Марині", 26, "1 людина", 2,
     "Кімната з диваном і комодом у двокімнатній квартирі, вікна на тихий двір.", "Живе сама, працює з дому"),
    ("kpi", "Кімната поруч із КПІ", "11 500", "Шевченківський · 2 співмешканки · з 12 жовтня", "armchair", 2, "Олі", 24, "2 людини", 3,
     "Кімната з робочим столом і кріслом. Десять хвилин пішки до метро.", "Живе з подругою, обидві студентки"),
    ("zoloti-vorota", "Кімната з диваном біля Золотих воріт", "12 000", "Шевченківський · 1 співмешканець · з 1 жовтня", "living", 1, "Марині", 27, "1 людина", 2,
     "Простора кімната в старому будинку зі стелями 3,2 м. Комунальні включено в ціну.", "Живе з братом"),
    ("lvivska", "Кімната з кріслом на Львівській площі", "10 000", "Шевченківський · 2 співмешканці · з 15 жовтня", "corner", 2, "Олі", 25, "2 людини", 3,
     "Затишна кімната з книжковою полицею. У квартирі є пральна машина й посудомийка.", "Живе з двома співмешканцями"),
    ("universytet", "Тиха кімната біля Університету", "9 500", "Шевченківський · 1 співмешканка · з 3 жовтня", "bedroom", 0, "Ірині", 29, "1 людина", 2,
     "Тиха кімната з видом на ботанічний сад. Без тварин.", "Живе сама"),
    ("syrets", "Кімната на Сирці з балконом", "8 700", "Шевченківський · 2 співмешканці · з 10 жовтня", "sofa", 1, "Марині", 26, "2 людини", 3,
     "Кімната з виходом на балкон. Поруч парк «Сирецький гай».", "Живе з двома співмешканцями"),
    ("dorohozhychi", "Кімната на Дорогожичах", "11 000", "Шевченківський · 1 співмешканець · з 20 жовтня", "armchair", 2, "Олі", 24, "1 людина", 2,
     "Кімната з робочим місцем у новому будинку, три хвилини до метро.", "Живе з одним співмешканцем"),
    ("nyvky", "Простора кімната на Нивках", "9 000", "Шевченківський · 2 співмешканки · з 7 жовтня", "living", 0, "Ірині", 29, "2 людини", 3,
     "Велика кімната з диваном у тихому районі біля парку «Нивки».", "Живе з двома співмешканками"),
]


# Чат з автором оголошення: Ірина, Марина, Оля (розділ «Чати» нижче).
CHAT_HREF = ["chat.html", "chat-maryna.html", "chat-olia.html"]


def room_href(slug):
    return "listing.html" if slug == ROOMS[0][0] else f"listing-{slug}.html"


def room_cards(current=None):
    """Картки видачі; current — slug вибраного оголошення (aria-current на посиланні)."""
    out = []
    for slug, title, price, meta, cover, who, *_ in ROOMS:
        c = card(title, f"{price} грн/міс", meta, ROOM_COVERS[cover], href=room_href(slug), author=AUTHORS[who])
        if slug == current:
            c = c.replace('class="listing-card__link"', 'class="listing-card__link" aria-current="page"', 1)
        out.append(c)
    return "".join(out)


page(
    "listings",
    title="Результати пошуку — Куток",
    job=JOB_SEARCH,
    body_class="has-tabbar has-split",
    body=split(search_head("Київ · кімнати та співмешканці")
    + f"""
<main class="shell__main" id="content">
{SEARCH_FILTERS}
<div class="results-meta"><span>12 оголошень</span>{SORT_SHEET}</div>
<ul class="card-list">{room_cards()}
</ul>
<a class="button button--secondary button--block" href="listings.html">Показати ще 3</a>
</main>"""),
)

page(
    "listings-empty",
    title="Результати пошуку — нічого не знайдено",
    job=JOB_SEARCH,
    body_class="has-tabbar has-split",
    body=split(search_head("Київ · кімнати та співмешканці")
    + f"""
<main class="shell__main" id="content">
{filters("Подільський", "8500", "2026-09-25", "25 вересня")}
<div class="results-meta"><span>0 оголошень</span></div>
<section class="state">
  <div class="state__icon">{icon("search-magnifier")}</div>
  <h2 class="state__title">За цими умовами оголошень немає</h2>
  <p class="state__text">Зміни бюджет, район або дату заїзду.</p>
  <div class="state__actions"><a class="button button--primary" href="listings.html">Змінити фільтри</a></div>
</section>
</main>"""),
)

page(
    "listings-error",
    title="Результати пошуку — помилка",
    job=JOB_SEARCH,
    body_class="has-tabbar has-split",
    body=split(search_head("Київ · кімнати та співмешканці")
    + f"""
<main class="shell__main" id="content">
{SEARCH_FILTERS}
<div class="results-meta"><span>Фільтри збережено</span></div>
<section class="state state--error" role="alert">
  <div class="state__icon">{icon("alerts-warning-triangle")}</div>
  <h2 class="state__title">Не вдалося завантажити оголошення</h2>
  <p class="state__text">Перевір з’єднання й спробуй ще.</p>
  <div class="state__actions"><a class="button button--primary" href="listings.html">Спробувати ще</a></div>
</section>
</main>"""),
)

SK_CARD = """
  <li class="listing-card"><div class="skeleton skeleton--photo"></div><div class="listing-card__body"><div class="skeleton skeleton--title"></div><div class="skeleton skeleton--line skeleton--w60"></div></div></li>"""

page(
    "listings-loading",
    title="Результати пошуку — завантаження",
    job=JOB_SEARCH,
    body_class="has-tabbar has-split",
    body=split(search_head("Київ · кімнати та співмешканці")
    + f"""
<main class="shell__main" id="content" aria-busy="true">
{SEARCH_FILTERS}
<div class="results-meta"><span role="status">Завантажуємо оголошення</span></div>
<ul class="card-list" aria-hidden="true">{SK_CARD * 3}
</ul>
</main>"""),
)

# ---------- Оголошення ----------

JOB_LISTING = "Related 1 — звузити пошук; Related 2 — зменшити невизначеність; Related 3 — оцінити придатність до спільного побуту; Related 4 — перевести придатний варіант у взаємну домовленість"
JOB_LISTING_STATE = "Related 1–4 — оцінка кімнати, людини й перехід до контакту"
# Рядок «що підтверджено» — і в оголошенні, і в профілі.
TRUST_ROW = f"""<li class="group__row verified-note"><span class="verified-note__icon">{lin("shield-check")}</span><span class="verified-note__text"><strong class="verified-note__title">Номер підтверджено 12 вересня</strong><br><span class="verified-note__limit">Це означає лише, що людина має доступ до цього номера.</span></span></li>"""
# Інші фото тієї ж квартири для каруселі під головним фото.
GALLERY = [
    (visual("room-lukianivska-living"), "Спільна вітальня з диваном, рослинами й книжковою полицею"),
    (visual("room-lukianivska-kitchen"), "Спільна кухня з білими шафами й обіднім столом біля вікна"),
    (visual("room-lukianivska-corner"), "Куточок вітальні з кріслом, торшером і книжковою полицею"),
    (visual("room-lukianivska-bathroom"), "Спільна ванна кімната з пральною машиною"),
]

# Стрічка ліворуч від оголошення (від --bp-desktop): та сама видача, вибрана
# картка — aria-current="page"; на телефоні цієї панелі не видно (--detail).
def feed_pane(current=ROOMS[0][0]):
    return search_head("Київ · кімнати та співмешканці", heading=False) + f"""
<div class="shell__main">
{SEARCH_FILTERS}
<div class="results-meta"><span>12 оголошень</span>{SORT_SHEET}</div>
<ul class="card-list">{room_cards(current)}
</ul>
<a class="button button--secondary button--block" href="listings.html">Показати ще 3</a>
</div>"""


FEED_PANE = feed_pane()
# Закрити оголошення — лише на ширині (split.css): справа в шапці деталі, веде на
# видачу без вибору; на телефоні той самий шлях — «назад».
CLOSE = f'<a class="topbar__action split__close" href="listings.html" aria-label="Закрити оголошення">{lin("close")}</a>'
LISTING_PHOTO_BAR = appbar("", "listings.html", "результатів", action=REPORT + CLOSE, over_photo=True)
LISTING_BAR = appbar("", "listings.html", "результатів", action=CLOSE)


def listing_detail(room):
    slug, title, price, meta, cover, who, dat, age, mates, flat, about, caption = room
    name, face = AUTHORS[who]
    gen = ("Ірини", "Марини", "Олі")[who]
    src, alt = ROOM_COVERS[cover]
    district, *_, date = meta.split(" · ")
    gallery = GALLERY if slug == ROOMS[0][0] else []  # інших фото квартири поки є лише в першого
    count = f'<span class="photo-count">1 / {len(gallery) + 1}</span>' if gallery else ""
    strip = (f'<ul class="gallery" tabindex="0" aria-label="Інші фото квартири">'
             + "".join(f'<li class="gallery__item"><img src="{g}" alt="{a}" loading="lazy"></li>' for g, a in gallery) + "</ul>") if gallery else ""
    rooms_word = {2: "2 кімнати", 3: "3 кімнати"}[flat]
    return LISTING_PHOTO_BAR + f"""
<main class="shell__main" id="content">
<div class="hero-photo"><img src="{src}" alt="{alt}"><p class="price-tag">{price} грн/міс</p>{count}</div>
{strip}
<div class="listing-title">
  <h1 class="listing-title__name">{title}</h1>
  <p class="listing-title__meta">{district} район · {date}</p>
</div>
<dl class="group">
  <div class="group__row"><dt class="group__label">Співмешканці</dt><dd class="group__value">{mates}</dd></div>
  <div class="group__row"><dt class="group__label">Квартира</dt><dd class="group__value">{rooms_word}</dd></div>
  <div class="group__row"><dt class="group__label">Комунальні</dt><dd class="group__value">окремо</dd></div>
</dl>
<p class="listing-description">{about}</p>
<h2 class="section-title">Хто живе в квартирі</h2>
<ul class="group">
  <li class="group__row"><a class="person-row" href="profile.html" aria-label="Відкрити профіль {gen}"><span class="avatar avatar--md"><img src="{face}" alt="Фото профілю {gen}">{MARK}</span><span class="person-row__text"><strong class="person-row__name">{name}, {age} {"роки" if age % 10 in (2, 3, 4) and age // 10 != 1 else "років"}</strong><span class="person-row__caption">{caption}</span></span>{CHEVRON_RIGHT}</a></li>
</ul>
<h2 class="section-title">Що підтверджено</h2>
<ul class="group">{TRUST_ROW}</ul>
</main>
<div class="actionbar"><a class="button button--primary" href="{CHAT_HREF[who]}">Написати {dat}</a></div>"""


for room in ROOMS:
    page(
        room_href(room[0])[:-5],
        title=f"{room[1]} — Куток",
        job=JOB_LISTING,
        body_class="has-tabbar has-actionbar photo-top has-split",
        body=split(feed_pane(room[0]), listing_detail(room), "split--detail"),
    )

page(
    "listing-empty",
    title="Оголошення — знято",
    job=JOB_LISTING_STATE,
    body_class="has-tabbar has-split",
    body=split(FEED_PANE, LISTING_BAR
    + f"""
<main class="shell__main" id="content">
<section class="state">
  <div class="state__icon">{icon("home")}</div>
  <h1 class="state__title">Оголошення зняли</h1>
  <p class="state__text">Кімната вже недоступна. Інші оголошення — в результатах пошуку.</p>
  <div class="state__actions"><a class="button button--primary" href="listings.html">Назад до результатів</a></div>
</section>
</main>""", "split--detail"),
)

page(
    "listing-error",
    title="Оголошення — помилка",
    job=JOB_LISTING_STATE,
    body_class="has-tabbar has-split",
    body=split(FEED_PANE, LISTING_BAR
    + f"""
<main class="shell__main" id="content">
<section class="state state--error" role="alert">
  <div class="state__icon">{icon("alerts-warning-triangle")}</div>
  <h1 class="state__title">Не вдалося завантажити оголошення</h1>
  <p class="state__text">Перевір з’єднання й спробуй ще.</p>
  <div class="state__actions"><a class="button button--primary" href="listing.html">Спробувати ще</a><a class="button button--secondary" href="listings.html">Назад до результатів</a></div>
</section>
</main>""", "split--detail"),
)

page(
    "listing-loading",
    title="Оголошення — завантаження",
    job=JOB_LISTING_STATE,
    body_class="has-tabbar has-actionbar photo-top status-dark has-split",
    body=split(FEED_PANE, LISTING_PHOTO_BAR
    + f"""
<main class="shell__main" id="content" aria-busy="true">
<h1 class="sr-only">Оголошення</h1>
<p class="sr-only" role="status">Завантажуємо оголошення</p>
<div class="hero-photo" aria-hidden="true"><div class="skeleton"></div></div>
<ul class="gallery" aria-hidden="true">{"<li class=\"gallery__item\"><div class=\"skeleton\"></div></li>" * len(GALLERY)}</ul>
<div class="listing-title skeleton-stack" aria-hidden="true"><div class="skeleton skeleton--title"></div><div class="skeleton skeleton--line skeleton--w40"></div></div>
<div class="group" aria-hidden="true"><div class="group__row"><div class="skeleton skeleton--line"></div></div><div class="group__row"><div class="skeleton skeleton--line skeleton--w60"></div></div><div class="group__row"><div class="skeleton skeleton--line skeleton--w40"></div></div></div>
<div class="skeleton skeleton--line skeleton--w40 skeleton--section" aria-hidden="true"></div>
<div class="group group--padded skeleton-person" aria-hidden="true"><div class="skeleton skeleton--avatar"></div><div class="skeleton-person__text"><div class="skeleton skeleton--line skeleton--w60"></div><div class="skeleton skeleton--line skeleton--w40"></div></div></div>
</main>
<div class="actionbar" aria-hidden="true"><div class="skeleton skeleton--button"></div></div>""", "split--detail"),
)

# ---------- Профіль ----------

JOB_PROFILE_STATE = "Related 2–3 — оцінка іншої сторони та побутової сумісності"
PROFILE_BAR = appbar("Профіль Ірини", "listing.html", "оголошення", action=REPORT, heading=False)
PROFILE_BAR_STATE = appbar("Профіль Ірини", "listing.html", "оголошення", heading=False)
PROFILE_HEAD = """
<div class="profile-head">
  <div class="avatar avatar--lg"><img src="{IRYNA}" alt="Фото профілю Ірини">{mark}</div>
  <h1 class="profile-head__name">{name}</h1>
  <p class="profile-head__caption">Оголошення «Кімната біля Лук’янівської»: 10 500 грн/місяць, заїзд з 1 жовтня.</p>
</div>"""
# Оголошення в профілі — та сама картка, що й у стрічці (урок 6, крок 6).
LISTING_ROW = card("Кімната біля Лук’янівської", "10 500 грн/міс", "з 1 жовтня", ROOM_PHOTOS[0], href="listing.html")

page(
    "profile",
    title="Профіль Ірини — Куток",
    job=JOB_LISTING,
    body_class="has-actionbar",
    body=PROFILE_BAR
    + f"""
<main class="shell__main" id="content">
{PROFILE_HEAD.format(name="Ірина, 29 років", mark=MARK, IRYNA=IRYNA)}
<h2 class="section-title">Спосіб життя</h2>
<dl class="group">
  <div class="group__row"><dt class="group__label">Розпорядок дня</dt><dd class="group__value">будні, 9:00–18:00</dd></div>
  <div class="group__row"><dt class="group__label">Куріння</dt><dd class="group__value">не курить</dd></div>
  <div class="group__row"><dt class="group__label">Тварини</dt><dd class="group__value">кіт у квартирі</dd></div>
  <div class="group__row"><dt class="group__label">Гості</dt><dd class="group__value">за домовленістю</dd></div>
  <div class="group__row"><dt class="group__label">Тиша ввечері</dt><dd class="group__value">після 23:00</dd></div>
</dl>
<h2 class="section-title">Що підтверджено</h2>
<ul class="group">{TRUST_ROW}</ul>
<h2 class="section-title">Оголошення</h2>
<ul class="card-list">{LISTING_ROW}</ul>
</main>
<div class="actionbar"><a class="button button--primary" href="chat.html">Написати Ірині</a></div>""",
)

page(
    "profile-empty",
    title="Профіль Ірини — неповний",
    job="Related 2 — зменшити невизначеність; Related 3 — оцінити придатність до спільного побуту",
    body_class="has-actionbar",
    body=PROFILE_BAR
    + f"""
<main class="shell__main" id="content">
{PROFILE_HEAD.format(name="Ірина", mark=MARK, IRYNA=IRYNA)}
<h2 class="section-title">Спосіб життя</h2>
<section class="state-note">
  <h3 class="state-note__title">Про розпорядок дня, куріння й гостей Ірина не написала</h3>
  <p class="state-note__text">Можна запитати в чаті.</p>
</section>
<h2 class="section-title">Що підтверджено</h2>
<ul class="group">{TRUST_ROW}</ul>
<h2 class="section-title">Оголошення</h2>
<ul class="card-list">{LISTING_ROW}</ul>
</main>
<div class="actionbar"><a class="button button--primary" href="chat.html">Написати Ірині</a></div>""",
)

page(
    "profile-error",
    title="Профіль Ірини — помилка",
    job=JOB_PROFILE_STATE,
    body_class="",
    body=PROFILE_BAR_STATE
    + f"""
<main class="shell__main" id="content">
<section class="state state--error" role="alert">
  <div class="state__icon">{icon("alerts-warning-triangle")}</div>
  <h1 class="state__title">Не вдалося завантажити профіль</h1>
  <p class="state__text">Перевір з’єднання й спробуй ще.</p>
  <div class="state__actions"><a class="button button--primary" href="profile.html">Спробувати ще</a><a class="button button--secondary" href="listings.html">Назад до результатів</a></div>
</section>
</main>""",
)

page(
    "profile-loading",
    title="Профіль Ірини — завантаження",
    job=JOB_PROFILE_STATE,
    body_class="has-actionbar",
    body=PROFILE_BAR_STATE
    + """
<main class="shell__main" id="content" aria-busy="true">
<h1 class="sr-only">Профіль Ірини</h1>
<p class="sr-only" role="status">Завантажуємо профіль</p>
<div class="profile-head" aria-hidden="true"><div class="skeleton skeleton--avatar-lg"></div><div class="skeleton skeleton--title"></div><div class="skeleton skeleton--line skeleton--w60"></div></div>
<div class="group" aria-hidden="true"><div class="group__row"><div class="skeleton skeleton--line"></div></div><div class="group__row"><div class="skeleton skeleton--line skeleton--w60"></div></div><div class="group__row"><div class="skeleton skeleton--line"></div></div><div class="group__row"><div class="skeleton skeleton--line skeleton--w40"></div></div></div>
</main>
<div class="actionbar" aria-hidden="true"><div class="skeleton skeleton--button"></div></div>""",
)


# ---------- Чати ----------
# Перелік чатів + чат (split.css, --tablet): на телефоні — два кроки, від
# --bp-tablet — дві панелі поруч (responsive/width-audit.md, «Перелік розмов» і
# «Чат із людиною»). Нічого не вибрано — права панель «Обери чат ліворуч»:
# рядки переліку не займають ширину, як картки, тож --solo тут лише тоді, коли
# чатів немає, вони не завантажились або ще вантажаться.

JOB_CHAT = "Related 4 — перевести придатний варіант у взаємну домовленість"
JOB_CHATS = "Related 4 — повернутися до потрібного чату й продовжити домовленість"


def bubble(mine, text, when):
    cls = "bubble bubble--mine" if mine else "bubble"
    return f'  <li class="{cls}"><p>{text}</p><time class="bubble__time" datetime="{when}">{when[-5:]}</time></li>'


# (сторінка, ім’я, давальний, орудний, автор у AUTHORS, оголошення в ROOMS, день, повідомлення)
CHATS = [
    ("chat", "Ірина", "Ірині", "Іриною", 0, 0, ("18 вересня", "2026-09-18"), [
        (True, "Вітаю! Чи актуальна кімната і чи можна подивитися її цього тижня?", "18:12"),
        (False, "Так, актуальна. Можу показати в суботу після 12:00. У квартирі живемо вдвох і є кіт.", "18:24"),
        (True, "Субота о 13:00 підходить. Домовилися?", "18:27"),
        (False, "Так, домовилися. Напишу адресу в суботу зранку.", "18:31"),
    ]),
    ("chat-maryna", "Марина", "Марині", "Мариною", 1, 1, ("20 вересня", "2026-09-20"), [
        (True, "Привіт! Кімната на Татарці ще вільна? Хочу заїхати з 5 жовтня.", "10:05"),
        (False, "Привіт! Так, вільна. Я працюю з дому, тож удень у квартирі тихо.", "10:40"),
        (True, "Мені підходить. Коли можна подивитися?", "10:42"),
        (False, "Можна в неділю після 11:00.", "11:15"),
    ]),
    ("chat-olia", "Оля", "Олі", "Олею", 2, 2, ("21 вересня", "2026-09-21"), [
        (True, "Вітаю! Я теж навчаюся в КПІ. Чи можна подивитися кімнату цього тижня?", "16:02"),
        (False, "Привіт! Так, можна. Ми з подругою вдома після 18:00.", "16:20"),
        (True, "Четвер о 18:30 підходить?", "16:21"),
        (False, "Так, четвер о 18:30. Чекаємо!", "16:34"),
    ]),
]
CHAT_IRYNA = CHATS[0]


def chats_head(heading=True):
    tag = "h1" if heading else "p"
    return f'<header class="header"><div class="header__top">{THEME}<{tag} class="header__title">Чати</{tag}></div></header>'


def chat_rows(current=None):
    """Рядки переліку: людина + останнє повідомлення; відкритий чат — aria-current."""
    rows = []
    for href, name, _dat, _ins, who, *_, msgs in CHATS:
        cur = ' aria-current="page"' if href == current else ""
        face = AUTHORS[who][1]
        rows.append(f'<li class="group__row"><a class="person-row" href="{href}.html"{cur}><span class="avatar avatar--md"><img src="{face}" alt="">{MARK}</span>'
                    f'<span class="person-row__text"><strong class="person-row__name">{name}</strong><span class="person-row__caption">{msgs[-1][1]}</span></span>{CHEVRON_RIGHT}</a></li>')
    return '<ul class="group">' + "".join(rows) + "</ul>"


def chats_pane(current=None):
    """Перелік чатів. current=None — він головний (<main>), інакше — поруч із чатом (div)."""
    if current is None:
        return chats_head() + f"""
<main class="shell__main" id="content">
{chat_rows()}
</main>"""
    return chats_head(heading=False) + f"""
<div class="shell__main">
{chat_rows(current)}
</div>"""


def chat_bar(chat):
    href, name, dat, ins, who, *_ = chat
    close = f'<a class="topbar__action split__close" href="chats.html" aria-label="Закрити чат">{lin("close")}</a>'
    return (f'<header class="topbar topbar--person"><a class="topbar__back" href="chats.html" aria-label="Назад до чатів">{CHEVRON_LEFT}</a>'
            f'<a class="topbar__person" href="profile.html"><span class="avatar"><img src="{AUTHORS[who][1]}" alt=""></span><strong class="topbar__name">{name}</strong>'
            f'<span class="topbar__verified" title="Номер підтверджено 12 вересня">{lin("shield-check")}<span class="sr-only">Номер підтверджено 12 вересня</span></span></a>'
            f'{end_slot(REPORT + close)}</header>\n<h1 class="sr-only">Чат з {ins}</h1>')


def chat_context(chat):
    room = ROOMS[chat[5]]
    slug, title, price, meta, cover = room[:5]
    date = meta.split(" · ")[-1].replace(" ", " ")
    price = price.replace(" ", " ")
    return (f'<a class="chat-context" href="{room_href(slug)}"><img class="chat-context__thumb" src="{ROOM_COVERS[cover][0]}" alt="">'
            f'<span class="chat-context__text"><strong class="chat-context__title">{title}</strong>'
            f'<span class="chat-context__meta">{price} грн/міс · {date} · номер підтверджено 12 вересня</span></span>{CHEVRON_RIGHT}</a>')


def composer(chat, text="", placeholder="Повідомлення", ready=None):
    # «Надіслати» активна, лише коли є що надіслати й чат завантажився.
    # Вимкнена — справжній disabled (поза Tab); вмикає скрипт за подією input.
    wait = ready is False
    ready = bool(text) if ready is None else ready
    off = "" if ready else " disabled"
    send = f'<button class="composer__send" type="submit" aria-label="Надіслати"{off}>{lin("plain-2")}</button>'
    attrs = f' action="{chat[0]}.html"' + (" data-wait" if wait else "")
    return f"""<form class="composer"{attrs}><label class="sr-only" for="message">Повідомлення {chat[2]}</label><textarea class="composer__input" id="message" name="message" rows="1" placeholder="{placeholder}">{text}</textarea>{send}</form>"""


def chat_page(name, chat, *, title, middle, text="", ready=None, busy=False):
    b = ' aria-busy="true"' if busy else ""
    detail = chat_bar(chat) + f"""
<main class="shell__main" id="content"{b}>
{chat_context(chat)}
{middle}
</main>
{composer(chat, text, ready=ready)}"""
    page(name, title=title, job=JOB_CHAT, body_class="has-tabbar has-composer has-split", tab="chats",
         body=split(chats_pane(chat[0]), detail, "split--tablet split--detail"))


page(
    "chats",
    title="Чати — Куток",
    job=JOB_CHATS,
    body_class="has-tabbar has-split",
    tab="chats",
    body=split(chats_pane(), nothing("чат", "messages-bubble-smile", "Тут відкриється переписка й кімната, про яку йдеться."), "split--tablet"),
)

page(
    "chats-empty",
    title="Чати — порожньо",
    job=JOB_CHATS,
    body_class="has-tabbar has-split",
    tab="chats",
    body=split(chats_head() + f"""
<main class="shell__main" id="content">
<section class="state">
  <div class="state__icon">{icon("messages-bubble-smile")}</div>
  <h2 class="state__title">Чатів ще немає</h2>
  <p class="state__text">Знайди кімнату чи співмешканця й напиши першим — чат з’явиться тут.</p>
  <div class="state__actions"><a class="button button--primary" href="listings.html">Перейти до пошуку</a></div>
</section>
</main>""", mods="split--tablet"),
)

page(
    "chats-error",
    title="Чати — помилка",
    job=JOB_CHATS,
    body_class="has-tabbar has-split",
    tab="chats",
    body=split(chats_head() + f"""
<main class="shell__main" id="content">
<section class="state state--error" role="alert">
  <div class="state__icon">{icon("alerts-warning-triangle")}</div>
  <h2 class="state__title">Не вдалося завантажити чати</h2>
  <p class="state__text">Перевір з’єднання й спробуй ще.</p>
  <div class="state__actions"><a class="button button--primary" href="chats.html">Спробувати ще</a></div>
</section>
</main>""", mods="split--tablet"),
)

SK_CHAT_ROW = '<div class="group__row skeleton-person"><div class="skeleton skeleton--avatar"></div><div class="skeleton-person__text"><div class="skeleton skeleton--line skeleton--w40"></div><div class="skeleton skeleton--line skeleton--w60"></div></div></div>'

page(
    "chats-loading",
    title="Чати — завантаження",
    job=JOB_CHATS,
    body_class="has-tabbar has-split",
    tab="chats",
    body=split(chats_head() + f"""
<main class="shell__main" id="content" aria-busy="true">
<p class="sr-only" role="status">Завантажуємо чати</p>
<div class="group" aria-hidden="true">{SK_CHAT_ROW * 3}</div>
</main>""", mods="split--tablet"),
)

for chat in CHATS:
    href, name, dat, ins, who, room, (day, iso), msgs = chat
    chat_page(href, chat, title=f"Чат з {ins} — Куток",
              middle=f'<p class="chat-day">{day}</p>\n<ol class="messages">\n'
              + "\n".join(bubble(m, t, f"{iso}T{h}") for m, t, h in msgs) + "\n</ol>")

chat_page(
    "chat-empty", CHAT_IRYNA, title="Чат з Іриною — новий",
    text="Вітаю! Мене звати Марта. Чи актуальна кімната і чи можна домовитися про перегляд?",
    middle=f"""<section class="state">
  <div class="state__icon">{icon("messages-bubble-smile")}</div>
  <h2 class="state__title">Повідомлень з Іриною ще немає</h2>
  <p class="state__text">Представся й запитай, чи кімната ще вільна і коли можна прийти на перегляд.</p>
</section>""",
)

chat_page(
    "chat-error", CHAT_IRYNA, title="Чат з Іриною — помилка",
    text="Чи можна подивитися кімнату в суботу?", ready=False,
    middle=f"""<section class="state state--error" role="alert">
  <div class="state__icon">{icon("alerts-warning-triangle")}</div>
  <h2 class="state__title">Не вдалося завантажити повідомлення</h2>
  <p class="state__text">Перевір з’єднання й спробуй ще. Чернетку збережено — її не надіслано.</p>
  <div class="state__actions"><a class="button button--primary" href="chat.html">Спробувати ще</a><a class="button button--secondary" href="listings.html">Назад до результатів</a></div>
</section>""",
)

chat_page(
    "chat-loading", CHAT_IRYNA, title="Чат з Іриною — завантаження", busy=True,
    middle="""<p class="sr-only" role="status">Завантажуємо повідомлення</p>
<div class="skeleton-stack" aria-hidden="true">
  <div class="skeleton skeleton--bubble skeleton--mine"></div>
  <div class="skeleton skeleton--bubble skeleton--bubble-tall"></div>
  <div class="skeleton skeleton--bubble skeleton--mine skeleton--bubble-short"></div>
</div>""",
)

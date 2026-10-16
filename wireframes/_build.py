#!/usr/bin/env python3
"""Збирає HTML-вайрфрейми «Кутка» зі спільної мобільної оболонки.

Запуск: python3 wireframes/_build.py — перезаписує всі *.html у wireframes/.
Зміст екранів редагуємо тут, а не в згенерованих файлах.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent

CHEVRON_LEFT = '<svg viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M12.5 4.5 7 10l5.5 5.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEVRON_RIGHT = '<svg class="chevron" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="m6 3.5 4.5 4.5L6 12.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MORE = '<svg viewBox="0 0 20 20" aria-hidden="true" focusable="false"><circle cx="4.5" cy="10" r="1.6" fill="currentColor"/><circle cx="10" cy="10" r="1.6" fill="currentColor"/><circle cx="15.5" cy="10" r="1.6" fill="currentColor"/></svg>'
SEND = '<svg viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M10 16V4M5 9l5-5 5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


# Усі екрани зібрані з кіта компонентів (урок 7): ../ui/kit.css — компоненти
# й змінні, screens.css — разові блоки. Іконки — iconify (Streamline Freehand
# і Solar linear).
HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="../ui/kit.css">
<link rel="stylesheet" href="screens.css">
<script src="https://cdn.jsdelivr.net/npm/iconify-icon@2.1.0/dist/iconify-icon.min.js"></script>"""
# Класи вайрфреймів → модифікатори оболонки кіта. status-dark — лише позначка
# для хабу уроків (темний статус-бар над світлим скелетоном), стилів не має.
SHELL = {"has-tabbar": "shell--tabbar", "has-actionbar": "shell--actionbar", "has-composer": "shell--composer", "photo-top": "shell--photo-top", "status-dark": "status-dark"}
# Тап за межами шторки (по затемненню) або Escape закриває її.
SHEET_SCRIPT = """
<script>
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


# Ірина — власний портрет (згенеровано Codex, 2026-10-09), решта — стоки Unsplash.
IRYNA = "../assets/people/iryna.jpg"


def portrait(photo_id, size):
    if photo_id.endswith(".jpg"):
        return photo_id
    return f"https://images.unsplash.com/photo-{photo_id}?w={size}&q=70&auto=format&fit=crop&crop=faces"


def page(name, *, title, job, body, body_class="has-tabbar", tab="search"):
    shell = " ".join(["shell"] + [SHELL[c] for c in body_class.split()])
    tabs = [("search", "Пошук", "listings.html"), ("chats", "Чати", "chat.html"), ("profile", "Профіль", None)]
    items = []
    for key, label, href in tabs:
        current = ' aria-current="page"' if key == tab else ""
        inner = f'{icon(TAB_ICONS[key])}<span>{label}</span>'
        if href:
            items.append(f'<li><a class="tabbar__item" href="{href}"{current}>{inner}</a></li>')
        else:
            items.append(f'<li><span class="tabbar__item"{current}>{inner}</span></li>')
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


def appbar(title, back_href=None, back_label="Назад", action="", over_photo=False):
    back = (
        f'<a class="topbar__back" href="{back_href}" aria-label="Назад до {back_label}">{CHEVRON_LEFT}</a>'
        if back_href
        else "<span></span>"
    )
    heading = f'<h1 class="topbar__title">{title}</h1>' if title else "<span></span>"
    mod = " topbar--over-photo" if over_photo else ""
    return f'<header class="topbar{mod}">{back}{heading}{action or "<span></span>"}</header>'


# ---------- Результати пошуку ----------

JOB_SEARCH = "Related 1 — звузити пошук до прийнятних варіантів"


def filters(district, budget, date, date_label):
    options = "".join(
        f'<option{" selected" if d == district else ""}>{d}</option>'
        for d in ["Усі райони", "Шевченківський", "Подільський", "Голосіївський", "Дніпровський"]
    )
    budget_label = f"{int(budget):,}".replace(",", " ")
    return f"""
<div class="chip-row"><div class="chip-row__track">
  <details class="sheet">
    <summary class="chip chip--selected">{lin("tuning-2")}Фільтри · 3</summary>
    <section class="sheet__panel" aria-labelledby="filters-title">
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


def search_head(sub):
    return f'<header class="header"><div class="header__top"><h1 class="header__title">Результати пошуку</h1><p class="header__subtitle">{sub}</p></div></header>'


def card(title, price, meta, photo, href="listing.html", author=None):
    # Keep "з 1 жовтня" and "2 співмешканці" from breaking across lines.
    meta = " · ".join(part.replace(" ", "\u00a0") for part in meta.split(" · "))
    src, alt = photo
    who = ""
    if author:
        name, face = author
        who = (
            f'\n      <p class="card-author"><span class="avatar"><img src="{portrait(face, 96)}" alt="">'
            f'<span class="avatar__mark" aria-label="Номер підтверджено">{lin("check")}</span></span>{name}</p>'
        )
    # Ціна — на бирці від ключа поверх фото (concept.html, «Бирка з ключем»).
    return f"""
  <li class="listing-card">
    <div class="listing-card__photo">
      <img src="https://images.unsplash.com/photo-{src}?w=720&q=70&auto=format&fit=crop" alt="{alt}" loading="lazy">
      <p class="price-tag">{price}</p>{who}
    </div>
    <div class="listing-card__body">
      <h2 class="listing-card__title"><a class="listing-card__link" href="{href}">{title}</a></h2>
      <p class="listing-card__meta">{meta}</p>
    </div>
  </li>"""


# Фото за темою: кімната — інтер'єр (список і перевірка — concept/references.md).
ROOM_PHOTOS = [
    ("1522771739844-6a9f6d5f14af", "Світла спальня з ліжком, тумбою і настінною лампою"),
    ("1513694203232-719a280e022f", "Світла кімната з чорним диваном, комодом, торшером і рослиною"),
    ("1586023492125-27b2c045efd7", "Кімната з жовтим кріслом, торшером і картиною"),
]
# Автори оголошень — портрети зі стоку (Unsplash), список — concept/references.md.
AUTHORS = [
    ("Ірина", IRYNA),
    ("Марина", "1544005313-94ddf0286df2"),
    ("Оля", "1517841905240-472988babdf9"),
]


# Сортування — така сама шторка, як фільтри (тап по «Спершу нові»).
SORT_OPTIONS = ["Спершу нові", "Спершу дешевші", "Спершу дорожчі"]
SORT_SHEET = f"""<details class="sheet sort-sheet">
  <summary class="sort">Спершу нові<svg viewBox="0 0 12 12" aria-hidden="true"><path d="m3 4.5 3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></summary>
  <section class="sheet__panel" aria-labelledby="sort-title">
    <div class="sheet__grabber" aria-hidden="true"></div>
    <div class="sheet__head"><h2 class="sheet__title" id="sort-title">Сортування</h2><a class="button button--text" href="listings.html">Скасувати</a></div>
    <ul class="sort-options">{"".join(f'<li><a href="listings.html"{' aria-current="true"' if i == 0 else ''}>{o}{lin("check") if i == 0 else ""}</a></li>' for i, o in enumerate(SORT_OPTIONS))}</ul>
  </section>
</details>"""

SEARCH_FILTERS = filters("Шевченківський", "12000", "2026-10-01", "1 жовтня")

page(
    "listings",
    title="Результати пошуку — Куток",
    job=JOB_SEARCH,
    body=search_head("Київ · кімнати та співмешканці")
    + f"""
<main class="shell__main" id="content">
{SEARCH_FILTERS}
<div class="results-meta"><span>12 оголошень</span>{SORT_SHEET}</div>
<ul class="card-list">{card("Кімната біля Лук’янівської", "10 500 грн/міс", "Шевченківський · 2 співмешканці · з 1 жовтня", ROOM_PHOTOS[0], author=AUTHORS[0])}{card("Світла кімната на Татарці", "9 800 грн/міс", "Шевченківський · 1 співмешканка · з 5 жовтня", ROOM_PHOTOS[1], author=AUTHORS[1])}{card("Кімната поруч із КПІ", "11 500 грн/міс", "Шевченківський · 2 співмешканки · з 12 жовтня", ROOM_PHOTOS[2], author=AUTHORS[2])}
</ul>
</main>""",
)

page(
    "listings-empty",
    title="Результати пошуку — нічого не знайдено",
    job=JOB_SEARCH,
    body=search_head("Київ · кімнати та співмешканці")
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
</main>""",
)

page(
    "listings-error",
    title="Результати пошуку — помилка",
    job=JOB_SEARCH,
    body=search_head("Київ · кімнати та співмешканці")
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
</main>""",
)

SK_CARD = """
  <li class="listing-card"><div class="skeleton skeleton--photo"></div><div class="listing-card__body"><div class="skeleton skeleton--title"></div><div class="skeleton skeleton--line skeleton--w60"></div></div></li>"""

page(
    "listings-loading",
    title="Результати пошуку — завантаження",
    job=JOB_SEARCH,
    body=search_head("Київ · кімнати та співмешканці")
    + f"""
<main class="shell__main" id="content" aria-busy="true">
{SEARCH_FILTERS}
<div class="results-meta"><span role="status">Завантажуємо оголошення</span></div>
<ul class="card-list" aria-hidden="true">{SK_CARD * 3}
</ul>
</main>""",
)

# ---------- Оголошення ----------

JOB_LISTING = "Related 1 — звузити пошук; Related 2 — зменшити невизначеність; Related 3 — оцінити придатність до спільного побуту; Related 4 — перевести придатний варіант у взаємну домовленість"
JOB_LISTING_STATE = "Related 1–4 — оцінка кімнати, людини й перехід до контакту"
LISTING_BAR = appbar("", "listings.html", "результатів")
LISTING_PHOTO_BAR = appbar("", "listings.html", "результатів", over_photo=True)
# Рядок «що підтверджено» — і в оголошенні, і в профілі.
TRUST_ROW = f"""<li class="group__row verified-note"><span class="verified-note__icon">{lin("shield-check")}</span><span class="verified-note__text"><strong class="verified-note__title">Номер підтверджено 12 вересня</strong><br><span class="verified-note__limit">Це означає лише, що людина має доступ до цього номера.</span></span></li>"""
# Інші фото квартири для каруселі під головним фото (стоки Unsplash).
GALLERY = [
    ("1493809842364-78817add7ffb", "Спільна вітальня з синім диваном і рослинами"),
    ("1484154218962-a197022b5858", "Кухня з білими шафами й острівцем"),
    ("1502672260266-1c1ef2d93688", "Куточок вітальні з диваном і книжковою полицею"),
    ("1554995207-c18c203602cb", "Вітальня з коричневим диваном і подушками"),
]

page(
    "listing",
    title="Оголошення — Куток",
    job=JOB_LISTING,
    body_class="has-actionbar photo-top",
    body=LISTING_PHOTO_BAR
    + f"""
<main class="shell__main" id="content">
<div class="hero-photo"><img src="https://images.unsplash.com/photo-{ROOM_PHOTOS[0][0]}?w=900&q=70&auto=format&fit=crop" alt="{ROOM_PHOTOS[0][1]}"><span class="photo-count">1 / {len(GALLERY) + 1}</span></div>
<ul class="gallery" aria-label="Інші фото квартири">{"".join(f'<li class="gallery__item"><img src="https://images.unsplash.com/photo-{g}?w=480&q=70&auto=format&fit=crop" alt="{alt}" loading="lazy"></li>' for g, alt in GALLERY)}</ul>
<div class="listing-title">
  <h1 class="listing-title__name">Кімната біля Лук’янівської</h1>
  <p class="listing-title__price">10 500 грн/міс</p>
  <p class="listing-title__meta">Шевченківський район · з 1 жовтня</p>
</div>
<dl class="group">
  <div class="group__row"><dt class="group__label">Співмешканці</dt><dd class="group__value">2 людини</dd></div>
  <div class="group__row"><dt class="group__label">Квартира</dt><dd class="group__value">3 кімнати</dd></div>
  <div class="group__row"><dt class="group__label">Комунальні</dt><dd class="group__value">окремо</dd></div>
</dl>
<p class="listing-description">Окрема кімната у трикімнатній квартирі. Комунальні платежі оплачуються окремо.</p>
<h2 class="section-title">Хто живе в квартирі</h2>
<ul class="group">
  <li class="group__row"><a class="person-row" href="profile.html" aria-label="Відкрити профіль Ірини"><span class="avatar avatar--md"><img src="{portrait(AUTHORS[0][1], 120)}" alt="Фото профілю Ірини"><span class="avatar__mark">{lin("check")}</span></span><span class="person-row__text"><strong class="person-row__name">Ірина, 29 років</strong><span class="person-row__caption">Живе з одним співмешканцем</span></span>{CHEVRON_RIGHT}</a></li>
  {TRUST_ROW}
</ul>
</main>
<div class="actionbar"><a class="button button--primary" href="chat.html">Написати Ірині</a></div>""",
)

page(
    "listing-empty",
    title="Оголошення про кімнату — стан не передбачений",
    job="Стан відсутній у wireframes/_screens.md",
    body_class="",
    body=LISTING_BAR
    + f"""
<main class="shell__main" id="content">
<section class="state">
  <div class="state__icon">{icon("home")}</div>
  <h2 class="state__title">Оголошення зняли</h2>
  <p class="state__text">Кімната вже недоступна. Інші оголошення — в результатах пошуку.</p>
  <div class="state__actions"><a class="button button--primary" href="listings.html">Назад до результатів</a></div>
</section>
</main>""",
)

page(
    "listing-error",
    title="Оголошення — помилка",
    job=JOB_LISTING_STATE,
    body_class="",
    body=LISTING_BAR
    + f"""
<main class="shell__main" id="content">
<section class="state state--error" role="alert">
  <div class="state__icon">{icon("alerts-warning-triangle")}</div>
  <h2 class="state__title">Не вдалося завантажити оголошення</h2>
  <p class="state__text">Перевір з’єднання й спробуй ще.</p>
  <div class="state__actions"><a class="button button--primary" href="listing.html">Спробувати ще</a><a class="button button--secondary" href="listings.html">Назад до результатів</a></div>
</section>
</main>""",
)

page(
    "listing-loading",
    title="Оголошення — завантаження",
    job=JOB_LISTING_STATE,
    body_class="has-actionbar photo-top status-dark",
    body=LISTING_PHOTO_BAR
    + f"""
<main class="shell__main" id="content" aria-busy="true">
<p class="sr-only" role="status">Завантажуємо оголошення</p>
<div class="hero-photo" aria-hidden="true"><div class="skeleton"></div></div>
<ul class="gallery" aria-hidden="true">{"<li class=\"gallery__item\"><div class=\"skeleton\"></div></li>" * len(GALLERY)}</ul>
<div class="listing-title skeleton-stack" aria-hidden="true"><div class="skeleton skeleton--title"></div><div class="skeleton skeleton--line skeleton--w40"></div></div>
<div class="group group--padded skeleton-stack" aria-hidden="true"><div class="skeleton skeleton--line group__row"></div><div class="skeleton skeleton--line skeleton--w60 group__row"></div><div class="skeleton skeleton--line skeleton--w40 group__row"></div></div>
<div class="skeleton skeleton--line skeleton--w40 skeleton--section" aria-hidden="true"></div>
<div class="group group--padded skeleton-person" aria-hidden="true"><div class="skeleton skeleton--avatar group__row"></div><div class="group__row skeleton-person__text"><div class="skeleton skeleton--line skeleton--w60"></div><div class="skeleton skeleton--line skeleton--w40"></div></div></div>
</main>
<div class="actionbar" aria-hidden="true"><div class="skeleton skeleton--button"></div></div>""",
)

# ---------- Профіль ----------

JOB_PROFILE_STATE = "Related 2–3 — оцінка іншої сторони та побутової сумісності"
PROFILE_BAR = appbar("Профіль Ірини", "listing.html", "оголошення")
PROFILE_HEAD = """
<div class="profile-head">
  <div class="avatar avatar--lg"><img src="{IRYNA}" alt="Фото профілю Ірини"><span class="avatar__mark">{mark}</span></div>
  <h2 class="profile-head__name">{name}</h2>
  <p class="profile-head__caption">Здає кімнату біля Лук’янівської</p>
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
{PROFILE_HEAD.format(name="Ірина, 29 років", mark=lin("check"), IRYNA=IRYNA)}
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
{PROFILE_HEAD.format(name="Ірина", mark=lin("check"), IRYNA=IRYNA)}
<h2 class="section-title">Спосіб життя</h2>
<section class="state-note">
  <h2 class="state-note__title">Про розпорядок дня, куріння й гостей Ірина не написала</h2>
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
    body=PROFILE_BAR
    + f"""
<main class="shell__main" id="content">
<section class="state state--error" role="alert">
  <div class="state__icon">{icon("alerts-warning-triangle")}</div>
  <h2 class="state__title">Не вдалося завантажити профіль</h2>
  <p class="state__text">Перевір з’єднання й спробуй ще.</p>
  <div class="state__actions"><a class="button button--primary" href="profile.html">Спробувати ще</a><a class="button button--secondary" href="listing.html">Назад до оголошення</a></div>
</section>
</main>""",
)

page(
    "profile-loading",
    title="Профіль Ірини — завантаження",
    job=JOB_PROFILE_STATE,
    body_class="has-actionbar",
    body=PROFILE_BAR
    + """
<main class="shell__main" id="content" aria-busy="true">
<p class="sr-only" role="status">Завантажуємо профіль</p>
<div class="profile-head" aria-hidden="true"><div class="skeleton skeleton--avatar-lg"></div><div class="skeleton skeleton--title"></div><div class="skeleton skeleton--line skeleton--w60"></div></div>
<div class="group group--padded skeleton-stack" aria-hidden="true"><div class="skeleton skeleton--line group__row"></div><div class="skeleton skeleton--line skeleton--w60 group__row"></div><div class="skeleton skeleton--line group__row"></div><div class="skeleton skeleton--line skeleton--w40 group__row"></div></div>
</main>
<div class="actionbar" aria-hidden="true"><div class="skeleton skeleton--button"></div></div>""",
)

# ---------- Чат ----------

JOB_CHAT = "Related 4 — перевести придатний варіант у взаємну домовленість"
CHAT_BAR = f"""<header class="topbar topbar--person"><a class="topbar__back" href="listing.html" aria-label="Назад до оголошення">{CHEVRON_LEFT}</a><a class="topbar__person" href="profile.html"><span class="avatar"><img src="{portrait(AUTHORS[0][1], 96)}" alt="Фото профілю Ірини"></span><strong class="topbar__name">Ірина</strong><span class="topbar__verified" title="Номер підтверджено">{lin("shield-check")}<span class="sr-only">Номер підтверджено</span></span></a><button class="topbar__action" type="button" aria-label="Заблокувати або поскаржитися">{MORE}</button></header>"""
CHAT_CONTEXT = f"""<a class="chat-context" href="listing.html"><img class="chat-context__thumb" src="https://images.unsplash.com/photo-{ROOM_PHOTOS[0][0]}?w=160&q=70&auto=format&fit=crop" alt="Фото кімнати"><span class="chat-context__text"><strong class="chat-context__title">Кімната біля Лук’янівської</strong><span class="chat-context__meta">10 500 грн/міс · з 1 жовтня</span></span>{CHEVRON_RIGHT}</a>"""


def composer(text, placeholder="Повідомлення"):
    return f"""<form class="composer"><label class="sr-only" for="message">Повідомлення Ірині</label><textarea class="composer__input" id="message" name="message" rows="1" placeholder="{placeholder}">{text}</textarea><a class="composer__send" href="chat.html" aria-label="Надіслати">{lin("plain-2")}</a></form>"""


page(
    "chat",
    title="Чат з Іриною — Куток",
    job=JOB_CHAT,
    body_class="has-composer",
    body=CHAT_BAR
    + f"""
<main class="shell__main" id="content">
{CHAT_CONTEXT}
<p class="chat-day">18 вересня</p>
<ol class="messages">
  <li class="bubble bubble--mine"><p>Вітаю! Чи актуальна кімната і чи можна подивитися її цього тижня?</p><time class="bubble__time" datetime="2026-09-18T18:12">18:12</time></li>
  <li class="bubble"><p>Так, актуальна. Можу показати в суботу після 12:00. У квартирі живемо вдвох і є кіт.</p><time class="bubble__time" datetime="2026-09-18T18:24">18:24</time></li>
  <li class="bubble bubble--mine"><p>Субота о 13:00 підходить. Домовилися?</p><time class="bubble__time" datetime="2026-09-18T18:27">18:27</time></li>
  <li class="bubble"><p>Так, домовилися. Напишу адресу в суботу зранку.</p><time class="bubble__time" datetime="2026-09-18T18:31">18:31</time></li>
</ol>
</main>
{composer("")}""",
)

page(
    "chat-empty",
    title="Чат з Іриною — новий",
    job=JOB_CHAT,
    body_class="has-composer",
    body=CHAT_BAR
    + f"""
<main class="shell__main" id="content">
{CHAT_CONTEXT}
<section class="state">
  <div class="state__icon">{icon("messages-bubble-smile")}</div>
  <h2 class="state__title">Повідомлень з Іриною ще немає</h2>
  <p class="state__text">Представся й запитай, чи кімната ще вільна і коли можна прийти на перегляд.</p>
</section>
</main>
{composer("Вітаю! Мене звати Марта. Чи актуальна кімната і чи можна домовитися про перегляд?")}""",
)

page(
    "chat-error",
    title="Чат з Іриною — помилка",
    job=JOB_CHAT,
    body_class="has-composer",
    body=CHAT_BAR
    + f"""
<main class="shell__main" id="content">
{CHAT_CONTEXT}
<section class="state state--error" role="alert">
  <div class="state__icon">{icon("alerts-warning-triangle")}</div>
  <h2 class="state__title">Не вдалося завантажити повідомлення</h2>
  <p class="state__text">Перевір з’єднання й спробуй ще. Чернетку збережено — її не надіслано.</p>
  <div class="state__actions"><a class="button button--primary" href="chat.html">Спробувати ще</a></div>
</section>
</main>
{composer("Чи можна подивитися кімнату в суботу?")}""",
)

page(
    "chat-loading",
    title="Чат з Іриною — завантаження",
    job=JOB_CHAT,
    body_class="has-composer",
    body=CHAT_BAR
    + f"""
<main class="shell__main" id="content" aria-busy="true">
{CHAT_CONTEXT}
<p class="sr-only" role="status">Завантажуємо повідомлення</p>
<div class="skeleton-stack" aria-hidden="true">
  <div class="skeleton skeleton--bubble skeleton--mine"></div>
  <div class="skeleton skeleton--bubble skeleton--bubble-tall"></div>
  <div class="skeleton skeleton--bubble skeleton--mine skeleton--bubble-short"></div>
</div>
</main>
{composer("")}""",
)

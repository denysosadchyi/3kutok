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
SLIDERS = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M2 4.5h7M12 4.5h2M2 11.5h2M7 11.5h7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="10.5" cy="4.5" r="1.6" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="5.5" cy="11.5" r="1.6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
SEND = '<svg viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M10 16V4M5 9l5-5 5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def page(name, *, title, job, body, body_class="has-tabbar", tab="search"):
    tabs = [("search", "Пошук", "listings.html"), ("chats", "Чати", None), ("profile", "Профіль", None)]
    items = []
    for key, label, href in tabs:
        current = ' aria-current="page"' if key == tab else ""
        inner = f'<span class="tab-icon" aria-hidden="true"></span><span>{label}</span>'
        if href:
            items.append(f'<li><a href="{href}"{current}>{inner}</a></li>')
        else:
            items.append(f'<li><span class="tab"{current}>{inner}</span></li>')
    tabbar = (
        '\n<nav class="tabbar" aria-label="Головна навігація"><ul>' + "".join(items) + "</ul></nav>"
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
<link rel="stylesheet" href="listings-states.css">
</head>
<body class="{body_class}">
{body.strip()}{tabbar}
</body>
</html>
"""
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")


def appbar(title, back_href=None, back_label="Назад", action=""):
    back = (
        f'<a class="appbar-back" href="{back_href}" aria-label="Назад до {back_label}">{CHEVRON_LEFT}</a>'
        if back_href
        else "<span></span>"
    )
    heading = f'<h1 class="appbar-title">{title}</h1>' if title else "<span></span>"
    return f'<header class="appbar">{back}{heading}{action or "<span></span>"}</header>'


# ---------- Результати пошуку ----------

JOB_SEARCH = "Related 1 — звузити пошук до прийнятних варіантів"


def filters(district, budget, date, date_label):
    options = "".join(
        f'<option{" selected" if d == district else ""}>{d}</option>'
        for d in ["Усі райони", "Шевченківський", "Подільський", "Голосіївський", "Дніпровський"]
    )
    budget_label = f"{int(budget):,}".replace(",", " ")
    return f"""
<div class="filters"><div class="filter-row">
  <details class="sheet">
    <summary class="chip chip-strong">{SLIDERS}Фільтри · 3</summary>
    <section class="sheet-panel" aria-labelledby="filters-title">
      <div class="sheet-grabber" aria-hidden="true"></div>
      <div class="sheet-head"><a class="btn btn-plain" href="listings.html">Скасувати</a><h2 id="filters-title">Фільтри</h2><span></span></div>
      <form class="sheet-body" action="listings-loading.html" method="get">
        <fieldset>
          <legend class="sr-only">Базові умови кімнати</legend>
          <div class="field"><label for="district">Район Києва</label><select id="district" name="district">{options}</select></div>
          <div class="field"><label for="budget">Бюджет до, грн/місяць</label><input id="budget" name="budget" type="number" inputmode="numeric" min="1000" step="500" value="{budget}"></div>
          <div class="field"><label for="move-in">Дата заїзду</label><input id="move-in" name="move-in" type="text" inputmode="none" readonly value="з {date_label} 2026"></div>
        </fieldset>
      </form>
      <div class="sheet-foot"><a class="btn btn-primary btn-block" href="listings-loading.html">Застосувати фільтри</a></div>
    </section>
  </details>
  <span class="chip">{district}</span>
  <span class="chip">до {budget_label} грн</span>
  <span class="chip">з {date_label}</span>
</div></div>"""


def search_head(sub):
    return f'<header class="appbar-large"><h1>Результати пошуку</h1><p>{sub}</p></header>'


def card(title, price, meta):
    # Keep "з 1 жовтня" and "2 співмешканці" from breaking across lines.
    meta = " · ".join(part.replace(" ", "\u00a0") for part in meta.split(" · "))
    return f"""
  <li class="card">
    <div class="ph ph-photo" role="img" aria-label="Фото кімнати">Фото кімнати</div>
    <div class="card-body">
      <h2><a class="card-link" href="listing-loading.html">{title}</a></h2>
      <p class="card-price">{price}</p>
      <p class="card-meta">{meta}</p>
    </div>
  </li>"""


SEARCH_FILTERS = filters("Шевченківський", "12000", "2026-10-01", "1 жовтня")

page(
    "listings",
    title="Результати пошуку — Куток",
    job=JOB_SEARCH,
    body=search_head("Київ · кімнати та співмешканці")
    + f"""
<main id="content">
{SEARCH_FILTERS}
<div class="results-meta"><span>12 оголошень</span><button class="sort" type="button">Спершу нові<svg viewBox="0 0 12 12" aria-hidden="true"><path d="m3 4.5 3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button></div>
<ul class="card-list">{card("Кімната біля Лук’янівської", "10 500 грн/міс", "Шевченківський · 2 співмешканці · з 1 жовтня")}{card("Світла кімната на Татарці", "9 800 грн/міс", "Шевченківський · 1 співмешканка · з 5 жовтня")}{card("Кімната поруч із КПІ", "11 500 грн/міс", "Шевченківський · 2 співмешканки · з 12 жовтня")}
</ul>
</main>""",
)

page(
    "listings-empty",
    title="Результати пошуку — нічого не знайдено",
    job=JOB_SEARCH,
    body=search_head("Київ · кімнати та співмешканці")
    + f"""
<main id="content">
{filters("Подільський", "8500", "2026-09-25", "25 вересня")}
<div class="results-meta"><span>0 оголошень</span></div>
<section class="state">
  <div class="state-icon" aria-hidden="true"></div>
  <h2>За цими умовами оголошень немає</h2>
  <p>Зміни бюджет, район або дату заїзду.</p>
  <div class="actions"><a class="btn btn-primary" href="listings.html">Змінити фільтри</a></div>
</section>
</main>""",
)

page(
    "listings-error",
    title="Результати пошуку — помилка",
    job=JOB_SEARCH,
    body=search_head("Київ · кімнати та співмешканці")
    + f"""
<main id="content">
{SEARCH_FILTERS}
<div class="results-meta"><span>Фільтри збережено</span></div>
<section class="state" role="alert">
  <div class="state-icon" aria-hidden="true"></div>
  <h2>Не вдалося завантажити оголошення</h2>
  <p>Перевір з’єднання й спробуй ще.</p>
  <div class="actions"><a class="btn btn-primary" href="listings-loading.html">Спробувати ще</a></div>
</section>
</main>""",
)

SK_CARD = """
  <li class="card"><div class="skeleton ph-photo"></div><div class="card-body stack-8"><div class="skeleton sk-title"></div><div class="skeleton sk-line w-40"></div><div class="skeleton sk-line w-60"></div></div></li>"""

page(
    "listings-loading",
    title="Результати пошуку — завантаження",
    job=JOB_SEARCH,
    body=search_head("Київ · кімнати та співмешканці")
    + f"""
<main id="content" aria-busy="true">
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

page(
    "listing",
    title="Оголошення — Куток",
    job=JOB_LISTING,
    body_class="has-actionbar",
    body=LISTING_BAR
    + f"""
<main id="content">
<div class="hero-photo"><div class="ph ph-photo" role="img" aria-label="Фото кімнати">Фото кімнати</div></div>
<div class="title-block">
  <h1>Кімната біля Лук’янівської</h1>
  <p class="price">10 500 грн/міс</p>
  <p class="muted small">Шевченківський район · з 1 жовтня</p>
</div>
<dl class="list">
  <div><dt>Співмешканці</dt><dd>2 людини</dd></div>
  <div><dt>Квартира</dt><dd>3 кімнати</dd></div>
  <div><dt>Комунальні</dt><dd>окремо</dd></div>
</dl>
<p class="surface">Окрема кімната у трикімнатній квартирі. Комунальні платежі оплачуються окремо.</p>
<h2 class="section-title">Хто живе в квартирі</h2>
<ul class="list">
  <li><a class="list-link" href="profile-loading.html" aria-label="Відкрити профіль Ірини"><span class="ph ph-avatar" role="img" aria-label="Фото профілю"></span><span class="grow"><strong>Ірина, 29 років</strong><span class="muted small">Живе з одним співмешканцем</span></span>{CHEVRON_RIGHT}</a></li>
  <li class="note"><span class="dot" aria-hidden="true"></span><span><strong>Номер підтверджено 12 вересня</strong><br><span class="muted small">Це означає лише, що людина має доступ до цього номера.</span></span></li>
</ul>
</main>
<div class="actionbar"><a class="btn btn-primary" href="chat-loading.html">Написати Ірині</a></div>""",
)

page(
    "listing-empty",
    title="Оголошення про кімнату — стан не передбачений",
    job="Стан відсутній у wireframes/_screens.md",
    body_class="",
    body=LISTING_BAR
    + """
<main id="content">
<section class="state">
  <div class="state-icon" aria-hidden="true"></div>
  <h2>Оголошення зняли</h2>
  <p>Кімната вже недоступна. Інші оголошення — в результатах пошуку.</p>
  <div class="actions"><a class="btn btn-primary" href="listings.html">Назад до результатів</a></div>
</section>
</main>""",
)

page(
    "listing-error",
    title="Оголошення — помилка",
    job=JOB_LISTING_STATE,
    body_class="",
    body=LISTING_BAR
    + """
<main id="content">
<section class="state" role="alert">
  <div class="state-icon" aria-hidden="true"></div>
  <h2>Не вдалося завантажити оголошення</h2>
  <p>Перевір з’єднання й спробуй ще.</p>
  <div class="actions"><a class="btn btn-primary" href="listing-loading.html">Спробувати ще</a><a class="btn btn-secondary" href="listings.html">Назад до результатів</a></div>
</section>
</main>""",
)

page(
    "listing-loading",
    title="Оголошення — завантаження",
    job=JOB_LISTING_STATE,
    body_class="has-actionbar",
    body=LISTING_BAR
    + """
<main id="content" aria-busy="true">
<p class="sr-only" role="status">Завантажуємо оголошення</p>
<div class="hero-photo" aria-hidden="true"><div class="skeleton ph-photo" style="border-radius:0"></div></div>
<div class="title-block stack-8" aria-hidden="true"><div class="skeleton sk-title"></div><div class="skeleton sk-line w-40"></div></div>
<div class="list stack-8" aria-hidden="true" style="padding:14px 16px"><div class="skeleton sk-line"></div><div class="skeleton sk-line w-60"></div><div class="skeleton sk-line w-40"></div></div>
<div class="skeleton sk-line w-40" aria-hidden="true" style="margin-top:8px"></div>
<div class="list" aria-hidden="true" style="padding:12px 16px;display:flex;gap:12px;align-items:center"><div class="skeleton ph-avatar"></div><div class="stack-8" style="flex:1"><div class="skeleton sk-line w-60"></div><div class="skeleton sk-line w-40"></div></div></div>
</main>
<div class="actionbar" aria-hidden="true"><div class="skeleton sk-btn"></div></div>""",
)

# ---------- Профіль ----------

JOB_PROFILE_STATE = "Related 2–3 — оцінка іншої сторони та побутової сумісності"
PROFILE_BAR = appbar("Профіль Ірини", "listing.html", "оголошення")
PROFILE_HEAD = """
<div class="profile-head">
  <div class="ph ph-avatar-lg" role="img" aria-label="Фото профілю">Фото профілю</div>
  <h2>{name}</h2>
  <p class="muted small">Здає кімнату біля Лук’янівської</p>
</div>"""
LISTING_ROW = f"""<li><a class="list-link" href="listing.html" aria-label="Відкрити оголошення"><span class="ph ph-thumb" role="img" aria-label="Фото кімнати"></span><span class="grow"><strong>Кімната біля Лук’янівської</strong><span class="muted small">10 500 грн/міс · з 1 жовтня</span></span>{CHEVRON_RIGHT}</a></li>"""
TRUST_ROW = """<li class="note"><span class="dot" aria-hidden="true"></span><span><strong>Номер підтверджено 12 вересня</strong><br><span class="muted small">Це означає лише, що людина має доступ до цього номера.</span></span></li>"""

page(
    "profile",
    title="Профіль Ірини — Куток",
    job=JOB_LISTING,
    body_class="has-actionbar",
    body=PROFILE_BAR
    + f"""
<main id="content">
{PROFILE_HEAD.format(name="Ірина, 29 років")}
<h2 class="section-title">Спосіб життя</h2>
<dl class="list">
  <div><dt>Розпорядок дня</dt><dd>будні, 9:00–18:00</dd></div>
  <div><dt>Куріння</dt><dd>не курить</dd></div>
  <div><dt>Тварини</dt><dd>кіт у квартирі</dd></div>
  <div><dt>Гості</dt><dd>за домовленістю</dd></div>
  <div><dt>Тиша ввечері</dt><dd>після 23:00</dd></div>
</dl>
<h2 class="section-title">Що підтверджено</h2>
<ul class="list">{TRUST_ROW}</ul>
<h2 class="section-title">Оголошення</h2>
<ul class="list">{LISTING_ROW}</ul>
</main>
<div class="actionbar"><a class="btn btn-primary" href="chat-loading.html">Написати Ірині</a></div>""",
)

page(
    "profile-empty",
    title="Профіль Ірини — неповний",
    job="Related 2 — зменшити невизначеність; Related 3 — оцінити придатність до спільного побуту",
    body_class="has-actionbar",
    body=PROFILE_BAR
    + f"""
<main id="content">
{PROFILE_HEAD.format(name="Ірина")}
<h2 class="section-title">Спосіб життя</h2>
<section class="state" style="padding:20px">
  <h2>Про розпорядок дня, куріння й гостей Ірина не написала</h2>
  <p>Можна запитати в чаті.</p>
</section>
<h2 class="section-title">Що підтверджено</h2>
<ul class="list">{TRUST_ROW}</ul>
<h2 class="section-title">Оголошення</h2>
<ul class="list">{LISTING_ROW}</ul>
</main>
<div class="actionbar"><a class="btn btn-primary" href="chat-loading.html">Написати Ірині</a></div>""",
)

page(
    "profile-error",
    title="Профіль Ірини — помилка",
    job=JOB_PROFILE_STATE,
    body_class="",
    body=PROFILE_BAR
    + """
<main id="content">
<section class="state" role="alert">
  <div class="state-icon" aria-hidden="true"></div>
  <h2>Не вдалося завантажити профіль</h2>
  <p>Перевір з’єднання й спробуй ще.</p>
  <div class="actions"><a class="btn btn-primary" href="profile-loading.html">Спробувати ще</a><a class="btn btn-secondary" href="listing.html">Назад до оголошення</a></div>
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
<main id="content" aria-busy="true">
<p class="sr-only" role="status">Завантажуємо профіль</p>
<div class="profile-head" aria-hidden="true"><div class="skeleton ph-avatar-lg"></div><div class="skeleton sk-title" style="width:40%"></div><div class="skeleton sk-line" style="width:55%"></div></div>
<div class="list stack-8" aria-hidden="true" style="padding:14px 16px"><div class="skeleton sk-line"></div><div class="skeleton sk-line w-60"></div><div class="skeleton sk-line"></div><div class="skeleton sk-line w-40"></div></div>
</main>
<div class="actionbar" aria-hidden="true"><div class="skeleton sk-btn"></div></div>""",
)

# ---------- Чат ----------

JOB_CHAT = "Related 4 — перевести придатний варіант у взаємну домовленість"
CHAT_BAR = f"""<header class="appbar"><a class="appbar-back" href="listing.html" aria-label="Назад до оголошення">{CHEVRON_LEFT}</a><div class="appbar-person"><span class="ph ph-avatar" role="img" aria-label="Фото профілю"></span><span><strong>Ірина</strong><span>Номер підтверджено</span></span></div><button class="appbar-action" type="button" aria-label="Заблокувати або поскаржитися">{MORE}</button></header>"""
CHAT_CONTEXT = f"""<a class="chat-context" href="listing.html"><span class="ph ph-thumb" role="img" aria-label="Фото кімнати"></span><span class="grow"><strong>Кімната біля Лук’янівської</strong><span>10 500 грн/міс · з 1 жовтня</span></span>{CHEVRON_RIGHT}</a>"""


def composer(text, placeholder="Повідомлення"):
    return f"""<form class="composer"><label class="sr-only" for="message">Повідомлення Ірині</label><textarea id="message" name="message" rows="1" placeholder="{placeholder}">{text}</textarea><a class="send" href="chat-loading.html" aria-label="Надіслати">{SEND}</a></form>"""


page(
    "chat",
    title="Чат з Іриною — Куток",
    job=JOB_CHAT,
    body_class="has-composer",
    body=CHAT_BAR
    + f"""
<main id="content">
{CHAT_CONTEXT}
<p class="day">18 вересня</p>
<ol class="messages">
  <li class="msg mine"><p>Вітаю! Чи актуальна кімната і чи можна подивитися її цього тижня?</p><time datetime="2026-09-18T18:12">18:12</time></li>
  <li class="msg"><p>Так, актуальна. Можу показати в суботу після 12:00. У квартирі живемо вдвох і є кіт.</p><time datetime="2026-09-18T18:24">18:24</time></li>
  <li class="msg mine"><p>Субота о 13:00 підходить. Домовилися?</p><time datetime="2026-09-18T18:27">18:27</time></li>
  <li class="msg"><p>Так, домовилися. Напишу адресу в суботу зранку.</p><time datetime="2026-09-18T18:31">18:31</time></li>
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
<main id="content">
{CHAT_CONTEXT}
<section class="state">
  <div class="state-icon" aria-hidden="true"></div>
  <h2>Повідомлень з Іриною ще немає</h2>
  <p>Представся й запитай, чи кімната ще вільна і коли можна прийти на перегляд.</p>
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
<main id="content">
{CHAT_CONTEXT}
<section class="state" role="alert">
  <div class="state-icon" aria-hidden="true"></div>
  <h2>Не вдалося завантажити повідомлення</h2>
  <p>Перевір з’єднання й спробуй ще. Чернетку збережено — її не надіслано.</p>
  <div class="actions"><a class="btn btn-primary" href="chat-loading.html">Спробувати ще</a></div>
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
<main id="content" aria-busy="true">
{CHAT_CONTEXT}
<p class="sr-only" role="status">Завантажуємо повідомлення</p>
<div class="stack-8" aria-hidden="true">
  <div class="skeleton" style="height:52px;width:70%;margin-left:auto;border-radius:18px"></div>
  <div class="skeleton" style="height:68px;width:76%;border-radius:18px"></div>
  <div class="skeleton" style="height:40px;width:52%;margin-left:auto;border-radius:18px"></div>
</div>
</main>
{composer("")}""",
)

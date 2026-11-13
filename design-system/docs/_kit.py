"""Шматки живої розмітки кіта для сторінок документації.

Розмітка — та сама, що в ui/kit.html (канон), лише шляхи до фото з docs/.
Сторінки docs/ підключають ../index.css, тож кожен шматок малює справжній
компонент системи, а не картинку. Інлайн-стилів немає: обгортки — класи
.doc-* з docs.css.

P(n, at) — позначка частини для анатомії: data-pin="n" (+ data-pin-at —
кут мітки: tl tr bl br t b l r c). docs.js ставить номер поверх сцени.
"""

import html as _html
import re as _re

V = "../../visuals/"

_uid = [0]


def uid(prefix="d"):
    """Унікальний id на сторінці (поля, заголовки шторок)."""
    _uid[0] += 1
    return f"{prefix}{_uid[0]}"


def P(n, at=None):
    return f' data-pin="{n}"' + (f' data-pin-at="{at}"' if at else "")


def ico(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<iconify-icon{c} icon="{name}" aria-hidden="true"></iconify-icon>'


# ── Навігація ──
def back(label="Назад до оголошення", pin=""):
    return f'<a class="topbar__back"{pin} href="#" aria-label="{label}">{ico("solar:alt-arrow-left-linear")}</a>'


def more(pin=""):
    return f'<button class="topbar__action"{pin} type="button" aria-label="Заблокувати чи поскаржитися">{ico("solar:menu-dots-linear")}</button>'


def topbar(title="Профіль Ірини", back_label="Назад до оголошення"):
    return f'<header class="topbar">{back(back_label)}<p class="topbar__title">{title}</p>{more()}</header>'


def topbar_person():
    return ('<header class="topbar topbar--person">' + back() +
            f'<a class="topbar__person" href="#">{avatar(mark=False, alt="Фото профілю Ірини")}<strong class="topbar__name">Ірина</strong>'
            f'<span class="topbar__verified" title="Номер підтверджено 12 вересня">{ico("solar:shield-check-linear")}<span class="sr-only">Номер підтверджено</span></span></a>'
            + more() + '</header>')


def topbar_photo():
    return f'<header class="topbar topbar--over-photo">{back("Назад до результатів")}<span></span>{more()}</header>'


def tabbar(active="search"):
    def item(key, icon, label):
        cur = ' aria-current="page"' if key == active else ""
        if key == "profile":
            return f'<li><a class="tabbar__item" aria-disabled="true">{ico(icon)}<span>{label}</span></a></li>'
        return f'<li><a class="tabbar__item" href="#"{cur}>{ico(icon)}<span>{label}</span></a></li>'
    return ('<nav class="tabbar" aria-label="Приклад нижнього меню"><ul class="tabbar__list">'
            + item("search", "streamline-freehand:search-magnifier", "Пошук")
            + item("chats", "streamline-freehand:messages-bubble-smile", "Чати")
            + item("profile", "streamline-freehand:smiley-happy", "Профіль")
            + '</ul></nav>')


def actionbar(label="Написати Ірині", loading=False):
    if loading:
        return '<div class="actionbar" aria-hidden="true"><div class="skeleton skeleton--button"></div></div>'
    return f'<div class="actionbar"><a class="button button--primary" href="#">{label}</a></div>'


def filters_chip(extra_cls=""):
    return f'<summary class="chip chip--selected{extra_cls}">{ico("solar:tuning-2-linear")}Фільтри · 3</summary>'


def sheet(open_=False):
    t = uid("sheet-t")
    a, b, c = uid("f"), uid("f"), uid("f")
    o = " open" if open_ else ""
    return (f'<details class="sheet"{o}>' + filters_chip() +
            f'<section class="sheet__panel" aria-labelledby="{t}">'
            '<div class="sheet__grabber" aria-hidden="true"></div>'
            f'<div class="sheet__head"><h3 class="sheet__title" id="{t}">Фільтри</h3><a class="button button--text" href="#">Скасувати</a></div>'
            '<form class="sheet__body" action="#"><fieldset><legend class="sr-only">Базові умови кімнати</legend>'
            f'<div class="field"><label class="field__label" for="{a}">Район Києва</label><select class="input" id="{a}"><option>Усі райони</option><option selected>Шевченківський</option><option>Подільський</option><option>Голосіївський</option><option>Дніпровський</option></select></div>'
            f'<div class="field"><label class="field__label" for="{b}">Бюджет до, грн/місяць</label><input class="input" id="{b}" type="number" inputmode="numeric" min="1000" step="500" value="12000"></div>'
            f'<div class="field"><label class="field__label" for="{c}">Дата заїзду</label><input class="input" id="{c}" type="text" inputmode="none" readonly value="з 1 жовтня 2026"></div>'
            '</fieldset></form>'
            '<div class="sheet__foot"><a class="button button--primary button--block" href="#">Застосувати фільтри</a></div>'
            '</section></details>')


def header(bar=True):
    """Шапка стрічки; bar=True — як на екрані: під нею .chip-row у .shell__main."""
    top = '<div class="header__top"><h3 class="header__title">Результати пошуку</h3><p class="header__subtitle">Київ · кімнати та співмешканці</p></div>'
    if not bar:
        return f'<header class="header">{top}</header>'
    return f'<header class="header">{top}</header><div class="shell__main">{chip_row()}</div>'


def chip_row():
    return ('<div class="chip-row"><div class="chip-row__track">'
            f'<span class="chip chip--selected">{ico("solar:tuning-2-linear")}Фільтри · 3</span>'
            '<span class="chip">Шевченківський</span><span class="chip">до 12 000 грн</span><span class="chip">з 1 жовтня</span>'
            '</div></div>')


# ── Картки й списки ──
def mark():
    return f'<span class="avatar__mark">{ico("solar:check-linear")}<span class="sr-only">Номер підтверджено</span></span>'


def avatar(size="", mark_=True, mark=None, alt="Ірина", photo="person-iryna.jpg"):
    if mark is not None:
        mark_ = mark
    cls = "avatar" + (f" avatar--{size}" if size else "")
    m = globals()["mark"]() if mark_ else ""
    return f'<span class="{cls}"><img src="{V}{photo}" alt="{alt}">{m}</span>'


def price_tag(price="10 500 грн/міс"):
    return f'<p class="price-tag">{price}</p>'


ROOM_ALT = "Світла спальня з ліжком, тумбою і настінною лампою"


def listing_card(title="Кімната біля Лук’янівської", meta="Шевченківський · 2 співмешканці · з 1 жовтня",
                 photo="room-lukianivska-bedroom.jpg", alt=ROOM_ALT, price="10 500 грн/міс", link_cls=""):
    lc = f" {link_cls}" if link_cls else ""
    return ('<li class="listing-card">'
            f'<div class="listing-card__photo"><img src="{V}{photo}" alt="{alt}">{price_tag(price)}</div>'
            f'<div class="listing-card__body"><h3 class="listing-card__title"><a class="listing-card__link{lc}" href="#">{title}</a></h3>'
            f'<p class="listing-card__meta">{meta}</p></div></li>')


def listing_card_tatarka(link_cls=""):
    return listing_card("Світла кімната на Татарці", "з 5 жовтня", "room-tatarka-sofa.jpg",
                        "Світла кімната з диваном, комодом, торшером і рослиною", "9 800 грн/міс", link_cls)


def listing_card_loading():
    return ('<li class="listing-card"><div class="skeleton skeleton--photo"></div><div class="listing-card__body">'
            '<div class="skeleton skeleton--title"></div><div class="skeleton skeleton--line skeleton--w60"></div></div></li>')


def card_list(*cards, hidden=False):
    h = ' aria-hidden="true"' if hidden else ""
    return f'<ul class="card-list"{h}>' + "".join(cards) + '</ul>'


def profile_head(age=True, loading=False):
    if loading:
        return ('<div class="profile-head" aria-hidden="true"><div class="skeleton skeleton--avatar-lg"></div>'
                '<div class="skeleton skeleton--title"></div><div class="skeleton skeleton--line skeleton--w60"></div></div>')
    name = "Ірина, 29 років" if age else "Ірина"
    return (f'<div class="profile-head">{avatar("lg", alt="Фото профілю Ірини")}'
            f'<h3 class="profile-head__name">{name}</h3><p class="profile-head__caption">Оголошення «Кімната біля Лук’янівської»: 10 500 грн/місяць, заїзд з 1 жовтня.</p></div>')


LIFESTYLE = [("Розпорядок дня", "будні, 9:00–18:00"), ("Куріння", "не курить"), ("Тварини", "кіт у квартирі"),
             ("Гості", "за домовленістю"), ("Тиша ввечері", "після 23:00")]
FLAT = [("Співмешканці", "2 людини"), ("Квартира", "3 кімнати"), ("Комунальні", "окремо")]


def group(rows=LIFESTYLE):
    return '<dl class="group">' + "".join(
        f'<div class="group__row"><dt class="group__label">{k}</dt><dd class="group__value">{v}</dd></div>' for k, v in rows) + '</dl>'


def group_loading():
    return ('<div class="group" aria-hidden="true"><div class="group__row"><div class="skeleton skeleton--line"></div></div>'
            '<div class="group__row"><div class="skeleton skeleton--line skeleton--w60"></div></div>'
            '<div class="group__row"><div class="skeleton skeleton--line"></div></div>'
            '<div class="group__row"><div class="skeleton skeleton--line skeleton--w40"></div></div></div>')


def verified_row():
    return (f'<li class="group__row verified-note"><span class="verified-note__icon">{ico("solar:shield-check-linear")}</span>'
            '<span class="verified-note__text"><strong class="verified-note__title">Номер підтверджено 12 вересня</strong><br>'
            '<span class="verified-note__limit">Це означає лише, що людина має доступ до цього номера.</span></span></li>')


def person_row(cls=""):
    c = f" {cls}" if cls else ""
    return (f'<li class="group__row"><a class="person-row{c}" href="#" aria-label="Відкрити профіль Ірини">{avatar("md", alt="Фото профілю Ірини")}'
            '<span class="person-row__text"><strong class="person-row__name">Ірина, 29 років</strong>'
            '<span class="person-row__caption">Живе з одним співмешканцем</span></span>'
            f'{ico("solar:alt-arrow-right-linear", "chevron")}</a></li>')


def person_row_loading():
    return ('<div class="group group--padded skeleton-person" aria-hidden="true"><div class="skeleton skeleton--avatar"></div>'
            '<div class="skeleton-person__text"><div class="skeleton skeleton--line skeleton--w60"></div>'
            '<div class="skeleton skeleton--line skeleton--w40"></div></div></div>')


def hero_photo(loading=False):
    if loading:
        return '<div class="hero-photo"><div class="skeleton"></div></div>'
    return f'<div class="hero-photo"><img src="{V}room-lukianivska-bedroom.jpg" alt="{ROOM_ALT}">{price_tag()}</div>'


GALLERY = [("room-lukianivska-living.jpg", "Спільна вітальня з диваном, рослинами й книжковою полицею"),
           ("room-lukianivska-kitchen.jpg", "Спільна кухня з білими шафами й обіднім столом біля вікна"),
           ("room-lukianivska-corner.jpg", "Куточок вітальні з кріслом, торшером і книжковою полицею"),
           ("room-lukianivska-bathroom.jpg", "Спільна ванна кімната з пральною машиною")]


def gallery(loading=False):
    if loading:
        return '<ul class="gallery" aria-hidden="true">' + '<li class="gallery__item"><div class="skeleton"></div></li>' * 4 + '</ul>'
    return '<ul class="gallery" aria-label="Інші фото квартири">' + "".join(
        f'<li class="gallery__item"><img src="{V}{f}" alt="{a}"></li>' for f, a in GALLERY) + '</ul>'


def listing_title(loading=False):
    if loading:
        return '<div class="listing-title skeleton-stack" aria-hidden="true"><div class="skeleton skeleton--title"></div><div class="skeleton skeleton--line skeleton--w40"></div></div>'
    return '<div class="listing-title"><h3 class="listing-title__name">Кімната біля Лук’янівської</h3><p class="listing-title__meta">Шевченківський район · з 1 жовтня</p></div>'


def photo_top(inner):
    """Обгортка для hero-photo / gallery / listing-title: shell__main без верхнього поля."""
    return f'<div class="shell shell--photo-top"><div class="shell__main">{inner}</div></div>'


def results_meta(text="12 оголошень", status=False):
    r = ' role="status"' if status else ""
    return f'<div class="results-meta"><span{r}>{text}</span></div>'


def section_title(text="Спосіб життя"):
    return f'<h3 class="section-title">{text}</h3>'


# ── Форми ──
def button(text="Написати Ірині", kind="primary", extra=""):
    # «is-disabled» — не клас-імітація, а справжній disabled на <button> (base.css)
    off = "is-disabled" in extra.split()
    extra = " ".join(c for c in extra.split() if c != "is-disabled")
    e = f" {extra}" if extra else ""
    if off:
        return f'<button class="button button--{kind}{e}" type="button" disabled>{text}</button>'
    return f'<a class="button button--{kind}{e}" href="#">{text}</a>'


def chip(text="Шевченківський", selected=False, extra="", tag="span"):
    e = f" {extra}" if extra else ""
    if tag != "span":
        return f'<{tag} class="chip{e}" type="button">{text}</{tag}>'
    if selected:
        return f'<span class="chip chip--selected{e}">{ico("solar:tuning-2-linear")}Фільтри · 3</span>'
    return f'<span class="chip{e}">{text}</span>'


def field(kind="select", extra=""):
    i = uid("f")
    off = "is-disabled" in extra.split()
    extra = " ".join(c for c in extra.split() if c != "is-disabled")
    e = f" {extra}" if extra else ""
    d = " disabled" if off else ""
    if kind == "select":
        return (f'<div class="field"><label class="field__label" for="{i}">Район Києва</label><select class="input{e}" id="{i}"{d}>'
                '<option>Усі райони</option><option selected>Шевченківський</option><option>Подільський</option></select></div>')
    if kind == "number":
        return f'<div class="field"><label class="field__label" for="{i}">Бюджет до, грн/місяць</label><input class="input{e}" id="{i}" type="number" inputmode="numeric" value="12000"{d}></div>'
    return f'<div class="field"><label class="field__label" for="{i}">Дата заїзду</label><input class="input{e}" id="{i}" type="text" inputmode="none" readonly value="з 1 жовтня 2026"{d}></div>'


# ── Зворотний зв'язок ──
STATES = {
    "listings-empty": ("streamline-freehand:search-magnifier", "За цими умовами оголошень немає", "Зміни бюджет, район або дату заїзду.", ["Змінити фільтри"], False),
    "chat-empty": ("streamline-freehand:messages-bubble-smile", "Повідомлень з Іриною ще немає", "Представся й запитай, чи кімната ще вільна і коли можна прийти на перегляд.", [], False),
    "listing-empty": ("streamline-freehand:home", "Оголошення зняли", "Кімната вже недоступна. Інші оголошення — в результатах пошуку.", ["Назад до результатів"], False),
    "chat-error": ("streamline-freehand:alerts-warning-triangle", "Не вдалося завантажити повідомлення", "Перевір з’єднання й спробуй ще. Чернетку збережено — її не надіслано.", ["Спробувати ще"], True),
    "profile-error": ("streamline-freehand:alerts-warning-triangle", "Не вдалося завантажити профіль", "Перевір з’єднання й спробуй ще.", ["Спробувати ще", "Назад до оголошення"], True),
}


def state(key="listings-empty"):
    icon, title, text, actions, err = STATES[key]
    cls = "state state--error" if err else "state"
    role = ' role="alert"' if err else ""
    acts = ""
    if actions:
        acts = '<div class="state__actions">' + "".join(
            button(a, "primary" if n == 0 else "secondary") for n, a in enumerate(actions)) + '</div>'
    return (f'<section class="{cls}"{role}><div class="state__icon">{ico(icon)}</div>'
            f'<h3 class="state__title">{title}</h3><p class="state__text">{text}</p>{acts}</section>')


# ── Чат ──
def chat_context(extra=""):
    e = f" {extra}" if extra else ""
    return (f'<a class="chat-context{e}" href="#"><img class="chat-context__thumb" src="{V}room-lukianivska-bedroom.jpg" alt="Фото кімнати">'
            '<span class="chat-context__text"><strong class="chat-context__title">Кімната біля Лук’янівської</strong>'
            '<span class="chat-context__meta">10 500 грн/міс · з 1 жовтня</span></span>'
            f'{ico("solar:alt-arrow-right-linear", "chevron")}</a>')


MESSAGES = [(True, "Вітаю! Чи актуальна кімната і чи можна подивитися її цього тижня?", "18:12"),
            (False, "Так, актуальна. Можу показати в суботу після 12:00. У квартирі живемо вдвох і є кіт.", "18:24"),
            (True, "Субота о 13:00 підходить. Домовилися?", "18:27"),
            (False, "Так, домовилися. Напишу адресу в суботу зранку.", "18:31")]


def bubble(mine, text, time):
    m = " bubble--mine" if mine else ""
    return f'<li class="bubble{m}"><p>{text}</p><time class="bubble__time" datetime="2026-09-18T{time}">{time}</time></li>'


def messages(items=MESSAGES):
    return '<ol class="messages">' + "".join(bubble(*i) for i in items) + '</ol>'


def messages_loading():
    return ('<div class="skeleton-stack" aria-hidden="true"><div class="skeleton skeleton--bubble skeleton--mine"></div>'
            '<div class="skeleton skeleton--bubble skeleton--bubble-tall"></div>'
            '<div class="skeleton skeleton--bubble skeleton--bubble-short skeleton--mine"></div></div>')


def composer(text="", disabled=False, input_extra="", send_extra=""):
    i = uid("msg")
    ie = f" {input_extra}" if input_extra else ""
    se = f" {send_extra}" if send_extra else ""
    ph = ' placeholder="Повідомлення"'
    send_icon = ico("solar:plain-2-linear")
    if disabled:
        send = f'<button class="composer__send{se}" type="submit" aria-label="Надіслати" disabled>{send_icon}</button>'
    else:
        send = f'<a class="composer__send{se}" href="#" aria-label="Надіслати">{send_icon}</a>'
    return (f'<form class="composer"><label class="sr-only" for="{i}">Повідомлення Ірині</label>'
            f'<textarea class="composer__input{ie}" id="{i}" rows="1"{ph}>{text}</textarea>{send}</form>')


# ── Обгортки сцен (класи docs.css) ──
def stage(inner, mod=""):
    m = "".join(f" doc-stage--{x}" for x in mod.split()) if mod else ""
    return f'<div class="doc-stage{m}">{inner}</div>'


def screen(inner, mod=""):
    """Сцена-екран: fixed-пояси (меню, панель дії, шторка, поле чату) прив'язані до неї. mod: bar | tall."""
    m = f" doc-screen--{mod}" if mod else ""
    return f'<div class="doc-screen{m}">{inner}</div>'


def photo_frame(inner):
    """Фото 4:3 з шапкою поверх нього, без статус-бару мокапа."""
    return f'<div class="doc-stage doc-stage--flush doc-frame"><img class="doc-photo" src="{V}room-lukianivska-bedroom.jpg" alt="">{inner}</div>'


# ── Три ширини (урок 10) ──
# Адаптив у системі — медіазапити на --bp-tablet / --bp-desktop. Медіазапит бачить
# ширину вікна, тож рамка-div на сторінці доків її не імітує: кожна ширина — iframe
# справжньої ширини з тією самою розміткою, зменшений у docs.css (.doc-widths).
# Тема — як у найближчого предка з data-theme (панелі «Світла / Темна» у станах)
# або як у самої сторінки доків; перемикач теми підхоплюється наживо.
_FRAME_THEME = ('(function(){try{var f=frameElement,r=parent.document.documentElement,h=document.documentElement;'
                'function s(){var t=f.parentElement.closest("[data-theme]");'
                'if(t&&t.getAttribute("data-theme")==="dark")h.setAttribute("data-theme","dark");else h.removeAttribute("data-theme")}'
                's();new MutationObserver(s).observe(r,{attributes:true,attributeFilter:["data-theme"]})}catch(e){}})()')
WIDTHS = (("phone", "телефон · 390"), ("tablet", "планшет · від <code>--bp-tablet</code> 48rem"),
          ("desktop", "десктоп · від <code>--bp-desktop</code> 72rem"))


def frame(inner, body="shell", title="Приклад"):
    """Iframe із цілою сторінкою: body.{body} > inner, стилі системи + docs.css (імітація станів)."""
    doc = ('<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8">'
           '<link rel="stylesheet" href="../index.css"><link rel="stylesheet" href="docs.css">'
           '<script src="https://cdn.jsdelivr.net/npm/iconify-icon@2.1.0/dist/iconify-icon.min.js"></script>'
           f'<script>{_FRAME_THEME}</script></head><body class="{body}">{inner}</body></html>')
    return f'<iframe title="{title}" loading="lazy" srcdoc="{_html.escape(doc, quote=True)}"></iframe>'


def widths(inner, body="shell", mod="", title="Приклад"):
    """Та сама розмітка на трьох ширинах поруч. mod: bar (низька сцена) | feed (стрічка)."""
    m = f" doc-widths--{mod}" if mod else ""
    out = "".join(f'<figure class="doc-width doc-width--{w}"><div class="doc-width__view" inert>{frame(inner, body, f"{title}: {_re.sub('<[^>]+>', '', cap)}")}</div>'
                  f'<figcaption>{cap}</figcaption></figure>' for w, cap in WIDTHS)
    return f'<div class="doc-widths{m}">{out}</div>'


def desk(inner, body="shell shell--tabbar", title="Приклад: десктоп"):
    """Смуга десктопа в натуральну величину: iframe 72rem, видно лівий край (меню, шапка)."""
    return f'<div class="doc-desk" inert>{frame(inner, body, title)}</div>'

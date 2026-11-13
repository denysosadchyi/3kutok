"""Блок «5. Стани» для кожної сторінки компонента (урок 9).

Стан показано нерухомо класами .is-hover / .is-active / .is-focus з
docs.css — вони дзеркалять :hover, :active, :focus-visible. Вимкнене —
не імітація: справжній disabled, тож працює саме правило components/base.css. Живий компонент
поруч реагує по-справжньому: наведи, натисни, пройди Tab.
"""
import re

from _pages_shell import chat_rows, close, current_card

from _kit import (back, button, card_list, chat_context, chip, composer, field, more,
                  listing_card, person_row, tabbar, topbar_photo, screen, photo_frame, desk)


def _on(html, cls, marker):
    """Додати клас стану до першого елемента з класом marker."""
    return html.replace(f'class="{marker}', f'class="{marker} {cls}', 1)


def _tab_hover():
    """«Чати» під курсором: друга вкладка (перша — поточний «Пошук»)."""
    a, b = tabbar("search").split('class="tabbar__item" href="#">', 1)
    return a + 'class="tabbar__item is-hover" href="#">' + b


def _tab(state):
    """«Чати» у стані state (is-hover / is-active / is-focus); «Пошук» — поточний."""
    a, b = tabbar("search").split('class="tabbar__item" href="#">', 1)
    return a + f'class="tabbar__item {state}" href="#">' + b


def _tab_active():
    return _tab("is-active")


def _rows(html):
    return f'<ul class="group">{html}</ul>'


# slug → (вступ, [(підпис, html)]). Порожній список — компонент не інтерактивний.
STATES = {
    "button": ("Фон міняється, розмір і положення — ні (до уроку 9 натискання стискало кнопку на 0.98 — прибрано).", [
        ("primary · спокій", button()),
        ("primary · наведення", button(extra="is-hover")),
        ("primary · натискання", button(extra="is-active")),
        ("primary · фокус з клавіатури", button(extra="is-focus")),
        ("primary · вимкнена", button(extra="is-disabled")),
        ("secondary · наведення", button("Назад до оголошення", "secondary", "is-hover")),
        ("secondary · натискання", button("Назад до оголошення", "secondary", "is-active")),
        ("secondary · вимкнена", button("Назад до оголошення", "secondary", "is-disabled")),
        ("text · наведення = натискання", button("Скасувати", "text", "is-hover")),
        ("text · фокус", button("Скасувати", "text", "is-focus")),
    ]),
    "chip": ("Стани є лише в чипа-кнопки (summary, button, a) — на екранах це «Фільтри · N», що відкриває шторку. Чип-значення (span) лише показує вибране й станів не має; вимкненого чипа в продукті немає.", [
        ("кнопка · спокій", chip("Шевченківський", tag="button")),
        ("кнопка · наведення", chip("Шевченківський", tag="button", extra="is-hover")),
        ("кнопка · натискання", chip("Шевченківський", tag="button", extra="is-active")),
        ("кнопка · фокус", chip("Шевченківський", tag="button", extra="is-focus")),
        ("вибраний «Фільтри · N» — уже стан, не міняється", chip(selected=True)),
    ]),
    "field": ("Під курсором темнішає рамка; фокус — зелене кільце; вимкнене поле глушиться прозорістю.", [
        ("спокій", field()),
        ("наведення", field(extra="is-hover")),
        ("фокус", field(extra="is-focus")),
        ("вимкнене", field("number", "is-disabled")),
    ]),
    "composer": ("Поле — як <code>.input</code>; кнопка «Надіслати» — як головна дія. Порожнє поле вимикає кнопку: прозорість, без курсора.", [
        ("поле · наведення", composer(input_extra="is-hover")),
        ("поле · фокус", composer(input_extra="is-focus")),
        ("надіслати · наведення", composer("Субота о 13:00 підходить", send_extra="is-hover")),
        ("надіслати · натискання", composer("Субота о 13:00 підходить", send_extra="is-active")),
        ("надіслати · фокус", composer("Субота о 13:00 підходить", send_extra="is-focus")),
        ("надіслати · вимкнена (порожнє поле)", composer(disabled=True)),
    ]),
    "topbar": ("Іконки без фону отримують підложку-коло; на фото — густіше затемнення.", [
        ("назад · наведення", f'<header class="topbar">{_on(back(), "is-hover", "topbar__back")}<p class="topbar__title">Профіль Ірини</p>{more()}</header>'),
        ("меню · натискання", f'<header class="topbar">{back()}<p class="topbar__title">Профіль Ірини</p>{_on(more(), "is-active", "topbar__action")}</header>'),
        ("назад · фокус", f'<header class="topbar">{_on(back(), "is-focus", "topbar__back")}<p class="topbar__title">Профіль Ірини</p>{more()}</header>'),
    ]),
    "tabbar": ("Неактивна вкладка під курсором темнішає до основного тексту; під пальцем капсула іконки отримує підложку; фокус з клавіатури — кільце. "
               "Підйом вкладки — розкладка, а не стан. На десктопі (від <code>--bp-desktop</code>) меню — шапка вгорі, а стани ті самі правила: "
               "змінюється лише розкладка, тож кільце фокусу йде по капсулі пункту.", [
        ("«Чати» під курсором", screen(_tab_hover(), "bar"), "phone"),
        ("«Чати» під пальцем", screen(_tab_active(), "bar"), "phone"),
        ("«Чати» · фокус з клавіатури", screen(_tab("is-focus"), "bar"), "phone"),
        ("десктоп · «Пошук» поточний, «Чати» під курсором", desk(_tab("is-hover")), "desk"),
        ("десктоп · «Чати» під пальцем", desk(_tab("is-active")), "desk"),
        ("десктоп · «Чати» · фокус з клавіатури", desk(_tab("is-focus")), "desk"),
    ]),
    "listing-card": ("Уся картка — одна ціль: під курсором заголовок стає кораловим, фокус обводить картку цілком.", [
        ("наведення / натискання", card_list(listing_card(link_cls="is-hover"))),
        ("фокус", card_list(listing_card(link_cls="is-focus"))),
    ]),
    "person-row": ("Рядок-посилання на картці під курсором і пальцем отримує темнішу підложку.", [
        ("спокій", _rows(person_row())),
        ("наведення / натискання", _rows(person_row("is-hover"))),
        ("фокус", _rows(person_row("is-focus"))),
    ]),
    "chat-context": ("Картка кімнати над чатом — посилання: під курсором фон темнішає.", [
        ("спокій", chat_context()),
        ("наведення / натискання", chat_context("is-hover")),
        ("фокус", chat_context("is-focus")),
    ]),
    "sheet": ("Шторка сама станів не має: їх дають її частини — чип-тригер (див. «Чип»), поля (див. «Поле») і «Скасувати» (див. «Кнопка», text).", []),
    "actionbar": ("Пояс станів не має; кнопка в ньому — <code>.button--primary</code> з усіма станами кнопки.", [
        ("кнопка · наведення", f'<div class="actionbar">{button(extra="button--block is-hover")}</div>'),
        ("кнопка · натискання", f'<div class="actionbar">{button(extra="button--block is-active")}</div>'),
    ]),
    "state": ("Екран стану не інтерактивний; дії в ньому — кнопки з їхніми станами (див. «Кнопка»).", []),
    "split": ("Сам спліт станів не має — їх мають вибраний елемент переліку і ×. Вибране — не наведення: <code>aria-current=\"page\"</code> тримає кільце "
              "<code>--color-current</code>, поки деталь відкрита; наведення на інший рядок лише темнить підложку.", [
        ("вибраний чат", chat_rows(0)),
        ("вибраний чат, під курсором — інший", chat_rows(0, state=(1, "is-hover"))),
        ("інший чат · фокус з клавіатури", chat_rows(0, state=(2, "is-focus"))),
        ("вибрана картка стрічки", card_list(current_card(listing_card()))),
        ("× · наведення", f'<header class="topbar">{back("Назад до чатів")}<p class="topbar__title">Ірина</p>{close(cls="is-hover")}</header>'),
        ("× · фокус з клавіатури", f'<header class="topbar">{back("Назад до чатів")}<p class="topbar__title">Ірина</p>{close(cls="is-focus")}</header>'),
    ]),
    "hero-photo": ("Фото станів не має; кнопки над ним — <code>.topbar--over-photo</code>: під курсором і пальцем затемнення густішає.", [
        ("назад · наведення", photo_frame(_on(topbar_photo(), "is-hover", "topbar__back")), "phone"),
    ]),
}

NONE = "Компонент не інтерактивний — наведення, натискання й фокусу не має. Завантаження показано у варіантах (скелет), вимкненого стану немає."


def _dark_ids(html):
    """Друга копія для темної панелі: id і for не мають повторюватись."""
    return re.sub(r'\b(id|for)="([^"]+)"', r'\1="\2-dark"', html)


def block(slug, variants):
    lead, items = STATES.get(slug, (NONE, []))
    common = ("Правила для всіх компонентів такі. Наведення й натискання міняють лише фон, колір або рамку. "
              "Фон кнопки, чипа, «Надіслати», шапки й капсули меню проступає шаром за <code>--dur-fast</code> (розділ «Рух»). "
              "Фокус з клавіатури — кільце <code>--color-focus</code> (AA в обох темах).</p><p class=\"doc-sources\">"
              "Вимкнене — <code>--opacity-disabled</code> і без курсора. Кнопку й поле вимикає атрибут <code>disabled</code> (поза Tab). "
              "Вимкнене посилання — без <code>href</code> з <code>aria-disabled=\"true\"</code>.")
    out = f'<div class="doc-prose"><p>{lead}</p></div>'
    if items:
        light = variants(items)
        dark = _dark_ids(light)
        out += ('<div class="doc-themes">'
                f'<section class="doc-theme" data-theme="light"><p class="doc-theme__label">Світла тема</p>{light}</section>'
                f'<section class="doc-theme" data-theme="dark"><p class="doc-theme__label">Темна тема</p>{dark}</section></div>')
    return out + f'<div class="doc-prose"><p class="doc-sources">{common}</p></div>'

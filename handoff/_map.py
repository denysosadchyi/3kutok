#!/usr/bin/env python3
"""Генерує таблиці в handoff/map.md: екран → елемент → компонент → токени → ключ тексту.

Запуск: python3 handoff/_map.py
Скрипт переписує лише блоки між маркерами `<!-- _map.py:<назва> -->` і
`<!-- /_map.py -->` у map.md. Прозу між блоками редагуємо в map.md руками.

Звідки дані:
- елементи екранів — список ROWS нижче (екран, стан, зона, елемент, класи, ключ);
- які токени читає елемент — скрипт парсить design-system/components/*.css і
  wireframes/screens.css: правило належить елементу, якщо клас-суб'єкт селектора є
  серед класів елемента, а класи-контекст (предки, :has) є в HTML цього стану;
- залежності токенів — design-system/tokens.css (який токен посилається на який);
- @media (min-width: N) зводиться до --bp-* з тим самим значенням;
- тексти — microcopy.md (ID рядків LS-, L-, P-, C-, O-).

Скрипт також перевіряє карту: кожен клас елемента є в HTML його стану, кожен
клас HTML покритий якимсь елементом, кожен ключ є в microcopy.md. Порушення
друкує й пише в блок «drift».
"""

import html as htmllib
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "handoff" / "map.md"
TOKENS = ROOT / "design-system" / "tokens.css"
COMPONENTS = ROOT / "design-system" / "components"
SCREENS_CSS = ROOT / "wireframes" / "screens.css"
MICROCOPY = ROOT / "microcopy.md"

# ---------------------------------------------------------------- екрани

# Екран → (назва з sitemap.md / _screens.md, {стан: HTML-файл}).
# Кімнати listing-<район>.html і chat-maryna/olia.html — той самий екран з
# іншими даними: у карту не входять.
SCREENS = OrderedDict([
    ("listings", ("Результати пошуку кімнат", OrderedDict([
        ("успіх", "wireframes/listings.html"),
        ("порожній", "wireframes/listings-empty.html"),
        ("помилка", "wireframes/listings-error.html"),
        ("завантаження", "wireframes/listings-loading.html"),
    ]))),
    ("listing", ("Оголошення про кімнату", OrderedDict([
        ("успіх", "wireframes/listing.html"),
        ("порожній", "wireframes/listing-empty.html"),
        ("помилка", "wireframes/listing-error.html"),
        ("завантаження", "wireframes/listing-loading.html"),
    ]))),
    ("profile", ("Профіль іншої людини", OrderedDict([
        ("успіх", "wireframes/profile.html"),
        ("порожній", "wireframes/profile-empty.html"),
        ("помилка", "wireframes/profile-error.html"),
        ("завантаження", "wireframes/profile-loading.html"),
    ]))),
    ("chat", ("Чат із людиною", OrderedDict([
        ("успіх", "wireframes/chat.html"),
        ("порожній", "wireframes/chat-empty.html"),
        ("помилка", "wireframes/chat-error.html"),
        ("завантаження", "wireframes/chat-loading.html"),
    ]))),
    ("chats", ("Перелік розмов", OrderedDict([
        ("успіх", "wireframes/chats.html"),
        ("порожній", "wireframes/chats-empty.html"),
        ("помилка", "wireframes/chats-error.html"),
        ("завантаження", "wireframes/chats-loading.html"),
    ]))),
    ("report", ("Скарга", OrderedDict([
        ("форма", "design-system/examples/report.html"),
        ("надіслано", "design-system/examples/report-sent.html"),
    ]))),
])

# На ширині екран показує поруч панель іншого екрана (split.css). Її класи
# покриває той екран, рядки не повторюємо.
EMBEDS = {"listing": "listings", "chat": "chats"}

ALL = "усі"

# ---------------------------------------------------------------- елементи

# (екран, стани, зона, елемент, класи, ключ microcopy.md)
# стани: ALL або кортеж станів. Перший клас — головний: за ним скрипт шукає
# файл компонента. Ключ: ID рядків через кому; «—» — тексту немає;
# «!E1» — ключа немає, текст за шаблоном voice.md → Словник, E1;
# «!» — ключа немає, шаблону в Словнику теж немає.
ROWS = [
    # ── Результати пошуку ──
    ("listings", ALL, "Каркас", "Оболонка сторінки", "shell shell--tabbar shell--split shell__main", "—"),
    ("listings", ALL, "Каркас", "Спліт: перелік на всю ширину", "split split--solo split__pane split__pane--list", "!"),
    ("listings", ALL, "Каркас", "Нижнє меню", "tabbar tabbar__list tabbar__item", "O-02, O-03, O-04"),
    ("listings", ALL, "Шапка", "Заголовок і підзаголовок", "header header__top header__title header__subtitle", "LS-01; підзаголовок — !"),
    ("listings", ALL, "Шапка", "Кнопка теми", "topbar__action theme-toggle", "!"),
    ("listings", ALL, "Фільтри", "Ряд чипів", "chip-row chip-row__track", "!"),
    ("listings", ALL, "Фільтри", "Чип «Фільтри · 3»", "chip chip--selected", "LS-02"),
    ("listings", ALL, "Фільтри", "Чипи активних умов", "chip", "LS-13"),
    ("listings", ALL, "Шторка фільтрів", "Шторка", "sheet sheet__panel sheet__grabber sheet__head sheet__title sheet__body sheet__foot sr-only", "LS-03, LS-05"),
    ("listings", ALL, "Шторка фільтрів", "Кнопка «Скасувати»", "button button--text", "!"),
    ("listings", ALL, "Шторка фільтрів", "Поле «Район Києва»", "field field__label input", "LS-06, LS-07"),
    ("listings", ALL, "Шторка фільтрів", "Поле «Бюджет до»", "field field__label input", "LS-08"),
    ("listings", ALL, "Шторка фільтрів", "Поле «Дата заїзду»", "field field__label input", "LS-09"),
    ("listings", ALL, "Шторка фільтрів", "Кнопка «Застосувати фільтри»", "button button--primary button--block", "LS-10"),
    ("listings", ("успіх",), "Результати", "Лічильник", "results-meta", "LS-11"),
    ("listings", ("успіх",), "Результати", "Сортування й шторка варіантів", "sort sort-options sheet sheet__panel sheet__grabber sheet__head sheet__title", "!"),
    ("listings", ("успіх",), "Результати", "Кнопка «Скасувати» в шторці сортування", "button button--text", "!"),
    ("listings", ("успіх", "завантаження"), "Результати", "Перелік карток", "card-list", "LS-14"),
    ("listings", ("успіх",), "Результати", "Картка оголошення", "listing-card listing-card__photo listing-card__body listing-card__title listing-card__link listing-card__meta", "LS-18, LS-21, LS-22, LS-23"),
    ("listings", ("успіх",), "Результати", "Бирка ціни на фото", "price-tag", "LS-20"),
    ("listings", ("успіх",), "Результати", "Пігулка автора на фото", "card-author", "!"),
    ("listings", ("успіх",), "Результати", "Аватар автора з позначкою", "avatar avatar__mark sr-only", "!"),
    ("listings", ("успіх",), "Результати", "Кнопка «Показати ще 3»", "button button--secondary button--block", "!"),
    ("listings", ("порожній",), "Результати", "Лічильник «0 оголошень»", "results-meta", "LS-27"),
    ("listings", ("порожній",), "Результати", "Порожній стан", "state state__icon state__title state__text state__actions", "LS-31, LS-32"),
    ("listings", ("порожній",), "Результати", "Кнопка «Змінити фільтри»", "button button--primary", "LS-33"),
    ("listings", ("помилка",), "Результати", "Рядок «Фільтри збережено»", "results-meta", "LS-36"),
    ("listings", ("помилка",), "Результати", "Стан помилки", "state state--error state__icon state__title state__text state__actions", "LS-34, LS-38, LS-39"),
    ("listings", ("помилка",), "Результати", "Кнопка «Спробувати ще»", "button button--primary", "LS-40"),
    ("listings", ("завантаження",), "Результати", "Статус «Завантажуємо оголошення»", "results-meta", "LS-41"),
    ("listings", ("завантаження",), "Результати", "Скелетон картки", "listing-card listing-card__body skeleton skeleton--photo skeleton--title skeleton--line skeleton--w60", "LS-44"),

    # ── Оголошення ──
    ("listing", ALL, "Каркас", "Оболонка сторінки", "shell shell--tabbar shell--split shell__main", "—"),
    ("listing", ("успіх", "завантаження"), "Каркас", "Оболонка: фото під шапкою й нижня панель", "shell shell--actionbar shell--photo-top", "—"),
    ("listing", ALL, "Каркас", "Спліт: стрічка ліворуч, оголошення праворуч", "split split--detail split__pane split__pane--list split__pane--detail", "!"),
    ("listing", ALL, "Каркас", "Нижнє меню", "tabbar tabbar__list tabbar__item", "O-02, O-03, O-04"),
    ("listing", ("успіх", "завантаження"), "Шапка", "Шапка поверх фото", "topbar topbar--over-photo topbar__end", "—"),
    ("listing", ("порожній", "помилка"), "Шапка", "Шапка", "topbar topbar__end", "—"),
    ("listing", ALL, "Шапка", "Кнопка «назад»", "topbar__back", "L-01"),
    ("listing", ("успіх", "завантаження"), "Шапка", "Кнопка ⋯ «Заблокувати чи поскаржитися»", "topbar__action", "C-19"),
    ("listing", ALL, "Шапка", "Кнопка «Закрити оголошення» (лише на ширині)", "topbar__action split__close", "!"),
    ("listing", ALL, "Шапка", "Кнопка теми", "topbar__action theme-toggle", "!"),
    ("listing", ("успіх",), "Кімната", "Головне фото", "hero-photo", "L-03"),
    ("listing", ("успіх",), "Кімната", "Бирка ціни на фото", "price-tag", "L-08"),
    ("listing", ("успіх",), "Кімната", "Лічильник фото «1 / 5»", "photo-count", "!"),
    ("listing", ("успіх",), "Кімната", "Галерея інших фото", "gallery gallery__item", "!"),
    ("listing", ("успіх",), "Кімната", "Назва й район", "listing-title listing-title__name listing-title__meta", "L-05, L-10, L-12"),
    ("listing", ("успіх",), "Кімната", "Умови: співмешканці, квартира, комунальні", "group group__row group__label group__value", "L-13, L-14; «Квартира», «Комунальні» — !"),
    ("listing", ("успіх",), "Кімната", "Опис кімнати", "listing-description", "L-15"),
    ("listing", ("успіх",), "Люди", "Заголовок «Хто живе в квартирі»", "section-title", "L-16"),
    ("listing", ("успіх",), "Люди", "Рядок людини", "group group__row person-row person-row__text person-row__name person-row__caption chevron", "L-18, L-19, L-20"),
    ("listing", ("успіх",), "Люди", "Аватар з позначкою", "avatar avatar--md avatar__mark", "!"),
    ("listing", ("успіх",), "Довіра", "Заголовок «Що підтверджено»", "section-title", "L-21"),
    ("listing", ("успіх",), "Довіра", "Рядок «Номер підтверджено»", "group group__row verified-note verified-note__icon verified-note__text verified-note__title verified-note__limit", "L-23, L-24"),
    ("listing", ("успіх",), "Контакт", "Нижня панель", "actionbar", "—"),
    ("listing", ("успіх",), "Контакт", "Кнопка «Написати Ірині»", "button button--primary", "L-27"),
    ("listing", ("порожній",), "Стан", "Порожній стан «Оголошення зняли»", "state state__icon state__title state__text state__actions", "L-28, L-29"),
    ("listing", ("порожній",), "Стан", "Кнопка «Назад до результатів»", "button button--primary", "L-30"),
    ("listing", ("помилка",), "Стан", "Стан помилки", "state state--error state__icon state__title state__text state__actions", "L-31, L-32"),
    ("listing", ("помилка",), "Стан", "Кнопка «Спробувати ще»", "button button--primary", "L-33"),
    ("listing", ("помилка",), "Стан", "Кнопка «Назад до результатів»", "button button--secondary", "L-34"),
    ("listing", ("завантаження",), "Стан", "Статус для читача екрана", "sr-only", "L-35"),
    ("listing", ("завантаження",), "Кімната", "Скелетон фото й галереї", "hero-photo gallery gallery__item skeleton", "—"),
    ("listing", ("завантаження",), "Кімната", "Скелетон назви", "listing-title skeleton-stack skeleton skeleton--title skeleton--line skeleton--w40", "—"),
    ("listing", ("завантаження",), "Кімната", "Скелетон умов", "group group__row skeleton skeleton--line skeleton--w60 skeleton--w40", "—"),
    ("listing", ("завантаження",), "Люди", "Скелетон заголовка розділу", "skeleton skeleton--line skeleton--w40 skeleton--section", "—"),
    ("listing", ("завантаження",), "Люди", "Скелетон рядка людини", "group group--padded skeleton-person skeleton-person__text skeleton skeleton--avatar skeleton--line", "—"),
    ("listing", ("завантаження",), "Контакт", "Скелетон кнопки в нижній панелі", "actionbar skeleton skeleton--button", "—"),

    # ── Профіль ──
    ("profile", ALL, "Каркас", "Оболонка сторінки", "shell shell__main", "—"),
    ("profile", ("успіх", "порожній", "завантаження"), "Каркас", "Оболонка: нижня панель", "shell shell--actionbar", "—"),
    ("profile", ALL, "Шапка", "Шапка", "topbar", "—"),
    ("profile", ALL, "Шапка", "Кнопка «назад»", "topbar__back", "P-01"),
    ("profile", ALL, "Шапка", "Заголовок «Профіль Ірини»", "topbar__title", "P-02"),
    ("profile", ("успіх", "порожній"), "Шапка", "Кнопка ⋯ «Заблокувати чи поскаржитися»", "topbar__action topbar__end", "C-19"),
    ("profile", ALL, "Шапка", "Кнопка теми", "topbar__action theme-toggle", "!"),
    ("profile", ("успіх",), "Особа", "Голова профілю", "profile-head profile-head__name profile-head__caption", "P-05, P-07"),
    ("profile", ("порожній",), "Особа", "Голова профілю", "profile-head profile-head__name profile-head__caption", "P-28, P-29"),
    ("profile", ("успіх", "порожній"), "Особа", "Великий аватар з позначкою", "avatar avatar--lg avatar__mark sr-only", "P-03"),
    ("profile", ("успіх", "порожній"), "Побут", "Заголовок «Спосіб життя»", "section-title", "P-08"),
    ("profile", ("успіх",), "Побут", "Поля способу життя", "group group__row group__label group__value", "P-10, P-11, P-12, P-13, P-14, P-15, P-16, P-17, P-18, P-19"),
    ("profile", ("порожній",), "Побут", "Компактний стан «не написала»", "state-note state-note__title state-note__text", "P-30, P-31"),
    ("profile", ("успіх", "порожній"), "Довіра", "Заголовок «Що підтверджено»", "section-title", "P-20"),
    ("profile", ("успіх", "порожній"), "Довіра", "Рядок «Номер підтверджено»", "group group__row verified-note verified-note__icon verified-note__text verified-note__title verified-note__limit", "P-22, P-23"),
    ("profile", ("успіх", "порожній"), "Оголошення", "Заголовок «Оголошення»", "section-title", "!"),
    ("profile", ("успіх", "порожній"), "Оголошення", "Картка оголошення", "card-list listing-card listing-card__photo listing-card__body listing-card__title listing-card__link listing-card__meta", "!"),
    ("profile", ("успіх", "порожній"), "Оголошення", "Бирка ціни на фото", "price-tag", "!"),
    ("profile", ("успіх", "порожній"), "Контакт", "Нижня панель", "actionbar", "—"),
    ("profile", ("успіх", "порожній"), "Контакт", "Кнопка «Написати Ірині»", "button button--primary", "P-26, P-33"),
    ("profile", ("помилка",), "Стан", "Стан помилки", "state state--error state__icon state__title state__text state__actions", "P-34, P-35"),
    ("profile", ("помилка",), "Стан", "Кнопка «Спробувати ще»", "button button--primary", "P-36"),
    ("profile", ("помилка",), "Стан", "Кнопка «Назад до результатів»", "button button--secondary", "P-37"),
    ("profile", ("завантаження",), "Стан", "Статус для читача екрана", "sr-only", "P-38"),
    ("profile", ("завантаження",), "Особа", "Скелетон голови профілю", "profile-head skeleton skeleton--avatar-lg skeleton--title skeleton--line skeleton--w60", "—"),
    ("profile", ("завантаження",), "Побут", "Скелетон полів", "group group__row skeleton skeleton--line skeleton--w60 skeleton--w40", "—"),
    ("profile", ("завантаження",), "Контакт", "Скелетон кнопки в нижній панелі", "actionbar skeleton skeleton--button", "—"),

    # ── Чат ──
    ("chat", ALL, "Каркас", "Оболонка сторінки", "shell shell--tabbar shell--composer shell--split shell__main", "—"),
    ("chat", ALL, "Каркас", "Спліт: чати ліворуч від ширини планшета", "split split--tablet split--detail split__pane split__pane--list split__pane--detail", "!"),
    ("chat", ALL, "Каркас", "Нижнє меню", "tabbar tabbar__list tabbar__item", "O-02, O-03, O-04"),
    ("chat", ALL, "Шапка", "Шапка з людиною", "topbar topbar--person topbar__end", "C-02"),
    ("chat", ALL, "Шапка", "Кнопка «назад»", "topbar__back", "C-01"),
    ("chat", ALL, "Шапка", "Людина: аватар, ім'я, щит перевірки", "topbar__person topbar__name topbar__verified avatar", "!"),
    ("chat", ALL, "Шапка", "Кнопка ⋯ «Заблокувати чи поскаржитися»", "topbar__action", "C-19"),
    ("chat", ALL, "Шапка", "Кнопка «Закрити чат» (лише на ширині)", "topbar__action split__close", "!"),
    ("chat", ALL, "Шапка", "Кнопка теми", "topbar__action theme-toggle", "!"),
    ("chat", ALL, "Контекст", "Кімната, про яку чат", "chat-context chat-context__thumb chat-context__text chat-context__title chat-context__meta chevron", "C-03, C-05, C-06"),
    ("chat", ("успіх",), "Історія", "Розділювач дня", "chat-day", "!"),
    ("chat", ("успіх",), "Історія", "Повідомлення", "messages bubble bubble--mine bubble__time", "C-09, C-10, C-11, C-12, C-13"),
    ("chat", ALL, "Нове повідомлення", "Поле й кнопка «Надіслати»", "composer composer__input composer__send", "C-15, C-17"),
    ("chat", ("порожній",), "Історія", "Порожній стан", "state state__icon state__title state__text", "C-22, C-23"),
    ("chat", ("порожній",), "Нове повідомлення", "Чернетка першого повідомлення", "composer composer__input", "C-25"),
    ("chat", ("помилка",), "Історія", "Стан помилки", "state state--error state__icon state__title state__text state__actions", "C-28, C-29"),
    ("chat", ("помилка",), "Історія", "Кнопка «Спробувати ще»", "button button--primary", "C-30"),
    ("chat", ("помилка",), "Історія", "Кнопка «Назад до результатів»", "button button--secondary", "C-31"),
    ("chat", ("завантаження",), "Історія", "Статус для читача екрана", "sr-only", "C-32"),
    ("chat", ("завантаження",), "Історія", "Скелетон повідомлень", "skeleton-stack skeleton skeleton--bubble skeleton--mine skeleton--bubble-tall skeleton--bubble-short", "—"),

    # ── Перелік розмов ──
    ("chats", ALL, "Каркас", "Оболонка сторінки", "shell shell--tabbar shell--split shell__main", "—"),
    ("chats", ("успіх",), "Каркас", "Спліт: перелік і порожня права панель", "split split--tablet split__pane split__pane--list split__pane--detail", "!"),
    ("chats", ("порожній", "помилка", "завантаження"), "Каркас", "Спліт: перелік на всю ширину", "split split--tablet split--solo split__pane split__pane--list", "!"),
    ("chats", ALL, "Каркас", "Нижнє меню", "tabbar tabbar__list tabbar__item", "O-02, O-03, O-04"),
    ("chats", ALL, "Шапка", "Заголовок «Чати»", "header header__top header__title", "!"),
    ("chats", ALL, "Шапка", "Кнопка теми", "topbar__action theme-toggle", "!"),
    ("chats", ("успіх",), "Перелік", "Рядок чату", "group group__row person-row person-row__text person-row__name person-row__caption chevron", "!"),
    ("chats", ("успіх",), "Перелік", "Аватар з позначкою", "avatar avatar--md avatar__mark sr-only", "!"),
    ("chats", ("успіх",), "Права панель", "Стан «Обери чат ліворуч» (лише на ширині)", "state state__icon state__title state__text", "!"),
    ("chats", ("порожній",), "Перелік", "Порожній стан", "state state__icon state__title state__text state__actions", "!"),
    ("chats", ("порожній",), "Перелік", "Кнопка «Перейти до пошуку»", "button button--primary", "!"),
    ("chats", ("помилка",), "Перелік", "Стан помилки", "state state--error state__icon state__title state__text state__actions", "!E1"),
    ("chats", ("помилка",), "Перелік", "Кнопка «Спробувати ще»", "button button--primary", "!D6"),
    ("chats", ("завантаження",), "Перелік", "Статус для читача екрана", "sr-only", "!E2"),
    ("chats", ("завантаження",), "Перелік", "Скелетон рядків", "group group__row skeleton-person skeleton-person__text skeleton skeleton--avatar skeleton--line skeleton--w40 skeleton--w60", "—"),

    # ── Скарга ──
    ("report", ALL, "Каркас", "Оболонка сторінки", "shell shell__main", "—"),
    ("report", ("форма",), "Каркас", "Оболонка: нижня панель", "shell shell--actionbar", "—"),
    ("report", ALL, "Шапка", "Шапка", "topbar", "—"),
    ("report", ALL, "Шапка", "Кнопка «Назад до чату»", "topbar__back", "!D1"),
    ("report", ("форма",), "Шапка", "Заголовок «Скарга на Ірину»", "topbar__title", "!"),
    ("report", ALL, "Шапка", "Кнопка теми", "topbar__action theme-toggle", "!"),
    ("report", ("форма",), "Про кого", "Рядок людини (без переходу)", "group group__row person-row person-row__text person-row__name person-row__caption", "!"),
    ("report", ("форма",), "Про кого", "Аватар", "avatar avatar--md", "!"),
    ("report", ("форма",), "Причина", "Заголовок «Що сталося?»", "section-title", "!"),
    ("report", ("форма",), "Причина", "Варіанти причини (радіо в рядках)", "group group__row", "!"),
    ("report", ("форма",), "Причина", "Поле «Що саме сталося»", "field field__label input", "!"),
    ("report", ("форма",), "Причина", "Підказка під полем", "muted", "!"),
    ("report", ("форма",), "Що далі", "Заголовок «Що буде далі»", "section-title", "!"),
    ("report", ("форма",), "Що далі", "Пояснення", "muted", "!"),
    ("report", ("форма",), "Що далі", "Кнопка «Заблокувати Ірину»", "button button--secondary button--block", "!D8"),
    ("report", ("форма",), "Дія", "Нижня панель", "actionbar", "—"),
    ("report", ("форма",), "Дія", "Кнопка «Надіслати скаргу»", "button button--primary", "!D5"),
    ("report", ("надіслано",), "Стан", "Стан успіху «Скаргу прийнято»", "state state__icon state__title state__text state__actions", "!"),
    ("report", ("надіслано",), "Стан", "Кнопка «Назад до чату»", "button button--primary", "!D1"),
    ("report", ("надіслано",), "Стан", "Кнопка «Заблокувати Ірину»", "button button--secondary", "!D8"),
]

# Класи без стилів: JS-гачки й позначки (design-system/_gate.py → JS_HOOKS).
NO_STYLE = {"status-dark"}

# ---------------------------------------------------------------- токени


def strip_comments(text):
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def read_tokens():
    """Повертає (порядок, рівень, залежності, значення --bp-*)."""
    text = strip_comments(TOKENS.read_text(encoding="utf-8"))
    order, deps, bp = [], defaultdict(set), {}
    for name, value in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", text):
        if name not in order:
            order.append(name)
        deps[name] |= set(re.findall(r"var\(\s*(--[\w-]+)", value))
        if name.startswith("--bp-"):
            bp[value.strip()] = name
    return order, deps, bp


def level(token):
    return "semantic" if re.match(r"--(color|dur|ease|move)-", token) else "primitive"


# ---------------------------------------------------------------- CSS


def css_rules(path):
    """Правила файла: (селектор, декларації, медіа-умова)."""
    text = strip_comments(path.read_text(encoding="utf-8"))
    out = []

    def walk(s, media):
        i = 0
        while i < len(s):
            j = s.find("{", i)
            if j < 0:
                return
            head = s[i:j].strip()
            depth, k = 1, j + 1
            while depth and k < len(s):
                depth += {"{": 1, "}": -1}.get(s[k], 0)
                k += 1
            body = s[j + 1:k - 1]
            if head.startswith("@media") or head.startswith("@supports"):
                walk(body, (media + " " + head).strip())
            elif head.startswith("@"):
                pass  # @keyframes, @font-face
            else:
                out.append((head, body, media))
            i = k

    walk(text, "")
    return out


def split_top(s, seps):
    """Ділить рядок за роздільниками поза дужками."""
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if depth == 0 and ch in seps:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def compound_classes(compound):
    """(обов'язкові класи, класи-альтернативи з :is/:where, контекст з :has)."""
    c = compound
    has = []
    for m in re.finditer(r":has\(([^()]*)\)", c):
        has += re.findall(r"\.([a-zA-Z][\w-]*)", m.group(1))
    c = re.sub(r":(not|has)\((?:[^()]|\([^()]*\))*\)", "", c)
    alts = []
    for m in re.finditer(r":(?:is|where)\(([^()]*)\)", c):
        alts += re.findall(r"\.([a-zA-Z][\w-]*)", m.group(1))
    c = re.sub(r":(is|where)\((?:[^()]|\([^()]*\))*\)", "", c)
    req = re.findall(r"\.([a-zA-Z][\w-]*)", c)
    return req, alts, has


def parse_selector(sel):
    compounds = [p for p in re.split(r"\s*[>+~]\s*|\s+", sel.strip()) if p]
    # re.split ламає :is(.a, .b) з пробілами — збираємо назад за дужками
    merged, buf = [], ""
    for p in compounds:
        buf = (buf + " " + p).strip() if buf else p
        if buf.count("(") == buf.count(")"):
            merged.append(buf)
            buf = ""
    if buf:
        merged.append(buf)
    subject = merged[-1]
    ancestors = merged[:-1]
    s_req, s_alts, s_has = compound_classes(subject)
    ctx, ctx_alts = list(s_has), []
    for a in ancestors:
        r, al, h = compound_classes(a)
        ctx += r + h
        if al:
            ctx_alts.append(al)
    return s_req, s_alts, ctx, ctx_alts


def load_css():
    files = sorted(COMPONENTS.glob("*.css"))
    files = [f for f in files if f.name != "index.css"] + [SCREENS_CSS]
    rules = []
    for f in files:
        for sel_list, body, media in css_rules(f):
            tokens = set(re.findall(r"var\(\s*(--[\w-]+)", body))
            for sel in split_top(sel_list, ","):
                s_req, s_alts, ctx, ctx_alts = parse_selector(sel)
                rules.append(dict(file=f, sel=sel, req=s_req, alts=s_alts, ctx=ctx,
                                  ctx_alts=ctx_alts, tokens=tokens, media=media))
    return files, rules


def html_classes(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    out = set()
    for m in re.findall(r'class="([^"]*)"', text):
        out |= set(m.split())
    return out


def html_text(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S)
    attrs = " ".join(re.findall(r'(?:aria-label|alt|placeholder|title)="([^"]*)"', text))
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return norm(htmllib.unescape(text + " " + attrs))


def norm(s):
    s = s.replace("’", "'").replace("ʼ", "'").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- microcopy


def read_microcopy():
    rows = {}
    for line in MICROCOPY.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| ([A-Z]+-\d+) \|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows[cells[0]] = dict(screen=cells[1], zone=cells[2], was=cells[3], now=cells[4],
                              kind=cells[5], marks=cells[6] if len(cells) > 6 else "")
    return rows


def microcopy_target(row):
    """Текст, який має стояти на екрані за microcopy.md, або None."""
    now, was = row["now"], row["was"]
    if row["kind"] == "дані" or "КОРИСТУВАЧ" in row["marks"] or "👤" in now or "P2" in now or "P1" in now or "P4" in now:
        return None
    m = re.search(r"\*\*(.+?)\*\*", now)
    if m:
        return None if m.group(1).startswith("[") else m.group(1)
    if now.startswith("без змін"):
        return was
    return None


# ---------------------------------------------------------------- збірка


def fam(cls):
    return re.split(r"__|--", cls)[0]


def match_rule(rule, row_classes, page_classes):
    """Чи стилізує правило елемент з класами row_classes на сторінці page_classes."""
    subj = rule["req"] + rule["alts"]
    if not subj:
        return False
    if rule["req"]:
        if not any(c in row_classes for c in rule["req"]):
            return False
        for c in rule["req"]:
            if c in row_classes:
                continue
            # інший клас того ж елемента: має бути на цьому елементі
            if fam(c) in {fam(r) for r in row_classes}:
                return False
            if c not in page_classes:
                return False
        if rule["alts"] and not any(a in row_classes or a in page_classes for a in rule["alts"]):
            return False
    else:
        if not any(a in row_classes for a in rule["alts"]):
            return False
    if any(c not in page_classes for c in rule["ctx"]):
        return False
    for alts in rule["ctx_alts"]:
        if not any(a in page_classes for a in alts):
            return False
    return True


def main():
    order, deps, bp = read_tokens()
    known = set(order)
    files, rules = load_css()
    mc = read_microcopy()

    primary_file = {}
    for r in rules:
        for c in r["req"]:
            if not r["ctx"] and len(r["req"]) == 1:
                primary_file.setdefault(c, r["file"])
    for f in files:  # файл з назвою блока має перевагу
        if f.stem in primary_file or f.stem in {c for r in rules for c in r["req"]}:
            primary_file[f.stem] = f if f != SCREENS_CSS else primary_file.get(f.stem, f)

    page_cls = {}
    for key, (_, states) in SCREENS.items():
        for st, path in states.items():
            page_cls[path] = html_classes(path)

    drift = []
    out_rows = []  # (screen, states, zone, element, comp, extra, tokens, key)
    token_use = defaultdict(lambda: defaultdict(set))  # token → screen → {component}

    for screen, states, zone, element, classes, key in ROWS:
        name, files_by_state = SCREENS[screen]
        st_list = list(files_by_state) if states == ALL else list(states)
        row_cls = classes.split()
        paths = [files_by_state[s] for s in st_list]
        for p in paths:
            for c in row_cls:
                if c not in page_cls[p]:
                    drift.append(f"карта: клас `{c}` елемента «{element}» немає в `{p}`")
        main_cls = row_cls[0]
        comp = primary_file.get(main_cls) or primary_file.get(fam(main_cls))
        toks, extra = set(), set()
        for p in paths:
            for r in rules:
                if match_rule(r, set(row_cls), page_cls[p]):
                    t = {x for x in r["tokens"] if x in known}
                    for w, name_bp in bp.items():
                        if f"min-width: {w}" in r["media"]:
                            t.add(name_bp)
                    if t and r["file"] != comp:
                        extra.add(r["file"])
                    toks |= t
        comp_name = comp.stem if comp else "?"
        for t in toks:
            token_use[t][screen].add(comp_name)
        # ключі
        for k in re.findall(r"\b[A-Z]+-\d+\b", key):
            if k not in mc:
                drift.append(f"карта: ключа {k} немає в `microcopy.md`")
        out_rows.append((screen, st_list, zone, element, comp, sorted(extra, key=lambda f: f.name), toks, key, paths))

    # покриття: кожен клас сторінки має елемент у карті
    for screen, (_, files_by_state) in SCREENS.items():
        for st, p in files_by_state.items():
            covered = set()
            for r in out_rows:
                if r[0] == screen and p in r[8]:
                    covered |= set(next(x for x in ROWS if x[0] == screen and x[3] == r[3] and x[2] == r[2])[4].split())
            if screen in EMBEDS:
                emb = SCREENS[EMBEDS[screen]][1]
                first = list(emb.values())[0]
                for r in ROWS:
                    if r[0] == EMBEDS[screen]:
                        covered |= set(r[4].split())
            for c in sorted(page_cls[p] - covered - NO_STYLE):
                drift.append(f"покриття: клас `{c}` зі `{p}` не має рядка в карті")

    # класи без стилів у системі
    defined = set()
    for r in rules:
        defined |= set(r["req"] + r["alts"] + r["ctx"])
    for p, cls in page_cls.items():
        for c in sorted(cls - defined - NO_STYLE):
            drift.append(f"система: клас `{c}` зі `{p}` не має стилю в `design-system/` чи `screens.css`")

    # тексти: microcopy.md → HTML
    text_drift = []
    seen = set()
    for screen, st_list, zone, element, comp, extra, toks, key, paths in out_rows:
        for k in re.findall(r"\b[A-Z]+-\d+\b", key):
            if k not in mc or (k, screen) in seen:
                continue
            seen.add((k, screen))
            target = microcopy_target(mc[k])
            if not target:
                continue
            body = " ".join(html_text(p) for p in paths)
            pieces = [norm(x).rstrip(".").strip() for x in re.split(r" / | · ", target)]
            missing = [x for x in pieces if x and not x.startswith("—") and x not in body]
            if missing:
                text_drift.append((k, SCREENS[screen][0], target))

    # ------------------------------------------------ рендер
    def link(f):
        return f"[`{f.stem}`](../{f.relative_to(ROOT).as_posix()})"

    def tok_cell(ts):
        sem = [t for t in order if t in ts and level(t) == "semantic"]
        pri = [t for t in order if t in ts and level(t) == "primitive"]
        parts = []
        if sem:
            parts.append("`" + " ".join(sem) + "`")
        if pri:
            parts.append("`" + " ".join(pri) + "`")
        return "<br>".join(parts) if parts else "—"

    def key_cell(key):
        def one(k):
            k = k.strip()
            if k == "—":
                return "—"
            if k == "!":
                return "немає ключа"
            if k.startswith("!"):
                return f"немає ключа; шаблон `voice.md` → Словник, {k[1:]}"
            return k
        if "; " in key:
            a, b = key.split("; ", 1)
            b = re.sub(r"— !(\w*)", lambda m: "— " + one("!" + m.group(1)), b)
            return f"{one(a)}; {b}"
        return one(key)

    forward = []
    for screen, (name, files_by_state) in SCREENS.items():
        forward.append(f"### {name}\n")
        links = " · ".join(f"[{st}](../{p})" for st, p in files_by_state.items())
        forward.append(f"Файли станів: {links}.\n")
        forward.append("| Стан | Зона | Елемент | Компонент | Токени: semantic, потім primitive | Ключ `microcopy.md` |")
        forward.append("|---|---|---|---|---|---|")
        for r in out_rows:
            if r[0] != screen:
                continue
            _, st_list, zone, element, comp, extra, toks, key, _ = r
            st = ALL if st_list == list(files_by_state) else ", ".join(st_list)
            if comp == SCREENS_CSS:
                c = f"{link(comp)} — разовий блок"
            elif comp:
                c = link(comp)
            else:
                c = "?"
            if extra:
                c += " + " + ", ".join(f"`{f.stem}`" for f in extra)
            forward.append(f"| {st} | {zone} | {element} | {c} | {tok_cell(toks)} | {key_cell(key)} |")
        forward.append("")

    # зворотний список: прямий + через токени, що посилаються на цей
    dependents = defaultdict(set)
    for t, ds in deps.items():
        for d in ds:
            dependents[d].add(t)

    def reach(t):
        out, stack = set(), [t]
        while stack:
            x = stack.pop()
            for y in dependents.get(x, ()):
                if y not in out:
                    out.add(y)
                    stack.append(y)
        return out

    short = {k: v[0] for k, v in SCREENS.items()}
    reverse = ["| Токен | Рівень | Читає напряму (компоненти) | Через токени | Екрани |", "|---|---|---|---|---|"]
    unused = []
    count_used = 0
    for t in order:
        direct = token_use.get(t, {})
        via = sorted(x for x in reach(t) if x in token_use)
        screens = set(direct)
        for v in via:
            screens |= set(token_use[v])
        if not screens:
            unused.append(t)
            continue
        count_used += 1
        comps = sorted({c for s in direct.values() for c in s})
        comp_cell = "`" + " ".join(comps) + "`" if comps else "—"
        via_cell = "`" + " ".join(via) + "`" if via else "—"
        scr_cell = ", ".join(short[k] for k in SCREENS if k in screens)
        reverse.append(f"| `{t}` | {level(t)} | {comp_cell} | {via_cell} | {scr_cell} |")

    unused_md = ("Ці токени не стоять на жодному екрані з карти, ні напряму, ні через інший токен:\n\n"
                 + "`" + " ".join(unused) + "`\n") if unused else "Таких токенів немає.\n"

    drift_md = []
    if drift:
        drift_md += [f"- {d}" for d in drift]
    else:
        drift_md.append("- Класи: кожен клас екрана має рядок у карті і стиль у системі.")
    if text_drift:
        drift_md.append("")
        drift_md.append("Текст на екрані не збігається з рядком `microcopy.md` (колонка «Стало», а якщо «без змін» — «Було»):")
        drift_md.append("")
        drift_md.append("| Ключ | Екран | Текст за `microcopy.md` |")
        drift_md.append("|---|---|---|")
        for k, scr, target in text_drift:
            drift_md.append(f"| {k} | {scr} | «{target}» |")

    stats = (f"Екранів: {len(SCREENS)}. Файлів станів: {sum(len(v[1]) for v in SCREENS.values())}. "
             f"Рядків-елементів: {len(out_rows)}. Токенів на екранах: {count_used} з {len(order)}.")

    blocks = {
        "stats": stats + "\n",
        "forward": "\n".join(forward),
        "reverse": "\n".join(reverse) + "\n",
        "unused": unused_md,
        "drift": "\n".join(drift_md) + "\n",
    }

    text = MAP.read_text(encoding="utf-8")
    for name, content in blocks.items():
        pat = re.compile(rf"(<!-- _map\.py:{name} -->\n).*?(<!-- /_map\.py -->)", re.S)
        if not pat.search(text):
            sys.exit(f"map.md: немає маркера <!-- _map.py:{name} -->")
        text = pat.sub(lambda m: m.group(1) + content + m.group(2), text)
    MAP.write_text(text, encoding="utf-8")
    print(stats)
    for d in drift:
        print("DRIFT", d)
    for k, scr, target in text_drift:
        print("TEXT", k, scr, target)


if __name__ == "__main__":
    main()

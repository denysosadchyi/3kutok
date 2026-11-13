# Карта екранів: з чого зібраний кожен екран

Ця карта показує, з яких частин системи зібраний кожен екран продукту.
Один рядок таблиці — один елемент екрана.
У рядку є зона екрана, компонент дизайн-системи, токени цього компонента і ключ тексту в `microcopy.md`.
Унизу є зворотний список: токен → компоненти → екрани.

## Як оновити карту

Таблиці між маркерами `<!-- _map.py:… -->` генерує скрипт [`_map.py`](_map.py).
Не редагуйте ці таблиці руками.

1. Змініть елементи екрана в списку `ROWS` у [`_map.py`](_map.py).
2. Запустіть `python3 handoff/_map.py`.
3. Прочитайте вивід. Рядки `DRIFT` і `TEXT` скрипт також пише в розділ «Розбіжності».

Скрипт не вгадує токени.
Він парсить [`design-system/components/`](../design-system/components/) і [`wireframes/screens.css`](../wireframes/screens.css).
Правило CSS належить елементу, якщо клас селектора є серед класів елемента.
Класи-предки і класи в `:has()` мають бути в HTML цього стану.
Зворотний список скрипт будує з прямої таблиці, тому ці дві таблиці не можуть розійтися.

<!-- _map.py:stats -->
Екранів: 6. Файлів станів: 22. Рядків-елементів: 149. Токенів на екранах: 155 з 163.
<!-- /_map.py -->

## Як читати таблицю

- **Стан** — у яких файлах стану є елемент: успіх, порожній, помилка, завантаження. «усі» — у кожному стані екрана.
- **Компонент** — файл у `design-system/components/`, де є базове правило головного класу. Після «+» стоять інші файли, які додають токени цьому елементу в контексті екрана.
- **разовий блок** — стиль живе у [`wireframes/screens.css`](../wireframes/screens.css), а не в системі. Правило переносу — `CLAUDE.md` → «Внесок у систему».
- **Токени** — спершу semantic (ролі `--color-*`, `--dur-*`, `--ease-*`, `--move-*`), потім primitive, які компонент читає напряму. `--bp-*` означає `@media` з цим breakpoint.
- **Ключ** — ID рядка в [`microcopy.md`](../microcopy.md). «немає ключа» — рядка для тексту немає. «шаблон» — текст відповідає шаблону з [`voice.md`](../voice.md) → «Словник». «—» — у елемента немає тексту.

Значень токенів у карті немає. Значення дивіться в [`design-system/tokens.css`](../design-system/tokens.css).
Тексти інтерфейсу карта цитує лише для того, щоб назвати елемент.

Ми не повторюємо в карті файли `listing-<район>.html` і `chat-maryna.html`, `chat-olia.html`.
Це ті самі екрани з іншими даними.
На ширині планшета чи десктопа екрани «Оголошення про кімнату» і «Чат із людиною» показують ліворуч панель іншого екрана.
Рядки цієї панелі стоять у таблиці «Результати пошуку кімнат» і «Перелік розмов».

## Екрани

<!-- _map.py:forward -->
### Результати пошуку кімнат

Файли станів: [успіх](../wireframes/listings.html) · [порожній](../wireframes/listings-empty.html) · [помилка](../wireframes/listings-error.html) · [завантаження](../wireframes/listings-loading.html).

| Стан | Зона | Елемент | Компонент | Токени: semantic, потім primitive | Ключ `microcopy.md` |
|---|---|---|---|---|---|
| усі | Каркас | Оболонка сторінки | [`shell`](../design-system/components/shell.css) + `split` | `--space-2 --space-3 --space-4 --space-5 --size-48 --size-56 --viewport-height --safe-bottom --bp-desktop` | — |
| усі | Каркас | Спліт: перелік на всю ширину | [`split`](../design-system/components/split.css) | `--color-divider`<br>`--stroke-1 --size-56 --bp-desktop --container-max --col-count-desktop` | немає ключа |
| усі | Каркас | Нижнє меню | [`tabbar`](../design-system/components/tabbar.css) + `split` | `--color-page --color-divider --color-text --color-inactive --color-current`<br>`--weight-medium --weight-bold --text-xs --text-sm --space-1 --space-2 --space-3 --space-4 --radius-round --stroke-1 --size-18 --size-36 --size-56 --safe-bottom --z-1 --z-4 --wave-mask --bp-desktop` | O-02, O-03, O-04 |
| усі | Шапка | Заголовок і підзаголовок | [`header`](../design-system/components/header.css) | `--color-page --color-text-secondary`<br>`--weight-bold --tracking-tight --text-sm --text-xl --leading-1-25 --space-1 --space-4` | LS-01; підзаголовок — немає ключа |
| усі | Шапка | Кнопка теми | [`topbar`](../design-system/components/topbar.css) + `screens` | `--color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--space-2 --radius-round --size-48 --z-minus-1` | немає ключа |
| усі | Фільтри | Ряд чипів | [`chip-row`](../design-system/components/chip-row.css) | `--color-page --color-focus`<br>`--space-1-5 --space-4 --space-6 --stroke-2` | немає ключа |
| усі | Фільтри | Чип «Фільтри · 3» | [`chip`](../design-system/components/chip.css) | `--color-control --color-text --color-current --color-control-hover --color-control-active --color-text-on-current --dur-fast --ease-standard`<br>`--weight-medium --text-sm --space-1 --space-3 --radius-14 --size-36 --z-minus-1` | LS-02 |
| усі | Фільтри | Чипи активних умов | [`chip`](../design-system/components/chip.css) | `--color-control --color-text --color-control-hover --color-control-active --dur-fast --ease-standard`<br>`--weight-medium --text-sm --space-1 --space-3 --radius-14 --size-36 --z-minus-1` | LS-13 |
| усі | Шторка фільтрів | Шторка | [`sheet`](../design-system/components/sheet.css) + `base` | `--color-divider --color-text --color-sheet --color-sheet-scrim --color-grabber --dur-slow --ease-enter`<br>`--weight-bold --text-lg --space-2 --space-3 --space-3-5 --space-4 --radius-3 --radius-18 --stroke-1 --size-5 --size-36 --pct-86 --safe-bottom --z-5 --z-6 --shadow-far` | LS-03, LS-05 |
| усі | Шторка фільтрів | Кнопка «Скасувати» | [`button`](../design-system/components/button.css) | `--color-ghost-hover --color-action-text --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | немає ключа |
| усі | Шторка фільтрів | Поле «Район Києва» | [`field`](../design-system/components/field.css) | `--color-control --color-field-edge --color-text --color-field-edge-hover`<br>`--weight-medium --text-sm --space-1 --space-4 --radius-14 --stroke-1 --size-48` | LS-06, LS-07 |
| усі | Шторка фільтрів | Поле «Бюджет до» | [`field`](../design-system/components/field.css) | `--color-control --color-field-edge --color-text --color-field-edge-hover`<br>`--weight-medium --text-sm --space-1 --space-4 --radius-14 --stroke-1 --size-48` | LS-08 |
| усі | Шторка фільтрів | Поле «Дата заїзду» | [`field`](../design-system/components/field.css) | `--color-control --color-field-edge --color-text --color-field-edge-hover`<br>`--weight-medium --text-sm --space-1 --space-4 --radius-14 --stroke-1 --size-48` | LS-09 |
| усі | Шторка фільтрів | Кнопка «Застосувати фільтри» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | LS-10 |
| успіх | Результати | Лічильник | [`results-meta`](../design-system/components/results-meta.css) | `--color-text-secondary`<br>`--text-sm --space-1 --size-28` | LS-11 |
| успіх | Результати | Сортування й шторка варіантів | [`screens`](../wireframes/screens.css) — разовий блок + `sheet` | `--color-text --color-sheet --color-sheet-scrim --color-ghost-hover --color-ghost-active --color-grabber --dur-slow --ease-enter`<br>`--weight-medium --weight-bold --text-sm --text-lg --space-1 --space-2 --space-4 --space-5 --radius-3 --radius-14 --radius-18 --size-5 --size-36 --size-48 --pct-86 --safe-bottom --z-5 --z-6 --shadow-far` | немає ключа |
| успіх | Результати | Кнопка «Скасувати» в шторці сортування | [`button`](../design-system/components/button.css) | `--color-ghost-hover --color-action-text --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | немає ключа |
| успіх, завантаження | Результати | Перелік карток | [`card-list`](../design-system/components/card-list.css) + `split` | `--bp-tablet --bp-desktop --grid-gap --col-count-tablet --col-count-desktop` | LS-14 |
| успіх | Результати | Картка оголошення | [`listing-card`](../design-system/components/listing-card.css) | `--color-stub --color-text-secondary --color-current --color-focus --color-link-hover`<br>`--weight-medium --text-sm --text-md --leading-1-25 --space-1 --space-2 --radius-18 --stroke-2 --ratio-4-3` | LS-18, LS-21, LS-22, LS-23 |
| успіх | Результати | Бирка ціни на фото | [`price-tag`](../design-system/components/price-tag.css) | `--color-over-photo --color-text --color-tag-hole --color-tag-hole-edge`<br>`--weight-bold --text-md --leading-1-25 --space-2 --space-3 --radius-8 --radius-round --stroke-2 --size-8 --size-10 --size-12 --size-28 --pct-50 --tilt-4 --shadow-near` | LS-20 |
| успіх | Результати | Пігулка автора на фото | [`screens`](../wireframes/screens.css) — разовий блок | `--color-over-photo --color-text`<br>`--weight-medium --text-sm --space-1 --space-2 --space-3 --radius-round --shadow-near` | немає ключа |
| успіх | Результати | Аватар автора з позначкою | [`avatar`](../design-system/components/avatar.css) + `base` | `--color-page --color-verified --color-text-on-verified`<br>`--text-xs --space-1 --radius-round --stroke-1 --stroke-2 --size-16` | немає ключа |
| успіх | Результати | Кнопка «Показати ще 3» | [`button`](../design-system/components/button.css) | `--color-control --color-text --color-control-hover --color-control-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | немає ключа |
| порожній | Результати | Лічильник «0 оголошень» | [`results-meta`](../design-system/components/results-meta.css) | `--color-text-secondary`<br>`--text-sm --space-1 --size-28` | LS-27 |
| порожній | Результати | Порожній стан | [`state`](../design-system/components/state.css) | `--color-text-secondary --color-state-icon --dur-base --ease-enter`<br>`--weight-bold --text-lg --measure-26 --measure-30 --space-2 --space-4 --space-6 --size-72` | LS-31, LS-32 |
| порожній | Результати | Кнопка «Змінити фільтри» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | LS-33 |
| помилка | Результати | Рядок «Фільтри збережено» | [`results-meta`](../design-system/components/results-meta.css) | `--color-text-secondary`<br>`--text-sm --space-1 --size-28` | LS-36 |
| помилка | Результати | Стан помилки | [`state`](../design-system/components/state.css) | `--color-text-secondary --color-error --color-state-icon --dur-base --ease-enter`<br>`--weight-bold --text-lg --measure-26 --measure-30 --space-2 --space-4 --space-6 --size-72` | LS-34, LS-38, LS-39 |
| помилка | Результати | Кнопка «Спробувати ще» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | LS-40 |
| завантаження | Результати | Статус «Завантажуємо оголошення» | [`results-meta`](../design-system/components/results-meta.css) | `--color-text-secondary`<br>`--text-sm --space-1 --size-28` | LS-41 |
| завантаження | Результати | Скелетон картки | [`listing-card`](../design-system/components/listing-card.css) + `skeleton` | `--color-stub --dur-slow --ease-standard`<br>`--space-1 --space-2 --space-3 --space-4 --radius-8 --radius-18 --pct-60 --pct-70 --ratio-4-3` | LS-44 |

### Оголошення про кімнату

Файли станів: [успіх](../wireframes/listing.html) · [порожній](../wireframes/listing-empty.html) · [помилка](../wireframes/listing-error.html) · [завантаження](../wireframes/listing-loading.html).

| Стан | Зона | Елемент | Компонент | Токени: semantic, потім primitive | Ключ `microcopy.md` |
|---|---|---|---|---|---|
| усі | Каркас | Оболонка сторінки | [`shell`](../design-system/components/shell.css) + `split` | `--space-2 --space-3 --space-4 --space-5 --size-48 --size-56 --viewport-height --safe-bottom --bp-desktop` | — |
| успіх, завантаження | Каркас | Оболонка: фото під шапкою й нижня панель | [`shell`](../design-system/components/shell.css) | `--space-3 --size-68 --viewport-height --safe-bottom` | — |
| усі | Каркас | Спліт: стрічка ліворуч, оголошення праворуч | [`split`](../design-system/components/split.css) | `--color-divider`<br>`--stroke-1 --size-56 --bp-desktop --container-max --col-count-desktop` | немає ключа |
| усі | Каркас | Нижнє меню | [`tabbar`](../design-system/components/tabbar.css) + `split` | `--color-page --color-divider --color-text --color-inactive --color-current`<br>`--weight-medium --weight-bold --text-xs --text-sm --space-1 --space-2 --space-3 --space-4 --radius-round --stroke-1 --size-18 --size-36 --size-56 --safe-bottom --z-1 --z-4 --wave-mask --bp-desktop` | O-02, O-03, O-04 |
| успіх, завантаження | Шапка | Шапка поверх фото | [`topbar`](../design-system/components/topbar.css) | `--color-page`<br>`--space-2 --space-3 --size-48 --safe-top --z-3` | — |
| порожній, помилка | Шапка | Шапка | [`topbar`](../design-system/components/topbar.css) | `--color-page`<br>`--space-2 --size-48 --z-3` | — |
| усі | Шапка | Кнопка «назад» | [`topbar`](../design-system/components/topbar.css) + `split` | `--color-over-photo-dim --color-text-on-photo --color-ghost-hover --color-ghost-active --color-over-photo-dim-hover --dur-fast --ease-standard`<br>`--radius-round --stroke-2 --size-8 --size-48 --z-minus-1 --bp-desktop` | L-01 |
| успіх, завантаження | Шапка | Кнопка ⋯ «Заблокувати чи поскаржитися» | [`topbar`](../design-system/components/topbar.css) | `--color-over-photo-dim --color-text-on-photo --color-ghost-hover --color-ghost-active --color-over-photo-dim-hover --dur-fast --ease-standard`<br>`--radius-round --stroke-2 --size-8 --size-48 --z-minus-1` | C-19 |
| усі | Шапка | Кнопка «Закрити оголошення» (лише на ширині) | [`topbar`](../design-system/components/topbar.css) + `split` | `--color-over-photo-dim --color-text-on-photo --color-ghost-hover --color-ghost-active --color-over-photo-dim-hover --dur-fast --ease-standard`<br>`--radius-round --stroke-2 --size-8 --size-48 --z-minus-1 --bp-desktop` | немає ключа |
| усі | Шапка | Кнопка теми | [`topbar`](../design-system/components/topbar.css) + `screens` | `--color-over-photo-dim --color-text-on-photo --color-ghost-hover --color-ghost-active --color-over-photo-dim-hover --dur-fast --ease-standard`<br>`--space-2 --radius-round --stroke-2 --size-8 --size-48 --z-minus-1` | немає ключа |
| успіх | Кімната | Головне фото | [`hero-photo`](../design-system/components/hero-photo.css) | `--space-4` | L-03 |
| успіх | Кімната | Бирка ціни на фото | [`price-tag`](../design-system/components/price-tag.css) + `hero-photo` | `--color-over-photo --color-text --color-tag-hole --color-tag-hole-edge`<br>`--weight-bold --text-md --leading-1-25 --space-2 --space-3 --space-4 --radius-8 --radius-round --stroke-2 --size-8 --size-10 --size-12 --size-28 --pct-50 --tilt-4 --shadow-near` | L-08 |
| успіх | Кімната | Лічильник фото «1 / 5» | [`screens`](../wireframes/screens.css) — разовий блок | `--color-over-photo-dim --color-text-on-photo`<br>`--weight-medium --text-xs --space-1 --space-2 --space-3 --radius-round` | немає ключа |
| успіх | Кімната | Галерея інших фото | [`gallery`](../design-system/components/gallery.css) | `--color-focus`<br>`--space-1 --space-2 --space-4 --stroke-2 --pct-42` | немає ключа |
| успіх | Кімната | Назва й район | [`listing-title`](../design-system/components/listing-title.css) | `--color-text-secondary`<br>`--weight-bold --tracking-tight --text-sm --text-xl --leading-1-25 --space-0-5` | L-05, L-10, L-12 |
| успіх | Кімната | Умови: співмешканці, квартира, комунальні | [`group`](../design-system/components/group.css) | `--color-card --color-divider --color-text-secondary`<br>`--weight-medium --text-sm --space-3 --space-4 --radius-18 --stroke-1 --size-48` | L-13, L-14; «Квартира», «Комунальні» — немає ключа |
| успіх | Кімната | Опис кімнати | [`screens`](../wireframes/screens.css) — разовий блок | `--color-card`<br>`--space-3 --space-4 --radius-18` | L-15 |
| успіх | Люди | Заголовок «Хто живе в квартирі» | [`section-title`](../design-system/components/section-title.css) | `--weight-bold --text-lg --space-4` | L-16 |
| успіх | Люди | Рядок людини | [`group`](../design-system/components/group.css) + `base`, `person-row` | `--color-card --color-divider --color-text-secondary --color-inactive --color-current --color-card-hover`<br>`--weight-bold --text-sm --space-px --space-3 --space-4 --radius-14 --radius-18 --stroke-1 --stroke-2 --size-16 --size-48` | L-18, L-19, L-20 |
| успіх | Люди | Аватар з позначкою | [`avatar`](../design-system/components/avatar.css) | `--color-page --color-verified --color-text-on-verified`<br>`--text-xs --space-1 --radius-round --stroke-2 --size-16` | немає ключа |
| успіх | Довіра | Заголовок «Що підтверджено» | [`section-title`](../design-system/components/section-title.css) | `--weight-bold --text-lg --space-4` | L-21 |
| успіх | Довіра | Рядок «Номер підтверджено» | [`group`](../design-system/components/group.css) + `verified-note` | `--color-card --color-divider --color-text-secondary --color-verified`<br>`--weight-medium --text-sm --leading-1-45 --space-3 --space-4 --radius-18 --stroke-1 --size-24 --size-48` | L-23, L-24 |
| успіх | Контакт | Нижня панель | [`actionbar`](../design-system/components/actionbar.css) + `split` | `--color-page --color-divider`<br>`--space-2 --space-3 --space-4 --stroke-1 --safe-bottom --z-3 --bp-desktop` | — |
| успіх | Контакт | Кнопка «Написати Ірині» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | L-27 |
| порожній | Стан | Порожній стан «Оголошення зняли» | [`state`](../design-system/components/state.css) | `--color-text-secondary --color-state-icon --dur-base --ease-enter`<br>`--weight-bold --text-lg --measure-26 --measure-30 --space-2 --space-4 --space-6 --size-72` | L-28, L-29 |
| порожній | Стан | Кнопка «Назад до результатів» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | L-30 |
| помилка | Стан | Стан помилки | [`state`](../design-system/components/state.css) | `--color-text-secondary --color-error --color-state-icon --dur-base --ease-enter`<br>`--weight-bold --text-lg --measure-26 --measure-30 --space-2 --space-4 --space-6 --size-72` | L-31, L-32 |
| помилка | Стан | Кнопка «Спробувати ще» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | L-33 |
| помилка | Стан | Кнопка «Назад до результатів» | [`button`](../design-system/components/button.css) | `--color-control --color-text --color-control-hover --color-control-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | L-34 |
| завантаження | Стан | Статус для читача екрана | [`base`](../design-system/components/base.css) | `--stroke-1` | L-35 |
| завантаження | Кімната | Скелетон фото й галереї | [`hero-photo`](../design-system/components/hero-photo.css) + `gallery`, `group`, `skeleton` | `--color-stub --color-focus --color-stub-on-card --dur-slow --ease-standard`<br>`--space-1 --space-2 --space-4 --radius-8 --radius-14 --stroke-2 --pct-42 --ratio-4-3 --ratio-4-3-6` | — |
| завантаження | Кімната | Скелетон назви | [`listing-title`](../design-system/components/listing-title.css) + `gallery`, `group`, `hero-photo`, `skeleton` | `--color-stub --color-stub-on-card --dur-slow --ease-standard`<br>`--space-0-5 --space-2 --space-3 --space-4 --radius-8 --radius-14 --pct-40 --pct-70 --ratio-4-3 --ratio-4-3-6` | — |
| завантаження | Кімната | Скелетон умов | [`group`](../design-system/components/group.css) + `gallery`, `hero-photo`, `skeleton` | `--color-card --color-stub --color-divider --color-stub-on-card --dur-slow --ease-standard`<br>`--space-3 --space-4 --radius-8 --radius-14 --radius-18 --stroke-1 --size-48 --pct-40 --pct-60 --ratio-4-3 --ratio-4-3-6` | — |
| завантаження | Люди | Скелетон заголовка розділу | [`skeleton`](../design-system/components/skeleton.css) + `gallery`, `group`, `hero-photo` | `--color-stub --color-stub-on-card --dur-slow --ease-standard`<br>`--space-2 --space-3 --radius-8 --radius-14 --pct-40 --ratio-4-3 --ratio-4-3-6` | — |
| завантаження | Люди | Скелетон рядка людини | [`group`](../design-system/components/group.css) + `gallery`, `hero-photo`, `skeleton` | `--color-card --color-stub --color-stub-on-card --dur-slow --ease-standard`<br>`--space-2 --space-3 --space-4 --radius-8 --radius-14 --radius-18 --radius-round --size-48 --ratio-4-3 --ratio-4-3-6` | — |
| завантаження | Контакт | Скелетон кнопки в нижній панелі | [`actionbar`](../design-system/components/actionbar.css) + `gallery`, `group`, `hero-photo`, `skeleton`, `split` | `--color-page --color-stub --color-divider --color-stub-on-card --dur-slow --ease-standard`<br>`--space-2 --space-3 --space-4 --radius-8 --radius-14 --stroke-1 --size-48 --ratio-4-3 --ratio-4-3-6 --safe-bottom --z-3 --bp-desktop` | — |

### Профіль іншої людини

Файли станів: [успіх](../wireframes/profile.html) · [порожній](../wireframes/profile-empty.html) · [помилка](../wireframes/profile-error.html) · [завантаження](../wireframes/profile-loading.html).

| Стан | Зона | Елемент | Компонент | Токени: semantic, потім primitive | Ключ `microcopy.md` |
|---|---|---|---|---|---|
| усі | Каркас | Оболонка сторінки | [`shell`](../design-system/components/shell.css) | `--space-2 --space-3 --space-4 --space-5 --size-48 --size-56 --viewport-height --safe-bottom` | — |
| успіх, порожній, завантаження | Каркас | Оболонка: нижня панель | [`shell`](../design-system/components/shell.css) | `--space-3 --size-68 --viewport-height --safe-bottom` | — |
| усі | Шапка | Шапка | [`topbar`](../design-system/components/topbar.css) | `--color-page`<br>`--space-2 --size-48 --z-3` | — |
| усі | Шапка | Кнопка «назад» | [`topbar`](../design-system/components/topbar.css) | `--color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--radius-round --size-48 --z-minus-1` | P-01 |
| усі | Шапка | Заголовок «Профіль Ірини» | [`topbar`](../design-system/components/topbar.css) | `--weight-bold --text-md --size-220` | P-02 |
| успіх, порожній | Шапка | Кнопка ⋯ «Заблокувати чи поскаржитися» | [`topbar`](../design-system/components/topbar.css) | `--color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--radius-round --size-48 --z-minus-1` | C-19 |
| усі | Шапка | Кнопка теми | [`topbar`](../design-system/components/topbar.css) | `--color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--radius-round --size-48 --z-minus-1` | немає ключа |
| успіх | Особа | Голова профілю | [`profile-head`](../design-system/components/profile-head.css) | `--color-text-secondary`<br>`--weight-bold --tracking-tight --text-sm --text-xl --space-1 --space-2` | P-05, P-07 |
| порожній | Особа | Голова профілю | [`profile-head`](../design-system/components/profile-head.css) | `--color-text-secondary`<br>`--weight-bold --tracking-tight --text-sm --text-xl --space-1 --space-2` | P-28, P-29 |
| успіх, порожній | Особа | Великий аватар з позначкою | [`avatar`](../design-system/components/avatar.css) + `base`, `profile-head` | `--color-page --color-verified --color-text-on-verified`<br>`--text-xs --space-1 --space-2 --radius-round --stroke-1 --stroke-2 --size-16 --size-24` | P-03 |
| успіх, порожній | Побут | Заголовок «Спосіб життя» | [`section-title`](../design-system/components/section-title.css) | `--weight-bold --text-lg --space-4` | P-08 |
| успіх | Побут | Поля способу життя | [`group`](../design-system/components/group.css) | `--color-card --color-divider --color-text-secondary`<br>`--weight-medium --text-sm --space-3 --space-4 --radius-18 --stroke-1 --size-48` | P-10, P-11, P-12, P-13, P-14, P-15, P-16, P-17, P-18, P-19 |
| порожній | Побут | Компактний стан «не написала» | [`screens`](../wireframes/screens.css) — разовий блок | `--color-card --color-text-secondary`<br>`--weight-bold --text-md --measure-26 --measure-30 --space-2 --space-5 --radius-18` | P-30, P-31 |
| успіх, порожній | Довіра | Заголовок «Що підтверджено» | [`section-title`](../design-system/components/section-title.css) | `--weight-bold --text-lg --space-4` | P-20 |
| успіх, порожній | Довіра | Рядок «Номер підтверджено» | [`group`](../design-system/components/group.css) + `verified-note` | `--color-card --color-divider --color-text-secondary --color-verified`<br>`--weight-medium --text-sm --leading-1-45 --space-3 --space-4 --radius-18 --stroke-1 --size-24 --size-48` | P-22, P-23 |
| успіх, порожній | Оголошення | Заголовок «Оголошення» | [`section-title`](../design-system/components/section-title.css) | `--weight-bold --text-lg --space-4` | немає ключа |
| успіх, порожній | Оголошення | Картка оголошення | [`card-list`](../design-system/components/card-list.css) + `listing-card` | `--color-stub --color-text-secondary --color-current --color-focus --color-link-hover`<br>`--weight-medium --text-sm --text-md --leading-1-25 --space-1 --space-2 --radius-18 --stroke-2 --ratio-4-3 --bp-tablet --bp-desktop --grid-gap --col-count-tablet --col-count-desktop` | немає ключа |
| успіх, порожній | Оголошення | Бирка ціни на фото | [`price-tag`](../design-system/components/price-tag.css) | `--color-over-photo --color-text --color-tag-hole --color-tag-hole-edge`<br>`--weight-bold --text-md --leading-1-25 --space-2 --space-3 --radius-8 --radius-round --stroke-2 --size-8 --size-10 --size-12 --size-28 --pct-50 --tilt-4 --shadow-near` | немає ключа |
| успіх, порожній | Контакт | Нижня панель | [`actionbar`](../design-system/components/actionbar.css) | `--color-page --color-divider`<br>`--space-2 --space-3 --space-4 --stroke-1 --safe-bottom --z-3` | — |
| успіх, порожній | Контакт | Кнопка «Написати Ірині» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | P-26, P-33 |
| помилка | Стан | Стан помилки | [`state`](../design-system/components/state.css) | `--color-text-secondary --color-error --color-state-icon --dur-base --ease-enter`<br>`--weight-bold --text-lg --measure-26 --measure-30 --space-2 --space-4 --space-6 --size-72` | P-34, P-35 |
| помилка | Стан | Кнопка «Спробувати ще» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | P-36 |
| помилка | Стан | Кнопка «Назад до результатів» | [`button`](../design-system/components/button.css) | `--color-control --color-text --color-control-hover --color-control-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | P-37 |
| завантаження | Стан | Статус для читача екрана | [`base`](../design-system/components/base.css) | `--stroke-1` | P-38 |
| завантаження | Особа | Скелетон голови профілю | [`profile-head`](../design-system/components/profile-head.css) + `group`, `skeleton` | `--color-stub --color-stub-on-card --dur-slow --ease-standard`<br>`--space-1 --space-2 --space-3 --space-4 --radius-8 --radius-round --size-84 --pct-60 --pct-70` | — |
| завантаження | Побут | Скелетон полів | [`group`](../design-system/components/group.css) + `skeleton` | `--color-card --color-stub --color-divider --color-stub-on-card --dur-slow --ease-standard`<br>`--space-3 --space-4 --radius-8 --radius-18 --stroke-1 --size-48 --pct-40 --pct-60` | — |
| завантаження | Контакт | Скелетон кнопки в нижній панелі | [`actionbar`](../design-system/components/actionbar.css) + `group`, `skeleton` | `--color-page --color-stub --color-divider --color-stub-on-card --dur-slow --ease-standard`<br>`--space-2 --space-3 --space-4 --radius-8 --radius-14 --stroke-1 --size-48 --safe-bottom --z-3` | — |

### Чат із людиною

Файли станів: [успіх](../wireframes/chat.html) · [порожній](../wireframes/chat-empty.html) · [помилка](../wireframes/chat-error.html) · [завантаження](../wireframes/chat-loading.html).

| Стан | Зона | Елемент | Компонент | Токени: semantic, потім primitive | Ключ `microcopy.md` |
|---|---|---|---|---|---|
| усі | Каркас | Оболонка сторінки | [`shell`](../design-system/components/shell.css) + `split` | `--space-2 --space-3 --space-4 --space-5 --space-6 --size-48 --size-56 --size-76 --viewport-height --safe-bottom --bp-tablet --bp-desktop` | — |
| усі | Каркас | Спліт: чати ліворуч від ширини планшета | [`split`](../design-system/components/split.css) | `--color-divider`<br>`--stroke-1 --size-56 --safe-bottom --bp-tablet --bp-desktop --container-max --col-count-tablet --col-count-desktop` | немає ключа |
| усі | Каркас | Нижнє меню | [`tabbar`](../design-system/components/tabbar.css) + `split` | `--color-page --color-divider --color-text --color-inactive --color-current`<br>`--weight-medium --weight-bold --text-xs --text-sm --space-1 --space-2 --space-3 --space-4 --radius-round --stroke-1 --size-18 --size-36 --size-56 --safe-bottom --z-1 --z-4 --wave-mask --bp-tablet --bp-desktop` | O-02, O-03, O-04 |
| усі | Шапка | Шапка з людиною | [`topbar`](../design-system/components/topbar.css) | `--color-page --color-divider`<br>`--space-2 --stroke-1 --size-48 --z-3` | C-02 |
| усі | Шапка | Кнопка «назад» | [`topbar`](../design-system/components/topbar.css) + `split` | `--color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--radius-round --size-48 --z-minus-1 --bp-tablet --bp-desktop` | C-01 |
| усі | Шапка | Людина: аватар, ім'я, щит перевірки | [`topbar`](../design-system/components/topbar.css) | `--color-verified --color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--weight-bold --text-md --leading-1-25 --space-2 --radius-14 --size-20 --size-48 --z-minus-1` | немає ключа |
| усі | Шапка | Кнопка ⋯ «Заблокувати чи поскаржитися» | [`topbar`](../design-system/components/topbar.css) | `--color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--radius-round --size-48 --z-minus-1` | C-19 |
| усі | Шапка | Кнопка «Закрити чат» (лише на ширині) | [`topbar`](../design-system/components/topbar.css) + `split` | `--color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--radius-round --size-48 --z-minus-1 --bp-tablet --bp-desktop` | немає ключа |
| усі | Шапка | Кнопка теми | [`topbar`](../design-system/components/topbar.css) + `screens` | `--color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--space-2 --radius-round --size-48 --z-minus-1` | немає ключа |
| усі | Контекст | Кімната, про яку чат | [`chat-context`](../design-system/components/chat-context.css) + `base` | `--color-card --color-text-secondary --color-inactive --color-card-hover`<br>`--weight-medium --text-xs --text-sm --space-2 --space-3 --radius-8 --radius-14 --size-16 --size-48` | C-03, C-05, C-06 |
| успіх | Історія | Розділювач дня | [`screens`](../wireframes/screens.css) — разовий блок | `--color-text-secondary`<br>`--text-xs` | немає ключа |
| успіх | Історія | Повідомлення | [`bubble`](../design-system/components/bubble.css) | `--color-card --color-inverted --color-text --color-text-secondary --color-text-on-inverted --color-text-secondary-on-inverted`<br>`--text-xs --space-0-5 --space-1 --space-2 --space-3 --radius-4 --radius-18 --pct-78` | C-09, C-10, C-11, C-12, C-13 |
| усі | Нове повідомлення | Поле й кнопка «Надіслати» | [`composer`](../design-system/components/composer.css) + `split` | `--color-page --color-control --color-divider --color-field-edge --color-text --color-action --color-action-hover --color-text-on-action --color-action-active --color-field-edge-hover --dur-fast --ease-standard`<br>`--leading-1-45 --space-2 --space-3 --space-4 --radius-14 --radius-round --stroke-1 --size-20 --size-48 --size-112 --safe-bottom --z-minus-1 --z-4 --bp-tablet --bp-desktop` | C-15, C-17 |
| порожній | Історія | Порожній стан | [`state`](../design-system/components/state.css) | `--color-text-secondary --color-state-icon --dur-base --ease-enter`<br>`--weight-bold --text-lg --measure-26 --measure-30 --space-2 --space-4 --space-6 --size-72` | C-22, C-23 |
| порожній | Нове повідомлення | Чернетка першого повідомлення | [`composer`](../design-system/components/composer.css) + `split` | `--color-page --color-control --color-divider --color-field-edge --color-text --color-field-edge-hover`<br>`--leading-1-45 --space-2 --space-3 --space-4 --radius-14 --stroke-1 --size-48 --size-112 --safe-bottom --z-4 --bp-tablet --bp-desktop` | C-25 |
| помилка | Історія | Стан помилки | [`state`](../design-system/components/state.css) | `--color-text-secondary --color-error --color-state-icon --dur-base --ease-enter`<br>`--weight-bold --text-lg --measure-26 --measure-30 --space-2 --space-4 --space-6 --size-72` | C-28, C-29 |
| помилка | Історія | Кнопка «Спробувати ще» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | C-30 |
| помилка | Історія | Кнопка «Назад до результатів» | [`button`](../design-system/components/button.css) | `--color-control --color-text --color-control-hover --color-control-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | C-31 |
| завантаження | Історія | Статус для читача екрана | [`base`](../design-system/components/base.css) | `--stroke-1` | C-32 |
| завантаження | Історія | Скелетон повідомлень | [`skeleton`](../design-system/components/skeleton.css) + `group` | `--color-stub --color-stub-on-card --dur-slow --ease-standard`<br>`--space-2 --space-4 --space-6 --space-7 --radius-8 --radius-18 --pct-52 --pct-70 --pct-76` | — |

### Перелік розмов

Файли станів: [успіх](../wireframes/chats.html) · [порожній](../wireframes/chats-empty.html) · [помилка](../wireframes/chats-error.html) · [завантаження](../wireframes/chats-loading.html).

| Стан | Зона | Елемент | Компонент | Токени: semantic, потім primitive | Ключ `microcopy.md` |
|---|---|---|---|---|---|
| усі | Каркас | Оболонка сторінки | [`shell`](../design-system/components/shell.css) + `split` | `--space-2 --space-3 --space-4 --space-5 --size-48 --size-56 --viewport-height --safe-bottom --bp-tablet --bp-desktop` | — |
| успіх | Каркас | Спліт: перелік і порожня права панель | [`split`](../design-system/components/split.css) | `--color-divider`<br>`--stroke-1 --size-56 --safe-bottom --bp-tablet --bp-desktop --container-max --col-count-tablet --col-count-desktop` | немає ключа |
| порожній, помилка, завантаження | Каркас | Спліт: перелік на всю ширину | [`split`](../design-system/components/split.css) | `--color-divider`<br>`--stroke-1 --size-56 --safe-bottom --bp-tablet --bp-desktop --container-max --col-count-tablet --col-count-desktop` | немає ключа |
| усі | Каркас | Нижнє меню | [`tabbar`](../design-system/components/tabbar.css) + `split` | `--color-page --color-divider --color-text --color-inactive --color-current`<br>`--weight-medium --weight-bold --text-xs --text-sm --space-1 --space-2 --space-3 --space-4 --radius-round --stroke-1 --size-18 --size-36 --size-56 --safe-bottom --z-1 --z-4 --wave-mask --bp-tablet --bp-desktop` | O-02, O-03, O-04 |
| усі | Шапка | Заголовок «Чати» | [`header`](../design-system/components/header.css) | `--color-page`<br>`--weight-bold --tracking-tight --text-xl --leading-1-25 --space-1 --space-4` | немає ключа |
| усі | Шапка | Кнопка теми | [`topbar`](../design-system/components/topbar.css) + `screens` | `--color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--space-2 --radius-round --size-48 --z-minus-1` | немає ключа |
| успіх | Перелік | Рядок чату | [`group`](../design-system/components/group.css) + `base`, `person-row` | `--color-card --color-divider --color-text-secondary --color-inactive --color-current --color-card-hover`<br>`--weight-bold --text-sm --space-px --space-3 --space-4 --radius-14 --radius-18 --stroke-1 --stroke-2 --size-16 --size-48` | немає ключа |
| успіх | Перелік | Аватар з позначкою | [`avatar`](../design-system/components/avatar.css) + `base` | `--color-page --color-verified --color-text-on-verified`<br>`--text-xs --space-1 --radius-round --stroke-1 --stroke-2 --size-16` | немає ключа |
| успіх | Права панель | Стан «Обери чат ліворуч» (лише на ширині) | [`state`](../design-system/components/state.css) | `--color-text-secondary --color-state-icon --dur-base --ease-enter`<br>`--weight-bold --text-lg --measure-26 --measure-30 --space-2 --space-4 --space-6 --size-72` | немає ключа |
| порожній | Перелік | Порожній стан | [`state`](../design-system/components/state.css) | `--color-text-secondary --color-state-icon --dur-base --ease-enter`<br>`--weight-bold --text-lg --measure-26 --measure-30 --space-2 --space-4 --space-6 --size-72` | немає ключа |
| порожній | Перелік | Кнопка «Перейти до пошуку» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | немає ключа |
| помилка | Перелік | Стан помилки | [`state`](../design-system/components/state.css) | `--color-text-secondary --color-error --color-state-icon --dur-base --ease-enter`<br>`--weight-bold --text-lg --measure-26 --measure-30 --space-2 --space-4 --space-6 --size-72` | немає ключа; шаблон `voice.md` → Словник, E1 |
| помилка | Перелік | Кнопка «Спробувати ще» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | немає ключа; шаблон `voice.md` → Словник, D6 |
| завантаження | Перелік | Статус для читача екрана | [`base`](../design-system/components/base.css) | `--stroke-1` | немає ключа; шаблон `voice.md` → Словник, E2 |
| завантаження | Перелік | Скелетон рядків | [`group`](../design-system/components/group.css) + `skeleton` | `--color-card --color-stub --color-divider --color-stub-on-card --dur-slow --ease-standard`<br>`--space-2 --space-3 --space-4 --radius-8 --radius-18 --radius-round --stroke-1 --size-48 --pct-40 --pct-60` | — |

### Скарга

Файли станів: [форма](../design-system/examples/report.html) · [надіслано](../design-system/examples/report-sent.html).

| Стан | Зона | Елемент | Компонент | Токени: semantic, потім primitive | Ключ `microcopy.md` |
|---|---|---|---|---|---|
| усі | Каркас | Оболонка сторінки | [`shell`](../design-system/components/shell.css) | `--space-2 --space-3 --space-4 --space-5 --size-48 --size-56 --viewport-height --safe-bottom` | — |
| форма | Каркас | Оболонка: нижня панель | [`shell`](../design-system/components/shell.css) | `--space-3 --size-68 --viewport-height --safe-bottom` | — |
| усі | Шапка | Шапка | [`topbar`](../design-system/components/topbar.css) | `--color-page`<br>`--space-2 --size-48 --z-3` | — |
| усі | Шапка | Кнопка «Назад до чату» | [`topbar`](../design-system/components/topbar.css) | `--color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--radius-round --size-48 --z-minus-1` | немає ключа; шаблон `voice.md` → Словник, D1 |
| форма | Шапка | Заголовок «Скарга на Ірину» | [`topbar`](../design-system/components/topbar.css) | `--weight-bold --text-md --size-220` | немає ключа |
| усі | Шапка | Кнопка теми | [`topbar`](../design-system/components/topbar.css) | `--color-ghost-hover --color-ghost-active --dur-fast --ease-standard`<br>`--radius-round --size-48 --z-minus-1` | немає ключа |
| форма | Про кого | Рядок людини (без переходу) | [`group`](../design-system/components/group.css) + `person-row` | `--color-card --color-divider --color-text-secondary --color-current --color-card-hover`<br>`--weight-bold --text-sm --space-px --space-3 --space-4 --radius-14 --radius-18 --stroke-1 --stroke-2 --size-48` | немає ключа |
| форма | Про кого | Аватар | [`avatar`](../design-system/components/avatar.css) | — | немає ключа |
| форма | Причина | Заголовок «Що сталося?» | [`section-title`](../design-system/components/section-title.css) | `--weight-bold --text-lg --space-4` | немає ключа |
| форма | Причина | Варіанти причини (радіо в рядках) | [`group`](../design-system/components/group.css) | `--color-card --color-divider`<br>`--space-3 --space-4 --radius-18 --stroke-1 --size-48` | немає ключа |
| форма | Причина | Поле «Що саме сталося» | [`field`](../design-system/components/field.css) | `--color-control --color-field-edge --color-text --color-field-edge-hover`<br>`--weight-medium --text-sm --space-1 --space-4 --radius-14 --stroke-1 --size-48` | немає ключа |
| форма | Причина | Підказка під полем | [`base`](../design-system/components/base.css) | `--color-text-secondary` | немає ключа |
| форма | Що далі | Заголовок «Що буде далі» | [`section-title`](../design-system/components/section-title.css) | `--weight-bold --text-lg --space-4` | немає ключа |
| форма | Що далі | Пояснення | [`base`](../design-system/components/base.css) | `--color-text-secondary` | немає ключа |
| форма | Що далі | Кнопка «Заблокувати Ірину» | [`button`](../design-system/components/button.css) | `--color-control --color-text --color-control-hover --color-control-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | немає ключа; шаблон `voice.md` → Словник, D8 |
| форма | Дія | Нижня панель | [`actionbar`](../design-system/components/actionbar.css) | `--color-page --color-divider`<br>`--space-2 --space-3 --space-4 --stroke-1 --safe-bottom --z-3` | — |
| форма | Дія | Кнопка «Надіслати скаргу» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | немає ключа; шаблон `voice.md` → Словник, D5 |
| надіслано | Стан | Стан успіху «Скаргу прийнято» | [`state`](../design-system/components/state.css) | `--color-text-secondary --color-state-icon --dur-base --ease-enter`<br>`--weight-bold --text-lg --measure-26 --measure-30 --space-2 --space-4 --space-6 --size-72` | немає ключа |
| надіслано | Стан | Кнопка «Назад до чату» | [`button`](../design-system/components/button.css) | `--color-action --color-action-hover --color-text-on-action --color-action-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | немає ключа; шаблон `voice.md` → Словник, D1 |
| надіслано | Стан | Кнопка «Заблокувати Ірину» | [`button`](../design-system/components/button.css) | `--color-control --color-text --color-control-hover --color-control-active --dur-fast --dur-slow --ease-standard --ease-enter --ease-exit`<br>`--weight-medium --text-md --space-2 --space-5 --radius-14 --size-48 --pct-50 --z-minus-1` | немає ключа; шаблон `voice.md` → Словник, D8 |
<!-- /_map.py -->

## Зворотний список: токен → екрани

Колонка «Через токени» показує semantic-ролі, які посилаються на цей токен.
Екрани в рядку — це екрани, де є сам токен або одна з цих ролей.
Темна тема міняє тільки semantic-ролі, тому список діє для обох тем.

<!-- _map.py:reverse -->
| Токен | Рівень | Читає напряму (компоненти) | Через токени | Екрани |
|---|---|---|---|---|
| `--white` | primitive | — | `--color-over-photo --color-page --color-sheet --color-text-on-current --color-text-on-inverted --color-text-on-photo --color-text-on-verified` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--grey-50` | primitive | — | `--color-card --color-control --color-ghost-hover --color-grabber --color-state-icon --color-stub --color-tag-hole --color-text` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--grey-100` | primitive | — | `--color-card-hover --color-control-hover --color-divider --color-field-edge-hover --color-ghost-active --color-inverted --color-stub-on-card --color-text-secondary-on-inverted` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--grey-400` | primitive | — | `--color-field-edge --color-grabber --color-inactive --color-tag-hole-edge --color-text-secondary` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--grey-600` | primitive | — | `--color-control-active --color-divider --color-inactive --color-text-secondary --color-text-secondary-on-inverted` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--grey-800` | primitive | — | `--color-control-hover --color-ghost-active --color-stub-on-card` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--grey-900` | primitive | — | `--color-card --color-control --color-ghost-hover --color-over-photo --color-sheet --color-stub` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--ink` | primitive | — | `--color-field-edge-hover --color-inverted --color-state-icon --color-tag-hole-edge --color-text --color-text-on-action --color-text-on-current --color-text-on-inverted --color-text-on-verified` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--coral` | primitive | — | `--color-action` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--coral-deep` | primitive | — | `--color-action-hover` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--coral-dark` | primitive | — | `--color-action-text --color-current --color-link-hover` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--coral-light` | primitive | — | `--color-action-text --color-current --color-link-hover` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--green` | primitive | — | `--color-focus --color-verified` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--green-light` | primitive | — | `--color-focus --color-verified` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--coral-pressed` | primitive | — | `--color-action-active` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--grey-200` | primitive | — | `--color-control-active` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Скарга |
| `--red` | primitive | — | `--color-error` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--black` | primitive | — | `--color-card-hover --color-page --color-tag-hole` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--ink-38` | primitive | — | `--color-sheet-scrim` | Результати пошуку кімнат |
| `--ink-60` | primitive | — | `--color-over-photo-dim --color-sheet-scrim` | Результати пошуку кімнат, Оголошення про кімнату |
| `--ink-80` | primitive | — | `--color-over-photo-dim-hover` | Оголошення про кімнату |
| `--black-12` | primitive | — | `--shadow-far` | Результати пошуку кімнат |
| `--black-14` | primitive | — | `--shadow-near` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--weight-medium` | primitive | `button card-list chat-context chip field group listing-card screens tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--weight-bold` | primitive | `group header listing-title price-tag profile-head screens section-title sheet state tabbar topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--tracking-tight` | primitive | `header listing-title profile-head` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Перелік розмов |
| `--text-xs` | primitive | `avatar bubble chat-context screens tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--text-sm` | primitive | `card-list chat-context chip field group header listing-card listing-title profile-head results-meta screens tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--text-md` | primitive | `button card-list listing-card price-tag screens topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--text-lg` | primitive | `screens section-title sheet state` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--text-xl` | primitive | `header listing-title profile-head` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Перелік розмов |
| `--leading-1-25` | primitive | `card-list header listing-card listing-title price-tag topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--leading-1-45` | primitive | `composer group` | — | Оголошення про кімнату, Профіль іншої людини, Чат із людиною |
| `--measure-26` | primitive | `screens state` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--measure-30` | primitive | `screens state` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--space-px` | primitive | `group` | — | Оголошення про кімнату, Перелік розмов, Скарга |
| `--space-0-5` | primitive | `bubble listing-title` | — | Оголошення про кімнату, Чат із людиною |
| `--space-1` | primitive | `avatar bubble card-list chip field gallery header hero-photo listing-card profile-head results-meta screens tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--space-1-5` | primitive | `chip-row` | — | Результати пошуку кімнат |
| `--space-2` | primitive | `actionbar avatar bubble button card-list chat-context composer gallery group hero-photo listing-card listing-title price-tag profile-head screens sheet shell skeleton state tabbar topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--space-3` | primitive | `actionbar bubble chat-context chip composer group listing-card listing-title price-tag profile-head screens sheet shell skeleton tabbar topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--space-3-5` | primitive | `sheet` | — | Результати пошуку кімнат |
| `--space-4` | primitive | `actionbar chip-row composer field gallery group header hero-photo listing-card listing-title price-tag profile-head screens section-title sheet shell skeleton state tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--space-5` | primitive | `button screens shell` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--space-6` | primitive | `chip-row shell skeleton state` | `--grid-gap` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--space-7` | primitive | `skeleton` | — | Чат із людиною |
| `--radius-3` | primitive | `screens sheet` | — | Результати пошуку кімнат |
| `--radius-4` | primitive | `bubble` | — | Чат із людиною |
| `--radius-8` | primitive | `actionbar chat-context group hero-photo listing-card listing-title price-tag profile-head skeleton` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--radius-14` | primitive | `actionbar button chat-context chip composer field group hero-photo listing-title screens skeleton topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--radius-18` | primitive | `bubble card-list group listing-card screens sheet skeleton` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--radius-round` | primitive | `avatar composer group price-tag profile-head screens tabbar topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--stroke-1` | primitive | `actionbar avatar base composer field group sheet split tabbar topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--stroke-2` | primitive | `avatar card-list chip-row gallery group hero-photo listing-card price-tag topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Перелік розмов, Скарга |
| `--size-5` | primitive | `screens sheet` | — | Результати пошуку кімнат |
| `--size-8` | primitive | `price-tag topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--size-10` | primitive | `price-tag` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--size-12` | primitive | `price-tag` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--size-16` | primitive | `avatar chat-context group` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--size-18` | primitive | `tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Чат із людиною, Перелік розмов |
| `--size-20` | primitive | `composer topbar` | — | Чат із людиною |
| `--size-24` | primitive | `avatar group` | — | Оголошення про кімнату, Профіль іншої людини |
| `--size-28` | primitive | `price-tag results-meta` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--size-36` | primitive | `chip screens sheet tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Чат із людиною, Перелік розмов |
| `--size-48` | primitive | `actionbar button chat-context composer field group screens shell topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--size-56` | primitive | `shell split tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--size-68` | primitive | `shell` | — | Оголошення про кімнату, Профіль іншої людини, Скарга |
| `--size-72` | primitive | `state` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--size-76` | primitive | `shell` | — | Чат із людиною |
| `--size-84` | primitive | `profile-head` | — | Профіль іншої людини |
| `--size-112` | primitive | `composer` | — | Чат із людиною |
| `--size-220` | primitive | `topbar` | — | Профіль іншої людини, Скарга |
| `--pct-40` | primitive | `group listing-title skeleton` | — | Оголошення про кімнату, Профіль іншої людини, Перелік розмов |
| `--pct-42` | primitive | `gallery hero-photo` | — | Оголошення про кімнату |
| `--pct-50` | primitive | `button price-tag` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--pct-52` | primitive | `skeleton` | — | Чат із людиною |
| `--pct-60` | primitive | `group listing-card profile-head` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Перелік розмов |
| `--pct-70` | primitive | `listing-card listing-title profile-head skeleton` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною |
| `--pct-76` | primitive | `skeleton` | — | Чат із людиною |
| `--pct-78` | primitive | `bubble` | — | Чат із людиною |
| `--pct-86` | primitive | `screens sheet` | — | Результати пошуку кімнат |
| `--ratio-4-3` | primitive | `actionbar card-list group hero-photo listing-card listing-title skeleton` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--ratio-4-3-6` | primitive | `actionbar group hero-photo listing-title skeleton` | — | Оголошення про кімнату |
| `--tilt-4` | primitive | `price-tag` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--viewport-height` | primitive | `shell` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--safe-top` | primitive | `topbar` | — | Оголошення про кімнату |
| `--safe-bottom` | primitive | `actionbar composer screens sheet shell split tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--z-minus-1` | primitive | `button chip composer topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--z-1` | primitive | `tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Чат із людиною, Перелік розмов |
| `--z-3` | primitive | `actionbar topbar` | — | Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Скарга |
| `--z-4` | primitive | `composer tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Чат із людиною, Перелік розмов |
| `--z-5` | primitive | `screens sheet` | — | Результати пошуку кімнат |
| `--z-6` | primitive | `screens sheet` | — | Результати пошуку кімнат |
| `--shadow-near` | primitive | `price-tag screens` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--shadow-far` | primitive | `screens sheet` | — | Результати пошуку кімнат |
| `--wave-mask` | primitive | `tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Чат із людиною, Перелік розмов |
| `--duration-120` | primitive | — | `--dur-fast` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--duration-200` | primitive | — | `--dur-base` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--duration-320` | primitive | — | `--dur-slow` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--curve-in-out` | primitive | — | `--ease-standard` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--curve-out` | primitive | — | `--ease-enter` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--curve-in` | primitive | — | `--ease-exit` | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--bp-tablet` | primitive | `card-list composer shell split tabbar topbar` | — | Результати пошуку кімнат, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--bp-desktop` | primitive | `actionbar card-list composer shell split tabbar topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--grid-gap` | primitive | `card-list` | — | Результати пошуку кімнат, Профіль іншої людини |
| `--container-max` | primitive | `split` | — | Результати пошуку кімнат, Оголошення про кімнату, Чат із людиною, Перелік розмов |
| `--col-count-tablet` | primitive | `card-list split` | — | Результати пошуку кімнат, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--col-count-desktop` | primitive | `card-list split` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--color-page` | semantic | `actionbar avatar chip-row composer header tabbar topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-card` | semantic | `bubble chat-context group screens` | — | Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-control` | semantic | `button chip composer field` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Скарга |
| `--color-stub` | semantic | `actionbar card-list group hero-photo listing-card listing-title profile-head skeleton` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--color-over-photo` | semantic | `price-tag screens` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--color-over-photo-dim` | semantic | `screens topbar` | — | Оголошення про кімнату |
| `--color-inverted` | semantic | `bubble` | — | Чат із людиною |
| `--color-divider` | semantic | `actionbar composer group sheet split tabbar topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-field-edge` | semantic | `composer field` | — | Результати пошуку кімнат, Чат із людиною, Скарга |
| `--color-text` | semantic | `bubble button chip composer field price-tag screens sheet tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-text-secondary` | semantic | `base bubble card-list chat-context group header listing-card listing-title profile-head results-meta screens state` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-inactive` | semantic | `chat-context group tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Чат із людиною, Перелік розмов |
| `--color-text-on-inverted` | semantic | `bubble` | — | Чат із людиною |
| `--color-text-on-photo` | semantic | `screens topbar` | — | Оголошення про кімнату |
| `--color-action` | semantic | `button composer` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-action-hover` | semantic | `button composer` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-text-on-action` | semantic | `button composer` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-current` | semantic | `card-list chip group listing-card tabbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-verified` | semantic | `avatar group topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--color-focus` | semantic | `card-list chip-row gallery hero-photo listing-card` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--color-error` | semantic | `state` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--color-sheet` | semantic | `screens sheet` | — | Результати пошуку кімнат |
| `--color-sheet-scrim` | semantic | `screens sheet` | — | Результати пошуку кімнат |
| `--color-action-active` | semantic | `button composer` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-control-hover` | semantic | `button chip` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Скарга |
| `--color-control-active` | semantic | `button chip` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Скарга |
| `--color-field-edge-hover` | semantic | `composer field` | — | Результати пошуку кімнат, Чат із людиною, Скарга |
| `--color-ghost-hover` | semantic | `button screens topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-ghost-active` | semantic | `screens topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-card-hover` | semantic | `chat-context group` | — | Оголошення про кімнату, Чат із людиною, Перелік розмов, Скарга |
| `--color-link-hover` | semantic | `card-list listing-card` | — | Результати пошуку кімнат, Профіль іншої людини |
| `--color-over-photo-dim-hover` | semantic | `topbar` | — | Оголошення про кімнату |
| `--color-action-text` | semantic | `button` | — | Результати пошуку кімнат |
| `--color-grabber` | semantic | `screens sheet` | — | Результати пошуку кімнат |
| `--color-text-on-verified` | semantic | `avatar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Перелік розмов |
| `--color-tag-hole` | semantic | `price-tag` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--color-tag-hole-edge` | semantic | `price-tag` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини |
| `--color-state-icon` | semantic | `state` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--color-stub-on-card` | semantic | `actionbar group hero-photo listing-title profile-head skeleton` | — | Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов |
| `--color-text-secondary-on-inverted` | semantic | `bubble` | — | Чат із людиною |
| `--color-text-on-current` | semantic | `chip` | — | Результати пошуку кімнат |
| `--dur-fast` | semantic | `button chip composer topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--dur-base` | semantic | `state` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--dur-slow` | semantic | `actionbar button group hero-photo listing-card listing-title profile-head screens sheet skeleton` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--ease-standard` | semantic | `actionbar button chip composer group hero-photo listing-card listing-title profile-head skeleton topbar` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--ease-enter` | semantic | `button screens sheet state` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
| `--ease-exit` | semantic | `button` | — | Результати пошуку кімнат, Оголошення про кімнату, Профіль іншої людини, Чат із людиною, Перелік розмов, Скарга |
<!-- /_map.py -->

### Токени поза картою

<!-- _map.py:unused -->
Ці токени не стоять на жодному екрані з карти, ні напряму, ні через інший токен:

`--font-onest --weight-regular --size-22 --opacity-disabled --duration-0-01 --dur-instant --move-sm --move-md`
<!-- /_map.py -->

## Тексти: `microcopy.md` і `voice.md`

Обидва файли є частиною пакета передачі.
Ми не копіюємо їх у `handoff/`, а даємо посилання.
Так у пакеті немає двох версій одного тексту.

- [`microcopy.md`](../microcopy.md) каже, які слова стоять на екрані. Один рядок — один текст, з ID, зоною, старим і новим текстом. Колонка «Ключ» у карті посилається на ці ID.
- [`voice.md`](../voice.md) каже, як писати нові слова. Там є принципи, словник термінів, заборонені форми і правила для кожного типу тексту.

Якщо текст на екрані і рядок `microcopy.md` різні, джерело правди ще не визначене.
Це відкрите питання G35 у [`onboarding-gaps.md`](onboarding-gaps.md).

### Новий екран, якого немає в карті: як написати тексти

1. Прочитайте [`voice.md`](../voice.md) → «Принципи», пункти 1–4. Вони кажуть, що писати про перевірку, про невідоме і про дію з наслідком.
2. Візьміть назви з [`voice.md`](../voice.md) → «Словник» → «Терміни». Звертання візьміть з розділу «Звертання».
3. Для кожного тексту знайдіть тип у [`voice.md`](../voice.md) → «Мікрокопі»: «Кнопка», «Заголовок екрана», «Поле форми», «Порожній стан», «Помилка», «Завантаження», «Успіх», «Небезпечна дія».
4. Якщо в «Словнику» є шаблон з позначкою (E1, E2, D1–D8, T1–T8), візьміть шаблон. Не пишіть свій варіант.
5. Перевірте текст за розділом [`voice.md`](../voice.md) → «Заборонене».
6. Додайте кожен текст рядком у [`microcopy.md`](../microcopy.md) з новим ID. Потім додайте ID у колонку «Ключ» цієї карти через `ROWS` у [`_map.py`](_map.py).

## Розбіжності

Ми записали розбіжності, але не виправили їх.
Кожен пункт треба вирішити окремо.

### Знайдено руками

Скрипт не бачить ці пункти. Ми знайшли їх, коли читали файли.

Тексти:

- У `microcopy.md` немає рядків для екранів «Перелік розмов» і «Скарга». У карті ці тексти мають позначку «немає ключа» або шаблон зі «Словника».
- У `microcopy.md` є підписи L-07 «Ціна», L-09 «Район», L-11 «Дата заїзду». На екрані «Оголошення про кімнату» цих підписів немає. Там є підписи «Квартира» і «Комунальні», а рядків для них у `microcopy.md` немає.
- Помилка на екрані «Результати пошуку кімнат» показує «Перевір з’єднання й спробуй ще.» замість тексту LS-38 і LS-39.
- C-01 каже «Назад до оголошення». На екрані «Чат із людиною» кнопка «назад» має підпис «Назад до чатів» і веде до `chats.html`.
- LS-14 — заголовок «Оголошення» над переліком. На екрані заголовка немає. Перелік має лише `aria-label` «Перелік».
- [`voice.md`](../voice.md) → «Мікрокопі» → «Успіх» дає приклад «Скаргу надіслано модераторам.». Екран [`report-sent.html`](../design-system/examples/report-sent.html) каже «Скаргу прийнято».
- Ці тексти не мають ні ключа, ні шаблону: «Спершу нові», «Показати ще 3», «Скасувати», «Закрити оголошення», «Закрити чат», «Темна тема», «Київ · кімнати та співмешканці», «Обери чат ліворуч», «Чатів ще немає».

Система:

- Клас `status-dark` на `listing-loading.html` не має стилю. Це позначка для хаба курсу, рядок у `JS_HOOKS` гейта. Карта його не показує.
- Блок `.header__top > .theme-toggle` у [`wireframes/screens.css`](../wireframes/screens.css) — разовий. Але він стоїть на двох екранах: «Результати пошуку кімнат» і «Перелік розмов». За правилом `CLAUDE.md` він має переїхати в `components/`. Див. також G23 в [`onboarding-gaps.md`](onboarding-gaps.md).
- [`report.html`](../design-system/examples/report.html) і [`report-sent.html`](../design-system/examples/report-sent.html) не підключають `screens.css`. Зараз екрану «Скарга» разові блоки не потрібні. Якщо він отримає разовий блок, стиль не спрацює.
- `state-note` — разовий блок у `screens.css`. А [`behavior/README.md`](behavior/README.md) називає його компонентом.

### Знайдено скриптом

<!-- _map.py:drift -->
- Класи: кожен клас екрана має рядок у карті і стиль у системі.

Текст на екрані не збігається з рядком `microcopy.md` (колонка «Стало», а якщо «без змін» — «Було»):

| Ключ | Екран | Текст за `microcopy.md` |
|---|---|---|
| LS-13 | Результати пошуку кімнат | «Шевченківський район · до 12 000 грн/місяць · заїзд з 1 жовтня» |
| LS-14 | Результати пошуку кімнат | «Оголошення» |
| LS-36 | Результати пошуку кімнат | «Фільтри збережено: Шевченківський район · до 12 000 грн/місяць · заїзд з 1 жовтня» |
| LS-39 | Результати пошуку кімнат | «Потім спробуй ще. Фільтри не зміняться.» |
| P-29 | Профіль іншої людини | «Оголошення «Кімната біля Лук’янівської». Номер підтверджено 12 вересня.» |
| C-01 | Чат із людиною | «Назад до оголошення» |
| C-05 | Чат із людиною | «10 500 грн/місяць · заїзд з 1 жовтня · Номер підтверджено 12 вересня» |
| C-06 | Чат із людиною | «10 500 грн/місяць · заїзд з 1 жовтня · Номер підтверджено 12 вересня» |
<!-- /_map.py -->

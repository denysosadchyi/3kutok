# Аудит токенів кіта «Кутка»

Стан на 2026-10-16. Джерела: `ui/kit.css` (змінні `:root` + класи), `wireframes/screens.css`
(разові блоки) і всі 16 екранів `wireframes/*.html`. Тут лише опис: нічого не виправлено
й не перейменовано.

Що перевірено в екранах: атрибутів `style=` і блоків `<style>` немає ніде, тож усі значення
надходять з двох CSS-файлів. Екрани беруть лише класи. Тому стовпчик «файли» нижче називає
екрани, на яких цей клас справді стоїть.

Скорочення екранів: **L** = `listings*` (4 стани: базовий, empty, error, loading), **D** = `listing*` (деталі
оголошення), **P** = `profile*`, **C** = `chat*`. Наприклад, «L» означає всі чотири стани listings,
а «L, P, P-empty» — лише ці екрани.

---

## 1. Таблиця змінних

### 1.1 Колір

| Змінна | Значення | Де вживається (клас → екрани) | Роль у цьому місці |
|---|---|---|---|
| `--color-bg` | `#ffffff` | `body` (усі) | фон сторінки |
| | | `.header` (L), `.topbar` (D, P, C), `.tabbar` + `.tabbar::after` (L), `.actionbar` (D, P), `.composer` (C) | фон закріплених смуг: шапки й нижніх поясів |
| | | `.sheet__panel` (L) | фон шторки, що піднімається над сторінкою |
| | | `.price-tag` (L, D, P), `.card-author` (L) | фон бирки чи пігулки поверх фото |
| | | `.avatar__mark` border, фолбек `--avatar-ring` (L, D, P) | кільце, що відділяє позначку від фото |
| | | `.chip-row::after` градієнт (L) | колір, у який згасає край стрічки чипів |
| `--color-surface` | `#f4f5f6` | `.group`, `.listing-description`, `.state-note`, `.chat-context` (D, P, C) | фон картки чи групи на сторінці |
| | | `.button--secondary`, `.chip` (L, D, P, C-error) | фон другорядного контролу |
| | | `.input`, `.composer__input` (L, C) | фон поля вводу |
| | | `.bubble` (C) | фон бульбашки співрозмовника |
| | | `.skeleton` (усі `*-loading`) | заглушка, поки вміст вантажиться |
| | | `.listing-card__photo`, `.avatar > img` (L, P, D, C) | заглушка, коли фото не завантажилось |
| | | `.composer__send[aria-disabled]` (C) | фон вимкненої дії |
| | | `.sheet__grabber` (L) | ручка шторки |
| | | `.price-tag::before` (L, D, P) | «отвір» у бирці |
| | | `--avatar-ring` усередині `.group` (D, P) | кільце позначки на сірому тлі |
| `--color-line` | `#e6e8eb` | `--hairline-top`: `.actionbar`, `.sheet__foot`, `.composer`, `.group__row + .group__row`, `.sort-options li+li`; `.topbar--person` (нижня лінія) | тонкий розділювач |
| | | `.button--secondary:hover` (L, D, P, C-error) | фон наведеного другорядного контролу |
| | | `.group .skeleton` (D-loading, P-loading) | заглушка на сірій групі |
| | | `.bubble--mine .bubble__time` (C) | **текст**: час на темній бульбашці |
| `--color-field-edge` | `#868c94` | `.input`, `.composer__input` (L, C) | межа поля (3.1:1, WCAG 1.4.11) |
| `--color-ink` | `#15171a` | `body`, `.sheet__title`, `.field__label`, `.chip`, `.price-tag`, `.card-author`, `.sort`, `.sort-options a`, `.bubble`, `.input`, `.button--secondary` | основний текст |
| | | `.chip--selected` (L), `.bubble--mine` (C) | **фон** вибраного чи «мого» елемента (інверсія) |
| | | `.input:hover` (L) | межа поля під курсором |
| | | `.price-tag::before` inset-тінь (L, D, P) | обвідка отвору бирки |
| | | `.state__icon` (усі `*-empty`, `*-error`) | колір великої ілюстрації стану |
| `--color-muted` | `#596069` | `.header__subtitle`, `.listing-card__meta`, `.listing-title__meta`, `.profile-head__caption`, `.group__label`, `.person-row__caption`, `.verified-note__limit`, `.results-meta`, `.chat-context__meta`, `.state__text`, `.state-note__text`, `.chat-day`, `.bubble__time` | другорядний текст |
| | | `::placeholder` (L, C) | підказка в полі |
| | | `.chevron` (D, C) | іконка-вказівник «далі» |
| | | `.tabbar__item` (L) | неактивна вкладка навігації |
| | | `.composer__send[aria-disabled]` (C) | іконка вимкненої дії |
| | | `.muted` | утиліта, на жодному екрані не вжита |
| `--color-on-ink` | `#ffffff` | `.chip--selected`, `.bubble--mine` (L, C) | текст на темному (`--color-ink`) |
| | | `.topbar--over-photo` кнопки (D), `.photo-count` (D) | текст чи іконка на затемненні поверх фото |
| | | `.avatar__mark` (L, D, P) | галочка на **зеленому** (`--color-verified`) |
| `--color-accent` | `#ff9b85` | `.button--primary` (L, D, P, C-error) | фон головної дії |
| | | `.composer__send` (C) | фон дії «Надіслати» |
| `--color-accent-hover` | `#ff8a75` | `.button--primary:hover`, `.composer__send:hover` | наведена головна дія |
| `--color-on-accent` | `#15171a` | `.button--primary`, `.composer__send` | текст чи іконка на коралі |
| `--color-link` | `#b94a40` | `.button--text` (L: «Скасувати» у шторці) | текстова дія (посилання-кнопка) |
| | | `.tabbar__item[aria-current]` (L) | **поточна вкладка** навігації |
| | | `.sort-options iconify-icon` (L) | **позначка вибраного** варіанта (галочка) |
| `--color-verified` | `#0a7d45` | `.avatar__mark` фон (L, D, P) | позначка «номер підтверджено» |
| | | `.topbar__verified` (C) | щит біля імені в чаті |
| | | `.verified-note__icon`, `.verified-note__title` (D, P) | іконка й заголовок рядка «Що підтверджено» |
| `--color-focus` | `#0a7d45` | `:focus-visible` outline (усі), `.listing-card__link:focus-visible::after` (L, P) | кільце фокусу клавіатури |
| `--color-error` | `#b42318` | `.state--error .state__icon` (усі `*-error`) | ілюстрація стану помилки |
| `--color-scrim` | `rgb(21 23 26 / .38)` | `.sheet[open]::before` (L) | затемнення сторінки під шторкою |
| `--color-scrim-photo` | `rgb(21 23 26 / .6)` | `.topbar--over-photo` кнопки (D), `.photo-count` (D) | підкладка під білий текст чи іконку на фото |
| `--color-transparent` | `transparent` | `.avatar > img` color (alt-текст), `.chip-row::after` градієнт | приховати текст; початок згасання |

### 1.2 Шрифт

| Змінна | Значення | Де вживається | Роль |
|---|---|---|---|
| `--font-ui` | Onest, system-ui… | `body` | єдина гарнітура |
| `--weight-regular` | 400 | **ніде** | — |
| `--weight-medium` | 500 | `.button`, `.chip`, `.field__label`, `.listing-card__title`, `.group__value`, `.verified-note__title`, `.chat-context__title`, `.tabbar__item`, `.card-author`, `.sort`, `.photo-count` | дія, значення, назва картки, мітка |
| `--weight-bold` | 700 | `.header__title`, `.topbar__title`, `.topbar__name`, `.sheet__title`, `.section-title`, `.profile-head__name`, `.listing-title__name`, `.person-row__name`, `.state__title`, `.state-note__title`, `.price-tag`, `.tabbar__item[aria-current]`, `.sort-options a[aria-current]` | заголовок; ціна; **виділення поточного** (вкладка, сортування) |
| `--tracking-head` | -0.01em | `.header__title`, `.profile-head__name`, `.listing-title__name` | трекінг великого заголовка (23 px) |
| `--text-xs` | 12 | `.tabbar__item`, `.chat-context__meta`, `.bubble__time`, `.chat-day`, `.photo-count` | дрібний підпис |
| | | `.avatar__mark` (L, D, P) | **розмір іконки** галочки |
| `--text-sm` | 14 | метадані, `.group__label`, `.chip`, `.field__label`, `.results-meta`, `.card-author`, `.sort`, `.chat-context__title`, `.header__subtitle`, `.profile-head__caption`, `.person-row__caption`, `.verified-note__limit` | другорядний текст; мітки контролів |
| `--text-md` | 16 | `body`, `.button`, `.price-tag`, `.topbar__title`, `.topbar__name`, `.listing-card__title`, `.sort-options a`, `.state-note__title` | основний текст; дія; ціна; малий заголовок |
| `--text-lg` | 19 | `.section-title`, `.sheet__title`, `.state__title` | заголовок секції, шторки чи стану |
| `--text-xl` | 23 | `.header__title`, `.profile-head__name`, `.listing-title__name` | заголовок екрана |
| `--leading-name` | 1.2 | `.topbar__name`, `.topbar__verified` | ім'я в шапці чату |
| `--leading-tight` | 1.25 | `.header__title`, `.listing-title__name`, `.listing-card__title`, `.price-tag` | заголовки, ціна |
| `--leading-note` | 1.35 | `.verified-note__text` | двоярусна примітка |
| `--leading-input` | 1.4 | `.composer__input` | поле повідомлення |
| `--leading-body` | 1.45 | `body` | основний текст |
| `--measure-state-title` | 26ch | `.state__title`, `.state-note__title` | ширина заголовка стану |
| `--measure-state-text` | 30ch | `.state__text`, `.state-note__text` | ширина тексту стану |

### 1.3 Форма: радіуси, лінії, тіні

| Змінна | Значення | Де вживається | Роль |
|---|---|---|---|
| `--radius-tag` | 8px | `.price-tag` (правий бік) | кут бирки |
| | | `.skeleton` (за замовчуванням) | кут заглушки-рядка |
| | | `.chat-context__thumb` (C) | кут **мініатюри фото** |
| `--radius-control` | 14px | `.button`, `.chip`, `.input`, `.composer__input`, `.skeleton--button` | кут контролу |
| | | `.chat-context` (C) | кут **картки** контексту |
| | | `.gallery__item > img` (D) | кут **фото** в галереї |
| `--radius-card` | 18px | `.group`, `.listing-description`, `.state-note`, `.listing-card__photo`, `.skeleton--photo` | кут картки чи групи |
| | | `.sheet__panel` (верхні кути) | кут шторки |
| | | `.bubble`, `.skeleton--bubble` | кут бульбашки |
| `--radius-round` | 999px | `.avatar > img`, `.avatar__mark`, `.skeleton--avatar*` | коло аватара |
| | | `.composer__send`, `.topbar--over-photo` кнопки | кругла іконка-кнопка |
| | | `.card-author`, `.photo-count` | пігулка |
| | | `.tabbar__item iconify-icon` | капсула під іконкою вкладки |
| | | `.price-tag::before` | отвір бирки |
| `--radius-grabber` | 3px | `.sheet__grabber` | ручка шторки |
| `--radius-tail` | 4px | `.bubble`, `.bubble--mine` | «хвостик» бульбашки |
| `--border` | 1px | `.input`, `.composer__input` | товщина межі поля |
| | | `--hairline-top`, `.topbar--person` | товщина розділювача |
| | | `.sr-only` width/height/margin | **розмір** прихованого блоку |
| | | `.verified-note__icon` margin-top | **оптичний зсув** іконки |
| | | `.tabbar::after` bottom | **нахлест** хвилі на смугу |
| `--stroke` | 2px | `:focus-visible` outline і offset | кільце фокусу |
| | | `.avatar__mark` border | кільце позначки |
| | | `.price-tag::before` | обвідка отвору |
| `--shadow-tag` | `0 4px 10px rgb(0 0 0/.14)` | `.price-tag` (filter: drop-shadow), `.card-author` (box-shadow) | тінь предмета на фото |
| `--shadow-float` | `0 8px 24px rgb(0 0 0/.12)` | `.sheet__panel` | тінь шару над сторінкою |
| `--hairline-top` | `0 -1px 0 var(--color-line)` | `.actionbar`, `.sheet__foot`, `.composer`, `.group__row + .group__row`, `.sort-options li+li` | верхній розділювач |

### 1.4 Відступи

| Змінна | Значення | Де вживається | Роль |
|---|---|---|---|
| `--space-px` | 1px | `.person-row__text` gap | зазор між іменем і підписом |
| `--space-0-5` | 2px | `.listing-title` gap і padding, `.bubble__time` margin | мікрозазор |
| `--space-1` | 4px | gap у `.field`, `.chip`, `.sort`, `.listing-card__body`, `.profile-head`; `.header__top` низ; `.results-meta` верх; `.gallery` низ; `.card-author` padding | малий внутрішній зазор |
| | | `.bubble--mine + .bubble--mine` | ритм між повідомленнями одного мовця |
| | | `.avatar__mark` right/bottom ×−1 | виступ позначки за аватар |
| | | `.listing-card__link:focus-visible::after` offset | відступ кільця фокусу на картці |
| | | `--tab-icon-drop` | опускання іконки вкладки |
| | | `.sheet__foot`: `--space-5 − --space-1` | віднімається, щоб дістати 20px |
| `--space-1-5` | 6px | `.chip-row__track` gap | зазор між чипами |
| `--space-2` | 8px | `.shell__main` верх, `.topbar` бічні, gap у `.listing-card`, `.gallery`, `.actionbar`, `.composer`, `.state`, `.skeleton-stack`, `.button`, `.card-author`, `.topbar__person`; padding у `.bubble` і `.chat-context` | базовий зазор |
| | | `.sheet__grabber` margin, `.sheet__head`, `.sheet__body` верх | ритм шторки |
| | | `--tab-icon-box-h` (+24) | **розмір** капсули вкладки |
| | | `.skeleton--bubble-short` (32+8) | **висота** заглушки |
| `--space-2-5` | 10px | `.actionbar` низ, `.sheet__foot` верх | відступ нижнього поясу |
| `--space-3` | 12px | `.shell__main` gap, gap у `.group__row`, `.person-row`, `.chat-context`, `.skeleton-person`; padding у `.group__row`, `.bubble`, `.chip`, `.composer`, `.listing-description`, `.group--padded`; `.price-tag`, `.card-author` і `.photo-count` (top/left/right/bottom) | середній зазор; відступ предмета від краю фото |
| | | `.bubble + .bubble` | ритм зміни мовця |
| | | `.actionbar` верх, `.composer` верх і низ, `.shell--actionbar` запас | відступ нижнього поясу |
| | | `.skeleton--line` height | **висота** заглушки-рядка |
| `--space-3-5` | 14px | `.sheet__body` gap, `fieldset` gap | зазор між полями форми |
| `--space-4` | 16px | `.header__top` верх, `.section-title` верх, `.group` бічні, `.input` бічні, `.composer__input` бічні, `.listing-description` бічні, `.state` бічні, `.sheet__body` низ, `.hero-photo > .price-tag` bottom | великий внутрішній відступ |
| | | `--tab-lift` ×−1 | підйом вкладки над хвилею |
| | | `.skeleton--title` height, `.skeleton--bubble-tall` (48+16) | **висота** заглушки |
| `--space-5` | 24px | `.shell__main` низ, `.button` бічні, `.state-note` padding | відступ кінця контенту; поля кнопки |
| | | `.sort-options` низ, `.sheet__foot` низ (24−4) | відступ нижнього поясу шторки |
| `--space-6` | 32px | `.card-list` gap | зазор між картками оголошень |
| | | `.state` верх і низ | поле стану |
| | | `--tab-icon-box-w` (+24), `.skeleton--bubble-short`, `.shell--composer` стан (48+32) | **розміри** |
| `--space-7` | 48px | `.skeleton--bubble`, `.skeleton--bubble-tall` | **висота** заглушки бульбашки |
| `--gutter` | 16px | padding у `.shell__main`, `.header__top`, `.header__bar`, `.actionbar`, `.composer`, `.sheet__head`, `.sheet__body`, `.sheet__foot`, `.sort-options`; від'ємний margin у `.hero-photo`, `.gallery`, `.chip-row__track`; `.hero-photo > .price-tag` left; `scroll-padding` | бічне поле екрана |
| `--fade` | 32px | `.chip-row::after` width, `.chip-row__track` правий padding | ширина згасання стрічки чипів |

### 1.5 Розміри

| Змінна | Значення | Де вживається | Роль |
|---|---|---|---|
| `--touch` | 48px | min-height у `.button`, `.input`, `.composer__input`, `.group__row`, `.sort`, `.sort-options a`; `.skeleton--button` | мінімальна висота цілі дотику |
| | | `.composer__send`, `.topbar--over-photo` кнопки | розмір круглої кнопки |
| | | `.chat-context__thumb` (C) | **розмір мініатюри фото** |
| | | `.shell--composer .shell__main:has(.state)` | **висота** composer у розрахунку |
| `--hit` | 44px | `.topbar__back`, `.topbar__action`, `.topbar__person`, `.person-row` | мінімальна ціль іконки-кнопки чи рядка |
| `--chip-height` | 36px | `.chip` | висота чипа |
| `--meta-height` | 28px | `.results-meta` | висота рядка під фільтрами |
| `--icon-xs` | 12px | **ніде** | — |
| `--icon-sm` | 16px | `.chevron`, `.sort svg`, `.avatar--lg .avatar__mark` | дрібна іконка |
| `--icon-md` | 20px | `.topbar__action`, `.topbar__verified`, `.chip iconify-icon`, `.composer__send`, `.sort-options iconify-icon` | іконка в контролі |
| `--icon-nav` | 22px | `.topbar__back` | стрілка «назад» |
| `--icon-lg` | 24px | `.tabbar__item iconify-icon`, `.verified-note__icon` | іконка навігації; щит підтвердження |
| | | `--tab-icon-box-w/h` | основа розміру капсули |
| `--icon-state` | 72px | `.state__icon` | ілюстрація стану |
| `--avatar-sm` | 28px | `.avatar > img` | аватар у пігулці та в шапці чату |
| `--avatar-md` | 48px | `.avatar--md`, `.skeleton--avatar` | аватар у рядку людини |
| `--avatar-lg` | 84px | `.avatar--lg`, `.skeleton--avatar-lg` | аватар у шапці профілю |
| `--mark-sm` | 16px | `.avatar__mark` | позначка на аватарі |
| `--mark-lg` | 24px | `.avatar--lg .avatar__mark` | позначка на великому аватарі |
| `--title-max` | 220px | `.topbar__title` | ширина заголовка в шапці |
| `--grabber-width` / `--grabber-height` | 36 / 5px | `.sheet__grabber` | ручка шторки |
| `--sheet-max` | 86% | `.sheet__panel` | висота шторки |
| `--bubble-max` | 78% | `.bubble` | ширина бульбашки |
| `--composer-max` | 112px | `.composer__input` | висота поля, що росте |
| `--gallery-item` | 42% | `.gallery__item` | ширина кадру в галереї |
| `--ratio-photo` | 4/3 | `.listing-card__photo`, `.gallery__item`, `.skeleton--photo` | пропорція фото |
| `--ratio-hero` | 4/3.6 | `.hero-photo` | пропорція головного фото |
| `--press` | 0.98 | `.button:active` | стиснення під час натискання |
| `--blur-photo` | 8px | `.topbar--over-photo` кнопки | розмиття під кнопкою на фото |
| `--sk-title`, `--sk-w60`, `--sk-w40`, `--sk-bubble`, `--sk-bubble-tall`, `--sk-bubble-short` | 70 / 60 / 40 / 70 / 76 / 52 % | однойменні модифікатори `.skeleton--*` (`*-loading`) | ширина заглушок |

### 1.6 Бирка, оболонка, рух

| Змінна | Значення | Де вживається | Роль |
|---|---|---|---|
| `--tag-notch` | 12px | `.price-tag` clip-path | глибина виїмки бирки |
| `--tag-hole` | 8px | `.price-tag::before` | діаметр отвору |
| `--tag-hole-x` | 10px | `.price-tag::before` left | позиція отвору |
| `--tag-pad-left` | 28px | `.price-tag` | лівий відступ, місце під отвір |
| `--tag-tilt` | -4deg | `.price-tag` | нахил бирки |
| `--appbar` | 48px | `.topbar` min-height; розрахунок висоти стану | висота шапки |
| `--tabbar` | 56px | `.tabbar__list`, `.shell--tabbar`, розрахунок стану | висота нижнього меню |
| `--actionbar` | 68px | `.shell--actionbar` | запас під панель дії |
| `--composer-reserve` | 76px | `.shell--composer` | запас під composer |
| `--tab-icon-box-w` / `-h` | calc(24+32) / calc(24+8) | `.tabbar__item iconify-icon` | капсула іконки |
| `--tab-lift` | calc(16 × −1) | `.tabbar__item` | підйом вкладки |
| `--tab-icon-drop` | `var(--space-1)` | `.tabbar__item iconify-icon` | опускання іконки |
| `--safe-bottom` | env(safe-area-inset-bottom) | `.shell--*`, `.tabbar`, `.actionbar`, `.sheet__foot`, `.composer`, `.sort-options`, розрахунок стану | безпечна зона знизу |
| `--z-bar` / `--z-nav` / `--z-scrim` / `--z-sheet` | 3 / 4 / 5 / 6 | `.topbar` і `.actionbar` / `.tabbar` і `.composer` / `.sheet::before` / `.sheet__panel` | шари |
| `--tabbar-wave` / `--tabbar-wave-height` | SVG-маска / 18px | `.tabbar::after` | хвиля над меню |
| `--ease-out` / `--duration` | cubic-bezier(.25,1,.5,1) / 180ms | `.button`, `.composer__send`, `.tabbar__item iconify-icon` | перехід кольору й стиснення |

Поза `:root`:

| Змінна | Значення | Де | Роль |
|---|---|---|---|
| `--avatar-ring` | `var(--color-surface)` у `.group`; фолбек `--color-bg` | `.avatar__mark` border | колір кільця залежить від тла |
| `--frame-status` | **не оголошена**, фолбек `env(safe-area-inset-top)`; задає її `lessons/index.html` | `.topbar--over-photo` top | висота статус-бару |

---

## 2. Знахідки

### 2.1 Дрейф значень: одна роль, різні значення

Hex-дрейфу на кшталт `#2E6E5C` / `#2F6F5D` немає: кожен колір записано один раз. Дрейф є на рівні
ролі, коли однакова за змістом річ отримує різні значення.

| # | Роль | Значення, що розійшлися | Де |
|---|---|---|---|
| D1 | Колір тіні чи затемнення | `--color-scrim*` = `rgb(21 23 26 / …)`, тобто ink; `--shadow-tag` і `--shadow-float` = `rgb(0 0 0 / …)`, чистий чорний | `:root` 35–36 проти 68–69 |
| D2 | Ink, записаний вдруге | `--color-scrim` і `--color-scrim-photo` повторюють `#15171a` як літерал `rgb(21 23 26)` замість посилання на `--color-ink` | `:root` 35–36 |
| D3 | Мінімальна ціль дотику | `--touch` 48 і `--hit` 44. Кнопки шапки мають 44, ті самі кнопки на фото мають 48. `.person-row` має 44 усередині `.group__row` з 48 | `.topbar__back/action` проти `.topbar--over-photo`; `.person-row` |
| D4 | Кут фото | картка 18 (`--radius-card`), галерея 14 (`--radius-control`), мініатюра в чаті 8 (`--radius-tag`), hero 0 | `.listing-card__photo`, `.gallery__item`, `.chat-context__thumb`, `.hero-photo` |
| D5 | Кут картки | `.group` і `.listing-description` 18, `.chat-context` 14 | C проти D, P |
| D6 | Нижній відступ поясу над safe-area | actionbar 10 (`--space-2-5`), composer 12 (`--space-3`), sheet__foot 20 (`--space-5 − --space-1`, поза шкалою), sort-options 24 (`--space-5`) | `.actionbar`, `.composer`, `.sheet__foot`, `.sort-options` |
| D7 | Верхній відступ поясу | actionbar і composer 12, sheet__foot 10 | там само |
| D8 | Резерв під composer | `--composer-reserve` 76 у `.shell--composer`, а розрахунок висоти стану бере `--touch + --space-6` = 80 | kit.css 197 проти 213 |
| D9 | Розмір іконки в позначці | малу позначку задано текстовим токеном `--text-xs` (12), велику іконковим `--icon-sm` (16) | `.avatar__mark` проти `.avatar--lg .avatar__mark` |
| D10 | Інтерліньяж | п'ять близьких значень: 1.2 / 1.25 / 1.35 / 1.4 / 1.45, кожне на 1–4 класах | `--leading-*` |
| D11 | Тонкий розділювач | верхній є токеном (`--hairline-top`), нижній у `.topbar--person` зібрано вручну | kit.css 268 |
| D12 | Тінь бирки | одна тінь, два механізми: `filter: drop-shadow` на `.price-tag` і `box-shadow` на `.card-author`. Розмиття з тим самим радіусом виглядає різно | `.price-tag`, `.card-author` |

Однакові значення під різними іменами. Це не помилка, але кандидати на злиття або на явний зв'язок:
- `#0a7d45`: `--color-verified` = `--color-focus` (див. M3).
- `#15171a`: `--color-ink` = `--color-on-accent`; `#ffffff`: `--color-bg` = `--color-on-ink`.
- 16px: `--space-4` = `--gutter` = `--icon-sm` = `--mark-sm`.
- 48px: `--touch` = `--appbar` = `--avatar-md` = `--space-7`.
- 24px: `--space-5` = `--icon-lg` = `--mark-lg`; 28px: `--avatar-sm` = `--meta-height` = `--tag-pad-left`.
- 2px: `--space-0-5` = `--stroke`; 1px: `--space-px` = `--border`; 4px: `--space-1` = `--radius-tail`; 14px: `--space-3-5` = `--radius-control`.
- 70%: `--sk-title` = `--sk-bubble`.

Оголошені, але не вжиті: `--weight-regular`, `--icon-xs`, клас `.muted`, `.header__bar`, `.shell--header`.

### 2.2 Одна змінна на кілька ролей

| # | Змінна | Ролі, що змішалися |
|---|---|---|
| M1 | `--color-link` | текстова дія «Скасувати» · поточна вкладка меню · галочка вибраного сортування. Справжні посилання (`<a>`) її не беруть: вони успадковують ink. Назва «link» не відповідає жодному з трьох вживань |
| M2 | `--color-surface` | фон картки чи групи · фон контролу (кнопка, чип, поле) · бульбашка · скелетон · фолбек фото · вимкнена дія · ручка шторки · отвір бирки. Тому вимкнена «Надіслати» має той самий колір, що й звичайне поле поруч, а заглушка скелетона збігається з карткою |
| M3 | `#0a7d45` (`--color-verified` + `--color-focus`) | «номер підтверджено» і кільце фокусу клавіатури мають той самий зелений. Фокус на будь-якому контролі читається як знак довіри |
| M4 | `--color-ink` | основний текст · **фон** вибраного чипа й «моєї» бульбашки · межа поля під курсором · обвідка отвору бирки · ілюстрація стану |
| M5 | `--color-line` | розділювач · фон hover другорядного контролу · скелетон на сірому · **колір тексту** часу на темній бульбашці |
| M6 | `--color-bg` | фон сторінки · фон закріплених смуг · фон шторки · фон бирки й пігулки на фото · кільце позначки · кінець згасання чипів |
| M7 | `--color-muted` | другорядний текст · placeholder · шеврон · неактивна вкладка · іконка вимкненої дії. «Вимкнене» і «неактивна вкладка» виглядають однаково, хоча вкладка клікабельна |
| M8 | `--color-on-ink` | текст на ink · текст на затемненні фото · галочка на зеленому. Три різні фони, один «on»-токен |
| M9 | `--weight-bold` | вага заголовка · позначка поточного пункту (вкладка, сортування). Поточний стан виражено вагою, а не окремим токеном |
| M10 | `--radius-control` | контроли · картка контексту в чаті · фото в галереї |
| M11 | `--radius-tag` | бирка · скелетон · мініатюра фото |
| M12 | `--touch` | висота цілі · розмір круглої кнопки · розмір мініатюри фото · висота composer у розрахунку |
| M13 | `--space-2`…`--space-7` | відступи, а також висоти скелетонів (`--space-3`, `--space-4`, `--space-7`) і розміри капсули вкладки (`--space-2`, `--space-6`) |
| M14 | `--border` | товщина межі · розмір `.sr-only` · оптичний зсув іконки · нахлест хвилі |
| M15 | `--stroke` | кільце фокусу · кільце позначки · обвідка отвору |
| M16 | `--text-xs` | розмір шрифту · розмір іконки галочки (`.avatar__mark`) |

`--color-accent` тримає одну роль, головну дію (`.button--primary`, `.composer__send`). На
верифікації й посиланнях його немає, тож саме цей приклад із брифу в коді не підтвердився.

### 2.3 Значення повз змінні

У `wireframes/screens.css` і в HTML літералів немає. Усе знайдене нижче лежить у класах `ui/kit.css`.

| # | Місце | Літерал | Коментар |
|---|---|---|---|
| L1 | `.topbar--person` (268) | `box-shadow: 0 var(--border) 0 var(--color-line)` | нижня лінія, зібрана в класі; дзеркало `--hairline-top` |
| L2 | `.topbar--over-photo` (284) | `top: var(--frame-status, env(safe-area-inset-top))` | `--frame-status` не оголошена в `:root`; верхня safe-area записана як `env()` у класі, а нижня має токен `--safe-bottom` |
| L3 | `.tabbar__list` (326) | `repeat(3, 1fr)` | кількість вкладок записана числом |
| L4 | `.tabbar__item` (334) | `z-index: 1` | поза шкалою `--z-*` |
| L5 | `.price-tag` (459), `.price-tag::before` (467) | `0 50%`, `top: 50%` | 50% не входить до дозволених винятків (0, 100%, 1fr) |
| L6 | `.price-tag::before` (471) | `calc(var(--tag-hole) / -2)` | число в розрахунку (центрування) |
| L7 | `.shell` (194), стани (211, 213) | `100dvh` | висота вікна літералом |
| L8 | `.sheet__foot` (420) | `calc(var(--space-5) - var(--space-1) + …)` | токени є, але результат (20px) поза шкалою, тобто «прихований» літерал |
| L9 | `:root` `--shadow-*` | `rgb(0 0 0 / .14)`, `rgb(0 0 0 / .12)` | колір тіні не прив'язаний до жодного колірного токена (див. D1) |
| L10 | `:root` `--color-scrim*` | `rgb(21 23 26 / …)` | ink переписаний вручну (див. D2) |

Незначні: множники `* -1` у calc (`.avatar__mark`, `.hero-photo`, `.gallery`, `.chip-row`, `.sr-only`, `--tab-lift`) і `inset 0 0 0` у тіні отвору. Вони структурні, але формально теж числа в класах.

Окремо: `status-dark` на `listing-loading.html` не описаний у жодному CSS екранів. Це позначка
для `lessons/index.html` (`_build.py:21`), а не токен. Тут він лише для повноти.

---

## 3. Кандидати в семантичні ролі

| Роль | Звідки її видно (сьогоднішні вживання) | Зараз тримає |
|---|---|---|
| **Фон сторінки** | `body`; закріплені смуги `.header`, `.topbar`, `.tabbar`, `.actionbar`, `.composer`; кінець згасання `.chip-row::after`; кільце `.avatar__mark` поза групою | `--color-bg` |
| **Фон картки** | `.group`, `.listing-description`, `.state-note`, `.chat-context`; співрозмовник `.bubble`; фолбек `.listing-card__photo`, `.avatar > img`. Окремі підролі всередині `--color-surface`: **фон контролу** (`.button--secondary`, `.chip`, `.input`, `.composer__input`), **скелетон** (`.skeleton`, `.group .skeleton` з `--color-line`), **шар над сторінкою** (`.sheet__panel` на `--color-bg`) і **предмет на фото** (`.price-tag`, `.card-author` на `--color-bg`) | `--color-surface` (+ частина `--color-bg`) |
| **Текст основний** | `body`, заголовки (`.section-title`, `.sheet__title`, `.state__title`), `.chip`, `.field__label`, `.input`, `.price-tag`, `.bubble`; плюс «on»-варіанти: `--color-on-accent` (на коралі), `--color-on-ink` (на темному, на фото, на зеленому) | `--color-ink`, `--color-on-*` |
| **Текст другорядний** | усі `__meta`, `__caption`, `__subtitle`, `.group__label`, `.state__text`, `.verified-note__limit`, `.bubble__time`, `.chat-day`, `.results-meta`, `::placeholder`. Окремо видно **неактивне чи вимкнене** (`.tabbar__item`, `.composer__send[aria-disabled]`, `.chevron`) і **другорядне на темному** (`.bubble--mine .bubble__time` з `--color-line`) | `--color-muted` (+ `--color-line`) |
| **Дія** | головна: `.button--primary`, `.composer__send` (+ hover і текст на ній). Текстова: `.button--text`. Видно ще дві суміжні ролі, що зараз сидять на «link»: **поточний пункт навігації** (`.tabbar__item[aria-current]`) і **вибране в списку** (`.sort-options` галочка); плюс **вибраний фільтр** (`.chip--selected` на ink) | `--color-accent*`, `--color-on-accent`, `--color-link`, `--color-ink` |
| **Довіра** | `.avatar__mark` (L, D, P), `.topbar__verified` (C), `.verified-note__icon`, `.verified-note__title` (D, P). Значення збігається з **фокусом** (`:focus-visible`), а фокус є окремою роллю, яку варто відв'язати | `--color-verified` (= `--color-focus`) |
| **Небезпека** | поки лише `.state--error .state__icon` на чотирьох `*-error`. У брифі є report і block (`.topbar__action` «Заблокувати чи поскаржитися» на D, P, C), але шторки з цими діями ще немає, тож руйнівна дія кольору не має | `--color-error` |

Ролі, які таблиця підсвічує додатково (без кольору з переліку вище): **межа** (`--color-line` як
розділювач і `--color-field-edge` як межа поля), **затемнення** (`--color-scrim`, `--color-scrim-photo`,
тіні), **фокус** (зараз склеєний з довірою).

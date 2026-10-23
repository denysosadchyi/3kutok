# Куток

Пошук співмешканців і вільних кімнат у Києві — мобільний веб-сервіс для
людей 22–30 років, побудований навколо довіри, а не просто обсягу
оголошень.

**MVP:** пошук за метро/ціною/датою заїзду/уподобаннями → профіль з
анкетою способу життя → вбудований чат. Довіра в MVP: обов'язкова
верифікація телефону + report, block і базова модерація. Рейтинги після
проживання — discovery-кандидат, не обіцянка MVP.

Повний продуктовий бриф — у [CLAUDE.md](./CLAUDE.md).

## Lesson hub (курс Design Engineering)

Статичний сайт без збірки: відкрити `index.html` або задеплоїти корінь
репо як є.

- [index.html](./index.html) — вхід, перенаправляє на урок 1.
- [research/research.html](./research/research.html) — урок 1 «Ресерч і
  бенчмарк» з сайдбаром на всі 12 уроків.
- [lessons/index.html](./lessons/index.html) — готовий урок 2 «Персони і
  JTBD» та placeholder для уроків 3–12 (`lessons/?lesson=N`); `?lesson=1`
  веде на урок 1.
- [ui/tokens.html](./ui/tokens.html) — урок 8 «Design Tokens»: primitive,
  ролі кольору, контраст обох тем (`lessons/?lesson=8`).
- [research/screens/](./research/screens/README.md) — скріншоти-докази.

## Структура репо

Живий індекс — оновлювати статус по мірі просування дизайн-процесу.

| Папка | Що там | Статус |
|---|---|---|
| [research/](./research/research.md) | Desk research: конкуренти, бенчмарк довіри, рішення та гіпотези; скріншоти в `research/screens/`; живі інтерв'ю ще не проведено | desk research завершено; потрібні інтерв'ю |
| [wireframes/](./wireframes/) | 16 мобільних екранів MVP зі станами, зібрані з кіта (`_build.py`) | уроки 4–8: на `tokens.css` + `components/`, критика й аудит пройдені |
| [concept/](./concept/) | Візуальний напрям «Бирка з ключем», референси, токени уроку 6 | урок 6 завершено; значення живуть у [`tokens.css`](./tokens.css) |
| [ui/](./ui/) | Оболонка, вітрина кіта, інвентар | уроки 7–8 |
| [visuals/](./visuals/README.md) | Власні згенеровані фото продукту + промпт | урок 7 |
| [tokens.css](./tokens.css) | Дизайн-токени у два рівні: primitive і semantic + темна тема; аудит — [tokens-audit.md](./tokens-audit.md) | урок 8 завершено |
| [components/](./components/README.md) | Один CSS-файл на компонент, збірка — `components/index.css` | урок 8 завершено |
| [design-system/](./design-system/) | Зведена документація дизайн-системи | не розпочато |
| [handoff/](./handoff/) | Матеріали для передачі в розробку | не розпочато |

## UI

Екрани збираються з кіта, а не мають власних стилів.

- [`tokens.css`](./tokens.css) — усі значення (див. «Tokens» нижче).
- [`components/`](./components/README.md) — класи компонентів, один файл на
  компонент; збірка — `components/index.css`. У класах літералів немає.
- [`ui/shell.html`](./ui/shell.html) — оболонка екрана: верхній шар, нижній
  пояс, шаблони app bar.
- [`ui/kit.html`](./ui/kit.html) — вітрина кіта: кожен компонент у кожному
  стані. На хабі — `lessons/?lesson=7`.
- [`ui/inventory.md`](./ui/inventory.md) — що стоїть на 2+ екранах (у кіті) і
  що разове (`wireframes/screens.css`).
- [`visuals/`](./visuals/README.md) — усі фото продукту, один колорит, промпт
  генерації. Стокових фото в продукті немає.
- [`DESIGN.md`](./DESIGN.md) — правила й причини правок.
- Екрани: редагувати `wireframes/_build.py`, потім
  `python3 wireframes/_build.py` — перезаписує всі `wireframes/*.html`.

## Tokens

Значення живуть в одному файлі [`tokens.css`](./tokens.css), у два рівні:

- **PRIMITIVE** — сирі значення без ролей: кольори (`--green`, `--grey-600`,
  `--coral`), відступи `--space-*`, радіуси `--radius-*`, розміри `--size-*`,
  шрифти, кегль, інтерліньяж `--leading-*`, тіні, тривалості.
- **SEMANTIC** — лише ролі кольору `--color-*` (сторінка, картка, текст,
  дія, довіра, небезпека, шар над сторінкою…). Кожна роль — `var()` на
  primitive і коментар, з яких вживань вона виросла
  ([tokens-audit.md](./tokens-audit.md)).

Правила:

- компонент бере колір **лише** через semantic-роль, геометрію — з
  primitive напряму (окремого рівня для геометрії немає);
- hex, пікселі й назви шрифтів — тільки в primitive;
- правка значення — у токен свого рівня; зміна розмітки — у `ui/kit.html`
  і в `wireframes/_build.py`; причина — у `DESIGN.md`.

**Темна тема** — блок `[data-theme="dark"]` перевизначає тільки semantic-
ролі; перемикач — кнопка-місяць у навпанелях (`localStorage 'kutok-theme'`).
Контраст обох тем за WCAG AA записано коментарями в `tokens.css`. Тема —
експеримент, стрес-тест semantic-шару: лишати її в продукті — окреме
продуктове рішення. На хабі — `lessons/?lesson=8`.

Живий сайт: https://3kutok.vercel.app

Порядок процесу: research → wireframes → concept → tokens → components → design-system → handoff.

Для уроку 1 (Max 1): [журнал прогону кроків 03–06](./research/prompt-runs.md)
і [HTML-версія уроку](./research/research.html).

# Хендофф

Матеріали для передачі «Кутка» в розробку. Реліз — тег `v1.0` у git.

## Посилання

| Що | Адреса |
|---|---|
| Репозиторій | https://github.com/denysosadchyi/3kutok (тег [`v1.0`](https://github.com/denysosadchyi/3kutok/tree/v1.0)) |
| Живий showcase системи | https://denysosadchyi.github.io/3kutok/design-system/docs/ |
| Живий продукт | https://denysosadchyi.github.io/3kutok/wireframes/listings.html |

Обидві адреси — GitHub Pages з гілки `main`, корінь репо. Кожен пуш у `main` оновлює сайт. Збірки на сервері немає: Pages віддає файли як є.

## Склад пакета

Головний матеріал — специфікація поведінки продукту. Вона описує те, чого не видно в статичних екранах:

- коли з'являється стан;
- що вважається валідним;
- що відбувається на порожньому списку, на збої й на граничному випадку.

| Файл | Що там |
|---|---|
| [`onboarding-gaps.md`](onboarding-gaps.md) | Питання нового розробника. Це замовлення на хендофф |
| [`map.md`](map.md) | Карта екранів: елемент → компонент → токени → ключ `microcopy.md`. Зворотний список «токен → екрани». Генерує `python3 handoff/_map.py` |
| [`a11y.md`](a11y.md) | Чекліст доступності за уроками 8–11: фокус, контраст AA, брейкпоінти в rem, `prefers-reduced-motion`. Де в коді і як перевірити. Борг — G41–G43 |
| [`behavior/README.md`](behavior/README.md) | Специфікація поведінки: спільні правила станів і формат посилань |
| [`behavior/search.md`](behavior/search.md) | Флоу «Пошук»: видача, фільтри, сортування, «показати ще» |
| [`behavior/listing.md`](behavior/listing.md) | Флоу «Оголошення про кімнату» |
| [`behavior/profile.md`](behavior/profile.md) | Флоу «Профіль іншої людини» |
| [`behavior/chats.md`](behavior/chats.md) | Флоу «Чати»: перелік, історія, надсилання, оновлення |
| [`behavior/safety.md`](behavior/safety.md) | Флоу «Блокування і скарга» |
| [`behavior/open-questions.md`](behavior/open-questions.md) | Рішення, яких немає в джерелах. Кожна мітка **[?]** веде сюди |
| [`../microcopy.md`](../microcopy.md) | Тексти інтерфейсу: які слова стоять на кожному екрані. Частина пакета, у `handoff/` не копіюється |
| [`../voice.md`](../voice.md) | Tone of voice: як писати нові тексти. Частина пакета, у `handoff/` не копіюється |

## Що продукт, а що курс

Репо тримає два проєкти: сервіс «Куток» і сайт курсу про нього. Хендофф передає лише продукт (`onboarding-gaps.md` → G1).

**Продукт — передаємо:**

- бриф і рішення: `CLAUDE.md`, `PRODUCT.md`, `DESIGN.md`, `tokens-audit.md`;
- вимоги: `jtbd.md`, `personas.md`, `flows.md`, `sitemap.md`;
- тексти: `microcopy.md`, `voice.md`;
- система: `design-system/` — єдине джерело токенів, компонентів і патернів;
- екрани: `wireframes/`, фото: `visuals/`;
- рішення за шириною й рухом: `responsive/width-audit.md`, `animations/motion-inventory.md`;
- цей хендофф: `handoff/`.

**Курс — не передаємо:** `index.html`, `lessons/`, `research/research.html`, `concept.html`, `concept-lesson.html`, `voice.html`, `ia.html`, `assets/`, `ui/`, `RUN-LOG.md`, `PLAN-lesson6-run.md`, `lesson-2-improvement-plan.md`, `lan_server.py`, `livereload.py`.

**Історія — читати лише для контексту:** `research/research.md`, `concept/`, `tokens/`.

**Інструменти:** `tools/ste/` (лінтер службових текстів), `design-system/_gate.py` (гейт системи).

## Запуск локально

Збірки немає. Екрани — статичні HTML (`onboarding-gaps.md` → G5).

1. Потрібні Python 3 і інтернет: шрифт та іконки приходять з CDN.
2. Після клонування увімкніть хук комміту: `git config core.hooksPath .githooks`.
3. З кореня репо запустіть сервер: `python3 -m http.server 8000`.
4. Відкрийте `http://localhost:8000/wireframes/listings.html`. Це перший екран продукту.

Чому сервер, а не `file://`: усі екрани мають одне походження. Тоді вибір теми й стан сесії спільні для всіх екранів, як у продукті.

Після зміни розмітки: `python3 wireframes/_build.py`, потім `python3 design-system/_gate.py`.

## Тема

Світла тема — за замовчуванням. Темна вмикається лише вибором людини: кнопка-місяць. Системне налаштування телефону тему не міняє (`onboarding-gaps.md` → G20). Поведінку тримає `design-system/theme.js`.

## Що закриває специфікація

З [`onboarding-gaps.md`](onboarding-gaps.md) специфікація закриває частково такі пункти:

- G25 — яка поведінка є контрактом, а яка — код прототипу;
- G28 — які дані на екрані є правилом, а які — прикладом;
- G29 — стан екрана, інший запис чи окремий екран;
- G40 — поведінка за межами вигляду.

Пункти G36 і G37 не закрито: екранів реєстрації, створення оголошення й модерації немає. Специфікація їх не описує.

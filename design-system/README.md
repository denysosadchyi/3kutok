# Design System

Дизайн-система «Кутка» одним пакетом (урок 9). Продукт підключає її
одним рядком — не токени й компоненти окремо:

```html
<link rel="stylesheet" href="../design-system/index.css">
```

| Шлях | Що там |
|---|---|
| [`index.css`](index.css) | Точка входу: імпортує `tokens.css`, потім `components/index.css` |
| [`tokens.css`](tokens.css) | Значення у два рівні: PRIMITIVE і SEMANTIC + темна тема (урок 8) |
| [`components/`](components/README.md) | Один CSS-файл на компонент, збірка — `components/index.css` (урок 8) |
| [`patterns/`](patterns/README.md) | Композиції компонентів, що вже стоять на 3+ екранах: один HTML-фрагмент на патерн, без нових стилів (урок 9) |
| `docs/` | Документація: сторінка на компонент (анатомія, варіанти, коли вживати, правило й антиправило), showcase `index.html`, `why.html` і `patterns.html` (патерни: коли брати патерн, а коли — окремі компоненти). Генерується `python3 design-system/docs/_build.py` — HTML руками не правити |
| [`examples/`](examples/) | Цілі екрани, зібрані лише з `index.css`, без власних стилів — перевірка самодостатності системи. Перший — «Скарга на Ірину» (`report.html`, `report-sent.html`, Related job 5) |
| [`_gate.py`](_gate.py) | Гейт: `python3 design-system/_gate.py` падає на токен, якого немає в `tokens.css`, сире значення, `<style>` на екрані, клас поза системою, компонент без `docs/`. Правила внеску — `../CLAUDE.md` і `../DESIGN.md`, «Внесок у систему» |
| [`backlog.md`](backlog.md) | Чого системі забракло при збірці прикладів — замовлення для системи, а не винятки для екранів |

Правила токенів і компонентів — у [`../CLAUDE.md`](../CLAUDE.md) і
[`../DESIGN.md`](../DESIGN.md). До уроку 9 `tokens.css` і `components/`
лежали в корені репо; історію видно через `git log --follow`.

Візуальна мова сторінок уроків (lesson hub) — окремо:
[`../DESIGN-artifacts.md`](../DESIGN-artifacts.md) і
[`../assets/styles/lesson-system.css`](../assets/styles/lesson-system.css).

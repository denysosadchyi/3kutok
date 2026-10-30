# Patterns

Патерн — композиція наявних компонентів, яка **вже** стоїть щонайменше на
трьох екранах `wireframes/`. Один файл на патерн: HTML-фрагмент із
коментарем угорі (що за композиція, з яких компонентів, де стоїть, коли
брати патерн і коли — окремі компоненти).

- Нових стилів немає: лише класи з `../index.css`, без `<style>` і `style=""`.
- Патерн не вигадується наперед: немає трьох екранів — немає патерна.
- Розмітка екранів редагується в `wireframes/_build.py`; фрагмент тут — зразок
  композиції, а не джерело для збірки екранів.
- Живі приклади й поради «патерн чи компоненти» — у
  [`../docs/patterns.html`](../docs/patterns.html) (генерує
  `python3 design-system/docs/_build.py`, зміст — `docs/_patterns.py`;
  екрани, де патерн стоїть, сторінка шукає в згенерованих `wireframes/*.html`).

| Файл | Патерн | Де стоїть |
|---|---|---|
| [`search-panel.html`](search-panel.html) | Панель пошуку: шапка → чипи зі шторкою фільтрів → підсумок | `listings`, `listings-empty`, `listings-error`, `listings-loading` |
| [`card-feed.html`](card-feed.html) | Стрічка карток оголошень з биркою ціни | `listings`, `listings-loading`, `profile`, `profile-empty` |
| [`section-group.html`](section-group.html) | Розділ зі списком: заголовок → `group` («Що підтверджено» тощо) | `listing`, `profile`, `profile-empty` |
| [`contact-frame.html`](contact-frame.html) | Деталі з контактом: шапка з ⋯ → вміст → панель «Написати Ірині» | `listing`, `profile`, `profile-empty` |
| [`chat-frame.html`](chat-frame.html) | Рамка чату: шапка з людиною → контекст оголошення → поле повідомлення | `chat`, `chat-empty`, `chat-error`, `chat-loading` |
| [`screen-state.html`](screen-state.html) | Стан замість екрана: шапка «назад» → стан з діями, без нижнього поясу | `listing-empty`, `listing-error`, `profile-error` |

Що не стало патерном (менше трьох екранів): фото + галерея + назва
оголошення (`listing`, `listing-loading` — один екран у двох станах),
шторка сортування (лише `listings`).

"""Блок «Рух» на сторінках компонентів, які рухаються (DESIGN.md → «Анімація»).

Кожен приклад — живий компонент із системи: рух дає його власний CSS, тут
нічого не анімується. Підпис каже, яку роботу виконує рух
(зв'язок / статус / відповідь — animations/motion-inventory.md) і як його побачити.
"""
from _kit import (back, button, chip, composer, more, screen, sheet, stage, state,
                  tabbar, topbar_photo, photo_frame, messages_loading)


def _replay(label, inner):
    """Показати появу ще раз без JS: <details> щоразу заново вставляє вміст — анімація стартує знову."""
    return (f'<details class="doc-replay"><summary class="button button--secondary">{label}</summary>'
            f'{inner}</details>')


LEAD = ("Рух живе в компоненті, а не на екрані: що тут, те й на кожному екрані. "
        "Анімуються лише <code>transform</code> і <code>opacity</code>, лише через ролі "
        "<code>--dur-*</code> / <code>--ease-*</code> / <code>--move-*</code>; фокус і колір — миттєво. "
        "З <code>prefers-reduced-motion: reduce</code> рух вимкнено, кінцевий стан той самий.")

# slug → [(робота, як побачити, html, mod)]
MOTION = {
    "button": [
        ("відповідь", "Наведи курсор з різних боків. Темніший круг розходиться з того місця, де курсор зайшов. "
         "За <code>--dur-slow</code> (320 мс, <code>--ease-enter</code>) він накриває всю кнопку. Разом із ним літери напису "
         "хвилею зліва направо перекочуються вгору. Кожну літеру змінює її копія знизу (<code>--dur-base</code>, крок хвилі — частка "
         "<code>--dur-fast</code>).<br>Прибери курсор — круг стягується туди, куди він пішов, за <code>--dur-fast</code>, "
         "літери перекочуються назад. Натисни й тримай — темнішає ще, "
         "прозорістю за <code>--dur-fast</code>.<br>Рухаються лише масштаб шару й зсув літер усередині кнопки: колір, розмір і положення кнопки "
         "не змінюються, кінцевий вигляд — той самий напис на ролі наведення. З клавіатури й без скрипта круг росте з центру, "
         "напис стоїть; з «менше руху» — фон одразу, без круга й перекату.",
         stage(button() + button("Назад до оголошення", "secondary") + button("Скасувати", "text"), "row"), ""),
    ],
    "chip": [
        ("відповідь", "Наведи або натисни чип-кнопку — підложка проступає за <code>--dur-fast</code>. "
         "Вибраний чип не реагує: вибір — уже стан, він вмикається миттєво.",
         stage(chip("Шевченківський", tag="button") + chip("Подільський", tag="button")
               + chip("Фільтри · 3", selected=True, tag="button"), "row"), ""),
    ],
    "composer": [
        ("відповідь", "Наведи на «Надіслати» або натисни — коралова підложка темнішає за <code>--dur-fast</code>. "
         "Коли поле порожнє, кнопка приглушена; щойно стає активною — розвиднюється за той самий час, а не стрибає.",
         screen(composer("Субота о 13:00 підходить"), "bar"), "phone"),
    ],
    "topbar": [
        ("відповідь", "Наведи на «назад» чи ⋯ і натисни — кругла підложка проступає за <code>--dur-fast</code>.",
         stage(f'<header class="topbar">{back()}<p class="topbar__title">Профіль Ірини</p>{more()}</header>', "flush"), "phone"),
        ("відповідь", "Поверх фото: наведи на кнопку — затемнення густішає. Спокійний і наведений шари міняються місцями, "
         "тож кінцевий колір — точно <code>--color-over-photo-dim-hover</code>.",
         photo_frame(topbar_photo()), "phone"),
    ],
    "tabbar": [
        ("відповідь", "Натисни й тримай вкладку — капсула під іконкою проступає за <code>--dur-fast</code>. "
         "Перехід на іншу вкладку — зміна кольору, миттєва.",
         screen(tabbar("search"), "bar"), "phone"),
    ],
    "sheet": [
        ("зв'язок", "Натисни «Фільтри · 3» — затемнення проступає, панель піднімається на <code>--move-md</code> (8) знизу, "
         "за <code>--dur-slow</code> (320 мс) з <code>--ease-enter</code>: видно, що вона лягла поверх стрічки. "
         "Закривається одразу — «Скасувати», тап поза панеллю або Esc.",
         screen('<div class="shell"><div class="shell__main">' + sheet() + '</div></div>', "tall"), "phone"),
    ],
    "skeleton": [
        ("статус", "Дивись: поки дані вантажаться, блоки рівно пульсують прозорістю (півхвилі — три <code>--dur-slow</code>). "
         "Прийшов вміст — скелетона в розмітці немає, і пульс зникає разом із ним.",
         stage('<p class="sr-only" role="status">Завантажуємо повідомлення</p>' + messages_loading()), "phone"),
    ],
    "state": [
        ("статус", "Натисни «Показати стан» — він проступає на місці вмісту за <code>--dur-base</code> (200 мс), без зсуву: "
         "екран змінився з очікування на відповідь.",
         stage(_replay("Показати стан", state("listings-empty"))), "phone"),
    ],
}


def _range(token, name, what, lo, hi):
    return (f'<label class="doc-tuner__row"><span class="doc-tuner__name"><code>{token}</code> · {name}'
            f'<small>{what}</small></span>'
            f'<input type="range" min="{lo}" max="{hi}" step="10" data-token="{token}">'
            f'<output class="doc-tuner__value"></output></label>')


_CURVES = [("var(--curve-out)", "--curve-out · швидкий старт, гальмує"),
           ("var(--curve-in-out)", "--curve-in-out · розгін і гальмування"),
           ("var(--curve-in)", "--curve-in · повільний старт, різкий кінець")]


def _curve(token, name, what):
    opts = "".join(f'<option value="{v}">{t}</option>' for v, t in _CURVES)
    return (f'<label class="doc-tuner__row"><span class="doc-tuner__name"><code>{token}</code> · {name}'
            f'<small>{what}</small></span><select data-token="{token}">{opts}</select>'
            f'<output class="doc-tuner__value"></output></label>')


# Повзунки підбору: міняють ролі руху лише всередині панелі (style на .doc-tuner,
# пише docs.js) — кнопки в ній ті самі .button з системи, власного руху тут немає.
TUNER = {
    "button": [
        _range("--dur-slow", "поява круга", "скільки круг розходиться від курсора", 0, 1500),
        _curve("--ease-enter", "крива круга", "як круг розганяється й гальмує"),
        _range("--dur-base", "перекат літери", "скільки їде одна літера", 0, 1000),
        _curve("--ease-standard", "крива літер", "також крива натискання"),
        _range("--dur-fast", "швидкий рух", "натискання, стягування круга; крок хвилі = 0.12 × це значення", 0, 600),
    ],
}

TUNER_LEAD = ("<strong>Підбір.</strong> Покрути повзунки й наведи на кнопки — вони беруть нові значення ролей руху "
              "(лише в цій панелі, на екранах нічого не змінюється). Унизу — рядки для <code>tokens.css</code>: "
              "скажи «залишаємо» з цими числами, і вони підуть у токени. З увімкненим «менше руху» в системі кнопки не рухаються.")


def _tuner(slug):
    rows = TUNER.get(slug)
    if not rows:
        return ""
    demo = stage(button() + button("Назад до оголошення", "secondary") + button("Скасувати", "text")
                 + button("Застосувати фільтри", "primary", "button--block"), "row")
    return (f'<div class="doc-prose"><p>{TUNER_LEAD}</p></div>'
            f'<div class="doc-tuner" data-tuner>{demo}<div class="doc-tuner__controls">{"".join(rows)}</div>'
            '<div class="doc-tuner__foot"><pre class="doc-tuner__code" aria-live="polite"></pre>'
            '<button class="button button--secondary" type="button" data-tuner-reset>Скинути</button></div></div>')


def block(slug, variants):
    items = MOTION.get(slug)
    if not items:
        return ""
    figs = variants([(f"<strong>Робота — {job}.</strong> {how}", html, mod) for job, how, html, mod in items])
    return f'<div class="doc-prose"><p>{LEAD}</p></div>' + figs + _tuner(slug)

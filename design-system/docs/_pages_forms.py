from _kit import *

"""Сторінки документації груп «Форми», «Зворотний зв’язок» і «Чат».

Дані для _build.py: button, chip, field · state, skeleton · chat-context,
bubble, composer. Кожен приклад — жива розмітка кіта з _kit.py (канон —
ui/kit.html), обгортки — лише класи .doc-* з docs.css і класи системи.
Тексти — за microcopy.md, правила — за DESIGN.md.
"""

import re


# ── Локальні помічники (лише складання розмітки, нових класів немає) ──
def pin(html, n, at=None, cls=None):
    """Мітка анатомії: P(n) у перший тег шматка або в тег з class="cls" (перший збіг)."""
    if cls:
        key = f'class="{cls}"'
        assert key in html, key
        return html.replace(key, key + P(n, at), 1)
    return re.sub(r"^(<[\w-]+)", lambda m: m.group(1) + P(n, at), html, count=1)


def col(inner):
    """Стовпчик з ритмом екрана: shell__main дає поля 16 і проміжок 12."""
    return f'<div class="shell"><div class="shell__main">{inner}</div></div>'


def stack(inner):
    """Сцена без власних полів зі стовпчиком усередині."""
    return stage(col(inner), "flush")


def chat_screen(main, comp, mod="", top=""):
    """Чатовий екран: стрічка + fixed-пояс composer (лише всередині screen)."""
    return screen(f'<div class="shell shell--composer">{top}<div class="shell__main">{main}</div>{comp}</div>', mod)


def readonly_field(label, value):
    i = uid("f")
    return (f'<div class="field"><label class="field__label" for="{i}">{label}</label>'
            f'<input class="input" id="{i}" type="text" readonly value="{value}"></div>')


def chat_context_tatarka():
    return (chat_context()
            .replace("room-lukianivska-bedroom.jpg", "room-tatarka-sofa.jpg")
            .replace("Кімната біля Лук’янівської", "Світла кімната на Татарці")
            .replace("10 500 грн/міс · з 1 жовтня", "9 800 грн/міс · з 5 жовтня"))


# ═════════════ Форми ═════════════

BUTTON = dict(
    slug="button", name="Кнопка", group="Форми",
    api="button",
    files=["button.css", "button.js"],
    classes="<code>.button</code> · <code>--primary</code> · <code>--secondary</code> · <code>--text</code> · <code>--block</code>",
    role="Дія, яку людина робить на екрані. Коралова — головна й одна на екран, сіра — друга, текстова — тихе «Скасувати».",
    card_role="Одна коралова дія на екран, решта — сірі.",
    preview=col(button("Написати Ірині", "primary", "button--block")
                + button("Назад до оголошення", "secondary", "button--block")
                + button("Скасувати", "text")),
    preview_mod="flush",
    anatomy=dict(
        live=stage(pin(button("Написати Ірині"), 1)
                   + pin(button("Назад до оголошення", "secondary"), 2)
                   + pin(button("Скасувати", "text"), 3)
                   + pin(button("Застосувати фільтри", "primary", "button--block"), 4), "row"),
        legend=[
            (1, "Головна дія", "<code>.button--primary</code> — коралова заливка, чорнильний текст 16/500, висота 48, кути 14. Одна на екран."),
            (2, "Друга дія", "<code>.button--secondary</code> — холодна сіра поверхня; поруч із кораловою, ніколи замість неї."),
            (3, "Тиха дія", "<code>.button--text</code> — лише текст корал-чорнила; «Скасувати» в шапці шторки."),
            (4, "На всю ширину", "<code>.button--block</code> — розтягує кнопку; низ шторки фільтрів."),
        ],
    ),
    variants=[
        ("primary · звичайна", button(), ""),
        ("primary · під курсором", button(extra="is-hover"), ""),
        ("primary · натиснута", button(extra="is-active"), ""),
        ("primary · фокус", button(extra="is-focus"), ""),
        ("secondary · звичайна", button("Назад до оголошення", "secondary"), ""),
        ("secondary · під курсором", button("Назад до оголошення", "secondary", "is-hover"), ""),
        ("secondary · натиснута", button("Назад до оголошення", "secondary", "is-active"), ""),
        ("secondary · фокус", button("Назад до оголошення", "secondary", "is-focus"), ""),
        ("text · звичайна", button("Скасувати", "text"), ""),
        ("text · натиснута", button("Скасувати", "text", "is-active"), ""),
        ("text · фокус", button("Скасувати", "text", "is-focus"), ""),
        ("button--block · на всю ширину, низ шторки", button("Застосувати фільтри", "primary", "button--block"), "phone"),
    ],
    variants_lead="Усі варіанти з <code>ui/inventory.md</code>, поруч. Стани показано нерухомо класами <code>is-hover</code> / <code>is-active</code> / <code>is-focus</code>; у продукті їх дає CSS. У текстової кнопки наведення й натискання однакові — підложка <code>--color-ghost-hover</code> (на темнішій коралу бракує AA).",
    usage=("<p>Коралова <code>--primary</code> — головна дія екрана: «Написати Ірині», «Застосувати фільтри», «Змінити фільтри», «Спробувати ще». "
           "За The One Coral Button Rule вона одна на екран, а за The Coral Means Do корал стоїть лише на тому, що можна натиснути. "
           "Текст на заливці — тільки чорнилом.</p>"
           "<p>Друга дія — сіра <code>--secondary</code>: «Назад до оголошення», «Назад до результатів», «Показати ще 9». "
           "Тиха дія без заливки — <code>--text</code>: «Скасувати» в шторці. Назви дій однакові на всіх екранах — словник дій у <code>microcopy.md</code>.</p>"
           "<p>Наведення й натискання міняють лише фон — розмір і положення не рухаються (стиск 0.98 прибрано в уроці 9). Фон наведення приходить кругом із того боку, звідки зайшов курсор: точку пише <code>components/button.js</code> (його підключають екрани, документація й вітрина), без нього круг росте з центру. Той самий скрипт розбиває напис на літери (<code>.button__label</code> / <code>.button__char</code>, для читача екрана — <code>.sr-only</code> з цілим словом): на наведенні вони хвилею перекочуються вгору, кожну змінює її копія знизу. Фокус — кільце <code>--color-focus</code> товщиною <code>--stroke-2</code>.</p>"),
    sources="<code>DESIGN.md</code> → Components → Buttons, Colors → Named Rules (The One Coral Button, The Coral Means Do); <code>microcopy.md</code> → Звірка після переписування → Дії; <code>ui/inventory.md</code> → Форми",
    do=("одна коралова, друга сіра",
        stage(button("Спробувати ще") + button("Назад до оголошення", "secondary"), "row"),
        "<p>Як у <code>profile-error</code>: «Спробувати ще» — головне, що людина може зробити; повернення — сіре. Око одразу знаходить одну дію.</p>"),
    dont=("дві коралові кнопки в одному екрані",
          screen('<div class="shell shell--actionbar"><div class="shell__main">' + profile_head()
                 + button("Поскаржитися") + '</div>' + actionbar() + '</div>'),
          "<p>«Поскаржитися» коралом посеред профілю сперечається з «Написати Ірині» внизу: дві однакові заливки — жодна не головна.</p>",
          "actionbar", "одна коралова дія внизу екрана, друга — <code>--secondary</code> або в меню ⋯ «Заблокувати чи поскаржитися»."),
)


_row = chip_row()
CHIP = dict(
    slug="chip", name="Чип", group="Форми",
    api="chip",
    files=["chip.css", "chip-row.css"],
    classes="<code>.chip</code> · <code>--selected</code> · ряд — <code>.chip-row</code> &gt; <code>__track</code>",
    role="Показує активні фільтри пошуку під шапкою. Вибраний чип «Фільтри · N» відкриває шторку, решта — значення, які зараз діють.",
    card_role="Активні фільтри; «Фільтри · 3» відкриває шторку.",
    preview=col(chip_row()),
    preview_mod="flush",
    anatomy=dict(
        live=stage(pin(pin(pin(pin(_row, 5, "r"), 4, "bl", "chip-row__track"), 1, "tr", "chip chip--selected"), 3, "tr", "chip")
                   .replace("<iconify-icon", "<iconify-icon" + P(2, "bl"), 1)),
        legend=[
            (1, "Вибраний чип", "<code>.chip--selected</code> — «Фільтри · 3», заливка корал-чорнила, білий текст 5.10 : 1. Відкриває шторку — це дія."),
            (2, "Іконка", "Solar linear <code>tuning-2</code> 20, проміжок 4 до підпису."),
            (3, "Значення фільтра", "<code>.chip</code> — сіра поверхня, 36 заввишки, кути 14, 14/500; лише показ."),
            (4, "Доріжка", "<code>.chip-row__track</code> — горизонтальний скрол без смуги, проміжок 6."),
            (5, "Згасання", "<code>.chip-row::after</code> — правий край тане в колір сторінки: видно, що далі є ще."),
        ],
    ),
    variants=[
        ("значення фільтра", chip(), ""),
        ("вибраний · «Фільтри · 3»", chip(selected=True), ""),
        ("вибраний · фокус", chip(selected=True, extra="is-focus"), ""),
        ("ряд чипів зі скролом і згасанням", stage(chip_row()), "phone"),
    ],
    usage=("<p>Чипи стоять у нижньому шарі шапки результатів пошуку. Перший — вибраний «Фільтри · 3»: лічильник каже, скільки умов діє, а тап відкриває шторку з полями. "
           "Його колір — корал-чорнило, не світлий корал: світлий лишається за кнопкою дії (The One Coral Button Rule).</p>"
           "<p>Решта — значення фільтрів: «Шевченківський», «до 12 000 грн», «з 1 жовтня». Вони лише показують, що діє; змінюють їх у шторці. "
           "Ряд скролиться вбік, правий край згасає.</p>"),
    sources="<code>DESIGN.md</code> → Components → Chips, Colors → Named Rules (The Coral Means Do); <code>microcopy.md</code> → Результати пошуку; <code>ui/inventory.md</code> → Форми",
    do=("фільтри, що діють, — у ряду",
        stage(chip_row()),
        "<p>Людина бачить умови пошуку без шторки, а «Фільтри · 3» веде туди, де їх змінити.</p>"),
    dont=("чип як головна дія",
          stage(profile_head() + '<a class="chip chip--selected" href="#">Написати Ірині</a>'),
          "<p>Чип 36 читається як фільтр, а не як крок до контакту: головна дія губиться й не має висоти 48.</p>",
          "button", "головна дія — <code>.button--primary</code> «Написати Ірині», одна на екран."),
)


FIELD = dict(
    slug="field", name="Поле", group="Форми",
    api="field",
    files=["field.css"],
    classes="<code>.field</code> · <code>__label</code> · <code>.input</code> на <code>select</code> / <code>input</code>",
    role="Умова пошуку з видимим підписом у шторці фільтрів: район, бюджет, дата заїзду.",
    card_role="Умова пошуку з підписом: район, бюджет, дата.",
    preview=col(field("select") + field("number")),
    preview_mod="flush",
    anatomy=dict(
        live=stack(pin(pin(field("select"), 1, "tr"), 2, "tr", "field__label").replace('<select class="input"', '<select class="input"' + P(3, "r"), 1)
                   + field("date").replace('<input class="input"', '<input class="input"' + P(4, "r"), 1)),
        legend=[
            (1, "Поле", "<code>.field</code> — підпис над полем, проміжок 4."),
            (2, "Підпис", "<code>.field__label</code> — 14/500 чорнилом, завжди видимий (не плейсхолдер)."),
            (3, "Список", "<code>select.input</code> — сіра поверхня, рамка 1 <code>field-edge</code> (3.1:1), висота 48, кути 14."),
            (4, "Дата тільки для читання", "<code>input.input[readonly]</code> з <code>inputmode=\"none\"</code> — значення обирають, а не набирають."),
        ],
    ),
    variants=[
        ("список · select", field("select"), "field"),
        ("число · inputmode=\"numeric\"", field("number"), "field"),
        ("дата, тільки для читання", field("date"), "field"),
        ("під курсором — рамка темніє", field("number", "is-hover"), "field"),
        ("фокус — зелене кільце 2", field("number", "is-focus"), "field"),
    ],
    usage=("<p>Поля живуть у шторці «Фільтри»: «Район Києва» — список, «Бюджет до, грн/місяць» — число з цифровою клавіатурою, «Дата заїзду» — значення тільки для читання. "
           "Підпис завжди над полем і названий так, як людина думає про умову; одиниці — у підписі, не в значенні.</p>"
           "<p>Рамка 1 <code>field-edge</code> тримає 3.1:1 до сірої поверхні — поле читається як поле (правка уроку 7). Під курсором рамка темніє, фокус — зелене кільце.</p>"),
    sources="<code>DESIGN.md</code> → Components → Inputs / Fields, Правки уроку 7; <code>microcopy.md</code> → Результати пошуку (шторка фільтрів); <code>ui/inventory.md</code> → Форми",
    do=("умови пошуку в шторці",
        stack(field("select") + field("number") + field("date")),
        "<p>Три умови — три типи вводу: вибір зі списку, число, дата. Кожна має видимий підпис.</p>"),
    dont=("readonly-поля для значень профілю",
          stack(readonly_field("Куріння", "не курить") + readonly_field("Тварини", "кіт у квартирі") + readonly_field("Гості", "за домовленістю")),
          "<p>Рамки й висота 48 кажуть «заповни мене», а людина лише читає факти про Ірину. Поля без вводу — шум і зайві зупинки для читача екрана.</p>",
          "group", "факти «назва — значення» у згрупованому списку: читаються одним поглядом, нічого не вдають."),
)


# ═════════════ Зворотний зв’язок ═════════════

_STATE_CAPS = {
    "listings-empty": "порожньо · listings-empty",
    "chat-empty": "порожньо без кнопки · chat-empty",
    "listing-empty": "знято · listing-empty",
    "chat-error": "помилка, одна дія · chat-error",
    "profile-error": "помилка, дві дії · profile-error",
}

STATE = dict(
    slug="state", name="Стан", group="Зворотний зв’язок",
    api="state",
    files=["state.css"],
    classes="<code>.state</code> · <code>--error</code> · <code>__icon</code> <code>__title</code> <code>__text</code> <code>__actions</code>",
    role="Пояснює по центру екрана, чому тут порожньо, що оголошення зняли або що не вдалося завантажити, — і що зробити далі.",
    card_role="Порожньо, знято чи помилка — і що робити далі.",
    preview=('<section class="state"><div class="state__icon">' + ico("streamline-freehand:search-magnifier")
             + '</div><h3 class="state__title">За цими умовами оголошень немає</h3></section>'),
    preview_mod="center",
    anatomy=dict(
        live=stage(pin(pin(pin(pin(pin(state("listings-empty"), 1, "tl"), 2, "tr", "state__icon"), 3, "l", "state__title"),
                           4, "l", "state__text"), 5, "bl", "state__actions")),
        legend=[
            (1, "Стан", "<code>.state</code> — по центру вільного екрана, без підкладки; у помилці — <code>--error</code> і <code>role=\"alert\"</code>."),
            (2, "Іконка", "<code>.state__icon</code> — мальована Streamline Freehand 72; у помилці червона."),
            (3, "Заголовок", "<code>.state__title</code> — 19/700, чому так: «За цими умовами оголошень немає»."),
            (4, "Пояснення", "<code>.state__text</code> — <code>muted</code>, що можна зробити."),
            (5, "Дії", "<code>.state__actions</code> — одна коралова, друга (якщо є) сіра; у <code>chat-empty</code> кнопки немає."),
        ],
    ),
    variants=[(_STATE_CAPS[k], stage(state(k)), "phone") for k in STATES],
    usage=("<p>Стан займає вільне місце між шапкою й нижнім поясом. Заголовок каже, що сталося, пояснення — що робити, кнопка — головна дія: "
           "«Змінити фільтри», «Назад до результатів», «Спробувати ще». Помилка завжди звучить однаково: «Не вдалося завантажити {оголошення / профіль / повідомлення}» "
           "і «Перевір з’єднання й спробуй ще.»</p>"
           "<p>У порожньому чаті кнопки немає — дія вже є внизу, в полі повідомлення. Якщо дій дві, друга сіра (The One Coral Button Rule). "
           "Тон спокійний: без «Ой», окликів і емодзі.</p>"),
    sources="<code>DESIGN.md</code> → Components → Стани; <code>microcopy.md</code> → Розбіжності → E, Звірка після переписування → Дії; <code>ui/inventory.md</code> → Зворотний зв’язок",
    do=("порожньо — і чому",
        stage(state("chat-empty")),
        "<p>Людина розуміє, що розмова ще не почалась, і знає, що написати першим повідомленням.</p>"),
    dont=("стан для завантаження",
          stage('<section class="state"><div class="state__icon">' + ico("streamline-freehand:messages-bubble-smile")
                + '</div><h3 class="state__title">Завантажуємо повідомлення</h3><p class="state__text">Зачекай кілька секунд.</p></section>'),
          "<p>Велика іконка й заголовок на мить, поки вантажиться, — екран смикається, коли дані приходять, і нічого не каже про форму вмісту.</p>",
          "skeleton", "сірі блоки у формі майбутніх повідомлень і невидимий <code>role=\"status\"</code> «Завантажуємо повідомлення»."),
)


SKELETON = dict(
    slug="skeleton", name="Скелетон", group="Зворотний зв’язок",
    api="skeleton",
    files=["skeleton.css"],
    classes=("<code>.skeleton</code> · <code>--title</code> <code>--line</code> <code>--w60</code> <code>--w40</code> <code>--photo</code> <code>--button</code> "
             "<code>--avatar</code> <code>--avatar-lg</code> <code>--bubble</code> <code>--bubble-tall</code> <code>--bubble-short</code> <code>--mine</code> "
             "<code>--section</code> · <code>.skeleton-stack</code> <code>.skeleton-person</code> <code>__text</code>"),
    role="Сірий блок у формі майбутнього вмісту, поки дані вантажаться. Поруч — невидимий для очей статус «Завантажуємо …».",
    card_role="Форма майбутнього вмісту, поки дані вантажаться.",
    preview=col(person_row_loading()
                + '<div class="skeleton-stack" aria-hidden="true"><div class="skeleton skeleton--title"></div><div class="skeleton skeleton--line"></div>'
                  '<div class="skeleton skeleton--line skeleton--w60"></div></div>'),
    preview_mod="flush",
    anatomy=dict(
        live=stack('<p class="sr-only" role="status">Завантажуємо профіль</p>'
                   + pin(pin(pin(profile_head(loading=True), 1, "tr", "skeleton skeleton--avatar-lg"), 2, "r", "skeleton skeleton--title"),
                         3, "r", "skeleton skeleton--line skeleton--w60")
                   + pin(group_loading(), 4, "tr")
                   + pin('<div class="skeleton skeleton--button" aria-hidden="true"></div>', 5, "r")),
        legend=[
            (1, "Аватар", "<code>.skeleton--avatar-lg</code> — коло 84 на місці фото профілю."),
            (2, "Заголовок", "<code>.skeleton--title</code> — смужка 16 на 70% ширини."),
            (3, "Рядок", "<code>.skeleton--line</code> 12; ширину вкорочують <code>--w60</code> / <code>--w40</code>."),
            (4, "У сірому списку", "<code>.group .skeleton</code> — смужка всередині справжнього <code>group__row</code> 48, на тон темніша."),
            (5, "Кнопка", "<code>.skeleton--button</code> — 48, кути 14; на місці «Написати Ірині»."),
        ],
    ),
    variants=[
        ("рядки · --title, --line, --w60, --w40",
         stage('<div class="skeleton-stack" aria-hidden="true"><div class="skeleton skeleton--title"></div><div class="skeleton skeleton--line"></div>'
               '<div class="skeleton skeleton--line skeleton--w60"></div><div class="skeleton skeleton--line skeleton--w40"></div></div>'), "phone"),
        ("фото · --photo — картка оголошення", stage(card_list(listing_card_loading(), hidden=True)), "phone"),
        ("кнопка · --button", stage('<div class="skeleton skeleton--button" aria-hidden="true"></div>'), "phone"),
        ("аватари · --avatar, --avatar-lg",
         stage('<div class="skeleton skeleton--avatar" aria-hidden="true"></div><div class="skeleton skeleton--avatar-lg" aria-hidden="true"></div>', "row"), ""),
        ("бульбашки · --bubble, --bubble-tall, --bubble-short, --mine", stage(messages_loading()), "phone"),
        ("людина · .skeleton-person", stage(person_row_loading()), "phone"),
        ("у сірому списку · .group .skeleton", stage(group_loading()), "phone"),
        ("фото, карусель і назва · .skeleton, .skeleton-stack",
         stage(photo_top(hero_photo(loading=True) + gallery(loading=True) + listing_title(loading=True)), "flush"), "phone"),
    ],
    usage=("<p>Скелетон стоїть на чотирьох екранах завантаження — <code>listings-loading</code>, <code>listing-loading</code>, <code>profile-loading</code>, "
           "<code>chat-loading</code> — і повторює форму того, що прийде: фото 4:3, рядки, аватар, бульбашки. Екран не смикається, коли дані з’являються.</p>"
           "<p>Блоки приховані від читача екрана (<code>aria-hidden</code>); натомість поруч один <code>role=\"status\"</code> зі словника: "
           "«Завантажуємо {оголошення / профіль / повідомлення}». Іконки в завантаженні немає — це свідоме рішення дизайнера.</p>"),
    sources="<code>DESIGN.md</code> → Components → Стани, Правки уроку 7 (скелетон у списку, скелетон людини); <code>microcopy.md</code> → Звірка після переписування → Статус завантаження; <code>ui/inventory.md</code> → Зворотний зв’язок",
    do=("форма майбутніх повідомлень",
        stage('<p class="sr-only" role="status">Завантажуємо повідомлення</p>' + messages_loading()),
        "<p>Як у <code>chat-loading</code>: три бульбашки на своїх боках — людина вже бачить, що тут буде розмова, а читач екрана чує статус.</p>"),
    dont=("скелетон замість відсутнього вмісту",
          stack(results_meta("0 оголошень") + card_list(listing_card_loading(), hidden=True)),
          "<p>Оголошень немає, а екран далі «вантажиться»: людина чекає того, що не прийде, і не знає, що змінити.</p>",
          "state", "«За цими умовами оголошень немає» з поясненням і кнопкою «Змінити фільтри»."),
)


# ═════════════ Чат ═════════════

CHAT_CONTEXT = dict(
    slug="chat-context", name="Контекст чату", group="Чат",
    api="chat-context",
    files=["chat-context.css"],
    classes="<code>.chat-context</code> · <code>__thumb</code> <code>__text</code> <code>__title</code> <code>__meta</code> · <code>.chevron</code>",
    role="Картка кімнати над розмовою: нагадує, про яке оголошення йдеться, і веде назад до нього.",
    card_role="Про яку кімнату розмова — і шлях до оголошення.",
    preview=col(chat_context() + messages(MESSAGES[:1])),
    preview_mod="flush",
    anatomy=dict(
        live=stage(pin(pin(pin(pin(pin(chat_context(), 1, "bl"), 2, "tl", "chat-context__thumb"), 3, "t", "chat-context__title"),
                           4, "b", "chat-context__meta"), 5, "r", "chevron")),
        legend=[
            (1, "Картка-посилання", "<code>.chat-context</code> — сіра поверхня, кути 14; уся картка веде на оголошення."),
            (2, "Мініатюра", "<code>.chat-context__thumb</code> — фото кімнати 48, кути 8."),
            (3, "Назва", "<code>.chat-context__title</code> — 14/500, обрізається трьома крапками; назву пише автор."),
            (4, "Ціна й дата", "<code>.chat-context__meta</code> — 12 <code>muted</code>: «10 500 грн/міс · з 1 жовтня»."),
            (5, "Шеврон", "<code>.chevron</code> — Solar linear 16: картка кудись веде."),
        ],
    ),
    variants=[
        ("звичайна", chat_context(), "phone"),
        ("фокус", chat_context("is-focus"), "phone"),
    ],
    usage=("<p>Стоїть першою в стрічці на всіх екранах чату — <code>chat</code>, <code>chat-loading</code>, <code>chat-empty</code>, <code>chat-error</code>. "
           "Людина може писати кільком господарям одразу, тож картка відповідає на «про яку кімнату ми говоримо?» без виходу з розмови.</p>"
           "<p>Дані ті самі, що на бирці й в оголошенні: «Кімната біля Лук’янівської», «10 500 грн/міс · з 1 жовтня». Тап веде на оголошення — "
           "як «Назад до оголошення» в шапці, але через саму кімнату.</p>"),
    sources="<code>DESIGN.md</code> → Components → Чат; <code>microcopy.md</code> → Чат (C-03, C-05, C-06); <code>ui/inventory.md</code> → Чат",
    do=("кімната над розмовою",
        chat_screen(chat_context() + messages(MESSAGES[:2]), composer(disabled=True), top=topbar_person()),
        "<p>Людина, ім’я й кімната — в одному погляді: шапка каже з ким, картка — про що.</p>"),
    dont=("chat-context у стрічці пошуку замість картки",
          stack(results_meta() + chat_context() + chat_context_tatarka()),
          "<p>Мініатюра 48 не показує кімнату, бирки з ціною немає, а саме фото — головне, з чого людина обирає оголошення.</p>",
          "listing-card", "у стрічці — картка оголошення з фото 4:3 і биркою ціни; chat-context — лише над розмовою."),
)


_m = MESSAGES
BUBBLE = dict(
    slug="bubble", name="Повідомлення", group="Чат",
    api="bubble", detect="bubble",
    files=["bubble.css"],
    classes="<code>.messages</code> &gt; <code>.bubble</code> · <code>--mine</code> · <code>__time</code>",
    role="Одне повідомлення в стрічці чату з часом. Мої — чорнило, чужі — сіра поверхня; хвостик 4 біля автора.",
    card_role="Повідомлення з часом: моє — чорнило, чуже — сіре.",
    preview=col(messages(MESSAGES[2:])),
    preview_mod="flush",
    anatomy=dict(
        live=stage(f'<ol class="messages"{P(1, "tr")}>'
                   f'<li class="bubble"{P(2, "tr")}><p{P(5, "bl")}>{_m[1][1]}</p><time class="bubble__time" datetime="2026-09-18T{_m[1][2]}">{_m[1][2]}</time></li>'
                   f'<li class="bubble bubble--mine"{P(3, "tl")}><p>{_m[2][1]}</p><time class="bubble__time"{P(4, "br")} datetime="2026-09-18T{_m[2][2]}">{_m[2][2]}</time></li>'
                   f'<li class="bubble"><p>{_m[3][1]}</p><time class="bubble__time" datetime="2026-09-18T{_m[3][2]}">{_m[3][2]}</time></li>'
                   '</ol>'),
        legend=[
            (1, "Стрічка", "<code>.messages</code> — нумерований список; 12, коли змінюється мовець, 4 — між повідомленнями того самого."),
            (2, "Чуже", "<code>.bubble</code> — сіра поверхня, кути 18, хвостик 4 унизу ліворуч, до 78% ширини."),
            (3, "Моє", "<code>.bubble--mine</code> — чорнило з білим текстом, праворуч, хвостик унизу праворуч."),
            (4, "Час", "<code>.bubble__time</code> — 12 у <code>&lt;time&gt;</code>; на чорнилі — свій приглушений колір."),
            (5, "Текст людини", "<code>.bubble &gt; p</code> — пише користувач; ми його не переписуємо."),
        ],
    ),
    variants=[
        ("чуже", stage(messages(MESSAGES[1:2])), "phone"),
        ("моє · --mine", stage(messages(MESSAGES[:1])), "phone"),
        ("ритм стрічки — 12 при зміні мовця", stage(messages()), "phone"),
        ("завантаження · скелетон", stage(messages_loading()), "phone"),
    ],
    usage=("<p>Бульбашки складають стрічку на екрані <code>chat</code> — третій крок core loop, прямий контакт. Мої повідомлення праворуч чорнилом, Іринині — "
           "ліворуч на сірій поверхні: хто що сказав, видно без підписів. Коралу в стрічці немає — повідомлення не дія (The Coral Means Do).</p>"
           "<p>Текст у бульбашці — рядок користувача (👤 у <code>microcopy.md</code>): «Вітаю! Чи актуальна кімната…» лишається як написано, "
           "навіть з окликом. Поки стрічка вантажиться — скелетон із трьох бульбашок.</p>"),
    sources="<code>DESIGN.md</code> → Components → Чат, Правки уроку 7 (ритм 4/12); <code>microcopy.md</code> → Чат (C-09…C-13), Розбіжності → 👤; <code>ui/inventory.md</code> → Чат",
    do=("розмова, як вона була",
        stage(messages(MESSAGES[:2])),
        "<p>Питання й відповідь на своїх боках, час під кожним — людина відтворює домовленість без жодного службового тексту.</p>"),
    dont=("помилка завантаження як бульбашка",
          stage(messages([(False, "Не вдалося завантажити повідомлення. Спробувати ще", "18:40")])),
          "<p>Збій виглядає як репліка Ірини: людина може вирішити, що це написала вона, а кнопки повторити немає.</p>",
          "state", "«Не вдалося завантажити повідомлення» по центру з червоною іконкою, <code>role=\"alert\"</code> і кнопкою «Спробувати ще»."),
)


_comp_anat = pin(pin(pin(composer("Дякую, до зустрічі в суботу о 13:00."), 1, "tr", "composer"), 2, "tl", "composer__input"), 3, "tr", "composer__send")
COMPOSER = dict(
    slug="composer", name="Поле повідомлення", group="Чат",
    api="composer",
    files=["composer.css"],
    classes="<code>.composer</code> · <code>__input</code> <code>__send</code> · оболонка <code>.shell--composer</code>",
    role="Білий пояс унизу чату: поле повідомлення Ірині й кругла «Надіслати». Коралова лише тоді, коли є що надіслати.",
    card_role="Поле повідомлення й «Надіслати» внизу чату.",
    preview=('<div class="shell shell--composer"><div class="shell__main">' + messages(MESSAGES[3:]) + '</div>'
             + composer("Дякую, до зустрічі в суботу о 13:00.") + '</div>'),
    preview_mod="flush",
    anatomy=dict(
        live=screen('<div class="shell shell--composer"><div class="shell__main"' + P(4, "tl") + '>' + messages(MESSAGES[2:]) + '</div>'
                    + _comp_anat + '</div>'),
        legend=[
            (1, "Пояс", "<code>.composer</code> — fixed унизу, папір, лінія 1 зверху, поля 12/16."),
            (2, "Поле", "<code>.composer__input</code> — <code>textarea</code> 48, росте з текстом до 112; підпис «Повідомлення Ірині» — для читача екрана."),
            (3, "Надіслати", "<code>.composer__send</code> — коло 48, корал, Solar <code>plain-2</code> 20; без тексту — <code>disabled</code>, приглушена <code>--opacity-disabled</code> (0.4) і поза Tab."),
            (4, "Резерв під пояс", "<code>.shell--composer</code> — нижнє поле 76, щоб останнє повідомлення не ховалось під поясом."),
        ],
    ),
    variants=[
        ("з текстом — «Надіслати» активна", screen(composer("Вітаю! Чи актуальна кімната?"), "bar"), "phone"),
        ("фокус у полі · «Надіслати» під курсором",
         screen(composer("Чи можна подивитися кімнату в суботу?", input_extra="is-focus", send_extra="is-hover"), "bar"), "phone"),
        ("неактивна · поле порожнє, розмова вантажиться або не завантажилась", screen(composer(disabled=True), "bar"), "phone"),
    ],
    usage=("<p>Пояс стоїть на всіх екранах чату й тримається внизу над клавіатурою. Плейсхолдер — «Повідомлення», кнопка — «Надіслати» (словник дій). "
           "Перше повідомлення людина пише сама: порожній стан підказує «Представся й запитай, чи кімната ще вільна…».</p>"
           "<p>«Надіслати» коралова, лише коли в полі є текст. Якщо поле порожнє, розмова вантажиться чи не завантажилась, кнопка має "
           "<code>disabled</code> і прозорість 0.4. На <code>chat-error</code> коралова дія одна — «Спробувати ще» (правка уроку 7, The One Coral Button Rule).</p>"),
    sources="<code>DESIGN.md</code> → Components → Buttons (Send), Inputs / Fields, Правки уроку 7 і 8; <code>microcopy.md</code> → Чат (C-15…C-17, C-23, C-29); <code>ui/inventory.md</code> → Чат",
    do=("на помилці «Надіслати» мовчить",
        chat_screen(state("chat-error"), composer(disabled=True), "tall"),
        "<p>Розмова не завантажилась — коралова лише «Спробувати ще», «Надіслати» приглушена. Чернетку збережено, людина нічого не втратила.</p>"),
    dont=("composer для не-чатового вводу",
          screen(composer("12000").replace("Повідомлення Ірині", "Бюджет до, грн/місяць")
                 .replace(' placeholder="Повідомлення"', ' placeholder="Бюджет до, грн/місяць"')
                 .replace('aria-label="Надіслати"', 'aria-label="Застосувати фільтри"'), "bar"),
          "<p>Бюджет у поясі чату без видимого підпису й з літачком «надіслати»: незрозуміло, що вводити й куди воно піде, а цифрова клавіатура не відкривається.</p>",
          "field", "поле з видимим підписом «Бюджет до, грн/місяць» і <code>inputmode=\"numeric\"</code> у шторці фільтрів."),
)


PAGES = [BUTTON, CHIP, FIELD, STATE, SKELETON, CHAT_CONTEXT, BUBBLE, COMPOSER]

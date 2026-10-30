"""Сторінки груп «Оболонка» і «Навігація»: shell, topbar, header, tabbar, actionbar, sheet."""

from _kit import *


def _shell(mods, top, main, bottom="", pin_main=""):
    return f'<div class="shell {mods}">{top}<div class="shell__main"{pin_main}>{main}</div>{bottom}</div>'


def _listings_screen(pins=False):
    p = (lambda n: P(n)) if pins else (lambda n: "")
    head = header().replace('<header class="header">', f'<header class="header"{p(1)}>', 1)
    bar = tabbar().replace('<nav class="tabbar"', f'<nav class="tabbar"{p(3)}', 1)
    return _shell("shell--header shell--tabbar", head, results_meta() + card_list(listing_card()), bar, p(2))


def _profile_screen(pins=False, bottom=None):
    p = (lambda n: P(n)) if pins else (lambda n: "")
    top = topbar().replace('<header class="topbar">', f'<header class="topbar"{p(1)}>', 1)
    bar = actionbar() if bottom is None else bottom
    if pins:
        bar = bar.replace('<div class="actionbar"', f'<div class="actionbar"{p(3)}', 1)
    return _shell("shell--actionbar", top, profile_head() + section_title() + group(LIFESTYLE[:3]), bar, p(2))


def _listing_screen():
    main = hero_photo() + listing_title() + section_title("Про квартиру") + group(FLAT)
    return ('<div class="shell shell--photo-top shell--actionbar doc-frame">' + topbar_photo()
            + f'<div class="shell__main">{main}</div>' + actionbar() + '</div>')


def _chat_screen():
    return _shell("shell--composer", topbar_person(), chat_context() + messages(MESSAGES[:2]), composer())


PAGES = [
    dict(
        slug="shell", name="Оболонка екрана", group="Оболонка", api="shell",
        files=["shell.css", "base.css"],
        classes="<code>.shell</code> · <code>__main</code> · <code>--header</code> <code>--tabbar</code> <code>--actionbar</code> <code>--composer</code> <code>--photo-top</code>",
        role="Каркас кожного екрана: шапка зверху, одна колонка вмісту і рівно один закріплений пояс знизу. Модифікатор називає цей пояс і резервує під нього місце.",
        card_role="Каркас: шапка, колонка вмісту, один нижній пояс.",
        preview=screen(_listings_screen()), preview_mod="flush",
        anatomy=dict(live=screen(_profile_screen(pins=True), "tall"), legend=[
            (1, "Шапка", "<code>.topbar</code> або <code>.header</code> — компактна 48 на деталях, велика на стрічці"),
            (2, "Вміст", "<code>.shell__main</code> — одна колонка, поля 16, між блоками 12"),
            (3, "Нижній пояс", "<code>.actionbar</code>, <code>.tabbar</code> або <code>.composer</code> — завжди один; <code>.shell--actionbar</code> резервує під нього висоту"),
        ]),
        variants_lead="Чотири поєднання верху й низу, що стоять на 16 екранах.",
        variants=[
            ("<code>shell--header shell--tabbar</code> · listings*", screen(_listings_screen(), "tall"), "phone"),
            ("<code>shell--actionbar</code> · profile*", screen(_profile_screen(), "tall"), "phone"),
            ("<code>shell--photo-top shell--actionbar</code> · listing*", screen(_listing_screen(), "tall"), "phone"),
            ("<code>shell--composer</code> · chat*", screen(_chat_screen(), "tall"), "phone"),
        ],
        usage=("<p>Кожен новий екран починається з оболонки: копіюєш <code>ui/shell.html</code> і заповнюєш <code>.shell__main</code>. "
               "Mobile-first, базовий viewport 390×844, одна колонка, бокові поля 16, горизонтального скролу сторінки немає.</p>"
               "<p>Нижній пояс — там, де великий палець. Стрічка має нижнє меню (людина переходить між розділами), оголошення й профіль — "
               "панель з однією кораловою дією «Написати Ірині», чат — поле повідомлення. Усі пояси враховують <code>safe-area-inset-bottom</code>. "
               "Оголошення починається з фото на всю ширину, яке заходить під статус-бар, — для цього <code>--photo-top</code> знімає верхнє поле.</p>"),
        sources="<code>DESIGN.md</code> → Layout; <code>ui/shell.html</code>; <code>ui/inventory.md</code> → Навігація",
        do=("один пояс знизу", screen(_profile_screen(), "tall"),
            "<p>Профіль: компактна шапка, вміст, одна панель дії. Людина знає, що робити далі, і кнопка під пальцем.</p>"),
        dont=("меню і панель дії разом",
              screen(_shell("shell--tabbar", topbar(), profile_head(), actionbar() + tabbar()), "tall"),
              "<p>Два закріплені пояси з’їдають висоту і змагаються за палець: панель дії налазить на меню, а коралова кнопка губиться поруч із навігацією.</p>",
              "actionbar", "на деталях лишається тільки панель дії; меню — на стрічці."),
    ),

    dict(
        slug="topbar", name="Компактна шапка", group="Навігація", api="topbar",
        files=["topbar.css"],
        classes="<code>.topbar</code> · <code>__back</code> <code>__title</code> <code>__action</code> <code>__person</code> <code>__name</code> <code>__verified</code> · <code>--person</code> <code>--over-photo</code>",
        role="App bar 48 на деталях: стрілка «назад», заголовок або людина і ⋯ «Заблокувати чи поскаржитися». Тримає людину в ланцюжку пошук → оголошення → профіль → чат.",
        card_role="App bar 48: назад, заголовок або людина, ⋯.",
        preview=stage(topbar(), "flush"), preview_mod="flush center",
        anatomy=dict(live=stage(
            '<header class="topbar">' + back(pin=P(1)) + f'<p class="topbar__title"{P(2)}>Профіль Ірини</p>' + more(P(3, "tr")) + '</header>'
            + '<header class="topbar topbar--person">' + back()
            + f'<a class="topbar__person"{P(4)} href="#">{avatar(mark=False, alt="Фото профілю Ірини")}<strong class="topbar__name">Ірина</strong>'
            + f'<span class="topbar__verified"{P(5, "tr")} title="Номер підтверджено 12 вересня">{ico("solar:shield-check-linear")}<span class="sr-only">Номер підтверджено</span></span></a>'
            + more() + '</header>', "flush"), legend=[
            (1, "Назад", "<code>.topbar__back</code> — Solar 24, підпис для скрінрідера: «Назад до оголошення» / «Назад до результатів»"),
            (2, "Заголовок", "<code>.topbar__title</code> — 16/700; <code>h1</code>, якщо нижче немає власного"),
            (3, "Дія ⋯", "<code>.topbar__action</code> — «Заблокувати чи поскаржитися»; у чаті, профілі й оголошенні"),
            (4, "Людина", "<code>.topbar__person</code> — аватар 28 + ім’я, посилання на профіль (<code>--person</code>, чат)"),
            (5, "Щит перевірки", "<code>.topbar__verified</code> — зелений щит 20 замість позначки на аватарі"),
        ]),
        variants=[
            ("із заголовком · profile*", stage(topbar(), "flush"), "phone"),
            ("«Назад» у фокусі", stage(topbar().replace('class="topbar__back"', 'class="topbar__back is-focus"', 1), "flush"), "phone"),
            ("<code>--person</code> · chat*", stage(topbar_person(), "flush"), "phone"),
            ("<code>--over-photo</code> · listing — круглі кнопки на затемненні з розмиттям", photo_frame(topbar_photo()), "phone"),
        ],
        usage=("<p>Компактна шапка стоїть на всіх екранах-деталях: оголошення, профіль, чат (12 сторінок). Стрілка завжди веде на крок назад і "
               "каже куди: «Назад до результатів», «Назад до оголошення» — одна назва для однієї дії на всіх екранах (D1, D2).</p>"
               "<p>У чаті замість заголовка — людина: аватар, ім’я і зелений щит «Номер підтверджено 12 вересня». Праворуч ⋯ «Заблокувати чи поскаржитися» — "
               "report і block входять у MVP, бо прямий чат без match-гейту без них небезпечний. Поверх фото кнопки круглі на затемненні, щоб їх було видно на будь-якому знімку.</p>"),
        sources="<code>DESIGN.md</code> → Components → Navigation; <code>microcopy.md</code> → D1, D2, D8, «Звірка після переписування»; <code>CLAUDE.md</code> → Довіра",
        do=("деталь із дорогою назад", stage(topbar(), "flush"),
            "<p>Профіль відкрився з оголошення — стрілка повертає туди ж, заголовок каже, де людина зараз.</p>"),
        dont=("стрілка на верхньому рівні",
              stage(topbar("Результати пошуку", "Назад"), "flush"),
              "<p>«Результати пошуку» — перший екран, повертатися нікуди. Стрілка без мети лише бреше про ієрархію.</p>",
              "header", "на стрічці — велика шапка із заголовком і смугою чипів."),
    ),

    dict(
        slug="header", name="Велика шапка", group="Навігація", api="header",
        files=["header.css"],
        classes="<code>.header</code> · <code>__top</code> <code>__title</code> <code>__subtitle</code> · під нею — <code>.chip-row</code> у <code>.shell__main</code>",
        role="Шапка стрічки: заголовок і підзаголовок; одразу під нею, першим блоком <code>.shell__main</code>, — смуга чипів із фільтрами. Каже, де людина, і дає змінити умови пошуку без зайвого екрана.",
        card_role="Шапка стрічки: заголовок, підзаголовок, смуга чипів.",
        preview=stage(header(), "flush"), preview_mod="flush",
        anatomy=dict(live=stage(
            '<header class="header"><div class="header__top">'
            f'<h3 class="header__title"{P(1)}>Результати пошуку</h3><p class="header__subtitle"{P(2)}>Київ · кімнати та співмешканці</p></div>'
            f'</header><div class="shell__main"{P(3, "bl")}>{chip_row()}</div>', "flush"), legend=[
            (1, "Заголовок", "<code>.header__title</code> — назва екрана"),
            (2, "Підзаголовок", "<code>.header__subtitle</code> — місто й що шукаємо, <code>muted</code>"),
            (3, "Смуга чипів", "<code>.chip-row</code> — перший блок <code>.shell__main</code>, не частина шапки (так на всіх listings*): «Фільтри · N» і активні значення; скролиться сама"),
        ]),
        variants_lead="Станів немає; на екранах під шапкою завжди стоїть смуга чипів.",
        variants=[
            ("перший шар — <code>.header__top</code>", stage(header(bar=False), "flush"), "phone"),
            ("з чипами під нею — listings*", stage(header(), "flush"), "phone"),
        ],
        usage=("<p>Велика шапка — лише на стрічці «Результати пошуку» (listings*). Перший крок core loop — пошук за фільтрами, тож фільтри живуть просто в шапці: "
               "чип «Фільтри · 3» відкриває шторку, решта чипів показують, що саме ввімкнено (район, бюджет, дата заїзду).</p>"
               "<p>Назви фільтрів — за словником: «Бюджет», «Дата заїзду», «з 1 жовтня» (T6, T7). Під шапкою — підсумок «12 оголошень».</p>"),
        sources="<code>DESIGN.md</code> → Layout; <code>microcopy.md</code> → D7, T6, T7; <code>ui/inventory.md</code> → Навігація",
        do=("заголовок стрічки з фільтрами", stage(header(), "flush"),
            "<p>Людина бачить, де вона і за якими умовами шукає, і може змінити їх одним тапом.</p>"),
        dont=("велика шапка на деталі",
              stage('<header class="header"><div class="header__top"><h3 class="header__title">Кімната біля Лук’янівської</h3>'
                    '<p class="header__subtitle">Шевченківський район · з 1 жовтня</p></div></header>', "flush"),
              "<p>На оголошенні немає дороги назад і ⋯, а назва кімнати дублює те, що має стояти під фото.</p>",
              "topbar", "компактна шапка над фото, назва — у <code>listing-title</code>."),
    ),

    dict(
        slug="tabbar", name="Нижнє меню", group="Навігація", api="tabbar",
        files=["tabbar.css"],
        classes="<code>.tabbar</code> · <code>__list</code> <code>__item</code> · активний — <code>aria-current=\"page\"</code>",
        role="Три розділи продукту — Пошук, Чати, Профіль — під великим пальцем. Білий пояс із хвилею і великими мальованими іконками: найпомітніша «рука» в системі.",
        card_role="Пошук · Чати · Профіль, мальовані іконки й хвиля.",
        preview=screen(tabbar(), "bar"), preview_mod="flush",
        anatomy=dict(live=screen(
            f'<nav class="tabbar"{P(1, "t")} aria-label="Приклад нижнього меню"><ul class="tabbar__list">'
            f'<li><a class="tabbar__item" href="#" aria-current="page"{P(2)}>{ico("streamline-freehand:search-magnifier")}<span>Пошук</span></a></li>'
            f'<li><a class="tabbar__item" href="#"{P(3)}>{ico("streamline-freehand:messages-bubble-smile")}<span>Чати</span></a></li>'
            f'<li><span class="tabbar__item"{P(4)}>{ico("streamline-freehand:smiley-happy")}<span>Профіль</span></span></li>'
            '</ul></nav>', "bar"), legend=[
            (1, "Пояс із хвилею", "<code>.tabbar</code> — білий, хвиля зверху маскою <code>--wave-mask</code>, fixed + safe-area"),
            (2, "Активний пункт", "<code>aria-current=\"page\"</code> — іконка й підпис кольору посилання, підпис 700, без підкладки"),
            (3, "Неактивний пункт", "<code>.tabbar__item</code> — Streamline Freehand 24, підпис 12 <code>muted</code>"),
            (4, "Без посилання", "«Профіль» — <code>span</code>: власного профілю у вайрфреймах ще немає"),
        ]),
        variants=[
            ("активний «Пошук»", screen(tabbar("search"), "bar"), "phone"),
            ("активні «Чати»", screen(tabbar("chats"), "bar"), "phone"),
        ],
        usage=("<p>Меню стоїть лише на стрічці (listings*): це точки входу, а не кроки. На деталях його місце займає панель дії або поле повідомлення — пояс знизу завжди один.</p>"
               "<p>Назви — за словником: «Чати», а не «Розмови» (T2). Великі мальовані іконки — свідомий характер: смак дизайнера забороняє екрани без іконок, "
               "а мальована лінія робить сервіс про довіру теплішим за дошку оголошень.</p>"),
        sources="<code>DESIGN.md</code> → Components → Navigation; <code>microcopy.md</code> → T2, O-02…O-04; <code>concept.md</code> → Смак дизайнера",
        do=("розділи на стрічці", screen(_listings_screen(), "tall"),
            "<p>Стрічка — головний екран: звідси людина переходить у чати й назад.</p>"),
        dont=("дія як пункт меню",
              screen('<nav class="tabbar" aria-label="Приклад: погане меню"><ul class="tabbar__list">'
                     f'<li><a class="tabbar__item" href="#">{ico("streamline-freehand:search-magnifier")}<span>Пошук</span></a></li>'
                     f'<li><a class="tabbar__item" href="#" aria-current="page">{ico("streamline-freehand:messages-bubble-smile")}<span>Написати</span></a></li>'
                     f'<li><a class="tabbar__item" href="#">{ico("streamline-freehand:alerts-warning-triangle")}<span>Поскаржитися</span></a></li>'
                     '</ul></nav>', "bar"),
              "<p>Меню — це місця, куди йдеш, а не те, що робиш. «Написати» без людини не має адресата, «Поскаржитися» — без предмета.</p>",
              "actionbar", "дія «Написати Ірині» — на панелі дії профілю чи оголошення, скарга — у ⋯ шапки."),
    ),

    dict(
        slug="actionbar", name="Панель дії", group="Навігація", api="actionbar",
        files=["actionbar.css"],
        classes="<code>.actionbar</code> — усередині одна <code>.button--primary</code>",
        role="Закріплений низ деталей з однією кораловою кнопкою на всю ширину. Це третій крок core loop — «Написати Ірині» — завжди під пальцем.",
        card_role="Одна коралова дія внизу на всю ширину.",
        preview=screen(actionbar(), "bar"), preview_mod="flush",
        anatomy=dict(live=screen(
            f'<div class="actionbar"{P(1, "t")}><a class="button button--primary"{P(2, "c")} href="#">Написати Ірині</a></div>', "bar"), legend=[
            (1, "Пояс", "<code>.actionbar</code> — білий, fixed, поля 12 + safe-area"),
            (2, "Одна дія", "<code>.button--primary</code> — корал на всю ширину, 48"),
        ]),
        variants=[
            ("звичайна · listing, profile, profile-empty", screen(actionbar(), "bar"), "phone"),
            ("завантаження — скелетон кнопки · listing-loading, profile-loading", screen(actionbar(loading=True), "bar"), "phone"),
        ],
        usage=("<p>Панель стоїть на оголошенні й профілі. Контакт у Кутку прямий, без заявок і матчингу, тож на деталях головна дія одна — «Написати Ірині» (D4). "
               "Це The One Coral Button Rule у найчистішому вигляді: на екрані одна коралова кнопка, і вона тут.</p>"
               "<p>Поки дані вантажаться, замість кнопки — скелетон тієї ж форми: людина не натисне «Написати» до того, як побачить, кому пише.</p>"),
        sources="<code>DESIGN.md</code> → Layout, Named Rules → The One Coral Button; <code>microcopy.md</code> → D4, «Звірка після переписування»",
        do=("одна дія на всю ширину", screen(actionbar(), "bar"),
            "<p>Ім’я в кнопці каже, кому підеш писати, і робить дію конкретною.</p>"),
        dont=("дві кнопки в панелі",
              screen('<div class="actionbar">' + button("Написати Ірині") + button("Поскаржитися") + '</div>', "bar"),
              "<p>Дві коралові кнопки однакової ваги — людина зупиняється вибирати, а скарга виглядає так само заохочено, як контакт.</p>",
              "topbar", "«Заблокувати чи поскаржитися» живе в ⋯ шапки (D8), панель лишається з однією дією."),
    ),

    dict(
        slug="sheet", name="Шторка", group="Навігація", api="sheet",
        files=["sheet.css"],
        classes="<code>details.sheet</code> · <code>__panel</code> <code>__grabber</code> <code>__head</code> <code>__title</code> <code>__body</code> <code>__foot</code>",
        role="Панель знизу для фільтрів: виїжджає поверх стрічки, не відриваючи людину від результатів. Побудована на <code>&lt;details&gt;</code> — працює без JS.",
        card_role="Фільтри знизу поверх стрічки, на <code>details</code>.",
        preview=screen('<div class="shell"><div class="shell__main">' + sheet(open_=True) + '</div></div>'), preview_mod="flush",
        anatomy=dict(lead="Живий компонент: «Скасувати», тап поза панеллю або Esc закривають шторку, чип «Фільтри · 3» відкриває знову.",
            live=screen('<div class="shell"><div class="shell__main">' + sheet(open_=True)
                        .replace('<summary class="chip', f'<summary{P(1)} class="chip', 1)
                        .replace('<div class="sheet__grabber"', f'<div{P(2, "t")} class="sheet__grabber"', 1)
                        .replace('<div class="sheet__head">', f'<div class="sheet__head"{P(3)}>', 1)
                        .replace('<form class="sheet__body"', f'<form{P(4)} class="sheet__body"', 1)
                        .replace('<div class="sheet__foot">', f'<div class="sheet__foot"{P(5)}>', 1)
                        + '</div></div>', "tall"), legend=[
            (1, "Чип-відкривач", "<code>summary.chip--selected</code> «Фільтри · 3» — дія, тому корал-посилання"),
            (2, "Тримач", "<code>.sheet__grabber</code> — показує, що панель знизу"),
            (3, "Голова", "<code>.sheet__head</code> — заголовок 19/700 ліворуч, «Скасувати» праворуч"),
            (4, "Тіло", "<code>.sheet__body</code> — <code>fieldset</code> з полями, скролиться саме"),
            (5, "Низ", "<code>.sheet__foot</code> — «Застосувати фільтри» на всю ширину"),
        ]),
        variants=[
            ("закрита — лише чип", stage(sheet()), "phone"),
            ("відкрита — затемнення під панеллю, плаваюча тінь", screen('<div class="shell"><div class="shell__main">' + sheet(open_=True) + '</div></div>', "tall"), "phone"),
        ],
        usage=("<p>Шторка — для короткого набору умов, які людина змінює, не покидаючи стрічку: район, бюджет, дата заїзду. Тінь «далеко» і затемнення — "
               "одне з небагатьох місць, де в системі є глибина: панель справді лежить поверх екрана.</p>"
               "<p>Тексти — «Фільтри · Застосувати фільтри · Змінити фільтри» однаково на всіх listings* (D7); «Скасувати» — текстова кнопка, бо корал-заливка тут одна — «Застосувати».</p>"),
        sources="<code>DESIGN.md</code> → Components → Navigation, Elevation; <code>microcopy.md</code> → D7, «Звірка після переписування»",
        do=("фільтри поверх стрічки", screen('<div class="shell"><div class="shell__main">' + sheet(open_=True) + '</div></div>', "tall"),
            "<p>Умови змінюються за секунду, результати — під панеллю, нікуди не ділися.</p>"),
        dont=("помилка в шторці",
              screen('<div class="shell"><div class="shell__main">'
                     f'<details class="sheet" open>{filters_chip()}<section class="sheet__panel" aria-label="Приклад: помилка в шторці">'
                     '<div class="sheet__grabber" aria-hidden="true"></div>'
                     '<div class="sheet__head"><h3 class="sheet__title">Не вдалося завантажити оголошення</h3><a class="button button--text" href="#">Скасувати</a></div>'
                     '<div class="sheet__body"><p>Перевір з’єднання й спробуй ще.</p></div>'
                     '<div class="sheet__foot"><a class="button button--primary button--block" href="#">Спробувати ще</a></div>'
                     '</section></details></div></div>', "tall"),
              "<p>Шторку можна змахнути, і помилка зникне разом із нею — а стрічка під нею так і лишиться порожньою.</p>",
              "state", "збій показуємо станом на місці вмісту, з «Спробувати ще»."),
    ),
]

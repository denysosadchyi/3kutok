"""Сторінки груп «Оболонка» і «Навігація»: shell, topbar, header, tabbar, actionbar, sheet."""

from _kit import *


def _shell(mods, top, main, bottom="", pin_main=""):
    return f'<div class="shell {mods}">{top}<div class="shell__main"{pin_main}>{main}</div>{bottom}</div>'


def _listings_screen(pins=False):
    p = (lambda n: P(n)) if pins else (lambda n: "")
    head = header().replace('<header class="header">', f'<header class="header"{p(1)}>', 1)
    bar = tabbar().replace('<nav class="tabbar"', f'<nav class="tabbar"{p(3)}', 1)
    return _shell("shell--header shell--tabbar", head, results_meta() + card_list(listing_card()), bar, p(2))


def _listings_page():
    """Стрічка як ціла сторінка (body.shell) — для «Трьох ширин»: медіазапити бачать iframe."""
    cards = card_list(listing_card(), listing_card_tatarka(), listing_card())
    return header() + f'<main class="shell__main">{results_meta()}{cards}</main>' + tabbar()


_LISTINGS_WIDTHS = widths(_listings_page(), "shell shell--header shell--tabbar", title="Стрічка listings")


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


# ── Split-view (урок 10): перелік + деталь ──
CHATS = [("Ірина", "person-iryna.jpg", "Так, домовилися. Напишу адресу в суботу зранку."),
         ("Марина", "person-maryna.jpg", "Можна в неділю після 11:00."),
         ("Оля", "person-olia.jpg", "Так, четвер о 18:30. Чекаємо!")]


def chat_rows(current=0, pin="", state=None):
    """Перелік чатів: ul.group з person-row; вибраний — aria-current="page". state=(n, клас) — стан рядка n."""
    out = []
    for n, (name, photo, last) in enumerate(CHATS):
        cur = ' aria-current="page"' if n == current else ""
        p = pin if n == current else ""
        cls = f" {state[1]}" if state and state[0] == n else ""
        out.append(f'<li class="group__row"><a class="person-row{cls}" href="#"{cur}{p}>{avatar("md", alt="", photo=photo)}'
                   f'<span class="person-row__text"><strong class="person-row__name">{name}</strong>'
                   f'<span class="person-row__caption">{last}</span></span>{ico("solar:alt-arrow-right-linear", "chevron")}</a></li>')
    return '<ul class="group">' + "".join(out) + '</ul>'


def chats_head(pin=""):
    return f'<header class="header"{pin}><div class="header__top"><h3 class="header__title">Чати</h3></div></header>'


def nothing(what="чат", icon="streamline-freehand:messages-bubble-smile", text="Тут відкриється переписка й кімната, про яку йдеться.", pin=""):
    """«Нічого не вибрано» — права панель на ширині, коли деталь ще не відкрита."""
    return (f'<section class="state"{pin}><div class="state__icon">{ico(icon)}</div>'
            f'<h3 class="state__title">Обери {what} ліворуч</h3><p class="state__text">{text}</p></section>')


def split(list_html, detail_html=None, mods="", pin_list="", pin_detail=""):
    """detail_html=None — деталі немає: --solo, перелік на всю ширину."""
    if detail_html is None:
        mods = (mods + " split--solo").strip()
    m = f" {mods}" if mods else ""
    detail = f'<section class="split__pane split__pane--detail"{pin_detail}>{detail_html}</section>' if detail_html is not None else ""
    return (f'<div class="split{m}"><section class="split__pane split__pane--list"{pin_list}>{list_html}</section>{detail}</div>')


def close(label="Закрити чат", cls="", pin=""):
    """× у шапці деталі — видно лише, коли панелі поруч (split.css)."""
    c = f" {cls}" if cls else ""
    return f'<a class="topbar__action split__close{c}"{pin} href="#" aria-label="{label}">{ico("solar:close-linear")}</a>'


def _chat_top(pin_close=""):
    """Шапка чату в спліті: «Назад до чатів», справа кластер ⋯ і × (.topbar__end)."""
    return topbar_person().replace(back(), back("Назад до чатів"), 1).replace(more(), end_cluster(more(), close(pin=pin_close)), 1)


def _chat_pane(pin_close=""):
    return _chat_top(pin_close) + f'<div class="shell__main">{chat_context()}{messages()}</div>' + composer()


def _chats_list(current=0, main=False, pin=""):
    tag = "main" if main else "div"
    return chats_head() + f'<{tag} class="shell__main">{chat_rows(current, pin)}</{tag}>'


def current_card(html):
    """Вибрана картка переліку — aria-current="page" на посиланні (кільце --color-current)."""
    return html.replace('class="listing-card__link"', 'class="listing-card__link" aria-current="page"', 1)


def _feed_pane(selected=False):
    cards = card_list(listing_card(), listing_card_tatarka(), listing_card())
    return header(bar=False) + f'<div class="shell__main">{chip_row()}{results_meta()}{current_card(cards) if selected else cards}</div>'


def _listing_pane():
    top = f'<header class="topbar topbar--over-photo">{back("Назад до результатів")}<span></span>{end_cluster(more(), close("Закрити оголошення"))}</header>'
    return top + f'<div class="shell__main">{hero_photo()}{listing_title()}{group(FLAT)}</div>' + actionbar()


_CHATS_PAGE = split(_chats_list(), _chat_pane(), "split--tablet split--detail") + tabbar("chats")
_CHATS_NOTHING = split(_chats_list(None, main=True), f'<div class="shell__main">{nothing()}</div>', "split--tablet") + tabbar("chats")
_LISTINGS_SOLO = split(_feed_pane()) + tabbar()
_LISTINGS_SPLIT = split(_feed_pane(selected=True), _listing_pane(), "split--detail") + tabbar()
# Антиприклад: стрічка з плейсхолдером «Обери оголошення ліворуч» замість --solo
_LISTINGS_NOTHING = split(_feed_pane(), '<div class="shell__main">' + nothing(
    "оголошення", "streamline-freehand:home", "Тут відкриється оголошення — фото, умови й хто живе в квартирі.") + '</div>') + tabbar()
B_CHATS = "shell shell--tabbar shell--composer shell--split"
B_CHATS_LIST = "shell shell--tabbar shell--split"
B_FEED = "shell shell--tabbar shell--split"
B_LISTING = "shell shell--tabbar shell--split shell--photo-top shell--actionbar"


def at(w, inner, body, title):
    """Одна сцена потрібної ширини (tablet | desktop) у зменшеному масштабі, як у «Трьох ширинах»."""
    cap = dict(WIDTHS)[w]
    return (f'<figure class="doc-width doc-width--{w}"><div class="doc-width__view" inert>{frame(inner, body, title)}</div>'
            f'<figcaption>{cap}</figcaption></figure>')


def wide(inner, body, title):
    """Одна сцена десктопа 72rem у зменшеному масштабі (як «Три ширини», без телефона й планшета)."""
    return at("desktop", inner, body, title)


def _anatomy_split():
    """Планшет 48rem — найвужча ширина, де панелі вже поруч; мітки — частини спліта."""
    inner = (split(chats_head(P(1)) + f'<div class="shell__main">{chat_rows(0, P(2, "tr"))}</div>',
                   _chat_pane(P(4, "tr")), "split--tablet split--detail", pin_detail=P(3))
             + tabbar("chats").replace('<nav class="tabbar"', f'<nav class="tabbar"{P(5, "t")}', 1))
    return at("tablet", inner, B_CHATS, "Анатомія: перелік чатів і чат поруч")


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
        widths=("Стрічка listings на 390, 48rem і 72rem. До <code>--bp-desktop</code> меню — пояс знизу, від нього — шапка вгорі: "
                "<code>.shell--tabbar</code> переносить резерв висоти з низу вгору. Картки — <code>.card-list</code>: 1 → 2 → 3 колонки. "
                "Решта оболонки не змінюється (<code>responsive/width-audit.md</code>).", _LISTINGS_WIDTHS),
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
               "Оголошення починається з фото на всю ширину, яке заходить під статус-бар, — для цього <code>--photo-top</code> знімає верхнє поле.</p>"
               "<p>Від <code>--bp-desktop</code> нижнього меню немає: <code>.shell--tabbar</code> резервує висоту меню зверху, бо меню стає шапкою сторінки "
               "(див. «Нижнє меню»). Правило діє лише на <code>body.shell--tabbar</code> — на сторінці, а не на зразку в рамці телефона.</p>"),
        sources="<code>DESIGN.md</code> → Layout; <code>ui/shell.html</code>; <code>ui/inventory.md</code> → Навігація",
        do=("один пояс знизу", screen(_profile_screen(), "tall"),
            "<p>Профіль: компактна шапка, вміст, одна панель дії. Людина знає, що робити далі, і кнопка під пальцем.</p>"),
        dont=("меню і панель дії разом",
              screen(_shell("shell--tabbar", topbar(), profile_head(), actionbar() + tabbar()), "tall"),
              "<p>Два закріплені пояси з’їдають висоту і змагаються за палець: панель дії налазить на меню, а коралова кнопка губиться поруч із навігацією.</p>",
              "actionbar", "на деталях лишається тільки панель дії; меню — на стрічці."),
    ),

    dict(
        slug="split", name="Список і деталь", group="Оболонка", api="split",
        files=["split.css", "split.js"],
        classes="<code>.split</code> · <code>__pane</code> <code>__pane--list</code> <code>__pane--detail</code> <code>__close</code> · <code>--detail</code> <code>--solo</code> <code>--tablet</code> · на <code>body</code> — <code>.shell--split</code>",
        role="Перелік і відкритий елемент на одній сторінці. На телефоні видно одну панель, як два окремі екрани; на ширині — поруч: перелік ліворуч, деталь праворуч. Людина перескакує між елементами, не повертаючись назад.",
        role_plain="Перелік і відкритий елемент на одній сторінці: на телефоні видно одну панель, на ширині — поруч.",
        card_role="Перелік + деталь: на телефоні по черзі, на ширині поруч.",
        preview=screen(_CHATS_NOTHING), preview_mod="flush",
        anatomy=dict(lead="Ціла сторінка на планшеті 48rem (iframe): панелі поруч стоять лише на сторінці, у рамці телефона — одна. Номери легенди описують частини сцени.",
            live=_anatomy_split(), legend=[
            (1, "Панель переліку", "<code>.split__pane--list</code> — своя шапка (<code>.header</code>, на деталі — <code>p</code>, не <code>h1</code>) і <code>.shell__main</code>; на ширині — 1 колонка сітки, прокручується сама"),
            (2, "Вибраний елемент", "<code>aria-current=\"page\"</code> на посиланні рядка чи картки — кільце <code>--color-current</code>"),
            (3, "Панель деталі", "<code>.split__pane--detail</code> — звичайна оболонка: шапка, <code>main</code>, свій пояс (поле повідомлення, панель дії) — sticky низом панелі"),
            (4, "Закрити ×", "<code>.split__close</code> (<code>topbar__action</code>) — лише коли панелі поруч; веде на перелік без вибору. «Назад» на ширині схований"),
            (5, "Меню", "<code>.tabbar</code> — після <code>.split</code>; на телефоні з <code>--detail</code> ховається, як на окремому екрані-деталі"),
        ]),
        variants_lead="Ті самі сторінки на різних ширинах. На телефоні <code>--detail</code> вирішує, яку панель видно; на ширині — чи є права панель узагалі.",
        variants=[
            ("телефон · перелік (chats) — деталь схована", screen(_CHATS_NOTHING, "tall"), "phone"),
            ("телефон · <code>--detail</code> (chat) — перелік і меню сховані", screen(_CHATS_PAGE, "tall"), "phone"),
            ("планшет · <code>--tablet --detail</code> — перелік чатів і чат поруч (chat*)", at("tablet", _CHATS_PAGE, B_CHATS, "Планшет: чати й чат"), "desk"),
            ("планшет · <code>--tablet</code>, нічого не вибрано — «Обери чат ліворуч» (chats)", at("tablet", _CHATS_NOTHING, B_CHATS_LIST, "Планшет: чат не вибрано"), "desk"),
            ("десктоп · <code>--solo</code> — стрічка без вибору на всю ширину, 3 колонки (listings*)", wide(_LISTINGS_SOLO, B_FEED, "Десктоп: стрічка"), "desk"),
            ("десктоп · <code>--detail</code> — стрічка в 1 колонку + оголошення (listing*)", wide(_LISTINGS_SPLIT, B_LISTING, "Десктоп: стрічка й оголошення"), "desk"),
        ],
        widths=("Чат з Іриною на 390, 48rem і 72rem. Телефон — лише чат, дорога до переліку — «Назад до чатів». "
                "Від <code>--bp-tablet</code> (<code>--tablet</code>) — перелік ліворуч, чат праворуч, «назад» сховано, з’являється ×. "
                "Від <code>--bp-desktop</code> — те саме в контейнері <code>--container-max</code>, меню — шапкою вгорі. "
                "Стрічка → оголошення без <code>--tablet</code> стає поруч лише від <code>--bp-desktop</code> (<code>responsive/width-audit.md</code>).",
                widths(_CHATS_PAGE, B_CHATS, title="Чат з Іриною")),
        usage=("<p><strong>Коли екран стає спліт-в’ю.</strong> Лише коли перелік і деталь — одна задача, і людина перескакує між елементами: "
               "порівнює кімнати підряд або відповідає в кількох чатах. На телефоні це два кроки (перелік → деталь → «назад»), на ширині — дві зони поруч, "
               "і крок «назад» зникає (<code>responsive/width-audit.md</code>, вердикт «нова поведінка»). Чати → чат — від <code>--bp-tablet</code> (<code>--tablet</code>): "
               "рядок переліку вузький, чату вистачає двох колонок. Стрічка → оголошення — від <code>--bp-desktop</code>: оголошення тримається на фото, "
               "у двох колонках планшета воно стало б мініатюрою.</p>"
               "<p><strong>Коли лишається одна колонка.</strong> Профіль, «оголошення зняли», помилки профілю — читання згори вниз без переліку поруч: "
               "аудит каже «однаково», точки нічого не вмикають. Не роби спліт, якщо зліва нема чого вибирати.</p>"
               "<p><strong>Нічого не вибрано — дві відповіді.</strong> Сітка карток (стрічка) — <code>--solo</code>: деталі немає, картки на всю ширину в 3 колонки, "
               "бо вільне місце й так займають картки. Перелік рядків (чати) — права панель зі станом «Обери чат ліворуч»: вузький рядок на всю ширину лише "
               "розтягнувся б. Немає переліку взагалі (порожньо, помилка, завантаження переліку) — <code>--solo</code> зі станом на всю ширину.</p>"
               "<p><strong>×, а не «назад».</strong> Коли панелі поруч, «назад» сховано — перелік уже видно. Щоб закрити деталь, у шапці деталі стоїть "
               "<code>.split__close</code>: веде на перелік без вибору (chats, listings). Підпис — «Закрити чат», «Закрити оголошення». На телефоні × схований: "
               "той самий шлях дає стрілка «Назад до чатів» / «Назад до результатів».</p>"
               "<p><strong>Розмітка.</strong> Рівно один <code>&lt;main id=\"content\"&gt;</code> стоїть у панелі, яка головна на телефоні. "
               "Це деталь з <code>--detail</code>, інакше перелік. Друга панель — <code>div.shell__main</code>, її заголовок — <code>p</code>. <code>body</code> отримує <code>.shell--split</code>: на ширині оболонка "
               "знімає власні резерви, панелі прокручуються самі, пояси деталі стають sticky. Рух відкриття й закриття — розділ «Рух» нижче і <code>split.js</code>.</p>"),
        sources="<code>responsive/width-audit.md</code> → «Перелік розмов», «Чат із людиною», питання 1; <code>DESIGN.md</code> → Адаптив; <code>microcopy.md</code> → T2, O-15",
        do=("чати поруч із чатом", at("tablet", _CHATS_PAGE, B_CHATS, "Так: чати й чат поруч"),
            "<p>Людина відповідає Ірині й бачить, що Марина теж написала, — перейти можна одним тапом, без «назад».</p>"),
        dont=("плейсхолдер замість стрічки",
              wide(_LISTINGS_NOTHING, B_FEED, "Ні: стрічка з плейсхолдером"),
              "<p>Картки стиснуті в одну колонку, а дві третини екрана займає «Обери оголошення ліворуч» — підказка, якої нікому не треба, коли вибирати й так видно з чого.</p>",
              "split", "сітка карток без вибору — <code>--solo</code>; плейсхолдер лише для переліку рядків (чати)."),
    ),

    dict(
        slug="topbar", name="Компактна шапка", group="Навігація", api="topbar",
        files=["topbar.css"],
        classes="<code>.topbar</code> · <code>__back</code> <code>__title</code> <code>__action</code> <code>__person</code> <code>__name</code> <code>__verified</code> <code>__end</code> · <code>--person</code> <code>--over-photo</code>",
        role="App bar 48 на деталях: стрілка «назад», заголовок або людина і ⋯ «Заблокувати чи поскаржитися». Тримає людину в ланцюжку пошук → оголошення → профіль → чат.",
        card_role="App bar 48: назад, заголовок або людина, ⋯.",
        preview=stage(topbar(), "flush"), preview_mod="flush center",
        anatomy=dict(live=stage(
            '<header class="topbar">' + back(pin=P(1)) + f'<p class="topbar__title"{P(2)}>Профіль Ірини</p>' + more(P(3, "tr")) + '</header>'
            + '<header class="topbar topbar--person">' + back()
            + f'<a class="topbar__person"{P(4)} href="#">{avatar(mark=False, alt="Фото профілю Ірини")}<strong class="topbar__name">Ірина</strong>'
            + f'<span class="topbar__verified"{P(5, "tr")} title="Номер підтверджено 12 вересня">{ico("solar:shield-check-linear")}<span class="sr-only">Номер підтверджено</span></span></a>'
            + more() + '</header>'
            + f'<header class="topbar">{back()}<p class="topbar__title">Профіль Ірини</p>{end_cluster(theme_btn(), more(), pin=P(6, "tr"))}</header>', "flush"), legend=[
            (1, "Назад", "<code>.topbar__back</code> — Solar 24, підпис для скрінрідера: «Назад до оголошення» / «Назад до результатів»"),
            (2, "Заголовок", "<code>.topbar__title</code> — 16/700; <code>h1</code>, якщо нижче немає власного"),
            (3, "Дія ⋯", "<code>.topbar__action</code> — «Заблокувати чи поскаржитися»; у чаті, профілі й оголошенні"),
            (4, "Людина", "<code>.topbar__person</code> — аватар 28 + ім’я, посилання на профіль (<code>--person</code>, чат)"),
            (5, "Щит перевірки", "<code>.topbar__verified</code> — зелений щит 20 замість позначки на аватарі"),
            (6, "Дві дії справа", "<code>.topbar__end</code> — кластер у правій комірці: тема + ⋯, у спліті ще ×. Кнопки впритул, над фото — проміжок <code>--space-2</code>"),
        ]),
        variants=[
            ("із заголовком · profile*", stage(topbar(), "flush"), "phone"),
            ("«Назад» у фокусі", stage(topbar().replace('class="topbar__back"', 'class="topbar__back is-focus"', 1), "flush"), "phone"),
            ("<code>--person</code> · chat*", stage(topbar_person(), "flush"), "phone"),
            ("<code>--over-photo</code> · listing — круглі кнопки на затемненні з розмиттям; в екрані (<code>.shell--photo-top</code>) шапка липка", photo_frame(topbar_photo()), "phone"),
            ("дві дії справа · <code>__end</code> — тема + ⋯", stage(topbar_end(), "flush"), "phone"),
            ("дві дії справа над фото — окремі кола з проміжком <code>--space-2</code>", photo_frame(topbar_photo_end()), "phone"),
        ],
        usage=("<p>Компактна шапка стоїть на всіх екранах-деталях: оголошення, профіль, чат (12 сторінок). Стрілка завжди веде на крок назад і "
               "каже куди: «Назад до результатів», «Назад до оголошення» — одна назва для однієї дії на всіх екранах (D1, D2).</p>"
               "<p>У чаті замість заголовка — людина: аватар, ім’я і зелений щит «Номер підтверджено 12 вересня». Праворуч ⋯ «Заблокувати чи поскаржитися» — "
               "report і block входять у MVP, бо прямий чат без match-гейту без них небезпечний. Поверх фото кнопки круглі на затемненні, щоб їх було видно на будь-якому знімку.</p>"
               "<p><strong>Дві дії справа.</strong> Права комірка тримає одну дію. Якщо дій дві чи більше (тема + ⋯, у спліті ще ×), "
               "загорни їх у <code>.topbar__end</code>: кластер стає в праву комірку. Кнопки йдуть впритул, бо ціль 48 уже дає відступ. "
               "Над фото кожна кнопка — окреме коло, тому між ними проміжок <code>--space-2</code>; одну дію не загортай.</p>"),
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
        usage=("<p>Велика шапка — лише на стрічці «Результати пошуку» (listings*). Перший крок core loop — пошук за фільтрами. Тому фільтри стоять просто в шапці: "
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
        role="Три розділи продукту — Пошук, Чати, Профіль — під великим пальцем. Білий пояс із хвилею і великими мальованими іконками: найпомітніша «рука» в системі. Від <code>--bp-desktop</code> — та сама навігація шапкою вгорі.",
        role_plain="Три розділи продукту — Пошук, Чати, Профіль — під великим пальцем. Від --bp-desktop — та сама навігація шапкою вгорі.",
        card_role="Пошук · Чати · Профіль, мальовані іконки й хвиля.",
        preview=screen(tabbar(), "bar"), preview_mod="flush",
        anatomy=dict(live=screen(
            f'<nav class="tabbar"{P(1, "t")} aria-label="Приклад нижнього меню"><ul class="tabbar__list">'
            f'<li><a class="tabbar__item" href="#" aria-current="page"{P(2)}>{ico("streamline-freehand:search-magnifier")}<span>Пошук</span></a></li>'
            f'<li><a class="tabbar__item" href="#"{P(3)}>{ico("streamline-freehand:messages-bubble-smile")}<span>Чати</span></a></li>'
            f'<li><span class="tabbar__item"{P(4)}>{ico("streamline-freehand:smiley-happy")}<span>Профіль</span></span></li>'
            '</ul></nav>', "bar"), legend=[
            (1, "Пояс із хвилею", "<code>.tabbar</code> — білий, хвиля зверху маскою <code>--wave-mask</code>, fixed + safe-area; від <code>--bp-desktop</code> — шапка вгорі з межею замість хвилі"),
            (2, "Активний пункт", "<code>aria-current=\"page\"</code> — іконка й підпис кольору посилання, підпис 700, без підкладки"),
            (3, "Неактивний пункт", "<code>.tabbar__item</code> — Streamline Freehand 24, підпис 12 <code>muted</code>"),
            (4, "Без посилання", "«Профіль» — <code>span</code>: власного профілю у вайрфреймах ще немає"),
        ]),
        variants=[
            ("активний «Пошук»", screen(tabbar("search"), "bar"), "phone"),
            ("активні «Чати»", screen(tabbar("chats"), "bar"), "phone"),
            ("десктоп, від <code>--bp-desktop</code> — шапка вгорі, активний «Пошук»", desk(tabbar("search")), "desk"),
            ("десктоп — активні «Чати»", desk(tabbar("chats")), "desk"),
        ],
        widths=("Та сама розмітка <code>nav.tabbar</code>, ті самі три пункти. Телефон і планшет — пояс знизу з хвилею: на планшеті "
                "сенсор і великий палець лишаються (<code>responsive/width-audit.md</code>, рядок «Оболонка»). Від <code>--bp-desktop</code> — "
                "шапка вгорі: пункти в рядок, іконка + підпис 14, межа <code>--color-divider</code> замість хвилі.", 
                widths(header(bar=False) + tabbar(), "shell shell--header shell--tabbar", "bar", "Меню")),
        usage=("<p>Меню стоїть лише на стрічці (listings*): це точки входу, а не кроки. На деталях його місце займає панель дії або поле повідомлення — пояс знизу завжди один.</p>"
               "<p>На десктопі (від <code>--bp-desktop</code>) нижня панель лише забирає висоту, а «великого пальця» там немає — тож меню стає шапкою сторінки. "
               "Це не новий компонент: та сама розмітка, той самий список і ті самі стани; <code>tabbar.css</code> міняє тільки розкладку. "
               "Шапкою меню стає лише на сторінці (<code>body.shell--tabbar</code>): у рамці телефона у вітрині воно лишається поясом знизу.</p>"
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
        role="Панель знизу для фільтрів: виїжджає поверх стрічки, і людина не втрачає результатів з поля зору. Побудована на <code>&lt;details&gt;</code> — працює без JS.",
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
        usage=("<p>Шторка — для короткого набору умов, які людина змінює й лишається на стрічці: район, бюджет, дата заїзду. Тінь «далеко» і затемнення — "
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

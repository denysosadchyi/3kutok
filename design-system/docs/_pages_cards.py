"""Сторінки групи «Картки й списки»: listing-card (+ card-list), price-tag, avatar,
profile-head, section-title, group, verified-note, person-row, hero-photo, gallery,
listing-title, results-meta.

Уся розмітка — з _kit.py або тими самими класами, що в ui/kit.html.
pin() вставляє P(n, at) у готовий шматок кіта, щоб не дублювати розмітку.
"""

from _kit import *


def pin(html, cls, n, at=None, nth=1):
    """Додає data-pin до nth-го елемента з точним class="cls"."""
    needle = f'class="{cls}"'
    i = -1
    for _ in range(nth):
        i = html.find(needle, i + 1)
        if i < 0:
            raise ValueError(f"немає {needle} №{nth}")
    j = i + len(needle)
    return html[:j] + P(n, at) + html[j:]


def main_(inner):
    """Колонка вмісту екрана (поля 16, між блоками 12) — для сцен із кількох блоків."""
    return f'<div class="shell"><div class="shell__main">{inner}</div></div>'


def ul_group(*rows):
    return '<ul class="group">' + "".join(rows) + '</ul>'


def card_photo(photo="room-lukianivska-bedroom.jpg", alt=ROOM_ALT, price="10 500 грн/міс"):
    return f'<div class="listing-card__photo"><img src="{V}{photo}" alt="{alt}">{price_tag(price)}</div>'


SECTION_SKELETON = '<div class="skeleton skeleton--line skeleton--w40 skeleton--section" aria-hidden="true"></div>'


PAGES = [
    # ── 1. Картка оголошення ──
    dict(
        slug="listing-card", name="Картка оголошення", group="Картки й списки", api="listing-card",
        files=["listing-card.css", "card-list.css"],
        classes="<code>.listing-card</code> · <code>__photo</code> <code>__body</code> <code>__title</code> <code>__link</code> <code>__meta</code> · список — <code>.card-list</code>",
        role="Одне оголошення в стрічці й у профілі: фото кімнати 4:3 з биркою ціни, назва-посилання і метадані. Уся картка — одне посилання «Відкрити оголошення».",
        card_role="Фото 4:3, бирка з ціною, назва й мета.",
        preview=card_list(listing_card()), preview_mod="",
        anatomy=dict(live=stage(card_list(
            pin(pin(pin(pin(pin(listing_card(), "listing-card__photo", 1, "tr"), "price-tag", 2, "r"),
                        "listing-card__link", 3, "r"), "listing-card__meta", 4, "r"), "listing-card", 5, "br"))),
            legend=[
                (1, "Фото", "<code>.listing-card__photo</code> — 4:3, кути 18, без тіні й рамки; фото домінує, текст його лише підписує"),
                (2, "Бирка з ціною", "<code>.price-tag</code> — зліва вгорі, 12 від країв; окремого рядка ціни немає"),
                (3, "Назва-посилання", "<code>.listing-card__title</code> · <code>__link</code> — 16/500; назву пише людина, ми її не переписуємо"),
                (4, "Метадані", "<code>.listing-card__meta</code> — 14 <code>muted</code>: район · хто живе · дата заїзду"),
                (5, "Уся картка — посилання", "<code>__link::after</code> розтягнуто на картку; фокус-кільце обводить її цілу"),
            ]),
        variants=[
            ("Звичайна — стрічка", stage(card_list(listing_card())), "phone"),
            ("У фокусі · коротка мета (профіль)", stage(card_list(listing_card_tatarka("is-focus"))), "phone"),
            ("Завантаження — скелетон: фото + 2 рядки", stage(card_list(listing_card_loading(), hidden=True)), "phone"),
            ("<code>.card-list</code> — стрічка, між картками 32", stage(card_list(listing_card(), listing_card_tatarka())), "phone"),
        ],
        usage=("<p>Картка відповідає на перше питання людини в стрічці: «Чи кімната справжня і як вона виглядає?» Тому фото займає більшу частину картки, "
               "а текст його лише підписує: назва 16/500 і метадані сірим. Ціна не в тексті — на білій бирці поверх фото.</p>"
               "<p>Метадані — у порядку «район · хто живе · дата заїзду», з однією формою дати: «з 1 жовтня», рік поточний не пишемо. "
               "У профілі, де район і люди вже відомі, мета коротка — лише «з 5 жовтня». Посилання картки для читача екрана — «Відкрити оголошення».</p>"
               "<p>Картки стоять у <code>.card-list</code> з проміжком 32. Скелетон картки — лише на час завантаження: "
               "постійно сірий прямокутник замість фото — те, чого дизайнер просив уникати.</p>"),
        sources="<code>DESIGN.md</code> → Cards / Containers, Do’s and Don’ts; <code>microcopy.md</code> → LS-22, LS-23, LS-25, T6; <code>ui/inventory.md</code> → Картки й списки",
        do=("фото з биркою, мета — без ціни", stage(card_list(listing_card())),
            "<p>Ціна — на бирці, мета — про район, людей і дату. Людина зчитує кімнату з фото, а суму — з одного місця.</p>"),
        dont=("сіре фото назавжди і ціна в мета",
              stage(card_list('<li class="listing-card"><div class="skeleton skeleton--photo"></div><div class="listing-card__body">'
                              '<h3 class="listing-card__title"><a class="listing-card__link" href="#">Кімната біля Лук’янівської</a></h3>'
                              '<p class="listing-card__meta">10 500 грн/міс · Шевченківський · з 1 жовтня</p></div></li>')),
              "<p>Скелетон-фото як постійний стан — «сіра плашка замість фото»: кімната без обличчя. А ціна в мета змагається з районом і датою й дублює бирку.</p>",
              "price-tag", "ціна — тільки на бирці поверх справжнього фото; скелетон — лише поки вантажиться."),
    ),

    # ── 2. Бирка з ціною ──
    dict(
        slug="price-tag", name="Бирка з ціною", group="Картки й списки", api="price-tag",
        files=["price-tag.css"],
        classes="<code>.price-tag</code> — лише всередині <code>.listing-card__photo</code> або <code>.hero-photo</code>",
        role="Signature «Кутка»: біла бирка з ключем, на якій висить ціна кімнати. Лежить поверх фото, трохи нахилена, з отвором для кільця.",
        card_role="Signature: ціна на білій бирці поверх фото.",
        preview=card_photo(), preview_mod="flush",
        anatomy=dict(live=(
            stage(pin(pin(card_photo(), "listing-card__photo", 1, "br"), "price-tag", 2, "r"))
            + stage(photo_top(pin(pin(hero_photo(), "hero-photo", 3, "tr"), "price-tag", 4, "r")), "flush")),
            legend=[
                (1, "Фото картки", "<code>.listing-card__photo</code> — основа; бирка позиціонується відносно нього"),
                (2, "Бирка в картці", "<code>.price-tag</code> — зліва вгорі, 12 від країв; 16/700, клин 12 з отвором 8, нахил −4°, тінь «над фото»"),
                (3, "Головне фото", "<code>.hero-photo</code> — фото оголошення на всю ширину"),
                (4, "Бирка на головному фото", "та сама <code>.price-tag</code> — зліва внизу, бо верх зайнятий кнопками шапки"),
            ]),
        variants=[
            ("На картці — зліва вгорі", stage(card_list(listing_card())), "phone"),
            ("На головному фото — зліва внизу", stage(photo_top(hero_photo()), "flush"), "phone"),
        ],
        usage=("<p>Бирка — головний носій характеру системи: «Куток — це біла стіна, на якій висить ключ». Вона натякає, що в цієї кімнати є ключ, "
               "який можна отримати. Тому ціна живе тільки тут — і в картці, і на головному фото оголошення; окремого текстового рядка ціни немає.</p>"
               "<p>Текст — «10 500 грн/міс»: на бирці бракує місця для «грн/місяць», це свідоме рішення дизайнера. Колір бирки не змінюється ніколи — "
               "ні корал (The Coral Means Do: бирку не натискають), ні зелений. Тінь у неї є лише тому, що біла річ лежить на фото (The Only-On-Photo Rule).</p>"),
        sources="<code>DESIGN.md</code> → Бирка з ключем (signature), Shapes, Elevation &amp; Depth, Правки уроку 7; <code>microcopy.md</code> → LS-20, T7",
        do=("на фото кімнати", stage(card_list(listing_card_tatarka())),
            "<p>Бирка лежить на фотографії, тож її біла заливка й тінь мають сенс: це річ поверх кадру, а ціна — перше, що чіпляє око після фото.</p>"),
        dont=("бирка на білому поза фото",
              stage(price_tag() +
                    '<div class="listing-title"><h3 class="listing-title__name">Кімната біля Лук’янівської</h3><p class="listing-title__meta">Шевченківський район · з 1 жовтня</p></div>'),
              "<p>На білому фоні бирка втрачає основу: біла форма на білому, тінь висить у повітрі, нахил читається як помилка верстки. "
              "Вона абсолютна й поза фото падає на чужий вміст.</p>",
              "listing-title", "під фото — назва й мета; ціна лишається на бирці головного фото."),
    ),

    # ── 3. Аватар ──
    dict(
        slug="avatar", name="Аватар", group="Картки й списки", api="avatar",
        files=["avatar.css"],
        classes="<code>.avatar</code> · <code>--md</code> <code>--lg</code> · <code>.avatar__mark</code> · змінна <code>--avatar-ring</code>",
        role="Фото людини в колі — з позначкою перевірки номера в правому нижньому куті. Сигнал «на обличчі»: видно, що підтверджено саме цю людину.",
        card_role="Фото людини в колі з позначкою перевірки.",
        preview=f'<p>{avatar()} {avatar("md")} {avatar("lg")}</p>', preview_mod="card center",
        anatomy=dict(live=stage(
            '<p>' + pin(pin(avatar("lg"), "avatar avatar--lg", 1, "tl"), "avatar__mark", 2, "br")
            + ' ' + pin(avatar(), "avatar__mark", 3, "r") + '</p>'),
            legend=[
                (1, "Фото", "<code>.avatar &gt; img</code> — коло; поки фото не завантажилось — сіре коло замість alt-тексту"),
                (2, "Позначка на великому", "<code>.avatar__mark</code> у <code>.avatar--lg</code> — 24, зелене коло з білою галочкою"),
                (3, "Позначка на малому", "на 28 і 48 — 16; обвідка 2 у колір фону (<code>--avatar-ring</code>)"),
            ]),
        variants=[
            ("28 · на білому", stage(avatar()), ""),
            ("48 · у сірому списку (<code>--avatar-ring</code>)", stage(avatar("md"), "card"), ""),
            ("84 · профіль", stage(avatar("lg")), ""),
            ("Без позначки — шапка чату", stage(avatar(mark=False)), ""),
        ],
        usage=("<p>Три розміри для трьох місць: 28 — плашка автора на фото й шапка чату, 48 — рядок «Хто живе в квартирі», 84 — голова профілю. "
               "Позначка — 16 на малих, 24 на великому. Для читача екрана в неї завжди той самий прихований текст «Номер підтверджено».</p>"
               "<p>Зелений тут — The Green Is Proof: він стоїть лише біля того, що Куток справді підтвердив, і там, де людина про це читає, поруч є межа "
               "«Це означає лише, що людина має доступ до цього номера». На сірій поверхні кільце позначки перефарбовує <code>--avatar-ring</code> — "
               "<code>.group</code> робить це сам. У шапці чату аватар без позначки: там сигнал несе щит біля імені.</p>"),
        sources="<code>DESIGN.md</code> → Позначка перевірки, Secondary, Правки уроку 7; <code>concept/references.md</code> → A4, C1; <code>microcopy.md</code> → T5",
        do=("позначка в рядку людини", stage(ul_group(person_row())),
            "<p>У «Хто живе в квартирі» позначка на аватарі 48, а в тому ж списку нижче — рядок перевірки з датою й межею.</p>"),
        dont=("позначка в шапці чату",
              screen('<header class="topbar topbar--person">' + back()
                     + f'<a class="topbar__person" href="#">{avatar(alt="Фото профілю Ірини")}<strong class="topbar__name">Ірина</strong></a>'
                     + more() + '</header>', "bar"),
              "<p>На 28 у шапці позначка зливається з фото й не має місця для дати. Сигнал «це та сама людина» губиться саме там, де людина пише.</p>",
              "topbar", "у шапці чату — аватар без позначки і зелений щит біля імені з датою в підказці (C1)."),
    ),

    # ── 4. Голова профілю ──
    dict(
        slug="profile-head", name="Голова профілю", group="Картки й списки", api="profile-head",
        files=["profile-head.css"],
        classes="<code>.profile-head</code> · <code>__name</code> <code>__caption</code> · всередині <code>.avatar--lg</code>",
        role="Верх профілю іншої людини: великий аватар із позначкою, ім’я й вік, підпис про її оголошення. Ім’я — <code>h1</code> екрана.",
        card_role="Великий аватар, ім’я й вік, підпис.",
        preview=profile_head(), preview_mod="center",
        anatomy=dict(live=stage(pin(pin(pin(pin(profile_head(), "avatar avatar--lg", 1, "tl"), "avatar__mark", 2, "br"),
                                            "profile-head__name", 3, "r"), "profile-head__caption", 4, "r")),
            legend=[
                (1, "Аватар 84", "<code>.avatar--lg</code> — фото людини"),
                (2, "Позначка 24", "<code>.avatar__mark</code> — номер підтверджено; дата й межа — нижче, у «Що підтверджено»"),
                (3, "Ім’я й вік", "<code>.profile-head__name</code> — 23/700; на екрані це <code>h1</code>"),
                (4, "Підпис", "<code>.profile-head__caption</code> — 14 <code>muted</code>: зв’язок з оголошенням"),
            ]),
        variants=[
            ("Повна", stage(profile_head()), "phone"),
            ("Неповний профіль — без віку", stage(profile_head(age=False)), "phone"),
            ("Завантаження — скелетон", stage(profile_head(loading=True)), "phone"),
        ],
        usage=("<p>Відповідає на «Хто ця людина?» до того, як людина прочитає анкету. Ім’я й вік пише користувач — «Ірина, 29 років» ми не переписуємо; "
               "якщо віку немає, лишається просто «Ірина», без заглушки. Заголовок вкладки — «Профіль Ірини — Куток».</p>"
               "<p>Підпис пов’язує людину з оголошенням, через яке на неї вийшли. Після голови йдуть «Спосіб життя», «Що підтверджено» і її оголошення, "
               "а внизу — одна коралова дія «Написати Ірині».</p>"),
        sources="<code>DESIGN.md</code> → Typography (Headline), Позначка перевірки; <code>microcopy.md</code> → P-02, P-05, P-07, P-28, O-14",
        do=("людина в профілі", stage(profile_head()),
            "<p>Обличчя, ім’я й підпис по центру: профіль про людину, з якою житимеш, а не про квадратні метри.</p>"),
        dont=("кімната в голові профілю",
              stage('<div class="profile-head">' + avatar("lg", mark=False, alt=ROOM_ALT, photo="room-lukianivska-bedroom.jpg")
                    + '<h3 class="profile-head__name">Кімната біля Лук’янівської</h3><p class="profile-head__caption">Шевченківський район · з 1 жовтня</p></div>'),
              "<p>Кругле фото кімнати й назва по центру читаються як профіль людини. Кімната в колі втрачає кадр, а людина не розуміє, з ким говорить.</p>",
              "listing-title", "у кімнати — головне фото на всю ширину й блок назви під ним."),
    ),

    # ── 5. Заголовок розділу ──
    dict(
        slug="section-title", name="Заголовок розділу", group="Картки й списки", api="section-title",
        files=["section-title.css"],
        classes="<code>.section-title</code>",
        role="Називає блок на деталях: «Спосіб життя», «Що підтверджено», «Хто живе в квартирі». Відступ 16 зверху відокремлює розділи без ліній.",
        card_role="Назва блоку на деталях, 19/700.",
        preview=section_title() + group(LIFESTYLE[:2]), preview_mod="",
        anatomy=dict(live=stage(main_(
            pin(section_title(), "section-title", 1, "r") + pin(group(LIFESTYLE[:2]), "group", 2, "br")
            + pin(section_title("Що підтверджено"), "section-title", 3, "r") + ul_group(verified_row())), "flush"),
            legend=[
                (1, "Заголовок", "<code>.section-title</code> — 19/700; на екрані <code>h2</code>"),
                (2, "Блок розділу", "зазвичай <code>.group</code> — заголовок називає його цілим"),
                (3, "Наступний розділ", "відступ 16 зверху + 12 колонки відділяють розділ без ліній і тіней"),
            ]),
        variants=[
            ("«Спосіб життя» — профіль", stage(main_(section_title() + group(LIFESTYLE[:3])), "flush"), "phone"),
            ("«Що підтверджено» — профіль і оголошення", stage(main_(section_title("Що підтверджено") + ul_group(verified_row())), "flush"), "phone"),
            ("«Хто живе в квартирі» — оголошення", stage(main_(section_title("Хто живе в квартирі") + ul_group(person_row())), "flush"), "phone"),
            ("Завантаження — скелетон рядка", stage(main_(SECTION_SKELETON + person_row_loading()), "flush"), "phone"),
        ],
        usage=("<p>Заголовок стоїть над блоком, а не над значенням. Назви — зі словника: «Спосіб життя» (не «Спосіб життя й побут»), "
               "«Що підтверджено» (не «Сигнали довіри»), «Хто живе в квартирі» (не «Авторка й мешканці»).</p>"
               "<p>«Що підтверджено» — окремий розділ і в профілі, і в оголошенні: сигнал довіри не має губитися в списку людей. "
               "Ієрархію тримає вага, а не кегль (The Weight Not Size Rule): 19/700 проти 23/700 заголовка екрана.</p>"),
        sources="<code>DESIGN.md</code> → Typography, Правки уроку 7; <code>microcopy.md</code> → P-08, P-20, L-16, L-21, T4, T5",
        do=("один заголовок на блок", stage(main_(section_title() + group(LIFESTYLE[:3])), "flush"),
            "<p>Одна назва — і п’ять фактів під нею в одному сірому блоці. Око бачить розділ цілим.</p>"),
        dont=("заголовок над кожним значенням",
              stage(main_(section_title("Куріння") + group([("Куріння", "не курить")])
                          + section_title("Гості") + group([("Гості", "за домовленістю")])), "flush"),
              "<p>Назва дублює підпис рядка, а кожен факт стає окремим розділом: екран дробиться, ритм 16 + 12 повторюється без сенсу.</p>",
              "group", "факти одного розділу — рядки одного списку під одним заголовком."),
    ),

    # ── 6. Згрупований список ──
    dict(
        slug="group", name="Згрупований список", group="Картки й списки", api="group",
        files=["group.css"],
        classes="<code>.group</code> · <code>__row</code> <code>__label</code> <code>__value</code> · <code>--padded</code>",
        role="Факти «назва — значення» на сірій картці: звички в профілі, умови квартири в оголошенні. Також тримає рядок людини й рядок перевірки.",
        card_role="Факти «назва — значення» на сірій картці.",
        preview=group(LIFESTYLE[:3]), preview_mod="",
        anatomy=dict(live=stage(pin(pin(pin(pin(group(LIFESTYLE[:3]), "group", 1, "tr"), "group__label", 2, "l", nth=2),
                                            "group__value", 3, "r", nth=2), "group__row", 4, "t", nth=3)),
            legend=[
                (1, "Картка списку", "<code>.group</code> — сіра поверхня, кути 18, поля 16; <code>dl</code> для фактів, <code>ul</code> для людей і перевірки"),
                (2, "Назва", "<code>.group__label</code> — 14 <code>muted</code>, ліворуч, не переноситься"),
                (3, "Значення", "<code>.group__value</code> — 16/500, праворуч, <code>text-wrap: balance</code>"),
                (4, "Рядок і розділювач", "<code>.group__row</code> — ≥ 48; між рядками лінія 1, а не рамка"),
            ]),
        variants=[
            ("Профіль — «Спосіб життя»", stage(group(LIFESTYLE)), "phone"),
            ("Оголошення — квартира", stage(group(FLAT)), "phone"),
            ("Завантаження — смужки в рядках 48", stage(group_loading()), "phone"),
        ],
        usage=("<p>Відповідає на «Чи зійдемося побутом?»: назва ліворуч сірим, значення праворуч. Назви — зі словника анкети: «Розпорядок дня», «Куріння», "
               "«Тварини», «Гості», «Тиша ввечері»; значення — фрази людини («будні, 9:00–18:00», «після 23:00»), тому їм потрібен рядок, а не мітка.</p>"
               "<p>В оголошенні той самий список тримає умови: «Співмешканці — 2 людини», «Квартира — 3 кімнати», «Комунальні — окремо». "
               "Скелетон — ті самі <code>.group__row</code> зі смужкою 12 на тон темнішою: рядок-скелетон на всю висоту виглядав як кнопка.</p>"),
        sources="<code>DESIGN.md</code> → Cards / Containers, Стани, Правки уроку 7; <code>concept.md</code> → атрибут 2 (B1 не взято); <code>microcopy.md</code> → P-10…P-19, L-13, T4",
        do=("звички — рядками", stage(group(LIFESTYLE[:3])),
            "<p>Фраза людини вміщається повністю, назви вирівняні по лівому краю — профілі легко порівнювати між собою.</p>"),
        dont=("звички чипами",
              stage('<div class="chip-row"><div class="chip-row__track">'
                    + chip("не курить") + chip("кіт у квартирі") + chip("гості за домовленістю") + chip("тиша після 23:00")
                    + '</div></div>'),
              "<p>Прийом B1 з референсів, який свідомо не взяли: фрази в пігулку не вміщаються, ряд скролиться, а назва поля зникає. "
              "До того ж чип у «Кутку» — це керування фільтром, і факт про людину почне виглядати як кнопка.</p>",
              "chip", "чип — лише значення фільтра в стрічці; факт про побут — рядок групи."),
    ),

    # ── 7. Рядок перевірки ──
    dict(
        slug="verified-note", name="Рядок перевірки", group="Картки й списки", api="verified-note",
        files=["verified-note.css"],
        classes="<code>.group__row.verified-note</code> · <code>__icon</code> <code>__text</code> <code>__title</code> <code>__limit</code>",
        role="Що саме Куток підтвердив і де межа цієї перевірки: зелений щит, «Номер підтверджено 12 вересня» і чесне пояснення під ним.",
        card_role="Щит, дата перевірки і її межа.",
        preview=ul_group(verified_row()), preview_mod="",
        anatomy=dict(live=stage(ul_group(pin(pin(pin(pin(verified_row(), "group__row verified-note", 1, "br"),
                                                       "verified-note__icon", 2, "tl"), "verified-note__title", 3, "r"),
                                             "verified-note__limit", 4, "r"))),
            legend=[
                (1, "Рядок групи", "<code>.group__row.verified-note</code> — стоїть у <code>.group</code>, вирівняний по верху"),
                (2, "Щит", "<code>.verified-note__icon</code> — Solar shield-check 24, зелений"),
                (3, "Що підтверджено", "<code>.verified-note__title</code> — зелений 500, з датою"),
                (4, "Межа перевірки", "<code>.verified-note__limit</code> — 14 <code>muted</code>; без неї зелений не ставимо"),
            ]),
        variants_lead="Компонент має один вигляд; змінюється лише розділ, де він стоїть.",
        variants=[
            ("Профіль — «Що підтверджено»", stage(main_(section_title("Що підтверджено") + ul_group(verified_row())), "flush"), "phone"),
            ("Оголошення — під рядком людини", stage(ul_group(person_row(), verified_row())), "phone"),
        ],
        usage=("<p>Це місце, де трастова обіцянка «Кутка» чесно звужується. Верифікація номера підтверджує контроль номера, але не особу, житло чи безпеку — "
               "тому під зеленим «Номер підтверджено 12 вересня» завжди стоїть «Це означає лише, що людина має доступ до цього номера.» "
               "Рік поточний не пишемо.</p>"
               "<p>The Green Is Proof: зелений — лише біля справжньої перевірки й лише з межею поруч. Рядок стоїть там, де людина читає про людину: "
               "у профілі й в оголошенні. Позначка на аватарі й щит у чаті — короткі нагадування про цей рядок, а не заміна.</p>"),
        sources="<code>DESIGN.md</code> → Позначка перевірки, The Green Is Proof Rule; <code>microcopy.md</code> → L-23, L-24, P-22, P-23, T5; <code>CLAUDE.md</code> → Довіра",
        do=("у профілі, з межею", stage(main_(section_title("Що підтверджено") + ul_group(verified_row())), "flush"),
            "<p>Окремий розділ, дата й межа: людина знає, що саме перевірено і чого перевірка не гарантує.</p>"),
        dont=("повний рядок у чаті",
              screen('<div class="shell">' + '<header class="topbar topbar--person">' + back()
                     + f'<a class="topbar__person" href="#">{avatar(mark=False, alt="Фото профілю Ірини")}<strong class="topbar__name">Ірина</strong></a>'
                     + more() + '</header><div class="shell__main">' + ul_group(verified_row()) + messages(MESSAGES[:2]) + '</div></div>'),
              "<p>У чаті розлогий рядок з’їдає висоту над розмовою й щоразу зсуває повідомлення. Людина тут пише, а не вивчає профіль.</p>",
              "topbar", "у шапці чату — зелений щит біля імені з датою в підказці (C1); повний рядок — у профілі."),
    ),

    # ── 8. Рядок людини ──
    dict(
        slug="person-row", name="Рядок людини", group="Картки й списки", api="person-row",
        files=["person-row.css"],
        classes="<code>.person-row</code> · <code>__text</code> <code>__name</code> <code>__caption</code> · <code>.chevron</code> — усередині <code>.group__row</code>",
        role="Людина, що живе в квартирі, — посилання з оголошення в її профіль: аватар 48, ім’я й вік, підпис і шеврон.",
        card_role="Аватар, ім’я й підпис — веде в профіль.",
        preview=ul_group(person_row()), preview_mod="",
        anatomy=dict(live=stage(ul_group(pin(pin(pin(pin(pin(person_row(), "person-row", 1, "br"), "avatar avatar--md", 2, "tl"),
                                                       "person-row__name", 3, "r"), "person-row__caption", 4, "r"), "chevron", 5, "tr"))),
            legend=[
                (1, "Посилання на всю ширину", "<code>.person-row</code> — ціль ≥ 48; «Відкрити профіль Ірини»"),
                (2, "Аватар 48", "<code>.avatar--md</code> з позначкою; кільце — у колір сірого списку"),
                (3, "Ім’я й вік", "<code>.person-row__name</code> — 16/700"),
                (4, "Підпис", "<code>.person-row__caption</code> — 14 <code>muted</code>"),
                (5, "Шеврон", "<code>.chevron</code> — Solar, каже «відкриється інший екран»"),
            ]),
        variants=[
            ("Звичайний", stage(ul_group(person_row())), "phone"),
            ("У фокусі", stage(ul_group(person_row("is-focus"))), "phone"),
            ("Завантаження — скелетон", stage(person_row_loading()), "phone"),
        ],
        usage=("<p>Відповідає на «Хто живе в квартирі?» прямо в оголошенні: обличчя, «Ірина, 29 років», «Живе з одним співмешканцем». "
               "Тап веде в профіль — там спосіб життя й перевірка. Посилання для читача екрана — «Відкрити профіль Ірини».</p>"
               "<p>Рядок стоїть у <code>.group</code> під заголовком «Хто живе в квартирі», а нижче, окремим розділом, — «Що підтверджено». "
               "Скелетон — аватар і дві смужки без розділювача.</p>"),
        sources="<code>DESIGN.md</code> → Позначка перевірки, Правки уроку 7–8; <code>microcopy.md</code> → L-16, L-18, L-19, T3, T8",
        do=("людина веде на людину", stage(main_(section_title("Хто живе в квартирі") + ul_group(person_row())), "flush"),
            "<p>Аватар і ім’я обіцяють профіль — і тап відкриває саме профіль.</p>"),
        dont=("рядок людини веде на кімнату",
              stage(ul_group('<li class="group__row"><a class="person-row" href="#" aria-label="Відкрити оголошення">'
                             + avatar("md", mark=False, alt=ROOM_ALT, photo="room-lukianivska-bedroom.jpg")
                             + '<span class="person-row__text"><strong class="person-row__name">Кімната біля Лук’янівської</strong>'
                             + '<span class="person-row__caption">10 500 грн/міс · з 1 жовтня</span></span>'
                             + ico("solar:alt-arrow-right-linear", "chevron") + '</a></li>')),
              "<p>Кругле фото й жирна назва читаються як людина. Кімната в колі втрачає кадр, а ціна потрапляє в підпис.</p>",
              "chat-context", "посилання на кімнату з чату — картка контексту з квадратною мініатюрою."),
    ),

    # ── 9. Головне фото ──
    dict(
        slug="hero-photo", name="Головне фото", group="Картки й списки", api="hero-photo",
        files=["hero-photo.css"],
        classes="<code>.hero-photo</code> — у <code>.shell--photo-top</code>; бирка — <code>.price-tag</code> усередині",
        role="Перше, що бачить людина в оголошенні: фото кімнати на всю ширину 4:3.6, що заходить під статус-бар, з биркою ціни зліва внизу.",
        card_role="Фото оголошення на всю ширину з биркою.",
        preview=photo_top(hero_photo()), preview_mod="flush",
        anatomy=dict(live=stage(photo_top(pin(pin(hero_photo(), "hero-photo", 1, "tr"), "price-tag", 3, "r").replace("<img ", f"<img{P(2, 'c')} ", 1)), "flush"),
            legend=[
                (1, "Контейнер на всю ширину", "<code>.hero-photo</code> — від’ємні бокові поля; верхнє поле знімає <code>.shell--photo-top</code>"),
                (2, "Фото 4:3.6", "<code>.hero-photo &gt; img</code> — без кутів, під статус-бар"),
                (3, "Бирка", "<code>.price-tag</code> — зліва внизу: верх зайнятий кнопками шапки"),
            ]),
        variants=[
            ("З фото", stage(photo_top(hero_photo()), "flush"), "phone"),
            ("Завантаження — скелетон", stage(photo_top(hero_photo(loading=True)), "flush"), "phone"),
        ],
        usage=("<p>Оголошення починається з кімнати, а не з тексту: смак «Airbnb — великі фото» і прохання дизайнера «фото кімнати нема». "
               "Над фото — прозора шапка з круглими «назад» і ⋯ на затемненні, тому бирка переїжджає вниз. На екрані поруч стоїть лічильник «1 / 5» — "
               "він разовий і в кіт не входить.</p>"
               "<p>Головне фото одне на екран. Решту фото квартири показує карусель під ним.</p>"),
        sources="<code>DESIGN.md</code> → Layout, Бирка з ключем; <code>concept.md</code> → атрибут 2; <code>ui/inventory.md</code> → Разове",
        do=("одне фото, а під ним — карусель", stage(photo_top(hero_photo() + gallery()), "flush"),
            "<p>Велике фото задає кімнату, карусель показує решту квартири, не відбираючи фокусу.</p>"),
        dont=("головні фото стопкою як стрічка",
              stage(photo_top(hero_photo() + hero_photo().replace(
                  f'room-lukianivska-bedroom.jpg" alt="{ROOM_ALT}"',
                  'room-tatarka-sofa.jpg" alt="Світла кімната з диваном, комодом, торшером і рослиною"').replace("10 500", "9 800")), "flush"),
              "<p>Фото на всю ширину без назви й мета: людина гортає кадри й не знає, де яка кімната і куди тапати.</p>",
              "listing-card", "у стрічці — картки з назвою, мета й посиланням на оголошення."),
    ),

    # ── 10. Галерея ──
    dict(
        slug="gallery", name="Галерея", group="Картки й списки", api="gallery",
        files=["gallery.css"],
        classes="<code>.gallery</code> · <code>__item</code>",
        role="Інші фото тієї самої квартири під головним: горизонтальна карусель плиток 4:3 по 42% ширини, зі snap і виходом за бокові поля.",
        card_role="Карусель інших фото квартири.",
        preview=photo_top(gallery() + listing_title()), preview_mod="flush",
        anatomy=dict(live=stage(photo_top(pin(pin(pin(gallery(), "gallery", 1, "b"), "gallery__item", 2, "tl"),
                                              "gallery__item", 3, "tr", nth=3)), "flush"),
            legend=[
                (1, "Стрічка", "<code>.gallery</code> — горизонтальний скрол зі snap; від’ємні бокові поля, тож виходить до краю екрана"),
                (2, "Плитка", "<code>.gallery__item</code> — 42% ширини, 4:3, кути 14"),
                (3, "Край наступної", "третя плитка обрізана краєм — підказка, що далі є ще фото"),
            ]),
        variants=[
            ("Фото", stage(photo_top(gallery()), "flush"), "phone"),
            ("Завантаження — 4 скелетони", stage(photo_top(gallery(loading=True)), "flush"), "phone"),
        ],
        usage=("<p>Відповідає на «А що крім кімнати?»: вітальня, кухня, ванна. Кожне фото має опис у <code>alt</code> — "
               "«Спільна кухня з білими шафами й обіднім столом біля вікна», а сама стрічка — «Інші фото квартири».</p>"
               "<p>Стоїть одразу під головним фото, до назви. Фото — тільки з <code>visuals/</code>: один колорит, кімната — інтер’єр.</p>"),
        sources="<code>DESIGN.md</code> → Layout, Shapes; <code>concept.md</code> → атрибут 2; <code>visuals/README.md</code>",
        do=("фото однієї квартири", stage(photo_top(gallery()), "flush"),
            "<p>Усі плитки — про одну кімнату й квартиру, тому їм не потрібні підписи й ціни.</p>"),
        dont=("галерея оголошень",
              stage(photo_top('<ul class="gallery" aria-label="Оголошення">'
                              f'<li class="gallery__item"><img src="{V}room-lukianivska-bedroom.jpg" alt="{ROOM_ALT}"></li>'
                              f'<li class="gallery__item"><img src="{V}room-tatarka-sofa.jpg" alt="Світла кімната з диваном, комодом, торшером і рослиною"></li>'
                              f'<li class="gallery__item"><img src="{V}room-kpi-armchair.jpg" alt="Кімната з ліжком, теракотовим кріслом, торшером і робочим столом"></li>'
                              '</ul>'), "flush"),
              "<p>Різні кімнати в каруселі — без назви, ціни й посилання. Плитка 42% замала, щоб вирішити, чи відкривати оголошення.</p>",
              "listing-card", "різні оголошення — картками у стрічці, кожна з биркою й назвою."),
    ),

    # ── 11. Назва оголошення ──
    dict(
        slug="listing-title", name="Назва оголошення", group="Картки й списки", api="listing-title",
        files=["listing-title.css"],
        classes="<code>.listing-title</code> · <code>__name</code> <code>__meta</code>",
        role="Назва кімнати й коротка мета під фото оголошення. Ціни тут немає — вона на бирці головного фото.",
        card_role="Назва кімнати й мета під фото.",
        preview=listing_title(), preview_mod="",
        anatomy=dict(live=stage(photo_top(pin(hero_photo(), "price-tag", 3, "r")
                                          + pin(pin(listing_title(), "listing-title__name", 1, "r"), "listing-title__meta", 2, "r")), "flush"),
            legend=[
                (1, "Назва", "<code>.listing-title__name</code> — 23/700; на екрані <code>h1</code>; пише людина"),
                (2, "Мета", "<code>.listing-title__meta</code> — 14 <code>muted</code>: район · дата заїзду"),
                (3, "Ціна — не тут", "ціна на <code>.price-tag</code> головного фото; рядок ціни прибрано в уроці 7"),
            ]),
        variants=[
            ("Заповнена", stage(listing_title()), "phone"),
            ("Завантаження — скелетон", stage(listing_title(loading=True)), "phone"),
        ],
        usage=("<p>Назву пише людина — «Кімната біля Лук’янівської» — і ми її не переписуємо й не міняємо регістр. Мета — «Шевченківський район · з 1 жовтня», "
               "рік поточний не пишемо, дата — у формі «з …».</p>"
               "<p>Блок стоїть під каруселлю, далі — список умов квартири. Ціна дублювалась у тексті й на бирці; з уроку 7 вона лише на бирці.</p>"),
        sources="<code>DESIGN.md</code> → Typography (Tag), Правки уроку 7; <code>microcopy.md</code> → L-05, L-12, T6",
        do=("назва й мета, ціна на бирці", stage(photo_top(hero_photo() + listing_title()), "flush"),
            "<p>Одна ціна на екрані — на бирці. Під фото людина читає, що це за кімната і коли можна заїхати.</p>"),
        dont=("ціна в мета",
              stage('<div class="listing-title"><h3 class="listing-title__name">Кімната біля Лук’янівської</h3>'
                    '<p class="listing-title__meta">10 500 грн/місяць · Шевченківський район · з 1 жовтня</p></div>'),
              "<p>Ціна в сірому рядку губиться серед району й дати і дублює бирку — дві ціни на одному екрані.</p>",
              "price-tag", "ціна — тільки на бирці поверх фото."),
    ),

    # ── 12. Підсумок результатів ──
    dict(
        slug="results-meta", name="Підсумок результатів", group="Картки й списки", api="results-meta",
        files=["results-meta.css"],
        classes="<code>.results-meta</code>",
        role="Рядок під фільтрами стрічки: скільки оголошень знайшлось або що зараз відбувається. Один рядок — чотири стани.",
        card_role="Кількість оголошень або статус під фільтрами.",
        preview=main_(chip_row() + results_meta() + card_list(listing_card())), preview_mod="flush",
        anatomy=dict(live=screen(main_(pin(chip_row(), "chip-row", 1, "tl")
                                       + pin(results_meta(), "results-meta", 2, "r").replace("<span>", f"<span{P(3, 'l')}>", 1)
                                       + pin(card_list(listing_card()), "card-list", 4, "tl"))),
            legend=[
                (1, "Над ним — фільтри", "<code>.chip-row</code> — що саме відфільтровано"),
                (2, "Рядок", "<code>.results-meta</code> — 14 <code>muted</code>, ≥ 28; праворуч на екрані — сортування (разове)"),
                (3, "Текст", "кількість або статус; у завантаженні — <code>role=\"status\"</code>"),
                (4, "Під ним — стрічка", "<code>.card-list</code> — те, що порахував рядок"),
            ]),
        variants=[
            ("Результати", stage(results_meta()), ""),
            ("Порожньо", stage(results_meta("0 оголошень")), ""),
            ("Завантаження · <code>role=\"status\"</code>", stage(results_meta("Завантажуємо оголошення", status=True)), ""),
            ("Помилка — фільтри збережено", stage(results_meta("Фільтри збережено")), ""),
        ],
        usage=("<p>Одразу результат, без «успішно» й без «кімнат, що відповідають критеріям»: «12 оголошень», «0 оголошень». Предмет — «оголошення», "
               "не «кімнати» й не «варіанти». Під час завантаження рядок каже «Завантажуємо оголошення» і є живим регіоном для читача екрана.</p>"
               "<p>У помилці рядок лише заспокоює — «Фільтри збережено»: те, що збереглося. Що сталося і що робити — у стані нижче. "
               "Підсумок тихий і сірий: він не дія, тож без коралу.</p>"),
        sources="<code>microcopy.md</code> → LS-11, LS-27, LS-36, E2, T1; <code>ui/inventory.md</code> → Картки й списки",
        do=("кількість одразу", stage(main_(chip_row() + results_meta())),
            "<p>Під фільтрами — число, і людина одразу бачить, чи варто звужувати пошук.</p>"),
        dont=("текст помилки в мета",
              stage(results_meta("Не вдалося завантажити оголошення. Перевір з’єднання й спробуй ще.")),
              "<p>Сірий дрібний рядок без іконки й кнопки: помилку легко не помітити, а «Спробувати ще» нема куди поставити.</p>",
              "state", "помилка — стан по центру з трикутником, поясненням і «Спробувати ще»; у мета лишається «Фільтри збережено»."),
    ),
]

#!/usr/bin/env python3
"""Гейт дизайн-системи «Кутка».

Перевіряє, що дизайн-файли не вносять значень повз систему:
  — токен (var(--x)), якого немає в design-system/tokens.css;
  — хардкод: hex, rgb()/hsl()…, назва кольору, назва шрифту, px/rem/ms…;
  — колір-primitive в обхід semantic-ролі (--coral замість --color-action);
  — новий токен, оголошений поза tokens.css;
  — власний <style> чи style="" на екрані або в патерні;
  — клас, якого немає в design-system/ (компонент з'явився на екрані раніше,
    ніж у системі);
  — компонент без збірки в components/index.css чи без сторінки в docs/;
  — патерн без рядка в patterns/README.md;
  — порушення будови tokens.css (semantic — лише var() на primitive, темна
    тема — лише semantic);
  — рух повз правила DESIGN.md «Анімація»: primitive руху (--duration-*,
    --curve-*) напряму замість ролі --dur-*/--ease-*; transition чи @keyframes
    на чомусь, крім transform і opacity; рух без prefers-reduced-motion у файлі;
    тривалість чи затримка числом або не з ролі --dur-*; крива ключовим словом
    чи cubic-bezier() замість --ease-*; transition без властивості (= all);
    немає глобального блоку prefers-reduced-motion у components/base.css
    (*, ::before, ::after: тривалість --dur-instant, повтор 1, прокрутка auto);
    JS компонента анімує (animate/setKeyframes) щось, крім transform і opacity,
    чи пише тривалість числом. Перевірка руху діє в усіх рівнях, і у вітрині.

Рівні перевірки (див. SCOPES нижче):
  product  — компоненти, screens.css, екрани, патерни, приклади: суворо,
             жодного сирого значення, крім 0, 1 і 100%;
  showcase — вітрина ui/*.html і docs/: каркас сторінки може мати свою
             геометрію (ширина колонки, висота сцени), але колір, шрифт і
             токени — лише з системи.

Запуск:  python3 design-system/_gate.py            — усе, код виходу 1 при помилці
         python3 design-system/_gate.py ФАЙЛ…      — показати лише ці файли
         python3 design-system/_gate.py --hook     — для хука Claude Code (stdin JSON)
Згенеровані HTML перевіряються як є: спершу _build.py, потім гейт.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DS = "design-system"
TOKENS = f"{DS}/tokens.css"

# Що перевіряємо і як суворо
SCOPES = {
    "component": [f"{DS}/components/*.css"],
    "screen-css": ["wireframes/screens.css"],
    "screen": ["wireframes/*.html"],
    "pattern": [f"{DS}/patterns/*.html"],
    "example": [f"{DS}/examples/*.html", f"{DS}/examples/*.css"],
    "showcase": ["ui/*.html", f"{DS}/docs/*.html", f"{DS}/docs/*.css"],
}
PRODUCT = {"component", "screen-css", "screen", "pattern", "example"}

# Класи-гачки для JS, без стилів у кіті. Новий гачок — рядок тут (видно в diff).
JS_HOOKS = {
    "theme-toggle",  # кнопка-місяць: перемикає data-theme (design-system/theme.js)
    "status-dark",   # позначка для мокапа хабу уроків: темний статус-бар над фото
}

# Сторінки, які дозволено підключати (відносно кореня репо)
ALLOWED_LINKS = {
    "screen": {f"{DS}/index.css", "wireframes/screens.css"},
    "pattern": {f"{DS}/index.css"},
    "example": {f"{DS}/index.css"},
}

NAMED_COLORS = set("""
aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue
blueviolet brown burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk
crimson cyan darkblue darkcyan darkgoldenrod darkgray darkgreen darkgrey darkkhaki
darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen
darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue
dimgray dimgrey dodgerblue firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite
gold goldenrod gray green greenyellow grey honeydew hotpink indianred indigo ivory khaki
lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan
lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen
lightskyblue lightslategray lightslategrey lightsteelblue lightyellow lime limegreen linen
magenta maroon mediumaquamarine mediumblue mediumorchid mediumpurple mediumseagreen
mediumslateblue mediumspringgreen mediumturquoise mediumvioletred midnightblue mintcream
mistyrose moccasin navajowhite navy oldlace olive olivedrab orange orangered orchid
palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum
powderblue purple rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown
seagreen seashell sienna silver skyblue slateblue slategray slategrey snow springgreen
steelblue tan teal thistle tomato turquoise violet wheat white whitesmoke yellow yellowgreen
""".split())
# Властивості, де слово — ім'я, а не колір
NAME_PROPS = {"animation-name", "animation", "grid-area", "grid-template-areas", "content",
              "counter-reset", "counter-increment", "view-transition-name", "container-name",
              "transition-property", "will-change", "list-style-type"}
FONT_KEYWORDS = {"inherit", "initial", "unset", "revert", "normal"}

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
COLOR_FN = re.compile(r"\b(rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|color-mix|light-dark)\(", re.I)
NUMBER = re.compile(r"(?<![\w.#-])(-?(?:\d+\.?\d*|\.\d+))([a-zA-Z%]*)")
UNITS = {"px", "rem", "em", "ex", "ch", "lh", "rlh", "vw", "vh", "vmin", "vmax", "dvh", "svh",
         "lvh", "dvw", "svw", "lvw", "cqw", "cqh", "cqi", "cqb", "cm", "mm", "in", "pt", "pc",
         "q", "deg", "rad", "grad", "turn", "s", "ms", "hz", "khz", "dpi", "dppx", "x", "%"}
VAR = re.compile(r"var\(\s*(--[\w-]+)\s*(,)?")
TOKEN_PROPS = {"font-weight", "line-height", "z-index", "letter-spacing"}  # число без одиниці — теж токен

# Рух (DESIGN.md «Анімація»): ролі — semantic, primitive — лише в tokens.css
MOTION_ROLE = re.compile(r"--(dur|ease|move)-")
MOTION_PRIM = re.compile(r"--(duration|curve)-")
MOTION_PROPS = {"transform", "opacity"}   # що дозволено анімувати; фокус, колір, розмір — миттєво
# Де стоять тривалості й криві (DESIGN.md «Анімація» → «Ціна кадру»)
TIME_PROPS = {"transition", "transition-duration", "transition-delay",
              "animation", "animation-duration", "animation-delay"}
EASE_PROPS = {"transition-timing-function", "animation-timing-function"}
TIME_NUM = re.compile(r"(?<![\w.#-])(-?(?:\d+\.?\d*|\.\d+))(ms|s)\b", re.I)
EASE_RAW = re.compile(r"(?<![\w-])(ease(?:-in-out|-in|-out)?|linear|step-start|step-end|cubic-bezier|steps)(?![\w-])", re.I)
# Глобальний блок «менше руху» (components/base.css): селектор і обов'язкові оголошення
REDUCED_FILE = f"{DS}/components/base.css"
REDUCED_SELECTORS = {"*", "*::before", "*::after"}
REDUCED_DECLS = {
    "animation-duration": r"var\(--dur-instant\)",
    "animation-iteration-count": r"1",
    "transition-duration": r"var\(--dur-instant\)",
    "scroll-behavior": r"auto",
}


class Report:
    def __init__(self):
        self.errors = []    # (file, line, msg)
        self.warnings = []

    def err(self, f, line, msg):
        self.errors.append((f, line, msg))

    def warn(self, f, line, msg):
        self.warnings.append((f, line, msg))


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def blank(m):
    """Замінити збіг пробілами, зберігши переноси — щоб не збити номери рядків."""
    return re.sub(r"[^\n]", " ", m.group(0))


def strip_css(text):
    text = re.sub(r"/\*.*?\*/", blank, text, flags=re.S)
    text = re.sub(r"url\((?:\"[^\"]*\"|'[^']*'|[^)]*)\)", lambda m: "url()" + blank(m)[5:], text)
    return text


def declarations(css):
    """(offset, prop, value) з найглибших блоків { … } — селектори й @-правила не чіпаємо."""
    for block in re.finditer(r"\{([^{}]*)\}", css):
        start = block.start(1)
        pos = 0
        for part in block.group(1).split(";"):
            if ":" in part:
                prop, value = part.split(":", 1)
                if prop.strip():
                    off = start + pos + len(prop) - len(prop.lstrip())
                    yield off, prop.strip().lower(), value.strip()
            pos += len(part) + 1


def line_of(text, off, base=1):
    return base + text.count("\n", 0, off)


# ── tokens.css ──────────────────────────────────────────────────────────

def is_pure_color(value):
    v = value.strip()
    return bool(re.fullmatch(r"#[0-9a-fA-F]{3,8}", v) or re.fullmatch(r"(rgba?|hsla?)\([^()]*\)", v)
                or v.lower() in NAMED_COLORS)


def load_tokens(rep):
    raw = read(TOKENS)
    css = strip_css(raw)
    root, dark = {}, {}
    for block in re.finditer(r"([^{}]*)\{([^{}]*)\}", css):
        sel = " ".join(block.group(1).split())
        target = dark if 'data-theme="dark"' in sel else root if ":root" in [s.strip() for s in re.split(r"[,;]", sel)] else None
        if target is None:
            continue
        for off, prop, value in declarations(css[block.start(2) - 1:block.end(2) + 1]):
            line = line_of(css, block.start(2) - 1 + off)
            if prop.startswith("--"):
                target[prop] = (value, line)
            elif not (prop == "color-scheme"):
                rep.err(TOKENS, line, f"у блоці токенів властивість {prop} — тут лише оголошення --*")

    color_prims = {n for n, (v, _) in root.items() if not n.startswith("--color-") and is_pure_color(v)}

    for name, (value, line) in root.items():
        for ref, _ in VAR.findall(value):
            if ref not in root:
                rep.err(TOKENS, line, f"{name} посилається на {ref}, якого немає в :root")
        if name.startswith("--color-"):
            m = re.fullmatch(r"var\((--[\w-]+)\)", value)
            if not m:
                rep.err(TOKENS, line, f"semantic {name} = «{value}»: роль — лише var() на primitive, без сирих значень")
            elif m.group(1).startswith("--color-"):
                rep.err(TOKENS, line, f"semantic {name} посилається на роль {m.group(1)}: роль — var() на primitive")
            elif m.group(1) not in color_prims and m.group(1) in root:
                rep.err(TOKENS, line, f"semantic {name} посилається на {m.group(1)}, а це не колір-primitive")
        elif MOTION_ROLE.match(name):
            m = re.fullmatch(r"var\((--[\w-]+)\)", value)
            if not m:
                rep.err(TOKENS, line, f"semantic {name} = «{value}»: роль руху — лише var() на primitive")
            elif MOTION_ROLE.match(m.group(1)) or m.group(1).startswith("--color-"):
                rep.err(TOKENS, line, f"semantic {name} посилається на роль {m.group(1)}: роль — var() на primitive")
        elif "--color-" in value or any(MOTION_ROLE.match(r) for r, _ in VAR.findall(value)):
            rep.err(TOKENS, line, f"primitive {name} посилається на роль: primitive не знає ролей")

    for name, (value, line) in dark.items():
        if not name.startswith("--color-"):
            rep.err(TOKENS, line, f"темна тема перевизначає {name}: лише semantic --color-*")
            continue
        if name not in root:
            rep.err(TOKENS, line, f"темна тема вводить {name}, якого немає в :root — нова роль спершу у світлій")
        m = re.fullmatch(r"var\((--[\w-]+)\)", value)
        if not m or m.group(1) not in color_prims:
            rep.err(TOKENS, line, f"темна {name} = «{value}»: лише var() на колір-primitive")

    contrast_check(raw, root, rep)
    breakpoints = {v: n for n, (v, _) in root.items() if n.startswith("--bp-")}
    return set(root), color_prims, breakpoints


def contrast_check(raw, root, rep):
    """Попередження: роль, перевизначена в темі, без жодного рядка контрасту в таблицях."""
    comments = re.findall(r"/\*.*?\*/", raw, flags=re.S)
    rows = [l for c in comments for l in c.split("\n") if re.search(r"\d+\.\d+", l) and "--color-" in l]
    for name in root:
        if not name.startswith("--color-"):
            continue
        short = name[len("--color"):]
        if not any(re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", r)
                   or re.search(rf"(?<![\w-]){re.escape(short)}(?![\w-])", r) for r in rows):
            rep.warn(TOKENS, None, f"роль {name} не має рядка в таблицях контрасту (якщо вона під текстом чи іконкою — допиши пару)")


# ── CSS-значення ───────────────────────────────────────────────────────

def component_api(rep):
    """Локальні змінні компонентів: читаються через var(--x, фолбек) і не є токенами.
    Повертає (прочитані, оголошені в components/)."""
    read_vars, declared = set(), {}
    for rel in sorted(glob.glob(f"{DS}/components/*.css", root_dir=ROOT)):
        css = strip_css(read(rel))
        for off, prop, value in declarations(css):
            if prop.startswith("--"):
                declared.setdefault(prop, rel)
            for ref, fb in VAR.findall(value):
                if fb:
                    read_vars.add(ref)
    return read_vars, declared


def check_value(rel, line, prop, value, scope, ctx, rep):
    tokens, color_prims, api = ctx["tokens"], ctx["color_prims"], ctx["api"]
    product = scope in PRODUCT

    if prop.startswith("--"):
        if prop in tokens:
            rep.err(rel, line, f"{prop} перевизначено поза tokens.css — значення токена міняється лише там")
        elif prop not in api:
            rep.err(rel, line, f"новий токен {prop} поза tokens.css — значення додається в tokens.css відповідним рівнем")

    for ref, fb in VAR.findall(value):
        if ref not in tokens and ref not in api:
            rep.err(rel, line, f"var({ref}) — такого токена немає в tokens.css")
        elif ref in color_prims:
            rep.err(rel, line, f"var({ref}) — колір-primitive напряму; колір береться лише через роль --color-*")
        elif MOTION_PRIM.match(ref):
            rep.err(rel, line, f"var({ref}) — primitive руху напряму; рух лише через --dur-*, --ease-*, --move-*")

    if prop in ("transition", "transition-property"):
        for seg in VAR.sub(" ", value).split(","):
            words = re.findall(r"[a-zA-Z][\w-]*", seg.replace("!important", " "))
            target = words[0].lower() if words else ""
            if prop == "transition" and target in ("ease", "ease-in", "ease-out", "ease-in-out", "linear",
                                                   "step-start", "step-end", "steps", "cubic-bezier"):
                target = ""
            if target and target != "none" and target not in MOTION_PROPS:
                rep.err(rel, line, f"{prop}: анімується «{target}» — лише transform і opacity (DESIGN.md «Анімація»); "
                                   "колір, рамка й кільце фокусу міняються миттєво")
            elif prop == "transition" and not target and seg.strip():
                rep.err(rel, line, "transition без властивості — це all (розмір, колір, відступи); "
                                   "назви transform чи opacity (DESIGN.md «Анімація»)")
    check_timing(rel, line, prop, value, rep, ctx["tokens"])

    rest = VAR.sub(" ", value)
    rest = re.sub(r"\"[^\"]*\"|'[^']*'", " ", rest) if prop not in ("font-family", "font") else rest

    if HEX.search(rest):
        rep.err(rel, line, f"{prop}: hex «{HEX.search(rest).group(0)}» — колір лише з --color-*")
    m = COLOR_FN.search(rest)
    if m:
        rep.err(rel, line, f"{prop}: {m.group(1)}() — новий колір повз tokens.css")
    if prop not in NAME_PROPS and not prop.startswith("--"):
        for word in re.findall(r"(?<![\w-])[a-zA-Z]+(?![\w(-])", rest):
            if word.lower() in NAMED_COLORS:
                rep.err(rel, line, f"{prop}: колір «{word}» — колір лише з --color-*")
    if prop in ("font-family", "font"):
        names = [w.strip(" \"'()") for w in rest.split(",") if w.strip(" \"'()")]
        if any(n.lower() not in FONT_KEYWORDS for n in names):
            rep.err(rel, line, f"{prop}: «{rest.strip()}» — шрифт лише var(--font-*), розмір і вага — токенами поштучно")

    if not product:
        return
    for num, unit in NUMBER.findall(rest):
        unit_l = unit.lower()
        n = float(num)
        if unit_l == "fr" or (unit_l in ("s", "ms") and prop in TIME_PROPS):
            continue   # тривалість — check_timing, щоб не дублювати
        if unit_l in UNITS:
            if n == 0 or (unit_l == "%" and n == 100):
                continue
            rep.err(rel, line, f"{prop}: «{num}{unit}» — сире значення; шукай primitive у tokens.css (--space-*, --size-*, --radius-*, --pct-*…)")
        elif unit_l == "":
            if prop in TOKEN_PROPS and not (prop == "z-index" and n == 0):
                rep.err(rel, line, f"{prop}: «{num}» — значення з токена (--weight-*, --leading-*, --z-*, --tracking-*)")
            elif prop == "opacity" and n not in (0, 1):
                rep.err(rel, line, f"opacity: «{num}» — значення з токена (--opacity-*)")
        elif unit_l not in ("e",):
            rep.err(rel, line, f"{prop}: «{num}{unit}» — невідома одиниця, значення лише з tokens.css")


def top_level_split(value):
    """Кома між шарами transition/animation — не кома всередині var(…, фолбек)."""
    parts, depth, cur = [], 0, ""
    for ch in value:
        depth += {"(": 1, ")": -1}.get(ch, 0)
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    return parts + [cur]


def check_timing(rel, line, prop, value, rep, tokens):
    """Тривалість, затримка й крива — лише ролі руху (DESIGN.md «Анімація»):
    число в ms/s, ключове слово кривої чи cubic-bezier() — дефект у будь-якому
    рівні, і у вітрині теж; токен не тієї родини (--space-* як тривалість) — теж."""
    if prop not in TIME_PROPS and prop not in EASE_PROPS:
        return
    bare = VAR.sub(" ", value)
    for num, unit in TIME_NUM.findall(bare):
        if float(num) != 0:
            rep.err(rel, line, f"{prop}: тривалість «{num}{unit}» записана числом — лише var(--dur-*) з tokens.css "
                               "(нова — спершу primitive --duration-* і роль)")
    m = EASE_RAW.search(bare)
    if m:
        rep.err(rel, line, f"{prop}: крива «{m.group(1)}» — лише var(--ease-*) з tokens.css")
    refs = [r for r, _ in VAR.findall(value)]
    allowed = {"transition-duration": "dur", "animation-duration": "dur", "transition-delay": "dur",
               "animation-delay": "dur", "transition-timing-function": "ease",
               "animation-timing-function": "ease"}.get(prop, "dur|ease")
    for ref in refs:   # локальна змінна компонента (--i — індекс літери) — множник, не тривалість
        if ref in tokens and not re.match(rf"--({allowed})-", ref):
            rep.err(rel, line, f"{prop}: var({ref}) — тривалість і крива лише з ролей --dur-* / --ease-*")
    if prop in EASE_PROPS and not refs and bare.strip().lower() not in ("inherit", "initial", "unset", "revert"):
        rep.err(rel, line, f"{prop}: «{value}» — крива лише var(--ease-*)")
    if prop in ("transition", "animation"):
        if bare.strip().lower() in ("none", "inherit", "initial", "unset", "revert"):
            return
        for seg in top_level_split(value):
            if seg.strip() and not re.search(r"var\(\s*--dur-", seg):
                rep.err(rel, line, f"{prop}: «{seg.strip()}» — тривалість не з токена; задай var(--dur-*)")


def check_reduced_global(rep):
    """Глобальний блок «менше руху» у components/base.css — страховка поверх
    блоків компонентів: *, *::before, *::after — тривалість --dur-instant,
    повтор 1, прокрутка auto (DESIGN.md «Анімація» → «Ціна кадру»)."""
    css = strip_css(read(REDUCED_FILE))
    found = {}
    for m in re.finditer(r"@media\s*\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)\s*\{", css):
        depth, i = 1, m.end()
        while depth and i < len(css):
            depth += {"{": 1, "}": -1}.get(css[i], 0)
            i += 1
        for rule in re.finditer(r"([^{}]+)\{([^{}]*)\}", css[m.end():i - 1]):
            sels = {re.sub(r"\s+", "", x) for x in rule.group(1).split(",")}
            if REDUCED_SELECTORS <= sels:
                for _, prop, value in declarations("{" + rule.group(2) + "}"):
                    found[prop] = value.replace("!important", "").strip()
    missing = [f"{p}: {v.replace(chr(92), '')}" for p, v in REDUCED_DECLS.items()
               if not re.fullmatch(v, found.get(p, ""))]
    if missing:
        rep.err(REDUCED_FILE, None,
                "немає глобального @media (prefers-reduced-motion: reduce) { *, *::before, *::after { … } } "
                f"або в ньому бракує: {'; '.join(missing)} (DESIGN.md «Анімація» → «Ціна кадру»)")


def check_js_motion(rep):
    """JS компонента не анімує повз CSS-правила: у animate()/setKeyframes() —
    лише transform, opacity (і службові offset, easing, composite); тривалість
    числом у JS — дефект."""
    service = {"offset", "easing", "composite"}
    for rel in sorted(glob.glob(f"{DS}/components/*.js", root_dir=ROOT)):
        js = re.sub(r"/\*.*?\*/|//[^\n]*", blank, read(rel), flags=re.S)
        for m in re.finditer(r"\.(animate|setKeyframes)\s*\(", js):
            depth, i = 1, m.end()
            while depth and i < len(js):
                depth += {"(": 1, ")": -1}.get(js[i], 0)
                i += 1
            args = js[m.end():i - 1]
            for key in re.findall(r"[{,]\s*[\"']?([A-Za-z-]+)[\"']?\s*:", args):
                k = re.sub(r"[A-Z]", lambda c: "-" + c.group(0).lower(), key)
                if k in ("duration", "delay", "end-delay", "iterations", "fill", "direction"):
                    if re.search(rf"{key}\s*:\s*\d", args):
                        rep.err(rel, line_of(js, m.start()), f"{m.group(1)}(): {key} числом — тривалість лише з --dur-* (читай getComputedStyle)")
                elif k not in MOTION_PROPS and k not in service:
                    rep.err(rel, line_of(js, m.start()), f"{m.group(1)}() анімує {k} — лише transform і opacity (DESIGN.md «Анімація»)")


def check_css(rel, text, scope, ctx, rep, base_line=1):
    css = strip_css(text)
    for off, prop, value in declarations(css):
        check_value(rel, line_of(css, off, base_line), prop, value, scope, ctx, rep)
    if scope in PRODUCT:
        check_media(rel, css, ctx, rep, base_line)
    check_motion(rel, css, rep, base_line)


def check_motion(rel, css, rep, base_line):
    """@keyframes — лише transform і opacity; рух у файлі — лише разом із
    @media (prefers-reduced-motion) у тому ж файлі (DESIGN.md «Анімація»)."""
    for m in re.finditer(r"@keyframes\s+[\w-]+\s*\{((?:[^{}]*\{[^{}]*\})*)[^{}]*\}", css):
        for off, prop, _ in declarations(m.group(1)):
            if prop not in MOTION_PROPS:
                rep.err(rel, line_of(css, m.start(1) + off, base_line),
                        f"@keyframes анімує {prop} — лише transform і opacity (DESIGN.md «Анімація»)")
    moving = [off for off, prop, value in declarations(css)
              if (prop in ("transition", "animation", "animation-name") and value.strip().lower() != "none")]
    if moving and "prefers-reduced-motion" not in css:
        rep.err(rel, line_of(css, moving[0], base_line),
                "рух без @media (prefers-reduced-motion: reduce) у цьому файлі — зсуви й масштаб мусять вимикатися, статус лишатися видимим")


def check_media(rel, css, ctx, rep, base_line):
    """var() у @media не працює, тож межа пишеться числом — і це число мусить
    дорівнювати значенню --bp-* з tokens.css (DESIGN.md → «Адаптив»)."""
    bps = ctx["breakpoints"]
    for m in re.finditer(r"@(?:media|container)\b([^{;]*)", css):
        for num in re.finditer(r"(?<![\w.-])(\d*\.?\d+)([a-z%]+)", m.group(1)):
            if num.group(0) not in bps:
                known = ", ".join(f"{n} = {v}" for v, n in sorted(bps.items(), key=lambda kv: kv[1]))
                rep.err(rel, line_of(css, m.start(1) + num.start(), base_line),
                        f"межа «{num.group(0)}» в @-правилі не є значенням --bp-* ({known}): "
                        "нова межа — спершу токен у tokens.css")


# ── HTML ─────────────────────────────────────────────────────────────────

def check_html(rel, scope, ctx, rep):
    raw = read(rel)
    html = re.sub(r"<script\b.*?</script>|<!--.*?-->", blank, raw, flags=re.S | re.I)
    product = scope in PRODUCT

    for m in re.finditer(r"<style\b[^>]*>(.*?)</style>", html, flags=re.S | re.I):
        line = line_of(html, m.start())
        if product:
            rep.err(rel, line, "власний <style> — стилі лише з design-system/ (разове на екрані — wireframes/screens.css)")
        check_css(rel, m.group(1), scope, ctx, rep, base_line=line_of(html, m.start(1)))

    for m in re.finditer(r"\sstyle\s*=\s*(\"[^\"]*\"|'[^']*')", html, flags=re.I):
        line = line_of(html, m.start())
        body = m.group(1)[1:-1]
        if product and not all(d.split(":", 1)[0].strip().startswith("--") for d in body.split(";") if d.strip()):
            rep.err(rel, line, f"style=\"{body.strip()[:60]}\" — інлайн-стиль; лише перемикання локальної змінної компонента")
        check_css(rel, "x{" + body + "}", scope, ctx, rep, base_line=line)

    for m in re.finditer(r"\s(fill|stroke|color|bgcolor|stop-color|flood-color)\s*=\s*\"([^\"]*)\"", html, flags=re.I):
        v = m.group(2).strip()
        if HEX.search(v) or COLOR_FN.search(v) or v.lower() in NAMED_COLORS:
            rep.err(rel, line_of(html, m.start()), f"{m.group(1)}=\"{v}\" — колір в атрибуті; лише currentColor або --color-*")

    if scope in ALLOWED_LINKS:
        here = os.path.dirname(rel)
        for m in re.finditer(r"<link\b[^>]*rel=\"stylesheet\"[^>]*>", html, flags=re.I):
            href = re.search(r"href=\"([^\"]+)\"", m.group(0))
            if not href or href.group(1).startswith(("http:", "https:")):
                continue
            target = os.path.normpath(os.path.join(here, href.group(1)))
            if target not in ALLOWED_LINKS[scope]:
                rep.err(rel, line_of(html, m.start()),
                        f"підключено {href.group(1)} — споживач бере лише design-system/index.css (один пакет)")

        defined = ctx["classes_ds"] | (ctx["classes_screens"] if scope == "screen" else set())
        seen = set()
        for m in re.finditer(r"\sclass=\"([^\"]*)\"", html):
            for cls in m.group(1).split():
                if cls in defined or cls in JS_HOOKS or cls in seen:
                    continue
                seen.add(cls)
                where = "у design-system/" + ("" if scope != "screen" else " чи wireframes/screens.css")
                rep.err(rel, line_of(html, m.start()),
                        f"клас .{cls} не визначено {where} — нове спершу з'являється в системі, потім на екрані")


def classes_in(paths):
    out = set()
    for rel in paths:
        css = strip_css(read(rel))
        selectors = re.sub(r"\{[^{}]*\}", " ", css)
        out |= set(re.findall(r"\.(-?[_a-zA-Z][\w-]*)", selectors))
    return out


# ── Склад системи ─────────────────────────────────────────────────────────

def check_inventory(rep):
    comp_dir = f"{DS}/components"
    index = re.sub(r"/\*.*?\*/", "", read(f"{comp_dir}/index.css"), flags=re.S)
    imported = set(re.findall(r"@import\s+(?:url\()?[\"']?([\w./-]+\.css)", index))
    docs = {os.path.basename(p): read(p) for p in glob.glob(f"{DS}/docs/*.html", root_dir=ROOT)}
    for imp in sorted(imported):
        if not os.path.exists(os.path.join(ROOT, comp_dir, imp)):
            rep.err(f"{comp_dir}/index.css", None, f"@import {imp} — файлу немає")
    for rel in sorted(glob.glob(f"{comp_dir}/*.css", root_dir=ROOT)):
        name = os.path.basename(rel)
        if name == "index.css":
            continue
        if name not in imported:
            rep.err(rel, None, "компонент не зібрано в components/index.css — споживачі його не отримають")
        stem = name[:-4]
        if f"{stem}.html" not in docs and not any(f"components/{name}" in d for d in docs.values()):
            rep.err(rel, None, f"немає документації: docs/{stem}.html (або згадки components/{name} на сторінці docs/) — "
                               "допиши сторінку в docs/_pages_*.py і збери docs/_build.py")

    readme = read(f"{DS}/patterns/README.md")
    for rel in sorted(glob.glob(f"{DS}/patterns/*.html", root_dir=ROOT)):
        if os.path.basename(rel) not in readme:
            rep.err(rel, None, "патерн без рядка в patterns/README.md (що за композиція, де стоїть — щонайменше 3 екрани)")


# ── Запуск ───────────────────────────────────────────────────────────────

def run():
    rep = Report()
    tokens, color_prims, breakpoints = load_tokens(rep)
    api_read, api_declared = component_api(rep)
    api = (api_read | set(api_declared)) - tokens
    for name in sorted(set(api_declared) - api_read - tokens):
        rep.err(api_declared[name], None, f"компонент оголошує {name}, але жоден компонент його не читає через var({name}, фолбек) — "
                                          "якщо це значення, місце йому в tokens.css")
    ctx = {
        "tokens": tokens,
        "color_prims": color_prims,
        "breakpoints": breakpoints,
        "api": api,
        "classes_ds": classes_in(sorted(glob.glob(f"{DS}/components/*.css", root_dir=ROOT))),
        "classes_screens": classes_in(["wireframes/screens.css"]),
    }
    for scope, patterns in SCOPES.items():
        for pat in patterns:
            for rel in sorted(glob.glob(pat, root_dir=ROOT)):
                if rel.endswith(".css"):
                    check_css(rel, read(rel), scope, ctx, rep)
                else:
                    check_html(rel, scope, ctx, rep)
    check_inventory(rep)
    check_reduced_global(rep)
    check_js_motion(rep)
    return rep


def fmt(items):
    return "\n".join(f"  {f}{':' + str(l) if l else ''}  {m}" for f, l, m in items)


# ── Заборона браузерної автоматизації (wireframes/_conventions.md) ──────
# PreToolUse-хук: Playwright і headless-браузери — лише коли користувач прямо
# попросив саме їх у поточному запиті. Тоді він сам створює прапорець
# `! touch .claude/allow-browser`; хук пропускає ОДНУ команду і стирає його.
BROWSER = re.compile(r"playwright|ms-playwright|puppeteer|chrom(e|ium)\b|chrome-headless|headless[-_ ]shell"
                     r"|--headless|wkhtmlto|firefox|webkit|selenium", re.I)
ALLOW_FLAG = ".claude/allow-browser"


def guard_browser():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    tool = data.get("tool_name") or ""
    cmd = (data.get("tool_input") or {}).get("command") or ""
    hit = tool if tool.startswith("mcp__") else (BROWSER.search(cmd).group(0) if BROWSER.search(cmd) else "")
    if not hit:
        return 0
    flag = os.path.join(ROOT, ALLOW_FLAG)
    if os.path.exists(flag):
        os.remove(flag)
        return 0
    print(f"Заблоковано: «{hit}» — Playwright і headless-браузери в цьому проєкті заборонені "
          "(wireframes/_conventions.md, «Головне правило перевірки»). Перевіряй гейтом і читанням CSS. "
          f"Дозвіл дає лише користувач: `! touch {ALLOW_FLAG}` — на одну команду.", file=sys.stderr)
    return 2


def main(argv):
    if "--guard-browser" in argv:
        return guard_browser()
    hook = "--hook" in argv
    only = [a for a in argv if not a.startswith("--")]
    if hook:
        try:
            data = json.load(sys.stdin)
            path = (data.get("tool_input") or {}).get("file_path") or ""
        except (ValueError, AttributeError):
            return 0
        rel = os.path.relpath(os.path.abspath(path), ROOT) if path else ""
        if not rel.startswith((f"{DS}/", "wireframes/", "ui/")) or not rel.endswith((".css", ".html", ".js")):
            return 0
        only = [rel]

    rep = run()
    errors = rep.errors
    if only:
        wanted = {os.path.normpath(os.path.relpath(os.path.abspath(p), ROOT)) for p in only}
        errors = [e for e in errors if os.path.normpath(e[0]) in wanted or e[0] == TOKENS and TOKENS in wanted]

    out = sys.stderr if hook else sys.stdout
    if rep.warnings and not hook:
        print(f"Попередження ({len(rep.warnings)}):\n{fmt(rep.warnings)}\n", file=out)
    if errors:
        print(f"Гейт дизайн-системи — порушень: {len(errors)}.\n{fmt(errors)}\n\n"
              "Правило: нове спершу з'являється в design-system/, потім на екрані — ніколи навпаки. "
              "Як додати значення, компонент чи патерн — CLAUDE.md і DESIGN.md, розділ «Внесок у систему».",
              file=out)
        return 2 if hook else 1
    if not hook:
        print("Гейт дизайн-системи: чисто.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

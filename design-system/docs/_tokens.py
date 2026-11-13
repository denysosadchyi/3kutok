"""Сторінка «Токени» (урок 9): читає design-system/tokens.css при збірці.

Два рівні — PRIMITIVE (сирі значення) і SEMANTIC (ролі кольору, світла й
темна). Зразки кольору фарбує сам tokens.css: зразок ролі стоїть у
data-theme="light" і data-theme="dark", тож показує значення обох тем без
жодного літерала на сторінці. Таблиці контрасту — дослівно з коментарів.
"""
import re
from html import escape
from pathlib import Path

TOKENS = Path(__file__).resolve().parent.parent / "tokens.css"
DESCRIPTION = "Усі токени дизайн-системи «Кутка»: primitive-значення, semantic-ролі кольору у світлій і темній темі, ролі руху, контраст пар."


def _blocks(css):
    """[(селектор, [(коментар над, назва, значення)])] з tokens.css."""
    out = []
    for m in re.finditer(r"([^{}]*)\{([^{}]*)\}", css):
        sel = " ".join(re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S).split())
        rows, note = [], ""
        for t in re.finditer(r"/\*(.*?)\*/|(--[\w-]+)\s*:\s*([^;]+);", m.group(2), flags=re.S):
            if t.group(1) is not None:
                note = " ".join(t.group(1).split())
            else:
                rows.append((note, t.group(2), " ".join(t.group(3).split())))
                note = ""
        out.append((sel, rows))
    return out


def _contrast(css):
    """Таблиці контрасту — коментарі від «Контраст …» до кінця коментаря."""
    return [m.group(0) for m in re.finditer(r"── Контраст.*?(?=\*/)", css, flags=re.S)]


def _sw(name, theme):
    t = f' data-theme="{theme}"'
    return f'<span class="doc-swatch"{t} style="background: var({name})" aria-hidden="true"></span>'


def body():
    css = TOKENS.read_text(encoding="utf-8")
    blocks = _blocks(css)
    prim = next(r for s, r in blocks if s.endswith(":root") and not s.startswith(":root,"))
    light = dict((n, (v, c)) for s, r in blocks if s.startswith(":root, [data-theme=\"light\"]") for c, n, v in r)
    dark = dict((n, v) for s, r in blocks if 'data-theme="dark"' in s for _, n, v in r)
    # Ролі руху — другий блок :root (SEMANTIC — рух), від теми не залежать
    motion = [(n, v, c) for s, r in blocks if s == ":root" for c, n, v in r if re.match(r"--(dur|ease|move)-", n)]
    motion_rows = "".join(
        f'<tr><td><code>{n}</code></td><td><code>{escape(v)}</code></td><td>{escape(c)}</td></tr>'
        for n, v, c in motion)

    groups = {}
    for _, n, v in prim:
        key = re.match(r"--([a-z]+)", n).group(1)
        groups.setdefault(key, []).append((n, v))
    # Зразків у primitive немає свідомо: колір-primitive напряму не читає ніхто, навіть docs (гейт);
    # колір видно в semantic-таблиці нижче — через роль.
    prim_rows = "".join(
        f'<tr><td><code>{n}</code></td><td><code>{escape(v)}</code></td></tr>'
        for k in groups for n, v in groups[k])
    sem_rows = "".join(
        f'<tr><td><code>{n}</code></td>'
        f'<td>{_sw(n, "light")}<code>{escape(v)}</code></td>'
        f'<td>{_sw(n, "dark")}<code>{escape(dark.get(n, v))}</code></td>'
        f'<td>{escape(c)}</td></tr>'
        for n, (v, c) in light.items() if n.startswith("--color-"))
    contrast = "".join(f'<pre class="doc-pre">{escape(t.strip())}</pre>' for t in _contrast(css))
    n_prim, n_sem, n_mot = len(prim), sum(1 for n in light if n.startswith("--color-")), len(motion)
    return (
        '<header class="doc-hero"><p class="doc-eyebrow">Документація · design-system/tokens.css</p>'
        f'<h1>Токени</h1><p class="doc-lead">{n_prim} primitive, {n_sem} semantic-ролей кольору і {n_mot} ролей руху. Сторінку зібрано з '
        '<code>tokens.css</code>: змінився файл — перезбери docs, і таблиці зміняться. Зразки фарбує сам файл, у світлій і темній темі.</p></header>'
        '<section class="doc-group" aria-labelledby="t-rules"><h2 id="t-rules">Два рівні</h2><div class="doc-prose">'
        '<p><strong>PRIMITIVE</strong> — сирі значення без ролей: колір, відступи, радіуси, розміри, шрифти, тіні. '
        '<strong>SEMANTIC</strong> — ролі кольору <code>--color-*</code> і ролі руху <code>--dur-*</code>, <code>--ease-*</code>, <code>--move-*</code>, кожна — <code>var()</code> на primitive. '
        'Колір і рух компонент бере тільки через роль, геометрію — з primitive напряму. Темна тема перевизначає лише ролі кольору.</p></div></section>'
        '<section class="doc-group" aria-labelledby="t-sem"><h2 id="t-sem">Semantic — ролі кольору</h2>'
        '<div class="doc-table-wrap"><table class="doc-table"><thead><tr><th>Роль</th><th>Світла</th><th>Темна</th><th>Звідки й де</th></tr></thead>'
        f'<tbody>{sem_rows}</tbody></table></div></section>'
        '<section class="doc-group" aria-labelledby="t-mot"><h2 id="t-mot">Semantic — ролі руху</h2><div class="doc-prose">'
        '<p>Анімуємо лише <code>transform</code> і <code>opacity</code>; кільце фокусу з\'являється миттєво. '
        'Під <code>prefers-reduced-motion</code> зсуви й масштаб вимикаються, статус лишається видимим. Правила — DESIGN.md «Анімація».</p></div>'
        '<div class="doc-table-wrap"><table class="doc-table"><thead><tr><th>Роль</th><th>Значення</th><th>Коли</th></tr></thead>'
        f'<tbody>{motion_rows}</tbody></table></div></section>'
        '<section class="doc-group" aria-labelledby="t-prim"><h2 id="t-prim">Primitive — сирі значення</h2>'
        '<div class="doc-table-wrap"><table class="doc-table"><thead><tr><th>Токен</th><th>Значення</th></tr></thead>'
        f'<tbody>{prim_rows}</tbody></table></div></section>'
        '<section class="doc-group" aria-labelledby="t-con"><h2 id="t-con">Контраст пар</h2><div class="doc-prose">'
        '<p>WCAG AA: текст 4.5, іконки, великий текст і межі контролів 3. Кожна нова пара — рядок у обох таблицях.</p></div>'
        f'<div class="doc-table-wrap">{contrast}</div></section>'
    )

# Екрани MVP

Тут лежать чинні екрани продукту для розробки. Назва теки — історична: на початку тут були ахроматичні вайрфрейми. Тепер екрани зібрано з [`design-system/`](../design-system/README.md): токени, компоненти, фото з `visuals/`, світла і темна тема.

- Склад екранів і станів — [`_screens.md`](_screens.md).
- Назви файлів і правила станів — [`_conventions.md`](_conventions.md), розділи 4 і 5.
- Розмітка — [`_build.py`](_build.py). HTML-файли генерує скрипт: `python3 wireframes/_build.py`. Руками їх не правлять.
- Разові блоки одного екрана — [`screens.css`](screens.css).
- Поведінка, якої не видно в статиці, — [`handoff/behavior/`](../handoff/behavior/README.md).

Перший екран — `listings.html`. Як запустити — [`handoff/README.md`](../handoff/README.md) → «Запуск локально».

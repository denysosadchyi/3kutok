/* Кнопка: точка, з якої розходиться круг наведення (components/button.css).
   Єдине джерело — цей файл; підключають екрани (wireframes/_build.py),
   документація (docs/_build.py), вітрина й оболонка (ui/kit.html, ui/shell.html).
   Пише лише локальні змінні компонента --button-hover-x / --button-hover-y
   (координати курсора всередині кнопки) на вході й на виході курсора: круг
   росте з боку, звідки навели, і стягується туди, куди курсор пішов.
   Без цього скрипта (і з клавіатури) круг росте з центру — фолбек у CSS.
   Друга робота — перекат літер на наведенні: текст кнопки розбивається на
   .button__char (data-char — для копії в ::after, --i — індекс для хвилі)
   у .button__label aria-hidden; поруч .sr-only з тим самим текстом, тож
   читач екрана чує слово, а не літери. Розбиває лише кнопки з самим текстом.
   Стилів не додає й нічого не анімує: рух дає CSS компонента. */
(function () {
  function mark(e) {
    var b = e.target;
    if (!b || !b.matches || !b.matches(".button")) return;
    var r = b.getBoundingClientRect();
    var x = Math.min(Math.max(e.clientX - r.left, 0), r.width);
    var y = Math.min(Math.max(e.clientY - r.top, 0), r.height);
    b.style.setProperty("--button-hover-x", x + "px");
    b.style.setProperty("--button-hover-y", y + "px");
  }
  function split(b) {
    if (b.children.length) return;
    var text = b.textContent.trim();
    if (!text) return;
    b.textContent = "";
    var sr = document.createElement("span");
    sr.className = "sr-only";
    sr.textContent = text;
    var label = document.createElement("span");
    label.className = "button__label";
    label.setAttribute("aria-hidden", "true");
    Array.from(text).forEach(function (ch, i) {
      var c = document.createElement("span");
      c.className = "button__char";
      c.textContent = ch;
      c.setAttribute("data-char", ch);
      c.style.setProperty("--i", i);
      label.appendChild(c);
    });
    b.appendChild(sr);
    b.appendChild(label);
  }
  function splitAll() {
    Array.prototype.forEach.call(document.querySelectorAll(".button"), split);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", splitAll);
  else splitAll();
  /* pointerenter/leave не спливають, але проходять фазу перехоплення */
  document.addEventListener("pointerenter", mark, true);
  document.addEventListener("pointerleave", mark, true);
})();

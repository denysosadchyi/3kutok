/* Поведінка сторінок документації (docs/). Підключено в <head> синхронно,
   щоб тема стояла до першого рендера. Згенеровано разом зі сторінками
   (docs/_build.py) — правити тут, а не в HTML. */

/* Шторки: закрити «Скасувати», тапом поза панеллю або Esc; посилання-заглушки нікуди не ведуть.
   Як у ui/kit.html. */
document.addEventListener("click", function (e) {
  var dismiss = e.target.closest('.sheet__panel a[href="#"]');
  if (dismiss) { e.preventDefault(); dismiss.closest("details.sheet").open = false; return; }
  if (e.target.closest('a[href="#"]')) e.preventDefault();
  var sheet = e.target.closest("details.sheet[open]");
  if (sheet && !e.target.closest(".sheet__panel, summary")) sheet.open = false;
});
document.addEventListener("keydown", function (e) {
  if (e.key !== "Escape") return;
  document.querySelectorAll("details.sheet[open]").forEach(function (d) { d.open = false; });
});

/* Анатомія: номери-мітки над живим компонентом.
   Частина позначена в розмітці data-pin="N" (і data-pin-at — кут:
   tl tr bl br t b l r c, типово tl). Мітка — окремий елемент поверх сцени,
   не всередині компонента, тож CSS компонента її не бачить. Наведення або
   фокус на рядку легенди обводить частину пунктиром. */
(function () {
  function place(live) {
    live.querySelectorAll(":scope > .doc-pin").forEach(function (p) { p.remove(); });
    var box = live.getBoundingClientRect();
    live.querySelectorAll("[data-pin]").forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (!r.width && !r.height) return;
      var at = el.getAttribute("data-pin-at") || "tl";
      var x = at.indexOf("l") > -1 ? r.left : at.indexOf("r") > -1 ? r.right : r.left + r.width / 2;
      var y = at.indexOf("t") > -1 ? r.top : at.indexOf("b") > -1 ? r.bottom : r.top + r.height / 2;
      if (at === "l" || at === "r") y = r.top + r.height / 2;
      var pin = document.createElement("span");
      pin.className = "doc-pin";
      pin.setAttribute("aria-hidden", "true");
      pin.textContent = el.getAttribute("data-pin");
      live.appendChild(pin);
      var w = pin.offsetWidth, h = pin.offsetHeight;
      var left = Math.min(Math.max(x - box.left - w / 2, 0), box.width - w);
      var top = Math.min(Math.max(y - box.top - h / 2, 0), box.height - h);
      pin.style.left = left + "px";
      pin.style.top = top + "px";
    });
  }
  function all() { document.querySelectorAll(".doc-anatomy__live").forEach(place); }
  function point(li, on) {
    var anatomy = li.closest(".doc-anatomy");
    if (!anatomy) return;
    li.classList.toggle("is-pointed", on);
    anatomy.querySelectorAll('.doc-anatomy__live [data-pin="' + li.getAttribute("data-pin") + '"]').forEach(function (el) {
      el.classList.toggle("doc-pointed", on);
    });
  }
  document.addEventListener("DOMContentLoaded", function () {
    all();
    if ("ResizeObserver" in window) {
      var ro = new ResizeObserver(all);
      document.querySelectorAll(".doc-anatomy__live").forEach(function (l) { ro.observe(l); });
    }
    document.querySelectorAll(".doc-legend > li[data-pin]").forEach(function (li) {
      li.addEventListener("mouseenter", function () { point(li, true); });
      li.addEventListener("mouseleave", function () { point(li, false); });
      li.addEventListener("focus", function () { point(li, true); });
      li.addEventListener("blur", function () { point(li, false); });
    });
  });
  window.addEventListener("load", all);
  window.addEventListener("resize", all);
  document.addEventListener("toggle", function () { requestAnimationFrame(all); }, true);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(all);
  /* Іконки iconify малюються асинхронно й можуть зсунути частини */
  setTimeout(all, 600);
  setTimeout(all, 1800);
})();

/* Повзунки підбору руху (docs/_motion.py → TUNER): ставлять ролі --dur-* / --ease-*
   у style панелі .doc-tuner — компоненти всередині читають їх як завжди, рух дає
   їхній власний CSS. Початкові значення — з tokens.css (обчислений стиль панелі). */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("[data-tuner]").forEach(function (panel) {
    var ctrls = Array.prototype.slice.call(panel.querySelectorAll("[data-token]"));
    var code = panel.querySelector(".doc-tuner__code");
    var cs = getComputedStyle(panel), defs = {};
    function ms(v) { v = v.trim(); return /ms$/.test(v) ? parseFloat(v) : parseFloat(v) * 1000; }
    ctrls.forEach(function (c) {
      var t = c.dataset.token, now = cs.getPropertyValue(t).trim();
      if (c.tagName === "SELECT") {
        Array.prototype.forEach.call(c.options, function (o) {
          var name = o.value.slice(4, -1);
          if (cs.getPropertyValue(name).trim() === now) c.value = o.value;
        });
      } else {
        c.value = ms(now);
      }
      defs[t] = c.value;
    });
    function render() {
      var lines = [];
      ctrls.forEach(function (c) {
        var t = c.dataset.token, range = c.tagName !== "SELECT";
        var out = c.parentNode.querySelector("output");
        if (range) {
          panel.style.setProperty(t, c.value + "ms");
          out.textContent = c.value + " мс" + (t === "--dur-fast" ? " · хвиля " + Math.round(c.value * 0.12) + " мс/літера" : "");
        } else {
          panel.style.setProperty(t, c.value);
          out.textContent = "";
        }
        if (c.value !== defs[t]) {
          lines.push(range
            ? t + ": var(--duration-" + c.value + ");   /* було " + defs[t] + " мс; новий primitive --duration-" + c.value + ": " + c.value + "ms */"
            : t + ": " + c.value + ";   /* було " + defs[t] + " */");
        }
      });
      code.textContent = lines.length ? lines.join("\n") : "Значення як у tokens.css — нічого не змінено.";
    }
    panel.addEventListener("input", render);
    panel.querySelector("[data-tuner-reset]").addEventListener("click", function () {
      ctrls.forEach(function (c) { c.value = defs[c.dataset.token]; });
      render();
    });
    render();
  });
});

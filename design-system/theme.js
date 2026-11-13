/* Перемикач теми — поведінка системи (backlog B9, 2026-11-13).
   Темна тема (tokens.css, [data-theme="dark"]) — частина продукту з 2026-10-23.
   Підключати в <head> поруч з index.css, без defer, щоб тема стала до
   першого кадру: <script src="design-system/theme.js"></script>.

   Що робить:
   - ставить data-theme="dark" на <html> за збереженим вибором (ключ
     kutok-theme спільний для екранів, вітрини, документації й хабу уроків);
   - перемикає тему по кліку на .theme-toggle і синхронізує aria-pressed та
     іконку (місяць / сонце);
   - підхоплює вибір з інших вкладок (подія storage);
   - у вбудованій сторінці (iframe, напр. мокап хабу уроків) ставить клас
     .in-frame: тему там перемикає батьківська сторінка, кнопку ховає
     topbar.css. */
(function () {
  var KEY = "kutok-theme", root = document.documentElement;
  if (window.self !== window.top) root.classList.add("in-frame");
  function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function apply(dark) {
    if (dark) root.setAttribute("data-theme", "dark"); else root.removeAttribute("data-theme");
    document.querySelectorAll(".theme-toggle").forEach(function (b) {
      b.setAttribute("aria-pressed", dark ? "true" : "false");
      var i = b.querySelector("iconify-icon");
      if (i) i.setAttribute("icon", dark ? "solar:sun-2-linear" : "solar:moon-linear");
    });
  }
  apply(saved() === "dark");
  document.addEventListener("DOMContentLoaded", function () { apply(saved() === "dark"); });
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".theme-toggle");
    if (!b) return;
    var dark = root.getAttribute("data-theme") !== "dark";
    apply(dark);
    try { localStorage.setItem(KEY, dark ? "dark" : "light"); } catch (err) {}
  });
  window.addEventListener("storage", function (e) { if (e.key === KEY) apply(e.newValue === "dark"); });
})();

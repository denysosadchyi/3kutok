/* Тема для сторінок курсу. Ключ kutok-theme той самий, що в
   design-system/theme.js (екрани, вітрина, документація). Тому вибір теми
   переходить між хабом, екранами, вітриною й документацією.
   Скрипт ставить кнопку-місяць у правий нижній кут. У вбудованій сторінці
   (iframe у хабі) кнопки немає: тему задає батьківська сторінка через ключ. */
(function () {
  var KEY = "kutok-theme", root = document.documentElement;
  var MOON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20.5 14.2A8.5 8.5 0 0 1 9.8 3.5a8.5 8.5 0 1 0 10.7 10.7Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  var SUN = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6 6 6M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>';
  function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function apply(dark) {
    if (dark) root.setAttribute("data-theme", "dark"); else root.removeAttribute("data-theme");
    document.querySelectorAll(".hub-theme").forEach(function (b) {
      b.setAttribute("aria-pressed", dark ? "true" : "false");
      b.innerHTML = dark ? SUN : MOON;
    });
  }
  apply(saved() === "dark");
  document.addEventListener("DOMContentLoaded", function () {
    if (window.self === window.top && !document.querySelector(".hub-theme")) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "hub-theme";
      b.setAttribute("aria-label", "Темна тема");
      b.title = "Темна тема";
      document.body.appendChild(b);
    }
    apply(saved() === "dark");
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".hub-theme")) return;
    var dark = root.getAttribute("data-theme") !== "dark";
    apply(dark);
    try { localStorage.setItem(KEY, dark ? "dark" : "light"); } catch (err) {}
  });
  window.addEventListener("storage", function (e) { if (e.key === KEY) apply(e.newValue === "dark"); });
})();

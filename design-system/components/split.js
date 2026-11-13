/* Спліт: перешикування карток між сторінками — лише transform (components/split.css,
   DESIGN.md «Анімація» → «Спліт — перехід між сторінками», 2026-11-06).
   Браузерний View Transition за замовчуванням анімує групу знімка картки через
   width і height (плюс transform). Тут ця анімація підміняється на transform:
   група одразу має кінцевий розмір, а старий розмір дає scale від лівого
   верхнього кута (transform-origin у split.css). Знімки всередині групи
   займають її ширину з висотою «auto», тож рівномірний scale(стара / нова
   ширина) дає той самий кадр, що й браузерний, — без перерахунку розміру.
   Клас split-vt на <html> вмикає імена карток (split.css): без цього скрипта
   картки не мають імен, сторінка міняється одразу, і width/height не анімується
   ніде. Підключається синхронно в <head> (wireframes/_build.py): pagereveal
   приходить до першого кадру нової сторінки. Стилів не додає. */
(function () {
  if (!("onpagereveal" in window)) return;
  document.documentElement.classList.add("split-vt");
  var GROUP = "::view-transition-group(split-card-";

  function cardWidth(name) {
    var cards = document.querySelectorAll("body.shell > .split .card-list > *");
    for (var i = 0; i < cards.length; i++) {
      if (getComputedStyle(cards[i]).viewTransitionName === name) return cards[i].getBoundingClientRect().width;
    }
    return 0;
  }

  window.addEventListener("pagereveal", function (e) {
    var vt = e.viewTransition;
    if (!vt) return;
    vt.ready.then(function () {
      document.getAnimations().forEach(function (a) {
        var fx = a.effect, pe = fx && fx.pseudoElement;
        if (!pe || pe.indexOf(GROUP) !== 0) return;
        var from = fx.getKeyframes()[0];
        var oldW = from && parseFloat(from.width);
        var newW = cardWidth(pe.slice(GROUP.length - "split-card-".length, -1));
        if (!oldW || !newW) return;
        var t = from.transform && from.transform !== "none" ? from.transform + " " : "";
        /* лише transform: кінець — власний transform групи (неявний кадр 100%) */
        fx.setKeyframes([{ offset: 0, transform: t + "scale(" + oldW / newW + ")" }]);
      });
    });
  });
})();

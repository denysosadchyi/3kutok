// Course rail tree: chevrons expand a lesson's in-page navigation.
// The lesson marked aria-current="page" opens by default.
(function () {
  var tree = document.querySelector(".course-tree");
  if (!tree) return;

  function setOpen(button, open) {
    var sub = document.getElementById(button.getAttribute("aria-controls"));
    if (!sub) return;
    button.setAttribute("aria-expanded", String(open));
    sub.hidden = !open;
  }

  tree.querySelectorAll(".ct-twisty").forEach(function (button) {
    button.addEventListener("click", function () {
      setOpen(button, button.getAttribute("aria-expanded") !== "true");
    });
  });

  var current = tree.querySelector('.ct-link[aria-current="page"]');
  var currentButton = current && current.parentElement.querySelector(".ct-twisty");
  if (currentButton) setOpen(currentButton, true);
})();

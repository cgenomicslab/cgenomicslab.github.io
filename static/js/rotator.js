// Rotates through the .rot-item children of every [data-rotate] element (homepage Research).
// Dots (.rot-dot) select an item; hovering pauses; data-hover-select makes hovering an item select it.
(function(){
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-rotate]').forEach(function(root){
    if (root.dataset.rotInit) return;
    root.dataset.rotInit = '1';
    var items = root.querySelectorAll('.rot-item');
    var dots = root.querySelectorAll('.rot-dot');
    var n = items.length, idx = 0, timer = null;
    var ms = parseInt(root.getAttribute('data-interval'), 10) || 4000;
    function show(i){
      idx = (i + n) % n;
      items.forEach(function(el, k){ el.classList.toggle('active', k === idx); });
      dots.forEach(function(d, k){ d.classList.toggle('active', k === idx); d.setAttribute('aria-current', k === idx ? 'true' : 'false'); });
    }
    function stop(){ if (timer) clearInterval(timer); timer = null; }
    function start(){ stop(); if (!still && n > 1) timer = setInterval(function(){ show(idx + 1); }, ms); }
    dots.forEach(function(d, k){ d.addEventListener('click', function(){ show(k); start(); }); });
    if (root.hasAttribute('data-hover-select')) {
      items.forEach(function(el, k){ el.addEventListener('mouseenter', function(){ show(k); }); });
    }
    root.addEventListener('mouseenter', stop);
    root.addEventListener('mouseleave', start);
    show(0);
    start();
  });
})();

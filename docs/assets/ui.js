/* Collapsible navigation panel. The sidebar slides shut and the reading column
   takes the full width, the way a side panel tucks away. The choice is
   remembered per browser, and everything still works if storage is unavailable. */
(function () {
  var shell = document.querySelector('.shell');
  var content = document.querySelector('.content');
  if (!shell || !content) return;

  var KEY = 'nav-collapsed';

  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'nav-toggle';
  btn.innerHTML =
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">' +
    '<rect x="1.5" y="2.5" width="13" height="11" rx="2" fill="none" stroke="currentColor" stroke-width="1.4"/>' +
    '<line x1="6.5" y1="2.5" x2="6.5" y2="13.5" stroke="currentColor" stroke-width="1.4"/>' +
    '</svg>';
  content.insertBefore(btn, content.firstChild);

  function apply(collapsed) {
    shell.classList.toggle('nav-collapsed', collapsed);
    btn.setAttribute('aria-expanded', String(!collapsed));
    btn.setAttribute('aria-label', collapsed ? 'Show navigation' : 'Hide navigation');
    btn.title = collapsed ? 'Show navigation' : 'Hide navigation';
  }

  var start = false;
  try { start = window.localStorage.getItem(KEY) === '1'; } catch (e) {}
  apply(start);

  btn.addEventListener('click', function () {
    var next = !shell.classList.contains('nav-collapsed');
    apply(next);
    try { window.localStorage.setItem(KEY, next ? '1' : '0'); } catch (e) {}
  });
})();

/* Collapsible code excerpts. Each codeblock starts closed; the toggle button
   opens it, the round close button (or Escape) shuts it again. */
(function () {
  document.querySelectorAll('.codeblock').forEach(function (block) {
    var openBtn = block.querySelector('.code-toggle');
    var closeBtn = block.querySelector('.code-close');
    if (!openBtn || !closeBtn) return;

    function open() {
      block.classList.add('is-open');
      openBtn.setAttribute('aria-expanded', 'true');
      closeBtn.focus();
    }
    function close() {
      block.classList.remove('is-open');
      openBtn.setAttribute('aria-expanded', 'false');
      openBtn.focus();
    }

    openBtn.addEventListener('click', open);
    closeBtn.addEventListener('click', close);
    block.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && block.classList.contains('is-open')) close();
    });
  });
})();

/* Fade between pages. Each page starts hidden (see body{opacity:0} in
   style.css) and fades in on load; a click on an internal nav link fades
   the page out first, then navigates, so moving between sections doesn't
   hard-cut. Skipped entirely under prefers-reduced-motion. */
(function () {
  var reduceMotion = false;
  try { reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  function reveal() { document.body.classList.add('is-visible'); }

  if (reduceMotion) {
    reveal();
  } else {
    requestAnimationFrame(function () { requestAnimationFrame(reveal); });
    // bfcache back/forward restores can skip re-running scripts' effects
    window.addEventListener('pageshow', reveal);
  }

  if (!reduceMotion) {
    document.querySelectorAll('.sidebar nav a').forEach(function (link) {
      link.addEventListener('click', function (e) {
        if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey ||
            e.shiftKey || e.altKey || link.target === '_blank') return;
        var href = link.getAttribute('href');
        if (!href || href.charAt(0) === '#') return;
        e.preventDefault();
        document.body.classList.remove('is-visible');
        setTimeout(function () { window.location.href = href; }, 190);
      });
    });
  }
})();

/* Section headings fade and rise into view as they scroll into the reading
   column, an understated version of the scroll-reveal treatment often used
   for editorial pages, scaled down for content people are here to read
   rather than watch move. Skipped under prefers-reduced-motion and when
   IntersectionObserver isn't available; either way headings just render
   normally. */
(function () {
  var reduceMotion = false;
  try { reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}
  if (reduceMotion || !('IntersectionObserver' in window)) return;

  var headings = document.querySelectorAll('.content h2');
  if (!headings.length) return;

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-revealed');
      observer.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });

  headings.forEach(function (h) {
    h.classList.add('reveal-init');
    observer.observe(h);
  });
})();

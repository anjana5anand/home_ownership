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

"""Single-file clickable preview, generated from the same pages that deploy.
Not a deliverable - a way to judge layout before the writing goes in."""
import base64, importlib.util, re, sys

sys.argv = ["_build_pages.py"]
spec = importlib.util.spec_from_file_location("bp", "_build_pages.py")
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)   # module-level only: build_all() is not called

css = open("assets/style.css").read()
import os
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml"}
IMAGES = {}
for fn in sorted(os.listdir("images")):
    ext = os.path.splitext(fn)[1].lower()
    if ext in MIME:
        IMAGES["images/" + fn] = "data:%s;base64,%s" % (
            MIME[ext], base64.b64encode(open("images/" + fn, "rb").read()).decode())
print("  inlined %d real images" % len(IMAGES))


def body_for(href):
    html = open(href).read()
    return re.search(r'<main class="content">(.*?)</main>', html, re.S).group(1)


def placehold(body):
    # a thumbnail whose file exists is inlined; one that does not becomes a hatched slot
    def thumb(m):
        src = m.group(1)
        if src in IMAGES:
            return m.group(0).replace('src="%s"' % src, 'src="%s"' % IMAGES[src])
        return '<div class="imgph">%s</div>' % src

    body = re.sub(r'<a href="images/[^"]*"><img src="(images/[^"]*)"[^>]*></a>', thumb, body)
    body = re.sub(r'<img src="(images/PLACEHOLDER[^"]*)"[^>]*>',
                  r'<div class="imgph">\1</div>', body)
    for path, uri in IMAGES.items():
        body = body.replace('src="%s"' % path, 'src="%s"' % uri)
    return body


sections, navlinks = [], []
for i, (href, label, _sub, group) in enumerate(bp.PAGES):
    pid = href.replace(".html", "")
    if group:
        navlinks.append('<p class="group">%s</p>' % group)
    navlinks.append('<a href="#" class="tab%s" data-target="%s">%s</a>'
                    % (" active" if i == 0 else "", pid, label))
    sections.append('<section id="%s" class="pane"%s>\n%s\n</section>'
                    % (pid, "" if i == 0 else " hidden", placehold(body_for(href))))

out = """<title>Housing Out of Reach</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400&family=Public+Sans:wght@400;500;650&display=swap">
<style>
%s

.imgph {
  border: 1px dashed var(--rule);
  border-radius: 8px;
  background: repeating-linear-gradient(45deg,#f5f6f4,#f5f6f4 10px,#eef0ec 10px,#eef0ec 20px);
  color: var(--muted);
  font: 11px/1.45 var(--mono);
  display: flex; align-items: center; justify-content: center;
  text-align: center; padding: 12px; word-break: break-all;
  aspect-ratio: 4/3;
}
.preview-note {
  background: var(--todo-bg); border-bottom: 1px solid var(--todo-rule);
  color: var(--todo-ink); padding: 9px 16px; font-size: 12.5px; text-align: center;
}
.sidebar nav a { cursor: pointer; }
</style>

<div class="preview-note">Layout preview &mdash; hatched boxes are figure slots, amber boxes are writing still to do.</div>
<div class="shell">
  <aside class="sidebar">
    <p class="site-title">%s</p>
    <p class="site-sub">%s</p>
    <p class="nav-label">Contents</p>
    <nav id="nav">
      %s
    </nav>
  </aside>
  <main class="content" id="main">
    %s
  </main>
</div>

<script>
/* collapsible nav panel, same behaviour as assets/ui.js on the real site */
(function () {
  var shell = document.querySelector('.shell');
  var content = document.querySelector('.content');
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'nav-toggle';
  btn.innerHTML = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">' +
    '<rect x="1.5" y="2.5" width="13" height="11" rx="2" fill="none" stroke="currentColor" stroke-width="1.4"/>' +
    '<line x1="6.5" y1="2.5" x2="6.5" y2="13.5" stroke="currentColor" stroke-width="1.4"/></svg>';
  content.insertBefore(btn, content.firstChild);
  function apply(c) {
    shell.classList.toggle('nav-collapsed', c);
    btn.setAttribute('aria-expanded', String(!c));
    btn.setAttribute('aria-label', c ? 'Show navigation' : 'Hide navigation');
    btn.title = c ? 'Show navigation' : 'Hide navigation';
  }
  var start = false;
  try { start = window.localStorage.getItem('nav-collapsed') === '1'; } catch (e) {}
  apply(start);
  btn.addEventListener('click', function () {
    var next = !shell.classList.contains('nav-collapsed');
    apply(next);
    try { window.localStorage.setItem('nav-collapsed', next ? '1' : '0'); } catch (e) {}
  });
})();

document.getElementById('nav').addEventListener('click', function (e) {
  var a = e.target.closest('a.tab');
  if (!a) return;
  e.preventDefault();
  document.querySelectorAll('#nav a.tab').forEach(function (n) { n.classList.remove('active'); });
  a.classList.add('active');
  document.querySelectorAll('.pane').forEach(function (p) { p.hidden = true; });
  document.getElementById(a.dataset.target).hidden = false;
  window.scrollTo(0, 0);
});
</script>
""" % (css, bp.SITE_TITLE, bp.SITE_SUB, "\n      ".join(navlinks), "\n".join(sections))

open("_layout_preview.html", "w").write(out)
print("wrote _layout_preview.html (%,d bytes, %d panes)".replace("%,d", "{:,}").format(len(out)) % len(sections)
      if False else "wrote _layout_preview.html ({:,} bytes, {} panes)".format(len(out), len(sections)))

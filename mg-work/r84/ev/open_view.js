(function () {
  var html = document.documentElement;
  if (html.getAttribute('data-av-chat-open') === null) {
    html.setAttribute('data-av-chat-open', '');
  }
  var drawer = document.getElementById('av-chat-drawer');
  if (!drawer) return JSON.stringify({ ok: false, why: 'no drawer' });
  var entry = drawer.querySelector('.td-right-acts [aria-label="会话历史"]');
  if (!entry) return JSON.stringify({ ok: false, why: 'no entry' });
  if (!drawer.hasAttribute('data-av-hs')) entry.click();
  var view = document.querySelector('.av-hs');
  if (!view) return JSON.stringify({ ok: false, why: 'no view' });
  document.querySelectorAll('.av-hs-item.is-on').forEach(function (el) { el.classList.remove('is-on'); });
  var first = document.querySelector('.av-hs-item');
  if (first) first.classList.add('is-on');
  return JSON.stringify({
    ok: true,
    open: html.getAttribute('data-av-chat-open'),
    hs: drawer.getAttribute('data-av-hs'),
    display: getComputedStyle(view).display,
    rect: (function (r) { return [r.x, r.y, r.width, r.height]; })(view.getBoundingClientRect())
  });
})();

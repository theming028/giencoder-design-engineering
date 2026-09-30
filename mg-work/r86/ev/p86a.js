JSON.stringify((function () {
  function box(el) { var b = el.getBoundingClientRect(); return [+b.x.toFixed(1), +b.y.toFixed(1), +b.width.toFixed(1), +b.height.toFixed(1)]; }
  var r = {};
  r.url = location.href;
  r.hash = location.hash;

  /* ---- aside 与拖拽条 ---- */
  var aside = document.querySelector('aside');
  if (aside) {
    r.aside = { box: box(aside), inlineW: aside.style.width, ariaHidden: aside.getAttribute('aria-hidden') };
    var scroller = aside.querySelector(':scope > div[class*="overflow-y-auto"]');
    r.aside.scrollerW = scroller ? +scroller.getBoundingClientRect().width.toFixed(1) : null;
  }
  var sep = document.querySelector('[role="separator"][aria-label="调整菜单宽度"]');
  r.sep = sep ? { box: box(sep), cls: sep.className, holder: (sep.parentElement && sep.parentElement.className || '').toString().slice(0, 80) } : null;

  /* ---- 现有 select（r85 手搓版） ---- */
  var sels = [].slice.call(document.querySelectorAll('.r85-sel'));
  r.sels = sels.map(function (s) {
    var cs = getComputedStyle(s);
    return { box: box(s), w: cs.width, h: cs.height, bd: cs.borderTopWidth + ' ' + cs.borderTopColor, r: cs.borderTopLeftRadius, bg: cs.backgroundColor, fs: cs.fontSize };
  });
  r.selCount = sels.length;

  /* ---- 卡片内分割线（.r85-row + .r85-row::before） ---- */
  var rows = [].slice.call(document.querySelectorAll('.r85-card .r85-row'));
  var lines = [];
  for (var i = 0; i < Math.min(rows.length, 12); i++) {
    var pb = getComputedStyle(rows[i], '::before');
    if (pb.content !== 'none' && pb.height !== 'auto' && pb.backgroundColor !== 'rgba(0, 0, 0, 0)') {
      lines.push({ i: i, bg: pb.backgroundColor, h: pb.height, content: pb.content });
    }
  }
  r.lines = lines;

  /* ---- 行图标底 ---- */
  var ic = document.querySelector('.r85-ic');
  if (ic) {
    var ics = getComputedStyle(ic);
    r.ic = { box: box(ic), bg: ics.backgroundColor, r: ics.borderTopLeftRadius };
  }

  /* ---- 页面主体几何（复核 r85 成果未变） ---- */
  var page = document.querySelector('.r85-page');
  var nav = document.querySelector('.r85-nav-host');
  r.page = page ? box(page) : null;
  r.nav = nav ? box(nav) : null;
  r.cards = [].slice.call(document.querySelectorAll('.r85-card')).map(box);
  return r;
})())

(function () {
  function box(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    var cs = getComputedStyle(el);
    return {
      x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1),
      pad: cs.paddingTop + ' ' + cs.paddingRight + ' ' + cs.paddingBottom + ' ' + cs.paddingLeft,
      cls: (el.className && el.className.toString ? el.className.toString() : '').slice(0, 90)
    };
  }
  var out = {};
  var aside = document.querySelector('aside');
  out.aside = box(aside);
  if (!aside) return JSON.stringify(out);
  out.asideStyleAttr = (aside.getAttribute('style') || '').slice(0, 160);
  var A = out.aside;

  function rel(b) { if (!b) return b; b.relL = +(b.x - A.x).toFixed(1); b.relR = +((A.x + A.w) - (b.x + b.w)).toFixed(1); return b; }

  out.asideChildren = [].slice.call(aside.children).map(function (c) {
    var b = rel(box(c)); b.tag = c.tagName.toLowerCase(); return b;
  });

  var host = document.querySelector('.r85-nav-host');
  out.navHost = rel(box(host));
  if (host) {
    out.navHostParent = rel(box(host.parentElement));
    out.navHostParentTag = host.parentElement.tagName.toLowerCase();
    out.navHostParentCls = (host.parentElement.className && host.parentElement.className.toString ? host.parentElement.className.toString() : '').slice(0, 120);
    out.r85nav = rel(box(document.querySelector('.r85-nav')));
    out.r85navi = rel(box(document.querySelector('.r85-navi')));
  }

  var items = [].slice.call(aside.querySelectorAll('button,[role="button"],a')).slice(0, 10);
  out.items = items.map(function (el) {
    var b = rel(box(el));
    b.text = (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 22);
    return b;
  });
  return JSON.stringify(out);
})()

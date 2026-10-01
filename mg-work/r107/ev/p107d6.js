(function () {
  var pane = document.querySelector('.td-browse');
  var bar = pane.querySelector('.td-browse-bar');
  var slot = document.getElementById('av-browse-slot');
  var menu = pane.querySelector('.td-mod-menu');
  function rr(e) {
    if (!e) return null;
    var r = e.getBoundingClientRect();
    var cs = getComputedStyle(e);
    return { t: e.tagName + '.' + String(e.className).split(' ')[0], x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), pos: cs.position, ov: cs.overflow };
  }
  return JSON.stringify({
    scrollY: window.scrollY,
    docTop: document.documentElement.scrollTop,
    bodyTop: document.body.scrollTop,
    htmlScrollH: document.documentElement.scrollHeight,
    winH: window.innerHeight,
    slot: rr(slot),
    pane: rr(pane),
    bar: rr(bar),
    menu: rr(menu),
    menuAriaHidden: menu.hasAttribute('hidden'),
    offsetParent: menu.offsetParent ? menu.offsetParent.tagName + '.' + String(menu.offsetParent.className).split(' ')[0] : null,
    menus: [].map.call(pane.querySelectorAll('.td-mod-menu, .td-rv-menu, .td-ctxmenu'), function (m) {
      var r = m.getBoundingClientRect();
      return { cls: String(m.className).split(' ').slice(0, 2).join('.'), x: Math.round(r.x), y: Math.round(r.y), h: Math.round(r.height) };
    })
  });
})()

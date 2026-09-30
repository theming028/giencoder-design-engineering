(function () {
  function r(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function info(el) {
    if (!el) return null;
    var cs = getComputedStyle(el);
    return { tag: el.tagName, cls: (el.className || '').toString().slice(0, 70), rect: r(el), disp: cs.display, pos: cs.position, zi: cs.zIndex, w: cs.width };
  }
  var row = document.querySelector('div:has(> main)');
  var main = document.querySelector('main');
  var out = { url: location.href.split('/').pop(), win: [innerWidth, innerHeight] };
  out.row = info(row);
  out.rowChildren = row ? [].map.call(row.children, function (c) { return info(c); }) : null;
  out.main = info(main);
  out.mainChildren = main ? [].map.call(main.children, function (c) { return info(c); }) : null;
  out.aside = info(document.querySelector('aside'));
  out.host = info(document.querySelector('.r93-conv-host'));
  out.baracts = document.querySelectorAll('.r93-baract').length;
  out.morebtn = document.querySelectorAll('.r93-morebtn').length;
  out.seg = info(document.querySelector('.r93-seg'));
  out.slider = info(document.querySelector('.r93-seg .giencoder-radio-button-slider'));
  out.slotExists = !!document.getElementById('av-browse-slot');
  return JSON.stringify(out);
})()

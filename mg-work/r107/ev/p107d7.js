(function () {
  var pane = document.querySelector('.td-browse');
  var m = pane.querySelector('.td-mod-menu');
  function snap(tag) {
    var cs = getComputedStyle(m);
    var r = m.getBoundingClientRect();
    return {
      tag: tag, hidden: m.hasAttribute('hidden'), display: cs.display,
      vis: cs.visibility, op: cs.opacity, top: cs.top, bottom: cs.bottom,
      translate: cs.translate, scale: cs.scale, origin: cs.transformOrigin,
      rect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]
    };
  }
  var out = [snap('closed')];
  pane.querySelector('[data-td-add]').click();
  out.push(snap('open-now'));
  return JSON.stringify({ out: out, anims: m.getAnimations().length });
})()

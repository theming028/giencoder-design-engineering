(function () {
  var sc = document.querySelector('.r93-scroll');
  if (!sc) return JSON.stringify({ err: 'no scroll' });
  var wrap = sc.querySelector('.r93-wrap');
  var pane = wrap && wrap.querySelector('.r93-pane');
  if (!pane) return JSON.stringify({ err: 'no pane' });
  var out = { scrollH: sc.scrollHeight, clientH: sc.clientHeight, n: pane.children.length, items: [] };
  var wr = wrap.getBoundingClientRect();
  for (var i = 0; i < pane.children.length; i++) {
    var el = pane.children[i];
    var r = el.getBoundingClientRect();
    var o = {
      i: i,
      cls: (el.className || '').replace('r93-it ', '').replace('r93-', ''),
      top: Math.round(r.top - wr.top),
      h: Math.round(r.height)
    };
    var head = el.querySelector('.r93-fh');
    if (head) o.headH = Math.round(head.getBoundingClientRect().height);
    var card = el.querySelector('.r93-card, .r93-diff, .r93-arts, .r93-note, .r93-alert, .r93-bub, .r93-asst');
    if (card) {
      var cr = card.getBoundingClientRect();
      o.cardH = Math.round(cr.height);
      o.cardW = Math.round(cr.width);
      o.cardTop = Math.round(cr.top - r.top);
      o.cardCls = (card.className || '').replace('r93-', '');
    }
    var t = el.querySelector('.r93-fh .r93-t14, .r93-nrow .r93-nt, .r93-ahd2 .r93-t14');
    if (t) o.t = (t.textContent || '').trim().slice(0, 16);
    out.items.push(o);
  }
  return JSON.stringify(out);
})();

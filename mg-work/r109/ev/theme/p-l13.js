(function () {
  var out = { ok: 1 };
  function cs(el) { return el ? getComputedStyle(el) : null; }
  function r(el) {
    if (!el) return null;
    var b = el.getBoundingClientRect();
    return { x: Math.round(b.x), w: Math.round(b.width) };
  }

  /* ① .r93-card 缩进：左缘是否与父容器左缘对齐（margin-left 归零 → rect.x 相等） */
  var cards = document.querySelectorAll('.r93-card');
  out.cardCount = cards.length;
  out.cards = [];
  for (var i = 0; i < cards.length; i++) {
    var c = cards[i];
    var s = cs(c);
    var par = c.parentElement;
    var pb = par ? par.getBoundingClientRect() : null;
    var cb = c.getBoundingClientRect();
    out.cards.push({
      cls: c.className,
      cssW: s.width, ml: s.marginLeft,
      relX: pb ? Math.round(cb.left - pb.left) : null
    });
  }
  var edge = document.querySelector('.r93-card--edge');
  if (edge) {
    var es = cs(edge), eb = edge.getBoundingClientRect();
    var ep = edge.parentElement.getBoundingClientRect();
    out.edge = { cssW: es.width, ml: es.marginLeft, relX: Math.round(eb.left - ep.left), w: Math.round(eb.width) };
  }

  /* ② .zd-host 显隐：当前 display + 开关命中 */
  var host = document.querySelector('.zd-host');
  if (host) {
    out.host = {
      display: cs(host).display,
      skInDom: !!document.querySelector('.r93-sk'),
      appAttr: document.documentElement.getAttribute('data-r93-app'),
      rect: r(host)
    };
  }

  /* 主体（对话内容 div.mt-8）当前 opacity，作为「就绪」的旁证 */
  var main = document.querySelector("html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > div.mt-8");
  if (main) out.hero = { opacity: cs(main).opacity };
  out.now = Date.now();
  return JSON.stringify(out);
})()

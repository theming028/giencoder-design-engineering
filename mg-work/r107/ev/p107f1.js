(function () {
  var out = {};
  function cs(el, props) {
    var c = getComputedStyle(el), o = {};
    props.forEach(function (p) { o[p] = c[p]; });
    return o;
  }
  // 1) composer 卡本体
  var card = document.querySelector('div.relative.flex.w-full.flex-col.rounded-\\[16px\\].border.bg-white.p-3');
  if (!card) {
    // 退路：按类 token 找
    var all = document.querySelectorAll('main div');
    for (var i = 0; i < all.length; i++) {
      var cl = all[i].className || '';
      if (typeof cl === 'string' && cl.indexOf('rounded-[16px]') >= 0 && cl.indexOf('bg-white') >= 0) { card = all[i]; break; }
    }
  }
  out.cardFound = !!card;
  if (card) {
    out.cardCls = (card.className || '').slice(0, 160);
    var foot = card.lastElementChild;
    out.footCls = (foot.className || '').slice(0, 120);
    out.footCs = cs(foot, ['userSelect', 'webkitUserSelect', 'pointerEvents', 'display', 'alignItems', 'justifyContent', 'height']);
    // footer 内所有元素（含文本节点父）
    var list = [];
    foot.querySelectorAll('*').forEach(function (e) {
      var r = e.getBoundingClientRect();
      var c = getComputedStyle(e);
      list.push({
        tag: e.tagName,
        cls: (typeof e.className === 'string' ? e.className : '').slice(0, 70),
        txt: (e.textContent || '').trim().slice(0, 40),
        wh: Math.round(r.width) + 'x' + Math.round(r.height),
        us: c.userSelect,
        pe: c.pointerEvents,
        pos: c.position,
        z: c.zIndex
      });
    });
    out.footKids = list;
  }
  // 2) 祖先链上的 user-select / pointer-events / z-index
  var chain = [];
  var n = card;
  while (n && n !== document.documentElement) {
    var c2 = getComputedStyle(n);
    chain.push({
      tag: n.tagName, cls: (typeof n.className === 'string' ? n.className : '').slice(0, 60),
      us: c2.userSelect, pe: c2.pointerEvents, z: c2.zIndex, pos: c2.position,
      w: Math.round(n.getBoundingClientRect().width)
    });
    n = n.parentElement;
  }
  out.chain = chain;
  return JSON.stringify(out);
})()

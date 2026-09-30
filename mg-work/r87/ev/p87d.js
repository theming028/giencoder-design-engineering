(function () {
  var out = {};
  var de = document.documentElement;
  var pg = location.pathname.split('/').pop();

  out.page = pg;
  out.uiFs = getComputedStyle(de).getPropertyValue('--ui-fs').trim();
  out.ratio = getComputedStyle(de).getPropertyValue('--ui-fs-ratio').trim();
  out.overflowX = de.scrollWidth - de.clientWidth;
  out.selCount = document.querySelectorAll('.giencoder-select').length;
  out.btnCount = document.querySelectorAll('.giencoder-btn').length;

  out.selects = [].slice.call(document.querySelectorAll('.giencoder-select')).slice(0, 24).map(function (s) {
    var v = s.querySelector('.giencoder-select-view');
    var b = s.getBoundingClientRect();
    var tx = s.querySelector('.giencoder-select-view-text');
    return {
      cls: (s.className || '').toString().replace('giencoder-select', 'sel').trim(),
      wh: [+b.width.toFixed(1), +b.height.toFixed(1)],
      radius: v ? getComputedStyle(v).borderTopLeftRadius : null,
      shadow: v ? getComputedStyle(v).boxShadow : null,
      ring: v ? (getComputedStyle(v).getPropertyValue('--select-ring') || '(未定义)').trim() : null,
      inlineW: s.style.width || '(无)',
      txt: tx ? tx.textContent.trim().slice(0, 14) : null,
      truncated: tx ? tx.scrollWidth > tx.clientWidth : null
    };
  });

  /* 是否存在任何元素仍带 --select-ring 局部变量 */
  var ringHolders = [];
  var all = document.querySelectorAll('.giencoder-select-view, .giencoder-select');
  for (var i = 0; i < all.length; i++) {
    var rv = (all[i].style.getPropertyValue('--select-ring') || '').trim();
    if (rv) ringHolders.push(all[i].className + ' => ' + rv);
  }
  out.ringInlineHolders = ringHolders;

  /* 整页裁切扫描（只报前 12 条，用于回归） */
  var bad = [];
  var els = document.querySelectorAll('*');
  for (var j = 0; j < els.length; j++) {
    var el = els[j];
    if (el.closest && el.closest('.giencoder-select-popup')) continue;
    if (el.tagName === 'HTML' || el.tagName === 'BODY') continue;
    var c = getComputedStyle(el);
    if (c.display === 'none' || c.visibility === 'hidden') continue;
    var bb = el.getBoundingClientRect();
    if (bb.width < 1 || bb.height < 1) continue;
    var ox = el.scrollWidth - el.clientWidth, oy = el.scrollHeight - el.clientHeight;
    if ((c.overflowX !== 'visible' && ox > 1) || (c.overflowY !== 'visible' && oy > 1)) {
      bad.push((el.className || el.tagName).toString().split(/\s+/).slice(0, 2).join('.') + ' ox=' + ox + ' oy=' + oy);
      if (bad.length >= 12) break;
    }
  }
  out.clipped = bad;

  return JSON.stringify(out, null, 1);
})()

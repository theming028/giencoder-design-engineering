(function () {
  var out = {};

  /* ============ 判据：只认「自身直接文本节点」被裁的元素 ============
     scrollWidth > clientWidth 分两种：
       (a) 元素自己有直接文本子节点，文本超出了盒宽  ← 这才是「文字容器」
       (b) 元素自己没有直接文本，是后代把它撑宽的     ← 容器，不该加 nowrap
     判据用 childNodes 里的 TEXT_NODE 区分。 */
  function directText(el) {
    var s = '';
    for (var i = 0; i < el.childNodes.length; i++) {
      var n = el.childNodes[i];
      if (n.nodeType === 3) s += n.nodeValue;
    }
    return s.replace(/\s+/g, ' ').trim();
  }
  function survey(rootSel, tag) {
    var root = document.querySelector(rootSel);
    if (!root) return tag + ':ABSENT';
    var groups = {}, n = 0;
    root.querySelectorAll('*').forEach(function (e) {
      var c = getComputedStyle(e);
      if (c.display === 'none' || c.visibility === 'hidden' || e.hasAttribute('hidden')) return;
      if (c.overflowX === 'auto' || c.overflowX === 'scroll') return;
      var txt = directText(e);
      if (!txt) return;                                     // ★ 无直接文本 ⇒ 是被后代撑出的容器
      var cw = e.clientWidth, sw = e.scrollWidth;
      if (cw <= 0 || sw <= cw + 1) return;
      var cls = String(e.className || '').trim().split(/\s+/).filter(Boolean).slice(0, 2).join('.');
      var k = e.tagName + (cls ? '.' + cls : '');
      if (!groups[k]) groups[k] = { n: 0, max: 0, te: c.textOverflow, ws: c.whiteSpace, ox: c.overflowX, mw: c.minWidth, sample: '' };
      groups[k].n++;
      groups[k].max = Math.max(groups[k].max, sw - cw);
      if (!groups[k].sample) groups[k].sample = txt.slice(0, 26);
      n++;
    });
    out['ov_' + tag] = { total: n, groups: groups, rootW: Math.round(root.getBoundingClientRect().width) };
    return null;
  }

  /* ---- 1) 1440 默认宽：全页 ---- */
  survey('body', 'page1440');

  /* ---- 2) 右栏压到 240px：暴露「宽度不够」的候选 ---- */
  var slot = document.getElementById('av-browse-slot');
  if (slot) {
    slot.style.flex = '0 0 240px'; slot.style.width = '240px'; slot.style.maxWidth = '240px';
    out.slotForced = 'ok';
  } else { out.slotForced = 'NO SLOT'; }
  survey('.td-browse', 'panel240');
  survey('body', 'page240');

  /* ---- 3) 还原 ---- */
  if (slot) { slot.style.flex = ''; slot.style.width = ''; slot.style.maxWidth = ''; }

  return JSON.stringify(out, null, 1);
})()

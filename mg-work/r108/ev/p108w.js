/* r108 第十九拍 · ① 右栏划词取证
   真鼠标拖选（CDP `Input.dispatchMouseEvent`）⇒ 判「浮条弹不弹、弹在哪」。
   相位：openSide / rvGeom / read / geomFiles / geomSummary */
(function () {
  var M = window.__M || 'x';
  function q(s) { return document.querySelector(s); }
  function qa(s) { return [].slice.call(document.querySelectorAll(s)); }
  function r(e) { if (!e) return null; var b = e.getBoundingClientRect();
    return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cs(e, p) { return e ? getComputedStyle(e)[p] : null; }
  var out = { phase: M };

  function act(mod) {
    var t = qa('.td-browse-tabs [data-td-tab]').filter(function (x) {
      return x.getAttribute('data-td-mod') === mod;
    })[0];
    if (t) { t.click(); return 'tab:' + mod; }
    var o = q('[data-td-open-mod="' + mod + '"]');
    if (o) { o.click(); return 'open:' + mod; }
    return 'miss:' + mod;
  }
  /* 某个元素里第一条「有实体文本」的文本节点，返回它的字形盒（带 Range 测，最准） */
  function textBox(host, skip) {
    if (!host) return null;
    var w = document.createTreeWalker(host, NodeFilter.SHOW_TEXT, null), n, k = 0;
    while ((n = w.nextNode())) {
      var v = (n.nodeValue || '');
      if (v.replace(/\s/g, '').length < 6) continue;
      if (k++ < (skip || 0)) continue;
      var rg = document.createRange();
      rg.selectNodeContents(n.parentElement || n);
      var b = rg.getBoundingClientRect();
      if (b.width > 20 && b.height > 6) return { box: [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)],
        cls: (n.parentElement && n.parentElement.className) || '', txt: v.trim().slice(0, 40) };
    }
    return null;
  }
  function vis(e) { if (!e) return false; var b = e.getBoundingClientRect();
    return b.width > 0 && b.height > 0 && b.top > 60 && b.bottom < window.innerHeight; }

  if (M === 'openSide') { out.done = act('review'); out.browse = r(q('.td-browse')); }
  /* 审查模块：挑两行「看得见」的代码行，给出拖选起止坐标 */
  if (M === 'rvGeom') {
    var rows = qa('.td-rv-body .td-diff .td-dr-t').filter(vis);
    out.rows = rows.length;
    var picks = [];
    for (var i = 0; i < rows.length && picks.length < 2; i++) {
      var t = textBox(rows[i], 0);
      if (!t) continue;
      var b = t.box;
      picks.push({ cls: t.cls, txt: t.txt, box: b, y: Math.round(b[1] + b[3] / 2) });
    }
    out.picks = picks;
    if (picks.length >= 2) {
      out.drag = [picks[0].box[0] + 2, picks[0].y, picks[1].box[0] + Math.min(120, picks[1].box[2] - 6), picks[1].y];
    }
    out.rvScrollTop = q('.td-rv-body') ? q('.td-rv-body').scrollTop : null;
    out.cardCount = qa('.td-rv-body > .td-diff').length;
    out.drTUserSel = cs(rows[0], 'userSelect');
    out.rvBodyUserSel = cs(q('.td-rv-body'), 'userSelect');
    out.browseUserSel = cs(q('.td-browse'), 'userSelect');
  }
  if (M === 'read') {
    var sb = q('.td-selbar');
    out.selText = String(window.getSelection()).slice(0, 90);
    out.selRange = window.getSelection().rangeCount;
    out.selbarExists = !!sb;
    out.selbarHidden = sb ? sb.hasAttribute('hidden') : null;
    out.selbarBox = r(sb);
    out.selbarBtns = sb ? qa('.td-selbar button').map(function (b) { return b.textContent.trim(); }) : [];
    /* 浮条在不在最上层（选中中心点做 elementFromPoint —— 判它有没有被右栏盖住） */
    if (sb && !sb.hasAttribute('hidden')) {
      var bb = sb.getBoundingClientRect();
      var hit = document.elementFromPoint(Math.round(bb.left + bb.width / 2), Math.round(bb.top + bb.height / 2));
      out.selbarOnTop = !!(hit && sb.contains(hit));
      out.selbarHit = hit ? (hit.tagName + '.' + (hit.className || '')) : null;
    }
    /* 浮条是不是真的落在选区**上方**（且没翻边到下方） */
    var r0 = window.getSelection().rangeCount ? window.getSelection().getRangeAt(0).getBoundingClientRect() : null;
    if (sb && r0) {
      var b2 = sb.getBoundingClientRect();
      out.above = Math.round(r0.top - (b2.top + b2.height));
    }
  }
  /* 摘要模块（散文） */
  if (M === 'openSummary') { out.done = act('summary'); }
  if (M === 'geomSummary') {
    var t2 = textBox(q('.td-mod-body[data-td-pane="summary"]') || q('.td-browse'), 0);
    out.pick = t2;
    if (t2) out.drag = [t2.box[0] + 2, Math.round(t2.box[1] + t2.box[3] / 2), t2.box[0] + Math.min(140, t2.box[2] - 6), Math.round(t2.box[1] + t2.box[3] / 2)];
  }
  /* 文件模块（代码区 `.td-browse-code` / `.td-browse-pre` / `.td-code-tx`）
     ⚠ 这个模块的正文**不是** `.td-mod-body`，而是从 r105 逐字剪出来的 `.td-browse-body`
       （左「文件树」+ 右「代码区」两栏）⇒ 选择器要用 `.td-browse-code`。 */
  if (M === 'openFiles') { out.done = act('files'); }
  if (M === 'geomFiles') {
    var pre = q('.td-browse-code');
    var t3 = pre ? textBox(pre, 2) : null;
    out.pick = t3;
    if (t3) out.drag = [t3.box[0] + 2, Math.round(t3.box[1] + t3.box[3] / 2), t3.box[0] + Math.min(140, t3.box[2] - 6), Math.round(t3.box[1] + t3.box[3] / 2)];
  }
  /* 浮条按钮点一下（验「添加到对话」真能用） */
  if (M === 'clickCopy') {
    var b2 = qa('.td-selbar button').filter(function (x) { return /复制/.test(x.textContent); })[0];
    out.found = !!b2; if (b2) b2.click();
  }
  return out;
})();

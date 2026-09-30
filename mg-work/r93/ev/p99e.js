/* r99 取证 E：返回全部受改动元素的视口矩形 + 关键读数，供裁剪对照 */
(function () {
  var out = {};
  function q(s, r) { return (r || document).querySelector(s); }
  function qa(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function R(e) { if (!e) return null; var r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]; }
  var host = q('.r93-conv-host');
  out.dpr = window.devicePixelRatio;
  out.scroll = { hostTop: host ? Math.round(host.getBoundingClientRect().top) : null, docScroll: Math.round(window.scrollY) };

  /* ① 假滚动条 / 真滚动条 */
  var dl = q('.r93-dlist');
  out.dlist = { rect: R(dl), dsb: qa('.r93-dsb').length, hasVBar: dl ? dl.scrollHeight > dl.clientHeight : null, ovf: dl ? getComputedStyle(dl).overflowY : null };

  /* ② 回到底部按钮 */
  var tb = q('.r93-tobottom');
  out.tobottom = { rect: R(tb), color: tb ? getComputedStyle(tb).color : null, bg: tb ? getComputedStyle(tb).backgroundColor : null, cls: tb ? tb.className : null };

  /* ③ rateline */
  var rl = q('.r93-rateline');
  if (rl) {
    var r0 = rl.getBoundingClientRect();
    var lines = qa('.r93-rline', rl), more = q('.r93-rateline > .r93-rbtn', rl), rate = q('.r93-rrate', rl);
    out.rateline = {
      rect: R(rl),
      line1: [Math.round(lines[0].getBoundingClientRect().left - r0.left), Math.round(lines[0].getBoundingClientRect().right - r0.left)],
      rate: [Math.round(rate.getBoundingClientRect().left - r0.left), Math.round(rate.getBoundingClientRect().right - r0.left)],
      line2: [Math.round(lines[1].getBoundingClientRect().left - r0.left), Math.round(lines[1].getBoundingClientRect().right - r0.left)],
      more: [Math.round(more.getBoundingClientRect().left - r0.left), Math.round(more.getBoundingClientRect().right - r0.left)]
    };
  }

  /* ④/⑭ 图标：SKILL（被修正过 viewBox 的）与 umeta 两枚 */
  var fixedSvg = qa('svg').filter(function (s) { return (s.getAttribute('viewBox') || '').indexOf('11.784') === 0; });
  out.fixedIcons = fixedSvg.map(function (s) { return { vb: s.getAttribute('viewBox'), rect: R(s.closest('.r93-iblk') || s) }; });
  var um = q('.r93-umeta');
  out.umeta = { rect: R(um), icons: um ? qa('.r93-iblk', um).map(function (b) { return R(b); }) : null };

  /* ⑦ 改动行 + ⋯ */
  var row = qa('.r93-drow')[2] || q('.r93-drow');
  out.drow = { rect: R(row), name: row ? (q('.r93-dname', row) || {}).textContent : null, more: row ? R(q('.r93-dmore', row)) : null };

  /* ⑥ 任务产物标签 / ⑪ alink / ⑫ pill / ⑬ asst 线 / ⑩ quiz 卡 / ⑧ 折叠头 */
  out.artlabel = { rect: R(q('.r93-artlabel')), fs: q('.r93-artlabel') ? getComputedStyle(q('.r93-artlabel')).fontSize : null };
  out.alink = { rect: R(q('.r93-alink')), fs: q('.r93-alink') ? getComputedStyle(q('.r93-alink')).fontSize : null };
  out.pill = { rect: R(q('.r93-pill')), fs: q('.r93-pill') ? getComputedStyle(q('.r93-pill')).fontSize : null, color: q('.r93-pill') ? getComputedStyle(q('.r93-pill')).color : null };
  var asst = qa('.r93-asst')[1] || q('.r93-asst');
  out.asst = { rect: R(asst), border: asst ? getComputedStyle(asst).borderBottomColor : null };
  out.quiz = { rect: R(q('.r93-card--quiz')), pad: q('.r93-card--quiz') ? getComputedStyle(q('.r93-card--quiz')).padding : null };
  var fh = q('.r93-fh');
  out.fh = { rect: R(fh), ico: fh ? R(q('.r93-iblk', fh)) : null };

  /* ⑨ 复制按钮（点击前状态） */
  var cp = q('[data-r93-copy]');
  out.copyBtn = { rect: R(cp), title: cp ? cp.getAttribute('title') : null, html: cp ? cp.innerHTML.slice(0, 80) : null };

  return JSON.stringify(out);
})();

(function () {
  var out = {};
  var s = document.querySelector('.r107-stats');
  if (!s) return JSON.stringify({ stats: 'ABSENT' });
  var host = s.parentElement;

  function snap(tag) {
    var c = getComputedStyle(s), hr = host.getBoundingClientRect(), sr = s.getBoundingClientRect();
    var rg = document.createRange(); rg.selectNodeContents(s);
    var tr = rg.getBoundingClientRect();                       // ★ 文字的真实盒
    return {
      tag: tag,
      box: [Math.round(sr.x), Math.round(sr.width)],
      text: [Math.round(tr.x), Math.round(tr.width)],
      host: [Math.round(hr.x), Math.round(hr.width)],
      boxCenterDelta: Math.round((sr.x + sr.width / 2) - (hr.x + hr.width / 2)),
      textCenterDelta: Math.round((tr.x + tr.width / 2) - (hr.x + hr.width / 2)),
      textLeftPad: Math.round(tr.x - sr.x),
      textRightPad: Math.round((sr.x + sr.width) - (tr.x + tr.width)),
      sw: s.scrollWidth, cw: s.clientWidth,
      width: c.width, minW: c.minWidth, maxW: c.maxWidth,
      fs: c.fontSize, ta: c.textAlign, ov: c.overflowX, te: c.textOverflow, ws: c.whiteSpace,
      clipped: s.scrollWidth > s.clientWidth + 1
    };
  }

  out.A_现状 = snap('A');
  /* 假设：flex 子项的 `min-width:auto`（= max-content）把它撑到比容器还宽 ⇒ 试加 min-width:0 */
  s.style.minWidth = '0';
  out.B_min0 = snap('B');
  s.style.removeProperty('min-width');
  /* 再试：显式 width:100% */
  s.style.width = '100%';
  out.C_w100 = snap('C');
  s.style.removeProperty('width');

  /* 宿主结构 + 输入卡参照 */
  out.hostKids = Array.prototype.map.call(host.children, function (e) {
    var b = e.getBoundingClientRect();
    return { cls: (e.tagName + '.' + String(e.className || '').trim().split(/\s+/).slice(0, 3).join('.')).slice(0, 46), x: Math.round(b.x), w: Math.round(b.width), h: Math.round(b.height), isStats: e === s };
  });
  out.hostCs = (function () { var c = getComputedStyle(host); return { disp: c.display, dir: c.flexDirection, align: c.alignItems, pad: c.padding, w: c.width }; })();
  out.viewport = [window.innerWidth, window.innerHeight];
  out.uiFs = getComputedStyle(document.documentElement).getPropertyValue('--ui-fs');
  out.browseOpen = !!(document.querySelector('.av-browse-on'));
  return JSON.stringify(out, null, 1);
})()

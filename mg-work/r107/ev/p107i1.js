(function () {
  var out = {};
  function r(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  function cs1(el, p) { return el ? getComputedStyle(el)[p] : 'ABSENT'; }

  /* ================= 一、六条指标的现状 ================= */
  out.m = {};

  /* ① 溢出普查（下面单独做） */

  /* ② 「折叠此文件」菜单项 —— 见 shell 侧 ctxmenu 探针 */

  /* ③ ll.td-sum-h 字号 */
  out.m.sumH = (function () {
    var a = document.querySelectorAll('.td-sum-h'), o = [];
    a.forEach(function (e) { var c = getComputedStyle(e); o.push({ fs: c.fontSize, fw: c.fontWeight, lh: c.lineHeight, r: r(e), t: (e.textContent || '').trim().slice(0, 10) }); });
    return { n: a.length, items: o };
  })();

  /* ④⑤ .td-diff-path 开合两态 + .td-diff-rows 内各档字号 */
  out.m.diff = (function () {
    var o = { paths: [], rows: [] };
    document.querySelectorAll('[data-td-diff]').forEach(function (art, i) {
      var open = art.classList.contains('is-open');
      var p = art.querySelector('.td-diff-path');
      if (p) { var c = getComputedStyle(p); o.paths.push({ i: i, open: open, fs: c.fontSize, fw: c.fontWeight, color: c.color, r: r(p), ov: p.scrollWidth - p.clientWidth }); }
      var rows = art.querySelector('.td-diff-rows:not(.td-diff-split)');
      if (rows) {
        var rc = getComputedStyle(rows);
        var inner = {};
        ['.td-dr', '.td-dr-no', '.td-dr-t', '.td-dsc-c', '.td-diff-more', '.td-dr-nn'].forEach(function (s) {
          var e = rows.querySelector(s) || art.querySelector(s);
          inner[s] = e ? getComputedStyle(e).fontSize : 'ABSENT';
        });
        o.rows.push({ i: i, open: open, fs: rc.fontSize, inner: inner, sh: rows.scrollHeight });
      }
    });
    return o;
  })();

  /* ⑥ .r107-stats */
  out.m.stats = (function () {
    var e = document.querySelector('.r107-stats');
    if (!e) return 'ABSENT';
    var c = getComputedStyle(e), host = e.parentElement, hc = getComputedStyle(host);
    return {
      ta: c.textAlign, disp: c.display, ws: c.whiteSpace, ov: c.overflowX, te: c.textOverflow,
      r: r(e), w: Math.round(e.getBoundingClientRect().width),
      hostR: r(host), hostDisp: hc.display, hostAlign: hc.alignItems, hostW: Math.round(host.getBoundingClientRect().width),
      sw: e.scrollWidth, cw: e.clientWidth,
      txt: (e.textContent || '').slice(0, 30)
    };
  })();

  /* ================= 二、① 全页「文字溢出」普查 ================= */
  var groups = {}, total = 0;
  document.querySelectorAll('body *').forEach(function (e) {
    var c = getComputedStyle(e);
    if (c.display === 'none' || c.visibility === 'hidden' || e.hasAttribute('hidden')) return;
    if (c.overflowX === 'auto' || c.overflowX === 'scroll') return;      // 滚动容器不算
    var cw = e.clientWidth, sw = e.scrollWidth;
    if (cw <= 0 || sw <= cw + 1) return;
    if (!(e.textContent || '').trim()) return;
    var cls = String(e.className || '').trim().split(/\s+/).filter(Boolean).slice(0, 2).join('.');
    var k = e.tagName + (cls ? '.' + cls : '');
    if (!groups[k]) groups[k] = { n: 0, max: 0, te: c.textOverflow, ws: c.whiteSpace, ox: c.overflowX, mw: c.minWidth, sample: '' };
    groups[k].n++;
    groups[k].max = Math.max(groups[k].max, sw - cw);
    if (!groups[k].sample) groups[k].sample = (e.textContent || '').trim().slice(0, 26);
    total++;
  });
  out.ovTotal = total;
  out.ovGroups = groups;

  return JSON.stringify(out, null, 1);
})()

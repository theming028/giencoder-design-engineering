(function () {
  var out = {};
  function r(el) { var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }

  /* ---------- ① 统计行：真节点 + 可框选 + 版式 ---------- */
  var host = document.querySelector('main > div > div.flex-1.justify-center > div.mt-8');
  out.hostFound = !!host;
  if (host) {
    var st = host.querySelector(':scope > .r107-stats');
    out.statsFound = !!st;
    if (st) {
      out.statsR = r(st);
      out.statsTxt = (st.textContent || '').slice(0, 40);
      out.statsIsLast = host.lastElementChild === st;
      out.statsHostGap = getComputedStyle(host).gap;
      out.statsCS = (function () {
        var c = getComputedStyle(st);
        return { fs: c.fontSize, lh: c.lineHeight, color: c.color, ws: c.whiteSpace, us: c.userSelect };
      })();
      /* 真·拖选：caretRangeFromPoint ×2 → setBaseAndExtent（与浏览器内部同一机制） */
      var mid = Math.round(st.getBoundingClientRect().top + st.getBoundingClientRect().height / 2);
      var xa = Math.round(st.getBoundingClientRect().left + 6);
      var xb = Math.round(st.getBoundingClientRect().right - 6);
      var r1 = document.caretRangeFromPoint(xa, mid), r2 = document.caretRangeFromPoint(xb, mid);
      if (r1 && r2) {
        var sel = window.getSelection();
        sel.setBaseAndExtent(r1.startContainer, r1.startOffset, r2.startContainer, r2.startOffset);
        out.selLen = sel.toString().length;
        out.selTxt = sel.toString().slice(0, 40);
        out.caretNode = r1.startContainer.nodeName;
      }
      /* 旧伪元素必须已被关掉 */
      out.afterContent = (getComputedStyle(host, '::after').content || 'none').slice(0, 40);
    }
    /* 伪元素残留检测：宿主 ::after 不该再产出可见盒子 */
    out.hostAfterW = (function () { var cs = getComputedStyle(host, '::after'); return cs.content; })();
  }

  /* ---------- ② .r93-pre 字体族 ---------- */
  var pre = document.querySelector('.r93-pre');
  if (pre) {
    out.preFont = getComputedStyle(pre).fontFamily;
    out.bodyFont = getComputedStyle(document.body).fontFamily;
    out.preSameAsBody = out.preFont === out.bodyFont;
    out.preFs = getComputedStyle(pre).fontSize;
    out.preLh = getComputedStyle(pre).lineHeight;
    var ps = document.querySelectorAll('.r93-pre'), fam = {};
    ps.forEach(function (e) { var f = getComputedStyle(e).fontFamily; fam[f] = (fam[f] || 0) + 1; });
    out.preCount = ps.length;
    out.preFams = Object.keys(fam).length + ' 种';
  }

  /* ---------- ③ 窄档两条 ---------- */
  var pane = document.querySelector('.r93-pane');
  var sc = document.querySelector('.r93-scroll');
  var sr = sc.getBoundingClientRect();
  var card = null, cs2 = document.querySelectorAll('main div');
  for (var i = 0; i < cs2.length; i++) {
    var cl = cs2[i].className || '';
    if (typeof cl === 'string' && cl.indexOf('rounded-[16px]') >= 0 && cl.indexOf('bg-white') >= 0) { card = cs2[i]; break; }
  }
  out.vw = window.innerWidth;
  out.pane = pane ? r(pane) : null;
  out.scrollContentBox = [Math.round(sr.left + 10), Math.round(sr.right - 10)];
  out.card = card ? r(card) : null;
  var sk = document.querySelector('[aria-label="技能选择"]');
  if (sk) {
    var skr = sk.getBoundingClientRect();
    out.skill = {
      r: r(sk), w: getComputedStyle(sk).width, open: !!sk.getAttribute('style'),
      overL: Math.round(out.scrollContentBox[0] - skr.left),
      overR: Math.round((skr.left + skr.width) - out.scrollContentBox[1])
    };
  }
  out.alerts = [];
  document.querySelectorAll('.r93-alert').forEach(function (e) {
    var b = e.getBoundingClientRect(), c = getComputedStyle(e);
    var desc = e.querySelector('.r93-adesc');
    var dr = desc ? desc.getBoundingClientRect() : null;
    out.alerts.push({
      r: r(e), h: c.height, minH: c.minHeight,
      ch_sh: e.clientHeight + '/' + e.scrollHeight,
      descInside: dr ? (Math.round(dr.top) >= Math.round(b.top) && Math.round(dr.bottom) <= Math.round(b.bottom)) : null,
      descH: dr ? Math.round(dr.height) : null
    });
  });
  return JSON.stringify(out);
})()

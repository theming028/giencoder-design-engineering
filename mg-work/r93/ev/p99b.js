(function () {
  var out = {};
  var q = function (s, r) { return (r || document).querySelector(s); };
  var qa = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var host = q('.r93-conv-host');
  var R = function (e) {
    if (!e) return null;
    var r = e.getBoundingClientRect();
    return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) };
  };
  var fs = function (e) { return e ? getComputedStyle(e).fontSize : null; };
  var lh = function (e) { return e ? getComputedStyle(e).lineHeight : null; };
  out.meta = { win: { w: innerWidth, h: innerHeight }, host: R(host) };

  /* ① 假滚动条已删 + 列表改真实滚动 */
  var dl = q('.r93-dlist');
  out.item1 = {
    dsbCount: qa('.r93-dsb').length,
    dlistOverflowY: dl ? getComputedStyle(dl).overflowY : null,
    dlist: dl ? { h: dl.clientHeight, sh: dl.scrollHeight, hasBar: dl.scrollHeight > dl.clientHeight } : null
  };

  /* ② 滚动到底部：默认前景色 + hover 规则是否在注入的样式里 */
  var tb = q('.r93-tobottom');
  var cssTxt = q('#r93-conv-css') ? q('#r93-conv-css').textContent : '';
  out.item2 = {
    color: tb ? getComputedStyle(tb).color : null,
    bg: tb ? getComputedStyle(tb).backgroundColor : null,
    hoverRule: /\.r93-tobottom:hover\s*\{[^}]*\}/.exec(cssTxt) ? /\.r93-tobottom:hover\s*\{[^}]*\}/.exec(cssTxt)[0] : null
  };

  /* ③ rateline：第 2 根线 与 ⋯ 按钮盒 的相对位置 */
  var rl = q('.r93-rateline');
  if (rl) {
    var r0 = rl.getBoundingClientRect();
    var lines = qa('.r93-rline', rl), btn = q('.r93-rbtn:last-of-type', rl);
    out.item3 = {
      line1: Math.round(lines[0].getBoundingClientRect().left - r0.left),
      line2: Math.round(lines[1].getBoundingClientRect().left - r0.left),
      moreBtn: Math.round(btn.getBoundingClientRect().left - r0.left),
      btnML: getComputedStyle(btn).marginLeft,
      line2ML: getComputedStyle(lines[1]).marginLeft
    };
  }

  /* ④/⑭ 14px 图标：viewBox 分布 + umeta 间距 */
  var vbMap = {};
  qa('.r93-iblk.r93-i14 > svg').forEach(function (s) {
    var v = s.getAttribute('viewBox');
    vbMap[v] = (vbMap[v] || 0) + 1;
  });
  out.item4 = { viewBoxes: vbMap, iconsWithOverflowFix: qa('.r93-iblk.r93-i14 > svg').filter(function (s) { return s.getAttribute('viewBox') !== '0 0 14 14'; }).length };
  var um = q('.r93-umeta');
  if (um) {
    var ur = um.getBoundingClientRect();
    var t = q('.r93-t12', um), bs = qa('.r93-ib', um);
    out.item14 = {
      box: R(um),
      timeRight: Math.round(t.getBoundingClientRect().right - ur.right),
      b1Left: Math.round(bs[0].getBoundingClientRect().left - ur.right),
      b2Left: Math.round(bs[1].getBoundingClientRect().left - ur.right),
      gapTB1: Math.round(bs[0].getBoundingClientRect().left - t.getBoundingClientRect().right),
      gapB1B2: Math.round(bs[1].getBoundingClientRect().left - bs[0].getBoundingClientRect().right),
      regenVB: q('svg', bs[0]) ? q('svg', bs[0]).getAttribute('viewBox') : null,
      regenD: q('svg path', bs[0]) ? q('svg path', bs[0]).getAttribute('d').slice(0, 60) : null
    };
  }

  /* ⑤ 涟漪 */
  var m = q('main.dot-bg');
  var probe = document.createElement('span');
  probe.className = 'r74-ripple';
  m.appendChild(probe);
  out.item5 = { rippleBg: getComputedStyle(probe).backgroundImage, mainBg: getComputedStyle(m).backgroundImage };
  probe.parentNode.removeChild(probe);

  /* ⑥ 任务产物标签 */
  out.item6 = { fs: fs(q('.r93-artlabel')), lh: lh(q('.r93-artlabel')),
    inkW: (function () { var e = q('.r93-artlabel');
      if (!e) return null; var rg = document.createRange(); rg.selectNodeContents(e);
      return Math.round(rg.getBoundingClientRect().width); })() };

  /* ⑦ 右键菜单 */
  var row = q('.r93-drow');
  var before = qa('.r93-ctx').length;
  var rr = row.getBoundingClientRect();
  row.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: rr.left + 60, clientY: rr.top + 18 }));
  var menu = q('.r93-ctx');
  out.item7 = {
    before: before,
    exists: !!menu,
    open: menu ? menu.classList.contains('giencoder-popup-open') : null,
    rect: R(menu),
    items: menu ? qa('.giencoder-dropdown-item', menu).map(function (i) { return i.textContent.trim() + '@' + R(i).h; }) : null,
    labelFs: menu ? fs(q('.r93-ctx-label', menu)) : null,
    divider: menu ? qa('.giencoder-dropdown-divider', menu).length : null,
    zIndex: menu ? getComputedStyle(menu).zIndex : null,
    rowName: row.getAttribute('data-r93-file')
  };
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
  /* ⋯ 按钮走同一份菜单 */
  var more = q('.r93-dmore');
  more.click();
  var menu2 = q('.r93-ctx');
  out.item7.viaMoreBtn = !!menu2 && menu2 === menu && menu2.classList.contains('giencoder-popup-open');
  out.item7.sameNode = (menu2 === menu);
  out.item7.afterMoreRect = R(menu2);
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
  out.item7.closedAfterEsc = q('.r93-ctx').classList.contains('giencoder-popup-open') === false;

  /* ⑧ 折叠块开合：两态图标槽宽 + 标题左偏移（关键=不跳） */
  var fold = q('.r93-fold');
  var meas = function () {
    var open = fold.getAttribute('data-open') === '1';
    var head = q(open ? '.r93-fh' : '.r93-fc', fold);
    var ic = q('.r93-iblk', head);
    var tx = q('span:not(.r93-iblk)', head);
    var fr = fold.getBoundingClientRect(), hr = head.getBoundingClientRect();
    return { open: open, headW: Math.round(hr.width), headH: Math.round(hr.height),
      icW: Math.round(ic.getBoundingClientRect().width), icH: Math.round(ic.getBoundingClientRect().height),
      icX: Math.round(ic.getBoundingClientRect().left - fr.left),
      txX: Math.round(tx.getBoundingClientRect().left - fr.left),
      txFs: fs(tx), txColor: getComputedStyle(tx).color,
      headTop: Math.round(hr.top - fr.top) };
  };
  var a1 = meas();
  q('.r93-fh', fold).click();
  var a0 = meas();
  q('.r93-fc', fold).click();
  var a2 = meas();
  out.item8 = { open: a1, closed: a0, reopened: a2, reopenMatches: a1.txX === a2.txX && a1.headH === a2.headH };

  /* ⑨ 复制按钮 hover 口径 + 点击后绿勾 */
  var cb = q('[data-r93-copy]');
  var icb = q('.r93-iblk', cb);
  var okBefore = icb.innerHTML.indexOf('circle') >= 0 || icb.innerHTML.length;
  cb.click();
  out.item9 = {
    hoverRule: /\.r93-ib:hover\s*\{[^}]*\}/.exec(cssTxt) ? /\.r93-ib:hover\s*\{[^}]*\}/.exec(cssTxt)[0] : null,
    copied: cb.classList.contains('is-copied'),
    color: getComputedStyle(cb).color,
    iconHtmlHead: icb.innerHTML.slice(0, 70),
    svgCount: qa('svg', icb).length
  };
  window.__cb = cb;

  /* ⑩ 需求采访卡 */
  var c2 = q('.r93-t14.r93-c2');
  var quiz = q('.r93-card--quiz');
  out.item10 = {
    c2MarginTop: c2 ? getComputedStyle(c2).marginTop : null,
    c2Fs: fs(c2),
    cardFs: fs(q('.r93-card')),
    quizPad: quiz ? getComputedStyle(quiz).padding : null,
    quizH: quiz ? Math.round(quiz.getBoundingClientRect().height) : null,
    quizInkFs: quiz ? qa('*', quiz).filter(function (e) { return e.children.length === 0 && e.textContent.trim(); }).map(function (e) { return fs(e); }).filter(function (v, i, a) { return a.indexOf(v) === i; }) : null
  };

  /* ⑪ alink */
  var al = q('.r93-alink');
  out.item11 = { fs: fs(al), lh: lh(al), h: R(al).h, inkW: (function () {
    var rg = document.createRange(); rg.selectNodeContents(al); return Math.round(rg.getBoundingClientRect().width); })() };

  /* ⑫ pill */
  var pill = q('.r93-pill');
  out.item12 = { rect: R(pill), fs: fs(pill), lh: lh(pill), pad: getComputedStyle(pill).padding,
    radius: getComputedStyle(pill).borderRadius, bg: getComputedStyle(pill).backgroundColor,
    color: getComputedStyle(pill).color, shadow: getComputedStyle(pill).boxShadow };

  /* ⑬ 助手头底线 */
  var asst = q('.r93-asst');
  out.item13 = { border: getComputedStyle(asst).borderBottomColor, w: getComputedStyle(asst).borderBottomWidth };

  return JSON.stringify(out);
})()

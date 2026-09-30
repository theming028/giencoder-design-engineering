(function () {
  var host = document.querySelector('.r93-conv-host');
  if (!host) return JSON.stringify({ err: 'no host' });
  var R = function (el, base) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    var b = (base || document.body).getBoundingClientRect();
    return { x: Math.round(r.left - b.left), y: Math.round(r.top - b.top), w: Math.round(r.width), h: Math.round(r.height) };
  };
  var cs = function (el, props) {
    if (!el) return null;
    var c = getComputedStyle(el), o = {};
    props.forEach(function (p) { o[p] = c.getPropertyValue(p); });
    return o;
  };
  var wrap = host.querySelector('.r93-wrap');
  var out = {};

  /* 1. 差分卡滚动条 & 列表 */
  var dl = host.querySelector('.r93-dlist');
  var dsb = host.querySelector('.r93-dsb');
  out.item1 = {
    dsbExists: !!dsb, dsbRect: R(dsb, dl),
    dlist: cs(dl, ['overflow-y', 'height']),
    dlistScroll: dl ? { scrollH: dl.scrollHeight, clientH: dl.clientHeight, rows: dl.querySelectorAll('.r93-drow').length } : null
  };

  /* 2. 滚动到底部按钮 */
  var tb = host.querySelector('.r93-tobottom');
  out.item2 = {
    rect: R(tb, wrap), color: tb && getComputedStyle(tb).color,
    bg: tb && getComputedStyle(tb).backgroundColor,
    border: tb && getComputedStyle(tb).borderColor,
    spanColor: tb && getComputedStyle(tb.querySelector('.r93-t14')).color,
    svgColor: tb && getComputedStyle(tb.querySelector('svg')).color
  };

  /* 3. rateline 各件 */
  var rl = host.querySelector('.r93-rateline');
  var kids = rl ? [].map.call(rl.children, function (k) {
    return { cls: k.className, rect: R(k, rl), color: getComputedStyle(k).color,
             bg: getComputedStyle(k).backgroundColor, ml: getComputedStyle(k).marginLeft };
  }) : null;
  var lastBtn = rl && rl.querySelector('.r93-rbtn:last-of-type');
  out.item3 = { rateline: R(rl, wrap), kids: kids, lastBtn: R(lastBtn, rl),
                line2: R(rl.querySelectorAll('.r93-rline')[1], rl) };

  /* 4/14. 内容区所有 .r93-i14 图标（定位“异常”的那个） */
  out.icons14 = [].map.call(host.querySelectorAll('.r93-iblk.r93-i14'), function (el, i) {
    var svg = el.querySelector('svg');
    return { i: i, rect: R(el, wrap), parent: el.parentElement.className,
             title: (el.parentElement.getAttribute('title') || ''),
             vb: svg ? svg.getAttribute('viewBox') : null,
             svgFirst: svg ? svg.innerHTML.slice(0, 60) : null };
  }).slice(0, 40);

  /* 14. umeta 行 */
  var um = host.querySelector('.r93-umeta');
  out.item14 = {
    rect: R(um, wrap), gap: um && getComputedStyle(um).gap,
    kids: um ? [].map.call(um.children, function (k) {
      return { cls: k.className, tag: k.tagName, rect: R(k, um), text: (k.textContent || '').slice(0, 8) };
    }) : null
  };

  /* 5. 波点 / 涟漪 */
  var mains = document.querySelectorAll('main');
  out.item5 = {
    mains: [].map.call(mains, function (m) {
      var c = getComputedStyle(m), b = getComputedStyle(m, '::before');
      return { cls: m.className, bgImage: c.backgroundImage.slice(0, 60),
               beforeDisplay: b.display, beforeContent: b.content };
    }),
    dotbg: [].map.call(document.querySelectorAll('.dot-bg,[class*=ripple]'), function (e) {
      return { tag: e.tagName, cls: e.className };
    }).slice(0, 30)
  };

  /* 6. artlabel */
  var al = host.querySelector('.r93-artlabel');
  out.item6 = { cls: al && al.className, fs: al && getComputedStyle(al).fontSize, lh: al && getComputedStyle(al).lineHeight, color: al && getComputedStyle(al).color };

  /* 7. drow */
  var dr = host.querySelector('.r93-drow');
  out.item7 = { row: R(dr, dl), moreBtn: R(dr && dr.querySelector('.r93-dmore'), dr),
                moreTitle: dr && dr.querySelector('.r93-dmore') && dr.querySelector('.r93-dmore').getAttribute('title'),
                menuInDom: !!host.querySelector('.r93-dmenu, .giencoder-menu, [role=menu]') };

  /* 8. fold 折叠头/展开头 */
  out.item8 = [].map.call(host.querySelectorAll('.r93-fold'), function (f, i) {
    var fc = f.querySelector(':scope > .r93-fc'), fh = f.querySelector(':scope > .r93-fh');
    return { i: i, open: f.getAttribute('data-open'),
             fc: R(fc, wrap), fh: R(fh, wrap),
             fcIc: fc && fc.querySelector('.r93-iblk') && R(fc.querySelector('.r93-iblk'), fc),
             fhIc: fh && fh.querySelector('.r93-iblk') && R(fh.querySelector('.r93-iblk'), fh),
             fcKind: fc && fc.querySelector('.r93-iblk') && fc.querySelector('.r93-iblk').className,
             fhKind: fh && fh.querySelector('.r93-iblk') && fh.querySelector('.r93-iblk').className,
             fcPad: fc && getComputedStyle(fc).padding, fhPad: fh && getComputedStyle(fh).padding };
  }).slice(0, 6);

  /* 9. 复制按钮 hover 底色（静态值，:hover 需另测） */
  var ib = host.querySelector('.r93-ib');
  out.item9 = { ibRect: R(ib, wrap), color: ib && getComputedStyle(ib).color,
                ibRadius: ib && getComputedStyle(ib).borderRadius,
                copySvgCount: host.querySelectorAll('.r93-ib svg').length };

  /* 10. t14.c2 顶距 + card 字号 */
  var c2 = host.querySelector('.r93-t14.r93-c2');
  var card = host.querySelector('.r93-card');
  out.item10 = { c2MarginTop: c2 && getComputedStyle(c2).marginTop, c2Fs: c2 && getComputedStyle(c2).fontSize,
                 cardFs: card && getComputedStyle(card).fontSize,
                 cardInnerFsList: [].map.call(host.querySelectorAll('.r93-card *'), function (e) {
                   var t = (e.textContent || '').trim();
                   return t ? getComputedStyle(e).fontSize : null;
                 }).filter(Boolean).slice(0, 20) };

  /* 11. alink */
  var alk = host.querySelector('.r93-alink');
  out.item11 = { fs: alk && getComputedStyle(alk).fontSize, lh: alk && getComputedStyle(alk).lineHeight, rect: R(alk, wrap), color: alk && getComputedStyle(alk).color };

  /* 12. pill */
  var pl = host.querySelector('.r93-pill');
  out.item12 = { rect: R(pl, wrap), fs: pl && getComputedStyle(pl).fontSize, lh: pl && getComputedStyle(pl).lineHeight,
                 pad: pl && getComputedStyle(pl).padding, radius: pl && getComputedStyle(pl).borderRadius,
                 bg: pl && getComputedStyle(pl).backgroundColor, color: pl && getComputedStyle(pl).color,
                 shadow: pl && getComputedStyle(pl).boxShadow };

  /* 13. asst */
  var asst = host.querySelector('.r93-asst');
  out.item13 = { bbColor: asst && getComputedStyle(asst).borderBottomColor, bbWidth: asst && getComputedStyle(asst).borderBottomWidth,
                 pb: asst && getComputedStyle(asst).paddingBottom };

  /* 附：wrap / 视口 */
  out.meta = { wrap: R(wrap), win: { w: innerWidth, h: innerHeight }, sc: { sh: host.querySelector('.r93-scroll').scrollHeight, ch: host.querySelector('.r93-scroll').clientHeight } };
  return JSON.stringify(out);
})()

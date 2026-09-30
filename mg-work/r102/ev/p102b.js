/* r102 改后读数（十一条） */
(function () {
  var out = {};
  function cs(el) { return el ? getComputedStyle(el) : null; }
  function R(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }
  var host = document.querySelector('.r93-conv-host') || document;

  /* ⑪ seg */
  var seg = document.querySelector('.r93-seg'), bar = document.querySelector('.r93-bar');
  var segBtn = document.querySelector('.r93-seg .giencoder-radio-button');
  var s1 = cs(seg), s2 = cs(segBtn);
  out.seg = {
    box: R(seg), barBox: R(bar), h: R(seg) ? R(seg)[3] : null,
    pad: s1 ? s1.padding : null,
    btnH: s2 ? s2.height : null, btnMinH: s2 ? s2.minHeight : null,
    upper: R(seg) && R(bar) ? R(seg)[1] - R(bar)[1] : null,
    lower: R(seg) && R(bar) ? (R(bar)[1] + R(bar)[3]) - (R(seg)[1] + R(seg)[3]) : null,
    txtBox: R(document.querySelector('.r93-seg .giencoder-radio-button-text'))
  };

  /* ① 字号 + 数字动效 */
  function probe(sel) { var e = document.querySelector(sel); if (!e) return { sel: sel, miss: 1 }; var c = cs(e); return { sel: sel, fs: c.fontSize, lh: c.lineHeight, box: R(e), txt: (e.textContent || '').slice(0, 22) }; }
  out.t14 = [probe('.r93-fh .r93-t14'), probe('.r93-ubt'), probe('.r93-tobottom .r93-t14'), probe('.r93-ahd .r93-t14b')];
  var hist = {}, all = document.querySelectorAll('.r93-t14');
  for (var i = 0; i < all.length; i++) { var f = cs(all[i]).fontSize; hist[f] = (hist[f] || 0) + 1; }
  out.t14Hist = hist; out.t14N = all.length;
  var inC = document.querySelectorAll('.r93-card .r93-t14'), h2 = {};
  for (var j = 0; j < inC.length; j++) { var g = cs(inC[j]).fontSize; h2[g] = (h2[g] || 0) + 1; }
  out.t14InCard = { n: inC.length, hist: h2 };

  var nums = document.querySelectorAll('.r93-num');
  var i0 = document.querySelector('.r93-num-i');
  var c0 = i0 ? cs(i0) : null;
  out.num = {
    n: nums.length,
    anim: c0 ? c0.animationName : null, dur: c0 ? c0.animationDuration : null,
    delay: c0 ? c0.animationDelay : null, fill: c0 ? c0.animationFillMode : null,
    op: c0 ? c0.opacity : null, tf: c0 ? c0.transform : null,
    firstTxt: i0 ? i0.textContent : null,
    outerBox: nums[0] ? R(nums[0]) : null,
    innerBox: i0 ? R(i0) : null
  };
  /* ① 基线 A/B：临时撤掉 .r93-num 的 overflow/valign，看数字 y 是否位移 */
  (function () {
    var el = document.querySelector('.r93-ubt .r93-num') || nums[0];
    if (!el) { out.numAB = 'none'; return; }
    var before = R(el);
    var keep = el.getAttribute('style') || '';
    el.setAttribute('style', keep + ';overflow:visible !important;vertical-align:baseline !important;');
    var after = R(el);
    el.setAttribute('style', keep);
    out.numAB = { before: before, after: after, dy: (before && after) ? (after[1] - before[1]) : null, dx: (before && after) ? (after[0] - before[0]) : null };
  })();

  /* ④ t12.nm */
  out.nm = [];
  [].forEach.call(document.querySelectorAll('.r93-t12.r93-nm'), function (e) {
    out.nm.push({ fs: cs(e).fontSize, box: R(e), txt: (e.textContent || '').slice(0, 26) });
  });

  /* ⑤ cv */
  var cv = document.querySelector('.r93-iblk.r93-cv'), csvg = cv ? cv.querySelector('svg') : null;
  out.cv = { slot: R(cv), slotW: cv ? cs(cv).width : null, svg: R(csvg), svgW: csvg ? cs(csvg).width : null, n: document.querySelectorAll('.r93-iblk.r93-cv').length };

  /* ② fchev 几何（基态） */
  var fcAll = document.querySelectorAll('.r93-fc');
  var fc0 = fcAll.length ? fcAll[fcAll.length - 1] : null;
  var fchev = fc0 ? fc0.querySelector('.r93-fchev') : null;
  out.fchevBase = {
    fcBox: R(fc0), gap: fc0 ? cs(fc0).gap : null, chevML: fchev ? cs(fchev).marginLeft : null,
    chevOp: fchev ? cs(fchev).opacity : null, nFc: fcAll.length,
    titleRight: (function () { var t = fc0 ? fc0.querySelector('.r93-t14') : null; return t ? Math.round(t.getBoundingClientRect().right) : null; })(),
    chevLeft: fchev ? Math.round(fchev.getBoundingClientRect().left) : null
  };

  /* ⑦ asst */
  var asst = document.querySelector('.r93-asst');
  out.asst = asst ? { border: cs(asst).borderBottomColor } : null;

  /* ⑧ drow */
  var drow = document.querySelector('.r93-drow');
  out.drow = drow ? { pad: cs(drow).padding, box: R(drow), nameBox: R(drow.querySelector('.r93-dname')), moreBox: R(drow.querySelector('.r93-dmore')), n: document.querySelectorAll('.r93-drow').length } : null;

  /* ⑨ dhead */
  var dhead = document.querySelector('.r93-dhead');
  out.dhead = dhead ? { pad: cs(dhead).padding, box: R(dhead), icBox: R(dhead.querySelector('.r93-dh1 > .r93-iblk')) } : null;

  /* ⑩ tobottom */
  var tb = document.querySelector('.r93-tobottom');
  var ctb = tb ? cs(tb) : null;
  out.tobottom = tb ? { bg: ctb.backgroundColor, bf: ctb.backdropFilter, wbf: ctb.webkitBackdropFilter, radius: ctb.borderRadius, box: R(tb) } : null;

  /* ③ 折叠：静态态（未点击） */
  var fb = document.querySelector('.r93-fold > .r93-fb');
  var cfb = fb ? cs(fb) : null;
  out.fbBase = fb ? { maxH: cfb.maxHeight, ovf: cfb.overflow, trans: cfb.transitionProperty, dur: cfb.transitionDuration, cls: fb.className, display: cfb.display, mt: cfb.marginTop } : null;
  var folds = document.querySelectorAll('.r93-fold'), dist = {};
  [].forEach.call(folds, function (f) { var k = f.getAttribute('data-open'); dist[k] = (dist[k] || 0) + 1; });
  out.folds = { n: folds.length, dist: dist };

  /* ⑥ meta（基态色） */
  var meta = document.querySelector('.r93-fh .r93-t12l.r93-fm') || document.querySelector('.r93-fh .r93-t12l');
  out.metaBase = meta ? { color: cs(meta).color, fs: cs(meta).fontSize, cls: meta.className } : null;
  return JSON.stringify(out);
})()

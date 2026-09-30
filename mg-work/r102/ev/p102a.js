/* r102 基线静态读数（改前）：十一条逐项量现状 */
(function () {
  var out = {};
  var host = document.querySelector('.r93-conv-host') || document;
  function cs(el) { return el ? getComputedStyle(el) : null; }
  function R(el) { if (!el) return null; var b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; }

  /* ⑪ seg */
  var seg = document.querySelector('.r93-seg');
  var bar = document.querySelector('.r93-bar');
  var segBtn = document.querySelector('.r93-seg .giencoder-radio-button');
  var segBtnCk = document.querySelector('.r93-seg .giencoder-radio-button-checked');
  var s1 = cs(seg), s2 = cs(segBtn);
  out.seg = {
    box: R(seg), barBox: R(bar),
    padding: s1 ? s1.paddingTop + ' ' + s1.paddingRight + ' ' + s1.paddingBottom + ' ' + s1.paddingLeft : null,
    bg: s1 ? s1.backgroundColor : null,
    radius: s1 ? s1.borderRadius : null,
    btnH: s2 ? s2.height : null, btnMinH: s2 ? s2.minHeight : null,
    btnLH: s2 ? s2.lineHeight : null, btnFS: s2 ? s2.fontSize : null,
    btnBox: R(segBtn), ckBox: R(segBtnCk),
    txtBox: R(document.querySelector('.r93-seg .giencoder-radio-button-text'))
  };

  /* ① .r93-t14 字号：取几个代表 */
  function probe(sel, tag) {
    var el = document.querySelector(sel);
    if (!el) return { sel: sel, tag: tag, miss: true };
    var c = cs(el);
    return { sel: sel, tag: tag, fs: c.fontSize, lh: c.lineHeight, box: R(el), txt: (el.textContent || '').slice(0, 24) };
  }
  out.t14 = [
    probe('.r93-fh .r93-t14', 'fh-标题'),
    probe('.r93-fc .r93-t14', 'fc-标题'),
    probe('.r93-ubt', '用户气泡'),
    probe('.r93-tobottom .r93-t14', '药丸文案'),
    probe('.r93-ahd .r93-t14b', 't14b-助手名')
  ];
  /* 全页 .r93-t14 字号直方图 */
  var hist = {}, all = document.querySelectorAll('.r93-t14');
  for (var i = 0; i < all.length; i++) {
    var f = cs(all[i]).fontSize; hist[f] = (hist[f] || 0) + 1;
  }
  out.t14Hist = hist;
  out.t14Count = all.length;
  /* 卡内 .r93-t14 单独看 */
  var inCard = document.querySelectorAll('.r93-card .r93-t14');
  var h2 = {};
  for (var j = 0; j < inCard.length; j++) { var g = cs(inCard[j]).fontSize; h2[g] = (h2[g] || 0) + 1; }
  out.t14InCard = { n: inCard.length, hist: h2 };

  /* ④ .r93-t12.r93-nm */
  out.nm = [];
  var nms = document.querySelectorAll('.r93-t12.r93-nm');
  for (var k = 0; k < nms.length; k++) {
    out.nm.push({ fs: cs(nms[k]).fontSize, box: R(nms[k]), txt: (nms[k].textContent || '').slice(0, 30) });
  }

  /* ⑤ cv 箭头 svg */
  var cv = document.querySelector('.r93-iblk.r93-cv');
  out.cv = {
    slot: R(cv), slotW: cv ? cs(cv).width : null,
    svg: cv ? R(cv.querySelector('svg')) : null,
    svgW: cv && cv.querySelector('svg') ? cs(cv.querySelector('svg')).width : null,
    n: document.querySelectorAll('.r93-iblk.r93-cv').length
  };

  /* ② fchev 间距 */
  var fc = document.querySelector('.r93-fold[data-open="0"] > .r93-fc') || document.querySelector('.r93-fc');
  var fchev = fc ? fc.querySelector('.r93-fchev') : null;
  out.fchev = {
    fcBox: R(fc),
    fcGap: fc ? cs(fc).gap : null,
    chevBox: R(fchev),
    chevML: fchev ? cs(fchev).marginLeft : null,
    chevOp: fchev ? cs(fchev).opacity : null,
    /* 标题右缘 → 箭头左缘 */
    titleRight: (function () { var t = fc ? fc.querySelector('.r93-t14') : null; return t ? Math.round(t.getBoundingClientRect().right) : null; })()
  };

  /* ⑥ fh hover 目标 meta */
  var meta = document.querySelector('.r93-fh .r93-t12l.r93-fm.r93-ell') || document.querySelector('.r93-fh .r93-t12l') || document.querySelector('.r93-t12l.r93-fm');
  out.meta = meta ? { cls: meta.className, color: cs(meta).color, fs: cs(meta).fontSize, txt: (meta.textContent || '').slice(0, 20) } : null;

  /* ⑦ asst 底边线 */
  var asst = document.querySelector('.r93-asst');
  out.asst = asst ? { border: cs(asst).borderBottomColor, box: R(asst) } : null;

  /* ⑧ drow */
  var drow = document.querySelector('.r93-drow');
  var dname = document.querySelector('.r93-drow .r93-dname');
  var dmore = document.querySelector('.r93-drow .r93-dmore');
  out.drow = drow ? {
    box: R(drow), pad: cs(drow).padding, gap: cs(drow).gap,
    nameBox: R(dname), moreBox: R(dmore),
    n: document.querySelectorAll('.r93-drow').length
  } : null;

  /* ⑨ dhead */
  var dhead = document.querySelector('.r93-dhead');
  var dh1ic = document.querySelector('.r93-dhead .r93-dh1 > .r93-iblk');
  out.dhead = dhead ? { box: R(dhead), pad: cs(dhead).padding, icBox: R(dh1ic), bg: cs(dhead).backgroundColor } : null;

  /* ⑩ 滚动到底部 */
  var tb = document.querySelector('.r93-tobottom');
  out.tobottom = tb ? {
    box: R(tb), bg: cs(tb).backgroundColor, bf: cs(tb).backdropFilter || cs(tb).webkitBackdropFilter,
    bd: cs(tb).borderColor, radius: cs(tb).borderRadius
  } : null;

  /* ③ 折叠态分布 */
  var folds = document.querySelectorAll('.r93-fold');
  var dist = { '1': 0, '0': 0 };
  for (var m = 0; m < folds.length; m++) { dist[folds[m].getAttribute('data-open')] = (dist[folds[m].getAttribute('data-open')] || 0) + 1; }
  out.folds = { n: folds.length, dist: dist };
  var fb = document.querySelector('.r93-fold > .r93-fb');
  out.fb = fb ? { anim: cs(fb).animationName, dur: cs(fb).animationDuration, display: cs(fb).display, mt: cs(fb).marginTop, maxH: cs(fb).maxHeight, ovf: cs(fb).overflow } : null;

  return JSON.stringify(out);
})()

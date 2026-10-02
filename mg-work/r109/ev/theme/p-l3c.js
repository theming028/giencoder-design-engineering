(async () => {
  /* r109 第三拍 ①② 收尾读数：
     · ① 提交这条批注（就地 update，不新增锚点）→ 交回**锚点中心**（编排脚本要用它发真鼠标点击）
     · ② `.r93-card` 的两端对齐：左边缘 == 父级内容左、右边缘 == 父级内容右、margin-left 0 */
  const W = ms => new Promise(r => setTimeout(r, ms));
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const cs = e => getComputedStyle(e);
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const R = n => +n.toFixed(2);
  const out = {};

  /* ---- ① 提交 ---- */
  var ta = q('.td-elnote-input');
  out.beforeCommit = { anchorCount: qa('.td-anchor').length };
  var TEXT = '第三拍①验证：在哪里点击，就在哪里落锚点、气泡也钉在那个点上。';
  ta.value = TEXT;
  ta.dispatchEvent(new Event('input', { bubbles: true }));
  await W(280);
  out.okTextBeforeCommit = q('.td-elnote-ok').textContent.trim();
  q('.td-elnote-ok').click();
  await W(520);
  var a = q('.td-anchor');
  out.noteText = TEXT;
  out.afterCommit = {
    anchorCount: qa('.td-anchor').length,
    elnoteHidden: q('.td-elnote').hasAttribute('hidden'),
    styleLeft: a.style.left, styleTop: a.style.top
  };
  out.anchorCenter = { x: Math.round(B(a).l + B(a).w / 2), y: Math.round(B(a).t + B(a).h / 2) };

  /* ---- ② 卡片两端对齐 ---- */
  var card = q('.r93-card');
  if (card) {
    var p = card.parentElement, pc = cs(p), cb = B(card), pb = B(p);
    var pl = parseFloat(pc.paddingLeft) || 0, pr = parseFloat(pc.paddingRight) || 0;
    var pbw = parseFloat(pc.borderLeftWidth) || 0, pbrw = parseFloat(pc.borderRightWidth) || 0;
    out.card = {
      cls: card.className,
      box: cb,
      parentBox: pb,
      parentCls: p.className,
      parentPad: [pl, pr],
      marginLeft: cs(card).marginLeft,
      marginRight: cs(card).marginRight,
      width: cs(card).width,
      /* 左边缘 − 父内容左 ; 父内容右 − 右边缘  ⇒ 两个都应 ≈ 0 */
      dLeft: R(cb.l - (pb.l + pbw + pl)),
      dRight: R((pb.l + pb.w - pbrw - pr) - (cb.l + cb.w)),
      isEdge: card.className.indexOf('r93-card--edge') >= 0
    };
    /* 同族抽查：所有 r93-card 的 dLeft 分布（防「只改了一处」） */
    out.cardsAll = qa('.r93-card').map(function (e) {
      var b = B(e), pp = e.parentElement, pcs = cs(pp), ppb = B(pp);
      var l = parseFloat(pcs.paddingLeft) || 0;
      return { cls: e.className, dLeft: R(b.l - (ppb.l + (parseFloat(pcs.borderLeftWidth) || 0) + l)),
               ml: cs(e).marginLeft };
    });
  } else { out.card = null; }
  return JSON.stringify(out);
})()

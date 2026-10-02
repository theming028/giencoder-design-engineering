(async () => {
  const W = ms => new Promise(r => setTimeout(r, ms));
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const out = {};
  var a = q('.td-anchor');
  out.before = { anchorCount: qa('.td-anchor').length, anchorBox: B(a),
                 left: a.style.left, top: a.style.top };
  /* 编辑态 ⇒ 改文案再提交，应当**update 同一条**（锚点数不增、位置不动） */
  var ta = q('.td-elnote-input');
  ta.value = '锚点可拖动验证（已编辑）：同一枚锚点，改文案后仍是这一条。';
  ta.dispatchEvent(new Event('input', { bubbles: true }));
  await W(300);
  q('.td-elnote-ok').click();
  await W(500);
  out.after = { anchorCount: qa('.td-anchor').length, anchorBox: B(a),
                left: a.style.left, top: a.style.top,
                elnoteHidden: q('.td-elnote').hasAttribute('hidden') };
  /* 再点开一次，读回文案 —— 应当是「已编辑」那版 */
  a.click();
  await W(400);
  out.reopen = { elnoteHidden: q('.td-elnote').hasAttribute('hidden'),
                 taValue: q('.td-elnote-input').value,
                 pin: q('.td-elnote-pin').textContent.trim() };
  return JSON.stringify(out);
})()

(async () => {
  const W = ms => new Promise(r => setTimeout(r, ms));
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const cs = e => getComputedStyle(e);
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const R = n => +n.toFixed(2);
  const out = {};
  // 幂等布景：开模块 → 进标注态 → 开气泡
  var om = q('[data-td-open-mod="browser"]');
  if (om) om.click();
  await W(800);
  var brw = q('.td-brw');
  if (!brw.classList.contains('is-annotating')) { q('.td-url-annot').click(); await W(300); }
  var els = qa('.td-page [data-td-el]');
  var target = els.filter(e => e.className.indexOf('td-page-card') >= 0)[0] || els[0];
  target.click();
  await W(300);
  // 输入稿2 的示例文字（邵先生：「就是输入框的内容示例」）
  var ta = q('.td-elnote-input');
  ta.value = '正常输入文字时，卡片右下角是回车按钮，按下回车键即可添加此条注释。';
  ta.dispatchEvent(new Event('input', { bubbles: true }));
  await W(300);
  var card = q('.td-elnote-card'), foot = q('.td-elnote-foot'), hint = q('.td-elnote-hint');
  var cancel = q('.td-elnote-cancel'), ok = q('.td-elnote-ok');
  out.card = { box: B(card), h: cs(card).height, dir: cs(card).flexDirection,
               hasText: card.classList.contains('has-text'), maxh: cs(card).maxHeight };
  out.ta = { box: B(ta), lh: cs(ta).lineHeight, sh: ta.scrollHeight,
             inlineH: ta.style.height, color: cs(ta).color };
  out.taDx = R(B(ta).l - B(card).l); out.taDy = R(B(ta).t - B(card).t);
  out.foot = { box: B(foot) };
  out.footDx = R(B(foot).l - B(card).l); out.footDy = R(B(foot).t - B(card).t);
  out.hint = { box: B(hint), txt: hint.textContent, color: cs(hint).color,
               fs: cs(hint).fontSize, lh: cs(hint).lineHeight,
               emColor: cs(q('.td-elnote-hint em')).color };
  out.hintDx = R(B(hint).l - B(card).l);
  out.cancel = { box: B(cancel), txt: cancel.textContent.trim(), bg: cs(cancel).backgroundColor,
                 color: cs(cancel).color, fs: cs(cancel).fontSize, bc: cs(cancel).borderTopColor,
                 br: cs(cancel).borderRadius, pad: cs(cancel).paddingLeft, sh: cs(cancel).boxShadow };
  out.cancelDx = R(B(cancel).l - B(card).l);
  out.ok = { box: B(ok), txt: ok.textContent.trim(), disabled: ok.disabled,
             bg: cs(ok).backgroundColor, color: cs(ok).color, fs: cs(ok).fontSize,
             br: cs(ok).borderRadius, sh: cs(ok).boxShadow };
  out.okDx = R(B(ok).l - B(card).l);
  out.gapBtns = R(B(ok).l - (B(cancel).l + B(cancel).w));
  out.rightInset = R(B(card).l + B(card).w - (B(ok).l + B(ok).w));
  out.hintMidY = R(B(hint).t + B(hint).h / 2 - B(foot).t);
  out.noteBox = B(q('.td-elnote'));
  return JSON.stringify(out);
})()

(async () => {
  const W = ms => new Promise(r => setTimeout(r, ms));
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const cs = e => getComputedStyle(e);
  const B = e => { const r = e.getBoundingClientRect();
    return { l: +r.left.toFixed(2), t: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
  const R = n => +n.toFixed(2);
  const out = {};
  document.documentElement.style.setProperty('--ui-fs', '18');
  await W(200);
  out.ratio = cs(document.documentElement).getPropertyValue('--ui-fs-ratio').trim();
  var om = q('[data-td-open-mod="browser"]');
  if (om) om.click();
  await W(800);
  var brw = q('.td-brw');
  if (!brw.classList.contains('is-annotating')) { q('.td-url-annot').click(); await W(300); }
  var els = qa('.td-page [data-td-el]');
  var target = els.filter(e => e.className.indexOf('td-page-card') >= 0)[0] || els[0];
  target.click();
  await W(300);
  var card = q('.td-elnote-card'), pin = q('.td-elnote-pin'), ta = q('.td-elnote-input');
  out.empty = { note: B(q('.td-elnote')), card: B(card), pin: B(pin), ta: B(ta),
                ok: B(q('.td-elnote-ok')), lh: cs(ta).lineHeight, fs: cs(ta).fontSize };
  ta.value = '正常输入文字时，卡片右下角是回车按钮，按下回车键即可添加此条注释。';
  ta.dispatchEvent(new Event('input', { bubbles: true }));
  await W(300);
  out.typing = { note: B(q('.td-elnote')), card: B(card), ta: B(ta), foot: B(q('.td-elnote-foot')),
                 ok: B(q('.td-elnote-ok')), hint: B(q('.td-elnote-hint')) };
  // 长文本压顶：验证 200px 上限 + 输入区自滚
  ta.value = new Array(14).join('一二三四五六七八九十一二三四五六七八九十');
  ta.dispatchEvent(new Event('input', { bubbles: true }));
  await W(300);
  out.capped = { note: B(q('.td-elnote')), card: B(card), ta: B(ta),
                 taScrollH: ta.scrollHeight, taClientH: ta.clientHeight,
                 taCanScroll: ta.scrollHeight > ta.clientHeight + 1,
                 maxh: cs(card).maxHeight, cardOverflow: cs(card).overflow,
                 footVisible: B(q('.td-elnote-foot')).h };
  out.docOverflowX = document.documentElement.scrollWidth - window.innerWidth;
  return JSON.stringify(out);
})()

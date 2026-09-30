(() => {
  const H = document.querySelector('.r93-conv-host');
  const qa = s => Array.from((H || document).querySelectorAll(s));
  const r = el => { const b = el.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; };
  const cs = el => el ? getComputedStyle(el) : null;
  const R = {};

  // ④ 折叠箭头：槽 / svg / 标题左缘
  R.cv = qa('.r93-cv').slice(0, 3).map(el => {
    const sv = el.querySelector('svg');
    const head = el.parentNode;
    const ft = head ? head.querySelector('.r93-ft') : null;
    return { slot: r(el), slotW: cs(el).width, svgW: sv ? cs(sv).width : null,
             svgRect: sv ? r(sv) : null, ftX: ft ? Math.round(ft.getBoundingClientRect().left) : null };
  });

  // ② ⑨ .r93-t12l 全量（字号 / 颜色 / 类名）
  R.t12l = qa('.r93-t12l').map(el => ({ t: (el.textContent || '').trim().slice(0, 16),
      fs: cs(el).fontSize, color: cs(el).color, cls: el.className }));
  R.fm = qa('.r93-fm').map(el => ({ t: (el.textContent || '').trim().slice(0, 16), fs: cs(el).fontSize, color: cs(el).color }));

  // ③ 图标按钮（静态）
  R.ib = qa('.r93-ib').slice(0, 3).map(el => ({ box: r(el), bg: cs(el).backgroundColor, sh: cs(el).boxShadow }));

  // ⑤ 绿勾
  R.okc = qa('.r93-okc').map(el => ({ box: r(el), ctx: (el.parentNode.textContent || '').trim().slice(0, 18) }));

  // ⑧ 旋转中的图标
  R.spin = qa('.r93-spin').map(el => ({ box: r(el), anim: cs(el).animationName, dur: cs(el).animationDuration,
      state: cs(el).animationPlayState, cls: el.className }));

  // ⑩ 状态条投影
  const sb = qa('.r93-sb')[0];
  R.sb = sb ? { box: r(sb), sh: cs(sb).boxShadow, bd: cs(sb).borderColor } : null;

  // ⑥ 衔接处渐隐层（.r93-tbsticky::after）
  const tbs = qa('.r93-tbsticky')[0];
  if (tbs) {
    const a = getComputedStyle(tbs, '::after');
    R.fade = { tbsBox: r(tbs), content: a.content, pos: a.position, h: a.height, bottom: a.bottom,
               z: a.zIndex, bg: a.backgroundImage.slice(0, 72), left: a.left, right: a.right };
    const pill = tbs.querySelector('.r93-tobottom');
    R.fade.pillOn = pill ? pill.classList.contains('is-on') : null;
    R.fade.scroll = (function () { const s = qa('.r93-scroll')[0]; return s ? [r(s), s.scrollTop, s.scrollHeight, s.clientHeight] : null; })();
  }

  // ⑦ 产物卡
  R.art = qa('.r93-artcard').map(el => ({ box: r(el), name: el.getAttribute('data-r93-artname') }));

  // ⑪ 骨架屏（此时应已移除）
  R.sk = { count: document.querySelectorAll('.r93-sk').length };

  // 宿主 / pane
  const pane = qa('.r93-pane')[0];
  R.pane = pane ? { pos: cs(pane).position, box: r(pane) } : null;
  return JSON.stringify(R);
})();

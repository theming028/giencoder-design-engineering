// r78 验收探针
// 用法：
//   __MODE='enum'  → 逐点枚举「是否触发涟漪」，并报告该点命中的真实元素
//   __MODE='fire'  → 在 (__CX, __CY) 触发涟漪并暂停到 __T 毫秒
// 关键：必须用 document.elementFromPoint 取真实命中元素再 dispatch，
//       否则直接 dispatch 在 main 上会让 e.target = main ⇒ 排除判定被绕过。
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const host = document.querySelector('main.dot-bg');
  const clr = () => host.querySelectorAll('.r74-ripple').forEach(e => e.remove());

  if (window.__MODE === 'enum') {
    const hr = host.getBoundingClientRect();
    const pts = window.__PTS;
    const rows = [];
    for (const [cx, cy] of pts) {
      clr();
      await wait(10);
      const hit = document.elementFromPoint(cx, cy) || host;
      hit.dispatchEvent(new PointerEvent('pointerdown', {
        clientX: cx, clientY: cy, bubbles: true, cancelable: true, pointerId: 1,
      }));
      await wait(25);
      const n = host.querySelectorAll('.r74-ripple').length;
      rows.push({
        pt: [cx, cy],
        hit: hit.tagName + '.' + String(hit.className).slice(0, 46),
        inContainer: !!hit.closest('.flex.flex-1.flex-col.items-center.justify-center.px-6'),
        ripple: n,
      });
      clr();
      await wait(10);
    }
    return JSON.stringify({
      hostRect: [Math.round(hr.left), Math.round(hr.top), Math.round(hr.right), Math.round(hr.bottom)],
      rows,
    });
  }

  if (window.__MODE === 'fire') {
    clr();
    await wait(10);
    const cx = window.__CX, cy = window.__CY;
    const hit = document.elementFromPoint(cx, cy) || host;
    hit.dispatchEvent(new PointerEvent('pointerdown', {
      clientX: cx, clientY: cy, bubbles: true, cancelable: true, pointerId: 1,
    }));
    await wait(20);
    const el = host.querySelector('.r74-ripple');
    if (!el) return JSON.stringify({ err: 'NO RIPPLE', hit: hit.tagName });
    el.getAnimations().forEach(a => { a.pause(); a.currentTime = window.__T || 160; });
    const cs = getComputedStyle(el);
    return JSON.stringify({
      hit: hit.tagName + '.' + String(hit.className).slice(0, 40),
      click: [cx, cy],
      zIndex: cs.zIndex,
      bgImage: cs.backgroundImage.slice(0, 88),
      bgSize: cs.backgroundSize,
      op: cs.opacity,
    });
  }
  return 'BAD MODE';
})()

// r79 验收探针 —— 涟漪触发范围（版权带排除）+ 点阵 16px 复核
// 用法：
//   __MODE='struct' → 报告 main.dot-bg 的子块构成（证明「只剩 2 块」）
//   __MODE='enum'   → 对 window.__PTS 逐点复刻真实 pointerdown，报告是否起涟漪
//   __MODE='grid'   → 全视口网格扫描（步长 __STEP，默认 120），报告涟漪总数
//   __MODE='size'   → 手工插入一个 .r74-ripple，读它的 computed backgroundSize（核 #4 点阵 16px）
// ★ 必须用 document.elementFromPoint 取真实命中元素再 dispatch：
//   直接 dispatch 在 main 上会让 e.target = main ⇒ 排除判定链被绕过 ⇒ 测试假阳性。
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const host = document.querySelector('main.dot-bg');
  if (!host) return JSON.stringify({ err: 'NO main.dot-bg' });
  const all = () => document.querySelectorAll('.r74-ripple');
  const clr = () => all().forEach(e => e.remove());

  if (window.__MODE === 'struct') {
    const hr = host.getBoundingClientRect();
    const kids = [...host.children].map(el => {
      const r = el.getBoundingClientRect();
      return {
        tag: el.tagName,
        cls: String(el.className).slice(0, 72),
        rect: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)],
        isContent: !!el.closest('.flex.flex-1.flex-col.items-center.justify-center.px-6'),
        isCopyright: el.matches('div[class*="pb-6"][class*="text-center"]'),
      };
    });
    return JSON.stringify({
      hostRect: [Math.round(hr.left), Math.round(hr.top), Math.round(hr.width), Math.round(hr.height)],
      childCount: host.children.length,
      kids,
    });
  }

  if (window.__MODE === 'enum' || window.__MODE === 'grid') {
    let pts = window.__PTS;
    if (window.__MODE === 'grid') {
      const s = window.__STEP || 120;
      pts = [];
      for (let y = 5; y < window.innerHeight; y += s)
        for (let x = 5; x < window.innerWidth; x += s) pts.push([x, y]);
    }
    const rows = [];
    let fired = 0;
    for (const [cx, cy] of pts) {
      clr();
      await wait(6);
      const hit = document.elementFromPoint(cx, cy);
      if (!hit) { rows.push({ pt: [cx, cy], hit: null, ripple: 0, note: 'no element' }); continue; }
      hit.dispatchEvent(new PointerEvent('pointerdown', {
        clientX: cx, clientY: cy, bubbles: true, cancelable: true, pointerId: 1,
      }));
      await wait(18);
      const n = all().length;
      if (n) fired++;
      rows.push({
        pt: [cx, cy],
        hit: hit.tagName + '.' + String(hit.className).slice(0, 44),
        inContent: !!hit.closest('.flex.flex-1.flex-col.items-center.justify-center.px-6'),
        inCopyright: !!hit.closest('div[class*="pb-6"][class*="text-center"]'),
        inMain: !!hit.closest('main.dot-bg'),
        ripple: n,
      });
      clr();
      await wait(6);
    }
    return JSON.stringify({ mode: window.__MODE, n: pts.length, fired, rows });
  }

  if (window.__MODE === 'size') {
    clr();
    await wait(10);
    const el = document.createElement('span');
    el.className = 'r74-ripple';
    el.setAttribute('aria-hidden', 'true');
    el.style.setProperty('--r74-rip-x', '50%');
    el.style.setProperty('--r74-rip-y', '50%');
    el.style.setProperty('--r74-rip-cap', '360px');
    host.insertBefore(el, host.firstChild);
    await wait(30);
    const cs = getComputedStyle(el);
    const base = getComputedStyle(document.querySelector('.dot-bg'));
    const out = {
      ripple_bgSize: cs.backgroundSize,
      ripple_bgImage: cs.backgroundImage.slice(0, 90),
      ripple_zIndex: cs.zIndex,
      ripple_animation: cs.animationDuration,
      dotbg_bgSize: base.backgroundSize,
      dotbg_bgImage: base.backgroundImage.slice(0, 90),
    };
    el.remove();
    return JSON.stringify(out);
  }
  return 'BAD MODE';
})()

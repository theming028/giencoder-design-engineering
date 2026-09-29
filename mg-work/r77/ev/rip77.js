// r77 需求 5 取帧：验证「涟漪在对话框之下」+ 强度
// 用法：__MODE = 'card' | 'gap'，返回场景信息
(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const host = document.querySelector('main.dot-bg');
  const hr = host.getBoundingClientRect();
  // 清掉旧涟漪
  host.querySelectorAll('.r74-ripple').forEach(e => e.remove());

  const dlg = document.querySelector('main [class~="w-[800px]"]');
  const dr = dlg ? dlg.getBoundingClientRect() : null;

  // 目标点击点：card = 对话框正中心；gap = main 左下空白
  let cx, cy;
  if (window.__MODE === 'card') {
    cx = Math.round(dr.left + dr.width / 2);
    cy = Math.round(dr.top + dr.height / 2);
  } else {
    cx = Math.round(hr.left + 80);
    cy = Math.round(hr.bottom - 60);
  }

  host.dispatchEvent(new PointerEvent('pointerdown', {
    clientX: cx, clientY: cy, bubbles: true, cancelable: true, pointerId: 1,
  }));
  await wait(20);
  const el = host.querySelector('.r74-ripple');
  if (!el) return JSON.stringify({ err: 'NO RIPPLE' });
  el.getAnimations().forEach(a => { a.pause(); a.currentTime = window.__T || 160; });

  const er = el.getBoundingClientRect();
  return JSON.stringify({
    mode: window.__MODE, T: window.__T,
    click: [cx, cy],
    hostRect: [Math.round(hr.left), Math.round(hr.top), Math.round(hr.right), Math.round(hr.bottom)],
    dlgRect: dr ? [Math.round(dr.left), Math.round(dr.top), Math.round(dr.right), Math.round(dr.bottom)] : null,
    rippleRect: [Math.round(er.left), Math.round(er.top), Math.round(er.right), Math.round(er.bottom)],
    zIndex: getComputedStyle(el).zIndex,
  });
})()

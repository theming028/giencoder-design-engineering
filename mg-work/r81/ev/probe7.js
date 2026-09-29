(() => {
  const R = el => { if (!el) return null; const r = el.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(','); };
  const CS = (el, keys) => { if (!el) return null; const c = getComputedStyle(el); const o = {}; keys.forEach(k => o[k] = c[k]); return o; };
  const hdr = document.querySelector('header');
  const left = hdr.children[0];
  const lights = left.children[0];
  const trig = document.querySelector('.r81-ws-trigger');
  const pop = document.querySelector('.r81-ws-pop');
  const panel = document.querySelector('.r81-ws-panel');
  const pill = trig.querySelector('.r81-ws-pill');
  const lr = lights.getBoundingClientRect(), tr = trig.getBoundingClientRect();

  const out = {
    file: location.pathname.split('/').pop(),
    headerRect: R(hdr),
    leftCls: left.className,
    leftRect: R(left),
    leftGap: getComputedStyle(left).gap,
    leftKids: [...left.children].map((el, i) => ({ i, tag: el.tagName, cls: (el.className || '').slice(0, 55), r: R(el) })),
    lightsRect: R(lights),
    // ★ 红绿灯右缘 → 触发器左缘 的净距（期望 20）
    gapLightsToTrig: Math.round(tr.left - lr.right),
    trigRect: R(trig),
    trigCls: trig.className,
    trigCS: CS(trig, ['backgroundColor', 'color', 'borderRadius', 'padding', 'marginLeft', 'height', 'gap']),
    logoRect: R(trig.querySelector('.r81-ws-logo')),
    logoCS: CS(trig.querySelector('.r81-ws-logo'), ['color', 'backgroundColor']),
    nameRect: R(trig.querySelector('.r81-ws-name')),
    pillRect: R(pill),
    // ★ 胶囊文字色（期望 rgb(255, 255, 255)）
    pillCS: CS(pill, ['color', 'backgroundColor', 'fontSize', 'lineHeight']),
    chevRect: R(trig.querySelector('.r81-ws-chev')),
    tabsRect: R(hdr.querySelector('[role="tablist"]')),
    rightRect: R(hdr.children[hdr.children.length - 1]),

    popHiddenClosed: pop.hidden,
    trigAriaClosed: trig.getAttribute('aria-expanded')
  };

  // 打开
  trig.click();
  const pr = pop.getBoundingClientRect();
  out.opened = {
    popHidden: pop.hidden,
    trigAria: trig.getAttribute('aria-expanded'),
    popInline: pop.getAttribute('style'),
    popRect: R(pop),
    panelRect: R(panel),
    // ★ 浮窗左缘 - 触发器左缘（期望 0，左对齐）；浮窗上缘 - 触发器下缘（期望 4）
    popVsTrigLeft: Math.round(pr.left - tr.left),
    popVsTrigTop: Math.round(pr.top - tr.bottom),
    itemCount: document.querySelectorAll('.r81-ws-item').length,
    dividerTitle: (panel.querySelector('.r81-ws-divider span') || {}).textContent,
    searchPh: (panel.querySelector('input') || {}).placeholder,
    selCount: document.querySelectorAll('.r81-ws-item[aria-selected="true"]').length
  };
  out.ran = window.__r81ws === 1;
  return JSON.stringify(out, null, 1);
})()

(async () => {
  const q = s => document.querySelector(s);
  const trig = q('.r81-ws-trigger');
  const pop = q('.r81-ws-pop');
  const input = q('.r81-ws-input');
  const list = q('.r81-ws-list');
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const names = () => [...list.querySelectorAll('.r81-ws-item')].map(b => b.querySelector('.r81-ws-iname').textContent);
  const log = [];

  log.push('0 初始: pop.hidden=' + pop.hidden + ' 触发器=' + JSON.stringify(trig.querySelector('.r81-ws-name').textContent));

  trig.click(); await wait(30);
  log.push('1 点开后: hidden=' + pop.hidden + ' aria-expanded=' + trig.getAttribute('aria-expanded') + ' 条目=' + list.children.length);

  input.value = '禅道'; input.dispatchEvent(new Event('input', { bubbles: true })); await wait(30);
  log.push('2 搜索"禅道": ' + JSON.stringify(names()));

  input.value = 'zzz'; input.dispatchEvent(new Event('input', { bubbles: true })); await wait(30);
  log.push('3 搜索"zzz": 条目数=' + list.children.length);

  input.value = ''; input.dispatchEvent(new Event('input', { bubbles: true })); await wait(30);
  log.push('4 清空: 条目数=' + list.children.length);

  list.querySelectorAll('.r81-ws-item')[2].click(); await wait(30);
  log.push('5 选第3条后: hidden=' + pop.hidden + ' 触发器名=' + JSON.stringify(trig.querySelector('.r81-ws-name').textContent));

  trig.click(); await wait(30);
  const sel = [...list.querySelectorAll('.r81-ws-item')].filter(b => b.getAttribute('aria-selected') === 'true');
  log.push('6 重开: 选中数=' + sel.length + ' 选中名=' + JSON.stringify(sel[0] && sel[0].querySelector('.r81-ws-iname').textContent) + ' 选中项类名=' + JSON.stringify(sel[0] && sel[0].className));

  const before = pop.hidden;
  const outside = q('main') || document.body;
  outside.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, pointerId: 1 })); await wait(30);
  log.push('7 外部按下: ' + before + ' → ' + pop.hidden);

  trig.click(); await wait(30);
  const b2 = pop.hidden;
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true })); await wait(30);
  log.push('8 Esc: ' + b2 + ' → ' + pop.hidden);

  trig.click(); await wait(30);
  input.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, pointerId: 1 })); await wait(30);
  log.push('9 点浮窗内部: hidden=' + pop.hidden);

  const hdr = document.querySelector('header');
  const left = hdr.children[0];
  const lights = left.children[0];
  const r = trig.getBoundingClientRect(), lr = lights.getBoundingClientRect(), pr = pop.getBoundingClientRect();
  log.push('10 左簇顺序=' + [...left.children].map(el => el.tagName + ':' + (el.className || '(空)').toString().slice(0, 12)).join(' | '));
  log.push('11 红绿灯右缘=' + Math.round(lr.right) + ' 触发器左缘=' + Math.round(r.left) + ' 净距=' + Math.round(r.left - lr.right) + 'px');
  log.push('12 浮窗左缘=' + Math.round(pr.left) + ' 触发器左缘=' + Math.round(r.left) + ' Δ=' + Math.round(pr.left - r.left) + '  浮窗上缘-触发器下缘=' + Math.round(pr.top - r.bottom));
  log.push('13 标记: window.__r81ws=' + window.__r81ws);

  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  return JSON.stringify(log, null, 1);
})()

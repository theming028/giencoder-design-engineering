(async () => {
  const q = s => document.querySelector(s);
  const trig = q('.r80-ws-trigger');
  const pop = q('.r80-ws-pop');
  const input = q('.r80-ws-input');
  const list = q('.r80-ws-list');
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const names = () => [...list.querySelectorAll('.r80-ws-item')].map(b => b.querySelector('.r80-ws-iname').textContent);
  const log = [];

  // 1. 初始关闭
  log.push('0 初始: pop.hidden=' + pop.hidden + ' trigger=' + JSON.stringify(trig.querySelector('.r80-ws-name').textContent));

  // 2. 点触发器 → 打开
  trig.click();
  await wait(30);
  log.push('1 点开后: hidden=' + pop.hidden + ' aria-expanded=' + trig.getAttribute('aria-expanded') + ' 条目=' + list.children.length);

  // 3. 搜索过滤（"禅道" 命中「禅道空间」+「PAA-数字构建智能体/禅道」）
  input.value = '禅道';
  input.dispatchEvent(new Event('input', { bubbles: true }));
  await wait(30);
  log.push('2 搜索"禅道": ' + JSON.stringify(names()));

  // 4. 搜索无结果
  input.value = 'zzz';
  input.dispatchEvent(new Event('input', { bubbles: true }));
  await wait(30);
  log.push('3 搜索"zzz": 条目数=' + list.children.length);

  // 5. 清空 → 恢复 7 条
  input.value = '';
  input.dispatchEvent(new Event('input', { bubbles: true }));
  await wait(30);
  log.push('4 清空: 条目数=' + list.children.length);

  // 6. 点第 3 条（考试空间）→ 选中 + 关闭 + 触发器名称同步
  list.querySelectorAll('.r80-ws-item')[2].click();
  await wait(30);
  log.push('5 选第3条后: hidden=' + pop.hidden + ' 触发器名=' + JSON.stringify(trig.querySelector('.r80-ws-name').textContent));

  // 7. 重开 → 选中态落在第 3 条
  trig.click();
  await wait(30);
  const sel = [...list.querySelectorAll('.r80-ws-item')].filter(b => b.getAttribute('aria-selected') === 'true');
  log.push('6 重开: 选中数=' + sel.length + ' 选中名=' + JSON.stringify(sel[0] && sel[0].querySelector('.r80-ws-iname').textContent) + ' 选中项 hover 类=' + JSON.stringify(sel[0] && sel[0].className));

  // 8. 外部 pointerdown → 关闭
  const before = pop.hidden;
  const outside = q('main') || document.body;
  outside.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, pointerId: 1 }));
  await wait(30);
  log.push('7 外部按下: ' + before + ' → ' + pop.hidden);

  // 9. 重开 → Esc → 关闭
  trig.click();
  await wait(30);
  const b2 = pop.hidden;
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  await wait(30);
  log.push('8 Esc: ' + b2 + ' → ' + pop.hidden);

  // 10. 打开状态下点内部不关（点搜索框）
  trig.click();
  await wait(30);
  input.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, pointerId: 1 }));
  await wait(30);
  log.push('9 点浮窗内部: hidden=' + pop.hidden);

  // 11. 触发器位置（右上角）
  const r = trig.getBoundingClientRect();
  log.push('10 触发器: right=' + Math.round(r.right) + ' top=' + Math.round(r.top) + ' w=' + Math.round(r.width) + ' 视口宽=' + innerWidth);
  log.push('11 标记: window.__r80ws=' + window.__r80ws);

  // 收尾：关掉
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  return JSON.stringify(log, null, 1);
})()

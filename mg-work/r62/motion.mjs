#!/usr/bin/env node
/**
 * r62 无障碍回归：用 CDP Emulation.setEmulatedMedia 强制 prefers-reduced-motion: reduce，
 * 验证流光确实被关掉、标题退回普通深色（否则「偏好减弱动效」就是空话）。
 *
 * 用法：node motion.mjs "<cdp-ws-url>" "pages/kanban.html"
 */
const [, , wsUrl, urlSuffix] = process.argv;
if (!wsUrl || !urlSuffix) { console.error('usage: node motion.mjs <cdp-ws-url> <url-suffix>'); process.exit(2); }

// 普通字符串拼接，勿改模板串
const READ = [
  "(function(){",
  "  var t=document.querySelector('.kb-card:has(.kb-running) .kb-card-title');",
  "  if(!t) return 'NO TITLE';",
  "  var cs=getComputedStyle(t);",
  "  return JSON.stringify({",
  "    reduceMatches: matchMedia('(prefers-reduced-motion: reduce)').matches,",
  "    animationName: cs.animationName,",
  "    backgroundImage: cs.backgroundImage.slice(0,60),",
  "    color: cs.color,",
  "    fill: cs.webkitTextFillColor",
  "  });",
  "})()"
].join('\n');

const ws = new WebSocket(wsUrl);
let id = 0; const pend = new Map();
function send(method, params, sessionId) {
  return new Promise(res => { const i = ++id; pend.set(i, res);
    ws.send(JSON.stringify({ id: i, method, params, sessionId })); });
}
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
ws.onerror = e => { console.error('WS ERROR', e.message); process.exit(1); };

ws.onopen = async () => {
  const t = await send('Target.getTargets', {});
  const pages = ((t.result && t.result.targetInfos) || []).filter(p => p.type === 'page');
  const pg = pages.find(p => p.url.endsWith(urlSuffix));
  if (!pg) { console.error('NO TARGET ending with', urlSuffix); process.exit(1); }
  const a = await send('Target.attachToTarget', { targetId: pg.targetId, flatten: true });
  const sid = a.result && a.result.sessionId;
  await send('Runtime.enable', {}, sid);

  const before = await send('Runtime.evaluate', { expression: READ, returnByValue: true }, sid);
  console.log('【默认】', before.result.result.value);

  await send('Emulation.setEmulatedMedia', {
    features: [{ name: 'prefers-reduced-motion', value: 'reduce' }]
  }, sid);
  await new Promise(r => setTimeout(r, 300));

  const after = await send('Runtime.evaluate', { expression: READ, returnByValue: true }, sid);
  console.log('【reduce】', after.result.result.value);

  // 复位，避免污染后续
  await send('Emulation.setEmulatedMedia', { features: [] }, sid);
  await send('Target.detachFromTarget', { sessionId: sid });
  ws.close();
};

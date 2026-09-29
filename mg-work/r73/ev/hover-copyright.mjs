#!/usr/bin/env node
/**
 * r73 · 需求 4 专用：CDP 真实鼠标悬停到 base.html 版权区，同一 session 回读 computed 颜色。
 *
 * 派生自 skill `css-pseudo-state-evidence`/scripts/hover.mjs，仅把 READ 段的目标
 * 换成版权区容器（main 下同时含 pb-6 与 text-center 的 div）。
 * ⚠️ 保持「普通字符串 + 拼接」写法，勿改成模板字符串（\s / \b 会被吞）。
 *
 * 用法：
 *   node hover-copyright.mjs "<cdp-browser-ws-url>" "<url 后缀>" <x> <y>
 */
const [, , wsUrl, urlSuffix, xs, ys] = process.argv;
if (!wsUrl || !urlSuffix) {
  console.error('usage: node hover-copyright.mjs <cdp-browser-ws-url> <url-suffix> <x> <y>');
  process.exit(2);
}
const x = Number(xs), y = Number(ys);

const READ = [
  "(function(){",
  '  var el=document.querySelector("main div[class*=pb-6][class*=text-center]");',
  "  var o={};",
  "  if(el){",
  "    o.cls=String(el.className).slice(0,64);",
  "    o.color=getComputedStyle(el).color;",
  "    o.isHover=el.matches(':hover');",
  "    var p=el.querySelector('p');",
  "    o.pColor=p?getComputedStyle(p).color:null;",
  "  } else { o.err='NOT_FOUND'; }",
  "  var hit=[].slice.call(document.querySelectorAll('*')).filter(function(e){",
  "    try{ return e.matches(':hover'); }catch(err){ return false; } });",
  "  o.deepest=hit.length?hit[hit.length-1].tagName+'.'+String(hit[hit.length-1].className).slice(0,44):'-';",
  "  return JSON.stringify(o);",
  "})()"
].join('\n');

const ws = new WebSocket(wsUrl);
let id = 0; const pend = new Map();
function send(method, params, sessionId) {
  return new Promise(res => { const i = ++id; pend.set(i, res);
    ws.send(JSON.stringify({ id: i, method, params, sessionId })); });
}
ws.onmessage = e => {
  const m = JSON.parse(e.data);
  if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); }
};
ws.onerror = e => { console.error('WS ERROR', e.message); process.exit(1); };

ws.onopen = async () => {
  const t = await send('Target.getTargets', {});
  const pages = ((t.result && t.result.targetInfos) || []).filter(p => p.type === 'page');
  const pg = pages.find(p => p.url.endsWith(urlSuffix));
  if (!pg) {
    console.error('NO TARGET ending with', urlSuffix);
    console.error('  candidates:', pages.map(p => p.url.slice(0, 90)).join('\n               '));
    process.exit(1);
  }
  const a = await send('Target.attachToTarget', { targetId: pg.targetId, flatten: true });
  const sid = a.result && a.result.sessionId;
  if (!sid) { console.error('NO SESSION'); process.exit(1); }

  await send('Page.bringToFront', {}, sid);
  await send('Runtime.enable', {}, sid);

  // 鼠标先移到别处，确保读到的是「未悬停」基态
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: 20, y: 20, buttons: 0 }, sid);
  await new Promise(r => setTimeout(r, 220));
  const r0 = await send('Runtime.evaluate', { expression: READ, returnByValue: true }, sid);
  console.log('未悬停 ->', (r0.result && r0.result.result && r0.result.result.value) || '?');

  // 真实鼠标移入目标点，发两次（第二次微移 2px）确保 :hover 稳定
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y, buttons: 0 }, sid);
  await new Promise(r => setTimeout(r, 150));
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y: y + 2, buttons: 0 }, sid);
  await new Promise(r => setTimeout(r, 300));

  const r = await send('Runtime.evaluate', { expression: READ, returnByValue: true }, sid);
  const v = r.result && r.result.result && r.result.result.value;
  console.log('悬停中 ->', v !== undefined ? v : JSON.stringify(r).slice(0, 400));

  await send('Target.detachFromTarget', { sessionId: sid });
  ws.close();
};

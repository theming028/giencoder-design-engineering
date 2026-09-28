#!/usr/bin/env node
/**
 * r63 取证：CDP 真实鼠标悬停到某张卡片上，回读该卡标题的字重与所属泳道。
 * 目的：证明「其它泳道 base 400 → hover 500」的既有行为未被 r63 破坏。
 *
 * 用法：node hover-card.mjs "<cdp-ws-url>" "pages/kanban.html" <x> <y> [outPng]
 *
 * ⚠️ 全文 JS 用普通字符串 + join 拼接，不要改成模板字符串。
 */
const [, , wsUrl, urlSuffix, xs, ys, outPng] = process.argv;
if (!wsUrl || !urlSuffix) {
  console.error('usage: node hover-card.mjs <cdp-ws-url> <url-suffix> <x> <y> [outPng]');
  process.exit(2);
}
const x = Number(xs), y = Number(ys);
import { writeFileSync } from 'node:fs';

const READ = [
  "(function(){",
  "  var hit=[].slice.call(document.querySelectorAll('*')).filter(function(e){",
  "    try{ return e.matches(':hover'); }catch(err){ return false; } });",
  "  function pick(sel){ for(var i=hit.length-1;i>=0;i--){",
  "    try{ if(hit[i].matches(sel)) return hit[i]; }catch(e){} } return null; }",
  "  var o={ mouseX:" + x + ", mouseY:" + y + " };",
  "  o.deepest = hit.length ? hit[hit.length-1].tagName+'.'+String(hit[hit.length-1].className).slice(0,40) : '-';",
  "  var card=pick('.kb-card');",
  "  if(!card){ o.err='没有 hover 到卡片'; return JSON.stringify(o); }",
  "  var col=card.closest('.kb-col');",
  "  o.col = col ? col.querySelector('.kb-col-name').textContent.trim()+' ('+col.className+')' : '-';",
  "  o.cardHovered = card.matches(':hover');",
  "  var t=card.querySelector('.kb-card-title');",
  "  o.title = t ? t.textContent.slice(0,16) : '-';",
  "  o.titleFontWeight = t ? getComputedStyle(t).fontWeight : '-';",
  "  o.titleBoxW = t ? Math.round(t.getBoundingClientRect().width) : '-';",
  "  o.running = !!card.querySelector('.kb-running');",
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

  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: 5, y: 5, buttons: 0 }, sid);
  await new Promise(r => setTimeout(r, 120));
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y, buttons: 0 }, sid);
  await new Promise(r => setTimeout(r, 150));
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y: y + 1, buttons: 0 }, sid);
  await new Promise(r => setTimeout(r, 250));

  const r = await send('Runtime.evaluate', { expression: READ, returnByValue: true }, sid);
  const v = r.result && r.result.result && r.result.result.value;
  console.log(v !== undefined ? v : JSON.stringify(r).slice(0, 400));

  if (outPng) {
    const shot = await send('Page.captureScreenshot', { format: 'png' }, sid);
    const b64 = shot.result && shot.result.data;
    if (b64) { writeFileSync(outPng, Buffer.from(b64, 'base64')); console.log('SHOT ' + outPng); }
    else { console.log('SHOT FAILED ' + JSON.stringify(shot).slice(0, 200)); }
  }

  await send('Target.detachFromTarget', { sessionId: sid });
  ws.close();
};

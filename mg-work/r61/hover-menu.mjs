#!/usr/bin/env node
/**
 * r61 取证：CDP 真实鼠标悬停到「更多操作」菜单某一项，回读该项的
 * 背景色 / 文字色 / 图标色 / 图标框与 svg 尺寸 / 文字列起点偏移。
 *
 * 用法：node hover-menu.mjs "<cdp-ws-url>" "pages/task-detail.html" <x> <y> [outPng]
 *   给了 outPng 就在**同一次悬停中**抓帧落盘（鼠标移开后 :hover 会丢，必须同 session 抓）
 *
 * ⚠️ 全文 JS 用普通字符串 + join 拼接，**不要**改成模板字符串（\s / \d 会被吞成转义）。
 */
const [, , wsUrl, urlSuffix, xs, ys, outPng] = process.argv;
if (!wsUrl || !urlSuffix) {
  console.error('usage: node hover-menu.mjs <cdp-browser-ws-url> <url-suffix> <x> <y>');
  process.exit(2);
}
const x = Number(xs), y = Number(ys);
import { writeFileSync } from 'node:fs';

const READ = [
  "(function(){",
  "  var hit=[].slice.call(document.querySelectorAll('*')).filter(function(e){",
  "    try{ return e.matches(':hover'); }catch(err){ return false; } });",
  "  function pick(re){ for(var i=hit.length-1;i>=0;i--){",
  "    if(re.test(String(hit[i].className))) return hit[i]; } return null; }",
  "  var o={ scope:'task-detail', mouseX:" + x + ", mouseY:" + y + " };",
  "  o.deepest = hit.length ? hit[hit.length-1].tagName+'.'+String(hit[hit.length-1].className).slice(0,36) : '-';",
  "  var row=pick(/^giencoder-dropdown-item(\\s|$)/);",
  "  if(!row){ o.err='没有 hover 到菜单项'; return JSON.stringify(o); }",
  "  var cs=getComputedStyle(row);",
  "  o.rowCls=row.className;",
  "  o.rowTxt=row.textContent.trim();",
  "  o.rowBg=cs.backgroundColor;",
  "  o.rowColor=cs.color;",
  "  var lb=row.querySelector('.td-more-label'), ic=row.querySelector('.td-more-ico');",
  "  if(lb){",
  "    o.labelColor=getComputedStyle(lb).color;",
  "    var menu=document.querySelector('.td-more');",
  "    if(menu){ o.labelLeftOffset=Math.round(lb.getBoundingClientRect().left-menu.getBoundingClientRect().left); }",
  "  }",
  "  if(ic){",
  "    o.icoBox=Math.round(ic.getBoundingClientRect().width)+'x'+Math.round(ic.getBoundingClientRect().height);",
  "    o.icoColor=getComputedStyle(ic).color;",
  "    var sv=ic.querySelector('svg');",
  "    if(sv) o.svgSize=Math.round(sv.getBoundingClientRect().width)+'x'+Math.round(sv.getBoundingClientRect().height);",
  "  }",
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

  // 真实鼠标移动：发两次，第二次微移 2px，确保 mouseover/mouseenter 与 :hover 稳定生效
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y, buttons: 0 }, sid);
  await new Promise(r => setTimeout(r, 150));
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y: y + 2, buttons: 0 }, sid);
  await new Promise(r => setTimeout(r, 250));

  const r = await send('Runtime.evaluate', { expression: READ, returnByValue: true }, sid);
  const v = r.result && r.result.result && r.result.result.value;
  console.log(v !== undefined ? v : JSON.stringify(r).slice(0, 400));

  if (outPng) {
    const shot = await send('Page.captureScreenshot', { format: 'png' }, sid);
    const b64 = shot.result && shot.result.data;
    if (b64) {
      writeFileSync(outPng, Buffer.from(b64, 'base64'));
      console.log('SHOT ' + outPng);
    } else {
      console.log('SHOT FAILED ' + JSON.stringify(shot).slice(0, 200));
    }
  }

  await send('Target.detachFromTarget', { sessionId: sid });
  ws.close();
};

#!/usr/bin/env node
/**
 * r73 · 查某个元素「哪条规则给了 border-radius」—— 走 CDP CSS.getMatchedStylesForNode。
 *
 * 用途：订正「凭肉眼推断样式来源」的错误。页面是压缩 bundle，正则搜 CSS 经常定位不到
 * （多选择器逗号列表、:where/:is、简写、变量继承都会让朴素匹配落空）。
 *
 * 用法：
 *   node matcher.mjs "<cdp-browser-ws-url>" "pages/kanban.html" ".kb-btn-assign"
 */
const [, , wsUrl, urlSuffix, selector] = process.argv;
if (!wsUrl || !urlSuffix || !selector) {
  console.error('usage: node matcher.mjs <cdp-browser-ws-url> <url-suffix> <selector>');
  process.exit(2);
}

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

  await send('DOM.enable', {}, sid);
  await send('CSS.enable', {}, sid);
  const doc = await send('DOM.getDocument', { depth: 0 }, sid);
  const rootId = doc.result && doc.result.root && doc.result.root.nodeId;
  const q = await send('DOM.querySelector', { nodeId: rootId, selector }, sid);
  const nid = q.result && q.result.nodeId;
  if (!nid) { console.error('NO NODE for', selector); ws.close(); process.exit(1); }

  const ms = await send('CSS.getMatchedStylesForNode', { nodeId: nid }, sid);
  const R = ms.result || {};
  const out = [];

  function scan(rules, tag) {
    (rules || []).forEach(function (r) {
      const rule = r.rule || r;
      const props = (rule.style && rule.style.cssProperties) || [];
      props.forEach(function (p) {
        if (p.name && p.name.indexOf('radius') >= 0 && p.value !== '<invalid>') {
          out.push({
            src: tag,
            sel: String((rule.selectorList && rule.selectorList.text) || r.text || '').slice(0, 130),
            prop: p.name,
            val: p.value,
            imp: p.important ? '!' : '',
            disabled: p.disabled ? 'DISABLED' : '',
            origin: String(rule.origin || '')
          });
        }
      });
    });
  }
  scan(R.matchedCSSRules, 'matched');
  scan(R.inherited, 'inherited');
  scan(R.pseudoElements, 'pseudo');
  if (R.inlineStyle && R.inlineStyle.cssProperties) {
    R.inlineStyle.cssProperties.forEach(function (p) {
      if (p.name && p.name.indexOf('radius') >= 0) {
        out.push({ src: 'inline', sel: '(element style attr)', prop: p.name, val: p.value, imp: p.important ? '!' : '' });
      }
    });
  }

  console.log(JSON.stringify(out, null, 1));
  await send('Target.detachFromTarget', { sessionId: sid });
  ws.close();
};

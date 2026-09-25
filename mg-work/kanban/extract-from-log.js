// Extract root node HTML from mgmcp log (WS payloads that arrived after HTTP timeout).
const fs = require('fs');
const LOG = 'C:/Users/Administrator/.mgmcp/mgmcp.log';
const lines = fs.readFileSync(LOG, 'utf8').split(/\r?\n/);
let best = null;
for (const line of lines) {
  if (!line.includes('recv ws msg') || !line.includes('sendSelectionCode')) continue;
  const idx = line.indexOf('msg:');
  if (idx < 0) continue;
  let j;
  try { j = JSON.parse(line.slice(idx + 4)); } catch (e) { continue; }
  let data = j.data;
  if (typeof data === 'string') { try { data = JSON.parse(data); } catch (e) { continue; } }
  if (!data || data.type !== 'sendSelectionCode' || !data.code) continue;
  if (!data.code.includes('553:06620')) continue;
  best = { id: j.id, code: data.code, assets: data.assetManifest || [] };
}
if (!best) { console.log('NOT_FOUND'); process.exit(1); }
fs.writeFileSync('mg-work/kanban/root/board-code.html', best.code);
fs.writeFileSync('mg-work/kanban/root/board-assets.json', JSON.stringify(best.assets, null, 2));
console.log('EXTRACTED msgId=' + best.id + ' codeBytes=' + best.code.length + ' assets=' + best.assets.length);

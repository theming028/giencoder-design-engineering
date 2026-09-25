// Decode root board screenshot base64 from mgmcp log line.
const fs = require('fs');
const lines = fs.readFileSync('C:/Users/Administrator/.mgmcp/mgmcp.log', 'utf8').split(/\r?\n/);
let best = null;
for (const line of lines) {
  if (!line.includes('recv ws msg') || !line.includes('sendScreenshot')) continue;
  const idx = line.indexOf('msg:');
  if (idx < 0) continue;
  let j;
  try { j = JSON.parse(line.slice(idx + 4)); } catch (e) { continue; }
  let data = j.data;
  if (typeof data === 'string') { try { data = JSON.parse(data); } catch (e) { continue; } }
  if (!data || data.type !== 'sendScreenshot' || !data.success || !data.images) continue;
  const img = data.images.find((x) => x.nodeId === '553:06620' && x.success && x.base64);
  if (img) best = img;
}
if (!best) { console.log('NOT_FOUND'); process.exit(1); }
fs.writeFileSync('mg-work/kanban/root/board-design.png', Buffer.from(best.base64, 'base64'));
console.log('SAVED board-design.png bytes=' + Buffer.from(best.base64, 'base64').length);

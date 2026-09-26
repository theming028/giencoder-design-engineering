// 用 goto 链接读取 836:21409（frame 含看板+模态）
const http = require('http');
const fs = require('fs');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';
const OUT = 'E:/GienCoder/giencoder-design-engineering/mg-work/kanban/r11/';
const URL = 'https://mastergo.com/goto/WnxPLRdy?page_id=836:21408&layer_id=836:21409&file=193158744355579';

function call(tool, args, timeoutMs) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random()*1000),
      method: 'tools/call', params: { name: tool, arguments: args } });
    const req = http.request({ host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body) }, timeout: timeoutMs || 280000 }, (res) => {
      const chunks = [];
      res.on('data', d => chunks.push(d));
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString('utf8');
        const p = [];
        for (const l of raw.split(/\r?\n/)) if (l.startsWith('data:')) p.push(l.slice(5).trim());
        resolve(p.length ? p.join('\n') : raw);
      });
    });
    req.on('error', e => resolve('REQ_ERROR: ' + e.message));
    req.on('timeout', () => { req.destroy(); resolve('REQ_TIMEOUT'); });
    req.write(body); req.end();
  });
}

function extractText(resp) {
  try {
    const j = JSON.parse(resp);
    const c = j.result && j.result.content;
    if (Array.isArray(c)) return c.map(x => x.text || '').join('\n');
  } catch (e) {}
  return resp;
}

(async () => {
  const r = await call('get_selection_node', { projectDir: PROJECT_DIR, targetNodeId: URL });
  const t = extractText(r);
  fs.writeFileSync(OUT + 'frame-node.txt', t);
  console.log('LEN:', t.length);
  console.log(t.slice(0, 400).replace(/\n/g, ' '));
  console.log('DONE');
})();

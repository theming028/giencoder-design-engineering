// 重试 get_frontend_code 836:21409，加长超时；失败则改用 get_selection_node 再试
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';
const OUT_REL = 'mg-work/kanban/r11';

function call(tool, args, timeoutMs) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random()*1000),
      method: 'tools/call', params: { name: tool, arguments: args } });
    const req = http.request({ host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body) }, timeout: timeoutMs || 300000 }, (res) => {
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
  let r = await call('get_frontend_code', { projectDir: PROJECT_DIR, targetNodeId: '836:21409', frontendFramework: 'html', outDir: OUT_REL, fileName: 'modal.html' });
  let t = extractText(r);
  console.log('TRY1:', t.slice(0, 300));
  if (t.includes('timeout') || t.includes('超时') || t.includes('TIMEOUT')) {
    r = await call('get_selection_node', { projectDir: PROJECT_DIR, targetNodeId: '836:21409' });
    t = extractText(r);
    fs.writeFileSync('mg-work/kanban/r11/modal-node.txt', t);
    console.log('TRY2 len:', t.length, t.slice(0, 200));
  }
  console.log('DONE');
})();

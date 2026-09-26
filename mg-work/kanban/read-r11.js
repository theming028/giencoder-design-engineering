// 用 get_selection_node 读取 836:21409 (模态) 和 836:21408 (整页) 的 HTML + 图层信息
const http = require('http');
const fs = require('fs');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';

function call(tool, args) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random()*1000),
      method: 'tools/call', params: { name: tool, arguments: args } });
    const req = http.request({ host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body) }, timeout: 240000 }, (res) => {
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
  const modal = await call('get_selection_node', { projectDir: PROJECT_DIR, targetNodeId: '836:21409' });
  fs.writeFileSync('mg-work/kanban/r11/modal-node.txt', extractText(modal));
  console.log('MODAL len:', extractText(modal).length);
  const page = await call('get_selection_node', { projectDir: PROJECT_DIR, targetNodeId: '836:21408' });
  const pt = extractText(page);
  fs.writeFileSync('mg-work/kanban/r11/page-node.txt', pt);
  console.log('PAGE len:', pt.length, pt.slice(0, 200).replace(/\n/g, ' '));
  console.log('DONE');
})();

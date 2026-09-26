// r13: 读取当前 MasterGo 选中图层（无 targetNodeId 时=当前选中）
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';
const OUT = path.join(PROJECT_DIR, 'mg-work/kanban/r13/selection.json');
const NODE_ID = process.argv[2] || null;

function call(tool, args) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random() * 1000), method: 'tools/call', params: { name: tool, arguments: args } });
    const req = http.request({ host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'Content-Length': Buffer.byteLength(body) },
      timeout: 170000 }, (res) => {
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

(async () => {
  const args = { projectDir: PROJECT_DIR };
  if (NODE_ID) args.targetNodeId = NODE_ID;
  const r = await call('get_selection_node', args);
  fs.writeFileSync(OUT, r);
  console.log('bytes=' + r.length);
  console.log(r.slice(0, 1500));
})();

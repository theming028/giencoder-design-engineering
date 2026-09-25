// Export a single full MasterGo node (HTML + screenshot) via local Vibe MCP.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 20678;
const PROJECT_DIR = 'C:\\Users\\Administrator\\Documents\\Qoder\\2026-09-24\\0bfb1ccc\\giencoder-design-engineering';
const NODE_ID = process.argv[2] || '1333:18255';
const OUT_REL = process.argv[3] || 'mg-work/kanban/full';
const FILE = process.argv[4] || 'node.html';

function call(tool, args) {
  return new Promise((resolve) => {
    const body = JSON.stringify({
      jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random() * 1000),
      method: 'tools/call', params: { name: tool, arguments: args }
    });
    const req = http.request({
      host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body)
      }, timeout: 180000
    }, (res) => {
      const chunks = [];
      res.on('data', (d) => chunks.push(d));
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString('utf8');
        const payloads = [];
        for (const line of raw.split(/\r?\n/)) if (line.startsWith('data:')) payloads.push(line.slice(5).trim());
        resolve(payloads.length ? payloads.join('\n') : raw);
      });
    });
    req.on('error', (e) => resolve('REQ_ERROR: ' + e.message));
    req.on('timeout', () => { req.destroy(); resolve('REQ_TIMEOUT'); });
    req.write(body); req.end();
  });
}

(async () => {
  // 1. selection node metadata
  const sel = await call('get_selection_node', { projectDir: PROJECT_DIR });
  fs.writeFileSync(path.join(PROJECT_DIR, OUT_REL, '_selection.json'), sel);
  console.log('SELECTION bytes=' + sel.length);

  // 2. screenshot of the target node
  const shot = await call('get_screenshot', { projectDir: PROJECT_DIR, targetNodeId: NODE_ID, savePath: path.join(OUT_REL, 'design.png') });
  console.log('SCREENSHOT: ' + shot.slice(0, 300));

  // 3. full HTML export
  const resp = await call('get_frontend_code', { projectDir: PROJECT_DIR, targetNodeId: NODE_ID, frontendFramework: 'html', outDir: OUT_REL, fileName: FILE });
  console.log('HTML: ' + resp.slice(0, 400));
  console.log('DONE');
})();

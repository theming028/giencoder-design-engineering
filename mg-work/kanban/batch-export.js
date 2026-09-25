// Batch export remaining kanban selection nodes via local Vibe MCP.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 20678;
const PROJECT_DIR = 'C:\\Users\\Administrator\\Documents\\Qoder\\2026-09-24\\0bfb1ccc\\giencoder-design-engineering';

const NODES = [
  ['n03', '1333:18136'],
  ['n04', '1333:18151'],
  ['n05', '1333:18159'],
  ['n06', '1333:18163'],
  ['n07', '1333:18143'],
  ['n08', '622:09511'],
  ['n09', '769:09604'],
  ['n10', '1333:18135'],
  ['n11', '1333:18176'],
  ['n12', '836:15093'],
  ['n13', '1333:18171']
];

function call(args) {
  return new Promise((resolve) => {
    const body = JSON.stringify({
      jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random() * 1000),
      method: 'tools/call',
      params: { name: 'get_frontend_code', arguments: args }
    });
    const req = http.request({
      host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body)
      },
      timeout: 120000
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

function firstText(resp) {
  try {
    const j = JSON.parse(resp);
    const c = j.result && j.result.content;
    if (Array.isArray(c) && c[0] && c[0].text) return c[0].text.split('\n')[0];
    if (j.error) return 'ERROR: ' + j.error.message;
  } catch (e) {}
  return resp.slice(0, 120);
}

(async () => {
  for (const [dir, id] of NODES) {
    const outDir = 'mg-work/kanban/' + dir;
    const resp = await call({ projectDir: PROJECT_DIR, targetNodeId: id, frontendFramework: 'html', outDir, fileName: 'node.html' });
    const iconsDir = path.join(PROJECT_DIR, outDir, 'asset', 'icons');
    let icons = [];
    try { icons = fs.readdirSync(iconsDir); } catch (e) {}
    console.log(dir + ' (' + id + '): ' + firstText(resp) + ' | icons=' + icons.join(','));
  }
  console.log('DONE');
})();

// Fetch node HTML inline via get_selection_node (lighter than get_frontend_code).
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 20678;
const PROJECT_DIR = 'C:\\Users\\Administrator\\Documents\\Qoder\\2026-09-24\\0bfb1ccc\\giencoder-design-engineering';
const NODE_ID = process.argv[2];
const OUT = process.argv[3]; // relative file to save raw response

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
      }, timeout: 170000
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
  const args = { projectDir: PROJECT_DIR };
  if (NODE_ID) args.targetNodeId = NODE_ID;
  const resp = await call('get_selection_node', args);
  fs.writeFileSync(path.join(PROJECT_DIR, OUT), resp);
  console.log('saved ' + OUT + ' bytes=' + resp.length);
  console.log(resp.slice(0, 500));
})();

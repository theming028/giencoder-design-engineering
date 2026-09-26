// 拉取需求看板节点 (769:13709) DSL
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';
const NODE_ID = process.argv[2];
const OUT = process.argv[3];

function call(tool, args) {
  return new Promise((resolve) => {
    const body = JSON.stringify({
      jsonrpc: '2.0', id: Date.now(),
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
  fs.writeFileSync(path.join(__dirname, OUT), resp);
  console.log('saved ' + OUT + ' bytes=' + resp.length);
  console.log(resp.slice(0, 800));
})();

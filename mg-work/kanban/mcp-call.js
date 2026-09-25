// MasterGo local Vibe MCP caller. Usage: node mcp-call.js <toolName> <jsonArgsFile>
const http = require('http');
const fs = require('fs');

const PORT = 20678;
const toolName = process.argv[2];
const argsFile = process.argv[3];
const args = argsFile ? JSON.parse(fs.readFileSync(argsFile, 'utf8')) : {};

const body = JSON.stringify({
  jsonrpc: '2.0',
  id: Date.now(),
  method: 'tools/call',
  params: { name: toolName, arguments: args }
});

const req = http.request({
  host: '127.0.0.1',
  port: PORT,
  path: '/mcp',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/event-stream',
    'Content-Length': Buffer.byteLength(body)
  },
  timeout: 120000
}, (res) => {
  let chunks = [];
  res.on('data', (d) => chunks.push(d));
  res.on('end', () => {
    const raw = Buffer.concat(chunks).toString('utf8');
    // Parse SSE: lines starting with "data: "
    let payloads = [];
    for (const line of raw.split(/\r?\n/)) {
      if (line.startsWith('data:')) {
        payloads.push(line.slice(5).trim());
      }
    }
    const out = payloads.length ? payloads.join('\n') : raw;
    process.stdout.write(out);
  });
});
req.on('error', (e) => { process.stdout.write('REQ_ERROR: ' + e.message); });
req.on('timeout', () => { req.destroy(); process.stdout.write('REQ_TIMEOUT'); });
req.write(body);
req.end();

// List tools on local Vibe MCP.
const http = require('http');
const body = JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/list', params: {} });
const req = http.request({
  host: '127.0.0.1', port: 20678, path: '/mcp', method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'Content-Length': Buffer.byteLength(body) },
  timeout: 30000
}, (res) => {
  const chunks = [];
  res.on('data', (d) => chunks.push(d));
  res.on('end', () => {
    const raw = Buffer.concat(chunks).toString('utf8');
    const payloads = [];
    for (const line of raw.split(/\r?\n/)) if (line.startsWith('data:')) payloads.push(line.slice(5).trim());
    const out = payloads.length ? payloads.join('') : raw;
    try {
      const j = JSON.parse(out);
      for (const t of (j.result && j.result.tools) || []) {
        console.log('## ' + t.name + ' :: ' + (t.description || '').split('\n')[0].slice(0, 120));
      }
    } catch (e) { console.log(out.slice(0, 3000)); }
  });
});
req.on('error', (e) => console.log('REQ_ERROR: ' + e.message));
req.write(body); req.end();

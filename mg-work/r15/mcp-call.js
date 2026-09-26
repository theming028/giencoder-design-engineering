// Generic MasterGo local Vibe MCP caller.
// usage: node mcp-call.js <toolName> '<jsonArgs>' [timeoutMs]
const http = require('http');

const toolName = process.argv[2];
const rawArgs = process.argv[3] || '{}';
const timeoutMs = parseInt(process.argv[4] || '120000', 10);
const args = JSON.parse(rawArgs);

const body = JSON.stringify({
  jsonrpc: '2.0', id: 1, method: 'tools/call',
  params: { name: toolName, arguments: args }
});

const req = http.request({
  host: '127.0.0.1', port: 20678, path: '/mcp', method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/event-stream',
    'Content-Length': Buffer.byteLength(body)
  },
  timeout: timeoutMs
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
      const r = j.result || j;
      // unwrap MCP content array
      if (r && Array.isArray(r.content)) {
        for (const c of r.content) {
          if (c.type === 'text') console.log(c.text);
          else console.log('[non-text content] ' + JSON.stringify(c).slice(0, 400));
        }
      } else {
        console.log(JSON.stringify(r, null, 2));
      }
    } catch (e) {
      console.log('RAW:' + out.slice(0, 20000));
    }
  });
});
req.on('timeout', () => { console.log('REQ_TIMEOUT after ' + timeoutMs + 'ms'); req.destroy(); });
req.on('error', (e) => console.log('REQ_ERROR: ' + e.message));
req.write(body); req.end();

// Proper MCP session: initialize -> notifications/initialized -> tools/call
// usage: node mcp-session.js <toolName> '<jsonArgs>' [timeoutMs]
const http = require('http');

const toolName = process.argv[2];
const args = JSON.parse(process.argv[3] || '{}');
const timeoutMs = parseInt(process.argv[4] || '120000', 10);

let sessionId = null;
let buffer = '';
const pending = new Map();
let nextId = 1;

function parseChunks(raw) {
  // split on SSE event boundaries; each event may hold one json payload
  const out = [];
  for (const part of raw.split(/\n\n/)) {
    const datas = part.split(/\r?\n/).filter((l) => l.startsWith('data:')).map((l) => l.slice(5).trim());
    if (datas.length) out.push(datas.join(''));
  }
  if (!out.length && raw.trim().startsWith('{')) out.push(raw.trim());
  return out;
}

function send(req, method, params, isNotification) {
  const msg = { jsonrpc: '2.0', method };
  if (!isNotification) msg.id = nextId++;
  if (params !== undefined) msg.params = params;
  // Node http client frames the body itself; write plain JSON only.
  req.write(JSON.stringify(msg));
  return msg.id;
}

const req = http.request({
  host: '127.0.0.1', port: 20678, path: '/mcp', method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/event-stream'
  },
  timeout: timeoutMs
}, (res) => {
  sessionId = res.headers['mcp-session-id'] || sessionId;
  console.log('[session] ' + JSON.stringify(sessionId));
  res.on('data', (d) => {
    buffer += d.toString('utf8');
    let idx;
    while ((idx = buffer.indexOf('\n\n')) !== -1) {
      const evt = buffer.slice(0, idx);
      buffer = buffer.slice(idx + 2);
      for (const payload of parseChunks(evt)) {
        let j;
        try { j = JSON.parse(payload); } catch (e) { continue; }
        handle(j);
      }
    }
  });
  res.on('end', () => { console.log('[closed]'); process.exit(0); });
});

function handle(j) {
  if (j.id && pending.has(j.id)) {
    const label = pending.get(j.id);
    pending.delete(j.id);
    console.log('=== response to ' + label + ' ===');
    print(j);
    if (label === 'initialize') {
      send(req, 'notifications/initialized', {}, true);
      const id = send(req, 'tools/call', { name: toolName, arguments: args });
      pending.set(id, 'tools/call:' + toolName);
    } else {
      process.exit(0);
    }
  } else if (j.id === null || j.id === undefined) {
    // notification
  }
}

function print(j) {
  if (j.error) { console.log('ERROR ' + JSON.stringify(j.error)); return; }
  const r = j.result || j;
  if (r && Array.isArray(r.content)) {
    for (const c of r.content) {
      if (c.type === 'text') console.log(c.text);
      else console.log('[non-text] ' + JSON.stringify(c).slice(0, 500));
    }
  } else {
    console.log(JSON.stringify(r, null, 2));
  }
}

req.on('timeout', () => { console.log('REQ_TIMEOUT after ' + timeoutMs + 'ms'); req.destroy(); process.exit(1); });
req.on('error', (e) => { console.log('REQ_ERROR: ' + e.message); process.exit(1); });

// write initialize
const initMsg = {
  jsonrpc: '2.0', id: nextId++, method: 'initialize',
  params: {
    protocolVersion: '2024-11-05',
    capabilities: {},
    clientInfo: { name: 'wb-probe', version: '1.0.0' }
  }
};
pending.set(initMsg.id, 'initialize');
req.write(JSON.stringify(initMsg));

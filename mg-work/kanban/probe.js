// Probe candidate node ids cheaply via get_screenshot (success msg includes name+size).
const http = require('http');
const PORT = 20678;
const PROJECT_DIR = 'C:\\Users\\Administrator\\Documents\\Qoder\\2026-09-24\\0bfb1ccc\\giencoder-design-engineering';

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
      }, timeout: 40000
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

function summarize(resp) {
  try {
    const j = JSON.parse(resp);
    const t = j.result && j.result.content && j.result.content[0] && j.result.content[0].text;
    if (!t) return resp.slice(0, 100);
    const m = t.match(/\[([\d:]+)\]\s*(\S+?\.png)，约\s*([\d.]+)\s*KB/);
    if (m) return 'OK ' + m[1] + ' ' + m[3] + 'KB ' + m[2];
    return (t.match(/[❌✅][^\n]*/) || [t.slice(0, 80)])[0].slice(0, 100);
  } catch (e) { return resp.slice(0, 100); }
}

(async () => {
  const ids = process.argv.slice(2);
  for (const id of ids) {
    const r = await call('get_screenshot', { projectDir: PROJECT_DIR, targetNodeId: id });
    console.log(id + ' -> ' + summarize(r));
  }
  console.log('PROBE_DONE');
})();

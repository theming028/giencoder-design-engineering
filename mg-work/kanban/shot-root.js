// 对任务看板设计根节点 553:06620 截图
const http = require('http');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';

function call(tool, args, timeoutMs) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random()*1000),
      method: 'tools/call', params: { name: tool, arguments: args } });
    const req = http.request({ host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body) }, timeout: timeoutMs || 240000 }, (res) => {
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
  const r = await call('get_screenshot', { projectDir: PROJECT_DIR, targetNodeId: '553:06620', savePath: 'mg-work/kanban/r11/design-board.png' });
  console.log(r.slice(0, 600));
  console.log('DONE');
})();

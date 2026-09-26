// 宽范围探测: 836:21300-21400 和 21431-21560, 找可导出的看板 frame
const http = require('http');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';

function call(tool, args, timeoutMs) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random()*1000),
      method: 'tools/call', params: { name: tool, arguments: args } });
    const req = http.request({ host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body) }, timeout: timeoutMs || 20000 }, (res) => {
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
  const ids = [];
  for (let i = 21300; i <= 21400; i++) ids.push('836:' + i);
  for (let i = 21431; i <= 21560; i++) ids.push('836:' + i);
  for (const id of ids) {
    const r = await call('get_screenshot', { projectDir: PROJECT_DIR, targetNodeId: id, savePath: 'mg-work/kanban/r11/probe2.png' }, 15000);
    if (r.includes('成功 1/1') || (r.includes('成功') && !r.includes('保存失败'))) {
      console.log('HIT', id, '=>', r.slice(0, 400).replace(/\\n/g, ' | '));
    }
  }
  console.log('ALL DONE');
})();

// 探测 836:21400~836:21430 范围内的可导出图层（截图探针）
const http = require('http');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';

function call(tool, args, timeoutMs) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random()*1000),
      method: 'tools/call', params: { name: tool, arguments: args } });
    const req = http.request({ host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body) }, timeout: timeoutMs || 30000 }, (res) => {
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
  for (let i = 21400; i <= 21430; i++) {
    const id = '836:' + i;
    const r = await call('get_screenshot', { projectDir: PROJECT_DIR, targetNodeId: id, savePath: 'mg-work/kanban/r11/probe-' + i + '.png' }, 25000);
    let msg = '';
    try { msg = JSON.parse(r).result.content[0].text.split('\n').filter(l => l.includes('保存') || l.includes('失败') || l.includes('成功')).join(' | ').slice(0, 150); }
    catch (e) { msg = r.slice(0, 100); }
    console.log(id, '=>', msg);
  }
  console.log('DONE');
})();

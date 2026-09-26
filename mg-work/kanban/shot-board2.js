// 重试截图旧设计看板根 553:06620, 多次尝试 + scale 选项
const http = require('http');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';

function call(tool, args, timeoutMs) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random()*1000),
      method: 'tools/call', params: { name: tool, arguments: args } });
    const req = http.request({ host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body) }, timeout: timeoutMs || 280000 }, (res) => {
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

function extractText(resp) {
  try {
    const j = JSON.parse(resp);
    const c = j.result && j.result.content;
    if (Array.isArray(c)) return c.map(x => x.text || '').join('\n');
  } catch (e) {}
  return resp;
}

(async () => {
  const url = 'https://mastergo.com/goto/WnxPLRdy?page_id=pu489:07981&layer_id=553:06620&file=193158744355579';
  for (const scale of [1, 0.5, 1]) {
    for (let i = 1; i <= 3; i++) {
      const r = await call('get_screenshot', { projectDir: PROJECT_DIR, targetNodeId: url, savePath: 'mg-work/kanban/r11/design-board.png', scale });
      const t = extractText(r);
      console.log('scale=' + scale + ' try' + i + ':', t.split('\n')[0].slice(0, 120));
      if (t.includes('成功 1/1')) { console.log('DONE'); return; }
    }
  }
  console.log('ALL FAILED');
})();

// 探测老设计页 pu489:07981 上 553:06620 的子节点 (1333:18100-18330, 622:08900-09600)
const http = require('http');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';
const URL_BASE = 'https://mastergo.com/goto/WnxPLRdy?page_id=pu489:07981&layer_id=';

function call(tool, args, timeoutMs) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random()*1000),
      method: 'tools/call', params: { name: tool, arguments: args } });
    const req = http.request({ host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body) }, timeout: timeoutMs || 15000 }, (res) => {
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
  for (let i = 18100; i <= 18330; i++) ids.push('1333:' + i);
  for (const id of ids) {
    const r = await call('get_screenshot', { projectDir: PROJECT_DIR, targetNodeId: URL_BASE + id, savePath: 'mg-work/kanban/r11/probe3.png' }, 13000);
    if (r.includes('成功 1/1')) {
      const m = r.match(/([^\\"/]+_\d+-\d+\.png)/);
      console.log('HIT', id, '=>', m ? m[1] : r.slice(80, 200));
    }
  }
  console.log('ALL DONE');
})();

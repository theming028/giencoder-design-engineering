// 导出设计稿节点 836:21409 (模态) 和 836:21408 (页面上下文)：截图 + 前端代码
const http = require('http');
const path = require('path');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';
const OUT_REL = 'mg-work/kanban/r11';

function call(tool, args) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random()*1000),
      method: 'tools/call', params: { name: tool, arguments: args } });
    const req = http.request({ host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body) }, timeout: 180000 }, (res) => {
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
  // 页面全景截图（836:21408 是含弹层的整页）
  const shot = await call('get_screenshot', { projectDir: PROJECT_DIR, targetNodeId: '836:21408', savePath: path.join(OUT_REL, 'design-page.png') });
  console.log('SHOT_PAGE:', shot.slice(0, 300));
  const shot2 = await call('get_screenshot', { projectDir: PROJECT_DIR, targetNodeId: '836:21409', savePath: path.join(OUT_REL, 'design-modal.png') });
  console.log('SHOT_MODAL:', shot2.slice(0, 300));
  const resp = await call('get_frontend_code', { projectDir: PROJECT_DIR, targetNodeId: '836:21409', frontendFramework: 'html', outDir: OUT_REL, fileName: 'modal.html' });
  console.log('HTML:', resp.slice(0, 400));
  console.log('DONE');
})();

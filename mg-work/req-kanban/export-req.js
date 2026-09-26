// 导出需求看板节点 (769:13709)：截图 + 完整前端代码（含 asset/icons）
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';
const NODE_ID = '769:13709';
const OUT_REL = 'mg-work/req-kanban/full';

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
  const shot = await call('get_screenshot', { projectDir: PROJECT_DIR, targetNodeId: NODE_ID, savePath: path.join(OUT_REL, 'design.png') });
  console.log('SCREENSHOT:', shot.slice(0, 300));
  const resp = await call('get_frontend_code', { projectDir: PROJECT_DIR, targetNodeId: NODE_ID, frontendFramework: 'html', outDir: OUT_REL, fileName: 'node.html' });
  console.log('HTML:', resp.slice(0, 400));
  console.log('DONE');
})();

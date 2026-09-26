// 逐个小节点导出缺失 SVG 资源
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';

// [输出目录, 节点ID] —— 均为小图标节点
const NODES = [
  ['r01', '769:13712'],  // 下载 icon
  ['r02', '817:11738'],  // 排序 icon
  ['r03', '817:12171'],  // 未开始 dot
  ['r04', '817:12008'],  // 进行中 dot
  ['r05', '817:11884'],  // 已完成 dot
  ['r06', '817:11906'],  // 已终止 dot
  ['r07', '817:12177'],  // 已取消 dot
  ['r08', '769:13140'],  // 进行中 stats icon
  ['r09', '817:12073'],  // 已取消 stats icon
  ['r10', '769:13145'],  // 已终止 stats icon
  ['r11', '769:13155'],  // 已完成 stats icon
  ['r12', '817:12068'],  // 未开始 stats icon
  ['r13', '769:13864'],  // 需求看板 radio icon
];

function call(tool, args) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: Date.now() + Math.floor(Math.random()*1000),
      method: 'tools/call', params: { name: tool, arguments: args } });
    const req = http.request({ host: '127.0.0.1', port: PORT, path: '/mcp', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'Content-Length': Buffer.byteLength(body) }, timeout: 170000 }, (res) => {
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
  for (const [dir, nid] of NODES) {
    const outRel = 'mg-work/req-kanban/' + dir;
    fs.mkdirSync(path.join(PROJECT_DIR, outRel, 'asset', 'icons'), { recursive: true });
    const resp = await call('get_frontend_code', { projectDir: PROJECT_DIR, targetNodeId: nid, frontendFramework: 'html', outDir: outRel, fileName: 'node.html' });
    const ok = resp.includes('成功') || fs.existsSync(path.join(PROJECT_DIR, outRel, 'node.html'));
    console.log(dir, nid, ok ? 'OK' : 'FAIL', resp.slice(0, 120).replace(/\n/g, ' '));
  }
  console.log('ALL DONE');
})();

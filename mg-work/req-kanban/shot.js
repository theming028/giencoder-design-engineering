const http = require('http');
const PORT = 20678;
const PROJECT_DIR = 'E://GienCoder//giencoder-design-engineering';
function call(tool, args) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc:'2.0', id:Date.now(), method:'tools/call', params:{name:tool,arguments:args} });
    const req = http.request({ host:'127.0.0.1', port:PORT, path:'/mcp', method:'POST',
      headers:{'Content-Type':'application/json','Accept':'application/json, text/event-stream','Content-Length':Buffer.byteLength(body)}, timeout:170000 }, (res)=>{
      const c=[]; res.on('data',d=>c.push(d)); res.on('end',()=>{ const raw=Buffer.concat(c).toString('utf8');
        const p=[]; for(const l of raw.split(/\r?\n/)) if(l.startsWith('data:')) p.push(l.slice(5).trim());
        resolve(p.length?p.join('\n'):raw); });
    });
    req.on('error',e=>resolve('ERR '+e.message)); req.on('timeout',()=>{req.destroy();resolve('TIMEOUT');});
    req.write(body); req.end();
  });
}
(async()=>{
  const r = await call('get_screenshot', { projectDir: PROJECT_DIR, targetNodeId: '769:13709', savePath: 'mg-work/req-kanban/design.png' });
  console.log(r.slice(0, 400));
})();

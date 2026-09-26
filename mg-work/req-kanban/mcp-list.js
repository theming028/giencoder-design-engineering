const http = require('http');
const PORT = 20678;
function call(method, params) {
  return new Promise((resolve) => {
    const body = JSON.stringify({ jsonrpc:'2.0', id:Date.now(), method, params });
    const req = http.request({ host:'127.0.0.1', port:PORT, path:'/mcp', method:'POST',
      headers:{'Content-Type':'application/json','Accept':'application/json, text/event-stream','Content-Length':Buffer.byteLength(body)}, timeout:30000 }, (res)=>{
      const c=[]; res.on('data',d=>c.push(d)); res.on('end',()=>{ const raw=Buffer.concat(c).toString('utf8');
        const p=[]; for(const l of raw.split(/\r?\n/)) if(l.startsWith('data:')) p.push(l.slice(5).trim());
        resolve(p.length?p.join('\n'):raw); });
    });
    req.on('error',e=>resolve('ERR '+e.message)); req.on('timeout',()=>{req.destroy();resolve('TIMEOUT');});
    req.write(body); req.end();
  });
}
(async()=>{
  const r = await call('tools/list', {});
  try { const j = JSON.parse(r); console.log((j.result.tools||[]).map(t=>t.name+' :: '+(t.description||'').slice(0,80)).join('\n')); }
  catch(e){ console.log(r.slice(0,2000)); }
})();

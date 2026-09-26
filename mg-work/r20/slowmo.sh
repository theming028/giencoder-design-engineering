AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
"$AB" set viewport 1440 900 >/dev/null 2>&1
"$AB" open "$URL" >/dev/null 2>&1
sleep 2
# 把弹窗动画放慢到 3s，并暂停在 35% 处，便于捕捉闪现的边
"$AB" eval "(function(){
  var st=document.createElement('style'); st.id='slowmo';
  st.textContent='.kb-crt-dialog{transition-duration:3000ms !important}.kb-crt-mask{transition-duration:3000ms !important}';
  document.head.appendChild(st);
  document.querySelector('.kb-create').click();
  return 'opened';
})()"
sleep 1
"$AB" screenshot "" mg-work/r20/anim-mid.png >/dev/null 2>&1
"$AB" eval "(function(){
  var d=document.querySelector('.kb-crt-dialog');
  var cs=getComputedStyle(d);
  var b=d.getBoundingClientRect();
  return JSON.stringify({rect:[b.left,b.top,b.width,b.height],opacity:cs.opacity,boxShadow:cs.boxShadow,willChange:cs.willChange,transform:cs.transform,overflow:cs.overflow});
})()"

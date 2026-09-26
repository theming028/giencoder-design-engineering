AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
"$AB" set viewport 1440 900 >/dev/null 2>&1
"$AB" open "$URL" >/dev/null 2>&1
sleep 2
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){
  var rows=document.querySelectorAll('.kb-crt-aside-body .kb-crt-row');
  var out=[];
  rows.forEach(function(row){
    var lbl=row.querySelector('.kb-crt-lbl');
    var vis=row.querySelector('.giencoder-select-view')||row.querySelector('.giencoder-input-wrapper');
    if(!vis) return;
    var cs=getComputedStyle(vis); var b=vis.getBoundingClientRect();
    out.push((lbl?lbl.textContent.trim():'?')+' w='+b.width.toFixed(2)+' h='+b.height.toFixed(2)+' pad='+cs.paddingLeft+'/'+cs.paddingRight+' bw='+cs.borderLeftWidth+'/'+cs.borderRightWidth+' box='+cs.boxSizing+' minW='+cs.minWidth+' maxW='+cs.maxWidth);
  });
  return out.join('\n');
})()"

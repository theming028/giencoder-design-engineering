AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
"$AB" set viewport 1440 900 >/dev/null 2>&1
"$AB" open "$URL" >/dev/null 2>&1
sleep 2
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){
  var out=[];
  document.querySelectorAll('.kb-crt-aside-body .kb-crt-row').forEach(function(row){
    var lbl=row.querySelector('.kb-crt-lbl');
    var vis=row.querySelector('.giencoder-select-view')||row.querySelector('.giencoder-input-wrapper');
    var fld=row.querySelector('.kb-crt-fld');
    var r=function(e){if(!e)return null;var b=e.getBoundingClientRect();return Math.round(b.width)+'@'+Math.round(b.left);};
    out.push((lbl?lbl.textContent.trim():'?')+' | rowFld='+r(fld)+' | visible='+r(vis)+' | visTag='+(vis?vis.className.split(' ').slice(0,2).join('.'):'-'));
  });
  return out.join('\n');
})()"

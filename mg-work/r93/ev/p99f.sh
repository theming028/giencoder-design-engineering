#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"
"$NODE" "$AB" wait 1800
shot () {  # $1=selector $2=outname
  "$NODE" "$AB" eval "(function(){var e=document.querySelector('$1');if(!e)return 'NO';e.scrollIntoView({block:'center'});var r=e.getBoundingClientRect();return '$2 ' + Math.round(r.left)+','+Math.round(r.top)+' '+Math.round(r.width)+'x'+Math.round(r.height);})();"
  "$NODE" "$AB" wait 500
  "$NODE" "$AB" screenshot "" "mg-work/r93/raw/$2.png"
}
echo '--- top ---'
"$NODE" "$AB" eval "(function(){var e=document.querySelector('.r93-conv-host');if(e)e.scrollTop=0;window.scrollTo(0,0);return 'top';})();"
"$NODE" "$AB" wait 400
"$NODE" "$AB" screenshot "" "mg-work/r93/raw/r99v-top.png"
shot ".r93-dlist"        "r99v-dlist"
shot ".r93-drow"         "r99v-drow"
shot ".r93-rateline"     "r99v-rateline"
shot ".r93-artlabel"     "r99v-artlabel"
"$NODE" "$AB" close --all >/dev/null 2>&1

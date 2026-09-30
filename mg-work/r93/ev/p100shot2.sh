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
echo "-- 树（展开）"
"$NODE" "$AB" eval "$(cat mg-work/r93/ev/p100shot2.js)"
"$NODE" "$AB" wait 300
"$NODE" "$AB" screenshot "" "mg-work/r93/raw/r100-tools5-open.png" >/dev/null 2>&1
echo "-- 内层收起"
"$NODE" "$AB" click ".r93-tree > .r93-fold > .r93-fh" >/dev/null 2>&1
"$NODE" "$AB" wait 400
"$NODE" "$AB" screenshot "" "mg-work/r93/raw/r100-tools5-collapsed.png" >/dev/null 2>&1
"$NODE" "$AB" click ".r93-tree > .r93-fold > .r93-fc" >/dev/null 2>&1
"$NODE" "$AB" wait 400
echo "-- ndesc"
"$NODE" "$AB" eval "(()=>{const e=document.querySelectorAll('.r93-ndesc')[0]; e.scrollIntoView({block:'center'}); return 'ok';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 300
"$NODE" "$AB" screenshot "" "mg-work/r93/raw/r100-ndesc.png" >/dev/null 2>&1
echo "-- agent 行"
"$NODE" "$AB" eval "(()=>{document.querySelector('.r93-agents').scrollIntoView({block:'center'}); return 'ok';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 300
"$NODE" "$AB" screenshot "" "mg-work/r93/raw/r100-agents.png" >/dev/null 2>&1
echo "-- 全页"
"$NODE" "$AB" eval "(()=>{const s=document.querySelector('.r93-scroll'); s.scrollTop=0; return 'ok';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 400
"$NODE" "$AB" screenshot "" "mg-work/r93/raw/r100-full-1440.png" >/dev/null 2>&1
echo done

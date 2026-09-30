#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
TS=$(date +%s)
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 2600 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var s=document.querySelector('.r93-scroll'); s.scrollTop=Math.round(s.scrollHeight*0.55); return s.scrollTop;})()" >/dev/null 2>&1
"$NODE" "$AB" wait 500 >/dev/null 2>&1
echo "[A 当前 60%]"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/k103-A60.png" >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var tb=document.querySelector('.r93-tobottom'); tb.style.setProperty('--r93-glass-pill','rgba(255,255,255,0.72)'); return getComputedStyle(tb).backgroundColor;})()"
"$NODE" "$AB" wait 300 >/dev/null 2>&1
echo "[B 回退 72%（对照）]"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/k103-B72.png" >/dev/null 2>&1
echo done

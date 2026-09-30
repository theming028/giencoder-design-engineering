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
echo "[rect 读数]"
"$NODE" "$AB" eval "(function(){var s=document.querySelector('.r93-scroll'); s.scrollTop=Math.round(s.scrollHeight*0.55); var tb=document.querySelector('.r93-tobottom'); var r=tb.getBoundingClientRect(); return JSON.stringify({show:getComputedStyle(tb).display, x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),bg:getComputedStyle(tb).backgroundColor,sc:Math.round(s.scrollTop)});})()"
"$NODE" "$AB" wait 400 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/j103-pill-1440.png" >/dev/null 2>&1
echo "  shot j103-pill-1440.png"

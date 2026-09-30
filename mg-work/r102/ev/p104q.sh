#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 2560 1440 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 120 >/dev/null 2>&1
echo "===== 2560 F1 首帧（应 app=null / sk=true / box.op=0 / pe=none）====="
"$NODE" "$AB" eval "(function(){var hero=document.querySelector('main > div > div.flex-1.justify-center');var box=hero.querySelector(':scope > div.mt-8');return JSON.stringify({app:document.documentElement.getAttribute('data-r93-app'),sk:!!document.querySelector('.r93-sk'),boxOp:getComputedStyle(box).opacity,boxPe:getComputedStyle(box).pointerEvents,hostZ:getComputedStyle(document.querySelector('.r93-conv-host')).zIndex,heroZ:getComputedStyle(hero).zIndex});})()"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/f2560-early.png" >/dev/null 2>&1
"$NODE" "$AB" wait 2600 >/dev/null 2>&1
echo "===== 2560 F2 就绪 ====="
"$NODE" "$AB" eval "(function(){var hero=document.querySelector('main > div > div.flex-1.justify-center');var box=hero.querySelector(':scope > div.mt-8');return JSON.stringify({app:document.documentElement.getAttribute('data-r93-app'),sk:!!document.querySelector('.r93-sk'),boxOp:getComputedStyle(box).opacity,boxPe:getComputedStyle(box).pointerEvents});})()"

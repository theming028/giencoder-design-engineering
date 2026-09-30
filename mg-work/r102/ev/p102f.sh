#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"; H="${2:-900}"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport "$W" "$H" >/dev/null 2>&1
echo "===== ① 数字滑入：真实时间轴两拍（不干预动画） ====="
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/z102-t1.png" >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var sk=document.querySelector('.r93-sk');var i=document.querySelector('.r93-num-i');var c=getComputedStyle(i);return JSON.stringify({skStillInDom:!!sk,skClass:sk?sk.className:null,numOp:c.opacity,numTf:c.transform,animDelay:c.animationDelay});})()"
"$NODE" "$AB" wait 1400 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/z102-t2.png" >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var sk=document.querySelector('.r93-sk');var i=document.querySelector('.r93-num-i');var c=getComputedStyle(i);return JSON.stringify({skStillInDom:!!sk,numOp:c.opacity,numTf:c.transform,delay:c.animationDelay});})()"
echo "  两拍已拍：z102-t1.png / z102-t2.png"

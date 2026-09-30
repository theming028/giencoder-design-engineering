#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"; H="${2:-900}"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport "$W" "$H" >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 2300 >/dev/null 2>&1
echo "===== ① 数字滑入：定格三帧（设 currentTime → 隔帧 → 读+拍） ====="
"$NODE" "$AB" eval "(function(){var i=document.querySelector('.r93-num-i');var a=i.getAnimations()[0];a.pause();window.__a=a;window.__i=i;return 'paused';})()" >/dev/null 2>&1
for CT in 0 130 460; do
  "$NODE" "$AB" eval "window.__a.currentTime=$CT; 'set $CT'" >/dev/null 2>&1
  "$NODE" "$AB" wait 200 >/dev/null 2>&1
  echo "[currentTime=$CT]"
  "$NODE" "$AB" eval "(function(){var i=window.__i,c=getComputedStyle(i);var b=i.getBoundingClientRect(),p=i.parentNode.getBoundingClientRect();var e=document.querySelector('.r93-num-i');var t=document.querySelector('.r93-num');var tb=t.getBoundingClientRect();return JSON.stringify({op:c.opacity,tf:c.transform,dy:Math.round(b.top-tb.top),winH:Math.round(tb.height),innerH:Math.round(b.height)});})()"
  "$NODE" "$AB" screenshot "" "mg-work/r102/raw/z102-num-$CT.png" >/dev/null 2>&1
done
echo "  三帧已拍"

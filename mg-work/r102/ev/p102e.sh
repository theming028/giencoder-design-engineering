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
"$NODE" "$AB" wait 2200 >/dev/null 2>&1
echo "===== ① 数字动效：定格三帧（对第一个 .r93-num-i 的动画设 currentTime） ====="
"$NODE" "$AB" eval "(function(){var i=document.querySelector('.r93-num-i');var a=i.getAnimations()[0];if(!a)return 'no-anim';a.pause();window.__a=a;window.__i=i;var t=a.effect.getTiming();return JSON.stringify({name:a.animationName,delay:t.delay,duration:t.duration,fill:t.fill,easing:t.easing});})()"
for CT in 0 150 300 460; do
  "$NODE" "$AB" eval "(function(){window.__a.currentTime=$CT;var c=getComputedStyle(window.__i);var b=window.__i.getBoundingClientRect();var p=window.__i.parentNode.getBoundingClientRect();return JSON.stringify({ct:$CT,op:c.opacity,tf:c.transform,dyFromWindowTop:Math.round(b.top-p.top),h:Math.round(b.height)});})()"
done
echo "[参考：同元素在 overflow:visible 下的静止位（作基准）]"
"$NODE" "$AB" eval "(function(){var i=window.__i,p=i.parentNode;var a=i.getAnimations();a.forEach(function(x){x.cancel();});var c=getComputedStyle(i);var b=i.getBoundingClientRect(),pb=p.getBoundingClientRect();return JSON.stringify({op:c.opacity,tf:c.transform,dyFromWindowTop:Math.round(b.top-pb.top),h:Math.round(b.height)});})()"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/p102e-num-final-${W}.png" >/dev/null 2>&1
echo "  shot p102e-num-final-${W}.png"

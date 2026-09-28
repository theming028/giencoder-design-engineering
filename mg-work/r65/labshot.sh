#!/usr/bin/env zsh
# r65：方案页取证 —— 主图（钉相位 0.5）+ A/B 两方案的四相位运动条
set -e
cd /Users/shaoyuming/Documents/GienCoderDesignEngineering
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=$PWD/mg-work/r65/ev
URL="file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r65/shimmer-lab.html"

$AB open "$URL" >/dev/null
$AB set viewport 1460 1420 >/dev/null
sleep 1.4

echo "--- 取样框 ---"
$AB eval '(function(){
  function box(sel){var r=document.querySelector(sel).getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)];}
  return JSON.stringify({A:box(".vA .kb-card"),B:box(".vB .kb-card"),now:box(".v0 .kb-card"),F:box(".vF .kb-card")});
})()'

$AB eval '(function(){ document.getAnimations().forEach(function(a){var d=a.effect.getTiming().duration; if(isFinite(d)){a.pause(); a.currentTime=d*0.5;}}); return "pinned 0.5"; })()' >/dev/null
sleep 0.3
$AB screenshot "$EV/30-shimmer-lab.png" >/dev/null
echo saved 30-shimmer-lab.png

for P in 0.10 0.35 0.60 0.85; do
  $AB eval "(function(){ document.getAnimations().forEach(function(a){var d=a.effect.getTiming().duration; if(isFinite(d)){a.pause(); a.currentTime=d*$P;}}); return '$P'; })()" >/dev/null
  sleep 0.25
  $AB screenshot "$EV/ph-$P.png" >/dev/null
  echo "saved ph-$P.png"
done

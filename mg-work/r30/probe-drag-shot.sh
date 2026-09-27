#!/usr/bin/env bash
# 对照实验：按住拖动期间 —— 截图前后各读一次 .td-left 的 getBoundingClientRect，
# 判断「截图里看不到位移」是截图时机问题，还是拖动状态被意外清掉。
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"
OUT="mg-work/r30/shots"
mkdir -p "$OUT"

HELP='var Q=function(s){return document.querySelector(s)},R=function(e){var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},PE=function(t,x,y,el){(el||Q(".td-bar")).dispatchEvent(new PointerEvent(t,{bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,button:0,buttons:t==="pointerup"?0:1,pointerId:7,pointerType:"mouse",isPrimary:true}))},SPIN=function(ms){var t=Date.now();while(Date.now()-t<ms){}};'

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0

echo "--- 基线 rect ---"
$AB eval "$HELP JSON.stringify({left:R(Q('.td-left')),right:R(Q('.td-right'))})" 2>&1 | tail -1

echo "--- pointerdown + 拖到 400px（保持按住）---"
$AB eval "$HELP (function(){var bar=Q('.td-bar');var r=bar.getBoundingClientRect();var y=Math.round(r.top+r.height/2),x=Math.round(r.left+220);
PE('pointerdown',x,y);SPIN(60);PE('pointermove',x+30,y);SPIN(60);PE('pointermove',x+400,y);})()" >/dev/null 2>&1

echo "--- 截图前 rect（transform 生效时会右移 154px）---"
$AB eval "$HELP JSON.stringify({left:R(Q('.td-left')),right:R(Q('.td-right')),tL:getComputedStyle(Q('.td-left')).transform,armed:Q('.td-root').classList.contains('is-xarmed')})" 2>&1 | tail -1
$AB screenshot "$OUT/exp-hold-before.png" >/dev/null 2>&1
echo "--- 截图后 rect ---"
$AB eval "$HELP JSON.stringify({left:R(Q('.td-left')),tL:getComputedStyle(Q('.td-left')).transform,held:Q('.td-root').classList.contains('is-xdrag')})" 2>&1 | tail -1

echo "--- 再截图一次（同一状态，应 md5 一致）---"
$AB screenshot "$OUT/exp-hold-before2.png" >/dev/null 2>&1
$AB eval "$HELP JSON.stringify({left:R(Q('.td-left'))})" 2>&1 | tail -1

echo "--- 松手 → 落位 ---"
$AB eval "$HELP (function(){var bar=Q('.td-bar');var r=bar.getBoundingClientRect();var y=Math.round(r.top+r.height/2),x=Math.round(r.left+220);PE('pointerup',x+400,y);})()" >/dev/null 2>&1
sleep 1.0
$AB eval "$HELP JSON.stringify({left:R(Q('.td-left')),right:R(Q('.td-right')),swapped:Q('.td-root').classList.contains('is-swapped')})" 2>&1 | tail -1
$AB screenshot "$OUT/exp-after-swap.png" >/dev/null 2>&1

echo "--- md5 ---"
for f in exp-hold-before exp-hold-before2 exp-after-swap; do
  printf "%-22s %s\n" "$f" "$($P -c "import hashlib,sys;print(hashlib.md5(open(sys.argv[1],'rb').read()).hexdigest())" "$OUT/$f.png")"
done

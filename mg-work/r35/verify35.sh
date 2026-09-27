#!/usr/bin/env bash
# 第 35 轮第 1 项实测：任务详情页「分栏布局记忆」
#   覆盖：拖标题栏互换 → 记忆 → 刷新保持；（再验）拖栏宽 → 记忆 → 刷新保持；双击复位 → 记忆清除
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r35/probe35.jsonl"
SHOT="mg-work/r35/shots"
mkdir -p "$SHOT"; : > "$OUT"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CS=function(e,p){return e?getComputedStyle(e)[p]:null},C=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)]},RR=function(e,p){return e?getComputedStyle(e).getPropertyValue(p).trim():null},STORE=function(){try{return localStorage.getItem("giencoder:td-cols:v1")}catch(e){return "ERR:"+e}};'

rec() { "$P" -c "
import json,sys
step=sys.argv[1]; raw=sys.argv[2]
try:
    d=json.loads(raw)
    if isinstance(d,str): d=json.loads(d)
except Exception as e:
    d={'__parse_error__':str(e),'raw':raw[:300]}
print(json.dumps({'step':step,'data':d},ensure_ascii=False))
" "$1" "$2" >> "$OUT"; }
ev() { "$AB" eval "$HELP $1" 2>&1 | tail -1; }
xy() { echo "$1" | "$P" -c "import json,sys;d=json.loads(sys.stdin.read())
if isinstance(d,str): d=json.loads(d)
print(d[0],d[1])"; }

SNAP='JSON.stringify((function(){var r=Q(".td-root"),L=Q(".td-left"),Rt=Q(".td-right"),g=Q("[data-td-gutter]");return{swapped:r.classList.contains("is-swapped"),collapsed:r.classList.contains("is-collapsed"),rightW:RR(r,"--td-right-w"),left:R(L),right:R(Rt),gutter:R(g),store:STORE()};})())'

# 真实拖动：按下后分多步移动（制造速度），再抬起
drag() { # $1=startX $2=startY $3=dx
  local x=$1 y=$2 dx=$3 i
  $AB mouse move "$x" "$y" >/dev/null 2>&1; sleep 0.18
  $AB mouse down >/dev/null 2>&1; sleep 0.10
  for i in 1 2 3 4 5 6; do
    $AB mouse move "$(( x + dx * i / 6 ))" "$y" >/dev/null 2>&1; sleep 0.05
  done
  sleep 0.10
  $AB mouse up >/dev/null 2>&1; sleep 0.85
}

$AB open "$BASE/task-detail.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.0

# 清空历史记忆，建立干净基线
ev 'localStorage.removeItem("giencoder:td-cols:v1");location.reload();1' >/dev/null 2>&1
sleep 4.0
rec baseline "$(ev "$SNAP")"

# ---------- A. 拖动右栏标题栏 → 互换 ----------
RB="$(ev 'JSON.stringify(C(Q(".td-right-bar")))')"
read RXX RYY <<< "$(xy "$RB")"
echo "right-bar center = $RXX,$RYY"
drag "$RXX" "$RYY" -140
rec afterSwap "$(ev "$SNAP")"
$AB screenshot "$SHOT/01-swapped.png" >/dev/null 2>&1

# ---------- B. 刷新 → 记忆应生效 ----------
$AB open "$BASE/task-detail.html" >/dev/null 2>&1
sleep 4.0
rec reload1 "$(ev "$SNAP")"
$AB screenshot "$SHOT/02-reload-swapped.png" >/dev/null 2>&1

# ---------- C. 再拖回原布局 ----------
RB2="$(ev 'JSON.stringify(C(Q(".td-right-bar")))')"
read RX2 RY2 <<< "$(xy "$RB2")"
drag "$RX2" "$RY2" 140
rec swapBack "$(ev "$SNAP")"
$AB open "$BASE/task-detail.html" >/dev/null 2>&1
sleep 4.0
rec reload2 "$(ev "$SNAP")"

# ---------- D. 拖动条改栏宽 ----------
GB="$(ev 'JSON.stringify(C(Q("[data-td-gutter]")))')"
read GXX GYY <<< "$(xy "$GB")"
echo "gutter center = $GXX,$GYY"
drag "$GXX" "$GYY" -160
rec afterWidth "$(ev "$SNAP")"
$AB screenshot "$SHOT/03-width.png" >/dev/null 2>&1
$AB open "$BASE/task-detail.html" >/dev/null 2>&1
sleep 4.0
rec reload3 "$(ev "$SNAP")"

# ---------- E. 窄视口：记忆里的宽栏必须被重新夹住（1440 → 1100） ----------
NSNAP='JSON.stringify((function(){var r=Q(".td-root"),Rt=Q(".td-right"),L=Q(".td-left"),g=Q("[data-td-gutter]");return{rightW:RR(r,"--td-right-w"),right:R(Rt),left:R(L),gutter:R(g),root:R(r),store:STORE()};})())'
NORMSNAP='JSON.stringify((function(){var r=Q(".td-root"),Rt=Q(".td-right"),L=Q(".td-left");return{rightW:RR(r,"--td-right-w"),right:R(Rt),left:R(L),root:R(r)};})())'
$AB set viewport 1100 900 >/dev/null 2>&1
sleep 1.2
rec narrow "$(ev "$NSNAP")"
$AB screenshot "$SHOT/05-narrow.png" >/dev/null 2>&1
$AB open "$BASE/task-detail.html" >/dev/null 2>&1
sleep 4.0
rec narrowReload "$(ev "$NSNAP")"

# ---------- F. 回宽视口：记忆里的原始宽度应原样复原（钳位值不落盘） ----------
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 1.2
rec wideBack "$(ev "$NORMSNAP")"

# ---------- G. 双击拖动条 → 复位 + 清记忆 ----------
$AB dblclick "[data-td-gutter]" >/dev/null 2>&1
sleep 1.0
rec afterReset "$(ev "$SNAP")"
$AB open "$BASE/task-detail.html" >/dev/null 2>&1
sleep 4.0
rec reload4 "$(ev "$SNAP")"
$AB screenshot "$SHOT/04-reset.png" >/dev/null 2>&1

echo OK
cat "$OUT"

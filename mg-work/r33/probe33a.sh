#!/usr/bin/env bash
# 第33轮现状探查：三个页面一次跑完（同一标签页，避免并发冲突）
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r33"
PROBE="mg-work/r33/probe33a.jsonl"
mkdir -p "$OUT"
: > "$PROBE"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},C=function(e){var r=e.getBoundingClientRect();return{x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)}},CS=function(e,p){return getComputedStyle(e)[p]},RR=function(e,p){return getComputedStyle(e).getPropertyValue(p).trim()},DISP=function(e){return getComputedStyle(e).display};'

rec() {
  "$P" -c "
import json,sys
step=sys.argv[1]; raw=sys.argv[2]
try:
    d=json.loads(raw)
    if isinstance(d,str): d=json.loads(d)
except Exception as e:
    d={'__parse_error__':str(e),'raw':raw[:600]}
print(json.dumps({'step':step,'data':d},ensure_ascii=False))
" "$1" "$2" >> "$PROBE"
}
ev() { "$AB" eval "$HELP $1" 2>&1 | tail -1; }
nums() { "$P" -c "
import json,sys
d=sys.stdin.read().strip()
d=json.loads(d); d=json.loads(d) if isinstance(d,str) else d
print(' '.join(str(d[k]) for k in sys.argv[1:]))
" "$@"; }

echo "########## A. task-detail 协作弹窗 ##########"
$AB open "$BASE/task-detail.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0
$AB click '[data-td-coop]' >/dev/null 2>&1
sleep 0.8

rec A1 "$(ev 'JSON.stringify((function(){var c=Q(".td-coop .giencoder-modal-content");return{cls:c.className,bg:CS(c,"backgroundColor"),bgToken:RR(document.documentElement,"--color-bg-5"),borderColor:CS(c,"borderTopColor"),borderWidth:CS(c,"borderTopWidth"),radius:CS(c,"borderTopLeftRadius"),border1:RR(document.documentElement,"--color-border-1"),border2:RR(document.documentElement,"--color-border-2"),fs:CS(c,"fontSize")};})())')"

rec A2 "$(ev 'JSON.stringify((function(){var t=Q(".td-coop-dvd-tx");return{exists:!!t,txt:t.textContent,fs:CS(t,"fontSize"),lh:CS(t,"lineHeight"),color:CS(t,"color"),rect:R(t)};})())')"

rec A3 "$(ev 'JSON.stringify((function(){var out=[];QA(".td-coop *").forEach(function(e){if(e.children.length===0&&e.textContent.trim()){out.push({cls:e.className||e.tagName,fs:CS(e,"fontSize"),fw:CS(e,"fontWeight"),tx:e.textContent.trim().slice(0,14)})}});return out;})())')"

rec A4 "$(ev 'JSON.stringify((function(){var si=QA("[data-td-step]");var g=function(e){var s=CS(e,"clipPath");return{rect:R(e),clip:s,padding:CS(e,"padding"),margin:CS(e,"margin"),border:CS(e,"borderTopWidth")+" "+CS(e,"borderTopColor"),bg:CS(e,"backgroundColor")}};return{g0:g(si[0]),g1:g(si[1]),wrap:R(Q(".td-coop .giencoder-steps"))};})())')"
$AB screenshot "$OUT/a-coop-step1.png" >/dev/null 2>&1

$AB click '[data-td-coop-next]' >/dev/null 2>&1
sleep 0.6
$AB screenshot "$OUT/a-coop-step2.png" >/dev/null 2>&1
$AB press Escape >/dev/null 2>&1
sleep 0.5

echo "########## B. kanban 卡片 ##########"
$AB open "$BASE/kanban.html" >/dev/null 2>&1
sleep 3.5
rec B1 "$(ev 'JSON.stringify((function(){var lanes=QA(".kb-col");var out=lanes.map(function(l){return{name:(l.querySelector(".kb-col-name")||{}).textContent||"",cls:l.className,cards:l.querySelectorAll(".kb-card").length}});return out;})())')"

rec B2 "$(ev 'JSON.stringify((function(){var d=QA(".kb-card.is-dashed")[0];if(!d)return{found:false};var r=d.querySelector(".kb-card-dash rect");var l=d.closest(".kb-col");return{found:true,rect:R(d),lane:(l.querySelector(".kb-col-name")||{}).textContent,cardCls:d.className,title:(d.querySelector(".kb-card-title")||{}).textContent,svgCls:d.querySelector(".kb-card-dash").className,rectFill:CS(r,"fill"),rectStroke:CS(r,"stroke"),rectSW:CS(r,"strokeWidth"),rectDash:CS(r,"strokeDasharray"),w6:RR(document.documentElement,"--color-warning-6"),w5:RR(document.documentElement,"--color-warning-5"),o6:RR(document.documentElement,"--orange-6"),o5:RR(document.documentElement,"--orange-5"),o4:RR(document.documentElement,"--orange-4"),o3:RR(document.documentElement,"--orange-3"),w4:RR(document.documentElement,"--color-warning-4"),wL2:RR(document.documentElement,"--color-warning-light-2")};})())')"

rec B3 "$(ev 'JSON.stringify((function(){var t=QA(".kb-card-title")[0];return{cls:t.className,fw:CS(t,"fontWeight"),fs:CS(t,"fontSize"),tx:t.textContent.trim().slice(0,20)};})())')"

echo "  -- hover 第一张非虚线卡 --"
PT=$($AB eval "$HELP JSON.stringify(C(QA('.kb-card:not(.is-dashed)')[0]))" 2>&1 | tail -1)
read PX PY <<< "$(printf '%s' "$PT" | nums x y)"
$AB mouse move "$PX" "$PY" >/dev/null 2>&1; sleep 0.5
rec B4 "$(ev 'JSON.stringify((function(){var c=QA(".kb-card:not(.is-dashed)")[0];var t=c.querySelector(".kb-card-title");return{fw:CS(t,"fontWeight"),borderColor:CS(c,"borderTopColor"),cardH:R(c)[3],titleRect:R(t)};})())')"
$AB screenshot "$OUT/b-kanban-hover.png" >/dev/null 2>&1

echo "  -- hover 虚线卡（进行中第一张） --"
PT2=$($AB eval "$HELP JSON.stringify(C(Q('.kb-card.is-dashed')))" 2>&1 | tail -1)
read PX2 PY2 <<< "$(printf '%s' "$PT2" | nums x y)"
$AB mouse move "$PX2" "$PY2" >/dev/null 2>&1; sleep 0.5
rec B5 "$(ev 'JSON.stringify((function(){var c=Q(".kb-card.is-dashed"),t=c.querySelector(".kb-card-title");return{fw:CS(t,"fontWeight"),stroke:CS(c.querySelector(".kb-card-dash rect"),"stroke"),titleTx:t.textContent.trim().slice(0,20)};})())')"
$AB screenshot "$OUT/b-kanban-dashed-hover.png" >/dev/null 2>&1

echo "########## C. base.html main 背景 ##########"
$AB open "$BASE/base.html" >/dev/null 2>&1
sleep 4.0
rec C1 "$(ev 'JSON.stringify((function(){var m=Q("main");return{exists:!!m,rect:R(m),bg:CS(m,"backgroundColor"),bgImg:CS(m,"backgroundImage").slice(0,300),cls:m.className,clsMap:CS(m,"background")};})())')"

rec C2 "$(ev 'JSON.stringify((function(){var m=Q("main");var out=[];QA("main *").forEach(function(e){var bg=CS(e,"backgroundImage");var bc=CS(e,"backgroundColor");if((bg&&bg!=="none")||(bc&&bc!=="rgba(0, 0, 0, 0)"&&bc!=="transparent")){out.push({tag:e.tagName,cls:(e.className||"").toString().slice(0,80),rect:R(e),pos:CS(e,"position"),bgImg:bg.slice(0,200),bgColor:bc,filter:CS(e,"filter").slice(0,60),opacity:CS(e,"opacity"),blend:CS(e,"mixBlendMode")})}});return out.slice(0,40);})())')"

rec C3 "$(ev 'JSON.stringify((function(){var m=Q("main");return{children:Array.prototype.map.call(m.children,function(e){return{tag:e.tagName,cls:(e.className||"").toString().slice(0,90),rect:R(e),pos:CS(e,"position"),bgImg:CS(e,"backgroundImage").slice(0,160)}})}})())')"
$AB screenshot "$OUT/c-base.png" >/dev/null 2>&1

echo ""
echo "================ probe33a.jsonl ================"
wc -l "$PROBE"

#!/usr/bin/env bash
# 第33轮 B 段追问：为什么详情页 .kb-crt 只有 712 宽（看板 1138）？
# 量：main 个数/几何/定位、shell 侧边栏、div:has(>main)、.kb-crt 自身几何、--kb-crt-width 解析值
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r33/probe33b.jsonl"
: > "$OUT"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CS=function(e,p){return e?getComputedStyle(e)[p]:null},RR=function(e,p){return e?getComputedStyle(e).getPropertyValue(p).trim():null};'

rec() {
  "$P" -c "
import json,sys
step=sys.argv[1]; raw=sys.argv[2]
try:
    d=json.loads(raw)
    if isinstance(d,str): d=json.loads(d)
except Exception as e:
    d={'__parse_error__':str(e),'raw':raw[:400]}
print(json.dumps({'step':step,'data':d},ensure_ascii=False))
" "$1" "$2" >> "$OUT"
}
ev() { "$AB" eval "$HELP $1" 2>&1 | tail -1; }

GEO='(function(){var ms=QA("main");return{mainCount:ms.length,mains:ms.map(function(m){return{rect:R(m),pos:CS(m,"position"),disp:CS(m,"display"),w:CS(m,"width"),h:CS(m,"height"),maxW:CS(m,"maxWidth"),pad:CS(m,"padding"),tf:CS(m,"transform"),cls:(m.className||"").toString().slice(0,120),parentTag:m.parentElement.tagName,parentRect:R(m.parentElement),parentPad:CS(m.parentElement,"padding"),parentCls:(m.parentElement.className||"").toString().slice(0,90)}})};})()'

echo "########## KANBAN 基准 ##########"
$AB open "$BASE/kanban.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.5
rec K_geo "$(ev "JSON.stringify($GEO)")"
rec K_aside "$(ev 'JSON.stringify((function(){var a=QA("aside");return a.map(function(e){return{disp:CS(e,"display"),rect:R(e),cls:(e.className||"").toString().slice(0,70)}});})())')"
$AB click '.kb-create' >/dev/null 2>&1
sleep 0.9
rec K_crt "$(ev 'JSON.stringify((function(){var m=Q(".kb-crt"),d=Q(".kb-crt-dialog");return{crt:R(m),crtPos:CS(m,"position"),crtInset:CS(m,"top")+"|"+CS(m,"left")+"|"+CS(m,"right")+"|"+CS(m,"bottom"),varW:RR(m,"--kb-crt-width"),dlgW:CS(d,"width"),dlgRect:R(d),host:(m.parentElement.className||"").toString().slice(0,90)};})())')"
$AB press Escape >/dev/null 2>&1
sleep 0.4

echo "########## TASK-DETAIL ##########"
$AB open "$BASE/task-detail.html" >/dev/null 2>&1
sleep 3.5
rec D_geo "$(ev "JSON.stringify($GEO)")"
rec D_aside "$(ev 'JSON.stringify((function(){var a=QA("aside");return a.map(function(e){return{disp:CS(e,"display"),rect:R(e),cls:(e.className||"").toString().slice(0,70)}});})())')"
rec D_wrap "$(ev 'JSON.stringify((function(){var w=Q(".td-wrap"),r=Q(".td-root");return{wrap:R(w),root:R(r),mainRect:R(Q("main")),mainPad:CS(Q("main"),"padding")};})())')"
$AB click '[data-td-edit]' >/dev/null 2>&1
sleep 0.9
rec D_crt "$(ev 'JSON.stringify((function(){var m=Q(".kb-crt"),d=Q(".kb-crt-dialog");return{crt:R(m),crtPos:CS(m,"position"),offsets:(function(){var s=CS(m,"top")+"|"+CS(m,"left")+"|"+CS(m,"right")+"|"+CS(m,"bottom");return s})(),varW:RR(m,"--kb-crt-width"),dlgW:CS(d,"width"),dlgRect:R(d),host:(m.parentElement.className||"").toString().slice(0,90),hostRect:R(m.parentElement)};})())')"
$AB screenshot "mg-work/r33/shots/B2-edit.png" >/dev/null 2>&1
$AB press Escape >/dev/null 2>&1
sleep 0.4

echo "OK"
cat "$OUT"

#!/usr/bin/env bash
# 第 36 轮验证：7 项需求逐项实测。整条链路必须在一次 bash 调用内跑完。
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r36/probe36.jsonl"
SHOT="mg-work/r36/shots"
mkdir -p "$SHOT"; : > "$OUT"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CS=function(e,p){return e?getComputedStyle(e)[p]:null};'

rec() { "$P" -c "
import json,sys
step=sys.argv[1]; raw=sys.argv[2]
try:
    d=json.loads(raw)
    if isinstance(d,str): d=json.loads(d)
except Exception as e:
    d={'__parse_error__':str(e),'raw':raw[:400]}
print(json.dumps({'step':step,'data':d},ensure_ascii=False))
" "$1" "$2" >> "$OUT"; }

ev() { "$AB" eval "$HELP $1" 2>&1 | tail -1; }

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 5

# ---------- 1 / 3 / 2 / 6 / 7：静态样式 ----------
rec styles "$(ev 'JSON.stringify((function(){
 var out={};
 var c=Q(".av-card"); var cs=getComputedStyle(c);
 out.card={radius:cs.borderRadius,border:cs.borderTopColor,w:cs.width,h:cs.height,overflow:cs.overflow};
 var h=Q(".av-card .giencoder-card-header"); out.header={bg:getComputedStyle(h).backgroundColor,h:Math.round(h.getBoundingClientRect().height)};
 out.thumbsLeft=QA(".av-card-thumb").length;
 out.bodies=QA(".av-card .giencoder-card-body").map(function(e){var s=getComputedStyle(e);return {ovf:s.overflowY,sh:e.scrollHeight,ch:e.clientHeight,scrollable:e.scrollHeight>e.clientHeight};});
 out.para=(function(){var p=Q(".av-para");return p?getComputedStyle(p).color:null})();
 out.btns=QA(".av-main-head-actions button").map(function(b){return {t:b.textContent.trim(),c:getComputedStyle(b).color}});
 out.links=QA(".av-link").map(function(e){return {t:e.textContent.trim(),c:getComputedStyle(e).color,b:R(e)}});
 out.root_var=getComputedStyle(document.documentElement).getPropertyValue("--av-chat-w");
 return out;})())')"

# ---------- 5：打开侧栏，检查是否 main 的同级 ----------
rec closed "$(ev 'JSON.stringify((function(){
 var d=Q("#av-chat-drawer");var r=d.getBoundingClientRect();
 return {parent:String(d.parentElement.tagName)+"."+String(d.parentElement.className).slice(0,60),open:document.documentElement.hasAttribute("data-av-chat-open"),rect:R(d),visibility:getComputedStyle(d).visibility,width:getComputedStyle(d).width,maskLeft:QA(".av-chat-mask").length,gutterLeft:QA("[data-av-chat-gutter]").length};})())')"

"$AB" eval "$HELP Q('[data-av-chat-toggle]').click(); 'clicked'" >/dev/null 2>&1
sleep 1.2

rec opened "$(ev 'JSON.stringify((function(){
 var d=Q("#av-chat-drawer"),m=Q("main"),g=Q("[data-av-chat-gutter]");
 var dr=d.getBoundingClientRect(),mr=m.getBoundingClientRect(),gr=g?g.getBoundingClientRect():null;
 return {parentCls:String(d.parentElement.className).slice(0,80),
   drawerParentIsMainRow: d.parentElement===m.parentElement,
   order: Array.prototype.slice.call(d.parentElement.children).map(function(e){return e.tagName}),
   main:[Math.round(mr.left),Math.round(mr.top),Math.round(mr.width),Math.round(mr.height)],
   drawer:[Math.round(dr.left),Math.round(dr.top),Math.round(dr.width),Math.round(dr.height)],
   gutter:gr?[Math.round(gr.left),Math.round(gr.top),Math.round(gr.width),Math.round(gr.height)]:null,
   gap: g?Math.round(dr.left-(gr.left+gr.width)):null,
   gapMain: g?Math.round(gr.left-mr.right):null,
   drawerRadius:getComputedStyle(d).borderRadius,
   drawerShadow:getComputedStyle(d).boxShadow,
   maskLeft:QA(".av-chat-mask").length,
   open:document.documentElement.hasAttribute("data-av-chat-open")};})())')"

"$AB" screenshot "$SHOT/36-open.png" >/dev/null 2>&1

# ---------- 5b：拖动把手拉伸 ----------
"$AB" eval "$HELP JSON.stringify((function(){var g=Q('[data-av-chat-gutter]');var r=g.getBoundingClientRect();window.__g=[Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)];return window.__g})())" >/dev/null 2>&1
GB=$("$AB" eval "$HELP JSON.stringify(window.__g)" 2>&1 | tail -1)
GX=$("$P" -c "import json,sys;d=json.loads(sys.argv[1]);print(d[0] if isinstance(d,list) else json.loads(d)[0])" "$GB")
GY=$("$P" -c "import json,sys;d=json.loads(sys.argv[1]);print(d[1] if isinstance(d,list) else json.loads(d)[1])" "$GB")
"$AB" mouse move "$GX" "$GY" >/dev/null 2>&1
sleep 0.3
"$AB" mouse down >/dev/null 2>&1
"$AB" mouse move "$((GX-140))" "$GY" >/dev/null 2>&1
sleep 0.4
"$AB" mouse up >/dev/null 2>&1
sleep 0.6

rec resized "$(ev 'JSON.stringify((function(){
 var d=Q("#av-chat-drawer"),m=Q("main"),g=Q("[data-av-chat-gutter]");
 var dr=d.getBoundingClientRect(),mr=m.getBoundingClientRect(),gr=g.getBoundingClientRect();
 return {mainW:Math.round(mr.width),drawerW:Math.round(dr.width),gap:Math.round(dr.left-(gr.left+gr.width)),total:Math.round(mr.width)+Math.round(gr.width)+Math.round(dr.width),
   cursor:getComputedStyle(g).cursor, cssVar:getComputedStyle(document.documentElement).getPropertyValue("--av-chat-w")};})())')"
"$AB" screenshot "$SHOT/36-resized.png" >/dev/null 2>&1

# ---------- 4：链接 hover ----------
for i in 0 1 2 3 4 5 6 7; do
  C=$("$AB" eval "$HELP JSON.stringify((function(){var e=QA('.av-link')[$i];if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)]})())" 2>&1 | tail -1)
  XY=$("$P" -c "import json,sys;d=json.loads(sys.argv[1]);d=json.loads(d) if isinstance(d,str) else d;print(('%d %d'%tuple(d)) if d else '')" "$C")
  [ -z "$XY" ] && continue
  "$AB" mouse move ${XY% *} ${XY#* } >/dev/null 2>&1
  sleep 0.35
  rec "hover$i" "$(ev "JSON.stringify((function(){var e=QA('.av-link')[$i];return {t:e.textContent.trim(),c:getComputedStyle(e).color,hover:e.matches(':hover')}})())")"
done

echo "=== 原始数据 ==="
cat "$OUT"

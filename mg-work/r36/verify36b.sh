#!/usr/bin/env bash
# 第 36 轮验证（第二段）：侧栏内部链接 hover / 全屏 / 窄宽换行 / 拖动边界 / Esc
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r36/probe36b.jsonl"
SHOT="mg-work/r36/shots"
mkdir -p "$SHOT"; : > "$OUT"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CS=function(e,p){return e?getComputedStyle(e)[p]:null},CX=function(e){var r=e.getBoundingClientRect();return [Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)]};'
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
# 把某个选择器下标元素滚进视野并 hover，返回其 hover 后的 color
hover_at() { # $1 selectors-js-expr  $2 index  $3 label
  local C XY
  C=$(ev "JSON.stringify((function(){var e=$1[$2];if(!e)return null;e.scrollIntoView({block:'center'});var r=e.getBoundingClientRect();return [Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)]})())")
  XY=$("$P" -c "import json,sys;d=json.loads(sys.argv[1]);d=json.loads(d) if isinstance(d,str) else d;print(('%d %d'%tuple(d)) if d else '')" "$C")
  [ -z "$XY" ] && { rec "$3" 'null'; return; }
  "$AB" mouse move ${XY% *} ${XY#* } >/dev/null 2>&1
  sleep 0.35
  rec "$3" "$(ev "JSON.stringify((function(){var e=$1[$2];return {t:e.textContent.trim().slice(0,20),c:getComputedStyle(e).color,hover:e.matches(':hover')}})())")"
}

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 5

# 行卡里的两个链接（在视口下方，先滚动）
hover_at "QA('.av-link')" 5 "avlink5"
hover_at "QA('.av-link')" 6 "avlink6"
hover_at "QA('.av-link')" 7 "avlink7"

# 打开侧栏
ev 'Q("[data-av-chat-toggle]").click();1' >/dev/null 2>&1
sleep 1.0

# 侧栏内部链接
hover_at "QA('.td-ai-meta a')" 0 "chatmeta0"
hover_at "QA('.td-ai-meta a')" 1 "chatmeta1"
rec fileHover "$(ev 'JSON.stringify((function(){
 var a=Q(\".av-chat-drawer .td-file\"); if(!a) return null;
 var tx=a.querySelector(\".td-file-tx\");
 var before=getComputedStyle(tx).color;
 return {before:before};})())')"
hover_at "QA('.av-chat-drawer .td-file')" 0 "chatfileHover"
rec fileTx "$(ev 'JSON.stringify((function(){var a=Q(\".av-chat-drawer .td-file\");return {tx:getComputedStyle(a.querySelector(\".td-file-tx\")).color, bg:getComputedStyle(a).backgroundColor, hover:a.matches(\":hover\")}})())')"

# 窄宽：拖到最小 → 头部动作区应换行（@container）
ev 'document.documentElement.style.setProperty("--av-chat-w","900px");1' >/dev/null 2>&1
sleep 0.6
rec narrow "$(ev 'JSON.stringify((function(){
 var m=Q("main"),w=Q(".av-main"),a=Q(".av-main-head-actions"),i=Q(".av-main-head-info");
 var ar=a.getBoundingClientRect(),ir=i.getBoundingClientRect(),mr=m.getBoundingClientRect();
 var c=Q(".av-card .giencoder-card-body");
 return {mainW:Math.round(mr.width),avW:Math.round(w.getBoundingClientRect().width),
   actions:R(a),info:R(i),actionsPosition:getComputedStyle(a).position,
   overlap:(ar.left<ir.right-1 && ar.top<ir.bottom-1 && ar.bottom>ir.top+1),
   cardsScroll:QA(".av-card .giencoder-card-body").map(function(e){return e.scrollHeight>e.clientHeight}),
   cardW:Math.round(Q(".av-card").getBoundingClientRect().width)};})())')"
"$AB" screenshot "$SHOT/36-narrow.png" >/dev/null 2>&1

# 拖动边界：拉到最小 / 最大
ev 'document.documentElement.style.setProperty("--av-chat-w","480px");1' >/dev/null 2>&1
sleep 0.4
G=$(ev 'JSON.stringify(CX(Q("[data-av-chat-gutter]")))')
GX=$("$P" -c "import json,sys;d=json.loads(sys.argv[1]);d=json.loads(d) if isinstance(d,str) else d;print(d[0])" "$G")
GY=$("$P" -c "import json,sys;d=json.loads(sys.argv[1]);d=json.loads(d) if isinstance(d,str) else d;print(d[1])" "$G")
# 使劲往右拖 → 应钳到 MIN_W=360
$AB mouse move "$GX" "$GY" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
$AB mouse move "$((GX+600))" "$GY" >/dev/null 2>&1; sleep 0.4; $AB mouse up >/dev/null 2>&1; sleep 0.6
rec dragMin "$(ev 'JSON.stringify((function(){var m=Q("main"),g=Q("[data-av-chat-gutter]"),d=Q("#av-chat-drawer");return {mainW:Math.round(m.getBoundingClientRect().width),drawerW:Math.round(d.getBoundingClientRect().width),varW:getComputedStyle(document.documentElement).getPropertyValue("--av-chat-w")}})())')"
# 使劲往左拖 → 应钳到 main 最小宽
G=$(ev 'JSON.stringify(CX(Q("[data-av-chat-gutter]")))')
GX=$("$P" -c "import json,sys;d=json.loads(sys.argv[1]);d=json.loads(d) if isinstance(d,str) else d;print(d[0])" "$G")
GY=$("$P" -c "import json,sys;d=json.loads(sys.argv[1]);d=json.loads(d) if isinstance(d,str) else d;print(d[1])" "$G")
$AB mouse move "$GX" "$GY" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
$AB mouse move "$((GX-900))" "$GY" >/dev/null 2>&1; sleep 0.4; $AB mouse up >/dev/null 2>&1; sleep 0.6
rec dragMax "$(ev 'JSON.stringify((function(){var m=Q("main"),g=Q("[data-av-chat-gutter]"),d=Q("#av-chat-drawer");var mr=m.getBoundingClientRect(),gr=g.getBoundingClientRect(),dr=d.getBoundingClientRect();return {mainW:Math.round(mr.width),drawerW:Math.round(dr.width),varW:getComputedStyle(document.documentElement).getPropertyValue("--av-chat-w"),overflow:Math.round(dr.right)>Math.round(m.parentElement.getBoundingClientRect().right)}})())')"

# 全屏
ev 'Q("[data-td-fullscreen]").click();1' >/dev/null 2>&1
sleep 0.8
rec fullscreen "$(ev 'JSON.stringify((function(){var d=Q("#av-chat-drawer"),m=Q("main");return {isFs:d.classList.contains("is-fullscreen"),drawer:R(d),mainDisplay:getComputedStyle(m).display,gutterDisplay:getComputedStyle(Q("[data-av-chat-gutter]")).display}})())')"
"$AB" screenshot "$SHOT/36-fullscreen.png" >/dev/null 2>&1
ev 'Q("[data-td-fullscreen]").click();1' >/dev/null 2>&1
sleep 0.6

# Esc 关侧栏
ev 'document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true})) || window.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}));1' >/dev/null 2>&1
sleep 0.7
rec afterEsc "$(ev 'JSON.stringify((function(){var d=Q("#av-chat-drawer");return {open:document.documentElement.hasAttribute("data-av-chat-open"),visibility:getComputedStyle(d).visibility,width:getComputedStyle(d).width,gutterDisplay:getComputedStyle(Q("[data-av-chat-gutter]")).display,main:Math.round(Q("main").getBoundingClientRect().width)}})())')"

echo "=== 原始数据 ==="
cat "$OUT"

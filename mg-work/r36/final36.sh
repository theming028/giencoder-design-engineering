#!/usr/bin/env bash
# 第 36 轮最终验收：7 项一并复测 + 出图
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r36/final.jsonl"; SHOT="mg-work/r36/shots"
mkdir -p "$SHOT"; : > "$OUT"
HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CX=function(e){var r=e.getBoundingClientRect();return [Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)]};'
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
xy() { "$P" -c "
import json,sys
d=json.loads(sys.argv[1]); d=json.loads(d) if isinstance(d,str) else d
print('%d %d'%(d[0],d[1]))" "$(ev "JSON.stringify(CX($1))")"; }

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 5

# 默认态（侧栏关闭）
rec default "$(ev 'JSON.stringify((function(){
 var c=Q(".av-card"),cs=getComputedStyle(c);
 return {cardRadius:cs.borderRadius,cardBorder:cs.borderTopColor,
  headerBg:getComputedStyle(Q(".av-card .giencoder-card-header")).backgroundColor,
  rowRadius:getComputedStyle(Q(".av-row")).borderRadius,rowBorder:getComputedStyle(Q(".av-row")).borderTopColor,
  para:getComputedStyle(Q(".av-para")).color,
  btnColors:QA(".av-main-head-actions button").map(function(b){return getComputedStyle(b).color}),
  thumbsLeft:QA(".av-card-thumb").length,
  bodyOverflow:getComputedStyle(Q(".av-card .giencoder-card-body")).overflowY,
  drawerParent:String(Q("#av-chat-drawer").parentElement.className).slice(0,50),
  drawerVis:getComputedStyle(Q("#av-chat-drawer")).visibility,
  mainW:Math.round(Q("main").getBoundingClientRect().width)};})())')"
$AB screenshot "$SHOT/36-final-closed.png" >/dev/null 2>&1

# 打开
ev 'Q("[data-av-chat-toggle]").click();1' >/dev/null 2>&1
sleep 1.2
rec open "$(ev 'JSON.stringify((function(){var d=Q("#av-chat-drawer"),m=Q("main"),g=Q("[data-av-chat-gutter]");
 var dr=d.getBoundingClientRect(),mr=m.getBoundingClientRect(),gr=g.getBoundingClientRect();
 return {sibling:d.parentElement===m.parentElement,order:Array.prototype.slice.call(d.parentElement.children).map(function(e){return e.tagName}),
  mainW:Math.round(mr.width),drawerW:Math.round(dr.width),gutterW:Math.round(gr.width),
  gapMainToGutter:Math.round(gr.left-mr.right),gapGutterToDrawer:Math.round(dr.left-gr.right),
  masks:QA(".av-chat-mask").length};})())')"
$AB screenshot "$SHOT/36-final-open.png" >/dev/null 2>&1

# 拉宽到极限
set -- $(xy 'Q("[data-av-chat-gutter]")')
$AB mouse move "$1" "$2" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
$AB mouse move "$(( $1 - 900 ))" "$2" >/dev/null 2>&1; sleep 0.45; $AB mouse up >/dev/null 2>&1; sleep 0.6
rec widen "$(ev 'JSON.stringify((function(){var tb=Q(".td-composer .mt-auto");
 return {mainW:Math.round(Q("main").getBoundingClientRect().width),drawerW:Math.round(Q("#av-chat-drawer").getBoundingClientRect().width),
  varW:getComputedStyle(document.documentElement).getPropertyValue("--av-chat-w"),
  toolbarOverflow:tb.scrollWidth-tb.clientWidth,
  headStatic:getComputedStyle(Q(".av-main-head-actions")).position};})())')"
$AB screenshot "$SHOT/36-final-widest.png" >/dev/null 2>&1

# 收窄到极限
set -- $(xy 'Q("[data-av-chat-gutter]")')
$AB mouse move "$1" "$2" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
$AB mouse move "$(( $1 + 900 ))" "$2" >/dev/null 2>&1; sleep 0.45; $AB mouse up >/dev/null 2>&1; sleep 0.6
rec narrow "$(ev 'JSON.stringify((function(){var tb=Q(".td-composer .mt-auto");
 return {mainW:Math.round(Q("main").getBoundingClientRect().width),drawerW:Math.round(Q("#av-chat-drawer").getBoundingClientRect().width),
  varW:getComputedStyle(document.documentElement).getPropertyValue("--av-chat-w"),
  toolbarOverflow:tb.scrollWidth-tb.clientWidth,textareaW:Math.round(Q(".td-composer textarea").getBoundingClientRect().width)};})())')"
$AB screenshot "$SHOT/36-final-narrowest.png" >/dev/null 2>&1

echo "=== 最终数据 ==="; cat "$OUT"

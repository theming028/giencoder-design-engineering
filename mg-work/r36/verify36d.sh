#!/usr/bin/env bash
# 第 36 轮验证（第四段）：拖动钳位 / MIN_W 下输入区 / 侧栏文件卡 hover 转蓝
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r36/probe36d.jsonl"; SHOT="mg-work/r36/shots"
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
xy() { # $1 = selector js expr ; echoes "X Y"
  "$P" -c "
import json,sys
d=json.loads(sys.argv[1]); d=json.loads(d) if isinstance(d,str) else d
print('%d %d'%(d[0],d[1]))" "$(ev "JSON.stringify(CX($1))")"
}
drag() { # $1 起点X $2 起点Y $3 目标X
  $AB mouse move "$1" "$2" >/dev/null 2>&1
  $AB mouse down >/dev/null 2>&1
  $AB mouse move "$3" "$2" >/dev/null 2>&1
  sleep 0.45
  $AB mouse up >/dev/null 2>&1
  sleep 0.6
}

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 5
ev 'Q("[data-av-chat-toggle]").click();1' >/dev/null 2>&1
sleep 1.2

echo "--- 拉宽到极限（拖把手指针向左 900px）---"
set -- $(xy 'Q("[data-av-chat-gutter]")'); drag "$1" "$2" "$(( $1 - 900 ))"
rec dragMax "$(ev 'JSON.stringify((function(){var m=Q("main"),d=Q("#av-chat-drawer"),g=Q("[data-av-chat-gutter]");
 var tb=Q(".td-composer .mt-auto");
 return {mainW:Math.round(m.getBoundingClientRect().width),drawerW:Math.round(d.getBoundingClientRect().width),
   gap:Math.round(g.getBoundingClientRect().width),varW:getComputedStyle(document.documentElement).getPropertyValue("--av-chat-w"),
   toolbarOverflow:tb?tb.scrollWidth-tb.clientWidth:null,textareaW:Math.round(Q(".td-composer textarea").getBoundingClientRect().width)};})())')"

echo "--- 收窄到极限（拖把手指针向右 900px）---"
set -- $(xy 'Q("[data-av-chat-gutter]")'); drag "$1" "$2" "$(( $1 + 900 ))"
rec dragMin "$(ev 'JSON.stringify((function(){var m=Q("main"),d=Q("#av-chat-drawer");
 var tb=Q(".td-composer .mt-auto");
 return {mainW:Math.round(m.getBoundingClientRect().width),drawerW:Math.round(d.getBoundingClientRect().width),
   varW:getComputedStyle(document.documentElement).getPropertyValue("--av-chat-w"),
   toolbarOverflow:tb?tb.scrollWidth-tb.clientWidth:null,toolbarScrollW:tb?tb.scrollWidth:null,toolbarClientW:tb?tb.clientWidth:null,
   textareaW:Math.round(Q(".td-composer textarea").getBoundingClientRect().width),
   composerR:R(Q(".td-composer")),toolbarR:R(tb)};})())')"
$AB screenshot "$SHOT/36-min.png" >/dev/null 2>&1

echo "--- 侧栏文件卡 hover ---"
set -- $(xy 'Q(".av-chat-drawer .td-file")')
rec fileRest "$(ev 'JSON.stringify((function(){var a=Q(".av-chat-drawer .td-file");return {tx:getComputedStyle(a.querySelector(".td-file-tx")).color,bg:getComputedStyle(a).backgroundColor}})())')"
$AB mouse move "$1" "$2" >/dev/null 2>&1
sleep 0.45
rec fileHover "$(ev 'JSON.stringify((function(){var a=Q(".av-chat-drawer .td-file");return {hover:a.matches(":hover"),tx:getComputedStyle(a.querySelector(".td-file-tx")).color,bg:getComputedStyle(a).backgroundColor}})())')"

echo "--- 复位（双击把手）---"
$AB mouse move "$1" "$2" >/dev/null 2>&1
$AB dblclick 2>/dev/null || true
echo "=== 原始数据 ==="; cat "$OUT"

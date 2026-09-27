#!/usr/bin/env bash
# 第 36 轮验证（第三段）：拖动钳位 / 最小宽下输入区是否破版 / 侧栏文件卡 hover / 行卡圆角
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r36/probe36c.jsonl"; SHOT="mg-work/r36/shots"
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
jget() { "$P" -c "import json,sys;d=json.loads(sys.argv[1]);d=json.loads(d) if isinstance(d,str) else d;print(d[sys.argv[2]])" "$1" "$2"; }

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 5
ev 'Q("[data-av-chat-toggle]").click();1' >/dev/null 2>&1
sleep 1.0

# --- 拖到最左（拉宽）→ 应钳到 main 最小宽 ---
GX=$(jget "$(ev 'JSON.stringify(CX(Q("[data-av-chat-gutter]")))')" 0)
GY=$(jget "$(ev 'JSON.stringify(CX(Q("[data-av-chat-gutter]")))')" 1)
$AB mouse move "$GX" "$GY" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
$AB mouse move "$((GX-900))" "$GY" >/dev/null 2>&1; sleep 0.4; $AB mouse up >/dev/null 2>&1; sleep 0.6
rec dragMax "$(ev 'JSON.stringify((function(){var m=Q("main"),g=Q("[data-av-chat-gutter]"),d=Q("#av-chat-drawer");
 var mr=m.getBoundingClientRect(),gr=g.getBoundingClientRect(),dr=d.getBoundingClientRect();
 var tb=Q(".td-composer .mt-auto");
 return {mainW:Math.round(mr.width),drawerW:Math.round(dr.width),gap:Math.round(gr.width),
   varW:getComputedStyle(document.documentElement).getPropertyValue("--av-chat-w"),
   composerR:R(Q(".td-composer")),
   toolbarOverflow: tb? tb.scrollWidth-tb.clientWidth : null,
   textareaR:R(Q(".td-composer textarea"))};})())')"

# --- 拖到最右（收窄）→ 应钳到 MIN_W，并检查输入区是否破版 ---
GX=$(jget "$(ev 'JSON.stringify(CX(Q("[data-av-chat-gutter]")))')" 0)
GY=$(jget "$(ev 'JSON.stringify(CX(Q("[data-av-chat-gutter]")))')" 1)
$AB mouse move "$GX" "$GY" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
$AB mouse move "$((GX+900))" "$GY" >/dev/null 2>&1; sleep 0.4; $AB mouse up >/dev/null 2>&1; sleep 0.6
rec dragMin "$(ev 'JSON.stringify((function(){var d=Q("#av-chat-drawer"),m=Q("main");
 var tb=Q(".td-composer .mt-auto");
 return {mainW:Math.round(m.getBoundingClientRect().width),drawerW:Math.round(d.getBoundingClientRect().width),
   varW:getComputedStyle(document.documentElement).getPropertyValue("--av-chat-w"),
   composerR:R(Q(".td-composer")), toolbar:R(tb),
   toolbarOverflow: tb? tb.scrollWidth-tb.clientWidth : null,
   toolbarScrollW: tb? tb.scrollWidth : null, toolbarClientW: tb? tb.clientWidth : null,
   textareaR:R(Q(".td-composer textarea")),
   hasStdSelect:(function(){var s=QA(".td-composer .giencoder-select");return s.map(function(e){return getComputedStyle(e).display})})()};})())')"
$AB screenshot "$SHOT/36-min.png" >/dev/null 2>&1

# --- 侧栏文件卡 hover：文字是否转主题蓝 ---
GX=$(jget "$(ev 'JSON.stringify(CX(Q(".av-chat-drawer .td-file")))')" 0)
GY=$(jget "$(ev 'JSON.stringify(CX(Q(".av-chat-drawer .td-file")))')" 1)
$AB mouse move "$GX" "$GY" >/dev/null 2>&1
sleep 0.4
rec fileTx "$(ev 'JSON.stringify((function(){var a=Q(".av-chat-drawer .td-file");var tx=a.querySelector(".td-file-tx");
 return {hover:a.matches(":hover"),txColor:getComputedStyle(tx).color,bg:getComputedStyle(a).backgroundColor};})())')"

# --- 行卡：圆角 / 边框 ---
rec rows "$(ev 'JSON.stringify(QA(".av-row").map(function(e){var s=getComputedStyle(e);return {radius:s.borderRadius,border:s.borderTopColor}}))')"
rec cardAgain "$(ev 'JSON.stringify((function(){var s=getComputedStyle(Q(".av-card"));return {radius:s.borderRadius,border:s.borderTopColor,headerBg:getComputedStyle(Q(".av-card .giencoder-card-header")).backgroundColor}})())')"

echo "=== 原始数据 ==="; cat "$OUT"

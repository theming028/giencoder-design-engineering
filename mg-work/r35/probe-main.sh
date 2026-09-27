#!/usr/bin/env bash
# 第 35 轮第 2 项实测：数字分身主内容还原（设计稿 1345:18487，内容宽 860px）
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r35/probe-main.jsonl"
SHOT="mg-work/r35/shots"
mkdir -p "$SHOT"; : > "$OUT"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CS=function(e,p){return e?getComputedStyle(e)[p]:null},REL=function(e,base){if(!e||!base)return null;var r=e.getBoundingClientRect(),b=base.getBoundingClientRect();return [Math.round(r.left-b.left),Math.round(r.top-b.top),Math.round(r.width),Math.round(r.height)]};'

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

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.5

# 主内容是否已挂载
rec mounted "$(ev 'JSON.stringify((function(){var h=Q(".av-main");return{host:!!h,ready:h?h.getAttribute("data-av-main-ready"):null,cards:QA(".av-card").length,rows:QA(".av-row").length,links:QA(".av-link").length,trigger:!!Q("[data-av-chat-toggle]")};})())')"

# 关键盒子（绝对）
rec boxes "$(ev 'JSON.stringify((function(){var m=Q(".av-main");return{main:R(m),head:R(Q(".av-main-head")),avatar:R(Q(".av-main-avatar")),nameRow:R(Q(".av-main-name-row")),created:R(Q(".av-main-created")),desc:R(Q(".av-main-desc")),actions:R(Q(".av-main-head-actions")),rule:R(Q(".av-main-rule")),grid:R(Q(".av-main-grid")),rows:R(Q(".av-main-rows")),foot:R(Q(".av-main-foot"))};})())')"

# 关键盒子（相对 .av-main 左上角）—— 可直接与设计稿 y 值比对
rec rel "$(ev 'JSON.stringify((function(){var m=Q(".av-main");var o={main:REL(m,m),head:REL(Q(".av-main-head"),m),avatar:REL(Q(".av-main-avatar"),m),rule:REL(Q(".av-main-rule"),m),grid:REL(Q(".av-main-grid"),m),rows:REL(Q(".av-main-rows"),m),foot:REL(Q(".av-main-foot"),m),cards:QA(".av-card").map(function(e){return REL(e,m)}),rowboxes:QA(".av-row").map(function(e){return REL(e,m)}),h1:REL(Q(".av-card:nth-child(1) .giencoder-card-header"),m),b1:REL(Q(".av-card:nth-child(1) .giencoder-card-body"),m),h2:REL(Q(".av-card:nth-child(2) .giencoder-card-header"),m)};return o;})())')"

# 容器可用宽（外壳给了多少）
rec avail "$(ev 'JSON.stringify((function(){var m=Q(".av-main"),p=m.parentElement;return{mainW:R(m)[2],parentR:R(p),parentW:p.clientWidth,parentPadL:CS(p,"paddingLeft"),parentPadR:CS(p,"paddingRight")};})())')"

# 内联样式核查：有没有硬编码 hex（应为 0，除 #fff 与设计稿真值 #6B6B6B）
rec css "$(ev 'JSON.stringify((function(){var m=Q(".av-main");var cs=CS(m,"maxWidth");return{maxWidth:cs,width:R(m)[2],bgCard:CS(Q(".av-card"),"backgroundColor"),radiusCard:CS(Q(".av-card"),"borderRadius"),cardBorder:CS(Q(".av-card"),"borderColor")};})())')"

# 抽屉联动：触发器能开抽屉
$AB click "[data-av-chat-toggle]" >/dev/null 2>&1
sleep 0.8
rec drawer "$(ev 'JSON.stringify((function(){var d=Q("#av-chat-drawer");return{open:document.documentElement.hasAttribute("data-av-chat-open"),box:R(d)};})())')"
$AB press Escape >/dev/null 2>&1
sleep 0.6
rec drawerClosed "$(ev 'JSON.stringify({open:document.documentElement.hasAttribute("data-av-chat-open")})')"

$AB screenshot "$SHOT/10-main.png" >/dev/null 2>&1
$AB set viewport 1920 1200 >/dev/null 2>&1
sleep 1.2
rec wide "$(ev 'JSON.stringify((function(){var m=Q(".av-main");return{main:R(m),grid:R(Q(".av-main-grid")),rows:R(Q(".av-main-rows"))};})())')"
$AB screenshot "$SHOT/11-main-1920.png" >/dev/null 2>&1

echo OK
cat "$OUT"

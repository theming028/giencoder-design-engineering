#!/usr/bin/env bash
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"; OUT="mg-work/r34/cmp-detail.jsonl"; : > "$OUT"
HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CS=function(e,p){return e?getComputedStyle(e)[p]:null};'
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

# A. 详情页右栏（真值）
$AB open "$BASE/task-detail.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.0
rec detail "$(ev 'JSON.stringify((function(){return{right:R(Q(".td-right")),addBtn:R(Q("[data-td-add-btn]")),skillBtn:R(Q("[data-td-skill-btn]")),chatInner:R(Q(".td-chat-inner")),composer:R(Q(".td-composer")),ta:{rect:R(Q(".td-composer textarea")),minH:CS(Q(".td-composer textarea"),"minHeight")}}}());
' 2>/dev/null | head -1)"
$AB click "[data-td-skill-btn]" >/dev/null 2>&1
sleep 0.5
rec detailSkill "$(ev 'JSON.stringify({rect:R(Q("[data-td-skill-pop]")),radius:CS(Q("[data-td-skill-pop]"),"borderRadius")})')"
$AB click "[data-td-skill-close]" >/dev/null 2>&1
sleep 0.4
$AB click "[data-td-add-btn]" >/dev/null 2>&1
sleep 0.5
rec detailAdd "$(ev 'JSON.stringify({rect:R(Q("[data-td-add-pop]")),radius:CS(Q("[data-td-add-pop]"),"borderRadius")})')"

# B. 数字分身页关闭态截图（展示触发器）
$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.5
$AB screenshot "mg-work/r34/shots/06-trigger-closed.png" >/dev/null 2>&1
rec avClosed "$(ev 'JSON.stringify({trig:R(Q(".av-chat-trigger")),drawer:R(Q("#av-chat-drawer")),row:R(Q("div.flex.items-start.justify-between"))})')"
echo OK; cat "$OUT"

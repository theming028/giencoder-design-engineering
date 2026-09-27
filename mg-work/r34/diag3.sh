#!/usr/bin/env bash
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"; OUT="mg-work/r34/diag3.jsonl"; : > "$OUT"
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

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.5
$AB click ".av-chat-trigger" >/dev/null 2>&1
sleep 0.8

rec hitTest "$(ev 'JSON.stringify((function(){var b=Q("[data-td-add-btn]"),r=b.getBoundingClientRect(),cx=Math.round(r.left+r.width/2),cy=Math.round(r.top+r.height/2),e=document.elementFromPoint(cx,cx?cy:0);var m=Q("[data-av-chat-mask]"),d=Q("#av-chat-drawer");return{btn:R(b),center:[cx,cy],atCenter:e?e.tagName+"."+(e.className||"").toString().slice(0,70):null,atCenterIsBtn:!!(e&&e.closest&&e.closest("[data-td-add-btn]")),maskZ:CS(m,"zIndex"),drawerZ:CS(d,"zIndex"),maskRect:R(m),drawerZPos:CS(d,"zIndex")};})())')"

# 程序化 click
rec prog "$(ev 'JSON.stringify((function(){Q("[data-td-add-btn]").click();return{drawer:R(Q("#av-chat-drawer")),open:document.documentElement.hasAttribute("data-av-chat-open"),addHidden:Q("[data-td-add-pop]").hidden};})())')"
sleep 0.3
rec progAfter "$(ev 'JSON.stringify({drawer:R(Q("#av-chat-drawer")),open:document.documentElement.hasAttribute("data-av-chat-open"),addHidden:Q("[data-td-add-pop]").hidden})')"
# 关掉
ev 'Q("[data-td-add-btn]").click();1' >/dev/null 2>&1
sleep 0.3

# 物理 click 到抽屉内的技能按钮
rec beforeSkill "$(ev 'JSON.stringify({drawer:R(Q("#av-chat-drawer")),open:document.documentElement.hasAttribute("data-av-chat-open"),skillBtn:R(Q("[data-td-skill-btn]"))})')"
$AB click "[data-td-skill-btn]" >/dev/null 2>&1
sleep 0.6
rec afterSkill "$(ev 'JSON.stringify({drawer:R(Q("#av-chat-drawer")),open:document.documentElement.hasAttribute("data-av-chat-open"),skillHidden:Q("[data-td-skill-pop]").hidden,skillRect:R(Q("[data-td-skill-pop]"))})')"

# 程序化 click 技能按钮
$AB click ".av-chat-trigger" >/dev/null 2>&1
sleep 0.7
rec reOpen "$(ev 'JSON.stringify({drawer:R(Q("#av-chat-drawer")),open:document.documentElement.hasAttribute("data-av-chat-open")})')"
rec progSkill "$(ev 'JSON.stringify((function(){Q("[data-td-skill-btn]").click();return{drawer:R(Q("#av-chat-drawer")),open:document.documentElement.hasAttribute("data-av-chat-open"),skillHidden:Q("[data-td-skill-pop]").hidden,skillRect:R(Q("[data-td-skill-pop]"))};})())')"
rec progFs "$(ev 'JSON.stringify((function(){Q("[data-td-fullscreen]").click();var d=Q("#av-chat-drawer");return{cls:d.className,open:document.documentElement.hasAttribute("data-av-chat-open"),rect:R(d),chatInner:Q(".td-chat-inner")?CS(Q(".td-chat-inner"),"maxWidth"):null};})())')"
echo OK; cat "$OUT"

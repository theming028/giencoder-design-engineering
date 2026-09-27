#!/usr/bin/env bash
# 诊断：抽屉内模块弹层为何整体右移 ~480px；顶栏按钮点击为何不生效
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r34/diag.jsonl"
: > "$OUT"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CS=function(e,p){return e?getComputedStyle(e)[p]:null},TXT=function(e){return e?e.textContent.trim():null},PATH=function(e,n){var o=[],i=0;while(e&&i<(n||6)){o.push(e.tagName+"."+((e.className||"").toString().split(" ").slice(0,3).join("."))+" "+JSON.stringify(R(e))+" pos="+getComputedStyle(e).position+" tf="+getComputedStyle(e).transform.slice(0,28));e=e.parentElement;i++}return o};'

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

# ============ A. 详情页（参考真值） ============
$AB open "$BASE/task-detail.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.0
rec ref_addpop "$(ev 'JSON.stringify((function(){var p=Q("[data-td-add-pop]");var s=Q("[data-td-add-btn]");return{popRect:R(p),pos:CS(p,"position"),left:CS(p,"left"),bottom:CS(p,"bottom"),tfOrig:CS(p,"transformOrigin"),offP:p?p.offsetParent.tagName+"."+(p.offsetParent.className||"").toString().slice(0,40):null,btnRect:R(s),wrapRect:R(s?s.parentElement:null),path:PATH(p,5)};})())')"

# ============ B. 数字分身页（问题现场） ============
$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.5
echo "--- click trigger ---"; $AB click ".av-chat-trigger" 2>&1 | tail -3
sleep 0.8
rec av_state "$(ev 'JSON.stringify({open:document.documentElement.hasAttribute("data-av-chat-open"),drawer:R(Q("#av-chat-drawer"))})')"

rec av_addpop "$(ev 'JSON.stringify((function(){var p=Q("[data-td-add-pop]");var s=Q("[data-td-add-btn]");return{popRect:R(p),pos:CS(p,"position"),left:CS(p,"left"),bottom:CS(p,"bottom"),tfOrig:CS(p,"transformOrigin"),offP:p?p.offsetParent.tagName+"."+(p.offsetParent.className||"").toString().slice(0,40):null,btnRect:R(s),wrapRect:R(s?s.parentElement:null),wrapDisp:CS(s?s.parentElement:null,"display"),wrapFD:CS(s?s.parentElement:null,"flexDirection"),wrapPos:CS(s?s.parentElement:null,"position"),path:PATH(p,6)};})())')"

echo "--- click add btn ---"; $AB click "[data-td-add-btn]" 2>&1 | tail -3
sleep 0.6
rec av_addpop_open "$(ev 'JSON.stringify((function(){var p=Q("[data-td-add-pop]");var c=getComputedStyle(p);return{hidden:p.hidden,vis:[c.display,c.visibility,c.opacity],rect:R(p),pos:CS(p,"position"),left:CS(p,"left"),bottom:CS(p,"bottom"),offP:p.offsetParent?p.offsetParent.tagName+"."+(p.offsetParent.className||"").toString().slice(0,40):null};})())')"

echo "--- click add btn again (close) ---"; $AB click "[data-td-add-btn]" 2>&1 | tail -3
sleep 0.5

echo "--- click skill btn ---"; $AB click "[data-td-skill-btn]" 2>&1 | tail -3
sleep 0.6
rec av_skill_after "$(ev 'JSON.stringify((function(){var p=Q("[data-td-skill-pop]");var b=Q("[data-td-skill-btn]");var c=p?getComputedStyle(p):null;return{hidden:p.hidden,disp:c?c.display:null,vis:c?c.visibility:null,op:c?c.opacity:null,rect:R(p),btnRect:R(b),btnExpanded:b?b.getAttribute("aria-expanded"):null,elAtCenter:(function(){var r=b.getBoundingClientRect();var e=document.elementFromPoint(Math.round(r.left+r.width/2),Math.round(r.top+r.height/2));return e?e.tagName+"."+(e.className||"").toString().slice(0,60):null})(),pos:CS(p,"position"),left:CS(p,"left"),bottom:CS(p,"bottom")};})())')"

echo "--- click fullscreen ---"; $AB click "[data-td-fullscreen]" 2>&1 | tail -3
sleep 0.6
rec av_fs_after "$(ev 'JSON.stringify((function(){var d=Q("#av-chat-drawer"),b=Q("[data-td-fullscreen]");var r=b.getBoundingClientRect();return{cls:d.className,btnRect:R(b),elAtCenter:(function(){var e=document.elementFromPoint(Math.round(r.left+r.width/2),Math.round(r.top+r.height/2));return e?e.tagName+"."+(e.className||"").toString().slice(0,60):null})()};})())')"

echo OK
cat "$OUT"

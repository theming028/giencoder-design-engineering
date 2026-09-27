#!/usr/bin/env bash
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r34/diag2.jsonl"; : > "$OUT"
HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CS=function(e,p){return e?getComputedStyle(e)[p]:null},TXT=function(e){return e?e.textContent.trim():null};'
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

SNAP='JSON.stringify((function(){var d=Q("#av-chat-drawer"),co=Q(".td-composer"),tb=Q(".td-composer .mt-auto"),lg=tb?tb.children[0]:null;return{scroll:{winX:window.scrollX,docElX:document.documentElement.scrollLeft,bodyX:document.body.scrollLeft,drawerX:d.scrollLeft,drawerSW:d.scrollWidth,drawerCW:d.clientWidth},drawer:R(d),composer:R(co),toolbar:R(tb),toolbarSW:tb?tb.scrollWidth:null,toolbarCW:tb?tb.clientWidth:null,toolbarKids:tb?tb.children.length:null,leftGroup:R(lg),leftGroupSW:lg?lg.scrollWidth:null,leftGroupCW:lg?lg.clientWidth:null,leftGroupDisp:lg?CS(lg,"display"):null,leftGroupWrap:lg?CS(lg,"flexWrap"):null,kids:lg?Array.prototype.slice.call(lg.children).map(function(e){return{cls:(e.className||"").toString().slice(0,40),rect:R(e),disp:CS(e,"display"),pos:CS(e,"position"),w:CS(e,"width"),minW:CS(e,"minWidth")}}):null};})())'

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.5
$AB click ".av-chat-trigger" >/dev/null 2>&1
sleep 0.8
rec before "$(ev "$SNAP")"
$AB click "[data-td-add-btn]" >/dev/null 2>&1
sleep 0.6
rec afterAdd "$(ev "$SNAP")"
$AB click "[data-td-add-btn]" >/dev/null 2>&1
sleep 0.6
rec afterClose "$(ev "$SNAP")"
echo OK; cat "$OUT"

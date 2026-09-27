#!/usr/bin/env bash
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r34/probe-header.jsonl"
: > "$OUT"
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

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.0

rec header "$(ev 'JSON.stringify((function(){var h=Q("header")||document.body.firstElementChild;var kids=[];if(h){kids=Array.prototype.slice.call(h.querySelectorAll("*")).map(function(e){var r=e.getBoundingClientRect();return{tag:e.tagName,cls:(e.className||"").toString().slice(0,50),rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],txt:TXT(e).slice(0,20)}}).filter(function(o){return o.rect[3]>0&&o.rect[0]>900}).slice(0,25)}return{header:R(h),rightSide:kids};})())')"

rec row "$(ev 'JSON.stringify((function(){var c=Q(".mx-auto.flex.w-full.max-w-3xl.flex-col.gap-5");if(!c)return null;var row=c.firstElementChild;return{rowCls:row.className,rowDisp:CS(row,"display"),rowJC:CS(row,"justifyContent"),rowGap:CS(row,"gap"),rowRect:R(row),kids:Array.prototype.slice.call(row.children).map(function(e){return{tag:e.tagName,cls:(e.className||"").toString().slice(0,70),rect:R(e),txt:TXT(e).slice(0,30)}}) };})())')"

rec cnt "$(ev 'JSON.stringify({rows:QA("div.flex.items-start.justify-between").length, allRows:QA("div").filter(function(e){return /items-start/.test(e.className||"")&&/justify-between/.test(e.className||"")}).map(function(e){return{cls:e.className.slice(0,80),rect:R(e)}})})')"

$AB screenshot "mg-work/r34/shots/avatar-before.png" >/dev/null 2>&1
echo OK
cat "$OUT"

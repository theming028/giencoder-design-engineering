#!/usr/bin/env bash
# 数字分身页现状探查：外壳结构 / 内容容器几何 / 右上按钮 / 可用 token
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"
OUT="mg-work/r34/probe-avatar-now.jsonl"
: > "$OUT"

HELP='var Q=function(s){return document.querySelector(s)},QA=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CS=function(e,p){return e?getComputedStyle(e)[p]:null},RR=function(e,p){return e?getComputedStyle(e).getPropertyValue(p).trim():null},TXT=function(e){return e?e.textContent.trim():null};'

rec() {
  "$P" -c "
import json,sys
step=sys.argv[1]; raw=sys.argv[2]
try:
    d=json.loads(raw)
    if isinstance(d,str): d=json.loads(d)
except Exception as e:
    d={'__parse_error__':str(e),'raw':raw[:500]}
print(json.dumps({'step':step,'data':d},ensure_ascii=False))
" "$1" "$2" >> "$OUT"
}
ev() { "$AB" eval "$HELP $1" 2>&1 | tail -1; }

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.0

rec shell "$(ev 'JSON.stringify((function(){var a=QA("aside"),m=Q("main"),bd=document.body;return{main:R(m),mainPad:CS(m,"padding"),mainCls:m?m.className:null,mainOverflow:CS(m,"overflow"),mainParentTag:m&&m.parentElement.tagName,mainParentPad:CS(m.parentElement,"padding"),asides:a.map(function(e){return{cls:(e.className||"").toString().slice(0,60),disp:CS(e,"display"),rect:R(e)}}),bodyBg:CS(bd,"backgroundColor")};})())')"

rec box "$(ev 'JSON.stringify((function(){var c=Q(".mx-auto.flex.w-full.max-w-3xl.flex-col.gap-5");if(!c)return{found:false};var r=c.getBoundingClientRect();return{found:true,cls:c.className,rect:R(c),maxW:CS(c,"maxWidth"),w:CS(c,"width"),pad:CS(c,"padding"),gap:CS(c,"gap"),parent:R(c.parentElement),parentCls:(c.parentElement.className||"").toString().slice(0,90),parentPad:CS(c.parentElement,"padding"),children:Array.prototype.slice.call(c.children).map(function(e){return{tag:e.tagName,cls:(e.className||"").toString().slice(0,80),rect:R(e),txt:TXT(e).slice(0,40)}})};})())')"

rec title "$(ev 'JSON.stringify((function(){var out=[];QA("h1,h2,h3").forEach(function(h){out.push({tag:h.tagName,txt:TXT(h),rect:R(h),fs:CS(h,"fontSize"),fw:CS(h,"fontWeight")})});return out.slice(0,10);})())')"

rec btns "$(ev 'JSON.stringify(QA("main button, main a[class*=btn]").map(function(b){return{tag:b.tagName,txt:TXT(b),cls:(b.className||"").toString().slice(0,90),rect:R(b),bg:CS(b,"backgroundColor")}}).slice(0,8))')"

rec tokens "$(ev 'JSON.stringify((function(){var r=document.documentElement,out={};["--color-bg-1","--color-border-2","--color-fill-1","--color-fill-2","--color-text-1","--color-text-3","--color-primary-6","--td-line","--border-radius-xl","--font-size-body-3","--shadow2-down","--shadow3-down"].forEach(function(k){out[k]=RR(r,k)});return out;})())')"

rec head "$(ev 'JSON.stringify((function(){var h=Q("header"),t=Q("[role=tablist]");return{header:R(h),headerBg:CS(h,"backgroundColor"),tabs:t?R(t):null,tabTexts:t?QA("[data-tab]").map(TXT):null,rootKids:Array.prototype.slice.call(document.body.children).map(function(e){return{tag:e.tagName,id:e.id,cls:(e.className||"").toString().slice(0,70)}})};})())')"

$AB screenshot "mg-work/r34/shots/avatar-now.png" >/dev/null 2>&1
echo OK
cat "$OUT"

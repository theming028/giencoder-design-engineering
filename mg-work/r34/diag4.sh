#!/usr/bin/env bash
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"; OUT="mg-work/r34/diag4.jsonl"; : > "$OUT"
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
ev() { "$AB" eval "$1" 2>&1 | tail -1; }

$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.5

# 插桩：监听 <html> 的属性增删
ev '(function(){var de=document.documentElement;window.__log=[];var ra=de.removeAttribute,ta=de.toggleAttribute,sa=de.setAttribute;de.removeAttribute=function(n){try{window.__log.push(["remove",n,((new Error()).stack||"").split("\n").slice(1,4).join(" < ")]);}catch(e){}return ra.apply(de,arguments);};de.toggleAttribute=function(n,f){try{window.__log.push(["toggle",n,String(f),((new Error()).stack||"").split("\n").slice(1,4).join(" < ")]);}catch(e){}return ta.apply(de,arguments);};de.setAttribute=function(n,v){try{window.__log.push(["set",n,String(v)]);}catch(e){}return sa.apply(de,arguments);};return "ok";})()' >/dev/null 2>&1

$AB click ".av-chat-trigger" >/dev/null 2>&1
sleep 0.8
rec afterOpen "$(ev 'JSON.stringify({open:document.documentElement.hasAttribute("data-av-chat-open"),log:window.__log.slice(0,12)})')"

ev 'window.__log=[];1' >/dev/null 2>&1
ev 'document.querySelector("[data-td-skill-btn]").click();1' >/dev/null 2>&1
sleep 0.5
rec afterSkillClick "$(ev 'JSON.stringify({open:document.documentElement.hasAttribute("data-av-chat-open"),skillHidden:document.querySelector("[data-td-skill-pop]").hidden,attrs:document.documentElement.getAttributeNames(),log:window.__log})')"
echo OK; cat "$OUT"

#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 2800 >/dev/null 2>&1

P="(function(){var f=document.querySelectorAll('.r93-fold')[2];var fb=f.querySelector(':scope > .r93-fb');return JSON.stringify({open:f.getAttribute('data-r93-open'),oh:fb.offsetHeight,maxH:getComputedStyle(fb).maxHeight});})()"

echo "-- 初始 --"; "$NODE" "$AB" eval "$P"
echo "-- 收起（eval）--"
"$NODE" "$AB" eval "(function(){document.querySelectorAll('.r93-fold')[2].querySelector('.r93-fh').click();return 1;})()" >/dev/null
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" eval "$P"

echo "-- 落点诊断（fc 中心 elementsFromPoint）--"
"$NODE" "$AB" eval "(function(){var f=document.querySelectorAll('.r93-fold')[2];var b=f.querySelector('.r93-fc');var r=b.getBoundingClientRect();var els=document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2);return JSON.stringify({rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],scrollY:Math.round(document.querySelector('.r93-scroll').scrollTop),top:els.slice(0,4).map(function(e){return e.tagName+'.'+String(e.className).slice(0,44);})});})()"

echo "-- agent-browser scrollintoview + click --"
"$NODE" "$AB" eval "(function(){document.querySelectorAll('.r93-fold')[2].querySelector('.r93-fc').setAttribute('data-p104n','1');return 1;})()" >/dev/null
"$NODE" "$AB" scrollintoview '[data-p104n="1"]' >/dev/null 2>&1
"$NODE" "$AB" click '[data-p104n="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "$P"

echo "-- 落点诊断（click 之后，tag 还在 fc 上）--"
"$NODE" "$AB" eval "(function(){var b=document.querySelector('[data-p104n=\"1\"]');if(!b)return 'no-tag';var r=b.getBoundingClientRect();var els=document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2);return JSON.stringify({rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],top:els.slice(0,4).map(function(e){return e.tagName+'.'+String(e.className).slice(0,44);})});})()"

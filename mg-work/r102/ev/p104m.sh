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

P="(function(){var f=document.querySelectorAll('.r93-fold')[2];var fb=f.querySelector(':scope > .r93-fb');return JSON.stringify({open:f.getAttribute('data-r93-open'),oh:fb.offsetHeight,maxH:getComputedStyle(fb).maxHeight,op:getComputedStyle(fb).opacity,isFree:fb.classList.contains('is-free')});})()"

echo "-- 初始 --"; "$NODE" "$AB" eval "$P"

echo "-- 收起：eval 直接派发 click 到 .r93-fh --"
"$NODE" "$AB" eval "(function(){var f=document.querySelectorAll('.r93-fold')[2];f.querySelector('.r93-fh').click();return 'done';})()"
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "$P"

echo "-- 展开：eval 直接派发 click 到 .r93-fc --"
"$NODE" "$AB" eval "(function(){var f=document.querySelectorAll('.r93-fold')[2];f.querySelector('.r93-fc').click();return 'done';})()"
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "$P"

echo "-- 再看：host 上是否只有一个 click 监听 / fold 委托是否还在 --"
"$NODE" "$AB" eval "(function(){var f=document.querySelectorAll('.r93-fold')[2];var b=f.querySelector('.r93-fc');var t=b.querySelector('.r93-iblk')||b;var els=document.elementsFromPoint.apply(document,(function(){var r=b.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2];})());return JSON.stringify({fcRect:(function(){var r=b.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)];})(),top3:els.slice(0,3).map(function(e){return e.tagName+'.'+(e.className||'').toString().slice(0,40);})});})()"

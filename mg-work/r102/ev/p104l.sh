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

P="(function(){var f=document.querySelectorAll('.r93-fold')[2];var fb=f.querySelector(':scope > .r93-fb');var r=f.getBoundingClientRect();var vh=f.querySelector('.r93-fh'),vf=f.querySelector('.r93-fc');return JSON.stringify({open:f.getAttribute('data-r93-open'),oh:fb.offsetHeight,maxH:getComputedStyle(fb).maxHeight,op:getComputedStyle(fb).opacity,isFree:fb.classList.contains('is-free'),fhVis:getComputedStyle(vh).display,fcVis:getComputedStyle(vf).display,rect:[Math.round(r.left),Math.round(r.top),Math.round(r.height)]});})()"

# 每轮把 tag 打在「当前可见的那个头」上
TAGG="(function(){var f=document.querySelectorAll('.r93-fold')[2];var h=f.querySelector('.r93-fh, .r93-fc');var kids=f.children;for(var i=0;i<kids.length;i++){var k=kids[i];if(k.classList&&(k.classList.contains('r93-fh')||k.classList.contains('r93-fc'))&&getComputedStyle(k).display!=='none'){h=k;break;}}h.setAttribute('data-p104l','1');return h.className+'|'+Math.round(h.getBoundingClientRect().top);})()"

echo "-- 初始 --"; "$NODE" "$AB" eval "$P"
echo "tag@初始 -> $("$NODE" "$AB" eval "$TAGG")"
for n in 1 2 3 4; do
  echo "-- 第 $n 次点击 --"
  echo "  tag -> $("$NODE" "$AB" eval "$TAGG")"
  "$NODE" "$AB" scrollintoview '[data-p104l="1"]' >/dev/null 2>&1
  "$NODE" "$AB" click '[data-p104l="1"]' >/dev/null 2>&1
  "$NODE" "$AB" wait 800 >/dev/null 2>&1
  "$NODE" "$AB" eval "$P"
done

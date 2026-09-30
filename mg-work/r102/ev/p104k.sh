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
P="(function(){var f=document.querySelectorAll('.r93-fold')[2];var fb=f.querySelector(':scope > .r93-fb');var r=f.querySelector('.r93-fh').getBoundingClientRect();return JSON.stringify({open:f.getAttribute('data-r93-open'),fbh:fb.style.getPropertyValue('--r93-fbh'),sh:fb.scrollHeight,oh:fb.offsetHeight,isFree:fb.classList.contains('is-free'),maxH:getComputedStyle(fb).maxHeight,op:getComputedStyle(fb).opacity,rect:[Math.round(r.left),Math.round(r.top)]});})()"
echo "-- 初始 --"; "$NODE" "$AB" eval "$P"
"$NODE" "$AB" eval "(function(){var f=document.querySelectorAll('.r93-fold')[2];f.querySelector('.r93-fh').setAttribute('data-p104h','1');return 'tagged';})()"
echo "-- 第 1 次点击（应收起）--"
"$NODE" "$AB" scrollintoview '[data-p104h="1"]' >/dev/null 2>&1
"$NODE" "$AB" click '[data-p104h="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "$P"
echo "-- 第 2 次点击（应展开）--"
"$NODE" "$AB" scrollintoview '[data-p104h="1"]' >/dev/null 2>&1
"$NODE" "$AB" click '[data-p104h="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "$P"

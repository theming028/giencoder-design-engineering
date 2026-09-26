#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r12
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 240 $AB open "http://127.0.0.1:8866/pages/base.html?v=r19" > $OUT/e1.log 2>&1
echo "OPEN: $(tail -2 $OUT/e1.log | tr '\n' ' ')"
timeout 200 $AB eval 'function info(p){var r=p.getBoundingClientRect();var cs=getComputedStyle(p);return [p.tagName,(typeof p.className==="string"?p.className.slice(0,160):""),Math.round(r.width)+"x"+Math.round(r.height)+"@"+Math.round(r.left)+","+Math.round(r.top),cs.width+"/"+cs.maxWidth+"/"+cs.minWidth]}var skip={SCRIPT:1,STYLE:1,HTML:1,HEAD:1,BODY:1};var hit=null;var all=document.querySelectorAll("main *");for(var i=0;i<all.length;i++){var e=all[i];if(skip[e.tagName])continue;var ph=e.getAttribute&&e.getAttribute("placeholder");if(ph&&ph.indexOf("描述")>=0){hit=e;break}}var res={};if(hit){res.byPlaceholder=info(hit);var c=[];var p=hit;for(var j=0;j<9&&p;j++){c.push(info(p));p=p.parentElement}res.chain=c}else{res.byPlaceholder=null}res.textareas=document.querySelectorAll("main textarea").length;res.ce=document.querySelectorAll("main [contenteditable]").length;var inn=[];var t=document.querySelectorAll("main textarea,main [contenteditable]");for(var k=0;k<t.length;k++)inn.push(info(t[k]));res.inputs=inn;JSON.stringify(res)' > $OUT/e-base.log 2>&1
echo "COMPOSER: $(tail -1 $OUT/e-base.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

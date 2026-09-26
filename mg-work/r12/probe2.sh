#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r12
mkdir -p $OUT
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 240 $AB open "http://127.0.0.1:8866/pages/base.html?v=r18" > $OUT/d1.log 2>&1
echo "OPEN: $(tail -2 $OUT/d1.log | tr '\n' ' ')"
timeout 200 $AB eval 'var skip={SCRIPT:1,STYLE:1,HTML:1,HEAD:1,BODY:1};var hit=null;var all=document.querySelectorAll("main *");for(var i=0;i<all.length;i++){var e=all[i];if(skip[e.tagName])continue;if(e.children.length===0&&e.textContent&&e.textContent.indexOf("描述你的任务")>=0){hit=e;break}}if(!hit){JSON.stringify({found:0})}else{var out=[];var p=hit;for(var j=0;j<8&&p;j++){var r=p.getBoundingClientRect();var cs=getComputedStyle(p);out.push([p.tagName,(typeof p.className==="string"?p.className.slice(0,150):""),Math.round(r.width),Math.round(r.height),Math.round(r.left),Math.round(r.top),cs.width,cs.maxWidth]);p=p.parentElement}JSON.stringify({found:1,n:out.length,chain:out})}' > $OUT/d-base.log 2>&1
echo "COMPOSER: $(tail -1 $OUT/d-base.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

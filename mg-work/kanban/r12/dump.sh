#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/kanban/r12
mkdir -p $OUT
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 240 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r14" > $OUT/a-open.log 2>&1
echo "OPEN: $(tail -2 $OUT/a-open.log | tr '\n' ' ')"

timeout 180 $AB eval 'var res={};var aside=document.querySelector("aside");res.aside=aside?1:0;var top=document.querySelector(".ws-trigger-hover");res.wsTrig=top?1:0;if(top){var r=top.getBoundingClientRect();res.wsRect=Math.round(r.left)+","+Math.round(r.top)+" "+Math.round(r.width)+"x"+Math.round(r.height);res.wsVisible=getComputedStyle(top).display+"/"+getComputedStyle(top).visibility+"/"+getComputedStyle(top).opacity;var p=top;var chain=[];for(var i=0;i<6&&p;i++){chain.push(p.tagName+"."+(p.className||""));p=p.parentElement}res.chain=chain.join(" < ")}res.bodyChildren=Array.prototype.slice.call(document.body.children).map(function(e){return e.tagName+"."+(typeof e.className==="string"?e.className:"")}).join(" | ");JSON.stringify(res)' > $OUT/a-dom.log 2>&1
echo "DOM: $(tail -1 $OUT/a-dom.log)"

timeout 240 $AB screenshot "" $OUT/a-kanban.png > $OUT/a-shot.log 2>&1
echo "SHOT: $(tail -1 $OUT/a-shot.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r12
mkdir -p $OUT
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1

# ---------- base.html: 找对话框 DOM ----------
timeout 240 $AB open "http://127.0.0.1:8866/pages/base.html?v=r17" > $OUT/c1.log 2>&1
echo "OPEN base: $(tail -2 $OUT/c1.log | tr '\n' ' ')"
timeout 200 $AB eval 'var hit=null;var all=document.querySelectorAll("*");for(var i=0;i<all.length;i++){var e=all[i];if(e.children.length===0&&e.textContent&&e.textContent.indexOf("描述你的任务")>=0){hit=e;break}}if(!hit){JSON.stringify({found:0})}else{var chain=[];var p=hit;for(var j=0;j<7&&p;j++){var r=p.getBoundingClientRect();var cs=getComputedStyle(p);chain.push({t:p.tagName,c:(typeof p.className==="string"?p.className:""),w:Math.round(r.width),h:Math.round(r.height),x:Math.round(r.left),y:Math.round(r.top),mw:cs.maxWidth,minw:cs.minWidth});p=p.parentElement}JSON.stringify({found:1,chain:chain})}' > $OUT/c-base.log 2>&1
echo "COMPOSER: $(tail -1 $OUT/c-base.log)"
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1

# ---------- kanban.html: FAB ----------
timeout 240 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r17" > $OUT/c2.log 2>&1
echo "OPEN kanban: $(tail -2 $OUT/c2.log | tr '\n' ' ')"
timeout 200 $AB eval 'var f=document.querySelector(".kb-fab");if(!f){JSON.stringify({found:0})}else{var r=f.getBoundingClientRect();var cs=getComputedStyle(f);JSON.stringify({found:1,rect:Math.round(r.width)+"x"+Math.round(r.height)+"@"+Math.round(r.left)+","+Math.round(r.top),offParent:f.offsetParent?f.offsetParent.className:null,html:f.innerHTML.length,svgCount:f.querySelectorAll("svg").length,pos:cs.position,right:cs.right,bottom:cs.bottom,bg:cs.backgroundImage.slice(0,80),mainRect:(function(){var m=document.querySelector("main").getBoundingClientRect();return Math.round(m.width)+"x"+Math.round(m.height)+"@"+Math.round(m.left)+","+Math.round(m.top)})(),mainPos:getComputedStyle(document.querySelector("main")).position})}' > $OUT/c-kanban.log 2>&1
echo "FAB: $(tail -1 $OUT/c-kanban.log)"
timeout 240 $AB screenshot "" $OUT/kanban.png > $OUT/c3.log 2>&1
echo "SHOT: $(tail -1 $OUT/c3.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

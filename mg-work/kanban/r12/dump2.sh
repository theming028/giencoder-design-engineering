#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/kanban/r12
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 240 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r15" > $OUT/b-open.log 2>&1
echo "OPEN: $(tail -2 $OUT/b-open.log | tr '\n' ' ')"

timeout 180 $AB eval 'var btn=document.querySelector("[aria-label=\"切换侧边栏\"]");if(!btn){JSON.stringify({found:0})}else{var wsRoot=btn.parentElement,wrap=wsRoot.parentElement;var path=[];var p=btn;while(p&&p!==document.documentElement){var idx=1,q=p;while(q.previousElementSibling){q=q.previousElementSibling;idx++}path.unshift(p.tagName.toLowerCase()+(p.id?"#"+p.id:"")+(typeof p.className==="string"&&p.className?"."+p.className.trim().split(/\s+/).join("."):"")+":nth-child("+idx+")");p=p.parentElement}JSON.stringify({found:1,btnRect:(function(r){return Math.round(r.left)+","+Math.round(r.top)+" "+Math.round(r.width)+"x"+Math.round(r.height)})(btn.getBoundingClientRect()),wsRootCls:wsRoot.className,wsRootStyle:wsRoot.getAttribute("style"),wrapCls:wrap.className,wrapStyle:wrap.getAttribute("style"),wrapOpacity:getComputedStyle(wrap).opacity,wrapPE:getComputedStyle(wrap).pointerEvents,path:path.join(" > ")})}' > $OUT/b-dom.log 2>&1
echo "DOM: $(tail -1 $OUT/b-dom.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r12
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 240 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r21" > $OUT/m1.log 2>&1
echo "OPEN: $(tail -2 $OUT/m1.log | tr '\n' ' ')"
timeout 180 $AB eval 'var t=document.querySelector(".kb-stat--coop");var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));JSON.stringify({open:!document.querySelector(".kb-coop").hidden})' > $OUT/m-click.log 2>&1
echo "CLICK: $(tail -1 $OUT/m-click.log)"
timeout 180 $AB eval 'var foot=document.querySelector(".kb-coop-foot"),pager=document.querySelector(".kb-coop-pager"),stats=document.querySelector(".kb-coop-stats"),jump=document.querySelector(".kb-coop-jump"),po=document.querySelector(".kb-coop-pageopt"),content=document.querySelector(".kb-coop-content");function W(e){var r=e.getBoundingClientRect();return Math.round(r.width)}function R(e){var r=e.getBoundingClientRect();return Math.round(r.left)+"~"+Math.round(r.right)}var tds=document.querySelectorAll(".kb-coop-tbl tbody tr:first-child td");JSON.stringify({contentInner:W(content),footW:W(foot),footScroll:foot.scrollWidth,statsW:W(stats),pagerW:W(pager),jumpW:W(jump),poW:W(po),footRight:R(foot),pagerRight:R(pager),contentRight:R(content),overflow:Math.round(pager.getBoundingClientRect().right-content.getBoundingClientRect().right),tdRects:Array.prototype.map.call(tds,function(e){return Math.round(e.getBoundingClientRect().width)}).join("|"),thead:document.querySelector(".kb-coop-tbl .giencoder-table-th").getBoundingClientRect().height,tableLayout:getComputedStyle(document.querySelector(".kb-coop-tbl")).tableLayout,closeOutline:getComputedStyle(document.querySelector(".kb-coop-close")).outlineWidth+" "+getComputedStyle(document.querySelector(".kb-coop-close")).outlineStyle,activeEl:document.activeElement.className})' > $OUT/m-foot.log 2>&1
echo "FOOT: $(tail -1 $OUT/m-foot.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

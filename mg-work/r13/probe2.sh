#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r13
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 300 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r13c" > $OUT/c-open.log 2>&1
echo "OPEN: $(tail -1 $OUT/c-open.log)"
timeout 180 $AB eval 'var t=document.querySelector(".kb-stat--coop");var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));JSON.stringify({opened:!document.querySelector(".kb-coop").hidden})' > /dev/null 2>&1
sleep 1
timeout 180 $AB eval 'var all=document.querySelectorAll(".kb-coop-sel");var s=all[1];var v=s.querySelector(".giencoder-select-view");v.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true}));JSON.stringify({clicked:true})' > /dev/null 2>&1
sleep 1
timeout 180 $AB eval 'var all=document.querySelectorAll(".kb-coop-sel");var s=all[1];var v=s.querySelector(".giencoder-select-view"),p=s.querySelector(".giencoder-select-popup");var d=document.querySelector(".kb-coop-dialog"),dr=d.getBoundingClientRect(),pr=p.getBoundingClientRect();JSON.stringify({viewW:Math.round(v.getBoundingClientRect().width),popupW:Math.round(pr.width),popupH:Math.round(pr.height),opts:p.querySelectorAll(".giencoder-select-option").length,disp:getComputedStyle(p).display,vis:getComputedStyle(p).visibility,opa:getComputedStyle(p).opacity,cls:p.className,items:Array.prototype.map.call(p.querySelectorAll(".giencoder-select-option"),function(e){return e.textContent}).join("/"),rightGap:Math.round(dr.right-pr.right),leftGap:Math.round(pr.left-dr.left),bottomGap:Math.round(dr.bottom-pr.bottom)})' > $OUT/c-det.log 2>&1
echo "DETAIL: $(tail -1 $OUT/c-det.log)"
timeout 240 $AB screenshot "" $OUT/assignee-open.png > $OUT/c-shot.log 2>&1
echo "SHOT: $(tail -1 $OUT/c-shot.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

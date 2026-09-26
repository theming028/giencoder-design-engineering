#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r12
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 240 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r22" > $OUT/f1.log 2>&1
echo "OPEN: $(tail -2 $OUT/f1.log | tr '\n' ' ')"

# 泳道 hover：把鼠标移到泳道头部（视口内确定可见）
timeout 120 $AB hover ".kb-col-head" > /dev/null 2>&1
timeout 120 $AB eval 'var cols=document.querySelectorAll(".kb-col");var out=[];for(var i=0;i<cols.length;i++){out.push(getComputedStyle(cols[i]).backgroundColor+(cols[i].querySelector(".kb-col-head").matches(":hover")?"*":"") )}JSON.stringify({lanes:out})' > $OUT/f-lane.log 2>&1
echo "LANE: $(tail -1 $OUT/f-lane.log)"

timeout 120 $AB hover ".kb-topbar" > /dev/null 2>&1
timeout 120 $AB eval 'var cols=document.querySelectorAll(".kb-col");JSON.stringify({idle:getComputedStyle(cols[0]).backgroundColor})' > $OUT/f-lane2.log 2>&1
echo "LANE-IDLE: $(tail -1 $OUT/f-lane2.log)"

# 模态
timeout 180 $AB eval 'var t=document.querySelector(".kb-stat--coop");var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));JSON.stringify({open:!document.querySelector(".kb-coop").hidden})' > $OUT/f-click.log 2>&1
echo "CLICK: $(tail -1 $OUT/f-click.log)"
timeout 180 $AB eval 'var dl=document.querySelector(".kb-coop-dialog"),mn=document.querySelector("main");var dr=dl.getBoundingClientRect(),mr=mn.getBoundingClientRect();var tds=document.querySelectorAll(".kb-coop-tbl tbody tr:first-child td");var th=document.querySelector(".kb-coop-tbl .giencoder-table-th");JSON.stringify({wRatio:(dr.width/mr.width).toFixed(3),topGap:Math.round(dr.top-mr.top),bottomGap:Math.round(mr.bottom-dr.bottom),cols:Array.prototype.map.call(tds,function(e){return Math.round(e.getBoundingClientRect().width)}).join("|"),thH:th.getBoundingClientRect().height,rowH:document.querySelector(".kb-coop-tbl tbody tr").getBoundingClientRect().height,timeText:document.querySelectorAll(".kb-coop-tbl tbody tr")[3].querySelectorAll("td")[5].textContent,timeCls:document.querySelectorAll(".kb-coop-tbl tbody tr")[3].querySelectorAll("td")[5].scrollWidth+"<="+Math.round(document.querySelectorAll(".kb-coop-tbl tbody tr")[3].querySelectorAll("td")[5].getBoundingClientRect().width),closeOutline:getComputedStyle(document.querySelector(".kb-coop-close")).outlineStyle,activeTag:document.activeElement.tagName+"."+document.activeElement.className})' > $OUT/f-geo.log 2>&1
echo "GEO: $(tail -1 $OUT/f-geo.log)"
timeout 240 $AB screenshot "" $OUT/modal-final.png > $OUT/f-shot.log 2>&1
echo "SHOT: $(tail -1 $OUT/f-shot.log)"
timeout 120 $AB eval 'document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}))' > /dev/null 2>&1
timeout 240 $AB screenshot "" $OUT/board-final.png > $OUT/f-shot2.log 2>&1
echo "SHOT2: $(tail -1 $OUT/f-shot2.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

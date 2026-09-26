#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r14
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 300 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r14b" > $OUT/c-open.log 2>&1
echo "OPEN: $(tail -1 $OUT/c-open.log)"
# 待评审
timeout 180 $AB eval 'var t=document.querySelectorAll(".kb-stat[data-modal-title]")[1];var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));1' > /dev/null 2>&1
sleep 1
timeout 180 $AB eval 'JSON.stringify({title:document.querySelector(".giencoder-modal-title").textContent})' > $OUT/c-t1.log 2>&1
echo "T1: $(tail -1 $OUT/c-t1.log)"
timeout 240 $AB screenshot "" $OUT/review-modal.png > /dev/null 2>&1
echo "SHOT1: ok"
timeout 180 $AB eval 'document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}));1' > /dev/null 2>&1
sleep 1
# 已取消
timeout 180 $AB eval 'var t=document.querySelectorAll(".kb-stat[data-modal-title]")[3];var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));1' > /dev/null 2>&1
sleep 1
timeout 180 $AB eval 'JSON.stringify({title:document.querySelector(".giencoder-modal-title").textContent})' > $OUT/c-t3.log 2>&1
echo "T3: $(tail -1 $OUT/c-t3.log)"
timeout 240 $AB screenshot "" $OUT/cancel-modal.png > /dev/null 2>&1
echo "SHOT2: ok"
# 表格标题链接的默认态（把鼠标移开）
timeout 180 $AB eval 'document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}));1' > /dev/null 2>&1
sleep 1
timeout 180 $AB eval 'var t=document.querySelectorAll(".kb-stat[data-modal-title]")[0];var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));1' > /dev/null 2>&1
sleep 1
timeout 120 $AB hover ".kb-coop-dialog .giencoder-modal-title" > /dev/null 2>&1
timeout 240 $AB screenshot "" $OUT/table-idle.png > /dev/null 2>&1
echo "SHOT3: ok"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/kanban/r11

timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 240 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r12" > $OUT/w-open.log 2>&1
echo "OPEN: $(tail -2 $OUT/w-open.log | tr '\n' ' ')"

# 1) JS 触发点击，看模态是否打开
timeout 180 $AB eval 'var t=document.querySelector(".kb-stat--coop");var m=document.querySelector(".kb-coop");t.click();JSON.stringify({hiddenAfterJsClick:m.hidden,cls:m.className,hasHandler:typeof t.onclick,rect:(function(r){return Math.round(r.left)+","+Math.round(r.top)+" "+Math.round(r.width)+"x"+Math.round(r.height)})(t.getBoundingClientRect())})' > $OUT/w-jsclick.log 2>&1
echo "JSCLICK: $(tail -1 $OUT/w-jsclick.log)"

# 2) 模态几何 + 色值
timeout 120 $AB eval 'var m=document.querySelector(".kb-coop"),d=document.querySelector(".kb-coop-dialog"),msk=document.querySelector(".kb-coop-mask");var r=d.getBoundingClientRect();JSON.stringify({hidden:m.hidden,dialog:Math.round(r.width)+"x"+Math.round(r.height)+"@"+Math.round(r.left)+","+Math.round(r.top),bg:getComputedStyle(d).backgroundColor,mask:getComputedStyle(msk).backgroundColor+" / "+getComputedStyle(msk).backdropFilter,prio:Array.prototype.slice.call(m.querySelectorAll(".kb-td-prio")).map(function(e){return e.textContent+":"+getComputedStyle(e).color}).join(" | "),title:getComputedStyle(m.querySelector(".giencoder-modal-title")).fontSize+"+"+getComputedStyle(m.querySelector(".giencoder-modal-title")).fontWeight})' > $OUT/w-geo.log 2>&1
echo "GEO: $(tail -1 $OUT/w-geo.log)"

# 3) 截图（模态打开态）
timeout 240 $AB screenshot "" $OUT/w-modal.png > $OUT/w-shot.log 2>&1
echo "SHOT: $(tail -1 $OUT/w-shot.log)"

# 4) 关闭键测试 + 再看一次
timeout 120 $AB eval 'document.querySelector(".kb-coop-close").click();JSON.stringify({hiddenAfterClose:document.querySelector(".kb-coop").hidden})' > $OUT/w-close.log 2>&1
echo "CLOSE: $(tail -1 $OUT/w-close.log)"

timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

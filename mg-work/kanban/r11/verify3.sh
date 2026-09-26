#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/kanban/r11

timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 240 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r13" > $OUT/x-open.log 2>&1
echo "OPEN: $(tail -2 $OUT/x-open.log | tr '\n' ' ')"

# 0) 先确认绑定落地：定义所在脚本 / 元素存在性 / 是否抛错
timeout 120 $AB eval 'var t=document.querySelector(".kb-stat--coop"),m=document.querySelector(".kb-coop");var r=t.getBoundingClientRect();JSON.stringify({coop:t?1:0,modal:m?1:0,coopText:t?t.innerText.replace(/\n/g,"|"):null,rect:Math.round(r.left)+","+Math.round(r.top)+" "+Math.round(r.width)+"x"+Math.round(r.height)})' > $OUT/x-dom.log 2>&1
echo "DOM: $(tail -1 $OUT/x-dom.log)"

# 1) 真实鼠标点击（不是 t.click()），验证事件链
timeout 180 $AB eval 'window.__err="";window.addEventListener("error",function(e){window.__err+=e.message});var t=document.querySelector(".kb-stat--coop");var r=t.getBoundingClientRect();var ev=new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+r.width/2,clientY:r.top+r.height/2});t.dispatchEvent(ev);var m=document.querySelector(".kb-coop");JSON.stringify({err:window.__err,hidden:m.hidden,cls:m.className,lock:document.documentElement.className})' > $OUT/x-click.log 2>&1
echo "CLICK: $(tail -1 $OUT/x-click.log)"

# 2) 模态几何 + 色值
timeout 120 $AB eval 'var m=document.querySelector(".kb-coop"),d=document.querySelector(".kb-coop-dialog"),msk=document.querySelector(".kb-coop-mask");var r=d.getBoundingClientRect();JSON.stringify({hidden:m.hidden,dialog:Math.round(r.width)+"x"+Math.round(r.height)+"@"+Math.round(r.left)+","+Math.round(r.top),bg:getComputedStyle(d).backgroundColor,mask:getComputedStyle(msk).backgroundColor+" / "+getComputedStyle(msk).backdropFilter,prio:Array.prototype.slice.call(m.querySelectorAll(".kb-td-prio")).map(function(e){return e.textContent+":"+getComputedStyle(e).color}).join(" | "),title:getComputedStyle(m.querySelector(".giencoder-modal-title")).fontSize+"+"+getComputedStyle(m.querySelector(".giencoder-modal-title")).fontWeight,th:getComputedStyle(m.querySelector(".giencoder-table-th")).backgroundColor,rowH:Math.round(m.querySelector(".giencoder-table-tr").getBoundingClientRect().height)})' > $OUT/x-geo.log 2>&1
echo "GEO: $(tail -1 $OUT/x-geo.log)"

# 3) 截图（模态打开态）
timeout 240 $AB screenshot "" $OUT/x-modal.png > $OUT/x-shot.log 2>&1
echo "SHOT: $(tail -1 $OUT/x-shot.log)"

# 4) Esc 关闭
timeout 120 $AB eval 'document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}));JSON.stringify({hidden:document.querySelector(".kb-coop").hidden,lock:document.documentElement.className})' > $OUT/x-esc.log 2>&1
echo "ESC: $(tail -1 $OUT/x-esc.log)"

timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

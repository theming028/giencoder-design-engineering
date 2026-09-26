#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r13
mkdir -p $OUT
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 300 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r13a" > $OUT/a-open.log 2>&1
echo "OPEN: $(tail -1 $OUT/a-open.log)"

# 打开模态
timeout 180 $AB eval 'var t=document.querySelector(".kb-stat--coop");var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));JSON.stringify({hidden:document.querySelector(".kb-coop").hidden,cls:document.querySelector(".kb-coop").className})' > $OUT/a-click.log 2>&1
echo "CLICK: $(tail -1 $OUT/a-click.log)"
sleep 1

# 1+2 几何：顶角直角 / 纵向拉伸 / 底距 48
timeout 180 $AB eval 'var d=document.querySelector(".kb-coop-dialog"),m=document.querySelector("main");var dr=d.getBoundingClientRect(),mr=m.getBoundingClientRect();var cs=getComputedStyle(d);JSON.stringify({radius:cs.borderRadius,top:cs.top,bottom:cs.bottom,maxH:cs.maxHeight,transformOrigin:cs.transformOrigin,transition:cs.transitionProperty+" "+cs.transitionDuration,topGap:Math.round(dr.top-mr.top),bottomGap:Math.round(mr.bottom-dr.bottom),dlgH:Math.round(dr.height),mainH:Math.round(mr.height),wRatio:(dr.width/mr.width).toFixed(3),wrapOverflow:getComputedStyle(document.querySelector(".kb-coop-tblwrap")).overflowY})' > $OUT/a-geo.log 2>&1
echo "GEOM: $(tail -1 $OUT/a-geo.log)"

# 5 select 图标：箭头类名 / path / stroke-width
timeout 180 $AB eval 'var sels=document.querySelectorAll(".kb-coop-sel");var o=[];for(var i=0;i<sels.length;i++){var a=sels[i].querySelector(".giencoder-select-arrow");var c=sels[i].querySelector(".giencoder-select-clear");var p=sels[i].querySelector(".giencoder-select-popup");o.push({lbl:sels[i].querySelector(".kb-coop-sel-lbl").textContent,arrow:!!a,path:a?a.querySelector("path").getAttribute("d"):null,sw:a?a.getAttribute("stroke-width"):null,clear:!!c,popup:!!p,opts:p?p.querySelectorAll(".giencoder-select-option").length:0,viewW:Math.round(sels[i].querySelector(".giencoder-select-view").getBoundingClientRect().width)})}var pg=document.querySelector(".kb-coop-pageopt");var pa=pg.querySelector("svg");JSON.stringify({sels:o,pageopt:{arrowCls:/giencoder-select-arrow/.test(pa.getAttribute("class")||""),path:pa.querySelector("path").getAttribute("d")}})' > $OUT/a-icon.log 2>&1
echo "ICON: $(tail -1 $OUT/a-icon.log)"

# 3 可点击：打开优先级下拉 -> 选项可见 -> 选中「高」-> 回显更新
timeout 180 $AB eval 'var v=document.querySelector(".kb-coop-sel .giencoder-select-view");v.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true}));var p=document.querySelector(".kb-coop-sel .giencoder-select-popup");JSON.stringify({disp:getComputedStyle(p).display,open:p.classList.contains("giencoder-popup-open"),aria:v.getAttribute("aria-expanded"),pr:Math.round(p.getBoundingClientRect().width)})' > $OUT/a-sel1.log 2>&1
echo "SEL-OPEN: $(tail -1 $OUT/a-sel1.log)"
sleep 1
timeout 240 $AB screenshot "" $OUT/sel-open.png > $OUT/a-shot1.log 2>&1
echo "SHOT-SEL: $(tail -1 $OUT/a-shot1.log)"
timeout 180 $AB eval 'var opts=document.querySelectorAll(".kb-coop-sel .giencoder-select-option");opts[1].dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true}));var s=document.querySelector(".kb-coop-sel");JSON.stringify({text:s.querySelector(".giencoder-select-view-text").textContent,hasValue:s.classList.contains("giencoder-select-has-value"),popupDisp:getComputedStyle(s.querySelector(".giencoder-select-popup")).display})' > $OUT/a-sel2.log 2>&1
echo "SEL-PICK: $(tail -1 $OUT/a-sel2.log)"

# 4 日期面板可点击 + 右对齐不越界
timeout 180 $AB eval 'var w=document.querySelector(".kb-coop-date .giencoder-input-wrapper");w.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true}));var p=document.querySelector(".kb-coop-date .giencoder-date-picker-popup");var d=document.querySelector(".kb-coop-dialog");var pr=p.getBoundingClientRect(),dr=d.getBoundingClientRect();JSON.stringify({disp:getComputedStyle(p).display,open:p.classList.contains("giencoder-panel-open"),panels:p.querySelectorAll(".giencoder-calendar").length,popupW:Math.round(pr.width),popupH:Math.round(pr.height),leftOverflow:Math.round(dr.left-pr.left),rightOverflow:Math.round(pr.right-dr.right),bottomOverflow:Math.round(pr.bottom-dr.bottom),otherCellStyled:getComputedStyle(p.querySelector(".giencoder-calendar-cell-other")).color})' > $OUT/a-date.log 2>&1
echo "DATE: $(tail -1 $OUT/a-date.log)"
sleep 1
timeout 240 $AB screenshot "" $OUT/date-open.png > $OUT/a-shot2.log 2>&1
echo "SHOT-DATE: $(tail -1 $OUT/a-shot2.log)"

# 6 动效：确认 CSS 过渡存在，并在慢放中途取一帧
timeout 180 $AB eval 'var d=document.querySelector(".kb-coop-dialog");JSON.stringify({tp:getComputedStyle(d).transitionProperty,td:getComputedStyle(d).transitionDuration,timing:getComputedStyle(d).transitionTimingFunction})' > $OUT/a-tr.log 2>&1
echo "TRANS: $(tail -1 $OUT/a-tr.log)"
timeout 180 $AB eval 'document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}));JSON.stringify({hidden:document.querySelector(".kb-coop").hidden,cls:document.querySelector(".kb-coop").className})' > $OUT/a-esc.log 2>&1
echo "ESC: $(tail -1 $OUT/a-esc.log)"
sleep 1
# 慢放：把过渡拉长到 2.5s，再打开，在中途读一次计算样式
timeout 180 $AB eval 'var d=document.querySelector(".kb-coop-dialog");d.style.transitionDuration="2.5s, 2.5s";document.querySelector(".kb-coop-mask").style.transitionDuration="2.5s";var t=document.querySelector(".kb-stat--coop");var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));JSON.stringify({opened:!document.querySelector(".kb-coop").hidden})' > $OUT/a-slowopen.log 2>&1
echo "SLOW-OPEN: $(tail -1 $OUT/a-slowopen.log)"
timeout 60 $AB eval 'JSON.stringify({t0:{transform:getComputedStyle(document.querySelector(".kb-coop-dialog")).transform,opacity:getComputedStyle(document.querySelector(".kb-coop-dialog")).opacity}})' > $OUT/a-t0.log 2>&1
echo "T0: $(tail -1 $OUT/a-t0.log)"
sleep 1
timeout 60 $AB eval 'JSON.stringify({mid:{transform:getComputedStyle(document.querySelector(".kb-coop-dialog")).transform,opacity:getComputedStyle(document.querySelector(".kb-coop-dialog")).opacity}})' > $OUT/a-mid.log 2>&1
echo "MID: $(tail -1 $OUT/a-mid.log)"
timeout 240 $AB screenshot "" $OUT/motion-mid.png > $OUT/a-shot3.log 2>&1
echo "SHOT-MID: $(tail -1 $OUT/a-shot3.log)"
sleep 2
timeout 60 $AB eval 'JSON.stringify({end:{transform:getComputedStyle(document.querySelector(".kb-coop-dialog")).transform,opacity:getComputedStyle(document.querySelector(".kb-coop-dialog")).opacity}})' > $OUT/a-end.log 2>&1
echo "END: $(tail -1 $OUT/a-end.log)"
timeout 240 $AB screenshot "" $OUT/modal-final.png > $OUT/a-shot4.log 2>&1
echo "SHOT-FINAL: $(tail -1 $OUT/a-shot4.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

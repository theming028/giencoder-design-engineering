#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r13
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 300 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r13b" > $OUT/b-open.log 2>&1
echo "OPEN: $(tail -1 $OUT/b-open.log)"

timeout 180 $AB eval 'var t=document.querySelector(".kb-stat--coop");var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));JSON.stringify({opened:!document.querySelector(".kb-coop").hidden})' > $OUT/b-click.log 2>&1
echo "CLICK: $(tail -1 $OUT/b-click.log)"
sleep 1

# 下拉宽度链路
timeout 180 $AB eval 'var s=document.querySelector(".kb-coop-sel"),v=s.querySelector(".giencoder-select-view"),p=s.querySelector(".giencoder-select-popup");var sc=getComputedStyle(s),pc=getComputedStyle(p);var rules=[];for(var i=0;i<document.styleSheets.length;i++){var rs;try{rs=document.styleSheets[i].cssRules}catch(e){continue}for(var j=0;j<rs.length;j++){var rr=rs[j];if(rr.selectorText&&/kb-coop-sel .*select-popup/.test(rr.selectorText))rules.push(rr.cssText.slice(0,160))}}JSON.stringify({selW:s.getBoundingClientRect().width,viewW:v.getBoundingClientRect().width,popupW:p.getBoundingClientRect().width,popupMinW:pc.minWidth,popupWStyle:pc.width,popupBox:pc.boxSizing,popupLeft:pc.left,popupRight:pc.right,hitRules:rules})' > $OUT/b-width.log 2>&1
echo "WIDTH: $(tail -1 $OUT/b-width.log)"

# 动效：拉长到 9s，取中间帧（跨进程开销约 1-2s，仍能落在过渡中段）
timeout 180 $AB eval 'document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}));JSON.stringify({afterEscCls:document.querySelector(".kb-coop").className})' > $OUT/b-esc.log 2>&1
echo "ESC: $(tail -1 $OUT/b-esc.log)"
sleep 1
timeout 180 $AB eval 'var d=document.querySelector(".kb-coop-dialog");d.style.transitionDuration="9s";document.querySelector(".kb-coop-mask").style.transitionDuration="9s";var t=document.querySelector(".kb-stat--coop");var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));JSON.stringify({opened:!document.querySelector(".kb-coop").hidden})' > $OUT/b-slow.log 2>&1
echo "SLOW: $(tail -1 $OUT/b-slow.log)"
timeout 120 $AB eval 'var d=document.querySelector(".kb-coop-dialog");var cs=getComputedStyle(d);JSON.stringify({frame:{transform:cs.transform,opacity:cs.opacity},maskOpacity:getComputedStyle(document.querySelector(".kb-coop-mask")).opacity})' > $OUT/b-frame.log 2>&1
echo "FRAME1: $(tail -1 $OUT/b-frame.log)"
timeout 240 $AB screenshot "" $OUT/motion-mid.png > $OUT/b-shot1.log 2>&1
echo "SHOT-MID: $(tail -1 $OUT/b-shot1.log)"
timeout 120 $AB eval 'var d=document.querySelector(".kb-coop-dialog");var cs=getComputedStyle(d);JSON.stringify({frame:{transform:cs.transform,opacity:cs.opacity}})' > $OUT/b-frame2.log 2>&1
echo "FRAME2: $(tail -1 $OUT/b-frame2.log)"
# 还原时长并确认终态
timeout 180 $AB eval 'var d=document.querySelector(".kb-coop-dialog");d.style.transitionDuration="";document.querySelector(".kb-coop-mask").style.transitionDuration="";JSON.stringify({cleared:true})' > /dev/null 2>&1
sleep 9
timeout 180 $AB eval 'var d=document.querySelector(".kb-coop-dialog");var cs=getComputedStyle(d);JSON.stringify({end:{transform:cs.transform,opacity:cs.opacity},cls:document.querySelector(".kb-coop").className})' > $OUT/b-end.log 2>&1
echo "END: $(tail -1 $OUT/b-end.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

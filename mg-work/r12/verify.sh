#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r12
mkdir -p $OUT
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1

echo "################ 1. kanban.html ################"
timeout 240 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r20" > $OUT/k1.log 2>&1
echo "OPEN: $(tail -2 $OUT/k1.log | tr '\n' ' ')"

timeout 180 $AB eval 'function d(e){return e?getComputedStyle(e).display:"n/a"}var btn=document.querySelector("[aria-label=\"切换侧边栏\"]");var wrap=btn?btn.parentElement.parentElement:null;var fab=document.querySelector(".kb-fab");var cs=fab?getComputedStyle(fab):null;JSON.stringify({wsBtnFound:btn?1:0,wsWrapDisplay:d(wrap),wsWrapOpacity:wrap?getComputedStyle(wrap).opacity:null,fabBg:cs?cs.backgroundImage.slice(0,90):null,fabColor:cs?cs.color:null,fabShadow:cs?cs.boxShadow.slice(0,70):null,fabIconD:fab?fab.querySelector("path").getAttribute("d").slice(0,28):null,laneIdle:getComputedStyle(document.querySelector(".kb-col")).backgroundColor})' > $OUT/k-state.log 2>&1
echo "STATE: $(tail -1 $OUT/k-state.log)"

timeout 120 $AB hover ".kb-col" > /dev/null 2>&1
timeout 120 $AB eval 'var c=document.querySelector(".kb-col");JSON.stringify({laneHovered:getComputedStyle(c).backgroundColor,isHover:c.matches(":hover")})' > $OUT/k-lane.log 2>&1
echo "LANE-HOVER: $(tail -1 $OUT/k-lane.log)"

timeout 120 $AB hover ".kb-topbar" > /dev/null 2>&1
timeout 120 $AB eval 'JSON.stringify({laneIdleAgain:getComputedStyle(document.querySelector(".kb-col")).backgroundColor})' > $OUT/k-lane2.log 2>&1
echo "LANE-IDLE: $(tail -1 $OUT/k-lane2.log)"

timeout 180 $AB eval 'var t=document.querySelector(".kb-stat--coop");var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));JSON.stringify({open:!document.querySelector(".kb-coop").hidden})' > $OUT/k-click.log 2>&1
echo "CLICK: $(tail -1 $OUT/k-click.log)"

timeout 180 $AB eval 'var m=document.querySelector(".kb-coop"),dl=document.querySelector(".kb-coop-dialog"),mn=document.querySelector("main");var dr=dl.getBoundingClientRect(),mr=mn.getBoundingClientRect(),wrap=document.querySelector(".kb-coop-tblwrap").getBoundingClientRect(),th=document.querySelector(".kb-coop-tbl .giencoder-table-th").getBoundingClientRect(),trs=document.querySelectorAll(".kb-coop-tbl tbody .giencoder-table-tr"),f=document.querySelector(".kb-coop-filters").getBoundingClientRect();var sw=function(e){var r=e.getBoundingClientRect();return Math.round(r.width)};JSON.stringify({modalParentIsMain:m.parentElement===mn,main:Math.round(mr.width)+"x"+Math.round(mr.height)+"@"+Math.round(mr.left)+","+Math.round(mr.top),dialog:Math.round(dr.width)+"x"+Math.round(dr.height)+"@"+Math.round(dr.left)+","+Math.round(dr.top),wRatio:(dr.width/mr.width).toFixed(3),topGap:Math.round(dr.top-mr.top),bottomGap:Math.round(mr.bottom-dr.bottom),thH:Math.round(th.height),thBg:getComputedStyle(document.querySelector(".kb-coop-tbl .giencoder-table-th")).backgroundColor,rowH:Math.round(trs[1].getBoundingClientRect().height),rowPitch:Math.round(trs[1].getBoundingClientRect().top-trs[0].getBoundingClientRect().top),rowBg:getComputedStyle(trs[0].querySelector("td")).backgroundColor,wrapBg:getComputedStyle(document.querySelector(".kb-coop-tblwrap")).backgroundColor,wrapBorder:getComputedStyle(document.querySelector(".kb-coop-tblwrap")).borderTopWidth+" "+getComputedStyle(document.querySelector(".kb-coop-tblwrap")).borderTopColor,wrapRadius:getComputedStyle(document.querySelector(".kb-coop-tblwrap")).borderTopLeftRadius,filterW:[sw(document.querySelector(".kb-coop-search")),sw(document.querySelectorAll(".kb-coop-sel")[0]),sw(document.querySelectorAll(".kb-coop-sel")[1]),sw(document.querySelector(".kb-coop-date"))].join("/"),firstTdPadLeft:getComputedStyle(document.querySelector(".kb-coop-tbl tbody td")).paddingLeft,closeBox:Math.round(document.querySelector(".kb-coop-close").getBoundingClientRect().width)+"x"+Math.round(document.querySelector(".kb-coop-close").getBoundingClientRect().height),closeBorder:getComputedStyle(document.querySelector(".kb-coop-close")).borderTopWidth,closeColor:getComputedStyle(document.querySelector(".kb-coop-close")).color})' > $OUT/k-geo.log 2>&1
echo "GEO: $(tail -1 $OUT/k-geo.log)"

timeout 240 $AB screenshot "" $OUT/modal-r12.png > $OUT/k-shot.log 2>&1
echo "SHOT: $(tail -1 $OUT/k-shot.log)"

timeout 120 $AB eval 'document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}));JSON.stringify({closed:document.querySelector(".kb-coop").hidden})' > $OUT/k-esc.log 2>&1
echo "ESC: $(tail -1 $OUT/k-esc.log)"

timeout 120 $AB eval 'var s=[];for(var i=0;i<document.styleSheets.length;i++){try{var rs=document.styleSheets[i].cssRules;for(var j=0;j<rs.length;j++){if(rs[j].selectorText&&rs[j].selectorText.indexOf("kb-col:hover")>=0)s.push(rs[j].cssText.slice(0,90))}}catch(e){}}JSON.stringify({laneHoverRule:s})' > $OUT/k-rule.log 2>&1
echo "RULE: $(tail -1 $OUT/k-rule.log)"
timeout 60 $AB close --all > /dev/null 2>&1

echo
echo "################ 2. req-kanban.html ################"
timeout 240 $AB open "http://127.0.0.1:8866/pages/req-kanban.html?v=r20" > $OUT/q1.log 2>&1
echo "OPEN: $(tail -2 $OUT/q1.log | tr '\n' ' ')"
timeout 180 $AB eval 'var btn=document.querySelector("[aria-label=\"切换侧边栏\"]");var wrap=btn?btn.parentElement.parentElement:null;var fab=document.querySelector(".kb-fab");JSON.stringify({wsWrapDisplay:wrap?getComputedStyle(wrap).display:"n/a",fabBg:fab?getComputedStyle(fab).backgroundImage.slice(0,70):null})' > $OUT/q-state.log 2>&1
echo "STATE: $(tail -1 $OUT/q-state.log)"
timeout 60 $AB close --all > /dev/null 2>&1

echo
echo "################ 3. base.html ################"
timeout 240 $AB open "http://127.0.0.1:8866/pages/base.html?v=r20" > $OUT/b1.log 2>&1
echo "OPEN: $(tail -2 $OUT/b1.log | tr '\n' ' ')"
timeout 180 $AB eval 'var m=document.querySelector("main");var cs=getComputedStyle(m);var layers=cs.backgroundImage.split(/,(?![^(]*\))/);var c=document.querySelector("main [class~=\"w-[800px]\"]");JSON.stringify({layerCount:layers.length,layers:layers.map(function(x){return x.slice(0,52)}),composerW:c?Math.round(c.getBoundingClientRect().width):null,composerH:c?Math.round(c.getBoundingClientRect().height):null})' > $OUT/b-dot.log 2>&1
echo "DOTBG: $(tail -1 $OUT/b-dot.log)"
timeout 240 $AB screenshot "" $OUT/base-r12.png > $OUT/b-shot.log 2>&1
echo "SHOT: $(tail -1 $OUT/b-shot.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

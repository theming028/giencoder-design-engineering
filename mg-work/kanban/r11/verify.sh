#!/bin/bash
# r11 验证：一个会话内完成 打开→量色→点开模态→截图
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/kanban/r11

timeout 60 $AB close --all > $OUT/v-close.log 2>&1
sleep 1
timeout 240 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r11" > $OUT/v-open.log 2>&1
echo "OPEN: $(tail -2 $OUT/v-open.log | tr '\n' ' ')"

timeout 120 $AB eval 'JSON.stringify({w:innerWidth,h:innerHeight,panel:document.querySelectorAll(".kb-panel").length,coop:document.querySelectorAll(".kb-stat--coop").length})' > $OUT/v-dom.log 2>&1
echo "DOM: $(cat $OUT/v-dom.log | tail -1)"

timeout 240 $AB screenshot "" $OUT/v-board.png > $OUT/v-shot1.log 2>&1
echo "SHOT1: $(tail -1 $OUT/v-shot1.log)"

timeout 180 $AB eval 'var m=document.querySelector(".kb-tag--mid"),h=document.querySelector(".kb-tag--high"),l=document.querySelector(".kb-tag--low");JSON.stringify({mid:m?getComputedStyle(m).color+" / "+getComputedStyle(m).backgroundColor:null,high:h?getComputedStyle(h).color+" / "+getComputedStyle(h).backgroundColor:null,low:l?getComputedStyle(l).color+" / "+getComputedStyle(l).backgroundColor:null})' > $OUT/v-colors.log 2>&1
echo "COLORS: $(tail -1 $OUT/v-colors.log)"

timeout 180 $AB click ".kb-stat--coop" > $OUT/v-click.log 2>&1
echo "CLICK: $(tail -1 $OUT/v-click.log)"

timeout 120 $AB eval 'var m=document.querySelector(".kb-coop");JSON.stringify({hidden:m?m.hidden:null,cls:m?m.className:null,dialog:m?!!m.querySelector(".kb-coop-dialog"):null,rows:m?m.querySelectorAll("tbody tr").length:0,prio:m?Array.prototype.slice.call(m.querySelectorAll(".kb-td-prio")).map(function(e){return e.textContent+":"+getComputedStyle(e).color}).join(" | "):null})' > $OUT/v-modal.log 2>&1
echo "MODAL: $(tail -1 $OUT/v-modal.log)"

timeout 240 $AB screenshot "" $OUT/v-modal.png > $OUT/v-shot2.log 2>&1
echo "SHOT2: $(tail -1 $OUT/v-shot2.log)"

timeout 120 $AB eval 'var m=document.querySelector(".kb-coop"),d=document.querySelector(".kb-coop-dialog");var r=d?d.getBoundingClientRect():null;JSON.stringify({dialog:r?Math.round(r.width)+"x"+Math.round(r.height)+"@"+Math.round(r.left)+","+Math.round(r.top):null,panelBg:d?getComputedStyle(d).backgroundColor:null,mask:(document.querySelector(".kb-coop-mask")?getComputedStyle(document.querySelector(".kb-coop-mask")).backgroundColor+"/"+getComputedStyle(document.querySelector(".kb-coop-mask")).backdropFilter:null)})' > $OUT/v-geo.log 2>&1
echo "GEO: $(tail -1 $OUT/v-geo.log)"

timeout 60 $AB close --all > $OUT/v-close2.log 2>&1
echo ALLDONE

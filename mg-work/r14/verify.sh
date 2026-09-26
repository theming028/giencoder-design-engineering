#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r14
mkdir -p $OUT
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 300 $AB open "http://127.0.0.1:8866/pages/kanban.html?v=r14a" > $OUT/a-open.log 2>&1
echo "OPEN: $(tail -1 $OUT/a-open.log)"

timeout 180 $AB eval 'var cs=document.querySelectorAll(".kb-stat[data-modal-title]");var o=[];for(var i=0;i<cs.length;i++){o.push(cs[i].className.replace("kb-stat ","")+":"+cs[i].getAttribute("data-modal-title")+":"+getComputedStyle(cs[i]).cursor)}JSON.stringify({cards:o})' > $OUT/a-cards.log 2>&1
echo "CARDS: $(tail -1 $OUT/a-cards.log)"

open_and_check() {
  local idx=$1
  timeout 180 $AB eval "var t=document.querySelectorAll('.kb-stat[data-modal-title]')[$idx];var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));JSON.stringify({opened:!document.querySelector('.kb-coop').hidden})" > $OUT/b-open$idx.log 2>&1
  sleep 1
  timeout 180 $AB eval 'var m=document.querySelector(".kb-coop");JSON.stringify({title:m.querySelector(".giencoder-modal-title").textContent,modalAria:m.getAttribute("aria-label"),dlgAria:m.querySelector(".kb-coop-dialog").getAttribute("aria-label")})' > $OUT/a-t$idx.log 2>&1
  echo "TITLE[$idx]: $(tail -1 $OUT/a-t$idx.log)"
  timeout 180 $AB eval 'document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}));1' > /dev/null 2>&1
  sleep 1
}
open_and_check 0
open_and_check 1
timeout 240 $AB screenshot "" $OUT/review-modal.png > /dev/null 2>&1
open_and_check 2
open_and_check 3

timeout 180 $AB eval 'var t=document.querySelectorAll(".kb-stat[data-modal-title]")[0];var r=t.getBoundingClientRect();t.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true,clientX:r.left+5,clientY:r.top+5}));JSON.stringify({opened:!document.querySelector(".kb-coop").hidden})' > /dev/null 2>&1
sleep 1
timeout 180 $AB eval 'var ths=document.querySelectorAll(".kb-coop-tbl .giencoder-table-th");var o=[];for(var i=0;i<ths.length;i++){var cs=getComputedStyle(ths[i]);o.push(ths[i].textContent.slice(0,4)+"/"+cs.fontSize+"/"+cs.fontWeight+"/h"+Math.round(ths[i].getBoundingClientRect().height))}var a=document.querySelector(".kb-coop-tbl tbody tr .kb-td-title a");var ac=getComputedStyle(a);var hv=document.querySelector(".kb-coop-tbl tbody tr.kb-row-hover .kb-td-title a");JSON.stringify({ths:o,link:{tag:a.tagName,cls:a.getAttribute("class"),comp:a.getAttribute("data-component"),color:ac.color,dec:ac.textDecorationLine,cursor:ac.cursor},rowHoverTitle:hv?getComputedStyle(hv).color:null,rowH:Math.round(document.querySelector(".kb-coop-tbl tbody tr").getBoundingClientRect().height),titleEllipsis:getComputedStyle(document.querySelector(".kb-coop-tbl tbody tr .kb-td-title")).textOverflow})' > $OUT/a-table.log 2>&1
echo "TABLE: $(tail -1 $OUT/a-table.log)"

timeout 120 $AB hover ".kb-coop-tbl tbody tr:first-child .kb-td-title a" > /dev/null 2>&1
timeout 180 $AB eval 'var a=document.querySelector(".kb-coop-tbl tbody tr:first-child .kb-td-title a");JSON.stringify({color:getComputedStyle(a).color,dec:getComputedStyle(a).textDecorationLine})' > $OUT/a-linkhover.log 2>&1
echo "LINK-HOVER: $(tail -1 $OUT/a-linkhover.log)"
timeout 240 $AB screenshot "" $OUT/table-final.png > /dev/null 2>&1
echo "SHOT: ok"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

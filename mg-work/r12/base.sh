#!/bin/bash
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
cd /e/GienCoder/giencoder-design-engineering || exit 1
OUT=mg-work/r12
mkdir -p $OUT
timeout 60 $AB close --all > /dev/null 2>&1
sleep 1
timeout 240 $AB open "http://127.0.0.1:8866/pages/base.html?v=r16" > $OUT/base-open.log 2>&1
echo "OPEN: $(tail -2 $OUT/base-open.log | tr '\n' ' ')"
timeout 240 $AB screenshot "" $OUT/base.png > $OUT/base-shot.log 2>&1
echo "SHOT: $(tail -1 $OUT/base-shot.log)"
timeout 180 $AB eval 'var m=document.querySelector("main");var r=m.getBoundingClientRect();var cs=getComputedStyle(m);JSON.stringify({main:Math.round(r.width)+"x"+Math.round(r.height)+"@"+Math.round(r.left)+","+Math.round(r.top),bg:cs.backgroundImage.slice(0,120),bgSize:cs.backgroundSize,bgColor:cs.backgroundColor})' > $OUT/base-main.log 2>&1
echo "MAIN: $(tail -1 $OUT/base-main.log)"
timeout 60 $AB close --all > /dev/null 2>&1
echo ALLDONE

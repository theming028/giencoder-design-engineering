#!/usr/bin/env bash
# r101 第②批 · Run D：终态复核（1440 + 2560）+ 渐隐带 + 汇总行左键 + 双视口自适应
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"

READ="(function(){var H=document.querySelector('.r93-conv-host');var R=function(e){if(!e)return null;var b=e.getBoundingClientRect();return [Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)];};var sc=H.querySelector('.r93-scroll');var tb=H.querySelector('.r93-tbsticky');var af=getComputedStyle(tb,'::after');var hs=getComputedStyle(document.querySelector('header[class*=\"h-12\"]'));var fs={};[].forEach.call(H.querySelectorAll('.r93-t12l'),function(e){var v=getComputedStyle(e).fontSize;fs[v]=(fs[v]||0)+1;});return JSON.stringify({vw:window.innerWidth,host:R(H),bar:R(H.querySelector('.r93-bar')),scroll:R(sc),scrollPad:getComputedStyle(sc).padding,pill:R(H.querySelector('.r93-tobottom')),fade:{h:af.height,bottom:af.bottom},firstReal:R(H.querySelector('.r93-wrap > *')),sk:H.querySelectorAll('.r93-sk').length,hdrSize:hs.backgroundSize,hdrBox:R(document.querySelector('header[class*=\"h-12\"]')),art0:R(H.querySelector('.r93-artcard')),t12l:fs});})()"

TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1

echo "=== [1] 1440 终态读数 ==="
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 1500 >/dev/null 2>&1
"$NODE" "$AB" eval "$READ"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fin2-1440.png" >/dev/null 2>&1

echo "=== [2] 汇总行**整行左键**（r100 ④ 行为是否保住） ==="
"$NODE" "$AB" eval "(function(){var r=document.querySelector('.r93-conv-host .r93-drow');r.scrollIntoView({block:'center'});r.setAttribute('data-r101-row','1');return 'ok';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 260 >/dev/null 2>&1
"$NODE" "$AB" click '[data-r101-row] .r93-dname' >/dev/null 2>&1
"$NODE" "$AB" wait 400 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var m=document.querySelector('.r93-ctx');if(!m)return 'no menu';var R=m.getBoundingClientRect();return JSON.stringify({open:m.classList.contains('giencoder-popup-open'),labels:[].map.call(m.querySelectorAll('.r93-ctx-label'),function(e){return e.textContent;}),box:[Math.round(R.x),Math.round(R.y),Math.round(R.width),Math.round(R.height)]});})()"
"$NODE" "$AB" press Escape >/dev/null 2>&1

echo "=== [3] 滚到底部 → 渐隐带取证截图 ==="
"$NODE" "$AB" eval "var s=document.querySelector('.r93-conv-host .r93-scroll');s.scrollTop=s.scrollHeight;'bottom'" >/dev/null 2>&1
"$NODE" "$AB" wait 320 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fin2-bottom.png" >/dev/null 2>&1
"$NODE" "$AB" eval "var s=document.querySelector('.r93-conv-host .r93-scroll');JSON.stringify({top:s.scrollTop,max:s.scrollHeight-s.clientHeight,pill:Math.round(document.querySelector('.r93-tobottom').getBoundingClientRect().y)})"

echo "=== [4] 2560 自适应读数 ==="
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 2560 1200 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 1500 >/dev/null 2>&1
"$NODE" "$AB" eval "$READ"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fin2-2560.png" >/dev/null 2>&1

#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
TS=$(date +%s)
AB() { "$NODE" "$CLI" "$@"; }
URL="file:///$ROOT/pages/conversation.html?v=$TS"
AB open "$URL" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2800 >/dev/null 2>&1
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 800 >/dev/null 2>&1
AB click "[data-td-add]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1
echo "--- 工具条每个直接子元素的盒子 ---"
AB eval "[].map.call(document.querySelector('.td-mod-bar').children,function(e){var r=e.getBoundingClientRect();return (e.className||e.tagName).slice(0,32)+' ['+Math.round(r.left)+','+Math.round(r.width)+'] d='+getComputedStyle(e).display;}).join('\n')" 2>&1
echo "--- 动作组内每枚按钮 ---"
AB eval "[].map.call(document.querySelectorAll('.td-mod-bar-acts > *'),function(e){var r=e.getBoundingClientRect();return (e.getAttribute('data-td-rv-act')||e.getAttribute('data-td-rv-opts')||e.getAttribute('data-td-commit')||e.tagName)+' ['+Math.round(r.left)+','+Math.round(r.width)+'] visible='+(r.width>0);}).join('\n')" 2>&1
echo "--- 工具条与侧栏宽度 ---"
AB eval "JSON.stringify({bar:document.querySelector('.td-mod-bar').clientWidth,barScroll:document.querySelector('.td-mod-bar').scrollWidth,panel:document.querySelector('.td-browse').clientWidth})" 2>&1
echo "--- 折叠项图标是否在（展开态应为上下相背箭头） ---"
AB eval "(function(){var ico=document.querySelector('[data-td-rv-fold] .td-mm-ico');return JSON.stringify({paths:ico.querySelectorAll('path').length,d:[].map.call(ico.querySelectorAll('path'),function(p){return p.getAttribute('d');}),w:ico.getBoundingClientRect().width,name:document.querySelector('[data-td-rv-fold-name]').textContent});})()" 2>&1
echo "--- 「展开全部文件」项可见性 ---"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "(function(){var b=document.querySelector('[data-td-rv-fold]');var r=b.getBoundingClientRect();var i=b.querySelector('.td-mm-ico').getBoundingClientRect();return JSON.stringify({item:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],ico:[Math.round(i.left),Math.round(i.width),Math.round(i.height)],name:document.querySelector('[data-td-rv-fold-name]').textContent});})()" 2>&1
AB screenshot "E:/GienCoder/giencoder-design-engineering/mg-work/r107/raw/y15-menu-zoom.png" >/dev/null 2>&1
echo "############ done ############"

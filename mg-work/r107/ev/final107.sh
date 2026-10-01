#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
TS=$(date +%s)
AB() { "$NODE" "$CLI" "$@"; }
URL="file:///$ROOT/pages/conversation.html?v=$TS"

AB open "$URL" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2600 >/dev/null 2>&1

echo "### A 关态（未展开侧栏）—— 单标签 × 应不可见"
AB eval "JSON.stringify({tabs:document.querySelectorAll('.td-browse-tab').length,single:document.querySelector('.td-browse-tabs').classList.contains('is-single'),xDisplay:(function(){var x=document.querySelector('.td-tab-x');return x?getComputedStyle(x).display:null;})(),panelOn:document.querySelector('div:has(> main)').classList.contains('av-browse-on')})" 2>&1

AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 800 >/dev/null 2>&1
AB screenshot "$OUT/f1-files-open.png" >/dev/null 2>&1

echo "### B 文件模块回归：折叠目录 / 选中文件 / 隐藏文件目录"
AB eval "JSON.stringify({rows:document.querySelectorAll('.td-bf').length,closed:document.querySelectorAll('.td-bf.is-closed').length,hidden:document.querySelectorAll('.td-bf.is-hidden').length})" 2>&1
AB click '[data-node="snake"] .td-bf-arrow' >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB eval "JSON.stringify({snakeClosed:document.querySelector('[data-node=\"snake\"]').classList.contains('is-closed'),visible:document.querySelectorAll('.td-bf:not(.is-hidden)').length})" 2>&1
AB click '[data-node="snake"]' >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB click ".td-browse-files .td-bf.is-file:not(.is-hidden)" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB eval "JSON.stringify({active:(document.querySelector('.td-bf.is-active')||{}).textContent})" 2>&1
AB click '[data-td-tree-toggle]' >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB eval "JSON.stringify({noTree:document.querySelector('.td-browse-body').classList.contains('is-no-tree')})" 2>&1
AB click '[data-td-tree-toggle]' >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB eval "JSON.stringify({noTree:document.querySelector('.td-browse-body').classList.contains('is-no-tree')})" 2>&1

echo "### C 四模块全开 + 回到文件模块（标签切换）"
for m in review terminal browser; do
  AB click ".td-browse-add" >/dev/null 2>&1
  AB wait 220 >/dev/null 2>&1
  AB click "[data-td-open-mod=\"$m\"]" >/dev/null 2>&1
  AB wait 350 >/dev/null 2>&1
done
AB eval "JSON.stringify({tabs:[].map.call(document.querySelectorAll('.td-browse-tab'),function(t){return t.getAttribute('data-td-mod')+(t.classList.contains('is-active')?'*':'');}),rects:[].map.call(document.querySelectorAll('.td-browse-tab'),function(t){var r=t.getBoundingClientRect();return Math.round(r.left)+'~'+Math.round(r.right);}),addBtn:(function(){var b=document.querySelector('.td-browse-add');var r=b.getBoundingClientRect();return Math.round(r.left)+'~'+Math.round(r.right);})()})" 2>&1
AB screenshot "$OUT/f2-four-tabs.png" >/dev/null 2>&1
AB click '[data-td-tab][data-td-mod="files"]' >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB eval "JSON.stringify({filesVisible:!document.querySelector('.td-browse-body').hasAttribute('hidden'),tree:document.querySelectorAll('.td-bf:not(.is-hidden)').length})" 2>&1

echo "### D 暗色档"
AB eval "document.documentElement.setAttribute('giencoder-theme','dark');'ok'" >/dev/null 2>&1
AB wait 600 >/dev/null 2>&1
AB screenshot "$OUT/f3-dark-files.png" >/dev/null 2>&1
AB click '[data-td-tab][data-td-mod="review"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB screenshot "$OUT/f4-dark-review.png" >/dev/null 2>&1
AB click '[data-td-tab][data-td-mod="terminal"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB screenshot "$OUT/f5-dark-terminal.png" >/dev/null 2>&1
AB click '[data-td-tab][data-td-mod="browser"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click ".td-url-annot" >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB screenshot "$OUT/f6-dark-browser.png" >/dev/null 2>&1
AB eval "JSON.stringify({annotBg:getComputedStyle(document.querySelector('.td-annot-bar')).backgroundColor,diffAdd:getComputedStyle(document.querySelector('.td-dr.is-add')).backgroundColor})" 2>&1
AB eval "document.documentElement.removeAttribute('giencoder-theme');'ok'" >/dev/null 2>&1

echo "### E 2560 视口 + 最大化"
AB set viewport 2560 1200 >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1
AB click '[data-td-tab][data-td-mod="review"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({panelW:Math.round(document.getElementById('av-browse-slot').getBoundingClientRect().width),mainW:Math.round(document.querySelector('main').getBoundingClientRect().width)})" 2>&1
AB click ".td-browse-acts [data-td-max]" >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB eval "JSON.stringify({panelW:Math.round(document.getElementById('av-browse-slot').getBoundingClientRect().width),mainW:Math.round(document.querySelector('main').getBoundingClientRect().width)})" 2>&1
AB screenshot "$OUT/f7-max-2560.png" >/dev/null 2>&1
echo "### done"

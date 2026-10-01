#!/usr/bin/env bash
# 第十二拍边界复测（修正版）：B 并排视图 · C 字号杠杆 · D 窄档 min(296,86%)
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
step() { "$NODE" "$CLI" "$@" >/dev/null 2>&1; }
run()  { "$NODE" "$CLI" "$@" 2>&1; }

step open "$URL"; step set viewport 1440 900; step wait 2800
step click ".r93-baract[data-r93-browse]"; step wait 1400
step click ".td-browse-add"; step wait 400
step click "[data-td-open-mod='review']"; step wait 700

echo "=== [A2] 先开抽屉（后续 B/C/D 都在开着抽屉的状态下量） ==="
step click "[data-td-rv-act='tree']"; step wait 500

echo "=== [C] --ui-fs = 18 杠杆（抽屉开着量） ==="
run eval "(function(){document.documentElement.style.setProperty('--ui-fs','18');return 'set';})()" | tail -1
step wait 700
run eval "(function(){var r=document.querySelector('.td-tf'),h=document.querySelector('.td-tree-h'),n=document.querySelector('.td-tree-panel');return JSON.stringify({rowH:Math.round(r.getBoundingClientRect().height),rowFS:getComputedStyle(r).fontSize,headH:Math.round(h.getBoundingClientRect().height),panelW:Math.round(n.getBoundingClientRect().width)});})()" | tail -1
run eval "(function(){document.documentElement.style.removeProperty('--ui-fs');return 'reset';})()" | tail -1
step wait 600

echo "=== [D] 视口 620（右栏变窄）下：面板宽应落到 86% ==="
step set viewport 620 800
step wait 1000
run eval "(function(){var p=document.querySelector('.td-tree-panel'),n=document.querySelector('.td-browse');var pw=Math.round(p.getBoundingClientRect().width),nw=Math.round(n.getBoundingClientRect().width);return JSON.stringify({panelW:pw,paneW:nw,pct:Math.round(pw/nw*100),treeHidden:document.querySelector('[data-td-tree]').hasAttribute('hidden')});})()" | tail -1
step set viewport 1440 900
step wait 900

echo "=== [B] 切「并排视图」：统一行应 display:none、并排行应有 border-top ==="
step click "[data-td-rv-opts]"; step wait 500
step click "[data-td-rv-view='split']"; step wait 700
run eval "(function(){var b=document.querySelector('.td-rv-body');var c=document.querySelector('.td-diff');var u=c.querySelector('.td-diff-rows:not(.td-diff-split)'),s=c.querySelector('.td-diff-split');return JSON.stringify({isSplit:b.classList.contains('is-split'),uniDisplay:getComputedStyle(u).display,uniBorder:getComputedStyle(u).borderTopWidth,splitDisplay:getComputedStyle(s).display,splitBorder:getComputedStyle(s).borderTopWidth,cardRadius:getComputedStyle(c).borderTopLeftRadius,cardGap:getComputedStyle(b).gap});})()" | tail -1
echo "--- 并排下折叠一张卡，看边框是否只剩外框（无残留分隔线） ---"
step click "[data-td-diff-h='1']"; step wait 500
run eval "(function(){var c=document.querySelector('.td-diff');return JSON.stringify({open:c.classList.contains('is-open'),rowsDisplay:getComputedStyle(c.querySelector('.td-diff-rows')).display,h:Math.round(c.getBoundingClientRect().height)});})()" | tail -1
echo done

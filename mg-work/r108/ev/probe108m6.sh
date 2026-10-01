#!/usr/bin/env bash
# 第十二拍 [B] 复测：**先关抽屉**（遮罩会挡住工具条的点击）再切并排视图。
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

echo "=== 确认抽屉是关着的 ==="
run eval "JSON.stringify({treeHidden:document.querySelector('[data-td-tree]').hasAttribute('hidden')})" | tail -1

echo "=== 切并排视图 ==="
step click "[data-td-rv-opts]"; step wait 600
run eval "JSON.stringify({optsOpen:!document.querySelector('.td-rv-opts').hasAttribute('hidden')})" | tail -1
step click "[data-td-rv-view='split']"; step wait 700
run eval "(function(){var b=document.querySelector('.td-rv-body');var c=document.querySelector('.td-diff');var u=c.querySelector('.td-diff-rows:not(.td-diff-split)'),s=c.querySelector('.td-diff-split');return JSON.stringify({isSplit:b.classList.contains('is-split'),uniDisplay:getComputedStyle(u).display,splitDisplay:getComputedStyle(s).display,splitBorder:getComputedStyle(s).borderTopWidth,cardRadius:getComputedStyle(c).borderTopLeftRadius,cardGap:getComputedStyle(b).gap,cardBox:[Math.round(c.getBoundingClientRect().width),Math.round(c.getBoundingClientRect().height)]});})()" | tail -1
step screenshot ".td-mod.td-rv" "$ROOT/mg-work/r108/raw/m-1440-diff-split.png"

echo "=== 并排 + 折叠第一张卡 ==="
step click "[data-td-diff-h='1']"; step wait 600
run eval "(function(){var c=document.querySelector('.td-diff');return JSON.stringify({open:c.classList.contains('is-open'),h:Math.round(c.getBoundingClientRect().height),rowsDisplay:getComputedStyle(c.querySelector('.td-diff-split')).display});})()" | tail -1
step click "[data-td-diff-h='1']"; step wait 500
echo done

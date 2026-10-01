#!/usr/bin/env bash
# 第十三拍补拍：④ 产物卡整卡可点 → 预览层（上一版截 `main` 漏掉了，预览层在 main 右侧、覆盖右栏）。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
RAW="$ROOT/mg-work/r108/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

step() { "$NODE" "$CLI" "$@" >/dev/null 2>&1; }
mkdir -p "$RAW"

step open "$URL"
step set viewport 1440 900
step wait 3800
step click ".r93-baract[data-r93-browse]"
step wait 1200

echo "### [4a] 点产物卡「图标区」（不是「预览」按钮）"
step click ".td-sum-art .td-sum-arti"
step wait 700
step screenshot ".td-sum-prev" "$RAW/n-1440-art-preview.png"
step screenshot ".td-browse"   "$RAW/n-1440-art-pane.png"

echo "### [4b] 掩掉 → 确认可反复开"
step click "[data-td-prev-x]"
step wait 400
step click ".td-sum-art .td-sum-arti"
step wait 700
step eval "JSON.stringify((function(){var p=document.querySelector('.td-sum-prev');return {pvHidden:p.hidden, name:(p.querySelector('[data-td-prev-name]')||{}).textContent};})())"
step click "[data-td-prev-x]"
step wait 300

echo "### [3] 审查模块：diff 折叠图标 + 工具条"
step click ".td-browse-add"
step wait 400
step click "[data-td-open-mod='review']"
step wait 900
step screenshot ".td-mod.td-rv .td-mod-bar" "$RAW/n-1440-revbar.png"
step screenshot ".td-diff" "$RAW/n-1440-diff.png"
echo done

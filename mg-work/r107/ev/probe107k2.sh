#!/usr/bin/env bash
# 第十拍 窄栏压力测试：右栏压到 315px，三枚菜单是否仍留在面板内
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
RAW="$ROOT/mg-work/r107/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

step() { "$NODE" "$CLI" "$@" >/dev/null 2>&1; }
snap() { "$NODE" "$CLI" eval "$(cat "$EV/p107k_narrow.js")" 2>&1 | tail -1; }

step open "$URL"
step set viewport 1440 900
step wait 2600
step click ".r93-baract[data-r93-browse]"
step wait 1500
step click ".td-browse-add"; step wait 400
step click "[data-td-open-mod='review']"; step wait 800
step eval "document.getElementById('av-browse-slot').style.setProperty('--av-browse-w','315px')"
step wait 900

echo "### narrow-base"
snap
echo "### narrow-scope"
step click "[data-td-rv-scope]"; step wait 500; snap
step screenshot "$RAW/k-narrow-scope.png"
step eval "document.body.click()"; step wait 300
echo "### narrow-opts"
step click "[data-td-rv-opts]"; step wait 500; snap
step screenshot "$RAW/k-narrow-opts.png"
step eval "document.body.click()"; step wait 300
echo "### narrow-commit"
step click "[data-td-commit]"; step wait 500; snap
step screenshot "$RAW/k-narrow-commit.png"

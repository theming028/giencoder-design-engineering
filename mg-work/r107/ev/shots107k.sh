#!/usr/bin/env bash
# 第十拍 目视取证：三枚 rv 菜单 + 模块菜单（回归），1440
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
RAW="$ROOT/mg-work/r107/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

step() { "$NODE" "$CLI" "$@" >/dev/null 2>&1; }

step open "$URL"
step set viewport 1440 900
step wait 2600
step click ".r93-baract[data-r93-browse]"
step wait 1500
step click ".td-browse-add"; step wait 400
step click "[data-td-open-mod='review']"; step wait 800

step click "[data-td-rv-scope]"; step wait 500
step screenshot "$RAW/k-1440-scope.png"
step eval "document.body.click()"; step wait 300

step click "[data-td-rv-opts]"; step wait 500
step screenshot "$RAW/k-1440-opts.png"
step eval "document.body.click()"; step wait 300

step click "[data-td-commit]"; step wait 500
step screenshot "$RAW/k-1440-commit.png"
step eval "document.body.click()"; step wait 300

step click ".td-browse-add"; step wait 500
step screenshot "$RAW/k-1440-modmenu.png"
step eval "document.body.click()"; step wait 300

# ---- 窄档：右栏压到 315，看 clamp 是否把菜单留在了面板内 ----
step set viewport 1024 900
step wait 900
step click "[data-td-rv-opts]"; step wait 500
step screenshot "$RAW/k-1024-opts.png"
step eval "document.body.click()"; step wait 300
step click "[data-td-rv-scope]"; step wait 500
step screenshot "$RAW/k-1024-scope.png"
echo done

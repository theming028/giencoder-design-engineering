#!/usr/bin/env bash
# 第十拍 ① 取证：四枚下拉「触发器 vs 菜单」几何对照（1440）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

step() { "$NODE" "$CLI" "$@" >/dev/null 2>&1; }
snap() { "$NODE" "$CLI" eval "$(cat "$EV/p107k_pos.js")" 2>&1 | tail -1; }

step open "$URL"
step set viewport 1440 900
step wait 2600
step click ".r93-baract[data-r93-browse]"
step wait 1400
step click ".td-browse-add"; step wait 400
step click "[data-td-open-mod='review']"; step wait 800

echo "### frame=base (no menu open)"
snap

echo "### frame=modmenu"
step click ".td-browse-add"; step wait 500
snap
step eval "document.body.click()"; step wait 300

echo "### frame=scopemenu"
step click "[data-td-rv-scope]"; step wait 500
snap
step eval "document.body.click()"; step wait 300

echo "### frame=opts"
step click "[data-td-rv-opts]"; step wait 500
snap
step eval "document.body.click()"; step wait 300

echo "### frame=commit"
step click "[data-td-commit]"; step wait 500
snap

#!/usr/bin/env bash
# 第十一拍 ①②③：时间线 + 浮条色 + 地址栏激活态
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

echo "### open"
"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1

echo "### arm"
"$NODE" "$CLI" eval "$(cat "$EV/p107l_time.js")" 2>&1 | tail -1

echo "### wait"
"$NODE" "$CLI" wait 4200 >/dev/null 2>&1

echo "### TIMELINE"
"$NODE" "$CLI" eval "$(cat "$EV/p107l_tt.js")" 2>&1 | tail -1

echo "### open browse panel + browser module"
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 1200 >/dev/null 2>&1
"$NODE" "$CLI" click ".td-browse-add" >/dev/null 2>&1
"$NODE" "$CLI" wait 400 >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-open-mod='browser']" >/dev/null 2>&1
"$NODE" "$CLI" wait 700 >/dev/null 2>&1

echo "### UI"
"$NODE" "$CLI" eval "$(cat "$EV/p107l_ui.js")" 2>&1 | tail -1

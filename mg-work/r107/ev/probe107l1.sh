#!/usr/bin/env bash
# 第十一拍 ①③：数字动效时间线 + .td-selbar 现状色值
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

step() { echo "### $*"; }

step open
"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1

step arm
"$NODE" "$CLI" eval "$(cat "$EV/p107l_time.js")" 2>&1 | tail -1

step wait
"$NODE" "$CLI" wait 4200 >/dev/null 2>&1

step read
"$NODE" "$CLI" eval "$(cat "$EV/p107l_read.js")" 2>&1 | tail -1

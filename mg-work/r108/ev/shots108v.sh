#!/usr/bin/env bash
# r108 第十九拍 · ② 菜单打开态截图（用已验证的开法：先滑侧栏，再点 `+`）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
RAW="$ROOT/mg-work/r108/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108x.js")"
run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
step() { run "$@" >/dev/null; }

step open "$URL"
step set viewport 1440 900
step wait 3800
ev openSide
step wait 1300
ev base
ev openMod
step wait 900
ev readMod
step screenshot "$RAW/v-after-menu.png"
step screenshot ".td-browse" "$RAW/v-after-menu-side.png"

#!/usr/bin/env bash
# r108 第十九拍 · ② 菜单入场取证 v2（侧栏真滑进视口之后再点 `+`）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
RAW="$ROOT/mg-work/r108/raw"
TAG="${1:-before}"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/r108v2.js")"
run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
step() { run "$@" >/dev/null; }

step open "$URL"
step set viewport 1440 900
step wait 3800

echo "=== 侧栏滑进视口 ==="
ev openSide
step wait 1200
ev in

echo "=== ② 逐帧采样（侧栏已开）==="
ev arm2
step wait 1200
ev read2

echo "=== `[hidden]` 压不压得住 ==="
ev probeHidden

echo "=== 菜单打开后的静态版面 ==="
run screenshot ".td-mod-menu" "$RAW/v-$TAG-menu.png"
run screenshot "$RAW/v-$TAG-side.png"
echo "done"

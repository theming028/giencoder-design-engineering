#!/usr/bin/env bash
# r108 第十九拍 · ② 菜单闪烁/跳动/位移 真机逐帧取证
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
RAW="$ROOT/mg-work/r108/raw"
TAG="${1:-before}"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/r108v-recon.js")"
run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
step() { run "$@" >/dev/null; }

step open "$URL"
step set viewport 1440 900
step wait 3800

echo "=== recon：侧栏 / 可拖选文本 / 菜单现状 ==="
ev recon
step wait 800
ev in

echo "=== ② 逐帧采样（开）==="
ev arm
step wait 1400
ev read

echo "=== ② 逐帧采样（开→关）==="
step wait 500
ev armClose
step wait 1400
ev readClose

echo "=== ① 合成选区（只验守卫这一层）==="
ev synthSel
step wait 300
ev selRead

echo "done"

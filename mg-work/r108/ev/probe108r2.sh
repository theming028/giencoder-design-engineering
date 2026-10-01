#!/usr/bin/env bash
# r108 第十六拍 · 复测（针对两处返工）：
#   [A] ① 复用页签时**页签名/图标**是否跟着换（首轮 bug：页签写 .md、正文是 .xlsx）
#   [B] 五条模块工具条在 --ui-fs=14 / 18 两档下的高度对照表（定性 41/46 那一处差异）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
RAW="$ROOT/mg-work/r108/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108r.js")"

run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
raw() { run eval "$1"; }
step() { run "$@" >/dev/null; }
on()   { run eval "window.__MOD='$1'; $(cat "$EV/on.js")"; }

step open "$URL"
step set viewport 1440 900
step wait 3800

echo "### [A] ① 连点两个产物：页签名必须跟着换"
ev pvA
step wait 600
ev pvB
step wait 400
step screenshot ".td-browse-bar" "$RAW/r2-tabs-after-pvB.png"
step screenshot ".td-browse" "$RAW/r2-pv-xlsx.png"
ev pvC
step wait 300

echo "### [B] 工具条高度对照（--ui-fs = 14）"
ev pvA
step wait 600
for M in summary review terminal browser preview; do
  on "$M"
  step wait 420
  ev slot
done
step screenshot ".td-browse" "$RAW/r2-bars-fs14-terminal.png"

echo "### [B'] 工具条高度对照（--ui-fs = 18）"
raw "document.documentElement.style.setProperty('--ui-fs','18'); 'fs-on'"
step wait 600
for M in summary review terminal browser preview; do
  on "$M"
  step wait 420
  ev slot
done
step screenshot ".td-browse" "$RAW/r2-bars-fs18-terminal.png"
step screenshot ".td-browse" "$RAW/r2-bars-fs18-preview.png"
raw "document.documentElement.style.removeProperty('--ui-fs'); 'fs-off'"
step wait 400

echo "### done"

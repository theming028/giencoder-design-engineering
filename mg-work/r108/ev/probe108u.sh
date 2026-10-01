#!/usr/bin/env bash
# r108 第十八拍（第七层补丁）· 四条真机取证（改前 / 改后同一条链）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
RAW="$ROOT/mg-work/r108/raw"
TAG="${1:-before}"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108u.js")"
run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
step() { run "$@" >/dev/null; }

step open "$URL"
step set viewport 1440 900
step wait 3800

echo "=== base：② 标题栏动作 / ④ 菜单项顺序 ==="
ev base

echo "=== ④ 菜单打开（多开页签，让侧栏滑进视口）==="
ev menuOpen
step wait 700
ev menuRead

echo "=== ③ 审查模块：rv-body 与祖先链 ==="
ev menuClose
step wait 400
# 先用菜单入口开一次审查，保证「从 '更多' 路径」也走通
ev menuOpen
step wait 600
ev rvOpen
step wait 900
ev rvRead

echo "=== ③ 真实滚动路径：滚容器（看整页会不会被带走）==="
ev rvScroll
step wait 500
ev rvRead

echo "=== ① 产物预览工具条 ==="
ev pvOpen
step wait 900
ev pvRead

step screenshot "$RAW/u-$TAG-full.png"
step screenshot ".td-browse" "$RAW/u-$TAG-browse.png"
echo "done"

#!/usr/bin/env bash
# 第十八拍四条目视证据（★ 每次截图前都先把侧栏滑进视口）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"; RAW="$ROOT/mg-work/r108/raw"
TAG="${1:-after}"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108u.js")"
run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
step() { run "$@" >/dev/null; }

step open "$URL"; step set viewport 1440 900; step wait 3800
echo "--- 先把侧栏滑进视口"
ev openTabs; step wait 900
echo "--- ④ 菜单（摘要第一）"
ev menuOpen; step wait 800
ev menuRead
step screenshot "$RAW/u-$TAG-menu.png"
step screenshot ".td-browse" "$RAW/u-$TAG-menu-browse.png"
ev menuClose; step wait 500
echo "--- ② 标题栏（只剩收起）"
step screenshot ".td-browse-bar" "$RAW/u-$TAG-bar.png"
step screenshot ".td-browse" "$RAW/u-$TAG-bar-browse.png"
echo "--- ① 预览工具条（两枚按钮）"
ev pvOpen; step wait 900
ev pvRead
step screenshot "#av-browse-pane-preview .td-mod-bar" "$RAW/u-$TAG-pvbar.png"
step screenshot ".td-browse" "$RAW/u-$TAG-pvbrowse.png"
echo "--- ③ 审查模块（顶 / 底）"
ev openTabs; step wait 600
step screenshot ".td-mod.td-rv" "$RAW/u-$TAG-rv-top.png"
ev rvScroll; step wait 600
step screenshot ".td-mod.td-rv" "$RAW/u-$TAG-rv-scrolled.png"
echo done

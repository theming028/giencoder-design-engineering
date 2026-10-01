#!/usr/bin/env bash
# 补：菜单落位目视证据（走 probe108t.sh 里已验证会滑入侧栏的那条路径）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
RAW="$ROOT/mg-work/r108/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108t.js")"
run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
step() { run "$@" >/dev/null; }

step open "$URL"
step set viewport 1440 900
step wait 3800
echo "--- base"
ev base
echo "--- 第一次开菜单"
ev menuOpen
step wait 800
ev read
step screenshot ".td-browse" "$RAW/t-menu-1tab.png"
ev menuClose
step wait 400
echo "--- 多开页签（这一步会滑入侧栏）"
ev openTabs
step wait 700
echo "--- 再开菜单"
ev menuOpen
step wait 800
ev read
step screenshot "$RAW/t-menu-full.png"
step screenshot ".td-browse" "$RAW/t-menu-4tabs-browse.png"
echo "done"

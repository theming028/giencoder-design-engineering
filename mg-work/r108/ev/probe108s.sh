#!/usr/bin/env bash
# r108 第十七拍 · 现状取证（六条）。同一时刻只能有一个 UI 实测进程 ⇒ 整条链一次跑完。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
RAW="$ROOT/mg-work/r108/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108s.js")"

run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
raw() { run eval "$1"; }
step() { run "$@" >/dev/null; }
mkdir -p "$RAW"

step open "$URL"
step set viewport 1440 900
step wait 3800

echo "### [0] base —— 基线几何 / 浏览器工具条图标 / diff 行数"
ev base

echo "### [1a] 点 + 打开菜单（同一 eval 只点）"
ev menuOpen
step wait 500

echo "### [1b] 读菜单与触发器几何（分帧后再读）"
ev menu
step screenshot ".td-browse-bar" "$RAW/s-menu-before.png"

echo "### [1c] 关菜单"
ev menuClose
step wait 400

echo "### [2a] 多开两枚页签（terminal + browser）⇒ + 应右移"
ev addTabs
step wait 500

echo "### [2b] 再开菜单 + 读几何（看是否跟随）"
ev menuOpen
step wait 500
ev menu
step screenshot ".td-browse-bar" "$RAW/s-menu-after.png"

echo "### [2c] 关菜单"
ev menuClose
step wait 400

echo "### [3a] 切到审查模块"
ev rvOpen
step wait 600

echo "### [3b] 打开文件树抽屉"
ev treeOpen
step wait 600

echo "### [3c] 读 tree / scrim / panel / bar 几何"
ev tree
step screenshot ".td-browse" "$RAW/s-tree-open.png"

echo "### [3d] 关抽屉"
ev treeClose
step wait 500

echo "### [4a] 字号 18 档的标题栏高度"
ev fs18
step wait 300
echo "### [4b] 还原 14"
ev fs14

echo "### [5] 浏览器工具条截图（删按钮前的基线）"
raw "document.querySelectorAll('.td-browse-tabs [data-td-tab]').forEach(function(t){ if(t.getAttribute('data-td-mod')==='browser') t.click(); }); 'to-browser'"
step wait 500
step screenshot ".td-url" "$RAW/s-url-before.png"
step screenshot ".td-browse" "$RAW/s-brw-before.png"
echo "done"

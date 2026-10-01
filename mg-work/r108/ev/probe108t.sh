#!/usr/bin/env bash
# r108 第十七拍 · 四条真机取证。整条链一次跑完（同一时刻只能有一个 UI 实测进程）。
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
raw() { run eval "$1"; }
step() { run "$@" >/dev/null; }
mkdir -p "$RAW"

step open "$URL"
step set viewport 1440 900
step wait 3800

echo "### [0] base —— 工具条图标 / diff 行数"
ev base

echo "### [1a] ① 场景 A：只有 1 枚页签时点 +（同时会把侧栏滑入）"
ev menuOpen
step wait 800

echo "### [1b] ① 量几何（dx 应 ≈ 0、dy = 6）"
ev read
step screenshot ".td-browse-bar" "$RAW/t-menu-1tab.png"

echo "### [1c] 关菜单"
ev menuClose
step wait 400

echo "### [2a] ① 场景 B：多开到 4 枚页签（+ 右移）"
ev openTabs
step wait 600

echo "### [2b] ① 再开菜单 + 量几何（关键：dx 应仍 ≈ 0）"
ev menuOpen
step wait 600
ev read
step screenshot ".td-browse-bar" "$RAW/t-menu-4tabs.png"

echo "### [2c] 关菜单"
ev menuClose
step wait 400

echo "### [3a] ① 场景 C：--ui-fs = 18（+ 位置再变一次）"
ev fs18
step wait 400
ev menuOpen
step wait 600
ev read
step screenshot ".td-browse-bar" "$RAW/t-menu-fs18.png"
ev menuClose
step wait 300
ev fs14
step wait 400

echo "### [4a] ③ 切到审查模块"
ev rvOpen
step wait 700

echo "### [4b] ④ 审查模块 diff 行数 / 可滚动高度"
ev rvRows
step screenshot ".td-browse" "$RAW/t-rv-rows.png"

echo "### [5a] ③ 打开文件树抽屉"
ev treeOpen
step wait 700

echo "### [5b] ③ 量 tree / bar / scrim（treeTopVsBarBottom 应为 0）"
ev treeRead
step screenshot ".td-browse" "$RAW/t-tree-open.png"
step screenshot ".td-browse-bar" "$RAW/t-tree-bar.png"

echo "### [5c] 关抽屉"
ev treeClose
step wait 600

echo "### [6] ② 浏览器模块：工具条只剩「更多」"
raw "document.querySelectorAll('.td-browse-tabs [data-td-tab]').forEach(function(t){ if(t.getAttribute('data-td-mod')==='browser') t.click(); }); 'to-browser'"
step wait 600
step screenshot ".td-url" "$RAW/t-url-after.png"
step screenshot ".td-browse" "$RAW/t-brw-after.png"
echo "done"

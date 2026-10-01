#!/usr/bin/env bash
# r108 第十九拍 · 旧坑回归重测（改了 toggleMenu 的时序 ⇒ 依赖它的路径全量重跑）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
RAW="$ROOT/mg-work/r108/raw"
TAG="${1:-after}"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108x.js")"
run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
step() { run "$@" >/dev/null; }

step open "$URL"
step set viewport 1440 900
step wait 3800

echo "### 侧栏滑进视口（审查模块）"
ev openSide
step wait 1200
ev base

echo "### ① 四枚下拉逐个开（每枚：点开 → 等过渡跑完 → 读）"
ev openMod   ; step wait 700 ; ev readMod
ev closeAll  ; step wait 400
ev openOpts  ; step wait 700 ; ev readOpts
ev closeAll  ; step wait 400
ev openScope ; step wait 700 ; ev readScope
ev closeAll  ; step wait 400
ev openCommit; step wait 700 ; ev readCommit
ev closeAll  ; step wait 400

echo "### ①b 四枚下拉「点开即读」——同一 eval 内拿 getAnimations（硬规则 25 ②）"
ev peekMod
step wait 600
ev closeAll ; step wait 300
ev peekOpts
step wait 600
ev closeAll ; step wait 300
ev peekScope
step wait 600
ev closeAll ; step wait 300
ev peekCommit
step wait 600
ev closeAll ; step wait 400

echo "### ② Esc 分层：只开「显示选项」时按 Esc"
ev openOptsOnly
step wait 600
ev escState
step press Escape
step wait 500
ev escState
run screenshot "$RAW/x-$TAG-after-esc.png"

echo "### ④ 右键菜单（审查 diff 代码行 —— 必须排在切模块之前）"
ev ctxOpen
step wait 600
ev ctxRead
run screenshot "$RAW/x-$TAG-ctx.png"
step press Escape
step wait 400

echo "### ③ `+` 菜单选「终端」⇒ 切模块 + 菜单自动收"
ev openMod
step wait 600
ev pickTerm
step wait 800
ev paneState

echo "### ⑤ 收起侧栏"
ev closeSidebar
step wait 900
ev sidebarState

echo "### ⑥ 重新滑入 + 切页签"
ev switchTab
step wait 900
ev base
echo "done"

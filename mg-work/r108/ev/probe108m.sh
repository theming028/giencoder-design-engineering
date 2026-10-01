#!/usr/bin/env bash
# 第十二拍真机取证：① diff 卡片化 · ② 文件树抽屉。
# ⚠ 同一时刻只有一个 UI 实测进程 ⇒ 整条链路必须在**一次调用**里跑完。
# ⚠ 「点击」与「读值」一律分帧（中间 `wait`）：避免量到过渡起点（第十一拍踩过）。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108m.js")"

run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS" | tail -1; }

echo "### open"
run open "$URL" >/dev/null
run set viewport 1440 900 >/dev/null

echo "### wait skeleton"
run wait 3800 >/dev/null

echo "### open right panel"
run click ".r93-baract[data-r93-browse]" >/dev/null
run wait 900 >/dev/null

echo "=== [0] 切到「审查」模块 ==="
run click ".td-browse-add" >/dev/null
run wait 400 >/dev/null
run click "[data-td-open-mod='review']" >/dev/null
run wait 700 >/dev/null

echo "=== [1] ① DIFF 卡片化 ==="
ev diff

echo "=== [2] ② 抽屉：打开前 / 点击 / 打开后（分帧） ==="
ev tree0
run wait 400 >/dev/null
ev tree1

echo "--- 折叠 games（点 → 等 → 读） ---"
ev fold
run wait 250 >/dev/null
ev tree2

echo "--- 再展开 games ---"
ev unfold
run wait 250 >/dev/null
ev tree2b

echo "--- 选中「文件」模块里的一个文件（验抽屉树自己的选中态） ---"
ev pick
run wait 250 >/dev/null
ev tree2c

echo "--- 回归：点过抽屉树后，「文件」模块那棵树有没有被带坏 ---"
ev regress

echo "--- 点遮罩关闭（点 → 等 → 读） ---"
ev mask
run wait 400 >/dev/null
ev tree3

echo "--- 重新打开 + Esc 裁决（抽屉关掉、侧栏不许关） ---"
ev reopen
run wait 400 >/dev/null
ev tree4
run press Escape >/dev/null
run wait 400 >/dev/null
ev tree5

echo "### done"

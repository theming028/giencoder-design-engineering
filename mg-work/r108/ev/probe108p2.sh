#!/usr/bin/env bash
# 第十四拍·边界与回归探针（与 probe108p.sh 主链互补）。
#   [A] 面板不遮挡 `.r93-bar` 的两枚按钮（elementFromPoint 命中自身）
#   [B] 暗色档：面板 / 胶囊 / 两枚 `.zd-menu` / `.zd-toast` 全部 token 派生 + §19.x 无硬编码 hex
#   [C] `--ui-fs = 18` 杠杆：分区头 32→41.14、**圆序号恒为正圆**、卡片不被压平
#   [D] 窄档 620：卡片不越右界
#   [E] 右栏四枚 `.td-rv-menu` 回归（第 1 节选择器组扩员后一字未变）
# ⚠ 同一时刻只有一个 UI 实测进程 ⇒ 整条链路在一次调用里跑完。
# ⚠ 点击 / hover 与读值分帧（硬规则 29）；hover 读数必须**另起一次 eval**。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108p2.js")"

run() { "$NODE" "$CLI" "$@" 2>&1; }
# ⚠ 不要 `tail -1`：eval 抛错时输出是「Error 行 + 栈行」两行，裁掉首行就只剩
#   一句无信息量的 `at <anonymous>:215:3`（本轮真踩过 —— 探针自身的 TypeError 极难定位）。
ev()  { run eval "window.__M='$1'; $JS"; }
raw() { run eval "$1"; }

echo "### open"
run open "$URL" >/dev/null
run set viewport 1440 900 >/dev/null
echo "### wait skeleton"
run wait 3800 >/dev/null

echo "=== [A] 顶栏两枚按钮不被面板遮挡 ==="
ev bar

echo "=== [B] 暗色档（token 派生 + hex 扫描） ==="
ev dark
raw "document.documentElement.removeAttribute('giencoder-theme'); 'dark-off'"

echo "=== [C] --ui-fs = 18 杠杆 ==="
ev fs
raw "document.documentElement.style.removeProperty('--ui-fs'); 'fs-off'"

echo "=== [D] 窄档 620 ==="
run set viewport 620 900 >/dev/null
run wait 600 >/dev/null
ev narrow
run set viewport 1440 900 >/dev/null
run wait 600 >/dev/null

echo "=== [E0] 打开右栏 + 审查模块（走 ① 的「更改」行） ==="
run click "[data-zd-git='review']" >/dev/null
run wait 1200 >/dev/null
ev rv0

echo "=== [E1] 右栏「对比范围」（.td-rv-scope-menu） ==="
run click "[data-td-rv-scope]" >/dev/null
run wait 600 >/dev/null
ev rvs

echo "=== [E1h] 真鼠标 hover 条目 → 另起一次 eval 读底色 ==="
run hover ".td-rv-scope-menu [data-td-rv-range='branch']" >/dev/null
run wait 400 >/dev/null
ev rvsh
run press Escape >/dev/null
run wait 400 >/dev/null

echo "=== [E2] 右栏「提交与推送」（.td-commit-menu） ==="
run click "[data-td-commit]" >/dev/null
run wait 600 >/dev/null
ev rvc
run press Escape >/dev/null
run wait 400 >/dev/null

echo "=== [E3] 右栏「显示选项」（.td-rv-opts） ==="
run click "[data-td-rv-opts]" >/dev/null
run wait 600 >/dev/null
ev rvo

echo "=== [E4] 互斥：同一时刻只应有一枚右栏下拉打开 ==="
ev rvall
run press Escape >/dev/null
run wait 400 >/dev/null

echo "=== [F] 收尾复核：zd-menu 骨架 / 右栏 td-rv-menu 骨架 ==="
ev final

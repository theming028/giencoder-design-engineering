#!/usr/bin/env bash
# 第十四拍真机取证（主链）：① Git 三行可点（审查 / 分支菜单 / 提交菜单）· ② 计划分区已删
#                          · ③ 目标分区图标与间距 · ④ 折展 + 面板⇄胶囊的弹性动效。
# ⚠ 同一时刻只有一个 UI 实测进程 ⇒ 整条链路必须在**一次调用**里跑完。
# ⚠ 「点击 / hover」与「读值」一律**分帧**（中间 `wait`）：同一次 eval 里点完就读，拿到的是
#   **过渡起始值**（硬规则 29）。本轮的弹性采样是**故意**要中间值 ⇒ 那几段自己装 rAF 采样器。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108p.js")"

run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS" | tail -1; }

echo "### open"
run open "$URL" >/dev/null
run set viewport 1440 900 >/dev/null
echo "### wait skeleton"
run wait 3800 >/dev/null

echo "=== [A] 静态结构（面板 / 三分区 / 目标几何 / 菜单 DOM） ==="
ev static

echo "=== [B] ① 分支菜单：点开（真鼠标，分帧读） ==="
run click "[data-zd-git='branch']" >/dev/null
run wait 600 >/dev/null
ev br1

echo "=== [B2] ① 分支菜单：选第 2 条 ==="
run click "[data-zd-br='feature/right-panel']" >/dev/null
run wait 500 >/dev/null
ev br2

echo "=== [C] ① 提交菜单：点开 ==="
run click "[data-zd-git='commit']" >/dev/null
run wait 600 >/dev/null
ev cm1

echo "=== [C2] ① 提交菜单：点「提交并推送」 ==="
run click "[data-zd-commit='push']" >/dev/null
run wait 400 >/dev/null
ev cm2

echo "=== [C3] Esc 关层：菜单开→按 Esc（不得顺带关侧栏 / 关面板） ==="
run click "[data-zd-git='commit']" >/dev/null
run wait 500 >/dev/null
run press Escape >/dev/null
run wait 500 >/dev/null
ev cm3

echo "=== [D] ④ 折展：先折叠「Git 工具」 ==="
run click "[data-zd-sec='git'] .zd-sec-t" >/dev/null
run wait 600 >/dev/null
ev foldRead

echo "=== [D2] ④ 折展：再展开（装 rAF 采样器，采 520ms） ==="
ev foldStart
run wait 800 >/dev/null
ev foldRead

echo "=== [E] ④ 面板⇄胶囊：收起（采样 320ms 出场过渡） ==="
ev miniOutStart
run wait 600 >/dev/null
ev miniOutRead

echo "=== [E2] ④ 面板⇄胶囊：摊回（采样 620ms 入场动画） ==="
ev miniInStart
run wait 1000 >/dev/null
ev miniInRead

echo "=== [F] ① 更改 → 打开右栏并切到「审查」（放在最后：它会改布局） ==="
ev rev0
run click "[data-zd-git='review']" >/dev/null
run wait 1200 >/dev/null
ev rev1

echo "=== [G] 复核：面板仍在 main 内 ==="
ev static

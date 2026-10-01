#!/usr/bin/env bash
# 第十三拍真机取证：① hover 边框 · ② 标题图标删除 · ③ diff 图标尺寸/色 · ④ 产物卡整卡可点 · ⑥ 右上角任务信息面板。
# ⚠ 同一时刻只有一个 UI 实测进程 ⇒ 整条链路必须在**一次调用**里跑完。
# ⚠ 「点击 / hover」与「读值」一律分帧（中间 `wait`）：避免量到过渡起点。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108n.js")"

run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS" | tail -1; }

echo "### open"
run open "$URL" >/dev/null
run set viewport 1440 900 >/dev/null

echo "### wait skeleton"
run wait 3800 >/dev/null

echo "### 先打开右栏（否则摘要模块整块落在视口外 ⇒ hover/点击都点不到）"
run click ".r93-baract[data-r93-browse]" >/dev/null
run wait 1000 >/dev/null

echo "=== [A] ①②③ 静态（无交互） ==="
ev fix

echo "=== [B] ① 摘要卡 hover：真鼠标移入（分帧） ==="
ev hover0
run hover ".td-sum-sec" >/dev/null
run wait 450 >/dev/null
ev hover1

echo "=== [C] ④ 产物卡整体可点：点「图标区」而非「预览」按钮 ==="
ev art
run click ".td-sum-art .td-sum-arti" >/dev/null
run wait 600 >/dev/null
ev art
run click "[data-td-prev-x]" >/dev/null
run wait 400 >/dev/null

echo "=== [D] ⑥ 面板：位置 / 分区 / 计数 ==="
ev zd0

echo "=== [E] ⑥ 折叠「Git 工具」分区 ==="
run click "[data-zd-sec='git'] .zd-sec-t" >/dev/null
run wait 350 >/dev/null
ev zd1

echo "=== [F] ⑥ 收起为胶囊 ==="
run click "[data-zd-min]" >/dev/null
run wait 350 >/dev/null
ev zd2

echo "=== [G] ⑥ 点胶囊摊回面板 ==="
run click "[data-zd-mini]" >/dev/null
run wait 350 >/dev/null
ev zd2

echo "=== [H] 复核：面板仍在 main 内、卡片已回 ==="
ev zd0

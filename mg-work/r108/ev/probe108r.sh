#!/usr/bin/env bash
# r108 第十六拍（第五层补丁）· 三条真机探针。
#   [0] base      —— ③ 毛玻璃 computed（四件套 + color-mix 支持性）+ ② 锚点 + ① 旧浮层归零
#   [1] pvA/pvB   —— ① 点两个产物：预览页签名 / 图标 / 骨架切换 / 页签复用（不新增第二枚）
#   [2] pvC       —— ① 页签 × 关闭：页签消失 + 面板回到 hidden
#   [3] pvD/pvE   —— ① 与「摘要」页签互相切换（activate 裁决）
#   [4] glassOn/Off —— ③ 在卡片正下方临时塞纯红块：卡片像素应被染（证明半透明 + 模糊）
#   [5] swapOut/In —— ② 「点 + 采样」同一次 eval：收进/摊开的 scale / translate / 锚点 / 关键帧
#   [6] dark / fs  —— 边界档回归（放最后：都会改全局状态）
# ⚠ 同一时刻只能有一个 UI 实测进程 ⇒ 整条链在一次调用里跑完。
# ⚠ 点击 / 采样与读值分帧（硬规则 29）；⚠ `ev()` **不要** `tail -1`（抛错时首行才有用）。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
RAW="$ROOT/mg-work/r108/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108r.js")"

run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
raw() { run eval "$1"; }
step() { run "$@" >/dev/null; }
mkdir -p "$RAW"

step open "$URL"
step set viewport 1440 900
step wait 3800

echo "### [0] base"
ev base

echo "### [1a] ① 点第 1 个产物（Markdown）"
ev pvA
step wait 600
ev slot
step screenshot ".td-browse" "$RAW/r-1440-pv-md.png"
step screenshot ".td-browse-bar" "$RAW/r-1440-pv-tabs1.png"

echo "### [1b] ① 点第 2 个产物（xlsx）——页签应**复用**、骨架应切到表格"
ev pvB
step screenshot ".td-browse" "$RAW/r-1440-pv-xlsx.png"

echo "### [2] ① 页签 × 关闭"
ev pvC

echo "### [3a] ① 再开一次 → 切回「摘要」页签"
ev pvD
step screenshot ".td-browse-bar" "$RAW/r-1440-tabs-summary.png"

echo "### [3b] ① 切回「预览」页签"
ev pvE
step screenshot ".td-browse" "$RAW/r-1440-pv-back.png"

echo "### [4] ③ 毛玻璃像素取证：卡片下方临时铺纯红"
raw "document.querySelectorAll('.td-browse-tabs [data-td-tab]').forEach(function(t){ if(t.getAttribute('data-td-mod')==='summary') t.click(); }); 'back-to-summary'"
step wait 300
ev glassOn
step screenshot ".zd-card" "$RAW/r-card-over-red.png"
ev glassOff
step screenshot ".zd-card" "$RAW/r-card-over-page.png"

echo "### [5a] ② 收起为胶囊（点 + 采样同一次 eval）"
ev swapOut
step wait 900
ev swapEnd

echo "### [5b] ② 从胶囊摊开"
ev swapIn
step wait 900
ev swapEnd

echo "### [6a] 暗色档"
raw "document.documentElement.setAttribute('giencoder-theme','dark'); 'dark-on'"
step wait 500
ev dark
step screenshot ".zd-card" "$RAW/r-1440-dark.png"
raw "document.documentElement.removeAttribute('giencoder-theme'); 'dark-off'"
step wait 400

echo "### [6b] --ui-fs = 18（两条工具条各测一次：同时可见不了，只能逐次激活）"
raw "document.querySelectorAll('.td-browse-tabs [data-td-tab]').forEach(function(t){ if(t.getAttribute('data-td-mod')==='preview') t.click(); }); 'preview-on'"
step wait 400
raw "document.documentElement.style.setProperty('--ui-fs','18'); 'fs-on'"
step wait 600
ev fs
step screenshot ".td-browse" "$RAW/r-1440-fs18-pv.png"
raw "document.querySelectorAll('.td-browse-tabs [data-td-tab]').forEach(function(t){ if(t.getAttribute('data-td-mod')==='summary') t.click(); }); 'summary-on'"
step wait 500
ev slot
raw "document.documentElement.style.removeProperty('--ui-fs'); 'fs-off'"
raw "document.querySelectorAll('.td-browse-tabs [data-td-tab]').forEach(function(t){ if(t.getAttribute('data-td-mod')==='preview') t.click(); }); 'preview-back'"
step wait 600
ev slot

echo "### done"

#!/usr/bin/env bash
# r108 第十五拍（第四层补丁）· 六条真机探针。
#   [0] base  —— ① `.zd-sec-t` 字阶/字重/色 + ③ 目标只剩 1 行 + ④ 进程三态 + ⑥ 默认 trailing 应 display:none
#   [1] sp0/sp1 —— ④ 进行中那段弧**在转**（两次采样角度不同）
#   [2] ico0/ico1 —— ② 真鼠标 hover 前后 `.zd-ico` 的 bg/color（★ 必须另起一次 eval 读）
#   [3] collapse/expand —— ⑥ 折叠态 trailing 应 display:flex，展开态 display:none
#   [4] skgate —— ⑤ `:has()` 支持性 + 造/删假 `.r93-sk` 时 `.zd-host` 的 display
#   [5] dark / fs / narrow —— 三档回归（放最后，都会改全局状态）
# ⚠ 同一时刻只能有一个 UI 实测进程 ⇒ 整条链在一次调用里跑完。
# ⚠ 点击 / hover 与读值分帧（硬规则 29）；⚠ `ev()` **不要** `tail -1`（抛错时首行才有用）。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
RAW="$ROOT/mg-work/r108/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108q.js")"

run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
raw() { run eval "$1"; }
step() { run "$@" >/dev/null; }
mkdir -p "$RAW"

step open "$URL"
step set viewport 1440 900
step wait 3800

echo "### [0] base（①③④⑥ 静态读数）"
ev base

echo "### [1] ④ 进行中那段弧在转吗（两次采样）"
ev sp0
step wait 320
ev sp1

echo "### [2] ② .zd-ico hover 前"
ev ico0
step hover "[title='收起为胶囊']"
step wait 400
ev ico1
step hover ".zd-name"        # 把鼠标移开（本仓 CLI 没有 move；hover 一个中性兄弟元素即可）
step wait 300

echo "### [3] ⑥ 折叠「目标」分区（trailing 应出现）"
step click "[data-zd-sec='goal'] .zd-sec-t"
step wait 600
ev collapse
step screenshot "$RAW/q-1440-collapsed.png"
step click "[data-zd-sec='goal'] .zd-sec-t"
step wait 600
ev expand

echo "### [4] ⑤ 骨架屏门控"
ev skgate

echo "### [6] 目视取证"
step screenshot "$RAW/q-1440-zd.png"
step screenshot ".zd-card" "$RAW/q-1440-rows.png"
step screenshot "[data-zd-sec='goal']" "$RAW/q-1440-goal.png"
step screenshot "[data-zd-sec='todo']" "$RAW/q-1440-todo.png"

echo "### [5a] 暗色档"
raw "document.documentElement.setAttribute('giencoder-theme','dark'); 'dark-on'"
step wait 500
ev dark
step screenshot "[data-zd-sec='todo']" "$RAW/q-1440-todo-dark.png"
raw "document.documentElement.removeAttribute('giencoder-theme'); 'dark-off'"
step wait 400

echo "### [5b] --ui-fs = 18"
raw "document.documentElement.style.setProperty('--ui-fs','18'); 'fs-on'"
step wait 500
ev fs
step screenshot ".zd-card" "$RAW/q-1440-fs18.png"
raw "document.documentElement.style.removeProperty('--ui-fs'); 'fs-off'"
step wait 400

echo "### [5c] 窄档 620"
step set viewport 620 900
step wait 600
ev narrow
step set viewport 1440 900
step wait 600

echo "### done"

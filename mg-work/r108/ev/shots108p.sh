#!/usr/bin/env bash
# 第十四拍目视取证（1440×900，另加暗色 / --ui-fs=18 两档）：
#   ① Git 三行交互（分支菜单 / 提交菜单 / 轻提示 / 更改→右栏审查）
#   ② 「计划」分区已删（`p-1440-zd-rows.png` 里只剩 Git 工具 / 目标 / 进程）
#   ③ 「目标」图标与间距（lucide goal / pause / minimize-2 + 8px 内距 + 16px 行高）
#   ④ 折展弹性 + 面板⇄胶囊弹性
#   [A] 面板不遮挡 `.r93-bar` 两枚按钮（`p-1440-bar.png`）
# ⚠ 同一时刻只能有一个 UI 实测进程 ⇒ 整条链在一次调用里跑完。
# ⚠ hover / 点击 与 截图一律分帧（中间 wait），否则拍到过渡起点（硬规则 29）。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
RAW="$ROOT/mg-work/r108/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

step() { "$NODE" "$CLI" "$@" >/dev/null 2>&1; }
mkdir -p "$RAW"

step open "$URL"
step set viewport 1440 900
step wait 3800

echo "### [0][A] 右上角面板（右栏关闭）+ 顶栏两枚按钮"
step screenshot "$RAW/p-1440-zd.png"          # 整屏：面板 + 顶栏两枚按钮同框
step screenshot ".r93-bar" "$RAW/p-1440-bar.png"
step screenshot ".zd-card" "$RAW/p-1440-zd-rows.png"

echo "### [3] 「目标」分区：图标 / 间距 / · 分隔符 / 暂停钮"
step screenshot "[data-zd-sec='goal']" "$RAW/p-1440-goal.png"
step screenshot ".zd-head" "$RAW/p-1440-zd-head.png"

echo "### [4a] 折叠「Git 工具」分区（grid-template-rows 收拢后的静止态）"
step click "[data-zd-sec='git'] .zd-sec-t"
step wait 600
step screenshot ".zd-card" "$RAW/p-1440-zd-fold.png"
step click "[data-zd-sec='git'] .zd-sec-t"
step wait 600

echo "### [1a] 分支菜单展开"
step click "[data-zd-git='branch']"
step wait 600
step screenshot "main" "$RAW/p-1440-br-menu.png"

echo "### [1b] 选「feature/right-panel」→ 行值更新 + 轻提示"
step click "[data-zd-br='feature/right-panel']"
step wait 350
step screenshot "main" "$RAW/p-1440-br-picked.png"
step wait 1400

echo "### [1c] 提交菜单展开"
step click "[data-zd-git='commit']"
step wait 600
step screenshot "main" "$RAW/p-1440-cm-menu.png"

echo "### [1d] 点「提交并推送」→ 轻提示"
step click "[data-zd-commit='push']"
step wait 350
step screenshot "main" "$RAW/p-1440-toast.png"
step wait 1400

echo "### [4b] 收起为胶囊"
step click "[data-zd-min]"
step wait 500
step screenshot "$RAW/p-1440-mini.png"        # 整屏：胶囊落在 main 右上角

echo "### [4c] 点胶囊摊回"
step click "[data-zd-mini]"
step wait 700
step screenshot "$RAW/p-1440-return.png"      # 整屏：摊回

echo "### 边界档：暗色"
step eval "document.documentElement.setAttribute('giencoder-theme','dark'); 'ok'"
step wait 600
step screenshot ".zd-card" "$RAW/p-1440-dark.png"
step eval "document.documentElement.removeAttribute('giencoder-theme'); 'ok'"
step wait 300

echo "### 边界档：--ui-fs = 18（字号杠杆；圆序号恒为正圆）"
step eval "document.documentElement.style.setProperty('--ui-fs','18'); 'ok'"
step wait 600
step screenshot ".zd-card" "$RAW/p-1440-fs18.png"
step eval "document.documentElement.style.removeProperty('--ui-fs'); 'ok'"
step wait 300

echo "### 边界档：窄档 620"
step set viewport 620 900
step wait 600
step screenshot "main" "$RAW/p-1440-narrow.png"
step set viewport 1440 900
step wait 600

echo "### [1e] 「更改」→ 打开右栏并切「审查」（放最后：它会改布局）"
step click "[data-zd-git='review']"
step wait 1400
step screenshot "$RAW/p-1440-review.png"      # 整屏：面板让位 + 右栏审查同框

echo done

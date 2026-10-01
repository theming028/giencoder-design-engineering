#!/usr/bin/env bash
# 第十三拍目视取证（1440×900）：
#   ① td-sum-sec hover 边框加深 · ② td-sum-h 标题图标移除 · ③ td-diff-toggle 图标正文色 13px
#   ④ td-sum-art 整卡可点预览 · ⑥ 右上角任务信息面板（展开 / 折叠 / 胶囊 / 暗色）
# ⚠ 同一时刻只能有一个 UI 实测进程 ⇒ 整条链必须在一次调用里跑完。
# ⚠ hover / 点击 与 截图 一律分帧（中间 wait），否则会拍到过渡起点。
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

echo "### [0] 右上角面板（右栏关闭态，检验不遮挡工具条）"
step screenshot "main" "$RAW/n-1440-zd.png"
step screenshot ".zd-card" "$RAW/n-1440-zd-card.png"
step screenshot ".r93-bar" "$RAW/n-1440-bar.png"

echo "### [6a] 折叠「Git 工具」分区"
step click "[data-zd-sec='git'] .zd-sec-t"
step wait 400
step screenshot ".zd-card" "$RAW/n-1440-zd-fold.png"

echo "### [6b] 点击分区头摊回"
step click "[data-zd-sec='git'] .zd-sec-t"
step wait 400

echo "### [6c] 收起为胶囊"
step click "[data-zd-min]"
step wait 450
step screenshot "main" "$RAW/n-1440-zd-mini.png"

echo "### [6d] 点胶囊摊回"
step click "[data-zd-mini]"
step wait 450

echo "### [6e] 暗色档"
step eval "document.documentElement.setAttribute('giencoder-theme','dark'); 'ok'"
step wait 600
step screenshot ".zd-card" "$RAW/n-1440-zd-dark.png"
step eval "document.documentElement.removeAttribute('giencoder-theme'); 'ok'"
step wait 300

echo "### 打开右栏（否则摘要模块整块落在视口外 ⇒ hover/点击都点不到）"
step click ".r93-baract[data-r93-browse]"
step wait 1200

echo "### [1][2][4] 摘要模块静态：标题无图标 / 产物卡可点"
step screenshot ".td-browse" "$RAW/n-1440-sum.png"

echo "### [1] 摘要卡 hover（真鼠标移入 → 分帧 → 截图）"
step hover ".td-sum-sec"
step wait 500
step screenshot ".td-sum-sec" "$RAW/n-1440-sum-hover.png"

echo "### [4] 点产物卡「图标区」→ 预览层"
step click ".td-sum-art .td-sum-arti"
step wait 700
step screenshot "main" "$RAW/n-1440-art-preview.png"
step click "[data-td-prev-x]"
step wait 400

echo "### [3] 切「审查」模块：diff 折叠图标正文色 / 13px"
step click ".td-browse-add"
step wait 400
step click "[data-td-open-mod='review']"
step wait 800
step screenshot ".td-mod.td-rv .td-mod-bar" "$RAW/n-1440-revbar.png"
step screenshot ".td-diff-toggle" "$RAW/n-1440-diff-toggle.png"

echo done

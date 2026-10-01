#!/usr/bin/env bash
# 第十二拍目视取证：① diff 卡片化 · ② 文件树抽屉（打开 / 折叠），1440
# ⚠ 同一时刻只能有一个 UI 实测进程 ⇒ 整条链在一次调用里跑完
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
step wait 2800
step click ".r93-baract[data-r93-browse]"
step wait 1400

# ---- 审查模块（diff 卡片化） ----
step click ".td-browse-add"; step wait 400
step click "[data-td-open-mod='review']"; step wait 700
step screenshot ".td-mod.td-rv" "$RAW/m-1440-diff.png"
step screenshot ".td-browse" "$RAW/m-1440-diff-pane.png"

# ---- 文件树抽屉 ----
step click "[data-td-rv-act='tree']"; step wait 500
step screenshot ".td-browse" "$RAW/m-1440-tree.png"
step screenshot ".td-tree-panel" "$RAW/m-1440-tree-panel.png"

# ---- 抽屉里折叠 games ----
step eval "(function(){var r=[].slice.call(document.querySelectorAll('.td-tf'));for(var i=0;i<r.length;i++){var e=r[i].querySelector('.td-tf-name');if(e&&e.textContent==='games'){r[i].click();return 1;}}return 0;})()"
step wait 400
step screenshot ".td-tree-panel" "$RAW/m-1440-tree-fold.png"

# ---- 关抽屉，看「文件树」按钮在工具条里的位置（在「在文件树中定位」右侧） ----
step eval "document.querySelector('[data-td-tree-x]').click()"
step wait 500
step screenshot ".td-mod.td-rv .td-mod-bar" "$RAW/m-1440-rvbar.png"
echo done

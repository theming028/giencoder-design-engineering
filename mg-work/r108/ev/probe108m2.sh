#!/usr/bin/env bash
# 第十二拍补测：点抽屉里的**文件行** → 选中态切换（上一条探针误点了不在白名单里的 index.html）。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108m.js")"

run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS" | tail -1; }

run open "$URL" >/dev/null
run set viewport 1440 900 >/dev/null
run wait 3800 >/dev/null
run click ".r93-baract[data-r93-browse]" >/dev/null
run wait 900 >/dev/null
run click ".td-browse-add" >/dev/null
run wait 400 >/dev/null
run click "[data-td-open-mod='review']" >/dev/null
run wait 700 >/dev/null

echo "### 打开抽屉"
ev tree0 >/dev/null
run wait 400 >/dev/null
ev tree1

echo "### 点抽屉里的 「Controls.tsx」"
run eval "window.__M='pick2'; (function(){var rows=[].slice.call(document.querySelectorAll('.td-tf'));for(var i=0;i<rows.length;i++){var e=rows[i].querySelector('.td-tf-name');if(e&&e.textContent==='Controls.tsx'){rows[i].click();return JSON.stringify({clicked:true});}}return JSON.stringify({clicked:false});})()" | tail -1
run wait 250 >/dev/null
ev tree2c

echo "### 回归：文件模块那棵树 & 抽屉树的选中态各自独立"
ev regress

echo "### done"

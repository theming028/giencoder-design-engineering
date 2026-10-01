#!/usr/bin/env bash
# 第十一拍 ④ 目视取证：产物预览层（md / xlsx）+ 终端多标签 + 地址栏截图按钮，1440
# ⚠ 同一时刻只能有一个 UI 实测进程 ⇒ 整条链在一次调用里跑完
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
RAW="$ROOT/mg-work/r107/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

step() { "$NODE" "$CLI" "$@" >/dev/null 2>&1; }

step open "$URL"
step set viewport 1440 900
step wait 2600
step click ".r93-baract[data-r93-browse]"
step wait 1400

# ---- 摘要默认页签 ⇒ 直接点「产物 · 预览」第一枚（Markdown） ----
step screenshot ".td-browse" "$RAW/m-1440-sum.png"
step click "[data-td-art]"
step wait 500
step screenshot ".td-browse" "$RAW/m-1440-prev-md.png"
step click "[data-td-prev-close]"
step wait 300

# ---- 第二枚（xlsx 表格骨架） ----
step eval "document.querySelectorAll('[data-td-art]')[1].click()"
step wait 500
step screenshot ".td-browse" "$RAW/m-1440-prev-xlsx.png"
step click "[data-td-prev-close]"
step wait 300

# ---- 终端多标签 ----
step click ".td-browse-add"; step wait 400
step click "[data-td-open-mod='terminal']"; step wait 700
step screenshot ".td-mod-term" "$RAW/m-1440-term-t1.png"
step click "[data-td-term-tab='t2']"; step wait 400
step screenshot ".td-mod-term" "$RAW/m-1440-term-t2.png"
step click "[data-td-term-add]"; step wait 400
step screenshot ".td-mod-term" "$RAW/m-1440-term-new.png"

# ---- 浏览器：地址栏多了相机按钮 ----
step click ".td-browse-add"; step wait 400
step click "[data-td-open-mod='browser']"; step wait 700
step screenshot ".td-url" "$RAW/m-1440-url.png"
step screenshot ".td-browse" "$RAW/m-1440-brw.png"
echo done

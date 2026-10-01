#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
AB() { "$NODE" "$CLI" "$@"; }

AB open "file:///$ROOT/pages/conversation.html?v=$(date +%s)" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2600 >/dev/null 2>&1
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1

# 切到审查模块（先开 + 菜单，点「审查」）
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
AB wait 600 >/dev/null 2>&1

# ① 打开「显示选项」菜单（默认态）
AB click '[data-td-rv-opts]' >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1
AB screenshot "$OUT/e1-opts.png" >/dev/null 2>&1

# ② hover 第 4 项（「刷新 diff」，非选中项）
AB hover '.td-rv-opts .td-mm-item:nth-of-type(3)' >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB screenshot "$OUT/e2-opts-hover.png" >/dev/null 2>&1

# ③ 读 hover 后该条的底色 + 状态
AB eval "(function(){var m=document.querySelector('.td-rv-opts');var its=m.querySelectorAll('.td-mm-item');var o=[];for(var i=0;i<its.length;i++){o.push([i,its[i].textContent.trim().slice(0,8),i===2?getComputedStyle(its[i]).backgroundColor:'-',its[i].matches(':hover')]);}return JSON.stringify(o);})()" > "$ROOT/mg-work/r107/ev/e107b.log" 2>&1

echo "shots-e1 done"

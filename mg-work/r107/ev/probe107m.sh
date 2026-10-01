#!/usr/bin/env bash
# 第十一拍 ④ 真机取证：产物预览层 / 终端多标签 / 浏览器截图。
# ⚠ 同一时刻只有一个 UI 实测进程 ⇒ 整条链路必须在**一次调用**里跑完。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p107m.js")"

run() { "$NODE" "$CLI" "$@" 2>&1; }
ph()  { run eval "window.__M='$1'; $JS" | tail -1; }

echo "### open"
run open "$URL" >/dev/null
run set viewport 1440 900 >/dev/null

echo "### wait skeleton"
run wait 3800 >/dev/null

echo "### open right panel"
run click ".r93-baract[data-r93-browse]" >/dev/null
run wait 900 >/dev/null

echo "=== [1] SUMMARY · 预览层（文档） ==="
run eval "window.__M='sum1'; $JS" | tail -1
echo "--- 关闭按钮 ---"
run eval "window.__M='sumx'; $JS" | tail -1
echo "--- 再开 + Esc 裁决（预览层关掉、侧栏不许关） ---"
run eval "window.__M='sum1'; $JS" >/dev/null
run wait 300 >/dev/null
run press Escape >/dev/null
run wait 300 >/dev/null
run eval "window.__M='sumx'; $JS" | tail -1
run eval "JSON.stringify({paneOpen: !!document.querySelector('.td-browse') && !document.querySelector('.td-browse').closest('[hidden]'), prevHidden: document.querySelector('[data-td-prev]').hasAttribute('hidden')})" | tail -1

echo "=== [2] SUMMARY · 预览层（表格） ==="
run eval "window.__M='sum2'; $JS" | tail -1

echo "=== [3] TERMINAL · 多标签 ==="
run click ".td-browse-add" >/dev/null
run wait 400 >/dev/null
run click "[data-td-open-mod='terminal']" >/dev/null
run wait 600 >/dev/null
run eval "window.__M='term'; $JS" | tail -1
echo "--- 切到 t2 ---"
run eval "window.__M='term2'; $JS" | tail -1
echo "--- 新建标签 ---"
run eval "window.__M='term3'; $JS" | tail -1

echo "=== [4] BROWSER · 截图 ==="
run click ".td-browse-add" >/dev/null
run wait 400 >/dev/null
run click "[data-td-open-mod='browser']" >/dev/null
run wait 600 >/dev/null
run eval "window.__M='shot'; $JS" | tail -1
run wait 500 >/dev/null
run eval "window.__M='shot2'; $JS" | tail -1

echo "### done"

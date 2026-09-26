#!/usr/bin/env bash
# 第21轮 补充实测：hover 后点卡内按钮不跳转 / 虚位卡不跳转 / 截图
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/task-detail.html"
KB="http://127.0.0.1:8866/pages/kanban.html"
OUT="mg-work/r21"

echo "=== A. hover 让「转派」可见后点击 ==="
$AB open "$KB" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.5
$AB hover ".kb-card" >/dev/null 2>&1
sleep 0.4
echo "  按钮 opacity: $($AB eval "getComputedStyle(document.querySelector('.kb-btn-assign')).opacity")  visibility: $($AB eval "getComputedStyle(document.querySelector('.kb-btn-assign')).visibility")"
echo "  按钮 box: $($AB eval "JSON.stringify((document.querySelector('.kb-btn-assign').getBoundingClientRect()))")"
$AB click ".kb-btn-assign" >/dev/null 2>&1
sleep 1.5
echo "  URL = $($AB eval "location.href")"

echo "=== B. 合成点击（target 就是按钮）==="
$AB open "$KB" >/dev/null 2>&1
sleep 2.5
$AB eval "(function(){document.querySelector('.kb-btn-assign').click();return 'clicked';})()"
sleep 1.2
echo "  URL = $($AB eval "location.href")"

echo "=== C. 虚位卡（is-dashed）不跳转 ==="
$AB open "$KB" >/dev/null 2>&1
sleep 2.5
$AB click ".kb-card.is-dashed" >/dev/null 2>&1
sleep 1.5
echo "  URL = $($AB eval "location.href")"

echo "=== D. 截图 ==="
$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.5
$AB screenshot "$OUT/td-default.png" >/dev/null 2>&1
echo "  default -> $OUT/td-default.png"
# 拖宽右栏
$AB mouse move 939 400 >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for x in 900 860 820 790 790; do $AB mouse move $x 400 >/dev/null 2>&1; sleep 0.03; done
$AB mouse up >/dev/null 2>&1; sleep 0.4
$AB screenshot "$OUT/td-drag-wide.png" >/dev/null 2>&1
echo "  drag-wide -> $OUT/td-drag-wide.png"
# 折叠
$AB eval "(function(){var r=document.querySelector('.td-root');r.classList.add('is-collapsed');r.style.setProperty('--td-right-w','48px');return 1;})()" >/dev/null 2>&1
sleep 0.3
$AB screenshot "$OUT/td-collapsed.png" >/dev/null 2>&1
echo "  collapsed -> $OUT/td-collapsed.png"
ls -la $OUT/*.png

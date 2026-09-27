#!/usr/bin/env bash
# 第29轮补测 1c：真实鼠标 hover → 点「执行」→ 跳转任务详情页
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL_BOARD="http://127.0.0.1:8866/pages/kanban.html"
OUT="mg-work/r29/shots"

$AB open "$URL_BOARD" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0

echo "--- 1c-1. hover 前：按钮存在但不可见 ---"
$AB eval "JSON.stringify((function(){var b=document.querySelector('.kb-btn-exec');var r=b.getBoundingClientRect();return {tag:b.tagName,text:b.textContent,vis:getComputedStyle(b).visibility,op:getComputedStyle(b).opacity,box:Math.round(r.width)+'x'+Math.round(r.height),gx:Math.round(r.left+r.width/2),gy:Math.round(r.top+r.height/2)};})())" 2>&1 | tail -1

GXY=$($AB eval "JSON.stringify((function(){var b=document.querySelector('.kb-btn-exec');var r=b.getBoundingClientRect();return {gx:Math.round(r.left+r.width/2),gy:Math.round(r.top+r.height/2)};})())" 2>&1 | tail -1)
read GX GY <<< "$(echo "$GXY" | $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")"
echo "target point: $GX,$GY"

echo "--- 1c-2. 真实鼠标移动到该点 → 卡片 hover，按钮应显形 ---"
$AB mouse move "$GX" "$GY" >/dev/null 2>&1
sleep 0.5
$AB eval "JSON.stringify((function(){var b=document.querySelector('.kb-btn-exec');var h=document.elementFromPoint($GX,$GY);return {vis:getComputedStyle(b).visibility,op:getComputedStyle(b).opacity,cardHover:!!b.closest('.kb-card').matches(':hover'),hitIsExec:!!(h&&h.classList&&h.classList.contains('kb-btn-exec')),hitTag:h?h.tagName:'none'};})())" 2>&1 | tail -1
$AB screenshot "$OUT/10-board-exec-hover.png" >/dev/null 2>&1

echo "--- 1c-3. 点下 → 应跳 task-detail.html ---"
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 1.6
$AB eval "JSON.stringify({url:location.pathname.split('/').pop(),isDetail:!!document.querySelector('.td-root'),hasFullscreenBtn:!!document.querySelector('[data-td-fullscreen]')})" 2>&1 | tail -1

echo "--- 1c-4. 从详情页返回看板（链接互通性） ---"
$AB open "$URL_BOARD" >/dev/null 2>&1
sleep 2.5
$AB eval "JSON.stringify({url:location.pathname.split('/').pop(),execCount:document.querySelectorAll('.kb-btn-exec').length})" 2>&1 | tail -1

echo "DONE"

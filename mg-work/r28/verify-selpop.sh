#!/usr/bin/env bash
# 第28轮补测：DS Select 弹层的真实可见性（opacity/visibility/命中测试）
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"
OUT="mg-work/r28/shots"
mkdir -p "$OUT"

M="[].slice.call(document.querySelectorAll('.td-composer .giencoder-select')).filter(function(e){return e.querySelector('.giencoder-select-view-text');})"
PROBE="JSON.stringify((function(){var s=$M;var m=s[s.length-1];var p=m.querySelector('.giencoder-select-popup');var cs=getComputedStyle(p);var b=p.getBoundingClientRect();var cx=Math.round(b.left+b.width/2),cy=Math.round(b.top+14);var hit=document.elementFromPoint(cx,cy);return {cls:p.className,open:p.classList.contains('giencoder-popup-open'),vis:cs.visibility,op:cs.opacity,tr:cs.translate,pop:[Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)],hitInPopup:!!(hit&&hit.closest&&hit.closest('.giencoder-select-popup')),hitCls:hit?String(hit.className).slice(0,40):'none'};})())"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0

echo "=== S1. 大模型下拉：关闭态 ==="
$AB eval "JSON.stringify((function(){var s=$M;var m=s[s.length-1];var p=m.querySelector('.giencoder-select-popup');var cs=getComputedStyle(p);return {cls:p.className,vis:cs.visibility,op:cs.opacity};})())" 2>&1 | tail -1

echo "=== S2. 点击展开 ==="
$AB eval "(function(){var s=$M;s[s.length-1].querySelector('.giencoder-select-view').click();})()" >/dev/null 2>&1
sleep 0.6
$AB eval "$PROBE" 2>&1 | tail -1
$AB screenshot "$OUT/06-model-pop.png" >/dev/null 2>&1

echo "=== S3. 选中第 2 项 → 文案回写 + 收起 ==="
$AB eval "(function(){var s=$M;s[s.length-1].querySelectorAll('.giencoder-select-option')[1].click();})()" >/dev/null 2>&1
sleep 0.5
$AB eval "JSON.stringify((function(){var s=$M;var m=s[s.length-1];var p=m.querySelector('.giencoder-select-popup');var cs=getComputedStyle(p);return {text:m.querySelector('.giencoder-select-view-text').textContent,open:p.classList.contains('giencoder-popup-open'),vis:cs.visibility,op:cs.opacity,aria:m.querySelector('.giencoder-select-view').getAttribute('aria-expanded'),popFlag:document.documentElement.hasAttribute('data-td-pop-open')};})())" 2>&1 | tail -1

echo "=== S4. 点禁用项 → 不选中、保持展开 ==="
$AB eval "(function(){var s=$M;s[s.length-1].querySelector('.giencoder-select-view').click();})()" >/dev/null 2>&1
sleep 0.5
$AB eval "(function(){var s=$M;s[s.length-1].querySelector('.giencoder-select-option-disabled').click();})()" >/dev/null 2>&1
sleep 0.4
$AB eval "JSON.stringify((function(){var s=$M;var m=s[s.length-1];var p=m.querySelector('.giencoder-select-popup');return {text:m.querySelector('.giencoder-select-view-text').textContent,open:p.classList.contains('giencoder-popup-open')};})())" 2>&1 | tail -1

echo "=== S5. 点外部 → 关闭 ==="
$AB eval "(function(){document.querySelector('.td-chat').click();})()" >/dev/null 2>&1
sleep 0.4
$AB eval "JSON.stringify((function(){var s=$M;var m=s[s.length-1];var p=m.querySelector('.giencoder-select-popup');return {open:p.classList.contains('giencoder-popup-open'),vis:getComputedStyle(p).visibility,popFlag:document.documentElement.hasAttribute('data-td-pop-open')};})())" 2>&1 | tail -1

echo "=== S6. Esc → 关闭弹层且不跳转看板 ==="
$AB eval "(function(){var s=$M;s[s.length-1].querySelector('.giencoder-select-view').click();})()" >/dev/null 2>&1
sleep 0.4
$AB press Escape >/dev/null 2>&1
sleep 0.5
$AB eval "JSON.stringify((function(){var s=$M;var m=s[s.length-1];return {open:m.querySelector('.giencoder-select-popup').classList.contains('giencoder-popup-open'),url:location.pathname.split('/').pop(),popFlag:document.documentElement.hasAttribute('data-td-pop-open')};})())" 2>&1 | tail -1

echo "=== S7. 标准模式下拉（第 1 个 select）==="
$AB eval "(function(){var s=$M;s[0].querySelector('.giencoder-select-view').click();})()" >/dev/null 2>&1
sleep 0.6
$AB eval "JSON.stringify((function(){var s=$M;var m=s[0];var p=m.querySelector('.giencoder-select-popup');var cs=getComputedStyle(p);var b=p.getBoundingClientRect();return {open:p.classList.contains('giencoder-popup-open'),vis:cs.visibility,op:cs.opacity,pop:[Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)]};})())" 2>&1 | tail -1
$AB screenshot "$OUT/08-mode-pop.png" >/dev/null 2>&1

echo "DONE"

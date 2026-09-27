#!/usr/bin/env bash
# 第29轮验证：1) 看板「执行」按钮 → 任务详情页；2) 详情页全屏后内容区 860px 居中
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL_BOARD="http://127.0.0.1:8866/pages/kanban.html"
URL_DETAIL="http://127.0.0.1:8866/pages/task-detail.html"
OUT="mg-work/r29/shots"
mkdir -p "$OUT"

echo "=================================================="
echo "第 1 项：看板「执行」按钮 → 任务详情页"
echo "=================================================="
echo "--- 1a. 修前状态与按钮存在性 ---"
$AB open "$URL_BOARD" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0
$AB eval "JSON.stringify((function(){var ex=document.querySelectorAll('.kb-btn-exec');var as=document.querySelectorAll('.kb-btn-assign');var e0=ex[0];var cs=e0?getComputedStyle(e0):null;return {execCount:ex.length,assignCount:as.length,execTag:e0?e0.tagName:'none',execText:e0?e0.textContent:'',visBeforeHover:cs?cs.visibility:'n/a',opBeforeHover:cs?cs.opacity:'n/a',cursor:cs?cs.cursor:'n/a'};})())" 2>&1 | tail -1

echo "--- 1b. hover 卡片 → 执行按钮显形，取中心点 ---"
CARD=$($AB eval "JSON.stringify((function(){var b=document.querySelector('.kb-btn-exec');return {card:!!b};})())" 2>&1 | tail -1)
$AB eval "(function(){var b=document.querySelector('.kb-btn-exec');var c=b.closest('.kb-card');c.dispatchEvent(new MouseEvent('mouseover',{bubbles:true}));})()" >/dev/null 2>&1
$AB eval "JSON.stringify((function(){var b=document.querySelector('.kb-btn-exec');var r=b.getBoundingClientRect();return {gx:Math.round(r.left+r.width/2),gy:Math.round(r.top+r.height/2),vis:getComputedStyle(b).visibility,op:getComputedStyle(b).opacity,box:Math.round(r.width)+'x'+Math.round(r.height)};})())" 2>&1 | tail -1
GXY=$($AB eval "JSON.stringify((function(){var b=document.querySelector('.kb-btn-exec');var r=b.getBoundingClientRect();return {gx:Math.round(r.left+r.width/2),gy:Math.round(r.top+r.height/2)};})())" 2>&1 | tail -1)
read GX GY <<< "$(echo "$GXY" | C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")"
echo "click 执行 at $GX,$GY"

echo "--- 1c. 点「执行」 → 应跳到 task-detail.html ---"
$AB mouse move "$GX" "$GY" >/dev/null 2>&1
sleep 0.35
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 1.5
$AB eval "JSON.stringify((function(){return {url:location.pathname.split('/').pop(),hasDetail:!!document.querySelector('.td-root')||document.title;};})())" 2>&1 | tail -1

echo "--- 1d. 回归：点卡片空白处仍进详情页 ---"
$AB open "$URL_BOARD" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.5
CT=$($AB eval "JSON.stringify((function(){var t=document.querySelector('.kb-card-title');var r=t.getBoundingClientRect();return {gx:Math.round(r.left+20),gy:Math.round(r.top+8)};})())" 2>&1 | tail -1)
read CX CY <<< "$(echo "$CT" | C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")"
$AB mouse move "$CX" "$CY" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 1.5
$AB eval "JSON.stringify({url:location.pathname.split('/').pop()})" 2>&1 | tail -1

echo "--- 1e. 回归：点「转派」按钮 → 不应跳转 ---"
$AB open "$URL_BOARD" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.5
AT=$($AB eval "JSON.stringify((function(){var b=document.querySelector('.kb-btn-assign');var c=b.closest('.kb-card');c.dispatchEvent(new MouseEvent('mouseover',{bubbles:true}));var r=b.getBoundingClientRect();return {gx:Math.round(r.left+r.width/2),gy:Math.round(r.top+r.height/2),box:Math.round(r.width)+'x'+Math.round(r.height)};})())" 2>&1 | tail -1)
echo "assign rect: $AT"
read AX AY <<< "$(echo "$AT" | C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")"
$AB mouse move "$AX" "$AY" >/dev/null 2>&1
sleep 0.35
$AB mouse down >/dev/null 2>&1
$AB mouse up >/dev/null 2>&1
sleep 1.2
$AB eval "JSON.stringify({url:location.pathname.split('/').pop()})" 2>&1 | tail -1

echo ""
echo "=================================================="
echo "第 2 项：详情页全屏后内容区 860px 居中"
echo "=================================================="
PROBE="JSON.stringify((function(){var right=document.querySelector('.td-right');var chat=document.querySelector('.td-chat');var inner=document.querySelector('.td-chat-inner');var comp=document.querySelector('.td-composer');function box(e){var r=e.getBoundingClientRect();return {l:Math.round(r.left),r:Math.round(r.right),w:Math.round(r.width),c:Math.round((r.left+r.right)/2*10)/10};}var rb=box(right),ib=box(inner),cb=box(comp);return {fullscreen:document.querySelector('.td-root').classList.contains('is-fullscreen'),rightW:rb.w,chatAlign:getComputedStyle(chat).alignItems,inner:ib,composer:cb,innerVsRightCenter:Math.round((ib.c-rb.c)*10)/10,composerVsRightCenter:Math.round((cb.c-rb.c)*10)/10,innerEqComposer:Math.abs(ib.l-cb.l)<=1&&Math.abs(ib.r-cb.r)<=1};})())"

echo "--- 2a. 全屏前（基线不应被改） ---"
$AB open "$URL_DETAIL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0
$AB eval "$PROBE" 2>&1 | tail -1

echo "--- 2b. 点全屏 → 内容区 860 居中 ---"
$AB eval "(function(){document.querySelector('[data-td-fullscreen]').click();})()" >/dev/null 2>&1
sleep 0.7
$AB eval "$PROBE" 2>&1 | tail -1
$AB screenshot "$OUT/01-fullscreen-1440.png" >/dev/null 2>&1

echo "--- 2c. 1920 视口下仍 860 居中 ---"
$AB set viewport 1920 1080 >/dev/null 2>&1
sleep 0.8
$AB eval "$PROBE" 2>&1 | tail -1
$AB screenshot "$OUT/02-fullscreen-1920.png" >/dev/null 2>&1

echo "--- 2d. 退出全屏 → 恢复 ---"
$AB eval "(function(){document.querySelector('[data-td-fullscreen]').click();})()" >/dev/null 2>&1
sleep 0.6
$AB eval "$PROBE" 2>&1 | tail -1

echo "--- 2e. 全屏下消息列内容宽度 / 用户气泡对齐（应贴 860 列右缘） ---"
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 0.4
$AB eval "(function(){document.querySelector('[data-td-fullscreen]').click();})()" >/dev/null 2>&1
sleep 0.6
$AB eval "JSON.stringify((function(){var inner=document.querySelector('.td-chat-inner');var u=document.querySelector('.td-msg-user');var ir=inner.getBoundingClientRect();var ur=u.getBoundingClientRect();var ai=document.querySelector('.td-msg-ai').getBoundingClientRect();return {innerW:Math.round(ir.width),innerL:Math.round(ir.left),innerR:Math.round(ir.right),userW:Math.round(ur.width),userRightGap:Math.round(ir.right-ur.right),aiW:Math.round(ai.width)};})())" 2>&1 | tail -1
$AB screenshot "$OUT/03-fullscreen-chat.png" >/dev/null 2>&1

echo "--- 2f. 回归：Esc 先退出全屏（不退详情页） ---"
$AB press Escape >/dev/null 2>&1
sleep 0.7
$AB eval "JSON.stringify((function(){return {url:location.pathname.split('/').pop(),fullscreen:document.querySelector('.td-root').classList.contains('is-fullscreen'),rightW:Math.round(document.querySelector('.td-right').getBoundingClientRect().width)};})())" 2>&1 | tail -1
$AB press Escape >/dev/null 2>&1
sleep 1.2
$AB eval "JSON.stringify({url:location.pathname.split('/').pop()})" 2>&1 | tail -1

echo "DONE"

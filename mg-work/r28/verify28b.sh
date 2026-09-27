#!/usr/bin/env bash
# 第28轮补测：1（标题栏拖动互换）+ 4e/4f（大模型下拉开合与选中）
# 上一轮 verify28.sh 里两处「测量脚本自身的 bug」：
#   · agent-browser eval 的输出是「JSON 编码过的字符串」→ 解析要 decode 两次
#   · 技能面板本身带 .giencoder-select 类（与 base.html 一致），
#     所以「取最后一个 .giencoder-select 当大模型选择器」会取到面板 → 要 :not(.td-skill-pop)
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"
J() { $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['$1'],d['$2'])"; }

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0

echo "=== 4e. 大模型下拉：点击展开 ==="
$AB eval "JSON.stringify((function(){var m=document.querySelector('.td-composer .giencoder-select:not(.td-skill-pop):not(:has(.giencoder-select-view-text))');var sels=[].slice.call(document.querySelectorAll('.td-composer .giencoder-select')).filter(function(e){return e.querySelector('.giencoder-select-view-text');});var m=sels[sels.length-1];window.__m=sels;return {n:sels.length,text:m.querySelector('.giencoder-select-view-text').textContent,display:getComputedStyle(m.querySelector('.giencoder-select-popup')).display,opts:[].map.call(m.querySelectorAll('.giencoder-select-option'),function(o){return o.textContent+(o.classList.contains('giencoder-select-option-disabled')?'(disabled)':'');})};})())"
$AB eval "(function(){var sels=[].slice.call(document.querySelectorAll('.td-composer .giencoder-select')).filter(function(e){return e.querySelector('.giencoder-select-view-text');});sels[sels.length-1].querySelector('.giencoder-select-view').click();})()" >/dev/null 2>&1
sleep 0.4
$AB eval "JSON.stringify((function(){var sels=[].slice.call(document.querySelectorAll('.td-composer .giencoder-select')).filter(function(e){return e.querySelector('.giencoder-select-view-text');});var m=sels[sels.length-1];return {display:getComputedStyle(m.querySelector('.giencoder-select-popup')).display,aria:m.querySelector('.giencoder-select-view').getAttribute('aria-expanded'),popFlag:document.documentElement.hasAttribute('data-td-pop-open'),box:(function(){var b=m.querySelector('.giencoder-select-popup').getBoundingClientRect();return Math.round(b.width)+'x'+Math.round(b.height);})()};})())"
$AB screenshot "mg-work/r28/verify-modelpop.png" >/dev/null 2>&1

echo "=== 4f. 选中 GLM-5.2-公司共用 → 文案回写 + 关闭 ==="
$AB eval "(function(){var sels=[].slice.call(document.querySelectorAll('.td-composer .giencoder-select')).filter(function(e){return e.querySelector('.giencoder-select-view-text');});sels[sels.length-1].querySelectorAll('.giencoder-select-option')[1].click();})()" >/dev/null 2>&1
sleep 0.3
$AB eval "JSON.stringify((function(){var sels=[].slice.call(document.querySelectorAll('.td-composer .giencoder-select')).filter(function(e){return e.querySelector('.giencoder-select-view-text');});var m=sels[sels.length-1];return {textAfter:m.querySelector('.giencoder-select-view-text').textContent,selected:[].map.call(m.querySelectorAll('.giencoder-select-option-selected'),function(o){return o.textContent;}),display:getComputedStyle(m.querySelector('.giencoder-select-popup')).display,popFlag:document.documentElement.hasAttribute('data-td-pop-open')};})())"
echo "=== 4f2. 点禁用项 → 不选中、不关闭 ==="
$AB eval "(function(){var sels=[].slice.call(document.querySelectorAll('.td-composer .giencoder-select')).filter(function(e){return e.querySelector('.giencoder-select-view-text');});sels[sels.length-1].querySelector('.giencoder-select-view').click();})()" >/dev/null 2>&1
sleep 0.3
$AB eval "(function(){var sels=[].slice.call(document.querySelectorAll('.td-composer .giencoder-select')).filter(function(e){return e.querySelector('.giencoder-select-view-text');});sels[sels.length-1].querySelector('.giencoder-select-option-disabled').click();})()" >/dev/null 2>&1
sleep 0.3
$AB eval "JSON.stringify((function(){var sels=[].slice.call(document.querySelectorAll('.td-composer .giencoder-select')).filter(function(e){return e.querySelector('.giencoder-select-view-text');});var m=sels[sels.length-1];return {text:m.querySelector('.giencoder-select-view-text').textContent,display:getComputedStyle(m.querySelector('.giencoder-select-popup')).display};})())"
$AB eval "(function(){document.body.click();})()" >/dev/null 2>&1

echo ""
echo "=== 1. 按住左栏标题栏向右拖 → 两栏互换 ==="
B=$($AB eval "JSON.stringify((function(){var b=document.querySelector('.td-bar').getBoundingClientRect();return {gx:Math.round(b.left+140),gy:Math.round(b.top+24)};})())" 2>&1 | tail -1)
read X Y <<< "$(echo "$B" | $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")"
echo "grab at $X,$Y"
$AB mouse move "$X" "$Y" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
for dx in 15 35 55 75 95 120 140; do $AB mouse move "$((X+dx))" "$Y" >/dev/null 2>&1; done
sleep 0.2
$AB eval "JSON.stringify({duringCls:document.querySelector('.td-root').className})"
$AB mouse up >/dev/null 2>&1
sleep 0.5
$AB eval "JSON.stringify((function(){var L=document.querySelector('.td-left').getBoundingClientRect();var R=document.querySelector('.td-right').getBoundingClientRect();var r=document.querySelector('.td-root');return {rootCls:r.className,flexDir:getComputedStyle(r).flexDirection,leftL:Math.round(L.left),rightL:Math.round(R.left),rightIsLeft:R.left<L.left,sideBorder:getComputedStyle(document.querySelector('.td-side')).borderLeftWidth};})())"
$AB screenshot "mg-work/r28/verify-swapped.png" >/dev/null 2>&1

echo "=== 1b. 反向拖回（标题栏此时在右侧，向左拖） ==="
B2=$($AB eval "JSON.stringify((function(){var b=document.querySelector('.td-bar').getBoundingClientRect();return {gx:Math.round(b.left+140),gy:Math.round(b.top+24)};})())" 2>&1 | tail -1)
read X2 Y2 <<< "$(echo "$B2" | $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")"
echo "grab at $X2,$Y2"
$AB mouse move "$X2" "$Y2" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
for dx in 15 35 55 75 95 120 140; do $AB mouse move "$((X2-dx))" "$Y2" >/dev/null 2>&1; done
$AB mouse up >/dev/null 2>&1
sleep 0.5
$AB eval "JSON.stringify((function(){var L=document.querySelector('.td-left').getBoundingClientRect();var R=document.querySelector('.td-right').getBoundingClientRect();var r=document.querySelector('.td-root');return {rootCls:r.className,leftL:Math.round(L.left),rightL:Math.round(R.left),restored:R.left>L.left};})())"

echo "=== 1c. 纯点击标题栏（位移<6px）→ 不应互换 ==="
$AB eval "JSON.stringify({before:document.querySelector('.td-root').className})"
B3=$($AB eval "JSON.stringify((function(){var b=document.querySelector('.td-bar').getBoundingClientRect();return {gx:Math.round(b.left+140),gy:Math.round(b.top+24)};})())" 2>&1 | tail -1)
read X3 Y3 <<< "$(echo "$B3" | $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")"
$AB mouse move "$X3" "$Y3" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1; $AB mouse move "$((X3+2))" "$Y3" >/dev/null 2>&1; $AB mouse up >/dev/null 2>&1
sleep 0.3
$AB eval "JSON.stringify({after:document.querySelector('.td-root').className})"

echo "=== 1d. 点顶栏「转派」按钮 → 不应触发拖动 ==="
$AB click ".td-bar .giencoder-btn-secondary.giencoder-btn-size-small:not(.giencoder-btn-icon)" >/dev/null 2>&1
sleep 0.3
$AB eval "JSON.stringify({afterBtnClick:document.querySelector('.td-root').className})"

echo "=== 1e. 互换后再拖（向右 140px）→ 复原 + 拖动条方向取反 ==="
B4=$($AB eval "JSON.stringify((function(){var b=document.querySelector('.td-bar').getBoundingClientRect();return {gx:Math.round(b.left+140),gy:Math.round(b.top+24)};})())" 2>&1 | tail -1)
read X4 Y4 <<< "$(echo "$B4" | $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")"
$AB mouse move "$X4" "$Y4" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for dx in 15 35 55 75 95 120 140; do $AB mouse move "$((X4+dx))" "$Y4" >/dev/null 2>&1; done
$AB mouse up >/dev/null 2>&1; sleep 0.4
$AB eval "JSON.stringify((function(){var r=document.querySelector('.td-root');var R=document.querySelector('.td-right').getBoundingClientRect();return {cls:r.className,rightW:Math.round(R.width),gutterAria:document.querySelector('[data-td-gutter]').getAttribute('aria-valuenow')};})())"
GB=$($AB eval "JSON.stringify((function(){var b=document.querySelector('[data-td-gutter]').getBoundingClientRect();return {gx:Math.round(b.left+b.width/2),gy:Math.round(b.top+b.height/2)};})())" 2>&1 | tail -1)
read GX GY <<< "$(echo "$GB" | $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")"
$AB mouse move "$GX" "$GY" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for dx in 10 20 30 40; do $AB mouse move "$((GX+dx))" "$GY" >/dev/null 2>&1; done
$AB mouse up >/dev/null 2>&1; sleep 0.3
$AB eval "JSON.stringify((function(){var R=document.querySelector('.td-right').getBoundingClientRect();return {afterSwappedGutterRight:Math.round(R.width)};})())"

echo "=== 1f. 复原态下拖动条：向左拖 → 右栏变宽（方向仍正确） ==="
GB2=$($AB eval "JSON.stringify((function(){var b=document.querySelector('[data-td-gutter]').getBoundingClientRect();return {gx:Math.round(b.left+b.width/2),gy:Math.round(b.top+b.height/2)};})())" 2>&1 | tail -1)
read GX2 GY2 <<< "$(echo "$GB2" | $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")"
$AB mouse move "$GX2" "$GY2" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for dx in 10 20 30 40; do $AB mouse move "$((GX2-dx))" "$GY2" >/dev/null 2>&1; done
$AB mouse up >/dev/null 2>&1; sleep 0.3
$AB eval "JSON.stringify((function(){var R=document.querySelector('.td-right').getBoundingClientRect();return {afterNormalGutterLeft:Math.round(R.width)};})())"

$AB close >/dev/null 2>&1
echo DONE

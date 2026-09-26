#!/usr/bin/env bash
# 第21轮 任务详情页 实测 v3：每步重新读取 gutter 实测中心再拖
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"
KB="http://127.0.0.1:8866/pages/kanban.html"

M='JSON.stringify((function(){var r=document.querySelector(".td-root"),l=document.querySelector(".td-left"),g=document.querySelector("[data-td-gutter]"),rt=document.querySelector(".td-right");if(!r)return{err:"NO_ROOT"};var cs=getComputedStyle(r);function b(e){if(!e)return null;var t=e.getBoundingClientRect();return{x:+t.left.toFixed(1),y:+t.top.toFixed(1),w:+t.width.toFixed(1),h:+t.height.toFixed(1),r:+t.right.toFixed(1)};}return{root:b(r),left:b(l),gut:b(g),right:b(rt),collapsed:r.classList.contains("is-collapsed"),vRight:cs.getPropertyValue("--td-right-w").trim(),scrollH:document.documentElement.scrollHeight};})())'

show() { $AB eval "$M" | $PY -c "
import sys,json
d=json.loads(json.loads(sys.stdin.read()))
if 'err' in d: print('  ERR', d['err']); raise SystemExit
print('  root=%sx%s  left=%s  gutter@%s(w%s)  right@%s w=%s h=%s' % (d['root']['w'],d['root']['h'],d['left']['w'],d['gut']['x'],d['gut']['w'],d['right']['x'],d['right']['w'],d['right']['h']))
print('  collapsed=%s  vRight=%s  scrollH=%s' % (d['collapsed'],d['vRight'],d['scrollH']))
"; }

center() { $AB eval "$M" | $PY -c "
import sys,json
d=json.loads(json.loads(sys.stdin.read()))
g=d['gut']
print(int(round(g['x']+g['w']/2.0)), int(round(min(g['y']+g['h']/2.0,400))))
"; }

drag() { # $1 = 目标 x
  local cx cy tx
  read cx cy <<< "$(center)"
  tx=$1
  $AB mouse move "$cx" "$cy" >/dev/null 2>&1
  $AB mouse down >/dev/null 2>&1
  local i x
  for i in 1 2 3 4 5 6; do
    x=$(( cx + (tx - cx) * i / 6 ))
    $AB mouse move "$x" "$cy" >/dev/null 2>&1
    sleep 0.04
  done
  $AB mouse up >/dev/null 2>&1
  sleep 0.4
  echo "  (dragged $cx -> $tx)"
}

echo "=== 0. 初始态 ==="
$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.5
show

echo "=== 1. 向左拖 150px（右栏应加宽）==="
drag 789
show

echo "=== 2. 向右拖 200px（右栏应收窄）==="
drag 989
show

echo "=== 3. 拖到右栏 < 320px 松手（应自动折叠）==="
RX=$($AB eval "$M" | $PY -c "import sys,json;d=json.loads(json.loads(sys.stdin.read()));print(int(d['root']['r']-200-12))")
drag "$RX"
show
echo "  折叠列文案: $($AB eval "JSON.stringify((document.querySelector('.td-collapsed')||{}).textContent||'')" | tr -d '\n' | tr -s ' ')"
echo "  折叠列 display: $($AB eval "getComputedStyle(document.querySelector('.td-collapsed')).display")"
echo "  右栏内容 display: $($AB eval "getComputedStyle(document.querySelector('.td-right-inner')).display")"

echo "=== 4. 点击折叠列（应恢复 480）==="
$AB click ".td-right" >/dev/null 2>&1
sleep 0.5
show
echo "  折叠列 display: $($AB eval "getComputedStyle(document.querySelector('.td-collapsed')).display")"

echo "=== 5. 返回箭头（应跳 kanban）==="
$AB click "[data-td-back]" >/dev/null 2>&1
sleep 2.5
echo "  URL = $($AB eval "location.href")"

echo "=== 6. 看板卡片点击 -> 详情页 ==="
$AB open "$KB" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.5
echo "  卡片数: $($AB eval "document.querySelectorAll('.kb-card').length")  虚位卡: $($AB eval "document.querySelectorAll('.kb-card.is-dashed').length")"
$AB click ".kb-card" >/dev/null 2>&1
sleep 2.5
echo "  URL = $($AB eval "location.href")"

echo "=== 7. 卡内「转派」按钮不跳转 ==="
$AB open "$KB" >/dev/null 2>&1
sleep 2.5
echo "  转派按钮数: $($AB eval "document.querySelectorAll('.kb-btn-assign').length")"
$AB click ".kb-btn-assign" >/dev/null 2>&1
sleep 1.5
echo "  URL = $($AB eval "location.href")"

echo "=== 8. 详情页 Esc 返回 ==="
$AB open "$URL" >/dev/null 2>&1
sleep 2.0
$AB press "Escape" >/dev/null 2>&1
sleep 2.0
echo "  URL = $($AB eval "location.href")"

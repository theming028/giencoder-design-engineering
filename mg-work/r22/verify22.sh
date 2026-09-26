#!/usr/bin/env bash
# 第22轮实测
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"
KB="http://127.0.0.1:8866/pages/kanban.html"

M='JSON.stringify((function(){function b(s){var e=document.querySelector(s);if(!e)return null;var r=e.getBoundingClientRect();return{x:+r.left.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1),r:+r.right.toFixed(1)};}var cs=function(s,p){var e=document.querySelector(s);return e?getComputedStyle(e)[p]:null;};return{root:b(".td-root"),left:b(".td-left"),gut:b(".td-gutter"),right:b(".td-right"),main:b(".td-main"),side:b(".td-side"),asideShell:(function(){var m=document.querySelector("main");var row=m&&m.parentElement;var a=row&&row.querySelector(":scope > aside");return a?getComputedStyle(a).display:"none-or-missing";})(),mainBorder:cs("main","borderTopWidth"),leftBorder:cs(".td-left","borderTopWidth"),rightBorder:cs(".td-right","borderTopWidth"),barBB:cs(".td-bar","borderBottomWidth"),sideBL:cs(".td-side","borderLeftWidth"),titleBg:cs(".td-title","backgroundColor"),titleBB:cs(".td-title","borderBottomWidth"),collapsed:document.querySelector(".td-root").classList.contains("is-collapsed"),vRight:getComputedStyle(document.querySelector(".td-root")).getPropertyValue("--td-right-w").trim()};})())'

show() { $AB eval "$M" | $PY -c "
import sys,json
d=json.loads(json.loads(sys.stdin.read()))
def f(k):
    v=d[k]
    if v is None: return k+'=None'
    if isinstance(v,dict): return '%s x=%s w=%s' % (k,v['x'],v['w'])
    return '%s=%s' % (k,v)
print('  ' + ' | '.join(f(k) for k in ['root','left','gut','right']))
print('  ' + ' | '.join(f(k) for k in ['main','side']))
print('  shell-aside=%s mainBorder=%s leftBorder=%s rightBorder=%s barBorderBottom=%s sideBorderLeft=%s titleBg=%s titleBorderBottom=%s' % (d['asideShell'],d['mainBorder'],d['leftBorder'],d['rightBorder'],d['barBB'],d['sideBL'],d['titleBg'],d['titleBB']))
print('  collapsed=%s vRight=%s' % (d['collapsed'],d['vRight']))
"; }

echo "=== 0. 布局 / 边框 / 底色 ==="
$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3
show

echo "=== 1. 复用的对话框模块元素 ==="
for sel in '[aria-label=\"添加\"]' '[aria-label=\"技能\"]' '[aria-label=\"数字分身\"]' '[aria-label=\"优化提示词\"]' '[aria-label=\"发送\"]'; do
  echo "  $sel -> $($AB eval "document.querySelectorAll('$sel').length")"
done
echo "  标准模式 -> $($AB eval "document.querySelectorAll('.giencoder-select-view-text').length")"
echo "  composer 高度 -> $($AB eval "document.querySelector('.td-composer').getBoundingClientRect().height")"
echo "  textarea minH -> $($AB eval "getComputedStyle(document.querySelector('.td-composer textarea')).minHeight")"
echo "  发送按钮尺寸 -> $($AB eval "JSON.stringify((function(){var e=document.querySelector('[aria-label=\\\"发送\\\"]');var r=e.getBoundingClientRect();return [+r.width.toFixed(1),+r.height.toFixed(1),getComputedStyle(e).borderRadius];})())")"
echo "  艾迪按钮 -> $($AB eval "JSON.stringify((function(){var e=document.querySelector('[aria-label=\\\"数字分身\\\"]');var r=e.getBoundingClientRect();var c=getComputedStyle(e);return [+r.width.toFixed(1),+r.height.toFixed(1),c.backgroundColor,c.color];})())")"

echo "=== 2. 右栏头部三图标（32×32） ==="
$AB eval "JSON.stringify(Array.prototype.map.call(document.querySelectorAll('.td-round-btn'),function(e){var r=e.getBoundingClientRect();return [e.getAttribute('aria-label'),+r.width.toFixed(1),+r.height.toFixed(1)];}))" | $PY -c "import sys,json;print(' ',json.loads(json.loads(sys.stdin.read())))"

echo "=== 3. 展开全文 / 收起 ==="
echo "  初始 描述区可视高/内容高 -> $($AB eval "JSON.stringify((function(){var e=document.querySelector('[data-td-desc]');return [+e.getBoundingClientRect().height.toFixed(1),e.scrollHeight];})())")"
echo "  按钮文案 -> $($AB eval "document.querySelector('[data-td-desc-toggle]').textContent")"
$AB click "[data-td-desc-toggle]" >/dev/null 2>&1; sleep 0.4
echo "  展开后 可视高/内容高 -> $($AB eval "JSON.stringify((function(){var e=document.querySelector('[data-td-desc]');return [+e.getBoundingClientRect().height.toFixed(1),e.scrollHeight];})())")"
echo "  按钮文案 -> $($AB eval "document.querySelector('[data-td-desc-toggle]').textContent")"
echo "  aria-expanded -> $($AB eval "document.querySelector('[data-td-desc-toggle]').getAttribute('aria-expanded')")"
$AB click "[data-td-desc-toggle]" >/dev/null 2>&1; sleep 0.4
echo "  再点后 可视高 -> $($AB eval "document.querySelector('[data-td-desc]').getBoundingClientRect().height")"
echo "  按钮文案 -> $($AB eval "document.querySelector('[data-td-desc-toggle]').textContent")"

echo "=== 4. 拖动 / 折叠 / 恢复 ==="
$AB eval "JSON.stringify((function(){var g=document.querySelector('[data-td-gutter]'),r=document.querySelector('.td-root');return {gutX:+g.getBoundingClientRect().left.toFixed(1),rootR:+r.getBoundingClientRect().right.toFixed(1)};})())"
GUT=$($AB eval "document.querySelector('[data-td-gutter]').getBoundingClientRect().left" | $PY -c "import sys;print(int(float(sys.stdin.read().strip())+4))")
ROOTR=$($AB eval "document.querySelector('.td-root').getBoundingClientRect().right" | $PY -c "import sys;print(int(float(sys.stdin.read().strip())))")
echo "  gutter 中心 x=$GUT, root 右边界=$ROOTR"
$AB mouse move $GUT 400 >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for i in 1 2 3 4 5 6; do $AB mouse move $((GUT - i*25)) 400 >/dev/null 2>&1; sleep 0.03; done
$AB mouse up >/dev/null 2>&1; sleep 0.4
echo "  向左拖 150px 后:"; show
# 拖到过窄
GUT2=$($AB eval "document.querySelector('[data-td-gutter]').getBoundingClientRect().left" | $PY -c "import sys;print(int(float(sys.stdin.read().strip())+4))")
$AB mouse move $GUT2 400 >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for i in 1 2 3 4 5 6; do $AB mouse move $((ROOTR - 200 - 12)) 400 >/dev/null 2>&1; sleep 0.03; done
$AB mouse up >/dev/null 2>&1; sleep 0.5
echo "  拖到右栏<320 松手后:"; show
$AB click ".td-right" >/dev/null 2>&1; sleep 0.5
echo "  点击折叠列后:"; show

echo "=== 5. 跳转链路 ==="
$AB open "$KB" >/dev/null 2>&1; $AB set viewport 1440 900 >/dev/null 2>&1; sleep 2.5
$AB click ".kb-card" >/dev/null 2>&1; sleep 2.5
echo "  卡片 -> $($AB eval "location.pathname")"
$AB click "[data-td-back]" >/dev/null 2>&1; sleep 2.5
echo "  返回 -> $($AB eval "location.pathname")"

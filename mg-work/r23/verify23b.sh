#!/usr/bin/env bash
# 第23轮 回归：字号对齐实测 / 展开收起 / 拖动分栏 / 折叠恢复 / 组件合规自检 / 截图
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.8

echo "=== A. 信息列字号（设计稿 12px / 行高 20） ==="
$AB eval "JSON.stringify((function(){var cs=function(s,p){var e=document.querySelector(s);return e?getComputedStyle(e)[p]:null;};return{attrRow:cs('.td-attr-row','fontSize')+'/'+cs('.td-attr-row','lineHeight'),attrPitch:Math.round((document.querySelectorAll('.td-attr-row')[1].getBoundingClientRect().top-document.querySelectorAll('.td-attr-row')[0].getBoundingClientRect().top)),tlWho:cs('.td-tl-who','fontSize'),tlTime:cs('.td-tl-time','fontSize')+'/'+cs('.td-tl-time','lineHeight'),tlPitch:Math.round((document.querySelectorAll('.td-tl li')[1].getBoundingClientRect().top-document.querySelectorAll('.td-tl li')[0].getBoundingClientRect().top)),sideScroll:[document.querySelector('.td-side').scrollHeight,document.querySelector('.td-side').clientHeight]};})())"

echo "=== B. 展开全文 / 收起 ==="
echo "  before: maxH=$($AB eval "getComputedStyle(document.querySelector('.td-desc-body')).maxHeight") text=$($AB eval "document.querySelector('[data-td-desc-toggle]').textContent")"
$AB click "[data-td-desc-toggle]" >/dev/null 2>&1; sleep 0.4
echo "  after : maxH=$($AB eval "getComputedStyle(document.querySelector('.td-desc-body')).maxHeight") h=$($AB eval "Math.round(document.querySelector('.td-desc-body').getBoundingClientRect().height)") text=$($AB eval "document.querySelector('[data-td-desc-toggle]').textContent") aria=$($AB eval "document.querySelector('[data-td-desc-toggle]').getAttribute('aria-expanded')")"
$AB click "[data-td-desc-toggle]" >/dev/null 2>&1; sleep 0.4
echo "  again : maxH=$($AB eval "getComputedStyle(document.querySelector('.td-desc-body')).maxHeight") text=$($AB eval "document.querySelector('[data-td-desc-toggle]').textContent")"

echo "=== C. 拖动分栏 ==="
gut() { $AB eval "Math.round(document.querySelector('[data-td-gutter]').getBoundingClientRect().left+document.querySelector('[data-td-gutter]').getBoundingClientRect().width/2)"; }
rw() { $AB eval "Math.round(document.querySelector('.td-right').getBoundingClientRect().width)"; }
echo "  init right=$(rw)"
X=$(gut); $AB mouse move $X 400 >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for x in 900 860 820 780 760; do $AB mouse move $x 400 >/dev/null 2>&1; sleep 0.03; done
$AB mouse up >/dev/null 2>&1; sleep 0.4
echo "  drag-left  right=$(rw)"
X=$(gut); $AB mouse move $X 400 >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for x in 1000 1100 1180 1240; do $AB mouse move $x 400 >/dev/null 2>&1; sleep 0.03; done
$AB mouse up >/dev/null 2>&1; sleep 0.4
echo "  drag-right right=$(rw)"

echo "=== D. 折叠 / 点击恢复 ==="
$AB eval "(function(){var r=document.querySelector('.td-root');r.classList.add('is-collapsed');r.style.setProperty('--td-right-w','48px');return 1;})()" >/dev/null 2>&1; sleep 0.4
echo "  collapsed right=$(rw) label=$($AB eval "document.querySelector('.td-collapsed')?document.querySelector('.td-collapsed').textContent.replace(/\s/g,''):''")"
$AB click ".td-right" >/dev/null 2>&1; sleep 0.5
echo "  restored  right=$(rw) isCollapsed=$($AB eval "document.querySelector('.td-root').classList.contains('is-collapsed')")"

echo "=== E. 顶栏按钮尺寸（回归） ==="
$AB eval "JSON.stringify(Array.from(document.querySelectorAll('.td-bar-actions .giencoder-btn')).map(function(b){var r=b.getBoundingClientRect();return (b.getAttribute('aria-label')||b.textContent.trim())+':'+Math.round(r.width)+'x'+Math.round(r.height);}))"

echo "=== F. 截图 ==="
$AB screenshot "mg-work/r23/r23-default.png" >/dev/null 2>&1
$AB eval "document.querySelector('main').scrollTop=0;1" >/dev/null 2>&1
echo "  -> mg-work/r23/r23-default.png"

echo "=== G. 组件合规自检（页面 giencoder-* 与 components.css 差集） ==="
$PY - <<'PY'
import io, re
raw  = io.open('pages/task-detail.html', encoding='utf-8').read()
html = raw.replace('\\"', '"').replace('\\/', '/')     # 内嵌 HTML 是 JS 字符串字面量，先反转义
css  = io.open('giencoder-design-system/components.css', encoding='utf-8').read()
used = set()
for m in re.finditer(r'class="([^"]*)"', html):
    for c in m.group(1).split():
        if c.startswith('giencoder-'): used.add(c)
defined = set(re.findall(r'\.(giencoder-[A-Za-z0-9_-]+)', css))
print('  页面 giencoder-* 类:', len(used), sorted(used))
extra = sorted(used - defined)
print('  虚构类名:', extra if extra else '无 ✓')
PY

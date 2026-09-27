#!/usr/bin/env bash
# 第24轮实测：容器边框形态 / 信息列左线色 / 描述区 list 圆点 / 拖到<100px 折叠+点击恢复 / 任务属性左右布局与行距
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.8

echo "=== 1. 容器边框形态（设计稿：无描边 + 柔和投影） ==="
$AB eval "JSON.stringify(['.td-left','.td-right'].reduce(function(o,s){var e=document.querySelector(s),c=getComputedStyle(e);o[s]={border:c.borderTopWidth+' '+c.borderTopStyle+' '+c.borderTopColor,shadow:c.boxShadow,radius:c.borderTopLeftRadius,bg:c.backgroundColor};return o;},{}))"
echo "  -- 左右边缘取色（x=4..12 / y=400） --"
$AB eval "JSON.stringify((function(){var out=[],r=document.querySelector('.td-left').getBoundingClientRect();for(var x=0;x<13;x++){var e=document.elementFromPoint(x,400);out.push(x+':'+(e?getComputedStyle(e).backgroundColor:'-'));}return {left:Math.round(r.left),out:out};})())"

echo ""
echo "=== 2. 信息列左分隔线颜色（应比 gray-3 #E5E5E5 浅一级 = #F2F2F2） ==="
$AB eval "JSON.stringify((function(){var c=getComputedStyle(document.querySelector('.td-side'));var b=getComputedStyle(document.querySelector('.td-bar'));var t=getComputedStyle(document.querySelector('.td-title'));return {sideLeft:{w:c.borderLeftWidth,color:c.borderLeftColor},barBottom:b.borderBottomColor,titleBottom:t.borderBottomColor};})())"

echo ""
echo "=== 3. 描述区 list（设计稿：圆点 4px / 左缘距内容 7px / 正文缩进 22px / 行距 24） ==="
$AB eval "JSON.stringify((function(){var ul=document.querySelector('.td-desc ul');var lis=ul?ul.querySelectorAll('li'):[];if(!lis.length)return{err:'no li'};var b=getComputedStyle(lis[0],'::before');var a=lis[0].getBoundingClientRect(),c=lis[1].getBoundingClientRect();return {liCount:lis.length,markerContent:b.content,markerSize:b.width+'x'+b.height,markerRadius:b.borderRadius,markerBg:b.backgroundColor,markerLeft:b.left,markerTop:b.top,liPadLeft:getComputedStyle(lis[0]).paddingLeft,liTextX:Math.round(a.left+parseFloat(getComputedStyle(lis[0]).paddingLeft)),descX:Math.round(document.querySelector('.td-desc').getBoundingClientRect().left+parseFloat(getComputedStyle(document.querySelector('.td-desc')).paddingLeft)),pitch:Math.round(c.top-a.top),liMarginBottom:getComputedStyle(lis[0]).marginBottom};})())"

echo ""
echo "=== 4. 任务属性：左右布局（label 列定宽 64）+ 行距 30 ==="
$AB eval "JSON.stringify((function(){var s=document.querySelector('.td-side-attr');var rows=s.querySelectorAll('.td-attr-row');var r0=s.getBoundingClientRect();var base=Math.round(rows[0].querySelector('.td-attr-v').getBoundingClientRect().left);var pitch=[];for(var i=1;i<rows.length;i++)pitch.push(Math.round(rows[i].getBoundingClientRect().top-rows[i-1].getBoundingClientRect().top));return {rows:rows.length,labelW:getComputedStyle(rows[0].querySelector('.td-attr-k')).width,labelX:Array.from(rows).map(function(r){return Math.round(r.querySelector('.td-attr-k').getBoundingClientRect().left);}),valueX:Array.from(rows).map(function(r){return Math.round(r.querySelector('.td-attr-v').getBoundingClientRect().left);}),valueXSpread:Math.max.apply(null,Array.from(rows).map(function(r){return r.querySelector('.td-attr-v').getBoundingClientRect().left}))-Math.min.apply(null,Array.from(rows).map(function(r){return r.querySelector('.td-attr-v').getBoundingClientRect().left})),pitch:pitch,h2Color:getComputedStyle(s.querySelector('h2')).color,labelColor:getComputedStyle(rows[0].querySelector('.td-attr-k')).color};})())"
echo "  -- 高优先级胶囊（设计稿 52x18 / r4 / #FFECE8 + #F53F3F） --"
$AB eval "JSON.stringify((function(){var t=document.querySelector('.td-tag-prio');if(!t)return{err:'no tag'};var r=t.getBoundingClientRect(),c=getComputedStyle(t);return {size:Math.round(r.width)+'x'+Math.round(r.height),bg:c.backgroundColor,color:c.color,radius:c.borderRadius,fontSize:c.fontSize};})())"

echo ""
echo "=== 5. 拖动到 <100px 自动折叠 + 点击恢复 ==="
gut() { $AB eval "Math.round(document.querySelector('[data-td-gutter]').getBoundingClientRect().left+document.querySelector('[data-td-gutter]').getBoundingClientRect().width/2)"; }
rw()  { $AB eval "Math.round(document.querySelector('.td-right').getBoundingClientRect().width)"; }
cl()  { $AB eval "document.querySelector('.td-root').classList.contains('is-collapsed')"; }
echo "  init      right=$(rw) collapsed=$(cl)"
X=$(gut); $AB mouse move $X 400 >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for x in 1300 1330 1350 1370 1390 1400 1410; do $AB mouse move $x 400 >/dev/null 2>&1; sleep 0.03; done
echo "  拖到 <100px 途中: right=$(rw) collapsed=$(cl)"
$AB mouse up >/dev/null 2>&1; sleep 0.5
echo "  松手后        : right=$(rw) collapsed=$(cl) label=$($AB eval "document.querySelector('.td-collapsed').textContent.replace(/\s/g,'')")"
echo "  折叠条几何    : $($AB eval "JSON.stringify((function(){var r=document.querySelector('.td-right').getBoundingClientRect();return {w:Math.round(r.width),h:Math.round(r.height),x:Math.round(r.left)};})())")"
$AB click ".td-right" >/dev/null 2>&1; sleep 0.5
echo "  点击折叠条后  : right=$(rw) collapsed=$(cl)"

echo ""
echo "=== 6. 布局回归（1440 = 8 + 左 + 8 + 右 + 8） ==="
$AB eval "JSON.stringify((function(){var L=document.querySelector('.td-left').getBoundingClientRect(),R=document.querySelector('.td-right').getBoundingClientRect(),G=document.querySelector('[data-td-gutter]').getBoundingClientRect();return {left:Math.round(L.left)+'~'+Math.round(L.right),leftW:Math.round(L.width),gap:Math.round(G.width),right:Math.round(R.left)+'~'+Math.round(R.right),rightW:Math.round(R.width),sum:Math.round(L.width)+Math.round(G.width)+Math.round(R.width)};})())"
echo "  -- 信息列/main 分栏 --"
$AB eval "JSON.stringify((function(){var m=document.querySelector('.td-main').getBoundingClientRect(),s=document.querySelector('.td-side').getBoundingClientRect();return {main:Math.round(m.width),side:Math.round(s.width),sideLeft:Math.round(s.left),sidePadLeft:getComputedStyle(document.querySelector('.td-side')).paddingLeft};})())"

echo ""
echo "=== 7. 回归：展开 / 顶栏按钮 ==="
echo "  descBody maxH=$($AB eval "getComputedStyle(document.querySelector('.td-desc-body')).maxHeight")"
$AB click "[data-td-desc-toggle]" >/dev/null 2>&1; sleep 0.4
echo "  展开后 maxH=$($AB eval "getComputedStyle(document.querySelector('.td-desc-body')).maxHeight") text=$($AB eval "document.querySelector('[data-td-desc-toggle]').textContent")"
$AB click "[data-td-desc-toggle]" >/dev/null 2>&1; sleep 0.3
$AB eval "JSON.stringify(Array.from(document.querySelectorAll('.td-bar-actions .giencoder-btn')).map(function(b){var r=b.getBoundingClientRect();return (b.getAttribute('aria-label')||b.textContent.trim())+':'+Math.round(r.width)+'x'+Math.round(r.height);}))"

echo ""
echo "=== 8. 截图 ==="
$AB screenshot "mg-work/r24/r24-default.png" >/dev/null 2>&1
echo "  -> mg-work/r24/r24-default.png"

echo ""
echo "=== 9. 容器边缘像素（证明：无描边 + 只有比底色更暗的柔和投影） ==="
$PY - <<'PY'
from PIL import Image
im = Image.open('mg-work/r24/r24-default.png').convert('RGB'); px = im.load()
print('  截图尺寸', im.size)
for tag, y, rng in (('左栏左缘', 400, range(2, 14)), ('右栏右缘', 400, range(1432, 1440))):
    seq = [(x, px[x, y]) for x in rng]
    print('  %s y=%d: %s' % (tag, y, '  '.join('%d:%s' % (x, c) for x, c in seq)))
bg = px[2, 400]
print('  底色 =', bg)
print('  判据: 紧贴容器外侧的像素应比底色**更暗**(投影)，且容器内第一像素=纯白(255,255,255) → 无描边')
for x in (6, 7, 8):
    c = px[x, 400]
    print('    x=%d %s  Δ=%s' % (x, c, tuple(c[i] - bg[i] for i in range(3))))
PY

echo ""
echo "=== 10. 组件合规自检（页面 giencoder-* ∩ (components.css ∪ 契约 anatomy) ） ==="
$PY - <<'PY'
import io, json, re, glob
raw  = io.open('pages/task-detail.html', encoding='utf-8').read()
html = raw.replace('\\"', '"').replace('\\/', '/')
css  = io.open('giencoder-design-system/components.css', encoding='utf-8').read()
defined = set(re.findall(r'\.(giencoder-[A-Za-z0-9_-]+)', css))
# 契约 anatomy 的 element 字段同样是硬约束（DS CSS 未必给每个 part 单写规则）
anatomy = set()
for f in glob.glob('giencoder-design-system/components/*.json'):
    d = json.load(io.open(f, encoding='utf-8'))
    for a in d.get('anatomy', []):
        el = a.get('element', '') or ''
        anatomy |= set(re.findall(r'giencoder-[A-Za-z0-9_-]+', el))
used = set()
for m in re.finditer(r'class="([^"]*)"', html):
    for c in m.group(1).split():
        if c.startswith('giencoder-'): used.add(c)
print('  页面 giencoder-* 类: %d' % len(used))
extra = sorted(used - defined - anatomy)
print('  既不在 components.css 也不在契约 anatomy 的类名:', extra if extra else '无 ✓')
print('  （仅由契约 anatomy 声明、DS CSS 未单写规则）:', sorted((used & anatomy) - defined) or '无')
PY

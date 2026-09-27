#!/usr/bin/env bash
# 第26轮实测：信息列宽度 / 分组间隔线 / 属性行距 / 底部分组一致 / AI全屏 / 消息墨色 / 底行图标
#             + 看板首卡跳转 + 看板悬浮球移除
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.8

echo "=== 1. 信息列 .td-side 宽度减少 5%（280 -> 266）+ 布局回归 ==="
$AB eval "JSON.stringify((function(){var L=document.querySelector('.td-left').getBoundingClientRect(),R=document.querySelector('.td-right').getBoundingClientRect(),S=document.querySelector('.td-side').getBoundingClientRect(),M=document.querySelector('.td-main').getBoundingClientRect(),G=document.querySelector('[data-td-gutter]').getBoundingClientRect();var cs=getComputedStyle(document.querySelector('.td-side'));return {left:Math.round(L.left)+'~'+Math.round(L.right),main:Math.round(M.left)+'~'+Math.round(M.right),side:Math.round(S.left)+'~'+Math.round(S.right),sideW:Math.round(S.width),sideMinToken:cs.minWidth,right:Math.round(R.left)+'~'+Math.round(R.right),gap:Math.round(G.width),scrollW:document.documentElement.scrollWidth+'/'+document.documentElement.clientWidth};})())"

echo ""
echo "=== 2. 任务属性 / 任务动态 之间的间隔线 ==="
$AB eval "JSON.stringify((function(){var s=document.querySelector('.td-side-dyn'),c=getComputedStyle(s),prev=s.previousElementSibling,r=s.getBoundingClientRect(),pr=prev.getBoundingClientRect();return {sectionCls:s.className,borderTop:c.borderTopWidth+' '+c.borderTopStyle+' '+c.borderTopColor,paddingTop:c.paddingTop,gapAboveLine:Math.round(r.top-pr.bottom),lineY:Math.round(r.top),h2TopMinusLine:Math.round(s.querySelector('h2').getBoundingClientRect().top-r.top)};})())"

echo ""
echo "=== 3. .td-attr-row gap = 16px（label 右缘 -> 值左缘） ==="
$AB eval "JSON.stringify((function(){var row=document.querySelector('.td-attr-row');var cs=getComputedStyle(row);var k=row.querySelector('.td-attr-k').getBoundingClientRect(),v=row.querySelector('.td-attr-v').getBoundingClientRect();return {gap:cs.gap,labelRight:Math.round(k.right),valueLeft:Math.round(v.left),measuredGap:Math.round(v.left-k.right)};})())"

echo ""
echo "=== 4. 底部分组（创建者/创建时间/最后更新）与任务属性排列一致 ==="
$AB eval "JSON.stringify((function(){function info(sel){var box=document.querySelector(sel);var rows=box.querySelectorAll('.td-attr-row');var kx=[],vx=[],pitch=[];for(var i=0;i<rows.length;i++){kx.push(Math.round(rows[i].querySelector('.td-attr-k').getBoundingClientRect().left));vx.push(Math.round(rows[i].querySelector('.td-attr-v').getBoundingClientRect().left));}for(var j=1;j<rows.length;j++)pitch.push(Math.round(rows[j].getBoundingClientRect().top-rows[j-1].getBoundingClientRect().top));return {n:rows.length,kW:getComputedStyle(rows[0].querySelector('.td-attr-k')).width,rowH:getComputedStyle(rows[0]).height,kx:kx,vx:vx,vxSpread:Math.max.apply(null,vx)-Math.min.apply(null,vx),pitch:pitch};}return {attr:info('.td-side-attr'),foot:info('.td-side-foot')};})())"

echo ""
echo "=== 5. AI 对话框全屏 / 取消全屏 ==="
echo "  点击前: $($AB eval "JSON.stringify((function(){var r=document.querySelector('.td-right').getBoundingClientRect();return {left:Math.round(r.left),w:Math.round(r.width),fs:document.querySelector('.td-root').classList.contains('is-fullscreen'),label:document.querySelector('[data-td-fullscreen]').getAttribute('aria-label')};})())")"
$AB click "[data-td-fullscreen]" >/dev/null 2>&1; sleep 0.5
echo "  全屏后: $($AB eval "JSON.stringify((function(){var r=document.querySelector('.td-right').getBoundingClientRect(),b=document.querySelector('[data-td-fullscreen]');return {left:Math.round(r.left),w:Math.round(r.width),right:Math.round(r.right),fs:document.querySelector('.td-root').classList.contains('is-fullscreen'),label:b.getAttribute('aria-label'),pressed:b.getAttribute('aria-pressed'),leftCol:getComputedStyle(document.querySelector('.td-left')).display,gutter:getComputedStyle(document.querySelector('[data-td-gutter]')).display,icoMax:getComputedStyle(document.querySelector('.td-ico-max')).display,icoMin:getComputedStyle(document.querySelector('.td-ico-min')).display};})())")"
$AB screenshot "mg-work/r26/r26-fullscreen.png" >/dev/null 2>&1
$AB click "[data-td-fullscreen]" >/dev/null 2>&1; sleep 0.5
echo "  取消全屏: $($AB eval "JSON.stringify((function(){var r=document.querySelector('.td-right').getBoundingClientRect(),b=document.querySelector('[data-td-fullscreen]');return {left:Math.round(r.left),w:Math.round(r.width),fs:document.querySelector('.td-root').classList.contains('is-fullscreen'),label:b.getAttribute('aria-label'),leftCol:getComputedStyle(document.querySelector('.td-left')).display};})())")"
$AB click "[data-td-fullscreen]" >/dev/null 2>&1; sleep 0.4
$AB eval "document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));1" >/dev/null 2>&1; sleep 0.4
echo "  全屏后按 Esc: $($AB eval "JSON.stringify({fs:document.querySelector('.td-root').classList.contains('is-fullscreen'),path:location.pathname.split('/').pop()})")"

echo ""
echo "=== 6. .td-msg-ai p 墨色 ==="
$AB eval "JSON.stringify((function(){var ps=document.querySelectorAll('.td-msg-ai p');return {n:ps.length,colors:[].map.call(ps,function(p){return getComputedStyle(p).color}),text1:getComputedStyle(document.documentElement).getPropertyValue('--color-text-1').trim()};})())"

echo ""
echo "=== 7. AI 底行图标（输出完成 / Token 速率） ==="
$AB eval "JSON.stringify((function(){var f=document.querySelector('.td-ai-foot');var icos=f.querySelectorAll('.td-ai-foot-ico');var out=[].map.call(icos,function(s){var r=s.getBoundingClientRect();return {w:Math.round(r.width),h:Math.round(r.height),color:getComputedStyle(s).color,svg:!!s.querySelector('svg')};});var chk=f.querySelector('.td-ico-check');return {icons:out,order:[].map.call(f.children,function(c){return (c.className||c.tagName)+'='+c.textContent.slice(0,8)}),checkStroke:chk?getComputedStyle(chk).stroke:null,rowH:Math.round(f.getBoundingClientRect().height)};})())"

echo ""
echo "=== 8. 回归：拖动折叠 / 展开收起 ==="
gut() { $AB eval "Math.round(document.querySelector('[data-td-gutter]').getBoundingClientRect().left+document.querySelector('[data-td-gutter]').getBoundingClientRect().width/2)"; }
rw()  { $AB eval "Math.round(document.querySelector('.td-right').getBoundingClientRect().width)"; }
X=$(gut); $AB mouse move $X 400 >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for x in 1300 1360 1400 1424 1430; do $AB mouse move $x 400 >/dev/null 2>&1; sleep 0.03; done
$AB mouse up >/dev/null 2>&1; sleep 0.4
echo "  拖<100px -> right=$(rw) collapsed=$($AB eval "document.querySelector('.td-root').classList.contains('is-collapsed')")"
$AB click ".td-right" >/dev/null 2>&1; sleep 0.5
echo "  点击恢复 -> right=$(rw)"
$AB eval "(function(){var b=document.querySelector('.td-desc-body');var btn=document.querySelector('[data-td-desc-toggle]');window.__h=[];var t0=performance.now();setTimeout(function(){btn.click();},80);function tick(){window.__h.push([Math.round(performance.now()-t0),Math.round(b.getBoundingClientRect().height)]);if(performance.now()-t0<640)requestAnimationFrame(tick);}tick();return 1;})()" >/dev/null 2>&1; sleep 1.0
echo "  展开判定 = $($AB eval "JSON.stringify((function(){var a=window.__h.map(function(v){return v[1];});var u=a.filter(function(v,i){return i===0||v!==a[i-1];});return {min:Math.min.apply(null,a),max:Math.max.apply(null,a),distinct:u.length};})())")"

$AB eval "window.scrollTo(0,0);1" >/dev/null 2>&1
$AB screenshot "mg-work/r26/r26-default.png" >/dev/null 2>&1
echo "  截图 -> mg-work/r26/r26-default.png"

echo ""
echo "=== 9. 组件合规自检 ==="
$PY - <<'PY'
import io, json, re, glob
raw  = io.open('pages/task-detail.html', encoding='utf-8').read()
html = raw.replace('\\"', '"').replace('\\/', '/')
css  = io.open('giencoder-design-system/components.css', encoding='utf-8').read()
defined = set(re.findall(r'\.(giencoder-[A-Za-z0-9_-]+)', css))
anatomy = set()
for f in glob.glob('giencoder-design-system/components/*.json'):
    d = json.load(io.open(f, encoding='utf-8'))
    for a in d.get('anatomy', []):
        anatomy |= set(re.findall(r'giencoder-[A-Za-z0-9_-]+', a.get('element', '') or ''))
used = set()
for m in re.finditer(r'class="([^"]*)"', html):
    for c in m.group(1).split():
        if c.startswith('giencoder-'): used.add(c)
extra = sorted(used - defined - anatomy)
print('  页面 giencoder-* 类: %d' % len(used))
print('  虚构类名:', extra if extra else '无 ✓')
PY

#!/usr/bin/env bash
# 第25轮实测：正文墨色 / 信息列字号统一14px(除td-tl-time) / 顶栏页签可点击 / 展开收起微动效
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.8

echo "=== 1. 描述区正文墨色（应 = 最深一级 --color-text-1 #1F1F1F） ==="
$AB eval "JSON.stringify((function(){var d=document.querySelector('.td-desc');var p=d.querySelector('p');var li=d.querySelector('li');var cs=getComputedStyle(li,'::before');return {descColor:getComputedStyle(d).color,pColor:getComputedStyle(p).color,liColor:getComputedStyle(li).color,markerBg:cs.backgroundColor,titleColor:getComputedStyle(document.querySelector('.td-title')).color,attrVColor:getComputedStyle(document.querySelector('.td-attr-v')).color};})())"
echo "  -- 与 token 对账 --"
$AB eval "JSON.stringify((function(){var s=getComputedStyle(document.documentElement);return {text1:s.getPropertyValue('--color-text-1').trim(),text2:s.getPropertyValue('--color-text-2').trim(),body3:s.getPropertyValue('--font-size-body-3').trim(),body1:s.getPropertyValue('--font-size-body-1').trim()};})())"

echo ""
echo "=== 2. 左栏 aside 字号普查（正文应全 14px，td-tl-time 保持 12px） ==="
$AB eval "JSON.stringify((function(){var side=document.querySelector('.td-side');var out={};side.querySelectorAll('*').forEach(function(el){var hasText=Array.prototype.some.call(el.childNodes,function(n){return n.nodeType===3&&n.textContent.trim();});if(!hasText)return;var fs=getComputedStyle(el).fontSize;var nm=el.tagName.toLowerCase()+'.'+String(el.className).split(' ').filter(Boolean).slice(0,2).join('.');var k=nm+'  @'+fs;out[k]=(out[k]||0)+1;});return out;})())"
echo "  -- 关键类点测 --"
$AB eval "JSON.stringify({'h2':getComputedStyle(document.querySelector('.td-side h2')).fontSize,'.td-attr-row':getComputedStyle(document.querySelector('.td-attr-row')).fontSize,'.td-attr-k':getComputedStyle(document.querySelector('.td-attr-k')).fontSize,'.td-attr-v':getComputedStyle(document.querySelector('.td-attr-v')).fontSize,'.td-tl-line1':getComputedStyle(document.querySelector('.td-tl-line1')).fontSize,'.td-tl-who':getComputedStyle(document.querySelector('.td-tl-who')).fontSize,'.td-tl-what':getComputedStyle(document.querySelector('.td-tl-what')).fontSize,'.td-tl-time':getComputedStyle(document.querySelector('.td-tl-time')).fontSize,'badge-status-text':getComputedStyle(document.querySelector('.giencoder-badge-status-text')).fontSize,'tag-prio':getComputedStyle(document.querySelector('.td-tag-prio')).fontSize})"
echo "  -- 任务属性行距 / 值列对齐（第24轮回归） --"
$AB eval "JSON.stringify((function(){var s=document.querySelector('.td-side-attr');var r=s.querySelectorAll('.td-attr-row');var lx=Array.from(r).map(function(x){return Math.round(x.querySelector('.td-attr-k').getBoundingClientRect().left);});var vx=Array.from(r).map(function(x){return Math.round(x.querySelector('.td-attr-v').getBoundingClientRect().left);});var pitch=[];for(var i=1;i<r.length;i++)pitch.push(Math.round(r[i].getBoundingClientRect().top-r[i-1].getBoundingClientRect().top));return {labelW:getComputedStyle(r[0].querySelector('.td-attr-k')).width,labelX:lx,valueX:vx,valueXSpread:Math.max.apply(null,vx)-Math.min.apply(null,vx),pitch:pitch};})())"
echo "  -- 高优先级 Tag（14px 后尺寸） --"
$AB eval "JSON.stringify((function(){var t=document.querySelector('.td-tag-prio');var r=t.getBoundingClientRect();return {size:Math.round(r.width)+'x'+Math.round(r.height),bg:getComputedStyle(t).backgroundColor,color:getComputedStyle(t).color};})())"

echo ""
echo "=== 3. 展开全文 / 收起 微动效（max-height 过渡，非瞬变） ==="
echo "  transition = $($AB eval "getComputedStyle(document.querySelector('.td-desc-body')).transition")"
echo "  限高       = $($AB eval "getComputedStyle(document.querySelector('.td-desc-body')).maxHeight")"
# 采样与点击必须同一次 eval 内完成（两次 eval 之间隔着 HTTP 往返，采样窗口会错过点击）
sample() { $AB eval "(function(){var b=document.querySelector('.td-desc-body');var btn=document.querySelector('[data-td-desc-toggle]');window.__h=[];var t0=performance.now();setTimeout(function(){btn.click();},80);function tick(){window.__h.push([Math.round(performance.now()-t0),Math.round(b.getBoundingClientRect().height)]);if(performance.now()-t0<640)requestAnimationFrame(tick);}tick();return 1;})()" >/dev/null 2>&1; }
sample; sleep 1.0
echo "  展开采样(ms:px) = $($AB eval "JSON.stringify(window.__h.filter(function(v,i){return i%5===0;}))")"
echo "  展开判定 = $($AB eval "JSON.stringify((function(){var a=window.__h.map(function(v){return v[1];});var u=a.filter(function(v,i){return i===0||v!==a[i-1];});return {min:Math.min.apply(null,a),max:Math.max.apply(null,a),distinct:u.length,animating:u.length>2};})())")"
echo "  展开后 text=$($AB eval "document.querySelector('[data-td-desc-toggle]').textContent") aria=$($AB eval "document.querySelector('[data-td-desc-toggle]').getAttribute('aria-expanded')") maxH=$($AB eval "getComputedStyle(document.querySelector('.td-desc-body')).maxHeight")"
sample; sleep 1.0
echo "  收起采样(ms:px) = $($AB eval "JSON.stringify(window.__h.filter(function(v,i){return i%5===0;}))")"
echo "  收起判定 = $($AB eval "JSON.stringify((function(){var a=window.__h.map(function(v){return v[1];});var u=a.filter(function(v,i){return i===0||v!==a[i-1];});return {min:Math.min.apply(null,a),max:Math.max.apply(null,a),distinct:u.length,animating:u.length>2};})())")"
echo "  收起后 text=$($AB eval "document.querySelector('[data-td-desc-toggle]').textContent") maxH=$($AB eval "getComputedStyle(document.querySelector('.td-desc-body')).maxHeight") 内联=$($AB eval "document.getElementById('td-desc-body').style.maxHeight||'(空)'")"

echo ""
echo "=== 4. 回归：布局 / 折叠 / 容器边缘 ==="
$AB eval "JSON.stringify((function(){var L=document.querySelector('.td-left').getBoundingClientRect(),R=document.querySelector('.td-right').getBoundingClientRect(),G=document.querySelector('[data-td-gutter]').getBoundingClientRect();var c=getComputedStyle(document.querySelector('.td-left'));return {left:Math.round(L.left)+'~'+Math.round(L.right),right:Math.round(R.left)+'~'+Math.round(R.right),gap:Math.round(G.width),border:c.borderTopWidth,shadow:c.boxShadow,sideBd:getComputedStyle(document.querySelector('.td-side')).borderLeftColor};})())"
gut() { $AB eval "Math.round(document.querySelector('[data-td-gutter]').getBoundingClientRect().left+document.querySelector('[data-td-gutter]').getBoundingClientRect().width/2)"; }
rw()  { $AB eval "Math.round(document.querySelector('.td-right').getBoundingClientRect().width)"; }
X=$(gut); $AB mouse move $X 400 >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for x in 1300 1350 1390 1410 1424; do $AB mouse move $x 400 >/dev/null 2>&1; sleep 0.03; done
$AB mouse up >/dev/null 2>&1; sleep 0.4
echo "  拖<100px -> right=$(rw) collapsed=$($AB eval "document.querySelector('.td-root').classList.contains('is-collapsed')")"
$AB click ".td-right" >/dev/null 2>&1; sleep 0.5
echo "  点击恢复 -> right=$(rw)"

$AB eval "document.querySelector('.td-desc-body')&&0;window.scrollTo(0,0);1" >/dev/null 2>&1
$AB screenshot "mg-work/r25/r25-default.png" >/dev/null 2>&1
echo "  截图 -> mg-work/r25/r25-default.png"

echo ""
echo "=== 5. 顶栏页签可点击（公共片段 SHELL-TABS-FIX） ==="
echo "  片段已注入 = $($AB eval "document.documentElement.outerHTML.includes('SHELL-TABS-FIX')")"
echo "  片段版本   = $($AB eval "(document.documentElement.outerHTML.match(/SHELL-TABS-FIX v[0-9]+/)||['缺失'])[0]")"
echo "  页签高亮   = $($AB eval "JSON.stringify([].map.call(document.querySelectorAll('[role=\"tablist\"][aria-label=\"工作台切换\"] [data-tab]'),function(b){return b.getAttribute('data-tab')+'|sel='+b.getAttribute('aria-selected')+'|svg='+(b.querySelector('svg')?1:0)+'|'+b.textContent}))")"
$AB eval "document.querySelectorAll('[data-tab]')[1].click();1" >/dev/null 2>&1; sleep 0.6
echo "  点「研发工作台」(当前分组) -> 停留=$($AB eval "location.pathname")"
$AB click "[data-tab='base']" >/dev/null 2>&1; sleep 1.2
echo "  点「基础工作台」 -> location=$($AB eval "location.pathname")  title=$($AB eval "document.title")"
$AB open "$URL" >/dev/null 2>&1; sleep 2.2
echo "  回到详情页 -> $($AB eval "location.pathname")  有 td-root=$($AB eval "!!document.querySelector('.td-root')")"

echo ""
echo "=== 6. 组件合规自检 ==="
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

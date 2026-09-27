#!/usr/bin/env bash
# 第27轮实测：
#   1) 2个附件 / 3个 AI 产物 / 文件 三处分组标题图标（回形针 / 文件夹 / 文件夹）
#   2) 「输出完成」图标 ↔ 文字 间距减半（8 -> 4）
#   3) .td-attr-link 来源需求链接显示更多文字
#   4) 任务看板三标签（拆分需求项 / 拆分需求条目 / 拆分子条目）配色对比设计稿
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"
KBURL="http://127.0.0.1:8866/pages/kanban.html"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.8

echo "=== 1. 三处分组标题图标 ==="
$AB eval "JSON.stringify((function(){var hs=document.querySelectorAll('.td-sec-head');var out=[];for(var i=0;i<hs.length;i++){var h=hs[i],sv=h.querySelector('svg');var r=sv.getBoundingClientRect(),t=document.createElement('span');var rng=document.createRange();var first=h.childNodes[0];rng.selectNodeContents(h);var rects=[];var walker=document.createTreeWalker(h,NodeFilter.SHOW_TEXT);var tn=walker.nextNode();var tr=tn.parentNode.getBoundingClientRect();out.push({head:h.textContent.trim(),svgW:Math.round(r.width),svgH:Math.round(r.height),d:sv.querySelector('path')?sv.querySelector('path').getAttribute('d'):null,color:getComputedStyle(sv).color,pathN:sv.querySelectorAll('path').length,gapIconText:Math.round(tr.left-r.right)});}return out;})())"

echo ""
echo "=== 2. 「输出完成」图标 ↔ 文字 间距 ==="
$AB eval "JSON.stringify((function(){var f=document.querySelector('.td-ai-foot');var items=f.querySelectorAll('.td-ai-foot-item');var out=[];for(var i=0;i<items.length;i++){var it=items[i];var ico=it.querySelector('.td-ai-foot-ico');var txt=it.querySelector('span:last-child');var ir=ico.getBoundingClientRect(),tr=txt.getBoundingClientRect();out.push({gap:getComputedStyle(it).gap,iconRight:Math.round(ir.right),textLeft:Math.round(tr.left),measured:Math.round(tr.left-ir.right),label:txt.textContent});}return {outerGap:getComputedStyle(f).gap,items:out,sepW:Math.round(f.querySelector('.td-sep').getBoundingClientRect().width)};})())"

echo ""
echo "=== 3. .td-attr-link 显示更多文字 ==="
$AB eval "JSON.stringify((function(){var row=document.querySelector('.td-attr-row.is-wrap');var a=row.querySelector('.td-attr-link');var v=row.querySelector('.td-attr-v');var cs=getComputedStyle(v);var lh=parseFloat(cs.lineHeight)||20;return {rowCls:row.className,text:a.textContent,chars:a.textContent.length,hasEllipsis:a.textContent.indexOf('…')>=0,aW:Math.round(a.getBoundingClientRect().width),vW:Math.round(v.getBoundingClientRect().width),vH:Math.round(v.getBoundingClientRect().height),lines:Math.round(v.getBoundingClientRect().height/lh),overflow:Math.round(a.scrollWidth-v.clientWidth),whiteSpace:cs.whiteSpace,lineClamp:cs.webkitLineClamp,iconFirst:!!a.querySelector('svg'),alignItems:getComputedStyle(row).alignItems,labelTop:Math.round(row.querySelector('.td-attr-k').getBoundingClientRect().top),valueTop:Math.round(v.getBoundingClientRect().top)};})())"

echo ""
echo "=== 3b. 其余属性行未被误伤（单行仍未折行） ==="
$AB eval "JSON.stringify((function(){var rows=document.querySelectorAll('.td-side .td-attr-row');var wrapN=document.querySelectorAll('.td-side .td-attr-row.is-wrap').length;var h=[];for(var i=0;i<rows.length;i++)h.push(Math.round(rows[i].getBoundingClientRect().height));return {total:rows.length,wrapN:wrapN,heights:h};})())"
$AB screenshot "mg-work/r27/verify-side.png" >/dev/null 2>&1

echo ""
echo "=== 4. 任务看板三标签配色（设计稿对比） ==="
$AB open "$KBURL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.8
$AB eval "JSON.stringify((function(){var want={'拆分需求项':1,'拆分需求条目':1,'拆分子条目':1};var ts=document.querySelectorAll('.kb-tag');var seen={};for(var i=0;i<ts.length;i++){var t=ts[i],k=t.textContent.trim();if(!want[k]||seen[k])continue;seen[k]=1;var c=getComputedStyle(t);seen[k]={cls:t.className,bg:c.backgroundColor,color:c.color,fs:c.fontSize,pad:c.padding,radius:c.borderRadius,w:Math.round(t.getBoundingClientRect().width),h:Math.round(t.getBoundingClientRect().height)};}return seen;})())"
$AB screenshot "mg-work/r27/verify-kanban.png" >/dev/null 2>&1

echo ""
echo "=== 5. 详情页回归：布局 / 语法 ==="
$AB open "$URL" >/dev/null 2>&1
sleep 2.5
$AB eval "JSON.stringify((function(){var S=document.querySelector('.td-side').getBoundingClientRect(),R=document.querySelector('.td-right').getBoundingClientRect();return {sideW:Math.round(S.width),rightL:Math.round(R.left),rightW:Math.round(R.width),scrollW:document.documentElement.scrollWidth+'/'+document.documentElement.clientWidth};})())"
$PY mg-work/kanban/r13/check-syntax.py pages/task-detail.html 2>&1 | tail -2

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

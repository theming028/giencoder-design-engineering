#!/usr/bin/env bash
# 第28轮实测（7 项）：
#   1) 左栏/右栏 按住标题栏左右拖动互换位置
#   2) .td-desc 插入合适尺寸的图片
#   3) .td-attr-link hover 变主题蓝
#   4) 右栏 AI 对话框底部「添加 / 技能 / 选择大模型」的点击交互（对齐基础工作台）
#   5) .td-ai-file 卡片样式对齐设计稿
#   6) 2个附件 / 3个AI产物 / 文件 下属卡片图标对齐设计稿
#   7) .giencoder-tag-content 字号 = 12px
# 注意：agent-browser 的 session 不跨 bash 调用 → 全部命令必须在一次调用里跑完。
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0

echo "=== 0. 基线：布局未被破坏 ==="
$AB eval "JSON.stringify((function(){var S=document.querySelector('.td-side').getBoundingClientRect();var L=document.querySelector('.td-left').getBoundingClientRect();var R=document.querySelector('.td-right').getBoundingClientRect();return {sideW:Math.round(S.width),leftL:Math.round(L.left),leftW:Math.round(L.width),rightL:Math.round(R.left),rightW:Math.round(R.width),scroll:document.documentElement.scrollWidth+'/'+document.documentElement.clientWidth};})())"

echo ""
echo "=== 7. giencoder-tag-content 字号 ==="
$AB eval "JSON.stringify((function(){var t=document.querySelector('.td-tag-prio');var c=t.querySelector('.giencoder-tag-content');var cs=getComputedStyle(c),ts=getComputedStyle(t);return {tagCls:t.className,contentFs:cs.fontSize,tagFs:ts.fontSize,contentLh:cs.lineHeight,box:Math.round(t.getBoundingClientRect().width)+'x'+Math.round(t.getBoundingClientRect().height)};})())"

echo ""
echo "=== 3. .td-attr-link hover 变主题蓝 ==="
$AB eval "JSON.stringify((function(){var a=document.querySelector('.td-attr-link');var s=a.querySelector('svg');return {before:{color:getComputedStyle(a).color,iconColor:getComputedStyle(s).color,textDecoration:getComputedStyle(a).textDecorationLine}};})())"
$AB hover ".td-attr-link" >/dev/null 2>&1
sleep 0.4
$AB eval "JSON.stringify((function(){var a=document.querySelector('.td-attr-link');var s=a.querySelector('svg');return {after:{color:getComputedStyle(a).color,iconColor:getComputedStyle(s).color,primary6:getComputedStyle(document.documentElement).getPropertyValue('--color-primary-6').trim()}};})())"

echo ""
echo "=== 6. 卡片图标 / 分隔线（附件 / AI 产物 / 文件） ==="
$AB eval "JSON.stringify((function(){var out=[];var cards=document.querySelectorAll('.td-file');for(var i=0;i<cards.length;i++){var c=cards[i],ico=c.querySelector('.td-file-ico'),sv=ico?ico.querySelector('svg'):null,sep=c.querySelector('.td-file-sep');var r=c.getBoundingClientRect(),ir=ico?ico.getBoundingClientRect():null;out.push({name:(c.querySelector('.td-file-tx')||{}).textContent,big:c.className.indexOf('td-file--lg')>=0,h:Math.round(r.height),w:Math.round(r.width),radius:getComputedStyle(c).borderRadius,icoBox:ir?Math.round(ir.width)+'x'+Math.round(ir.height):null,icoLeft:ir?Math.round(ir.left-r.left):null,icoCls:ico?ico.className:null,icoColor:ico?getComputedStyle(ico).color:null,shapes:sv?sv.querySelectorAll('path,circle,ellipse').length:null,sep:sep?Math.round(sep.getBoundingClientRect().width)+'x'+Math.round(sep.getBoundingClientRect().height):null,sepColor:sep?getComputedStyle(sep).backgroundColor:null,sepLeft:sep?Math.round(sep.getBoundingClientRect().left-r.left):null});}return {cards:out};})())"
echo "--- 6b. 图标实际着墨尺寸（渲染盒 vs 笔画） ---"
$AB eval "JSON.stringify((function(){var out=[];var icos=document.querySelectorAll('.td-file-ico, .td-ai-file .td-file-ico');for(var i=0;i<icos.length;i++){var sv=icos[i].querySelector('svg');var vb=sv.getAttribute('viewBox');var b=sv.getBoundingClientRect();out.push({cls:icos[i].className,vb:vb,render:Math.round(b.width)+'x'+Math.round(b.height)});}return out;})())"

echo ""
echo "=== 5. AI 消息文件卡 ==="
$AB eval "JSON.stringify((function(){var ai=document.querySelector('.td-ai-file');var r=ai.getBoundingClientRect();var parts={};var sel=['.td-file-ico','.td-file-sep','.td-file-tx','.td-file-size'];for(var i=0;i<sel.length;i++){var e=ai.querySelector(sel[i]);var b=e.getBoundingClientRect();parts[sel[i]]={box:Math.round(b.width)+'x'+Math.round(b.height),left:Math.round(b.left-r.left),top:Math.round(b.top-r.top),color:getComputedStyle(e).color,bg:getComputedStyle(e).backgroundColor,fs:getComputedStyle(e).fontSize,fw:getComputedStyle(e).fontWeight};}var body=ai.querySelector('.td-file-body');return {card:{box:Math.round(r.width)+'x'+Math.round(r.height),radius:getComputedStyle(ai).borderRadius,bg:getComputedStyle(ai).backgroundColor,gap:getComputedStyle(ai).gap},bodyDisplay:getComputedStyle(body).display,bodyDir:getComputedStyle(body).flexDirection,parts:parts};})())"

echo ""
echo "=== 2. .td-desc 配图 ==="
$AB eval "JSON.stringify((function(){var im=document.querySelector('.td-desc img');var db=document.querySelector('.td-desc-body');var r=im?im.getBoundingClientRect():null;var br=db.getBoundingClientRect();return {exists:!!im,src:im?im.getAttribute('src').slice(0,40):null,natural:im?im.naturalWidth+'x'+im.naturalHeight:null,box:r?Math.round(r.width)+'x'+Math.round(r.height):null,radius:im?getComputedStyle(im).borderRadius:null,imgBottomInBody:r?Math.round(r.bottom-br.top):null,bodyCollapsedH:Math.round(br.height),maxH:getComputedStyle(db).maxHeight,fullyVisibleInCollapsed:r?(r.bottom-br.top)<=374:null};})())"
$AB screenshot "mg-work/r28/verify-desc.png" >/dev/null 2>&1

echo ""
echo "=== 4. 对话框三个弹层的交互 ==="
echo "--- 4a. 点「添加」 ---"
$AB click "[data-td-add-btn]" >/dev/null 2>&1
sleep 0.35
$AB eval "JSON.stringify((function(){var p=document.querySelector('[data-td-add-pop]');var r=p.getBoundingClientRect();var btn=document.querySelector('[data-td-add-btn]');return {hidden:p.hidden,box:Math.round(r.width)+'x'+Math.round(r.height),radius:getComputedStyle(p).borderRadius,items:p.querySelectorAll('[role=menuitem]').length,seps:p.querySelectorAll('.td-add-sep').length,labels:[].map.call(p.querySelectorAll('[role=menuitem] span'),function(s){return s.textContent;}),aria:btn.getAttribute('aria-expanded'),gapAboveBtn:Math.round(r.bottom-btn.getBoundingClientRect().top)};})())"
echo "--- 4b. 点菜单项 → 只关闭 ---"
$AB click ".td-add-item" >/dev/null 2>&1
sleep 0.3
$AB eval "JSON.stringify((function(){var p=document.querySelector('[data-td-add-pop]');var ta=document.querySelector('.td-composer textarea');return {hiddenAfterItemClick:p.hidden,textareaUntouched:ta.value==='',aria:document.querySelector('[data-td-add-btn]').getAttribute('aria-expanded')};})())"

echo "--- 4c. 点「技能」 → 面板 ---"
$AB click "[data-td-skill-btn]" >/dev/null 2>&1
sleep 0.4
$AB eval "JSON.stringify((function(){var p=document.querySelector('[data-td-skill-pop]');var r=p.getBoundingClientRect();var comp=document.querySelector('.td-composer > div').getBoundingClientRect();return {hidden:p.hidden,box:Math.round(r.width)+'x'+Math.round(r.height),radius:getComputedStyle(p).borderRadius,rows:p.querySelectorAll('.td-skill-row').length,groups:p.querySelectorAll('.td-skill-group').length,tags:[].map.call(p.querySelectorAll('.td-skill-tag'),function(s){return s.textContent;}),goalActive:!!p.querySelector('.td-skill-row.is-active'),goalPurple:getComputedStyle(p.querySelector('.td-skill-ico.is-goal')).color,buttons:p.querySelectorAll('.td-skill-foot .giencoder-btn').length,withinComposer:r.left>=comp.left-1&&r.right<=comp.right+1,aria:document.querySelector('[data-td-skill-btn]').getAttribute('aria-expanded')};})())"
$AB screenshot "mg-work/r28/verify-skillpop.png" >/dev/null 2>&1
echo "--- 4d. 点技能行 → 只关闭 ---"
$AB click ".td-skill-row" >/dev/null 2>&1
sleep 0.3
$AB eval "JSON.stringify((function(){return {hiddenAfterRowClick:document.querySelector('[data-td-skill-pop]').hidden};})())"

echo "--- 4e. 大模型下拉（DS 契约：开合唯一开关 = .giencoder-popup-open）---"
# ⚠️ 第 28 轮踩坑修正：DS 的 gienx-templates/ui-controls.css 给 .giencoder-select-popup 设了
#    opacity:0 / visibility:hidden，加 .giencoder-popup-open 才可见。
#    所以断言必须看 class + visibility + opacity，**不能只看 display**（display 恒为 block）。
#    另：技能面板自身也带 .giencoder-select 类，须按「内部含 .giencoder-select-view-text」过滤。
M="[].slice.call(document.querySelectorAll('.td-composer .giencoder-select')).filter(function(e){return e.querySelector('.giencoder-select-view-text');})"
$AB eval "JSON.stringify((function(){var s=$M;var m=s[s.length-1];var p=m.querySelector('.giencoder-select-popup');return {openBefore:p.classList.contains('giencoder-popup-open'),visBefore:getComputedStyle(p).visibility,options:m.querySelectorAll('.giencoder-select-option').length,disabled:m.querySelectorAll('.giencoder-select-option-disabled').length,text:m.querySelector('.giencoder-select-view-text').textContent};})())"
$AB eval "(function(){var s=$M;s[s.length-1].querySelector('.giencoder-select-view').click();})()" >/dev/null 2>&1
sleep 0.5
$AB eval "JSON.stringify((function(){var s=$M;var m=s[s.length-1];var p=m.querySelector('.giencoder-select-popup');var cs=getComputedStyle(p);var b=p.getBoundingClientRect();var h=document.elementFromPoint(Math.round(b.left+b.width/2),Math.round(b.top+14));return {open:p.classList.contains('giencoder-popup-open'),vis:cs.visibility,opacity:cs.opacity,rect:[Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)],inViewport:b.bottom<=innerHeight,hitInPopup:!!(h&&h.closest&&h.closest('.giencoder-select-popup')),aria:m.querySelector('.giencoder-select-view').getAttribute('aria-expanded'),popFlag:document.documentElement.hasAttribute('data-td-pop-open')};})())"
echo "--- 4f. 选中第 2 项 → 文案回写 + 关闭 ---"
$AB eval "(function(){var s=$M;s[s.length-1].querySelectorAll('.giencoder-select-option')[1].click();})()" >/dev/null 2>&1
sleep 0.4
$AB eval "JSON.stringify((function(){var s=$M;var m=s[s.length-1];var p=m.querySelector('.giencoder-select-popup');return {textAfter:m.querySelector('.giencoder-select-view-text').textContent,selected:[].map.call(m.querySelectorAll('.giencoder-select-option-selected'),function(o){return o.textContent;}),open:p.classList.contains('giencoder-popup-open'),vis:getComputedStyle(p).visibility,popFlag:document.documentElement.hasAttribute('data-td-pop-open')};})())"

echo "--- 4g. 外部点击关闭 ---"
$AB click "[data-td-skill-btn]" >/dev/null 2>&1
sleep 0.35
$AB eval "(function(){document.querySelector('.td-right-bar').click();})()" >/dev/null 2>&1
sleep 0.3
$AB eval "JSON.stringify((function(){return {hiddenAfterOutsideClick:document.querySelector('[data-td-skill-pop]').hidden,popFlag:document.documentElement.hasAttribute('data-td-pop-open')};})())"

echo "--- 4h. Esc 关弹层且不跳转 ---"
$AB click "[data-td-skill-btn]" >/dev/null 2>&1
sleep 0.35
$AB press Escape >/dev/null 2>&1
sleep 0.4
$AB eval "JSON.stringify((function(){return {url:location.pathname.split('/').pop(),hiddenAfterEsc:document.querySelector('[data-td-skill-pop]').hidden,popFlag:document.documentElement.hasAttribute('data-td-pop-open')};})())"

echo ""
echo "=== 1. 标题栏拖动互换两栏 ==="
INFO=$($AB eval "JSON.stringify((function(){var b=document.querySelector('.td-bar').getBoundingClientRect();var L=document.querySelector('.td-left').getBoundingClientRect();var R=document.querySelector('.td-right').getBoundingClientRect();return {gx:Math.round(b.left+140),gy:Math.round(b.top+24),leftL:Math.round(L.left),rightL:Math.round(R.left),cls:document.querySelector('.td-root').className};})())" 2>&1 | tail -1)
echo "before: $INFO"
XY=$(echo "$INFO" | $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")
X=$(echo $XY | cut -d' ' -f1); Y=$(echo $XY | cut -d' ' -f2)
$AB mouse move "$X" "$Y" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
for dx in 15 35 55 75 95 120 140; do $AB mouse move "$((X+dx))" "$Y" >/dev/null 2>&1; done
sleep 0.2
$AB eval "JSON.stringify((function(){var r=document.querySelector('.td-root');return {duringDragCls:r.className};})())"
$AB mouse up >/dev/null 2>&1
sleep 0.5
$AB eval "JSON.stringify((function(){var L=document.querySelector('.td-left').getBoundingClientRect();var R=document.querySelector('.td-right').getBoundingClientRect();var r=document.querySelector('.td-root');return {rootCls:r.className,flexDir:getComputedStyle(r).flexDirection,leftL:Math.round(L.left),rightL:Math.round(R.left),swapped_rightIsLeft:R.left<L.left};})())"
$AB screenshot "mg-work/r28/verify-swapped.png" >/dev/null 2>&1

echo "--- 1b. 再拖回（此时 .td-bar 已在右侧，向左拖 → 复原） ---"
INFO2=$($AB eval "JSON.stringify((function(){var b=document.querySelector('.td-bar').getBoundingClientRect();return {gx:Math.round(b.left+140),gy:Math.round(b.top+24)};})())" 2>&1 | tail -1)
XY2=$(echo "$INFO2" | $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")
X2=$(echo $XY2 | cut -d' ' -f1); Y2=$(echo $XY2 | cut -d' ' -f2)
$AB mouse move "$X2" "$Y2" >/dev/null 2>&1
$AB mouse down >/dev/null 2>&1
for dx in 15 35 55 75 95 120 140; do $AB mouse move "$((X2-dx))" "$Y2" >/dev/null 2>&1; done
$AB mouse up >/dev/null 2>&1
sleep 0.5
$AB eval "JSON.stringify((function(){var L=document.querySelector('.td-left').getBoundingClientRect();var R=document.querySelector('.td-right').getBoundingClientRect();var r=document.querySelector('.td-root');return {rootCls:r.className,leftL:Math.round(L.left),rightL:Math.round(R.left),restored:R.left>L.left};})())"

echo ""
echo "--- 1c. 交换后拖动条方向取反（向右拖 → 右栏变宽） ---"
INFO3=$($AB eval "JSON.stringify((function(){var b=document.querySelector('.td-bar').getBoundingClientRect();return {gx:Math.round(b.left+140),gy:Math.round(b.top+24)};})())" 2>&1 | tail -1)
XY3=$(echo "$INFO3" | $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")
X3=$(echo $XY3 | cut -d' ' -f1); Y3=$(echo $XY3 | cut -d' ' -f2)
$AB mouse move "$X3" "$Y3" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for dx in 15 35 55 75 95 120 140; do $AB mouse move "$((X3+dx))" "$Y3" >/dev/null 2>&1; done
$AB mouse up >/dev/null 2>&1; sleep 0.4
$AB eval "JSON.stringify((function(){var b=document.querySelector('[data-td-gutter]').getBoundingClientRect();var R=document.querySelector('.td-right').getBoundingClientRect();return {gx:Math.round(b.left+b.width/2),gy:Math.round(b.top+b.height/2),rightWBefore:Math.round(R.width)};})())"
GB=$($AB eval "JSON.stringify((function(){var b=document.querySelector('[data-td-gutter]').getBoundingClientRect();return {gx:Math.round(b.left+b.width/2),gy:Math.round(b.top+b.height/2)};})())" 2>&1 | tail -1)
GXY=$(echo "$GB" | $PY -c "import sys,json;d=json.loads(sys.stdin.read());d=json.loads(d) if isinstance(d,str) else d;print(d['gx'],d['gy'])")
GX=$(echo $GXY | cut -d' ' -f1); GY=$(echo $GXY | cut -d' ' -f2)
$AB mouse move "$GX" "$GY" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for dx in 10 20 30 40; do $AB mouse move "$((GX+dx))" "$GY" >/dev/null 2>&1; done
$AB mouse up >/dev/null 2>&1; sleep 0.3
$AB eval "JSON.stringify((function(){var R=document.querySelector('.td-right').getBoundingClientRect();return {rightWAfter:Math.round(R.width)};})())"

echo ""
echo "=== 回归：换页 / 语法 / 组件合规 ==="
$AB open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1
sleep 2.5
$AB eval "JSON.stringify({kanbanOk:!!document.querySelector('.kb-tag')})" 2>&1 | tail -1
$PY mg-work/kanban/r13/check-syntax.py pages/task-detail.html 2>&1 | tail -2
$AB close >/dev/null 2>&1
echo DONE

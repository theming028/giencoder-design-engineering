#!/usr/bin/env bash
# Round 15 / item 2 —— 修正后复测（圆角 / 标题高 / 编辑器封顶）+ 交互补测（关闭 / 继续创建 / 上传）
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
OUT="mg-work/r15"
mkdir -p "$OUT"

"$AB" open "$URL" >/dev/null 2>&1
sleep 2

echo "=== A. 修正项复测 ==="
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var d=document.querySelector('.kb-crt-dialog'),cs=getComputedStyle(d);var ti=document.querySelector('.kb-crt-title');var te=document.querySelector('.kb-crt-editor'),ecs=getComputedStyle(te);var m=document.querySelector('.kb-crt-msgs');var dr=d.getBoundingClientRect(),mr=m.getBoundingClientRect();var inh=document.querySelector('.kb-crt-head');return JSON.stringify({dialogRadius:cs.borderRadius,dialogW:Math.round(dr.width),dialogH:Math.round(dr.height),headH:Math.round(inh.getBoundingClientRect().height),headRadius:getComputedStyle(inh).borderTopLeftRadius,titleH:Math.round(ti.getBoundingClientRect().height),titleRadius:getComputedStyle(ti).borderRadius,titlePad:getComputedStyle(ti).paddingLeft,editorH:Math.round(te.getBoundingClientRect().height),editorMaxH:ecs.maxHeight,editorMinH:ecs.minHeight,msgsTopRelDialog:Math.round(mr.top-dr.top),msgsH:Math.round(mr.height)});})()"
"$AB" screenshot "" "$OUT/crt-open2.png" >/dev/null 2>&1

echo
echo "=== B1. ✕ 关闭 ==="
"$AB" eval "(function(){document.querySelector('.kb-crt-close').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var m=document.querySelector('.kb-crt');return JSON.stringify({hidden:m.hidden,isOpen:m.classList.contains('is-open')});})()"

echo
echo "=== B2. 「取消」关闭 ==="
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){document.querySelectorAll('.kb-crt-foot .kb-crt-btn')[0].click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var m=document.querySelector('.kb-crt');return JSON.stringify({hidden:m.hidden});})()"

echo
echo "=== B3. 蒙层关闭 ==="
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){document.querySelector('.kb-crt-mask').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var m=document.querySelector('.kb-crt');return JSON.stringify({hidden:m.hidden});})()"

echo
echo "=== B4. Esc 关闭 ==="
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var m=document.querySelector('.kb-crt');return JSON.stringify({hidden:m.hidden});})()"

echo
echo "=== C. 「保存并继续创建」→ 表单清空且弹窗保留 ==="
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){document.querySelectorAll('.kb-crt-type .giencoder-select-option')[1].click();var ti=document.querySelector('.kb-crt-title .giencoder-input');ti.value='测试标题';ti.dispatchEvent(new Event('input',{bubbles:true}));return JSON.stringify({type:document.querySelector('.kb-crt-type .giencoder-select-view-text').textContent,title:ti.value});})()"
"$AB" eval "(function(){document.querySelector('[data-crt-keep]').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var s=document.querySelector('.kb-crt-type');var ti=document.querySelector('.kb-crt-title .giencoder-input');var m=document.querySelector('.kb-crt');return JSON.stringify({stillOpen:!m.hidden,typeText:s.querySelector('.giencoder-select-view-text').textContent,typeHasValue:s.classList.contains('giencoder-select-has-value'),title:ti.value});})()"

echo
echo "=== D. 上传文件列表增删 ==="
"$AB" eval "(function(){var inp=document.querySelector('.kb-crt-file');if(!inp)return 'NO_INPUT';var f1=new File(['a'],'需求文档.md',{type:'text/markdown'});var f2=new File(['b'],'接口定义.yaml',{type:'text/yaml'});var dt=new DataTransfer();dt.items.add(f1);dt.items.add(f2);inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));var it=document.querySelectorAll('.kb-crt-upitem');var names=[];it.forEach(function(e){names.push(e.textContent.trim());});return JSON.stringify({count:it.length,names:names});})()"
"$AB" eval "(function(){var rm=document.querySelector('.kb-crt-uprm');rm.click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var it=document.querySelectorAll('.kb-crt-upitem');var names=[];it.forEach(function(e){names.push(e.textContent.trim());});return JSON.stringify({countAfterRemove:it.length,names:names});})()"
"$AB" screenshot "" "$OUT/crt-upload.png" >/dev/null 2>&1

echo
echo "=== E. 大视口下编辑器高度封顶 ==="
"$AB" resize 1440 900 >/dev/null 2>&1
sleep 2
"$AB" eval "(function(){var m=document.querySelector('.kb-crt');if(m.hidden)document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var d=document.querySelector('.kb-crt-dialog').getBoundingClientRect();var t=document.querySelector('.kb-crt-title').getBoundingClientRect();var e=document.querySelector('.kb-crt-editor').getBoundingClientRect();var a=document.querySelector('.kb-crt-attach').getBoundingClientRect();var f=document.querySelector('.kb-crt-foot').getBoundingClientRect();return JSON.stringify({vw:innerWidth,vh:innerHeight,dialog:[Math.round(d.width),Math.round(d.height)],title:[Math.round(t.width),Math.round(t.height)],editor:[Math.round(e.width),Math.round(e.height)],editorTopRel:Math.round(e.top-d.top),attachH:Math.round(a.height),footH:Math.round(f.height)});})()"
"$AB" screenshot "" "$OUT/crt-large.png" >/dev/null 2>&1
echo DONE

#!/usr/bin/env bash
# Round 16 实测：假滚动条移除 / rq-status 字号 / 浅灰底加深一级 / 两弹窗尺寸统一
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
OUT="mg-work/r16"
mkdir -p "$OUT"

echo "############ kanban.html ############"
"$AB" set viewport 1440 900 >/dev/null 2>&1
"$AB" open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1
sleep 2

echo "=== A. 泳道假滚动条是否已移除（期望 0）==="
"$AB" eval "(function(){return JSON.stringify({colScrollEls:document.querySelectorAll('.kb-col-scroll').length});})()"

echo
echo "=== B. 项目选择器 / kb-radio 底色（期望 #F2F2F2 = rgb(242,242,242)）==="
"$AB" eval "(function(){var v=document.querySelector('.kb-proj-select .giencoder-select-view');var r=document.querySelector('.kb-radio');var o={};if(v)o.projSelectBg=getComputedStyle(v).backgroundColor;if(r)o.radioBg=getComputedStyle(r).backgroundColor;var on=document.querySelector('.kb-radio-btn.is-on');if(on)o.radioOnBg=getComputedStyle(on).backgroundColor;o.fill2=getComputedStyle(document.documentElement).getPropertyValue('--color-fill-2');return JSON.stringify(o);})()"
"$AB" eval "(function(){var v=document.querySelector('.kb-proj-select .giencoder-select-view');v.dispatchEvent(new MouseEvent('mouseover',{bubbles:true}));return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var v=document.querySelector('.kb-proj-select .giencoder-select-view');var cs=getComputedStyle(v);return JSON.stringify({hoverRule:'见 stylesheet',bgNow:cs.backgroundColor});})()"
"$AB" screenshot "" "$OUT/kanban-top.png" >/dev/null 2>&1

echo
echo "=== C. 两个弹窗尺寸对比 ==="
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1
echo -n "创建任务 kb-crt : "
"$AB" eval "(function(){var d=document.querySelector('.kb-crt-dialog'),r=d.getBoundingClientRect(),cs=getComputedStyle(d);return JSON.stringify({w:Math.round(r.width),h:Math.round(r.height),left:Math.round(r.left),top:Math.round(r.top),bottom:Math.round(innerHeight-r.bottom),radius:cs.borderRadius});})()"
"$AB" eval "(function(){document.querySelector('.kb-crt-mask').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var t=document.querySelector('.kb-stat[data-modal-title]');t.click();return 1;})()" >/dev/null 2>&1
sleep 1
echo -n "待协作 kb-coop : "
"$AB" eval "(function(){var d=document.querySelector('.kb-coop-dialog'),r=d.getBoundingClientRect(),cs=getComputedStyle(d);return JSON.stringify({w:Math.round(r.width),h:Math.round(r.height),left:Math.round(r.left),top:Math.round(r.top),bottom:Math.round(innerHeight-r.bottom),radius:cs.borderRadius,transform:cs.transform});})()"
"$AB" screenshot "" "$OUT/coop-new.png" >/dev/null 2>&1

echo
echo "############ req-kanban.html ############"
"$AB" open "http://127.0.0.1:8866/pages/req-kanban.html" >/dev/null 2>&1
sleep 2

echo "=== D. rq-status 字号（期望 12px）==="
"$AB" eval "(function(){var els=document.querySelectorAll('.rq-status');var o=[];els.forEach(function(e){var cs=getComputedStyle(e);o.push({cls:e.className.replace('rq-status ',''),fs:cs.fontSize,h:Math.round(e.getBoundingClientRect().height)});});return JSON.stringify({count:els.length,items:o.slice(0,6)});})()"

echo
echo "=== E. req-kanban 项目选择器 / kb-radio 底色 ==="
"$AB" eval "(function(){var v=document.querySelector('.kb-proj-select .giencoder-select-view');var r=document.querySelector('.kb-radio');var o={};if(v)o.projSelectBg=getComputedStyle(v).backgroundColor;if(r)o.radioBg=getComputedStyle(r).backgroundColor;o.colScrollEls=document.querySelectorAll('.kb-col-scroll').length;return JSON.stringify(o);})()"
"$AB" screenshot "" "$OUT/req-kanban.png" >/dev/null 2>&1
echo DONE

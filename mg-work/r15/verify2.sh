#!/usr/bin/env bash
# Round 15 / item 2 —— 创建任务弹窗实测
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
OUT="mg-work/r15"
mkdir -p "$OUT"

"$AB" open "$URL" >/dev/null 2>&1
sleep 2

echo "=== A. 触发卡片存在性 ==="
"$AB" eval "(function(){var c=document.querySelector('.kb-create');if(!c)return 'NO_CARD';var m=document.querySelector('.kb-crt');return JSON.stringify({card:!!c,modal:!!m,hidden:m?m.hidden:null,dialog:!!document.querySelector('.kb-crt-dialog')});})()"

echo
echo "=== B. 点击创建任务 → 打开弹窗 ==="
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 'clicked';})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var m=document.querySelector('.kb-crt'),d=document.querySelector('.kb-crt-dialog');if(!m)return 'NO_MODAL';var cs=getComputedStyle(d),r=d.getBoundingClientRect();return JSON.stringify({hidden:m.hidden,isOpen:m.classList.contains('is-open'),w:Math.round(r.width),h:Math.round(r.height),radius:cs.borderRadius,shadow:cs.boxShadow,opacity:cs.opacity,maskBg:getComputedStyle(m.querySelector('.kb-crt-mask')).backgroundColor,blur:getComputedStyle(m.querySelector('.kb-crt-mask')).backdropFilter});})()"
"$AB" screenshot "" "$OUT/crt-open.png" >/dev/null 2>&1

echo
echo "=== C. 布局关键尺寸 ==="
"$AB" eval "(function(){var q=function(s){var e=document.querySelector(s);if(!e)return null;var r=e.getBoundingClientRect();var c=getComputedStyle(e);return {w:Math.round(r.width),h:Math.round(r.height),fs:c.fontSize,pad:c.padding};};return JSON.stringify({head:q('.kb-crt-head'),title:q('.giencoder-modal-title'),type:q('.kb-crt-type .giencoder-select-view'),titleInput:q('.kb-crt-title'),editor:q('.kb-crt-editor'),toolbar:q('.kb-crt-toolbar'),upbtn:q('.kb-crt-upbtn'),hint:q('.kb-crt-uptip'),aside:q('.kb-crt-aside'),asideHead:q('.kb-crt-aside-head'),fld:q('.kb-crt-fld'),lbl:q('.kb-crt-lbl'),foot:q('.kb-crt-foot')});})()"

echo
echo "=== D. 页脚三按钮宽度 ==="
"$AB" eval "(function(){var bs=document.querySelectorAll('.kb-crt-foot .kb-crt-btn');var o=[];for(var i=0;i<bs.length;i++){var r=bs[i].getBoundingClientRect();o.push({t:bs[i].textContent.trim(),w:Math.round(r.width),h:Math.round(r.height),pad:getComputedStyle(bs[i]).paddingLeft+'/'+getComputedStyle(bs[i]).paddingRight});}var f=document.querySelector('.kb-crt-foot').getBoundingClientRect();var last=bs[bs.length-1].getBoundingClientRect();return JSON.stringify({btns:o,rightGap:Math.round(f.right-last.right)});})()"

echo
echo "=== E. 交互：任务类型下拉 ==="
"$AB" eval "(function(){document.querySelector('.kb-crt-type .giencoder-select-view').click();return 'open';})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var p=document.querySelector('.kb-crt-type .giencoder-select-popup');var cs=getComputedStyle(p);var r=p.getBoundingClientRect();var v=document.querySelector('.kb-crt-type .giencoder-select-view').getBoundingClientRect();return JSON.stringify({disp:cs.display,vis:cs.visibility,open:p.classList.contains('giencoder-popup-open'),popupW:Math.round(r.width),viewW:Math.round(v.width),opts:document.querySelectorAll('.kb-crt-type .giencoder-select-option').length});})()"
"$AB" screenshot "" "$OUT/crt-type-open.png" >/dev/null 2>&1

echo
echo "=== F. 选一项后回显 ==="
"$AB" eval "(function(){var o=document.querySelectorAll('.kb-crt-type .giencoder-select-option')[1];o.click();return 'picked';})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var s=document.querySelector('.kb-crt-type');var t=s.querySelector('.giencoder-select-view-text');return JSON.stringify({val:t.textContent,hasValue:s.classList.contains('giencoder-select-has-value'),color:getComputedStyle(t).color,collapsed:s.querySelector('.giencoder-select-view').getAttribute('aria-expanded')});})()"

echo
echo "=== G. 右栏选择器 + 日期面板 ==="
"$AB" eval "(function(){var s=document.querySelectorAll('.kb-crt-fld')[0];s.querySelector('.giencoder-select-view').click();return 'ok';})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var s=document.querySelectorAll('.kb-crt-fld')[0];var p=s.querySelector('.giencoder-select-popup');return JSON.stringify({disp:getComputedStyle(p).display,open:p.classList.contains('giencoder-popup-open')});})()"
"$AB" eval "(function(){document.querySelector('.kb-crt-date .giencoder-input-wrapper').click();return 'ok';})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var p=document.querySelector('.kb-crt-date .giencoder-date-picker-popup');var r=p.getBoundingClientRect();var d=document.querySelector('.kb-crt-dialog').getBoundingClientRect();return JSON.stringify({disp:getComputedStyle(p).display,open:p.classList.contains('giencoder-panel-open'),panels:document.querySelectorAll('.kb-crt-date .giencoder-calendar').length,cells:document.querySelectorAll('.kb-crt-date .giencoder-calendar-cell').length,inDialog:(r.left>=d.left-1&&r.right<=d.right+1)});})()"
"$AB" screenshot "" "$OUT/crt-date-open.png" >/dev/null 2>&1

echo
echo "=== H. 校验：空标题点创建任务 ==="
"$AB" eval "(function(){document.body.click();return 'ok';})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){document.querySelector('[data-crt-submit]').click();return 'submitted';})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var m=document.querySelector('.kb-crt-msgs');var shown=[];m.querySelectorAll('.giencoder-message').forEach(function(e){if(!e.hidden)shown.push(e.textContent.trim());});return JSON.stringify({msgsHidden:m.hidden,shown:shown,stillOpen:!document.querySelector('.kb-crt').hidden});})()"
"$AB" screenshot "" "$OUT/crt-error.png" >/dev/null 2>&1
echo DONE

#!/usr/bin/env bash
# Round 17 实测：创建任务弹窗 5 项调整
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
OUT="mg-work/r17"
mkdir -p "$OUT"

"$AB" set viewport 1440 900 >/dev/null 2>&1
"$AB" open "$URL" >/dev/null 2>&1
sleep 2
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1

echo "=== 1. footer 按钮垂直居中（期望 上=下）==="
"$AB" eval "(function(){var f=document.querySelector('.kb-crt-foot').getBoundingClientRect();var bs=document.querySelectorAll('.kb-crt-foot .kb-crt-btn');var o=[];bs.forEach(function(b){var r=b.getBoundingClientRect();o.push({t:b.textContent.trim(),top:Math.round(r.top-f.top),bottom:Math.round(f.bottom-r.bottom),h:Math.round(r.height)});});return JSON.stringify({footH:Math.round(f.height),align:getComputedStyle(document.querySelector('.kb-crt-foot')).alignItems,btns:o});})()"

echo
echo "=== 2. 任务类型宽度自适应 ==="
"$AB" eval "(function(){var t=document.querySelector('.kb-crt-type');return JSON.stringify({empty:Math.round(t.getBoundingClientRect().width),cssW:getComputedStyle(t).width,minW:getComputedStyle(t).minWidth});})()"
"$AB" eval "(function(){var o=document.querySelectorAll('.kb-crt-type .giencoder-select-option');o[1].click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var t=document.querySelector('.kb-crt-type');return JSON.stringify({pickedText:t.querySelector('.giencoder-select-view-text').textContent,width:Math.round(t.getBoundingClientRect().width)});})()"

echo
echo "=== 3. aside 字段左右排列（label 在控件外、之前）==="
"$AB" eval "(function(){var rows=document.querySelectorAll('.kb-crt-aside-body .kb-crt-row');var o=[];rows.forEach(function(r){var l=r.querySelector('.kb-crt-lbl');var c=r.querySelector('.giencoder-select-view, .giencoder-input-wrapper');var lr=l?l.getBoundingClientRect():null;var cr=c?c.getBoundingClientRect():null;o.push({lbl:l?l.textContent.trim():null,lblLeft:lr?Math.round(lr.left):null,lblW:lr?Math.round(lr.width):null,ctrlLeft:cr?Math.round(cr.left):null,ctrlW:cr?Math.round(cr.width):null,inView:!!(l&&l.closest('.giencoder-select-view'))});});return JSON.stringify(o);})()"

echo
echo "=== 4. 编辑器为 textarea（可多行输入）==="
"$AB" eval "(function(){var e=document.querySelector('.kb-crt-editor-body textarea');if(!e)return 'NO_TEXTAREA';return JSON.stringify({tag:e.tagName,cls:e.className,ph:e.placeholder,phLines:e.placeholder.split(String.fromCharCode(10)).length,w:Math.round(e.getBoundingClientRect().width),h:Math.round(e.getBoundingClientRect().height),resize:getComputedStyle(e).resize});})()"
"$AB" eval "(function(){var e=document.querySelector('.kb-crt-editor-body textarea');e.value='第一行：作为产品经理，我需要梳理需求。'+String.fromCharCode(10)+'第二行：以便团队能按优先级排期。'+String.fromCharCode(10)+'第三行：验收标准待补充。';return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var e=document.querySelector('.kb-crt-editor-body textarea');return JSON.stringify({lines:e.value.split(String.fromCharCode(10)).length,scrollH:e.scrollHeight,clientH:e.clientHeight});})()"
"$AB" screenshot "" "$OUT/crt-1440.png" >/dev/null 2>&1

echo
echo "=== 5. 与待协作弹窗尺寸/形态一致 ==="
echo -n "创建任务 kb-crt : "
"$AB" eval "(function(){var d=document.querySelector('.kb-crt-dialog'),r=d.getBoundingClientRect(),cs=getComputedStyle(d);return JSON.stringify({w:Math.round(r.width),h:Math.round(r.height),left:Math.round(r.left),top:Math.round(r.top),bottom:Math.round(innerHeight-r.bottom),radius:cs.borderRadius,origin:cs.transformOrigin});})()"
"$AB" eval "(function(){document.querySelector('.kb-crt-mask').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){document.querySelector('.kb-stat[data-modal-title]').click();return 1;})()" >/dev/null 2>&1
sleep 1
echo -n "待协作 kb-coop : "
"$AB" eval "(function(){var d=document.querySelector('.kb-coop-dialog'),r=d.getBoundingClientRect(),cs=getComputedStyle(d);return JSON.stringify({w:Math.round(r.width),h:Math.round(r.height),left:Math.round(r.left),top:Math.round(r.top),bottom:Math.round(innerHeight-r.bottom),radius:cs.borderRadius,origin:cs.transformOrigin});})()"
echo DONE

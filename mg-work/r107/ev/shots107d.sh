#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
AB() { "$NODE" "$CLI" "$@"; }

AB open "file:///$ROOT/pages/conversation.html?v=$(date +%s)" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2600 >/dev/null 2>&1

# 打开右栏：默认应落在「摘要」页签，四个模块卡片式
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 900 >/dev/null 2>&1
AB screenshot "$OUT/d1-summary.png" >/dev/null 2>&1

# 「+」菜单（DS 下拉）
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB screenshot "$OUT/d2-modmenu.png" >/dev/null 2>&1
AB eval "document.dispatchEvent(new MouseEvent('click',{bubbles:true}))" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1

# 右键菜单（标签栏上）
AB eval "(function(){var t=document.querySelector('.td-browse .td-browse-tab');t.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:900,clientY:100}));return 'ok';})()" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB screenshot "$OUT/d3-ctxmenu.png" >/dev/null 2>&1
AB eval "document.dispatchEvent(new MouseEvent('click',{bubbles:true}))" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1

# 划词浮条（主对话区选中一段文字）
AB eval "(function(){var sc=document.querySelector('.r93-scroll');var w=document.createTreeWalker(sc,NodeFilter.SHOW_TEXT,null,false);var node=null;while(w.nextNode()){var t=w.currentNode;if(t.nodeValue&&t.nodeValue.trim().length>=14){node=t;break;}}if(!node)return 'no';var r=document.createRange();r.setStart(node,0);r.setEnd(node,Math.min(14,node.nodeValue.length));var s=window.getSelection();s.removeAllRanges();s.addRange(r);var rect=r.getBoundingClientRect();node.parentElement.dispatchEvent(new MouseEvent('mouseup',{bubbles:true,clientX:Math.round(rect.left+12),clientY:Math.round(rect.top+6)}));return 'sel';})()" >/dev/null 2>&1
AB wait 550 >/dev/null 2>&1
AB screenshot "$OUT/d4-selbar.png" >/dev/null 2>&1

echo "shots-d done"

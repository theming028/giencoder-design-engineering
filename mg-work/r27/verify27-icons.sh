#!/usr/bin/env bash
# 第27轮第1项精确复测：三处分组标题的「图标 → 文字」间距 + 图标形状
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/task-detail.html"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3

echo "=== 分组标题：图标盒 / 间距 / 颜色 ==="
$AB eval "JSON.stringify((function(){var hs=document.querySelectorAll('.td-sec-head');var out=[];for(var i=0;i<hs.length;i++){var h=hs[i],sv=h.querySelector('svg');var ir=sv.getBoundingClientRect();var cs=getComputedStyle(h);var tn=null,w=document.createTreeWalker(h,NodeFilter.SHOW_TEXT);while(w.nextNode()){if(w.currentNode.textContent.trim()){tn=w.currentNode;break;}}var rg=document.createRange();rg.selectNodeContents(tn);var tr=rg.getBoundingClientRect();out.push({head:h.textContent.trim(),gap:cs.gap,display:cs.display,icon:{l:Math.round(ir.left),r:Math.round(ir.right),w:Math.round(ir.width),h:Math.round(ir.height)},textL:Math.round(tr.left),iconToText:Math.round(tr.left-ir.right),color:getComputedStyle(sv).color,firstPathD:(sv.querySelector('path')||{}).getAttribute?sv.querySelector('path').getAttribute('d').slice(0,26):null});}return out;})())"

echo ""
echo "=== 与设计稿图标对照（裁剪放大） ==="
$AB eval "window.scrollTo(0,0);1" >/dev/null 2>&1
$AB screenshot "mg-work/r27/verify-detail-r27.png" >/dev/null 2>&1
C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe - <<'PY'
from PIL import Image
im = Image.open('mg-work/r27/verify-detail-r27.png').convert('RGB')
# 三处分组标题：从整页截图里按 DOM 位置裁（下面用 eval 得到的坐标由人工核对）
im.crop((16, 300, 420, 560)).resize((int(404*2.2), int(260*2.2)), Image.LANCZOS).save('mg-work/r27/cmp-detail-new.png')
print('  -> mg-work/r27/cmp-detail-new.png')
PY

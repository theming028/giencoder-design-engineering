#!/usr/bin/env bash
# Round 15 / item 1 verification: 转派(secondary) + 执行(primary) 按钮字号是否 14px 且走 DS 契约类
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
OUT="mg-work/r15"
mkdir -p "$OUT"

"$AB" open "$URL" >/dev/null 2>&1
sleep 2

echo "=== A. 待开始泳道 转派按钮（hover 显现）==="
"$AB" hover ".kb-col--todo .kb-card" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var b=document.querySelector('.kb-col--todo .kb-card .kb-btn-assign');if(!b)return 'NO_BTN';var cs=getComputedStyle(b);var r=b.getBoundingClientRect();return JSON.stringify({cls:b.className,fontSize:cs.fontSize,fontWeight:cs.fontWeight,lineHeight:cs.lineHeight,height:Math.round(r.height),width:Math.round(r.width),bg:cs.backgroundColor,color:cs.color,border:cs.borderColor,opacity:cs.opacity,vis:cs.visibility,pad:cs.paddingTop+' '+cs.paddingRight,bs:cs.boxSizing});})()"

echo
echo "=== B. 进行中泳道 执行按钮（hover 显现）==="
"$AB" hover ".kb-col--doing .kb-card" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var b=document.querySelector('.kb-col--doing .kb-card .kb-btn-exec');if(!b)return 'NO_BTN';var cs=getComputedStyle(b);var r=b.getBoundingClientRect();return JSON.stringify({cls:b.className,fontSize:cs.fontSize,fontWeight:cs.fontWeight,lineHeight:cs.lineHeight,height:Math.round(r.height),width:Math.round(r.width),bg:cs.backgroundColor,color:cs.color,opacity:cs.opacity,vis:cs.visibility,pad:cs.paddingTop+' '+cs.paddingRight,bs:cs.boxSizing});})()"

echo
echo "=== C. 是否残留自建视觉（应为 false）==="
"$AB" eval "(function(){var a=document.querySelector('.kb-btn-assign'),e=document.querySelector('.kb-btn-exec');function idOf(n){var out=[];for(var i=0;i<n.classList.length;i++)out.push(n.classList[i]);return out;}return JSON.stringify({assign:idOf(a),exec:idOf(e),dsBase:getComputedStyle(a).display});})()"

echo
echo "=== D. 与卡尾日期是否重叠 / 卡片宽度 ==="
"$AB" hover ".kb-col--todo .kb-card" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var card=document.querySelector('.kb-col--todo .kb-card');var b=card.querySelector('.kb-btn-assign');var vals=card.querySelectorAll('.kb-card-foot .kb-val');var out=[];for(var i=0;i<vals.length;i++){var r=vals[i].getBoundingClientRect();out.push([Math.round(r.left),Math.round(r.right)]);}var rb=b.getBoundingClientRect();var rc=card.getBoundingClientRect();return JSON.stringify({cardW:Math.round(rc.width),btn:[Math.round(rb.left),Math.round(rb.right),Math.round(rb.top),Math.round(rb.bottom)],vals:out,overlap:out.some(function(p){return p[1]>rb.left&&p[0]<rb.right;})});})()"

echo
echo "=== E. 截图 ==="
"$AB" hover ".kb-col--todo .kb-card" >/dev/null 2>&1
sleep 1
"$AB" screenshot "" "$OUT/assign-hover.png" >/dev/null 2>&1
"$AB" hover ".kb-col--doing .kb-card" >/dev/null 2>&1
sleep 1
"$AB" screenshot "" "$OUT/exec-hover.png" >/dev/null 2>&1
ls -la "$OUT"/*.png
echo DONE

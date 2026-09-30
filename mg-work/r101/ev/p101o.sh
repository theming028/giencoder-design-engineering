#!/usr/bin/env bash
# r101 第②批 · Run B：折叠头 hover 箭头 + 展开回弹动画 + 汇总卡菜单合一（全流程一次跑完）
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 900 >/dev/null 2>&1

echo "=== [1] 折叠第一个折叠块（真点击） ==="
"$NODE" "$AB" eval "(function(){var fh=document.querySelector('.r93-conv-host .r93-fold[data-open=\"1\"] > .r93-fh'); if(!fh) return 'no fh'; var t=fh.querySelector('.r93-ft'); var name=t?t.textContent:'?'; fh.click(); return 'clicked: '+name;})()"

echo "=== [2] 折叠后读数（箭头静态 opacity / 间距 / 子女） ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101n.js)"

echo "=== [3] 真鼠标 hover 折叠头，再读箭头 ==="
"$NODE" "$AB" eval "(function(){var f=document.querySelector('.r93-conv-host .r93-fold[data-open=\"0\"] > .r93-fc'); f.setAttribute('data-r101-fc','1'); return f?'tagged @'+JSON.stringify(f.getBoundingClientRect().top):'none';})()" >/dev/null 2>&1
"$NODE" "$AB" hover '[data-r101-fc]' >/dev/null 2>&1
"$NODE" "$AB" wait 320 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var f=document.querySelector('[data-r101-fc]'); var a=f.querySelector('.r93-fchev'); var p=a.previousElementSibling; var r=f.getBoundingClientRect(); var ar=a.getBoundingClientRect(); return JSON.stringify({hov:f.matches(':hover'),arrowOp:getComputedStyle(a).opacity,arrowBox:[Math.round(ar.x),Math.round(ar.y),Math.round(ar.width),Math.round(ar.height)],gap:Math.round(ar.left-p.getBoundingClientRect().right),gapFromRightEdge:Math.round(r.right-ar.right),fcBox:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)],fcColor:getComputedStyle(f).color});})()"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fc-hover2.png" >/dev/null 2>&1
echo "   （已截 r101-fc-hover2.png）"

echo "=== [4] 再点一次展开 → 抓 r93-fold-in 动画是否在播 ==="
"$NODE" "$AB" eval "(function(){var f=document.querySelector('[data-r101-fc]'); f.click(); return 'expand';})()" >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var h=document.querySelector('.r93-conv-host'); var fb=h.querySelector('.r93-fold[data-open=\"1\"] > .r93-fb'); if(!fb) return 'no fb'; var as=fb.getAnimations?fb.getAnimations():[]; return JSON.stringify({n:as.length, list:as.map(function(a){return (a.animationName||a.transitionProperty||'?')+'@'+Math.round(a.currentTime)+'ms/'+a.playState;}), refoldClosed:h.querySelectorAll('.r93-fold[data-open=\"0\"]').length});})()"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fold-spring.png" >/dev/null 2>&1

echo "=== [5] 汇总卡「⋯」→ 菜单内容 ==="
"$NODE" "$AB" eval "(function(){var b=document.querySelector('.r93-conv-host .r93-dmore'); b.setAttribute('data-r101-more','1'); return 'tagged';})()" >/dev/null 2>&1
"$NODE" "$AB" click '[data-r101-more]' >/dev/null 2>&1
"$NODE" "$AB" wait 380 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var m=document.querySelector('.r93-ctx'); if(!m) return 'no menu'; var R=m.getBoundingClientRect(); return JSON.stringify({open:m.classList.contains('giencoder-popup-open'),labels:[].map.call(m.querySelectorAll('.r93-ctx-label'),function(e){return e.textContent;}),divider:m.querySelectorAll('.giencoder-dropdown-divider').length,box:[Math.round(R.x),Math.round(R.y),Math.round(R.width),Math.round(R.height)],menus:document.querySelectorAll('.r93-ctx').length});})()"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-diff-menu2.png" >/dev/null 2>&1
echo "=== [6] hover「打开方式」→ 子菜单 ==="
"$NODE" "$AB" hover '.r93-ctx [data-r93-fctx="openwith"]' >/dev/null 2>&1
"$NODE" "$AB" wait 320 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var s=document.querySelector('.r93-ctx.giencoder-dropdown-submenu-popup'); if(!s) return 'no sub'; var R=s.getBoundingClientRect(); return JSON.stringify({open:s.classList.contains('giencoder-popup-open'),labels:[].map.call(s.querySelectorAll('.r93-ctx-label'),function(e){return e.textContent;}),box:[Math.round(R.x),Math.round(R.y),Math.round(R.width),Math.round(R.height)]});})()"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-diff-menu-sub2.png" >/dev/null 2>&1

echo "=== [7] Esc 关闭 → 汇总行整行右键（合成事件）→ 菜单应与上面同一套 ==="
"$NODE" "$AB" press Escape >/dev/null 2>&1
"$NODE" "$AB" wait 260 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var r=document.querySelector('.r93-conv-host .r93-drow'); var b=r.getBoundingClientRect(); r.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:Math.round(b.left+120),clientY:Math.round(b.top+18)})); return 'ctx-dispatch';})()"
"$NODE" "$AB" wait 320 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var m=document.querySelector('.r93-ctx'); return JSON.stringify({open:m?m.classList.contains('giencoder-popup-open'):null,labels:m?[].map.call(m.querySelectorAll('.r93-ctx-label'),function(e){return e.textContent;}):null});})()"

echo "=== [8] 产物卡右键（回归：应与上面逐字相同） ==="
"$NODE" "$AB" press Escape >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var r=document.querySelector('.r93-conv-host .r93-artcard'); var b=r.getBoundingClientRect(); r.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:Math.round(b.left+60),clientY:Math.round(b.top+20)})); return 'art-ctx';})()"
"$NODE" "$AB" wait 320 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var m=document.querySelector('.r93-ctx'); return JSON.stringify({labels:[].map.call(m.querySelectorAll('.r93-ctx-label'),function(e){return e.textContent;})});})()"

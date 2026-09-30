#!/usr/bin/env bash
# r101 第②批 · Run B2：补验「⋯」真点击（先滚到视口中央，避开毛玻璃标题栏那条 44px 带）
#                              + 展开回弹动画的「起播瞬间」读数
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 900 >/dev/null 2>&1

echo "=== [1] 折叠 + 展开，同一 tick 抓 r93-fold-in 的起播状态 ==="
"$NODE" "$AB" eval "(function(){var H=document.querySelector('.r93-conv-host');var fh=H.querySelector('.r93-fold[data-open=\"1\"] > .r93-fh');fh.click();var fc=H.querySelector('.r93-fold[data-open=\"0\"] > .r93-fc');fc.click();var fb=H.querySelector('.r93-fold[data-open=\"1\"] > .r93-fb');var a=fb.getAnimations()[0];return JSON.stringify({name:a.animationName,dur:a.effect.getTiming().duration,ease:a.effect.getTiming().easing,state:a.playState,ct:Math.round(a.currentTime),fill:a.effect.getTiming().fill});})()"
"$NODE" "$AB" wait 120 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var fb=document.querySelector('.r93-conv-host .r93-fold[data-open=\"1\"] > .r93-fb');var a=fb.getAnimations()[0];return a?('t+120ms: '+a.playState+' '+Math.round(a.currentTime)+'ms'):'动画已结束并被回收';})()"

echo "=== [2] 汇总卡「⋯」：先滚到视口中央，再真点击 ==="
"$NODE" "$AB" eval "(function(){var b=document.querySelector('.r93-conv-host .r93-dmore');b.scrollIntoView({block:'center'});b.setAttribute('data-r101-more','1');var r=b.getBoundingClientRect();var hit=document.elementFromPoint(Math.round(r.x+r.width/2),Math.round(r.y+r.height/2));return JSON.stringify({top:Math.round(r.top),hit:hit?hit.className.slice(0,40):null});})()"
"$NODE" "$AB" wait 260 >/dev/null 2>&1
"$NODE" "$AB" click '[data-r101-more]' >/dev/null 2>&1
"$NODE" "$AB" wait 400 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var m=document.querySelector('.r93-ctx');if(!m)return 'no menu';var R=m.getBoundingClientRect();var b=document.querySelector('[data-r101-more]').getBoundingClientRect();return JSON.stringify({open:m.classList.contains('giencoder-popup-open'),labels:[].map.call(m.querySelectorAll('.r93-ctx-label'),function(e){return e.textContent;}),divider:m.querySelectorAll('.giencoder-dropdown-divider').length,box:[Math.round(R.x),Math.round(R.y),Math.round(R.width),Math.round(R.height)],btnBottom:Math.round(b.bottom),dx:Math.round(R.x-b.x),dy:Math.round(R.y-b.bottom)});})()"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-diff-menu2.png" >/dev/null 2>&1
echo "   （已截 r101-diff-menu2.png）"

echo "=== [3] 真鼠标 hover「打开方式」→ 子菜单 ==="
"$NODE" "$AB" hover '.r93-ctx [data-r93-fctx="openwith"]' >/dev/null 2>&1
"$NODE" "$AB" wait 340 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var s=document.querySelector('.r93-ctx.giencoder-dropdown-submenu-popup');if(!s)return 'no sub';var R=s.getBoundingClientRect();return JSON.stringify({open:s.classList.contains('giencoder-popup-open'),labels:[].map.call(s.querySelectorAll('.r93-ctx-label'),function(e){return e.textContent;}),box:[Math.round(R.x),Math.round(R.y),Math.round(R.width),Math.round(R.height)]});})()"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-diff-menu-sub2.png" >/dev/null 2>&1
echo "   （已截 r101-diff-menu-sub2.png）"

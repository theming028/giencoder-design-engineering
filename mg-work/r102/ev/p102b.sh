#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"; H="${2:-900}"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport "$W" "$H" >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 1900 >/dev/null 2>&1

echo "===== A) 静态读数（十一条） ====="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p102b.js)"
echo
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/p102b-${W}.png" >/dev/null 2>&1
echo "  shot p102b-${W}.png"

echo
echo "===== B) ③ 折叠收起动效（真鼠标点击第一个折叠头） ====="
"$NODE" "$AB" eval "(function(){var f=document.querySelector('.r93-fold');f.scrollIntoView({block:'center'});return 'scrolled';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 260 >/dev/null 2>&1
"$NODE" "$AB" click ".r93-fold > .r93-fh" >/dev/null 2>&1
echo "[t0 立即]"
"$NODE" "$AB" eval "(function(){var f=document.querySelector('.r93-fold');var fb=f.querySelector(':scope > .r93-fb');var g=document.getAnimations();return JSON.stringify({open:f.getAttribute('data-open'),bh:fb.style.getPropertyValue('--r93-fbh'),h:Math.round(fb.getBoundingClientRect().height),maxH:getComputedStyle(fb).maxHeight,ovf:getComputedStyle(fb).overflow,nAnim:g.length,trans:g.filter(function(a){return a.constructor.name==='CSSTransition';}).map(function(a){return a.transitionProperty+'@'+Math.round(a.currentTime||0);})});})()"
"$NODE" "$AB" wait 120 >/dev/null 2>&1
echo "[t≈120ms]"
"$NODE" "$AB" eval "(function(){var f=document.querySelector('.r93-fold');var fb=f.querySelector(':scope > .r93-fb');var g=document.getAnimations();return JSON.stringify({h:Math.round(fb.getBoundingClientRect().height),maxH:getComputedStyle(fb).maxHeight,op:getComputedStyle(fb).opacity,nAnim:g.length});})()"
"$NODE" "$AB" wait 600 >/dev/null 2>&1
echo "[t≈720ms 终态]"
"$NODE" "$AB" eval "(function(){var f=document.querySelector('.r93-fold');var fb=f.querySelector(':scope > .r93-fb');var c=getComputedStyle(fb);return JSON.stringify({open:f.getAttribute('data-open'),h:Math.round(fb.getBoundingClientRect().height),maxH:c.maxHeight,mt:c.marginTop,op:c.opacity,ovf:c.overflow,cls:fb.className,nAnim:document.getAnimations().length});})()"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/p102b-folded-${W}.png" >/dev/null 2>&1
echo "  shot p102b-folded-${W}.png"

echo
echo "===== C) ② + ⑥ 折叠头 hover（真鼠标） ====="
"$NODE" "$AB" hover ".r93-fold > .r93-fc" >/dev/null 2>&1
"$NODE" "$AB" wait 320 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var f=document.querySelector('.r93-fold');var fc=f.querySelector(':scope > .r93-fc');var ch=fc.querySelector('.r93-fchev');var t=fc.querySelector('.r93-t14');var m=fc.querySelector('.r93-t12l');var meta=document.querySelector('.r93-fh .r93-t12l.r93-fm')||document.querySelector('.r93-fh .r93-t12l');return JSON.stringify({hov:fc.matches(':hover'),gap:getComputedStyle(fc).gap,chevML:getComputedStyle(ch).marginLeft,chevOp:getComputedStyle(ch).opacity,titleRight:Math.round(t.getBoundingClientRect().right),chevLeft:Math.round(ch.getBoundingClientRect().left),chevW:Math.round(ch.getBoundingClientRect().width),gapPx:Math.round(ch.getBoundingClientRect().left-t.getBoundingClientRect().right),fcColor:getComputedStyle(fc).color,metaColor:m?getComputedStyle(m).color:null,expMetaBase:meta?getComputedStyle(meta).color:null});})()"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/p102b-fchover-${W}.png" >/dev/null 2>&1
echo "  shot p102b-fchover-${W}.png"

echo
echo "===== D) ⑥ 展开头 hover 的 meta 色 ====="
"$NODE" "$AB" hover ".r93-fold > .r93-fh" >/dev/null 2>&1
"$NODE" "$AB" wait 320 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var fh=document.querySelector('.r93-fold > .r93-fh');var meta=fh.querySelector('.r93-t12l.r93-fm')||fh.querySelector('.r93-t12l');var t=fh.querySelector('.r93-t14');return JSON.stringify({hov:fh.matches(':hover'),metaColor:meta?getComputedStyle(meta).color:'no-meta',titleColor:t?getComputedStyle(t).color:null,metaTxt:meta?(meta.textContent||'').slice(0,16):null});})()"

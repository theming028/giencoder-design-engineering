#!/usr/bin/env bash
# r107 · 侧栏模块标签化 —— UI 实测链路（整条链路一次跑完，避免多进程串味）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
mkdir -p "$OUT"
TS=$(date +%s)
URL="file:///$ROOT/pages/conversation.html?v=$TS"
AB() { "$NODE" "$CLI" "$@"; }

echo "### 0 open + viewport"
AB open "$URL" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2600 >/dev/null 2>&1

echo "### 1 打开侧栏（真鼠标点页头那枚按钮）"
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 700 >/dev/null 2>&1
AB eval "JSON.stringify({
  on: !!(document.querySelector('div:has(> main)')||{}).classList && document.querySelector('div:has(> main)').classList.contains('av-browse-on'),
  tabs: [].map.call(document.querySelectorAll('.td-browse-tab'),function(t){return t.getAttribute('data-td-mod')+':'+t.textContent.trim();}),
  barH: (function(){var b=document.querySelector('.td-browse-bar');return b?Math.round(b.getBoundingClientRect().height):null;})(),
  panelW: Math.round((document.getElementById('av-browse-slot')||{getBoundingClientRect:function(){return {width:0}}}).getBoundingClientRect().width),
  panes: [].map.call(document.querySelectorAll('.td-browse-body,[data-td-pane]'),function(p){return (p.classList.contains('td-browse-body')?'files':p.getAttribute('data-td-pane'))+(p.hasAttribute('hidden')?'(hidden)':'');}),
  menuHidden: document.querySelector('.td-mod-menu').hasAttribute('hidden'),
  splitMainPlaced: (function(){var s=document.getElementById('av-browse-split');return !!(s&&s.parentElement&&s.parentElement.tagName!=='BODY');})()
})" 2>&1

echo "### 2 点 `+` 出模块菜单"
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB eval "JSON.stringify({menuHidden:document.querySelector('.td-mod-menu').hasAttribute('hidden'),items:[].map.call(document.querySelectorAll('[data-td-open-mod]'),function(b){return b.getAttribute('data-td-open-mod');})})" 2>&1
AB screenshot "$OUT/s1-modmenu.png" >/dev/null 2>&1

echo "### 3 开「审查」"
AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB eval "JSON.stringify({
  tabs: [].map.call(document.querySelectorAll('.td-browse-tab'),function(t){return t.getAttribute('data-td-mod')+(t.classList.contains('is-active')?'*':'');}),
  rvVisible: !document.querySelector('[data-td-pane=\"review\"]').hasAttribute('hidden'),
  filesHidden: document.querySelector('.td-browse-body').hasAttribute('hidden'),
  diffs: document.querySelectorAll('[data-td-diff]').length,
  open: document.querySelectorAll('.td-diff.is-open').length
})" 2>&1
AB screenshot "$OUT/s2-review.png" >/dev/null 2>&1

echo "### 4 审查：并排视图"
AB click ".td-rv-opts" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB click '[data-td-rv-view="split"]' >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB eval "JSON.stringify({isSplit:document.querySelector('.td-rv-body').classList.contains('is-split'),splitRowsVisible:(function(){var e=document.querySelector('.td-diff-split');return e?getComputedStyle(e).display:null;})(),uniRowsDisplay:(function(){var e=document.querySelector('.td-diff-rows:not(.td-diff-split)');return e?getComputedStyle(e).display:null;})()})" 2>&1
AB screenshot "$OUT/s3-review-split.png" >/dev/null 2>&1

echo "### 5 终端"
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB click '[data-td-open-mod="terminal"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click ".td-term" >/dev/null 2>&1
AB keyboard type "ls" >/dev/null 2>&1
AB press Enter >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB eval "JSON.stringify({termVisible:!document.querySelector('[data-td-pane=\"terminal\"]').hasAttribute('hidden'),outs:document.querySelectorAll('.td-term-out').length,echo:(document.querySelector('[data-td-term-echo]')||{}).textContent,lines:document.querySelectorAll('.td-term-line').length})" 2>&1
AB screenshot "$OUT/s4-terminal.png" >/dev/null 2>&1

echo "### 6 浏览器 + 标注"
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB click '[data-td-open-mod="browser"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click ".td-url-annot" >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB eval "JSON.stringify({annot:document.querySelector('.td-brw').classList.contains('is-annotating'),bar:!document.querySelector('.td-annot-bar').hasAttribute('hidden')})" 2>&1
AB screenshot "$OUT/s5-browser-annot.png" >/dev/null 2>&1
AB click ".td-page-card" >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB eval "JSON.stringify({note:!document.querySelector('.td-elnote').hasAttribute('hidden'),who:(document.querySelector('.td-elnote-t b')||{}).textContent})" 2>&1
AB screenshot "$OUT/s6-browser-elnote.png" >/dev/null 2>&1

echo "### 7 标签多开态 + 最大宽"
AB eval "JSON.stringify({
  tabs: [].map.call(document.querySelectorAll('.td-browse-tab'),function(t){return t.getAttribute('data-td-mod')+(t.classList.contains('is-active')?'*':'');}),
  tabRects: [].map.call(document.querySelectorAll('.td-browse-tab'),function(t){var r=t.getBoundingClientRect();return Math.round(r.left)+','+Math.round(r.width);}),
  panelW: Math.round(document.getElementById('av-browse-slot').getBoundingClientRect().width),
  mainW: Math.round(document.querySelector('main').getBoundingClientRect().width)
})" 2>&1

echo "### 8 关掉浏览器标签 → 激活邻居"
AB click '[data-td-tab][data-td-mod="browser"] [data-td-tab-x]' >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB eval "JSON.stringify({tabs:[].map.call(document.querySelectorAll('.td-browse-tab'),function(t){return t.getAttribute('data-td-mod')+(t.classList.contains('is-active')?'*':'');}),activePane:(function(){var a=document.querySelector('.td-browse-tab.is-active');return a?a.getAttribute('data-td-mod'):null;})()})" 2>&1

echo "### 9 最大化 / 还原"
AB click ".td-browse-acts [data-td-max]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({maxw:document.getElementById('av-browse-slot').getAttribute('data-td-maxw'),panelW:Math.round(document.getElementById('av-browse-slot').getBoundingClientRect().width),mainW:Math.round(document.querySelector('main').getBoundingClientRect().width)})" 2>&1
AB screenshot "$OUT/s7-max.png" >/dev/null 2>&1
AB click ".td-browse-acts [data-td-max]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({maxw:document.getElementById('av-browse-slot').getAttribute('data-td-maxw'),panelW:Math.round(document.getElementById('av-browse-slot').getBoundingClientRect().width)})" 2>&1

echo "### 10 侧边聊天：划词浮条"
AB eval "(function(){var m=document.querySelector('div:has(> main) > main')||document.querySelector('main');var ps=m.querySelectorAll('p');var el=null;for(var i=0;i<ps.length;i++){if((ps[i].textContent||'').trim().length>20){el=ps[i];break;}}if(!el)return 'no-target';var r=document.createRange();r.selectNodeContents(el);var s=window.getSelection();s.removeAllRanges();s.addRange(r);document.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));return 'sel='+JSON.stringify((s.toString()||'').slice(0,24));})()" 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({bar:!document.querySelector('.td-selbar').hasAttribute('hidden'),pos:(function(){var b=document.querySelector('.td-selbar');return b.style.left+','+b.style.top;})()})" 2>&1
AB screenshot "$OUT/s8-selbar.png" >/dev/null 2>&1

echo "### 11 点浮条 → 开「侧边聊天」标签"
AB click '[data-td-side-ask]' >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB eval "JSON.stringify({tabs:[].map.call(document.querySelectorAll('.td-browse-tab'),function(t){return t.getAttribute('data-td-mod')+(t.classList.contains('is-active')?'*':'');}),sideVisible:!document.querySelector('[data-td-pane=\"side\"]').hasAttribute('hidden'),quote:(document.querySelector('[data-td-side-quote]')||{}).textContent,bar:document.querySelector('.td-selbar').hasAttribute('hidden')})" 2>&1
AB screenshot "$OUT/s9-sidechat.png" >/dev/null 2>&1

echo "### 12 侧边聊天发一条"
AB fill ".td-side-ta" "这样改会不会影响暗色档？" >/dev/null 2>&1
AB press Enter >/dev/null 2>&1
AB wait 700 >/dev/null 2>&1
AB eval "JSON.stringify({msgs:document.querySelectorAll('.td-side-msg').length,last:(function(){var l=document.querySelectorAll('.td-side-msg');return l.length?l[l.length-1].textContent.trim():null;})()})" 2>&1
AB screenshot "$OUT/s10-sidechat-send.png" >/dev/null 2>&1

echo "### 13 拖拽重排：把最后一枚标签拖到最前"
AB eval "(function(){var t=document.querySelectorAll('.td-browse-tab');var last=t[t.length-1],first=t[0];var a=last.getBoundingClientRect(),b=first.getBoundingClientRect();var el=document.elementFromPoint(a.left+a.width/2,a.top+a.height/2);if(!el)return 'no-el';var cx=a.left+a.width/2,cy=a.top+a.height/2,tx=b.left+2;el.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,button:0,clientX:cx,clientY:cy}));window.dispatchEvent(new PointerEvent('pointermove',{bubbles:true,clientX:cx-10,clientY:cy}));window.dispatchEvent(new PointerEvent('pointermove',{bubbles:true,clientX:tx,clientY:cy}));window.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,clientX:tx,clientY:cy}));return 'dragged from '+Math.round(cx)+' to '+Math.round(tx);})()" 2>&1
AB wait 300 >/dev/null 2>&1
AB eval "JSON.stringify({tabs:[].map.call(document.querySelectorAll('.td-browse-tab'),function(t){return t.getAttribute('data-td-mod');})})" 2>&1
AB screenshot "$OUT/s11-tabs-reorder.png" >/dev/null 2>&1

echo "### 14 全屏整页（供裁切）"
AB set viewport 1440 900 >/dev/null 2>&1
AB screenshot "$OUT/s12-full.png" >/dev/null 2>&1
echo "### done"

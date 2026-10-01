#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
TS=$(date +%s)
AB() { "$NODE" "$CLI" "$@"; }
AB open "file:///$ROOT/pages/conversation.html?v=$TS" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2600 >/dev/null 2>&1
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 700 >/dev/null 2>&1

echo "--- A 找 main 里可见文本元素并划词 ---"
AB eval "(function(){
  var m=document.querySelector('div:has(> main) > main')||document.querySelector('main');
  var el=document.elementFromPoint(500,300);
  var hop=0;
  while(el && el!==m && hop<6){ var t=(el.textContent||'').trim(); if(t.length>16) break; el=el.parentElement; hop++; }
  if(!el) return 'no-el';
  var r0=el.getBoundingClientRect();
  var rg=document.createRange(); rg.selectNodeContents(el);
  var s=window.getSelection(); s.removeAllRanges(); s.addRange(rg);
  var out={tag:el.tagName,cls:String(el.className).slice(0,40),rect:[Math.round(r0.left),Math.round(r0.top),Math.round(r0.width),Math.round(r0.height)],selLen:(s.toString()||'').length,vis:r0.width>0&&r0.height>0};
  document.dispatchEvent(new MouseEvent('mouseup',{bubbles:true,clientX:500,clientY:300}));
  return JSON.stringify(out);
})()" 2>&1
AB wait 500 >/dev/null 2>&1
AB eval "JSON.stringify({bar:!document.querySelector('.td-selbar').hasAttribute('hidden'),left:document.querySelector('.td-selbar').style.left,top:document.querySelector('.td-selbar').style.top})" 2>&1
AB screenshot "$ROOT/mg-work/r107/raw/d4-selbar.png" >/dev/null 2>&1

echo "--- B 点浮条 → 侧边聊天 ---"
AB click '[data-td-side-ask]' >/dev/null 2>&1
AB wait 600 >/dev/null 2>&1
AB eval "JSON.stringify({tabs:[].map.call(document.querySelectorAll('.td-browse-tab'),function(t){return t.getAttribute('data-td-mod')+(t.classList.contains('is-active')?'*':'');}),sideVisible:!document.querySelector('[data-td-pane=\"side\"]').hasAttribute('hidden'),quote:(document.querySelector('[data-td-side-quote]')||{}).textContent.slice(0,40),bar:document.querySelector('.td-selbar').hasAttribute('hidden'),focus:(document.activeElement||{}).className})" 2>&1
AB screenshot "$ROOT/mg-work/r107/raw/d5-sidechat.png" >/dev/null 2>&1
AB focus ".td-side-ta" >/dev/null 2>&1
AB fill ".td-side-ta" "这样改会不会影响暗色档？" >/dev/null 2>&1
AB press Enter >/dev/null 2>&1
AB wait 800 >/dev/null 2>&1
AB eval "JSON.stringify({msgs:document.querySelectorAll('.td-side-msg').length,last:(function(){var l=document.querySelectorAll('.td-side-msg');return l.length?l[l.length-1].textContent.trim():null;})()})" 2>&1
AB screenshot "$ROOT/mg-work/r107/raw/d6-sidechat-send.png" >/dev/null 2>&1

echo "--- C 终端：AB focus + 真按键 ---"
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB click '[data-td-open-mod="terminal"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB focus ".td-term" >/dev/null 2>&1
AB eval "JSON.stringify({active:(document.activeElement||{}).className})" 2>&1
AB keyboard type "ls" >/dev/null 2>&1
AB eval "JSON.stringify({echo:(document.querySelector('[data-td-term-echo]')||{}).textContent})" 2>&1
AB press Enter >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB eval "JSON.stringify({outs:document.querySelectorAll('.td-term-out').length,lines:document.querySelectorAll('.td-term-line').length,last:(function(){var o=document.querySelectorAll('.td-term-out');return o.length?o[o.length-1].textContent:'-';})()})" 2>&1
AB keyboard type "pwd" >/dev/null 2>&1
AB press Enter >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB eval "JSON.stringify({outs:document.querySelectorAll('.td-term-out').length,last:(function(){var o=document.querySelectorAll('.td-term-out');return o.length?o[o.length-1].textContent:'-';})()})" 2>&1
AB screenshot "$ROOT/mg-work/r107/raw/d7-term.png" >/dev/null 2>&1

echo "--- D Esc 只关菜单、不关侧栏 ---"
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB eval "JSON.stringify({menuOpen:!document.querySelector('.td-mod-menu').hasAttribute('hidden')})" 2>&1
AB press Escape >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB eval "JSON.stringify({menuOpen:!document.querySelector('.td-mod-menu').hasAttribute('hidden'),panelOn:document.querySelector('div:has(> main)').classList.contains('av-browse-on')})" 2>&1
AB press Escape >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({panelOn:document.querySelector('div:has(> main)').classList.contains('av-browse-on')})" 2>&1
echo done

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
echo "--- A 选区诊断 ---"
AB eval "(function(){
  var m=document.querySelector('div:has(> main) > main')||document.querySelector('main');
  if(!m) return 'no main';
  var ps=m.querySelectorAll('p');
  var out={main:!!m,ps:ps.length,txts:[]};
  for(var i=0;i<Math.min(ps.length,6);i++){out.txts.push((ps[i].textContent||'').trim().slice(0,20));}
  var el=null;
  for(var j=0;j<ps.length;j++){ if((ps[j].textContent||'').trim().length>20){el=ps[j];break;} }
  out.el=el?el.tagName+'.'+el.className:'none';
  if(!el) return JSON.stringify(out);
  out.rect=(function(){var r=el.getBoundingClientRect();return Math.round(r.left)+','+Math.round(r.top)+','+Math.round(r.width)+','+Math.round(r.height);})();
  var rg=document.createRange(); rg.selectNodeContents(el);
  var s=window.getSelection(); s.removeAllRanges(); s.addRange(rg);
  out.selLen=(s.toString()||'').length;
  out.ranges=s.rangeCount;
  out.userSelect=getComputedStyle(el).userSelect;
  out.parentUS=(function(){var p=el.parentElement;while(p){var u=getComputedStyle(p).userSelect;if(u==='none')return p.tagName+'.'+p.className; p=p.parentElement;} return 'ok';})();
  return JSON.stringify(out);
})()" 2>&1
echo "--- B 直接调 panel.js 的划词逻辑（派发 mouseup 后读浮条）---"
AB eval "(function(){document.dispatchEvent(new MouseEvent('mouseup',{bubbles:true,clientX:600,clientY:200}));return 'fired';})()" 2>&1
AB wait 500 >/dev/null 2>&1
AB eval "JSON.stringify({bar:!document.querySelector('.td-selbar').hasAttribute('hidden'),left:document.querySelector('.td-selbar').style.left,top:document.querySelector('.td-selbar').style.top,selLen:(window.getSelection()||{}).toString?window.getSelection().toString().length:-1})" 2>&1
echo "--- C 审查显示选项（正确选择器）---"
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click '[data-td-rv-opts]' >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB eval "JSON.stringify({optsHidden:document.querySelector('.td-rv-opts').hasAttribute('hidden')})" 2>&1
AB screenshot "$ROOT/mg-work/r107/raw/d1-rvopts.png" >/dev/null 2>&1
AB click '[data-td-rv-view="split"]' >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB eval "JSON.stringify({isSplit:document.querySelector('.td-rv-body').classList.contains('is-split'),uni:(function(){var e=document.querySelector('.td-diff-rows:not(.td-diff-split)');return e?getComputedStyle(e).display:null;})(),spl:(function(){var e=document.querySelector('.td-diff-split');return e?getComputedStyle(e).display:null;})()})" 2>&1
AB screenshot "$ROOT/mg-work/r107/raw/d2-review-split.png" >/dev/null 2>&1
echo "--- D 终端键入（真按键）---"
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB click '[data-td-open-mod="terminal"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click ".td-term" >/dev/null 2>&1
AB wait 200 >/dev/null 2>&1
AB eval "JSON.stringify({active:(document.activeElement||{}).className})" 2>&1
AB press l >/dev/null 2>&1
AB press s >/dev/null 2>&1
AB eval "JSON.stringify({echo:(document.querySelector('[data-td-term-echo]')||{}).textContent})" 2>&1
AB press Enter >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB eval "JSON.stringify({outs:document.querySelectorAll('.td-term-out').length,lines:document.querySelectorAll('.td-term-line').length,last:(function(){var o=document.querySelectorAll('.td-term-out');return o.length?o[o.length-1].textContent:'-';})()})" 2>&1
AB screenshot "$ROOT/mg-work/r107/raw/d3-term-ls.png" >/dev/null 2>&1
echo "done"

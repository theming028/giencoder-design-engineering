#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 3000 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){
function d(el,depth,out){ if(!el||depth>4) return; var r=el.getBoundingClientRect();
 out.push('  '.repeat(depth)+el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+'.'+String(el.className||'').split(' ').slice(0,6).join('.')+' ['+Math.round(r.left)+','+Math.round(r.top)+','+Math.round(r.width)+','+Math.round(r.height)+']');
 var k=el.children; for(var i=0;i<k.length && i<8;i++) d(k[i],depth+1,out); }
var out=[]; d(document.body,0,out); return out.join(chr=String.fromCharCode(10));
})()" 2>&1 | head -5
echo "---- 用文本方式 ----"
"$NODE" "$AB" eval "(function(){
var out=[];
function d(el,depth){ if(!el||depth>4) return; var r=el.getBoundingClientRect();
 out.push(new Array(depth+1).join('  ')+el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+' ['+Math.round(r.left)+','+Math.round(r.top)+','+Math.round(r.width)+','+Math.round(r.height)+'] .'+String(el.className||'').replace(/\s+/g,'.').slice(0,60));
 var k=el.children; for(var i=0;i<k.length && i<6;i++) d(k[i],depth+1); }
d(document.body,0); return out.join('\n'); })()"
echo "===== main 直接子元素 ====="
"$NODE" "$AB" eval "(function(){
var m=document.querySelector('main'); var o=[];
if(!m) return 'no main';
o.push('main children = '+m.children.length);
for(var i=0;i<m.children.length;i++){ var e=m.children[i]; var r=e.getBoundingClientRect();
 o.push('  ['+i+'] '+e.tagName.toLowerCase()+' ['+Math.round(r.left)+','+Math.round(r.top)+','+Math.round(r.width)+','+Math.round(r.height)+'] cls='+String(e.className).slice(0,90)); }
var par=m.parentElement; o.push('main.parent = '+par.tagName.toLowerCase()+' .'+String(par.className).slice(0,80));
o.push('par.display='+getComputedStyle(par).display+' flexDir='+getComputedStyle(par).flexDirection);
o.push('main.display='+getComputedStyle(m).display+' flexDir='+getComputedStyle(m).flexDirection);
var aside=document.querySelector('aside');
if(aside){var ar=aside.getBoundingClientRect(); o.push('aside ['+Math.round(ar.left)+','+Math.round(ar.top)+','+Math.round(ar.width)+','+Math.round(ar.height)+']');}
return o.join('\n'); })()"

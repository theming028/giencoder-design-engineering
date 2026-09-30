#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/avatar.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 3200 >/dev/null 2>&1

M="(function(){var o=[];
function R(sel){var e=document.querySelector(sel); if(!e) return sel+' = null'; var r=e.getBoundingClientRect();
 return sel+' = ['+Math.round(r.left)+','+Math.round(r.top)+','+Math.round(r.width)+','+Math.round(r.height)+'] disp='+getComputedStyle(e).display+' flex='+getComputedStyle(e).flex; }
['aside','.av-chat-drawer','.td-browse-slot','.td-browse','.td-tree','.td-code','.td-bf','.td-split','.td-crumb'].forEach(function(s){o.push(R(s));});
o.push('shellRow = '+ (function(){var a=document.querySelector('aside'); if(!a) return 'n/a'; var p=a.parentElement; var r=p.getBoundingClientRect(); return p.className.slice(0,70)+' ['+Math.round(r.width)+'] display='+getComputedStyle(p).display+' dir='+getComputedStyle(p).flexDirection;})());
o.push('drawerParent = '+(function(){var d=document.querySelector('.av-chat-drawer'); if(!d) return 'null'; var p=d.parentElement; return p.tagName+'.'+String(p.className).slice(0,60);})());
return o.join('\n');})()"

echo "===== 关闭态 ====="
"$NODE" "$AB" eval "$M"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/a105-av-closed.png" >/dev/null 2>&1

echo "===== 点「打开侧栏」后 ====="
"$NODE" "$AB" eval "(function(){var b=document.querySelector('[data-td-browse-toggle]'); if(!b) return 'no btn'; b.click(); return 'clicked';})()"
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" eval "$M"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/a105-av-open.png" >/dev/null 2>&1

echo "===== 再点「全屏」  ====="
"$NODE" "$AB" eval "(function(){var b=document.querySelector('[data-td-fullscreen]'); if(!b) return 'no fs'; b.click(); return 'clicked';})()"
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" eval "$M"
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/a105-av-fs.png" >/dev/null 2>&1

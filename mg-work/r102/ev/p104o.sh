#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 3200 >/dev/null 2>&1

SNAP="(function(){var folds=document.querySelectorAll('.r93-fold'),o=[];window.__f0=window.__f0||[];for(var i=0;i<folds.length;i++){var f=folds[i];var fb=f.querySelector(':scope > .r93-fb');o.push(f.getAttribute('data-r93-open')+'/'+(fb?fb.offsetHeight:'-')+'/'+(fb?Math.round(fb.scrollHeight):'-'));}return JSON.stringify(o);})()"

echo "-- 初始快照（open/offsetH/scrollH）--"
"$NODE" "$AB" eval "$SNAP"
"$NODE" "$AB" eval "(function(){var folds=document.querySelectorAll('.r93-fold');window.__f0=[];for(var i=0;i<folds.length;i++){var fb=folds[i].querySelector(':scope > .r93-fb');window.__f0.push(fb?fb.scrollHeight:0);}return 'saved '+window.__f0.length;})()"

echo "-- 全部收起（点每个块的当前可见头）--"
"$NODE" "$AB" eval "(function(){var folds=document.querySelectorAll('.r93-fold');for(var i=0;i<folds.length;i++){var f=folds[i];var hs=f.querySelectorAll(':scope > .r93-fh, :scope > .r93-fc');var w=null;for(var j=0;j<hs.length;j++){if(getComputedStyle(hs[j]).display!=='none'){w=hs[j];break;}}if(w)w.click();}return 'clicked';})()"
"$NODE" "$AB" wait 900 >/dev/null 2>&1
echo "-- 收起后快照 --"
"$NODE" "$AB" eval "$SNAP"

echo "-- 全部展开（再点一次）--"
"$NODE" "$AB" eval "(function(){var folds=document.querySelectorAll('.r93-fold');for(var i=0;i<folds.length;i++){var f=folds[i];var hs=f.querySelectorAll(':scope > .r93-fh, :scope > .r93-fc');var w=null;for(var j=0;j<hs.length;j++){if(getComputedStyle(hs[j]).display!=='none'){w=hs[j];break;}}if(w)w.click();}return 'clicked';})()"
"$NODE" "$AB" wait 1000 >/dev/null 2>&1
echo "-- 展开后快照 --"
"$NODE" "$AB" eval "$SNAP"
echo "-- 与初始 scrollH 逐块比对 --"
"$NODE" "$AB" eval "(function(){var folds=document.querySelectorAll('.r93-fold'),o=[];for(var i=0;i<folds.length;i++){var fb=folds[i].querySelector(':scope > .r93-fb');var h=fb?fb.scrollHeight:0;o.push(i+':'+(h===window.__f0[i]?'OK':'DIFF '+window.__f0[i]+'->'+h));}return JSON.stringify(o);})()"

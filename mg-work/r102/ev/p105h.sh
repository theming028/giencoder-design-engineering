#!/bin/bash
# r105 ③ 2560 视口 + 暗色：文件预览栏 / 页头按钮 / 页签滑块 全要素复核
cd /e/GienCoder/giencoder-design-engineering || exit 1
NODE=/c/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe
AB=/c/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js
R=mg-work/r102/raw
V=$(date +%s)

echo "=========== A. 2560 浅色 ==========="
"$NODE" "$AB" set viewport 2560 1400 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$V" >/dev/null 2>&1
"$NODE" "$AB" wait 2800 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105f.js)" 2>&1
"$NODE" "$AB" click '[data-r93-browse]' >/dev/null 2>&1
"$NODE" "$AB" wait 900 >/dev/null 2>&1
echo "--- 2560 预览栏展开 ---"
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105f.js)" 2>&1
"$NODE" "$AB" screenshot "" "$R/z2560-browse.png" >/dev/null 2>&1
echo "--- 2560 侧栏 + 全屏 ---"
"$NODE" "$AB" click '[data-r93-fullscreen]' >/dev/null 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105f.js)" 2>&1
"$NODE" "$AB" screenshot "" "$R/z2560-browse-fs.png" >/dev/null 2>&1

echo
echo "=========== B. 2560 暗色 ==========="
"$NODE" "$AB" eval "(function(){document.documentElement.removeAttribute('data-r93-full');document.documentElement.setAttribute('giencoder-theme','dark');return 'dark';})()" 2>&1
"$NODE" "$AB" wait 700 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105f.js)" 2>&1
"$NODE" "$AB" screenshot "" "$R/z2560-dark-browse.png" >/dev/null 2>&1
echo "--- 暗色关键变量 ---"
"$NODE" "$AB" eval "(function(){
  var cs=getComputedStyle(document.documentElement);
  var names=['--color-bg-1','--color-bg-2','--color-bg-popup','--td-panel-line','--td-tree-active-bg','--td-crumb-line'];
  var o={};
  names.forEach(function(n){o[n]=cs.getPropertyValue(n).trim();});
  var p=document.querySelector('.td-browse');
  o.panelBg=getComputedStyle(p).backgroundColor;
  o.panelBorder=getComputedStyle(p).borderTopColor;
  o.barBg=getComputedStyle(document.querySelector('.r93-bar')).backgroundColor;
  var b=document.querySelector('.r93-baract');
  o.btnBg=getComputedStyle(b).backgroundColor; o.btnBd=getComputedStyle(b).borderColor;
  o.codeKey=getComputedStyle(document.querySelector('.td-code-k')).color;
  o.codeTx=getComputedStyle(document.querySelector('.td-code-tx')).color;
  o.bfColor=getComputedStyle(document.querySelector('.td-bf-name')||document.querySelector('.td-bf')).color;
  return JSON.stringify(o);
})()" 2>&1
echo
echo "=========== C. 1440 暗色（无侧栏） ==========="
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" wait 300 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "$R/z1440-dark-105.png" >/dev/null 2>&1
echo shot

#!/bin/bash
# r105 ② 页签滑块动效逐帧实测 + r105 ③ hover 态
cd /e/GienCoder/giencoder-design-engineering || exit 1
NODE=/c/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe
AB=/c/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js
V=$(date +%s)

"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$V" >/dev/null 2>&1
"$NODE" "$AB" wait 2600 >/dev/null 2>&1

echo "=== 滑块初始（对话选中） ==="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105g1.js)" 2>&1

echo
echo "=== 逐帧采样：点「轨迹」后 ==="
"$NODE" "$AB" eval "(function(){
  var g=document.querySelector('.r93-seg');
  var sl=g.querySelector('.giencoder-radio-button-slider');
  window.__rec=[];
  var t0=performance.now();
  function tick(){
    var m=getComputedStyle(sl).transform;
    window.__rec.push([Math.round(performance.now()-t0), m, sl.offsetWidth]);
    if (performance.now()-t0 < 600) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
  g.querySelector('[data-r93-tab=\"trace\"]').click();
  return 'started';
})()" 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "JSON.stringify(window.__rec.filter(function(v,i){return i%4===0||i>window.__rec.length-4}))" 2>&1

echo
echo "=== 轨迹态读数 ==="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105g1.js)" 2>&1

echo
echo "=== 回「对话」 ==="
"$NODE" "$AB" click '[data-r93-tab="chat"]' >/dev/null 2>&1
"$NODE" "$AB" wait 900 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p105g1.js)" 2>&1

echo
echo "=== 页头按钮 hover 态 ==="
"$NODE" "$AB" eval "(function(){
  var b=document.querySelectorAll('.r93-baract');
  var o=[];
  [].forEach.call(b,function(x){var cs=getComputedStyle(x);o.push({al:x.getAttribute('aria-label'),bg:cs.backgroundColor,bd:cs.borderColor,br:cs.borderRadius,cur:cs.cursor});});
  return JSON.stringify(o);
})()" 2>&1

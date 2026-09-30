#!/usr/bin/env bash
# r101 第②批 · Run A：静态读数 + 滚动后毛玻璃 A/B 取证（全流程一次跑完）
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 900 >/dev/null 2>&1
echo "=== [1] 静态读数（未滚动） ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101n.js)"
echo
echo "=== [2] 滚动到 1200 / 1800，各拍 ON/OFF 两张 ==="
for TOP in 1200 1800; do
  "$NODE" "$AB" eval "document.querySelector('.r93-conv-host .r93-scroll').scrollTop = $TOP; 'scrollTop=' + document.querySelector('.r93-conv-host .r93-scroll').scrollTop" >/dev/null 2>&1
  "$NODE" "$AB" wait 260 >/dev/null 2>&1
  "$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-frost-on-$TOP.png" >/dev/null 2>&1
  "$NODE" "$AB" eval "(function(){var b=document.querySelector('.r93-bar');b.style.backdropFilter='none';b.style.webkitBackdropFilter='none';return 'off';})()" >/dev/null 2>&1
  "$NODE" "$AB" wait 200 >/dev/null 2>&1
  "$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-frost-off-$TOP.png" >/dev/null 2>&1
  "$NODE" "$AB" eval "(function(){var b=document.querySelector('.r93-bar');b.style.backdropFilter='';b.style.webkitBackdropFilter='';return 'on';})()" >/dev/null 2>&1
  echo "   top=$TOP 已拍"
done
echo
echo "=== [3] 滚动后的几何（bar 是否仍贴顶、内容是否已到它底下） ==="
"$NODE" "$AB" eval "(function(){var h=document.querySelector('.r93-conv-host');var R=function(e){var b=e.getBoundingClientRect();return [Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)];};var sc=h.querySelector('.r93-scroll');return JSON.stringify({scrollTop:sc.scrollTop,bar:R(h.querySelector('.r93-bar')),scroll:R(sc),wrapTop:Math.round(h.querySelector('.r93-wrap').getBoundingClientRect().top)});})()"

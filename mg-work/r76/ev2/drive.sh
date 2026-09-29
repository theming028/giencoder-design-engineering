#!/bin/zsh
# r76b · 波点涟漪取帧驱动（重取新实现）
set -e
ROOT=/Users/shaoyuming/Documents/GienCoderDesignEngineering
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=$ROOT/mg-work/r76/ev2
mkdir -p $EV

URL="file://$ROOT/pages/base.html"

# 必须：先 open 再 set viewport
$AB open "$URL" >/dev/null
$AB set viewport 1440 900 >/dev/null
sleep 1.2

echo "== pathname =="
$AB eval 'location.pathname + " | " + innerWidth + "x" + innerHeight'
echo "== fire =="
$AB eval "window.__M='fire';$(cat $EV/../ev/rip.js)"

for T in 0 40 100 160 230 290; do
  $AB eval "window.__M='seek';window.__T=$T;$(cat $EV/../ev/rip.js)" >/dev/null
  $AB screenshot "$EV/rip-$T.png" >/dev/null
done
echo "== done =="
ls -la $EV

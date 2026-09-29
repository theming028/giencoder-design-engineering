#!/bin/zsh
# r76c · 波点涟漪取帧驱动
set -e
ROOT=/Users/shaoyuming/Documents/GienCoderDesignEngineering
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=$ROOT/mg-work/r76/ev2
mkdir -p $EV

URL="file://$ROOT/pages/base.html"
$AB open "$URL" >/dev/null
$AB set viewport 1440 900 >/dev/null
sleep 1.2

echo "== fire =="
$AB eval "window.__M='fire';$(cat $ROOT/mg-work/r76/ev/rip.js)"

for T in 0 40 80 120 160 200 240 285; do
  $AB eval "window.__M='seek';window.__T=$T;$(cat $ROOT/mg-work/r76/ev/rip.js)" >/dev/null
  $AB screenshot "$EV/c-$T.png" >/dev/null
done
echo "== done =="
ls $EV/c-*.png

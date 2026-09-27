set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
$AB open "http://127.0.0.1:8866/pages/task-detail.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.8
X=$($AB eval "Math.round(document.querySelector('[data-td-gutter]').getBoundingClientRect().left+4)")
$AB mouse move $X 400 >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1
for x in 1300 1350 1390 1405 1415 1420 1424; do $AB mouse move $x 400 >/dev/null 2>&1; sleep 0.03; done
$AB mouse up >/dev/null 2>&1; sleep 0.5
echo "collapsed=$( $AB eval "document.querySelector('.td-root').classList.contains('is-collapsed')") w=$($AB eval "Math.round(document.querySelector('.td-right').getBoundingClientRect().width)")"
$AB screenshot "mg-work/r24/r24-collapsed.png" >/dev/null 2>&1
echo shot

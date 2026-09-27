AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
run() { $AB open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1; $AB set viewport 1440 900 >/dev/null 2>&1; sleep 2.5; }
lane() { echo "document.querySelectorAll('.kb-col')[$1].querySelector('.kb-card')"; }

echo "=== 泳道结构 ==="
run
$AB eval "JSON.stringify([].map.call(document.querySelectorAll('.kb-col'),function(c,i){return i+':'+c.className.split(' ').pop()+' cards='+c.querySelectorAll('.kb-card').length}))"

echo ""
echo "=== 8b. 进行中 lane 第 1/2/3 张卡都跳转 ==="
for n in 0 1 2; do
  run
  $AB eval "(function(){document.querySelectorAll('.kb-col')[1].querySelectorAll('.kb-card')[$n].id='__c';return 1})()" >/dev/null 2>&1
  $AB click "#__c" >/dev/null 2>&1; sleep 1.3
  echo "  进行中第 $((n+1)) 张 -> $($AB eval "location.pathname.split('/').pop()")"
done

echo ""
echo "=== 8d. 其他泳道首卡（回归） ==="
for n in 0 2 3; do
  run
  $AB eval "(function(){document.querySelectorAll('.kb-col')[$n].querySelector('.kb-card').id='__d';return 1})()" >/dev/null 2>&1
  LBL=$($AB eval "document.querySelectorAll('.kb-col')[$n].textContent.slice(0,4)")
  $AB click "#__d" >/dev/null 2>&1; sleep 1.3
  echo "  lane[$n] '$LBL' 首卡 -> $($AB eval "location.pathname.split('/').pop()")"
done

echo ""
echo "=== 8c. hover 出「执行」按钮后点它：不应跳转 ==="
run
$AB eval "(function(){var b=document.querySelector('.kb-card.is-dashed .kb-btn-exec');var r=b.getBoundingClientRect();window.__b=[Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)];return 1})()" >/dev/null 2>&1
CARD=$($AB eval "(function(){var r=document.querySelector('.kb-card.is-dashed').getBoundingClientRect();return JSON.stringify([Math.round(r.left+r.width/2),Math.round(r.top+20)])})()")
CX=$(echo "$CARD" | tr -d '[]"' | cut -d, -f1); CY=$(echo "$CARD" | tr -d '[]"' | cut -d, -f2)
$AB mouse move "$CX" "$CY" >/dev/null 2>&1; sleep 0.4
echo "  hover 后按钮可见性 = $($AB eval "getComputedStyle(document.querySelector('.kb-card.is-dashed .kb-btn-exec')).visibility")"
BX=$($AB eval "window.__b[0]"); BY=$($AB eval "window.__b[1]")
$AB mouse move "$BX" "$BY" >/dev/null 2>&1; sleep 0.3; $AB mouse down >/dev/null 2>&1; $AB mouse up >/dev/null 2>&1; sleep 1.2
echo "  点击执行按钮($BX,$BY) -> $($AB eval "location.pathname.split('/').pop()")"

echo ""
echo "=== 9. req-kanban 页脚（回归：悬浮球已无） ==="
$AB open "http://127.0.0.1:8866/pages/req-kanban.html" >/dev/null 2>&1; sleep 2.4
echo "  fab = $($AB eval "document.querySelectorAll('.kb-fab').length")  rq-panel = $($AB eval "!!document.querySelector('.rq-panel')")"

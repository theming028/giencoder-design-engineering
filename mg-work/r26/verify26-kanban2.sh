set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
run() {
  $AB open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1
  $AB set viewport 1440 900 >/dev/null 2>&1
  sleep 2.5
}
echo "=== 8b. 同泳道第 2 张普通卡（回归：仍应跳转） ==="
run
echo "  lane 统计 = $($AB eval "JSON.stringify((function(){var lane=document.querySelector('.kb-card.is-dashed').closest('.kb-lane');var cs=lane.querySelectorAll('.kb-card');cs[1].id='__p2';return {laneCls:lane.className,n:cs.length,second:cs[1].className,secondTitle:cs[1].querySelector('.kb-card-title').textContent.slice(0,16)};})())")"
$AB click "#__p2" >/dev/null 2>&1; sleep 1.4
echo "  第2张点击后 path = $($AB eval "location.pathname.split('/').pop()")"

echo ""
echo "=== 8c. 卡内按钮不应触发跳转（回归） ==="
run
echo "  dashed 卡内按钮数 = $($AB eval "(function(){var c=document.querySelector('.kb-card.is-dashed');var b=c.querySelector('button');if(b)b.id='__pb';return c.querySelectorAll('button,a').length})()")"
$AB click "#__pb" >/dev/null 2>&1; sleep 1.2
echo "  点 dashed 卡内按钮后 path = $($AB eval "location.pathname.split('/').pop()")"

echo ""
echo "=== 8d. 其他泳道首卡（回归） ==="
run
echo "  待开始首卡 = $($AB eval "(function(){var c=document.querySelectorAll('.kb-lane')[0].querySelector('.kb-card');c.id='__p3';return c.className})()")"
$AB click "#__p3" >/dev/null 2>&1; sleep 1.4
echo "  点击后 path = $($AB eval "location.pathname.split('/').pop()")"

echo ""
echo "=== 8e. 已终止泳道首卡（回归） ==="
run
echo "  已终止首卡 = $($AB eval "(function(){var ls=document.querySelectorAll('.kb-lane');var t=null;for(var i=0;i<ls.length;i++){if(ls[i].querySelector('.kb-card')&&ls[i].textContent.indexOf('已终止')>=0)t=ls[i];}var c=t.querySelector('.kb-card');c.id='__p4';return c.className})()")"
$AB click "#__p4" >/dev/null 2>&1; sleep 1.4
echo "  点击后 path = $($AB eval "location.pathname.split('/').pop()")"

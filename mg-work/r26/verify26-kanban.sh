set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"

echo "=== 9. 右下角悬浮球已移除 ==="
for f in kanban.html req-kanban.html; do
  $AB open "http://127.0.0.1:8866/pages/$f" >/dev/null 2>&1
  $AB set viewport 1440 900 >/dev/null 2>&1
  sleep 2.4
  echo "  $f -> .kb-fab = $($AB eval "JSON.stringify({fab:!!document.querySelector('.kb-fab'),n:document.querySelectorAll('.kb-fab').length,panel:!!document.querySelector('.kb-panel')})")"
done

echo ""
echo "=== 8. 任务看板「进行中」泳道首卡点击进入详情页 ==="
$AB open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.6
echo "  首卡信息 = $($AB eval "JSON.stringify((function(){var c=document.querySelector('.kb-card.is-dashed');var r=c.getBoundingClientRect();return {cls:c.className,title:c.querySelector('.kb-card-title').textContent.slice(0,20),x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),cursor:getComputedStyle(c).cursor};})())")"
$AB click ".kb-card.is-dashed" >/dev/null 2>&1
sleep 1.4
echo "  点击后 path = $($AB eval "location.pathname.split('/').pop()")  title = $($AB eval "document.title")"
echo "  详情页容器存在 = $($AB eval "!!document.querySelector('.td-root')")"

echo ""
echo "=== 8b. 同泳道第二张普通卡（回归：仍应跳转） ==="
$AB open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1
sleep 2.4
$AB eval "document.querySelectorAll('.kb-lane')[1] && 1" >/dev/null 2>&1
LANESEL=$($AB eval "(function(){var ls=document.querySelectorAll('.kb-lane');for(var i=0;i<ls.length;i++){if(ls[i].textContent.slice(0,4).indexOf('进行中')>=0)return i;}return -1})()")
echo "  进行中 lane index = $LANESEL"
$AB eval "(function(){var ls=document.querySelectorAll('.kb-lane');for(var i=0;i<ls.length;i++){if(ls[i].textContent.slice(0,4).indexOf('进行中')>=0){var cs=ls[i].querySelectorAll('.kb-card');cs[1].id='__probe2';return cs.length;}}return 0})()" >/dev/null 2>&1
$AB click "#__probe2" >/dev/null 2>&1
sleep 1.4
echo "  第二张卡点击后 path = $($AB eval "location.pathname.split('/').pop()")"

echo ""
echo "=== 8c. 卡内按钮不应触发跳转（回归） ==="
$AB open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1
sleep 2.4
$AB eval "(function(){var ls=document.querySelectorAll('.kb-lane');for(var i=0;i<ls.length;i++){if(ls[i].textContent.slice(0,4).indexOf('进行中')>=0){var b=ls[i].querySelector('.kb-card button');if(b){b.id='__probebtn';return 1;}}}return 0})()" >/dev/null 2>&1
$AB click "#__probebtn" >/dev/null 2>&1
sleep 1.0
echo "  点卡内按钮后 path = $($AB eval "location.pathname.split('/').pop()")"

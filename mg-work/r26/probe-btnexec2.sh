AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
$AB open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.5
$AB eval "(function(){var b=document.querySelector('.kb-card.is-dashed .kb-btn-exec');var r=b.getBoundingClientRect();window.__b=[Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)];return 1})()" >/dev/null 2>&1
$AB eval "(function(){window.__t=[];document.addEventListener('click',function(e){var el=e.target;window.__t.push({tag:el.tagName,cls:String(el.className).slice(0,60),closestBtn:!!(el.closest&&el.closest('button')),closestCard:!!(el.closest&&el.closest('.kb-card'))});},true);return 1})()" >/dev/null 2>&1
echo "按钮中心 = $($AB eval "JSON.stringify(window.__b)")"
echo "-- A. agent-browser click 选择器 --"
$AB eval "(function(){document.querySelector('.kb-card.is-dashed .kb-btn-exec').id='__pb';return 1})()" >/dev/null 2>&1
$AB click "#__pb" >/dev/null 2>&1; sleep 1.2
echo "   targets = $($AB eval "JSON.stringify(window.__t)")"
echo "   path = $($AB eval "location.pathname.split('/').pop()")"

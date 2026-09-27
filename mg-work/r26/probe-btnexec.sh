set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
$AB open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.5
echo "按钮矩形:"
$AB eval "JSON.stringify((function(){var b=document.querySelector('.kb-card.is-dashed .kb-btn-exec');var r=b.getBoundingClientRect();window.__b=[Math.round(r.left+r.width/2),Math.round(r.top+r.height/2)];return {rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],center:window.__b};})())"
echo "安装 capture 监听:"
$AB eval "(function(){window.__t=[];document.addEventListener('click',function(e){var el=e.target;window.__t.push((el.tagName||'')+'.'+(el.className||'')+' | closestBtn='+!!(el.closest&&el.closest('button'))+' | closestCard='+!!(el.closest&&el.closest('.kb-card')));},true);return 'ok'})()"
$AB eval "(function(){var c=window.__b;$ABX=c;return 1})()" >/dev/null 2>&1
X=$(eval "$AB eval 'window.__b[0]'" 2>/dev/null); Y=$(eval "$AB eval 'window.__b[1]'" 2>/dev/null)
echo "点击中心 ($X,$Y)"
$AB mouse move "$X" "$Y" >/dev/null 2>&1; $AB mouse down >/dev/null 2>&1; $AB mouse up >/dev/null 2>&1
sleep 1.2
echo "click targets = $($AB eval "JSON.stringify(window.__t)")"
echo "path = $($AB eval "location.pathname.split('/').pop()")"

set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
$AB open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.5
echo "泳道容器类名:"
$AB eval "JSON.stringify((function(){var c=document.querySelector('.kb-card.is-dashed');var p=c.parentElement;var chain=[];for(var i=0;i<5&&p;i++){chain.push(p.tagName+'.'+p.className);p=p.parentElement;}return chain})())"
echo "虚线卡内按钮:"
$AB eval "JSON.stringify((function(){var c=document.querySelector('.kb-card.is-dashed');var b=c.querySelector('button');var cs=getComputedStyle(b);return {text:b.textContent.trim(),disabled:b.disabled,disabledAttr:b.hasAttribute('disabled'),pe:cs.pointerEvents,cls:b.className,outer:b.outerHTML.slice(0,180)};})())"
echo "虚线卡整块 HTML:"
$AB eval "(function(){var c=document.querySelector('.kb-card.is-dashed');return c.outerHTML.replace(/\s+/g,' ').slice(0,900)})()"

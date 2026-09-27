set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
$AB open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.6
echo "=== 首张普通卡 vs 虚线卡 结构对比 ==="
$AB eval "(function(){var a=document.querySelector('.kb-card:not(.is-dashed)'),b=document.querySelector('.kb-card.is-dashed');function d(c){return {cls:c.className,attrs:[].map.call(c.attributes,function(x){return x.name+'='+x.value}).slice(0,8),kids:[].map.call(c.children,function(k){return k.tagName+'.'+String(k.className)}),title:(c.querySelector('.kb-card-title')||{}).textContent}}return JSON.stringify({normal:d(a),dashed:d(b)},null,1)})()"
echo "=== .kb-fab 结构 ==="
$AB eval "(function(){var f=document.querySelector('.kb-fab');if(!f)return 'none';return JSON.stringify({cls:f.className,html:f.outerHTML.slice(0,300),parentCls:f.parentElement.className})})()"

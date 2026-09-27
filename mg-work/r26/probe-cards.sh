set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
$AB open "http://127.0.0.1:8866/pages/kanban.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.6
echo "=== 进行中泳道首卡 ==="
$AB eval "(function(){var ls=document.querySelectorAll('.kb-lane');for(var i=0;i<ls.length;i++){var t=ls[i].textContent.slice(0,10);if(t.indexOf('进行中')>=0){var c=ls[i].querySelector('.kb-card');return JSON.stringify({lane:ls[i].className,cardCls:c.className,cardText:c.textContent.slice(0,24),clickTargets:c.querySelectorAll('button,a,[data-nogo]').length});}}return 'no lane'})()"
echo "=== .is-dashed 卡片数量与文本 ==="
$AB eval "(function(){var d=document.querySelectorAll('.kb-card.is-dashed');return JSON.stringify([].map.call(d,function(c){return c.textContent.slice(0,26)}))})()"
echo "=== 右下角固定/绝对定位大元素 ==="
$AB eval "(function(){var out=[];document.querySelectorAll('body *').forEach(function(el){var cs=getComputedStyle(el);if(cs.position!=='fixed'&&cs.position!=='absolute')return;var r=el.getBoundingClientRect();if(r.width<28||r.width>80||r.height<28||r.height>80)return;if(r.left<1000||r.top<600)return;out.push({tag:el.tagName,cls:String(el.className).slice(0,140),al:el.getAttribute('aria-label'),x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),bg:cs.backgroundColor});});return JSON.stringify(out,null,1)})()"

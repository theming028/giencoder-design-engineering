AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
$AB open "http://127.0.0.1:8866/pages/task-detail.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.8
$AB eval "JSON.stringify((function(){var a=document.querySelector('.td-attr-link');var v=a.closest('.td-attr-v');var r=a.getBoundingClientRect(),vr=v.getBoundingClientRect();return {linkText:JSON.stringify(a.textContent),linkW:Math.round(r.width),valueW:Math.round(vr.width),overflow:Math.round(r.width-vr.width),aDisplay:getComputedStyle(a).display,vWhite:getComputedStyle(v).whiteSpace,txt:getComputedStyle(v).textOverflow};})())"
$AB eval "window.scrollTo(0,0);1" >/dev/null 2>&1
$AB screenshot "mg-work/r27/now.png" >/dev/null 2>&1

AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
"$AB" set viewport 1440 900 >/dev/null 2>&1
"$AB" open "$URL" >/dev/null 2>&1
sleep 2
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 2
# 定格在动画中间态：opacity 0.5 + translateY -6 + scaleY 0.985
FREEZE="var d=document.querySelector('.kb-crt-dialog');d.style.transition='none';d.style.opacity='0.5';d.style.transform='translateX(-50%) translateY(-6px) scaleY(0.985)';"
# A: 旧阴影（无同色 spread）
"$AB" eval "(function(){${FREEZE}d.style.boxShadow='0 1px 2px rgba(0,0,0,0.08)';return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" screenshot "" mg-work/r20/mid-OLD.png >/dev/null 2>&1
# B: 新阴影（1px 同色 spread）
"$AB" eval "(function(){${FREEZE}d.style.boxShadow='0 0 0 1px #fff, 0 1px 2px rgba(0,0,0,0.08)';return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" screenshot "" mg-work/r20/mid-NEW.png >/dev/null 2>&1
echo DONE

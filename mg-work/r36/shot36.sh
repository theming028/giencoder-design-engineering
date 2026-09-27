set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
$AB open "http://127.0.0.1:8866/pages/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 5
$AB screenshot "mg-work/r36/shots/36-final-closed.png" >/dev/null 2>&1
$AB eval 'document.querySelector("[data-av-chat-toggle]").click();1' >/dev/null 2>&1
sleep 1.3
$AB screenshot "mg-work/r36/shots/36-final-open.png" >/dev/null 2>&1
echo done

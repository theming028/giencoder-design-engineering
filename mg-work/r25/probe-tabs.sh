set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
for f in base.html kanban.html dev.html skills.html; do
  $AB open "http://127.0.0.1:8866/pages/$f" >/dev/null 2>&1
  $AB set viewport 1440 900 >/dev/null 2>&1
  sleep 2.2
  cur=$($AB eval "location.pathname")
  $AB click "[data-tab='dev']" >/dev/null 2>&1; sleep 1.1
  afterDev=$($AB eval "location.pathname + location.hash")
  $AB open "http://127.0.0.1:8866/pages/$f" >/dev/null 2>&1; sleep 2.0
  $AB click "[data-tab='base']" >/dev/null 2>&1; sleep 1.1
  afterBase=$($AB eval "location.pathname + location.hash")
  echo "$f  cur=$cur  |点研发->$afterDev  |点基础->$afterBase"
done

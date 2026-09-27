set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PAGES="base.html dev.html kanban.html req-kanban.html task-detail.html avatar.html automation.html skills.html settings.html"
echo "page                 |selected| 点【基础】->               | 点【研发】->"
echo "---------------------+--------+----------------------------+---------------------------"
for f in $PAGES; do
  $AB open "http://127.0.0.1:8866/pages/$f" >/dev/null 2>&1
  $AB set viewport 1440 900 >/dev/null 2>&1
  sleep 2.2
  sel=$($AB eval "(function(){var tl=document.querySelector('[role=\"tablist\"][aria-label=\"工作台切换\"]');if(!tl)return 'NO_TABLIST';var c=tl.querySelector('[data-tab][aria-selected=\"true\"]');return c?c.getAttribute('data-tab'):'none'})()" 2>&1 | tr -d '"' | tr -d '\n')
  # 点「基础工作台」
  $AB click "[data-tab='base']" >/dev/null 2>&1; sleep 1.2
  afterBase=$($AB eval "location.pathname.split('/').pop() + location.hash" 2>&1 | tr -d '"' | tr -d '\n')
  # 重新打开，点「研发工作台」
  $AB open "http://127.0.0.1:8866/pages/$f" >/dev/null 2>&1; sleep 2.0
  $AB click "[data-tab='dev']" >/dev/null 2>&1; sleep 1.2
  afterDev=$($AB eval "location.pathname.split('/').pop() + location.hash" 2>&1 | tr -d '"' | tr -d '\n')
  printf "%-20s | %-6s | %-26s | %s\n" "$f" "$sel" "$afterBase" "$afterDev"
done

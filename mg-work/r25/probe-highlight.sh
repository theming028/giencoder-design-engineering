set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
for f in dev.html base.html kanban.html; do
  $AB open "http://127.0.0.1:8866/pages/$f" >/dev/null 2>&1
  $AB set viewport 1440 900 >/dev/null 2>&1
  sleep 2.2
  echo "=== $f ==="
  $AB eval "(function(){var tl=document.querySelector('[role=\"tablist\"][aria-label=\"工作台切换\"]');if(!tl)return 'NO_TABLIST';return [].map.call(tl.querySelectorAll('[data-tab]'),function(b){return b.getAttribute('data-tab')+'|sel='+b.getAttribute('aria-selected')+'|svg='+(b.querySelector('svg')?1:0)+'|text='+JSON.stringify(b.textContent)}).join('  ;;  ')})()" 2>&1 | tail -3
done

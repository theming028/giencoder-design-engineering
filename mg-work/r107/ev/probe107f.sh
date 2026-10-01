set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
for W in 1440 1280 1100 1024; do
  "$NODE" "$CLI" open "file:///$ROOT/pages/conversation.html?v=$(date +%s)" >/dev/null 2>&1
  "$NODE" "$CLI" set viewport $W 900 >/dev/null 2>&1
  "$NODE" "$CLI" wait 2600 >/dev/null 2>&1
  "$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
  "$NODE" "$CLI" wait 900 >/dev/null 2>&1
  "$NODE" "$CLI" eval "$(cat $EV/p107f6.js)" > "$EV/f107w$W.log" 2>&1
  echo "done $W"
done

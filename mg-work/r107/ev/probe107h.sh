set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
echo "########## A. 右栏关闭态 ##########"
"$NODE" "$CLI" eval "$(cat $EV/p107h1.js)" > "$EV/h107-closed.log" 2>&1
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 1200 >/dev/null 2>&1
echo "########## B. 右栏展开态 ##########"
"$NODE" "$CLI" eval "$(cat $EV/p107h1.js)" > "$EV/h107-open.log" 2>&1
echo "done"

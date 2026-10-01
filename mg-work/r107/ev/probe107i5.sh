set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

# A. 1440 · 右栏关
"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107i5.js)" > "$EV/i107-s-1440closed.log" 2>&1

# B. 1440 · 右栏开
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 1200 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107i5.js)" > "$EV/i107-s-1440open.log" 2>&1

# C. 1024 · 右栏开
"$NODE" "$CLI" set viewport 1024 900 >/dev/null 2>&1
"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 1200 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107i5.js)" > "$EV/i107-s-1024open.log" 2>&1
echo done

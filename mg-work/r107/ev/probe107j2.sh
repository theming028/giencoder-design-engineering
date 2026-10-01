set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
RAW="$ROOT/mg-work/r107/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" eval "localStorage.removeItem('giencoder:r105-browse:v1')" >/dev/null 2>&1
"$NODE" "$CLI" reload >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 1300 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107j_snap.js)" >/dev/null 2>&1

# 进全屏
"$NODE" "$CLI" click "[data-td-max]" >/dev/null 2>&1
"$NODE" "$CLI" wait 800 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107j_snap.js)" >/dev/null 2>&1
"$NODE" "$CLI" screenshot "$RAW/j2-fullscreen.png" >/dev/null 2>&1

# 合成拖拽（两轮）
"$NODE" "$CLI" eval "$(cat $EV/p107j_drag.js)" >/dev/null 2>&1
"$NODE" "$CLI" wait 400 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107j_snap.js)" >/dev/null 2>&1

# 再进全屏 → 收起侧栏（验「收起退出全屏」）
"$NODE" "$CLI" click "[data-td-max]" >/dev/null 2>&1
"$NODE" "$CLI" wait 600 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107j_snap.js)" >/dev/null 2>&1
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107j_snap.js)" >/dev/null 2>&1

"$NODE" "$CLI" eval "$(cat $EV/p107j_dump.js)" > "$EV/i107j-2.log" 2>&1
echo "===== i107j-2.log ====="
cat "$EV/i107j-2.log"

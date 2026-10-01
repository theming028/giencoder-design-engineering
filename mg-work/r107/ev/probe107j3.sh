set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
RAW="$ROOT/mg-work/r107/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

boot () {  # $1 = 视口宽
  "$NODE" "$CLI" open "$URL" >/dev/null 2>&1
  "$NODE" "$CLI" eval "localStorage.removeItem('giencoder:r105-browse:v1')" >/dev/null 2>&1
  "$NODE" "$CLI" reload >/dev/null 2>&1
  "$NODE" "$CLI" set viewport "$1" 900 >/dev/null 2>&1
  "$NODE" "$CLI" wait 2600 >/dev/null 2>&1
  "$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
  "$NODE" "$CLI" wait 1300 >/dev/null 2>&1
}

# ---------- 1440：常态 → 全屏 → 还原 ----------
boot 1440
"$NODE" "$CLI" eval "$(cat $EV/p107j_snap.js)" >/dev/null 2>&1
"$NODE" "$CLI" screenshot ".td-browse-bar" "$RAW/j3-bar-1440-max.png" >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-max]" >/dev/null 2>&1
"$NODE" "$CLI" wait 700 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107j_snap.js)" >/dev/null 2>&1
"$NODE" "$CLI" screenshot ".td-browse-bar" "$RAW/j3-bar-1440-min.png" >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-max]" >/dev/null 2>&1
"$NODE" "$CLI" wait 700 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107j_snap.js)" >/dev/null 2>&1
"$NODE" "$CLI" screenshot ".td-browse" "$RAW/j3-panel-1440-restored.png" >/dev/null 2>&1

# ---------- 1024：全屏 + 拖拽 ----------
boot 1024
"$NODE" "$CLI" click "[data-td-max]" >/dev/null 2>&1
"$NODE" "$CLI" wait 700 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107j_snap.js)" >/dev/null 2>&1
"$NODE" "$CLI" screenshot "$RAW/j3-1024-fullscreen.png" >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107j_drag.js)" >/dev/null 2>&1
"$NODE" "$CLI" wait 400 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107j_snap.js)" >/dev/null 2>&1

"$NODE" "$CLI" eval "$(cat $EV/p107j_dump.js)" > "$EV/i107j-3.log" 2>&1
echo "done"

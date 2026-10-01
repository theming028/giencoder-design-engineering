set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
OUT="$ROOT/mg-work/r107/raw"
P="$ROOT/pages/conversation.html"

# ---------- 1) 1440 关态（① + ② 基线） ----------
"$NODE" "$CLI" open "file:///$P?v=$(date +%s)" >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 2800 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107g1.js)" > "$EV/g1-1440off.log" 2>&1
"$NODE" "$CLI" screenshot "$OUT/g1-stats.png" >/dev/null 2>&1

# ---------- 2) 1440 右栏开 + 技能浮窗 ----------
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" click "textarea" >/dev/null 2>&1
"$NODE" "$CLI" keyboard type "/" >/dev/null 2>&1
"$NODE" "$CLI" wait 800 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107g1.js)" > "$EV/g1-1440on.log" 2>&1
"$NODE" "$CLI" screenshot "$OUT/g2-skill1440.png" >/dev/null 2>&1

# ---------- 3) 1280 右栏开 + 技能浮窗 ----------
"$NODE" "$CLI" set viewport 1280 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" click "textarea" >/dev/null 2>&1
"$NODE" "$CLI" keyboard type "/" >/dev/null 2>&1
"$NODE" "$CLI" wait 800 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107g1.js)" > "$EV/g1-1280on.log" 2>&1
"$NODE" "$CLI" screenshot "$OUT/g3-skill1280.png" >/dev/null 2>&1

# ---------- 4) 1100 右栏开：alert 折行 ----------
"$NODE" "$CLI" set viewport 1100 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107g1.js)" > "$EV/g1-1100on.log" 2>&1
"$NODE" "$CLI" scrollintoview ".r93-alert" >/dev/null 2>&1
"$NODE" "$CLI" wait 600 >/dev/null 2>&1
"$NODE" "$CLI" screenshot "$OUT/g4-alert1100.png" >/dev/null 2>&1
echo "verify done"

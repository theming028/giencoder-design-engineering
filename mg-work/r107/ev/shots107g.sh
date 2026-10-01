set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
# ---- A. 1100 右栏开：把第一条 alert 滚进视野 ----
"$NODE" "$CLI" open "file:///$ROOT/pages/conversation.html?v=$(date +%s)" >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1100 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" scrollintoview ".r93-alert" >/dev/null 2>&1
"$NODE" "$CLI" wait 500 >/dev/null 2>&1
"$NODE" "$CLI" eval "(function(){var a=document.querySelectorAll('.r93-alert')[0];var r=a.getBoundingClientRect();window.__ay=Math.round(r.top);return JSON.stringify({y:Math.round(r.top),h:Math.round(r.height),sh:a.scrollHeight});})()" > "$ROOT/mg-work/r107/ev/f107g.log" 2>&1
"$NODE" "$CLI" screenshot "$OUT/f3-alert1100.png" >/dev/null 2>&1
# ---- B. 1280 右栏开：开技能浮窗 ----
"$NODE" "$CLI" open "file:///$ROOT/pages/conversation.html?v=$(date +%s)" >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1280 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" click "textarea" >/dev/null 2>&1
"$NODE" "$CLI" keyboard type "/" >/dev/null 2>&1
"$NODE" "$CLI" wait 800 >/dev/null 2>&1
"$NODE" "$CLI" screenshot "$OUT/f4-skill1280.png" >/dev/null 2>&1
echo "shots done"

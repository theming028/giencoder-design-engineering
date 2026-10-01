set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
RAW="$ROOT/mg-work/r107/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

# ② 右键菜单条目（键：文件头）
CTX='(function(){var p=document.querySelector(".td-diff-path");if(!p)return "no path";p.dispatchEvent(new MouseEvent("contextmenu",{bubbles:true,cancelable:true,clientX:640,clientY:300}));var h=document.querySelector(".td-ctxmenu");if(!h)return "no menu";var L=Array.prototype.map.call(h.querySelectorAll(".giencoder-dropdown-item .td-mm-name"),function(b){return (b.textContent||"").trim();});return JSON.stringify({open:!h.hasAttribute("hidden"),n:L.length,labels:L,hasFoldOne:(h.textContent||"").indexOf("此文件")>=0});})()'

open_review () {
  "$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
  "$NODE" "$CLI" wait 900 >/dev/null 2>&1
  "$NODE" "$CLI" click ".td-browse-add" >/dev/null 2>&1
  "$NODE" "$CLI" wait 500 >/dev/null 2>&1
  "$NODE" "$CLI" click "[data-td-open-mod='review']" >/dev/null 2>&1
  "$NODE" "$CLI" wait 900 >/dev/null 2>&1
}

# ---------- A. 1440 · 摘要页（③ ⑥ ①）----------
"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 1200 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107i4.js)" > "$EV/i107-v-summary.log" 2>&1
"$NODE" "$CLI" screenshot "$RAW/i2-summary.png" >/dev/null 2>&1

# ---------- B. 1440 · 审查页（④⑤ + ① 窄栏）----------
"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
open_review
"$NODE" "$CLI" eval "$(cat $EV/p107i4.js)" > "$EV/i107-v-review.log" 2>&1
"$NODE" "$CLI" screenshot "$RAW/i2-review.png" >/dev/null 2>&1
"$NODE" "$CLI" eval "$CTX" > "$EV/i107-v-ctx.log" 2>&1
"$NODE" "$CLI" screenshot "$RAW/i2-ctxmenu.png" >/dev/null 2>&1
"$NODE" "$CLI" screenshot ".mt-8" "$RAW/i2-stats-1440open.png" >/dev/null 2>&1

# ---------- C. 1440 · 窄栏出图（①：--av-browse-w=240 后的摘要来源卡）----------
"$NODE" "$CLI" eval "(function(){document.getElementById('av-browse-slot').style.setProperty('--av-browse-w','230px');return 'ok';})()" >/dev/null 2>&1
"$NODE" "$CLI" wait 400 >/dev/null 2>&1
"$NODE" "$CLI" screenshot "$RAW/i2-narrow-summary.png" >/dev/null 2>&1

# ---------- D. 1024 · 右栏开（主列变窄）统计行 ----------
"$NODE" "$CLI" set viewport 1024 900 >/dev/null 2>&1
"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 1200 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107i4.js)" > "$EV/i107-v-1024.log" 2>&1
"$NODE" "$CLI" screenshot ".mt-8" "$RAW/i2-stats-1024open.png" >/dev/null 2>&1
echo "done"

set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
RAW="$ROOT/mg-work/r107/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

CTX='(function(){var p=document.querySelector(".td-diff-path");if(!p)return "no path";p.dispatchEvent(new MouseEvent("contextmenu",{bubbles:true,cancelable:true,clientX:640,clientY:300}));var h=document.querySelector(".td-ctxmenu");if(!h)return "no menu";var L=Array.prototype.map.call(h.querySelectorAll(".giencoder-dropdown-item"),function(b){return (b.textContent||"").trim();});return JSON.stringify({open:!h.hasAttribute("hidden"),n:L.length,labels:L});})()'

"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1

# 开右栏 → 审查
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" click ".td-browse-add" >/dev/null 2>&1
"$NODE" "$CLI" wait 500 >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-open-mod='review']" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1

# ---- 1440：六指标 + 溢出普查 ----
"$NODE" "$CLI" eval "$(cat $EV/p107i1.js)" > "$EV/i107-1440.log" 2>&1
"$NODE" "$CLI" screenshot "$RAW/i1-1440-review.png" >/dev/null 2>&1

# ---- 右键菜单项清单（②）----
"$NODE" "$CLI" eval "$CTX" > "$EV/i107-ctx.log" 2>&1

# ---- 1024：六指标 + 溢出普查 ----
"$NODE" "$CLI" set viewport 1024 900 >/dev/null 2>&1
"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" click ".td-browse-add" >/dev/null 2>&1
"$NODE" "$CLI" wait 500 >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-open-mod='review']" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107i1.js)" > "$EV/i107-1024.log" 2>&1
"$NODE" "$CLI" screenshot "$RAW/i1-1024-review.png" >/dev/null 2>&1

# ---- 摘要页（③ td-sum-h / ⑥ r107-stats）----
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 1200 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107i1.js)" > "$EV/i107-summary.log" 2>&1
"$NODE" "$CLI" screenshot "$RAW/i1-summary.png" >/dev/null 2>&1
echo "done"

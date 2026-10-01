set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
RAW="$ROOT/mg-work/r107/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

"$NODE" "$CLI" open "$URL" >/dev/null 2>&1
"$NODE" "$CLI" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$CLI" wait 2600 >/dev/null 2>&1

# ---- A. 右栏关闭态（⑦：全屏按钮应可见）----
"$NODE" "$CLI" eval "$(cat $EV/p107h3.js)" > "$EV/h107-v-closed.log" 2>&1

# ---- 开右栏 → 切「审查」→ 开提交卡 ----
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" click ".td-browse-add" >/dev/null 2>&1
"$NODE" "$CLI" wait 500 >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-open-mod='review']" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-commit='1']" >/dev/null 2>&1
"$NODE" "$CLI" wait 500 >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-commit-act='commit']" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1

# ---- B. 右栏展开态（全部七条）----
"$NODE" "$CLI" eval "$(cat $EV/p107h3.js)" > "$EV/h107-v-open.log" 2>&1
"$NODE" "$CLI" screenshot "$RAW/h3-commit.png" >/dev/null 2>&1

"$NODE" "$CLI" click "[data-td-commit-x='1']" >/dev/null 2>&1
"$NODE" "$CLI" wait 400 >/dev/null 2>&1

# ---- C. 显示选项菜单（③ 选中态底色 + ④ 快捷键已去）----
"$NODE" "$CLI" click "[data-td-rv-opts='1']" >/dev/null 2>&1
"$NODE" "$CLI" wait 700 >/dev/null 2>&1
"$NODE" "$CLI" screenshot "$RAW/h3-opts-menu.png" >/dev/null 2>&1

# ---- D. + 菜单（② 标题已去 + ④ 快捷键已去）----
"$NODE" "$CLI" click ".td-browse-add" >/dev/null 2>&1
"$NODE" "$CLI" wait 700 >/dev/null 2>&1
"$NODE" "$CLI" screenshot "$RAW/h3-add-menu.png" >/dev/null 2>&1

# ---- E. 右键菜单（② 目标名行 + ④ 快捷键）----
"$NODE" "$CLI" eval "(function(){var t=document.querySelector('.td-browse-tab');if(!t)return 'no tab';t.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:640,clientY:60}));var h=document.querySelector('.td-ctxmenu');return JSON.stringify({open:!h.hasAttribute('hidden'),headDisp:(function(){var e=h.querySelector('.td-ctx-head');return e?getComputedStyle(e).display:'ABSENT';})(),keyDisp:(function(){var e=h.querySelector('.td-ctx-key');return e?getComputedStyle(e).display:'ABSENT';})(),heads:h.querySelectorAll('.td-ctx-head').length,keys:h.querySelectorAll('.td-ctx-key').length,text:(h.textContent||'').slice(0,60),r:(function(){var b=h.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height)];})()});})()" > "$EV/h107-v-ctx.log" 2>&1
"$NODE" "$CLI" screenshot "$RAW/h3-ctxmenu.png" >/dev/null 2>&1
echo "done"

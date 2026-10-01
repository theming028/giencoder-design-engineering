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
"$NODE" "$CLI" click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1

# --- 打开「审查」模块 ---
"$NODE" "$CLI" click ".td-browse-add" >/dev/null 2>&1
"$NODE" "$CLI" wait 500 >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-open-mod='review']" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1

# --- ① 提交卡：量 td-commit-in ---
"$NODE" "$CLI" click "[data-td-commit='1']" >/dev/null 2>&1
"$NODE" "$CLI" wait 500 >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-commit-act='commit']" >/dev/null 2>&1
"$NODE" "$CLI" wait 900 >/dev/null 2>&1
"$NODE" "$CLI" eval "$(cat $EV/p107h2.js)" > "$EV/h107-commit.log" 2>&1
"$NODE" "$CLI" screenshot "$RAW/h2-commit.png" >/dev/null 2>&1
"$NODE" "$CLI" click "[data-td-commit-x='1']" >/dev/null 2>&1
"$NODE" "$CLI" wait 400 >/dev/null 2>&1

# --- ② 显示选项菜单（4 个选中项）---
"$NODE" "$CLI" click "[data-td-rv-opts='1']" >/dev/null 2>&1
"$NODE" "$CLI" wait 700 >/dev/null 2>&1
"$NODE" "$CLI" screenshot "$RAW/h2-opts-menu.png" >/dev/null 2>&1

# --- ③ + 菜单（分组标题 + 快捷键）---
"$NODE" "$CLI" click ".td-browse-add" >/dev/null 2>&1
"$NODE" "$CLI" wait 700 >/dev/null 2>&1
"$NODE" "$CLI" screenshot "$RAW/h2-add-menu.png" >/dev/null 2>&1
echo "done"

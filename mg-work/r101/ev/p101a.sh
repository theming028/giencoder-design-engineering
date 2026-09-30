#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport "$W" 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"
"$NODE" "$AB" wait 1800
echo "=== [$W] 静态读数 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101a.js)"
echo "=== hover 展开头 .r93-fh ==="
"$NODE" "$AB" scrollintoview ".r93-fh" >/dev/null 2>&1
"$NODE" "$AB" hover ".r93-fh" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101h_fh.js)"
echo "=== hover 图标按钮 .r93-ib ==="
"$NODE" "$AB" scrollintoview ".r93-ib" >/dev/null 2>&1
"$NODE" "$AB" hover ".r93-ib" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101h_ib.js)"
echo "=== 打标 + 截图 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101tag.js)"
"$NODE" "$AB" scrollintoview "[data-r101-shot='bash']" >/dev/null 2>&1
"$NODE" "$AB" wait 300
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-before-bash.png" >/dev/null 2>&1
"$NODE" "$AB" scrollintoview "[data-r101-shot='okc']" >/dev/null 2>&1
"$NODE" "$AB" wait 300
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-before-okc.png" >/dev/null 2>&1
echo "=== done ==="

#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"
"$NODE" "$AB" wait 2200
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-after-sb.png" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101tag.js)"
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101shot.js)"
"$NODE" "$AB" scrollintoview "[data-r101-shot='bash']" >/dev/null 2>&1
"$NODE" "$AB" wait 400
"$NODE" "$AB" screenshot "[data-r101-shot='bash']" "mg-work/r101/raw/r101-after-bashhead.png" >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101jump.js)"
"$NODE" "$AB" hover "[data-r101-fc]" >/dev/null 2>&1
"$NODE" "$AB" wait 300
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-fc-hover.png" >/dev/null 2>&1
echo "=== done ==="

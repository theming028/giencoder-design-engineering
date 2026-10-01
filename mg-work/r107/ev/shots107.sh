#!/usr/bin/env bash
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
AB() { "$NODE" "$CLI" "$@"; }
AB open "file:///$ROOT/pages/conversation.html?v=$(date +%s)" >/dev/null 2>&1
AB set viewport 1440 900 >/dev/null 2>&1
AB wait 2600 >/dev/null 2>&1
AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
AB wait 800 >/dev/null 2>&1
AB screenshot "$OUT/g1-files.png" >/dev/null 2>&1
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB screenshot "$OUT/g2-modmenu.png" >/dev/null 2>&1
AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB screenshot "$OUT/g3-review.png" >/dev/null 2>&1
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB click '[data-td-open-mod="terminal"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB focus ".td-term" >/dev/null 2>&1
AB press l >/dev/null 2>&1
AB press s >/dev/null 2>&1
AB press Enter >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB screenshot "$OUT/g4-terminal.png" >/dev/null 2>&1
AB click ".td-browse-add" >/dev/null 2>&1
AB wait 250 >/dev/null 2>&1
AB click '[data-td-open-mod="browser"]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click ".td-url-annot" >/dev/null 2>&1
AB wait 300 >/dev/null 2>&1
AB click ".td-page-card" >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB screenshot "$OUT/g5-browser.png" >/dev/null 2>&1
AB click ".td-page-card" >/dev/null 2>&1
AB wait 200 >/dev/null 2>&1
AB click '.td-elnote [data-td-elnote-cancel]' >/dev/null 2>&1
AB wait 200 >/dev/null 2>&1
# 划词 → 侧边聊天
AB eval "(function(){var m=document.querySelector('div:has(> main) > main')||document.querySelector('main');var el=document.elementFromPoint(500,300);var hop=0;while(el&&el!==m&&hop<6){if((el.textContent||'').trim().length>16)break;el=el.parentElement;hop++;}var rg=document.createRange();rg.selectNodeContents(el);var s=window.getSelection();s.removeAllRanges();s.addRange(rg);document.dispatchEvent(new MouseEvent('mouseup',{bubbles:true,clientX:500,clientY:300}));return 'ok';})()" >/dev/null 2>&1
AB wait 500 >/dev/null 2>&1
AB screenshot "$OUT/g6-selbar.png" >/dev/null 2>&1
AB click '[data-td-side-ask]' >/dev/null 2>&1
AB wait 600 >/dev/null 2>&1
AB focus ".td-side-ta" >/dev/null 2>&1
AB fill ".td-side-ta" "暗色档要不要也给这个分叉单独配色？" >/dev/null 2>&1
AB press Enter >/dev/null 2>&1
AB wait 800 >/dev/null 2>&1
AB screenshot "$OUT/g7-sidechat.png" >/dev/null 2>&1
echo "shots done"

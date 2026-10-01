#!/usr/bin/env bash
# 第十拍 行为回归：Esc 关 / 点空白关 / 重开位置一致 / 右键菜单未受影响
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r107/ev"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"

step() { "$NODE" "$CLI" "$@" >/dev/null 2>&1; }
st() { "$NODE" "$CLI" eval "JSON.stringify({optsOpen:!document.querySelector('.td-rv-opts').hasAttribute('hidden'),scopeOpen:!document.querySelector('.td-rv-scope-menu').hasAttribute('hidden'),ctxOpen:!document.querySelector('.td-ctxmenu').hasAttribute('hidden'),optsTop:getComputedStyle(document.querySelector('.td-rv-opts')).top,optsLeft:getComputedStyle(document.querySelector('.td-rv-opts')).left,ctxTop:getComputedStyle(document.querySelector('.td-ctxmenu')).top,ctxLeft:getComputedStyle(document.querySelector('.td-ctxmenu')).left})" 2>&1 | tail -1; }

step open "$URL"
step set viewport 1440 900
step wait 2600
step click ".r93-baract[data-r93-browse]"
step wait 1500
step click ".td-browse-add"; step wait 400
step click "[data-td-open-mod='review']"; step wait 800

echo "T1-open";  step click "[data-td-rv-opts]"; step wait 450; st
echo "T2-esc";   step press Escape; step wait 400; st
echo "T3-reopen"; step click "[data-td-rv-opts]"; step wait 450; st
echo "T4-clickbody"; step click ".td-rv-body"; step wait 400; st

echo "T5-scope-then-blank"; step click "[data-td-rv-scope]"; step wait 400; st
step click ".td-mod-bar"; step wait 400; st

echo "T6-ctxmenu"; step eval "document.querySelector('.td-diff-h').dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:900,clientY:300}))"; step wait 400; st
step press Escape; step wait 300; st

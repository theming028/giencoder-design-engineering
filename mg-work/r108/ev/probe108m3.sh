#!/usr/bin/env bash
# 第十二拍复查：点「文件树」按钮**不再弹「已执行」** + 补一张干净的抽屉图。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
RAW="$ROOT/mg-work/r108/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
step() { "$NODE" "$CLI" "$@" >/dev/null 2>&1; }
run() { "$NODE" "$CLI" "$@" 2>&1; }

step open "$URL"; step set viewport 1440 900; step wait 2800
step click ".r93-baract[data-r93-browse]"; step wait 1400
step click ".td-browse-add"; step wait 400
step click "[data-td-open-mod='review']"; step wait 700

# 点「文件树」按钮，同一次 eval 里读 toast（避免 1.4s 自动收起）
run eval "(function(){var b=document.querySelector('[data-td-rv-act=\"tree\"]');b.click();var t=document.querySelector('.td-toast');return JSON.stringify({treeHidden:document.querySelector('[data-td-tree]').hasAttribute('hidden'),toastShown:t?!t.hasAttribute('hidden'):null,toastText:t?t.textContent:null,btnAria:b.getAttribute('aria-expanded')});})()"
step wait 500
step screenshot ".td-browse" "$RAW/m-1440-tree.png"
step screenshot ".td-tree-panel" "$RAW/m-1440-tree-panel.png"
# 折叠 games
step eval "(function(){var r=[].slice.call(document.querySelectorAll('.td-tf'));for(var i=0;i<r.length;i++){var e=r[i].querySelector('.td-tf-name');if(e&&e.textContent==='games'){r[i].click();return 1;}}return 0;})()"
step wait 400
step screenshot ".td-tree-panel" "$RAW/m-1440-tree-fold.png"
# 关掉抽屉，再点一次「定位」按钮，确认老动作没被带坏
step eval "document.querySelector('[data-td-tree-x]').click()"; step wait 500
run eval "(function(){var b=document.querySelector('[data-td-rv-act=\"reveal\"]');b.click();var t=document.querySelector('.td-toast');return JSON.stringify({toastShown:t?!t.hasAttribute('hidden'):null,toastText:t?t.textContent:null,activeTab:(document.querySelector('.td-browse-tab.is-active .td-tab-name')||{}).textContent});})()"
echo done

#!/usr/bin/env bash
# r107 第三拍 · 补充复测：修掉上一轮两处**探针自身**的瑕疵
#   ① B4 用的选择器 `.td-diff` 量到的是 article 的 display（不是 rows）⇒ 没验到统一视图折叠
#   ② toast 用「点完再另起一次 eval」读 ⇒ agent-browser 进程开销 >1.4s，早已自动隐藏
#      ⇒ 改成**同一个 eval 内**先点后读（同步，必然还开着）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
OUT="$ROOT/mg-work/r107/raw"
TS=$(date +%s)
AB() { "$NODE" "$CLI" "$@"; }
URL="file:///$ROOT/pages/conversation.html?v=$TS"

openreview() {
  AB open "$URL" >/dev/null 2>&1
  AB set viewport 1440 900 >/dev/null 2>&1
  AB wait 2800 >/dev/null 2>&1
  AB click ".r93-baract[data-r93-browse]" >/dev/null 2>&1
  AB wait 800 >/dev/null 2>&1
  AB click "[data-td-add]" >/dev/null 2>&1
  AB wait 400 >/dev/null 2>&1
  AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
  AB wait 900 >/dev/null 2>&1
}

echo "############ H 统一视图下的折叠（正确选择器） ############"
openreview
echo "--- H1 初始：第 1 个文件 is-open，统一行可见"
AB eval "JSON.stringify({open:document.querySelector('.td-diff').classList.contains('is-open'),uni:getComputedStyle(document.querySelector('.td-diff-rows:not(.td-diff-split)')).display})" 2>&1
echo "--- H2 折叠 → 统一行应 none"
AB click "[data-td-diff]:nth-child(1) [data-td-diff-h]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({open:document.querySelector('.td-diff').classList.contains('is-open'),uni:getComputedStyle(document.querySelector('.td-diff-rows:not(.td-diff-split)')).display,note:getComputedStyle(document.querySelector('.td-note')).display})" 2>&1
echo "--- H3 展开 → 统一行应 block"
AB click "[data-td-diff]:nth-child(1) [data-td-diff-h]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({open:document.querySelector('.td-diff').classList.contains('is-open'),uni:getComputedStyle(document.querySelector('.td-diff-rows:not(.td-diff-split)')).display})" 2>&1
echo "--- H4 并排态 + 折叠 → 统一行/并排行/评论 三者都该隐藏"
AB click "[data-td-rv-opts]" >/dev/null 2>&1
AB wait 350 >/dev/null 2>&1
AB click '[data-td-rv-view="split"]' >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB click "[data-td-diff]:nth-child(1) [data-td-diff-h]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({open:document.querySelector('.td-diff').classList.contains('is-open'),uni:getComputedStyle(document.querySelector('.td-diff-rows:not(.td-diff-split)')).display,split:getComputedStyle(document.querySelector('.td-diff-split')).display,note:getComputedStyle(document.querySelector('.td-note')).display})" 2>&1
AB screenshot "$OUT/y10-split-all-hidden.png" >/dev/null 2>&1
echo "--- H5 展开回来（并排）"
AB click "[data-td-diff]:nth-child(1) [data-td-diff-h]" >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({uni:getComputedStyle(document.querySelector('.td-diff-rows:not(.td-diff-split)')).display,split:getComputedStyle(document.querySelector('.td-diff-split')).display})" 2>&1

echo
echo "############ I 动作反馈 toast（同一次 eval 内先点后读） ############"
echo "--- I1 「复制 diff」"
AB eval "(function(){document.querySelector('[data-td-rv-act=\"copy\"]').click();var t=document.querySelector('.td-toast');return t.hasAttribute('hidden')+' | '+t.textContent;})()" 2>&1
echo "--- I2 「在文件树中定位」→ 自动切到「文件」标签 + toast"
AB eval "(function(){document.querySelector('[data-td-rv-act=\"reveal\"]').click();var t=document.querySelector('.td-toast');return t.hasAttribute('hidden')+' | '+t.textContent+' | active='+document.querySelector('.td-browse-tab.is-active .td-tab-name').textContent;})()" 2>&1
AB wait 600 >/dev/null 2>&1
echo "--- I3 回到审查 + 「暂存」"
AB eval "(function(){document.querySelector('.td-browse-tab[data-td-mod=\"review\"]').click();var b=document.querySelector('[data-td-stage]');b.click();var t=document.querySelector('.td-toast');return b.textContent+' | '+b.classList.contains('is-staged')+' | '+t.hasAttribute('hidden')+' | '+t.textContent;})()" 2>&1
AB screenshot "$OUT/y11-stage-toast.png" >/dev/null 2>&1
echo "--- I4 「Open PR」"
AB eval "(function(){document.querySelector('[data-td-rv-act=\"pr\"]').click();var t=document.querySelector('.td-toast');return t.hasAttribute('hidden')+' | '+t.textContent;})()" 2>&1

echo
echo "############ J 「折叠 N 行未改动」展开 ############"
echo "--- J1 初始：4 个折叠条，隐藏行 6 条"
AB eval "JSON.stringify({more:document.querySelectorAll('[data-td-more]').length,rows:document.querySelectorAll('[data-td-more-row]').length,rowsShown:document.querySelectorAll('[data-td-more-row]:not([hidden])').length,label:document.querySelector('[data-td-more]').textContent})" 2>&1
echo "--- J2 点第 1 个折叠条 → 文案翻 + 放出 4 行"
AB click '[data-td-more]' >/dev/null 2>&1
AB wait 450 >/dev/null 2>&1
AB eval "JSON.stringify({rowsShown:document.querySelectorAll('[data-td-more-row]:not([hidden])').length,label:document.querySelector('[data-td-more]').textContent})" 2>&1
AB screenshot "$OUT/y12-more-expanded.png" >/dev/null 2>&1
echo "--- J3 再点 → 收起"
AB click '[data-td-more]' >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB eval "JSON.stringify({rowsShown:document.querySelectorAll('[data-td-more-row]:not([hidden])').length,label:document.querySelector('[data-td-more]').textContent})" 2>&1

echo
echo "############ K 标签关闭 / 重开 + 最大化回归 ############"
echo "--- K1 关掉「审查」标签（还剩「文件」）"
AB click '.td-browse-tab[data-td-mod="review"] [data-td-tab-x]' >/dev/null 2>&1
AB wait 600 >/dev/null 2>&1
AB eval "JSON.stringify({tabs:[].map.call(document.querySelectorAll('.td-browse-tab .td-tab-name'),function(e){return e.textContent;}),active:document.querySelector('.td-browse-tab.is-active .td-tab-name').textContent,singleHidden:getComputedStyle(document.querySelector('.td-tab-x')).display})" 2>&1
echo "--- K2 从 `+` 菜单重开「审查」"
AB click "[data-td-add]" >/dev/null 2>&1
AB wait 400 >/dev/null 2>&1
AB click '[data-td-open-mod="review"]' >/dev/null 2>&1
AB wait 800 >/dev/null 2>&1
AB eval "JSON.stringify({tabs:[].map.call(document.querySelectorAll('.td-browse-tab .td-tab-name'),function(e){return e.textContent;}),active:document.querySelector('.td-browse-tab.is-active .td-tab-name').textContent})" 2>&1
echo "--- K3 最大化 / 还原"
AB eval "JSON.stringify({before:document.getElementById('av-browse-slot').style.getPropertyValue('--av-browse-w')})" 2>&1
AB click '[data-td-max]' >/dev/null 2>&1
AB wait 600 >/dev/null 2>&1
AB eval "JSON.stringify({max:document.getElementById('av-browse-slot').style.getPropertyValue('--av-browse-w'),pressed:document.querySelector('[data-td-max]').getAttribute('aria-pressed')})" 2>&1
AB click '[data-td-max]' >/dev/null 2>&1
AB wait 600 >/dev/null 2>&1
AB eval "JSON.stringify({back:document.getElementById('av-browse-slot').style.getPropertyValue('--av-browse-w'),pressed:document.querySelector('[data-td-max]').getAttribute('aria-pressed')})" 2>&1

echo "############ done ############"

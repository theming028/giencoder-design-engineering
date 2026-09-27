#!/usr/bin/env bash
# 第28轮交付截图：默认态 / 描述配图 / 添加菜单 / 技能面板 / 大模型下拉 / 两栏互换
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/task-detail.html"
OUT="mg-work/r28/shots"

mkdir -p "$OUT"

# ---- 1. 默认态（视口 + 整页） ----
$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 3.0
$AB screenshot "$OUT/01-default.png" >/dev/null 2>&1

# ---- 2. 描述区配图（滚动到描述区） ----
$AB eval "(function(){var d=document.querySelector('.td-desc');if(d){d.scrollIntoView({block:'center'});}})()" >/dev/null 2>&1
sleep 0.6
$AB screenshot "$OUT/03-desc-img.png" >/dev/null 2>&1

# ⚠️ 验收铁律：截图必须比 md5 —— 若两张理应不同的截图哈希一致，说明画面根本没变
#    （第 28 轮正是靠这一步发现「大模型下拉 display:block 但 visibility:hidden ⇒ 未绘制」）。
md5sum "$OUT"/*.png

# ---- 3. 添加菜单展开 ----
$AB eval "(function(){window.scrollTo(0,0);document.querySelector('[data-td-add-btn]').click();})()" >/dev/null 2>&1
sleep 0.5
$AB screenshot "$OUT/04-add-pop.png" >/dev/null 2>&1
$AB eval "(function(){document.dispatchEvent(new CustomEvent('td:close-popovers'));})()" >/dev/null 2>&1
sleep 0.3

# ---- 4. 技能面板展开 ----
$AB eval "(function(){document.querySelector('[data-td-skill-btn]').click();})()" >/dev/null 2>&1
sleep 0.5
$AB screenshot "$OUT/05-skill-pop.png" >/dev/null 2>&1
$AB eval "(function(){document.dispatchEvent(new CustomEvent('td:close-popovers'));})()" >/dev/null 2>&1
sleep 0.3

# ---- 5. 大模型下拉展开 ----
$AB eval "(function(){var s=[].slice.call(document.querySelectorAll('.td-composer .giencoder-select')).filter(function(e){return e.querySelector('.giencoder-select-view-text');});s[s.length-1].querySelector('.giencoder-select-view').click();})()" >/dev/null 2>&1
sleep 0.5
$AB screenshot "$OUT/06-model-pop.png" >/dev/null 2>&1
$AB eval "(function(){document.dispatchEvent(new CustomEvent('td:close-popovers'));})()" >/dev/null 2>&1
sleep 0.3

# ---- 6. 两栏互换态 ----
$AB eval "JSON.stringify((function(){window.__l=document.querySelector('.td-left');document.querySelector('.td-root').classList.add('is-swapped');return {cls:document.querySelector('.td-root').className};})())" >/dev/null 2>&1
sleep 0.6
$AB screenshot "$OUT/07-swapped.png" >/dev/null 2>&1
$AB eval "(function(){document.querySelector('.td-root').classList.remove('is-swapped');})()" >/dev/null 2>&1

echo "SHOTS_DONE"
ls -la "$OUT"

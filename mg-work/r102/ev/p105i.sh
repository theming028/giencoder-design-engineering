#!/usr/bin/env bash
# r105 ① 逐页实测：点 aside 里的「会话任务」是否跳到 conversation.html
set -u
cd /e/GienCoder/giencoder-design-engineering || exit 1
NODE="/c/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="/c/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
V=$(date +%s)

for P in base task-detail avatar automation skills; do
  "$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
  "$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$P.html?v=$V" >/dev/null 2>&1
  "$NODE" "$AB" wait 2600 >/dev/null 2>&1
  before=$("$NODE" "$AB" eval "location.href.split('/').pop()" 2>&1 | tr -d '"')
  # 真鼠标点第一枚「会话任务」（min-w-0 + flex-1 的那类）
  "$NODE" "$AB" eval "(function(){var a=document.querySelector('aside');var bs=[].slice.call(a.querySelectorAll('button'));var s=bs.filter(function(b){return b.classList.contains('min-w-0')&&b.classList.contains('flex-1')});s[0].setAttribute('data-p105i','1');return s.length;})()" >/dev/null 2>&1
  "$NODE" "$AB" click '[data-p105i="1"]' >/dev/null 2>&1
  "$NODE" "$AB" wait 1200 >/dev/null 2>&1
  after=$("$NODE" "$AB" eval "location.href.split('/').pop()" 2>&1 | tr -d '"')
  echo "$(printf '%-13s' $P) before=$before → after=$after"
done

echo
echo "=== 负例：点「分组标题」「新会话」不该跳 ==="
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/base.html?v=$(date +%s)" >/dev/null 2>&1
"$NODE" "$AB" wait 2600 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var a=document.querySelector('aside');var bs=[].slice.call(a.querySelectorAll('button'));var h=bs.filter(function(b){return b.classList.contains('rounded-md')&&b.classList.contains('py-0')});h[0].setAttribute('data-p105i-h','1');return h.length;})()" >/dev/null 2>&1
"$NODE" "$AB" click '[data-p105i-h="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 900 >/dev/null 2>&1
echo "分组标题后: $("$NODE" "$AB" eval "location.href.split('/').pop()" 2>&1 | tr -d '"')"

"$NODE" "$AB" eval "(function(){var a=document.querySelector('aside');var bs=[].slice.call(a.querySelectorAll('button'));var n=bs.filter(function(b){return (b.textContent||'').indexOf('新会话')>=0});if(n[0]){n[0].setAttribute('data-p105i-n','1');return 'ok';}return 'none';})()" >/dev/null 2>&1
"$NODE" "$AB" click '[data-p105i-n="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 900 >/dev/null 2>&1
echo "「新会话」后: $("$NODE" "$AB" eval "location.href.split('/').pop()" 2>&1 | tr -d '"')"

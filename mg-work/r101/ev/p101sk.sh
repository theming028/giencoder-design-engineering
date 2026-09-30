#!/usr/bin/env bash
# ⑪ 骨架屏取证：**临时**把退场延时 1100ms 改成 60000ms（只为取证），拍完立刻重跑 apply101.py 还原。
# 全部动作在这一次 bash 调用里跑完（同一时刻只有一个 UI 进程）。
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"

python - <<'PY'
import io
p = 'pages/conversation.html'
s = io.open(p, encoding='utf-8').read()
n = s.count('}, 1100);')
print('  temp-patch: "}, 1100);" 命中 %d 次' % n)
if n != 1:
    raise SystemExit('!! 锚点不唯一，放弃取证（页面未改动）')
io.open(p, 'w', encoding='utf-8').write(s.replace('}, 1100);', '}, 60000);'))
print('  已临时改写为 60000ms')
PY

TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS"
"$NODE" "$AB" wait 900
echo "=== [⑪] 临时长驻（延时 60s）读数 ==="
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101sk.js)"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-sk-on.png" >/dev/null 2>&1
"$NODE" "$AB" wait 600
"$NODE" "$AB" eval "$(cat mg-work/r101/ev/p101sk.js)"

echo "=== 还原 ==="
python mg-work/r101/apply101.py
python - <<'PY'
import io
s = io.open('pages/conversation.html', encoding='utf-8').read()
print('  还原核对：60000 残留 %d 处；1100 命中 %d 处' % (s.count('60000'), s.count('}, 1100);')))
PY
echo "=== done ==="

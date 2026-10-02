#!/usr/bin/env bash
# r109 第三拍 ③-c：基础工作台 5 页「暗色档下的硬值清单」侦察。
#   ★ 先在真机里 __giTheme.set('dark')，再跑 p-hard.js 数「亮底 / 暗字」两类硬值。
#   用法： bash mg-work/r109/ev/theme/scan-hard.sh [page ...]（缺省 = 全部 5 页）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev/theme"
TS=$(date +%s)
run() { "$NODE" "$CLI" "$@" 2>&1; }

PAGES="${*:-base avatar automation skills settings}"

run set viewport 1440 900 > "$EV/h-set.log" 2>&1
for PAGE in $PAGES; do
  run open "file:///$ROOT/pages/$PAGE.html?v=$TS" > "$EV/h-open-$PAGE.log" 2>&1
  run wait 3800 > "$EV/h-wait-$PAGE.log" 2>&1
  # 挂暗色档（走机制出口，与用户点设置页同一条路）
  run eval "window.__giTheme.set('dark'); window.__giTheme.isDark()" > "$EV/h-theme-$PAGE.log" 2>&1
  run wait 600 > /dev/null 2>&1
  run eval "$(cat "$EV/p-hard.js")" > "$EV/hard-$PAGE.json.raw" 2>&1
  python -c "
import json,io
raw=io.open(r'$EV/hard-$PAGE.json.raw',encoding='utf-8').read().strip()
try: d=json.loads(raw)
except Exception as e:
    print('  PARSE_FAIL', e, raw[:160]); raise SystemExit(0)
if isinstance(d,str): d=json.loads(d)
io.open(r'$EV/hard-$PAGE.json','w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=1))
print('%-12s groups=%d' % (d['page'], d['groups']))
bg=[x for x in d['items'] if x['needBg']]
fg=[x for x in d['items'] if x['needFg'] and not x['needBg']]
print('   亮底 %d 组 / 暗字 %d 组' % (len(bg), len(fg)))
for x in bg[:14]:
    print('     BG n=%-3d %-8s %-42s %-20s %s' % (x['n'],x['tag'],(x['cls'][:42] or '(无类)'),x['bg'],x['inline'][:40]))
for x in fg[:10]:
    print('     FG n=%-3d %-8s %-42s %-20s %s' % (x['n'],x['tag'],(x['cls'][:42] or '(无类)'),x['fg'],x['inline'][:40]))
"
done

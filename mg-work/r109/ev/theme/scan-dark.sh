#!/usr/bin/env bash
# r109 第三拍 ③-c：基础工作台 5 页「浅 / 暗」双档取证 + 暗色档硬值复扫。
#   浅色截图 = 回归基线（必须与改动前一致）；暗色截图 = 适配效果。
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev/theme"; RAW="$ROOT/mg-work/r109/raw/theme-dark"
mkdir -p "$RAW"
TS=$(date +%s)
run() { "$NODE" "$CLI" "$@" 2>&1; }

PAGES="${*:-base avatar automation skills settings}"
run set viewport 1440 900 > "$EV/d-set.log" 2>&1
for PAGE in $PAGES; do
  run open "file:///$ROOT/pages/$PAGE.html?v=$TS" > "$EV/d-open-$PAGE.log" 2>&1
  run wait 3800 > /dev/null 2>&1
  run eval "window.__giTheme.set('light'); window.__giTheme.get()" > /dev/null 2>&1
  run wait 400 > /dev/null 2>&1
  run screenshot "$RAW/$PAGE-light.png" > /dev/null 2>&1
  run eval "window.__giTheme.set('dark'); window.__giTheme.get()" > "$EV/d-theme-$PAGE.log" 2>&1
  run wait 800 > /dev/null 2>&1
  run screenshot "$RAW/$PAGE-dark.png" > /dev/null 2>&1
  run eval "$(cat "$EV/p-hard.js")" > "$EV/hard2-$PAGE.json.raw" 2>&1
  python -c "
import json,io,os
raw=io.open(r'$EV/hard2-$PAGE.json.raw',encoding='utf-8').read().strip()
try: d=json.loads(raw)
except Exception as e:
    print('  %-12s PARSE_FAIL %s' % ('$PAGE', raw[:120])); raise SystemExit(0)
if isinstance(d,str): d=json.loads(d)
io.open(r'$EV/hard2-$PAGE.json','w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=1))
bg=[x for x in d['items'] if x['needBg']]; fg=[x for x in d['items'] if x['needFg'] and not x['needBg']]
print('%-12s groups=%-4d 亮底 %d / 暗字 %d' % (d['page'], d['groups'], len(bg), len(fg)))
for x in bg[:12]:
    print('     BG n=%-3d %-42s %-20s %s' % (x['n'],(x['cls'][:42] or '(无类)'),x['bg'],x['inline'][:34]))
for x in fg[:8]:
    print('     FG n=%-3d %-42s %-20s %s' % (x['n'],(x['cls'][:42] or '(无类)'),x['fg'],x['inline'][:34]))
"
done
echo "截图 → $RAW"

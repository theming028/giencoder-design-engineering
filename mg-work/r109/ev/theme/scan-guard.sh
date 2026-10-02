#!/usr/bin/env bash
# r109 第三拍 ③ 护栏逐页实测：p-guard.js 走全部 10 页。
# ★★ 铁律：agent-browser 的 stdout **绝不能接管道**（CLI 把 stdout 交给常驻守护进程
#   ⇒ 管道永不 EOF ⇒ `| tail` 永久等待）。一律重定向到文件。
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
EV="mg-work/r109/ev/theme"

"$NODE" "$CLI" close --all >"$EV/g-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$EV/g-set.log" 2>&1

for pg in base avatar automation skills settings conversation dev kanban req-kanban task-detail; do
  TS=$(date +%s%N)
  "$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$pg.html?v=$TS" >"$EV/g-open-$pg.log" 2>&1
  "$NODE" "$CLI" wait 4200 >"$EV/g-wait-$pg.log" 2>&1
  "$NODE" "$CLI" eval "$(cat "$EV/p-guard.js")" >"$EV/g-$pg.json" 2>&1
done

"$NODE" "$CLI" close --all >"$EV/g-close2.log" 2>&1
echo "=== 护栏实测（10 页）==="
python - <<'PY'
import io, json, glob, os
rows = []
for f in sorted(glob.glob('mg-work/r109/ev/theme/g-*.json')):
    try:
        d = json.load(io.open(f, encoding='utf-8'))
        if isinstance(d, str):
            d = json.loads(d)
    except Exception as e:
        rows.append((os.path.basename(f), 'PARSE_FAIL', str(e)))
        continue
    rows.append((d.get('page'), d.get('supported'), d.get('attr1'),
                 d.get('mode1'), d.get('bg1') if 'bg1' in d else d.get('tok1', {}).get('bg1'),
                 d.get('shellBg'), d.get('darkPaint')))
print('%-18s %-6s %-6s %-6s %-10s %-18s %s' % ('页', '适配', '切后属性', '档位', 'bg1', '外壳底色', '真暗'))
for r in rows:
    print('%-18s %-6s %-6s %-6s %-10s %-18s %s' % tuple(str(x) for x in r))
PY

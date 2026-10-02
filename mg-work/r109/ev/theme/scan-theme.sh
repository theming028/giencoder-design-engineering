#!/usr/bin/env bash
# r109 第三拍 ③-b：基础工作台 5 页的浅/暗双档侦察（一次 eval 拿两档数据）
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev/theme"; RAW="$ROOT/mg-work/r109/raw/theme"
mkdir -p "$RAW"
TS=$(date +%s)
run() { "$NODE" "$CLI" "$@" 2>&1; }

run set viewport 1440 900 > "$EV/t-set.log" 2>&1
for PAGE in base avatar automation skills settings; do
  run open "file:///$ROOT/pages/$PAGE.html?v=$TS" > "$EV/t-open-$PAGE.log" 2>&1
  run wait 3600 > "$EV/t-wait-$PAGE.log" 2>&1
  run eval "$(cat "$EV/p-theme.js")" > "$EV/$PAGE.json" 2>&1
  echo "########## $PAGE ##########"
  python -c "
import json,sys
raw=open(r'$EV/$PAGE.json',encoding='utf-8').read().strip()
try: d=json.loads(raw)
except Exception as e:
    print('PARSE_FAIL', e, raw[:200]); sys.exit(0)
if isinstance(d,str): d=json.loads(d)
for k in ('light','dark'):
    o=d[k]
    print(' [%s] mode=%s attr=%s data=%s stored=%s colorScheme=%s' % (k,o['mode'],o['attr'],o['dataAttr'],o['stored'],o['colorScheme']))
    print('       bodyBg=%s  color=%s  seg=%s' % (o['bodyBg'],o['titleColor'],o['segPressed']))
    print('       low=%d bright=%d' % (o['lowCount'],o['brightCount']))
    for x in o['lowText'][:6]:
        print('         LOW  r=%-5s %-26s fg=%-20s bg=%-20s %s' % (x['r'],x['sel'][:26],x['fg'],x['bg'],x['t']))
    for x in o['brightBg'][:6]:
        print('         BRIGHT %-24s %-22s %s' % (x['sel'][:24],x['bg'],x['box']))
"
done

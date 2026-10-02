#!/usr/bin/env bash
# r109 第十一拍 · 品牌 LOGO 双档实测（canvas 采样 <img> 内部像素 + [fill] 规则命中数）
# 用法：bash scan-brand.sh base
set -u
cd "$(dirname "$0")/../../../.." || exit 1

NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
EV="mg-work/r109/ev/theme"; TMP="$EV/tmp"
PG="${1:-base}"
OUT="mg-work/r109/raw/brand11"
mkdir -p "$OUT" "$TMP"
TS=$(date +%s%N)

"$NODE" "$CLI" close --all >"$TMP/br-close.log" 2>&1
"$NODE" "$CLI" set viewport 1440 900 >"$TMP/br-set.log" 2>&1
"$NODE" "$CLI" open "file:///E:/GienCoder/giencoder-design-engineering/pages/$PG.html?v=$TS" >"$OUT/open.log" 2>&1
"$NODE" "$CLI" wait 4500 >"$TMP/br-w.log" 2>&1
"$NODE" "$CLI" eval "$(cat "$EV/p-brand3.js")" >"$OUT/init.log" 2>&1

for TH in light dark; do
  "$NODE" "$CLI" eval "window.__giTheme.set('$TH'); 'T'" >"$TMP/br-t-$TH.log" 2>&1
  "$NODE" "$CLI" wait 1200 >"$TMP/br-w-$TH.log" 2>&1
  "$NODE" "$CLI" eval "JSON.stringify(window.__brand3())" >"$OUT/$PG-$TH.json" 2>&1
  "$NODE" "$CLI" screenshot "$OUT/$PG-$TH.png" >"$TMP/br-shot-$TH.log" 2>&1
  echo "done $PG/$TH"
done

"$NODE" "$CLI" close --all >"$TMP/br-close2.log" 2>&1

# 裁剪 logo 区域放大（用 Python）
"$PY" - "$OUT" "$PG" <<'PYEOF' 2>&1
import sys, os
from PIL import Image
out, pg = sys.argv[1], sys.argv[2]
for th in ('light','dark'):
    p = os.path.join(out, '%s-%s.png' % (pg, th))
    if not os.path.exists(p): continue
    im = Image.open(p).convert('RGB')
    im.crop((690,262,1010,296)).resize((1280,136), Image.NEAREST).save(os.path.join(out,'crop-%s-%s.png'%(pg,th)))
    print('crop', th, im.size)
PYEOF
echo "=== done · 产物 $OUT ==="

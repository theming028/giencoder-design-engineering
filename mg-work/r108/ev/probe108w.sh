#!/usr/bin/env bash
# r108 第十九拍 · ① 右栏划词浮条：真鼠标拖选取证
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r108/ev"
RAW="$ROOT/mg-work/r108/raw"
TAG="${1:-before}"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
JS="$(cat "$EV/p108w.js")"
run() { "$NODE" "$CLI" "$@" 2>&1; }
ev()  { run eval "window.__M='$1'; $JS"; }
step() { run "$@" >/dev/null; }

# 把 eval 的 JSON 里 drag 坐标抽出来：echo "x1 y1 x2 y2"
dragrc() {
  "$PY" -c "
import json,sys
s=sys.stdin.read()
d=json.JSONDecoder(); i=s.find('{'); o=None
while i>=0:
    try:
        o,_=d.raw_decode(s,i); break
    except Exception:
        i=s.find('{',i+1)
if not o or not o.get('drag'):
    print(''); sys.exit(0)
print(' '.join(str(v) for v in o['drag']))
"
}
# 真鼠标拖选：move → down → 分 3 步 move → up
drag() {
  set -- $1
  step mouse move "$1" "$2"
  step mouse down left
  step mouse move "$(( ($1+$3)/2 ))" "$(( ($2+$4)/2 ))"
  step mouse move "$3" "$4"
  step mouse move "$3" "$4"
  step mouse up left
}

step open "$URL"
step set viewport 1440 900
step wait 3800

echo "=== 侧栏滑进视口（审查模块）==="
ev openSide
step wait 1200

echo "=== 审查模块：几何 ==="
G=$(ev rvGeom) ; echo "$G"
D=$(echo "$G" | dragrc)
echo "drag = [$D]"

if [ -n "$D" ]; then
  drag "$D"
  step wait 500
  echo "=== 拖选后 ==="
  ev read
  run screenshot "$RAW/w-$TAG-selbar.png"
  ev clickCopy
  step wait 400
  ev read
fi

echo "=== 摘要模块（散文）==="
ev openSummary
step wait 900
G2=$(ev geomSummary) ; echo "$G2"
D2=$(echo "$G2" | dragrc) ; echo "drag = [$D2]"
if [ -n "$D2" ]; then
  drag "$D2"
  step wait 500
  ev read
fi

echo "=== 文件模块（代码区）==="
ev openFiles
step wait 900
G3=$(ev geomFiles) ; echo "$G3"
D3=$(echo "$G3" | dragrc) ; echo "drag = [$D3]"
if [ -n "$D3" ]; then
  drag "$D3"
  step wait 500
  ev read
  run screenshot "$RAW/w-$TAG-files-selbar.png"
fi
echo "done"

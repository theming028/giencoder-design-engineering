#!/usr/bin/env bash
# r109 第二拍真机取证：① zd 自动折叠 ② 终端字号 13px ③ regen 图标 ④ 锚点编辑态详情 ⑤ 锚点拖动
set -u
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
CLI="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
ROOT="E:/GienCoder/giencoder-design-engineering"
EV="$ROOT/mg-work/r109/ev"; RAW="$ROOT/mg-work/r109/raw"
URL="file:///$ROOT/pages/conversation.html?v=$(date +%s)"
run() { "$NODE" "$CLI" "$@" 2>&1; }
# ★ eval 的返回是「JSON 套 JSON」：外层 str 里装着真正的 JSON 串 ⇒ 必须解两层
jget() { python -c "
import json,sys
try:
    d=json.load(open(sys.argv[1],encoding='utf-8'))
except Exception as e:
    print('PARSE_FAIL'); sys.exit(0)
if isinstance(d,str):
    try: d=json.loads(d)
    except Exception: print('PARSE_FAIL'); sys.exit(0)
cur=d
for k in sys.argv[2].split('.'):
    try:
        cur=cur[int(k)] if isinstance(cur,list) else cur.get(k)
    except Exception:
        print('PARSE_FAIL'); sys.exit(0)
    if cur is None: print('PARSE_FAIL'); sys.exit(0)
print(cur)
" "$1" "$2"; }

run set viewport 1440 900 > "$EV/l2-z1.log" 2>&1
run open "$URL" > "$EV/l2-z2.log" 2>&1
run wait 4200 > "$EV/l2-z3.log" 2>&1

echo "########## 【①②③】zd 折叠矩阵 / 终端字号与盒子 / regen 图标 ##########"
run eval "$(cat "$EV/p109k.js")" > "$EV/k1.json" 2>&1
cat "$EV/k1.json"; echo
run screenshot " " "$RAW/f-zd-mini.png" > "$EV/l2-s1.log" 2>&1
run screenshot '[title="重新生成"]' "$RAW/g-regen-btn.png" > "$EV/l2-s2.log" 2>&1

echo "########## 【④ 准备】进批注态 → 加一条批注 → 气泡收起 ##########"
run eval "$(cat "$EV/p109g.js")" > "$EV/g1.json" 2>&1
cat "$EV/g1.json"; echo
run screenshot " " "$RAW/d2-anchor-committed.png" > "$EV/l2-s3.log" 2>&1

CX=$(jget "$EV/g1.json" anchorCenter.x); CY=$(jget "$EV/g1.json" anchorCenter.y)
echo ">>> 锚点中心 = $CX,$CY"

echo "########## 【⑤-a】真鼠标拖拽（+40/+30 ⇒ 越过 4px 阈值）—— 期望：移动、且不弹气泡 ##########"
run mouse move "$CX" "$CY" > "$EV/l2-m1.log" 2>&1
run mouse down > "$EV/l2-m2.log" 2>&1
run mouse move "$((CX+16))" "$((CY+11))" > "$EV/l2-m3.log" 2>&1
run mouse move "$((CX+30))" "$((CY+22))" > "$EV/l2-m4.log" 2>&1
run mouse move "$((CX+40))" "$((CY+30))" > "$EV/l2-m5.log" 2>&1
run mouse up > "$EV/l2-m6.log" 2>&1
run eval "$(cat "$EV/p109h.js")" > "$EV/h1.json" 2>&1
cat "$EV/h1.json"; echo

echo "########## 【④-a】复位拖动标记 → 真鼠标单击锚点（不动）⇒ 期望重开编辑态详情 ##########"
CX2=$(jget "$EV/h1.json" anchorCenter.x); CY2=$(jget "$EV/h1.json" anchorCenter.y)
echo ">>> 拖动后锚点中心 = $CX2,$CY2"
run eval "$(cat "$EV/p109r.js")" > "$EV/l2-r1.log" 2>&1
cat "$EV/l2-r1.log"; echo
run mouse move "$CX2" "$CY2" > "$EV/l2-m7.log" 2>&1
run mouse down > "$EV/l2-m8.log" 2>&1
run mouse up > "$EV/l2-m9.log" 2>&1
run eval "$(cat "$EV/p109i.js")" > "$EV/i1.json" 2>&1
cat "$EV/i1.json"; echo
run screenshot " " "$RAW/d2-anchor-reopen.png" > "$EV/l2-s4.log" 2>&1

echo "########## 【⑤-b】真鼠标拖到视口右下外 ⇒ 期望被 .td-view 夹回可视区 ##########"
run mouse move "$CX2" "$CY2" > "$EV/l2-m10.log" 2>&1
run mouse down > "$EV/l2-m11.log" 2>&1
run mouse move 1430 880 > "$EV/l2-m12.log" 2>&1
run mouse move 1439 899 > "$EV/l2-m13.log" 2>&1
run mouse up > "$EV/l2-m14.log" 2>&1
run eval "$(cat "$EV/p109h.js")" > "$EV/h2.json" 2>&1
cat "$EV/h2.json"; echo
run screenshot " " "$RAW/e2-anchor-clamped.png" > "$EV/l2-s5.log" 2>&1

echo "########## 【④-c】在拖到底角的锚点上真鼠标单击 ⇒ 气泡是否被 .td-view 裁掉？ ##########"
CX3=$(jget "$EV/h2.json" anchorCenter.x); CY3=$(jget "$EV/h2.json" anchorCenter.y)
echo ">>> 底角锚点中心 = $CX3,$CY3"
run mouse move "$CX3" "$CY3" > "$EV/l2-m15.log" 2>&1
run mouse down > "$EV/l2-m16.log" 2>&1
run mouse up > "$EV/l2-m17.log" 2>&1
run eval "$(cat "$EV/p109i.js")" > "$EV/i2.json" 2>&1
cat "$EV/i2.json"; echo
run screenshot " " "$RAW/e2-anchor-corner-note.png" > "$EV/l2-s6.log" 2>&1

echo "########## 【④-b】编辑态 update 语义（不新增锚点、不挪位置、文案就地更新）##########"
run eval "$(cat "$EV/p109j.js")" > "$EV/j1.json" 2>&1
cat "$EV/j1.json"; echo

echo "########## 关掉标签页 ##########"
run close > "$EV/l2-z9.log" 2>&1
ls -la "$RAW"/f-*.png "$RAW"/g-*.png "$RAW"/d2-*.png "$RAW"/e2-*.png 2>&1

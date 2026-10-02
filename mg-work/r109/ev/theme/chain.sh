#!/usr/bin/env bash
# r109 整链（第 1~12 层）· 一次跑到尾
# ★ 铁律：跑完必须 check-syntax + verify-design + git checkout -- pages/gaps.log
# ★ 稳定性判据：连跑两轮比整链 md5（应为 0 行差异）
set -u
cd "$(dirname "$0")/../../../.." || exit 1
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"

rm -rf mg-work/r109/ev/theme/__pycache__ mg-work/r109/ev/__pycache__

echo "=== [1] make109 ==="
"$PY" -B mg-work/r109/ev/make109.py         2>&1 | tail -4
echo "=== [2] splice109 ==="
"$PY" -B mg-work/r109/ev/splice109.py       2>&1 | tail -4
echo "=== [3] apply109 ==="
"$PY" -B mg-work/r109/apply109.py           2>&1 | tail -4
echo "=== [4] apply-theme ==="
"$PY" -B mg-work/r109/ev/theme/apply-theme.py     2>&1 | tail -3
echo "=== [5] apply-dark ==="
"$PY" -B mg-work/r109/ev/theme/apply-dark.py      2>&1 | tail -3
echo "=== [6] apply-tokens ==="
"$PY" -B mg-work/r109/ev/theme/apply-tokens.py    2>&1 | tail -3
echo "=== [7] apply-literals ==="
"$PY" -B mg-work/r109/ev/theme/apply-literals.py  2>&1 | tail -3
echo "=== [8] apply-popup ==="
"$PY" -B mg-work/r109/ev/theme/apply-popup.py     2>&1 | tail -3
echo "=== [9] apply-border ==="
"$PY" -B mg-work/r109/ev/theme/apply-border.py    2>&1 | tail -3
echo "=== [10] apply-zcode ==="
"$PY" -B mg-work/r109/ev/theme/apply-zcode.py     2>&1 | tail -3
echo "=== [11] apply-menuwhite ==="
"$PY" -B mg-work/r109/ev/theme/apply-menuwhite.py 2>&1 | tail -3
echo "=== [12] apply-dots ==="
"$PY" -B mg-work/r109/ev/theme/apply-dots.py      2>&1 | tail -3
echo "=== 链尾 md5 ==="
md5sum pages/*.html | md5sum

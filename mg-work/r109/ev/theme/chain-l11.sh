#!/usr/bin/env bash
# r109 第十一拍（增量子链）· 从「第十拍定稿基线」出发，只跑第 11 / 12 层。
#
# ★★ 为什么不是「整链 1~12 层循环」？（本拍实测踩过的红线）
#   apply109.py 的净底摘除清单只有 RE_STYLE / RE_JS / RE_NAV / RE_HDR
#   （r100 / r101 那几代的块），**不含第 4~12 层（theme/dark/tokens/literals/
#   popup/border/zcode/menuwhite/dots）注入的新块**。
#   ⇒ 从「链尾态」重跑 apply109.py 时，那些新块会被带进 net、复制到
#     conversation 等页 ⇒ 每轮 +3 字符、10 页 md5 全变 ⇒ **整链不可循环**。
#   实测：从基线连跑两轮整链，10 页 md5 全不相同（每页净 +3 字符 / 轮）。
#
# ★ 正确工作流：
#   1) 先恢复到本代定稿基线：  cp mg-work/r109/ev/bak-r109-l10/*.html pages/
#   2) 只跑「本拍新增的层」：    本拍 = 第 11 层（menuwhite）+ 第 12 层（dots）
#   3) 幂等判据：连跑两轮比 md5（应 0 行差异）
#
# 用法：bash mg-work/r109/ev/theme/chain-l11.sh
set -u
cd "$(dirname "$0")/../../../.." || exit 1
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"

rm -rf mg-work/r109/ev/theme/__pycache__ mg-work/r109/ev/__pycache__

echo "=== [11] apply-menuwhite ==="
"$PY" -B mg-work/r109/ev/theme/apply-menuwhite.py 2>&1 | tail -6
echo "=== [12] apply-dots ==="
"$PY" -B mg-work/r109/ev/theme/apply-dots.py 2>&1 | tail -4
echo "=== 链尾 md5 ==="
md5sum pages/*.html | md5sum

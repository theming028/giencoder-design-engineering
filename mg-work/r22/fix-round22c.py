# -*- coding: utf-8 -*-
"""第22轮 c 补丁：让复用的基础工作台对话框模块在 480px 右栏里不破版。

实测：模块工具栏自然宽 489px（添加40+技能40+艾迪62+标准模式96 | 模型147+优化32+发送32 + gap），
      480 右栏可用宽仅 414px（480 − 外边距40 − 卡片边框2 − p-3 24），超 75px
      → 艾迪文案换行、发送按钮被挤出容器。
处理：模块结构与类名保持 1:1，仅在窄容器下收起占位最大的「标准模式」选择器，
      并把左右组内间距 8px 收到 4px；其余控件（添加/技能/数字分身/模型/优化提示词/发送）全部保留。
      收敛后 158 + 227 = 385 ≤ 414。
"""
import io

SRC = "mg-work/r21/build-detail.py"
s = io.open(SRC, encoding="utf-8").read()

OLD = """      /* 补齐 base 页使用、本页 Tailwind 产物未包含的 3 个任意值类 */
      .td-composer .min-h-\\[96px\\] { min-height: 96px; }
      .td-composer .gap-\\[2px\\] { gap: 2px; }
      .td-composer .bg-\\[var\\(--color-fill-3\\)\\] { background: var(--color-fill-3); }
"""

NEW = """      /* 补齐 base 页使用、本页 Tailwind 产物未包含的 3 个任意值类 */
      .td-composer .min-h-\\[96px\\] { min-height: 96px; }
      .td-composer .gap-\\[2px\\] { gap: 2px; }
      .td-composer .bg-\\[var\\(--color-fill-3\\)\\] { background: var(--color-fill-3); }
      /* 窄容器收敛：480 右栏可用 414px，模块工具栏自然宽 489px
         → 收起占位最大的「标准模式」选择器、组内间距 8→4、文本不换行；其余控件全部保留 */
      .td-composer .giencoder-select[style*="width: 96px"] { display: none; }
      .td-composer .flex.items-center.gap-\\[8px\\] { gap: 4px; }
      .td-composer .flex.items-center.gap-2 { gap: 4px; }
      .td-composer [aria-label="数字分身"] { white-space: nowrap; }
"""

n = s.count(OLD)
if n != 1:
    raise SystemExit("PATCH FAIL count=%d" % n)
s = s.replace(OLD, NEW)
io.open(SRC, "w", encoding="utf-8").write(s)
print("OK  composer-narrow")
print("PATCHED", len(s))

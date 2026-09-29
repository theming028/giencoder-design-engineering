# -*- coding: utf-8 -*-
"""r78 两项需求补丁（幂等）。

需求：
  1. 基础工作台 main 的波点涟漪：点击「欢迎态主内容块」范围内（
     class="flex flex-1 flex-col items-center justify-center px-6"
     = 问候语 + LOGO + 输入卡 + 技能胶囊那一整块）及其内部任意元素时，
     不再触发涟漪。
  2. 涟漪强度「再减半」：点色 α 0.28 -> 0.14。

幂等三要素：
  ① 先判 NEW 标记命中即 skip；
  ② 再判 count(OLD) 恰好为 N，否则 sys.exit；
  ③ 跑完立刻复跑一次确认「应用: 0 项 / 跳过: N 项」。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, "pages")
BASE = os.path.join(PAGES, "base.html")

applied = 0
skipped = 0


def rd(p):
    return io.open(p, encoding="utf-8").read()


def wr(p, s):
    io.open(p, "w", encoding="utf-8").write(s)


def inject_tail(path, style_id, css, label):
    """在唯一 </body> 前注入 <style id=...>；带标签级计数断言。

    ⚠️ 落点必须在 </body> 前（而不是 </head> 前）：r76 / r77 那几块也注入在
       </body> 前，同特异性规则「文档顺序后者胜」才成立。r77 第一版误注入到
       </head> 前，结果 .r74-ripple 的 z-index / 点色被页尾的 r76 块反向压回去。
    """
    global applied, skipped
    s = rd(path)
    mark = '<style id="%s">' % style_id
    if mark in s:
        print("  skip  %-34s 已应用" % label)
        skipped += 1
        return False
    if s.count("</body>") != 1:
        sys.exit("!! %s：</body> 出现 %d 次（期望 1）" % (label, s.count("</body>")))
    n_style = s.count("<style")
    n_end = s.count("</style>")
    block = '<style id="%s">\n%s\n</style>\n' % (style_id, css)
    s = s.replace("</body>", block + "</body>", 1)
    if s.count("<style") != n_style + 1:
        sys.exit("!! %s：<style> 计数 %d → %d（期望 +1）" % (label, n_style, s.count("<style")))
    if s.count("</style>") != n_end + 1:
        sys.exit("!! %s：</style> 计数 %d → %d（期望 +1）" % (label, n_end, s.count("</style>")))
    wr(path, s)
    print("  ok    %-34s 1 处（标签 %d→%d）" % (label, n_style, n_style + 1))
    applied += 1
    return True


# ---------------------------------------------------------------- 需求 1
print("\n=== 需求 1：欢迎态主内容块内点击不再触发涟漪 ===")
# 原有判定：不在可交互控件上 ⇒ 视为「空白处」
OLD_GUARD = ("        if (t.closest('button, a, input, textarea, select, label, "
             "[role=\"button\"], [role=\"tab\"], [contenteditable=\"true\"]')) return;\n")
# 追加一条：命中欢迎态主内容块（自身或其任意后代）即提前返回
NEW_GUARD = OLD_GUARD + (
    "        /* 第 78 轮 · 需求 1：欢迎态主内容块（LOGO + 问候语 + 输入卡 + 技能胶囊）"
    "整块不算「空白处」 */\n"
    "        if (t.closest('.flex.flex-1.flex-col.items-center.justify-center.px-6')) return;\n")
MARK_GUARD = "closest('.flex.flex-1"

s = rd(BASE)
if MARK_GUARD in s:
    print("  skip  %-34s 已应用" % "base.html 涟漪触发排除")
    skipped += 1
else:
    n = s.count(OLD_GUARD)
    if n != 1:
        sys.exit("!! base.html 涟漪排除：锚点出现 %d 次（期望 1）\n   old=%r" % (n, OLD_GUARD))
    n_script = s.count("<script")
    n_end = s.count("</script>")
    s2 = s.replace(OLD_GUARD, NEW_GUARD, 1)
    # 自检：只改脚本正文，标签级计数必须不变
    if s2.count("<script") != n_script:
        sys.exit("!! <script 计数 %d → %d（期望不变）" % (n_script, s2.count("<script")))
    if s2.count("</script>") != n_end:
        sys.exit("!! </script> 计数 %d → %d（期望不变）" % (n_end, s2.count("</script>")))
    # 自检：新增的排除判定恰 1 份；原判定仍在
    if s2.count(MARK_GUARD) != 1:
        sys.exit("!! 新排除判定计 %d（期望 1）" % s2.count(MARK_GUARD))
    if s2.count(OLD_GUARD) != 1:
        sys.exit("!! 原判定保留计 %d（期望 1）" % s2.count(OLD_GUARD))
    wr(BASE, s2)
    print("  ok    %-34s 1 处（脚本 %d→%d，标签不变）" % ("base.html 涟漪触发排除", len(s), len(s2)))
    applied += 1

# ---------------------------------------------------------------- 需求 2
print("\n=== 需求 2：涟漪点色 α 0.28 -> 0.14（再减半）===")
BASE_CSS = """  /* 第 78 轮 · 需求 2：涟漪强度再减半。
     第 77 轮把点色 α 定在 0.28（灰-9 白底合成 rgb(196)，对底色点阵 rgb(240) 的 Δ≈55），
     邵先生反馈「还是太明显」⇒ 本轮 α 再砍一半到 0.14：
       合成 rgb(212) ⇒ Δ≈28，恰为第 77 轮的一半
       （本组合下 α 与 Δ 成正比：Δ = (底色 - 描点色) × α，底色与描点色都不变）。
     只动点色这一项 —— 点径 1.7px、环带 mask（第 76 轮那套 max(比例, 固定值) 整流公式）、
     半径上限 480px、时长 300ms 全部保持不变。
     ⚠️ 落点必须在 </body> 前（第 77 轮块之后）：同为 .r74-ripple（特异性 0-1-0），
        只能靠文档顺序取胜 —— 与第 77 轮压回第 76 轮同一机制。 */
  .r74-ripple {
    background-image: radial-gradient(circle, rgba(var(--gray-9), 0.14) 1.7px, transparent 1.7px);
  }"""
inject_tail(BASE, "r78-base-css", BASE_CSS, "base.html 涟漪强度再减半")

print("\n应用: %d 项 | 跳过: %d 项" % (applied, skipped))

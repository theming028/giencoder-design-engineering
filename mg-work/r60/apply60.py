#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
r60：浏览态隐藏左栏内的信息列（.td-side）

需求（邵先生 2026-09-28 拍板）：
  浏览态（右栏 .td-browse-slot 文件预览展开）下，左栏不再完全隐藏、保留 600px（r58）。
  但左栏内部的 .td-side（任务属性 / 任务动态 / 底部记录）靠 min-width:266px 硬吃掉近一半，
  正文列只剩 ≈332px，第一步流程示意明显拥挤 → 浏览态隐藏 .td-side。

改法：纯 CSS 追加一条规则。退出浏览态（关闭预览）自动恢复，无 JS 参与。
      不作用于普通态 —— 普通态「任务属性」照常可见。

幂等：以 MARK 判重，命中即 SKIP 不写盘。
自检：① 标签级计数（style/script 开闭）② 被改对象邻接规则的精确计数不变
      ③ 新规则必须恰好出现 1 次。
"""
import io
import os
import sys

P = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', 'pages', 'task-detail.html'))

OLD = """      .td-root.is-browse.is-keep-left .td-left {
        display: flex;
        flex: 0 0 var(--td-left-keep-w, 600px);
        min-width: var(--td-left-keep-w, 600px);
        max-width: var(--td-left-keep-w, 600px);
        margin-right: var(--td-gap);
      }"""

NEW = OLD + """
      /* ★ 第 60 轮：浏览态（右侧文件预览栏展开）为「阅读正文」让位 —— 隐藏左栏内的信息列
         （任务属性 / 任务动态 / 底部记录）。
         改前：左栏保留 600px，但 .td-side 靠 min-width:266px 吃掉近一半，正文列只剩 ≈332px，
               第一步流程示意明显拥挤。
         改后：正文列独占 ≈598px（= 600 − 上下 1px 描边 ×2）。
         纯 CSS，退出浏览态（关闭预览）自动恢复，无 JS 参与；
         且不作用于普通态 —— 普通态「任务属性」照常可见。 */
      .td-root.is-browse .td-side { display: none; }"""

MARK = ".td-root.is-browse .td-side { display: none; }"

# ① 标签级计数：改前/改后必须不变
STABLE = [
    "<style>", "</style>", "<script>", "</script>",
    # ② 邻接规则的精确计数不变（防止粗放替换吞并周围 CSS）
    ".td-root.is-browse .td-left { display: none; }",
    ".td-root.is-browse .td-gutter { display: none; }",
    ".td-root.is-browse .td-browse { display: flex; }",
    ".td-root.is-browse.is-keep-left .td-left",
]
# ③ 必须存在的精确计数
EXACT_AFTER = {
    ".td-root.is-browse .td-side { display: none; }": 1,
}


def main():
    with io.open(P, encoding='utf-8') as f:
        before = f.read()

    applied = MARK in before
    if applied:
        src = before
        print("[SKIP] MARK 已存在 → 补丁此前已应用，本次不写盘")
    else:
        n = before.count(OLD)
        if n != 1:
            print("[FAIL] OLD 命中 %d 次（应为 1）→ 未写盘" % n)
            return 1
        src = before.replace(OLD, NEW, 1)
        print("[OK] OLD 命中 1 次 → 已替换")

    fails = []
    for t in STABLE:
        if src.count(t) != before.count(t):
            fails.append("stable token %r 计数变化：%d → %d"
                         % (t, before.count(t), src.count(t)))
    for t, exp in EXACT_AFTER.items():
        c = src.count(t)
        if c != exp:
            fails.append("token %r 计数 %d（应为 %d）" % (t, c, exp))

    if fails:
        for x in fails:
            print("[FAIL]", x)
        print("!! 自检未通过，未写盘")
        return 1

    print("[OK] 自检通过：标签计数不变 / 邻接规则计数不变 / 新规则恰好 1 条")
    for t in STABLE:
        print("      %-52s %d" % (t, src.count(t)))
    print("      %-52s %d" % (MARK, src.count(MARK)))

    if applied:
        print("      bytes %d → %d (Δ %+d)" % (len(before.encode('utf-8')),
                                               len(src.encode('utf-8')), 0))
        print("ALL PASS (no-op)")
        return 0

    with io.open(P, 'w', encoding='utf-8') as f:
        f.write(src)
    print("      bytes %d → %d (Δ %+d)" % (len(before.encode('utf-8')),
                                           len(src.encode('utf-8')),
                                           len(src.encode('utf-8')) - len(before.encode('utf-8'))))
    print("ALL PASS")
    return 0


if __name__ == '__main__':
    sys.exit(main())

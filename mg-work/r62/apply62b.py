#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
r62b：修 shimmer 的「背景盒宽度」保真度问题

问题（运行时发现）：
  motion-primitives 的元素是 `relative inline-block` —— 背景盒**贴住文字**。
  本页 .kb-card-title 是块级，实测宽 292px，而文字墨迹只有 ≈154px：
    · 贴字时（原版）：光带中心在文字区内的扫描占比 ≈ 67%（1/1.5）
    · 撑满时（本页）：band 中心从 -73px 扫到 +365px，落在文字区 [0,154] 的占比只有 ≈ 35%
  ⇒ 超过一半的周期里标题完全没有光带，观感比原版「闪得少」。

改法：给流光态加 `width: fit-content` —— 块级元素宽度收缩到内容宽，
  兄弟元素（.kb-card-tags / .kb-card-foot 各自成行）布局不变，标题文字起始 x 也不变。

幂等：以 MARK 判重。
"""
import io
import os
import sys

P = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', 'pages', 'kanban.html'))

OLD = """      .kb-card:has(.kb-running) .kb-card-title {
        --kb-shimmer-spread: 20px;
        background-image:"""

NEW = """      .kb-card:has(.kb-running) .kb-card-title {
        --kb-shimmer-spread: 20px;
        /* ★ 第 62 轮（二）：让背景盒等于文字盒 —— 原版元素是 inline-block，盒子贴字。
           本页 .kb-card-title 是块级，实测块宽 292px 而文字墨迹只有 ≈154px：
           若背景盒跟着撑满，光带中心从 -73px 扫到 +365px，真正落在文字区的占比仅 ≈35%；
           贴字后回到原版的 ≈67%。兄弟元素各自成行，布局与文字起始 x 均不变。 */
        width: fit-content;
        background-image:"""

MARK = 'width: fit-content;\n        background-image:'


def main():
    with io.open(P, encoding='utf-8') as f:
        before = f.read()

    if MARK in before:
        src = before
        print('[SKIP] MARK 已存在 → 补丁此前已应用，本次不写盘')
    else:
        n = before.count(OLD)
        if n != 1:
            print('[FAIL] OLD 命中 %d 次（应为 1）→ 未写盘' % n)
            return 1
        src = before.replace(OLD, NEW, 1)
        print('[OK] OLD 命中 1 次 → 已替换')

    fails = []
    for t in ['<style>', '</style>', '<script>', '</script>',
              '.kb-card-title { color: var(--color-text-1); font-size: 14px; font-weight: 400; line-height: 22px; }',
              '.kb-card:hover .kb-card-title { font-weight: 500; }']:
        if src.count(t) != before.count(t):
            fails.append('stable token %r 计数变化：%d → %d' % (t[:48], before.count(t), src.count(t)))
    if src.count(MARK) != 1:
        fails.append('MARK 出现 %d 次（应为 1）' % src.count(MARK))

    if fails:
        for x in fails:
            print('[FAIL]', x)
        print('!! 自检未通过，未写盘')
        return 1

    print('[OK] 自检通过：标签与既有规则计数不变 / MARK 恰好 1 处')
    if src == before:
        print('      bytes %d（no-op）' % len(src.encode('utf-8')))
        print('ALL PASS (no-op)')
        return 0
    with io.open(P, 'w', encoding='utf-8') as f:
        f.write(src)
    print('      bytes %d → %d (Δ %+d)' % (len(before.encode('utf-8')),
                                           len(src.encode('utf-8')),
                                           len(src.encode('utf-8')) - len(before.encode('utf-8'))))
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())

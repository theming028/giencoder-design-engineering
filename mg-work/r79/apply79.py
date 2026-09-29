#!/usr/bin/env python3
"""r79 · base.html 需求 1：涟漪触发范围再排除「版权带」⇒ 欢迎态完全不触发。

幂等三要素：
  1) 先判 NEW 标记（r79-cr-excl）命中即 skip
  2) 再判 count(OLD) 恰好为 1，否则 sys.exit
  3) 跑完复跑一次，须为「应用: 0 项 | 跳过: 1 项」
标签级断言：改的是 <script> 正文 ⇒ <script / </script> 计数**不变**（不是插 <style> 那套 ±1）。
"""
import sys, io, os, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGE = os.path.join(ROOT, "pages", "base.html")

MARK = "r79-cr-excl"

OLD = "        if (t.closest('.flex.flex-1.flex-col.items-center.justify-center.px-6')) return;\n"

NEW = (
    "        if (t.closest('.flex.flex-1.flex-col.items-center.justify-center.px-6')) return;\n"
    "        /* " + MARK + " · 第 79 轮 · 需求 1：版权带也算「内容」，一并排除。\n"
    "           选择器与上方 ① 段抓的版权容器是同一个（main 里 class 含 pb-6 + text-center 的 div）。\n"
    "           ⚠️ 范围后果（已与邵先生确认）：main.dot-bg 只有「欢迎态内容容器 + 版权带」两块，\n"
    "              两块都排除 ⇒ 本页不再有任何区域能起涟漪，涟漪特效在 base.html 实际已停用。\n"
    "              脚本与样式**保留不删**（死代码清理另行拍板），便于随时回退。 */\n"
    "        if (t.closest('div[class*=\"pb-6\"][class*=\"text-center\"]')) return;\n"
)


def counts(s):
    return {t: s.count(t) for t in ("<script", "</script>", "<style", "</style>")}


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def main():
    src = io.open(PAGE, encoding="utf-8").read()

    if MARK in src:
        print("应用: 0 项 | 跳过: 1 项  （%s 已存在）" % MARK)
        return 0

    n = src.count(OLD)
    if n != 1:
        print("!! 锚点计数异常：count(OLD) = %d（应为 1）—— 拒绝执行" % n)
        return 2

    before = counts(src)
    out = src.replace(OLD, NEW, 1)
    after = counts(out)
    if before != after:
        print("!! 标签级计数被改动：%s -> %s —— 拒绝执行" % (before, after))
        return 3

    io.open(PAGE, "w", encoding="utf-8").write(out)
    print("应用: 1 项 | 跳过: 0 项")
    print("   标签级计数不变：%s" % after)
    print("   md5: %s -> %s" % (md5(os.path.join(ROOT, "mg-work/r79/before/base.html")), md5(PAGE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

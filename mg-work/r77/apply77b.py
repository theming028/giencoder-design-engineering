# -*- coding: utf-8 -*-
"""r77b：修 base.html 第 74 轮页尾脚本①段的「版权区」逻辑（幂等）。

背景
----
第 74 轮需求②把版权区改成三行，用的是「运行时抓最后一个 <p> 拆两行」：
    React 源码顺序 = [内容由 AI 生成，请核实重要信息, © 2026 中电金信研究院 · … · 版本：1.2.5]
    脚本把最后一个 p（© 一整行）覆盖成「© 2026 中电金信」，再 append 一行「中电金信研究院 · …」
    => [AI 提示句, © 2026 中电金信, 中电金信研究院 · … · 版本：1.2.5]

第 77 轮需求③要求把「内容由 AI 生成，请核实重要信息」挪到最下面。
apply77.py 已把源码两行调成 [© 一整行, AI 提示句]；但脚本仍抓「最后一个 p」，
那正是 AI 提示句 => 会被覆盖掉、整句消失（实测渲染成三行重复版权文本）。
本脚本把该段改成抓「第一个 p」（© 那一整行）来拆，新行插在它紧后面。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(ROOT, "pages", "base.html")

applied = 0
skipped = 0


def rd(p):
    return io.open(p, encoding="utf-8").read()


def wr(p, s):
    io.open(p, "w", encoding="utf-8").write(s)


def replace_once(path, old, new, label, mark):
    global applied, skipped
    s = rd(path)
    if mark in s:
        print("  skip  %-30s 已应用" % label)
        skipped += 1
        return False
    n = s.count(old)
    if n != 1:
        sys.exit("!! %s：锚点出现 %d 次（期望 1）\n   old=%r" % (label, n, old[:160]))
    s = s.replace(old, new, 1)
    wr(path, s)
    print("  ok    %-30s 1 处" % label)
    applied += 1
    return True


# 1) 脚本块头部注释
replace_once(
    BASE,
    "     ① 需求 2 —— 版权区拆成「© 2026 中电金信」+「中电金信研究院 · … · 版本：1.2.5」两行",
    "     ① 需求 2 —— 版权区拆成「© 2026 中电金信」+「中电金信研究院 · … · 版本：1.2.5」两行；\n"
    "        第 77 轮需求 3 —— 「内容由 AI 生成，请核实重要信息」改落在最下面（三行）",
    "脚本头注释",
    mark="第 77 轮需求 3 —— 「内容由 AI 生成",
)

# 2) ①段主体：抓最后一个 p -> 抓第一个 p，插在它后面
OLD = (
    "      var last = ps[ps.length - 1];\n"
    "      if (last.getAttribute('data-r74-cr') === '1') return true;\n"
    "      last.textContent = L1;\n"
    "      last.setAttribute('data-r74-cr', '1');\n"
    "      var p3 = document.createElement('p');\n"
    "      p3.setAttribute('data-r74-cr', '1');\n"
    "      p3.textContent = L2;\n"
    "      host.appendChild(p3);\n"
    "      return true;"
)
NEW = (
    "      /* 第 77 轮 · 需求 3：「内容由 AI 生成，请核实重要信息」要落在最下面。\n"
    "         第 74 轮抓的是「最后一个 p」—— 那时源码顺序是 [AI 提示句, © 一整行]，\n"
    "         拆完正好三行。本轮源码两行已调成 [© 一整行, AI 提示句]，若仍拆最后一个 p\n"
    "         就会把提示句整句盖掉（实测渲染成「© … 版本：1.2.5」+「© 2026 中电金信」\n"
    "         +「中电金信研究院 · …」三行，提示句消失）。\n"
    "         故改为抓「第一个 p」（© 那一整行）来拆，新行插在它紧后面 —— 提示句自然\n"
    "         落到最下，第 74 轮「© 拆两行」的版式保持不变。 */\n"
    "      var first = ps[0];\n"
    "      if (first.getAttribute('data-r74-cr') === '1') return true;\n"
    "      first.textContent = L1;\n"
    "      first.setAttribute('data-r74-cr', '1');\n"
    "      var p2 = document.createElement('p');\n"
    "      p2.setAttribute('data-r74-cr', '1');\n"
    "      p2.textContent = L2;\n"
    "      host.insertBefore(p2, first.nextSibling);\n"
    "      return true;"
)
replace_once(BASE, OLD, NEW, "版权区脚本主逻辑", mark="var first = ps[0];")

print("\n应用: %d 项 | 跳过: %d 项" % (applied, skipped))

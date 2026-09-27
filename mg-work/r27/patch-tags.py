# -*- coding: utf-8 -*-
"""第 27 轮第 4 项：任务看板三个标签（拆分需求项 / 拆分需求条目 / 拆分子条目）配色对齐设计稿。

设计稿来源：画板 553:06620 的 1x 导出 `mg-work/kanban/root/board-design.png`（1440×900，无损）。
该导出无色彩空间偏移的证据：同一张图里 `#3770F7`(353px)、`#FF6157`(144px)、`#1F1F1F`(7898px)
均以精确值出现；且三组标签文字的『底色→文字色』抗锯齿渐变序列为严格等差
（例：蓝 231→188→146→104→61，步长恒为 43），说明序列末端 α=1，即观测值就是真值。

设计稿实测：
  拆分需求项   底 #E7F0FF rgb(231,240,255)   文字 #3D6EBF rgb(61,110,191)   盒 63×18
  拆分需求条目 底 #F5E8FF rgb(245,232,255)   文字 #7A4B9E rgb(122,75,158)   盒 74×18
  拆分子条目   底 #FFE8F1 rgb(255,232,241)   文字 #A74B6F rgb(167,75,111)   盒 63×18
（其中 #F5E8FF == rgb(var(--purple-1))、#FFE8F1 == rgb(var(--magenta-1))，与 DS 一档色一致。）

原实现误用了 -2 档底 + -6 档文字，明显偏艳：
  蓝  rgb(218,228,254) / rgb(55,112,247)
  紫  rgb(221,190,246) / rgb(114,46,209)
  品红 rgb(253,194,219) / rgb(245,49,157)

做法：只改两个页面 :root 里的 6 个 `--kb-tag-*` 适配层变量（见本仓既有先例
`--kb-prio-high: #F53F3F`、`--td-ink-2: #57626D`，均为「设计稿实测」字面值）。
暗色块同步补一份 tx 覆盖（原来 tx 走 `rgb(var(--*-6))` 是主题自适应的，
换成字面 hex 后会失效），使暗色表现与本轮之前完全一致。

⚠️ 不改标签的盒尺寸（设计 63×18 / 74×18，当前 72×20 / 84×20）——本轮需求只提颜色。
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OLD_LIGHT = (
    "        --kb-tag-blue-bg: var(--color-primary-light-2); --kb-tag-blue-tx: var(--color-primary-6);\n"
    "        --kb-tag-purple-bg: rgb(var(--purple-2)); --kb-tag-purple-tx: rgb(var(--purple-6));\n"
    "        --kb-tag-magenta-bg: rgb(var(--magenta-2)); --kb-tag-magenta-tx: rgb(var(--magenta-6));\n"
)
NEW_LIGHT = (
    "        /* r27#4: 三个标签配色对齐设计稿（画板 553:06620 的 1x 导出 board-design.png 逐像素实测，\n"
    "           导出无色彩空间偏移：同图 #3770F7/#FF6157/#1F1F1F 均精确出现）。\n"
    "           实测 —— 拆分需求项 #E7F0FF/#3D6EBF、拆分需求条目 #F5E8FF/#7A4B9E、拆分子条目 #FFE8F1/#A74B6F。\n"
    "           原实现误用 -2 档底色 + -6 档文字，明显偏艳。 */\n"
    "        --kb-tag-blue-bg: #E7F0FF;    --kb-tag-blue-tx: #3D6EBF;\n"
    "        --kb-tag-purple-bg: #F5E8FF;  --kb-tag-purple-tx: #7A4B9E;\n"
    "        --kb-tag-magenta-bg: #FFE8F1; --kb-tag-magenta-tx: #A74B6F;\n"
)

OLD_DARK = (
    "        --kb-tag-blue-bg: rgba(var(--giencoderblue-6), 0.24);\n"
    "        --kb-tag-purple-bg: rgba(var(--purple-6), 0.24);\n"
    "        --kb-tag-magenta-bg: rgba(var(--magenta-6), 0.24);\n"
)
NEW_DARK = (
    "        --kb-tag-blue-bg: rgba(var(--giencoderblue-6), 0.24);\n"
    "        --kb-tag-purple-bg: rgba(var(--purple-6), 0.24);\n"
    "        --kb-tag-magenta-bg: rgba(var(--magenta-6), 0.24);\n"
    "        /* r27#4: 亮色底/文字改字面值后需在暗色下补回主题自适应文字色，暗色表现与本轮前一致 */\n"
    "        --kb-tag-blue-tx: var(--color-primary-6);\n"
    "        --kb-tag-purple-tx: rgb(var(--purple-6));\n"
    "        --kb-tag-magenta-tx: rgb(var(--magenta-6));\n"
)


def run(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        print("%-44s SKIP (not found)" % rel)
        return
    s = io.open(path, encoding="utf-8").read()
    msgs = []
    if "--kb-tag-blue-bg: #E7F0FF" in s:
        msgs.append("light=SKIP (already patched)")
    elif s.count(OLD_LIGHT) == 1:
        s = s.replace(OLD_LIGHT, NEW_LIGHT, 1)
        msgs.append("light=OK")
    elif OLD_LIGHT in s:
        msgs.append("light=FAIL (anchor x%d)" % s.count(OLD_LIGHT))
    else:
        msgs.append("light=FAIL (anchor missing)")

    if "--kb-tag-magenta-tx: rgb(var(--magenta-6));" in s and "--kb-tag-blue-tx: var(--color-primary-6);" in s:
        msgs.append("dark=SKIP (already patched)")
    elif s.count(OLD_DARK) == 1:
        s = s.replace(OLD_DARK, NEW_DARK, 1)
        msgs.append("dark=OK")
    elif OLD_DARK in s:
        msgs.append("dark=FAIL (anchor x%d)" % s.count(OLD_DARK))
    else:
        msgs.append("dark=FAIL (anchor missing)")

    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print("%-44s %s" % (rel, "  ".join(msgs)))


if __name__ == "__main__":
    run("pages/kanban.html")
    run("pages/req-kanban.html")
    run("mg-work/kanban/kanban-template.html")

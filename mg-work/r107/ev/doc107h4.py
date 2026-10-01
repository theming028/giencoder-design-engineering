# -*- coding: utf-8 -*-
"""r107 第七拍 · 刷新仓库 `.workbuddy/memory/MEMORY.md` 索引。
用法： python mg-work/r107/ev/doc107h4.py
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P = os.path.join(REPO, '.workbuddy', 'memory', 'MEMORY.md')

P343_INDEX = (
    u'｜**P3.43=r107 第七拍（六条）** ★★ **「渲染出来的字」与「渲染不出来的字」要分开判**'
    u'（渲染成文字的必改 / 外链 `href` **不改**（替换域名段即 404、且不渲染）/ 历代**设计来源注释保留**；'
    u'★ 顺手 `grep -i` 扫**别的页** —— 本拍在 `avatar.html` 又挖到 1 处；★ 自己新增的注释要避开被清理的词）/ '
    u'★★ **同一处改动先判「节点从哪来」：静态 HTML vs JS 现场生成**'
    u'（菜单标题行 = `.td-mm-cap`（写死的）+ `.td-ctx-head`（`ctxBuild()` 里建的）⇒ 删 HTML 治不全 '
    u'⇒ **一段 `display:none` 把两类一起关**，column flex 里塌行不占位、与删节点视觉等价）/ '
    u'★ **DS 组件「宽度不拉通」先查它自己的 `display`**'
    u'（`.giencoder-input-wrapper` 编译样式 = `inline-flex; width:auto` ⇒ 同卡别的行 308、它只有 207；'
    u'修法 = **写双类** `.giencoder-input-wrapper.td-commit-in{display:flex}`，不赌文档序）/ '
    u'★★ **「统一字体族」要分清「本代自己的样式」与「跨代沿用的移植件」**'
    u'（自己那 8 条就地改；「文件」模块代码区那条在 **r102 代已交付的 `part105/browse.css`** 里 '
    u'⇒ 页内**多一级类数覆盖**（`.td-browse .td-browse-pre`），153 个 `.td-code*` 靠继承；'
    u'★ **这条是「改完第一遍量出来才补的」⇒ 判据要覆盖整棵子树，别只验自己改过的那些选择器**）/ '
    u'★★ **联动显隐先量「状态类挂在哪一级」**'
    u'（`.av-browse-on` 实测挂在 shell flex 行 = `main` 与预览栏的共同父级 ⇒ **纯 CSS 可判**，'
    u'省掉一整个 MutationObserver；⚠ 只写要隐藏的那一枚，别用 `.r93-baracts` 整组）/ '
    u'跨页文案替换的锚点用**带引号的整串**（不碰同名注释、天然幂等）+ '
    u'**写回必须 `newline=\'\'` / 走二进制**（本仓页面 CRLF，默认 `\'w\'` 会把整页翻成 CRLF ⇒ 内容没变却全变 `M`）'
)

TABLE = [
    # 行 5：PAGES 索引
    (u'技能浮窗与 `.r93-alert` 随内容列自适应**）**）｜ `YYYY-MM-DD.md` 原始日志',
     u'技能浮窗与 `.r93-alert` 随内容列自适应** / **右栏竞品名全换 GienCoder + 菜单标题行与快捷键隐藏 + '
     u'选中项补底色 + 提交卡输入框拉通 + 右栏字体统一 + 全屏按钮随右栏联动**）**）｜ `YYYY-MM-DD.md` 原始日志', 1),
    (u'（r107 · 共六拍：三段式+五模块', u'（r107 · 共七拍：三段式+五模块', 1),

    # 行 7：PLAYBOOK 索引
    (u'｜ skill（用户级）：design-to-code-modular',
     P343_INDEX + u'｜ skill（用户级）：design-to-code-modular', 1),

    # 行 181 / 182
    (u'> **r107（2026-10-01 09:3x ~ 11:4x · 会话详情页「侧栏模块标签化」= 复刻 Codex 右栏 · 六拍）—— 🚫 未提交（新一代，承接 r106 `4d081ba`）**：',
     u'> **r107（2026-10-01 09:3x ~ 12:1x · 会话详情页「侧栏模块标签化」= 复刻 Codex 右栏 · 七拍）—— 🚫 未提交（新一代，承接 r106 `4d081ba`）**：', 1),
    (u'（由 `ev/make107.py` 从 `apply106.py` 做 **11 处精确替换**生成，命中数不符即 `sys.exit`）。',
     u'（由 `ev/make107.py` 从 `apply106.py` 做 **13 处精确替换**生成，命中数不符即 `sys.exit`）。', 1),

    # 六拍链 → 七拍链
    (u'> ★ 本代**六拍**（同一代、`apply107.py` 就地返工六次、**始终未提交**）：① 三段式骨架 + 五模块｜② 浮窗关不掉 / 侧聊对齐｜③ 侧聊全链路删 + 折叠修正 + 对照 Codex 补遗漏｜\n'
     u'> ④ 摘要默认 + 卡片式 + 划词浮条 + 右键菜单 + tab 14px + 全右栏下拉 DS 化｜⑤ hover 补齐 + **下拉换族**（`giencoder-menu` → **DS Dropdown**）｜\n'
     u'> ⑥ 统计行「伪元素 → 真节点」+ `.r93-pre` 去字体族 + 技能浮窗 / `.r93-alert` 随内容列自适应。',
     u'> ★ 本代**七拍**（同一代、`apply107.py` 就地返工七次、**始终未提交**）：① 三段式骨架 + 五模块｜② 浮窗关不掉 / 侧聊对齐｜③ 侧聊全链路删 + 折叠修正 + 对照 Codex 补遗漏｜\n'
     u'> ④ 摘要默认 + 卡片式 + 划词浮条 + 右键菜单 + tab 14px + 全右栏下拉 DS 化｜⑤ hover 补齐 + **下拉换族**（`giencoder-menu` → **DS Dropdown**）｜\n'
     u'> ⑥ 统计行「伪元素 → 真节点」+ `.r93-pre` 去字体族 + 技能浮窗 / `.r93-alert` 随内容列自适应｜\n'
     u'> ⑦ 右栏竞品名全换 GienCoder（含 `avatar.html` 1 处）+ 菜单标题行与快捷键隐藏 + 选中项补底色 + 提交卡输入框拉通 + 右栏字体统一 + 全屏按钮随右栏联动。', 1),

    # 第七拍要点
    (u'⑰ `.r93-pre { font-family: var(--font-family) }`（**不用 `inherit`**）｜⑱ 技能选择浮窗 `width: min(760px,100%) !important` + `.r93-alert { height:auto; min-height:44px; padding:8px 16px }`。',
     u'⑰ `.r93-pre { font-family: var(--font-family) }`（**不用 `inherit`**）｜⑱ 技能选择浮窗 `width: min(760px,100%) !important` + `.r93-alert { height:auto; min-height:44px; padding:8px 16px }`。\n'
     u'> **第七拍六条** = ⑲ 竞品名 → GienCoder（右栏**渲染成文字**的 8 处 + 2 处 `title`；三条外链 `href` 与历代注释**有意保留**；另清 `avatar.html` 1 处）；\n'
     u'> ⑳ 菜单标题行（`.td-mm-cap` + JS 的 `.td-ctx-head`）与快捷键（`.td-mm-key` + JS 的 `.td-ctx-key`）**一律 `display:none`**；\n'
     u'> ㉑ 选中项 `.is-checked` 补底色 `--color-primary-light-1`（原只有蓝字 + ✓）+ 提交卡 `.giencoder-input-wrapper.td-commit-in { display:flex }`（207 → 308）；\n'
     u'> ㉒ 右栏字体统一：`panel.css` 8 条就地改 + `.td-browse .td-browse-pre` 覆盖跨代移植件（判据 153 → 0）；\n'
     u'> ㉓ `.av-browse-on .r93-baract[data-r93-fullscreen] { display:none }`（全屏按钮随右栏显隐，纯 CSS）。', 1),

    # 产物 / 门禁 / 改动面
    (u'> **产物**：`conversation.html` **799231（= HEAD）→ 866988 → 876008 → 894916 → 920259 → 921730 → 925776 Unicode 字符**（六拍合计 **+126545**）；\n'
     u'> UTF-8 字节（LF 归一）**1012253** ｜ 工作区字节（CRLF）**1019153** ｜ LF `sha1 6655f13a1afd`；`base.html` **472150 逐字节不变**。\n'
     u'> **六查**：幂等 ✓（**每拍连跑两遍**）｜`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）｜',
     u'> **产物**：`conversation.html` **799231（= HEAD）→ 866988 → 876008 → 894916 → 920259 → 921730 → 925776 → 927464 Unicode 字符**（七拍合计 **+128233**）；\n'
     u'> UTF-8 字节（LF 归一）**1015265** ｜ 工作区字节（CRLF）**1022207** ｜ LF `sha1 79aa4533761b`；`base.html` **472150 逐字节不变**。\n'
     u'> **七查**：幂等 ✓（**每拍连跑两遍**）｜`check-syntax.py pages/*.html` **10/10**（conversation `script=9 style=16`）｜', 1),

    (u'> `git status` 只有 `M pages/conversation.html`（`+2202 / −3` 行）+ `?? mg-work/r107/`。',
     u'> `git status` = `M pages/conversation.html`（`+2244 / −3` 行）+ `M pages/avatar.html`（`+1 / −1`，第七拍文案）+ `?? mg-work/r107/`。', 1),

    (u'> ★★ **新增定论见 PLAYBOOK P3.39 ~ P3.42**；各拍要点见 **PAGES P3.11i（共六拍）**；逐条实测见 **`mg-work/r107/acceptance.md`（十一节）**。',
     u'> ★★ **新增定论见 PLAYBOOK P3.39 ~ P3.43**；各拍要点见 **PAGES P3.11i（共七拍）**；逐条实测见 **`mg-work/r107/acceptance.md`（十二节）**。', 1),
]


def main():
    b = io.open(P, 'rb').read()
    t = b.decode('utf-8')
    for old, new, want in TABLE:
        n = t.count(old)
        if n != want:
            sys.exit(u'!! 锚点命中 %d 次（应 %d 次）：%r' % (n, want, old[:80]))
        t = t.replace(old, new)
    io.open(P, 'wb').write(t.encode('utf-8'))
    print(u'   MEMORY.md %d → %d 字符'
          % (len(b.decode('utf-8').replace('\r\n', '\n')), len(t.replace('\r\n', '\n'))))
    for k in [u'共七拍', u'P3.43=r107 第七拍', u'927464', u'79aa4533761b', u'七查', u'12:1x']:
        print(u'     %s x %d' % (k, t.count(k)))
    for k in [u'共六拍', u'**六拍**', u'11 处精确替换', u'6655f13a1afd', u'1019153']:
        print(u'     残留 %r x %d' % (k, t.count(k)))


if __name__ == '__main__':
    main()

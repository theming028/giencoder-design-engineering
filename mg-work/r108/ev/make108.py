# -*- coding: utf-8 -*-
"""r108 · 由 `mg-work/r107/apply107.py` 精确替换生成 `mg-work/r108/apply108.py`。

为什么用「生成」而不是手抄：apply107.py 有 3594 行、内联了整份站点 CSS/JS 与移植件加载逻辑，
手抄必漏；精确替换 + 每处命中数断言，能保证**除下表 6 处外一字不差**（先例：ev/make106.py、ev/make107.py）。

★ r108 的核心体位决定：**nav 块继续沿用 r106 的名字（NAV_TAG='r106'）**。
  理由 —— 本代只改会话详情页的右栏（diff 卡片化 + 文件树抽屉），nav 跳转脚本一字未动；
  按硬规则「跨代沿用的宿主标记不换名」，不换代就能让 base.html 与 8 个外壳页**逐字节不变**，
  满足邵先生「绝对不得改动其他不必涉及的模块」。

用法： python mg-work/r108/ev/make108.py     # 写 apply108.py（先备份到 ev/apply108.prev.py）
"""
import io
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SRC = os.path.join(REPO, 'mg-work', 'r107', 'apply107.py')
DST = os.path.join(REPO, 'mg-work', 'r108', 'apply108.py')

# 表 = (说明, 旧串, 新串, 期望命中数)。命中数不符即 sys.exit（不做任何写入）。
EDITS = [
    (
        'E1 顶部标题 → r108',
        '"""r107 · 会话详情 · 侧栏模块标签化（**新代** —— r106 已交付 `4d081ba`，故不再就地返工）\n'
        '（承接 r106 代产物，仍是 pages/{base,conversation}.html）\n',
        '"""r108 · 会话详情 · diff 卡片化 + 文件树抽屉（**新代** —— r107 已交付 `e9c9498`，故不再就地返工）\n'
        '（承接 r107 代产物，仍是 pages/{base,conversation}.html）\n',
        1,
    ),
    (
        'E2 用法块 → r108',
        'mg-work/r107/apply107.py',
        'mg-work/r108/apply108.py',
        5,
    ),
    (
        'E2b 「见本文件顶部的 rNNN 段」措辞',
        '见本文件顶部的 r106 段',
        '见本文件顶部的 r108 段',
        2,
    ),
    (
        'E3 GENS 扩到六代（nav 继续沿用 r106）',
        "GENS = (\n"
        "    ('r93',  'r93-conv-css',  'r93-conv-js',  'r93-nav-js'),\n"
        "    ('r101', 'r101-conv-css', 'r101-conv-js', 'r101-nav-js'),\n"
        "    ('r102', 'r102-conv-css', 'r102-conv-js', 'r102-nav-js'),\n"
        "    ('r106', 'r106-conv-css', 'r106-conv-js', 'r106-nav-js'),\n"
        "    ('r107', 'r107-conv-css', 'r107-conv-js', 'r106-nav-js'),\n"
        ")\n",
        "GENS = (\n"
        "    ('r93',  'r93-conv-css',  'r93-conv-js',  'r93-nav-js'),\n"
        "    ('r101', 'r101-conv-css', 'r101-conv-js', 'r101-nav-js'),\n"
        "    ('r102', 'r102-conv-css', 'r102-conv-js', 'r102-nav-js'),\n"
        "    ('r106', 'r106-conv-css', 'r106-conv-js', 'r106-nav-js'),\n"
        "    ('r107', 'r107-conv-css', 'r107-conv-js', 'r106-nav-js'),\n"
        "    ('r108', 'r108-conv-css', 'r108-conv-js', 'r106-nav-js'),\n"
        ")\n"
        "# ★ r108：nav 块本代**依旧一字未改** ⇒ 继续沿用下面那行的 `NAV_TAG = 'r106'`\n"
        "#   （硬规则「跨代沿用的宿主标记不换名」）⇒ base.html 的 nav 块「摘下来再原样挂回去」，\n"
        "#   与 8 个外壳页一起**逐字节不变**。\n"
        "#   ⚠ 本代 CSS / JS 两块都改了 ⇒ 这两块**必须换名**成 `r108-conv-css` / `r108-conv-js`，\n"
        "#     否则「摘块」正则会连本代自己的新内容一起摘掉。\n",
        1,
    ),
    (
        'E4 PART_DIRS 加 part108（本代优先 → r107 回落 → r105 源件）',
        "PART_DIRS = (\n"
        "    os.path.join(HERE, 'part107'),\n"
        "    os.path.join(REPO, 'mg-work', 'r102', 'part105'),\n"
        ")\n",
        "PART_DIRS = (\n"
        "    os.path.join(HERE, 'part108'),\n"
        "    os.path.join(REPO, 'mg-work', 'r107', 'part107'),\n"
        "    os.path.join(REPO, 'mg-work', 'r102', 'part105'),\n"
        ")\n",
        1,
    ),
    (
        'E5 移植件注释里的目录名',
        '#   放进 mg-work/r107/part107/ 同名即可。',
        '#   放进 mg-work/r108/part108/ 同名即可。',
        1,
    ),
    (
        'E6 docstring 追加第十二拍说明',
        '         （实测约 4.5 千字符）⇒ make107 只在「本代首个补丁还没落地」时才跑。\n\n体位与历代一致：',
        '         （实测约 4.5 千字符）⇒ make107 只在「本代首个补丁还没落地」时才跑；\n'
        '         ★ **r108 同理**：`ev/make108.py` 会按 `apply107.py` 重新生成本文件 ⇒ 冲掉下面这段\n'
        '         「第十二拍」，故 make108 只在「本代首个补丁还没落地」时才跑。\n\n'
        '★ **第十二拍（2026-10-01 19:3x 邵先生两条）** —— **新代 r108**（r107 已交付 `e9c9498`，\n'
        '  工作区已干净 ⇒ 按硬规则「已交付才新建 rNN+1」开新一代，不再就地返工 apply107.py）；\n'
        '  注入块换名 `r108-conv-css` / `r108-conv-js`；★ **nav 块照旧沿用 `r106-nav-js`**（本代没碰 nav）⇒\n'
        '  `base.html` 与 8 个外壳页仍逐字节不变，本代仍只有 `conversation.html` 一页进 git diff。\n'
        '  落点全部在 `part108/{_mods.html,panel.css,panel.js}`。★ 改序 = `part108/_mods.html` →\n'
        '  `ev/splice108.py` → 本脚本；⚠ `part108/browse.html` 是 **splice108 的产物**、不是手改对象。\n'
        '    ① **`.td-diff` 从「平铺 + 分隔线」改成一张张独立小卡片** —— `.td-rv-body` 由\n'
        '       `padding: 4px 0 16px` 改 `flex` 纵列 + `gap: 8px` + `padding: 8px`；`.td-diff` 由\n'
        '       `border-bottom: 1px solid --color-border-1` 改 `1px 描边 + 8px 圆角 + --color-bg-2 底 +\n'
        '       overflow: hidden`（`overflow` 是为了让头部 hover 底色被圆角裁住，否则四角露方角）；\n'
        '       卡片头与代码区之间补一条 `border-top` 分隔线（折叠态 `.td-diff-rows` 本就是 `display:none`，\n'
        '       不会留残线）。\n'
        '    ② **「在文件树中定位」右侧新增一枚「文件树」按钮 ⇒ 点开在右栏右缘滑出文件树抽屉** ——\n'
        '       `.td-tree`（`position:absolute; inset:0; z-index:35`）= 半透明遮罩 + 右侧 `min(296px, 86%)`\n'
        '       面板（与「文件」模块的树同宽），从 `translateX(100%)` 滑入（220ms）；三条关闭路径 =\n'
        '       点遮罩 / 关闭按钮 / Esc（已接进 `panel.js` 的 Esc 裁决链，排在「提交模态」之后、「菜单」之前，\n'
        '       与 z-index 同序）。\n'
        '       ★★ **抽屉里的树刻意用独立类名 `td-tf*`（不是 `td-bf*`）** —— `ctrl-conv.js` 的\n'
        "          `pane.querySelectorAll('.td-bf')` 作用域是整个 `.td-browse`，复用同名类会把抽屉里的行\n"
        '          一起接管（`refresh()` / `selectFile()` 互相打架；且 `files` 变量只绑第一个\n'
        "          `.td-browse-files` ⇒ 抽屉里的行点了没反应）。✚ 对应地，抽屉树自己的展开/折叠 +\n"
        '          选中由 `panel.js` 新写一小段（与 ctrl-conv 同一套语义、互不干扰）。\n'
        '       ⚠ 「点那枚按钮」必须 `stopPropagation` —— 否则会冒到 `document` 的 closeMenus 那条，\n'
        '          把刚开的抽屉当「点了别处」立刻关掉。\n\n'
        '体位与历代一致：',
        1,
    ),
]


def main():
    s = io.open(SRC, encoding='utf-8', newline='').read()
    for label, old, new, want in EDITS:
        n = s.count(old)
        if n != want:
            sys.exit('!! %s：锚点命中 %d 次（应 %d 次）' % (label, n, want))
        s = s.replace(old, new)
    if os.path.exists(DST):
        shutil.copyfile(DST, os.path.join(HERE, 'apply108.prev.py'))
    io.open(DST, 'w', encoding='utf-8', newline='').write(s)
    print('   写出 %s（%d 行 / %d 字符，%d 处替换）'
          % (DST, s.count('\n') + 1, len(s), len(EDITS)))


if __name__ == '__main__':
    main()

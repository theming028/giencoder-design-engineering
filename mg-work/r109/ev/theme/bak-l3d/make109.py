# -*- coding: utf-8 -*-
"""r109 · 由 `mg-work/r108/apply108.py` 精确替换生成 `mg-work/r109/apply109.py`。

为什么用「生成」而不是手抄：apply108.py 有 3628 行、内联了整份站点 CSS/JS 与移植件加载逻辑，
手抄必漏；精确替换 + 每处命中数断言，能保证**除下表 7 处外一字不差**（先例：ev/make106~108.py）。

★ r109 的体位决定：**nav 块继续沿用 r106 的名字（NAV_TAG='r106'）**。
  理由 —— 本代只改会话详情页右栏的**浏览器模块**（标注流水线），nav 跳转脚本一字未动；
  按硬规则「跨代沿用的宿主标记不换名」，不换代就能让 base.html 与 8 个外壳页**逐字节不变**，
  满足邵先生「绝对不得改动其他不必涉及的模块」。

用法： python mg-work/r109/ev/make109.py     # 写 apply109.py（先备份到 ev/apply109.prev.py）
"""
import io
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SRC = os.path.join(REPO, 'mg-work', 'r108', 'apply108.py')
DST = os.path.join(REPO, 'mg-work', 'r109', 'apply109.py')

# 表 = (说明, 旧串, 新串, 期望命中数)。命中数不符即 sys.exit（不做任何写入）。
# ---------------------------------------------------------------- ③ 图标
# ★ r109 第二拍 · ③：重新生成图标（`.r93-ib.r93-bt`）的正身是 `ICON_INLINE['regen']`，
#   而 `apply109.py` 是本脚本从 `apply108.py` **逐字生成**的 ⇒ 修它 = 改本脚本的 EDITS 表
#   （重跑自愈；不存在「手改 apply109.py 被重生成冲掉」的隐患）。
#   判据与取证（`mg-work/r109/ev/tools/`）：
#     · `evalpath.py`     —— 把**真实 SVG path 串**解析后按 SS=8 覆盖率光栅化，与
#                            design-rgb.png 的 14px 盒逐像素比（含 SVG 弧的旗标推导）；
#     · `refiteregen.py`  —— 墨迹盒硬约束（(0.1,4.2)-(13.9,11.0)）下的坐标下降重拟。
#   ⚠ 防过拟合**不能**用「越界罚项」（设计真值在弧顶下方本来就有洞，罚项会连正确的
#     弧顶一起罚 ⇒ 解被推向另一侧，err 从 2.3 抬到 10.7）；正解是收紧参数的物理边界。
REGEN_OLD = (
        "    #   故重画为 **14 栅格**（与 `.r93-i14` 盒 1:1，stroke 1.3 就是设计稿的 1.3），\n"
        "    #   墨迹包络 0.5..13.9 × 4.5..10.6，与设计稿实测 0.5..14.5 × 4..10 对齐。\n"
        "    'regen': '<svg viewBox=\"0 0 14 14\" fill=\"none\" aria-hidden=\"true\">'\n"
        "             '<path d=\"M13.9 9.4A5 5 0 0 0 4.1 8.9\" stroke=\"currentColor\" stroke-width=\"1.3\" '\n"
        "             'stroke-linecap=\"round\"/><path d=\"M1.05 7.85 4.4 7.95 2.95 10.6Z\" '\n"
        "             'fill=\"currentColor\"/></svg>',\n"
)
REGEN_NEW = (
        "    # ★ r109 第二拍 ③：**重画**。上一版（r99 ⑭）是目测读法 ——「圆心 (9,10)、半径 5 的\n"
        "    #   上半圆 + 左下小三角」，实测右端被 14 盒裁平、箭头糊成一团。本拍把 `design-rgb.png`\n"
        "    #   的 14px 盒（png x956..969 / y225..231，墨迹实测 **14×7**）逐像素读出来，再用自造的\n"
        "    #   解析光栅化器（`mg-work/r109/ev/tools/evalpath.py`，SS=8 覆盖率）+ 边界约束坐标下降\n"
        "    #   （`refiteregen.py`）重拟：\n"
        "    #     旧版 err **15.05** → 新版 **2.30**（6.5×）；墨迹包络 (1,5)-(13,11)（设计 (0,4)-(13,10)）。\n"
        "    #   全图**只有 1 个格**与设计差 ≥0.33：`(x2,y8)` 设计 0 / 本版 0.84 —— 那是设计稿里\n"
        "    #   「弧的左端」与「左下实心箭头」之间**故意留的凹口**（弧的末端其实在 x3..x4 那两格），\n"
        "    #   「圆弧 + 凸三角形」两种图元表达不了凹口 ⇒ err 的下限就在这里，不是没拟好。\n"
        "    #   ⚠ 判据口径：**别只看总 err** —— 多起点寻优能拿到 err 2.19 的解，但它有 7 个格\n"
        "    #     差 ≥0.33（箭头在 y10 整行弱 0.4~0.5、弧左端弱 0.44）⇒ 视觉上「箭头变细」。\n"
        "    #     本版是「坏格数 = 1 / max|Δ| = 0.84」的解，这才是该取的解。\n"
        "    'regen': '<svg viewBox=\"0 0 14 14\" fill=\"none\" aria-hidden=\"true\">'\n"
        "             '<path d=\"M12.95 10.64A5.03 5.03 0 0 0 3.37 8.5\" stroke=\"currentColor\" '\n"
        "             'stroke-width=\"1.3\" stroke-linecap=\"round\"/>'\n"
        "             '<path d=\"M2.07 11.4 5.61 9.61 1.05 7.56Z\" fill=\"currentColor\"/></svg>',\n"
)

# ---------------------------------------------------------------- ② 卡片两端对齐
# ★ r109 第三拍 ②：邵先生「对话内容中的类似 `r93-card r93-card--edge` 这样的容器前面的
#   缩进都取消，两端都对齐吧」。`.r93-card` 的 CSS 长在 `apply109.py` 的内联样式里，
#   而 `apply109.py` 是本脚本从 `apply108.py` **逐字生成**的 ⇒ 与第二拍 ③（图标）同路：
#   改本脚本的 EDITS 表（重跑自愈）。⚠ 只改宽度两项，其余声明一字未动。
CARD_OLD = (
        "/* 卡片 ★ r95 ①：宽度改为**流式 + 右侧撑满** —— 保留设计稿 18px 左缩进，右侧填满内容列。\n"
        "   （原先写死 822px 是按设计稿量死：容器恰 840 时刚好，容器一变宽右侧就留白。） */\n"
        ".r93-card {\n"
        "  position: relative; width: calc(100% - 18px); margin-left: 18px; border-radius: 8px;\n"
)
CARD_NEW = (
        "/* ★ r109 第三拍 ②：**取消 18px 左缩进 ⇒ 两端对齐**（邵先生：「对话内容中的类似\n"
        "   `r93-card r93-card--edge` 这样的容器前面的缩进都取消，两端都对齐吧」）。\n"
        "   沿革：r95 ① 把写死的 822px 改成「流式 + 右侧撑满」，同时**保留设计稿的 18px 左缩进**\n"
        "   （`width: calc(100% - 18px)` + `margin-left: 18px`）—— 视觉上是一列右侧贴边、左侧留白 18px 的卡。\n"
        "   本拍按需求改成**满行等宽**：左右两端都贴内容列。\n"
        "   ⚠ 只动宽度这两项：`border-radius` / `background` / `padding` / 字号 / 高度一字未动\n"
        "     ⇒ 卡内的换行位置会随宽度变化（可用宽度 +18px），这是本需求的应有结果。\n"
        "   ⚠ `.r93-card--full`（下面那条 `width:100%; margin-left:0`）从此成为**本规则的冗余**，\n"
        "     但它是「显式满宽」的语义声明、且被多处调用，**保留不动**。 */\n"
        ".r93-card {\n"
        "  position: relative; width: 100%; margin-left: 0; border-radius: 8px;\n"
)

EDITS = [
    (
        'E9 对话卡片取消 18px 左缩进 ⇒ 两端对齐',
        CARD_OLD,
        CARD_NEW,
        1,
    ),
    (
        'E8 重新生成图标：r99 ⑭ 版 → r109-l2 重绘版',
        REGEN_OLD,
        REGEN_NEW,
        1,
    ),
    (
        'E1 顶部标题 → r109',
        '"""r108 · 会话详情 · diff 卡片化 + 文件树抽屉（**新代** —— r107 已交付 `e9c9498`，故不再就地返工）\n'
        '（承接 r107 代产物，仍是 pages/{base,conversation}.html）\n',
        '"""r109 · 会话详情 · 浏览器模块「标注流水线」重做（**新代** —— r108 已交付 `172e580`，故不再就地返工）\n'
        '（承接 r108 代产物，仍是 pages/{base,conversation}.html）\n',
        1,
    ),
    (
        'E2 用法块 → r109',
        'mg-work/r108/apply108.py',
        'mg-work/r109/apply109.py',
        5,
    ),
    (
        'E2b 「见本文件顶部的 rNNN 段」措辞',
        '见本文件顶部的 r108 段',
        '见本文件顶部的 r109 段',
        2,
    ),
    (
        'E3 GENS 扩到七代（nav 继续沿用 r106）',
        "    ('r108', 'r108-conv-css', 'r108-conv-js', 'r106-nav-js'),\n"
        ")\n"
        "# ★ r108：nav 块本代**依旧一字未改** ⇒ 继续沿用下面那行的 `NAV_TAG = 'r106'`\n"
        "#   （硬规则「跨代沿用的宿主标记不换名」）⇒ base.html 的 nav 块「摘下来再原样挂回去」，\n"
        "#   与 8 个外壳页一起**逐字节不变**。\n"
        "#   ⚠ 本代 CSS / JS 两块都改了 ⇒ 这两块**必须换名**成 `r108-conv-css` / `r108-conv-js`，\n"
        "#     否则「摘块」正则会连本代自己的新内容一起摘掉。\n",
        "    ('r108', 'r108-conv-css', 'r108-conv-js', 'r106-nav-js'),\n"
        "    ('r109', 'r109-conv-css', 'r109-conv-js', 'r106-nav-js'),\n"
        ")\n"
        "# ★ r109：nav 块本代**依旧一字未改** ⇒ 继续沿用下面那行的 `NAV_TAG = 'r106'`\n"
        "#   （硬规则「跨代沿用的宿主标记不换名」）⇒ base.html 的 nav 块「摘下来再原样挂回去」，\n"
        "#   与 8 个外壳页一起**逐字节不变**。\n"
        "#   ⚠ 本代 CSS / JS 两块都改了 ⇒ 这两块**必须换名**成 `r109-conv-css` / `r109-conv-js`，\n"
        "#     否则「摘块」正则会连本代自己的新内容一起摘掉。\n"
        "# ★ r108：以上同理（nav 沿用 `r106-nav-js`，注入块 `r108-conv-css` / `r108-conv-js`）。\n",
        1,
    ),
    (
        'E4 PART_DIRS 加 part109（本代优先 → r108 → r107 → r105 源件）',
        "PART_DIRS = (\n"
        "    os.path.join(HERE, 'part108'),\n"
        "    os.path.join(REPO, 'mg-work', 'r107', 'part107'),\n"
        "    os.path.join(REPO, 'mg-work', 'r102', 'part105'),\n"
        ")\n",
        "PART_DIRS = (\n"
        "    os.path.join(HERE, 'part109'),\n"
        "    os.path.join(REPO, 'mg-work', 'r108', 'part108'),\n"
        "    os.path.join(REPO, 'mg-work', 'r107', 'part107'),\n"
        "    os.path.join(REPO, 'mg-work', 'r102', 'part105'),\n"
        ")\n",
        1,
    ),
    (
        'E5 移植件注释里的目录名',
        '#   放进 mg-work/r108/part108/ 同名即可。',
        '#   放进 mg-work/r109/part109/ 同名即可。',
        1,
    ),
    (
        'E6 docstring 追加第一拍说明',
        '         「第十二拍」，故 make108 只在「本代首个补丁还没落地」时才跑。\n',
        '         「第十二拍」，故 make108 只在「本代首个补丁还没落地」时才跑。\n'
        '\n'
        '★ **第一拍（2026-10-02 08:5x 邵先生四条）** —— **新代 r109**（r108 已交付 `172e580`，\n'
        '  工作区已干净 ⇒ 按硬规则「已交付才新建 rNN+1」开新一代，不再就地返工 apply108.py）；\n'
        '  注入块换名 `r109-conv-css` / `r109-conv-js`；★ **nav 块照旧沿用 `r106-nav-js`**（本代没碰 nav）⇒\n'
        '  `base.html` 与 8 个外壳页仍逐字节不变，本代仍只有 `conversation.html` 一页进 git diff。\n'
        '  落点全部在 `part109/{_mods.html,panel.css,panel.js}`。★ 改序 = `part109/_mods.html` →\n'
        '  `ev/splice109.py` → 本脚本；⚠ `part109/browse.html` 是 **splice109 的产物**、不是手改对象。\n'
        '    ① **删掉 `.td-page-blank`**（浏览器视图顶部那条 26px 的灰带 + 它在 `.td-page` 上的\n'
        '       `margin: -12px -12px 12px` 负外边距一起清）—— HTML 与 CSS 两处都要删，不留死规则。\n'
        '    ② **`.td-annot-bar` 由「底部 sticky」改「顶部 sticky」**（`bottom: 0` → `top: 0`）——\n'
        '       原来贴在浏览器视图最底部、很容易被忽略；改顶部后与 `.td-url` 工具条上下呼应。\n'
        '    ③ **`.td-url-annot`（顶栏那枚「标注」胶囊）进批注态 ⇒ 变「退出批注」红胶囊** ——\n'
        '       浅底红 `--color-danger-light-1`(#FFECE8) + 红字/红描边 `--color-danger-6`(#F53F3F)，\n'
        '       文案由「标注」换「退出批注」（两个文字节点都要换）。\n'
        '    ④ **`.td-elnote`（发起批注卡片）按邵先生三张 MasterGo 稿像素级重做** —— 稿 1 = 空态、\n'
        '       稿 2 = 有内容态、稿 3 = 已批注锚点。结构由「整宽贴底卡片」改成\n'
        '       **pin(24×24) + 12px 间距 + 卡片(320 宽)** 的浮层；细节见 `ev/patch109l1.py` 顶部注释。\n',
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
        shutil.copyfile(DST, os.path.join(HERE, 'apply109.prev.py'))
    io.open(DST, 'w', encoding='utf-8', newline='').write(s)
    print('   写出 %s（%d 行 / %d 字符，%d 处替换）'
          % (DST, s.count('\n') + 1, len(s), len(EDITS)))


if __name__ == '__main__':
    main()

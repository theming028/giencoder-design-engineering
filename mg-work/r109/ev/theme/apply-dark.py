# -*- coding: utf-8 -*-
u"""r109 第四拍 ③-c：**全站 10 页的暗色适配层**。

★ 本拍的**唯一机制性变更**（第三拍只覆盖基础工作台 5 页 ⇒ 本拍扩到全 10 页）：
  ① `SCOPE` 5 → 10；② 作用域前缀去掉 `:not([data-r93-page])` 护栏。
  ⇒ 全 10 页的 `<html>` 都挂上 `data-gi-dark="1"`，机制层（apply-theme.py）的
    `DARK_OK` 才为真 ⇒ 用户选「深色 / 跟随系统」时**每一页**都真的变暗。

★★ 为什么「扩范围」这一步就能解决绝大部分混色（本拍最重要的实测结论）：
  **各页早就自带页面级暗色档了**。它们一直没生效，唯一原因就是机制层的护栏
  （`data-gi-dark` 缺失 ⇒ `DARK_OK=false` ⇒ 一律按浅色渲染）。实测各页已有的暗色档：
    · kanban / req-kanban —— `[giencoder-theme='dark'] { --kb-appbar: var(--color-bg-1); … }`
      + 十余条 `[giencoder-theme='dark'] .kb-xxx { … }`（全走 DS token）；
    · conversation —— `[giencoder-theme='dark'] { --r93-line: #333335; … }`
      + `[giencoder-theme='dark'] .td-browse { … }`（代码语法色）；
    · avatar —— `[giencoder-theme='dark'] { --av-hs-line: rgb(var(--gray-3)); }`；
    · base —— `[giencoder-theme='dark'] .dot-bg { … }`（点阵层）。
  ⇒ 本层只需补**它们没覆盖到的残差**（见下方 RULES / HOVERS 的 `★ r109 第四拍` 段）。

★ 为什么机制层（apply-theme.py）不够：
  机制层只把 `giencoder-theme="dark"` 挂到 `<html>` 上 —— DS 的 `--color-*` / `--gray-*`
  那套 token 立刻翻转（真机实测 `--color-bg-1: #17171a` ✓）。但**页面颜色几乎没变**，
  因为页面里大量颜色**根本不走 token**。逐个定位后一共五类，本脚本逐类收敛：

  ① **第二套 shadcn 风格 HSL token 层**（最隐蔽、影响最大）
     页面除 DS 之外还内联了 `:root{--background:0 0% 98.82%;--foreground:240 4.76% 4.12%;…}`
     （81 个 token），且
         `body{background-color:hsl(var(--background));color:hsl(var(--foreground))}`
     排在 DS 的 `body{color:var(--color-text-1);background:var(--color-bg-1)}` **之后**、
     同特异性 ⇒ **后者胜出**（同特异性看文档顺序）。而这套 token 不在 DS 暗色档里翻转
     ⇒ 暗色下 body 仍是浅底深字，且满屏 `rgb(10,10,11)` 文字都是**从 body 继承**来的。
     ⚠ 页面里其实自带一份标准的 `.dark{…}` 变体块，但它是**自成一体的灰阶**
       （`--background:0 0% 3.92%`），不是 DS 色彩系统 ⇒ 按邵先生「色值全部来自 DS」的要求
       **不用它**，改为把这套 token 在暗色档**重指到 DS 暗色 token**（消费方是 `hsl(var(--x))`，
       故必须写 HSL 三元组，由右侧 DS token 现算）。

  ② **React 写死的内联样式 / Tailwind 字面色**（不吃 token）
     · `div.flex.h-dvh` / `div.flex.min-h-0.flex-1` 内联 `background: rgb(244,245,246)`
     · Tailwind 字面色类 `.bg-[#F4F5F6]`（顶栏 / 侧栏）、`.bg-[#E4E6EA]`（分段轨道）、
       `.bg-white`（主面板 / 卡片）、`[class~="border-[var(--color-border-1)]"]`（面板描边）
     · 内联 `background: rgb(229,229,229)` / `rgb(255,255,255)` / `rgb(236,242,255)`
     ⇒ 内联样式**只能靠 `!important` 压**（内联的优先级只输给样式表里的 `!important`）。

  ③ **页面自定义变量的字面色**（声明在 **body 内**的 `<style>`，排在本块之后 ⇒ 靠特异性取胜）
     · `.av-main { --av-ink-2:#6B6B6B; --av-ink-4:#A9A9A9 }`（avatar 次级文字）
     · `.td-browse { --td-code-key:#0451A5; --td-code-str:#A31515; --td-code-num:#098658 }`
       （代码语法色，页面注释自己写了「DS 暂无对应语义 token」）
     ★★ 收敛手法 = **DS 阶梯镜像**：DS 的 `--gray-N` / `--blue-N` … 浅色档与暗色档是
        **镜像**的（`--gray-7` 浅=`107,107,107` ↔ 暗=`201,201,201`；`--blue-8` 浅=`17,75,163`
        ↔ 暗=`159,212,253`）。而页面里的字面值恰好踩在某个阶梯步上
        （`#6B6B6B` ≡ `--gray-7` 浅；`#A9A9A9` ≡ `--gray-5` 浅）⇒ 暗色档直接写
        `rgb(var(--gray-7))` 就**自动得到同一步阶的镜像亮度**。可证、可核、且浅色零风险。

  ④ **亮色 hover / 激活态**（静态截图看不见，但暗色下会「闪白」）
     `.ws-trigger-hover:hover{background-color:#e4e6ea!important}`、
     `.model-dropdown-menu-item:hover{background-color:#f3f4f5!important}`、
     `.ws-dropdown-hover:hover` / `.ws-item-hover:hover`、
     Tailwind `.hover\\:\\!bg-\\[\\#E9ECEE\\]:hover`（自带 `!important`）等。

  ⑤ **顶栏装饰位图**（唯一「整块亮」的残留）
     `r92-hdr-css` 给 `header[class*="h-12"]` 铺了 `assets/images/bg-img-1.png`
     （1580×134、平底 `#F6F8FA`、右侧 8px 点距点阵）⇒ 暗色下整条顶栏被这张浅色位图盖住
     （像素实测顶栏 `(243,245,248)` 而其余整屏已全暗）。
     ⚠⚠ **r92 / r101 两块注入在 `</body>` 前，排在本块之后、同特异性 ⇒ 必须带 `!important`。**
     修法：暗色档**不用这张位图**，用 DS token 现画同样的几何
     （`--color-bg-1` 平底 + `--gray-2` 圆点、8px 点距、只露右侧 ~23%，与素材的点阵区一致）。

★★ 作用域 = `html[giencoder-theme='dark']`：
  · 由机制层挂（用户选档 / 跟随系统）；
  · 第三拍曾带 `:not([data-r93-page])` 把 conversation.html 排除（那一拍只做 5 页），
    本拍**去掉**——10 页全部纳入，不再需要护栏；
  · 一条规则都不在浅色档生效 ⇒ **浅色零风险**（「不破坏稳定性」的硬保证）。

★ 幂等：先按 `RE_DARK` 剥旧块、再插 ⇒ 重跑逐字节不变。
★ 落点锚：紧跟 `<script id="r109-theme-js">…</script>` 之后（机制层的尾巴，唯一且稳定）。
  ⚠ 先跑 `apply-theme.py`，再跑本脚本。

用法： python mg-work/r109/ev/theme/apply-dark.py            # 10 页注入（幂等）
      python mg-work/r109/ev/theme/apply-dark.py --check    # 只报会改什么，不落盘
      python mg-work/r109/ev/theme/apply-dark.py --revert   # 剥块（回滚）
"""
import argparse
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PAGES = os.path.join(REPO, 'pages')
DS_CSS = os.path.join(REPO, 'giencoder-design-system', 'colors_and_type.css')

DARK_ID = 'r109-dark-css'

# ★ r109 第四拍 ③-c：作用域扩到**全站 10 页**（邵先生 2026-10-02：
#   「基础工作台还有很多页面的很多 UI 元素没有将浅色和暗色适配到位…请完全的彻底的解决」）。
#   ⚠ 顺序有意义：基础工作台 5 页排在前，与第三拍的清单逐字保持同序（便于 diff 对照）。
SCOPE = ('base', 'avatar', 'automation', 'skills', 'settings',
         'conversation', 'dev', 'kanban', 'req-kanban', 'task-detail')

# ---------------------------------------------------------------- DS 暗色 token
# ★ 逐字取自 giencoder-design-system/colors_and_type.css 的暗色块
#   （`body[giencoder-theme='dark'], [giencoder-theme='dark'] { … }`）。
#   `_check_ds()` 会拿这份表去核对该文件，防手抄漂移。
DS_DARK = {
    'bg-1': '#17171A', 'bg-2': '#232324', 'bg-3': '#2E2E30',
    'bg-4': '#484849', 'bg-5': '#5F5F60',
    'text-1': 'rgb(247, 247, 247)', 'text-2': 'rgb(229, 229, 229)',
    'text-3': 'rgb(169, 169, 169)', 'text-4': 'rgb(107, 107, 107)',
    'fill-1': 'rgb(31, 31, 31)', 'fill-2': 'rgb(43, 43, 43)',
    'fill-3': 'rgb(78, 78, 78)', 'fill-4': 'rgb(107, 107, 107)',
    'border-1': 'rgb(43, 43, 43)', 'border-2': 'rgb(78, 78, 78)',
    'border-3': 'rgb(107, 107, 107)', 'border-4': 'rgb(169, 169, 169)',
}

# ★ 原语阶梯（暗色档）。本脚本的「镜像替换」全靠它 ⇒ 一并核对。
DS_RAMP_DARK = {
    'gray-2': '43, 43, 43',
    'gray-5': '134, 134, 134',
    'gray-7': '201, 201, 201',
    'blue-8': '159, 212, 253',
    'red-8': '251, 172, 163',
    'green-7': '127, 209, 132',
    'giencoderblue-1': '5, 38, 112',
    'giencoderblue-2': '10, 56, 148',
    'giencoderblue-3': '19, 75, 184',
    'giencoderblue-6': '84, 151, 255',
}


def _dark_block():
    t = io.open(DS_CSS, encoding='utf-8').read()
    i = t.find("body[giencoder-theme='dark']")
    if i < 0:
        sys.exit('!! 在 %s 里找不到暗色块' % DS_CSS)
    return t[i:t.find('}', i) + 1]


def _check_ds():
    """核对本表与 DS 色系文件（防手抄漂移）。

    ⚠ DS 的语义 token 是**引用式**的：`--color-text-1: rgb(var(--gray-10))`、
      `--color-fill-1: rgb(var(--gray-1))` ⇒ 必须把 `--gray-N` 在同一块里解开再比。
    """
    blk = _dark_block()

    def raw(name):
        m = re.search(r'--%s\s*:\s*([^;}]+)' % re.escape(name), blk)
        return (m.group(1) if m else '').strip()

    def norm(v):
        """把 `rgb(var(--gray-N))` 解成 `rgb(r, g, b)`；顺手统一大小写与空格。"""
        v = v.strip()
        m = re.match(r'rgb\(\s*var\(--([a-z0-9-]+)\)\s*\)$', v)
        if m:
            tri = raw(m.group(1)).split(',')
            if len(tri) == 3:
                v = 'rgb(%s)' % ','.join(x.strip() for x in tri)
        return v.replace(' ', '').lower()

    bad = []
    for k, v in DS_DARK.items():
        got = raw('color-' + k)
        if norm(got) != norm(v):
            bad.append('--color-%s: DS=%r 本表=%r' % (k, got, v))
    for k, v in DS_RAMP_DARK.items():
        got = raw(k)
        if got.replace(' ', '').lower() != v.replace(' ', '').lower():
            bad.append('--%s: DS=%r 本表=%r' % (k, got, v))
    if bad:
        sys.exit('!! DS 暗色 token 与本表不一致：\n   ' + '\n   '.join(bad))


def _hsl(v):
    """`#RRGGBB` / `rgb(r, g, b)` → `H S% L%`（供 `hsl(var(--x))` 消费）。"""
    m = re.match(r'#([0-9a-fA-F]{6})$', v.strip())
    if m:
        h = m.group(1)
        r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    else:
        m = re.match(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$', v.strip())
        if not m:
            sys.exit('!! 认不出的色值：%r' % v)
        r, g, b = (int(m.group(i)) / 255.0 for i in (1, 2, 3))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2.0
    if mx == mn:
        hu = s = 0.0
    else:
        d = mx - mn
        s = d / (2.0 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            hu = ((g - b) / d) % 6.0
        elif mx == g:
            hu = (b - r) / d + 2.0
        else:
            hu = (r - g) / d + 4.0
        hu *= 60.0
    return '%.4g %.4g%% %.4g%%' % (round(hu, 3), round(s * 100, 3), round(l * 100, 3))


# ------------------------------------------------------- ① shadcn token → DS
# 左 = 页面里那套 shadcn HSL token；中 = 本拍给它指定的 DS 暗色 token。
BRIDGE = [
    ('background',           'bg-1',     '页面底'),
    ('foreground',           'text-1',   '正文'),
    ('card',                 'bg-2',     '卡片 / 容器面'),
    ('card-foreground',      'text-1',   '卡片正文'),
    ('popover',              'bg-3',     '浮层底'),
    ('popover-foreground',   'text-1',   '浮层正文'),
    ('primary',              'text-1',   '反转面（浅色下 near-black ⇒ 暗色下 near-white）'),
    ('primary-foreground',   'bg-1',     '反转面上的字'),
    ('secondary',            'fill-2',   '次级面'),
    ('secondary-foreground', 'text-1',   '次级面上的字'),
    ('muted',                'fill-2',   '弱化面'),
    ('muted-foreground',     'text-3',   '弱化文字（次级说明）'),
    ('accent',               'fill-2',   '强调面（hover 底）'),
    ('accent-foreground',    'text-1',   '强调面上的字'),
    ('border',               'border-2', '全局描边（`*{border-color:hsl(var(--border))}`）'),
    ('input',                'border-2', '输入框描边'),
    ('ring',                 'border-3', '焦点环'),
]

# ------------------------------------------------------------- ② 硬值覆盖
# ★ 值一律取 DS token（`var(--color-*)` / `rgb(var(--gray-N))`），不写任何字面色。
# ★ `!important` 给「有内联样式挡着」的、以及「竞争规则排在本块之后」的。
RULES = [
    # ---- 外壳 / 侧栏 / 内容区：React 内联灰底 + Tailwind 字面 bg-[#F4F5F6] ----
    ('__SHELL__', 'background-color: var(--color-bg-1) !important',
     '外壳 / 侧栏 / 内容区'),
    # ---- 面板与卡片：Tailwind 字面 .bg-white（主面板 + 内嵌白卡）----
    ('__PANEL__', 'background-color: var(--color-bg-2) !important',
     '主面板 / 白卡'),
    ('__PANEL_HOVER__', 'background-color: var(--color-bg-3) !important',
     '白卡的 hover 态（原文是 .hover\\:bg-white:hover）'),
    # ---- 面板描边 #ECEEF2（字面色类）----
    ('__PANEL_BORDER__', 'border-color: var(--color-border-1) !important',
     '主面板描边'),
    # ---- 分段控件轨道 #E4E6EA ----
    ('__SEGTRACK__', 'background-color: var(--color-fill-3)',
     '分段控件轨道'),
    ('__SEGTRACK_BORDER__', 'border-color: var(--color-fill-3)',
     '分段控件轨道描边'),
    # ---- 「新建会话」按钮：内联 rgba(255,255,255,.5) + 内白发光；原文 hover 带 !important ----
    ('__NEWCHAT__', 'background: var(--color-fill-2) !important;'
                    ' border-color: var(--color-border-1) !important;'
                    ' box-shadow: none !important',
     '新建会话按钮（含内联的 inset 白色高光）'),
    ('__NEWCHAT_HOVER__', 'background: var(--color-fill-3) !important',
     '新建会话按钮 hover'),
    # ---- 内联写死的浅色（React 生成，属性选择器 + !important）----
    ('[style*="background: rgb(229, 229, 229)"]',
     'background-color: var(--color-border-2) !important',
     '顶栏分隔条（内联 #E5E5E5）'),
    ('[style*="background: rgb(255, 255, 255)"]',
     'background-color: var(--color-bg-2) !important',
     '内联白底按钮'),
    # ---- 设置页侧栏图标盒：`.r85-ic{background:var(--color-fill-3);color:#6B6B6B}`
    #      ⇒ 暗色下 #6B6B6B 压 --color-fill-3（暗 = 78,78,78）对比仅 1.5:1，几乎看不清。
    #      ★ 用镜像步 `--gray-7`（浅 = 107,107,107 ≡ #6B6B6B；暗 = 201,201,201）
    ('__R85IC__', 'color: rgb(var(--gray-7))',
     '设置页侧栏图标盒 .r85-ic（#6B6B6B ≡ --gray-7 浅）'),
    # ---- 蓝色 chip：内联 background #ECF2FF / color #3770F7 / border #D3E2FF ----
    #      ★ 三个值都恰好踩在 DS giencoderblue 阶梯上（#3770F7 ≡ --giencoderblue-6 浅）
    ('[style*="background: rgb(236, 242, 255)"]',
     'background-color: rgb(var(--giencoderblue-1)) !important;'
     ' color: rgb(var(--giencoderblue-6)) !important;'
     ' border-color: rgb(var(--giencoderblue-2)) !important',
     '蓝色 chip（#ECF2FF / #3770F7 / #D3E2FF ⇒ DS giencoderblue 1/6/2）'),
    # ---- DS 次级按钮被 React 内联压掉 token：`background: rgba(255,255,255,.5)`
    #      + `color: #1F1F1F` + `box-shadow: inset … rgba(255,255,255,.9)`（内白发光）
    #      ⇒ 内联只在「样式表里的 !important」面前低头 ⇒ 三条都带 `!important`。
    ('[style*="background: rgba(255, 255, 255, 0.5)"]',
     'background: var(--color-fill-2) !important;'
     ' color: var(--color-text-1) !important;'
     ' border-color: var(--color-border-1) !important;'
     ' box-shadow: none !important',
     'DS 次级按钮（内联 rgba 白底 + #1F1F1F 字 + 内白发光的整体覆盖）'),
    # ---- React 内联字色（DOM 里被规范化成 `rgb(r, g, b)`，属性选择器按这个形态写）----
    ('[style*="color: rgb(31, 31, 31)"]',
     'color: var(--color-text-1) !important',
     '内联 #1F1F1F 字（≡ --color-text-1 浅，最多；「新会话」/ 菜单项 / skill 名）'),
    ('[style*="color: rgb(30, 30, 30)"]',
     'color: var(--color-text-1) !important',
     '内联 #1E1E1E 字（模型菜单项 textColor，≈ --color-text-1 浅）'),
    ('[style*="color: rgb(107, 107, 107)"]',
     'color: rgb(var(--gray-7)) !important',
     '内联 #6B6B6B 字（≡ --gray-7 浅 107,107,107）'),
    ('[style*="color: rgb(169, 169, 169)"]',
     'color: rgb(var(--gray-5)) !important',
     '内联 #A9A9A9 字（≡ --gray-5 浅 169,169,169）'),
    # ---- SVG 的 fill 是**呈现属性**（不是内联样式）⇒ 用属性选择器即可，无需 !important。
    #      ⚠ 别写成 `path[fill=…]`：同一批字面值也直接挂在 `<svg>` 上。 ----
    ('[fill="#1F1F1F"]', 'fill: var(--color-text-1)',
     'SVG fill #1F1F1F（≡ --color-text-1 浅）'),
    ('[fill="#1E1E1E"]', 'fill: var(--color-text-1)',
     'SVG fill #1E1E1E（≈ --color-text-1 浅 #1F1F1F）'),
    ('[fill="#6B6B6B"]', 'fill: rgb(var(--gray-7))',
     'SVG fill #6B6B6B（≡ --gray-7 浅）'),
    ('[fill="#A9A9A9"]', 'fill: rgb(var(--gray-5))',
     'SVG fill #A9A9A9（≡ --gray-5 浅）'),
    # ---- 搜索框 placeholder：`.ws-search-input::placeholder{color:#a9a9a9}` ----
    ('__PLACEHOLDER__', 'color: rgb(var(--gray-5))',
     '搜索框 placeholder #A9A9A9'),
    # ---- ★ 第 74 轮「新会话」复刻（`r74-nc-css`，只落在 4 页、base 没有）----
    #      它把第 74 轮那枚按钮的**字面色**逐个复刻：半透明白底 / #E4E6EA 描边 /
    #      内白发光 / #1F1F1F 字 / mask 图标 #1F1F1F / ⌘K #A9A9A9 / hover #FFFFFF。
    #      ⚠⚠ 它的选择器特异性是 **(0,4,1)**（1 元素 + 2 类 + 2 属性），
    #        高于本块常规前缀的 (0,3,1) ⇒ **必须原样复用同一串选择器**再叠前缀
    #        （叠完 (0,6,1)）+ `!important`，否则暗色下这枚按钮始终是半透明白底。
    ('__NC74__', 'background: var(--color-fill-2) !important;'
                 ' border-color: var(--color-border-1) !important;'
                 ' box-shadow: none !important;'
                 ' color: var(--color-text-1) !important',
     '第 74 轮「新会话」复刻主体（半透明白底 / #E4E6EA 边 / 内白发光 / #1F1F1F 字）'),
    ('__NC74_HOVER__', 'background: var(--color-fill-3) !important',
     '…hover（原文 #FFFFFF!important）'),
    ('__NC74_BEFORE__', 'background-color: var(--color-text-1) !important',
     '…mask 画出的对话气泡图标（原文 #1F1F1F）'),
    ('__NC74_AFTER__', 'color: rgb(var(--gray-5)) !important',
     '…右侧 ⌘K 提示（原文 #A9A9A9 ≡ --gray-5 浅）'),
    # ================================================================ ★ r109 第四拍
    # ---- ⑥-a 研发工作台外壳：**Tailwind 任意值类**（编译后的 React bundle 产出）----
    #   ⚠ 为什么走 `[class~="…"]` 而不是「把类里的字面色换成 token」：
    #     它编译出来是 `.bg-\[\#E5EDF5\]{--tw-bg-opacity:1;background-color:rgb(229 237 245/var(--tw-bg-opacity,1))}`
    #     —— 值里挂着 `--tw-bg-opacity` 这条**透明度通道**，直接换成 `rgb(var(--gray-N))`
    #     会连通道一起丢掉（`bg-opacity-*` 从此失效）⇒ 风险不对等，沿用本脚本既有手法。
    ('__DEV_SHELL__', 'background-color: var(--color-bg-1) !important',
     '研发工作台外壳底（`bg-[var(--color-fill-2)]`；React 按路由选 base/dev 两色。原为冷灰字面色类）'),
    ('__DEV_PILL__', 'background-color: var(--color-fill-3) !important',
     '顶栏「基础/研发工作台」切换胶囊底（`bg-[var(--color-border-2)]`；原为冷灰字面色类）'),
    ('__DEV_PILL_BG__', 'background-color: var(--color-fill-3) !important',
     '同上的另一档 #C9CDD3（`bg-[#C9CDD3]`）'),
    ('__DEV_PANE_BD__', 'border-color: var(--color-border-1) !important',
     '内容区描边（`border-[var(--color-border-2)]`；原为冷灰字面色类）'),
    # ---- ⑥-b 需求看板「统计瓷片」的彩色底：**静态 HTML 里的内联样式** ----
    #   ⚠ 这三个底写在 KB_HTML 模板串里，形态是**十六进制**（不是 React 规范化后的 rgb()）
    #     ⇒ 属性选择器必须按 `#E3EEFF` 这个样子写（且大小写敏感）。
    ('[style*="#E3EEFF"]', 'background-color: rgba(var(--blue-6), 0.24) !important',
     '统计瓷片·进行中（内联 #E3EEFF）'),
    ('[style*="#E2F4E4"]', 'background-color: rgba(var(--green-6), 0.24) !important',
     '统计瓷片·已完成（内联 #E2F4E4）'),
    ('[style*="#FFECD9"]', 'background-color: rgba(var(--orange-6), 0.24) !important',
     '统计瓷片·已取消（内联 #FFECD9）'),
    # ---- ⑥-c 同色但走**样式表**的两处（内联选择器打不到）----
    ('__RQ_ENTRY__', 'background: rgba(var(--orange-6), 0.24)',
     '需求条目标签底 #FFECD9'),
    ('__RQ_CANCEL__', 'background: rgba(var(--orange-6), 0.24)',
     '需求状态·已取消底 #FFECD9'),
    # ---- ⑥-e 本页覆盖掉 DS 组件本体的那一处（**唯一一处**，实测扫出）----
    #   `.r85-sw.giencoder-switch { background: rgb(var(--gray-7)) }` 是 r85 为对齐设计稿
    #   （40×24）加的**页面级覆盖**，它把 DS 组件本体的 `var(--color-fill-3)` 顶掉了。
    #   浅色档 `--gray-7` = 107（一档中深灰，符合设计稿）；暗色档**阶梯是镜像的**
    #   ⇒ `--gray-7` 变 201，开关轨道在暗色下**发亮**，看着像「已开启」。语义反了。
    #   修法 = **保亮度不保索引**：暗色档改挂 `--gray-4`（暗色档 = 107），与浅色档同亮度。
    ('__R85_SW_TRACK__', 'background: rgb(var(--gray-4)) !important',
     'settings 开关·未选中轨道（页面覆盖 DS 本体，暗色档镜像错位）'),

    # ================================================================ ★ r109 第四拍（裁决落地）
    # ---- ⑦ 品牌 logo **内部**的浅色装饰（邵先生 2026-10-02 裁决①）----
    #   现场：工作空间标识（`ws-trigger` 紫方块）内部有一片 `fill:'#F5E8FF'` 的浅紫装饰，
    #   `apply-tokens.py` 按「逐位等值」把它换成了 `rgb(var(--purple-1))` ——
    #   浅色档恰好 = `#F5E8FF`（正确），但**暗色档 `--purple-1` = `rgb(22,0,77)`**（深紫）
    #   ⇒ 压在 `#9E67E1` 紫块上「耳朵变黑洞」（像素取证：t2 暗色 `(245,232,255)`×11 →
    #   t3 暗色 `(22,0,77)`×11；浅色档 t2/t3 逐像素完全相同）。
    #   ★ 裁决 = **保留变量 + 暗色档定向覆盖**（不还原字面）。
    #   ★ 覆盖值取**紫色阶梯的镜像步** `--purple-10`：暗色档 = `245,232,255` ≡ 浅色档 `--purple-1`
    #     ⇒ 两档**同一支浅紫**，且全程只用 DS 变量（不写任何绝对色值）。
    #   ⚠ 选择器用 `*="var(--purple-1))"`（带双右括号）而不是 `*="var(--purple-1)"`：
    #     后者是 `var(--purple-10)` 的**真前缀** ⇒ 会顺带命中紫色阶梯的另一档。
    #   ⚠ 用属性选择器（不是 `[style*=]`）：`fill` 在 SVG 上是**呈现属性**，优先级低于任何 CSS 规则。
    ('[fill*="var(--purple-1))"]', 'fill: rgb(var(--purple-10))',
     '品牌标识内部浅紫装饰（浅色 = --purple-1；暗色档镜像步 --purple-10 = 同一支 #F5E8FF）'),

    # ================================================ ★ r109 第四拍（邵先生裁决③落地）
    # 出处：`scan-state.sh` + `p-state.js`（**真鼠标驱动**的逐状态亮面审计）在 10 页上的取证。
    #   ★★ 为什么必须真鼠标：JS 合成 `el.click()` **打不开**本站的浮层（实测点完
    #      `aria-expanded` 仍是 `false`），于是「逐状态」会退化成「默认态重复扫描」，
    #      权限浮层 / 技能浮层这类只存在于展开态的元素**一条都扫不到**（假阴性）。
    #   ★★ 内联属性选择器必须写 **CSSOM 规范化后**的形态（实测序列化结果，不是源串）：
    #      React 写 `#E5E5E5`，`getAttribute('style')` 读回来是 `rgb(229, 229, 229)`；
    #      `box-shadow` 的颜色会被**提到前面**、`inset` 挪到**末尾**：
    #        `0px 8px 20px 0px rgba(0,0,0,.08), inset 0px 3px 3px 0px #FFFFFF`
    #        ⇒ `rgba(0, 0, 0, 0.08) 0px 8px 20px 0px, rgb(255, 255, 255) 0px 3px 3px 0px inset`
    #      （`apply-dark.py` 里既有的 `[style*="#E3EEFF"]` 之所以能用十六进制，是因为它打的是
    #        **静态 HTML 里的内联样式**（浏览器按源串存），与 React 写入的两套规范化路径不同。）
    ('[style*="background: rgba(255, 255, 255, 0.88)"]',
     'background: rgba(var(--gray-1), 0.9) !important;'
     ' border-color: var(--color-border-1) !important;'
     ' box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.45) !important',
     '浮层材质·玻璃白底（权限浮层 280×126 / 技能浮层 760×320，React 内联）'),
    ('[style*="border: 1px solid rgb(229, 229, 229)"]',
     'border-color: var(--color-border-1) !important',
     '浮层与下拉的 1px 描边 #E5E5E5（工作空间下拉 356×32 容器 + 48×20 徽标）'),
    ('[style*="rgb(255, 255, 255) 0px 3px 3px 0px inset"]',
     'box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.45) !important',
     '浮层内白发光（原文 inset 0px 3px 3px 0px #FFFFFF）'),
    ('[style*="rgb(229, 229, 229) 0px 0px 0px 1px inset"]',
     'box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.45) !important',
     '「添加内容」菜单的 inset 亮环（原文 inset 0 0 0 1px #E5E5E5）'),
    ('[style*="border: 1px solid rgb(242, 242, 242)"]',
     'border-color: var(--color-border-1) !important',
     '技能行「自有」徽标描边 #F2F2F2'),
    # ---- ⑨ 页面级浮层 / 提示条：写在**样式表**里的字面色（属性选择器打不到，走类选择器）----
    #   ★ 描边取**镜像步**（`--giencoderblue-2` 暗色档 = 浅色 giencoderblue-9）⇒ 保色相、同亮度关系。
    ('.r81-ws-item[aria-selected="true"]',
     'box-shadow: inset 0 0 0 1px rgb(var(--giencoderblue-2))',
     '工作空间下拉·选中行描边 #D3E2FF（≡ --giencoderblue-2 浅，走镜像步）'),
    ('.td-skill-pop',
     'background: rgba(var(--gray-1), 0.9) !important',
     'task-detail 技能浮层底 rgba(255, 255, 255, 0.88)'),
    ('.td-coop .giencoder-modal',
     'background: var(--color-bg-2) !important',
     'task-detail 协作弹窗底 rgba(255, 255, 255, 0.95)'),
    #   ★★ 这一条是**DS 自身的配对裂缝**，值得单独记：`.r85-toast{background:var(--color-tooltip-bg);
    #      color:var(--color-white)}`，而 `--color-tooltip-bg` 两档都声明成 `rgb(var(--gray-10))`
    #      —— `--gray-10` 是**镜像**的（暗色档 = 247,247,247）⇒ 暗色下提示条翻成**浅底**，
    #      而字色 `--color-white` 是**语义锚点**（两档都是 #ffffff）⇒ **白底白字**（比值 ≈1.05）。
    #      这里只补字色（最小改动、保住 DS「反色胶囊」的原意：暗色档 = 浅底深字）。
    #   ★★ 同一处裂缝的**更大受害者**：DS 自带的 Tooltip 组件（10 页编译 bundle 里每页都有）。
    #      它写的是 `... bg-[var(--color-tooltip-bg)] ... text-[color:var(--color-white)]`
    #      —— 与 `.r85-toast` **同一对 token、同一个病**：暗色档底 = gray-10 = 247（浅底），
    #      字 = `--color-white`（**语义锚点**，两档恒 #ffffff）⇒ 白底白字、比值 ≈1.05，悬停即不可读。
    #      ★ 为什么前三轮扫描一条都没扫到：它是**悬停才挂载的 portal**（`createPortal` 进 body），
    #        默认态、点击展开态都不在 DOM 里 ⇒ 属「hover 态」一类，只能由 `scan-hover.sh` 兜住。
    #      ★ 只补**字色**（保住 DS「反色胶囊」原意：暗色档 = 浅底深字），
    #        特异性 `html[giencoder-theme='dark'] [role="tooltip"]` = (0,2,1)
    #        压得住 Tailwind 任意值的 `text-[color:...]` = (0,1,0)，不需要 `!important`。
    ('[role="tooltip"]', 'color: rgb(var(--gray-1))',
     'DS Tooltip 组件：暗色档底翻浅（--color-tooltip-bg=gray-10）、字色恒白 ⇒ 白底白字（悬停态）'),
    ('.r85-toast', 'color: rgb(var(--gray-1))',
     'settings 提示条：暗色档 --color-tooltip-bg 翻成浅底，字色仍是 --color-white ⇒ 白底白字'),
    #   ★★ 同一条裂缝的**另两处实现**（都在 `avatar`，10 页各带一份）：
    #      `.avatar-tooltip`（静态 HTML 里的悬停身份提示）与 `.av-tip`（JS 自绘的图标按钮 tooltip）
    #      —— 前者原写死 `background: rgba(29,33,41,.8)`，后者用 `var(--color-tooltip-bg)`，
    #      **两个都是深底 + `color: var(--color-white)`**。底色已由 `apply-tokens.py` 第七批·B
    #      收敛成 `rgba(var(--gray-10), .8)`（暗色档随镜像翻浅）⇒ 这里只补**字色**。
    #   ★ 至此**四处 tooltip / 提示条实现**（DS 组件 / `.r85-toast` / `.avatar-tooltip` / `.av-tip`）
    #     全部落到同一对语义上：底 = `--color-tooltip-bg` 家族、字 = 对侧灰。
    ('.avatar-tooltip', 'color: rgb(var(--gray-1))',
     'avatar 悬停身份提示：磨砂底暗色档翻浅 ⇒ 字色补对侧（原 --color-white）'),
    ('.av-tip', 'color: rgb(var(--gray-1))',
     'avatar 图标按钮 tooltip：同上（原 --color-white）'),
]

SEL_TOKENS = {
    '__SHELL__': ['[class~="bg-[var(--color-fill-1)]"]', '.flex.h-dvh', '.flex.min-h-0.flex-1'],
    '__PANEL__': ['.bg-white', '.bg-white\\/50'],
    '__PANEL_HOVER__': ['.hover\\:bg-white:hover'],
    '__PANEL_BORDER__': ['[class~="border-[var(--color-border-1)]"]'],
    '__SEGTRACK__': ['[class~="bg-[var(--color-border-2)]"]'],
    '__SEGTRACK_BORDER__': ['[class~="border-[var(--color-border-2)]"]'],
    '__NEWCHAT__': ['.new-chat-btn'],
    '__NEWCHAT_HOVER__': ['.new-chat-btn:hover'],
    '__R85IC__': ['.r85-ic'],
    '__PLACEHOLDER__': ['.ws-search-input::placeholder'],
    # ★ 第 74 轮「新会话」复刻：**原样复用它的长选择器**（特异性 (0,4,1) 及以上才能压住）
    '__NC74__': ['__NC74_SEL__'],
    '__NC74_HOVER__': ['__NC74_SEL__:hover'],
    '__NC74_BEFORE__': ['__NC74_SEL__::before'],
    '__NC74_AFTER__': ['__NC74_SEL__::after'],
    # ★ r109 第四拍 ⑥-a：Tailwind 任意值类（编译产物，类名逐字照抄）
    '__DEV_SHELL__': ['[class~="bg-[var(--color-fill-2)]"]'],
    '__DEV_PILL__': ['[class~="bg-[var(--color-border-2)]"]'],
    '__DEV_PILL_BG__': ['[class~="bg-[#C9CDD3]"]'],
    '__DEV_PANE_BD__': ['[class~="border-[var(--color-border-2)]"]'],
    # ★ r109 第四拍 ⑥-c：样式表里的两处橙底（内联选择器打不到）
    '__RQ_ENTRY__': ['.rq-type--entry'],
    '__RQ_CANCEL__': ['.rq-status--cancel'],
    # ★ r109 第四拍 ⑥-e：页面覆盖 DS 开关本体的那一处（未选中轨道）
    '__R85_SW_TRACK__': ['.r85-sw.giencoder-switch'],
}

# ------------------------------------------- ⑥-d 页面级「冷灰外壳」变量的暗色档
# ★ 这些变量在**各页自己的 `:root`** 里声明成硬编码的冷灰（`#E5EDF5` / `#DAE3ED`），
#   离 DS 灰阶 Δ11~16 且**有色相差**（DS 灰阶是纯中性）⇒ `apply-tokens.py` 按
#   「不得影响浅色模式」把它们**排除**了（见该脚本 EXCLUDE_VALUES）。
#   这里用暗色档定向覆盖：`html[giencoder-theme='dark']` 的特异性 (0,1,1) 高于页面 `:root` (0,1,0)
#   ⇒ 稳赢；而浅色档一个字都不生效 ⇒ **浅色零风险**。
#   ⚠ 变量是**继承**的，故挂在 `html` 上即可覆盖整棵子树（已核：这些变量都声明在 `:root`）。
#   ★ 2026-10-02 批次二之后，本表**只剩两个真·无 token 可用的变量**：
#     `--td-appbar` / `--td-pane-line` / `--r81-hover-bg` 的**字面值**已由 `apply-tokens.py`
#     的 OVERRIDE 表换成 `var(--color-fill-3)` / `var(--color-border-2)`（自身即随档翻转）
#     ⇒ 必须从本表**撤掉**，否则 `--td-pane-line` 会拿 `--color-border-1`（暗色档 = 242 浅灰）
#     盖掉正确值，暗色下出现一条**发亮的分栏线**（本拍实测踩到）。
PAGE_VARS = [
    ('--kb-surround', 'var(--color-bg-1)', 'kanban 页面底 #E5EDF5（冷灰，Δ16 无等值 token）'),
    ('--td-surround', 'var(--color-bg-1)', 'task-detail 页面底 #E5EDF5（同上）'),
]

# ---------------------------------------------- ③ 局部变量重声明（镜像替换）
# (选择器, [(变量, DS 暗色值, 说明)])
LOCAL_VARS = [
    ('.av-main', [
        ('--av-ink-2', 'rgb(var(--gray-7))', '#6B6B6B ≡ --gray-7 浅'),
        ('--av-ink-4', 'rgb(var(--gray-5))', '#A9A9A9 ≡ --gray-5 浅'),
    ]),
    ('.td-browse', [
        ('--td-code-key', 'rgb(var(--blue-8))', '#0451A5 ≈ --blue-8 浅 (Δ≈13,6,2)'),
        ('--td-code-str', 'rgb(var(--red-8))', '#A31515 ≈ --red-8 浅 (Δ≈2,0,9)'),
        ('--td-code-num', 'rgb(var(--green-7))', '#098658 ≈ --green-7 浅 (Δ≈39,15,29)'),
    ]),
]

# --------------------------------------------------- ④ 亮色 hover / 激活态
# ★ 这些在静态截图里看不见，但暗色下会「闪白」⇒ 一并收敛（DS 面 token，不用色阶）。
HOVERS = [
    ('.ws-trigger-hover:hover',
     'background-color: var(--color-fill-3) !important',
     '侧栏「新会话」hover（原文 #e4e6ea!important）'),
    ('.ws-dropdown-hover:hover',
     'background-color: var(--color-fill-3) !important',
     '工作目录下拉项 hover（原文 #e4e6ea!important）'),
    ('.ws-item-hover:hover',
     'background-color: var(--color-fill-2) !important',
     '工作目录条目 hover（原文 #f7f7f7!important）'),
    ('.model-dropdown-menu-item:hover',
     'background-color: var(--color-fill-2) !important',
     '模型菜单项 hover（原文 #f3f4f5!important）'),
    ('.perm-menu-item:hover',
     'background-color: var(--color-fill-2) !important',
     '权限菜单项 hover（原文 #f3f4f5!important）'),
    ('.session-action-item:hover',
     'background-color: var(--color-fill-2) !important',
     '会话操作项 hover（原文 #f3f4f5!important）'),
    ('.hover\\:\\!bg-\\[var\\(--color-fill-2\\)\\]:hover',
     'background-color: var(--color-fill-3) !important',
     'Tailwind hover:!bg-[var(--color-fill-2)]（自带 !important）'),
    ('[class~="bg-[var(--color-fill-2)]"]',
     'background-color: var(--color-fill-3)',
     'Tailwind bg-[var(--color-fill-2)]（激活态，非 hover）'),
    ('.skills-popup-bg',
     'background: rgba(var(--gray-1), 0.9) !important;'
     ' border-color: var(--color-border-1) !important;'
     ' box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.45) !important',
     '技能浮窗（原文底 rgba(255,255,255,.88) + border #E5E5E5 + inset 白色高光）'),
    ('.skills-popup-row-tag',
     'background: var(--color-fill-2)',
     '技能浮窗标签底（原文 #FFFFFF）'),
]

PRE = "html[giencoder-theme='dark']"

# ★ 第 74 轮「新会话」复刻（r74-nc-css）的选择器 —— 逐字抄自该块，不可简化。
NC74 = ('button.giencoder-btn.giencoder-btn-secondary'
        '[class*="rounded-[8px]"][class*="mb-2"]')


def build_css():
    out = ['<style id="%s">' % DARK_ID]
    out.append("""  /* ★ r109 第四拍 ③-c：**全站 10 页的暗色适配层**（详情见本脚本文件头）。
     一句话：机制层只把 `giencoder-theme="dark"` 挂到 `<html>` 上；真正让页面变暗，
     得在这里把「不吃 token 的硬值」逐个换成 DS 暗色 token。
     ★ 作用域 `html[giencoder-theme='dark']`（= 机制层挂在 `<html>` 上的那个属性）。
       第三拍曾带 `:not([data-r93-page])` 把 conversation.html 排除（那一拍只做 5 页）；
       本拍**去掉** —— 全 10 页纳入。各页自带的页面级暗色档（见每页自己的
       `[giencoder-theme='dark']` 规则）也从这一刻起真正生效。
     ★ 浅色档一条都不生效 ⇒ 浅色零风险。
     ⚠ 本块注入在 `</head>` 前，而页面自定义的几块样式、以及第 92 / 101 两代顶栏装饰块
       都在 **body 内、排在本块之后** ⇒ 凡与它们竞争的一律靠**特异性**
       （前缀 `html[..]` 给到 0-1-1 起）或 `!important`。
     ⚠⚠ 写本块注释时**不得出现任何「注入块 id」的字面**（就是那些 `rNNN-xxx-css` 形式的名字）——
       apply109 的净底自检是「剥完块后 net 里不得再出现该 id」，注释里的字面会被它
       当成**残留标记** ⇒ 整条 apply 链当场报错退出（本拍真踩过，见 acceptance 二十九节）。 */""")

    # ---- ① shadcn HSL token → DS 暗色 token ----
    out.append('')
    out.append('  /* ── ① shadcn HSL token 层 → DS 暗色 token ────────────────────────────────')
    out.append('     `body{background-color:hsl(var(--background));color:hsl(var(--foreground))}` 排在 DS 的')
    out.append('     `body{color:var(--color-text-1);background:var(--color-bg-1)}` 之后、同特异性 ⇒ 前者胜出；')
    out.append('     而这套 token 不在 DS 暗色档里翻转 ⇒ 暗色下 body 仍是浅底深字，满屏文字从 body 继承。')
    out.append('     ⚠ 消费方是 `hsl(var(--x))` ⇒ 这里必须写 **HSL 三元组**（每个值 = 右侧 DS token 换算而来）。 */')
    out.append('%s {' % PRE)
    for tok, ds, note in BRIDGE:
        out.append('    --%s: %s;   /* = --color-%s（%s） */'
                   % (tok, _hsl(DS_DARK[ds]), ds, note))
    out.append('  }')

    # ---- ② 硬值覆盖 ----
    out.append('')
    out.append('  /* ── ② React 写死的内联 / Tailwind 字面色 → DS 暗色面'
               '（内联只能靠 `!important` 压）──────────── */')
    for key, decl, note in RULES:
        sels = [s.replace('__NC74_SEL__', NC74) for s in SEL_TOKENS.get(key, [key])]
        head = ',\n  '.join('%s %s' % (PRE, s) for s in sels)
        out.append('  /* %s */' % note)
        out.append('  %s { %s; }' % (head, decl))

    # ---- ③ 局部变量重声明 ----
    out.append('')
    out.append('  /* ── ③ 页面自定义变量的字面色 → DS 阶梯**镜像**（同一步阶，自动取到暗色端）──── */')
    for sel, vars_ in LOCAL_VARS:
        out.append('  /* %s */' % sel)
        out.append('  %s %s {' % (PRE, sel))
        for name, val, note in vars_:
            out.append('    %-16s %s;   /* %s */' % (name + ':', val, note))
        out.append('  }')

    # ---- ④ 亮色 hover / 激活态 ----
    out.append('')
    out.append('  /* ── ④ 亮色 hover / 激活态（静态看不见，暗色下会闪白）──── */')
    for sel, decl, note in HOVERS:
        out.append('  /* %s */' % note)
        out.append('  %s %s { %s; }' % (PRE, sel, decl))

    # ---- ⑤ 顶栏装饰位图 ----
    out.append('')
    out.append('  /* ── ⑤ 顶栏装饰位图 → DS token 点阵 ─────────────────────────────────────')
    out.append('     `r92-hdr-css` 给的 `assets/images/bg-img-1.png`（1580×134、平底 #F6F8FA、')
    out.append('     右侧 8px 点距点阵）是**浅色位图**，暗色下会整条盖亮顶栏；')
    out.append('     第 101 轮那一块再把它的 `background-size` 改成 70%。')
    out.append('     ⚠⚠ 这两块注入在 `</body>` 前、排在本块之后、特异性相同 ⇒ **必须 `!important`**。')
    out.append('     改法：不用位图，按素材同样的几何用 DS token 现画 ——')
    out.append('       平底 `--color-bg-1`；点阵取 `rgb(var(--gray-2))`（比底色亮一档，同素材的「微差」手感）；')
    out.append('       8px 点距、2px 圆点；只露右侧 —— 素材点阵占图宽 32.5%、图又只占视口 70%')
    out.append('       ⇒ 点阵区起点 ≈ 视口 77%，左侧 77% 用同色实心层盖住（第 1 层在最上面）。 */')
    out.append('  %s header[class*="h-12"] {' % PRE)
    out.append('    background-image:')
    out.append('      linear-gradient(to right,')
    out.append('        var(--color-bg-1) 0, var(--color-bg-1) 77%, rgba(0, 0, 0, 0) 77%),')
    out.append('      radial-gradient(circle, rgb(var(--gray-2)) 2px, rgba(0, 0, 0, 0) 2px) !important;')
    out.append('    background-size: 100% 100%, 8px 8px !important;')
    out.append('    background-repeat: no-repeat, repeat !important;')
    out.append('    background-position: left top, center center !important;')
    out.append('    background-color: var(--color-bg-1) !important;')
    out.append('  }')

    # ---- ⑥ 研发工作台冷灰外壳变量 ----
    out.append('')
    out.append('  /* ── ⑥ 页面级「冷灰外壳」变量 → 暗色档定向覆盖 ─────────────────────────')
    out.append('     这些变量写在**各页自己的 `:root`** 里，是设计侧给研发工作台的一档**偏冷**浅灰')
    out.append('     （`#E5EDF5` 页面底 / `#DAE3ED` 顶栏与描边）。DS 灰阶是**纯中性**的，最近一级也差')
    out.append('     Δ11~16 且**掉色相** ⇒ 浅色档必须原样保留（「绝对不得影响已正确的浅色模式」）。')
    out.append('     这里只在暗色档把它们的**取值**换成 DS token：特异性 (0,1,1) > 页面 `:root` (0,1,0)，稳赢；')
    out.append('     且变量沿继承树生效 ⇒ 挂 `html` 一处即可覆盖整棵子树。 */')
    out.append('  %s {' % PRE)
    for name, val, note in PAGE_VARS:
        out.append('    %-18s %s;   /* %s */' % (name + ':', val, note))
    out.append('  }')

    out.append('</style>')
    return '\n'.join(out) + '\n'


DARK_CSS = build_css()

RE_ANCHOR = re.compile(r'<script id="r109-theme-js">.*?</script>\n', re.S)
RE_DARK = re.compile(r'<style id="%s">.*?</style>\n?' % DARK_ID, re.S)

# ★★ 适配护栏标记：挂在 `<html>` 上的静态属性 `data-gi-dark="1"`。
#   机制层在 `<head>` 里**同步执行**，此刻它后面的 `<style id="r109-dark-css">` 还没解析
#   ⇒ 不能用「查 DOM 里的样式块」来判断，只能用**执行时已存在**的信号。
#   `<html>` 属性正好满足：它在 HTML 第一个字节就解析出来了，且**不在任何注入块内部**
#   ⇒ 不会被 `apply-theme.py` 的邻接剥离正则牵连（用 `<meta>` 夹在两块之间就会）。
#   没有这个属性 ⇒ 机制层 `DARK_OK=false` ⇒ 一律按浅色渲染（杜绝半暗半亮）。
FLAG = 'data-gi-dark'
RE_HTML = re.compile(r'<html(\s[^>]*)?>')
RE_FLAG = re.compile(r'\s*data-gi-dark="[^"]*"')
# 机制层里护栏那段代码的指纹（缺它说明 apply-theme.py 是旧版 ⇒ 不能注入，否则会半暗半亮）
RE_GUARD = re.compile(r"root\.getAttribute\('data-gi-dark'\)")


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def set_flag(t, on):
    """在 `<html>` 上挂/摘 `data-gi-dark="1"`（幂等：先摘后挂）。"""
    def rep(m):
        attrs = RE_FLAG.sub('', m.group(1) or '').rstrip()
        if on:
            attrs = (attrs + ' data-gi-dark="1"') if attrs else ' data-gi-dark="1"'
        return '<html' + attrs + '>'
    return RE_HTML.sub(rep, t, count=1)


def patch(t):
    t = RE_DARK.sub('', t)              # 先剥旧块 ⇒ 幂等
    m = RE_ANCHOR.search(t)
    if not m:
        return t, False
    t = t[:m.end()] + DARK_CSS + t[m.end():]
    return set_flag(t, True), True


def strip_all(t):
    return set_flag(RE_DARK.sub('', t), False)


def sweep(name):
    """★★ 越界清扫：把**不在 SCOPE 的页**上残留的本块摘掉。

    为什么必须做：`apply109.py` 从 `pages/base.html` 的**净底**重建 `conversation.html`，
    而本块**不在**它的剥离名单里 ⇒ conversation 会把 base 上的本块一起**继承**过去。
    继承一份「作用域里带 `:not([data-r93-page])`」的死规则虽然不影响观感，
    却会让「**适配层只存在于被适配的 5 页**」这条可核契约失效 ——
    而这条契约正是本拍「不破坏稳定性」的书面保证（也是本脚本 --revert 的依据）。
    ⇒ 每次跑本脚本都顺手扫一遍：范围外的页若有残留，一律摘净（含摘护栏标记）。
    """
    p = os.path.join(PAGES, name + '.html')
    if not os.path.exists(p):
        return None
    t, nl = rd(p)
    if not RE_DARK.search(t) and not RE_FLAG.search(t):
        return 0
    t2 = strip_all(t)
    if t2 == t:
        return 0
    io.open(p, 'wb').write(t2.replace('\n', nl).encode('utf-8'))
    return len(t) - len(t2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='只报会改什么，不落盘')
    ap.add_argument('--revert', action='store_true', help='把本块整段剥掉')
    a = ap.parse_args()

    _check_ds()

    print('=== r109 ③-c 暗色适配层：%s（范围 %s） ==='
          % ('回滚' if a.revert else ('检查' if a.check else '注入'), ' / '.join(SCOPE)))
    n_ok = n_skip = n_bad = 0
    for name in SCOPE:
        p = os.path.join(PAGES, name + '.html')
        if not os.path.exists(p):
            print('   !! %-20s 不存在' % name)
            n_bad += 1
            continue
        t, nl = rd(p)
        before = len(t)
        has = bool(RE_DARK.search(t))
        if a.revert:
            if not has and not RE_FLAG.search(t):
                n_skip += 1
                continue
            t2 = strip_all(t)
        else:
            if not RE_ANCHOR.search(t):
                print('   !! %-20s 找不到锚点 `<script id="r109-theme-js">`'
                      '（先跑 apply-theme.py）' % name)
                n_bad += 1
                continue
            if not RE_GUARD.search(t):
                print('   !! %-20s 机制层里没有暗色护栏（`DARK_OK`）—— 先重跑 apply-theme.py，'
                      '否则未适配页会半暗半亮' % name)
                n_bad += 1
                continue
            t2, ok = patch(t)
            if not ok:
                n_bad += 1
                continue
            if t2 == t:
                n_skip += 1
                print('   =   %-20s 已是目标态' % name)
                continue
        if not a.check:
            io.open(p, 'wb').write(t2.replace('\n', nl).encode('utf-8'))
        n_ok += 1
        print('   %s %-20s %7d → %7d（%+d 字符）%s'
              % ('*' if a.check else '√', name, before, len(t2), len(t2) - before,
                 '（已有旧块，先剥后插）' if has and not a.revert else ''))
    print()

    # ---- ★★ 越界清扫（范围外的页不许留本块）----
    if not a.check:
        swept = []
        for fn in sorted(os.listdir(PAGES)):
            if not fn.endswith('.html'):
                continue
            name = fn[:-5]
            if name in SCOPE:
                continue
            d = sweep(name)
            if d:
                swept.append('%s（−%d 字符）' % (name, d))
        if swept:
            print('   ★ 越界清扫（非适配页残留的本块）：%s' % ' / '.join(swept))
            print()

    print('   变更 %d 页 / 已是目标态 %d 页 / 失败 %d 页' % (n_ok, n_skip, n_bad))
    if n_bad:
        sys.exit('!! 有页面处理失败')


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""r109 第三拍 ③-c：**基础工作台 5 页的暗色适配层**。

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
       `.bg-white`（主面板 / 卡片）、`[class~="border-[#ECEEF2]"]`（面板描边）
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

★★ 作用域 = `html[giencoder-theme='dark']:not([data-r93-page])`：
  · `html[giencoder-theme='dark']` 由机制层挂（用户选档 / 跟随系统）；
  · `:not([data-r93-page])` 是**护栏**：`conversation.html` 由 `apply109.py` 从 `base.html`
    的净底重建 ⇒ 会**继承**本块（`r109-dark-css` 不在 apply109 的剥离名单里）。
    本拍决策是「机制层 + **基础工作台 5 页**」（研发工作台下一轮）⇒ 用它把 conversation 排除，
    免得半暗半亮。⚠ 实测 10 页里**只有** conversation.html 的 `<html>` 挂 `data-r93-page`。
  · 一条规则都不在浅色档生效 ⇒ **浅色零风险**（「不破坏稳定性」的硬保证）。

★ 幂等：先按 `RE_DARK` 剥旧块、再插 ⇒ 重跑逐字节不变。
★ 落点锚：紧跟 `<script id="r109-theme-js">…</script>` 之后（机制层的尾巴，唯一且稳定）。
  ⚠ 先跑 `apply-theme.py`，再跑本脚本。

用法： python mg-work/r109/ev/theme/apply-dark.py            # 5 页注入（幂等）
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

# 本拍只做基础工作台 5 页（邵先生 2026-10-02 决策）。
SCOPE = ('base', 'avatar', 'automation', 'skills', 'settings')

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
]

SEL_TOKENS = {
    '__SHELL__': ['[class~="bg-[#F4F5F6]"]', '.flex.h-dvh', '.flex.min-h-0.flex-1'],
    '__PANEL__': ['.bg-white', '.bg-white\\/50'],
    '__PANEL_HOVER__': ['.hover\\:bg-white:hover'],
    '__PANEL_BORDER__': ['[class~="border-[#ECEEF2]"]'],
    '__SEGTRACK__': ['[class~="bg-[#E4E6EA]"]'],
    '__SEGTRACK_BORDER__': ['[class~="border-[#E4E6EA]"]'],
    '__NEWCHAT__': ['.new-chat-btn'],
    '__NEWCHAT_HOVER__': ['.new-chat-btn:hover'],
    '__R85IC__': ['.r85-ic'],
    '__PLACEHOLDER__': ['.ws-search-input::placeholder'],
    # ★ 第 74 轮「新会话」复刻：**原样复用它的长选择器**（特异性 (0,4,1) 及以上才能压住）
    '__NC74__': ['__NC74_SEL__'],
    '__NC74_HOVER__': ['__NC74_SEL__:hover'],
    '__NC74_BEFORE__': ['__NC74_SEL__::before'],
    '__NC74_AFTER__': ['__NC74_SEL__::after'],
}

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
    ('.hover\\:\\!bg-\\[\\#E9ECEE\\]:hover',
     'background-color: var(--color-fill-3) !important',
     'Tailwind hover:!bg-[#E9ECEE]（自带 !important）'),
    ('[class~="bg-[#E9ECEE]"]',
     'background-color: var(--color-fill-3)',
     'Tailwind bg-[#E9ECEE]（激活态，非 hover）'),
    ('.skills-popup-bg',
     'border-color: var(--color-border-1) !important;'
     ' box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.45) !important',
     '技能浮窗（原文 border #E5E5E5 + inset 白色高光）'),
    ('.skills-popup-row-tag',
     'background: var(--color-fill-2)',
     '技能浮窗标签底（原文 #FFFFFF）'),
]

PRE = "html[giencoder-theme='dark']:not([data-r93-page])"

# ★ 第 74 轮「新会话」复刻（r74-nc-css）的选择器 —— 逐字抄自该块，不可简化。
NC74 = ('button.giencoder-btn.giencoder-btn-secondary'
        '[class*="rounded-[8px]"][class*="mb-2"]')


def build_css():
    out = ['<style id="%s">' % DARK_ID]
    out.append("""  /* ★ r109 第三拍 ③-c：**基础工作台 5 页的暗色适配层**（详情见本脚本文件头）。
     一句话：机制层只把 `giencoder-theme="dark"` 挂到 `<html>` 上；真正让页面变暗，
     得在这里把「不吃 token 的硬值」逐个换成 DS 暗色 token。
     ★ 作用域 `html[giencoder-theme='dark']:not([data-r93-page])`：
       · 前者 = 机制层挂的属性；后者 = 把 conversation.html（apply109 从 base 净底重建时会
         继承本块）排除掉 —— 本拍只做基础工作台 5 页，研发工作台下一轮。
     ★ 浅色档一条都不生效 ⇒ 浅色零风险。
     ⚠ 本块注入在 `</head>` 前，而页面自定义的几块样式、以及第 92 / 101 两代顶栏装饰块
       都在 **body 内、排在本块之后** ⇒ 凡与它们竞争的一律靠**特异性**
       （前缀 `html[..]:not(..)` 给到 0-2-1 起）或 `!important`。
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

# -*- coding: utf-8 -*-
u"""r109 第四拍 ②：**把「我们自己的页面 CSS」里的硬编码绝对色值换成 DS 色彩系统变量。**

邵先生 2026-10-02 铁律：
  「除了我特别声明的之外，全局所有界面的色值一律要使用 giencoder 设计系统里已有的
    色彩系统变量，不得有写死的绝对色值（前提是绝对不得影响目前已经正确的浅色模式）。」

★ 为什么是「叠加一层」而不是回改各代补丁：
  这些字面值散落在 r73 ~ r109 各代注入块（还有几大块**匿名的页面级 `<style>`**，
  如 kanban 的 `--kb-*`、task-detail 的 `--td-*`）。回改那些已交付代的
  `applyNNN.py` 会牵动整条生成链（part → splice → make → apply），风险与收益完全不成比例。
  与 `apply-theme.py` / `apply-dark.py` 同一体位：**新加一层、排在链尾、幂等、可 `--revert`**。
  ⇒ 新链序： `make109.py` → `apply109.py` → `apply-theme.py` → `apply-dark.py` → **本脚本**。

★★ 只改**声明块** `{...}` 之内（这是本脚本唯一敢做文本替换的前提）：
  · CSS 里 `[style*="background: rgb(229, 229, 229)"]` 这种**选择器**里的色值是
    「匹配用字面」，改了选择器就失配了 —— 它在 `{` 之外，天然不在替换区；
  · `@media (…)` / `@supports (…)` 的前导同理；
  · `<script>` 块**整块跳过**（JS 里的色值可能是字符串拼接、模板、状态机，改动语义不可控）。

★ 三条替换策略（判据全部可核）：
  ① **EXACT**：该字面值**逐位等于**某个 DS 原语阶梯的浅色值 ⇒ 直接换成
     `rgb(var(--<族>-<级>))`。浅色档**逐位不变**（零风险），暗色档自动取镜像亮度。
  ② **NEAR**：不等，但同族最近一级的**最大通道差 ≤ TOL(12)** ⇒ 换成那一级
     （邵先生 2026-10-02 决策：「就近映射到 DS 阶梯」）。浅色档有微差，逐条列在 --check 里。
  ③ 其余**一律不动**：Δ > TOL 的、半透明的（阴影 / 遮罩 / 渐变透明端）、品牌 logo、
     `mask-image` 里的色（那是**遮罩 alpha 通道，根本不是颜色**）。
     ——这些由 `apply-dark.py` 用暗色档**定向覆盖**（浅色零变化的另一边保证）。

★ 豁免（写死不替换）：
  · 属性名含 `mask` ⇒ 跳过（`mask-image: linear-gradient(#000 …)` 里的 `#000` 是 alpha）；
  · 属性 ∈ {box-shadow, text-shadow, filter, backdrop-filter} ⇒ 跳过（阴影是主题中性的黑/白 scrim）；
  · 属性名含 `logo` ⇒ 跳过（邵先生：「只豁免品牌 logo」）；
  · 值 ∈ EXEMPT_VALUES（纯黑、Google 四色、产品 logo 色）⇒ 跳过。

★ 作用域：只处理这 10 页里**我们自己的** `<style>` 块 —— 除外的两块各有硬理由：
  · **DS 内联包**（每页 1 块、~93.7KB，指纹 `:root{--giencoderblue-1:245, 248, 255;`）
    —— 那是**设计系统本体**（`--color-*` / `--gray-N` 的**定义处**），改它 = 改设计系统；
  · `r109-theme-css` / `r109-dark-css` —— 本拍的适配层，里面本来就该出现暗色值。

★ 幂等：替换后字面值即消失 ⇒ 重跑「应用 0 处」。
用法：
  python mg-work/r109/ev/theme/apply-tokens.py            # 落盘
  python mg-work/r109/ev/theme/apply-tokens.py --check    # 只报会改什么（含每处 Δ）
"""
import argparse
import collections
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PAGES = os.path.join(REPO, 'pages')
DS = os.path.join(REPO, 'giencoder-design-system', 'colors_and_type.css')

ALL = ['base', 'avatar', 'automation', 'skills', 'settings',
       'conversation', 'dev', 'kanban', 'req-kanban', 'task-detail']

DS_FINGERPRINT = u':root{--giencoderblue-1:245, 248, 255;'
SKIP_BID = {u'r109-theme-css', u'r109-dark-css', u'r109-tw-css'}

# 同族最近一级允许的最大通道差（② NEAR 档）
TOL = 12

# 整值豁免
EXEMPT_VALUES = {
    '#000000', '#000',
    '#4285f4', '#ea4335', '#fbbc05', '#34a853',      # Google logo
    '#0f5197', '#0c88da', '#2cc3d5', '#49d66a',      # 产品 logo
    '#f9a01e', '#f7c015', '#2196f3', '#00cb60',
}

# ★★「研发工作台冷灰外壳」`#E5EDF5` —— **刻意排除，永久保留字面**。
#   本集合是一个「显式不改」的出口。
#   ⚠ 历史教训一（别删）：这个值的通道**极差 16** ⇒ `neutral()` 判不出来 ⇒ 启发式会把它挑到
#     `--green-1`（冷灰拉成浅绿）。所以它必须走**显式表**，不能交给启发式。
#   ⚠ 历史教训二（**本拍真踩，推翻上一版裁决**）：
#     上一版按邵先生「按同族就近全收敛」把它挂到了 `rgb(var(--gray-2))`（浅 #F2F2F2，Δ13）。
#     本拍用**像素级 diff** 一量：`task-detail-light.png` 单页 **91581 像素**（占 7.4%）从
#     `#E5EDF5` 变成 `#F2F2F2` —— 那就是**整张页面画布**。而 `apply-dark.py` ⑥ 段早就为它写了
#     定向覆盖（`html[giencoder-theme='dark'] { --td-surround: var(--color-bg-1) }`），
#     并在注释里写明「**浅色档必须原样保留**（绝对不得影响已正确的浅色模式）」。
#     ⇒ 两条铁律在这里**冲突**：①「不得有写死的绝对色值」vs ②「**前提是**绝对不得影响
#       目前已经正确的浅色模式」。②是①的**前提**，且 `#E5EDF5`/`#DAE3ED` 这类**冷灰**在
#       DS 的**纯中性**灰阶里根本没有等值档（最近的 gray-2 差 Δ13 且**掉色相**）。
#     ⇒ 处置：**排除**，仍由暗色档定向覆盖。这是本拍**唯一**保留的字面值，已记入
#       `acceptance.md` §30.6 待裁决（候选：保持现状 / gray-2 Δ13 / blue-1 Δ10 保色相）。
EXCLUDE_VALUES = {'#e5edf5'}

# ★★ 显式覆盖表：**逐条人工核对过「角色 + Δ」**，优先于一切启发式。
#
#   为什么需要它：启发式按「最近通道」挑族，对**带轻微色相的浅灰**会翻车（见上 `#E5EDF5`）；
#   而页面级自定义属性（`--td-bubble` / `--kb-appbar` …）的消费方从声明处看不出来，
#   泛化阈值 = 赌。⇒ 这些「一看就知道该去哪儿」的值，写死。
#
#   Δ 口径 = **最大通道差**（浅色档与原字面值），全部 ≤ 12（≤ 1 级阶梯），符合邵先生
#   2026-10-02 的裁决「就近映射到 DS 阶梯（允许 ≤1 级色差）」。
#   ★ 全部落在**会随暗色档翻转**的 token 上（原语阶梯 / `--color-fill-*` / `--color-border-*`
#     / `--color-text-*`）⇒ 一处改动**同时**解决铁律 2（token 化）与第 3 条（暗色适配）。
OVERRIDE = {
    # 值          目标                          角色                        Δ
    '#e5edfe': (u'rgb(var(--blue-1))',           u'用户聊天气泡底（--td-bubble / --r93-bubble）', 10),
    '#d3e2ff': (u'rgb(var(--giencoderblue-2))',  u'激活 / 悬停描边（--td-tree-active-bd 等）',     7),
    '#e7ebf1': (u'rgb(var(--gray-2))',           u'发丝线 / 面包屑线（--td-crumb-line / --av-hs-line）', 11),
    '#ebebed': (u'rgb(var(--gray-2))',           u'会话分隔线（--r93-line）',                      7),
    '#ebeced': (u'rgb(var(--gray-2))',           u'看板表格线 / 分割线（--kb-tbl-line 等）',        7),
    '#333333': (u'rgb(var(--gray-9))',           u'主图标色（--r93-ioc）',                        10),
    '#fdddc3': (u'rgb(var(--orange-2))',         u'标签描边（--r93-tag-bd）',                       9),
    '#e7f0ff': (u'rgb(var(--blue-1))',           u'蓝标签底（--kb-tag-blue-bg）',                   7),
    '#ff6157': (u'rgb(var(--red-5))',            u'状态·延期（--kb-st-delay）',                     8),
    '#3686ff': (u'rgb(var(--blue-6))',           u'状态·协同（--kb-st-coop）',                     11),
    '#3491fa': (u'rgb(var(--blue-6))',           u'研发工作台 logo 底（--r81-logo-bg，逐位等值）',  0),
    # `#DAE3ED` 是**双角色**（面 / 线）⇒ 见 map_value 里的按属性名分流
    '#dae3ed': (None,                            u'顶栏 / 侧栏 hover 底 · 分栏描边（双角色）',      11),

    # ══ 第三批（邵先生 2026-10-02 裁决「按同族就近**全收敛**」）══════════════════
    #    ★ 手法与批次二**不同**：这里**由我逐条指定族**，级别取「该族内最大通道差最小」的一级。
    #      为什么不交给启发式挑族：启发式按「最近通道」挑，`#E5EDF5` 就是被它挑成 `--green-1` 的。
    #      ⇒ 族是**语义判断**（冷灰 / 蓝 / 靛 / 紫 / 品红 / 橙 / 金 / 红 / 青 / 绿），级别才是算术。
    #    ★ Δ 会明显变大（最大 54）——这是邵先生明确接受的代价（原话「按同族就近全收敛」）。
    #    ★ 品牌 logo（Google 四色 + 产品 logo 八色）**仍豁免**（邵先生「只豁免品牌 logo」）。
    # ── 冷灰壳 / 中性 ──
    # `#E5EDF5`（页面底）**不在此表**：它在 `EXCLUDE_VALUES`（见上，浅色必须原样保留）。
    '#57626d': (u'rgb(var(--gray-7))',           u'次级文字 --td-ink-2',                           20),
    '#5e5e5e': (u'rgb(var(--gray-7))',           u'说明文字 --r81-desc-fg',                        13),
    '#96abc2': (u'rgb(var(--gray-5))',           u'胶囊底 --r81-pill-bg（冷板岩灰）',               25),
    '#575757': (u'rgb(var(--gray-8))',           u'优先级·低 --kb-prio-low',                        9),
    # ── 蓝 ──
    '#167ab8': (u'rgb(var(--blue-7))',           u'图标 --td-ico-md',                              23),
    '#4196d6': (u'rgb(var(--blue-6))',           u'图标 --td-ico-md-fold',                         36),
    '#327fcb': (u'rgb(var(--blue-7))',           u'图标 --td-ico-web',                             19),
    '#0451a5': (u'rgb(var(--blue-8))',           u'代码 keyword --td-code-key',                    13),
    # ── 靛 giencoderblue ──
    '#bbd1fb': (u'rgb(var(--giencoderblue-3))',  u'分页激活描边 --kb-pg-active-bd',                  8),
    '#4f68ce': (u'rgb(var(--giencoderblue-7))',  u'JS/图标·靛',                                    27),
    '#a0baf7': (u'rgb(var(--giencoderblue-4))',  u'JS/图标·靛（浅）',                              18),
    '#3d6ebf': (u'rgb(var(--giencoderblue-8))',  u'蓝标签字 --kb-tag-blue-tx',                     16),
    '#d0d7ea': (u'rgb(var(--giencoderblue-2))',  u'气泡阴影边 --r93-bubble-sh',                    20),
    '#5592eb': (u'rgb(var(--giencoderblue-5))',  u'状态·进行中 .rq-status--doing',                 17),
    '#3770f7': (u'rgb(var(--giencoderblue-6))',  u'JS 激活底（逐位等值）',                           0),
    # ── 紫 / 品红 ──
    '#7766fd': (u'rgb(var(--purple-5))',         u'--td-ico-skill · 代码关键字',                   35),
    '#7a4b9e': (u'rgb(var(--purple-7))',         u'紫标签字 --kb-tag-purple-tx',                   46),
    '#a74b6f': (u'rgb(var(--magenta-7))',        u'品红标签字 --kb-tag-magenta-tx',                45),
    # ── 橙 / 金 ──
    '#f3881e': (u'rgb(var(--orange-5))',         u'状态·已取消 .rq-type--entry 等',                18),
    '#f77234': (u'rgb(var(--orange-5))',         u'优先级·中 --kb-prio-mid / --r93-tag-ic',        40),
    '#f36c1d': (u'rgb(var(--orange-6))',         u'--kb-confirm',                                  29),
    '#ffecd9': (u'rgb(var(--orange-1))',         u'橙标签底（原被启发式误配 --red-1）',             15),
    '#e59800': (u'rgb(var(--gold-7))',           u'状态·评审 --kb-st-review',                      25),
    # ── 红 ──
    '#a31515': (u'rgb(var(--red-8))',            u'代码 string --td-code-str',                      9),
    '#f53f3f': (u'rgb(var(--red-6))',            u'JS 状态点（逐位等值 --color-danger-6）',           0),
    '#ffece8': (u'rgb(var(--red-1))',            u'JS 浅红底（逐位等值）',                           0),
    '#fdcdc5': (u'rgb(var(--red-2))',            u'JS 浅红底',                                       8),
    # ── 青 ──
    '#0fa79a': (u'rgb(var(--cyan-7))',           u'子需求标签字 .rq-type--sub',                    16),
    '#098658': (u'rgb(var(--cyan-9))',           u'代码 number --td-code-num',                     37),
    '#009e61': (u'rgb(var(--cyan-8))',           u'状态·已完成 .rq-status--done',                  42),
    '#3c8ba1': (u'rgb(var(--cyan-7))',           u'文件类型图标·青',                                47),

    # ══ 第四批：`<script>`（React 编译产物）里的颜色字面 ══════════════════════════
    #    ★★ 先做了**真机实测**才敢动：`fill="var(--color-danger)"` 在本机 Chromium
    #       **解析成功**（`getComputedStyle().fill` = `rgb(245, 63, 63)`）⇒ SVG 呈现属性里的
    #       `var()` 可用 ⇒ 把字面换成变量**是**安全的（`style:{\`fill\`:\`var(…)\`}` 同理）。
    #    ★ 只替换**引号包裹**的字面（`'#x'` / `"#x"` / `` `#x` ``）——
    #      尾风类名里的 `text-[#3770F7]`（方括号相邻、无引号）**天然不会被命中**，
    #      否则会把「类名 ↔ CSS 选择器」这层配对改断（真踩过同类坑）。
    #    ★ 品牌 logo 色（Google 四色 + 产品 logo 八色）在 `EXEMPT_VALUES` 里，**不动**。
    # ── JS 图标字形（灰）──
    '#6b6b6b': (u'rgb(var(--gray-7))',           u'JS 图标字形（逐位等值）',                          0),
    '#a9a9a9': (u'rgb(var(--gray-5))',           u'JS 图标字形（逐位等值）',                          0),
    '#868686': (u'rgb(var(--gray-6))',           u'JS 图标字形（逐位等值）',                          0),
    '#e5e5e5': (u'rgb(var(--gray-3))',           u'JS 弹层描边（逐位等值）',                          0),
    # ── JS 靛 / 紫 / 品红 ──
    '#6079e5': (u'rgb(var(--giencoderblue-5))',  u'文件类型图标·靛',                                25),
    '#7c82c7': (u'rgb(var(--giencoderblue-5))',  u'图标·靛（灰紫）',                                50),
    '#8865f3': (u'rgb(var(--purple-5))',         u'文件类型图标·紫',                                25),
    '#b6536e': (u'rgb(var(--magenta-7))',        u'文件类型图标·品红',                              53),
    # ── JS 橙 / 金 / 绿 ──
    '#ffa000': (u'rgb(var(--orange-6))',         u'文件夹图标（VS 风格橙）',                         35),
    '#de8f3e': (u'rgb(var(--orange-5))',         u'文件类型图标·橙',                                33),
    '#c49e29': (u'rgb(var(--gold-7))',           u'文件类型图标·金',                                22),
    '#699650': (u'rgb(var(--green-5))',          u'文件类型图标·绿',                                44),
    # ── JS 青（热力/等级）──
    '#14c9c9': (u'rgb(var(--cyan-6))',           u'JS 热力（逐位等值）',                              0),
    '#89e9e0': (u'rgb(var(--cyan-3))',           u'JS 热力（逐位等值）',                              0),
    '#09b396': (u'rgb(var(--cyan-7))',           u'JS 热力',                                        20),
    '#4cdbc3': (u'rgb(var(--cyan-4))',           u'JS 热力',                                        19),

    # ══ 第五批：**从 bundle 自带的设计规格注释里挖出来的权威映射** ═════════════════
    #    ★★ 这是本轮最硬的一手，值得单列：编译产物里有一批形如
    #        `{text:`DeepSeek-V4-Pro`, textColor:`#1E1E1E`, textToken:`文本/@color-text-1`,
    #          bg:`#F3F4F5`, bgToken:`填充/@colorFill-1`, iconPaths:[…]}`
    #      的**规格数据** —— 产品自己把「字面值 ↔ DS token 名」写在了一起。
    #      ⇒ 这三条**不是启发式、不是就近猜**，而是产品方的**自证映射**（比 Δ 判据更可信）。
    #    ★ 也就是说：规格锚点在这里同时是「要修的对象」（它带着硬编码）与「判据来源」
    #      （它的 `*Token` 字段告诉我们该换成哪个 token）。⇒ 一处数据解决两条铁律。
    #    ★ 规格数据本身**不替换**（`RE_JSSPEC` 哨兵拦住）—— 只有真正参与渲染的那份字面
    #      （`textColor` / `bg` / `iconPaths[].fill` 的**同一字面**）会被换掉，注释保留可比对。
    '#1e1e1e': (u'var(--color-text-1)',          u'规格·模型菜单项字色 textToken=文本/@color-text-1', 1),
    '#bebebe': (u'var(--color-text-4)',          u'规格·禁用项字色 textToken=文本/@color-text-4',   11),
    '#f3f4f5': (u'var(--color-fill-1)',          u'规格·选中行底 bgToken=填充/@colorFill-1',          4),

    # ══ 第六批：邵先生 2026-10-02 裁决（本拍「深压深」侦察后）═════════════════════
    #    判据来源不是 Δ，而是**真机取色 + 对比度算术**：`apply-dark.py` 里没有它们的钩子，
    #    暗色档直接掉到「比值 < 1.3」= 肉眼不可见。三条都落在**模型厂商单色标识**
    #    （`iconPaths[].fill`）与**中性图标/提示字**上，按裁决：
    #      · ① 单色厂商标识（GLM/Kimi）→ 收敛（邵先生原话「收敛为 --color-text-1」）；
    #      · ② `#F5E8FF`（品牌 logo 内部浅紫装饰）**不在这里** —— 裁决是「保留变量 + 暗色覆盖」，
    #        落在 `apply-dark.py` 的 `__LOGO_TINT__` 规则里（用紫色阶梯的**镜像步**取回浅紫）。
    #    ⚠ `#000000` 同时躺在 `EXEMPT_VALUES`（CSS 侧阴影/半透明黑要用它）⇒
    #      只在 JS 侧生效，见 `map_js_value` 里把 OVERRIDE 提前的那段注释。
    '#2d2d2d': (u'var(--color-text-1)',          u'裁决①·GLM 单色厂商标识（暗色比值 1.20 → 不可见）', 14),
    '#000000': (u'var(--color-text-1)',          u'裁决①·Kimi 单色厂商标识（暗色比值 0.79 → 不可见）', 31),
    '#8e8e8e': (u'rgb(var(--gray-6))',           u'中性图标/提示字（--color-text-3 的取色；浅色 Δ8 ≤ 1 级）', 8),
}

# ══ 第七批：邵先生 2026-10-02 裁决「同族就近全收敛」（第四拍收尾，含 §30.6 的 5 类）══
#    口径：§30.6 列的那批「Δ 大、没等值 token」的残余，**一律落 DS 同族阶梯**。
#    与第六批的分工：第六批按「**真机对比度算术**」咬（比值 < 1.3 = 不可见）；
#    本批按「**色相族 + 族内就近**」咬（颜色本身没错，只是没 token 化）。
#    ★★ 族的判定用**色相**（`colorsys.rgb_to_hsv`），**不用最大通道差**。实测反例：
#       `#009E61`（绿，hue 157）按最大通道差会落到 `cyan-8`（Δ42 < green-8 的 Δ50）
#       ⇒ **绿变青**。按色相判则稳落 green 族。同理 `#098658`（hue 158）落 `green-7`
#       —— ★ 这里**改了 §30.6 原表的 `cyan-9`**（Δ39 vs 37 几乎持平，但保住了色相）。
#    ⚠ Δ 一律**如实标注**（最大 62）；邵先生已确认接受浅色档像素变化。
#    ⚠ 不在本表的：品牌 logo（属性/键名含 `logo`，走 `SKIP_PROP_SUB`）·
#      `#E5EDF5` 冷灰外壳（`EXCLUDE_VALUES`，已由 `apply-dark.py` 的 `--kb-surround` /
#      `--td-surround` 做暗色定向覆盖）· `#000000` 系（`EXEMPT_VALUES`，阴影/遮罩 scrim）。
OVERRIDE.update({
    #      ---- ① 类型 / 状态标签前景 ----
    '#7766fd': (u'rgb(var(--purple-5))',          u'① 类型标签·紫（hue 247 → purple 族）',          35),
    '#f3881e': (u'rgb(var(--orange-5))',          u'① 状态标签·橙（hue 30 → orange 族）',           18),
    '#0fa79a': (u'rgb(var(--cyan-7))',            u'① 状态标签·青（hue 173 → cyan 族）',            16),
    '#5592eb': (u'rgb(var(--giencoderblue-5))',   u'① 状态标签·蓝（品牌蓝族；Δ17 优于 blue-5 Δ23）', 17),
    '#009e61': (u'rgb(var(--green-8))',           u'① 状态标签·绿（hue 157 → green 族）',           50),
    #      ---- ② 代码语法高亮 ----
    '#0451a5': (u'rgb(var(--blue-8))',            u'② 语法·关键字蓝',                              13),
    '#a31515': (u'rgb(var(--red-8))',             u'② 语法·字符串红',                               9),
    '#098658': (u'rgb(var(--green-7))',           u'② 语法·数字绿（★ 改 §30.6 的 cyan-9 → green-7：保色相）', 39),
    #      ---- ③ 头像身份色板（`--avatar-bg-1..7`）----
    '#e57470': (u'rgb(var(--red-5))',             u'③ 头像色板 1（hue 2 → red 族）',                18),
    '#e88b4d': (u'rgb(var(--orange-5))',          u'③ 头像色板 2（hue 24 → orange 族）',            31),
    '#dcab35': (u'rgb(var(--gold-6))',            u'③ 头像色板 3（hue 42 → gold 族；Δ27 优于 yellow-7 Δ38）', 27),
    '#a2c143': (u'rgb(var(--lime-5))',            u'③ 头像色板 4（hue 75 → lime 族）',              33),
    '#67b85d': (u'rgb(var(--green-5))',           u'③ 头像色板 5（hue 113 → green 族）',            13),
    '#47c2c4': (u'rgb(var(--cyan-5))',            u'③ 头像色板 6（hue 181 → cyan 族）',             18),
    '#4c93d4': (u'rgb(var(--giencoderblue-6))',   u'③ 头像色板 7（hue 209 → 品牌蓝族）',            35),
    #      ---- 同批扫出的「状态 / 标签 / 文件类型图标」同族残余 ----
    '#3d6ebf': (u'rgb(var(--blue-7))',            u'看板·标签蓝字（hue 217）',                      29),
    '#7a4b9e': (u'rgb(var(--purple-7))',          u'看板·标签紫字（hue 274）',                      46),
    '#a74b6f': (u'rgb(var(--magenta-7))',         u'看板·标签洋红字（hue 337 → magenta 族）',        45),
    '#f77234': (u'rgb(var(--orange-5))',          u'会话页·橙（hue 19）',                           40),
    '#2196f3': (u'rgb(var(--blue-6))',            u'文件类型图标·蓝（hue 207）',                     19),
    '#699650': (u'rgb(var(--lime-7))',            u'文件类型图标·橄榄（hue 99 → lime 族；Δ 偏大，如实标注）', 62),
    '#de8f3e': (u'rgb(var(--orange-5))',          u'文件类型图标·橙（hue 30）',                      33),
})


# ══ 第七批·B：**函数式**字面（`rgb()` / `rgba()`）─────────────────────────────────
#    为什么单开一张表：hex 那套（EXACT 逐位等值 / NEAR 就近）**只认 `#rrggbb`**，
#    侦察器的 `HEX` 正则也是 hex-only ⇒ `rgba(255,255,255,.88)` 这类**从来没被扫过**
#    （本拍实测：页面自带非 var 的 rgb()/rgba() 共 **264 处 / 61 值**）。
#    ★ 邵先生 2026-10-02 裁决：「**能对上 token 的就收敛**；整条阴影与遮罩保留字面」。
#      ⇒ 阴影/遮罩天然走 `SKIP_PROP_EXACT` / `SKIP_PROP_SUB`（`box-shadow` / `*mask*` / `*shadow*`），
#        本表只管「面 / 线 / 浅底」。
#    ⚠ `rgb(0,0,0,*)` 系**一律不进表**（深色 scrim / 半透明黑描边，α 主导，主题中性；
#      且 `rgba(0,0,0,.16)` 那种「压暗遮罩」若翻成浅色会反义）—— 保留字面，
#      暗色不可见的那几处由 `apply-dark.py` 的定向规则单独处理。
#    ⚠ 不透明的 `rgb(255,255,255)` **不进表**：它必须走 `pick_role` 按**属性角色**分流
#      （面 → `--color-bg-2`、字/边 → `--color-white`），与 hex 侧 `#ffffff` 同口径。
def _rgb_of(v):
    u"""`rgb(r,g,b[,a])` → (r,g,b)；认不出给 None。"""
    m = re.match(r'^rgb\((\d+),(\d+),(\d+)(?:,[\d.]+)?\)$', v)
    return tuple(int(m.group(i)) for i in (1, 2, 3)) if m else None


def norm_lit(raw):
    u"""字面 → **规范键**：hex 走 `#rrggbb`；函数式走 `rgb(r,g,b[,a])`（0~1 归一、去空格）。

    ★ 为什么要归一：同一个颜色在页面里有 `rgba(0,0,0,.1)` / `rgba(0, 0, 0, 0.10)` /
      `rgba(0,0,0,0.1)` 三种写法 ⇒ 不归一的话表要写三遍，且漏一种是**静默漏改**。
    """
    if raw.startswith('#'):
        try:
            return hex6(raw[1:])
        except Exception:
            return None
    m = re.match(r'^(rgba?|hsla?)\(\s*([^()]*?)\s*\)$', raw, re.I)
    if not m:
        return None
    fn, inner = m.group(1).lower(), m.group(2)
    if not fn.startswith('rgb'):            # hsl 字面页面里没有（且 `hsl(var(--x))` 会被上面挡掉）
        return None
    parts = [p.strip() for p in inner.split(',')]
    if len(parts) not in (3, 4):
        return None
    try:
        r, g, b = (int(round(float(x))) for x in parts[:3])
    except ValueError:
        return None
    if len(parts) == 3:
        return u'rgb(%d,%d,%d)' % (r, g, b)
    try:
        a = float(parts[3])
    except ValueError:
        return None
    if a >= 1:
        return u'rgb(%d,%d,%d)' % (r, g, b)
    return u'rgb(%d,%d,%d,%s)' % (r, g, b, u'%g' % a)


LIT_OVERRIDE = {}
#   ---- 玻璃白底 / 白描边（白 → 灰阶最浅档；Δ8 ≤ 1 级）----
for _a in ('0.88', '0.9', '0.95', '0.5', '0.55', '0.72', '0.74', '0.6',
           '0.2', '0.24', '0.28', '0.35', '0.45', '0'):
    LIT_OVERRIDE[u'rgb(255,255,255,%s)' % _a] = u'rgba(var(--gray-1), %s)' % _a
#   ---- 磨砂深底 / 深色胶囊（`.avatar-tooltip` 等；**这一条同时解掉暗色「白字压白底」**）----
LIT_OVERRIDE[u'rgb(29,33,41,0.8)'] = u'rgba(var(--gray-10), 0.8)'
LIT_OVERRIDE[u'rgb(35,35,36,0.6)'] = u'rgba(var(--gray-10), 0.6)'
LIT_OVERRIDE[u'rgb(35,35,36,0.72)'] = u'rgba(var(--gray-10), 0.72)'
LIT_OVERRIDE[u'rgb(35,35,36,0.74)'] = u'rgba(var(--gray-10), 0.74)'
LIT_OVERRIDE[u'rgb(31,31,31,0.6)'] = u'rgba(var(--gray-10), 0.6)'
#   ---- 品牌 / 状态 tint（Δ0~11）----
LIT_OVERRIDE[u'rgb(55,112,247)'] = u'rgb(var(--giencoderblue-6))'
LIT_OVERRIDE[u'rgb(55,112,247,0.12)'] = u'rgba(var(--giencoderblue-6), 0.12)'
LIT_OVERRIDE[u'rgb(55,112,247,0.16)'] = u'rgba(var(--giencoderblue-6), 0.16)'
LIT_OVERRIDE[u'rgb(55,112,247,0.4)'] = u'rgba(var(--giencoderblue-6), 0.4)'
LIT_OVERRIDE[u'rgb(54,134,255,0.12)'] = u'rgba(var(--blue-6), 0.12)'
LIT_OVERRIDE[u'rgb(255,97,87,0.12)'] = u'rgba(var(--red-5), 0.12)'
LIT_OVERRIDE[u'rgb(245,63,63,0.12)'] = u'rgba(var(--red-6), 0.12)'
LIT_OVERRIDE[u'rgb(247,101,96,0.12)'] = u'rgba(var(--red-5), 0.12)'
LIT_OVERRIDE[u'rgb(255,228,186,0.26)'] = u'rgba(var(--orange-2), 0.26)'
LIT_OVERRIDE[u'rgb(243,136,30,0.14)'] = u'rgba(var(--orange-5), 0.14)'
LIT_OVERRIDE[u'rgb(247,114,52,0.12)'] = u'rgba(var(--orange-5), 0.12)'
LIT_OVERRIDE[u'rgb(247,114,52,0.14)'] = u'rgba(var(--orange-5), 0.14)'
LIT_OVERRIDE[u'rgb(247,114,52,0.4)'] = u'rgba(var(--orange-5), 0.4)'
LIT_OVERRIDE[u'rgb(229,152,0,0.14)'] = u'rgba(var(--yellow-7), 0.14)'
LIT_OVERRIDE[u'rgb(87,87,87,0.1)'] = u'rgba(var(--gray-8), 0.1)'
LIT_OVERRIDE[u'rgb(255,190,110,0.1)'] = u'rgba(var(--orange-4), 0.1)'
#   ---- 中性近等值（Δ0~11）----
LIT_OVERRIDE[u'rgb(201,201,201)'] = u'rgb(var(--gray-4))'
LIT_OVERRIDE[u'rgb(242,242,242)'] = u'rgb(var(--gray-2))'
LIT_OVERRIDE[u'rgb(247,247,247)'] = u'rgb(var(--gray-1))'
LIT_OVERRIDE[u'rgb(231,235,241)'] = u'rgb(var(--gray-2))'
LIT_OVERRIDE[u'rgb(236,242,255)'] = u'rgb(var(--giencoderblue-1))'   # #ECF2FF 蓝色 chip 底（与 apply-dark 的定向规则同族同档）
LIT_OVERRIDE[u'rgb(229,237,254)'] = u'rgb(var(--blue-1))'
LIT_OVERRIDE[u'rgb(211,226,255)'] = u'rgb(var(--giencoderblue-2))'

# 双角色值：按**属性名**分流（两档数值相同，但语义不同 ⇒ 交给不同 token 管）
DAE3ED_FILL = u'var(--color-fill-3)'      # 面：顶栏底 / hover 底
DAE3ED_LINE = u'var(--color-border-2)'    # 线：分栏 1px 描边
RE_LINEISH = re.compile(r'line|border|bd|edge|hairline|stroke|outline|divider')

# 属性（或其前缀）豁免
SKIP_PROP_EXACT = {'box-shadow', 'text-shadow', 'filter', 'backdrop-filter',
                   '-webkit-filter', '-webkit-backdrop-filter', 'mask', 'mask-image'}
SKIP_PROP_SUB = ('mask', 'logo', 'shadow')

# ★ 反向回滚表：本脚本**只做替换、不会还原** ⇒ 历史上被它换掉的字面无法自动回来。
#   2026-10-02：`#E5EDF5` 从「可换（gray-2）」改成「**永久排除**」（理由见 `EXCLUDE_VALUES`），
#   于是必须把已经落盘的 `--kb-surround / --td-surround: rgb(var(--gray-2))` 改回字面。
#   ★ 幂等：第二次跑 pattern 已不存在 ⇒ 0 处。加这一条让脚本**自我修复**（重跑即回目标态），
#     而不是靠手工 `git checkout` —— 手工改的文本在下一次「从干净树跑链」时会丢。
REVERT = (
    (u'--kb-surround: rgb(var(--gray-2));', u'--kb-surround: #E5EDF5;'),
    (u'--td-surround: rgb(var(--gray-2));', u'--td-surround: #E5EDF5;'),
)

HEX = re.compile(r'#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b')
# ★★ 第七批·B：**色值字面的总入口** = hex ∪ 函数式。函数式只认「括号里以数字开头」的形态，
#    ⇒ `rgb(var(--gray-1))` / `rgba(var(--x), .5)`（DS 消费形态）天然不命中，幂等无忧。
RE_ANYCOLOR = re.compile(
    r'#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b'
    r'|\brgba?\(\s*\d[^()]*\)')
RE_DECL = re.compile(r'([-a-zA-Z][-a-zA-Z0-9]*)\s*:\s*([^;{}]*)')


# ---------------------------------------------------------------- 读 / 写
def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def hex6(s):
    if len(s) in (3, 4):
        s = u''.join(c * 2 for c in s)
    r, g, b = (int(s[i:i + 2], 16) for i in (0, 2, 4))
    return u'#%02x%02x%02x' % (r, g, b)


# ---------------------------------------------------------------- DS 阶梯
def ramps():
    u"""→ {族: {级: (r,g,b)}}，取 DS 的**浅色档**原语。"""
    t = io.open(DS, encoding='utf-8').read().replace(u'\r\n', u'\n')
    i = t.find(u"giencoder-theme='dark'")
    light = t[:i]
    raw = dict(re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', light))
    out = collections.defaultdict(dict)
    for k, v in raw.items():
        v = v.strip()
        m = re.match(r'^--([a-z]+)-(\d+)$', k)
        if not m or not re.match(r'^\d+\s*,\s*\d+\s*,\s*\d+$', v):
            continue
        out[m.group(1)][int(m.group(2))] = tuple(int(x) for x in v.split(','))
    return out


def semantic_light():
    u"""→ {token: (r,g,b)}：语义 token 的**浅色**取值（含直接写字面的一批）。"""
    t = io.open(DS, encoding='utf-8').read().replace(u'\r\n', u'\n')
    i = t.find(u"giencoder-theme='dark'")
    light = t[:i]
    raw = dict(re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', light))
    prim = {}
    for k, v in raw.items():
        v = v.strip()
        if re.match(r'^\d+\s*,\s*\d+\s*,\s*\d+$', v):
            prim[k] = tuple(int(x) for x in v.split(','))
    out = {}
    for k, v in raw.items():
        v = v.strip()
        m = re.match(r'^rgb\(\s*var\((--[a-z0-9-]+)\)\s*\)$', v)
        if m and m.group(1) in prim:
            out[k] = prim[m.group(1)]
        elif re.match(r'^#[0-9a-fA-F]{6}$', v):
            out[k] = tuple(int(v[1:][i:i + 2], 16) for i in (0, 2, 4))
    return out


RAMP = ramps()
SEM = semantic_light()

# 值 → 原语 token 名（EXACT）
EXACT = {}
for fam, steps in RAMP.items():
    for lv, rgb in steps.items():
        EXACT.setdefault(u'#%02x%02x%02x' % rgb, []).append((fam, lv))

# 「白」与「黑」不走阶梯，按**角色**定（见 pick_role）
WHITE = {u'#ffffff'}


def near(v, fam=None):
    u"""→ (族, 级, maxΔ) 或 None。maxΔ ≤ TOL 才收。"""
    r, g, b = v
    best = None
    for f, steps in RAMP.items():
        if fam and f != fam:
            continue
        for lv, rgb in steps.items():
            d = max(abs(rgb[0] - r), abs(rgb[1] - g), abs(rgb[2] - b))
            if best is None or d < best[2]:
                best = (f, lv, d)
    if best is None or best[2] > TOL:
        return None
    return best


def pick_role(prop, v):
    u"""白 / 黑按**属性角色**给 token（阶梯里没有纯白纯黑）。

    ⚠ 这里的取舍是「**暗色下的语义**」：
      · 面（background*）⇒ `--color-bg-2`（浅色 #ffffff ≡ 原值；暗色 #232324 = 卡片面）
      · 字（color/fill/stroke）⇒ `--color-white`（**两个档都保持白** —— 压在有色底上的白字）
      · 边（border*）⇒ `--color-white`
    ⚠ 键名做**去连字符 + 小写**归一：CSS 侧是 `caret-color` / `text-decoration-color`，
      JS（React style 对象）侧是 `caretColor` / `textDecorationColor` / `backgroundColor`，
      归一后两边用**同一张判定表** ⇒ 少一处漂移。
    """
    if v in WHITE:
        p = prop.lower().replace('-', '')
        if p.startswith('background') or p == 'bg':
            return u'var(--color-bg-2)'
        if p.startswith('border') or p == 'outline':
            return u'var(--color-white)'
        if p in ('color', 'fill', 'stroke', 'caretcolor', 'textdecorationcolor'):
            return u'var(--color-white)'
        return None       # 自定义属性 / 不认识的角色：语义不明 ⇒ 不动
    return None


def neutral(v):
    u"""近中性（三通道极差 ≤ 8）⇒ 只许落到灰阶族上。
    ⚠ 不加这条，`#E7EBF1` 这种「带一点点蓝的浅灰」会被拉到某个有色阶梯的浅档上
      （`--blue-1` / `--giencoderblue-1` 与它通道差很小）⇒ 浅色档会出现肉眼可见的**偏色**。
    ⚠ 阈值取 8 而不是 16：`#EFF4FF`（极差 16）是**明明白**的浅蓝，按 16 会把它当灰阶上的
      `--gray-1`（Δ8）⇒ 直接丢掉色相。取 8 后它落到 `--blue-1`（Δ7），保色相。"""
    return max(v) - min(v) <= 8


def map_value(prop, v):
    """→ 替换串 或 None（不改）。"""
    p = prop.lower()
    if p in SKIP_PROP_EXACT or any(s in p for s in SKIP_PROP_SUB):
        return None
    if v in EXEMPT_VALUES or v in EXCLUDE_VALUES:
        return None
    # ★★ 第七批·B：**函数式字面**（`rgb()/rgba()`）走**独立显式表**，不与 hex 的启发式混用。
    #    理由见 `LIT_OVERRIDE` 上方：hex 那套的 EXACT/NEAR 判据是**逐位十六进制**，喂函数式会直接崩。
    if not v.startswith('#'):
        if v in LIT_OVERRIDE:
            return LIT_OVERRIDE[v]
        if _rgb_of(v) == (255, 255, 255):     # 不透明白：按**属性角色**分流（与 hex 侧 `#ffffff` 同口径）
            return pick_role(prop, u'#ffffff')
        return None
    # ★★ 显式覆盖表优先于一切启发式（含自定义属性的 lim=6 限制）
    if v in OVERRIDE:
        tgt, _note, _d = OVERRIDE[v]
        if tgt:
            return tgt
        # 双角色 `#DAE3ED`：按属性名分流（面 → fill，线 → border）
        nm = prop.lower()
        return DAE3ED_LINE if RE_LINEISH.search(nm) else DAE3ED_FILL
    w = pick_role(prop, v)
    if w:
        return w
    # ★ 自定义属性（`--xxx`）**只收 EXACT 与极近的 NEAR(≤6)**：
    #   它的消费方（谁拿它当底色 / 字色 / 描边）从声明处看不出来 ⇒ 放宽阈值 = 赌。
    #   典型反例：`--xxx: #FFFFFF` 若按 NEAR 走，会被 Δ8 拉到 `--gray-1`（#f7f7f7）——
    #   浅色档凭白变灰，而它本来可能是「压在有色底上的白字」。宁可不改。
    lim = 6 if p.startswith('--') else TOL
    ex = EXACT.get(v)
    if ex:
        fam, lv = ex[0]
        return u'rgb(var(--%s-%d))' % (fam, lv)
    vv = tuple(int(v[i:i + 2], 16) for i in (1, 3, 5))
    r = near(vv, fam='gray' if neutral(vv) else None)
    if r and r[2] <= lim:
        return u'rgb(var(--%s-%d))' % (r[0], r[1])
    return None


# ★★ 第四批：`<script>` 里的颜色字面 —— **必须带「这是渲染值」的正向证据**才敢换。
#
#   背景（本拍实测，**改变了原先的判断**）：这 10 页里各有一个 229~324KB 的匿名编译 bundle，
#   里面引号色值**混着三类东西**：
#     ① 真·渲染值：`fill:`#FFFFFF`` / `style:{color:`#6B6B6B`}` / `fill="#FFA000"`（SVG 呈现属性）；
#     ② **设计规格数据**：`{textColor:`#1E1E1E`, textToken:`文本/@color-text-1`, …}`
#        —— ★ 本拍**推翻了上一版判断**：实测它的消费方是
#          `style:{...Ve, color:e.textColor}` / `style:{background:e.bg||'transparent'}` /
#          `(…jsx)('path',{d:e.d, fill:e.fill})` ⇒ 它**就是渲染值本身**，
#          不是「只给人看的规格面板」⇒ **该换**（而且它自带的 `*Token` 字段正好告诉我们换成哪个 token）。
#          `textToken` / `bgToken` 两个字段**全站 0 处被消费**，是纯注释 ⇒ 永远不该动（且它们存的是
#          token 名、不是色值 ⇒ 正则天然匹配不到）。
#     ③ **选择器/查找用字面**：`[style*="#fff"]` / `querySelector('#fff')` ⇒ 换了就失配。
#
#   ⇒ 判据收紧成**三条同时成立**：
#     a. **属性键白名单**：字面必须**紧跟** `fill|color|background|stroke|border*|outline*|…:` 之后
#        （或 SVG 的 `fill="…"`）；—— 这条把 ③ 那类「选择器里的字面」天然排除
#        （选择器里 hex 前面是 `*=` 或引号，不是属性键）；
#     b. **注释值哨兵**：字面**自己**是被 `…Token:` 引导的（回看紧邻的键名含 `Token`）⇒ 跳过；
#        ⚠ 上一版用的是「**向后** 70 字符内有 `Token:`」⇒ 会把 `textColor:` 这个**渲染值**
#          连同它的 `textToken:` 兄弟字段一起误杀。实测后果：同一枚 logo 的 `fill` 有 3 处被
#          拦下、133 处被换（同页同图标两种颜色）——**不一致比不换更糟**。改成**回看**后归零。
#     c. 品牌 logo 色 + 不在显式表里且非逐位等值 ⇒ 跳过。
#   ★ 另做了**真机实测**：`fill="var(--color-danger)"` 在本机 Chromium 解析成功
#     （`getComputedStyle().fill` = `rgb(245, 63, 63)`）⇒ SVG 呈现属性里的 `var()` 可用。
JS_KEY = (u'fill|color|background|backgroundColor|bg|bgColor|border|borderColor|'
          u'borderTopColor|borderBottomColor|borderLeftColor|borderRightColor|stroke|'
          u'outline|outlineColor|boxShadow|textDecorationColor|caretColor|backgroundImage')
#   ⚠ `bg` 收进来的依据（实测，不是猜）：全站 `bg:'<色值>'` 共 54 处，**清一色是面**——
#     50 处 `bg:'#FFFFFF'` + 4 处 `bg:'#F3F4F5'`，消费方是
#     `style:{...Be, background: e.bg || 'transparent'}` / `background: e.bg ?? void 0`
#     ⇒ 全是 `background` 角色，零误伤。
#   ⚠ **没收**的键与其理由（同样实测）：
#     · `logoColor`（70 处，值 `#9E67E1/#0E97FC/#F87461/#2DAD6A/#F49250`）——
#       工作空间身份色，且**键名含 `logo`**，与 CSS 侧 `SKIP_PROP_SUB` 的 `logo` 豁免同口径；
#     · `c`（28 处，值 `#699650/#DE8F3E/#C49E29/#8865F3/#B6536E/#3C8BA1/#6079E5`）——
#       单字母键，实为**工作空间头像调色板**（`var SPACES=[{n:…,c:'#699650'}…]`）。
#       身份色若随档翻转，同一个空间在明暗两档会换色 ⇒ **语义错误**，故不动。
#     · `bg-[#28C840]` / `bg-[#DAE3ED]` 这类**尾风任意值类名**：`bg` 后面是 `-[` 不是 `:`/`=`，
#       正则天然不命中 —— 这是对的，类名与 CSS 选择器必须成对改，改一边就是断链。
RE_JSLIT = re.compile(
    u"(?:\\b(" + JS_KEY + u")\\s*[:=]\\s*|\\b(fill)=)"          # ①属性键 + 冒号/等号 ②SVG 的 fill=
    u"(['\"`])(#[0-9a-fA-F]{3,8}|rgba?\\(\\s*\\d[^)]*\\))\\3")
RE_JSSPEC = re.compile(u"Token\\s*:\\s*['\"`]?$")     # 回看：这个引号前面就是 token 注释键
JS_HITS = set()          # 只在报告里打「JS」标记用


def map_js_value(v, key=None):
    u"""JS 侧：**显式表优先**，其次逐位等值，再其次按角色定「白」。

    ⚠ 不做**就近推断**（与 CSS 侧不同）：JS 字面可能是数据、可能是状态机，Δ 判据在这里不成立。
      ⇒ 想扩表就往 `OVERRIDE` 里加条目（族由**语义**定），别放阈值。
    ⚠ 「白」**必须按角色分流**，理由是可核的：页面早就有一批暗色档钩子
      `[style*="background: rgb(255, 255, 255)"] → --color-bg-2`（见 apply-dark.py ⑥）。
      若 JS 侧一律给 `var(--color-white)`（两档都是 #ffffff），**内联属性就变成
      `background: var(--color-white)`，那个 `[style*=]` 钩子立刻失配** ⇒ 白底按钮在暗色下
      重新变白 = **真回归**。给 `var(--color-bg-2)` 则与钩子**逐位同值**（浅 #ffffff / 暗 #232324）。
    """
    v = v.lower()
    # ★★ 第七批·B：**函数式字面**（JS 侧同口径）。`RE_JSLIT` 本来就匹配 `rgba?(...)`，
    #    以前「扫得到但不换」是因为表里没有函数式的键 ⇒ 这里接上同一张 `LIT_OVERRIDE`。
    #    ⚠ `rewrite_scripts` 传进来的是 `raw.lower()`，**可能带空格**（`rgba(255, 255, 255, 0.88)`）
    #      ⇒ 必须先 `norm_lit` 归一，否则静默漏改。
    if not v.startswith('#'):
        _lit = norm_lit(v)
        if _lit is None:
            return None
        if _lit in LIT_OVERRIDE:
            return LIT_OVERRIDE[_lit]
        if _rgb_of(_lit) == (255, 255, 255):
            return pick_role(key or u'', u'#ffffff')
        return None
    # ★★ 第六批（邵先生 2026-10-02 裁决①）：**OVERRIDE 提到 EXEMPT 之前**。
    #   为什么必须动这个顺序：`#000000` 是 `EXEMPT_VALUES` 里的成员（CSS 侧要豁免 ——
    #   页面里有一批 `rgba(0,0,0,…)` / 阴影字面用它），但在 **JS 侧**它是 Kimi 单色标识的
    #   `fill:'#000000'`，暗色档比值 0.79 ⇒ 必须换成 `var(--color-text-1)`。
    #   ⚠ 两集合的**唯一**重叠项就是 `#000000`（已逐项核对：其余 13 个豁免值没有一个是
    #     OVERRIDE 的键）⇒ 提前 OVERRIDE 只影响这一个值，且 `map_value`（CSS 侧）**不动**，
    #     豁免语义原样保留。
    if v in OVERRIDE:
        tgt = OVERRIDE[v][0]
        return tgt if tgt else None
    if v in EXEMPT_VALUES or v in EXCLUDE_VALUES:
        return None
    w = pick_role(key or u'', v)
    if w:
        return w
    ex = EXACT.get(v)
    if ex:
        fam, lv = ex[0]
        return u'rgb(var(--%s-%d))' % (fam, lv)
    return None


def rewrite_scripts(body, sink):
    u"""把 `<script>` 里**有渲染证据**的颜色字面换成 DS 变量（保持引号样式）。
    三条守卫见 `RE_JSLIT` / `RE_JSSPEC` 上方注释；不满足则**原样保留**（宁可漏，不可错）。"""
    n = 0
    out = []
    last = 0
    for m in RE_JSLIT.finditer(body):
        key = (m.group(1) or m.group(2) or u'').lower()
        q, raw = m.group(3), m.group(4)
        if RE_JSSPEC.search(body[max(0, m.start(3) - 26):m.start(3)]):
            continue                      # 字面自己就是 token 注释值
        v = hex6(raw[1:]) if raw.startswith('#') else raw.lower()
        rep = map_js_value(v, key)
        if not rep:
            continue
        sink.append((u'script', v, rep))
        JS_HITS.add(v)
        out.append(body[last:m.start(4)])
        out.append(rep)
        last = m.end(4)
        n += 1
    if not out:
        return body, 0
    out.append(body[last:])
    return u''.join(out), n


# ------------------------------------------------------------------ 块扫描
RE_OPEN = re.compile(r'<(style|script)([^>]*)>')


def blocks(t):
    u"""**严格顺序扫描**（逐块推进 `pos`，绝不重叠）。

    ★★ 为什么不能用 `re.finditer` 一把列出开头标签（真踩，会毁页）：
      该页的匿名编译 bundle 里含有**字面的 `<script …>` 字符串**（React/Vite 产物里
      创建 script 元素那段），于是 `finditer` 会把它当成第二个块头，
      而它**到真正的 `</script>` 的距离**又构成一个「内层块」——
      该内层块的 `body` 完全落在前一块 `body` 内部（实测：base 224229 字符是
      324028 字符的后缀，两块 `end` 同为 324303）。
      而 `main()` 的拼接契约是 `t[last:s] + new_body`，一旦两块重叠，
      第二块的 `ns`（新块体）会被**再插一遍** ⇒ 单页凭空多出 ~224KB 重复 bundle。
      ⇒ 判据：**块区间必须两两不交且按位置升序**；实现方式 = 每找到一块就从其
        `</tag>` 之后继续搜，而不是预先枚举所有开头标签。
    """
    pos = 0
    while True:
        m = RE_OPEN.search(t, pos)
        if not m:
            return
        tag = m.group(1)
        end = t.find(u'</' + tag + u'>', m.end())
        if end < 0:
            return
        idm = re.search(r'id="([^"]+)"', m.group(2))
        bid = idm.group(1) if idm else u'(anon)'
        yield bid, tag, m.end(), end, t[m.end():end]
        pos = end + len(tag) + 3          # 越过 `</tag>`


def segs(t):
    u"""`blocks()` 的**补集版**：在块与块之间再插入「HTML 静态区」伪块（`tag='html'`）。

    ★★ 为什么必须补这一层（第七批·C 实测，第 6 类盲区）：本脚本原先只走 `blocks()`，
      而**静态 HTML 里的内联 `style="…"` 属性既不在 `<style>` 也不在 `<script>` 里**
      ⇒ 从来没被扫过。实测 `avatar.html` 有一处
      `style="background: rgb(236,242,255); color: rgb(55,112,247); border: 1px solid rgb(211,226,255)"`
      —— 暗色档早就被 `apply-dark.py` 的 `[style*=…]` 规则管住了，**但浅色档一直是字面**。
      判别方式：`(tag == 'html')` ⇒ 交给 `rewrite_inline()`。
    ⚠ 与 `blocks()` 的拼接契约**完全一致**：区间两两不交、按位置升序、首尾闭合到 `len(t)`。
    """
    prev = 0
    for bid, tag, s, e, body in blocks(t):
        if s > prev:
            yield u'(html)', u'html', prev, s, t[prev:s]
        yield bid, tag, s, e, body
        prev = e
    if prev < len(t):
        yield u'(html)', u'html', prev, len(t), t[prev:]


RE_STYLEATTR = re.compile(r'style="([^"]*)"')


def rewrite_inline(body, sink):
    u"""静态 HTML 区：只处理 `style="…"` 属性里的声明（复用 `rewrite_decls` ⇒ 判据完全一致）。"""
    out = []
    last = 0
    n = 0
    for m in RE_STYLEATTR.finditer(body):
        val = m.group(1)
        if not RE_ANYCOLOR.search(val):
            continue
        nv, k = rewrite_decls(val, sink)
        if not k:
            continue
        out.append(body[last:m.start(1)])
        out.append(nv)
        last = m.end(1)
        n += k
    if not out:
        return body, 0
    out.append(body[last:])
    return u''.join(out), n


RE_RULE = re.compile(r'([^{}]*)\{([^{}]*)\}')
# ★★ 暗色选择器：**命中即整条规则跳过**。
#   理由（本脚本最危险的一处，真踩过）：页面里早就有一批
#   `[giencoder-theme='dark'] { --r93-card: #232324; --r93-edge: #333335; … }`
#   —— 那里面写的字面值**本来就是暗色值**。若照浅色档那套表去查，
#   `#232324` 会被「就近」拉成 `rgb(var(--gray-10))`，而 `--gray-10` 在暗色档是 **#f7f7f7**
#   ⇒ 暗色卡底被翻成**近白**，整页破相。凡暗色档一律不碰（它的取值由 apply-dark.py 负责）。
RE_DARKSEL = re.compile(r"giencoder-theme|\.dark\b|\[data-theme|prefers-color-scheme")


def rewrite_body(tag, body, sink):
    u"""把块体里每条规则 `选择器 { 声明… }` 的色值逐个查表替换（暗色选择器整条跳过）。"""
    if tag != 'style':
        return body, 0
    out = []
    last = 0
    n = 0
    for m in RE_RULE.finditer(body):
        sel = m.group(1)
        out.append(body[last:m.end(1)])
        seg = m.group(2)
        if RE_DARKSEL.search(sel):
            out.append(u'{')
            out.append(seg)
            out.append(u'}')
        else:
            seg2, k = rewrite_decls(seg, sink)
            out.append(u'{')
            out.append(seg2)
            out.append(u'}')
            n += k
        last = m.end()
    out.append(body[last:])
    return u''.join(out), n


def rewrite_decls(seg, sink):
    res = []
    last = 0
    n = 0
    for m in RE_DECL.finditer(seg):
        prop, val = m.group(1), m.group(2)
        if not RE_ANYCOLOR.search(val):
            continue
        newval = val
        # ★★ 第七批·B：遍历**统一色值正则**（hex ∪ 函数式），每个命中先 `norm_lit` 归一成规范键。
        for h in RE_ANYCOLOR.finditer(val):
            raw = h.group(0)
            v = norm_lit(raw)
            if not v:
                continue
            rep = map_value(prop, v)
            if not rep:
                continue
            sink.append((prop.strip(), v, rep))
            newval = newval.replace(raw, rep, 1)
            n += 1
        if newval != val:
            res.append(seg[last:m.start(2)])
            res.append(newval)
            last = m.end(2)
    if not res:
        return seg, 0
    res.append(seg[last:])
    return u''.join(res), n


# ---------------------------------------------------------------- 第七拍·D
# ★★ 尾风**任意值色类**里的硬编码 hex（`bg-[#E9ECEE]` / `hover:bg-[#E9ECEE]` …）
#
# 这是全站「暗色没统一」的**总根源**：类名写在 React 源里、由尾风**预编译**成
# `.bg-\[\#E9ECEE\]{--tw-bg-opacity:1;background-color:rgb(233 236 238/var(--tw-bg-opacity,1))}`
# —— 值被**烧死**在产物里，暗色档不会翻转。
#
# 实测依据（base 页 DS 内联包，`script/(anon)` 之外）：
#   产物中**已预编译** 32 个 `var()` 形式的工具类，含我们要用的全部目标：
#     .bg-\[var\(--color-fill-1\)\]            {background-color:var(--color-fill-1)}
#     .bg-\[var\(--color-fill-2\)\]            {background-color:var(--color-fill-2)}
#     .hover\:bg-\[var\(--color-fill-1\)\]:hover{background-color:var(--color-fill-1)}
#     .hover\:bg-\[var\(--color-fill-2\)\]:hover{background-color:var(--color-fill-2)}
#     .bg-\[var\(--color-border-2\)\]          {background-color:var(--color-border-2)}
#     .border-\[var\(--color-border-1\)\]      {border-color:var(--color-border-1)}
#     .border-\[var\(--color-border-2\)\]      {border-color:var(--color-border-2)}
#   ⇒ 改名**安全**（产物已备好），无需新增规则、无需重编译。
#
# 映射铁律：**只用「上一档/下一档」的语义 token**，且色差取最小可用（见每行尾注）。
# 尾风类名区分大小写、且 `hover:bg-[x]` **包含** `bg-[x]` 子串 ⇒ 必须**按长度倒序**替换。
TW_CLASS = [
    # —— 菜单 / 下拉项（⭐ 本拍主目标：统一到「默认权限」下拉的 --color-fill-2）
    (u'hover:!bg-[#E9ECEE]', u'hover:!bg-[var(--color-fill-2)]'),   # ×8   「新会话」按钮（带 !important）
    (u'hover:bg-[#E9ECEE]',  u'hover:bg-[var(--color-fill-2)]'),    # ×74  浅 Δ9
    (u'bg-[#E9ECEE]',        u'bg-[var(--color-fill-2)]'),          # ×10  当前项底 浅 Δ9
    # —— 外壳底
    (u'bg-[#F4F5F6]',        u'bg-[var(--color-fill-1)]'),          # ×20  基础工作台 浅 Δ3
    (u'bg-[#E5EDF5]',        u'bg-[var(--color-fill-2)]'),          # ×10  研发工作台 浅 Δ13（比基础深一档，保留层级）
    # —— 分段控件槽 / 面板描边
    (u'bg-[#E4E6EA]',        u'bg-[var(--color-border-2)]'),        # ×10  浅 Δ5（=gray-3）
    (u'bg-[#DAE3ED]',        u'bg-[var(--color-border-2)]'),        # ×10  浅 Δ11
    (u'border-[#DAE3ED]',    u'border-[var(--color-border-2)]'),    # ×10  浅 Δ11
    (u'border-[#ECEEF2]',    u'border-[var(--color-border-1)]'),    # ×10  浅 Δ6
    # 说明：`bg-[#FF5F57]` / `bg-[#FEBC2E]` / `bg-[#28C840]`（macOS 交通灯，各 10 处）
    #       是**操作系统语义色**，不属设计系统用色范畴 ⇒ 按「只豁免品牌 logo + 系统色」保留。
]
TW_CLASS.sort(key=lambda kv: -len(kv[0]))          # ★ 先长后短（避免 hover: 前缀被吃）

# ★ 目标类**未被预编译**时才需要的手写补充（目前只有 1 条）：
#   `hover:!bg-[…]` 这个「带 !important 的 hover 任意值类」在产物里**没有** var 版本
#   （实测产物中带 `\!` 的 var 类 = 0 个）⇒ 必须自己补一条，否则改完类名会**失去 hover 底色**。
#   ⚠ 不能省掉 `!important`：`.new-chat-btn` 在暗色层有 `background: … !important`，
#     浅色档 `.r74-nc-css` 也有同族声明 —— 不带 `!` 会被压掉。
TW_EXTRA = u'''
  /* ★ r109 第七拍：**尾风任意值工具类的目标规则补充**。
     背景：源码里的**任意值色类**（`bg-[#RRGGBB]` 这种形态）已被本拍整体换成
     `bg-[var(--color-fill-N)]` / `border-[var(--color-border-N)]`；其中绝大多数目标类
     尾风**已预编译**在 DS 内联包里（实测 32 个 var 形式工具类），无需补。
     **唯此一条**「带 `!important` 的 hover 变体」没有预编译版本 ⇒ 在此手写补齐；
     缺了它「新会话」按钮会失去 hover 底色。
     ⚠ 本块**两档都生效**（无 theme 前缀），故紧接暗色层之后 —— 与暗色层同特异性时由后者胜。 */
  .hover\\:\\!bg-\\[var\\(--color-fill-2\\)\\]:hover { background-color: var(--color-fill-2) !important; }
'''
TW_BLOCK_ID = u'r109-tw-css'
# ★★ 锚点必须是**真正的**锚点：`</head>` 在本仓**不可用** —— `apply-dark.py` 的块注释里
#    就写着 `` `</head>` `` 这个字面（"本块注入在 `</head>` 前…"），`find('</head>')`
#    会命中**注释内**那一个，把补充块插进注释中间 ⇒ 既非法、又会在暗色层下次重插时被整段吞掉。
#    ⇒ 与 `apply-dark.py` 用**同一个锚点**：`<script id="r109-theme-js">…</script>`（每页唯一、
#      由 `apply-theme.py` 注入、且在 `</head>` 之前）。
RE_ANCHOR_TW = re.compile(r'<script id="r109-theme-js">.*?</script>\n', re.S)
# ★★ 插入点必须**锚在暗色块之后**，不能也用 `r109-theme-js` 那个锚点：
#    两个脚本若抢同一个锚点，`apply-dark.py` 每次都会把自己的块插回锚点正后方
#    ⇒ 两块的先后**来回翻转** ⇒ 每次跑都报「有变更」⇒ **破坏幂等**。
#    锚在「暗色块之后 ⇒ 二者顺序恒为 `dark → tw`，无论哪个脚本先跑都收敛到同一形态。
RE_DARK_BLOCK = re.compile(r'<style id="r109-dark-css">.*?</style>\n', re.S)


def ensure_tw_block(t):
    u"""幂等注入 / 刷新 `r109-tw-css` 补充块（锚点见上）。"""
    tag = u'<style id="%s">%s</style>\n' % (TW_BLOCK_ID, TW_EXTRA)
    if tag in t:
        return t, 0                                  # 已是目标态
    t = re.sub(r'<style id="%s">.*?</style>\n?' % TW_BLOCK_ID, u'', t, flags=re.S)
    m = RE_DARK_BLOCK.search(t)
    if not m:
        m = RE_ANCHOR_TW.search(t)                   # 退化：暗色块还没注入
    if not m:
        return t, 0
    return t[:m.end()] + tag + t[m.end():], 1


def tw_class_swap(t, gtw=None):
    u"""把尾风任意值色类整体换成 DS 变量形式（纯字符串替换，幂等）。"""
    n = 0
    for a, b in TW_CLASS:
        c = t.count(a)
        if c:
            t = t.replace(a, b)
            n += c
            if gtw is not None:
                gtw[(a, b)] += c
    return t, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()

    print(u'=== r109 第四拍 ②：页面 CSS 字面值 → DS 色彩变量（%s） ==='
          % (u'检查' if a.check else u'落盘'))
    gtot = collections.Counter()
    gjs = collections.Counter()
    gtw = collections.Counter()
    gwhere = collections.defaultdict(set)
    n_page = n_block = 0
    for pg in ALL:
        p = os.path.join(PAGES, pg + '.html')
        t, nl = rd(p)
        n_rev = 0
        for _old, _new in REVERT:
            if _old in t:
                n_rev += t.count(_old)
                t = t.replace(_old, _new)
        if n_rev:
            print(u'   ~ %-13s 回滚 %d 处（冷灰页面底改回字面）' % (pg, n_rev))
        sink = []
        parts = []
        last = 0
        changed = 0
        prev_end = 0
        for bid, tag, s, e, body in segs(t):
            # ★ 拼接契约的不变量：块区间**两两不交且升序**（见 blocks() 头注释）。
            assert s >= prev_end, u'块区间重叠：%s %s [%d,%d) 与上块止于 %d' % (pg, bid, s, e, prev_end)
            prev_end = e
            if bid in SKIP_BID:
                continue
            if tag == 'html':                       # 第七批·C：静态内联 style 属性
                nb, kt = tw_class_swap(body, gtw)   # ★ 第七拍·D：块外静态 class 里的尾风任意值
                nb, k = rewrite_inline(nb, sink)
                k += kt
            elif tag == 'style':
                if bid == u'(anon)' and DS_FINGERPRINT in body:
                    continue
                nb, k = rewrite_body(tag, body, sink)
            else:
                nb, kt = tw_class_swap(body, gtw)   # ★ 第七拍·D：尾风任意值色类
                nb, k = rewrite_scripts(nb, sink)
                k += kt
            if k:
                parts.append(t[last:s])
                parts.append(nb)
                last = e
                changed += k
                n_block += 1
        if parts or n_rev:
            parts.append(t[last:])
            t2 = u''.join(parts)
        else:
            t2 = t
        # ★ 第七拍·D：末尾统一刷新补充块（放循环外 ⇒ 不动块区间偏移）
        t2, twk = ensure_tw_block(t2)
        if twk:
            changed += twk
        if not parts and not n_rev and not twk:
            continue
        n_page += 1
        for prop, v, rep in sink:
            gtot[(v, rep)] += 1
            if prop == u'script':
                gjs[(v, rep)] += 1
            gwhere[(v, rep)].add(pg)
        if not a.check:
            io.open(p, 'wb').write(t2.replace(u'\n', nl).encode('utf-8'))
        print(u'   %s %-13s %5d 处' % (u'*' if a.check else u'√', pg, changed))
    print()
    print(u'── 替换明细（值 → 变量，×次数；JS = 其中来自 <script> 的次数）──')
    for (v, rep), n in sorted(gtot.items(), key=lambda x: -x[1]):
        ex = EXACT.get(v)
        if not v.startswith('#'):
            tag = u'LIT   '                      # 第七批·B：函数式字面（独立显式表）
        elif v in OVERRIDE:
            _t, _n, _d = OVERRIDE[v]
            tag = u'TABLE Δ%-2d' % _d
        elif v in WHITE:
            tag = u'ROLE  '
        elif ex:
            tag = u'EXACT '
        else:
            vv = tuple(int(v[i:i + 2], 16) for i in (1, 3, 5))
            r = near(vv, fam='gray' if neutral(vv) else None)
            tag = u'NEAR Δ%-2d' % (r[2] if r else -1)
        print(u'   %-12s %-18s → %-30s ×%-4d JS %-4d [%s]'
              % (tag, v, rep, n, gjs[(v, rep)], u','.join(sorted(gwhere[(v, rep)]))[:52]))
    print()
    if gtw:
        print(u'── 第七拍·D：尾风任意值色类 → DS 变量类（%d 处）──' % sum(gtw.values()))
        for (v, rep), n in sorted(gtw.items(), key=lambda x: -x[1]):
            print(u'   %-24s → %-34s ×%-4d' % (v, rep, n))
        print()
    print(u'   合计 %d 处（其中 <script> %d 处）/ %d 个不同值 / 触及 %d 页'
          % (sum(gtot.values()), sum(gjs.values()), len(gtot), n_page))
    print(u'   ⚠ <script> 侧多为**同一份编译 bundle 复制到 10 页**，故次数 ≈ 单页站点数 × 页数。')
    if a.check:
        print(u'   （--check：未落盘）')


if __name__ == '__main__':
    main()

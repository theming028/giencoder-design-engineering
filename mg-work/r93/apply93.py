# -*- coding: utf-8 -*-
"""r93 · 基础工作台「会话详情」视图（邵先生第 2 条）

需求：点击左侧 aside 里的会话任务标题后，右侧 main 容器呈现该会话的用户/AI 对话详情，
      按设计稿 MasterGo `1393:18748`（容器 264 · 1168×5144）像素级还原。
邵先生已回答的四点：① 全量还原；② 所有会话都用设计稿这一份内容；③ 轨迹页签切统一空态；
                    ④ 折叠可点 + 关键 hover/popover 做。

★ r93 ④（用户第 2 轮答复）—— 会话详情改成**独立页面**，composer 改为**复用真实组件**：

  · `pages/conversation.html` = **新独立页**（由 base.html 净底重建，见 main()），承载会话详情。
    它不自己实现「点会话 → 切视图」，因为进入这一页就是详情本身。
  · `pages/base.html` 只保留一个 4KB 的 `r93-nav-js`：捕获阶段监听 aside，
    `button.min-w-0.flex-1`（会话项）⇒ `location.href='conversation.html'`；
    分组标题（`rounded-md` + `py-0`）⇒ 放行（只折叠）；其余放行（外壳自己处理）。
  · 路由：`SHELL-NAV-FIX v5` 的 `var ROUTE = {...}` 每页一份（实测 9 页逐字相同），
    本脚本幂等插入 `'/conversation': 'conversation.html'`（**共 9 处**；conversation.html 的
    ROUTE 由 base 净底继承，不再重复插）。
  · ★ 底部 composer **不再自绘** —— 直接复用外壳 React 渲染的那一份
    （`div.relative.flex.w-full.flex-col.rounded-[16px].border.bg-white.p-3.transition-cols`，
    含 textarea + [添加/技能/数字分身/标准模式] + [模型/优化提示词/发送] 及其下方
    `工作目录 (可选) / 默认权限` 一整行）。做法 = **纯 CSS**：把 hero 的
    「LOGO + 问候语」与「版权页脚」藏掉、hero 由 `justify-center` 改 `justify-end` 贴底、
    宿主 `order:-1` 排到 hero 之前 ⇒ 视觉顺序 = 详情(可滚) 在上、真实 composer 在下。
  · MutationObserver 兜底：React 若把我们的节点冲掉就补回。

几何标定（设计稿 PNG mg-work/r93/raw/design-1393-18748-s1.png，1170×5146，png = design + 1）：
  · 内容列 840 宽、在 1168 的面板里**左右各 164 ⇒ 居中**；实机 main 内宽 1162 ⇒ 居中后左右各 161。
    故一律 `width:840px; margin:0 auto`（不照搬 164 的左内距 —— 那会偏左 3px 且不自适应）。
  · 纵向节奏：普通块间距 16；分节块（压缩上下文 / 上下文已压缩 / 搜索资料 / 告警条 / 模型已切换）24；
    用户气泡距头 32、助手头距气泡 32、「上下文注入」距助手头 12；composer 距状态条 12。逐块写进
    `--mt`（不用 nth-child，改一处不动别的）。
  · 字号：正文/标签 14px、元信息 12px、页头标题 16px 600（逐像素量过：标题「开发管理」4 字墨迹 63px
    = 16px/字；文件名「部门人员名单.xlsx」卡片 160 = 12+16+8+112+12，文字墨迹 111 ⇒ 14px）。

⚠️ 与全局字号机制（r87-ui-css）的约定：本块 CSS 里**凡是带 `var(--font-size-*)` 的规则都不得声明
   `height:Npx`** —— apply88b 的 scale_block 会把这类规则的高度一并按 --ui-fs-ratio 派生，盒子会跟着字号
   变高。故「尺寸」与「字号」一律拆成两条规则（见 CSS 里 r93-t14 / r93-t12 系列）。

用法：
  python mg-work/r93/apply93.py            # 应用（幂等：base 先摘净底，再分别落到两页 + 9 页路由表）
  python mg-work/r93/apply93.py --revert   # 回滚（删 conversation.html + 摘 base 的 nav 脚本 + 摘路由表条目）
  python mg-work/r93/apply93.py --dry
"""
import argparse
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
RAWI = os.path.join(HERE, 'raw', 'asset', 'icons')
PAGE = os.path.join(REPO, 'pages', 'base.html')
PAGE_CONV = os.path.join(REPO, 'pages', 'conversation.html')

CSS_ID = 'r93-conv-css'      # → conversation.html
JS_ID = 'r93-conv-js'        # → conversation.html
NAV_ID = 'r93-nav-js'        # → base.html（只有「点会话 ⇒ 跳独立页」这一条）
ATTR_HOST = 'r93-conv-host'
ATTR_PAGE = 'data-r93-page'  # conversation.html 的 <html> 上打这个标记，CSS 全挂它

# `SHELL-NAV-FIX v5` 里的路由表（每页一份，实测 9 页逐字相同）
ROUTE_OLD = "'/settings': 'settings.html' };"
ROUTE_NEW = "'/settings': 'settings.html', '/conversation': 'conversation.html' };"
# conversation.html 的 <html> 标记（幂等：已存在则不再插）
HTML_OLD = '<html lang="zh-CN">'
HTML_NEW = '<html lang="zh-CN" data-r93-page="conversation">'
# 独立页的浏览器标签名（与基础工作台区分）
TITLE_OLD = '<title>基础工作台</title>'
TITLE_NEW = '<title>会话 · 基础工作台</title>'

# ---------------------------------------------------------------- 图标
# 全部来自设计稿导出（72 个临时 Artifact 落盘在 mg-work/r93/raw/asset/icons）。
# 单色图标由 extract_icon() 剥掉写死的 fill 改 currentColor ⇒ 颜色交给 CSS token；
# 多色图标（GienCoder 头像 / 文件类型徽标 / agent 徽标）保留原色。
ICON_FILES = {
    # 页头 / 用户消息
    'auto':   'svg_07c0df05.svg',   # 「自动化」胶囊里的小图标（12px，#F77234）
    'gienx':  'svg_f429800f.svg',   # GienCoder 头像 24px（多色）
    'fmd':    'svg_8a09417c.svg',   # 附件徽标 · .md / .xlsx（多色）
    'fxls':   'svg_6b6ff8ec.svg',   # 附件徽标 · vscode 配色（多色）
    # 折叠块头图标（14px）
    'ctx':    'svg_c92382eb.svg',   # 上下文注入
    'think':  'svg_babd97a5.svg',   # 深度思考
    'bash':   'svg_1edf52f8.svg',   # Bash（红）
    'bashg':  'svg_b1ed08f4.svg',   # Bash（灰）
    'web':    'svg_bfdedd58.svg',   # 网页搜索
    'quiz':   'svg_7c1c891e.svg',   # 需求采访
    'todo':   'svg_eaa3d24d.svg',   # 更新任务清单
    'write':  'svg_9e161bef.svg',   # 文件写入
    'skill':  'svg_1d5c65e3.svg',   # SKILL
    'tool':   'svg_b730ef8d.svg',   # Tool call
    'retry':  'svg_e85b8c94.svg',   # 以重试模型请求
    'tools':  'svg_5312e834.svg',   # 调用 N 个工具
    'zip':    'svg_1448f5c9.svg',   # 压缩上下文
    'search': 'svg_536db15e.svg',   # 搜索资料
    'surf':   'svg_66ad9348.svg',   # 未知 surface 事件
    'ok':     'svg_812e0422.svg',   # 绿色勾（#30953B）
    'model':  'svg_e79db3dd.svg',   # 模型已切换
    # 任务产物
    'arthtml': 'svg_58f34b4f.svg',  # prd-template.html（蓝，多色）
    'artmd':   'svg_6d57fa43.svg',  # user-story-*.md（灰，多色）
    'artall':  'svg_f31b60d8.svg',  # 查看所有产物（多色）
    'arthov':  'svg_a5ad09ed.svg',  # hover 卡 spec-template.md（多色）
    # 改动汇总
    'diffh':  'svg_fdb14c72.svg',   # 卡片头小图标
    'undo':   'svg_ac810281.svg',   # 撤销
    'review': 'svg_4be648ce.svg',   # 审查
    # 底部
    'rate':   'svg_bff3c9ce.svg',   # Token 速率
    'sync':   'svg_410da48c.svg',   # 状态条左图标（＝ agent 卡的「进行中」）
    'chevu':  'svg_55f7cbed.svg',   # 状态条右侧折叠箭头
    # composer
    'a1':     'svg_a131949f.svg',   # 游戏策划（多色）
    'a2':     'svg_21c343d2.svg',   # 项目经理（多色）
    'a3':     'svg_296dcd57.svg',   # 软件开发工程师（多色）
    'a4':     'svg_5939b075.svg',   # 测试工程师（多色）
    'c1':     'svg_f222a191.svg',   # 工具条第 1 枚
    'c2':     'svg_e08b0fbd.svg',   # 工具条第 2 枚
    'perm':   'svg_9798373b.svg',   # 默认权限
    'mbox':   'svg_401e4b68.svg',   # 模型选择右侧 28×28 钮
    'send':   'svg_2f5c1e18.svg',   # 发送钮（红）
}

# 设计稿没给导出（是 DS 图标实例）⇒ 按同风格手写。1.4px 描边 / 圆头，尺寸由 CSS 控。
ICON_INLINE = {
    'cv': '<svg viewBox="0 0 12 12" fill="none" aria-hidden="true">'
          '<path d="M2.6 4.4L6 7.8l3.4-3.4" stroke="currentColor" stroke-width="1.3" '
          'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'cvu': '<svg viewBox="0 0 12 12" fill="none" aria-hidden="true">'
           '<path d="M2.6 7.6L6 4.2l3.4 3.4" stroke="currentColor" stroke-width="1.3" '
           'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'cvb': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
           '<path d="M4 6.2L8 10.2l4-4" stroke="currentColor" stroke-width="1.4" '
           'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'more': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
            '<circle cx="3.4" cy="8" r="1.3" fill="currentColor"/>'
            '<circle cx="8" cy="8" r="1.3" fill="currentColor"/>'
            '<circle cx="12.6" cy="8" r="1.3" fill="currentColor"/></svg>',
    # ★ r96 ⑤：「分支」（Token 速率行第 2 枚图标）。设计稿里它是 DS 的 `icon-wrapper` 实例
    # （没有导出独立 svg），形状按 `raw/design-rgb.png` 的 14×14 点阵逐像素反推后换算到 16 网格：
    #   上节点 (4.5,3) r1.6 · 下节点 (4.5,12) r1.6 · 右节点 (10.5,3) r1.6（都是**空心圆**：
    #   PNG 里圆内像素比圆边浅 ⇒ 是 stroke 而非 fill）· 主线 x4.5 贯通上下节点 ·
    #   曲线自右节点下沿弯向左下，在主线 y≈8 处并入。
    'branch': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
              '<path d="M5.14 5.26V11.9" stroke="currentColor" stroke-width="1.5"/>'
              '<path d="M12 5.26c0 2.9-3 4.1-6.86 3.88" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
              '<circle cx="5.14" cy="3.43" r="1.83" stroke="currentColor" stroke-width="1.5"/>'
              '<circle cx="5.14" cy="13.71" r="1.83" stroke="currentColor" stroke-width="1.5"/>'
              '<circle cx="12" cy="3.43" r="1.83" stroke="currentColor" stroke-width="1.5"/></svg>',
    'copy': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
            '<rect x="5.6" y="1.6" width="8.8" height="8.8" rx="1.6" stroke="currentColor" '
            'stroke-width="1.3"/><path d="M10.4 11.6v1.4a1.6 1.6 0 0 1-1.6 1.6H3.2a1.6 1.6 0 0 1'
            '-1.6-1.6V7.4a1.6 1.6 0 0 1 1.6-1.6h1.4" stroke="currentColor" stroke-width="1.3" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    # ★ r99 ⑭：umeta 的「重新生成」图标重画。
    #   原实现是 **16 栅格**的一段小圆弧 + 右上角 L 形记号（`M13.2 8a5.2 5.2 0 1 1-1.7-3.85`
    #   + `M13.5 1.6v3.2h-3.2`），而宿主是 `.r93-iblk.r93-i14`（14px 盒）⇒ viewBox 16 被压到 14
    #   ⇒ 墨迹只有 10.7 单位 ≈ 9.4px，实测渲染成「一个小圆圈」。
    #   设计稿 `1393:18477` 的第一枚按钮（`fw647:14503`，props 尺寸14）里，把 design-rgb.png 的
    #   14×14 盒（png x955..969 / y221..235）逐像素分离后，墨迹只落在一条**上半圆弧 + 左下实心箭头**：
    #   弧 = 圆心 (9,10)、半径 5 的正圆上半（右端 13.9 起、越过顶点 (9,5)、左端收在 (4,4,9.4) 附近），
    #   弧外/弧内多出来的墨迹集中在 x1..6 / y7..10 一簇 ⇒ 即左下的实心箭头。
    #   故重画为 **14 栅格**（与 `.r93-i14` 盒 1:1，stroke 1.3 就是设计稿的 1.3），
    #   墨迹包络 0.5..13.9 × 4.5..10.6，与设计稿实测 0.5..14.5 × 4..10 对齐。
    'regen': '<svg viewBox="0 0 14 14" fill="none" aria-hidden="true">'
             '<path d="M13.9 9.4A5 5 0 0 0 4.1 8.9" stroke="currentColor" stroke-width="1.3" '
             'stroke-linecap="round"/><path d="M1.05 7.85 4.4 7.95 2.95 10.6Z" '
             'fill="currentColor"/></svg>',
    'open': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
            '<path d="M6.4 3.2H3.8a1.4 1.4 0 0 0-1.4 1.4v7.6a1.4 1.4 0 0 0 1.4 1.4h7.6a1.4 1.4 '
            '0 0 0 1.4-1.4v-2.6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>'
            '<path d="M9.6 2h4.4v4.4" stroke="currentColor" stroke-width="1.3" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M13.6 2.4L7.6 8.4" stroke="currentColor" stroke-width="1.3" '
            'stroke-linecap="round"/></svg>',
    'spin': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
            '<path d="M8 1.8a6.2 6.2 0 1 0 6.2 6.2" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round"/></svg>',
    'clock': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
             '<circle cx="8" cy="8" r="6.2" stroke="currentColor" stroke-width="1.3"/>'
             '<path d="M8 4.6V8l2.4 1.4" stroke="currentColor" stroke-width="1.3" '
             'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'plus': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
            '<path d="M8 3.2v9.6M3.2 8h9.6" stroke="currentColor" stroke-width="1.4" '
            'stroke-linecap="round"/></svg>',
}


# ★ r99 ④ 复盘：这里**曾经**有一段 `fit_viewbox()`（把「字形坐标跑到 viewBox 外」的图标自动
#   重算 viewBox）。它是个**假警报**，而且把两枚本来正确的图标改坏了，故整段删除。
#   实测根因：`svg_1d5c65e3.svg`（SKILL）与 `svg_e08b0fbd.svg` 的路径确实画在 x[12.8, 25.0]，
#   但同一元素上挂着 `transform="matrix(-1,0,0,1,26,0)"`（x → 26−x 的镜像）—— 镜像后字形正好
#   落在 x[1, 13] / y[1, 13]，**原本就与 `viewBox="0 0 14 14"` 严丝合缝**。
#   而 `glyph_bbox()` 只读 `d` 里的数字、不认 `transform`，于是算出「越界 90%」，把 viewBox 改成
#   `11.784 -0.05 14.225 14.225` ⇒ 字形反而被推到框外，只剩左沿一条 1px 残片（r99 目视取证抓到）。
#   按 transform 感知重新体检 78 个源文件：真正越界的只有 4 件 DS 组件内部结构图
#   （`svg_19c68c88` / `svg_38cbaeab` / `svg_b49ce54b` / `svg_31dd5c7e`），全部未被引用。
#   ⚠️ 教训：**改几何前先看元素上有没有 `transform`**；本页 8 个源文件带 matrix（含 4 个旋转 90° 的
#   `matrix(0,1,-1,0,1,-1)`），只按裸坐标推算一定会翻车。


def extract_icon(fname):
    """读设计稿导出 SVG → 精简成可内联的片段。

    ① 剥 `<defs>`（里面的 clipPath rect 恒等于整块 viewBox ⇒ 无作用），顺带消除多份内联后
       `master_svg0_*` id 重复的隐患；
    ② 单色图标（只有 0~1 种 fill）把写死的 fill 换成 currentColor，颜色交 CSS；
    ③ 多色图标（GienCoder 头像、文件徽标、agent 徽标）原样保留。
    """
    src = io.open(os.path.join(RAWI, fname), encoding='utf-8').read()
    m = re.search(r'viewBox="([^"]+)"', src)
    vb = m.group(1) if m else '0 0 16 16'
    src = re.sub(r'<defs>.*?</defs>', '', src, flags=re.S)
    src = re.sub(r'\s+clip-path="url\([^)]*\)"', '', src)
    body = src[src.index('>', src.index('<svg')) + 1:src.rindex('</svg>')].strip()
    fills = set(re.findall(r'fill="(#[0-9A-Fa-f]{3,8})"', body))
    if len(fills) <= 1:
        body = re.sub(r'\s+fill="(?:#[0-9A-Fa-f]{3,8}|none)"', '', body)
        body = re.sub(r'\s+fill-opacity="[^"]*"', '', body)
        body = re.sub(r'<(path|ellipse|circle|rect|polygon)\b',
                      lambda mm: '<%s fill="currentColor"' % mm.group(1), body)
    return '<svg viewBox="%s" fill="none" aria-hidden="true">%s</svg>' % (vb, body)


def jsstr(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ') + "'"


def build_icon_js():
    parts = []
    for k in sorted(ICON_FILES):
        parts.append('  %s: %s' % (k, jsstr(extract_icon(ICON_FILES[k]))))
    for k in sorted(ICON_INLINE):
        parts.append('  %s: %s' % (k, jsstr(ICON_INLINE[k])))
    return 'var ICON = {\n' + ',\n'.join(parts) + '\n};'


# ---------------------------------------------------------------- CSS

CSS = r"""
/* =====================================================================
   r93 · 基础工作台「会话详情」视图（设计稿 MasterGo 1393:18748 / 容器 264）
   几何标定与字号推导见脚本头注释；本节全部类名以 r93- 前缀自持。
   ===================================================================== */

/* --- 设计稿直出色（giencoder-design-system/tokens.md 无对应 token） ---
   逐条实测自 mg-work/r93/raw/design-1393-18748-s1.png（1170×5146，png = design + 1）：
     #EBEBED 页头下边框（png y=45 全宽平色带）
     #F5F6F7 卡片底（工具输出卡 / 产物卡 / 汇总卡，占位最多的一个色）
     #ECEEF2 带代码头卡片的 1px 描边 + 卡内头分隔线（png y=1017/1056）
     #E5EDFE 用户气泡底；#D0D7EA 气泡内药丸投影
     #FFF3E8/#FDDDC3  「自动化」虚线胶囊；#F77234 其图标
     #FFF7E8/#FFE4BA 告警条底/描边；#D25F00 其圆点
     #30953B 绿色勾；#333333 模型已切换图标；#C4C7C9 状态条圆点
     #327FCB 产物卡蓝色徽标；rgba(0,0,0,0.16) 卡内滚动条
     agent 徽标四组：紫 #E6E1FC/#6E27D9 · 靛 #E0E7FF/#4F46E5 · 蓝 #DBEAFE/#2563EB · 红 #FEE2E2/#DC2626
   ⚠ 设计稿只有浅色稿；暗色档按 DS 暗色 token 的口径给出等价替代（非设计稿实测）。 */
:root {
  --r93-line: #EBEBED;
  --r93-card: #F5F6F7;
  --r93-edge: #ECEEF2;
  --r93-bubble: #E5EDFE;
  --r93-bubble-sh: #D0D7EA;
  --r93-tag-bg: #FFF3E8;
  --r93-tag-bd: #FDDDC3;
  --r93-tag-ic: #F77234;
  --r93-warn-bg: #FFF7E8;
  --r93-warn-bd: #FFE4BA;
  --r93-warn-ic: #D25F00;
  --r93-ok: #30953B;
  --r93-ioc: #333333;
  /* ★ r96 ⑤：Token 速率行前两枚图标（复制 / 分支）。设计稿是 DS 的 `icon-wrapper`
     实例（PNG 实测 png(170,4670) 与 (204,4671) 的笔画色 = #6B6B6B，= 色阶 gray-7），
     比同行「Token 速率」文字（#868686 = gray-6）深一级 ⇒ 单列一条变量，别混用 text-3。 */
  --r93-ioc2: #6B6B6B;
  /* ★ r97 ④：输入卡**下方**那行统计文字（设计稿 `fw647:20893`，640×16）。
     PNG 逐像素实测笔画色 = (169,169,169) = #A9A9A9 = DS 原始色阶 **gray-5**
     （不是 `--color-text-4` 的 gray-4 #C9C9C9，也不是 text-3 的 #868686）。
     直接引 `--gray-5` 三元组 ⇒ 暗色档自动跟着色阶翻转（暗色 gray-5 = #868686），
     故**本变量只在浅色档声明一次**，暗色块里不再重复。 */
  --r93-meta: rgb(var(--gray-5));
  --r93-dim: #C4C7C9;
  --r93-blue: #327FCB;
  /* ★ r99 ⑫：用户气泡里 `/命令` 胶囊（`.r93-pill`）的文字色。设计稿 `fw647:14402`
     的 `text/text` **没有显式字号**（走 DS 默认），字号由 PNG 墨迹反推为 14px 档；
     颜色 PNG 实测笔画 (52,145,250) = #3491FA —— **不是** `--color-primary-6` 的 #3770F7：
     同一张图上「网页搜索」那些蓝字实测正是 (55,112,247)，两者确为不同色。 */
  --r93-pillc: #3491FA;
  --r93-sb: rgba(0,0,0,0.16);
  --r93-hov-bg: #ECF2FF; --r93-hov-bd: #D3E2FF;
  --r93-a1-bg: #E6E1FC; --r93-a1-ic: #6E27D9; --r93-a1-bd: #E2D3F9;
  --r93-a2-bg: #E0E7FF; --r93-a2-ic: #4F46E5;
  --r93-a3-bg: #DBEAFE; --r93-a3-ic: #2563EB;
  --r93-a4-bg: #FEE2E2; --r93-a4-ic: #DC2626;
}
[giencoder-theme='dark'] {
  --r93-line: #333335;
  --r93-card: #232324;
  --r93-edge: #333335;
  --r93-bubble: #24314C;
  --r93-bubble-sh: rgba(0,0,0,0.45);
  --r93-tag-bg: rgba(247,114,52,0.14);
  --r93-tag-bd: rgba(247,114,52,0.4);
  --r93-warn-bg: rgba(255,190,110,0.1);
  --r93-warn-bd: rgba(255,228,186,0.26);
  --r93-sb: rgba(255,255,255,0.18);
  /* r99 ⑫：浅色 #3491FA 的暗色等价（暗底上要提亮 ⇒ 取更浅一档蓝）。 */
  --r93-pillc: #6BA6FF;
  --r93-hov-bg: rgba(55,112,247,0.16); --r93-hov-bd: rgba(55,112,247,0.4);
  --r93-a1-bg: rgba(110,39,217,0.2); --r93-a1-bd: rgba(110,39,217,0.5);
  --r93-a2-bg: rgba(79,70,229,0.2);
  --r93-a3-bg: rgba(37,99,235,0.2); --r93-a4-bg: rgba(220,38,38,0.2);
  /* r96 ⑤：浅色 gray-7 的暗色等价（暗色色阶是反的 ⇒ gray-7 取 #C9C9C9）。 */
  --r93-ioc2: #C9C9C9;
}

/* --- 宿主：只在 pages/conversation.html 常显；基础工作台里永不显示 ---
   ★ r93 ④：本页 = 外壳（顶栏 + aside）照旧 + main 内常驻的会话详情 + **外壳自己的真实 composer**。
   技巧：mainInner（`main > div`，外壳 React 渲染的 flex column）里，
     · 我们的宿主 `.r93-conv-host` 用 `order:-1` 排到 hero 之前；
     · hero（`div.flex-1.justify-center`）由居中改**贴底**、且只留它里面的 composer；
     · hero 的「LOGO + 问候语」与 mainInner 的「版权页脚」用 display:none 藏掉。
   ⇒ 视觉顺序 = 会话详情（可滚，flex:1）在上、真实 composer（flex:none）在下。
   全程只改**视觉**，不动 DOM 血缘 ⇒ React 重渲染不会炸。 */
.r93-conv-host { display: none; }
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center {
  flex: 0 0 auto !important; justify-content: flex-end !important;
  /* ★ r97 ③：把 hero 的 `px-6`（左右各 24）**清零**。原因：composer 的外壳 `div.mt-8` 是
     hero 的 `w-full` 子盒，hero 一有横向内距，`.mt-8` 就比 main 内宽**少 48** ⇒ 它下面的
     `width:50%` 算出来的输入卡比「状态条 / 内容列」两端各短一截（2560 实测短 12px）。
     清零后 `.mt-8` = main 内宽，三个宽度基准才真正统一（详见 `.r93-wrap` 的 r97 ③ 注释）。
     问候语（`.pointer-events-none`）已隐藏 ⇒ 本页无其它内容依赖这个内距。 */
  padding: 0 0 8px 0 !important;   /* 底部留白：设计稿 artboard 底 − 统计行底 ≈ 7px（本轮补回统计行后） */
}
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > .pointer-events-none {
  display: none !important;
}
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > div.mt-8 {
  margin-top: 0 !important;
}
/* ★ r97 ④：输入卡**下方**那行统计文字（设计稿 `fw647:20893`：640×16 / 12px / #A9A9A9）。
   做法 = 纯 CSS 的 `::after` 挂在 React 渲染的 `div.mt-8` 上（React 重渲染拿不掉，
   零 DOM 注入）。该容器是 `flex flex-col items-center gap-2` ⇒ 文字天然成为**第 2 个居中
   flex 项**，与输入卡的间距正好是容器的 gap = 8px（设计稿实测 8px）。 */
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > div.mt-8::after {
  content: '2 轮 · 27 步 · LLM 3m36s · 工具调用 7.2s · 首 token 平均 0.8s · 159 tok/s · 缓存命中 96% · 输入 1M tok · 输出 31.1K token';
  font-size: var(--font-size-body-1); line-height: 16px; color: var(--r93-meta);
  white-space: nowrap;
}
html[data-r93-page='conversation'] main > div > div.pb-6 { display: none !important; }
html[data-r93-page='conversation'] .r93-conv-host {
  display: flex; flex-direction: column; flex: 1 1 auto; min-height: 0;
  order: -1;
  background: var(--color-bg-2); overflow: hidden;
}

/* ★ r94 ③：真 composer **只留输入卡本体** —— 邵先生点名 `div.relative.flex.w-full.flex-col.
   rounded-[16px].border.bg-white.p-3.transition-colors`，其外围（外壳的灰壳 `bg-[var(--color-fill-1)]`
   + `px-3 py-3` + `rounded-[16px]`，以及「工作目录 / 默认权限」那一行）全部不要。
   实测 outer（`div.mt-8 > div`）只有 2 个直接子：① 输入卡（含 textarea）② 底排 ⇒ 用 `:not(:has(textarea))`
   精确只留输入卡（不依赖顺序）。不动 DOM 血缘，React 重渲染安全。 */
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > div.mt-8 > div {
  background: none !important; padding: 0 !important; border-radius: 0 !important;
  /* ★ r95 ②：外壳宽度**自适应撑满内容列**（与 `.r93-wrap` / `.r93-bottom` 同口径）。
     它原本由 Tailwind 写死一个定值 ⇒ 容器一变宽就跟不上内容列。基数同为 `.mt-8`（= main 内宽）。 */
  width: 50% !important; min-width: 860px !important;
}
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > div.mt-8 > div > div:not(:has(textarea)) {
  display: none !important;
}

/* ★ r94 ④：本页**不需要「波点」装饰**。⚠ 点阵不在 `div.mt-8` 容器内（实测该容器只有 1 个子 = composer 外壳），
   真正的来源是 `main.dot-bg` 自身的点阵 + `main.dot-bg::before` 的光斑层（全页唯一的这两处装饰层）
   ⇒ 页面级把这两层一起摘掉（滚动区与 composer 区一并变干净）。 */
html[data-r93-page='conversation'] main.dot-bg { background-image: none !important; }
html[data-r93-page='conversation'] main.dot-bg::before { display: none !important; }
/* ★ r99 ⑤：本页「点哪都起涟漪」的补刀。r94 ④ 只摘掉了 *点阵底色*，但 r74 那条
   `document` 捕获段的 pointerdown 监听**仍在跑** —— 它把 `.r74-ripple` 插进 `main.dot-bg`
   的队首并按点击位置播环，排除名单只覆盖了「欢迎态主内容块 + 版权带 + 可交互控件」，
   会话语义区（我们的 `.r93-conv-host`、真实 composer）**不在名单里** ⇒ 页面底部一点就冒波点。
   ⚠️ 修法用 CSS 而不是加排除项：那条监听是另一轮的产物（r74/r79 的注入块），
     往它的选择器里塞本页选择器会污染 base 页的脚本；而且脚本自身要留「播完自毁」的逻辑。
     只把涟漪**画的东西**清零（点阵 background-image），`animationend` 仍会照常触发 ⇒
     节点照旧自毁、不留垃圾；本页的 `main.dot-bg` 反正也已无点阵（见上一条），语义一致。 */
html[data-r93-page='conversation'] .r74-ripple { background-image: none !important; }

/* --- 字号/行高工具类（**只放字号与行高**，尺寸一律另立规则 —— 见脚本头注释） ---
   字号口径全部由设计稿 1393:18748 反推（PNG 逐像素 + 节点框高双向验证）：
     · 折叠头标题 / 用户气泡正文 / 深度思考 / 需求采访 = 14px，行高 22px
       （由「取代先前的快照」84px÷7 字 = 12px、深度思考卡 200 = 24 + 8×22 互证）
     · 折叠头 meta（skill-catalog / 2s / deepwiki …）= 12px，行高 22px
     · 卡内正文/代码 = **12px，行高 20px**（SKILL 64 = 24 + 2×20、网页搜索 184 = 24 + 8×20、
       重试 64 = 24 + 2×20、搜索资料 116 = 24 + 4×20 + 12 gap、未知 surface 84 = 24 + 3×20）
     · 上下文注入 = 12px，行高 **16px**（788×80 = 5 行，PNG 实测行距 16）
     · Bash 卡代码 = 12px，行高 **16px**（780×96 = 6 行） */
.r93-t14 { font-size: var(--font-size-body-3); line-height: 22px; color: var(--color-text-3); }
.r93-t14m { font-size: var(--font-size-body-3); line-height: 22px; font-weight: 500; }
.r93-t14b { font-size: var(--font-size-body-3); line-height: 22px; font-weight: 600; }
.r93-t12 { font-size: var(--font-size-body-1); line-height: 16px; }
.r93-t12g { font-size: var(--font-size-body-1); line-height: 16px; font-weight: 500; }
.r93-t12l { font-size: var(--font-size-body-1); line-height: 22px; }
/* ★ r98 ①：**对话内容区的 14px 统一上调到 15px**。DS 字号档只有 body-3=14 / title-1=16，
   没有 15 ⇒ 走页面级覆盖。三条讲究：
     · **只写 font-size**，不碰 line-height/height ⇒ 上面三条的 `line-height: 22px` 仍由 apply88b
       派生成 `calc(22px * var(--ui-fs-ratio))`（字号杠杆继续生效）。⚠ 本规则自身不含
       `var(--font-size-*)`，故 unscale→scale 不会去动它（无行高/高度可动）。
     · 选择器保持 **(0,1,0)**：r97 ① 的 `.r93-card.r93-card *`（0,2,0）仍能把**卡内**文本压回 13px
       （绝不能给它加 `html[data-...]` 前缀 ⇒ (0,2,1) 会反超卡规则）。
     · 字号写成 `calc(15px * var(--ui-fs-ratio))` 而**不写裸 px 字面量**，与本工程字号杠杆口径一致
       （⚠ 措辞讲究：门禁会扫注释里的裸字号写法 ⇒ 注释里也别出现字面量）。 */
.r93-t14, .r93-t14m, .r93-t14b { font-size: calc(15px * var(--ui-fs-ratio)); }
/* ★ r93 ②：卡内正文（12/20）、上下文注入（12/16）、居中提示卡片下的说明行（12/24 —— 
   设计稿 ui 778×24 / 300×24）。与 .r93-t14 严格区分。 */
.r93-t12c { font-size: var(--font-size-body-1); line-height: 20px; }
.r93-t12s { font-size: var(--font-size-body-1); line-height: 16px; }
.r93-t12h { font-size: var(--font-size-body-1); line-height: 24px; }
.r93-t16b { font-size: var(--font-size-title-1); line-height: 24px; font-weight: 600; }
.r93-ell { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.r93-c3 { color: var(--color-text-3); }
.r93-c2 { color: var(--color-text-2); }
/* ★ r96 ③：需求采访卡的「回答行」= `.r93-t14.r93-c2`。设计稿实测为**正文色**不是浅一级 ——
   design-rgb.png 该两行（y=1579 / y=1639）笔画色 (31,31,31) = #1F1F1F = text-1；
   同卡的问题行（y=1553/1613/1673）实测 (134,134,134) = #868686 = text-3（即 `.r93-t14` 默认值）。
   ⇒ 显式拉回 text-1。特异性 (0,2,0) > `.r93-c2` 的 (0,1,0)，与书写顺序无关。 */
.r93-t14.r93-c2 { color: var(--color-text-1); }
.r93-c1 { color: var(--color-text-1); }
.r93-clink { color: var(--color-primary-6); }
.r93-cwarn { color: var(--r93-warn-ic); }
.r93-okc { color: var(--r93-ok); }
/* ★ r93 ②：网页搜索 / 搜索资料卡里「整行是链接」的样式（PNG 实测 #3770F7 + 下划线）。 */
.r93-wlink { display: block; color: var(--color-primary-6); text-decoration: underline; text-underline-offset: 2px; }
.r93-wlink:hover { color: var(--color-primary-5); }
.r93-wlist { display: flex; flex-direction: column; }
.r93-srch { display: flex; flex-direction: column; gap: 6px; }
.r93-srchg { display: flex; flex-direction: column; gap: 3px; }

/* --- 图标盒（尺寸与色，不含字号） --- */
.r93-iblk { display: inline-flex; align-items: center; justify-content: center; flex: none; }
.r93-iblk > svg { width: 100%; height: 100%; display: block; }
.r93-i14 { width: 14px; height: 14px; }
.r93-i16 { width: 16px; height: 16px; }
.r93-i12 { width: 12px; height: 12px; }
.r93-i24 { width: 24px; height: 24px; }
.r93-i32 { width: 32px; height: 32px; }
.r93-dot4 { width: 4px; height: 4px; border-radius: 50%; background: var(--color-text-4); flex: none; }
.r93-dot6 { width: 6px; height: 6px; border-radius: 50%; background: var(--color-border-2); flex: none; }
.r93-bt { border: 0; background: transparent; padding: 0; cursor: pointer; color: inherit; font: inherit; }

/* ===================== 页头 44px ===================== */
.r93-bar {
  position: relative; flex: none; height: 44px;
  border-bottom: 1px solid var(--r93-line); background: var(--color-bg-2);
}
.r93-seg {
  position: absolute; left: 8px; top: 8px;
  gap: 0; padding: 1px; border-radius: 6px; background: var(--color-fill-1);
}
.r93-seg .giencoder-radio-button { height: 24px; padding: 0 12px; border-radius: 5px; }
.r93-seg .giencoder-radio-button { font-size: var(--font-size-body-3); line-height: 22px; }
.r93-seg .giencoder-radio-button-checked {
  background: var(--color-bg-2); border: 1px solid var(--color-border-2);
  color: var(--color-primary-6); font-weight: 400;
}
.r93-seg .giencoder-radio-button-checked:hover { background: var(--color-bg-2); }
.r93-seg-cap {
  /* ★ r94 ①：在页头 `.r93-bar` 内**水平居中**（原 left:396px 是按设计稿 1168 面板量的固定值，换视口即偏）
     ⇒ 用 50% + translateX(-50%)；垂直已居中（10 + 24 + 10 = 44 = bar 高）。 */
  position: absolute; left: 50%; top: 10px; transform: translateX(-50%); height: 24px;
  display: flex; align-items: center; gap: 8px;
}
.r93-capname { color: var(--color-text-1); }
.r93-capname { max-width: 208px; }
.r93-captag {
  display: inline-flex; align-items: center; gap: 4px; flex: none;
  height: 24px; padding: 0 10px; border-radius: 24px;
  background: var(--r93-tag-bg); border: 1px dashed var(--r93-tag-bd);
  color: var(--r93-tag-ic);
}
.r93-captag .r93-iblk { color: var(--r93-tag-ic); }
.r93-captime { color: var(--color-text-3); flex: none; }
.r93-morebtn {
  position: absolute; right: 8px; top: 8px; width: 28px; height: 28px;
  border-radius: 6px; color: var(--color-text-2);
}
.r93-morebtn:hover { background: var(--color-fill-2); }

/* ===================== 主体 ===================== */
.r93-pane { display: flex; flex-direction: column; flex: 1 1 auto; min-height: 0; }
.r93-pane[hidden] { display: none; }
/* ★ r95：`scrollbar-gutter: stable both-edges` —— 滚动条占位会把本容器内容盒收窄，
   使内容列相对**没有滚动条**的底部列（`.r93-bottom`）与 composer 偏左半个滚动条宽
   （1440 实测偏 5px ⇒ 内容块右边界 1265 / 状态条 1270 / 输入卡 1280 三条线打架）。
   both-edges 让两侧各让出等量 gutter ⇒ 内容恒居中，与底部同轴。 */
.r93-scroll { position: relative; flex: 1 1 auto; min-height: 0; overflow-y: auto; overflow-x: hidden; scrollbar-gutter: stable both-edges; }
/* ★ r97 ③：把滚动条宽度在本容器上**显式钉死**（全站默认也是 10px，见页面自身的
   `::-webkit-scrollbar{width:10px}`）—— 好让下面 `.r93-wrap` 的 `+10px` 补偿有据可依。 */
.r93-scroll::-webkit-scrollbar { width: 10px; }
/* ★ r94 ②：内容容器宽度 = **main 容器的 50%**、**最小 860px**。
   ★ r95 ①：内容块从「设计稿固定宽」改为**流式撑满** ⇒ 这里不再需要左右内距，wrap 的 padding 只留纵向。
   ★ r97 ③：**宽度基准与底部列 / composer 对齐**。根因：三者各挂在宽度不同的父盒上，
     却都用百分比 ⇒ 父盒不同宽则结果不同（2560 实测）：
       · `.r93-wrap`   的父盒 = 滚动内容盒（`both-edges` gutter 左右各占 10 ⇒ 比 main 内宽少 20）
       · `.r93-bottom` 的父盒 = `.r93-pane` （= main 内宽）
       · composer      的父盒 = `div.mt-8`（原 hero 带 `px-6` ⇒ 比 main 内宽少 48）
     结果 wrap 1131 / bottom 1141 / composer 1117 —— 输入卡比状态条**两端各短 12px**。
     修法：把父盒的基准差补回来（+10px）+ hero 横向内距清零 ⇒ 三者恒等于 `max(50% × main 内宽, 860px)`。
     ⚠ 补偿值 = 滚动条宽 10px（上一条已在本容器钉死；改滚动条宽度必须同步改这里）。 */
.r93-wrap { width: calc(50% + 10px); min-width: 860px; box-sizing: border-box; margin: 0 auto; padding: 32px 0 48px; }
/* ★ r98 ②：**单轮末尾 `.r93-rateline` 下面留 48px**（原为 24）。
   该模块是本轮最后一个 `.r93-it`（`isLast` 实测 true、无 nextSibling）⇒ 「下面间距」= 内容盒下内距，
   直接改 wrap 的下内距即可（每块自带的 `--mt` 只管「上面」）。 */

/* 纵向节奏：每块自带 --mt，默认 16 */
.r93-it { margin-top: var(--mt, 16px); }
.r93-it:first-child { margin-top: 0; }

/* ★ r94 ⑤：设计稿里的「假滚动条」`.r93-vsb`（6px 绝对定位色条）已按要求移除 ——
   卡内改用真实 `overflow-y: auto`（见 `.r93-card--ctx`）。 */

/* ===================== 用户消息 ===================== */
.r93-bub { margin-left: auto; width: 728px; display: flex; flex-direction: column; }
/* ★ r96 ①：气泡内容**最大高度 240px**，超出**卡内滚动**（长提问不把整列顶下去）。
   ⚠ 只改体（`.r93-bubi`）不改 `.r93-bub`（气泡列本身仍是内容高，右侧对齐不受影响）。 */
.r93-bubi {
  display: flex; align-items: flex-start; gap: 6px;
  padding: 9px 12px; border-radius: 8px 8px 2px 8px; background: var(--r93-bubble);
  max-height: 240px; overflow-y: auto; overflow-x: hidden;
}
/* ★ r99 ⑫：按设计稿 `fw647:14402`（节点名「容器 25」）逐项对齐。它挂的 `.r93-t12`
   （12/16）把尺寸压小了 —— 设计稿实测：
     · 盒 **138×22**（board x288..425 / y85..106）：内距 1/6 + 文字行盒 20 ⇒ 1+20+1 = 22
     · 文字墨迹 x294..414 = 120px（17 个半角）⇒ 字号 **14px 档**（@12px 只有 102px，对不上）；
       本轮按「内容区统一 15px」口径取 15，行高仍写 20 ⇒ 盒高保持 22（高度是设计稿硬值）
     · 文字色 #3491FA（见 `--r93-pillc` 注释）；圆角 3 / 白底 / 投影 `0 1px 2px #D0D7EA` 设计稿原本就叠了
       （`box-shadow` 写在 `容器 25` 的 style 上，不是我们加的）⇒ 全部保留。
   ⚠️ 不再复用 `.r93-t12`（模板里已摘掉）：两者同为 (0,1,0)，靠书写顺序压太脆。 */
.r93-pill {
  flex: none; display: inline-flex; align-items: center; padding: 1px 6px;
  border-radius: 3px; background: var(--color-bg-2); color: var(--r93-pillc);
  box-shadow: 0 1px 2px 0 var(--r93-bubble-sh);
  font-size: calc(15px * var(--ui-fs-ratio)); line-height: 20px;
}
.r93-ubt { color: var(--color-text-1); min-width: 0; }
/* 附件卡：设计稿是**两行右对齐**（第 1 行 部门人员名单.xlsx + 产品初版设计方案.md，第 2 行 vscode…），
   总宽 645+12 < 728 本可一行放下 ⇒ 说明换行是画稿显式排的，故用两个 row 写死。 */
.r93-attrow { margin-top: 6px; display: flex; justify-content: flex-end; gap: 6px; }
.r93-att {
  display: inline-flex; align-items: center; gap: 8px; height: 40px; padding: 0 12px;
  border-radius: 8px; border: 1px solid var(--color-border-1);
  background: var(--r93-card); color: var(--color-text-1);
}
.r93-att:nth-child(1) { background: var(--color-fill-1); }
.r93-umeta { margin-top: 8px; height: 24px; display: flex; align-items: center; justify-content: flex-end; gap: 0; }
.r93-umeta .r93-t12 { color: var(--color-text-3); }
/* ★ r99 ⑭：时间与右侧两枚图标按钮的间距。设计稿 `1393:18477`（容器 180，95×24）内三件：
   时间墨迹 0..28 · 第一个 icon-wrapper 盒 41..65 · 第二个 71..95（右缘贴容器右缘，= 气泡右缘）
   ⇒ 时间→按钮 **13**、按钮↔按钮 **6**；原实现 `gap: 0` 三件连排（实测 15:26 右缘正好压在
   第一个按钮左缘、两按钮也贴死）。两条间距用 margin 表达（父级 gap 仍为 0）。 */
.r93-umeta > .r93-t12 { margin-right: 13px; }
.r93-umeta > .r93-ib + .r93-ib { margin-left: 6px; }
.r93-ib { display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 4px; color: var(--color-text-2); }
/* ★ r99 ⑨：hover 底色改「白底 + 1px 描边」。原 `--color-fill-2`（242）在**灰卡**里
   （`.r93-card` = #F5F6F7）比卡底还深，看起来像一块脏斑；设计稿给的图标按钮 hover 态
   正是这个口径 —— 改动汇总卡的悬停行里，⋯ 盒实测是「白底 24×24 + 1px (229,229,230) 描边」，
   与本页 `.r93-dmore:hover` 同款。白底 + 描边在白底页面上同样成立，两处都不违和。 */
.r93-ib:hover { background: var(--color-bg-2); box-shadow: inset 0 0 0 1px var(--color-border-2); }
/* ★ r99 ⑨：复制成功态（点击后图标换成绿勾，图标由脚本替换，这里只管颜色与动效）。 */
.r93-ib.is-copied { color: var(--r93-ok); }
.r93-ib.is-copied > .r93-iblk > svg { animation: r93-pop-in 0.18s cubic-bezier(0.34, 0.69, 0.1, 1) both; }
@keyframes r93-pop-in { from { opacity: 0; scale: 0.6; } }

/* ===================== 助手头 ===================== */
.r93-ahd { height: 24px; display: flex; align-items: center; gap: 6px; }
.r93-ahd .r93-t14b { color: var(--color-text-1); }
.r93-alink {
  margin-top: 14px; height: 22px; display: inline-flex; align-items: center; gap: 2px;
  color: var(--color-text-3); border-radius: 4px;
  /* ★ r98 ①：补一次字号。根因：`.r93-bt`（第 412 行）的 `font: inherit` 与 `.r93-t12` 同为 (0,1,0)
     却**写在后面** ⇒ 后写者胜，这条「任务完成，耗时28m12s」一直被撑成 14px。
     ★ r99 ⑪：本轮改为与内容区一致的 15px。设计稿 `fw647:14447`（DS Link 164×22，gap 2）的
     文字墨迹实测 x166..311 = 145px —— 7 个汉字 + 6 个半角 ⇒ 字号落在 14~15px（@12px 只有 120px，
     对不上；r98 当时把字数点成「11 汉字 + 5 半角」才误判成 12px）。按本轮「内容区统一 15px」口径取 15。
     本规则写在 `.r93-bt` 之后 ⇒ 同特异性压得住那个 shorthand。 */
  font-size: calc(15px * var(--ui-fs-ratio));
}
.r93-alink:hover { color: var(--color-text-2); }
/* ★ r99 ⑬：助手头底边线「深一级」。原 `--color-border-1`（gray-2 = 242）与卡片里那些
   1px 分隔线同色，整块助手区收口太弱；设计稿 `直线 28` 实测 (242,242,242) 确实是最浅那档，
   但邵先生按可读性拍板深一级 ⇒ 取 `--color-border-2`（gray-3 = 229）。 */
.r93-asst { padding-bottom: 13px; border-bottom: 1px solid var(--color-border-2); }

/* ===================== 折叠块 ===================== */
.r93-fold { display: flex; flex-direction: column; }
.r93-fh {
  height: 22px; display: inline-flex; align-items: center; gap: 4px;
  align-self: flex-start; border-radius: 4px; color: var(--color-text-1); max-width: 100%;
}
.r93-fh:hover { background: var(--color-fill-2); }
.r93-fh .r93-cv { color: var(--color-text-1); }
.r93-ft { color: var(--color-text-1); flex: none; }
.r93-fm { color: var(--color-text-3); min-width: 0; }
.r93-fb { margin-top: 12px; }
.r93-fc {
  height: 22px; display: inline-flex; align-items: center; gap: 4px;
  /* ★ r100 ⑦：补 `max-width:100%` —— 折叠头现在也可能带一截元信息（`.ctmeta`），
     没有上限就会顶出内容列；与展开头 `.r93-fh` 同口径。 */
  max-width: 100%; align-self: flex-start; border-radius: 4px; color: var(--color-text-3);
}
.r93-fc:hover { background: var(--color-fill-2); }
.r93-fold[data-open='1'] > .r93-fc { display: none; }
.r93-fold[data-open='0'] > .r93-fh,
.r93-fold[data-open='0'] > .r93-fb { display: none; }
.r93-cv { transition: transform 0.2s ease; }
.r93-fold[data-open='0'] .r93-cv { transform: rotate(-90deg); }

/* 卡片 ★ r95 ①：宽度改为**流式 + 右侧撑满** —— 保留设计稿 18px 左缩进，右侧填满内容列。
   （原先写死 822px 是按设计稿量死：容器恰 840 时刚好，容器一变宽右侧就留白。） */
.r93-card {
  position: relative; width: calc(100% - 18px); margin-left: 18px; border-radius: 8px;
  background: var(--r93-card); padding: 12px; box-sizing: border-box;
  color: var(--color-text-1);
  /* ★ r96 ②：卡**默认字号 13px**（DS `--font-size-body-2`）—— 卡内未标字号的内容直接落这一档。
     ⚠ 本规则**不得**声明裸 `height`（apply88b 的 converge 会把带 `var(--font-size-*)` 的规则
     里的高度按比例改写）；本规则无 height ✓。具体块仍由 `.r93-t12*` / `.r93-t14*` 显式覆盖。
     ★ r99 ⑩：整卡曾升到 15px（与 r98 的「内容区统一 15px」同一口径）。
     ★ r100 ②：邵先生本轮要求 **卡内一律 14px** ⇒ 这两条一起回落到 14px
       （= DS 正牌档位 body-3；写法仍用 `calc(… * var(--ui-fs-ratio))` 以保住字号杠杆）。 */
  font-size: calc(14px * var(--ui-fs-ratio));
}
/* ★ r97 ①：`.r93-card` 容器内**所有**文本统一同一档。
   上一轮（r96 ②）只把「卡内裸文本」的默认档调成 13px，卡内仍混着 12px（`.r93-t12*` /
   `.r93-pre` / `.r93-wlink` / `.r93-clink` / `.r93-diffstar`）与 14px（`.r93-t14`）⇒ 同一张卡里
   出现 12 / 13 / 14 三档。本轮用一条后代通配把卡内字号**钉死在同一档**。
   ★ r99 ⑩ → r100 ②：这一档由 13px → 15px → **本轮的 14px**（邵先生：「所有 r93-card 容器内的
   字号都改成 14px」）。14px 就是 DS 正牌档位 `--font-size-body-3`，故不再特殊说明。
   ⚠ 只改 `font-size`，**不碰 `line-height`** ⇒ 卡高（含 4 张固定高的 tool-call 卡）零变化；
     代码块是等宽字体且 `pre-wrap`，14px 下最长一行（66 字符）≈ 554px < 可用 782px，不会换行。
   ⚠ 本规则不含 `height`/`min-height` ⇒ 不会被 apply88b 的 converge 改坏（见脚本头约束）。
   ⚠ 更新任务清单卡是**另一个容器** `.r93-todocard`（不在 `.r93-card` 名单里）：它 height 220
     且 `overflow:hidden`，输入区是 9 行 × 16 的定高 pre ⇒ 保持原档不动，避免被裁。
   ★★ **特异性坑**：`*` 的通配符**不贡献特异性** ⇒ `.r93-card *` 其实只有 (0,1,0)，与 `.r93-t12*`
      同级；写在本规则**之后**的同级规则（`.r93-pre`）会反超它（r97 首跑实测：卡内 37 处 13px，
      唯独 5 处 `.r93-pre` 仍是 12px）。故把类名写两遍，抬到 (0,2,0)，与书写顺序无关。
      （`.r93-card *` 的另一个替身写法 `.r93-card *:not(#x)` 更晦涩，不如重复类名好读。） */
.r93-card.r93-card, .r93-card.r93-card * { font-size: calc(14px * var(--ui-fs-ratio)); }
/* ★ r99 ⑩：**需求采访卡**（设计稿 1393:18500「容器 201」822×208）的专属内距与行距。
   设计稿子树逐节点读到：`容器 200`（第 1 组问答）252×48 @(20,20) —— 组内两行各 22 高、相差 4；
   `容器 199`（第 2 组）486×48 @(20,80) ⇒ 组间 **12**（20+48 = 68 → 80）。
   ⇒ 卡内距 **20**（不是通用卡的 12），问→答 **4**，答→问 **12**；
      卡高 = 20 + 3×48 + 2×12 + 20 = 208 ✓ 与设计稿一致。
   （旧实现是「12 内距 + 8/14 行距」，167 的净高凑巧也是 208，但左内距与行距都不是设计稿的值。） */
.r93-card--quiz { padding: 20px; }
/* ⚠ 刻意**不写 overflow:hidden**：卡内文件路径的 hover popover 要溢出卡片（设计稿 1393:18507
   就是浮在卡外的），裁剪会把浮层切掉；圆角改由内层 `.r93-chead` 自己收。 */
.r93-card--edge { border: 1px solid var(--r93-edge); padding: 0; }
.r93-card--full { width: 100%; margin-left: 0; }
.r93-cbody { padding: 12px 20px; }
/* ★ r93 ②：上下文注入卡的正文块。设计稿卡 822×150 = padding 24 + 16 + 7 + 16 + 7 + 80，
   末段 788×80（5 行 × 16）。PNG 逐像素实测行中心 447/470/492/508/524/540/556，
   即首两段行距 22、英文段行距 16、段间 7。 */
.r93-ctxbody { display: flex; flex-direction: column; gap: 7px; }
/* ★ r93 ②：上下文注入卡固定 822×150。设计稿长文在 MiSans 12px 下折 5 行（80px），
   实机 Mona Sans 度量更宽只折 4 行 ⇒ 用 min-height 保住卡高（内容自然排布，不裁切）。 */
/* ★ r94 ⑤：卡**最大高度 240px**，内容溢出**卡内滚动**（同时移除设计稿那根「假滚动条」`.r93-vsb`）。 */
.r93-card--ctx { min-height: 150px; max-height: 240px; overflow-y: auto; overflow-x: hidden; }
/* ★ r93 ②：更新任务清单卡（设计稿 822×220 = 16 + 144 + 线@181 + 16@192 + 12）。
   ⚠ 本规则**不含** var(--font-size-*)，故可安全写 height —— 见脚本头 converge 约束。 */
.r93-todocard {
  position: relative; width: calc(100% - 18px); margin-left: 18px; box-sizing: border-box;
  height: 220px; padding: 16px 20px 12px; border-radius: 8px;
  background: var(--r93-card); border: 1px solid var(--r93-edge);
  display: flex; flex-direction: column; overflow: hidden;
}
.r93-todoin { display: flex; gap: 12px; flex: none; }
.r93-todoline { flex: none; height: 1px; background: var(--r93-edge); margin: 21px -20px 0; }
.r93-todoout { flex: none; display: flex; align-items: center; gap: 12px; margin-top: 10px; }
.r93-chead {
  height: 40px; display: flex; align-items: center; gap: 8px; padding: 0 12px;
  border-bottom: 1px solid var(--r93-edge); box-sizing: border-box;
  border-radius: 7px 7px 0 0;
}
.r93-chead .r93-t12 { color: var(--color-text-1); }
.r93-chead .r93-cpath { color: var(--color-text-3); }
.r93-chead .r93-cmk { margin-left: auto; display: flex; align-items: center; gap: 4px; }
.r93-pre { margin: 0; white-space: pre-wrap; word-break: break-all; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
.r93-pre { font-size: var(--font-size-body-1); line-height: 20px; }
/* Bash 卡代码行高 16（设计稿 ui 780×96 = 6 行；PNG 实测行中心 Δ16.5/16）。 */
.r93-pre--tight { line-height: 16px; }
.r93-code { color: var(--color-text-1); }
.r93-diffstar { color: var(--color-text-3); }

/* 折叠头里的 4px 点 */
.r93-fh .r93-dot4 { margin: 0 4px; }

/* ===================== 居中分隔提示 ===================== */
/* ★ r95 ①：整行块一律 100%（撑满内容列右边界）。 */
.r93-note { width: 100%; display: flex; align-items: center; gap: 16px; }
.r93-nline { flex: 1 1 auto; height: 1px; background: var(--color-border-2); }
.r93-nrow { flex: none; display: flex; align-items: center; gap: 8px; }
.r93-nt { color: var(--color-text-1); }
.r93-nm { color: var(--color-text-3); }
/* ★ r100 ⑥：设计稿里这两行「说明」文字是**带浅灰圆角底的胶囊**，不是纯文字。
   取数 = `raw/design-rgb.png` 逐像素扫描（board 坐标，1x；`board(x,y) → png(x+1,y+1)`）：
     · 第 1 行（`fw647:18372`）底 x195..972 / y3355..3378 ⇒ **778×24**，墨迹左内距 13 / 右内距 13
     · 第 2 行（`fw647:18418`）底 x434..733 / y3433..3456 ⇒ **300×24**，墨迹左内距 13 / 右内距 14
   ⇒ 底 = **文字宽 + 两侧 12px 内距**（墨迹量到 13，减掉字形约 1px 侧承即为 12）；
      底色实测 **rgb(247,247,247)**，正是 `--color-fill-1`（gray-1）；
      圆角由角部灰度剖面反解 ≈ **12px**（= `--border-radius-xl`；24 高取到上限 ⇒ 视觉是全圆角胶囊）；
      行高 24（`.r93-t12h` 已给）。
   两行都在 840 内容列里**水平居中**（778 ⇒ 左右各留 31；300 ⇒ 左右各留 270 ✓）。
   ⚠ 原来是 `width:100%` 的整行居中文本，故这里同时改掉盒模型（`fit-content` + `margin:auto`）。 */
.r93-ndesc {
  width: fit-content; max-width: 100%; box-sizing: border-box;
  margin: 8px auto 0; height: 24px; padding: 0 12px;
  border-radius: var(--border-radius-xl);
  background: var(--color-fill-1); color: var(--color-text-3);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

/* ===================== 告警条 ===================== */
.r93-alert {
  width: 100%; height: 44px; box-sizing: border-box; border-radius: 8px;
  background: var(--r93-warn-bg); border: 1px solid var(--r93-warn-bd);
  display: flex; align-items: center; gap: 12px; padding: 0 16px;
}
.r93-alert .r93-adot { width: 6px; height: 6px; border-radius: 50%; background: var(--r93-warn-ic); flex: none; }
.r93-ahd2 { display: flex; align-items: center; gap: 8px; flex: none; }
.r93-ahd2 > .r93-t14 { color: var(--color-text-1); }
.r93-adesc { color: var(--color-text-2); min-width: 0; }
.r93-atag { margin-left: auto; color: var(--color-text-3); flex: none; }

/* ===================== 改动汇总卡 =====================
   ★ r98 ③：按设计稿 `1393:18681`「容器 252」（840×300）**逐像素重做**。
   取数双源 = `raw/design-1393-18748.html` 的节点样式 + `raw/design-rgb.png` 逐像素扫描
   （下列 x / y 均为**卡内相对值**；实测点见 `ev/p98a.js` / 本轮日志）：
     · 卡 840×300 / 圆角 8 / 外框 1px（--r93-edge）。★ **表头带铺 --r93-card、文件列表是纯白面板**
       （旧实现整张卡都铺 gray ⇒ 列表区偏灰、丢了那条白面板；实测 y42..299 = 255,255,255）
     · 表头**高 40**（`容器 238` = 822×28 @(12,6) ⇒ 上下各 6），**底部 1px 分隔线**（实测 y41 = (236,238,242)）
     · 行高 **36**、分隔线 `--color-border-1`（实测 (242,242,242)）；**首行无上边线**（表头已有分隔线）
     · 行内距 **左 11 / 右 13**（文件名墨迹 x13；⋯ 盒 x801..825 ⇒ 距卡内右沿 13）
     · 数字列右沿距卡内右沿 **54**（实测 x784 = 卡右 838 − 54）；数字列与 ⋯ 之间 **17**
     · 列表右沿一条 **6×128** 的滚动条 thumb（`矩形 219`：rgba(0,0,0,0.16) / 圆角 6 / 顶 4 / 右 4）
     · 字色：标题 / 文件名 / ⋯ / 按钮文字实测最深像素全是 (31,31,31) = text-1
       ⚠ ⋯ 旧值 text-2((78,78,78)) 偏浅，本轮改 text-1
     · +800 = **--r93-ok**（实测 (48,149,59) —— 注意**不是** `--color-success-6`(59,179,70)）
       -125 = `--color-danger-6`（实测 (245,63,63) ✓）
     · 按钮 = DS 次要按钮 small（白底 / --color-border-2 / 8 圆角）；设计稿外框 **70×28**
       ⇒ DS 基类自带 1px transparent 边框占 2px，内距要写 **11**（写 12 会得到 72）
     · 悬停行（设计稿叠了 app.json 的 hover 态）：行底 --r93-card + 文件名 primary +
       ⋯ 盒变**白底 + 1px 描边**（实测盒 = 24×24、描边 (229,229,230)） */
.r93-diff {
  position: relative; width: 100%; box-sizing: border-box; border-radius: 8px;
  background: var(--color-bg-2); border: 1px solid var(--r93-edge);
  overflow: hidden;
}
.r93-dhead {
  height: 40px; box-sizing: border-box; padding: 6px 6px 5px 12px;
  background: var(--r93-card); border-bottom: 1px solid var(--r93-edge);
  display: flex; align-items: center;
}
.r93-dh1 { display: flex; align-items: center; gap: 12px; min-width: 0; }
/* 表头图标槽：设计稿 `容器 236` 的图标槽宽 **24**（字形左缩 2 ⇒ 墨迹 x14..27）、标题紧随其后
   （`容器 168` @24 ⇒ 标题盒落在卡内 x36）。本页图标盒是 14（`.r93-i14`）⇒ 补 −3 让视觉间隙
   等于 9（= 设计稿「槽内字形右沿 15 → 标题 24」），标题正好落在 36。 */
.r93-dhead .r93-dh1 > .r93-iblk:first-child { margin-right: -3px; }
/* 表头里的 +800 / -125 是一组（`容器 167` gap 8），与外层 12 的间距分开 */
.r93-dh2 { display: inline-flex; align-items: center; gap: 8px; }
.r93-dtitle { color: var(--color-text-1); }
.r93-plus { color: var(--r93-ok); }
.r93-minus { color: var(--color-danger-6); }
.r93-dacts { margin-left: auto; display: flex; align-items: center; gap: 8px; }
.r93-dbtn { gap: 4px; height: 28px; padding: 0 11px; border-radius: 8px; }
/* 列表 = **白色面板**（设计稿 容器 251 内的 矩形 358），258 = 7×36 + 6 尾隙
   ★ r99 ①：**去掉「假滚动条」改为真实滚动**。原实现是「`overflow:hidden` + 绝对定位的
   6×128 色条 `.r93-dsb`」—— 那根条是照设计稿静态描出来的装饰，永远不动、也跟内容无关。
   本轮按邵先生要求：列表自己滚，滚动条交给浏览器。
   ⚠ 页面自身的 `@media (pointer:fine)` 已把滚动条钉成 10px 宽 / thumb 取色
     `rgba(gray-10,.16)` + 左右各 1/5px 透明边（= `width:10 - 1 - 5 = 4px` 可见、右贴 4px），
     与设计稿那根 6×128 / 右 4 / rgba(0,0,0,0.16) 是同一套参数 ⇒ 不再单独覆盖。
   ⚠ 7 行 ×36 = 252 < 258 ⇒ 当前**不会**出现滚动条（这正是「需要时显示」）；真溢出了才占 10px
     沟槽，此时 ⋯ 会随内容盒一起左移 10 —— 与设计稿「浮层式滚动条」的差别就在这里，可接受。 */
.r93-dlist { position: relative; height: 258px; overflow-y: auto; overflow-x: hidden; background: var(--color-bg-2); }
.r93-drow {
  height: 36px; display: flex; align-items: center; gap: 17px; padding: 0 13px 0 11px;
  border-top: 1px solid var(--color-border-1); position: relative;
  /* ★ r100 ④：整行都可点（左键 = 与右侧「⋯」同一张菜单，见 wire() 的点击委托），
     故整行给手型光标；原来只有 `.r93-dmore` 是 pointer、行本身是 auto。 */
  cursor: pointer;
}
.r93-drow:first-of-type { border-top: 0; }
.r93-drow:hover { background: var(--r93-card); }
.r93-drow:hover .r93-dname { color: var(--color-primary-6); }
.r93-dname { color: var(--color-text-1); flex: 1 1 auto; min-width: 0; }
.r93-dnum { display: flex; align-items: center; gap: 8px; flex: none; }
.r93-dmore { display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 4px; color: var(--color-text-1); }
.r93-dmore:hover { background: var(--color-bg-2); box-shadow: inset 0 0 0 1px var(--color-border-2); }

/* ===================== 改动汇总 · 行右键菜单（★ r99 ⑦） =====================
   邵先生要求：`.r93-drow` 整行支持右键菜单，且**点右侧「⋯」出的是同一个菜单**。
   设计稿没画这个菜单（是交互态）⇒ 取值全部走 DS Dropdown 契约 + 本仓 `pages/task-detail.html`
   已经落地过的右键菜单范式（`.td-ctx`，第 54/57 轮的实测结论）：
     面板 宽 182 / 内距 6 / 项间距 2 / 圆角 8 / 1px `--color-border-2` 描边 / `--shadow3-down`
     菜单项 内距 5px 8px / 图标-文字 8 / 圆角 4 / 13px-22px / 文字 `--color-text-1`
     hover  `--color-fill-2`
   ⚠️ 本页产物里已有一条同名 `.giencoder-dropdown-popup`（外壳 React 组件样式：
      `transform-origin:top / min-width:168 / padding:6` **且挂了一条 0.2s 的 entry 动画**，
      动画播完 `opacity` 会回落到 0 ⇒ 菜单「闪一下就不见」）。故这里用 `.r93-ctx` 双类提权，
      并把 `animation` 显式关掉，开合改走契约状态类 `.giencoder-popup-open`（与 Select / Popover 同参）。
   ⚠️ `.giencoder-dropdown-item` / `-divider` 在本页**没有内联**（只内联了 `-popup` / `-submenu` /
      `-arrow` 的骨架），所以这几条必须自己补 —— 这正是 r93 头注释里说的「按需自补」。 */
.r93-ctx.giencoder-dropdown-popup {
  position: fixed; z-index: var(--z-index-popup);
  box-sizing: border-box; min-width: 0; width: 182px; padding: 6px;
  display: flex; flex-direction: column; gap: 2px;
  background: var(--color-bg-popup);
  border: 1px solid var(--color-border-2);
  border-radius: 8px;
  box-shadow: var(--shadow3-down);
  transform-origin: top left;
  animation: none;
  opacity: 0; visibility: hidden; translate: 0 4px; scale: 0.96;
  transition: opacity 0.15s cubic-bezier(0.34, 0.69, 0.1, 1),
              translate 0.15s cubic-bezier(0.34, 0.69, 0.1, 1),
              scale 0.15s cubic-bezier(0.34, 0.69, 0.1, 1),
              visibility 0s 0.15s;
}
.r93-ctx.giencoder-dropdown-popup.giencoder-popup-open {
  opacity: 1; visibility: visible; translate: 0 0; scale: 1;
  transition: opacity 0.2s cubic-bezier(0.34, 0.69, 0.1, 1),
              translate 0.2s var(--transition-timing-function-spring, cubic-bezier(0.34, 0.69, 0.1, 1)),
              scale 0.2s var(--transition-timing-function-spring, cubic-bezier(0.34, 0.69, 0.1, 1)),
              visibility 0s;
}
.r93-ctx .giencoder-dropdown-item {
  display: flex; align-items: center; gap: 8px;
  padding: 5px 8px; border-radius: 4px;
  font-size: var(--font-size-body-3); line-height: calc(22px * var(--ui-fs-ratio));
  color: var(--color-text-1);
  white-space: nowrap; cursor: pointer; user-select: none; outline: none;
}
.r93-ctx .giencoder-dropdown-item:hover { background: var(--color-fill-2); }
.r93-ctx .giencoder-dropdown-item.is-danger { color: var(--color-danger-6); }
.r93-ctx .giencoder-dropdown-divider { height: 1px; margin: 4px 0; background: var(--color-border-2); }
.r93-ctx-ico {
  flex: none; width: 14px; height: 14px; display: inline-flex;
  align-items: center; justify-content: center; color: var(--color-text-1);
}
.r93-ctx-ico svg { display: block; width: 14px; height: 14px; }
.r93-ctx .is-danger .r93-ctx-ico { color: var(--color-danger-6); }
.r93-ctx-label { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; }

/* ===================== 「调用 N 个工具」的层级树（★ r100 ⑧） =====================
   邵先生要求：这个分组**下面是一层套一层**的，可以一级一级点开 / 收起，并且要有**层级连接线**。
   设计稿 `1393:18521 容器 221`（840×404）给出的层级与缩进（board 坐标，相对本块左缘）：
     容器 163 / 容器 220 的折叠头 · 展开头                 left   0
     容器 218（内嵌 Tool call 折叠块，822×200）            left  18
       容器 217（它的代码卡，804×132）                     left  36
     容器 219（4 行汇总清单，305×124 @ top 246）           left  18
   ⇒ **L0 = 0 / L1 = 18 / L2 = 36**。设计稿本身没画连接线（PNG 逐像素扫描该区域只扫到
     卡片底 `#F5F6F7` 与卡片描边 `#ECEEF2`，没有竖线，见 `ev/p100a.js` 读数），
     本轮按邵先生要求补 **一条贯穿整个 L1 组的竖导线 + 每个 L1 子项一枚横向肘节**（= `├─` / `└─`）。 */
.r93-tree { position: relative; margin: 12px 0 0 6px; padding-left: 12px; }
/* L1 竖导线：贯穿「Tool call 块 + 4 行清单」整组 */
.r93-tree::before {
  content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 1px;
  background: var(--color-border-2);
}
.r93-tree > .r93-fold,
.r93-tree > .r93-sumlist > .r93-sumrow { position: relative; }
/* L1 子项左侧的横向肘节（8px），自竖导线伸出；top 11 = 22 高的行 / 折叠头的中线。
   ⚠ `position: absolute` 的伪元素**不算 flex item** ⇒ 不会把 `.r93-fold`（列向 flex）的头挤下去。 */
.r93-tree > .r93-fold::before,
.r93-tree > .r93-sumlist > .r93-sumrow::before {
  content: ''; position: absolute; left: -12px; top: 11px; width: 8px; height: 1px;
  background: var(--color-border-2);
}
/* 4 行汇总清单：本身不再画线（线归 `.r93-tree`），只留「与上一个 L1 子项隔 12」 */
.r93-sumlist { display: flex; flex-direction: column; gap: 12px; margin-top: 12px; }
.r93-sumrow { height: 22px; display: flex; align-items: center; gap: 4px; color: var(--color-text-3); }
.r93-sumrow .r93-dot4 { margin: 0 4px; }

/* ===================== 任务产物 ===================== */
.r93-arts { width: 100%; }
.r93-artdiv { display: flex; align-items: center; gap: 16px; }
.r93-artdiv .r93-nline { flex: 1 1 auto; height: 1px; background: var(--color-border-2); }
/* ★ r99 ⑥：标签「任务产物」与内容区同字号（15px）。它挂的是 `.r93-t12l`（12/22），
   设计稿 `fw647:19683` 的 divider 是 DS 组件（`text` 属性走默认档）—— PNG 实测
   「任务产物」4 字墨迹 x558..611 = 54px、字距 14 ⇒ 设计稿是 14px 档，按本轮口径升到 15。 */
.r93-artlabel { flex: none; color: var(--color-text-3); font-size: calc(15px * var(--ui-fs-ratio)); }
.r93-artgrid { margin-top: 16px; display: flex; flex-wrap: wrap; gap: 12px; }
/* ★ r95 ①：产物卡两列**等分撑满**（原来写死 414 = 2×414+12 = 840 恰好，列变宽就右留白）。 */
.r93-artcard {
  width: calc(50% - 6px); height: 56px; box-sizing: border-box; border-radius: 8px;
  background: var(--r93-card); display: flex; align-items: center;
  padding: 0 12px; position: relative; cursor: pointer; text-align: left;
}
.r93-artcard:hover { background: var(--r93-hov-bg); box-shadow: inset 0 0 0 1px var(--r93-hov-bd); }
.r93-artcard:hover .r93-artname { color: var(--color-primary-6); }
.r93-artic { width: 24px; height: 24px; flex: none; }
.r93-artsep { width: 1px; height: 24px; background: var(--color-border-2); margin: 0 11px; flex: none; }
.r93-arttxt { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.r93-artname { color: var(--color-text-1); }
.r93-artmeta { color: var(--color-text-3); }
.r93-artopen { margin-left: auto; flex: none; color: var(--color-text-3); }
.r93-artcard:hover .r93-artopen { color: var(--color-primary-6); }

/* ===================== Token 速率行（设计稿 1393:18599「容器 247」= 256×24） =====================
   ★ r96 ⑤：按设计稿**精确还原**。依据 `raw/design-1393-18748.html` 的节点结构
   ＋ `raw/design-rgb.png` 逐像素实测（x 均为**行内相对值**；行左 = 设计稿 164 = 视口 420）：
     · `1393:18598` 容器 246（56×24 @0）= 2 个 24×24 `icon-wrapper`（图标 14，**gap 8**）
          → 图标1 视觉 x 6..18（复制，色 #6B6B6B）· 图标2 视觉 x 40..49（分支，色 #6B6B6B）
     · 第 1 根分隔线 @ x=68 —— 源 SVG 是 `viewBox="0 0 2 14"` ⇒ **1×14 竖线**，色 #E5E5E5
     · `fw647:19591` Link（142×24 @80，`gap:4`）= 时钟 14×14 + 「Token 速率：256/s」
          （**14px / line-height 24 / #868686**）
     · 第 2 根分隔线 @ x=234
     · 省略号：三点视觉 x 240..249（色 #868686）⇒ 24×24 盒落在 x ≈ 231.5（与第 2 根线重叠）
   ⚠ 旧实现两处硬错（本轮修正）：① 把「容器 246 的 56 宽」误当成**线宽** ⇒ 画成 56×1 的横线；
   ② `gap:16`，而设计稿各段间距是 **12**（56→68→80→222→234）。 */
.r93-rateline { display: flex; align-items: center; gap: 12px; }
.r93-rgrp { display: inline-flex; align-items: center; gap: 8px; flex: none; }
.r93-rbtn {
  display: inline-flex; align-items: center; justify-content: center; flex: none;
  width: 24px; height: 24px; padding: 0; border: 0; background: none; border-radius: 4px;
  color: var(--r93-ioc2); cursor: pointer;
}
.r93-rbtn > svg { width: 14px; height: 14px; display: block; }
.r93-rbtn:hover { background: var(--color-fill-2); }
.r93-rline { flex: none; width: 1px; height: 14px; background: var(--color-border-2); position: relative; z-index: 1; }
.r93-rrate { display: inline-flex; align-items: center; gap: 4px; flex: none; color: var(--color-text-3); }
/* ★ r99 ③：「⋯」按钮与第 2 根竖线贴在一起。逐像素对照（设计稿 `1393:18599` 容器 247，
   x 为行内相对值，PNG 已按 board→png 偏移 +1 换算）：
     设计稿：第 2 根线 @**234**，⋯ 盒（24 宽）231.5..255.5 ⇒ 线右沿 235 到首个点墨迹 239 之间 **4px**
     实机旧值：第 2 根线 @236（各段间距累计多 2），⋯ 盒 233..257 ⇒ 视觉间距只剩 **2px**
   ⇒ 两处修正：① 第 2 根线按设计稿左移 2（`.r93-rrate + .r93-rline`，flex 会把后续项一起左移，
     所以 ② 把 ⋯ 的负 margin 由 −16 收到 −14，让按钮**留在原位**（实测 x233，与设计稿 231.5 只差
     1.5px —— 设计稿那个 24px 盒本来就向右探出容器右沿 0.5px，是右端对齐的写法）。
   线在上层（`.r93-rline` 的 z-index:1）⇒ 按钮 hover 底色不会把线盖掉。 */
.r93-rateline > .r93-rrate + .r93-rline { margin-left: -2px; }
.r93-rateline > .r93-rline + .r93-rbtn { margin-left: -14px; color: var(--color-text-3); }

/* ===================== 底部：状态条 + composer ===================== */
/* ★ r95 ②：底部列与内容列**同口径**（宽 50% / min 860px、水平居中，padding 只留纵向）
   ⇒ 状态条 / agent 卡行 / 对话框外壳三层一起**自适应撑满**，
   右边界与上方内容块、以及 React 渲染的 composer 外壳严格对齐。 */
.r93-bottom { flex: none; width: 50%; min-width: 860px; box-sizing: border-box; margin: 0 auto; padding: 0 0 12px; }
.r93-bottom > * { width: 100%; margin: 0; }
.r93-sb {
  height: 40px; box-sizing: border-box; border-radius: 8px; background: var(--color-bg-2);
  border: 1px solid var(--color-border-2); display: flex; align-items: center;
  gap: 8px; padding: 0 16px;
}
.r93-sbtxt { color: var(--color-text-1); }
.r93-sbmeta { color: var(--color-text-3); }
.r93-sbd { display: flex; align-items: center; gap: 6px; flex: none; }
.r93-sbic { display: inline-flex; align-items: center; color: var(--color-text-3); flex: none; }
.r93-sbchev { margin-left: auto; color: var(--color-text-2); display: inline-flex; }

/* ★ r93 ④：输入卡改为**复用外壳真实 composer** ⇒ 这里不再自绘 `.r93-input`。
   本容器只承载「状态条下方的 agent 卡行」；灰底/描边/圆角全部交给真实 composer 的
   `bg-[var(--color-fill-1)]` 外壳承担，避免出现两层灰壳叠罗汉。 */
.r93-cp { margin-top: 12px; }

/* ★ r93 ④：composer 贴底后，**所有下拉必须向上弹** ——
   真组件的下拉默认 `top: calc(100% + 4px)`（向下），在欢迎态（composer 居中）没问题；
   本页 composer 钉在 main 底部（main 是 `overflow:hidden`）⇒ 向下的弹层会被裁掉
   （实测「默认权限」popup rect y 871..997，main 底 892 ⇒ 只剩 21px 可见）。
   这是**页面级适配层**（只补几何，不动组件本体）：只在本页把锚点翻到上方。 */
html[data-r93-page='conversation'] .giencoder-select-popup {
  top: auto !important; bottom: calc(100% + 4px) !important;
  transform-origin: bottom;
}
html[data-r93-page='conversation'] [aria-label='权限选择'] {
  top: auto !important; bottom: calc(100% + 4px) !important;
}
.r93-agents { display: flex; gap: 6px; }
.r93-agent {
  /* ★ r97 ③：4 张 agent 卡**撑满整行**（与状态条 / 输入卡同左右边界）。
     原 `flex:none` 是按内容宽左对齐 —— 设计稿 PNG 实测该行 4 张卡的外框是
     x 171 | 361 ‖ 369 | 538 ‖ 545 | 742 ‖ 749 | 1004（第 4 张**顶到内容列右缘**）
     ⇒ 设计稿里这一行是**填满**的，不是留白。列宽一变（1920/2560）`flex:none` 就会在
     右端露出几十到几百 px 的空档。改 `1 1 auto` = 按内容宽成比例吃掉剩余空间
     （保住了设计稿「四张不等宽」的比例，而不是平分）。 */
  flex: 1 1 auto; min-width: 0; height: 48px; box-sizing: border-box; border-radius: 6px;
  background: var(--color-bg-2); border: 1px solid var(--color-border-2);
  display: flex; align-items: center; gap: 8px; padding: 0 8px; cursor: pointer;
  text-align: left;
}
/* ★ r100 ⑤：邵先生要求「hover 时加个**浅灰底色**即可，边框颜色不要变」⇒ 撤掉 r93 的
   `border-color: --color-border-3`，改成 `background: --color-fill-2`（gray-2 = #F2F2F2）。
   ⚠ 选中态 `.is-on` 的紫色描边（`--r93-a1-bd`）**不受影响** —— 那是状态色、不是 hover 反馈。 */
.r93-agent:hover { background: var(--color-fill-2); }
.r93-agent.is-on { border-color: var(--r93-a1-bd); }
.r93-agentic { width: 32px; height: 32px; border-radius: 4px; display: flex; align-items: center; justify-content: center; flex: none; }
.r93-agentic .r93-iblk { width: 16px; height: 16px; }
.r93-agent1 .r93-agentic { background: var(--r93-a1-bg); color: var(--r93-a1-ic); }
.r93-agent2 .r93-agentic { background: var(--r93-a2-bg); color: var(--r93-a2-ic); }
.r93-agent3 .r93-agentic { background: var(--r93-a3-bg); color: var(--r93-a3-ic); }
.r93-agent4 .r93-agentic { background: var(--r93-a4-bg); color: var(--r93-a4-ic); }
.r93-agenttx { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.r93-agent1 .r93-agname { color: var(--r93-a1-ic); }
.r93-agname { color: var(--color-text-1); }
.r93-agdesc { color: var(--color-text-3); }
.r93-agendi { margin-left: 8px; flex: none; display: inline-flex; }
.r93-agent1 .r93-agendi { color: var(--color-primary-6); }
.r93-agent2 .r93-agendi { color: var(--r93-ok); }
.r93-agent3 .r93-agendi { color: var(--color-text-3); }
.r93-agent4 .r93-agendi { color: var(--color-text-2); }

/* 删（r93 ④）：.r93-input / .r93-ta / .r93-itools / .r93-ictl / .r93-perm /
   .r93-itools-r / .r93-model / .r93-send —— 自绘输入卡整组退场，改由真实 composer 承担。
   对应图标（c1 / c2 / perm / regen / send）已无引用，保留在 ICON_FILES 里不影响产物。 */

/* ===================== 滚动到底部 ===================== */
/* 滚动到底部：设计稿里它浮在内容之上（840 内容列居中），故用 0 高 sticky 壳承载，
   不占额外高度。壳体 bottom = (滚动口底 − 药丸底边) − 32（药丸自高）：
   bottom:44 ⇒ 药丸底边距滚动口底 12px（r93 定稿值，实测 ok）。
   ⚠ r93 ④ 追加留白 12px 后滚动口底 = 状态条顶边，故药丸底边到状态条 = 12px。 */
.r93-tbsticky { position: sticky; bottom: 44px; height: 0; display: flex; justify-content: center; z-index: 3; pointer-events: none; }
.r93-tobottom {
  display: none; align-items: center; gap: 4px; height: 32px; padding: 0 16px;
  /* ★ r97 ②：**胶囊**按钮（不是 8px 圆角矩形）。设计稿 `1393:18683` 是 DS Button
     「次要按钮 / 标准 / 长方形 / 中 / 默认」120×32，PNG 逐像素扫形状：顶行 x 556..653、
     8 行后收到 547、再往下到 546 ⇒ 左缘轨迹与 R=16（= 高/2 全圆角）吻合，R=8 明显不符。
     DS 无「胶囊」半径 token（最大 `--border-radius-xl:12px`）⇒ 用 999px 表达全圆角。 */
  border-radius: 999px;
  background: var(--color-bg-2); border: 1px solid var(--color-border-2);
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.08);
  /* ★ r97 ②：整枚按钮**只有一个前景色**（图标与文案同色）。设计稿 PNG 实测图标笔画
     与文字笔画**都是** (107,107,107) = #6B6B6B（= r96 ⑤ 已建立的 `--r93-ioc2`）。
     原来按钮继承 `--color-text-1`（图标 #1F1F1F）、`<span class="r93-t14">` 自带 text-3
     (#868686) ⇒ 两者深浅不一，故统一到 `--r93-ioc2`。
     ★ r99 ②：本轮再**深一级** ⇒ 改用 `--color-text-2`（色阶 gray-8 = #4E4E4E；原 gray-7 = #6B6B6B）。
       仍是「单一前景色」口径，图标与文案一起换。 */
  color: var(--color-text-2);
  cursor: pointer; pointer-events: auto;
}
/* ★ r99 ② → r100 ③：邵先生本轮要求「hover 时**边框颜色不要变化**，图标和文字颜色**再变为深一级**
   的颜色即可」⇒ 撤掉 `border-color` 那条；前景色由默认的 `--color-text-2`（gray-8 #4E4E4E）
   再深一级到 `--color-text-1`（gray-10 #1F1F1F）。本按钮是「单一前景色」口径 ⇒ 图标与文案一起换。
   底色沿用 r99 的 `--color-fill-1`：邵先生只点了「描边」与「前景色」两条，未要求撤掉底色。 */
.r93-tobottom:hover { background: var(--color-fill-1); color: var(--color-text-1); }
/* 文案随按钮同色（`.r93-t14` 自己有 (0,1,0) 的默认色 ⇒ 用 (0,2,0) 压回去）。 */
.r93-tobottom .r93-t14 { color: inherit; }
.r93-tobottom.is-on { display: inline-flex; }

/* ===================== 轨迹空态 ===================== */
.r93-trace { flex: 1 1 auto; min-height: 0; display: flex; align-items: center; justify-content: center; }
.r93-tracebox { text-align: center; color: var(--color-text-3); }

/* ===================== 文件路径的 hover popover ===================== */
.r93-fpath { position: relative; display: inline-block; }
.r93-fpath > .r93-flink { color: var(--color-primary-6); }
.r93-pop {
  position: absolute; left: 0; bottom: 100%; margin-bottom: 6px; display: none;
  width: 314px; box-sizing: border-box; border-radius: 8px; background: var(--color-bg-2);
  border: 1px solid var(--color-border-2); box-shadow: 0 4px 8px 0 rgba(0,0,0,0.08);
  padding: 4px; gap: 4px; z-index: 5;
}
.r93-fpath:hover .r93-pop, .r93-pop:hover { display: flex; }
.r93-pop a { flex: 1 1 0; text-align: center; padding: 4px 0; border-radius: 4px; color: var(--color-primary-6); }
.r93-pop a:hover { background: var(--color-fill-2); }
"""


# ---------------------------------------------------------------- JS

JS_TMPL = r"""
(function () {
  'use strict';
  /*__ICONS__*/

  var IC = function (n, cls) {
    var s = ICON[n];
    if (!s) return '';
    return cls ? s.replace('<svg', '<svg class="' + cls + '"') : s;
  };
  var E = function (s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  };
  /* 折叠块：折叠头（灰）与展开头（黑 + 点 + 元信息）是设计稿里的两个状态，
     真机上只出现其中一个 —— data-open 切换。 */
  var fold = function (o) {
    /* ★ r99 ⑧：展开头（`.r93-fh`）的 chevron 由 12 改成 **14** —— 与折叠头（`.r93-fc`，
       `.r93-iblk.r93-i14`）的图标槽同宽。原来两态图标槽 12 vs 14 差 2px，点一下标题就横向
       抖 2px（实测展开态标题 tx = 436 = 12+4，设计稿是 18 = 14+4），这就是邵先生说的「跳动」。
       尺寸也有据：设计稿 `direction/down`（`容器 161` 内）是 14×14 盒，PNG 实测 chevron 墨迹
       x167..175 / y401..406 = 9×6；`ICON.cv` 的路径在 12 网格里墨迹 8.1×4.7，渲到 14 网格
       正好是 9.45×5.5 —— 与设计稿吻合。 */
    var head = '<button class="r93-fh r93-bt" type="button">'
      + '<span class="r93-iblk r93-i14 r93-cv">' + (o.chev === 'u' ? IC('cvu') : IC('cv')) + '</span>'
      + '<span class="r93-t14 r93-ft r93-ell">' + E(o.t) + '</span>'
      + (o.meta ? '<i class="r93-dot4"></i><span class="r93-t12l r93-fm r93-ell">' + E(o.meta) + '</span>' : '')
      + '</button>';
    var body = '<div class="r93-fb">' + o.body + '</div>';
    /* ★ r100 ⑦：折叠头（`.r93-fc`）走同一工厂 ⇒ 图标槽与展开头**同为 `.r93-i14`**，
       不再出现「展开态 14 / 折叠态 12」的错位（邵先生：「这个折叠后前面的图标异常」）。
       `ctmeta` 是给内嵌 Tool call 层用的：设计稿 `fw647:18138`（424×22）的折叠头里
       「Tool call」后面**也带**「• str_replace_editor · …」那截元信息。 */
    var col = '<button class="r93-fc r93-bt" type="button">'
      + '<span class="r93-iblk r93-i14 r93-c3">' + IC(o.ic) + '</span>'
      + '<span class="r93-t14 r93-ell">' + E(o.ct || o.t) + '</span>'
      + (o.ctmeta && o.meta ? '<i class="r93-dot4"></i><span class="r93-t12l r93-fm r93-ell">' + E(o.meta) + '</span>' : '')
      + '</button>';
    /* ⚠ `o.mt` 用 `!= null` 判空：`mt:0` 也要真的落成 `--mt:0px`（原来 `o.mt ?` 会把 0 当假值
       ⇒ 内嵌层退化成默认的 16px 上边距）。已有调用全传真值，行为不变。 */
    return '<div class="r93-it r93-fold" data-open="' + (o.open === false ? '0' : '1') + '"'
      + (o.mt != null ? ' style="--mt:' + o.mt + 'px"' : '') + '>' + head + body + col + '</div>';
  };
  var card = function (inner, opt) {
    opt = opt || {};
    var st = [];
    if (opt.w) st.push('width:' + opt.w + 'px');
    if (opt.h) st.push('height:' + opt.h + 'px');
    return '<div class="r93-card' + (opt.edge ? ' r93-card--edge' : '')
      + (opt.full ? ' r93-card--full' : '')
      + (opt.cls ? ' ' + opt.cls : '') + '"'
      + (st.length ? ' style="' + st.join(';') + '"' : '') + '>' + inner + '</div>';
  };
  /* 带内层头的卡片（40px 头 + 1px 分隔线） */
  var codecard = function (head, body, opt) {
    return card('<div class="r93-chead">' + head + '</div>'
      + '<div class="r93-cbody">' + body + '</div>',
      { edge: true, h: (opt || {}).h, w: (opt || {}).w });
  };
  var copybtn = '<span class="r93-cmk"><button class="r93-ib r93-bt" type="button" title="复制" data-r93-copy>'
    + '<span class="r93-iblk r93-i14">' + IC('copy') + '</span></button></span>';

  var TPL = [
    '<div class="r93-pane">',

    /* ---------- ① 用户消息 ---------- */
    '<div class="r93-it" style="--mt:0px"><div class="r93-bub">',
    '<div class="r93-bubi"><span class="r93-pill">/awesome-design-md</span>',
    '<span class="r93-t14 r93-ubt">创建一个任务看板，加到左侧菜单。根据任务状态分三个泳道，未开始，进行中，已完成。</span></div>',
    '<div class="r93-attrow">',
    '<span class="r93-att r93-t14"><span class="r93-iblk r93-i16">' + IC('fmd') + '</span>部门人员名单.xlsx</span>',
    '<span class="r93-att r93-t14"><span class="r93-iblk r93-i16">' + IC('fmd') + '</span>产品初版设计方案.md</span>',
    '</div>',
    '<div class="r93-attrow">',
    '<span class="r93-att r93-t14"><span class="r93-iblk r93-i16">' + IC('fxls') + '</span>vscode-light-modern-color-system.xlsx</span>',
    '</div>',
    '<div class="r93-umeta"><span class="r93-t12">15:26</span>',
    '<button class="r93-ib r93-bt" type="button" title="重新生成"><span class="r93-iblk r93-i14">' + IC('regen') + '</span></button>',
    '<button class="r93-ib r93-bt" type="button" title="复制" data-r93-copy><span class="r93-iblk r93-i14">' + IC('copy') + '</span></button>',
    '</div></div></div>',

    /* ---------- ② 助手头 ---------- */
    '<div class="r93-it" style="--mt:32px"><div class="r93-asst">',
    '<div class="r93-ahd"><span class="r93-iblk r93-i24">' + IC('gienx') + '</span>',
    '<span class="r93-t14b">GienCoder</span></div>',
    '<button class="r93-alink r93-bt r93-t12" type="button">任务完成，耗时28m12s',
    '<span class="r93-iblk r93-i14">' + IC('cv') + '</span></button>',
    '</div></div>',

    /* ---------- ③ 上下文注入 ----------
       设计稿 1393:18483 = 822×150 = padding 12 + [16 + 7 + 16 + 7 + 788×80]；
       末段 5 行 × 行高 16（PNG 实测行中心 447/470/492/508/524/540/556）。 */
    fold({
      ic: 'ctx', t: '上下文注入', meta: 'skill-catalog', mt: 12,
      body: card('<div class="r93-ctxbody">'
        + '<div class="r93-t12s">取代先前的快照</div>'
        + '<div class="r93-t12s">sandbox:policy</div>'
        + '<div class="r93-t12s r93-ctxtext">Current DSH file policy: workspace-write. Any available '
        + 'operation enforced by the DSH file sandbox may modify files under the session workspace: '
        + '&quot;/Users/shaoyuming/Library/Application Support/dsh-desktop/launch-root&quot;. Some platform '
        + 'temporary areas may also be writable.<br>Approval policy: ask. Operations that require approval may '
        + 'ask through the configured answerers; without an available answerer, the request fails closed.</div>'
        + '</div>', { cls: 'r93-card--ctx' })
    }),

    /* ---------- ④ 深度思考 ----------
       设计稿 1393:18487 = 822×200 = padding 24 + 8 行 × 22。
       ★ 字号 **12px**（非 14px）：PNG 实测首行「让我理解用户的需求。这是关于 Table 组件右键菜单的三个改动：」
       宽 342 ÷ 29.4 当量字符 ≈ 11.6px；最长行（第 4 条）仅 737px —— 14px 会折成 9 行把卡撑到 222。
       列表项符号在导出图里渲染为「1. 2. 3.」，故直接用有序列表文本（私有区图标字符无字形）。 */
    fold({
      ic: 'think', t: '深度思考', mt: 16,
      body: card('<div class="r93-t12l">让我理解用户的需求。这是关于 Table 组件右键菜单的三个改动：<br>'
        + '1. 标题&quot;Default 基础表格（带排序 + 行选择）&quot;改为&quot;Default 基础表格（带排序 + 行选择 + 支持右键菜单）&quot;<br>'
        + '2. 右键菜单里的文字默认都应该是黑色的（即之前我选的&quot;继承操作列颜色&quot;方案要改成&quot;标准菜单深色文字&quot;）<br>'
        + '3. 右键菜单不需要键盘快捷选择的那种选中态，可去掉（即去掉 focus trap、↑/↓/Enter 键盘导航相关的选中态，以及 focus 进入首项等）<br>'
        + '我需要先读取相关文件来了解现状，然后精确修改。<br>'
        + '让我先读取 component-table.html 的当前状态，找到相关代码。<br>'
        + '让我先 grep 定位相关部分。<br>需要读取：</div>')
    }),

    /* ---------- ⑤ AI 文本 ---------- */
    '<div class="r93-it" style="--mt:16px"><div class="r93-t14 r93-c1">'
    + '我来深度理解一下你选中的这个项目。先看看目录结构，然后做全面分析。</div></div>',

    /* ---------- ⑥ Bash ---------- */
    fold({
      ic: 'bash', t: 'Bash', meta: 'Inspect harness bin and dsh cli', mt: 16, chev: 'd',
      body: codecard(
        '<span class="r93-dot6" style="background:var(--r93-ok)"></span>'
        + '<span class="r93-t12 r93-cpath">launch-root</span>'
        + '<span class="r93-t12 r93-c1">ls -la &quot;/Applications/DSH Desktop.app/Contents/Resources/app/&quot;</span>'
        + '<span class="r93-cmk"><span class="r93-iblk r93-i14 r93-okc">' + IC('ok') + '</span>'
        + '<button class="r93-ib r93-bt" type="button" title="复制" data-r93-copy><span class="r93-iblk r93-i14">' + IC('copy') + '</span></button></span>',
        '<pre class="r93-pre r93-pre--tight r93-code">total 64\n'
        + 'drwxr-xr-x@   5 shaoyuming  staff    160 Sep  3 06:53 .\n'
        + 'drwxr-xr-x@  18 shaoyuming  staff    576 Sep  3 06:53 ..\n'
        + 'drwxr-xr-x@ 327 shaoyuming  staff  10464 Sep  3 06:53 node_modules\n'
        + 'drwxr-xr-x@   4 shaoyuming  staff    128 Sep  3 06:53 out\n'
        + '-rw-r--r--@   1 shaoyuming  staff  31490 Sep  3 06:53 package.json</pre>', { h: 160 })
    }),

    /* ---------- ⑦ 网页搜索 ---------- */
    fold({
      ic: 'web', t: '网页搜索', meta: '左侧菜单 sidebar page 开发, dsh-desktop client plugin create left menu item docs',
      mt: 16,
      body: card('<div class="r93-wlist">' + [
        'dsh-md-quiz/NOTES.md at main · MrElysium/dsh-md-quiz - Skip to content',
        'DSH Desktop 文档',
        'hello-dsh/README.md at main · pingfanfan/hello-dsh - Skip to content',
        'dsh-desktop/docs/README.md at master · anywhere-labs/dsh-desktop - Skip to content',
        'deepseek-harness/packages/client/ui-sidebar/README.zh.md at master · deepseek-ai/deepseek-harness · GitHub',
        'DSH Desktop',
        'dsh-sidebar-files -',
        'dsh-desktop/dsh-plugin-desktop/README.md at v2.0.2 · anywhere-labs/dsh-desktop - Skip to content'
      ].map(function (s, i) {
        return '<a class="r93-wlink r93-t12c" href="javascript:void 0">' + (i + 1) + '. ' + E(s) + '</a>';
      }).join('') + '</div>')
    }),

    /* ---------- ⑧ 需求采访 ----------
       ★ r99 ⑩：按设计稿子树重排（卡 1393:18500 = 822×208）。设计稿里是**三组问答**：
         `容器 200` 252×48 @(20,20)、`容器 199` 486×48 @(20,80) … 组内两行各 22 高、差 **4**；
         组间 12（20+48 = 68 → 80）；卡内距 **20** ⇒ 20 + 3×48 + 2×12 + 20 = 208 ✓
       旧实现「内距 12 + 8/14 行距」净高凑巧也是 208，但两处都不是设计稿的值 ⇒ 本轮一并对齐。 */
    fold({
      ic: 'quiz', t: '需求采访', meta: '3/3 已回答', mt: 16,
      body: card(
        '<div class="r93-t14">你要把「任务看板」加到哪个左侧菜单？</div>'
        + '<div class="r93-t14 r93-c2" style="margin-top:4px">这个 GienCoder 桌面 GUI 的左侧栏</div>'
        + '<div class="r93-t14" style="margin-top:12px">环境中已装了一个 5 泳道、支持 agent 执行的「任务看板」插件。如何处理？</div>'
        + '<div class="r93-t14 r93-c2" style="margin-top:4px">无视它，我新建一个简单 3 泳道看板</div>'
        + '<div class="r93-t14" style="margin-top:12px">任务数据希望存到哪里？</div>'
        + '<div class="r93-t14 r93-c2" style="margin-top:4px">未回答</div>', { cls: 'r93-card--quiz' })
    }),

    /* ---------- ⑨ 更新任务清单 ----------
       设计稿卡 1393:18503 = 822×220，**没有 40px 卡头**：PNG 实测 1px 分隔线在卡内 y=181
       （不是 40）。结构 = padding-top 16 + 输入区（9 行 × 16 = 144）+ 线 @181 + 输出区（16 @192）。 */
    fold({
      ic: 'todo', t: '更新任务清单', meta: '0/5 已完成', mt: 16,
      body: '<div class="r93-todocard">'
        + '<div class="r93-todoin">'
        + '<span class="r93-t12s r93-c3">输入</span>'
        + '<pre class="r93-pre r93-pre--tight r93-code" style="flex:1 1 auto;min-width:0">{'
        + '\n  &quot;todos&quot;: [\n    {\n      &quot;content&quot;: &quot;Study existing task-board plugin&#39;s mount/sidebar architecture to learn the DSH client-plugin pattern&quot;,\n      &quot;status&quot;: &quot;in_progress&quot;\n    },\n    {\n      &quot;content&quot;: &quot;Design the new 3-lane kanban plugin structure and data model&quot;,\n      &quot;status&quot;: &quot;pending&quot;</pre>'
        + '</div>'
        + '<div class="r93-todoline"></div>'
        + '<div class="r93-todoout">'
        + '<span class="r93-t12s r93-c3">输出</span>'
        + '<span class="r93-t12s r93-c1">Updated todo list: 4 pending, 1 in progress, 0 completed.</span>'
        + '</div>'
        + '</div>'
    }),

    /* ---------- ⑩ 文件写入 ---------- */
    fold({
      ic: 'write', t: '文件写入', meta: 'gienx-taskboard-kanban/package.json', mt: 16,
      body: codecard(
        '<span class="r93-fpath"><span class="r93-t12 r93-cpath r93-flink">'
        + '/Users/shaoyuming/Library/Application Support/dsh-desktop/launch-root/dsh-taskboard-kanban/package.json'
        + '</span><span class="r93-pop"><a href="javascript:void 0">复制链接</a>'
        + '<a href="javascript:void 0">已复制</a><a href="javascript:void 0">打开所在文件夹</a></span></span>'
        + '<span class="r93-cmk"><button class="r93-ib r93-bt" type="button" title="复制" data-r93-copy>'
        + '<span class="r93-iblk r93-i14">' + IC('copy') + '</span></button></span>',
        '<pre class="r93-pre r93-code">{\n  &quot;name&quot;: &quot;dsh-taskboard-kanban&quot;,\n'
        + '  &quot;version&quot;: &quot;0.1.0&quot;,\n… 其余 18 行\n'
        + '      &quot;inject&quot;: []\n    }\n  }\n}\n'
        + '<span class="r93-diffstar">└ +25 -0 · 1 个文件</span></pre>', { h: 244 })
    }),

    /* ---------- ⑪ SKILL ----------
       设计稿卡 1393:18509 = 822×64 = padding 24 + 798×40（2 行 × 20，12px）。 */
    fold({
      ic: 'skill', t: 'SKILL', meta: 'deepwiki', mt: 16,
      body: card('<div class="r93-t12c">Browser automation CLI for AI agents. Use when the user needs to interact '
        + 'with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, '
        + 'extracting data, testing web apps, or automating any browser task. Triggers include requests to &quot;open a web…</div>')
    }),

    /* ---------- ⑫ Tool call ---------- */
    fold({
      ic: 'tool', t: 'Tool call', meta: 'str_replace_editor · src/ui/components/drag-strip/index.tsx', mt: 16,
      body: codecard(
        '<span class="r93-t12 r93-c1">src/ui/components/drag-strip/index.tsx</span>'
        + '<span class="r93-cmk"><button class="r93-ib r93-bt" type="button" title="复制" data-r93-copy>'
        + '<span class="r93-iblk r93-i14">' + IC('copy') + '</span></button></span>',
        '<pre class="r93-pre r93-code">const THICKNESS = 6\nconst THICKNESS = 8\n'
        + '<span class="r93-diffstar">└ +1 -1 · 1 file</span></pre>', { h: 132 })
    }),

    /* ---------- ⑬ 以重试模型请求 ----------
       设计稿卡 1393:18514 = 822×64 = padding 24 + 798×40（2 行 × 20，12px）。 */
    fold({
      ic: 'retry', t: '以重试模型请求 (1/5)', meta: '2s', mt: 16,
      body: card('<div class="r93-t12c">重试延迟：2000ms</div>'
        + '<div class="r93-t12c">失败原因：provider connection reset</div>')
    }),

    /* ---------- ⑭ 调用 5 个工具（★ r100 ⑦⑧ 改成分层可折叠树） ----------
       设计稿 1393:18521：展开层里先是一个**内嵌的 Tool call 折叠块**（容器 218 = 822×200，
       整体再右移 18 ⇒ 它的卡片落在 36 处、宽 804），下方才是 4 行汇总清单（1393:18519）。
       ★ r100 ⑦：内嵌那层原来是**手写的静态头**（`<button class="r93-fh r93-bt">`），chevron 槽
         写死 `.r93-i12`、而且**根本没有折叠头** ⇒ ① 比全页其它折叠头小 2px（邵先生：「这个折叠后
         前面的图标异常」）② 压根折不起来。现改走同一个 `fold()` 工厂：两态都是 `.r93-i14` 槽 + 真开合。
       ★ r100 ⑧：整层再包一层 `.r93-tree`（见 CSS）—— 贯穿 L1 的竖导线 + 每个 L1 子项一枚横向肘节。 */
    fold({
      ic: 'tools', t: '调用 5 个工具', mt: 16,
      body: '<div class="r93-tree">'
        + fold({
        ic: 'tool', t: 'Tool call', ctmeta: true, mt: 0,
        meta: 'str_replace_editor · src/ui/components/drag-strip/index.tsx',
        body: codecard('<span class="r93-t12 r93-c1">src/ui/components/drag-strip/index.tsx</span>'
          + '<span class="r93-cmk"><button class="r93-ib r93-bt" type="button" title="复制" data-r93-copy>'
          + '<span class="r93-iblk r93-i14">' + IC('copy') + '</span></button></span>',
          '<pre class="r93-pre r93-code">const THICKNESS = 6\nconst THICKNESS = 8\n'
          + '<span class="r93-diffstar">└ +1 -1 · 1 file</span></pre>', { h: 132 })
        })
        + '<div class="r93-sumlist">'
        + '<div class="r93-sumrow"><span class="r93-iblk r93-i14">' + IC('skill') + '</span>'
        + '<span class="r93-t14">SKILL</span><i class="r93-dot4"></i><span class="r93-t12l">deepwiki</span></div>'
        + '<div class="r93-sumrow"><span class="r93-iblk r93-i14">' + IC('quiz') + '</span>'
        + '<span class="r93-t14">需求采访</span><i class="r93-dot4"></i><span class="r93-t12l">1/3 已回答</span></div>'
        + '<div class="r93-sumrow"><span class="r93-iblk r93-i14">' + IC('write') + '</span>'
        + '<span class="r93-t14">文件写入</span><i class="r93-dot4"></i>'
        + '<span class="r93-t12l r93-ell">gienx-taskboard-kanban/package.json</span></div>'
        + '<div class="r93-sumrow"><span class="r93-iblk r93-i14">' + IC('todo') + '</span>'
        + '<span class="r93-t14">更新任务清单</span><i class="r93-dot4"></i><span class="r93-t12l">0/5 已完成</span></div>'
        + '</div>'
        + '</div>'
    }),

    /* ---------- ⑮ 压缩上下文 ---------- */
    '<div class="r93-it" style="--mt:24px"><div class="r93-note"><i class="r93-nline"></i>'
    + '<div class="r93-nrow"><span class="r93-iblk r93-i14 r93-c3">' + IC('zip') + '</span>'
    + '<span class="r93-t14 r93-nt">压缩上下文</span><i class="r93-dot6"></i>'
    + '<span class="r93-t12 r93-nm">已压缩 19 条历史记录（约 18,320 tokens）</span></div>'
    + '<i class="r93-nline"></i></div>'
    + '<div class="r93-ndesc r93-t12h">此前对话围绕「会话流渲染管线」展开：定位了 conversation / runtime / renderer 三层包职责，枚举了 15 类 ChatNode kind 与对应行组件</div></div>',

    /* ---------- ⑯ 上下文已压缩 ---------- */
    '<div class="r93-it" style="--mt:24px"><div class="r93-note"><i class="r93-nline"></i>'
    + '<div class="r93-nrow"><span class="r93-iblk r93-i14 r93-okc">' + IC('ok') + '</span>'
    + '<span class="r93-t14 r93-nt">上下文已压缩</span><i class="r93-dot6"></i>'
    + '<span class="r93-t12 r93-nm">已压缩 24 条历史记录（约 31,220 tokens）</span></div>'
    + '<i class="r93-nline"></i></div>'
    + '<div class="r93-ndesc r93-t12h">上下文接近窗口上限，已将前 40 条历史折叠为摘要</div></div>',

    /* ---------- ⑰ 搜索资料 ----------
       设计稿卡 1393:18528 = 822×116 = padding 24 + 92；92 = 4 块 × 20 + 3×4(组内) + 6(组间)。
       标题行整行是蓝色下划线链接（PNG 实测同网页搜索卡 #3770F7）。 */
    fold({
      ic: 'search', t: '搜索资料', meta: 'gienx harness client ui', mt: 24,
      body: card('<div class="r93-srch">'
        + '<div class="r93-srchg">'
        + '<a class="r93-wlink r93-t12c" href="javascript:void 0">1. gienx-harness — GitHub</a>'
        + '<div class="r93-t12c r93-c3">Harness-style client packages: ui-conversation, ui-tool, ui-trajectory…</div>'
        + '</div>'
        + '<div class="r93-srchg">'
        + '<a class="r93-wlink r93-t12c" href="javascript:void 0">2. cordis framework docs</a>'
        + '<div class="r93-t12c r93-c3">Context proxy, plugin registry, service injection</div>'
        + '</div></div>')
    }),

    /* ---------- ⑱ 告警条 ×2 ---------- */
    '<div class="r93-it" style="--mt:24px"><div class="r93-alert"><i class="r93-adot"></i>'
    + '<span class="r93-ahd2"><span class="r93-t14">已达到输出 token 上限</span></span>'
    + '<span class="r93-t14 r93-adesc">回答被截断，已有输出保留在对话中。发送 “继续” 可让模型接着输出。</span></div></div>',
    '<div class="r93-it" style="--mt:16px"><div class="r93-alert"><i class="r93-adot"></i>'
    + '<span class="r93-ahd2"><span class="r93-t14">本轮运行失败</span></span>'
    + '<span class="r93-t14 r93-adesc">上游提供方连接被重置，且重试次数已用尽。</span>'
    + '<span class="r93-t12 r93-atag">TIMEOUT</span></div></div>',

    /* ---------- ⑲ 未知 surface 事件 ---------- */
    fold({
      ic: 'surf', t: '未知 surface 事件', meta: 'workspace/reminder', mt: 16,
      body: card('<pre class="r93-pre r93-code">{ \n'
        + '<span class="r93-clink">&#39;text&#39;: &#39;这是一个未来版本才会识别的 surface 事件。&#39; </span>\n}</pre>')
    }),

    /* ---------- ⑳ 模型已切换 ---------- */
    '<div class="r93-it" style="--mt:24px"><div class="r93-note"><i class="r93-nline"></i>'
    + '<div class="r93-nrow"><span class="r93-iblk r93-i14" style="color:var(--r93-ioc)">' + IC('model') + '</span>'
    + '<span class="r93-t14 r93-nt">模型已切换</span></div><i class="r93-nline"></i></div></div>',

    /* ---------- ㉑ AI 文本 ---------- */
    '<div class="r93-it" style="--mt:16px"><div class="r93-t14 r93-c1">'
    + '很好，目录存在。现在让我来构建完整的原型。鉴于其规模，我将创建一个完整的单文件 HTML 应用，并包含全部 18 个页面/组件。让我系统地完成它。</div></div>',

    /* ---------- ㉒ 改动汇总卡 ---------- */
    '<div class="r93-it" style="--mt:24px"><div class="r93-diff">'
    + '<div class="r93-dhead"><div class="r93-dh1">'
    + '<span class="r93-iblk r93-i14 r93-c1">' + IC('diffh') + '</span>'
    + '<span class="r93-t14 r93-dtitle">已编辑 18 个文件</span>'
    + '<span class="r93-dh2"><span class="r93-t12 r93-plus">+800</span>'
    + '<span class="r93-t12 r93-minus">-125</span></span></div>'
    + '<div class="r93-dacts">'
    + '<button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small r93-dbtn" type="button">'
    + '<span class="r93-iblk r93-i14">' + IC('undo') + '</span>撤销</button>'
    + '<button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small r93-dbtn" type="button">'
    + '<span class="r93-iblk r93-i14">' + IC('review') + '</span>审查</button>'
    + '</div></div>'
    + '<div class="r93-dlist">'
    + [
      ['store.js', '+800', '-125'],
      ['app.js', '+12', '-0'],
      ['app.json', '+12', '-0'],
      ['create-trip.js', '+800', '-125'],
      ['detail.js', '+800', '-125'],
      ['detail-diary.js', '+800', '-125'],
      ['favorites.js', '+800', '-125']
    ].map(function (r) {
      return '<div class="r93-drow" data-r93-file="' + E(r[0]) + '"><span class="r93-t14 r93-dname r93-ell">' + E(r[0]) + '</span>'
        + '<span class="r93-dnum"><span class="r93-t12 r93-plus">' + r[1] + '</span>'
        + '<span class="r93-t12 r93-minus">' + r[2] + '</span></span>'
        + '<button class="r93-dmore r93-bt" type="button" title="更多">'
        + '<span class="r93-iblk r93-i14">' + IC('more') + '</span></button></div>';
    }).join('')
    /* ★ r99 ①：这里原本还有一只 `<i class="r93-dsb">`（照设计稿描出来的静态滚动条 thumb）——
       已随假滚动条一起删除；列表改真实 `overflow-y:auto`（见 `.r93-dlist`）。 */
    + '</div></div></div>',

    /* ---------- ㉓ 任务产物 ----------
       设计稿 1393:18600 = 840×230（标签行 22 + 16 + 3 行 × 56 + 2×12 = 230）。
       ★ Token 速率行在画稿里是**独立容器** 1393:18599（840×24 @ +20），故拆成下一块。 */
    '<div class="r93-it" style="--mt:24px"><div class="r93-arts">'
    + '<div class="r93-artdiv"><i class="r93-nline"></i><span class="r93-artlabel r93-t12l">任务产物</span><i class="r93-nline"></i></div>'
    + '<div class="r93-artgrid">'
    + [['arthtml', 'prd-template.html'], ['arthov', 'spec-template.md', 1], ['artmd', 'user-story-breakdown-template.md'],
       ['artmd', 'user-story-template.md'], ['artall', '查看所有产物 (12)']].map(function (c, i) {
      return '<button class="r93-artcard r93-bt" type="button"><span class="r93-iblk r93-artic">' + IC(c[0]) + '</span>'
        + '<i class="r93-artsep"></i><span class="r93-arttxt">'
        + '<span class="r93-t14m r93-artname r93-ell"' + (c[2] ? ' style="color:var(--color-primary-6)"' : '') + '>' + E(c[1]) + '</span>'
        + (c[0] === 'artall' ? '' : '<span class="r93-t12 r93-artmeta">128KB</span>')
        + '</span><span class="r93-iblk r93-i14 r93-artopen">' + IC('open') + '</span></button>';
    }).join('')
    + '</div></div></div>',

    /* ---------- ㉔ Token 速率行（设计稿 1393:18599「容器 247」= 256×24） ----------
       ★ r96 ⑤ 重组：`[复制][分支]`（24×24 盒 / gap8）· 竖线 · `[时钟] Token 速率：256/s` · 竖线 · `[…]`
       前两枚与末尾「…」都走同一 `.r93-rbtn`（24 盒 + 14 图标居中），保证点击区与设计一致。 */
    '<div class="r93-it" style="--mt:20px"><div class="r93-rateline">'
    + '<span class="r93-rgrp">'
    + '<button class="r93-rbtn r93-bt" type="button" title="复制">' + IC('copy') + '</button>'
    + '<button class="r93-rbtn r93-bt" type="button" title="分支">' + IC('branch') + '</button>'
    + '</span>'
    + '<i class="r93-rline"></i>'
    + '<span class="r93-rrate"><span class="r93-iblk r93-i14">' + IC('rate') + '</span>'
    + '<span class="r93-t14">Token 速率：256/s</span></span>'
    + '<i class="r93-rline"></i>'
    + '<button class="r93-rbtn r93-bt" type="button" title="更多">' + IC('more') + '</button>'
    + '</div></div>',

    '</div>'
  ].join('');

  var TPL_BOTTOM = [
    '<div class="r93-bottom">',
    '<div class="r93-sb">',
    '<span class="r93-sbic r93-iblk r93-i14">' + IC('sync') + '</span>',
    '<span class="r93-t14 r93-sbtxt">执行第 2/5 个待办</span>',
    '<i class="r93-dot6" style="background:var(--r93-dim)"></i>',
    '<span class="r93-t14 r93-sbtxt">游戏玩法策略构思</span>',
    '<span class="r93-sbd"><span class="r93-t12 r93-plus">+1,256</span><span class="r93-t12 r93-minus">-22</span></span>',
    '<span class="r93-sbchev r93-iblk r93-i14">' + IC('chevu') + '</span>',
    '</div>',
    '<div class="r93-cp">',
    '<div class="r93-agents">',
    '<button class="r93-agent r93-agent1 is-on r93-bt" type="button"><span class="r93-agentic">'
    + '<span class="r93-iblk">' + IC('a1') + '</span></span>'
    + '<span class="r93-agenttx"><span class="r93-t12g r93-agname">游戏策划</span>'
    + '<span class="r93-t12 r93-agdesc r93-ell">研究休闲游戏设计趋势</span></span>'
    + '<span class="r93-agendi r93-iblk r93-i14">' + IC('spin') + '</span></button>',
    '<button class="r93-agent r93-agent2 r93-bt" type="button"><span class="r93-agentic">'
    + '<span class="r93-iblk">' + IC('a2') + '</span></span>'
    + '<span class="r93-agenttx"><span class="r93-t12g r93-agname">项目经理</span>'
    + '<span class="r93-t12 r93-agdesc r93-ell">设计游戏玩法攻略</span></span>'
    + '<span class="r93-agendi r93-iblk r93-i14">' + IC('ok') + '</span></button>',
    '<button class="r93-agent r93-agent3 r93-bt" type="button"><span class="r93-agentic">'
    + '<span class="r93-iblk">' + IC('a3') + '</span></span>'
    + '<span class="r93-agenttx"><span class="r93-t12g r93-agname">软件开发工程师</span>'
    + '<span class="r93-t12 r93-agdesc r93-ell">开发完整的游戏能力</span></span>'
    + '<span class="r93-agendi r93-iblk r93-i14">' + IC('clock') + '</span></button>',
    '<button class="r93-agent r93-agent4 r93-bt" type="button"><span class="r93-agentic">'
    + '<span class="r93-iblk">' + IC('a4') + '</span></span>'
    + '<span class="r93-agenttx"><span class="r93-t12g r93-agname">测试工程师</span>'
    + '<span class="r93-t12 r93-agdesc r93-ell">对整个游戏进行</span></span>'
    + '<span class="r93-agendi r93-iblk r93-i12">' + IC('cv') + '</span></button>',
    '</div>',
    /* ★ r93 ④：自绘输入卡整组已删 —— 输入框改用外壳 React 渲染的真实 composer（见脚本头）。 */
    '</div></div>'
  ].join('');

  var HEAD = [
    '<div class="r93-bar">',
    '<div class="r93-seg giencoder-radio-group giencoder-radio-group-button" role="radiogroup">',
    '<label class="giencoder-radio-button giencoder-radio-button-checked" data-r93-tab="chat">'
    + '<span class="giencoder-radio-button-text">对话</span></label>',
    '<label class="giencoder-radio-button" data-r93-tab="trace">'
    + '<span class="giencoder-radio-button-text">轨迹</span></label>',
    '</div>',
    '<div class="r93-seg-cap"><span class="r93-t16b r93-capname r93-ell">开发管理系统单文件工作台…</span>'
    + '<span class="r93-captag r93-t12"><span class="r93-iblk r93-i12">' + IC('auto') + '</span>自动化</span>'
    + '<span class="r93-t12 r93-captime">07月02日 15:26</span></div>',
    '<button class="r93-morebtn r93-bt" type="button"><span class="r93-iblk r93-i14">' + IC('more') + '</span></button>',
    '</div>'
  ].join('');

  var TRACE = '<div class="r93-pane r93-trace" hidden><div class="r93-tracebox">'
    + '<div class="r93-t14">暂无轨迹数据</div></div></div>';

  var full = HEAD
    + '<div class="r93-pane" data-r93-pane="chat">'
    + '<div class="r93-scroll"><div class="r93-wrap">' + TPL + '</div>'
    + '<div class="r93-tbsticky"><button class="r93-tobottom r93-bt" type="button">'
    + '<span class="r93-iblk r93-i12">' + IC('cv') + '</span>'
    + '<span class="r93-t14">滚动到底部</span></button></div></div>'
    + TPL_BOTTOM + '</div>'
    + TRACE;

  /* ---------------------------------------------------------------- 挂载 */
  function mainEl() { return document.querySelector('main'); }
  function innerEl() {
    var m = mainEl();
    if (!m) return null;
    return m.querySelector(':scope > div') || m;
  }

  function wire(host) {
    /* 页签 */
    [].forEach.call(host.querySelectorAll('[data-r93-tab]'), function (lb) {
      lb.addEventListener('click', function () {
        var id = lb.getAttribute('data-r93-tab');
        [].forEach.call(host.querySelectorAll('[data-r93-tab]'), function (o) {
          o.classList.toggle('giencoder-radio-button-checked', o === lb);
        });
        host.querySelector('[data-r93-pane="chat"]').hidden = (id !== 'chat');
        host.querySelector('.r93-trace').hidden = (id !== 'trace');
      });
    });
    /* 折叠块 */
    host.addEventListener('click', function (ev) {
      var t = ev.target;
      if (!t || !t.closest) return;
      var b = t.closest('.r93-fh, .r93-fc');
      if (!b) return;
      var f = b.closest('.r93-fold');
      /* ★ r100 ⑦：内嵌的 Tool call 层**现在也是** `.r93-fold` ⇒ 这里命中的是**最近**的那一层，
         本来就该一层一层点开 / 收起；若某个静态头没有 `.r93-fold` 祖先则照旧放行。 */
      if (!f) return;
      f.setAttribute('data-open', f.getAttribute('data-open') === '1' ? '0' : '1');
    });
    /* 滚动到底部 */
    var sc = host.querySelector('.r93-scroll');
    var tb = host.querySelector('.r93-tobottom');
    var sync = function () {
      var far = sc.scrollHeight - sc.scrollTop - sc.clientHeight > 120;
      tb.classList.toggle('is-on', far);
    };
    sc.addEventListener('scroll', sync);
    tb.addEventListener('click', function () { sc.scrollTo({ top: sc.scrollHeight, behavior: 'smooth' }); });
    setTimeout(sync, 60);

    /* ★ r99 ⑨：复制按钮「点击 → 换绿勾」。所有复制按钮在模板里都带 `data-r93-copy`
       （6 处：用户消息 1 · Bash 1 · 文件写入 1 · tool-call 卡 2 · codecard 预算好 1），
       显隐/还原全部走**事件委托**，React 重渲染换掉节点也不会丢监听。
       真去写剪贴板：优先复制同一张卡里的代码块 / 路径文本，拿不到就跳过（prototype 够用），
       写失败（file:// 下 clipboard API 可能被拒）也不影响绿勾反馈。 */
    host.addEventListener('click', function (ev) {
      var t = ev.target;
      if (!t || !t.closest) return;
      var btn = t.closest('[data-r93-copy]');
      if (!btn) return;
      var ic = btn.querySelector('.r93-iblk');
      if (!ic) return;
      if (btn.getAttribute('data-r93-copied') === '1') return;
      var src = '';
      var box = btn.closest('.r93-card, .r93-chead, .r93-bub');
      var pre = box && box.querySelector('.r93-pre');
      if (pre) src = pre.textContent || '';
      else {
        var nm = box && box.querySelector('.r93-cpath, .r93-dname');
        if (nm) src = nm.textContent || '';
      }
      if (src) {
        try {
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(src).catch(function () {});
          }
        } catch (e) { /* 忽略：反馈照旧 */ }
      }
      btn.setAttribute('data-r93-copied', '1');
      btn.classList.add('is-copied');
      ic.innerHTML = IC('ok');
      clearTimeout(btn._r93t);
      btn._r93t = setTimeout(function () {
        btn.removeAttribute('data-r93-copied');
        btn.classList.remove('is-copied');
        ic.innerHTML = IC('copy');
      }, 1600);
    });

    /* ★ r99 ⑦：改动汇总卡的文件行 —— 整行右键 + 右侧「⋯」左键，弹出**同一个**菜单。
       参数与范式照搬本仓 `pages/task-detail.html` 的右键菜单（`.td-ctx`）：面板
       182/内距 6/项 2/圆角 8/`--shadow3-down`，项 = 14px 图标 + 13px 文字 + hover fill-2。
       键盘那套（↑/↓/Enter/focus trap）**刻意不做** —— 与邵先生此前对 Table 右键菜单的
       要求一致（不要键盘快捷选择态）。关闭途径：点外面 / Esc / 滚动 / 改窗口尺寸 / 换行再开。 */
    var ctx = null, ctxRow = null;
    var CTX_ITEMS = [
      { id: 'open', label: '查看文件', cls: '', ic: 'open' },
      { id: 'diff', label: '查看改动', cls: '', ic: 'diffh' },
      { id: 'path', label: '复制文件路径', cls: '', ic: 'copy' },
      { divider: true },
      { id: 'revert', label: '撤销此文件改动', cls: 'is-danger', ic: 'undo' }
    ];
    var buildCtx = function () {
      var box = document.createElement('div');
      box.className = 'giencoder-dropdown-popup r93-ctx';
      box.setAttribute('role', 'menu');
      CTX_ITEMS.forEach(function (it) {
        if (it.divider) {
          var d = document.createElement('div');
          d.className = 'giencoder-dropdown-divider';
          d.setAttribute('role', 'separator');
          box.appendChild(d);
          return;
        }
        var row = document.createElement('div');
        row.className = 'giencoder-dropdown-item' + (it.cls ? ' ' + it.cls : '');
        row.setAttribute('role', 'menuitem');
        row.setAttribute('tabindex', '-1');
        row.setAttribute('data-r93-ctx', it.id);
        row.innerHTML = '<span class="r93-ctx-ico" aria-hidden="true">' + IC(it.ic) + '</span>'
          + '<span class="r93-ctx-label"></span>';
        row.querySelector('.r93-ctx-label').textContent = it.label;
        box.appendChild(row);
      });
      document.body.appendChild(box);
      /* 菜单内部的按下不冒到「点外面关闭」那条判断里 */
      box.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
      box.addEventListener('click', function (e) {
        var r = e.target && e.target.closest ? e.target.closest('[data-r93-ctx]') : null;
        if (!r) return;
        if (r.getAttribute('data-r93-ctx') === 'path' && ctxRow) {
          var nm = ctxRow.querySelector('.r93-dname');
          var path = nm ? nm.textContent : '';
          try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
              navigator.clipboard.writeText(path).catch(function () {});
            }
          } catch (err) { /* 忽略 */ }
        }
        closeCtx();
      });
      return box;
    };
    var closeCtx = function () {
      if (!ctx) return;
      ctx.classList.remove('giencoder-popup-open');
      ctx.setAttribute('aria-hidden', 'true');
      ctxRow = null;
    };
    var openCtx = function (row, x, y) {
      if (!ctx) ctx = buildCtx();
      ctxRow = row;
      ctx.style.visibility = 'hidden';
      ctx.style.display = 'flex';
      ctx.style.left = '0px';
      ctx.style.top = '0px';
      var w = ctx.offsetWidth, h = ctx.offsetHeight;
      var left = Math.min(x, window.innerWidth - w - 8);
      var top = Math.min(y, window.innerHeight - h - 8);
      ctx.style.left = Math.max(8, left) + 'px';
      ctx.style.top = Math.max(8, top) + 'px';
      ctx.style.visibility = '';
      ctx.setAttribute('aria-hidden', 'false');
      ctx.classList.add('giencoder-popup-open');
    };
    host.addEventListener('contextmenu', function (ev) {
      var t = ev.target;
      if (!t || !t.closest) return;
      var row = t.closest('.r93-drow');
      if (!row) return;
      ev.preventDefault();
      openCtx(row, ev.clientX, ev.clientY);
    });
    /* ★ r99 ⑦ + r100 ④：点右侧「⋯」**或点行内任意位置**，出的都是同一张菜单。
       行是整块可点区（`.r93-drow{cursor:pointer}`），「⋯」只是其中一枚更明确的触发器 ⇒
       点 ⋯ 时菜单贴按钮左下角、点行内其余位置时贴整行左下角（两者都是 DS dropdown 的
       「向下弹、左缘对齐触发器」口径；右/下溢出时 `openCtx` 会自己夹回来）。 */
    host.addEventListener('click', function (ev) {
      var t = ev.target;
      if (!t || !t.closest) return;
      var row = t.closest('.r93-drow');
      if (!row) return;
      var btn = t.closest('.r93-dmore');
      if (btn) {
        var r = btn.getBoundingClientRect();
        openCtx(row, r.left, r.bottom + 4);
      } else {
        var rr = row.getBoundingClientRect();
        openCtx(row, rr.left + 11, rr.bottom + 4);
      }
    });
    document.addEventListener('pointerdown', function (ev) {
      if (!ctx || !ctx.classList.contains('giencoder-popup-open')) return;
      if (ctx.contains(ev.target)) return;
      /* 触发器自己（⋯ 按钮 / 行本身）不关 —— 否则同一次点击会「先关后开」闪一下：
         pointerdown 先到、click 后到，click 那边还会把菜单重新打开。 */
      var t = ev.target;
      if (t && t.closest && t.closest('.r93-dmore, .r93-drow')) return;
      closeCtx();
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') closeCtx();
    });
    window.addEventListener('resize', closeCtx);
    window.addEventListener('blur', closeCtx);
    document.addEventListener('scroll', closeCtx, true);
  }

  /* 本页 = 会话详情独立页，宿主**常驻**（不存在「打开/关闭」两种态）。
     React 重渲染可能把宿主冲掉 ⇒ MutationObserver 补回。 */
  function mount() {
    var inner = innerEl();
    if (!inner) return false;
    if (!inner.querySelector('.r93-conv-host')) {
      var h = document.createElement('div');
      h.className = 'r93-conv-host';
      h.innerHTML = full;
      inner.appendChild(h);
      wire(h);
    }
    return true;
  }

  /* aside 里点别的会话：内容只有这一份 ⇒ 只把详情滚回顶部（不跳转、不重载）。
     分组标题（rounded-md + py-0）与导航项一律放行，交给外壳自己处理。 */
  document.addEventListener('click', function (ev) {
    var t = ev.target;
    if (!t || !t.closest) return;
    var b = t.closest('aside button');
    if (!b) return;
    var cl = b.classList;
    if (cl.contains('min-w-0') && cl.contains('flex-1')) {
      var sc = document.querySelector('.r93-conv-host .r93-scroll');
      if (sc) sc.scrollTo({ top: 0 });
    }
  }, true);

  var mo = new MutationObserver(function () { mount(); });
  document.addEventListener('DOMContentLoaded', function () {
    if (!mount()) { setTimeout(mount, 800); }
    var inner = innerEl();
    if (inner) mo.observe(inner, { childList: true });
  });
  setTimeout(function () {
    mount();
    var inner = innerEl();
    if (inner) mo.observe(inner, { childList: true });
  }, 1500);
})();
"""

# ---------------------------------------------------------------- base 页的跳转脚本

NAV_JS_TMPL = r"""
/* r93 ④ · 会话详情已独立成页（pages/conversation.html）
   —— 基础工作台只需要把「点 aside 里的会话任务标题」接到那一页去。
   背景：aside 是外壳 React 渲染的，拿不到它的 onClick，只能在捕获阶段识别（先例 r86/r88）。 */
(function () {
  'use strict';
  document.addEventListener('click', function (ev) {
    var t = ev.target;
    if (!t || !t.closest) return;
    var b = t.closest('aside button');
    if (!b) return;
    var cl = b.classList;
    /* 会话项 = `min-w-0 flex-1` 的那 13 个（实测）；分组标题 = `rounded-md py-0` 的那 4 个，
       点它是折叠/展开，不能跳页；其余（新会话 / 数字分身 / 自动化 / 技能 / 设置）交给外壳。 */
    if (!(cl.contains('min-w-0') && cl.contains('flex-1'))) return;
    location.href = 'conversation.html';
  }, true);
})();
"""


def build_js():
    js = JS_TMPL.replace('/*__ICONS__*/', build_icon_js())
    return '<script id="%s">\n%s\n</script>\n' % (JS_ID, js.strip())


def build_css():
    return '<style id="%s">\n%s\n</style>\n' % (CSS_ID, CSS.strip())


# ---------------------------------------------------------------- 主流程

RE_STYLE = re.compile(r'<style id="%s">.*?</style>\n?' % CSS_ID, re.S)
RE_JS = re.compile(r'<script id="%s">.*?</script>\n?' % JS_ID, re.S)
RE_NAV = re.compile(r'<!-- r93-nav -->\n?<script id="%s">.*?</script>\n?<!-- /r93-nav -->\n?' % NAV_ID, re.S)


def build_nav_js():
    return ('<!-- r93-nav -->\n<script id="%s">\n%s\n</script>\n<!-- /r93-nav -->\n'
            % (NAV_ID, NAV_JS_TMPL.strip()))


def route_patch(text):
    """给 `SHELL-NAV-FIX v5` 的 ROUTE 表加 /conversation（幂等）。"""
    if '/conversation' in text:
        return text, 0
    if text.count(ROUTE_OLD) != 1:
        sys.exit('!! 路由表锚点命中 %d 次（应 1 次）' % text.count(ROUTE_OLD))
    return text.replace(ROUTE_OLD, ROUTE_NEW), 1


def route_unpatch(text):
    if '/conversation' not in text:
        return text, 0
    if text.count(ROUTE_NEW) != 1:
        sys.exit('!! 路由表新锚点命中 %d 次（应 1 次）' % text.count(ROUTE_NEW))
    return text.replace(ROUTE_NEW, ROUTE_OLD), 1


def inject_tail(text, blob):
    idx = text.rfind('</body>')
    if idx < 0:
        sys.exit('!! 找不到 </body>')
    if len(text) - idx > 120:
        sys.exit('!! 最后一处 </body> 距文件尾 %d 字符（不像收尾标签）' % (len(text) - idx))
    return text[:idx] + blob + text[idx:]


def load_fs88b():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'fs88b', os.path.join(REPO, 'mg-work', 'r88', 'apply88b-fontsize.py'))
    fs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fs)
    return fs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revert', action='store_true')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    forward = not a.revert
    fs = load_fs88b()
    changes = []

    # ---- 1) base.html：先摘净底（本代两块 + nav 块），净底是两页的唯一来源 ----
    src = io.open(PAGE, encoding='utf-8').read()
    net = src
    for rx in (RE_STYLE, RE_JS, RE_NAV):
        net = rx.sub('', net)
    if forward:
        for tok in (CSS_ID, JS_ID, NAV_ID, ATTR_HOST):
            if tok in net:
                sys.exit('!! 摘块后基线里仍残留本轮标记 %r' % tok)

    n_style0, n_end0 = net.count('<style'), net.count('</style>')
    n_scr0, n_es0 = net.count('<script'), net.count('</script>')

    if forward:
        # ---- 2) 路由表：net（→ base + conversation 共用）与其余 8 页各插一条 ----
        net, n = route_patch(net)
        if n:
            changes.append('base 净底 ROUTE 表 +1 条')
        for path in sorted(glob.glob(os.path.join(REPO, 'pages', '*.html'))):
            if os.path.abspath(path) == PAGE:
                continue
            t = io.open(path, encoding='utf-8').read()
            t2, n = route_patch(t)
            if n:
                if not a.dry:
                    io.open(path, 'w', encoding='utf-8').write(t2)
                changes.append('%s ROUTE 表 +1 条' % os.path.basename(path))

        # ---- 2b) ★ r100 ① 全站更名 GienX → GienCoder（可见文案） ----
        #      conversation.html 的两处（助手名 + 用户回话）已在模板里改掉；
        #      本仓**剩下的最后一处可见文案**在 task-detail.html 的「来源需求」链接里
        #      （示例标题「GienX端到端初始化：用户输入业务流程描述…」）。
        #      ⚠ 只替换带 `>` 前缀的那一处 ⇒ 不动该文件里两条历史注释中的同名串；幂等。
        td_path = os.path.join(REPO, 'pages', 'task-detail.html')
        if os.path.exists(td_path):
            tt = io.open(td_path, encoding='utf-8').read()
            tt2 = tt.replace('>GienX端到端初始化', '>GienCoder端到端初始化')
            if tt2 != tt:
                if not a.dry:
                    io.open(td_path, 'w', encoding='utf-8').write(tt2)
                changes.append('task-detail.html 文案 GienX → GienCoder')

        # ---- 3) base.html = 净底 + 跳转脚本 ----
        out_base = inject_tail(net, build_nav_js())
        if out_base.count('<script') != n_scr0 + 1 or out_base.count('</script>') != n_es0 + 1:
            sys.exit('!! base.html <script> 计数异常')
        out_base = fs.converge(out_base)

        # ---- 4) conversation.html = 净底（带 data-r93-page） + 详情块 ----
        if net.count(HTML_OLD) != 1:
            sys.exit('!! <html> 锚点命中 %d 次（应 1 次）' % net.count(HTML_OLD))
        conv = net.replace(HTML_OLD, HTML_NEW)
        if conv.count(TITLE_OLD) != 1:
            sys.exit('!! <title> 锚点命中 %d 次（应 1 次）' % conv.count(TITLE_OLD))
        conv = conv.replace(TITLE_OLD, TITLE_NEW)
        if conv.count('<style') != n_style0 or conv.count('</style>') != n_end0:
            sys.exit('!! conversation.html <style> 计数异常')
        conv = inject_tail(conv, build_css() + build_js())
        if conv.count('<style') != n_style0 + 1 or conv.count('</style>') != n_end0 + 1:
            sys.exit('!! conversation.html <style> 计数异常')
        if conv.count('<script') != n_scr0 + 1 or conv.count('</script>') != n_es0 + 1:
            sys.exit('!! conversation.html <script> 计数异常')
        conv = fs.converge(conv)
    else:
        # ---- 回滚 ----
        net, n = route_unpatch(net)
        if n:
            changes.append('base 净底 ROUTE 表 -1 条')
        for path in sorted(glob.glob(os.path.join(REPO, 'pages', '*.html'))):
            if os.path.abspath(path) == PAGE or os.path.abspath(path) == PAGE_CONV:
                continue
            t = io.open(path, encoding='utf-8').read()
            t2, n = route_unpatch(t)
            if n:
                if not a.dry:
                    io.open(path, 'w', encoding='utf-8').write(t2)
                changes.append('%s ROUTE 表 -1 条' % os.path.basename(path))
        # ---- ★ r100 ① 的逆操作（与上面 2b 对称） ----
        td_path = os.path.join(REPO, 'pages', 'task-detail.html')
        if os.path.exists(td_path):
            tt = io.open(td_path, encoding='utf-8').read()
            tt2 = tt.replace('>GienCoder端到端初始化', '>GienX端到端初始化')
            if tt2 != tt:
                if not a.dry:
                    io.open(td_path, 'w', encoding='utf-8').write(tt2)
                changes.append('task-detail.html 文案 GienCoder → GienX')
        out_base = net.replace('\n\n\n', '\n\n')
        conv = None

    tag = '应用' if forward else '回滚'
    for label, path, new in (('base.html', PAGE, out_base), ('conversation.html', PAGE_CONV, conv)):
        if new is None:
            if os.path.exists(path) and not a.dry:
                os.remove(path)
                changes.append('%s 已删除' % label)
            continue
        old = io.open(path, encoding='utf-8').read() if os.path.exists(path) else ''
        if old == new:
            print('   %-20s 已是目标态（无改动）' % label)
            continue
        if a.dry:
            print('   %-20s %d → %d (%+d)  %s（--dry 未写盘）' % (label, len(old), len(new), len(new) - len(old), tag))
            continue
        io.open(path, 'w', encoding='utf-8').write(new)
        print('   %-20s %d → %d (%+d)  %s' % (label, len(old), len(new), len(new) - len(old), tag))

    for c in changes:
        print('   · %s' % c)


if __name__ == '__main__':
    main()


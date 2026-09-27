# -*- coding: utf-8 -*-
"""构建 pages/task-detail.html：复用 kanban.html 的外壳与 DS，页面内容按设计稿重建。
设计依据：
  详情页画板 622:13950（1440x1080, bg #E5EDF5）
  左栏 1343:18534（936x1024）
  右栏 1343:18535（480x1024）
  折叠态 1343:18532（48x844, 竖排「展开 AI 会话」#57626D/14px/500/lh18）
"""
import base64
import io
import json
import os
import sys

SRC = "pages/kanban.html"
DST = "pages/task-detail.html"

s = io.open(SRC, encoding="utf-8").read()

# ---- 骨架切分（偏移来自实测） ----
HEAD_END = s.find("</head>")                 # 327967
CSS_START = 335412                            # 页面 CSS <style>
JS_START = 381834                             # 页面 JS <script>
BODY_TAIL = 516461                            # 主题同步 script 起

head = s[:HEAD_END]
mid = s[HEAD_END:CSS_START]                   # </head><body> + SKILL_DATA
tail_from = s[BODY_TAIL:]                     # 主题同步 + 看板切换 + </body></html>

head = head.replace("<title>任务看板 · 研发工作台</title>",
                    "<title>任务详情 · 研发工作台</title>", 1)

# ============================== CSS ==============================
CSS = r"""<style>
      /* ===== 任务详情页 =====
         设计稿：画板 622:13950 (1440x1080, bg #E5EDF5) / 左栏 1343:18534 (936x1024)
                 右栏 1343:18535 (480x1024) / 折叠态 1343:18532 (48x844) */
      :root {
        --td-bar: 48px;
        --td-gap: 8px;               /* 两栏间隙固定 8px（第22轮）；拖动热区由 ::before 外扩 */
        --td-side-min: 266px;        /* 信息列最小宽度（第26轮第1项：280 → 266，比例减少 5%） */
        --td-right-w: 480px;         /* 右栏默认宽（设计稿实测） */
        --td-right-min: 100px;       /* 拖到此值以下，松手即自动折叠（第24轮：原 320） */
        --td-left-min: 480px;        /* 左栏保底宽（★ 第32轮第4项：320 → 480，与右栏默认宽同值；与 JS LEFT_MIN 一致） */
        --td-collapsed-w: 48px;      /* 折叠条宽（设计稿实测） */
        --td-card: var(--color-fill-1);        /* #F7F7F7 卡片底 */
        --td-line: var(--color-fill-2);        /* #F2F2F2 分隔线 */
        --td-ink-2: #57626D;                   /* 折叠态文字（设计稿实测） */
        --td-surround: #E5EDF5;                /* 页面底（设计稿实测） */
        --td-appbar: #DAE3ED;                  /* 顶栏页签轨道底（shell dev 态实测，同 kanban 的 --kb-appbar） */
        --td-bubble: #E5EDFE;                  /* 用户气泡（设计稿实测） */
        --td-meta: var(--color-text-3);
        --td-strong: var(--color-text-1);
        /* 结构发丝线（顶栏底 / 标题区底 / 信息列左分隔）：设计稿 2x 逐像素实测 #EBECED，
           它介于 gray-2(#F2F2F2) 与 gray-3(#E5E5E5) 之间、不在 DS 灰阶上；
           这里取 DS 的「结构发丝线」语义 token --color-border-1，
           同时满足第 24 轮第 2 项「比原 gray-3 浅一级」的要求。 */
        --td-hairline: var(--color-border-1);
        /* 容器边缘柔和投影：设计稿容器**没有描边**，边缘是一层向下的柔和投影。
           由 2x 截图多行平均反推：左右 Δ7 / 下 Δ14 / 上 Δ2（相对 #E5EDF5），
           衰减 2~3px、纵向偏移 1px → 拟合 0 1px 3px rgba(0,0,0,.06)。 */
        --td-panel-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
        /* ★ 第 28 轮第 6 项：卡片文件类型图标色。
           设计稿 622:13950 逐像素实测（2x 图色频统计）：
             灰色描边文档 #6B6B6B（DS 灰阶里没有这一级：gray-4=#6B6B6B 反向映射上是
             --color-border-3，语义不符；base.html 的技能图标也用同一个 #6B6B6B）
             .html 的「地球」#327FCB / .md 徽标主体 #167AB8 / 徽标折角 #4196D6
           三者均为文件类型品牌色，DS 无对应 token → 按「非 token 色处理约定」字面写进适配层变量。 */
        --td-ico-gray: #6B6B6B;
        --td-ico-web: #327FCB;
        --td-ico-md: #167AB8;
        --td-ico-md-fold: #4196D6;
        --td-ico-skill: #7766FD;               /* 技能面板 Goal 行（base.html 实测 fill #7766FD） */
        /* 设计稿 6px 圆角档（附件小卡 / 转派浮窗全体系）：
           设计稿圆角剖面实测 r≈6（dy=0.5 内缩 3.5 / dy=2.5 内缩 1.0）；
           第 31 轮转派浮窗用「覆盖率 0.5 亚像素交点法」复测，搜索框 5.69 / 选中行 5.66 /
           按钮 5.69 / 面板 ≈5.5~6 → 全体系同为 6。DS 圆角档位只有 0/2/4/8/12/50%，
           6 不在其中 → 适配层变量。 */
        --td-radius-card: 6px;
        /* ★ 第 29 轮第 2 项：AI 对话框全屏后「内容区」最大宽度。860 不是新数值 ——
           pages/base.html 的基础工作台 composer 内容宽就是 860px（见其 r12 注释），此处沿用同一读数。 */
        --td-fs-content: 860px;
        /* ★ 第 31 轮：转派浮窗选中行着色（设计稿 1345:18366 逐像素实测，DevMode 直出，
           与 pages/*.html 既有 --td-* 非 token 色处理约定一致）。 */
        --td-dp-on-bg: #ECF2FF;      /* 选中行底（实测） */
        --td-dp-on-line: #D3E2FF;    /* 选中行描边（实测） */
        /* ★ 以下 token 由构建期从 giencoder-design-system/colors_and_type.css 抽取，
             请勿在此手改 —— 改 token 请改 DS 源文件后重跑本脚本。 */
__DS_PICKER_TOKENS__
      }
      /* 注入口：撑满 main 的确定高度（main 为 844 高）
         ⚠️ 这里必须 overflow:visible —— 两栏的白卡片是「贴边」的（左栏左缘 = main 左缘 = x8，
         右栏右缘 = main 右缘 = x1432），容器投影会落在 root 之外；
         若 root / main 任一保持 overflow:hidden，投影会被整圈裁掉（第 24 轮实测 Δ=0）。
         已实测放开后不产生任何滚动条（docScrollWidth 1440 = clientWidth 1440，bodyH = winH）。 */
      .td-wrap { height: 100%; overflow: visible; }
      .td-root {
        position: relative; width: 100%; height: 100%; min-height: 0;
        display: flex; background: var(--td-surround); overflow: visible;
      }
      /* -------------------- 左栏 -------------------- */
      /* 容器边框（第 24 轮第 1 项）：设计稿里白底大容器（矩形 329）**没有描边**，
         边缘是一圈比底色更暗的柔和投影（实测 Δ 左/右 7、下 14、上 2）。
         原来那圈 1px #E5E5E5 硬边框正是「颜色不对」的根源：它比底色 #E5EDF5 更亮、
         又比容器白底更暗，形成一圈发灰的框。改为投影后边缘恢复成设计稿的「干净白卡片」。 */
      .td-left {
        flex: 1 1 auto; min-width: var(--td-left-min); box-sizing: border-box;
        display: flex; flex-direction: column; overflow: hidden;
        background: var(--color-bg-1); border-radius: 8px;
        box-shadow: var(--td-panel-shadow);
      }
      .td-bar {
        height: var(--td-bar); flex: none; box-sizing: border-box;
        display: flex; align-items: center; gap: 8px; padding: 0 20px;
        background: var(--color-bg-1); border-bottom: 1px solid var(--td-hairline);
      }
      /* 顶栏标题：16px / 中粗 500（设计稿 text/text 64×24 = 4 字 × 16px） */
      .td-bar-title { font-size: 16px; font-weight: 500; line-height: 24px; color: var(--td-strong); white-space: nowrap; }
      .td-bar-actions { margin-left: auto; display: flex; align-items: center; gap: 8px; }
      /* 右侧尾部：…「更多」│ [上一个任务][下一个任务]
         （设计稿：直线 48 @left 380 · 容器 71 @left 392，两钮 28×28 间距 4） */
      .td-bar-sep { flex: none; width: 1px; height: 20px; margin: 0 4px; background: var(--color-border-2); }
      .td-bar-nav { flex: none; display: flex; align-items: center; gap: 4px; }
      .td-btn { border-radius: 6px; }                       /* 设计稿 28 高 / radius 6 */
      /* 顶栏按钮宽度对齐设计稿：98(开始任务)/70(转派·协作·编辑) × 28，内边距 20px；
         图标按钮不参与（保持正方） */
      .td-bar-actions .giencoder-btn:not(.giencoder-btn-icon) { padding: 0 20px; }
      /* 适配层：DS Button(secondary + size-small + icon) → 设计稿 28×28 / radius 6 */
      .td-iconbtn { box-sizing: border-box; width: 28px; padding: 0; border-radius: 6px; line-height: 0; }
      .td-back { border-color: transparent; }
      .td-left-body { flex: 1; min-height: 0; display: flex; overflow: hidden; }
      .td-main {
        flex: 1 1 80%; min-width: 0; overflow: auto; padding: 0 0 32px;  /* 主体 : 信息列 = 8 : 2 */
      }
      .td-title {
        margin: 0; box-sizing: border-box; padding: 16px 40px;
        background: var(--color-fill-1);                      /* 浅灰标题区（设计稿 #FAFAFA） */
        border-bottom: 1px solid var(--td-hairline);
        font-size: 18px; font-weight: 600; line-height: 28px; color: var(--td-strong);
      }
      /* 描述区正文（第 25 轮第 1 项）：正文用最深一级墨色 --color-text-1(#1F1F1F)。
         设计稿 2x 实测该区最暗像素恰为 (31,31,31) = text-1，与标题/值同级。 */
      .td-desc { padding: 24px 40px 0; font-size: var(--font-size-body-3); line-height: 24px; color: var(--color-text-1); }
      .td-desc p { margin: 0 0 12px; }
      /* ★ 第 28 轮第 2 项：描述区插入流程示意图。
         尺寸取值依据：描述区可用宽 856（左栏 936 - 左右 padding 40×2）。
         折叠态限高 374，图放在第 1 段之后（该段仅 1 行 24px + 12 间距 = 36），
         所以图高必须 < 338 才能「折叠态也完整可见」→ 取 max-width 620 + 素材 2:1 → 高 310，末端 346 < 374 ✓。
         （不写死 height/width，只约束 max-width，窄窗口下 width:100% 自适应。）
         ★ 第 30 轮第 1 项：配图改用 DS Image 契约（components/image.json）——
           div.giencoder-image > div.giencoder-image-mask-wrapper > img.giencoder-image-img
           + div.giencoder-image-mask（悬停出现「预览」提示），点击打开 .giencoder-image-preview 遮罩。
           组件样式由本脚本在构建期从 giencoder-design-system 两个文件抽取注入（见 CSS 块末尾占位符）；
           这里**只写视图适配层的尺寸**（作用在组件类上，不改组件本体）。 */
      .td-desc .giencoder-image { display: block; margin: 2px 0 16px; }
      .td-desc .giencoder-image-mask-wrapper { width: 100%; max-width: 620px; cursor: zoom-in; }
      /* 描述区列表（第 24 轮第 3 项）：设计稿每行前面是一个小圆点。
         全站 `ol,ul,menu{list-style:none}` 把默认圆点清掉了 → 用 ::before 还原。
         设计稿实测：圆点直径 3.5~4px、圆心正对正文行中心、圆点左缘距内容左缘 7px、
         正文缩进 22px；list 行距 = 行高 24px（与正文行距一致，item 之间无额外间距）。 */
      .td-desc ul { margin: 0 0 12px; padding-left: 0; }
      .td-desc li { position: relative; padding-left: 22px; margin-bottom: 0; }
      .td-desc li::before {
        content: ''; position: absolute; left: 7px; top: 10px;
        width: 4px; height: 4px; border-radius: 50%; background: currentColor;
      }
      /* 描述区折叠（第 25 轮第 4 项）：默认限高（设计稿 374），点「展开全文」平滑过渡。
         ⚠️ max-height 从 px 到 none 不可动画 → 过渡始终在**像素值**之间做，
         由 JS 在过渡结束后才把内联 max-height 置 none（见 bindDetail）。 */
      .td-desc-body {
        max-height: 374px; overflow: hidden;
        transition: max-height 320ms var(--transition-timing-function-standard, cubic-bezier(0.4, 0, 0.2, 1));
      }
      .td-desc-body.is-open { max-height: none; }
      .td-desc-body.is-animating { will-change: max-height; }
      @media (prefers-reduced-motion: reduce) {
        .td-desc-body { transition: none; }
      }
      .td-expand { display: flex; align-items: center; gap: 16px; margin: 12px 40px 0; }
      .td-expand-line { flex: 1; height: 1px; background: var(--td-line); }
      .td-expand-btn { flex: none; }
      .td-sec { padding: 24px 40px 0; }
      .td-sec-head {
        display: inline-flex; align-items: center; gap: 4px; margin-bottom: 10px;
        font-size: var(--font-size-body-3); font-weight: 500; color: var(--td-ink-2);
      }
      .td-sec-head svg { width: 14px; height: 14px; flex: none; }
      .td-files { display: flex; flex-wrap: wrap; gap: 8px; }
      /* 附件 / AI 产物 / 文件 卡片：本身是链接，hover 背景加深一级（fill-1 → fill-2）
         ★ 第 28 轮第 6 项：按设计稿 622:13950 逐像素实测重标定（此前 4 处卡片共用一个图标、尺寸也不对）。
           小卡（附件）: 高 36 / 圆角 6（实测 r≈6，DS 圆角 token 无 6 → 适配层变量 --td-radius-card）
                        图标盒 16×16（字形 10.5×13）；图标↔文字 gap **4px**（实测文字左缘距卡左 32px）
           大卡（AI 产物/文件）: 294×56 / 圆角 8(=--border-radius-large) / 图标盒 **24×24** / 间距 **12px**
                        且图标与文字之间有一条 1×24 的竖分隔线（--color-border-3 = #C9C9C9），
                        线心距卡左缘 48px（= 12 内距 + 24 图标 + 12 间距）→ 文字左缘 61px（实测 60.5）。 */
      .td-file {
        box-sizing: border-box; display: flex; align-items: center; gap: 4px;
        height: 36px; padding: 0 12px; min-width: 0; max-width: 100%;
        background: var(--td-card); border-radius: var(--td-radius-card);
        color: inherit; text-decoration: none; cursor: pointer;
        transition: background-color 120ms var(--transition-timing-function-standard);
      }
      .td-file:hover, .td-file:focus-visible { background: var(--color-fill-2); }
      .td-file:focus-visible { outline: 2px solid var(--color-primary-6); outline-offset: 2px; }
      .td-file-ico { width: 16px; height: 16px; flex: none; color: var(--td-ico-gray); line-height: 0; }
      .td-file-ico svg { display: block; width: 100%; height: 100%; }
      /* 文件类型着色：只覆盖色，不改图标形状 */
      .td-file-ico.is-web { color: var(--td-ico-web); }
      .td-file-tx {
        font-size: var(--font-size-body-3); color: var(--td-strong);
        overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
      }
      /* 大卡：294×56 + 24px 图标 + 竖分隔线（分隔线由 DOM 里的 .td-file-sep 承担） */
      .td-file--lg { width: 294px; height: 56px; padding: 0 12px; align-items: center; gap: 12px; border-radius: var(--border-radius-large); }
      .td-file--lg .td-file-ico { width: 24px; height: 24px; }
      .td-file-sep { flex: none; width: 1px; height: 24px; background: var(--color-border-3); }
      .td-file--lg .td-file-body { display: flex; flex-direction: column; gap: 0; min-width: 0; }
      .td-file--lg .td-file-tx { font-size: var(--font-size-body-3); font-weight: 500; line-height: 22px; }
      .td-file-size { font-size: var(--font-size-body-1); line-height: 16px; color: var(--td-meta); }
      /* .md 徽标是双色实心图标，颜色走 CSS（SVG 内不写死色值） */
      .td-ico-md-body { fill: var(--td-ico-md); }
      .td-ico-md-fold { fill: var(--td-ico-md-fold); }
      .td-ico-md-mark { fill: none; stroke: var(--color-bg-1); stroke-width: 1.1; stroke-linecap: round; stroke-linejoin: round; }
      .td-ico-md-mark.is-solid { fill: var(--color-bg-1); stroke: none; }
      /* -------------------- 左栏右侧信息列 -------------------- */
      /* 信息列左分隔线（第 24 轮第 2 项）：原用 --color-border-2(#E5E5E5) 偏深，
         浅一级 → --td-hairline(--color-border-1)；
         设计稿实测该线为 #EBECED（介于 gray-2 与 gray-3 之间，见 :root 注释）。 */
      .td-side {
        flex: 1 1 20%; min-width: var(--td-side-min); box-sizing: border-box; overflow: auto;
        padding: 20px; display: flex; flex-direction: column; gap: 24px;
        border-left: 1px solid var(--td-hairline);
      }
      /* 小节标题：设计稿「任务属性」墨色实测 #1F1F1F = --color-text-1（非灰蓝） */
      .td-side h2 {
        margin: 0 0 16px; font-size: var(--font-size-body-3); font-weight: 500;
        color: var(--color-text-1); line-height: 20px;
      }
      /* 「任务属性」与「任务动态」两组之间的一条间隔线（第 26 轮第 2 项）。
         线色取 --td-line(#F2F2F2)，与底部 .td-side-foot 上方的分隔线同色；
         .td-side 是 flex column + gap 24，所以线上下各留 24px（padding-top 24 补下半）。 */
      .td-side-dyn { border-top: 1px solid var(--td-line); padding-top: 24px; }
      /* 信息列正文（第 25 轮第 2 项：14px → ★ 第 30 轮第 3 项：统一 13px = --font-size-body-2）。
         第 30 轮：任务属性、任务动态（含时间）以及底部「创建者/创建时间/最后更新」三组
         内容文字**全部** 13px；唯一不动的是两组小节标题 `.td-side h2`（14px）与
         优先级 `.giencoder-tag`（12px，tag 契约 sizes.small，第 28 轮第 7 项已按你的要求回归契约）。 */
      .td-attr { margin: 0; display: flex; flex-direction: column; gap: 14px; }
      /* 第 26 轮第 3 项：label 与值之间的间距 8 → 16px */
      .td-attr-row { display: flex; align-items: center; gap: 16px; font-size: var(--font-size-body-2); line-height: 20px; }
      .td-attr-k { flex: none; color: var(--td-meta); }
      .td-attr-v { color: var(--td-strong); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .td-attr-link { display: inline-flex; align-items: center; gap: 4px; color: var(--td-strong); text-decoration: none; min-width: 0; }
      .td-attr-link svg { width: 14px; height: 14px; flex: none; color: var(--td-ink-2); }
      /* ★ 第 28 轮第 3 项：来源需求是链接，hover 时文字变主题蓝。
         与 `.td-ai-meta a:hover`（第 305 行）保持同一套交互语言：文字用 --color-primary-6(#3770F7)，
         前置图标（回形针）同步变色，避免出现「文字蓝、图标灰」的割裂。
         ⚠️ 本页无 `[giencoder-theme='dark']` CSS 分支（DS 的 components.css 也没有），
         故无需补主题前缀规则；但若将来加暗色 token，需同步补一份带前缀的 hover。 */
      .td-attr-link:hover, .td-attr-link:focus-visible { color: var(--color-primary-6); }
      .td-attr-link:hover svg, .td-attr-link:focus-visible svg { color: var(--color-primary-6); }
      /* ★ 第 27 轮第 3 项：来源需求的链接要显示更多文字。
         原因有两个：(1) 原来的「…」是**写死在文案里**的，永远只到「GienX端到端初始化…」9 字；
         (2) 值列只有 145px，链接实测 149px 反而溢出 4px 被裁。
         改法：放真实完整标题 + 真截断；并允许该行折行 2 行（-webkit-line-clamp:2 会自动补结尾省略号），
         label 顶对齐。实测单行仅能显示约 6 个汉字，折 2 行后可显示约 26 个字符。
         另外按设计稿把链接图标移到文字**前面**（设计稿 = 🔗 GienX端到端初始化…）。 */
      .td-side .td-attr-row.is-wrap { align-items: flex-start; }
      .td-side .td-attr-row.is-wrap .td-attr-v {
        white-space: normal; text-overflow: clip;
        display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2;
      }
      .td-side .td-attr-row.is-wrap .td-attr-link { display: inline; }
      .td-side .td-attr-row.is-wrap .td-attr-link svg {
        display: inline-block; vertical-align: -2px; margin-right: 4px;
      }
      /* ★ 信息列所有属性组统一为「左右布局」（第 24 轮第 5 项 + 第 26 轮第 4 项）
         设计稿实测：7 行的 label 全部从 x=712.5 起、值全部从 x=776.5 起 → label 列固定 **64px**；
         行距：值行 pitch = 34px（行高 20 + 间距 14）。按要求「稍微收一下」→ 间距 14 → 10（pitch 30）。
         做法就是 label 定宽 + 值跟随（原来 label 自适应宽 → 各行值起点参差不齐）。
         第 26 轮第 4 项：原来只作用于「任务属性」（.td-side-attr），现在改为作用于 .td-side 下
         **所有** .td-attr —— 使底部「创建者 / 创建时间 / 最后更新」三行与上方任务属性排列方式完全一致
         （原来底部单独覆写成 gap 4px + 行高 24px、label 自适应，值起点参差）。 */
      .td-side .td-attr { gap: 10px; }
      .td-side .td-attr-k { width: 64px; }
      /* 视图适配层：「高优先级」在 DS 里是 Tag（tag 契约：danger 预设色 = --color-*-light-1 底
         + --color-*-6 文字）。设计稿实测 52×18 / 圆角 4 / 底 #FFECE8(=--color-danger-light-1)
         / 文字 #F53F3F(=--color-danger-6)；DS 现版 .giencoder-tag-danger 用的是 15% color-mix
         近似色 + --color-text-1 文字、small 档高 20px → 本页按契约描述的配色收敛。
         选择器 (0,3,0) ≥ DS 的 .giencoder-tag.giencoder-tag-* (0,2,0)，不会被静默覆盖。 */
      .td-side-attr .td-attr-v .giencoder-tag.td-tag-prio {
        height: 18px; padding: 0 1px; border-radius: var(--border-radius-medium);
        background: var(--color-danger-light-1); color: var(--color-danger-6);
        /* ★ 第 28 轮第 7 项：标签字号回归 DS 契约。
           tag.json 的 sizes 里 small = 12px；DS 本体 `.giencoder-tag` 用
           --font-size-body-1(12px)，`.giencoder-tag-content` **自身不设 font-size**（纯继承）。
           这里原先把父级覆写成 --font-size-body-3(14px)，导致标签文字 14px。
           → 改回 --font-size-body-1，与 tag 契约一致（仍然是 (0,3,0) 特异性，不会被 DS 覆盖）。 */
        font-size: var(--font-size-body-1); line-height: 1;
      }
      /* 信息列底部：创建者 / 创建时间 / 最后更新（设计稿 容器 121 220×96、首行距分隔线 16）
         第 26 轮第 4 项：排列方式已由 `.td-side .td-attr` 统一到与上方「任务属性」一致，
         这里不再单独覆写 gap / 行高（原为 gap 4px + 行高 24px）。 */
      .td-side-foot { margin-top: auto; padding-top: 16px; border-top: 1px solid var(--td-line); }
      .td-tl { margin: 0; padding: 0; list-style: none; position: relative; }
      .td-tl::before {
        content: ''; position: absolute; left: 3px; top: 10px; bottom: 10px;
        width: 1px; background: var(--td-line);
      }
      .td-tl li { position: relative; padding: 0 0 8px 18px; }   /* 设计稿行距 50 = 42 + 8 */
      .td-tl li:last-child { padding-bottom: 0; }
      .td-tl li::before {
        content: ''; position: absolute; left: 0; top: 7px; width: 7px; height: 7px;
        border-radius: 50%; background: rgb(var(--gray-4)); box-sizing: border-box;
        border: 1px solid var(--color-bg-1);
      }
      .td-tl-line1 { display: flex; gap: 8px; font-size: var(--font-size-body-2); line-height: 20px; }
      .td-tl-who { color: var(--td-strong); flex: none; }
      .td-tl-what { color: var(--color-text-2); }
      /* ★ 第 30 轮第 3 项：任务动态的「时间」也并入 13px（第 25 轮曾声明它保持 12px，本轮按「全部 13px」取消该例外） */
      .td-tl-time { display: block; margin-top: 2px; font-size: var(--font-size-body-2); line-height: 20px; color: var(--td-meta); }
      /* -------------------- 拖动条 -------------------- */
      .td-gutter {
        flex: none; width: var(--td-gap); position: relative; cursor: col-resize;
        display: flex; align-items: center; justify-content: center;
        background: transparent; border: none; padding: 0;
        transition: background-color 120ms var(--transition-timing-function-standard);
      }
      /* 间隙仅 8px，用 ::before 把拖动热区向两侧各扩 8px（视觉仍为 8px） */
      .td-gutter::before { content: ''; position: absolute; left: -8px; right: -8px; top: 0; bottom: 0; }
      .td-gutter-bar {
        width: 2px; height: 32px; border-radius: 1px; background: transparent;
        transition: background-color 120ms var(--transition-timing-function-standard), height 120ms var(--transition-timing-function-standard);
      }
      .td-gutter:hover .td-gutter-bar,
      .td-gutter:focus-visible .td-gutter-bar,
      .td-gutter.is-dragging .td-gutter-bar { background: var(--color-primary-6); height: 56px; }
      .td-gutter:focus-visible { outline: none; }
      /* -------------------- 右栏 -------------------- */
      .td-right {
        flex: none; width: var(--td-right-w); box-sizing: border-box;
        display: flex; flex-direction: column; overflow: hidden;
        background: var(--color-bg-1); border-radius: 8px;
        box-shadow: var(--td-panel-shadow);   /* 同左栏：设计稿无描边，只有柔和投影 */
      }
      .td-right-inner { flex: 1; min-height: 0; display: flex; flex-direction: column; }
      .td-right-bar {
        height: 64px; flex: none; box-sizing: border-box;
        display: flex; align-items: flex-start; gap: 8px; padding: 12px 20px 0;
      }
      .td-right-head { min-width: 0; flex: 1; }
      .td-right-title {
        font-size: var(--font-size-body-3); font-weight: 500; line-height: 24px; color: var(--td-strong);
        overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
      }
      .td-right-time { font-size: var(--font-size-body-1); line-height: 16px; color: var(--td-meta); }
      .td-right-acts { display: flex; align-items: center; gap: 8px; flex: none; }
      /* 适配层：DS Button(secondary + size-mini + icon) → 设计稿 24×24 / 无边 / radius 4 */
      .td-round-btn { box-sizing: border-box; width: 32px; padding: 0; border-color: transparent; line-height: 0; }
      .td-chat { flex: 1; min-height: 0; overflow: auto; padding: 16px 20px 8px; display: flex; flex-direction: column; }
      /* ★ 第 29 轮第 2 项：消息列独立成一个内层列 —— 全屏时只收窄它，.td-chat 保持满宽，
         这样滚动条仍贴面板边缘（不跟着 860 一起缩进去）。 */
      .td-chat-inner { display: flex; flex-direction: column; gap: 16px; min-width: 0; }
      .td-msg-user {
        align-self: flex-end; max-width: 100%; box-sizing: border-box;
        padding: 8px 12px; border-radius: var(--border-radius-large);
        background: var(--td-bubble);
        font-size: var(--font-size-body-3); line-height: 24px; color: var(--td-strong);
      }
      .td-msg-ai { display: flex; flex-direction: column; gap: 8px; }
      .td-ai-head { display: flex; align-items: center; gap: 8px; }
      .td-ai-avatar {
        width: 24px; height: 24px; flex: none; border-radius: 50%;
        background: var(--color-primary-light-2, var(--td-card));
        display: inline-flex; align-items: center; justify-content: center;
        color: var(--color-primary-6); line-height: 0;
      }
      .td-ai-name { font-size: var(--font-size-body-3); font-weight: 500; color: var(--td-strong); line-height: 22px; }
      .td-ai-meta { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-3); color: var(--td-meta); }
      .td-ai-meta a { display: inline-flex; align-items: center; gap: 4px; color: var(--td-meta); text-decoration: none; }
      .td-ai-meta a:hover { color: var(--color-primary-6); }
      .td-ai-meta svg { width: 14px; height: 14px; flex: none; }
      /* 第 26 轮第 6 项：AI 消息正文墨色加深（原 --color-text-2 → 最深一级 --color-text-1） */
      .td-msg-ai p { margin: 0; font-size: var(--font-size-body-3); line-height: 24px; color: var(--color-text-1); }
      /* ★ 第 32 轮第 3 项：AI 消息里的文件卡**不再是独立形态**。
         原先是 `.td-ai-file`（281×56 的 div、无链接无 hover），与「3 个 AI 产物」的
         `.td-file--lg`（294×56、<a> + hover 加深）视觉/交互不一致。
         现改为复用同一个卡片构造函数（`__AIFILE__` → fcard(..., big=True)），
         两处为**同一组件**：同宽同高、同图标盒、同竖分隔线、同 hover 交互。
         已删除 `.td-ai-file` 全部样式（下方原注释保留作历史记录）：
         第 28 轮第 5 项曾按设计稿把它标定为 281×56 / 图标 24 / 竖分隔线；第 32 轮统一到 294。 */
      .td-ai-foot { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-3); color: var(--td-meta); }
      .td-ai-foot .td-sep { width: 1px; height: 12px; background: var(--color-border-2); }
      /* 第 27 轮第 2 项：图标与文字之间的间距减半（8px → 4px）。
         做法是把「图标 + 文字」包成 .td-ai-foot-item（组内 gap 4px），
         组与组之间的间隔仍走外层 .td-ai-foot 的 gap 8px，互不影响。 */
      .td-ai-foot-item { display: inline-flex; align-items: center; gap: 4px; }
      /* 底行图标（第 26 轮第 7 项）：设计稿 2x 逐像素实测 ——
         「输出完成」前是**实心圆 + 白色对勾**（12×12，色 (134,134,134) = --color-text-3，与同行文字同色）；
         「Token 速率」前是一个**仪表盘**图标（同为 12×12）。图标与文字间距 7.5px ≈ gap 8px。 */
      .td-ai-foot-ico { width: 12px; height: 12px; flex: none; line-height: 0; color: var(--td-meta); }
      /* 对勾用面板底色（不是写死 #fff），保持 token 化 */
      .td-ai-foot-ico .td-ico-check { stroke: var(--color-bg-1); }
      /* -------------------- 底部输入区（复用基础工作台对话框模块） -------------------- */
      /* 模块本体来自 pages/base.html，本页只负责外层定位；不新增同义类 */
      .td-composer { flex: none; margin: 8px 20px 20px; }
      /* 补齐 base 页使用、本页 Tailwind 产物未包含的 3 个任意值类 */
      .td-composer .min-h-\[96px\] { min-height: 96px; }
      .td-composer .gap-\[2px\] { gap: 2px; }
      .td-composer .bg-\[var\(--color-fill-3\)\] { background: var(--color-fill-3); }
      /* 窄容器收敛：480 右栏可用 414px，模块工具栏自然宽 489px
         → 收起占位最大的「标准模式」选择器、组内间距 8→4、文本不换行；其余控件全部保留 */
      .td-composer .giencoder-select[style*="width: 96px"] { display: none; }
      .td-composer .flex.items-center.gap-\[8px\] { gap: 4px; }
      .td-composer .flex.items-center.gap-2 { gap: 4px; }
      .td-composer [aria-label="数字分身"] { white-space: nowrap; }
      /* ================= 对话框三个弹层（★ 第 28 轮第 4 项） =================
         结构与尺寸对齐 pages/base.html 里同一个对话框模块（该页是 Vite 产物，只能作真值参考）：
           (1) 添加菜单   180×92 / 圆角 8 / 白底 + inset 0 0 0 1px #E5E5E5 + blur(20px)
                        两个 168×32 菜单项（left 6 / top 6 与 top 54），中间 148×1 分隔线（top 45.5）
           (2) 技能面板   原 760×320 居中 → 本页右栏窄（480，可用 414），760 会溢出，
                        故宽度改为 min(760px, 100%)，其余几何（圆角 12 / 88% 白 + blur / 底部 44px 操作条）不变
           (3) 大模型下拉 沿用 DS Select 契约结构（.giencoder-select-popup / -option），只补开合与选中
         ⚠️ 三个弹层都靠 hidden 属性或内联 display 控制显隐，显式补 [hidden] 规则以免被 display 覆盖。 */
      .td-add-pop[hidden], .td-skill-pop[hidden] { display: none !important; }
      .td-add-pop {
        position: absolute; left: 0; bottom: calc(100% + 4px); width: 180px; height: 92px;
        background: var(--color-bg-5); border-radius: var(--border-radius-large);
        box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.1), inset 0 0 0 1px var(--color-border-2);
        -webkit-backdrop-filter: blur(20px); backdrop-filter: blur(20px); z-index: 9999;
      }
      .td-add-item {
        position: absolute; left: 6px; width: 168px; height: 32px;
        border-radius: var(--border-radius-medium); cursor: pointer;
        color: var(--td-ico-gray);
        transition: background-color 0.1s ease;
      }
      .td-add-item:hover, .td-add-item:focus-visible { background: var(--color-fill-2); outline: none; }
      .td-add-item > svg { position: absolute; left: 10px; top: 9px; width: 14px; height: 14px; }
      .td-add-item > span {
        position: absolute; left: 32px; top: 5px;
        font-size: var(--font-size-body-3); line-height: 22px; color: var(--color-text-1);
      }
      .td-add-item[data-td-add="file"] { top: 6px; }
      .td-add-item[data-td-add="kb"] { top: 54px; }
      .td-add-sep { position: absolute; left: 16px; top: 45.5px; width: 148px; height: 1px; background: var(--color-fill-2); }
      .td-skill-pop {
        position: absolute; left: 50%; transform: translateX(-50%); bottom: calc(100% + 8px);
        width: min(760px, 100%); height: 320px; box-sizing: border-box; overflow: hidden;
        border-radius: var(--border-radius-xl); border: 1px solid var(--color-border-2);
        background: rgba(255, 255, 255, 0.88);
        -webkit-backdrop-filter: blur(10px) saturate(100%); backdrop-filter: blur(10px) saturate(100%);
        box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.08), inset 0 3px 3px 0 var(--color-bg-5);
        z-index: 9998;
      }
      .td-skill-list { position: absolute; left: 0; right: 0; top: 0; bottom: 44px; overflow-y: auto; overflow-x: hidden; padding: 12px 12px 6px; }
      .td-skill-list::-webkit-scrollbar { width: 6px; }
      .td-skill-list::-webkit-scrollbar-thumb { background: var(--color-border-2); border-radius: 3px; }
      .td-skill-row {
        position: relative; height: 32px; border-radius: var(--border-radius-medium); cursor: pointer;
        transition: background-color 0.1s ease;
      }
      .td-skill-row:hover, .td-skill-row.is-active { background: var(--color-fill-2); }
      .td-skill-ico { position: absolute; left: 11px; top: 10px; width: 12px; height: 12px; color: var(--td-ico-gray); line-height: 0; }
      .td-skill-ico svg { display: block; width: 100%; height: 100%; }
      .td-skill-ico.is-goal { left: 10px; top: 9px; width: 14px; height: 14px; color: var(--td-ico-skill); }
      .td-skill-txt { position: absolute; left: 34px; top: 5px; right: 46px; display: flex; gap: 12px; align-items: center; overflow: hidden; }
      .td-skill-name { flex: none; font-size: var(--font-size-body-3); line-height: 22px; color: var(--color-text-1); }
      .td-skill-desc {
        flex: 1 1 0; min-width: 0; font-size: var(--font-size-body-1); line-height: 22px; color: var(--color-text-3);
        overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
      }
      .td-skill-row.is-goal .td-skill-name { color: var(--td-ico-skill); }
      .td-skill-tag {
        position: absolute; right: 6px; top: 6px; box-sizing: border-box; height: 20px; padding: 0 6px;
        background: var(--color-bg-5); border: 1px solid var(--color-fill-2); border-radius: 3px;
        font-size: 11px; line-height: 18px; color: var(--color-text-3);
      }
      .td-skill-group { margin: 12px 0 8px 7px; font-size: var(--font-size-body-1); font-weight: 500; line-height: 20px; color: var(--color-text-3); }
      .td-skill-foot { position: absolute; left: 12px; right: 12px; bottom: 12px; height: 44px; }
      .td-skill-foot::before { content: ''; position: absolute; left: 0; top: 0; width: 100%; height: 1px; background: var(--color-fill-2); }
      .td-skill-foot > div { position: absolute; left: 0; top: 12px; display: flex; gap: 8px; }
      .td-skill-foot .giencoder-btn { width: 88px; }
      .td-skill-x {
        position: absolute; right: 32px; top: 10px; width: 12px; height: 12px; padding: 0;
        display: inline-flex; align-items: center; justify-content: center;
        border: 0; background: none; color: var(--color-text-4); cursor: pointer; line-height: 0; z-index: 3;
      }
      .td-skill-x:hover { color: var(--color-text-1); }
      .td-skill-x svg { display: block; width: 100%; height: 100%; }
      /* 大模型 / 标准模式下拉：完全沿用 DS 契约的开合机制
         —— gienx-templates/ui-controls.css 里 `.giencoder-select-popup` 默认 opacity:0 / visibility:hidden /
            translate:0 4px / scale:.96，加 `.giencoder-popup-open` 后 spring 过渡到展开态。
         ⚠️ 第 28 轮踩坑：最初用内联 `style.display = 'block' | 'none'` 代替该类 —— display 确实是 block，
           但 **opacity 仍为 0、visibility 仍为 hidden，页面上完全看不到**（getBoundingClientRect 却完全正常，
           极易误判为"已实现"）。必须用 `.giencoder-popup-open`。
         这里只补两处方向适配（选择器限定在组件类上，不改组件本体）： */
      .td-composer .giencoder-select-popup {
        /* ① DS 默认向下展开（top: calc(100% + 4px)），但本页 AI 对话框固定在右栏底部，
              实测弹层 rect bottom 1005 > 视口 900 → 只剩 37px 可见、4 个选项有 3 个点不到。
              选择器锚点在底部 ⇒ 翻转为向上展开，与「添加菜单」(.td-add-pop) 朝向一致。 */
        top: auto;
        bottom: calc(100% + 4px);
        /* ② 缩放原点随之从顶边翻到底边 */
        transform-origin: bottom center;
      }
      /* -------------------- AI 会话全屏 / 取消全屏（第 26 轮第 5 项） --------------------
         点右栏右上角「全屏」→ 整个 AI 对话框向左扩展到最大化：左栏（含信息列）与拖动条让位隐藏，
         .td-right 由固定宽改为 flex:1 撑满 .td-root（x8 ~ x1432）。
         再点一次（图标已换成「取消全屏」）恢复原状；全屏态下 Esc 也先退出全屏（见页尾脚本）。
         两个图标用类切换显隐，避免 JS 改 innerHTML。 */
      .td-root.is-fullscreen .td-left,
      .td-root.is-fullscreen .td-gutter { display: none; }
      .td-root.is-fullscreen .td-right { flex: 1 1 auto; width: auto; }
      /* ★ 第 29 轮第 2 项：全屏后内容区（消息列 + 输入区）最大宽度 860px 并水平居中。
         · 消息列：.td-chat 靠 align-items:center 把内层 860 列居中；
         · 输入区：.td-composer 自身收成 860，左右留 auto（保留原有上下 8/20 边距）。
         两者同宽同中心 ⇒ 输入框与消息列左右边缘严格对齐。 */
      .td-root.is-fullscreen .td-chat { align-items: center; }
      .td-root.is-fullscreen .td-chat-inner { width: 100%; max-width: var(--td-fs-content); }
      .td-root.is-fullscreen .td-composer {
        width: 100%; max-width: var(--td-fs-content);
        margin-left: auto; margin-right: auto;
      }
      .td-ico-min { display: none; }
      .td-root.is-fullscreen .td-ico-max { display: none; }
      .td-root.is-fullscreen .td-ico-min { display: block; }
      /* -------------------- 折叠态 -------------------- */
      .td-collapsed { display: none; }
      .td-root.is-collapsed .td-right-inner { display: none; }
      .td-root.is-collapsed .td-collapsed {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        width: 100%; height: 100%; cursor: pointer; border: none; background: transparent; padding: 0;
      }
      .td-root.is-collapsed .td-collapsed span {
        font-size: 14px; font-weight: 500; line-height: 18px; color: var(--td-ink-2);
      }
      .td-root.is-collapsed .td-collapsed:hover span { color: var(--color-primary-6); }
      /* 拖动中禁用文本选中与过渡，避免抖动 */
      .td-root.is-dragging, .td-root.is-dragging * { user-select: none; }
      .td-root.is-dragging .td-right { transition: none; }
      @media (prefers-reduced-motion: reduce) {
        .td-gutter, .td-gutter-bar { transition: none; }
      }
      /* ------------- 按住标题栏左右拖动互换两栏位置 -------------
         （★ 第 28 轮第 1 项建立；★ 第 30 轮第 2 项大幅优化手感）
         静止态只切一个类：.td-root.is-swapped{flex-direction:row-reverse} 反转主轴顺序，DOM 顺序不变
         ⇒ 页面里所有「按 DOM 查找」的 JS（全屏/折叠/拖动条/描述折叠）全部不受影响。
         .td-side 的 border-left 正好仍落在 .td-main 与 .td-side 之间 → 无需翻转分隔线。
         与既有交互互斥：全屏态 .td-left/.td-gutter 已 display:none；折叠态 .td-right-inner 已 display:none。

         ★ 第 30 轮的观感优化（原实现 = 瞬间切类 + 260ms 透明度闪一下 → 生硬）：
           · 跟手：拖动中主动栏按指针位移 —— **橡皮筋**而非硬限幅：|dx| ≤ cap 时 1:1 跟手；
             超出后继续按 RB 走（越拖越沉但不「顶住不动」）；
             另一栏反向微移「让位」，让两栏立刻有物理联动感；
           · 真实滑动：交换用 FLIP（先记 rect → 切类 → 再记 rect → 从 translateX(dx) 滑回 0），
             两栏真的横move过去；飞行期把**被拖的那一栏**抬到 z=3 并加深投影（is-fly-left/right），
             读起来像「把卡片拎起来挪过去」，而不是两张不透明卡片硬生生对穿；
           · 回弹：未达阈值时把跟手位移用同一条曲线弹回 0，不再瞬间归位；
           · 甩动：|v| ≥ 0.6 px/ms 且方向正确时，位移不足 72px 也换位（短促快拖可换）；
           · 统一曲线 cubic-bezier(0.22,1,0.36,1)（ease-out-quint：起步快、收尾稳，无过冲不越界）；
           · prefers-reduced-motion 下跳过全部位移动画，只切类。
         ★ 第 32 轮第 2 项：cap 14%→28%、RB 0.18→0.28（跟手区 ≈200px，指针走多远卡片走多远）；
           并**去掉 scale**（大尺寸文字密集容器每帧重栅格化 = 掉帧），位移改为 rAF 合并写入。 */
      .td-root.is-swapped { flex-direction: row-reverse; }
      .td-bar, .td-right-bar { cursor: grab; touch-action: none; }
      .td-bar .giencoder-btn, .td-right-bar .giencoder-btn { cursor: pointer; }
      .td-root.is-xdrag, .td-root.is-xdrag * { user-select: none; }
      .td-root.is-xdrag .td-bar, .td-root.is-xdrag .td-right-bar { cursor: grabbing; }
      /* 跟手/回弹期间的位移过渡由 JS 用 Web Animations 驱动；这里只给「提示态」加过渡。
         （will-change 只在交互期开，长期挂着会白白提升图层） */
      .td-left, .td-right {
        outline: 2px solid transparent; outline-offset: -2px;
        transition: outline-color 140ms var(--transition-timing-function-standard),
                    box-shadow 180ms var(--transition-timing-function-standard);
      }
      .td-root.is-xdrag .td-left, .td-root.is-xdrag .td-right,
      .td-root.is-swap-fly .td-left, .td-root.is-swap-fly .td-right { will-change: transform; }
      .td-root.is-xdrag.is-xarmed .td-left,
      .td-root.is-xdrag.is-xarmed .td-right { outline-color: var(--color-primary-6); }
      /* 主动栏轻微的「拎起来」：加深投影（复用既有面板投影变量，不新增色值） */
      .td-root.is-xdrag .td-left.is-xdrag-panel,
      .td-root.is-xdrag .td-right.is-xdrag-panel { box-shadow: var(--td-panel-shadow), 0 8px 24px rgba(0, 0, 0, 0.10); }
      /* 让位栏：轻微降透明，暗示它正在被替换 */
      .td-root.is-xdrag .td-left.is-xdrag-peer,
      .td-root.is-xdrag .td-right.is-xdrag-peer { opacity: 0.88; }
      /* FLIP 飞行期：两栏都进独立层叠上下文，**被拖的那一栏**抬到 z=3 并加深投影，
         避免两栏重叠时看着像穿模（is-fly-left / is-fly-right 由 JS 按 d.panel 打） */
      .td-root.is-swap-fly .td-left,
      .td-root.is-swap-fly .td-right { position: relative; z-index: 1; }
      .td-root.is-swap-fly.is-fly-left .td-left,
      .td-root.is-swap-fly.is-fly-right .td-right {
        z-index: 3; box-shadow: var(--td-panel-shadow), 0 10px 28px rgba(0, 0, 0, 0.12);
      }
      @media (prefers-reduced-motion: reduce) {
        .td-left, .td-right { transition: none; }
        .td-root.is-xdrag .td-left.is-xdrag-panel,
        .td-root.is-xdrag .td-right.is-xdrag-panel { box-shadow: var(--td-panel-shadow); }
      }
      /* -------------------- 归属研发工作台：外壳切到「研发工作台」态 -------------------- */
      /* 详情页是研发工作台的下一级页面。React 外壳按「文件名 → 路由」映射判定页签
         （St = {base.html:/base, dev.html:/dev, kanban.html:/kanban, …}），
         pages/task-detail.html 不在映射表内 → 会被判成「基础工作台」。
         这里用本页作用域把外壳拉回研发工作台态（沿用 shell 自己的 dev 外观：
         shell / header / row 底色 #E5EDF5、row 左右 8px、页签选中「研发工作台」），
         并隐藏侧边菜单栏（1440 = 8 + 936 + 8 + 480 + 8，与设计稿一致）。 */
      body:has(.td-wrap) div.flex.h-dvh,
      body:has(.td-wrap) div.flex.h-dvh > header,
      body:has(.td-wrap) div.flex.h-dvh > div { background: var(--td-surround) !important; }
      body:has(.td-wrap) div:has(> main) { padding-left: 8px !important; padding-right: 8px !important; }
      body:has(.td-wrap) div:has(> main) > aside { display: none; }
      /* main 的 overflow 也要放开：否则容器投影仍被 main 的 padding box 裁掉 */
      body:has(.td-wrap) main { border: none; border-radius: 0; overflow: visible; }
      /* 页签游标与文字色：从「基础工作台」移到「研发工作台」
         （游标几何与 shell 的 dev 态一致：left 62 / width 124）
         ⚠️ shell 里未选中态的 class 是 `[color:color-mix(in_srgb,var(--color-text-1)_75%_transparent)]`，
         但 Tailwind 生成的声明缺逗号（`75% transparent`）→ 整条被丢弃，实测取的是继承色（body #0A0A0B）。
         这里按 dev 态实测结果还原：未选中 = 继承色，选中 = --color-text-1。 */
      body:has(.td-wrap) [role="tablist"] { background: var(--td-appbar) !important; }
      body:has(.td-wrap) [role="tablist"] > span[aria-hidden] { left: 62px !important; width: 124px !important; }
      body:has(.td-wrap) [role="tablist"] [data-tab="base"] { color: inherit !important; }
      body:has(.td-wrap) [role="tablist"] [data-tab="dev"] { color: var(--color-text-1) !important; }

      /* ------------------------------------------------------------------
         ★ 第 31 轮：顶栏「转派」成员浮窗（设计稿节点 1345:18366，320×480）
         组件一律用 DS 契约组装，不自造同义结构：
           浮层   div.giencoder-popover（popover.json anatomy，按契约渲染到 popupContainer=body）
           触发器 span.giencoder-popover-reference
           搜索   .giencoder-input-wrapper + -input-prefix + -input
           成员行 .giencoder-list-item[data-size=small] + -item-hoverable + -item-meta
                  + -item-title + -item-action
           头像   .giencoder-avatar + -circle + -text（底色走 --avatar-bg-N token）
           底栏   .giencoder-popover-footer + .giencoder-btn-primary
           滚动条 .giencoder-scroll-thin
         本段只写「视图适配层」：设计稿实测尺寸/间距/字色，以及 DS List 未定义的
         「选中行」着色 —— 用 role=option + aria-selected 表达，不新增类名。
         ★ 面板有 1px 边框（契约 .giencoder-popover 的 border: 1px solid --color-border-2）
           → 下面所有内距 = 设计稿真值 **− 1px**：
             标题 16→15 · 内容 16→15 · 底栏 16→15 · 搜索框内距 11→10
           （曾漏算这 1px，导致浮窗内所有元素整体右/下偏 1px；判据 x17≠16）
         ★ 实测真值（2x 图原点 PNG(60,44)、scale=2，逐像素反解）：
           面板 320×480 · **r6** · 边框 #E5E5E5 · 投影左/右峰值 alpha15、下 24、上 6
             → 与 --shadow2-down（0 4px 10px rgba(0,0,0,.1)）逐点吻合（也是契约声明的 token）
           圆角：面板 / 搜索框 / 行 / 按钮 **一律 6px**（覆盖率 0.5 亚像素法：5.5~5.7）
             → 用本页既有的 --td-radius-card（6px 档），DS 默认的 8/4 在此被适配层覆盖
           标题 14px/lh22 · 字重 400（笔画密度 46.8/39.1 ≈ 行名 44.5/38.7，不是 600）
           副标题 12px/lh16 · 距标题 4 · 色 --color-text-3
           搜索框 288×32 @(16,70) · 图标 14 色 #6B6B6B · 占位文字 14px 起 x53
           列表 x16 y118 高 297（7 行 × 32 + 6 × 2 间距 = 236 → 余 61 空白，溢出才出滚动条）
           行 32 高 / 内距 8 / 头像 20（字形 11px 白字）/ 名字 14px text-1 + 工号 text-3
           选中行 底 #ECF2FF + 描边 #D3E2FF + 尾部 14px 对勾（primary-6）
           hover 行 底 #F7F7F7(=--color-fill-1) · 分隔线 #F2F2F2(=--color-border-1) @y415
           按钮 288×32 @y432（14px）· 面板底部留白 16
         设计稿未定义的两处，自行取 DS 既有约定（已记录）：
           · 浮窗与按钮的 4px 间距 → 沿用 DS 弹层 calc(100% + 4px) 约定；
           · 水平对齐 → 左对齐触发按钮（越界时钳到视口内 8px）。 */
      .td-dp.giencoder-popover { width: 320px; border-radius: var(--td-radius-card); }
      /* 15 = 设计稿 16 − 面板 1px 边框；标题首行文字盒正好落在面板内 (16,16)，与设计稿「容器 145」同位 */
      .td-dp .giencoder-popover-title { padding: 15px 15px 0; font-size: 14px; line-height: 22px; font-weight: 400; }
      .td-dp-t2 { margin-top: 4px; font-size: 12px; line-height: 16px; font-weight: 400; color: var(--color-text-3); }
      .td-dp .giencoder-popover-content { padding: 12px 15px 0; }
      /* 内距 10 + 面板边框 1 = 11 → 图标盒起面板内 x27（ink x28）；图标右间距 11 → 文字盒起 x52（ink x53） */
      .td-dp .giencoder-input-wrapper { width: 100%; padding: 0 12px 0 10px; border-radius: var(--td-radius-card); }
      .td-dp .giencoder-input-prefix { margin-right: 11px; color: var(--td-ico-gray); }
      .td-dp .giencoder-input { font-size: 14px; }
      .td-dp .giencoder-input::placeholder { color: var(--color-text-3); }
      /* 列表定高：flex 列 + 行 flex:none，保证行恒为 32 高（不被压缩），溢出才滚 */
      .td-dp .giencoder-list { display: flex; flex-direction: column; margin-top: 16px; height: 297px; overflow-y: auto; }
      .td-dp .td-dp-item { flex: none; padding: 0 8px; border-radius: var(--td-radius-card); }
      .td-dp .td-dp-item[hidden] { display: none; }   /* .giencoder-list-item 是 flex，需压掉 hidden 的默认 display:none 失效 */
      .td-dp .giencoder-list-item[aria-selected="true"] {
        background: var(--td-dp-on-bg);
        /* 1px 描边用 inset ring 表达：不占布局、不产生 1px 位移，且跟随行圆角 */
        box-shadow: inset 0 0 0 1px var(--td-dp-on-line);
      }
      .td-dp .giencoder-list-item[aria-selected="true"]:hover { background: var(--td-dp-on-bg); }
      .td-dp-av { width: 20px; height: 20px; --avatar-color: var(--color-white); }
      .td-dp-name { font-size: 14px; line-height: 22px; }
      .td-dp-id { color: var(--color-text-3); }
      /* 对勾是 .giencoder-list-item-action（display:flex）的 flex item —— 按 CSS Display 规定，
         inline-flex 会被 **块化** 成 flex（实测 computed = flex），故这里直接写 flex，两者等价 */
      .td-dp-check { display: none; align-items: center; color: var(--color-primary-6); }
      .td-dp .giencoder-list-item[aria-selected="true"] .td-dp-check { display: flex; }
      .td-dp-none { margin: auto; }
      .td-dp-none[hidden] { display: none; }
      .td-dp-none .giencoder-empty-description { margin-top: 0; font-size: 12px; color: var(--color-text-3); }
      /* 下内距 15（不是 16）：设计稿「按钮底 y464 距面板底 480 = 16」由 15px 内距 + 面板自身 1px 下边框构成，
         写 16 会让面板长到 481（多算一次边框），实测过 320×481 → 320×480 */
      .td-dp .giencoder-popover-footer { padding: 16px 15px 15px; }
      /* 底栏按钮：DS 尺寸档 size-default(32) + width:100%（288 = 320 − 2 边框 − 2×15） */
      .td-dp .td-dp-ok { width: 100%; font-size: 14px; border-radius: var(--td-radius-card); }
      /* 转派结果提示：DS Message 组件（第 19 轮全局约定：凡消息提示一律用它） */
      .td-dp-msg { position: fixed; top: 64px; left: 50%; transform: translateX(-50%); z-index: 1100; }
      .td-dp-msg[hidden] { display: none; }
      .td-dp-msg .giencoder-message-icon { display: inline-flex; color: var(--color-success-6); }

      /* ------------------------------------------------------------------
         ★ 第 32 轮第 5 项：顶栏「协作」→ 分步模态弹窗（设计稿节点 622:20081，640×640）
         组件一律用 DS 契约组装，不自造同义结构：
           遮罩/面板 div.giencoder-modal-wrapper > div.giencoder-modal-mask
                    + div.giencoder-modal[role=dialog]（modal.json anatomy 全套：
                      -header / -title / -close-btn / -content / -footer）
           步骤条   .giencoder-steps.giencoder-steps-horizontal（steps.json anatomy：
                    div[role=list] / div[role=listitem] / 节点 span / 标题）
           行       .giencoder-list-item[data-size=small].giencoder-list-item-hoverable（list.json）
           勾选框   .giencoder-checkbox + -checkbox-input + -checkbox-mask（checkbox.json anatomy：
                    label / input[type=checkbox] / span 选框 / span 文本）
           头像     .giencoder-avatar + -circle + -text（avatar.json）
           搜索框   .giencoder-input-wrapper[data-size=medium] + -input-prefix + -input
           按钮     .giencoder-btn + -primary/-secondary + -size-default
           滚动条   .giencoder-scroll-thin
         本段只写「视图适配层」（设计稿实测尺寸/间距/字色 + DS 未定义的形态）。
         设计稿实测（mg-work/r32/design/coop.png 1440×900 1x，坐标即设计稿坐标）：
           遮罩 rgba(0,0,0,.4) + backdrop-filter blur(10px)（面板外取样 #959697）；
                DS --color-mask-bg 是 rgba(31,31,31,.6) → 本弹窗按设计稿取值
           面板 640×640 @(60,130) · 底 rgba(255,255,255,.95)（合成 ≈ #FEFEFE）
                · **圆角 16px**（左下角剖面拟合 r=16：y769→内缩14 / y764→4 / y760→2 / y757→1 逐点吻合；
                  DS 圆角档只有 0/2/4/8/12/50% → 适配层）
                · 面板 640 的纵向节奏（逐段闭合）：
                  header 46 + 18 + steps 32 + 19 + divider 24 + 11 + content 410 + footer 80 = 640
           标题「任务协作」16px 墨色盒 @(25,24..38) · 关闭 X 28×28（右内距 24，图标 16 居中）
           步骤条 592×32 @y64 · **两段咬合**：段1 右端尖角凸 6px / 段2 左端凹 6px，段间重叠 6px
                （逐行实测：段1 右缘 y64→317 / y72→321；段2 左缘 y64→316 / y72→319，中线最右）
                · 当前态 底 #ECF2FF + 1px #D3E2FF（= 本页已有的 --td-dp-on-bg / --td-dp-on-line）
                  文字 14px --color-primary-6
                · 未开始 底 --color-fill-2 + 文字 14px --color-text-2
                · 已完成 底 --color-fill-2 + 14px 对勾 + 文字 14px --color-text-1
                · 文字墨色高 13、段内居中（实测 step1 x132..213 / step2 x440..500）
           分割线 @y126（1px --color-border-1，实测 #EFEFEF）+ 14px --color-text-3 说明文字居中
                （文字墨色盒 x209..430 / w222 / 高 13 —— 12px 下只有 190×11，故取 14px）
           内容区 592×410 @y150 · 1px --color-border-1（实测 #F2F2F2）+ **r6**
                · 内距 15（= 设计稿 16 − 容器 1px 边框；写 16 会让行卡落到 x41、行宽掉到 558）
                Step1 行 560×32 + 2 间距（DS List 本体 `+` 选择器就是 2px）· hover --color-fill-1
                      内距 8 · 勾选框 14×14 @x48 · 文件名 14px @x68（DS checkbox 本体 gap 6）
                Step2 搜索框 560×32 @y166（1px --color-border-2，实测 #E5E5E5）
                      内距 0 12 0 10 · 放大镜 14 @x50 · 占位文字 14px @x77
                      成员列表 @y214（距搜索框 16）· 行内距 8
                      勾选框 14 @x48 → gap 16 → 头像 20 @x78 → gap 8 → 姓名 14px @x105 + 工号 text-3
           底栏 按钮 32 高 @y584 · 右内距 24 · 按钮间距 8
                Step1 取消 60 + 下一步 74 · Step2 取消 60 + 上一步 74 + 提交 60
                （DS .giencoder-btn 本体已是 14px 字 + padding 0 16px → 2 字 60 / 3 字 74，
                  与设计稿完全一致，无需改 padding）
                左侧计数 14px --color-text-3 @(24,593)「已选 N/8 个产物」/「已选 N/7 位协作者」
                （设计稿墨色盒 101×13 / 起点 x25；12px 下只有 83×11 → 取 14px）
         设计稿未定义处取 DS 既有约定：开合动效（modal.json motion：.2s decelerate，面板缩放 + 淡入）、
         遮罩点击关闭、Esc 关闭。
         ⚠️ 设计稿把勾选框标为「选中+禁用」（浅蓝 #B4C9FC = --color-primary-3），但需求是
            「用户按步骤执行选择」→ 取 DS checkbox.json 的可交互选中态 --color-primary-6；
            产物默认全选 8/8（与设计稿初始态一致）。
         ------------------------------------------------------------------ */
      .td-coop { position: fixed; inset: 0; z-index: 1050; display: flex; align-items: center; justify-content: center; }
      .td-coop[hidden] { display: none; }
      .td-coop .giencoder-modal-wrapper { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
      .td-coop .giencoder-modal-mask {
        position: absolute; inset: 0; background: rgba(0, 0, 0, 0.4);
        -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);
        opacity: 0; transition: opacity .2s cubic-bezier(0.34, 0.69, 0.1, 1);
      }
      .td-coop.is-open .giencoder-modal-mask { opacity: 1; }
      .td-coop .giencoder-modal {
        position: relative; box-sizing: border-box;
        width: 640px; height: 640px; max-height: calc(100vh - 48px);
        display: flex; flex-direction: column;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px; box-shadow: var(--shadow3-down);
        transform-origin: top center;
        opacity: 0; transform: translateY(-8px) scale(0.98);
        transition: opacity .2s cubic-bezier(0.34, 0.69, 0.1, 1), transform .2s var(--transition-timing-function-spring);
      }
      .td-coop.is-open .giencoder-modal { opacity: 1; transform: none; }
      /* header：内距 18 + 行高 28 = 46；steps 上外边距相应 20→18，纵向节奏不变（仍在 y64 起步）。
         ⚠️ 内距是 18 而非 16：设计稿标题「任务协作」墨色盒落在 y24..39，
            DS 字体度量下 16px 字在 28 行盒内墨色只会到 y22..37 → 需要下移 2px 对齐 */
      .td-coop .giencoder-modal-header {
        flex: none; height: 46px; box-sizing: border-box;
        padding: 18px 24px 0; border-bottom: none; align-items: flex-start;
      }
      .td-coop .giencoder-modal-title { font-size: 16px; line-height: 28px; font-weight: 600; }
      .td-coop .giencoder-modal-close-btn {
        width: 28px; height: 28px; padding: 0; flex: none;
        align-items: center; justify-content: center; border-radius: var(--td-radius-card);
      }
      /* ---- 步骤条：592×32，两段咬合（段1 右尖角 6px / 段2 左凹 6px，段间重叠 6px） ---- */
      .td-coop .giencoder-steps { flex: none; display: flex; height: 32px; margin: 18px 24px 0; }
      .td-coop .giencoder-steps-item {
        flex: 1 1 0; min-width: 0; height: 32px; box-sizing: border-box;
        display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 6px;
        background: var(--color-fill-2); border: 1px solid transparent;
        border-radius: var(--td-radius-card);
        font-size: 14px; line-height: 22px; color: var(--color-text-2); cursor: pointer;
      }
      /* DS Steps 的连接线伪元素在本形态下不需要（两段自成一体）→ 整段压掉 */
      .td-coop .giencoder-steps-item::after { content: none !important; }
      .td-coop .giencoder-steps-item:first-child {
        margin-right: -6px; z-index: 1;
        clip-path: polygon(0 0, calc(100% - 6px) 0, 100% 50%, calc(100% - 6px) 100%, 0 100%);
      }
      .td-coop .giencoder-steps-item:last-child {
        clip-path: polygon(6px 0, 100% 0, 100% 100%, 6px 100%, 0 50%);
      }
      .td-coop .giencoder-steps-item.is-active {
        background: var(--td-dp-on-bg); border-color: var(--td-dp-on-line); color: var(--color-primary-6);
      }
      .td-coop .giencoder-steps-item.is-finish { color: var(--color-text-1); }
      /* 节点 span：DS 本体是 32 圆底，本形态只保留 14px 对勾（仅已完成态出现） */
      .td-coop .giencoder-steps-icon {
        width: 14px; height: 14px; background: none; border-radius: 0;
        font-size: 0; color: inherit; display: none;
      }
      .td-coop .giencoder-steps-item.is-finish .giencoder-steps-icon { display: inline-flex; }
      .td-coop .giencoder-steps-title { font-size: 14px; font-weight: 400; color: inherit; }
      /* ---- 分割线：两段线 + 12px 说明文字居中（DS divider 契约 anatomy = div + span） ---- */
      /* 下外边距 11（不是 12）：分割线底 y139 + 11 = 内容区顶 y150（设计稿实测），
         写 12 会让内容区整体下移 1px（150 → 151），进而内容区高度掉到 409（应 410） */
      .td-coop-dvd { flex: none; display: flex; align-items: center; gap: 4px; height: 24px; margin: 19px 24px 11px; }
      .td-coop-dvd::before, .td-coop-dvd::after { content: ''; flex: 1 1 0; height: 1px; background: var(--color-border-1); }
      .td-coop-dvd-tx { flex: none; font-size: 14px; line-height: 20px; color: var(--color-text-3); }
      /* ---- 内容区：592×410，1px 边框 + r6 + 内距 15 ----
         内距 15（不是 16）：容器自带 1px 边框，设计稿行卡左缘在面板内 x40，
         边框占 x24 → 内容从 25，25 + 15 = 40；写 16 会让行卡落到 41、行宽掉到 558（应 560） */
      .td-coop .giencoder-modal-content {
        flex: 1 1 auto; min-height: 0; box-sizing: border-box;
        margin: 0 24px; padding: 15px;
        border: 1px solid var(--color-border-1); border-radius: var(--td-radius-card);
        /* 内容区是**纯白**卡片（设计稿实测 #FFFFFF），与面板底 rgba(255,255,255,.95)
           合成出的 #F9F9F9 不同 —— 少了这层白底，内容区会跟着面板变灰（实测 250 → 应 255） */
        background: var(--color-bg-5);
        overflow: hidden;
      }
      .td-coop-pane { display: flex; flex-direction: column; height: 100%; min-height: 0; }
      .td-coop-pane[hidden] { display: none; }
      /* ---- 行（产物 / 成员共用）：560×32 + 2 间距（DS List 的 `+` 选择器），内距 8 ---- */
      .td-coop .td-coop-row {
        flex: none; box-sizing: border-box; height: 32px; min-height: 32px;
        gap: 16px; padding: 0 8px; border-radius: var(--td-radius-card);
        font-size: 14px; color: var(--color-text-1);
      }
      .td-coop .td-coop-row[hidden] { display: none; }
      .td-coop .td-coop-cb { flex: none; }
      .td-coop .td-coop-tx { font-size: 14px; line-height: 22px; }
      .td-coop .td-coop-av { width: 20px; height: 20px; --avatar-color: var(--color-white); }
      .td-coop .td-coop-mname { font-size: 14px; line-height: 22px; }
      .td-coop .td-coop-mid { color: var(--color-text-3); }
      .td-coop .td-coop-list { flex: 0 1 auto; min-height: 0; overflow-y: auto; }
      /* ---- 搜索框（560×32 @y166，距成员列表 16） ---- */
      .td-coop .giencoder-input-wrapper { flex: none; width: 100%; box-sizing: border-box; padding: 0 12px 0 10px; }
      .td-coop .giencoder-input-prefix { margin-right: 12px; color: var(--color-text-3); }
      .td-coop .giencoder-input { font-size: 14px; }
      .td-coop .giencoder-input::placeholder { color: var(--color-text-3); }
      .td-coop .td-coop-members { margin-top: 16px; flex: 0 1 auto; min-height: 0; overflow-y: auto; }
      /* ---- 底栏：24 + 32 + 24 = 80 ---- */
      .td-coop .giencoder-modal-footer {
        flex: none; box-sizing: border-box; height: 80px;
        padding: 24px; border-top: none; gap: 8px;
        align-items: center; justify-content: space-between;
      }
      /* 计数文字 14px（不是 12px）：设计稿墨色盒 101×13 / 起点 x25，12px 下只有 83×11 */
      .td-coop-count { font-size: 14px; line-height: 22px; color: var(--color-text-3); }
      .td-coop-btns { display: flex; align-items: center; gap: 8px; }
      /* 按钮宽度对齐设计稿（取消/提交 60、下一步/上一步 74）：
         DS .giencoder-btn 是 14px 字 + padding 0 16px + 1px 边框 → 2 字 62 / 3 字 76，各多 2px；
         改内距 15 后 2 字 = 28+30+2 = 60、3 字 = 42+30+2 = 74，与设计稿逐值吻合 */
      .td-coop .td-coop-btn { padding: 0 15px; }
      /* .giencoder-btn 是 inline-flex，会盖掉 hidden 属性自带的 display:none → 显式补规则 */
      .td-coop .td-coop-btn[hidden] { display: none; }

      /* ------------------------------------------------------------------
         ★ 第 31 轮：转派浮窗用到的 DS 组件样式（构建期从 DS 源文件实时抽取）
         不要在这里手写这些组件的样式 —— 改样式请改 DS 源文件：
           · 静态结构（Popover / List / Avatar 形状与字符头像 / 细滚动条）
             giencoder-design-system/components.css
           · 弹层定位 + 开合动效（.giencoder-popup-open）
             giencoder-design-system/gienx-templates/ui-controls.css
         ------------------------------------------------------------------ */
      __DS_PICKER_CSS__

      /* ------------------------------------------------------------------
         ★ DS Image 组件样式占位符（第 30 轮第 1 项）
         构建期由本脚本末尾的 CSS.replace 用 DS 源文件实时抽取结果替换。
         不要在这里手写 Image 样式 —— 改样式请改 DS 源文件：
           · 静态结构   giencoder-design-system/components.css
           · 全屏遮罩 + 开合动效   giencoder-design-system/gienx-templates/ui-controls.css
         ------------------------------------------------------------------ */
      __DS_IMAGE_CSS__
    </style>"""

# ============================== HTML ==============================
# ---- 卡片文件类型图标（★ 第 28 轮第 6 项，全部按设计稿 622:13950 逐像素重画）----
# 原先 4 类卡片（附件 / AI 产物 / 文件 / AI 消息文件卡）共用同一个「折角文档」图标，与设计稿不符。
# 设计稿实测（2x 图，ASCII 位图读笔画 + 连通域量 bbox）：
#   ① 附件小卡（盒 16×16，字形 10.5×13，描边 ~1.2，色 #6B6B6B）
#      = 圆角文档，**右上角折角**；内部 2 条横线（上行 x3.7→8.2 / 下行 x3.7→6.8，y7.6 / y10.2）
#      折角：外轮廓在 x8 处开始斜切到 (11.5,5.75)；折片两条腿 = 竖线 x7(y1.5→5.75) + 横线 y5.75(x7→11.5)
#   ② .md 纯文本报告（盒 24×24，字形 17.5×20.5，描边 ~1.45，色 #6B6B6B）
#      = 圆角文档，**右下角折角**；内部 3 条横线（前两条 x7.5→15 @y7.2/y11，第三条短 x7.5→11 @y14.7）
#      折角：底边在 x16.6 处斜切到 (20.3,15.6)；折片两条腿 = 竖线 x15(y21→15.75) + 横线 y15.75(x15→20.3)
#   ③ .html（盒 24×24，字形 21×21，描边 ~1.8，色 #327FCB）
#      = 地球：圆 r9.6 + 赤道横线（贯穿直径）+ 竖椭圆（实测 rx≈3.5 → 取 3.4，ry = 9.6）
#   ④ .md 徽标（盒 24×24，字形 18×22，双色实心）
#      = 圆角方形 #167AB8 + 右上「L 形台阶」缺角内嵌浅蓝折片 #4196D6 +
#        白色「M」+ 白色下箭头（Markdown 官方标志的 M↓）
#      L 形台阶：顶边到 x15 → 下到 y6.5 → 右到 x21 → 下到底；折片三角 (15,1)-(21,6.5)-(15,6.5)
ATT_ICO = ('<svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" '
           'stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<path d="M8 1.5H2.6A1.1 1.1 0 0 0 1.5 2.6V12.9A1.1 1.1 0 0 0 2.6 14H10.4A1.1 1.1 0 0 0 11.5 12.9V5.75Z"/>'
           '<path d="M7 1.5v4.25H11.5"/>'
           '<path d="M3.7 7.6h4.5"/>'
           '<path d="M3.7 10.2h3.1"/></svg>')
DOC_ICO = ('<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
           'stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<path d="M4.5 1.5H18.8A1.5 1.5 0 0 1 20.3 3V15.6L16.6 21H4.5A1.5 1.5 0 0 0 3 19.5V3'
           'A1.5 1.5 0 0 1 4.5 1.5Z"/>'
           '<path d="M15 21v-5.25H20.3"/>'
           '<path d="M7.5 7.2h7.5"/>'
           '<path d="M7.5 11h7.5"/>'
           '<path d="M7.5 14.7h3.5"/></svg>')
WEB_ICO = ('<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
           'stroke-width="1.8" aria-hidden="true">'
           '<circle cx="12" cy="12" r="9.6"/>'
           '<ellipse cx="12" cy="12" rx="3.4" ry="9.6"/>'
           '<path d="M2.4 12h19.2" stroke-linecap="round"/></svg>')
MD_ICO = ('<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">'
          '<path class="td-ico-md-body" d="M3 1h12v5.5h6V23H3z"/>'
          '<path class="td-ico-md-fold" d="M15 1l6 5.5h-6z"/>'
          '<path class="td-ico-md-mark" d="M5 16.5v-5l3.35 3.5L11.7 11.5v5"/>'
          '<path class="td-ico-md-mark" d="M15.9 11.5v5"/>'
          '<path class="td-ico-md-mark is-solid" d="M13.9 14.15h4l-2 2.5z"/></svg>')
FILE_ICO = DOC_ICO   # 兼容旧引用（AI 消息文件卡用灰色折角文档）

# ---- 描述区配图（★ 第 28 轮第 2 项）----
# 设计稿的 .td-desc 里没有配图，这张「端到端交付链路」示意图是本次新增内容。
# 形态选择：内联 SVG → base64 挂到 <img src="data:image/svg+xml;base64,...">。
#   ① 页面其余部分都是「单文件自包含」（Vite 产物 + DS CSS 全部内联），外链 assets/*.svg 会破坏这个约定；
#   ② 换位图 base64 会让页面膨胀几百 KB，矢量图只有 ~6KB；
#   ③ <img> 里的 SVG 是独立文档、拿不到页面 CSS 变量 → 素材内色值字面写死（见 build-desc-fig.py 注释）。
# 素材由 mg-work/r28/build-desc-fig.py 生成到 mg-work/desc-fig.svg（改内容改脚本再重跑）。
DESC_FIG = io.open("mg-work/desc-fig.svg", encoding="utf-8").read()
DESC_IMG = "data:image/svg+xml;base64," + base64.b64encode(DESC_FIG.encode("utf-8")).decode("ascii")

# ---- 对话框三个弹层的图标与技能行（★ 第 28 轮第 4 项）----
# 图标路径统一从 mg-work/pop-icons.json 读入（该文件由 mg-work/r28/build-pop-icons.py 从
# pages/base.html 实测 DOM 抽取并压缩坐标生成）；色值一律走 currentColor + CSS 变量，不写死在 SVG 里。
POP_ICONS = json.load(io.open("mg-work/pop-icons.json", encoding="utf-8"))
SKILL_GOAL_ICO = ('<svg viewBox="0 0 14.076962 14.882011" width="14" height="14" fill="currentColor" '
                  'aria-hidden="true"><path d="%s"/></svg>' % POP_ICONS["skill_goal"])
SKILL_ROW_ICO = ('<svg viewBox="0 0 14 14" width="12" height="12" aria-hidden="true">'
                 '<path d="%s" fill="currentColor" transform="matrix(-1,0,0,1,26,0)"/></svg>' % POP_ICONS["skill_row"])
SKILL_X_ICO = ('<svg viewBox="0 0 10.4989 10.487117" width="12" height="12" aria-hidden="true">'
               '<path d="%s" fill="currentColor"/></svg>' % POP_ICONS["skill_x"])

# 技能面板内容（与 pages/base.html 实测面板一致）：Goal 行置顶且高亮，其后是分组标题 + 5 个技能行
SKILL_LIST = [
    ("systematic-debugging", "一个用于调试软件问题的结构化方法，强制要求在提出修复方案前进行根本原因分析。", "预置"),
    ("writing-skills", "将测试驱动开发方法应用于Claude技能文档创建。", "预置"),
    ("create-ex", "Distill an ex-partner into an AI Skill. Import WeChat history, photos, social media posts, generate...", "预置"),
    ("nuwa-skill", "女娲（Nuwa）：输入任何人的名字，自动调研 → 提取思维框架 → 生成可运行的视角技能。", "自有"),
    ("subagent-driven-development", "将实施计划分解为独立任务的工作流，每个任务由新的AI子代理处理，并经过规...", "自有"),
]


def skill_row(name, desc, tag=None, goal=False):
    cls = "td-skill-row is-goal is-active" if goal else "td-skill-row"
    ico = "td-skill-ico is-goal" if goal else "td-skill-ico"
    badge = '<span class="td-skill-tag">%s</span>' % tag if tag else ''
    return ('<div class="%s" role="option" tabindex="-1"><span class="%s">%s</span>'
            '<span class="td-skill-txt"><span class="td-skill-name">%s</span>'
            '<span class="td-skill-desc">%s</span></span>%s</div>'
            % (cls, ico, SKILL_GOAL_ICO if goal else SKILL_ROW_ICO, name, desc, badge))


SKILL_ROWS = "\n                ".join(
    [skill_row("Goal", "构建一个以实现目标为结果的任务，持续运行直到全部完成。", None, True),
     '<div class="td-skill-group">技能 Skills</div>']
    + [skill_row(n, d, t) for n, d, t in SKILL_LIST])
LINK_ICO = ('<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" '
            'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M6.4 9.6a2.6 2.6 0 0 0 3.7 0l2-2a2.6 2.6 0 0 0-3.7-3.7l-1 1"/>'
            '<path d="M9.6 6.4a2.6 2.6 0 0 0-3.7 0l-2 2a2.6 2.6 0 0 0 3.7 3.7l1-1"/></svg>')
# 分组标题图标（第 27 轮第 1 项，按设计稿 622:13950 实测校正）：
#   设计稿里三个分组的图标**不是同一个**（我们原来三处都用了「链接」图标，是错的）：
#     「2 个附件」  → 回形针（paperclip）
#     「3 个 AI 产物」→ 文件夹（folder）
#     「文件」      → 文件夹（folder）
#   实测：图标字形约 26×23（2x，即 13×11.5 @1x）→ 用 14px 盒；图标↔文字间距 10px(2x)=5px，
#   与现有 .td-sec-head gap 4px 基本一致；图标与标题文字同色（实测同为 (107,107,107)）→ 直接 currentColor 继承。
#
#   ⚠️ 第 27 轮补充校正：先用的 lucide 斜向回形针 / 闭合文件夹与设计稿形状不符。
#      对设计稿 622:13950 的图标做 ASCII 位图读取（阈值扫描）后确认真实笔画：
#        「2 个附件」= **竖直**回形针：一个竖直闭合外环（胶囊，7×11 @1x）＋ 内层 U ＋ 右侧游离端短线
#                      （@2x 四根竖线 x100-102 / 106-108 / 112-114 / 118-120，外环顶 y1222 封口、底 y1243 圆底）
#        「3 个 AI 产物」「文件」= **打开态**文件夹：带标签页的外轮廓（**左边／顶边／右边，底边不画**）
#                      ＋ 内嵌前板（完整圆角矩形，其底边即文件夹底边 → 底部只有一条线）
#                      （@2x：外左竖 x98 贯通 y1413..1432；页签顶 y1410 x99..107，主体顶 y1414..1416；
#                        内板顶 y1418 x101..122、内板左竖 x101）
#      形状选型在 mg-work/r27/cand.html 里逐一对渲染比对（A~H 八版），最终取候选 C / E。
CLIP_ICO = ('<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" '
            'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M2.9 5.5v4a3.5 3.5 0 0 0 7 0v-4a3.5 3.5 0 0 0-7 0z"/>'
            '<path d="M6.4 6.2v3.6a1.75 1.75 0 0 0 3.5 0V6.2"/>'
            '<path d="M12.7 3.2v7.6"/></svg>')
FOLDER_ICO = ('<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" '
              'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M2.6 12.6V5.3a1.5 1.5 0 0 1 1.5-1.5h2.4c.5 0 .97.25 1.25.67l.5.76c.28.42.75.67 1.25.67'
              'h3.9a1.5 1.5 0 0 1 1.5 1.5v5.2"/>'
              '<path d="M4.7 8.4h7.2a1.1 1.1 0 0 1 1.1 1.1v2a1.1 1.1 0 0 1-1.1 1.1H4.7a1.1 1.1 0 0 1-1.1-1.1'
              'v-2a1.1 1.1 0 0 1 1.1-1.1z"/></svg>')
# 「输出完成」前的图标（第 26 轮第 7 项）：实心圆 + 白色对勾，设计稿实测 12×12。
# 圆填 currentColor；对勾描边走 .td-ico-check → var(--color-bg-1)（不写死 #fff，保持 token 化）。
DONE_ICO = ('<svg viewBox="0 0 12 12" width="12" height="12" fill="none" aria-hidden="true">'
            '<circle cx="6" cy="6" r="6" fill="currentColor"/>'
            '<path class="td-ico-check" d="M3.3 6.1l1.9 1.85 3.5-3.75" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')
# 「Token 速率」前的图标（第 26 轮第 7 项）：仪表盘，设计稿实测 12×12（圆圈 + 指针 + 刻度）
GAUGE_ICO = ('<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" '
             'stroke-width="1.1" stroke-linecap="round" aria-hidden="true">'
             '<circle cx="6" cy="6" r="5"/>'
             '<path d="M6 6l2.4-2.4"/>'
             '<circle cx="6" cy="6" r=".75" fill="currentColor" stroke="none"/>'
             '<path d="M3.5 3.9l.75.75"/><path d="M2.9 6.5h1.05"/><path d="M9.1 6.5H8.05"/></svg>')


def fcard(name, size, big=False, ico=None, extra_cls=""):
    """附件 / AI 产物 / 文件 卡片：本身是链接（<a>），hover 背景加深一级。
    第 28 轮第 6 项：图标按文件类型逐个传入；大卡在图标与文字之间插入 1×24 竖分隔线。"""
    cls = "td-file td-file--lg" if big else "td-file"
    ico_cls = "td-file-ico" + ((" " + extra_cls) if extra_cls else "")
    if big:
        inner = ('<span class="td-file-sep" aria-hidden="true"></span>'
                 '<span class="td-file-body"><span class="td-file-tx">%s</span>'
                 '<span class="td-file-size">%s</span></span>' % (name, size))
    else:
        inner = '<span class="td-file-tx">%s</span>' % name
    return ('<a class="%s" href="#" title="%s"><span class="%s">%s</span>%s</a>'
            % (cls, name, ico_cls, ico or ATT_ICO, inner))


def tl(who, what, when):
    return ('<li><div class="td-tl-line1"><span class="td-tl-who">%s</span>'
            '<span class="td-tl-what">%s</span></div><span class="td-tl-time">%s</span></li>'
            % (who, what, when))


def attr(k, v, wrap=False):
    """一行左右属性。wrap=True -> 值列允许折行 2 行（第 27 轮第 3 项：来源需求链接要显示更多文字）。"""
    return ('<div class="td-attr-row%s"><span class="td-attr-k">%s</span>'
            '<span class="td-attr-v">%s</span></div>' % (' is-wrap' if wrap else '', k, v))


BADGE = ('<span class="giencoder-badge giencoder-badge-status">'
         '<span class="giencoder-badge-status-dot giencoder-badge-status-processing"></span>'
         '<span class="giencoder-badge-status-text">进行中</span></span>')

HTML = """<div class="td-root" role="region" aria-label="任务详情">
  <section class="td-left" aria-label="任务详细信息">
    <header class="td-bar">
      <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn td-back" type="button" aria-label="返回任务看板" data-td-back="1">
        <svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9.8 3.4L5.2 8l4.6 4.6"/></svg>
      </button>
      <span class="td-bar-title">任务详情</span>
      <div class="td-bar-actions">
        <button class="giencoder-btn giencoder-btn-primary giencoder-btn-size-small td-btn" type="button">开始任务</button>
        <span class="giencoder-popover-reference"><button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn" type="button" data-td-dispatch aria-haspopup="dialog" aria-expanded="false">转派</button></span>
        <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn" type="button" data-td-coop="1" aria-haspopup="dialog" aria-expanded="false">协作</button>
        <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn" type="button">编辑</button>
        <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn" type="button" aria-label="更多操作">
          <svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><circle cx="3.4" cy="8" r="1.3"/><circle cx="8" cy="8" r="1.3"/><circle cx="12.6" cy="8" r="1.3"/></svg>
        </button>
        <span class="td-bar-sep" aria-hidden="true"></span>
        <div class="td-bar-nav">
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn" type="button" aria-label="上一个任务" data-td-prev="1">
            <svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3.6 9.8L8 5.4l4.4 4.4"/></svg>
          </button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn" type="button" aria-label="下一个任务" data-td-next="1">
            <svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3.6 6.2L8 10.6l4.4-4.4"/></svg>
          </button>
        </div>
      </div>
    </header>
    <div class="td-left-body">
      <div class="td-main">
        <h1 class="td-title">端到端流程初始化：用户输入业务流程并触发全链路交付</h1>
        <div class="td-desc">
          <div class="td-desc-body" id="td-desc-body" data-td-desc="1">
            <p>第一步：梳理端到端交付链路</p>
            <div class="giencoder-image" data-td-desc-img="1">
              <div class="giencoder-image-mask-wrapper" role="button" tabindex="0" aria-label="预览大图：端到端交付链路示意图">
                <img class="giencoder-image-img" src="__DESCIMG__" width="1240" height="620" alt="端到端交付链路示意图：需求澄清、方案设计、任务拆分、开发实现、自测验证、联调验收、灰度发布、交付归档 共 8 个阶段">
                <div class="giencoder-image-mask" aria-hidden="true"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg><span>预览</span></div>
              </div>
            </div>
            <p>从业务方原始需求进入系统开始，到最终交付物归档为止，完整链路包含需求澄清、方案设计、任务拆分、开发实现、自测验证、联调验收、灰度发布与交付归档共 8 个阶段。每个阶段都需要明确输入、输出、责任人与准入准出条件，避免出现“任务已发起但无人认领”或“交付物缺失但流程已关闭”的情况。</p>
            <p>第二步：定义状态流转规则（启动整个流程）</p>
            <p>状态标识采用“交通灯”模式，方便直观管理：</p>
            <ul>
              <li>未开始：任务尚未启动。</li>
              <li>进行中：任务已启动，正在执行。</li>
              <li>已完成：任务成功完成并通过质量门禁。</li>
              <li>阻塞/异常：任务执行受阻，需要人工介入处理。</li>
            </ul>
            <p>第三步：设定交付物标准</p>
            <p>每类任务需产出对应交付物并登记到任务详情：需求类任务产出需求说明与验收标准；设计类任务产出概要设计与接口定义；开发类任务产出代码与单元测试报告；验证类任务产出测试用例与缺陷清单。所有交付物需带版本号与责任人，便于回溯。</p>
            <p>第四步：明确质量门禁</p>
            <p>进入“已完成”前必须通过三项门禁检查：交付物齐全且可访问、关键路径有自动化验证覆盖、遗留缺陷已评估且不影响验收。任一门禁未通过，任务自动回退到“进行中”并通知责任人。</p>
          </div>
        </div>
        <div class="td-expand"><span class="td-expand-line"></span><button class="giencoder-btn giencoder-btn-text giencoder-btn-size-small td-expand-btn" type="button" aria-expanded="false" aria-controls="td-desc-body" data-td-desc-toggle="1">展开全文</button><span class="td-expand-line"></span></div>
        <section class="td-sec">
          <div class="td-sec-head">__CLIPICO__2个附件</div>
          <div class="td-files">
            __ATT1__
            __ATT2__
          </div>
        </section>
        <section class="td-sec">
          <div class="td-sec-head">__FOLDERICO__3个 AI 产物</div>
          <div class="td-files">
            __AI1__
            __AI2__
            __AI3__
          </div>
        </section>
        <section class="td-sec">
          <div class="td-sec-head">__FOLDERICO__文件</div>
          <div class="td-files">
            __F1__
          </div>
        </section>
      </div>
      <aside class="td-side" aria-label="任务属性与动态">
        <section class="td-side-attr">
          <h2>任务属性</h2>
          <div class="td-attr">
            __A1__
            __A2__
            __A3__
            __A4__
            __A5__
            __A6__
            __A7__
          </div>
        </section>
        <section class="td-side-dyn">
          <h2>任务动态</h2>
          <ul class="td-tl">
            __T1__
            __T2__
            __T3__
            __T4__
            __T5__
          </ul>
        </section>
        <section class="td-side-foot" aria-label="任务记录信息">
          <div class="td-attr">
            __M1__
            __M2__
            __M3__
          </div>
        </section>
      </aside>
    </div>
  </section>
  <div class="td-gutter" role="separator" tabindex="0" aria-orientation="vertical" aria-label="调整 AI 会话栏宽度" aria-valuenow="480" aria-valuemin="48" aria-valuemax="1200" data-td-gutter="1"><span class="td-gutter-bar"></span></div>
  <aside class="td-right" aria-label="AI 会话">
    <div class="td-right-inner">
      <header class="td-right-bar">
        <div class="td-right-head">
          <div class="td-right-title">端到端流程初始化：用户输入业务流程并触发全链路交付</div>
          <div class="td-right-time">2026/08/01 11:26</div>
        </div>
        <div class="td-right-acts">
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn" type="button" aria-label="新会话"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-plus" aria-hidden="true"><path d="M5 12h14"/><path d="M12 5v14"/></svg></button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn" type="button" aria-label="会话历史"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-history" aria-hidden="true"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/></svg></button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn" type="button" aria-label="全屏" aria-pressed="false" title="全屏" data-td-fullscreen="1"><svg class="td-ico-max" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/></svg><svg class="td-ico-min" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 3v3a2 2 0 0 1-2 2H3"/><path d="M21 8h-3a2 2 0 0 1-2-2V3"/><path d="M3 16h3a2 2 0 0 1 2 2v3"/><path d="M16 21v-3a2 2 0 0 1 2-2h3"/></svg></button>
        </div>
      </header>
      <div class="td-chat">
        <div class="td-chat-inner">
          <div class="td-msg-user">请帮我先分析一下这个任务</div>
          <div class="td-msg-ai">
            <div class="td-ai-head">
              <span class="td-ai-avatar"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2.2l1.8 4 4 1.8-4 1.8L8 13.8l-1.8-4-4-1.8 4-1.8z"/></svg></span>
              <span class="td-ai-name">艾迪</span>
            </div>
            <div class="td-ai-meta">
              <a href="#">__LINKICO__思考过程</a>
              <span class="td-sep"></span>
              <a href="#">任务完成，耗时 28m12s</a>
            </div>
            <p>好的，收到您的需求。这是一个典型的“从需求到交付”的端到端流程初始化场景。我将为您设计一个完整的交付状态跟踪表，并定义启动整个流程所需的初始状态和关键节点。</p>
            <p>我先把几个核心不确定性列出来，请你选择倾向，不确定的地方我会标注我的判断。</p>
            __AIFILE__
            <div class="td-ai-foot"><span class="td-ai-foot-item"><span class="td-ai-foot-ico">__DONEICO__</span><span>输出完成</span></span><span class="td-sep"></span><span class="td-ai-foot-item"><span class="td-ai-foot-ico">__GAUGEICO__</span><span>Token 速率：256/s</span></span></div>
          </div>
        </div>
      </div>
        <!-- 复用基础工作台的对话框模块（pages/base.html，结构与类名一致） -->
        <div class="td-composer">
          <div class="relative flex w-full flex-col rounded-[16px] border bg-white p-3 transition-colors" style="border-color: var(--color-border-2); box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);">
            <textarea rows="1" placeholder="描述你的任务，/ 调用技能，@引用文件" aria-label="输入消息" class="min-w-0 resize-none bg-transparent text-sm leading-[22px] [color:var(--color-text-1)] outline-none placeholder:[color:var(--color-text-3)] min-h-[96px]"></textarea>
            <div class="mt-auto flex items-center justify-between">
              <div class="flex items-center gap-[8px]">
                <div class="giencoder-select" style="flex-direction: row; align-items: flex-start; position: relative;">
                  <button type="button" aria-label="添加" aria-haspopup="menu" aria-expanded="false" data-td-add-btn="1" class="flex size-8 items-center justify-center rounded-full border border-[var(--color-border-1)] text-[var(--color-text-2)] transition-colors hover:bg-[var(--color-fill-1)] hover:[color:var(--color-text-1)]"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-plus size-[14px]" aria-hidden="true"><path d="M5 12h14"></path><path d="M12 5v14"></path></svg></button>
                  <div role="menu" aria-label="添加内容" class="td-add-pop" data-td-add-pop="1" hidden>
                    <div role="menuitem" tabindex="-1" class="td-add-item" data-td-add="file"><svg viewBox="0 0 14 14" width="14" height="14" fill="currentColor" fill-rule="evenodd" aria-hidden="true"><path d="__ADDFILE__"/></svg><span>添加本地文件</span></div>
                    <span class="td-add-sep" aria-hidden="true"></span>
                    <div role="menuitem" tabindex="-1" class="td-add-item" data-td-add="kb"><svg viewBox="0 0 14 14" width="14" height="14" fill="currentColor" fill-rule="evenodd" aria-hidden="true"><path d="__ADDKB__"/></svg><span>知识库</span></div>
                  </div>
                </div>
                <button type="button" aria-label="技能" aria-haspopup="listbox" aria-expanded="false" data-td-skill-btn="1" class="flex size-8 items-center justify-center rounded-full border border-[var(--color-border-1)] text-[var(--color-text-2)] transition-colors hover:bg-[var(--color-fill-1)] hover:[color:var(--color-text-1)]"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-wrench size-[14px]" aria-hidden="true"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.106-3.105c.32-.322.863-.22.983.218a6 6 0 0 1-8.259 7.057l-7.91 7.91a1 1 0 0 1-2.999-3l7.91-7.91a6 6 0 0 1 7.057-8.259c.438.12.54.662.219.984z"></path></svg></button>
                <div class="avatar-wrap relative flex items-center">
                  <button type="button" aria-label="数字分身" aria-pressed="true" class="flex h-8 items-center gap-[2px] rounded-full px-3 py-[5px] text-[14px] leading-[19px] transition-colors" style="background: rgb(236, 242, 255); color: rgb(55, 112, 247); border: 1px solid rgb(211, 226, 255);"><svg viewBox="0 0 14 14" width="14" height="14" class="size-[14px]"><path d="M6.988754947683716,13.43000001192093C5.103876847683716,13.43000001192093,3.4284298476837156,12.17341601192093,2.9048526476837155,10.497968511920929L2.590706447683716,10.812115011920929C2.381275537683716,11.02154501192093,1.9624137876837158,11.02154501192093,1.6482674076837158,10.812115011920929C1.334121017683716,10.602683011920929,1.4388364836837158,10.183822411920929,1.6482674076837158,9.869675411920928L2.6954218476837157,8.822521011920928L2.6954218476837157,7.984796811920929C2.2765598876837156,7.670650811920929,2.067129017683716,7.147073111920929,2.067129017683716,6.623495911920929L2.067129017683716,3.586747711920929C2.067129017683716,2.539593411920929,2.9048526476837155,1.701869811920929,3.952006847683716,1.701869811920929L6.360462447683716,1.701869811920929L6.360462447683716,1.1782926319209288C6.360462447683716,0.8641463219209289,6.674608947683716,0.550000011920929,6.988754947683716,0.550000011920929C7.302901547683716,0.550000011920929,7.617047547683716,0.8641463219209289,7.617047547683716,1.1782926319209288L7.617047547683716,1.701869811920929L10.025503347683715,1.701869811920929C11.072657847683717,1.701869811920929,11.910381047683716,2.539593411920929,11.910381047683716,3.586747711920929L11.910381047683716,6.623495911920929C11.910381047683716,7.147073111920929,11.700949047683716,7.670649811920929,11.282088547683715,7.984796811920929L11.282088547683715,8.822521011920928L12.329243047683716,9.869675411920928C12.538674047683715,10.079107111920928,12.538674047683715,10.497968511920929,12.329243047683716,10.812115011920929C12.119811047683715,11.126262011920929,11.700951047683716,11.02154501192093,11.386802947683716,10.812115011920929L11.072657847683717,10.497968511920929C10.549079147683717,12.17341601192093,8.873632647683717,13.43000001192093,6.988754947683716,13.43000001192093ZM3.9520075476837158,9.13666611192093C3.9520075476837158,10.81211401192093,5.313308247683716,12.173413011920928,6.988754947683716,12.173413011920928C8.664201947683715,12.173413011920928,10.025503347683715,10.81211401192093,10.025503347683715,9.13666611192093L10.025503347683715,8.50837351192093L3.9520075476837158,8.50837351192093L3.9520075476837158,9.13666611192093ZM3.9520075476837158,3.063170711920929C3.6378612476837158,3.063170711920929,3.3237144476837157,3.2726017119209287,3.3237144476837157,3.586747911920929L3.3237144476837157,6.623495911920929C3.3237144476837157,6.937641911920929,3.6378610476837157,7.251788411920929,3.952006847683716,7.251788411920929L10.025502447683715,7.251788411920929C10.339648447683716,7.251788411920929,10.549078247683715,7.042357311920929,10.549078247683715,6.728210711920929L10.549078247683715,3.586747511920929C10.549078247683715,3.272601211920929,10.339647547683716,3.0631702119209288,10.025502447683715,3.0631702119209288L3.9520075476837158,3.063170711920929ZM8.873633647683715,6.099919111920929C8.559487547683716,6.099919111920929,8.245341047683716,5.785772111920929,8.245341047683716,5.471626611920929L8.245341047683716,4.843334011920929C8.140625747683716,4.424471911920929,8.454771747683715,4.1103256119209295,8.873633647683715,4.1103256119209295C9.292495947683715,4.1103256119209295,9.501925747683716,4.424471911920929,9.501925747683716,4.738618211920929L9.501925747683716,5.366911211920929C9.501925747683716,5.785772111920929,9.187779647683715,6.099919111920929,8.873633647683715,6.099919111920929ZM5.103877547683716,6.099919111920929C4.789731547683716,6.099919111920929,4.475585247683716,5.785772111920929,4.475585247683716,5.471626611920929L4.475585247683716,4.843334011920929C4.475585247683716,4.424471911920929,4.789731547683716,4.1103256119209295,5.103877547683716,4.1103256119209295C5.418023847683716,4.1103256119209295,5.732170347683716,4.424471911920929,5.732170347683716,4.738618211920929L5.732170347683716,5.366911211920929C5.836885647683716,5.785772111920929,5.5227391476837155,6.099919111920929,5.103877547683716,6.099919111920929Z" fill="currentColor" fill-rule="evenodd"></path></svg>艾迪</button>
                  <div role="tooltip" class="avatar-tooltip">停用数字分身</div>
                </div>
                <div class="giencoder-select" style="width: 96px; flex-shrink: 0;">
                  <div class="giencoder-select-view select-view-ghost" tabindex="0" role="combobox" aria-haspopup="listbox" aria-expanded="false" style="height: 32px; min-height: 32px; border: 1px solid var(--color-border-1); border-radius: 32px; background-color: transparent; box-shadow: none; padding: 5px 12px; gap: 4px;">
                    <div class="giencoder-select-selection" style="gap: 4px;"><span class="giencoder-select-view-text">标准模式</span></div>
                    <span class="giencoder-select-suffix"><svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M2.6 4.6L6 8l3.4-3.4"/></svg></span>
                  </div>
                  <div class="giencoder-select-popup">
                    <ul class="giencoder-select-option-list" role="listbox">
                      <li class="giencoder-select-option giencoder-select-option-selected" role="option" aria-selected="true">标准模式</li>
                      <li class="giencoder-select-option" role="option" aria-selected="false">专家模式</li>
                    </ul>
                  </div>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <div class="giencoder-select" style="width: fit-content; max-width: 200px; flex-shrink: 0; margin-left: auto;">
                  <div class="giencoder-select-view select-view-ghost" tabindex="0" role="combobox" aria-haspopup="listbox" aria-expanded="false" style="height: 32px; min-height: 32px; border: none; border-radius: 32px; gap: 2px; padding: 0 12px;">
                    <div class="giencoder-select-selection" style="gap: 2px;"><span class="giencoder-select-view-text">DeepSeek-V4-Pro</span></div>
                    <span class="giencoder-select-suffix"><svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M2.6 4.6L6 8l3.4-3.4"/></svg></span>
                  </div>
                  <div class="giencoder-select-popup">
                    <ul class="giencoder-select-option-list" role="listbox" aria-label="大模型选择">
                      <li class="giencoder-select-option giencoder-select-option-selected" role="option" aria-selected="true">DeepSeek-V4-Pro</li>
                      <li class="giencoder-select-option" role="option" aria-selected="false">GLM-5.2-公司共用</li>
                      <li class="giencoder-select-option giencoder-select-option-disabled" role="option" aria-selected="false" aria-disabled="true">Qwen 3.8-max</li>
                      <li class="giencoder-select-option" role="option" aria-selected="false">Kimi-2.6</li>
                    </ul>
                  </div>
                </div>
                <button type="button" aria-label="优化提示词" class="flex size-8 items-center justify-center rounded-full transition-colors hover:bg-[var(--color-fill-1)]" style="background: rgb(255, 255, 255);"><svg viewBox="0 0 14.08 14.06" width="14" height="14" fill="none"><path d="M9.1414957,4.6432233C8.8303785,4.9347887,8.3439808,4.9266973,8.0427332,4.6249452C7.7414865,4.3231936,7.7342105,3.8367827,8.0262985,3.5261555L9.7009659,1.8514888C10.009434,1.5430192,10.509562,1.5430192,10.818031,1.8514888C11.126502,2.1599586,11.126502,2.6600869,10.818032,2.9685569L9.1405592,4.6432233L9.1414957,4.6432233Z" fill="#BEBEBE"></path><path d="M11.878967,7.1103153L9.5091734,7.1103153C9.0621662,7.1256995,8.6914234,6.7674994,8.6914234,6.3202286C8.6914234,5.8729568,9.0621662,5.5147567,9.5091734,5.5301414L11.879902,5.5301414C12.326908,5.5147567,12.697651,5.8729568,12.697651,6.3202286C12.697649,6.7674994,12.326908,7.1256995,11.879902,7.1103153L11.878967,7.1103153Z" fill="#BEBEBE"></path><path d="M4.1137528,4.8761797C3.9033761,4.8776922,3.7011769,4.7947903,3.5524123,4.6460304L1.8777457,2.971364C1.569276,2.6628945,1.569276,2.162766,1.8777457,1.8542962C2.1862154,1.5458264,2.6863437,1.5458263,2.9948137,1.854296L4.6694798,3.5289626C4.8958349,3.7551589,4.9632897,4.0956059,4.8402843,4.3910227C4.717279,4.68644,4.4281397,4.8784089,4.1081395,4.8771148L4.1137528,4.8761797Z" fill="#BEBEBE"></path><path d="M6.3497601,0C6.7863712,0,7.1403146,0.35394344,7.1403146,0.79055488L7.1403146,3.1612837C7.1256599,3.5870585,6.7762556,3.9246454,6.3502278,3.9246454C5.9242005,3.9246454,5.5747943,3.5870588,5.5601397,3.1612837L5.5601397,0.79055488C5.5601397,0.35430831,5.9135146,0.00051608856,6.3497601,0Z" fill="#BEBEBE"></path><path d="M0.819619,5.5301414L3.1884768,5.5301414C3.6354835,5.5147562,4.0062251,5.8729568,4.0062251,6.3202286C4.0062251,6.7674994,3.6354835,7.1256995,3.1884768,7.1103153L0.81774795,7.1103153C0.37074119,7.1256995,0,6.7674994,0,6.3202286C2.5033659e-8,5.8729568,0.37074125,5.5147562,0.81774795,5.5301414L0.819619,5.5301414Z" fill="#BEBEBE"></path><path d="M3.5570905,7.9972339C3.8655162,7.6885071,4.3658547,7.6883845,4.6744308,7.9969606C4.9830074,8.3055372,4.9828858,8.8058758,4.6741581,9.1143007L2.9994922,10.788968C2.688375,11.08053,2.2019811,11.072435,1.9007362,10.770686C1.5994915,10.468936,1.5922134,9.9825287,1.8842953,9.6718998L3.5570905,7.9972339Z" fill="#BEBEBE"></path><path d="M6.3497601,8.6886187C6.7863712,8.6886187,7.1403146,9.0425615,7.1403146,9.4791737L7.1403146,11.849901C7.1256599,12.275676,6.7762556,12.613264,6.3502278,12.613264C5.9242005,12.613264,5.5747943,12.275676,5.5601397,11.849901L5.5601397,9.4791737C5.5601397,9.0429258,5.9135141,8.6891346,6.3497601,8.6886187Z" fill="#BEBEBE"></path><path d="M5.9540148,5.9240155C6.2626376,5.6159139,6.7624602,5.6159139,7.0710826,5.9240155L9.1424294,7.9953628L10.817097,9.6700287L13.785653,12.650749C14.077717,12.96138,14.070429,13.447771,13.769192,13.749513C13.467955,14.051255,12.981577,14.059359,12.670459,13.767816L5.9577575,7.0410843C5.6478443,6.7339692,5.6457491,6.2337155,5.9530797,5.9240155L5.9540148,5.9240155Z" fill="#BEBEBE"></path></svg></button>
                <button type="button" aria-label="发送" disabled class="flex shrink-0 !size-8 !rounded-full !p-0 items-center justify-center transition-colors" style="background: var(--color-fill-3); cursor: not-allowed; opacity: 0.5;"><svg viewBox="8.82 10.73 14.08 11.38" width="14" height="14" fill="none"><path d="M9.028238606,34.839137L11.6378174,29.1173639C11.6825285,28.9479885,11.6825285,28.7663059,11.6378174,28.6000094L9.028238606,22.87514764C8.88469238,22.32391092,9.31768426,21.81578781,9.7224375,22.065230064L19.998936,28.4367857C20.267201,28.6030817,20.267201,29.1050444,19.998936,29.2713394L9.7224375,35.649054C9.31768426,35.898499,8.88469242,35.390374,9.028238606,34.839137Z" fill="#FFFFFF" transform="matrix(0,-1,1,0,-13,31)"></path></svg></button>
              </div>
            </div>
            <!-- 技能面板（★ 第 28 轮第 4 项）：结构与内容对齐 pages/base.html 实测面板。
                 放在对话框根容器内、absolute 定位于其上方（bottom: calc(100% + 8px)）。 -->
            <div class="giencoder-select td-skill-pop" role="listbox" aria-label="技能选择" data-td-skill-pop="1" hidden>
              <div class="td-skill-list">
                __SKILLROWS__
              </div>
              <button type="button" class="td-skill-x" aria-label="关闭技能面板" data-td-skill-close="1">__SKILLXICO__</button>
              <div class="td-skill-foot">
                <div>
                  <button type="button" class="giencoder-btn giencoder-btn-size-default giencoder-btn-secondary">安装技能</button>
                  <button type="button" class="giencoder-btn giencoder-btn-size-default giencoder-btn-secondary">管理技能</button>
                </div>
              </div>
            </div>
          </div>
        </div>
    </div>
    <button class="td-collapsed" type="button" aria-label="展开 AI 会话" data-td-expand="1">
      <span>展</span><span>开</span><span>AI</span><span>会</span><span>话</span>
    </button>
  </aside>
</div>

<!-- ★ 第 32 轮第 5 项：顶栏「协作」→ 分步模态弹窗（设计稿节点 622:20081）
     全部用 DS 契约组装（Modal / Steps / Checkbox / List / Avatar / Input / Button），
     结构说明与设计稿实测真值见上方 CSS 段注释。
     显隐开关 = 根节点 .td-coop 的 is-open + hidden（配合 <html data-td-coop-open> 供 Esc 链判断）。 -->
<div class="td-coop" hidden>
  <div class="giencoder-modal-wrapper">
    <div class="giencoder-modal-mask" data-td-coop-mask="1"></div>
    <div class="giencoder-modal td-coop-dialog" role="dialog" aria-modal="true" aria-label="任务协作" tabindex="-1">
      <div class="giencoder-modal-header">
        <span class="giencoder-modal-title">任务协作</span>
        <button class="giencoder-modal-close-btn" type="button" aria-label="Close" data-td-coop-close="1"><svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="M3.8 3.8l8.4 8.4M12.2 3.8l-8.4 8.4"/></svg></button>
      </div>
      <div class="giencoder-steps giencoder-steps-horizontal td-coop-steps" role="list" aria-label="协作流程">
        <div class="giencoder-steps-item is-active" role="listitem" aria-current="step" data-td-step="1">
          <span class="giencoder-steps-icon" aria-hidden="true"><svg viewBox="0 0 14 14" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M2.6 7.5l3 3L11.4 4.2"/></svg></span>
          <span class="giencoder-steps-content"><span class="giencoder-steps-title">选择阶段产物</span></span>
        </div>
        <div class="giencoder-steps-item" role="listitem" data-td-step="2">
          <span class="giencoder-steps-icon" aria-hidden="true"><svg viewBox="0 0 14 14" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M2.6 7.5l3 3L11.4 4.2"/></svg></span>
          <span class="giencoder-steps-content"><span class="giencoder-steps-title">选择协作者</span></span>
        </div>
      </div>
      <div class="td-coop-dvd" role="separator"><span class="td-coop-dvd-tx" data-td-coop-hint="1">选择需要流转到下一阶段的协作产物</span></div>
      <div class="giencoder-modal-content">
        <div class="td-coop-pane" data-td-pane="1">
          <div class="giencoder-list td-coop-list giencoder-scroll-thin" role="group" aria-label="阶段产物">
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox" checked><span class="giencoder-checkbox-mask"></span><span class="td-coop-tx">研发协同主页-空间.html</span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox" checked><span class="giencoder-checkbox-mask"></span><span class="td-coop-tx">设置-工作项-关系-了解更多.html</span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox" checked><span class="giencoder-checkbox-mask"></span><span class="td-coop-tx">用户故事.md</span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox" checked><span class="giencoder-checkbox-mask"></span><span class="td-coop-tx">AGENTS.md</span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox" checked><span class="giencoder-checkbox-mask"></span><span class="td-coop-tx">README.md</span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox" checked><span class="giencoder-checkbox-mask"></span><span class="td-coop-tx">SKILL.md</span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox" checked><span class="giencoder-checkbox-mask"></span><span class="td-coop-tx">附件1.xlsx</span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox" checked><span class="giencoder-checkbox-mask"></span><span class="td-coop-tx">附件2.rar</span></span></label>
          </div>
        </div>
        <div class="td-coop-pane" data-td-pane="2" hidden>
          <div class="giencoder-input-wrapper" data-size="medium">
            <span class="giencoder-input-prefix" aria-hidden="true"><svg viewBox="0 0 14 14" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><circle cx="6.1" cy="6.1" r="4.35"/><path d="M9.3 9.3l3.1 3.1"/></svg></span>
            <input class="giencoder-input" type="text" placeholder="搜索协作者" aria-label="搜索协作者" autocomplete="off">
          </div>
          <div class="giencoder-list td-coop-members giencoder-scroll-thin" role="group" aria-label="协作者">
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small" data-td-midx="0"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox"><span class="giencoder-checkbox-mask"></span></span><span class="giencoder-list-item-meta"><span class="giencoder-avatar giencoder-avatar-circle giencoder-avatar-text td-coop-av" style="--avatar-bg: var(--avatar-bg-1)" aria-hidden="true">铭</span><span class="giencoder-list-item-title td-coop-mname">邵禹铭 <span class="td-coop-mid">(P0098602)</span></span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small" data-td-midx="1"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox"><span class="giencoder-checkbox-mask"></span></span><span class="giencoder-list-item-meta"><span class="giencoder-avatar giencoder-avatar-circle giencoder-avatar-text td-coop-av" style="--avatar-bg: var(--avatar-bg-2)" aria-hidden="true">怡</span><span class="giencoder-list-item-title td-coop-mname">秦怡 <span class="td-coop-mid">(P0098603)</span></span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small" data-td-midx="2"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox"><span class="giencoder-checkbox-mask"></span></span><span class="giencoder-list-item-meta"><span class="giencoder-avatar giencoder-avatar-circle giencoder-avatar-text td-coop-av" style="--avatar-bg: var(--avatar-bg-3)" aria-hidden="true">毅</span><span class="giencoder-list-item-title td-coop-mname">韩佳毅 <span class="td-coop-mid">(P0098604)</span></span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small" data-td-midx="3"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox"><span class="giencoder-checkbox-mask"></span></span><span class="giencoder-list-item-meta"><span class="giencoder-avatar giencoder-avatar-circle giencoder-avatar-text td-coop-av" style="--avatar-bg: var(--avatar-bg-4)" aria-hidden="true">帆</span><span class="giencoder-list-item-title td-coop-mname">顾帆 <span class="td-coop-mid">(P0098605)</span></span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small" data-td-midx="4"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox"><span class="giencoder-checkbox-mask"></span></span><span class="giencoder-list-item-meta"><span class="giencoder-avatar giencoder-avatar-circle giencoder-avatar-text td-coop-av" style="--avatar-bg: var(--avatar-bg-5)" aria-hidden="true">怡</span><span class="giencoder-list-item-title td-coop-mname">姜嘉怡 <span class="td-coop-mid">(P0098606)</span></span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small" data-td-midx="5"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox"><span class="giencoder-checkbox-mask"></span></span><span class="giencoder-list-item-meta"><span class="giencoder-avatar giencoder-avatar-circle giencoder-avatar-text td-coop-av" style="--avatar-bg: var(--avatar-bg-6)" aria-hidden="true">甜</span><span class="giencoder-list-item-title td-coop-mname">朱甜 <span class="td-coop-mid">(P0098607)</span></span></span></label>
            <label class="giencoder-list-item giencoder-list-item-hoverable td-coop-row" data-size="small" data-td-midx="6"><span class="giencoder-checkbox td-coop-cb"><input class="giencoder-checkbox-input" type="checkbox"><span class="giencoder-checkbox-mask"></span></span><span class="giencoder-list-item-meta"><span class="giencoder-avatar giencoder-avatar-circle giencoder-avatar-text td-coop-av" style="--avatar-bg: var(--avatar-bg-7)" aria-hidden="true">辰</span><span class="giencoder-list-item-title td-coop-mname">齐瑞辰 <span class="td-coop-mid">(P0098608)</span></span></span></label>
          </div>
        </div>
      </div>
      <div class="giencoder-modal-footer">
        <span class="td-coop-count" data-td-coop-count="1"></span>
        <div class="td-coop-btns">
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default td-coop-btn" type="button" data-td-coop-cancel="1">取消</button>
          <button class="giencoder-btn giencoder-btn-primary giencoder-btn-size-default td-coop-btn" type="button" data-td-coop-next="1">下一步</button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default td-coop-btn" type="button" data-td-coop-prev="1" hidden>上一步</button>
          <button class="giencoder-btn giencoder-btn-primary giencoder-btn-size-default td-coop-btn" type="button" data-td-coop-submit="1" hidden>提交</button>
        </div>
      </div>
    </div>
  </div>
</div>"""

repl = {
    "__LINKICO__": LINK_ICO,
    "__CLIPICO__": CLIP_ICO,
    "__FOLDERICO__": FOLDER_ICO,
    "__FILEICO__": FILE_ICO,
    "__DESCIMG__": DESC_IMG,
    "__SKILLROWS__": SKILL_ROWS,
    "__SKILLXICO__": SKILL_X_ICO,
    "__ADDFILE__": POP_ICONS["add_file"],
    "__ADDKB__": POP_ICONS["add_kb"],
    "__DONEICO__": DONE_ICO,
    "__GAUGEICO__": GAUGE_ICO,
    "__ATT1__": fcard("端到端流程初始化：用户输入业务流程并触发全链路交付.docx", ""),
    "__ATT2__": fcard("TaskBoard.png", ""),
    "__AI1__": fcard("prd-template.html", "128KB", True, WEB_ICO, "is-web"),
    "__AI2__": fcard("端到端初始化 - 任务分析报告.md", "128KB", True, DOC_ICO),
    "__AI3__": fcard("spec-template.md", "128KB", True, MD_ICO),
    "__F1__": fcard("概要设计-Steps.md", "17KB", True, MD_ICO),
    "__AIFILE__": fcard("端到端初始化 - 任务分析报告.md", "128KB", True, DOC_ICO),
    "__A1__": attr("状态", BADGE),
    "__A2__": attr("执行人", "邵禹铭"),
    "__A3__": attr("优先级", '<span class="giencoder-tag giencoder-tag-danger td-tag-prio">'
                           '<span class="giencoder-tag-content">高优先级</span></span>'),
    "__A4__": attr("项目", "演练指挥系统"),
    "__A5__": attr("来源需求",
                   '<a class="td-attr-link" href="#">%sGienX端到端初始化：用户输入业务流程描述，自动生成需求条目并触发全链路交付</a>' % LINK_ICO,
                   True),
    "__A6__": attr("实际开始", "2026/08/01 10:12"),
    "__A7__": attr("实际完成", "2026/08/12 15:27"),
    "__T1__": tl("Agent", "完成了任务开发", "刚刚"),
    "__T2__": tl("Agent", "已确认任务目标和优先级", "半小时前"),
    "__T3__": tl("邵禹铭", "状态更新为进行中", "昨天 10:02"),
    "__T4__": tl("邵禹铭", "补充了需求说明材料", "08/12 09:27"),
    "__T5__": tl("系统", "已同步最新处理进展", "08/11 16:51"),
    "__M1__": attr("创建者", "秦怡"),
    "__M2__": attr("创建时间", "2026/08/12 15:27"),
    "__M3__": attr("最后更新", "半小时前"),
}
for k, v in repl.items():
    HTML = HTML.replace(k, v)

# ============================== JS ==============================
JS = r"""<script>
(function () {
  var KB_HTML = [
__LINES__
].join('\n');

  function bindDetail(wrap) {
    var root = wrap.querySelector('.td-root');
    if (!root) return;
    /* 返回任务看板 */
    var back = wrap.querySelector('[data-td-back]');
    if (back) back.addEventListener('click', function () { location.href = 'kanban.html'; });

    /* 描述区：展开全文 / 收起（第 25 轮第 4 项：加 max-height 微动效）
       max-height 从 px → none 不可动画，所以全程只用像素值过渡，
       过渡结束后才把内联值清掉（回到 CSS 的 374px / none）。 */
    var descBody = wrap.querySelector('[data-td-desc]');
    var descBtn = wrap.querySelector('[data-td-desc-toggle]');
    if (descBody && descBtn) {
      var COLLAPSED_H = parseFloat(getComputedStyle(descBody).maxHeight) || 374;
      var descBusy = false;
      function onDescEnd(fn) {
        var done = false;
        function once() { if (done) return; done = true; descBody.removeEventListener('transitionend', once); fn(); }
        descBody.addEventListener('transitionend', once);
        setTimeout(once, 420);   /* 兜底：transitionend 可能因高度无变化而不触发 */
      }
      descBtn.addEventListener('click', function () {
        if (descBusy) return;
        var open = !descBody.classList.contains('is-open');
        var curH = descBody.getBoundingClientRect().height;
        descBusy = true;
        descBody.classList.add('is-animating');
        if (open) {
          /* 先离屏量出展开后的真实高度（临时 max-height:none），再回到当前高度起跑 */
          descBody.style.maxHeight = 'none';
          var fullH = descBody.getBoundingClientRect().height;
          descBody.style.maxHeight = curH + 'px';
          descBody.classList.add('is-open');
          requestAnimationFrame(function () { descBody.style.maxHeight = fullH + 'px'; });
          onDescEnd(function () {
            descBusy = false;
            descBody.classList.remove('is-animating');
            if (descBody.classList.contains('is-open')) descBody.style.maxHeight = 'none';
          });
        } else {
          descBody.style.maxHeight = curH + 'px';   /* 从 none 落到确定像素值，才能起跑 */
          descBody.classList.remove('is-open');
          requestAnimationFrame(function () { descBody.style.maxHeight = COLLAPSED_H + 'px'; });
          onDescEnd(function () {
            descBusy = false;
            descBody.classList.remove('is-animating');
            descBody.style.maxHeight = '';
          });
        }
        descBtn.textContent = open ? '收起' : '展开全文';
        descBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }

    /* AI 会话全屏 / 取消全屏（第 26 轮第 5 项）：形态完全由 CSS 的 .td-root.is-fullscreen 决定，
       这里只切类并同步按钮语义（aria-label / title / aria-pressed），图标显隐由 .td-ico-max/.td-ico-min 控制。 */
    var fsBtn = wrap.querySelector('[data-td-fullscreen]');
    if (fsBtn) {
      fsBtn.addEventListener('click', function () {
        var on = root.classList.toggle('is-fullscreen');
        fsBtn.setAttribute('aria-label', on ? '取消全屏' : '全屏');
        fsBtn.setAttribute('title', on ? '取消全屏' : '全屏');
        fsBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }

    /* ================= 对话框三个弹层（★ 第 28 轮第 4 项） =================
       行为对齐 pages/base.html 实测：
         · 点「添加」按钮 → 在按钮上方弹出 180×92 菜单（两项 + 分隔线）；再点按钮关闭；
         · 点「技能」按钮 → 在对话框上方弹出 760×320 面板（Goal + 技能列表 + 底部两个按钮）；
         · 点「大模型 / 标准模式」视图 → 展开 DS Select 弹层；
         · 点菜单项 / 技能行 / 模型项 → **只关闭弹层**（base 实测：不写 textarea、也没有隐藏的
           input[type=file]，所以「添加本地文件」这里同样只关闭，保持一致）；
         · 点弹层外部 → 全部关闭；
         · Esc → 全部关闭。⚠️ base 里 Esc 不关技能面板，但本页 Esc 是「返回任务看板」的全局快捷键，
           必须先吃掉这次 Esc，否则会误跳转 → 用自定义事件 td:close-popovers 与页尾脚本约定（见 TAIL）。 */
    var opAdd = null, opSkill = null, opSel = null;
    function popFlag() { document.documentElement.toggleAttribute('data-td-pop-open', !!(opAdd || opSkill || opSel)); }
    function closeAdd() { if (!opAdd) return; opAdd.pop.hidden = true; opAdd.btn.setAttribute('aria-expanded', 'false'); opAdd = null; popFlag(); }
    function closeSkill() { if (!opSkill) return; opSkill.pop.hidden = true; opSkill.btn.setAttribute('aria-expanded', 'false'); opSkill = null; popFlag(); }
    /* ⚠️ DS Select 弹层的开合唯一开关是 `.giencoder-popup-open`（ui-controls.css），
       不要用内联 display（display:block 但 opacity:0/visibility:hidden ⇒ 看不见）。 */
    function closeSel() { if (!opSel) return; opSel.pop.classList.remove('giencoder-popup-open'); opSel.view.setAttribute('aria-expanded', 'false'); opSel = null; popFlag(); }
    function closePops() { closeAdd(); closeSkill(); closeSel(); }

    var addBtn = wrap.querySelector('[data-td-add-btn]');
    var addPop = wrap.querySelector('[data-td-add-pop]');
    if (addBtn && addPop) {
      addBtn.addEventListener('click', function () {
        closeSkill(); closeSel();
        if (opAdd) { closeAdd(); return; }
        addPop.hidden = false;
        addBtn.setAttribute('aria-expanded', 'true');
        opAdd = { btn: addBtn, pop: addPop }; popFlag();
        var f = addPop.querySelector('[role="menuitem"]');
        if (f) f.focus();
      });
      Array.prototype.forEach.call(addPop.querySelectorAll('[role="menuitem"]'), function (it) {
        it.addEventListener('click', function () { closeAdd(); });
      });
    }

    var skillBtn = wrap.querySelector('[data-td-skill-btn]');
    var skillPop = wrap.querySelector('[data-td-skill-pop]');
    if (skillBtn && skillPop) {
      skillBtn.addEventListener('click', function () {
        closeAdd(); closeSel();
        if (opSkill) { closeSkill(); return; }
        skillPop.hidden = false;
        skillBtn.setAttribute('aria-expanded', 'true');
        opSkill = { btn: skillBtn, pop: skillPop }; popFlag();
      });
      Array.prototype.forEach.call(skillPop.querySelectorAll('.td-skill-row'), function (row) {
        row.addEventListener('click', function () { closeSkill(); });
      });
      var skillX = skillPop.querySelector('[data-td-skill-close]');
      if (skillX) skillX.addEventListener('click', function () { closeSkill(); skillBtn.focus(); });
    }

    /* 大模型 / 标准模式：DS Select 契约结构 —— 视图点击开合、选项点击选中并回写文案 */
    Array.prototype.forEach.call(wrap.querySelectorAll('.td-composer .giencoder-select'), function (sel) {
      var view = sel.querySelector('.giencoder-select-view');
      var pop = sel.querySelector('.giencoder-select-popup');
      if (!view || !pop) return;
      view.addEventListener('click', function () {
        closeAdd(); closeSkill();
        if (opSel && opSel.pop === pop) { closeSel(); return; }
        closeSel();
        pop.classList.add('giencoder-popup-open');
        view.setAttribute('aria-expanded', 'true');
        opSel = { view: view, pop: pop }; popFlag();
      });
      view.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); view.click(); }
      });
      Array.prototype.forEach.call(pop.querySelectorAll('.giencoder-select-option'), function (opt) {
        opt.addEventListener('click', function () {
          if (opt.classList.contains('giencoder-select-option-disabled')) return;
          Array.prototype.forEach.call(pop.querySelectorAll('.giencoder-select-option'), function (o) {
            o.classList.remove('giencoder-select-option-selected');
            o.setAttribute('aria-selected', 'false');
          });
          opt.classList.add('giencoder-select-option-selected');
          opt.setAttribute('aria-selected', 'true');
          var txt = view.querySelector('.giencoder-select-view-text');
          if (txt) txt.textContent = opt.textContent.trim();
          closeSel();
        });
      });
    });

    /* 点弹层与触发器以外的任何地方 → 全部关闭
       ⚠️ 「技能」按钮本身不在 .giencoder-select 里，必须单独列出，否则它的 click 会先打开面板、
          紧接着冒泡到 document 又被立刻关掉。 */
    document.addEventListener('click', function (e) {
      if (!opAdd && !opSkill && !opSel) return;
      if (e.target.closest && e.target.closest('.td-add-pop, .td-skill-pop, .giencoder-select, [data-td-skill-btn]')) return;
      closePops();
    });
    document.addEventListener('td:close-popovers', closePops);

    var gutter = wrap.querySelector('[data-td-gutter]');
    var right = wrap.querySelector('.td-right');
    var left = wrap.querySelector('.td-left');
    if (!gutter || !right) return;

    var DEFAULT_W = 480;   /* 右栏默认宽（设计稿实测） */
    var MIN_W = 100;       /* 拖到此值以下即自动折叠（第24轮：原 320） */
    var COLLAPSED_W = 48;  /* 折叠条宽（设计稿实测 1343:18532 = 48×844） */
    var LEFT_MIN = 480;    /* 左栏保底（★ 第32轮第4项：320 → 480，与 CSS --td-left-min 同值） */
    var dragging = false, curW = DEFAULT_W;

    /* 右栏可达到的最大宽度 = 根容器宽 − 拖动条宽 − 左栏保底。
       ★ 第 32 轮修正：原先漏算拖动条 8px，导致钳位后左栏实际只剩 LEFT_MIN−8，
         触发 CSS min-width 兜底 → 两栏总宽超容器（溢出）。 */
    function maxRightW() {
      return root.getBoundingClientRect().width - gutter.getBoundingClientRect().width - LEFT_MIN;
    }

    function setWidth(w) {
      curW = w;
      root.style.setProperty('--td-right-w', w + 'px');
      gutter.setAttribute('aria-valuenow', String(Math.round(w)));
    }
    /* 由指针 x 反推右栏应有的宽度。
       第 28 轮第 1 项：两栏可互换位置（.is-swapped → row-reverse）后 .td-right 会跑到左侧、
       拖动条落在它**右侧**，此时宽度与 clientX 是正相关（原来恒为负相关）→ 必须按状态取反。 */
    function widthFrom(clientX) {
      var box = root.getBoundingClientRect();
      var w = root.classList.contains('is-swapped') ? (clientX - box.left) : (box.right - clientX);
      var maxW = maxRightW();
      if (w > maxW) w = maxW;
      if (w < 0) w = 0;
      return w;
    }
    function collapse() {
      root.classList.add('is-collapsed');
      setWidth(COLLAPSED_W);
    }
    function expand(w) {
      root.classList.remove('is-collapsed');
      setWidth(w || DEFAULT_W);
    }
    /* 拖动分栏 */
    gutter.addEventListener('pointerdown', function (e) {
      if (root.classList.contains('is-collapsed')) return;
      dragging = true;
      root.classList.add('is-dragging');
      gutter.classList.add('is-dragging');
      if (gutter.setPointerCapture) { try { gutter.setPointerCapture(e.pointerId); } catch (err) {} }
      e.preventDefault();
    });
    gutter.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var w = widthFrom(e.clientX);
      /* 第 24 轮第 4 项：拖到 100px 以下立刻折叠成窄条（实时反馈）；
         继续向左拖回 100px 以上则恢复跟随鼠标。松手时以 curW 判定最终状态。 */
      if (w < MIN_W) {
        curW = w;                                  /* 记录真实拖拽宽度，便于反向恢复 */
        root.classList.add('is-collapsed');
        setWidth(COLLAPSED_W);
      } else {
        root.classList.remove('is-collapsed');
        setWidth(Math.round(w));
      }
    });
    function endDrag() {
      if (!dragging) return;
      dragging = false;
      root.classList.remove('is-dragging');
      gutter.classList.remove('is-dragging');
      if (curW < MIN_W) collapse();          /* 过窄 -> 自动折叠 */
      else root.classList.remove('is-collapsed');
    }
    gutter.addEventListener('pointerup', endDrag);
    gutter.addEventListener('pointercancel', endDrag);
    /* 键盘可达：默认 ← 变宽 / → 变窄（到阈值即折叠）；两栏互换后方向随之取反 */
    gutter.addEventListener('keydown', function (e) {
      var step = 24;
      var maxW = maxRightW();
      var swapped = root.classList.contains('is-swapped');
      var widerKey = swapped ? 'ArrowRight' : 'ArrowLeft';
      var narrowKey = swapped ? 'ArrowLeft' : 'ArrowRight';
      if (e.key === widerKey) { expand(Math.min(curW + step, maxW)); e.preventDefault(); }
      else if (e.key === narrowKey) {
        var nw = curW - step;
        if (nw < MIN_W) collapse(); else expand(nw);
        e.preventDefault();
      }
    });
    /* 折叠态：点击整列恢复默认宽度比例 */
    right.addEventListener('click', function (e) {
      if (!root.classList.contains('is-collapsed')) return;
      e.preventDefault();
      expand(DEFAULT_W);
    });

    /* ---------- 按住标题栏左右拖动互换两栏位置 ----------
       ★ 第 28 轮第 1 项建立；★ 第 30 轮第 2 项重写（原实现「瞬间切类 + 260ms 透明度闪一下」太生硬）。

       保留的判定规则：
         · pointerdown 必须落在 .td-bar / .td-right-bar 上，且不在按钮/链接/输入控件上
           （否则会和顶栏那些按钮的点击抢事件）；
         · 位移 < 6px 视为点击（不进入拖动态、不 preventDefault、不影响原有点击）；
         · 方向在 pointerdown 时按两栏实测中心算出 ⇒ 换位后再拖同一个标题栏会自动反向，
           不会出现「单向死锁」；
         · 静止态仍只切 .is-swapped（CSS row-reverse），DOM 顺序不动。

       第 30 轮的五个手感优化：
         ① 跟手位移（橡皮筋，不是硬限幅）：|dx| ≤ cap 时 1:1 跟手；超出后按 RB 继续走，
            不会「顶住不动」；另一栏反向微移「让位」→ 立刻有物理反馈，两栏不会交叉重叠；
         ② FLIP 滑动：松手判定换位时，先记 first rect → 切类 → 记 last rect →
            用 Web Animations 从 translateX(dx) 滑回 0，两栏真的横着挪过去（不是瞬移）；
            飞行期被拖的那一栏加 is-fly-left/right → z=3 + 加深投影（「拎起来」）；
         ③ 回弹：未达阈值时把跟手位移用同一条曲线弹回 0，而不是瞬间归位；
         ④ 甩动判定：|v| ≥ 0.6 px/ms 且方向正确 ⇒ 即使位移不够也换位（短促快拖也能换）。
       ★ 第 32 轮第 2 项（用户仍反馈「拖拽过程不流畅」）修掉两处根因：
         · cap 14%→28%（≈100px → ≈200px）、RB 0.18→0.28：上一版拖过 100px 后卡片几乎不跟手，
           手感上就是「卡住了」；现在指针走多远卡片走多远。
         · **去掉 scale(1.006)**：「拎起来」只由投影 + z-index 表达。scale 会让这种大尺寸、
           文字密集的滚动容器**每帧重新栅格化**（掉帧主因）。
         · 位移写入用 **rAF 合并**（一帧只写一次 transform）；去掉 pointermove 里的
           preventDefault（非被动监听器会让浏览器等回调 → 输入延迟）。
       曲线统一 cubic-bezier(0.22, 1, 0.36, 1)：起步快、收尾稳、**无过冲**（不会越界出容器）。
       prefers-reduced-motion 下跳过所有位移动画，只切类。 */
    var SWAP_T = 72;              /* 距离阈值 px（原 80：略微降低，配合甩动判定更好触发） */
    var SWAP_FLICK = 0.6;         /* 甩动速度阈值 px/ms */
    var SWAP_DUR = 400;           /* FLIP 滑动时长 ms */
    /* ★ 第 32 轮第 2 项重新调参：上一版 cap = 两栏中心距 ×14%（1440 下仅 ~100px）+
       RB 0.18，超过 100px 后卡片几乎不跟手 —— 用户反馈「拖拽过程不流畅」的主因。
       现在 1:1 跟手区放宽到中心距 ×28%（≈200px，是换位阈值 72px 的 2.8 倍），
       超出后按 0.28 继续走（原来 0.18）→ 指针走多远卡片就走多远，绝不「顶住不动」。 */
    var FOLLOW = 0.28;            /* 1:1 跟手区间（× 两栏中心距） */
    var RB = 0.28;                /* 超出限幅后的橡皮筋系数 */
    var PEER = 0.14;              /* 让位栏反向跟随比例 */
    var SWAP_EASE = 'cubic-bezier(0.22, 1, 0.36, 1)';
    var reduceMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var xdrag = null;

    /* 把元素从 from px 位移滑回 0，结束即清掉内联 transform（回到自然布局位） */
    function slideBack(el, from, dur) {
      if (!el) return;
      if (reduceMotion || !from) { el.style.transform = ''; return; }
      var anim = el.animate(
        [{ transform: 'translate3d(' + from + 'px,0,0)' },
         { transform: 'translate3d(' + Math.round(from * 0.55) + 'px,0,0)', offset: 0.45 },
         { transform: 'translate3d(0,0,0)' }],
        { duration: dur, easing: SWAP_EASE, fill: 'both' });
      anim.onfinish = function () {
        el.style.transform = '';
        if (anim.cancel) anim.cancel();
      };
    }

    function bindSwapBar(bar, panel) {
      if (!bar) return;
      var other = (panel === left) ? right : left;

      bar.addEventListener('pointerdown', function (e) {
        if (e.button !== 0) return;
        if (e.target.closest('button, a, input, textarea, select, [role="combobox"]')) return;
        if (root.classList.contains('is-fullscreen') || root.classList.contains('is-collapsed')) return;
        var a = panel.getBoundingClientRect(), b = other.getBoundingClientRect();
        var gap = Math.abs((b.left + b.width / 2) - (a.left + a.width / 2));
        xdrag = {
          bar: bar, panel: panel, other: other,
          x0: e.clientX, dx: 0, applied: 0, peer: 0, v: 0, moved: false, tPrev: e.timeStamp,
          cap: Math.max(48, Math.round(gap * FOLLOW)),   /* 跟手限幅：一次性算好，避免 pointermove 里反复取 rect */
          dir: (b.left + b.width / 2) >= (a.left + a.width / 2) ? 1 : -1
        };
        if (bar.setPointerCapture) { try { bar.setPointerCapture(e.pointerId); } catch (err) {} }
      });

      /* ★ 第 32 轮：位移写入用 rAF 合并 —— 指针事件一帧内可能来好几个，
         每个都写一次 transform 会白白多做几次样式计算/绘制。这里一帧只写一次。 */
      var rafId = 0;
      function paint() {
        rafId = 0;
        var d = xdrag;
        if (!d || reduceMotion) return;
        d.panel.style.transform = 'translate3d(' + d.applied + 'px,0,0)';
        d.other.style.transform = 'translate3d(' + d.peer + 'px,0,0)';
      }

      bar.addEventListener('pointermove', function (e) {
        var d = xdrag;
        if (!d || d.bar !== bar) return;
        var dt = Math.max(1, e.timeStamp - d.tPrev);
        var next = e.clientX - d.x0;
        d.v = (next - d.dx) / dt;        /* 瞬时速度 px/ms */
        d.tPrev = e.timeStamp;
        d.dx = next;
        if (!d.moved) {
          if (Math.abs(d.dx) < 6) return;
          d.moved = true;
          root.classList.add('is-xdrag');
          d.panel.classList.add('is-xdrag-panel');
          d.other.classList.add('is-xdrag-peer');
        }
        root.classList.toggle('is-xarmed', (d.dx * d.dir >= SWAP_T) || (d.v * d.dir >= SWAP_FLICK));
        /* 跟手：|dx| ≤ cap 时 **纯 1:1**（指针走多少卡片走多少，不加任何缓动/缩放）；
           超出后按 RB 系数继续走 → 越拖越沉但不顶死。
           ★ 第 32 轮去掉了上一版的 scale(1.006)：「拎起来」只靠投影 + z-index 表达。
           scale 会让这种大尺寸、文字密集的滚动容器每帧重新栅格化（明显的掉帧源）。 */
        var abs = Math.abs(d.dx);
        var raw = abs <= d.cap ? abs : d.cap + (abs - d.cap) * RB;
        d.applied = (d.dx < 0 ? -1 : 1) * Math.round(raw);
        d.peer = Math.round(d.applied * -PEER);
        if (!rafId) rafId = requestAnimationFrame(paint);
      });

      function endSwap() {
        var d = xdrag;
        if (!d || d.bar !== bar) return;
        xdrag = null;
        d.panel.classList.remove('is-xdrag-panel');
        d.other.classList.remove('is-xdrag-peer');
        root.classList.remove('is-xarmed', 'is-xdrag');
        if (!d.moved) return;

        var pass = (d.dx * d.dir >= SWAP_T) || (d.v * d.dir >= SWAP_FLICK);
        if (pass) {
          /* ② FLIP：先清掉跟手位移 → 记 first → 切类 → 记 last → 从差值滑入 */
          d.panel.style.transform = '';
          d.other.style.transform = '';
          var fL = left.getBoundingClientRect(), fR = right.getBoundingClientRect();
          var fG = gutter.getBoundingClientRect();
          root.classList.toggle('is-swapped');
          var lL = left.getBoundingClientRect(), lR = right.getBoundingClientRect();
          var lG = gutter.getBoundingClientRect();
          var dxL = Math.round(fL.left - lL.left);
          var dxR = Math.round(fR.left - lR.left);
          var dxG = Math.round(fG.left - lG.left);
          if (!reduceMotion && (dxL || dxR)) {
            /* 飞行期把**被拎起的那一栏**抬到上层并加深投影：两栏重叠时读起来像
               「把卡片拎起来挪过去」，而不是两张不透明卡片硬生生对穿。
               （is-fly-left / is-fly-right 由 d.panel 决定，谁被拖谁在上层。） */
            root.classList.add('is-swap-fly', d.panel === left ? 'is-fly-left' : 'is-fly-right');
            if (dxL) left.style.transform = 'translate3d(' + dxL + 'px,0,0)';
            if (dxR) right.style.transform = 'translate3d(' + dxR + 'px,0,0)';
            if (dxG) gutter.style.transform = 'translate3d(' + dxG + 'px,0,0)';
            slideBack(left, dxL, SWAP_DUR);
            slideBack(right, dxR, SWAP_DUR);
            slideBack(gutter, dxG, SWAP_DUR);
            setTimeout(function () {
              root.classList.remove('is-swap-fly', 'is-fly-left', 'is-fly-right');
            }, SWAP_DUR + 40);
          }
        } else {
          /* ③ 回弹 */
          slideBack(d.panel, d.applied, 260);
          slideBack(d.other, d.peer, 260);
        }
      }
      bar.addEventListener('pointerup', endSwap);
      bar.addEventListener('pointercancel', endSwap);
    }
    bindSwapBar(wrap.querySelector('.td-bar'), left);
    bindSwapBar(wrap.querySelector('.td-right-bar'), right);
  }

  /* 外壳页签：本页归属研发工作台。React 外壳按「文件名 → 路由」判页签
     （task-detail.html 不在映射表内 → 被判成「基础工作台」）。外观（轨道底/游标/文字色）
     已由 CSS 覆盖；这里把页签的**文案与图标**也还原成 shell 自己的 dev 态：
     未选中 = 无图标 + 前 2 字；选中 = 图标 + 完整文案（与 shell 内 `r?label:label.slice(0,2)` 一致）。 */
  var DEV_ICON = '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" class="mr-1.5 size-4 shrink-0" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M23.08 4.315a3 3 0 012.328.01l17.769 7.576A3 3 0 0145 14.661v19.645a3 3 0 01-1.951 2.81L25.28 43.745a3 3 0 01-2.074.008L4.974 37.12A3 3 0 013 34.299V14.668a3 3 0 011.848-2.77l18.231-7.582zm1.146 3.855L7 15.334V33.6l17.227 6.27L41 33.61V15.32L24.226 8.17zm3.498 17.623L21.608 18l-6.377 4.723h-6.19L9 26.37h7.367l4.376-3.051l6.34 7.68 6.307-4.63H39l-.02-3.647h-7.117l-4.139 3.07z" fill="currentColor"></path></svg>';
  function setTabLabel(btn, text) {
    for (var i = btn.childNodes.length - 1; i >= 0; i--) {
      if (btn.childNodes[i].nodeType === 3) btn.removeChild(btn.childNodes[i]);
    }
    btn.appendChild(document.createTextNode(text));
  }
  function syncShellTab() {
    var tl = document.querySelector('[role="tablist"][aria-label="工作台切换"]');
    if (!tl) return false;
    var base = tl.querySelector('[data-tab="base"]');
    var dev = tl.querySelector('[data-tab="dev"]');
    if (base) {
      base.setAttribute('aria-selected', 'false');
      var bi = base.querySelector('svg');
      if (bi) base.removeChild(bi);
      setTabLabel(base, '基础');
    }
    if (dev) {
      dev.setAttribute('aria-selected', 'true');
      if (!dev.querySelector('svg')) dev.insertAdjacentHTML('afterbegin', DEV_ICON);
      setTabLabel(dev, '研发工作台');
    }
    return true;
  }

  /* ---------- 描述区配图的蒙层预览（★ 第 30 轮第 1 项） ----------
     完全按 DS Image 契约（components/image.json）实现，不自造同义结构：
       · 缩略图 = div.giencoder-image > div.giencoder-image-mask-wrapper > img.giencoder-image-img
         + div.giencoder-image-mask（悬停提示「预览」）；
       · 点缩略图 → 动态创建 div.giencoder-image-preview（契约 anatomy 的「预览层」= 全屏遮罩，
         内含 -preview-mask / -preview-img / -preview-close / -preview-zoom），挂在 <body> 上
         ——与 preview/component-image.html 参考实现同一套类名，只是把 demo 的 pv-* 换成契约 is-* 状态类；
       · 关闭方式：右上关闭按钮 / 点遮罩空白处 / Esc；
       · 动效：遮罩淡入 0.3s + 大图 scale(.95→1)（spring）；关闭 0.2s —— 与参考实现同参数。
     Esc 优先级约定（页尾 TAIL）：图片预览 > 对话框弹层 > 退出全屏 > 返回看板；
       打开时给 <html> 打 data-td-img-preview，页尾先判它再派发 td:close-image-preview。 */
  function bindDescImagePreview(wrap) {
    var thumb = wrap.querySelector('.td-desc .giencoder-image-mask-wrapper');
    if (!thumb) return;
    var thumbImg = thumb.querySelector('img.giencoder-image-img');
    if (!thumbImg) return;

    var overlay = null, scale = 1, closing = false;

    function build() {
      if (overlay) return overlay;
      overlay = document.createElement('div');
      overlay.className = 'giencoder-image-preview';
      overlay.setAttribute('role', 'dialog');
      overlay.setAttribute('aria-modal', 'true');
      overlay.setAttribute('aria-label', '图片预览');
      overlay.innerHTML =
        '<div class="giencoder-image-preview-mask">' +
          '<button type="button" class="giencoder-image-preview-btn giencoder-image-preview-close" aria-label="关闭预览">' +
            '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 5l14 14M19 5L5 19"/></svg>' +
          '</button>' +
          '<img class="giencoder-image-preview-img" alt="">' +
          '<div class="giencoder-image-preview-zoom">' +
            '<button type="button" class="giencoder-image-preview-btn" aria-label="缩小" data-td-zoom="out">' +
              '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 12h14"/></svg>' +
            '</button>' +
            '<button type="button" class="giencoder-image-preview-btn" aria-label="放大" data-td-zoom="in">' +
              '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>' +
            '</button>' +
          '</div>' +
        '</div>';
      document.body.appendChild(overlay);

      overlay.querySelector('.giencoder-image-preview-close').addEventListener('click', close);
      /* 点遮罩空白处关闭（mask 铺满全屏，target 落在遮罩/mask 上即视为点背景） */
      overlay.addEventListener('click', function (e) {
        var isBg = (e.target === overlay) ||
                   (e.target.classList && e.target.classList.contains('giencoder-image-preview-mask'));
        if (isBg) close();
      });
      Array.prototype.forEach.call(overlay.querySelectorAll('[data-td-zoom]'), function (btn) {
        btn.addEventListener('click', function () {
          var im = overlay.querySelector('.giencoder-image-preview-img');
          scale = btn.getAttribute('data-td-zoom') === 'in'
            ? Math.min(3, +(scale * 1.25).toFixed(2))
            : Math.max(0.5, +(scale * 0.8).toFixed(2));
          im.style.transform = 'scale(' + scale + ')';
          im.style.setProperty('--giencoder-image-scale', scale);
        });
      });
      return overlay;
    }

    function flag(on) { document.documentElement.toggleAttribute('data-td-img-preview', on); }

    function close() {
      if (!overlay || closing || overlay.style.display === 'none') return;
      closing = true;
      var im = overlay.querySelector('.giencoder-image-preview-img');
      im.style.setProperty('--giencoder-image-scale', scale);
      im.classList.remove('is-opening');
      im.classList.add('is-closing');
      overlay.classList.add('is-closing');
      overlay.classList.remove('is-open');
      flag(false);
      setTimeout(function () {
        overlay.style.display = 'none';
        overlay.classList.remove('is-open', 'is-closing');
        im.classList.remove('is-opening', 'is-closing');
        closing = false;
      }, 240);
    }

    function open() {
      build();
      if (closing || overlay.style.display === 'flex') return;
      var im = overlay.querySelector('.giencoder-image-preview-img');
      im.setAttribute('src', thumbImg.getAttribute('src'));
      im.setAttribute('alt', thumbImg.getAttribute('alt') || '');
      scale = 1;
      im.style.transform = '';
      im.style.setProperty('--giencoder-image-scale', 1);
      overlay.classList.remove('is-closing');
      overlay.style.display = 'flex';
      void overlay.offsetHeight;             /* 强制回流，让遮罩淡入过渡生效 */
      overlay.classList.add('is-open');
      im.classList.add('is-opening');
      flag(true);
      setTimeout(function () { im.classList.remove('is-opening'); }, 340);
    }

    thumb.addEventListener('click', open);
    thumb.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });
    /* 页尾 Esc 链通过自定义事件通知关闭（与 td:close-popovers 同一约定） */
    document.addEventListener('td:close-image-preview', close);
  }

  /* ---------- 顶栏「转派」→ 成员浮窗（★ 第 31 轮，设计稿节点 1345:18366） ----------
     完全按 DS 契约组装，不自造同义结构：
       div.giencoder-popover（契约 popover.json 的 popup；按契约渲染到 popupContainer=body）
         ├ div.giencoder-popover-title     标题 + 副标题
         ├ div.giencoder-popover-content
         │   ├ div.giencoder-input-wrapper > span.giencoder-input-prefix + input.giencoder-input
         │   └ div.giencoder-list.giencoder-scroll-thin > div.giencoder-list-item（role=option）
         └ div.giencoder-popover-footer > button.giencoder-btn-primary
     显隐唯一开关 = DS 弹层的 .giencoder-popup-open（ui-controls.css），与 Select 弹层同参数。
     关闭途径：再点触发按钮 / 点浮窗外 / Esc（页尾 Esc 链派发 td:close-dispatch，
     优先级排在图片预览之后、对话框弹层之前）。
     渲染到 body 而不是 .td-bar 内：① 契约默认 popupContainer=body；② 顶栏本身是
     「按住拖动互换两栏」的把手，浮窗落在顶栏内会被拖拽判定命中。
     设计稿实测的尺寸/间距见 CSS 段注释；两处设计稿未定义处取 DS 既有约定（4px 间距 + 左对齐）。 */
  var DISPATCH_MEMBERS = [
    { name: '邵禹铭', sid: 'P0098602', ch: '铭' },
    { name: '秦怡',   sid: 'P0098603', ch: '怡' },
    { name: '韩佳毅', sid: 'P0098604', ch: '毅' },
    { name: '顾帆',   sid: 'P0098605', ch: '帆' },
    { name: '姜嘉怡', sid: 'P0098606', ch: '怡' },
    { name: '朱甜',   sid: 'P0098607', ch: '甜' },
    { name: '齐瑞辰', sid: 'P0098608', ch: '辰' }
  ];
  var DP_CHECK_SVG = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.6 7.5l3 3L11.4 4.2"/></svg>';
  var DP_SEARCH_SVG = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><circle cx="6.1" cy="6.1" r="4.35"/><path d="M9.3 9.3l3.1 3.1"/></svg>';
  var DP_MSG_SVG = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true"><circle cx="7" cy="7" r="6.2" fill="currentColor"/><path d="M4.3 7.2l1.9 1.9 3.5-3.7" stroke="var(--color-white)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  /* ---------- 全局轻提示：DS Message（第 19 轮全局约定：凡消息提示一律用它）----------
     ★ 第 32 轮：由转派浮窗（第 31 轮）与协作弹窗（第 5 项）共用同一实例。 */
  function tdToast(text) {
    var box = document.querySelector('.td-dp-msg');
    if (!box) {
      box = document.createElement('div');
      box.className = 'td-dp-msg';
      box.innerHTML = '<div class="giencoder-message" role="status">' +
        '<span class="giencoder-message-icon" aria-hidden="true">' + DP_MSG_SVG + '</span>' +
        '<span class="giencoder-message-content"></span></div>';
      box.hidden = true;
      document.body.appendChild(box);
    }
    box.querySelector('.giencoder-message-content').textContent = text;
    box.hidden = false;
    clearTimeout(box._t);
    box._t = setTimeout(function () { box.hidden = true; }, 2400);
  }

  function bindDispatchPicker() {
    var btn = document.querySelector('[data-td-dispatch]');
    if (!btn || btn.hasAttribute('data-td-dp-bound')) return;
    btn.setAttribute('data-td-dp-bound', '1');

    var pop = null, listEl = null, inputEl = null, noneEl = null, okEl = null;
    var items = [], cur = 0;

    function build() {
      if (pop) return pop;
      pop = document.createElement('div');
      pop.className = 'giencoder-popover td-dp';
      pop.setAttribute('role', 'dialog');
      pop.setAttribute('aria-label', '选择转派人员');
      pop.setAttribute('tabindex', '-1');   /* 打开时焦点落在浮层本身：Esc 可关且不会给搜索框套上 focus 环 */
      pop.innerHTML =
        '<div class="giencoder-popover-title">将任务转派给：' +
          '<div class="td-dp-t2">转派仅变更任务负责人，不改变任务状态。</div>' +
        '</div>' +
        '<div class="giencoder-popover-content">' +
          '<div class="giencoder-input-wrapper" data-size="medium">' +
            '<span class="giencoder-input-prefix">' + DP_SEARCH_SVG + '</span>' +
            '<input class="giencoder-input" type="text" placeholder="搜索成员" aria-label="搜索成员" autocomplete="off">' +
          '</div>' +
          '<div class="giencoder-list giencoder-scroll-thin" role="listbox" aria-label="成员列表">' +
            DISPATCH_MEMBERS.map(function (m, i) {
              return '<div class="giencoder-list-item giencoder-list-item-hoverable td-dp-item" role="option"' +
                     ' data-size="small" data-td-idx="' + i + '"' +
                     ' aria-selected="' + (i === cur ? 'true' : 'false') + '"' +
                     ' style="--avatar-bg: var(--avatar-bg-' + ((i % 7) + 1) + ')">' +
                     '<span class="giencoder-avatar giencoder-avatar-circle giencoder-avatar-text td-dp-av" aria-hidden="true">' + m.ch + '</span>' +
                     '<span class="giencoder-list-item-meta"><span class="giencoder-list-item-title td-dp-name">' + m.name +
                       '<span class="td-dp-id"> (' + m.sid + ')</span></span></span>' +
                     '<span class="giencoder-list-item-action"><span class="td-dp-check" aria-hidden="true">' + DP_CHECK_SVG + '</span></span>' +
                     '</div>';
            }).join('') +
            '<div class="giencoder-empty td-dp-none" hidden><div class="giencoder-empty-description">未找到匹配成员</div></div>' +
          '</div>' +
        '</div>' +
        '<div class="giencoder-popover-footer">' +
          '<button class="giencoder-btn giencoder-btn-primary giencoder-btn-size-default td-dp-ok" type="button">确定转派</button>' +
        '</div>';
      /* ★ 挂载前先写内联坐标：绝对定位元素若 left/top 还是 auto，会先按「静态位置」落在文档末尾，
         把文档撑高 → 出现页面竖向滚动条 → 顶栏右对齐按钮整体左移一个滚动条宽度（实测 10px），
         于是 place() 读到的按钮 x 比最终值小 10px。预置 0/0 后挂载，布局不抖，place() 才拿到真值。 */
      pop.style.left = '0px';
      pop.style.top = '0px';
      document.body.appendChild(pop);

      listEl = pop.querySelector('.giencoder-list');
      inputEl = pop.querySelector('.giencoder-input');
      noneEl = pop.querySelector('.td-dp-none');
      okEl = pop.querySelector('.td-dp-ok');
      items = Array.prototype.slice.call(pop.querySelectorAll('[data-td-idx]'));

      listEl.addEventListener('click', function (e) {
        var it = e.target.closest('[data-td-idx]');
        if (it) select(+it.getAttribute('data-td-idx'));
      });
      inputEl.addEventListener('input', filter);
      /* 焦点在搜索框里时 Esc 不该被页尾「INPUT 直接 return」吞掉 → 浮层内自行处理 */
      pop.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { e.stopPropagation(); close(); }
      });
      okEl.addEventListener('click', confirm);
      return pop;
    }

    function place() {
      var r = btn.getBoundingClientRect();
      var left = Math.min(r.left, window.innerWidth - pop.offsetWidth - 8);
      pop.style.left = Math.round(Math.max(8, left) + window.scrollX) + 'px';
      pop.style.top = Math.round(r.bottom + 4 + window.scrollY) + 'px';
      pop.style.right = 'auto';
      pop.style.bottom = 'auto';
    }

    function select(i) {
      cur = i;
      items.forEach(function (it, k) { it.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
    }

    function filter() {
      var q = inputEl.value.trim().toLowerCase();
      var shown = 0;
      items.forEach(function (it, i) {
        var m = DISPATCH_MEMBERS[i];
        var hit = !q || (m.name + m.sid).toLowerCase().indexOf(q) >= 0;
        it.hidden = !hit;
        if (hit) shown++;
      });
      noneEl.hidden = shown > 0;
    }

    function flag(on) { document.documentElement.toggleAttribute('data-td-dp-open', on); }

    function open() {
      build();
      place();
      if (pop.classList.contains('giencoder-popup-open')) return;
      pop.classList.add('giencoder-popup-open');
      btn.setAttribute('aria-expanded', 'true');
      flag(true);
      pop.focus();
    }

    function close() {
      if (!pop || !pop.classList.contains('giencoder-popup-open')) return;
      pop.classList.remove('giencoder-popup-open');
      btn.setAttribute('aria-expanded', 'false');
      flag(false);
    }

    /* 转派结果：写回 aside「执行人」+ 一条 DS Message 提示（实现见模块级 tdToast） */
    var toast = tdToast;

    function confirm() {
      var m = DISPATCH_MEMBERS[cur];
      close();
      var rows = document.querySelectorAll('.td-attr-row');
      for (var i = 0; i < rows.length; i++) {
        var k = rows[i].querySelector('.td-attr-k');
        if (!k || k.textContent.indexOf('执行人') < 0) continue;
        var v = rows[i].querySelector('.td-attr-v');
        if (v) v.textContent = m.name;
        break;
      }
      toast('已转派给 ' + m.name);
    }

    btn.addEventListener('click', function () {
      if (pop && pop.classList.contains('giencoder-popup-open')) close(); else open();
    });
    document.addEventListener('pointerdown', function (e) {
      if (!pop || !pop.classList.contains('giencoder-popup-open')) return;
      if (pop.contains(e.target) || btn.contains(e.target)) return;
      close();
    });
    window.addEventListener('resize', function () {
      if (pop && pop.classList.contains('giencoder-popup-open')) place();
    });
    document.addEventListener('td:close-dispatch', close);
  }

  /* ---------- 顶栏「协作」→ 分步模态弹窗（★ 第 32 轮第 5 项，设计稿节点 622:20081） ----------
     完全按 DS 契约组装（结构说明 + 设计稿实测真值见 HTML / CSS 段注释）：
       遮罩/面板 div.giencoder-modal-wrapper > div.giencoder-modal-mask + div.giencoder-modal[role=dialog]
       步骤条  .giencoder-steps[role=list] > .giencoder-steps-item[role=listitem][aria-current=step]
               + .giencoder-steps-icon（仅已完成态显示对勾）+ .giencoder-steps-title
       产物行  .giencoder-list-item[data-size=small] > .giencoder-checkbox（input + mask + 文本）
       成员行  同上 + .giencoder-list-item-meta > .giencoder-avatar + .giencoder-list-item-title
       搜索框  .giencoder-input-wrapper[data-size=medium] + -input-prefix + -input
     显隐：根 .td-coop 的 hidden + is-open；同时写 <html data-td-coop-open> 供页尾 Esc 链判断。
     步骤切换：当前态 is-active，已完成 is-finish（带对勾）；点步骤条可跳转（steps.json clickable）。
     每次打开复位：勾选态回到初始快照（产物全选 / 成员未选）+ 搜索清空 + 回到 Step1。
     关闭途径：取消 / 右上 X / 点遮罩 / Esc（页尾 Esc 链派发 td:close-coop）+ 提交。 */
  function bindCoop() {
    var btn = document.querySelector('[data-td-coop]');
    var root = document.querySelector('.td-coop');
    if (!btn || !root || btn.hasAttribute('data-td-coop-bound')) return;
    btn.setAttribute('data-td-coop-bound', '1');

    var dialog = root.querySelector('.giencoder-modal');
    var maskEl = root.querySelector('[data-td-coop-mask]');
    var hintEl = root.querySelector('[data-td-coop-hint]');
    var countEl = root.querySelector('[data-td-coop-count]');
    var panes = [].slice.call(root.querySelectorAll('[data-td-pane]'));
    var stepEls = [].slice.call(root.querySelectorAll('[data-td-step]'));
    var btnNext = root.querySelector('[data-td-coop-next]');
    var btnPrev = root.querySelector('[data-td-coop-prev]');
    var btnSubmit = root.querySelector('[data-td-coop-submit]');
    var searchEl = root.querySelector('[data-td-pane="2"] .giencoder-input');
    var mrows = [].slice.call(root.querySelectorAll('[data-td-midx]'));
    var HINTS = { 1: '选择需要流转到下一阶段的协作产物', 2: '将当前任务 (含产物) 流转给下一位协作者' };
    var step = 1;
    /* 初始勾选态快照（产物默认全选、成员默认未选）→ 每次打开复位，避免残留上一轮选择 */
    var allBoxes = [].slice.call(root.querySelectorAll('.giencoder-checkbox-input'));
    var defaults = allBoxes.map(function (b) { return b.checked; });
    function resetChecks() {
      allBoxes.forEach(function (b, i) { b.checked = defaults[i]; });
    }

    function boxes(pane) {
      return [].slice.call(root.querySelectorAll('[data-td-pane="' + pane + '"] .giencoder-checkbox-input'));
    }
    function checked(n) { return boxes(n).filter(function (c) { return c.checked; }).length; }
    function countText() {
      return step === 1
        ? '已选 ' + checked(1) + '/' + boxes(1).length + ' 个产物'
        : '已选 ' + checked(2) + '/' + mrows.length + ' 位协作者';
    }
    function syncCount() { countEl.textContent = countText(); }

    function filter() {
      var q = (searchEl.value || '').replace(/\s+/g, '').toLowerCase();
      mrows.forEach(function (r) {
        var t = r.textContent.replace(/\s+/g, '').toLowerCase();
        r.hidden = !!q && t.indexOf(q) < 0;
      });
    }

    function goStep(n) {
      step = n;
      panes.forEach(function (p) { p.hidden = (+p.getAttribute('data-td-pane')) !== n; });
      stepEls.forEach(function (s) {
        var k = +s.getAttribute('data-td-step');
        s.classList.toggle('is-active', k === n);
        s.classList.toggle('is-finish', k < n);
        if (k === n) s.setAttribute('aria-current', 'step'); else s.removeAttribute('aria-current');
      });
      btnNext.hidden = n !== 1;
      btnPrev.hidden = n !== 2;
      btnSubmit.hidden = n !== 2;
      hintEl.textContent = HINTS[n];
      syncCount();
    }

    function flag(on) { document.documentElement.toggleAttribute('data-td-coop-open', on); }

    function open() {
      resetChecks();
      goStep(1);
      searchEl.value = '';
      filter();
      root.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      flag(true);
      void root.offsetWidth;   /* 强制 reflow，保证 is-open 的过渡真正触发 */
      root.classList.add('is-open');
      dialog.focus();
    }

    function close() {
      if (root.hidden) return;
      root.classList.remove('is-open');
      root.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
      flag(false);
    }

    function submit() {
      var n = checked(1);
      var m = mrows.filter(function (r) { return r.querySelector('.giencoder-checkbox-input').checked; });
      close();
      tdToast('已流转 ' + n + ' 个产物给 ' + m.length + ' 位协作者');
    }

    btn.addEventListener('click', function () { if (root.hidden) open(); else close(); });
    root.querySelector('[data-td-coop-close]').addEventListener('click', close);
    root.querySelector('[data-td-coop-cancel]').addEventListener('click', close);
    maskEl.addEventListener('click', close);
    btnNext.addEventListener('click', function () { goStep(2); });
    btnPrev.addEventListener('click', function () { goStep(1); });
    btnSubmit.addEventListener('click', submit);
    searchEl.addEventListener('input', filter);
    /* 点步骤条跳转（steps.json variants.clickable） */
    stepEls.forEach(function (s) {
      s.addEventListener('click', function () {
        var k = +s.getAttribute('data-td-step');
        if (k !== step) goStep(k);
      });
    });
    /* 搜索框里按 Esc：页尾 Esc 链对 INPUT 直接 return → 弹窗内自行处理 */
    root.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.stopPropagation(); close(); }
    });
    /* 勾选框变化 → 计数实时更新（change 冒泡到根节点） */
    root.addEventListener('change', function (e) {
      if (e.target && e.target.classList && e.target.classList.contains('giencoder-checkbox-input')) syncCount();
    });
    document.addEventListener('td:close-coop', close);
  }

  function inject() {
    var main = document.querySelector('main');
    if (!main || main.querySelector('.td-root')) return false;
    var wrap = document.createElement('div');
    wrap.className = 'td-wrap';
    wrap.innerHTML = KB_HTML;
    main.appendChild(wrap);
    bindDetail(wrap);
    bindDescImagePreview(wrap);
    bindDispatchPicker();
    bindCoop();
    return true;
  }
  /* 注意：两个动作都要执行，不能短路（页签在 React 挂载后才出现，可能晚于注入）。
     inject() 只在首次真正插入时返回 true，所以这里补一个「已注入」判断，
     否则 ready() 永远返回 false、MutationObserver 永不卸载、每次 DOM 变更都白跑一遍。
     页签点击（第 25 轮第 3 项）改由公共片段 SHELL_TABS 承担，见文件尾部。 */
  function ready() {
    var injected = inject() || !!document.querySelector('.td-root');
    var tabbed = syncShellTab();
    return injected && tabbed;
  }
  if (!ready()) {
    var mo = new MutationObserver(function () { if (ready()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
</script>"""

lines = [l for l in HTML.split("\n")]
js_lines = ",\n".join('        ' + json.dumps(l, ensure_ascii=False) for l in lines)
JS = JS.replace("__LINES__", js_lines)

# ---- 尾部：主题同步 + 返回看板 + 公共片段（顶栏页签可点击，第 25 轮第 3 项） ----
SHELL_TABS = io.open("mg-work/shell-tabs.snippet.html", encoding="utf-8").read()
TAIL = """<script>
      // Sync theme with dev workbench if opened from it; default light.
      (function () {
        try {
          var t = localStorage.getItem('giencoder-theme');
          if (t === 'dark' || location.hash === '#dark') document.documentElement.setAttribute('giencoder-theme', 'dark');
        } catch (e) {}
      })();
    </script>
  <script>
      /* 详情页：Esc 返回任务看板（全屏态下先退出全屏，第 26 轮第 5 项） */
      document.addEventListener('keydown', function (ev) {
        if (ev.key !== 'Escape') return;
        var tag = (ev.target && ev.target.tagName) || '';
        if (tag === 'TEXTAREA' || tag === 'INPUT') return;
        /* ★ 第 30 轮第 1 项：图片蒙层预览优先级最高 —— 打开时 Esc 只关预览，不继续往下走。
           预览侧监听自定义事件 td:close-image-preview（见 bindDescImagePreview）。 */
        if (document.documentElement.hasAttribute('data-td-img-preview')) {
          document.dispatchEvent(new CustomEvent('td:close-image-preview'));
          return;
        }
        /* ★ 第 32 轮第 5 项：协作模态弹窗次优先（模态层级最高，Esc 只关它）。
           弹窗侧监听自定义事件 td:close-coop（见 bindCoop）。 */
        if (document.documentElement.hasAttribute('data-td-coop-open')) {
          document.dispatchEvent(new CustomEvent('td:close-coop'));
          return;
        }
        /* ★ 第 31 轮：转派成员浮窗次优先（不是模态，但浮在顶栏之上，Esc 应先收它）。
           浮窗侧监听自定义事件 td:close-dispatch（见 bindDispatchPicker）。 */
        if (document.documentElement.hasAttribute('data-td-dp-open')) {
          document.dispatchEvent(new CustomEvent('td:close-dispatch'));
          return;
        }
        /* ★ 第 28 轮第 4 项：对话框弹层打开时，Esc 先关弹层而不是跳回看板。
           弹层侧监听自定义事件 td:close-popovers（见 bindDetail 里的对话框绑定）。 */
        if (document.documentElement.hasAttribute('data-td-pop-open')) {
          document.dispatchEvent(new CustomEvent('td:close-popovers'));
          return;
        }
        var fsRoot = document.querySelector('.td-root.is-fullscreen');
        if (fsRoot) {
          fsRoot.classList.remove('is-fullscreen');
          var fb = fsRoot.querySelector('[data-td-fullscreen]');
          if (fb) {
            fb.setAttribute('aria-label', '全屏');
            fb.setAttribute('title', '全屏');
            fb.setAttribute('aria-pressed', 'false');
          }
          return;
        }
        location.href = 'kanban.html';
      });
    </script>
  """ + SHELL_TABS + """
  </body>
</html>
"""

# ---- ★ 第 30 轮第 1 项：Image 组件样式在**构建期**从 DS 源文件抽取后内联（避免页面副本与 DS 漂移）
# 静态结构 ← giencoder-design-system/components.css（「/* === Image 图片」段起至文件末）
# 全屏定位 + 开合动效 ← giencoder-design-system/gienx-templates/ui-controls.css（「/* ---- Image 预览层」段起）
# 注：本仓页面一直是「DS 文件为源 + 页面内联副本」的模式（:root token、Select 弹层同理），
#     这里改成构建期读源文件，源文件一改、重跑本脚本即同步。
DS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "giencoder-design-system")


def ds_slice(path, marker):
    txt = io.open(path, encoding="utf-8").read()
    i = txt.find(marker)
    assert i > 0, "DS 里找不到锚点 %r：%s" % (marker, path)
    return txt[i:].rstrip()


def ds_seg(path, start, end):
    """抽取 (start, end) 之间的片段（不含 end），用于取文件中间的段落"""
    txt = io.open(path, encoding="utf-8").read()
    i = txt.find(start)
    assert i > 0, "DS 里找不到起点 %r：%s" % (start, path)
    j = txt.find(end, i + len(start))
    assert j > 0, "DS 里找不到终点 %r：%s" % (end, path)
    return txt[i:j].rstrip()


_DS = lambda *p: os.path.join(DS_DIR, *p)

# ---- ★ 第 31 轮：转派浮窗用到的 token（从 DS colors_and_type.css 抽取，避免页面副本漂移）----
_ds_picker_tokens = ds_seg(_DS("colors_and_type.css"),
                           "  /* ---- 字符头像底色",
                           "  /* ==== 头像 / 滚动条 token 段结束（构建期抽取锚点，勿删）==== */")
DS_PICKER_TOKENS = "\n".join("        " + ln.strip() if ln.strip() else ""
                            for ln in _ds_picker_tokens.split("\n"))
CSS = CSS.replace("__DS_PICKER_TOKENS__", DS_PICKER_TOKENS)
assert "__DS_PICKER_TOKENS__" not in CSS, "转派浮窗 token 占位符未替换"

# ---- ★ 第 31 轮：转派浮窗用到的组件样式（Popover 静态结构 + List + Avatar + 细滚动条 + 弹层定位动效）----
_ds_picker = "\n\n".join([
    ds_seg(_DS("components.css"), "/* === Avatar 头像 === */", "/* === Breadcrumb 面包屑 === */"),
    ds_seg(_DS("components.css"), "/* === List 列表 === */", "/* === Badge 徽标 === */"),
    ds_slice(_DS("components.css"), "/* === Popover 气泡卡片"),
    ds_slice(_DS("gienx-templates", "ui-controls.css"), "/* ---- Popover 弹层"),
])
DS_PICKER_CSS = (
    "      /* ⚠️ 以下组件样式由 build-detail.py 在构建期从 DS 源文件抽取，请勿在此手改：\n"
    "         静态结构 ← giencoder-design-system/components.css\n"
    "         弹层定位/开合动效 ← giencoder-design-system/gienx-templates/ui-controls.css */\n"
    + "".join(("      " + ln + "\n") if ln.strip() else "\n" for ln in _ds_picker.split("\n"))
)
CSS = CSS.replace("__DS_PICKER_CSS__", DS_PICKER_CSS)
assert "__DS_PICKER_CSS__" not in CSS, "转派浮窗样式占位符未替换"

_ds_img = (
    ds_seg(os.path.join(DS_DIR, "components.css"), "/* === Image 图片", "/* === Popover 气泡卡片")
    + "\n\n"
    + ds_seg(os.path.join(DS_DIR, "gienx-templates", "ui-controls.css"),
             "/* ---- Image 预览层", "/* ---- Popover 弹层")
)
DS_IMAGE_CSS = (
    "      /* ⚠️ 以下 Image 组件样式由 build-detail.py 在构建期从 DS 源文件抽取，请勿在此手改：\n"
    "         静态结构 ← giencoder-design-system/components.css\n"
    "         全屏定位/开合动效 ← giencoder-design-system/gienx-templates/ui-controls.css */\n"
    + "".join(("      " + ln + "\n") if ln.strip() else "\n" for ln in _ds_img.split("\n"))
)
CSS = CSS.replace("__DS_IMAGE_CSS__", DS_IMAGE_CSS)
assert "__DS_IMAGE_CSS__" not in CSS, "Image 样式占位符未替换"

out = head + mid + CSS + "\n" + JS + "\n" + TAIL
io.open(DST, "w", encoding="utf-8", newline="").write(out)
print("WROTE %s  %d chars (src %d)" % (DST, len(out), len(s)))
print("HTML lines:", len(lines))

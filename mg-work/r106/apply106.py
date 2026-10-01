# -*- coding: utf-8 -*-
"""r106 · 会话详情 · 四条（**新代** —— r102 代已交付 `87e2caa`，故不再就地返工）
（承接 r102 代产物，仍是 pages/{base,conversation}.html）

体位与历代一致：本脚本 = **净底（base.html 摘掉历代注入块）+ 重新注入本代块**，
故「改完直接重跑即自愈」照旧成立；「历代标记」由下面的 `GENS` 表承担
（r93 / r101 / r102 三代都已提交、页面里仍留着它们各三块 ⇒ **必须与本代一起摘掉**）。

★ **r106 四条（2026-09-30 23:5x 提要求 · 2026-10-01 08:0x 落地）**：

  ① 「上下文注入」与「深度思考」两个模块**默认折叠**。
     —— 只改 `fold()` 工厂的**调用参数**（加 `open:false`）：工厂本来就支持
        `data-r93-open="0"` 这一态（折叠头 `.r93-fc` 可见 / 展开头 `.r93-fh` 隐藏），
        当年那两处调用没传而已。**零 CSS、零新结构。**                              JS(TMPL)
     ⚠ 连带确认：`wire()` 只给「初始就展开」的块挂 `.is-free`（放行卡内 popover），
        这两块默认收起后不会被挂上 —— 正是想要的行为（收起态本就该裁剪）。无需改。
  ② 文件预览栏的顶栏 `.td-browse-bar` 高 **40 → 44px**，与标题栏 `.r93-bar` 同高、底线对齐。CSS
     ⚠ 走本页适配层，**不动** `part105/browse.css`（要与源页 avatar.html 逐字节同源）。
  ③ 预览栏展开时：`main` 的**右侧两个圆角改直角** + 接缝线**收成 1px**。             CSS
  ④ **「空间不足才自适应、空间足够保持原逻辑」**（口径经邵先生 2026-10-01 二次更正）：
     预览栏展开时 main 只剩 779，而内容列仍锁 `max(50%, 860px)` ⇒ 右侧 92px 被裁掉。
     修法 = **上限型 clamp** `width: min(<撑满可用宽>, <原逻辑式>)`，跟着**容器可用宽**走： CSS
       a) 内容列 `.r93-wrap` / 底部列 `.r93-bottom` / composer 外壳 / 骨架屏 `.r93-sk-in`
          —— 四列同宽（1440 开 778 · 2560 开 949 · 关态逐像素不变）；
       b) **用户消息块 `.r93-bub`** —— 原规则**写死 `width: 728px`**（全仓唯一的 728px），
          内容列窄于 728 时该块（`margin-left:auto` 右对齐）向左溢出被裁 ⇒
          改 `min(100%, 728px)`：列 ≥728 保持 728（设计原样）、列 <728 跟着收。
          ⚠ 这一条**不带 `.av-browse-on`** —— 溢出与「预览栏开不开」无关，窄窗口关态同样会溢。

用法：
  python mg-work/r106/apply106.py            # 应用（幂等：base 先摘净底，再落到两页 + 9 页路由表）
  python mg-work/r106/apply106.py --revert   # 回滚（删 conversation.html + 摘 base 的 nav 脚本 + 摘路由表条目）
  python mg-work/r106/apply106.py --dry
  ⚠️ 自检： python mg-work/check-syntax.py pages/*.html  &&  python verify-design.py ./pages

--------------------------------------------------------------- 以下为历代原说明（几何 / 字号标定沿用）

★ r102 代（十一条 ＋ r103 六条 ＋ r104 四条 ＋ r105 三条 —— 五者都是「未提交期就地返工」，
  已于 2026-09-30 23:5x 一并交付 `87e2caa`；本代 r106 在那一版产物的净底之上重做）。

★ **r104 四条（2026-09-30 21:2x；r102 / r103 尚未提交 ⇒ 就地改本脚本、注入块 id 不变）**：

  ① 底部对话框的**所有浮窗**（技能列表 / 大模型下拉 …）被遮 ⇒ 见根因与修法：
     它们都是 hero 的定位后代，r103 ⑤ 给 hero 的 `z-index: 1` 把它们的 1000/9999 **封顶在 1**，
     反被宿主内部 `.r93-tbsticky` 3 / `.r93-sk` 9 / `.r93-bar` 10 压住。
     修法 = **宿主补 `z-index: 0`**（整块降成 0 级上下文，内部 3/9/10 再也爬不出来）。
     ⚠ 与 r103 ⑤ **必须成对存在**：少了宿主这一行，浮窗被洗；少了 hero 那一行，外发光被截。  CSS
  ② 刷新后「骨架屏之前先闪一下对话框」⇒ 纯 CSS **首帧守卫**：`.mt-8` 默认 `opacity: 0`，
     由 `<html data-r93-app="ready">` 在**骨架屏退场那一拍（1100ms）**放行。                CSS + JS
  ③ 页签「对话 ⇄ 轨迹」**滑动交接**（旧 pane 滑出 22px + 淡出 → 新 pane 滑入）；
     且**切到轨迹页收起底部对话框**（CSS 隐形 + hero `display:none` 让位，宿主顺势长高）。  CSS + JS
  ④ 全局全要素代码审查（冗余 / 命名 / DS 规范与组件复用 / token 命名一致性 / 稳定性），
     **逐条结论见 mg-work/r102/acceptance.md 的「r104 段 · 代码审查」**，本文件只落**已采纳的修正**。

★ **r103 六条（2026-09-30 20:5x；r102 尚未提交 ⇒ 就地改本脚本、注入块 id 不变）**：

  ① `.r93-t14` 这种**正文**字号 → **15px**（撤销 r102 ① 的字号部分；数字动效保留）。   CSS
  ② `.r93-t14.r93-ell` 同类型也 15px（`.r93-c1` / `.r93-ell` 本身不含字号 ⇒ 随 ① 自动生效）。CSS
  ③ 「滚动到底部」药丸的毛玻璃**再透一点**：72% → **60%**（新增 `--r93-glass-pill`
     / `--r93-glass-pill-h`，**不与标题栏共用**）。                                    CSS
  ④ `.r93-agents` 那一行（4 张 agent 卡）**整行退役**（连 `.r93-cp` 容器一起摘）。     JS(TMPL)
  ⑤ 底部对话框**激活态外发光顶部被截断** ⇒ hero 提层（`position:relative` + `z-index:1`）。CSS
  ⑥ `.r93-fh.r93-bt` 这类折叠块：**开合两态动效统一** + 修「折叠时闪动」
     （撤掉单向 keyframes 动画、改对称 transition；`setFold` 改 rAF 延迟翻属性）。    CSS + JS

r102 十一条（逐字原文见 mg-work/r102/acceptance.md）与落点：

  ① `.r93-t14` 的字号 15 → **13px**（**已被 r103 ① 撤回，现为 15px**）；
     且**里面的数字要有动效** —— 数字逐串「自下而上滑入」（odometer-lite），见 `r93-num`。CSS + JS
  ② 折叠头右侧那枚 hover 箭头（`.r93-fchev`）的间距 8 → **4px**。                  CSS
  ③ `.r93-fh` **展开有动效、折叠收起没有** ⇒ 补折叠方向的动效
     （r101 ⑦ 只做了展开；见 CSS 里 `r93-fold-out` + JS 写 `--r93-fbh`）。          CSS + JS
  ④ `.r93-t12.r93-nm` 这类（改动汇总的 +800 / −125）字号 12 → **13px**。            CSS
  ⑤ `.r93-iblk.r93-i14.r93-cv` 里的箭头**加大一号**：svg 10 → **12px**（槽仍 14×14）。CSS
  ⑥ `.r93-fh` hover 时，后面的小字（`.r93-t12l.r93-fm.r93-ell` 这类 meta）也要变**正文色**
     （r101 ① 只把图标与主标题提到了正文色，meta 仍是 text-3）。                    CSS
  ⑦ `.r93-asst` 底部的线条**浅一级**（`--color-border-2` → `--color-border-1`，
     r99 ⑬ 当年拍的「深一级」本轮回退）。                                            CSS
  ⑧ `.r93-drow` 的 padding 改 **0 16px**（原 `0 13px 0 11px`）。                    CSS
  ⑨ `.r93-dhead` 的左侧内距改 **16px**（原 `6px 6px 5px 12px` 里的 12）。            CSS
  ⑩ 「滚动到底部」按钮（`.r93-tobottom`）也改**毛玻璃**（**透明度已被 r103 ③ 由 72% 调低到 60%**）。CSS
  ⑪ `.r93-seg`（`giencoder-radio-group-button`）**总高 28px**、且在标题栏内**垂直居中**。CSS

用法：见本文件顶部的 r106 段（命令一律走 mg-work/r106/apply106.py）。

--------------------------------------------------------------- 以下为 r101 原说明（几何 / 字号标定沿用）

★ r101 前情（两批共十八条 · **已交付 `9f252e5`**）—— 本代全部在它之上继续改造。

r101 第一批（十一条，逐字原文见 mg-work/r101/acceptance.md）：

  ① `.r93-fh` / `.r93-fc` hover：**不再铺浅灰底**，只把图标 + 文字提到正文色。        CSS
  ② `.r93-t12l` 容器的文字色用「浅两级」= `--color-text-3`（正文 text-1 往下两级）。  CSS
  ③ `.r93-ib`（hover 态）：**浅灰底、不显示边框**（撤掉 r99 ⑨ 的白底 + 1px 内描边）。 CSS
  ④ 折叠箭头 `.r93-iblk.r93-i14.r93-cv` 偏大 → svg 14 → **10px**；
     ⚠ 只缩 svg、**槽仍 14×14** ⇒ 展开/收起零跳动（r99 ⑧ 当年正是为了防跳动才把槽由 12 提到 14）。CSS
  ⑤ 去掉 Bash 卡头那枚绿勾（`.r93-iblk.r93-i14.r93-okc`）；
     ⚠ 页面里 `.r93-okc` 共 2 处，「上下文已压缩」行首那枚**保留**（它带文案，且④⑤相邻 ⇒ 指 Bash 头）。JS
  ⑥ `.r93-pane` 与底部对话框「相切」的衔接处**渐隐**。                              CSS + JS(1 个空壳)
  ⑦ 「任务产物」卡片支持右键菜单 —— 即 AI 对话框右栏 `td-browse-slot` 那一套
     （打开 / 打开所在文件夹 / 添加到对话 / 添加到 GienCoder / 复制路径 / 分隔线 / 打开方式▸6 项子菜单）。JS + CSS
  ⑧ 「压缩上下文」前面的图标**转起来**（`@keyframes r93-spin`，1.2s 线性无限）。      CSS + JS(1 个类名)
  ⑨ 折叠头 meta（`.r93-t12l.r93-fm.r93-ell`）与「调用 N 个工具」卡汇总值
     （`.r93-sumrow .r93-t12l`）的字号 12 → **13px**（共 17 处；同卡相邻，只改一半会 13/12 混杂）。CSS
  ⑩ `.r93-sb` 少了投影 → 按设计稿 PNG 逐像素反推补上（见 CSS 里的实测剖面）。        CSS
  ⑪ 进入页面时「对话内容模块」显示**骨架屏 Skeleton**（复用 DS 已编译进本页的
     `.giencoder-skeleton-line / -title / -avatar`，约 1.1s 后淡出并移除）。           CSS + JS

★ r101 第二批（同日 19:50 邵先生再发七条 —— **当时本代仍未提交 ⇒ 按硬规则就地返工 `apply101.py`**，
  不另起代数；`GENS` 表、注入 id、宿主标记一律不动。现已被本代 r102 继承）：

  ① `.r93-bar` 改成**浮在滚动口之上的毛玻璃标题栏**：内容滚到它底下时呈高斯模糊。
     做法：宿主补 `position:relative`；`.r93-bar` 由流内兄弟改 `position:absolute` +
     `backdrop-filter: blur()`；滚动口用 `padding-top:44px` 把被盖掉的那一档补回来
     （视觉静止态与原来逐像素一致，只有「滚起来」才看得见区别）。
     ⚠ 连带修 `.r93-sk-in` 的上内距（32 → 76），否则骨架屏整体上移 44px 钻进标题栏底下。CSS
  ② 顶栏装饰图的 `background-size` = **70%**（新起一块 `r101-hdr-css` 兜在 r92 块之后）。
     ⚠ 该块要落到**全部 6 个带 `r92-hdr-css` 的页面**
       （base / conversation / avatar / skills / automation / settings）。              PY（注入）
  ③ 骨架屏里那块「浅灰容器」（`.r93-sk-card` 的 `--r93-card` 圆角底）去掉，只留 3 条灰条。CSS
  ④ 衔接处渐隐「距离稍微加大」：`.r93-tbsticky::after` 高度 40 → **56px**。            CSS
  ⑤ `.r93-diff` 里的**右键菜单 + 右侧「更多」菜单**统一成「任务产物卡右键菜单」那一套
     （r99 ⑦ 那 4 项 `.r93-drow` 菜单退役 ⇒ 全页只剩**一张** FMenu）。                  JS
  ⑥ 折叠头（`.r93-fc.r93-bt`）hover 时**右侧浮出一枚向右箭头**（间距 8px）——
     直接复用子菜单那枚 `fright` 图标；**常驻占位 + opacity 淡入**（不引起横向跳动）。  CSS + JS
  ⑦ 展开 / 折叠的**弹性微动效**：`.r93-fb` 由 `display:none` 变可见时播 0.34s 回弹
     （`cubic-bezier(.34,1.56,.64,1)`）；chevron 旋转改用同一条曲线。                   CSS

用法：
  python mg-work/r101/apply101.py            # 应用（幂等：base 先摘净底，再落到两页 + 9 页路由表）
  python mg-work/r101/apply101.py --revert   # 回滚（删 conversation.html + 摘 base 的 nav 脚本 + 摘路由表条目）
  python mg-work/r101/apply101.py --dry
  ⚠️ 自检： python mg-work/check-syntax.py pages/*.html  &&  python verify-design.py ./pages

--------------------------------------------------------------- 以下为 r93 原说明（几何 / 字号标定沿用）
r93 · 基础工作台「会话详情」视图（邵先生第 2 条）

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

用法：见本文件顶部的 r106 段（命令一律走 mg-work/r106/apply106.py）。
"""
import argparse
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
# 图标源目录：**本代优先 → r101 → r93 代**（三级回落）。
# 那 78 个资产是同一次设计稿导出（r93 代已连源一起提交），r101 / r102 一个都没改 ⇒
# 不再在 git 里存第二份；将来本代要新增/覆盖某个图标，放进 mg-work/r102/raw/asset/icons 即可。
RAWI_DIRS = (
    os.path.join(HERE, 'raw', 'asset', 'icons'),
    os.path.join(REPO, 'mg-work', 'r101', 'raw', 'asset', 'icons'),
    os.path.join(REPO, 'mg-work', 'r93', 'raw', 'asset', 'icons'),
)
PAGE = os.path.join(REPO, 'pages', 'base.html')
PAGE_CONV = os.path.join(REPO, 'pages', 'conversation.html')

# ---------------------------------------------------------------- 代数标记
# ★ r101：**逐代摘除**。r93 代已提交（d7e2151），页面里仍留着它的三块注入物（style / script /
#   nav 注释对）⇒ 只摘本代会让「摘块后基线里仍残留标记」这条自检炸掉，而且两代并存会双份生效。
#   故 GENS 里列出**历代**标记，剥离正则对每一代的 id 都生成一条分支；
#   本代的 id（GENS[-1]）用于注入 —— 这样「上一代已提交、本代未提交」的返工体位天然成立。
#   元组 = (tag 前缀, CSS id, JS id, NAV JS id)；nav 的注释对恒为 `<!-- <tag>-nav -->`。
# ★ r102：r101 代**已提交**（9f252e5）⇒ 本代新建脚本、本代 id 取 `r102-*`；
#   GENS 现在有**三代**（r93 / r101 / r102），三条剥离正则各摘三支、注入只用 r102。
# ★ r106：r102 代**已交付**（87e2caa，内含 r103/r104/r105 三条就地返工）⇒ 本代新建脚本、
#   本代 id 取 `r106-*`；GENS 现在有**四代**（r93 / r101 / r102 / r106），
#   四条剥离正则各摘四支、注入只用 r106。
#   ⚠ r103 / r104 / r105 从未单独占代（都是 r102 的就地返工）⇒ **不入表**。
GENS = (
    ('r93',  'r93-conv-css',  'r93-conv-js',  'r93-nav-js'),
    ('r101', 'r101-conv-css', 'r101-conv-js', 'r101-nav-js'),
    ('r102', 'r102-conv-css', 'r102-conv-js', 'r102-nav-js'),
    ('r106', 'r106-conv-css', 'r106-conv-js', 'r106-nav-js'),
)
CSS_ID, JS_ID, NAV_ID = GENS[-1][1], GENS[-1][2], GENS[-1][3]
_N_CSS = '|'.join(g[1] for g in GENS)
_N_JS = '|'.join(g[2] for g in GENS)
_N_NAV = '|'.join(g[3] for g in GENS)
_N_TAG = '|'.join(g[0] for g in GENS)

ATTR_HOST = 'r93-conv-host'  # 宿主类名（跨代沿用：它只出现在被整块重写的 CSS/JS 里，无残留风险）
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

# ------------------------------------------------- 顶栏装饰图（★ r101 第②批 ②）
# r92 ① 给基础工作台顶栏铺了 `assets/images/bg-img-1.png`（1580×134 / `right center` /
# `no-repeat` / **刻意不写 background-size** ⇒ CSS 默认 auto = 原尺寸）。邵先生本轮要求
# 把尺寸改成 **70%**。
# 体位：r92 代**已提交**（d7e2151）⇒ 不回改 `mg-work/r92/apply92.py`，另起一块
# `r101-hdr-css` 兜在它后面 —— 两者同特异性（`header[class*="h-12"]`）、靠**文档顺序**取胜
# （与 r77 / r78 压 `.r74-ripple` 同一机制）。
# 落点 = 所有带 `r92-hdr-css` 的页面（实测 6 个：base / conversation / avatar / skills /
# automation / settings）。base 的净底注入后，base.html 与 conversation.html 天然各继承一份，
# 其余 4 页逐个插（revert 时逐个摘）。
HDR_ID = 'r101-hdr-css'
HDR_BODY = '''  /* r101 第②批 ②：顶栏装饰图（r92 ① 那张 `assets/images/bg-img-1.png`）按**宽度 70%** 缩放。
     原铺法是「不写 background-size」= 素材原尺寸 1580×134；顶栏高 48 ⇒ 竖直居中后上下各被裁掉
     （只露中间那条 48px 横带），横向在 1440 视口下右对齐、左端溢出 140px。
     本轮改成 `background-size: 70%`（单值 ⇒ 高按同比例自适应，落 `70% auto`）：
       · 图宽 = 视口宽 × 70%（1440 ⇒ 1008px），点阵密度随之变细（素材点距 8px ⇒ 5.6px）；
       · 仍右对齐 + 竖直居中（r92 那两条不动，本块只覆盖尺寸这一项）。
     ⚠ 本块**必须**排在 `r92-hdr-css` 之后（同特异性 ⇒ 后写者胜）：注入点固定在 `</body>` 前，
       而 r92 块也在 `</body>` 前、更靠前 ⇒ 恒成立。
     ⚠ 选择器与 r92 完全一致（`header[class*="h-12"]`，**不是裸 header 标签**）——
        avatar / task-detail 等页还有别的 `<header>`，裸标签会误伤（详见 r92 块里的注释）。 */
  header[class*="h-12"] {
    background-size: 70%;
  }
'''
HDR_BLOB = '<style id="%s">\n%s</style>\n' % (HDR_ID, HDR_BODY)
RE_HDR = re.compile(r'<style id="%s">.*?</style>\n?' % HDR_ID, re.S)

# ------------------------------------------------- r105 ③ 文件预览栏（三件套）
# 来源 = **数字分身** avatar.html 的「AV-BROWSE-SLOT v1」模块（r69 从任务详情页移植、r70/r71 更新）。
# 抽取方式见 `ev/extract105.py`：把 HTML / CSS / JS 三件**逐字抄出**（未做任何改写），
# 于是同一份内容在 avatar.html 与本页里逐字节一致 —— 将来对不上，先跑那个脚本比对。
#   · browse.html —— `<div class="td-split" id="av-browse-split">` + `<div class="td-browse-slot"
#     id="av-browse-slot">`（含顶栏 / 文件目录树 / 代码预览 / 两条分栏条）。**静态 HTML**：
#     与 avatar 同体位（插在样式表之后、脚本之前），这样控制器解析期就能拿到 slot，不必延迟挂载。
#   · browse.css  —— 面板 / 文件树 / 代码语法色 / 右键菜单 / 分栏条。
#   · browse.js   —— 只用它的**前半段**（`bindBrowseContextMenu` + `avToast` + 图标表，与页无关）；
#     后半段那个「按本页布局改写」的控制器见 `part105/ctrl-conv.js`（本页没有会话抽屉 / gutter，
#     预览栏直接接在 `main` 之后；宽度记忆的 localStorage key 也换成 `giencoder:r105-browse:v1`）。
# ⚠ 三件套都在**本代注入块内**（CSS 进 `r102-conv-css`、JS 进 `r102-conv-js`、HTML 是同一次
#   `inject_tail` 的静态片段）⇒ conversation.html 每次都由净底重建，天然幂等、不会累积。
# ★ r106：三件套仍是 r105 移植的那一份（**本代一个字节都没改**）⇒ 沿用「本代优先 → 上一代回落」
#   的资产体位（与上面的 RAWI_DIRS 同规矩），不在 git 里存第二份；本代若要覆盖某个文件，
#   放进 mg-work/r106/part106/ 同名即可。
#   ⚠ r106 ② 要改 `.td-browse-bar` 的高度，但**改的是本页适配层**（见 R106_CSS），
#     源件逐字不动 ⇒ `mg-work/r102/ev/extract105.py` 那套「与 avatar.html 逐字节同源」的校验
#     仍然成立。
PART_DIRS = (
    os.path.join(HERE, 'part106'),
    os.path.join(REPO, 'mg-work', 'r102', 'part105'),
)


def _read_part(name):
    for d in PART_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return io.open(p, encoding='utf-8').read()
    sys.exit('!! 缺少文件预览栏移植件 %s（找过：%s）' % (name, list(PART_DIRS)))


BROWSE_CSS = _read_part('browse.css')
BROWSE_HTML = _read_part('browse.html')
BROWSE_JS = _read_part('browse.js').split('\n(function () {\n  var KEY')[0] + '\n' \
            + _read_part('ctrl-conv.js')

# ★ r105 ③：文件预览栏的**暗色档**（移植时补的，源件保持逐字不动 ⇒ `extract105.py` 仍能证明同源）。
#   源页 avatar.html / task-detail.html **都没有**这个模块的暗色分支（avatar 里还有注释明说
#   「本页无 `[giencoder-theme='dark']` CSS 分支」）—— 但本模块这回第一次落到一个**有暗色分支**
#   的页面上（conversation.html 的 r93 一族全量做了暗色），按 PLAYBOOK 规则 5「字面 hex 必须在
#   `[giencoder-theme='dark']` 块补回」必须补。**只覆盖 browse.css 里那 6 个「设计稿实测色」自定义
#   属性，不动任何几何；浅色档一字未改**（改前/改后浅色计算值逐字节相同）。
#   实测（1440）：面板底 `--color-bg-1` 暗色 #17171a（自动翻转 ✓）；不补的话
#     ① 面板外缘线 #ECEEF2（近白）在暗底上成一条亮框；
#     ② 代码主色 #0451A5 与 #17171a 的对比度 ≈ 2.0（远低于 4.5）—— 变量名几乎读不出来；
#     ③ 文件树激活行 #ECF2FF（近白）在暗底上是一整块白。
BROWSE_DARK = r'''
/* ★ r105 ③：文件预览栏（.td-browse / .td-code / .td-bf）的**暗色档** —— 见 apply102.py 里本块注释。 */
[giencoder-theme='dark'] {
  /* 面板外缘线：浅色档 #ECEEF2（取 main 容器那一档灰）⇒ 暗色跟灰阶 3（实测 78,78,78）。 */
  --td-panel-line: rgb(var(--gray-3));
}
[giencoder-theme='dark'] .td-browse {
  /* 代码语法配色：浅色档是设计稿实测的 **VSCode Light** 三色（#0451A5 / #A31515 / #098658），
     压在暗底 `--color-bg-1` #17171a 上几乎不可读 ⇒ 换 **VSCode Dark+** 同位置三色
     （DS 无语义 token，故仍走本模块的自定义属性；出处 = VSCode Dark+ 默认主题）。 */
  --td-code-key: #569CD6; --td-code-str: #CE9178; --td-code-num: #B5CEA8;
  /* 文件树激活行：浅色 #ECF2FF 底 / #D3E2FF 描边（设计稿实测）⇒ 暗色改用蓝阶 7 的低透明度实心，
     保住浅色档那层「淡蓝底 + 深一档蓝描边」的层次（暗色下直接把近白铺上去会是一块白）。 */
  --td-tree-active-bg: rgba(var(--blue-7), 0.20);
  --td-tree-active-bd: rgba(var(--blue-7), 0.38);
  /* crumb 底线：浅色 #E7EBF1 ⇒ 暗色跟 border-1（实测 43,43,43）。 */
  --td-crumb-line: var(--color-border-1);
}
'''

# 守卫：静态片段里**不能**出现 `<script` / `<style` / `</script` —— 会打乱 main() 里的
# `<script>` 计数断言，也会让注入的 script 标签提前闭合（`</script>` 出现在 JS 字符串里）。
for _tok in ('<script', '</script', '<style', '</style'):
    for _label, _blob in (('browse.html', BROWSE_HTML), ('browse.js+ctrl-conv.js', BROWSE_JS),
                          ('browse.css', BROWSE_CSS)):
        if _tok in _blob:
            sys.exit('!! r105 ③ %s 里出现了 %r（会破坏注入结构）' % (_label, _tok))

# ------------------------------------------------- r106 四条（本代新增；②③④ 都是 CSS）
# ② `.td-browse-bar` 40 → 44：**只写 height**。源件（part105/browse.css）逐字不动。
# ③ 接缝：main 右两角归零 + 去掉 main 的右边框（那一根线让给面板）。
# ④ 三列自适应：预览栏展开时 main 只剩 779，而列宽仍锁 max(50%, 860) ⇒ 右侧被裁。
#    实测改前（1440，见 ev/p106a.log）：wrap [23,93,860] 右缘 883 vs main 右缘 791 ⇒ overRight +92；
#    底部列右缘 873（+82）；composer 更糟（left −28）。改后四列右缘 = main 右内缘 − 32（见 ④c）。
# ④b 用户消息块 `.r93-bub` 写死 728px（全仓唯一）⇒ 列窄于 728 时右对齐后向左溢出被裁。
#    证据 ev/p106i.log（1440/1370/1280 关·开）+ ev/p106l.log（.r93-bubi 727/728 蓝底盒）。
# ④c 空间不足时四列**各留 32px 内间距**（邵先生 2026-10-01 三次反馈）：④ 原把「可用宽」写成
#    `calc(100% + 20px)` = 吃满两侧 gutter ⇒ 列**紧贴** `.r93-pane` 左右边（1280 开时内间距 0）。
#    现改为「可用宽 − 64px」⇒ 距 pane 左右各 32px；空间足够时 `min()` 仍取原逻辑值 ⇒ 不变。
R106_CSS = r'''
/* ==================== r106 ②③④（会话详情页 · 文件预览栏的协作几何）====================
   ① 不在这里 —— 它是 JS(TMPL)：给两处 fold() 调用加 `open:false`（见本文件 r106 段）。
   下面四条里前三条只在 `html[data-r93-page='conversation']` **且** `.av-browse-on`
   （预览栏展开）时生效 ⇒ 浏览态 / 关闭态的外观一字未动；
   **唯一例外 = ④b 用户消息块 `.r93-bub`**（不带 `.av-browse-on`，理由见该条注释）。
   实测证据：mg-work/r106/ev/p106a.log、p106i.log、p106l.log、raw/a106-1-open.png（逐像素）。 */

/* --- ② 预览栏顶栏 40 → 44px，与 `.r93-bar` 同高（两条底线同在 y=93） ------------------------
   ⚠ 只覆盖 `height`：源件的 `padding: 4px 16px` / `align-items: center` 不动 ⇒ 里面那枚 32px
     胶囊上下各得 2px 余量、仍水平居中；底部那 1px 边框随盒高落到 44 的底边。
   ⚠ 走本页适配层而**不改 part105/browse.css** —— 那份要与源页 avatar.html 逐字节同源
     （校验脚本 mg-work/r102/ev/extract105.py）；且 `r93-bar` 只存在于本页，
     没有理由让 avatar / task-detail 跟着变高。 */
html[data-r93-page='conversation'] .td-browse-bar {
  height: 44px;
}

/* --- ③ 接缝：main 右侧两角改直角 + 那条线收成 1px ------------------------------------------
   改前（1440 逐像素，raw/a106-1-open.png）：
     · main 的圆角（`--radius` = 10px）**只暴露在右缘**（左边贴着左导航，看不见）⇒ 与面板
       左缘之间**漏出 10px 缺口**：上角 y=49..57 的 x=785..790、下角 y=883..891 的 x=787..790
       全是行底色 #F4F5F6；
     · 接缝是**两条 1px 并排**：x=790 是 #ECEEF2（main 的右边框）、x=791 是 #E5E5E5（面板左边框）。
   修法：① main 右两角归零 —— 与面板齐平；
         ② **去掉 main 的右边框**，把那一根线让给面板 —— 面板的左边线是设计稿专门为
            「与 AI 会话栏接缝」另取的一档（见 part105/browse.css「第 52 轮第 3 项」注释），
            故接缝的线归面板，恒 1px。
   ⚠ `border-right-width: 0` 只让 main 的**内容盒**宽 1px（Tailwind `border` 按 border-box）——
     边框盒宽仍是 779，面板位置、拖拽手感都不变；下面 ④ 的内容列正好借这 1px 贴到右内缘。 */
html[data-r93-page='conversation'] .av-browse-on main {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-right-width: 0;
}

/* --- ④ 预览栏展开时，内容列「空间不足才自适应（两侧各留 32px 内间距）、空间足够保持原逻辑」 --------
   改前：四列宽度都是 `max(50% × main 内宽, 860px)`（见各自规则里的 r94 ② / r95 ② / r97 ③ 注释）。
   main 一旦被预览栏挤到 779，860 这条**下限**就压过 50% ⇒ 内容列右缘 883 超出 main 右缘 791
   **92px**（滚动容器 `overflow: hidden` ⇒ 直接被裁）—— 这就是邵先生说的「内容被遮挡」。

   ★★ 本代口径（邵先生 2026-10-01 更正）：**只在「空间不足」时自适应**；**空间足够时保持原逻辑**
      `max(50% × main 内宽, 860px)`。⚠ 判据不是**视口分辨率**，而是**容器可用宽**
      （预览栏开/关、左导航收拢都会改它）⇒ 写成 `min(可用宽, 原逻辑值)`，天然跟着容器走：
        · 1440 开：可用 758 / 原逻辑 860 ⇒ 取 **714**（两侧各留 32px，不再溢 92px）
        · 2560 开：可用 1878（扣 64 后仍 1814）/ 原逻辑 **949** ⇒ 取 **949**（居中，与 r105 逐像素一致）

   ▸ 内容列 `.r93-wrap`：父盒是**滚动容器** `.r93-scroll`，带
     `scrollbar-gutter: stable both-edges`（左右各占 10px：778 → clientWidth **758**）
     ⇒ ① 可用宽 = `calc(100% − 44px)`（`+20px` 讨回两侧 gutter、再 `−64px` 留 32×2 内间距 ⇒ 恒 = pane 内宽 − 64）；
        ② 上限写 `max(calc(50% + 10px), 860px)` —— 这是**原逻辑的等价式**（`.r93-wrap` 的 `50%`
           基数比 `.r93-bottom` 少 20px，故 `+10px` 补偿；页内既有约定，`.r93-sk-in` 原来也是同款写法）；
        ③ 外距写 `calc((100% − 宽) / 2)` —— **不能用 `margin: 0 auto`**：宽 > 包含块时
           `auto` 在溢出方向只会退化成 0（实测原逻辑给出 mL 0 / mR −102 的**不对称**结果），
           必须显式算；④c 之后恒为 **+22px**（= 32px 内间距 − 10px gutter），不再出现负外距。
   ▸ 底部列 `.r93-bottom`：父盒就是 `.r93-pane`（778，**无 gutter**）⇒ 口径 = `min(calc(100% − 64px), max(50%, 860px))`。
     原规则自带 `margin: 0 auto` ⇒ 变窄后**自动居中**，不用另加外距。
   ▸ composer 外壳：父盒是 `div.mt-8`（778，hero 的 `px-6` 已被 r97 ③ 清零）⇒ 同底部列口径（`− 64px`）；
     **两行都必须带 `!important`** —— 原规则本身就是 `!important`、特异性 (0,3,6) 更高，
     这里靠 `html[data-r93-page] .av-browse-on` 前缀提到 (0,5,6) 才压得住。
   ▸ 骨架屏 `.r93-sk-in`：父盒是 `inset:0` 的 `.r93-sk`（= pane 大小、无 gutter）⇒ 同底部列口径（`− 64px`）。
     （原式 `calc(50% + 10px)` 是按「有 gutter」写的，而它的父盒其实**没有** gutter ⇒ 会宽出 10px；
      本轮顺手对齐内容列，骨架屏淡出时不会横跳。）
   ▸ **④c 空间不足时四列各留 32px 内间距**（邵先生 2026-10-01 三次反馈）：
     原来把「可用宽」写成 `calc(100% + 20px)` ⇒ 列**紧贴** `.r93-pane` 左右边（1280 开时列 = pane
     618、左右内间距 **0**）。改成「可用宽 − 64px」后，距 pane 左右各 **32px**。
     ⚠ 只改「撑满」那一支：`min()` 的另一支（原逻辑 `max(50% ± 10px, 860px)`）一字不动
     ⇒ 空间足够时（2560 开 949 与各关态）**逐像素不变**；仅「可用宽 − 64 < 原逻辑值」时才生效。
     ⚠ 四列**必须同改**（wrap `−44px` = `+20px − 64px`；bottom / composer / sk-in `−64px`），
       否则窄档下四列不同宽 —— 用户消息块 `.r93-bub` 跟着 wrap 走，无需另改。
   ▸ **④b 用户消息块 `.r93-bub`（邵先生 2026-10-01 二次反馈）**：原规则
     `.r93-bub { margin-left: auto; width: 728px; … }` —— **写死的 728px**（已全仓 grep：
     `pages/*.html` 里 `728px` 仅此一处），且它就是把蓝底气泡 `.r93-bubi` 撑成 728 的那一层
     （ev/p106l.log：`.r93-bubi` x[552..1280] w=728 BG=rgb(229,237,254)）。
     症状：内容列一旦窄于 728，这个**右对齐**（`margin-left:auto`）的块就**向左溢出**被
     `.r93-scroll` 的 `overflow:hidden` 裁掉 —— 实测 1370 开（列 708）溢 20px、
     1280 开（列 618）溢 **110px**；且 1440 关（列 860）/1440 开（列 778）/2560 关（列 1141）
     一律 728 不动 ⇒ 邵先生读到的「**宽度是固定的 728px**」。
     修法：`min(100%, 728px)` —— 列 ≥728 时**保持设计原样的 728**，列 <728 时跟着收。
     ⚠ **本条不吃 `.av-browse-on`**：溢出只取决于「列 ↔ 728」的大小关系，窄窗口下的**关态**
       同样会溢 ⇒ 全局生效才是对的。1440 关（860）与 2560 关（1141）下 `min` 取 728，
       与 r105 **逐像素一致**（唯一生效区间是「列 < 728」，而那本来就是坏的）。
   ⚠ 四列**必须同宽**（r97 的「全宽块等宽」）⇒ wrap 那条 `+10px` 补偿**不可省**。
   ⚠ 关态下 ④ 的 a) 四条**全部不生效**（都带 `.av-browse-on`）⇒ 关态与 r105 逐像素一致；
     唯一的 ④b 例外见上。 */
html[data-r93-page='conversation'] .av-browse-on .r93-wrap {
  width: min(calc(100% - 44px), max(calc(50% + 10px), 860px));
  min-width: 0;
  margin: 0 calc((100% - min(calc(100% - 44px), max(calc(50% + 10px), 860px))) / 2);
}
html[data-r93-page='conversation'] .av-browse-on .r93-bottom {
  width: min(calc(100% - 64px), max(50%, 860px)); min-width: 0;
}
html[data-r93-page='conversation'] .av-browse-on main > div > div.flex-1.justify-center > div.mt-8 > div {
  width: min(calc(100% - 64px), max(50%, 860px)) !important; min-width: 0 !important;
}
html[data-r93-page='conversation'] .av-browse-on .r93-sk-in {
  width: min(calc(100% - 64px), max(50%, 860px)); min-width: 0;
}

/* --- ④b 用户消息块 `.r93-bub`：写死 728px → 上限型 clamp（口径同 ④） -------------------------
   原规则：`.r93-bub { margin-left: auto; width: 728px; display: flex; flex-direction: column; }`
   （在 r93 段「用户消息」里，**非 !important**、特异性 (0,1,0)）⇒ 本页适配层 (0,2,1) 压得住。
   `margin-left: auto` 保留：列 ≥728 时维持「右对齐」，列 <728 时 `auto` 自然退化成 0 ⇒ 满行。 */
html[data-r93-page='conversation'] .r93-bub {
  width: min(100%, 728px);
}

'''

for _tok in ('<script', '</script', '<style', '</style'):
    if _tok in R106_CSS:
        sys.exit('!! r106 新增 CSS 里出现了 %r（会破坏注入结构）' % _tok)

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
    # ★ r105 ③：页头右侧两枚按钮的图标 —— **逐字取自数字分身 AI 对话框标题栏**
    # （avatar.html 的 `.td-right-acts`：`td-ico-max` / `td-ico-min` / panel），24 网格 / 2px 描边，
    # 渲染尺寸由 CSS 收到 14px（与数字分身 `.td-right-acts .td-round-btn svg` 同口径）。
    'fsmax': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/>'
             '<path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/></svg>',
    'fsmin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M8 3v3a2 2 0 0 1-2 2H3"/><path d="M21 8h-3a2 2 0 0 1-2-2V3"/>'
             '<path d="M3 16h3a2 2 0 0 1 2 2v3"/><path d="M16 21v-3a2 2 0 0 1 2-2h3"/></svg>',
    'panel': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M3 5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>'
             '<path d="M15 3v18"/></svg>',
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
    for d in RAWI_DIRS:
        p = os.path.join(d, fname)
        if os.path.exists(p):
            src = io.open(p, encoding='utf-8').read()
            break
    else:
        sys.exit('!! 找不到图标 %s（已查 %s）' % (fname, RAWI_DIRS))
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
    ic = dict(ICON_INLINE)
    ic.update(load_ow_icons())
    for k in sorted(ic):
        parts.append('  %s: %s' % (k, jsstr(ic[k])))
    return 'var ICON = {\n' + ',\n'.join(parts) + '\n};'


# ---------------------------------------------------------------- r101 ⑦ · 右键菜单图标
# 「任务产物」卡的右键菜单要**照搬 AI 对话框右栏 `td-browse-slot` 那一套**（邵先生原话），
# 故菜单图标直接复用 r54 / r57 落地在 mg-work/r69/part-ctx.js 里的那两组：
#   · 主菜单 7 枚线条图标（file / folder / message / brand / copy / apps / right）
#   · 「打开方式」子菜单 6 枚彩色品牌图标（VS Code / Trae / Chrome / Edge / Notes / 资源管理器）
# 为什么不塞进 ICON_FILES：extract_icon() 会给「0~1 种 fill」的图标统一补 `fill="currentColor"`，
# 而主菜单那 7 枚是 `fill="none"` + stroke 的**空心轮廓** —— 补上 fill 就变实心块。
# 故这里只在构建期做一次文本抽取、原样内联，零改写（品牌那 6 枚本来就是多色，同理不碰）。
OW_JS = os.path.join(REPO, 'mg-work', 'r69', 'part-ctx.js')
_OW_MAP = (('file', 'fopen'), ('folder', 'ffolder'), ('message', 'fmsg'), ('brand', 'fbrand'),
           ('copy', 'fcopy'), ('apps', 'fapps'), ('right', 'fright'))
_OW_CACHE = {}


def load_ow_icons():
    if _OW_CACHE:
        return _OW_CACHE
    src = io.open(OW_JS, encoding='utf-8').read()
    plain = dict(re.findall(r"\n\s*(\w+):\s*'(<svg.*?</svg>)'", src))
    brand = dict(re.findall(r"\{\s*id:\s*'(\w+)',\s*label:\s*'[^']*',\s*svg:\s*'(<svg.*?</svg>)'\s*\}", src))
    if len(plain) != 7 or len(brand) != 6:
        sys.exit('!! part-ctx.js 图标抽取异常：线条 %d 枚（应 7）/ 品牌 %d 枚（应 6）'
                 % (len(plain), len(brand)))
    for k, v in _OW_MAP:
        _OW_CACHE[v] = plain[k]
    for k, v in brand.items():
        _OW_CACHE['ow' + k] = v
    return _OW_CACHE


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
     ⚠ r104 ④ 代码审查后：`#327FCB` / `rgba(0,0,0,0.16)` / agent 四组 —— **这三组已随死代码一并删除**
       （零引用；agent 四组的原始值留档在 `:root` 块尾，需要时照抄恢复）。
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
  /* ★ r104 ④（代码审查）：下面两条原为字面值，与 DS 色阶**逐字节相同** ⇒ 改成引色阶三元组。
     ① 浅色像素零变化（取色逻辑没动，只是不再写死）；
     ② 暗色档由 DS 自动翻转（`orange-7` 暗色 = #FFB65D、`green-7` 暗色 = #7FD184）
        ⇒ 这两条**从此不需要在暗色块里重复声明**，少一处「改了浅色忘改暗色」的隐患。 */
  --r93-warn-ic: rgb(var(--orange-7));   /* 设计稿实测 #D25F00 = orange-7（告警条圆点） */
  --r93-ok: rgb(var(--green-7));         /* 设计稿实测 #30953B = green-7（绿色勾） */
  /* 「模型已切换」图标。设计稿实测 #333333 —— 色阶里**没有**这一档
     （gray-8 #4E4E4E / gray-9 #2B2B2B 都不是）⇒ 保留字面值，暗色等价在 dark 块补。 */
  --r93-ioc: #333333;
  /* ★ r96 ⑤：Token 速率行前两枚图标（复制 / 分支）。设计稿是 DS 的 `icon-wrapper`
     实例（PNG 实测 png(170,4670) 与 (204,4671) 的笔画色 = #6B6B6B，= 色阶 gray-7），
     比同行「Token 速率」文字（#868686 = gray-6）深一级 ⇒ 单列一条变量，别混用 text-3。
     ★ r104 ④：同理改成引 `gray-7` 三元组（浅色 #6B6B6B 不变；暗色自动变 #C9C9C9 ——
     正好等于原来手写在暗色块里的那一个）⇒ **删掉暗色档的重复声明**，两档只剩一处真相源。 */
  --r93-ioc2: rgb(var(--gray-7));
  /* ★ r97 ④：输入卡**下方**那行统计文字（设计稿 `fw647:20893`，640×16）。
     PNG 逐像素实测笔画色 = (169,169,169) = #A9A9A9 = DS 原始色阶 **gray-5**
     （不是 `--color-text-4` 的 gray-4 #C9C9C9，也不是 text-3 的 #868686）。
     直接引 `--gray-5` 三元组 ⇒ 暗色档自动跟着色阶翻转（暗色 gray-5 = #868686），
     故**本变量只在浅色档声明一次**，暗色块里不再重复。 */
  --r93-meta: rgb(var(--gray-5));
  --r93-dim: #C4C7C9;
  /* ★ r104 ④：原 `--r93-blue: #327FCB` 已删除 —— 全页零引用（产物卡蓝徽标后来改用
     `--color-primary-6`），属僵尸变量，留着只会误导 grep。 */
  /* ★ r99 ⑫：用户气泡里 `/命令` 胶囊（`.r93-pill`）的文字色。设计稿 `fw647:14402`
     的 `text/text` **没有显式字号**（走 DS 默认），字号由 PNG 墨迹反推为 14px 档；
     颜色 PNG 实测笔画 (52,145,250) = #3491FA —— **不是** `--color-primary-6` 的 #3770F7：
     同一张图上「网页搜索」那些蓝字实测正是 (55,112,247)，两者确为不同色。 */
  --r93-pillc: #3491FA;
  /* ★ r104 ④：原 `--r93-sb: rgba(0,0,0,0.16)`（卡内滚动条）已删除 —— 全页零引用，
     滚动条后来统一走 Tailwind 的 `scrollbar-*` 工具类，这条是 r93 早期遗留的僵尸。 */
  /* ★ r101 第②批 ①：毛玻璃标题栏（`.r93-bar`）的底色。**无设计稿依据** —— 设计稿只有一张
     静态画板，没有「滚动时标题栏压住内容」这一帧；按 DS 语义自定「底色 72% 透 + 12px 高斯」。
     ⚠ 必须走变量：暗色档要给等价替代（见下面 dark 块），写死 rgba(255,255,255,…) 会糊出白带。 */
  --r93-glass: rgba(255,255,255,0.72);
  /* ★ r102 ⑩ 的 `--r93-glass-h`（白度 86% 的 hover 档）**已在 r104 ④ 删除** ——
     r103 ③ 给药丸单开 `--r93-glass-pill-h` 之后它就彻底没人引用了（僵尸变量）。
     现在毛玻璃只有两族、各有明确归属：
       · `--r93-glass`（标题栏，72%）—— 横贯 44px 的压顶容器，透多了糊不住底下滚过的内容；
       · `--r93-glass-pill[-h]`（药丸，60% / 74%）—— 小胶囊，背后永远是正文，透一点更好看。 */
  /* ★ r103 ③：邵先生「「滚动到底部」按钮的模糊透明度可以再透一点」⇒ 药丸**单独一档**，
     **不与标题栏共用** `--r93-glass` —— 标题栏是横贯整条 44px 的压顶容器，透太多就糊不住
     从它底下滚过的内容；药丸是一枚小胶囊、背后永远是正文，透一点更好看。
     白度 72% → **60%**；hover 档按同一 delta（14 个百分点）从 86% → **74%**。 */
  --r93-glass-pill: rgba(255,255,255,0.60);
  --r93-glass-pill-h: rgba(255,255,255,0.74);
  --r93-hov-bg: #ECF2FF; --r93-hov-bd: #D3E2FF;
  /* ★ r104 ④：`--r93-a1..a4-bg/-ic/-bd` 共 15 条**已随 agent 卡一行退役一并删除**
     （r103 ④ 把那一行的 DOM 摘掉后，它们只剩 `.r93-agent*` 那族 CSS 在引用；
      本轮把那族 CSS 也删了 ⇒ 变量与规则同进同出，不会给门禁添「未使用变量」告警）。
     agent 徽标四组的原始值留档在这里，将来若要恢复整行，照抄即可：
       紫 #E6E1FC / #6E27D9 / #E2D3F9 · 靛 #E0E7FF / #4F46E5 · 蓝 #DBEAFE / #2563EB · 红 #FEE2E2 / #DC2626 */
  /* ★ r104 ④：两处 `box-shadow` 的字面 rgba 收进变量（本页禁止在声明里直接写色值）。
     值**逐字节照抄 r99/r101 落定的设计稿实测**，两处浅暗档同值 ⇒ 只在 `:root` 声明一次
     （自定义属性会继承，暗色块不重复）。 */
  --r93-sh: 0 4px 8px 0 rgba(0,0,0,0.08);   /* 浮层（`.r93-pop` 路径气泡）与药丸（`.r93-tobottom`） */
  --r93-sbsh: 0 2px 9px rgba(0,0,0,0.07);   /* 底部状态条（`.r93-sb`） */
}
[giencoder-theme='dark'] {
  --r93-line: #333335;
  /* ★ r101 第②批 ①：浅色档毛玻璃底的暗色等价（取暗色底 `--color-bg-2` = #232324 的 72%）。 */
  --r93-glass: rgba(35,35,36,0.72);
  /* ★ r103 ③：药丸专用档的暗色等价（60% / 74%，见浅色档注释）。 */
  --r93-glass-pill: rgba(35,35,36,0.60);
  --r93-glass-pill-h: rgba(35,35,36,0.74);
  --r93-card: #232324;
  --r93-edge: #333335;
  --r93-bubble: #24314C;
  --r93-bubble-sh: rgba(0,0,0,0.45);
  --r93-tag-bg: rgba(247,114,52,0.14);
  --r93-tag-bd: rgba(247,114,52,0.4);
  /* ★ r104 ④（代码审查）：浅色档那 3 条**设计稿实测字面值**的暗色等价。
     此前它们只在浅色档定义 ⇒ 暗色下直接漏用浅色值，最严重的是 `--r93-ioc`：
     #333333 压在 `--color-bg-2` = #232324 上 = **隐形图标**（实测见 acceptance 的审查表）。
     一律**引 DS 色阶/语义 token**，不再手写 hex；深浅两档从此都由色阶自动翻转：
       · ioc    模型图标      → gray-10（暗色 #F7F7F7）
       · dim    状态条圆点    → gray-4 （暗色 #6B6B6B）
       · tag-ic 「自动化」胶囊 → orange-6（暗色 #FF9A2E） */
  --r93-ioc: rgb(var(--gray-10));
  --r93-dim: rgb(var(--gray-4));
  --r93-tag-ic: rgb(var(--orange-6));
  --r93-warn-bg: rgba(255,190,110,0.1);
  --r93-warn-bd: rgba(255,228,186,0.26);
  /* r99 ⑫：浅色 #3491FA 的暗色等价（暗底上要提亮 ⇒ 取更浅一档蓝）。 */
  --r93-pillc: #6BA6FF;
  --r93-hov-bg: rgba(55,112,247,0.16); --r93-hov-bd: rgba(55,112,247,0.4);
  /* ★ r104 ④：以下三处**不再重复声明**（浅色档已改成随主题翻转的引用或两档同值），
     少一处「改了浅色忘改暗色」的隐患：
       · `--r93-warn-ic` / `--r93-ok` / `--r93-ioc2` —— 已引色阶（orange-7 / green-7 / gray-7）；
       · `--r93-meta` —— 已引 `--gray-5`；
       · `--r93-sh` / `--r93-sbsh` —— 投影两档同值（设计稿只有浅色稿，暗色不另造数值）。
       · `--r93-a1..a4-*` —— 随 agent 卡一行退役（见浅色档留档）。 */
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
  /* ★ r103 ⑤：修「底部对话框点击时**激活态外发光顶部被截断**」。
     根因（实测 5 组 A/B 截图，扫 y=698..711 中轴像素）：
       · 真实 composer 的激活态 = 它自己的 `box-shadow: rgba(55,112,247,.12) 0 0 0 3px`
         ＋ 描边转 `rgb(160,186,247)`；这圈光**向上外溢 3px**。
       · composer 顶边 y=705 与我们的宿主 `.r93-conv-host` 底边 y=705 **正好相切** ⇒
         那 3px 落在宿主的地盘里。
       · 宿主在 r101 第②批 ① 加了 `position: relative`（给毛玻璃标题栏当包含块）⇒ 它从
         「非定位 flex 项」（按 order-modified 顺序绘制 = 在 hero **之前**）
         变成「定位后代」（按**树序**绘制）—— 而宿主是 `appendChild` 追加的、排在 hero 之后
         ⇒ **宿主改绘在 hero 之上**，它那层 `--color-bg-2` 底把这 3px 光盖掉了。
     实测对照（中轴 y 702..704 的非白像素）：
       基线 / 宿主 `overflow:visible` → **无**（被盖）；宿主 `position:static` → **有**；
       hero 加 `position:relative + z-index:5` → **有**。⇒ `overflow` 无关，就是**绘制顺序**。
     修法：把 hero 提到正 z-index 层（flex 项的 `z-index` 即使 `position:static` 也生效，
     这里连 `position: relative` 一起给，取其确定）。宿主里那些更高的 `z-index`
     （`.r93-bar` 10 / 骨架屏 9 / `.r93-tbsticky` 3）仍在本层之上，互不打架（两者本就不重叠）。
     ⚠ **r104 ① 更正**：上面「两者本就不重叠」只对**盒子**成立，对**浮窗**不成立 ——
     composer 的下拉/技能浮窗是向上翻的，会伸进宿主的box里。正 z-index 会把它们封顶在本层，
     于是被宿主内部的 z-index 3/9/10 反压。**配套修法见 `.r93-conv-host` 的 `z-index: 0`**：
     宿主整体降成 0 级上下文 ⇒ 内部再怎么排也出不了宿主，本层的 1 恒胜。
     两处**必须成对存在**：只留这里（浮窗被遮）、只留那里（外发光又被盖）。 */
  position: relative !important; z-index: 1 !important;
}
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > .pointer-events-none {
  display: none !important;
}
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > div.mt-8 {
  margin-top: 0 !important;
}
/* ★★ r104 ②：底部对话框的**首帧守卫**（邵先生第 2 条：「刷新后、骨架屏之前总会先闪一下对话框」）。
   为什么纯 CSS 挡得住：外壳是 `<head>` 里的 `type="module"` 脚本（**延迟执行**），而我们这块
   样式表在文档尾 —— 两者都在**首次绘制之前**落地 ⇒ 只要默认就写成 `opacity: 0`，
   「React 先画对话框、我们的骨架屏后到」那个窗口从**根上**不存在，不靠时序抢跑。
   放行时刻＝ `data-r93-app="ready"`，由脚本在**骨架屏开始退场的那一拍（1100ms）**打上 ⇒
   读起来就是「骨架屏淡出 = 页面就绪」，对话框与骨架屏前后脚淡入淡出。
   ★ r104 ③ 复用：同一个开关顺带管「切到轨迹页要收起对话框」——
     状态机是**正交两维**：`data-r93-app`（loading ⇄ ready）× `data-r93-tab`（chat ⇄ trace），
     只有 `ready + chat` 这一格才显形。轨迹页那一格由脚本额外把 hero `display: none`
     （让宿主 flex:1 顺势长高，轨迹内容因此居中于整个视口高）。
   ⚠ 用 `opacity` 不用 `display` —— 保住占位，加载完成时零位移、零重排（加载态与就绪态同高）。
   ⚠ `pointer-events: none` 是必须的：不可见却可点，会点出一个「凭空出现的下拉」。
   ⚠ `opacity: 0` 会造层叠上下文，但只在隐藏态；`ready + chat` 时是 `opacity: 1`（不造）⇒
     不影响 r104 ① 的浮窗层级结论。 */
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > div.mt-8 {
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
html[data-r93-page='conversation'][data-r93-app='ready'][data-r93-tab='chat'] main > div > div.flex-1.justify-center > div.mt-8 {
  opacity: 1;
  pointer-events: auto;
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
  /* ★ r101 第②批 ①：宿主补 `position: relative` —— 它是毛玻璃标题栏 `.r93-bar` 的**包含块**
     （标题栏已改绝对定位浮在滚动口之上，见下）。`overflow: hidden` 原本就在 ⇒ 浮层不会外溢。 */
  position: relative;
  /* ★★ r104 ①：`z-index: 0` —— **一行修两类问题**，是本轮最要紧的一处。
     缘起：r103 ⑤ 给 hero（= 外壳渲染的 composer 容器）补了 `position: relative; z-index: 1`
     才修好「激活态外发光被截断」。但**正 z-index 会创建层叠上下文**，而 composer 的
     所有浮窗（`.giencoder-select-popup` z1000 / 技能浮窗 z9999 …）都是 hero 的定位后代
     ⇒ 它们的 z-index **被整体封顶在 hero 这一层（= 1）**，反而落到本宿主内部那些
     「数值更小的 z-index」之下：`.r93-tbsticky` 3 / `.r93-sk` 9 / `.r93-bar` 10。
     实测（1440，点开模型下拉）：下拉 rect `{x1039,y594,w202,h216}` 与
     `.r93-tbsticky::after` 的渐隐带（`y597~653`，z3）重叠 ⇒ 第 2/3 项
     「GLM 5.2 公司共用 / 异常不能用的大模型」被那层白渐变洗掉（见 `raw/z104-model-crop.png`）。
     修法：**不去动 hero（⑤ 的结论要保住），改把本宿主整体压成一层 0 级上下文** ——
     宿主成了层叠上下文后，它内部那些 3/9/10 就再也爬不出宿主这一层，永远在 hero（= 1）之下。
     ⇒ ⑤（外发光）与 ①（浮窗被遮）**同时成立**，且互不依赖谁大谁小。
     ⚠ 副作用（已知、可接受）：宿主内元素不再能压到 hero/composer 之上 —— 本页没有这种需求。 */
  z-index: 0;
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
/* ★ r101 ②：补上「浅两级」的文字色 —— 正文是 `--color-text-1`（gray-10），
   往下两级 = `--color-text-3`（gray-6）。DS 的 text 阶梯正是每级跨 **两个色阶**
   （text-1 gray-10 / text-2 gray-8 / text-3 gray-6 / text-4 gray-4）⇒「两级」= text-3。
   全页 `.r93-t12l` 实测只有 8 处（1440 读数）：
     · 4 处折叠头 meta（挂 `.r93-fm`，本来就被 (0,1,0) 后写的 `.r93-fm` 定成 text-3）→ 不变
     · 3 处「调用 N 个工具」卡里的汇总值（在 `.r93-sumrow` 里，本来继承 text-3）→ 变成同值，不变
     · 1 处「任务产物」标签（挂 `.r93-artlabel`，后写定成 text-3）→ 不变
     · **1 处「深度思考」卡正文**（`<div class="r93-t12l">`，在 `.r93-card` 里继承 text-1）
       → 由 #1F1F1F 变 #868686，**这是本条唯一的视觉变化**。
   ⚠ 该正文在设计稿里是 DS `text/text` 的「层级=主要」（= text-1，见 raw/design-1393-18748.html
     的 `fw647:15080`）⇒ 本轮是**邵先生主动下调一档**，不是还原设计稿。 */
.r93-t12l { font-size: var(--font-size-body-1); line-height: 22px; color: var(--color-text-3); }
/* ★ r101 ⑨：这一档字号 12 → **13px**。邵先生点的是折叠头那截 meta（`r93-t12l r93-fm r93-ell`），
   但「调用 N 个工具」卡的**汇总清单**（`.r93-sumrow`，与折叠头同卡、上下紧邻）也是一模一样的
   `.r93-t12l` 元信息值 —— 只改一半会在同一张卡里出现 13 / 12 两档，故**两条一起提**。
   本规则**不含 height** ⇒ 折叠头 22px 定高、`.r93-sumrow` 的 22px 定高都不受影响，
   展开 / 收起零跳动（r99 ⑧ 的成果）不会被破坏。
   ⚠ `.r93-card` 内的 `.r93-t12l` 不受影响：`.r93-card.r93-card *`（0,2,0）把它钉在 14px；
     `.r93-artlabel`（15px）写在后面、同为 (0,1,0) ⇒ 也不受影响。 */
.r93-t12l.r93-fm.r93-ell,
.r93-sumrow .r93-t12l { font-size: calc(13px * var(--ui-fs-ratio)); }
/* ★ r98 ①：**对话内容区的 14px 统一上调到 15px**。DS 字号档只有 body-3=14 / title-1=16，
   没有 15 ⇒ 走页面级覆盖。三条讲究：
     · **只写 font-size**，不碰 line-height/height ⇒ 上面三条的 `line-height: 22px` 仍由 apply88b
       派生成 `calc(22px * var(--ui-fs-ratio))`（字号杠杆继续生效）。⚠ 本规则自身不含
       `var(--font-size-*)`，故 unscale→scale 不会去动它（无行高/高度可动）。
     · 选择器保持 **(0,1,0)**：r97 ① 的 `.r93-card.r93-card *`（0,2,0）仍能把**卡内**文本压回 13px
       （绝不能给它加 `html[data-...]` 前缀 ⇒ (0,2,1) 会反超卡规则）。
     · 字号写成 `calc(15px * var(--ui-fs-ratio))` 而**不写裸 px 字面量**，与本工程字号杠杆口径一致
       （⚠ 措辞讲究：门禁会扫注释里的裸字号写法 ⇒ 注释里也别出现字面量）。 */
/* ★ r102 ① → r103 ①②：**回到 15px**。
   经过：r98 ① 把对话内容区统一上调到 15px → r102 ① 邵先生要求「`.r93-t14` 的字号 13px」→
   落到 13px → 本轮（r103）邵先生要求「`r93-t14 r93-c1` 这种**正文**字号默认是 15px」+
   「`r93-t14 r93-ell` 同类型的字号也是 15px」⇒ 即撤销 r102 ① 的字号部分（数字动效**保留**）。
   ⚠ ② 的两个例子（`.r93-c1` 是颜色类、`.r93-ell` 是截断类）**自己都不含 font-size**
     ⇒ 它们只是 `.r93-t14` 的两种挂法，本条改完自动跟着 15px（实测：`.r93-t14.r93-c1` 2 处、
     `.r93-t14.r93-ell` 35 处，全部落在 `.r93-t14` 上）。
   ⚠ 行高仍 22px 不动 ⇒ 定高的行（气泡 22 / 折叠头 22 / 药丸 32）**零跳动**（r99 ⑧ 的成果保住）。
   ⚠ 卡内不受影响：`.r93-card.r93-card *`（0,2,0）会把卡内文本钉在 14px，本规则 (0,1,0) 压不进去。
   ⚠ 影响面（实测）= **卡外**全部 `.r93-t14`（58 处）：展开/折叠头标题、用户气泡、附件名、
     药丸文案、状态条文案、助手告警行等；卡内 6 处一律不受影响。 */
.r93-t14 { font-size: calc(15px * var(--ui-fs-ratio)); }
.r93-t14m, .r93-t14b { font-size: calc(15px * var(--ui-fs-ratio)); }
/* ★ r102 ④：`.r93-t12.r93-nm`（改动汇总表头的 +800 / −125 这类数值）字号 12 → **13px**。
   `.r93-nm` 自己只声明颜色（text-3）、`.r93-t12` 是 12px ⇒ 用 (0,2,0) 提一档，
   与 r101 ⑨ 把同卡的折叠头 meta / 汇总值提到 13px 是同一口径（同一张卡里不出现 12/13 两档）。
   本规则不含 height / line-height ⇒ 表头 `.r93-dhead` 的 40px 定高不受影响。 */
.r93-t12.r93-nm { font-size: calc(13px * var(--ui-fs-ratio)); }
/* ★ r93 ②：卡内正文（12/20）、上下文注入（12/16）、居中提示卡片下的说明行（12/24 —— 
   设计稿 ui 778×24 / 300×24）。与 .r93-t14 严格区分。 */
.r93-t12c { font-size: var(--font-size-body-1); line-height: 20px; }
.r93-t12s { font-size: var(--font-size-body-1); line-height: 16px; }
.r93-t12h { font-size: var(--font-size-body-1); line-height: 24px; }
.r93-t16b { font-size: var(--font-size-title-1); line-height: 24px; font-weight: 600; }
.r93-ell { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
/* ★ r102 ①：「`.r93-t14` 里面的数字要有动效」—— 数字串**自下而上滑入**（odometer-lite）。
   —— 结构由 JS 在 `wire()` 里现包：把每个 `.r93-t14` 的文本节点里的连续数字串
      （`\d[\d,]*`，故 `18,320` 算**一串**、`1/3` 算**两串**）包成
      `<span class="r93-num"><i class="r93-num-i">5</i></span>`，并给每个 `i` 写 `--r93-ni`（同元素内**从 0 递增**）。
   —— 做法讲究：
       · 外层 `.r93-num` 是 `overflow: hidden` 的 inline-block = 「窗口」，内层 `<i>` 从
         `translateY(0.7em)` 滑到位 ⇒ 视觉就是数字**从窗口下沿滚进来**。
       · `vertical-align: bottom` 是为了让这枚 inline-block 的**基线不变**（`overflow != visible` 的
         inline-block 基线会退化成 margin box 底边；底部对齐 + 与行盒同高，能把数字压回原来的位置）。
       · 内层 `font-style: normal` —— `<i>` 默认斜体。
       · 外层**不设** width/height/line-height ⇒ 与父行盒同高（继承 line-height），数字字形位置不变。
   —— 延迟：`1.5s` 是**基础延迟**。它必须**大于**骨架屏的完整生命周期（r101 ⑪：1100ms 才开始淡出、
      +320ms 从 DOM 移除 ⇒ 1.42s 才彻底干净）。原来取 1.25s 会让数字在**骨架屏还盖着的时候**就滑完，
      用户根本看不到 —— 实测骨架屏 `is-out` 过渡期正好压在数字动画的前半段上，故提到 1.5s。
      之后每串再错开 55ms；`--r93-ni` 按**每个 `.r93-t14` 内部**重新从 0 计，
      故一张卡里最多累计几百毫秒，不会因为全页几十个数字而拖成几秒。
   —— `both` ⇒ 延迟期间停在 `from`（透明 + 下移），不会先闪一下原位置。 */
.r93-num { display: inline-block; overflow: hidden; vertical-align: bottom; }
.r93-num > .r93-num-i {
  display: inline-block; font-style: normal;
  animation: r93-num-in 0.46s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: calc(1.5s + var(--r93-ni, 0) * 55ms);
}
@keyframes r93-num-in {
  from { opacity: 0; transform: translateY(0.7em); }
  to   { opacity: 1; transform: none; }
}

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
/* ★ r101 第②批 ①：**毛玻璃标题栏**。邵先生：「对话内容滚动时，`r93-bar` 这个标题栏容器要呈现
   高斯模糊的毛玻璃效果」——「滚动时」是题眼：原来的 `.r93-bar` 是 `.r93-pane` 的**流内兄弟**
   （实测 bar [269,49,1162,44] / pane [269,93,…]，两者相切、内容永不到它底下），
   `backdrop-filter` 就没有 backdrop 可糊 ⇒ 必须让它**盖在滚动口上**。三处联动：
     · 宿主 `.r93-conv-host` 补 `position: relative`（包含块）；
     · 本规则由 `position: relative; flex: none` 改 `position: absolute; inset: 0 0 auto` ⇒
       脱离流、贴宿主顶边、左右撑满（1162 = 原宽度，故页头里的三件 `absolute` 子元素
       —— `.r93-seg`(left8) / `.r93-seg-cap`(50%) / `.r93-baracts`(right8) —— **坐标一字不变**
       （`.r93-baracts` 是 ★ r105 ③ 换上的按钮组，取代原先那枚 `.r93-morebtn`，两者同为 right8/top8）；
     · `.r93-scroll` 补 `padding-top: 44px` ⇒ 内容从标题栏下沿起排（静止态与改前逐像素一致），
       一旦滚动，内容就从它底下经过并被糊掉。
   `z-index: 10` 有据：骨架屏 `.r93-sk` 是 9 —— 原来标题栏在 pane **之外**、骨架屏盖不到它，
   现在它进了 pane 的box范围，必须压到骨架屏之上才能保住「加载中页头照旧可见」的观感。
   ⚠ 副作用（已知、可接受）：滚动条的**最上 44px** 会落在毛玻璃底下（被 72% 白 + 模糊洗淡）——
     与 macOS 那条「滚动条滑到标题栏底下就淡出」是同一种观感。
   ⚠ 底色走 `--r93-glass` 变量（暗色档有等价替代），不写死 rgba。 */
.r93-bar {
  position: absolute; top: 0; left: 0; right: 0; z-index: 10; height: 44px;
  border-bottom: 1px solid var(--r93-line);
  background: var(--r93-glass);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
}
.r93-seg {
  position: absolute; left: 8px; top: 8px;
  gap: 0; padding: 1px; border-radius: 6px; background: var(--color-fill-1);
}
/* ★ r102 ⑪：邵先生「`.r93-seg.giencoder-radio-group.giencoder-radio-group-button` 的**总高度**
   要调整为 28px，且在标题栏内**垂直居中**」。
   实测基线（1440）：`.r93-seg` 高 **34px**（= 内距 1 + 按钮 32 + 内距 1）、bar 44、
   `.r93-seg` 的 `top: 8px` ⇒ 上 8 / 下 2 ⇒ **贴下沿、不居中**。
   根因：页面当年只覆盖了 `height: 24px`，**DS 的 `min-height: calc(32px * ratio)` 没被覆盖**
   ⇒ min-height 顶住了 24（实测按钮仍是 32px 高）。
   ⇒ 本代**两条一起覆盖**（height + min-height = 26px）：
       总高 = 1 + 26 + 1 = **28px** ✓；
       `top: 8px` 保持不变即 `(44 − 28) / 2 = 8` ⇒ **上下各 8px，真居中** ✓。
   ⚠ 行高仍 22px（下一条），按钮高 26 ⇒ 文字垂直居中（沿用基线同一机制：32px 时文字
     居中于 (32−22)/2 = 5，现居中于 (26−22)/2 = 2）。
   ⚠ `.giencoder-radio-group-button` 的 DS 内距是 2px、`.r93-seg` 早覆盖成 1px（实测 1px）⇒ 不动。 */
.r93-seg .giencoder-radio-button { height: 26px; min-height: 26px; padding: 0 12px; border-radius: 5px; }
.r93-seg .giencoder-radio-button { font-size: var(--font-size-body-3); line-height: 22px; }
/* ★ r105 ②：选中态改由 **DS 官方滑块**承载 —— 邵先生「`.r93-seg` 切换时要有滑动动效」。
   DS 的分段控件本来就带滑块机制（`components.css` 的 `.giencoder-radio-button-slider`：
   `transition: transform .28s, width .28s`，`z-index:0` + `pointer-events:none`）；
   页面当年只覆盖了 checked 的**自绘白底 + 描边** ⇒ 位移没有载体，切换只能硬切。
   现在：滑块承担白底 + 描边，几何按本页口径对齐（`.r93-seg` 内距 1px / 按钮高 26 ⇒ top·left 1 / 高 26 / 圆角 5）；
   文字颜色与字重仍留在 label 上。几何由 JS 写（`r93SegMove`：宽 = 选中项 offsetWidth，位移 = offsetLeft − 1）。 */
.r93-seg .giencoder-radio-button-slider {
  top: 1px; left: 1px; height: 26px; border-radius: 5px;
  background: var(--color-bg-2); border: 1px solid var(--color-border-2);
}
/* 首帧（JS 还没定位）不带过渡 —— 滑块宽度不能从 0「长」到目标值。就绪后由 JS 摘掉该属性。 */
.r93-seg[data-r93-seg-init='0'] .giencoder-radio-button-slider { transition: none; }
.r93-seg .giencoder-radio-button-checked {
  background: transparent; border: 0;
  color: var(--color-primary-6); font-weight: 400;
}
.r93-seg .giencoder-radio-button-checked:hover { background: transparent; }
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
/* ★ r105 ③：页头右侧按钮组（原单枚 `.r93-morebtn` ⋯ 已被替换）。
   结构与类名**逐字对齐** avatar.html 的 `.td-right-acts`（DS Button 契约）：
     giencoder-btn + giencoder-btn-secondary + giencoder-btn-size-default + giencoder-btn-icon
   本页只加一层 `.r93-baract` 的**几何适配层**（DS 没有的尺寸口径），不改组件本体。
   ⚠ `border-color: transparent` 必须写 —— avatar 的 `.td-round-btn` 就是靠它去掉 DS 默认描边
     （不写的话页头会多出两条 1px 灰边框）；圆角**不覆盖**，随 DS 口径 8px（全站 large 档）。
   ⚠ 高度写 28px 与同一条标题栏上的 `.r93-seg`（28px）齐平（avatar 那边算出来是 32px，
     那是因为它的抽屉题栏比本页 44px 的毛玻璃标题栏更高；本页取 28 才是同一条线上的对齐）。
   ⚠ 图标本体 14px（`.r93-iblk.r93-i14` + `.r93-iblk > svg { width:100% }`），
     与 avatar 的 `.td-right-acts .td-round-btn svg { width:14px }` 同口径。 */
.r93-baracts {
  position: absolute; right: 8px; top: 8px;
  display: flex; align-items: center; gap: 8px;
}
.r93-baracts .r93-baract,
.r93-baracts .r93-baract:hover,
.r93-baracts .r93-baract:active {
  box-sizing: border-box; width: 28px; height: 28px; padding: 0;
  border-color: transparent; box-shadow: none; line-height: 0;
}
/* ★ r105 ③：「全屏 ⇄ 退出全屏」的两枚图标共用一枚按钮（同 avatar 的 .td-ico-max / .td-ico-min）。
   ⚠ 选择器带 `.r93-baracts` 前缀（(0,2,0)）——基础那条 `.r93-iblk { display: inline-flex }`
     是 (0,1,0)，不带前缀的 `.r93-ico-min { display:none }` 只是同特异性靠顺序取胜，太脆。 */
.r93-baracts .r93-ico-min { display: none; }
html[data-r93-full='1'] .r93-baracts .r93-ico-max { display: none; }
html[data-r93-full='1'] .r93-baracts .r93-ico-min { display: inline-flex; }
/* ★ r105 ③：**全屏**（`.r93-baract[data-r93-fullscreen]`）＝ 让左导航 aside 收拢到 0，
   对话区（main）吃满整行 —— 与数字分身全屏「让 main 让位」同语义（那边让的是 main，这边让的是 aside）。
   做法与 `.av-browse-on > aside:first-child`（r105 ③ 移植的文件预览栏）**完全同款**：
   外壳给 aside 的宽度是 React 内联 style ⇒ 必须 !important；它自带 overflow:hidden，
   收拢过程内容被裁掉，不用额外处理；摘掉属性即由外壳自带的 200ms transition-all 原样长回。 */
html[data-r93-full='1'] div:has(> main) > aside:first-child {
  width: 0 !important; min-width: 0 !important;
  padding-left: 0 !important; padding-right: 0 !important;
  opacity: 0; pointer-events: none;
}

/* ===================== 主体 ===================== */
.r93-pane { display: flex; flex-direction: column; flex: 1 1 auto; min-height: 0; }
.r93-pane[hidden] { display: none; }
/* ★ r104 ③：页签「对话 ⇄ 轨迹」的**滑动动效**（邵先生第 3 条）。
   两态一律是「外向位移 + 淡出 → 内向位移 + 淡入」，由脚本挂 `data-r93-slide` 驱动：
     · 出场（旧 pane）：`out-l` / `out-r` —— 朝**背离目标**的一侧滑 22px 并淡出；
     · 入场（新 pane）：`in-l` / `in-r` —— 先「无过渡」地摆到对侧 22px，撤掉属性即滑回原位；
     · 方向 = 目标页签的相对方位（去右边的「轨迹」⇒ 内容左移出、右移入）。
   ⚠ 位移量 22px 是「能看出方向、又不至于把卡片甩出去」的口径；两段各 0.24s，总 0.46s（含 0.22s 交接）。
   ⚠ 过渡只挂在**本宿主的直接子 pane** 上（`>` 必须留 —— 消息列 `TPL` 也叫 `.r93-pane`，
     是本页既有的**类名复用**，加 `>` 才不会误伤；该复用已记入本轮代码审查结论）。
   ⚠ 静止态 `transform` / `opacity` 都回到初始值 ⇒ 不留常驻层叠上下文（pane 里挂着
     骨架屏 `.r93-sk` 与 sticky 药丸，常驻 transform 会多出包含块，没必要冒这个险）。 */
html[data-r93-page='conversation'] .r93-conv-host > .r93-pane {
  transition: transform 0.24s cubic-bezier(0.4, 0, 0.2, 1),
              opacity 0.24s cubic-bezier(0.4, 0, 0.2, 1);
}
html[data-r93-page='conversation'] .r93-conv-host > .r93-pane[data-r93-slide='out-l'] { transform: translateX(-22px); opacity: 0; }
html[data-r93-page='conversation'] .r93-conv-host > .r93-pane[data-r93-slide='out-r'] { transform: translateX(22px); opacity: 0; }
html[data-r93-page='conversation'] .r93-conv-host > .r93-pane[data-r93-slide='in-l'] { transform: translateX(-22px); opacity: 0; transition: none; }
html[data-r93-page='conversation'] .r93-conv-host > .r93-pane[data-r93-slide='in-r'] { transform: translateX(22px); opacity: 0; transition: none; }
/* ★ r95：`scrollbar-gutter: stable both-edges` —— 滚动条占位会把本容器内容盒收窄，
   使内容列相对**没有滚动条**的底部列（`.r93-bottom`）与 composer 偏左半个滚动条宽
   （1440 实测偏 5px ⇒ 内容块右边界 1265 / 状态条 1270 / 输入卡 1280 三条线打架）。
   both-edges 让两侧各让出等量 gutter ⇒ 内容恒居中，与底部同轴。 */
.r93-scroll { position: relative; flex: 1 1 auto; min-height: 0; overflow-y: auto; overflow-x: hidden; scrollbar-gutter: stable both-edges; }
/* ★ r101 第②批 ①：补 `padding-top: 44px`（= 标题栏高）。
   标题栏改绝对定位后，滚动口的**上沿就是宿主顶边**（原先从标题栏下沿开始）⇒ 不补这一档，
   首屏内容会整块上移 44px 钻进毛玻璃底下，静止态就与改前不一致了。
   补上之后：静止态 = 内容仍从「标题栏下沿 + 32」起排（与改前逐像素相同）；
   滚动时 = 内容从这块 padding 里穿过去、被标题栏糊掉。 */
.r93-scroll { padding-top: 44px; }
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
/* ★ r99 ⑨（**已被 r101 ③ 取代，保留备查**）：hover 底色曾改为「白底 + 1px 描边」。
   理由：原 `--color-fill-2`（242）在**灰卡**（`.r93-card` = #F5F6F7）里比卡底还深，像一块脏斑；
   改动汇总卡的悬停行里 ⋯ 盒实测正是「白底 24×24 + 1px (229,229,230) 描边」，与 `.r93-dmore:hover` 同款。 */
/* ★ r101 ③：邵先生改成 **hover 只要浅灰底、不要边框** ⇒ 回到 `--color-fill-2`
   （= DS 组件自身的 hover 档位，与 Dropdown 菜单项 / `.r93-rbtn` 同一口径），box-shadow 整条撤掉。
   ⚠ 只改 `.r93-ib`：`.r93-dmore`（改动汇总行的「⋯」）落在**灰卡**上，fill-2 仍会显得比卡底深，
   r99 ⑨ 的白底 + 描边就是为它定的 —— 邵先生本轮只点了 `.r93-ib r93-bt` 这两枚，
   故 `.r93-dmore` 保持原样，两处口径暂不统一（等邵先生发话）。 */
.r93-ib:hover { background: var(--color-fill-2); }
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
/* ★ r99 ⑬（**已被 r102 ⑦ 回退**）：助手头底边线曾「深一级」到 `--color-border-2`（gray-3 = 229）。
   原注释记录：设计稿 `直线 28` 实测 (242,242,242) 确实是最浅那档（= `--color-border-1`，gray-2），
   但当时邵先生按可读性拍板深一级。
   ★ r102 ⑦：邵先生「`.r93-asst` 底部的线条颜色变浅一级」⇒ 回到设计稿原值 `--color-border-1`
   （即深一级 → 浅一级，等于撤销 r99 ⑬）。 */
.r93-asst { padding-bottom: 13px; border-bottom: 1px solid var(--color-border-1); }

/* ===================== 折叠块 ===================== */
.r93-fold { display: flex; flex-direction: column; }
.r93-fh {
  height: 22px; display: inline-flex; align-items: center; gap: 4px;
  align-self: flex-start; border-radius: 4px; color: var(--color-text-1); max-width: 100%;
}
/* ★ r101 ①：hover **不给底色**，只把前景色提到正文色。
   原来展开头 / 折叠头各铺一层 `--color-fill-2`（浅灰），邵先生本轮要求取消。
   展开态本来就已是正文色（`.r93-ft` 与 `.r93-fh .r93-cv` 都写死 `--color-text-1`）⇒
   只需撤掉底色；折叠态 `.r93-fc` 默认是 `--color-text-3`、图标挂 `.r93-c3`
   ⇒ hover 时把这两处一起提到 `--color-text-1`（`.r93-fm` 那截 meta 仍留 text-3，属次级信息）。 */
.r93-fh:hover, .r93-fc:hover { background: transparent; }
.r93-fc:hover, .r93-fc:hover .r93-c3, .r93-fc:hover .r93-t14 { color: var(--color-text-1); }
/* ★ r102 ⑥：hover 时后面的小字（`.r93-t12l.r93-fm.r93-ell` 这类 meta）也变**正文色**。
   r101 ① 只把「图标 + 主标题」提到了正文色，meta 仍留在 text-3 —— 邵先生本轮要求一起提。
   展开头（`.r93-fh`）与折叠头（`.r93-fc`）**两条都写**：邵先生点的是 `r93-fh`，但折叠头
   是同一枚「22px 行内按钮」的另一种状态，只改一半会在展开/收起两态间闪色。
   特异性：`.r93-fh:hover .r93-fm` = (0,3,0) > 基础 `.r93-fm` / `.r93-t12l` 的 (0,1,0)；
   与 `.r93-t12l.r93-fm.r93-ell`（同为 (0,3,0)，但那条只写 font-size、不写 color）也不冲突。 */
.r93-fh:hover .r93-fm, .r93-fc:hover .r93-fm,
.r93-fh:hover .r93-t12l, .r93-fc:hover .r93-t12l { color: var(--color-text-1); }
.r93-fh .r93-cv { color: var(--color-text-1); }
.r93-ft { color: var(--color-text-1); flex: none; }
.r93-fm { color: var(--color-text-3); min-width: 0; }
/* ★ r102 ③：折叠**收起**方向的动效（r101 ⑦ 只做了展开 —— 邵先生本轮要求补上）。
   —— 为什么不能沿用它那套：`.r93-fold[data-r93-open='0'] > .r93-fb { display:none }` 是**瞬间**消失，
      `display` 不可过渡；要「缩回去」必须换成**高度动画**。
   —— 做法：`max-height` 过渡（不是 `grid-template-rows`，因为后者要给 `.r93-fb` 外套一层包裹元素，
      得改 `fold()` 工厂产出的 DOM；`max-height` 零结构改动）。
   —— **精确高度**是这条的关键：`max-height` 从「CSS 兜底的大值」收到 0 会让动画前 90% 时间里
      内容看似不动、末尾突然塌（值域失真）。故 JS 在**每次开合前**把 `--r93-fbh` 写成
      `scrollHeight`（= 精确内容高），`max-height` 就在「精确值 ↔ 0」之间过渡 ⇒ 全程可见。
   —— `overflow: hidden` 只在过渡期间需要（收干净 + 展开时不外溢），但**常驻会剪掉卡内向上翻的
      popover**（`.r93-pop`）⇒ 交给 JS：展开稳定后（360ms）给 `.r93-fb` 挂 `.is-free` 放行。
      初始加载时所有折叠块都是展开态，`wire()` 会一并挂上 `.is-free`。
   —— ★ r103 ⑥：**开合两个方向现在完全同一套 transition**（不再有单向的 keyframes 动画），
      详见下面 `.r93-fb` 里的 ⑥ 注释。 */
.r93-fb {
  margin-top: 12px;
  max-height: var(--r93-fbh, 4000px);
  overflow: hidden;
  /* ★ r103 ⑥：四条属性一起过渡，**两个方向完全同一套**（曲线 / 时长 / 属性都对称）。
     · `opacity` 时长由 0.26s 改成 **0.32s** —— 与高度同步：收完的同时正好淡完，
       不会出现「已经透明了、盒子还占着高度」的空壳阶段。
     · 新增 `transform` 一条：原来「展开时的上滑弹入」是挂在 `[data-r93-open='1'] > .r93-fb` 上的
       **keyframes 动画**（r101 第②批 ⑦）。它有两个毛病：
         ① 只跑展开方向 ⇒ 两个方向观感不一致（邵先生本轮点名）；
         ② `animation` 一旦成立就**抢占该属性**（CSS Transitions 规定：属性被运行中的动画
            影响时不启动过渡）⇒ `data-r93-open` 翻回 0 时动画被移除，`opacity` 会从 1 **一帧硬切**
            到 0（实测 rAF：t=33 op=1 → t=134 op=0，而 max-height 还停在 150px）
            = 「内容瞬间消失、空盒子再慢慢收」= 邵先生看到的**闪动**。
       改成 transition 后：展开 = 淡入 + 下滑弹入 + 长高；收起 = 淡出 + 上滑 + 收高，**完全对称**。
     · `transform` 用回 r101 那条**回弹曲线**（back-out，端点超调 56%）⇒ 弹性没丢，
       且因为它是 transition 而不是 animation，**移除时不会有任何硬切**。 */
  transform: none;
  transition: max-height 0.32s cubic-bezier(0.4, 0, 0.2, 1),
              margin-top 0.32s cubic-bezier(0.4, 0, 0.2, 1),
              opacity 0.32s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.34s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.r93-fb.is-free { overflow: visible; }
/* ★ r103 ⑥：收起态多一条 `transform: translateY(-8px)` —— 与展开态的「从 -8px 滑到位」
   严格镜像（原来那 8px 只由单向 keyframes 提供）。 */
.r93-fold[data-r93-open='0'] > .r93-fb { max-height: 0; opacity: 0; margin-top: 0; transform: translateY(-8px); }
.r93-fc {
  height: 22px; display: inline-flex; align-items: center; gap: 4px;
  /* ★ r100 ⑦：补 `max-width:100%` —— 折叠头现在也可能带一截元信息（`.ctmeta`），
     没有上限就会顶出内容列；与展开头 `.r93-fh` 同口径。 */
  max-width: 100%; align-self: flex-start; border-radius: 4px; color: var(--color-text-3);
}
/* ★ r101 ①：折叠头的 hover 底色已撤（见上方合并规则），这里不再重复声明。 */
.r93-fold[data-r93-open='1'] > .r93-fc { display: none; }
.r93-fold[data-r93-open='0'] > .r93-fh { display: none; }
/* ★ r102 ③：原来这里还有 `.r93-fold[data-r93-open='0'] > .r93-fb { display: none }` —— 已删除：
   `.r93-fb` 的收起改由 `max-height: 0` + `overflow: hidden`（见上）承担，
   若保留 `display:none`，它会盖掉高度过渡、收起又变回瞬变。 */
/* ★ r101 第②批 ⑦：chevron 的旋转走**同一条回弹曲线**（原 `0.2s ease`）——
   展开/折叠两个方向都看得见这枚箭头，它的回弹就是整套动效的「另一半」。 */
.r93-cv { transition: transform 0.34s cubic-bezier(0.34, 1.56, 0.64, 1); }
/* ★ r101 ④（**已被 r102 ⑤ 调整**）：折叠箭头偏大 ⇒ **只缩 svg（14 → 10px），槽保持 14×14**。
   ①「小两号」按本工程图标档位（12 / 14 / 16 / 24）解读：14 → 12 → **10**。
   ② 槽宽不动是本条的关键 —— r99 ⑧ 当年就是为了让「展开 ↔ 收起」两态不横向抖动，
      才把折叠态的槽由 12 提到 14（标题左缘 = 槽宽 + gap4）。本轮若连槽一起缩，
      点一下标题就左移 2px，「不要引起跳动」的正是不许这么干。
   ③ 旋转仍作用在**槽**上、svg 居中于槽 ⇒ 两个中心重合，转动不偏心。
   特异性 (0,2,1) > `.r93-iblk > svg` 的 (0,1,1) ⇒ 与书写顺序无关。
   ★ r102 ⑤：邵先生「这个箭头下了，加大一号」⇒ 由 10px **加大一号**回到 **12px**
     （档位 10 → 12；仍未回到 r101 之前的 14）。槽依旧是 14×14 ⇒ 上面第 ②③ 条的
     「零横向跳动 + 转轴不偏心」继续成立。 */
.r93-iblk.r93-cv > svg { width: 12px; height: 12px; }
.r93-fold[data-r93-open='0'] .r93-cv { transform: rotate(-90deg); }

/* ★ r101 第②批 ⑦ → **r103 ⑥ 已整段退役**：原来这里挂的是
   `@keyframes r93-fold-in { from{opacity:0;transform:translateY(-8px)} to{opacity:1;transform:none} }`
   ＋ `.r93-fold[data-r93-open='1'] > .r93-fb { animation: r93-fold-in … }`。
   为什么必须撤掉（邵先生本轮点名的「折叠时闪动」的真凶）：
     · 它是**单向**的（只在展开方向成立）⇒ 展开/收起观感不一致；
     · 更严重：`animation` 成立期间会**抢占**它声明的属性，而 CSS Transitions 规定
       「属性被运行中的动画影响时**不启动过渡**」⇒ 折叠时 `data-r93-open` 翻回 0、动画被移除，
       `opacity` 从 1 **一帧硬切**到 0（实测 rAF：t=33 op=1 → t=134 op=0，此时 max-height
       还停在 150px）⇒ 用户看到的是「内容瞬间消失、空盒子再慢慢收」。
   现在那 8px 滑移改由 `.r93-fb` 的 `transform` **transition** 承担（回弹曲线照旧，
   两个方向镜像），并在收起态由 `[data-r93-open='0']` 补 `translateY(-8px)`。 */

/* ★ r101 第②批 ⑥：折叠头（`.r93-fc.r93-bt`）hover 时，**右端浮出一枚向右的箭头**
   （「这里点得开」的暗示），与前一件的间距 **8px**。
     · 间距：父级是 `gap: 4px` 的 inline-flex ⇒ 箭头再补 `margin-left: 4px`，合计 8px。
     · 图标：直接用「打开方式 ▸」子菜单里那枚 `fright`（同一位图库的右向 chevron），
       **不新画**，天然与全站箭头一致。
     · 常驻占位 + 只淡入（`opacity`）⇒ 悬停时箭头**不会把标题挤动**（`r93-*` 的 ellipsis 也
       因此在 hover 前后保持一致）。位移那 2px 是纯视觉的「滑入」，仍在按钮自身盒内。
   特异性：`.r93-fc:hover .r93-fchev` = (0,2,0) > 基态 (0,1,0)，与书写顺序无关。 */
.r93-fc .r93-fchev {
  /* ★ r102 ②：间距 **8 → 4px**（邵先生）。原为「父级 gap 4 + 本元素 margin-left 4」= 8；
     现在**去掉 margin**、只留父级 gap 4 ⇒ 图标与标题之间正好 4px（与标题前的图标槽同档）。
     ⚠ 常驻占位（不是 `display:none`）⇒ 间距变化**不会**在 hover 前后把标题挤动。 */
  margin-left: 0;
  opacity: 0; transform: translateX(-2px);
  transition: opacity 0.18s ease, transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.r93-fc:hover .r93-fchev { opacity: 1; transform: none; }

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
  /* ★ r102 ⑨：左侧内距 12 → **16px**（邵先生）。上下右三项不动 ⇒ `.r93-dh1` 里的图标槽、
     标题、+800/−125 整组**右移 4px**，表头 40px 定高与右侧 `.r93-dacts`（`margin-left:auto`）
     都不受影响。 */
  height: 40px; box-sizing: border-box; padding: 6px 6px 5px 16px;
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
  /* ★ r102 ⑧：padding 改 **0 16px**（邵先生）—— 原为左右不对称的 `0 13px 0 11px`
     （右端 13 是给「⋯」留的、左端 11 是设计稿行内缩进）。改后：
       · 文件名左缘 11 → **16**（与 r102 ⑨ 的表头同一条竖线，表头内容也落在 16）；
       · 「⋯」右缘 13 → **16**。
     `gap: 17px`（文件名 ↔ +800/−125 组 ↔ ⋯）与 36px 行高都不动。 */
  height: 36px; display: flex; align-items: center; gap: 17px; padding: 0 16px;
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
/* ★ r101 ⑩：补投影。设计稿 PNG 逐像素实测（`raw/design-rgb.png`，状态条 board(164,4876) 840×40；
   取样 x300..800 逐行平均灰度，背景为纯白 255）：
     下方 rel+0..+9 = 244 / 245 / 246 / 248 / 249 / 251 / 252 / 253 / 254 / 255
        ⇒ 峰值 Δ=11、**10px 才收干净**
     左方 rel-1..-5 = 249 / 251 / 252 / 253 / 254（约 5px、峰值 Δ≈6）
     上方 rel-1..-2 = 254 / 254.8（约 2px、极弱 ⇒ 说明有下沉 offset）
   ⇒ 档位**实测反推**（不是照搬 token）：DS 的 `--shadow1-down` 是 `0 2px 5px #0000001a`，
     峰值 Δ≈26 —— 实测只有 11 ⇒ 设计稿这一处比 token 弱一半以上，直接引 token 会明显偏重。
   本值是在**同一浏览器会话里内联试出来的**（`ev/p101shadow.sh`）：四档各拍一张、逐行比对 Σ|Δ|：
     0 2px 6px  α=.06  → 245 246 249 250 252 253 254 255 255 255   Σ|Δ|=17
     0 2px 9px  α=.07  → 244 245 247 248 250 251 252 253 254 254   Σ|Δ|= **3**  ← 采用
     0 2px 10px α=.07  → 244 245 247 248 249 251 252 253 253 254   Σ|Δ|= 3
     0 2px 12px α=.08  → 243 245 246 247 248 250 251 252 252 253   Σ|Δ|=10
   （9px 与 10px 打平；取 9px 是因为它的上方外溢更小，与设计稿「上方只有 2px 的极弱痕迹」一致。）
   ⚠ 本仓 `--shadow*` 虽在页面样式块里定义过，但 `getComputedStyle` 读不到（r93 头注释已记）
     ⇒ 这里写完整字面值，不走 `var()`。 */
.r93-sb {
  height: 40px; box-sizing: border-box; border-radius: 8px; background: var(--color-bg-2);
  border: 1px solid var(--color-border-2); display: flex; align-items: center;
  gap: 8px; padding: 0 16px;
  box-shadow: var(--r93-sbsh);
}
.r93-sbtxt { color: var(--color-text-1); }
.r93-sbmeta { color: var(--color-text-3); }
.r93-sbd { display: flex; align-items: center; gap: 6px; flex: none; }
.r93-sbic { display: inline-flex; align-items: center; color: var(--color-text-3); flex: none; }
.r93-sbchev { margin-left: auto; color: var(--color-text-2); display: inline-flex; }

/* ★ r93 ④：输入卡改为**复用外壳真实 composer** ⇒ 这里不再自绘 `.r93-input`。
   本容器只承载「状态条下方的 agent 卡行」；灰底/描边/圆角全部交给真实 composer 的
   `bg-[var(--color-fill-1)]` 外壳承担，避免出现两层灰壳叠罗汉。 */
/* ★ r104 ④（代码审查）：`.r93-cp` 这条规则**已删**。r103 ④ 把 agent 那一行的 DOM 摘掉后
   它就没人引用了（`.r93-cp` 这个类名现在全页 0 处 `class=` 命中，`r93-cpath` 是另一个类）。
   ⚠ 注意下面这条「下拉向上弹」是**活的**（real composer 的 select/权限弹层用），别一起删。 */

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
/* ★ r104 ④（代码审查）：`.r93-agents` / `.r93-agent*` / `.r93-agname` / `.r93-agdesc` /
   `.r93-agendi` 一族共 20 条规则（≈2.3 KB）**整族删除**。
   r103 ④ 按邵先生「这一行的内容都去掉吧」摘掉了 DOM，当时为「随时可恢复」留着这族 CSS；
   本轮审查判定为**死代码**并清掉，理由三条：
     ① 全页 `class="…"` 里 0 命中（不是「暂时隐藏」，是彻底没有宿主）；
     ② 同一族的 15 个 `--r93-a1..a4-*` 变量也一并删除 ⇒ **变量与规则同进同出**，
        不会留下「未使用变量」给门禁添告警（这才是 r103 保留它的真正理由，现已不成立）；
     ③ 本工程的日常手法是 grep 式定位 ⇒ 2.3 KB 死规则会持续污染检索结果。
   ⚠ 将来若要恢复那一行：`git show <r103 交付前>` 取回这族 CSS + 模板切片，
     变量原值见 `:root` 块尾的留档注释。 */

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
  /* ★ r102 ⑩：邵先生「滚动到底部按钮也调整为**毛玻璃效果**」⇒ 与 r101 ① 的标题栏同一套配方
     （`--r93-glass` + 12px 高斯）。原为实底 `--color-bg-2` + `--color-border-2` 描边。
     ⚠ 这枚药丸**浮在内容之上** ⇒ 背后永远有东西可糊（不像定高容器那样可能没有 backdrop）。
     ⚠ `-webkit-` 前缀与标准属性成对写（本页既有的毛玻璃标题栏也是这么写的）。
     ★ r103 ③：邵先生「模糊透明度可以再透一点」⇒ 底色从共用的 `--r93-glass`（72%）换成
       药丸专用的 `--r93-glass-pill`（**60%**）。标题栏**不动**（它要压住滚过的内容）。 */
  background: var(--r93-glass-pill);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  border: 1px solid var(--color-border-2);
  box-shadow: var(--r93-sh);
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
   底色沿用 r99 的 `--color-fill-1`：邵先生只点了「描边」与「前景色」两条，未要求撤掉底色。
   ★ r102 ⑩：底色改毛玻璃后，hover **不能再回 `--color-fill-1`**（那是不透明的，一 hover 毛玻璃
   就没了）⇒ 换成毛玻璃的 hover 档（白度 72% → 86%，仍是「透 + 糊」）。描边照旧不动。
   ★ r103 ③：底色降到 60% 后，hover 档同步降到 **74%**（`--r93-glass-pill-h`）。 */
.r93-tobottom:hover { background: var(--r93-glass-pill-h); color: var(--color-text-1); }
/* 文案随按钮同色（`.r93-t14` 自己有 (0,1,0) 的默认色 ⇒ 用 (0,2,0) 压回去）。 */
.r93-tobottom .r93-t14 { color: inherit; }
.r93-tobottom.is-on { display: inline-flex; }

/* ★ r101 ⑥：「`.r93-pane` 与底部对话框相切处的衔接处渐隐」（邵先生标了「重要」）。
   ── 为什么挂在 `.r93-tbsticky::after` 上，而不是给 `.r93-scroll` 加 mask：
     mask 确实是最顺手的写法（它按**滚动口**取景，与内容长度无关），但 mask 是**祖先级**的绘制
     效果 ⇒ 连滚动口内的一切一起淡出，包括那枚「滚动到底部」药丸（底边距滚动口底仅 12px，
     必落在任何 ≥16px 的渐隐带里）—— 浮按钮下半截发虚，是肉眼可见的瑕疵。
     改挂到已有的 0 高 sticky 壳 `.r93-tbsticky`（`bottom: 44px`）上：它本来就**恒被吸在
     滚动口底 − 44**，于是
       · 伪元素 `bottom: -44px` ⇒ 底边正好压在**滚动口底**（= 与底部对话框的衔接线）；
       · 高度 56 ⇒ 渐隐带 = 滚动口最下 56px（★ r101 第②批 ④：邵先生要求「距离稍微加大一点」，
         由 40 提到 56；底边不动，只把定色点往上推 ⇒ 越靠近衔接线越浓、且过渡更缓）；
       · `z-index: -1` ⇒ 伪元素的层级落在 `.r93-tbsticky` 自己的层叠上下文里，且
         **在流内子元素之前绘制** ⇒ 药丸盖在渐隐层之上、永远清晰；
       · 整个 `.r93-tbsticky` 是 `z-index: 3` ⇒ 渐隐层又盖在 `.r93-scroll` 的滚动内容之上。
       ⇒ 层级恰好是「滚动内容 < 渐隐层 < 药丸」。
   ── 渐变终点用 `var(--color-bg-2)`（浅色 #fff / 暗色 #232324，与宿主底色同源），
      不用 `#fff` 字面量 ⇒ 暗色档不会糊出一条白带。
   ── 已知边界：内容是 4290px、滚动口 500px（1440 实测）⇒ 恒定溢出，壳永远吸在底部。
      若某天内容短于滚动口，sticky 不会被拉动，渐隐带会停在内容末尾 —— 与药丸同款、
      且此时「相切」本身不存在，可接受。 */
.r93-tbsticky::after {
  content: ''; position: absolute; left: 0; right: 0; bottom: -44px; height: 56px;
  background: linear-gradient(to bottom, transparent, var(--color-bg-2));
  z-index: -1; pointer-events: none;
}

/* ===================== 轨迹空态 ===================== */
.r93-trace { flex: 1 1 auto; min-height: 0; display: flex; align-items: center; justify-content: center; }
.r93-tracebox { text-align: center; color: var(--color-text-3); }

/* ===================== 文件路径的 hover popover ===================== */
.r93-fpath { position: relative; display: inline-block; }
.r93-fpath > .r93-flink { color: var(--color-primary-6); }
.r93-pop {
  position: absolute; left: 0; bottom: 100%; margin-bottom: 6px; display: none;
  width: 314px; box-sizing: border-box; border-radius: 8px; background: var(--color-bg-2);
  border: 1px solid var(--color-border-2); box-shadow: var(--r93-sh);
  padding: 4px; gap: 4px; z-index: 5;
}
.r93-fpath:hover .r93-pop, .r93-pop:hover { display: flex; }
.r93-pop a { flex: 1 1 0; text-align: center; padding: 4px 0; border-radius: 4px; color: var(--color-primary-6); }
.r93-pop a:hover { background: var(--color-fill-2); }

/* ==========================================================================
   r101 追加规则（⑦ 右键菜单子菜单 / ⑧ 图标旋转 / ⑪ 骨架屏）
   —— 放在 CSS 段末尾：与既有规则同特异性时按书写顺序胜出，故这三块的「补 / 覆盖」都稳。
   ========================================================================== */

/* --- ⑧ 「压缩上下文」前面那枚图标转起来 ------------------------------------
   该图标是 DS 的 `icon-wrapper` 实例（无独立导出），本页用的是 `ICON.zip`，
   宿主 `<span class="r93-iblk r93-i14 r93-c3">`（r101 ⑧ 给它加了 `r93-spin`）。
   1.2s 线性无限：线性是刻意的 —— 缓动会让「转」这件事看起来一顿一顿的。
   ⚠ 只转 svg 不动盒子 ⇒ 该行 22px 定高与左侧竖线不受影响。 ------------------- */
@keyframes r93-spin { to { transform: rotate(360deg); } }
.r93-spin { animation: r93-spin 1.2s linear infinite; transform-origin: 50% 50%; }

/* --- ⑦ 右键菜单的「打开方式」二级菜单 --------------------------------------
   结构与主菜单**完全同构**（DS Dropdown 契约的 contextMenu 变体）：
     div.giencoder-dropdown-popup.r93-ctx.giencoder-dropdown-submenu-popup[role=menu]
   故这里让子菜单**同时挂 `.r93-ctx`**，直接白拿上面那整套面板/菜单项/分隔线样式；
   本页产物里没有 `.giencoder-dropdown-submenu` / `-submenu-popup` 的编译样式（它们在
   task-detail.html 里也没有，r69 是靠**纯 JS 摆 left/top** + 面板类撑起来的）⇒
   这两条只做「契约占位 + 让子菜单不被父级 flex 拉伸」，位置一律由 JS 给 left/top。 */
.r93-ctx.giencoder-dropdown-submenu-popup { position: fixed; }
.r93-ctx .giencoder-dropdown-submenu { position: relative; }
.r93-ctx .giencoder-dropdown-submenu.is-hover { background: var(--color-fill-2); }
/* 右向箭头：与文字同档的 14px 盒子，居中 14px 的箭头 svg；靠 `.r93-ctx-label` 的
   `flex: 1` 自然顶到右缘（设计稿 `836:28993` 实测箭头 14px、色 = --color-text-3）。 */
.r93-ctx .giencoder-dropdown-arrow {
  flex: none; width: 14px; height: 14px; display: inline-flex;
  align-items: center; justify-content: center; color: var(--color-text-3);
}
.r93-ctx .giencoder-dropdown-arrow svg { display: block; width: 14px; height: 14px; }
/* 二级菜单项里的品牌图标是**多色**的（VS Code / Trae / Chrome / Edge / Notes / 资源管理器）
   ⇒ 标签自带的 fill 出彩，`.r93-ctx-ico` 的 `color` 只影响其中那枚单色的 GienCoder 徽标，
   无需额外规则。 */

/* --- ⑪ 骨架屏 Skeleton ------------------------------------------------------
   复用 DS **已经编译进本页**的 `.giencoder-skeleton-line / -title / -avatar`
   （渐变 + `1.4s infinite giencoder-skeleton-loading`，色走 `--color-fill-2/3`），
   不自己重画一套。外层 `.r93-sk` 覆盖整个 `.r93-pane`（= 对话内容区 + 底部状态条列），
   因为「对话内容模块」在结构上就是这一整块；页面真实 composer 在外壳里、不受影响。
   ⚠ `.r93-pane` 原本没有 `position`（static）⇒ 这里补 `relative` 作为 `.r93-sk` 的包含块；
     它不影响任何既有子元素（都是流内布局，没有依赖 static 定位的绝对定位后代）。 */
.r93-pane { position: relative; }
.r93-sk {
  position: absolute; inset: 0; z-index: 9; overflow: hidden;
  background: var(--color-bg-2);
  display: flex; flex-direction: column;
  transition: opacity 0.3s ease;
}
.r93-sk[hidden] { display: none; }
.r93-sk.is-out { opacity: 0; }
/* 内层与内容列同宽同轴（`.r93-wrap` 是 `calc(50% + 10px)` / min 860 ⇒ 这里照抄，
   保证骨架屏的横轴与真实内容完全一致，淡出时不会左右错位）。
   ★ r101 第②批 ①：上内距 32 → **76**（= 44 标题栏 + 32 内容留白）。根因：`.r93-sk` 的定位父级
   是 `.r93-pane`，而标题栏改绝对定位后 pane 从宿主顶边起算 ⇒ 不补这 44，骨架屏会比真实内容
   整体高 44px、头两条直接钻进毛玻璃底下。 */
.r93-sk-in { width: calc(50% + 10px); min-width: 860px; box-sizing: border-box; margin: 0 auto; padding: 76px 0 0; }
.r93-sk-gap { height: 32px; }
/* 用户气泡：右对齐的两条短灰条 */
.r93-sk-bub { display: flex; flex-direction: column; align-items: flex-end; gap: 10px; }
.r93-sk-bub > .giencoder-skeleton-line { width: 62%; margin: 0; }
.r93-sk-bub > .giencoder-skeleton-line:last-child { width: 34%; }
/* 助手头：头像 + 名称 */
.r93-sk-head { display: flex; align-items: center; gap: 8px; }
.r93-sk-head > .giencoder-skeleton-avatar { width: 24px; height: 24px; }
.r93-sk-head > .giencoder-skeleton-title { width: 96px; height: 16px; margin: 0; }
/* 正文若干行 */
.r93-sk-body { margin-top: 16px; }
.r93-sk-body > .giencoder-skeleton-line:last-child { width: 58%; }
/* 代码卡：灰底 + 内嵌几行 */
/* ★ r101 第②批 ③：骨架屏里那块「浅灰容器」已**去掉**（邵先生：「骨架屏显示时有一个浅灰色的
   容器，需去掉」）。它原来照真实内容里那张灰卡（`.r93-card` = `--r93-card`）画了个同色圆角盒 ——
   但骨架屏阶段内容还没出现，先铺一块灰底反而像「一个加载失败的空盒」。
   故 `background` / `border-radius` / `padding` 三项一起撤，只留 3 条灰条 + 20px 上间距；
   撤掉 `padding` 后灰条的左缘与上面那 3 条正文条对齐（都在内容列 0 位）。 */
.r93-sk-card { margin-top: 20px; }
.r93-sk-card > .giencoder-skeleton-line { margin-bottom: 12px; }
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
     真机上只出现其中一个 —— data-r93-open 切换。 */
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
      /* ★ r101 第②批 ⑥：折叠头右端的**hover 箭头**（右向 chevron，基态 `opacity: 0` 常驻占位）。
         用它暗示「这一条点得开」；hover 时淡入，连同 `margin-left: 4px` 与父级 `gap: 4px`
         一起给出邵先生要的 8px 间距（详见 CSS `.r93-fc .r93-fchev` 注释）。 */
      + '<span class="r93-iblk r93-i14 r93-fchev">' + IC('fright') + '</span>'
      + '</button>';
    /* ⚠ `o.mt` 用 `!= null` 判空：`mt:0` 也要真的落成 `--mt:0px`（原来 `o.mt ?` 会把 0 当假值
       ⇒ 内嵌层退化成默认的 16px 上边距）。已有调用全传真值，行为不变。 */
    return '<div class="r93-it r93-fold" data-r93-open="' + (o.open === false ? '0' : '1') + '"'
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
      ic: 'ctx', t: '上下文注入', meta: 'skill-catalog', mt: 12, open: false,   /* ★ r106 ①：默认折叠 */
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
      ic: 'think', t: '深度思考', mt: 16, open: false,   /* ★ r106 ①：默认折叠 */
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
        /* ★ r101 ⑤：卡头右侧原来有「绿勾 + 复制」两枚，绿勾已按邵先生要求删掉，只留复制。
           归属判定（页面里 `.r93-okc` 共 2 处，见 ev/p101a.log 的 `okc` 读数）：
             · 本处 Bash 卡头 x1225 / y987 —— 同一折叠块内、与 ④ 的箭头上下相邻，且**没有文案可指**；
             · 另一处是「上下文已压缩」行首 x669 / y3089 —— 那行有「上下文已压缩」这串文案可指，
               邵先生要删的显然是「只能靠类名指认」的那枚。
           ⇒ 本处删除；「上下文已压缩」那枚**保留**（设计稿 PNG 上同样是绿勾，见
             raw/design-1393-18748.html 的 `1393:18525` → `svg_812e0422.svg`，色 = `--r93-ok`）。
           ⚠ 待邵先生复核：若指的是另一枚，把这一行挪回去即可（脚本重跑即自愈）。 */
        + '<span class="r93-cmk">'
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

    /* ---------- ⑮ 压缩上下文 ----------
       ★ r101 ⑧：行首那枚图标加 `r93-spin` ⇒ 常转（`@keyframes r93-spin` 1.2s linear infinite）。
       用「额外加一个类」而不是改 `.r93-iblk` 本身 ⇒ 只影响这一枚，其余图标纹丝不动。 */
    '<div class="r93-it" style="--mt:24px"><div class="r93-note"><i class="r93-nline"></i>'
    + '<div class="r93-nrow"><span class="r93-iblk r93-i14 r93-c3 r93-spin">' + IC('zip') + '</span>'
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
       ★ Token 速率行在画稿里是**独立容器** 1393:18599（840×24 @ +20），故拆成下一块。
       ★ r101 ⑦：每张卡补 `data-r93-artname`（= 文件名），供右键菜单的「复制路径」用；
         「查看所有产物」不是文件 ⇒ 不打这个属性（菜单里「复制路径」对它自然空转）。 */
    '<div class="r93-it" style="--mt:24px"><div class="r93-arts">'
    + '<div class="r93-artdiv"><i class="r93-nline"></i><span class="r93-artlabel r93-t12l">任务产物</span><i class="r93-nline"></i></div>'
    + '<div class="r93-artgrid">'
    /* ★ r106 ②：产物卡文件名**不再有默认蓝色**。
       原先把第 2 张卡（spec-template.md）用内联 `style="color:var(--color-primary-6)"` 标蓝 ——
       内联是最高优先级，把 CSS 里「`.r93-artname` 默认 text-1、`.r93-artcard:hover .r93-artname`
       才转 primary-6」的既有规则整条压死 ⇒ 邵先生 2026-10-01 指出「默认不该是蓝、hover 才是」。
       修法 = 只是**删掉那处内联**，CSS 侧一行未动（hover 变蓝照旧）。 */
    + [['arthtml', 'prd-template.html'], ['arthov', 'spec-template.md'], ['artmd', 'user-story-breakdown-template.md'],
       ['artmd', 'user-story-template.md'], ['artall', '查看所有产物 (12)']].map(function (c, i) {
      return '<button class="r93-artcard r93-bt" type="button"'
        + (c[0] === 'artall' ? '' : ' data-r93-artname="' + E(c[1]) + '"') + '>'
        + '<span class="r93-iblk r93-artic">' + IC(c[0]) + '</span>'
        + '<i class="r93-artsep"></i><span class="r93-arttxt">'
        + '<span class="r93-t14m r93-artname r93-ell">' + E(c[1]) + '</span>'
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
    /* ★ r103 ④：邵先生「`r93-agents` 这一行的内容都去掉吧」⇒ **整行（含容器）退役**。
       原本是 4 张 agent 卡（游戏策划 / 项目经理 / 软件开发工程师 / 测试工程师），
       排在状态条与真实 composer 之间。连它专属的容器 `.r93-cp` 一起摆掉（该容器只承载这一行）。
       ⚠ 相关 CSS（`.r93-cp` / `.r93-agents` / `.r93-agent*` / `.r93-ag*`）**已于 r104 ④ 整族删除**
         （r103 当时为「随时可恢复」保留，本轮审查判定为死代码 —— 连它专用的 15 个
          `--r93-a1..a4-*` 变量一并清掉，不会给门禁添「未使用变量」告警）。恢复办法见 CSS 段说明。
       ⚠ 连带效果：`.r93-bottom` 由 112px 收到 52px，底部整块上移（实测见 acceptance）。 */
    /* ★ r93 ④：自绘输入卡整组已删 —— 输入框改用外壳 React 渲染的真实 composer（见脚本头）。 */
    '</div>'
  ].join('');

  var HEAD = [
    '<div class="r93-bar">',
    '<div class="r93-seg giencoder-radio-group giencoder-radio-group-button" role="radiogroup" data-r93-seg-init="0">',
    /* ★ r105 ②：DS 官方滑块指示器（选中态的白底 + 描边现在由它承载，见 CSS 段）。 */
    '<span class="giencoder-radio-button-slider" aria-hidden="true"></span>',
    '<label class="giencoder-radio-button giencoder-radio-button-checked" data-r93-tab="chat">'
    + '<span class="giencoder-radio-button-text">对话</span></label>',
    '<label class="giencoder-radio-button" data-r93-tab="trace">'
    + '<span class="giencoder-radio-button-text">轨迹</span></label>',
    '</div>',
    '<div class="r93-seg-cap"><span class="r93-t16b r93-capname r93-ell">开发管理系统单文件工作台…</span>'
    + '<span class="r93-captag r93-t12"><span class="r93-iblk r93-i12">' + IC('auto') + '</span>自动化</span>'
    + '<span class="r93-t12 r93-captime">07月02日 15:26</span></div>',
    /* ★ r105 ③：页头右侧由单枚「⋯」（`.r93-morebtn`，**本来就没有行为**）换成
       **「全屏」+「打开侧栏」**两枚 —— 邵先生原话「就是数字分身 AI 对话框的 `td-right-acts` 那一部分」。
       ⇒ 类名与结构**逐字对齐** avatar.html 的 `.td-right-acts`（DS Button：secondary + size-default + icon），
         只把 avatar 的 `.td-round-btn` 换成本页前缀的 `.r93-baract`（几何在 CSS 的适配层，见下）。
       ⚠ 全屏两枚图标共用一枚按钮：`.r93-ico-max` / `.r93-ico-min` 由 `<html data-r93-full>` 切换显隐
         （与 avatar 的 `.td-ico-max` / `.td-ico-min` 同机制）。 */
    '<div class="r93-baracts">',
    '<button class="r93-baract giencoder-btn giencoder-btn-secondary giencoder-btn-size-default '
    + 'giencoder-btn-icon" type="button" aria-label="全屏" aria-pressed="false" title="全屏" '
    + 'data-r93-fullscreen="1"><span class="r93-iblk r93-i14 r93-ico-max">' + IC('fsmax') + '</span>'
    + '<span class="r93-iblk r93-i14 r93-ico-min">' + IC('fsmin') + '</span></button>',
    '<button class="r93-baract giencoder-btn giencoder-btn-secondary giencoder-btn-size-default '
    + 'giencoder-btn-icon" type="button" aria-label="打开侧栏" aria-pressed="false" title="打开侧栏" '
    + 'data-r93-browse="1"><span class="r93-iblk r93-i14">' + IC('panel') + '</span></button>',
    '</div>',
    '</div>'
  ].join('');

  var TRACE = '<div class="r93-pane r93-trace" hidden><div class="r93-tracebox">'
    + '<div class="r93-t14">暂无轨迹数据</div></div></div>';

  /* ★ r101 ⑪：进入页面先显示**骨架屏 Skeleton**（邵先生第 11 条）。
     三件套 `.giencoder-skeleton-line / -title / -avatar` 是 DS **已经编译进本页**的（r93 头注释
     里有原始 CSS），渐变 + 1.4s 无限闪烁全部现成 ⇒ 这里只搭骨架、不重画样式。
     形状照内容走：右对齐用户气泡（2 条）→ 助手头（头像 + 名称）→ 正文 3 行 → 一张灰卡 3 行。
     退场：`wire()` 里 1.1s 后加 `.is-out`（透明度过渡 0.3s），再 0.32s 后从 DOM 摘掉。 */
  var SKEL = [
    '<div class="r93-sk" aria-hidden="true"><div class="r93-sk-in">',
    '<div class="r93-sk-bub">',
    '<div class="giencoder-skeleton-line"></div>',
    '<div class="giencoder-skeleton-line"></div>',
    '</div>',
    '<div class="r93-sk-gap"></div>',
    '<div class="r93-sk-head"><div class="giencoder-skeleton-avatar"></div>',
    '<div class="giencoder-skeleton-title"></div></div>',
    '<div class="r93-sk-body">',
    '<div class="giencoder-skeleton-line"></div>',
    '<div class="giencoder-skeleton-line"></div>',
    '<div class="giencoder-skeleton-line"></div>',
    '</div>',
    '<div class="r93-sk-card">',
    '<div class="giencoder-skeleton-line"></div>',
    '<div class="giencoder-skeleton-line"></div>',
    '<div class="giencoder-skeleton-line"></div>',
    '</div>',
    '</div></div>'
  ].join('');

  var full = HEAD
    + '<div class="r93-pane" data-r93-pane="chat">'
    + SKEL
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

  /* ★ r102 ③ → r103 ⑥：把 `.r93-fb` 的真实高度写进 `--r93-fbh`（= `max-height` 的过渡起点）。
     ⚠ **必须在「翻 `data-r93-open` 之前的那一帧」写**（见 setFold：先 refreshFbh，rAF 里再翻属性）。
       踩过两次坑：
       ① 若「写变量」与「翻 data-r93-open」落在**同一帧**，会被合并成一次样式重算 ⇒ 浏览器只比较
          「上一帧的兜底 4000px → 本帧的 0」，收起过渡从 4000 起步
          （实测 rAF 曲线：`222 222 222 … 194 120 66 30 8 0`，前 2/3 时间里内容纹丝不动）。
          `void fb.offsetHeight` 强制 style flush **实测无效**。
       ② 只靠「wire 时 + 1.8s 后」提前维护也不够：**嵌套折叠**一收起，外层块的内容高度就变了，
          而外层那个变量还停在旧值（实测 fold#10 = `--r93-fbh:314px` 而真实高只有 170px）
          ⇒ 收起时前 46% 的时长里高度不动、之后突然塌 —— 这也是一种「闪」。
       ⇒ 现在的做法：**每次开合都重新量**（refreshFbh），并把翻属性推迟一帧（rAF）——
          这样浏览器能看见中间态 `max-height: 真实值`，过渡起点天然正确。 */
  function refreshFbh(fb) {
    if (fb) fb.style.setProperty('--r93-fbh', fb.scrollHeight + 'px');
  }

  /* ★ r102 ③ → r103 ⑥：折叠开合的**唯一入口**（点击委托与初始 `.is-free` 都走它）。
     —— `overflow: hidden` 会剪掉卡内**向上翻**的 popover（`.r93-pop`）⇒ 它只在「开合过渡期间」
        是必需的，故展开稳定后（360ms）挂 `.is-free` 放行；收起时立刻撤掉（收的过程必须裁剪）。
     —— 初始就展开的块由 wire() 统一挂 `.is-free`（页面加载时全员展开，见 wire 开头）。
     —— ★ r103 ⑥ 的顺序：`refreshFbh`（本帧）→ `requestAnimationFrame` 里翻 `data-r93-open`（下一帧）。
        多等一帧肉眼不可见（≈16ms），换来的是「过渡起点恒等于真实高度」。
        连点防护：上一帧没跑完的 rAF 先 `cancelAnimationFrame`。 */
  function setFold(f, open) {
    var fb = null, kids = f.children, i;
    for (i = 0; i < kids.length; i++) {
      if (kids[i].classList && kids[i].classList.contains('r93-fb')) { fb = kids[i]; break; }
    }
    var want = open ? '1' : '0';
    if (!fb) { f.setAttribute('data-r93-open', want); return; }
    fb.classList.remove('is-free');
    clearTimeout(fb.__r93free);
    refreshFbh(fb);                       /* 本帧：把真实高度写进变量（此时 data-r93-open 还没翻） */
    if (f.__r93raf) cancelAnimationFrame(f.__r93raf);
    f.__r93raf = requestAnimationFrame(function () {
      f.__r93raf = 0;
      f.setAttribute('data-r93-open', want);  /* 下一帧：过渡起点已就位 */
    });
    /* 两个方向都跑满 0.32s 过渡；落定后再刷新一次变量（并放行 overflow）。 */
    fb.__r93free = setTimeout(function () {
      if (want === '1') fb.classList.add('is-free');
      refreshFbh(fb);
    }, 360);
  }

  /* ★ r102 ①：把 `.r93-t14` 文本里的**数字串**包成 odometer 结构（样式见 CSS `.r93-num`）。
     —— 幂等：元素内已有 `.r93-num` 就整体跳过（wire 可能被 MutationObserver 重调）。
     —— 只替换**文本节点**（TreeWalker 只取 SHOW_TEXT）⇒ 内嵌的标签/图标一律不碰。
     —— `--r93-ni` 按**每个 `.r93-t14` 内部**从 0 重新计 ⇒ 单卡内最多几百毫秒错开；
        基础延迟 1.25s 由 CSS 承担（让过骨架屏的 1.1s 覆盖期）。 */
  function wrapNums(host) {
    var els = host.querySelectorAll('.r93-t14');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.querySelector('.r93-num')) continue;
      var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false);
      var texts = [], nd;
      while ((nd = walker.nextNode())) { if (/\d/.test(nd.nodeValue)) texts.push(nd); }
      for (var j = 0; j < texts.length; j++) {
        var node = texts[j], s = node.nodeValue, re = /\d[\d,]*/g, m, last = 0, seq = 0, hit = false;
        var frag = document.createDocumentFragment();
        while ((m = re.exec(s))) {
          hit = true;
          if (m.index > last) frag.appendChild(document.createTextNode(s.slice(last, m.index)));
          var sp = document.createElement('span');
          sp.className = 'r93-num';
          var it = document.createElement('i');
          it.className = 'r93-num-i';
          it.style.setProperty('--r93-ni', seq++);
          it.textContent = m[0];
          sp.appendChild(it);
          frag.appendChild(sp);
          last = m.index + m[0].length;
        }
        if (!hit) continue;
        if (last < s.length) frag.appendChild(document.createTextNode(s.slice(last)));
        node.parentNode.replaceChild(frag, node);
      }
    }
  }

  function wire(host) {
    /* ★ r101 ⑪：骨架屏退场。1100ms 后淡出（CSS `.r93-sk.is-out` 过渡 0.3s），
       再 320ms 从 DOM 移除 —— 移除而非 `hidden`，免得留一个 `position:absolute` 的盒子
       在后面持续参与合成。 */
    var sk = host.querySelector('.r93-sk');
    if (sk) {
      setTimeout(function () {
        sk.classList.add('is-out');
        setTimeout(function () { if (sk.parentNode) sk.parentNode.removeChild(sk); }, 320);
      }, 1100);
    }
    /* ★ r104 ②：与骨架屏退场**同一拍**放行底部对话框（= CSS 那个 `data-r93-app="ready"` 开关）。
       —— 刻意独立于上面的 `if (sk)`：万一骨架屏节点缺失，对话框也不能被永久锁在隐藏态。
       —— 数值与骨架屏的 1100ms 一致 ⇒ 骨架屏开始淡出、对话框开始淡入，是一组交叉过渡。 */
    setTimeout(function () {
      document.documentElement.setAttribute('data-r93-app', 'ready');
    }, 1100);
    /* ★ r102 ① + ③：进页面立即做的两件初始化。
       ① 数字动效包装 —— 越早越好，免得数字先以「原样、无动效」出现一帧；
       ③ 初始就展开的折叠块挂 `.is-free` —— 否则 `.r93-fb` 上常驻的 `overflow: hidden`
          会把卡内向上翻的 popover（`.r93-pop`）剪掉（页面加载时折叠块全员展开）。 */
    wrapNums(host);
    [].forEach.call(host.querySelectorAll('.r93-fold[data-r93-open="1"] > .r93-fb'), function (fb) {
      fb.classList.add('is-free');
    });
    /* ★ r102 ③：**提前**把每块的真实高度写进 `--r93-fbh`（展开态 + 字体就绪时）——
       详见 refreshFbh() 的注释：等到点击那一刻才写会与 data-r93-open 合并成一帧、起点退化成兜底值。
       两次：立即一次（绝大多数块此时已可测），1.8s 再一次（骨架屏退场 + 字体落定后校正）。 */
    [].forEach.call(host.querySelectorAll('.r93-fold > .r93-fb'), refreshFbh);
    setTimeout(function () {
      [].forEach.call(host.querySelectorAll('.r93-fold > .r93-fb'), refreshFbh);
    }, 1800);
    /* 页签 —— ★ r104 ③ 重写：从「直接切 hidden」改为「滑动交接 + 轨迹页收起对话框」。
       ① 滑动：旧 pane 朝**背离目标**的一侧滑出 22px 并淡出，新 pane 从对侧滑入
          （两态规则在 CSS 的 `data-r93-slide`，本函数只管挂/摘属性）。
       ② 收起：对话框是**外壳 React 渲染**的（在宿主之外、hero 盒里）——
          CSS 只能把它隐形，整块让位要额外把 hero 置 `display: none`：宿主是 `flex: 1 1 auto`
          ⇒ 顺势长高，轨迹内容因此垂直居中于**整个视口高**（否则会被对话框挤在上方 656px 里）。
       ③ 交接时序 = 「旧 pane 先滑干净（R93_SWAP）→ 改高度 → 新 pane 滑入」：
          高度突变那一拍画面里恰好没有内容（新 pane 还是 `in-*` 的 `opacity: 0`）⇒ 看不到跳；
          反过来写就会看到对话框「在半透明时突然消失」。
       ④ 状态分两处：`host.__r93tabId` 是**防连点的真相源**；DOM 上的 `data-r93-tab` 只给 CSS 看，
          且刻意**延后**翻 —— 去轨迹时立刻翻（对话框先淡出），回对话时挪到交接之后再翻
          （这样对话框才真有一次淡入，而不是 `display` 恢复瞬间硬出现）。 */
    var R93_SWAP = 220;                            /* 旧 pane 滑出时长（ms），与 CSS 的 0.2s 对齐 */
    function r93Composer(onTrace) {
      var hero = document.querySelector('main > div > div.flex-1.justify-center');
      if (hero) hero.style.display = onTrace ? 'none' : '';
    }
    function r93SetTab(id) {
      if (host.__r93tabId === id) return;
      host.__r93tabId = id;
      var doc = document.documentElement;
      var chat = host.querySelector('[data-r93-pane="chat"]');
      var trace = host.querySelector('.r93-trace');
      var to = (id === 'trace') ? trace : chat;
      var from = (to === chat) ? trace : chat;
      var right = (id === 'trace');                /* 目标在右侧 ⇒ 内容整体向左走 */
      if (right) doc.setAttribute('data-r93-tab', 'trace');
      from.hidden = false;
      from.setAttribute('data-r93-slide', right ? 'out-l' : 'out-r');
      to.setAttribute('data-r93-slide', right ? 'in-r' : 'in-l');
      to.hidden = false;
      clearTimeout(host.__r93tabT);
      host.__r93tabT = setTimeout(function () {
        from.hidden = true;
        from.removeAttribute('data-r93-slide');
        r93Composer(right);
        requestAnimationFrame(function () {
          to.removeAttribute('data-r93-slide');
          if (!right) doc.setAttribute('data-r93-tab', 'chat');
        });
      }, R93_SWAP);
    }
    if (!host.__r93tabId) {
      host.__r93tabId = 'chat';
      document.documentElement.setAttribute('data-r93-tab', 'chat');
    }
    [].forEach.call(host.querySelectorAll('[data-r93-tab]'), function (lb) {
      lb.addEventListener('click', function () {
        var id = lb.getAttribute('data-r93-tab');
        [].forEach.call(host.querySelectorAll('[data-r93-tab]'), function (o) {
          o.classList.toggle('giencoder-radio-button-checked', o === lb);
        });
        r93SegMove();                              /* ★ r105 ②：滑块跟着选中项滑过去 */
        r93SetTab(id === 'trace' ? 'trace' : 'chat');
      });
    });
    /* ★ r105 ②：页签滑块定位（DS 官方 `.giencoder-radio-button-slider` 机制）。
       位移 = 选中项 `offsetLeft` − 1（本页 `.r93-seg` 的内距是 1px；DS 原生口径是 2px）；
       宽度 = 选中项 `offsetWidth`。只写行内几何，**过渡在 CSS 里**（0.28s，官方同值）。
       ⚠ 必须在 `.r93-seg` 的 `data-r93-seg-init="0"` 摘掉**之前**完成首次定位 ——
         否则滑块会从 0 宽「长」出来；同理字体落定/视口变化都要重定位（文字宽会变）。 */
    var segGroup = host.querySelector('.r93-seg');
    function r93SegMove() {
      if (!segGroup) return;
      var sl = segGroup.querySelector('.giencoder-radio-button-slider');
      var on = segGroup.querySelector('.giencoder-radio-button-checked');
      if (!sl || !on) return;
      sl.style.width = on.offsetWidth + 'px';
      sl.style.transform = 'translateX(' + (on.offsetLeft - 1) + 'px)';
    }
    r93SegMove();
    requestAnimationFrame(function () {            /* 两帧后再放开过渡（首帧那次不能播动画） */
      requestAnimationFrame(function () {
        if (segGroup) segGroup.removeAttribute('data-r93-seg-init');
      });
    });
    if (document.fonts && document.fonts.ready && document.fonts.ready.then) {
      document.fonts.ready.then(r93SegMove);
    }
    window.addEventListener('resize', r93SegMove);
    setTimeout(r93SegMove, 1200);                  /* 与骨架屏退场同一拍再校一次（--ui-fs 已落定） */
    /* ★ r105 ③：页头「全屏」（`.r93-baract[data-r93-fullscreen]`）。
       语义 = 左导航 aside 收拢到 0、对话区吃满整行（CSS 里那条 `html[data-r93-full='1'] …`）。
       状态放 `<html data-r93-full>` 而不是宿主上：宿主会被 React 重渲染替换，html 上的属性不会丢。
       宽度变化后要让外壳与文件预览栏控制器都重算一遍 ⇒ 顺手派发一次 `resize`（两者都监听它）。
       ⚠ 暴露成自定义事件 `r93:fullscreen` 给预览栏控制器用 —— 它要在**自己那层 Esc 之后**
         才轮到关全屏（Esc 逐层关），而它比本脚本更晚注册，直接调函数会反序。 */
    function r93SetFs(on) {
      var doc = document.documentElement;
      if (on) doc.setAttribute('data-r93-full', '1'); else doc.removeAttribute('data-r93-full');
      var b = host.querySelector('[data-r93-fullscreen]');
      if (b) {
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
        b.setAttribute('title', on ? '退出全屏' : '全屏');
        b.setAttribute('aria-label', on ? '退出全屏' : '全屏');
      }
      try { window.dispatchEvent(new Event('resize')); } catch (e) {}
    }
    host.addEventListener('click', function (ev) {
      var t = ev.target;
      if (!t || !t.closest) return;
      if (!t.closest('[data-r93-fullscreen]')) return;
      r93SetFs(!document.documentElement.hasAttribute('data-r93-full'));
    });
    document.addEventListener('r93:fullscreen', function (ev) {
      r93SetFs(!!(ev.detail && ev.detail.on));
    });
    /* 宿主被 React 重渲染换掉 ⇒ 按钮上的 aria 状态要按 `<html>` 上的真相重画一次 */
    if (document.documentElement.hasAttribute('data-r93-full')) r93SetFs(true);
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
      /* ★ r102 ③：改走 setFold() —— 它要在改 `data-r93-open` **之前**把真实高度写进 `--r93-fbh`，
         并在展开稳定后挂 `.is-free`（放行卡内 popover）。 */
      setFold(f, f.getAttribute('data-r93-open') !== '1');
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

    /* ★ r101 第②批 ⑤：**两条菜单合一**。
       r99 ⑦ 那套「改动汇总行」专用菜单（`.r93-ctx` 的 4 项：查看文件 / 查看改动 /
       复制文件路径 / 撤销此文件改动）**整段退役** —— 邵先生：「`r93-diff` 这个容器里的
       右键菜单和更多菜单，需要和任务产物卡片的右键菜单保持一致」。
       ⇒ 全页只剩**一张** FMenu（= 下面那套照搬 `td-browse-slot` 的 6 项 + 「打开方式 ▸」6 项），
         触发器扩到三处：产物卡右键 / 改动汇总行右键 / 改动汇总行左键（含行内那枚「⋯」）。
       `runF` 的「复制路径」对两类触发器都成立：产物卡读 `data-r93-artname`、
       汇总行读 `data-r93-file`（该属性 r99 ⑦ 就在，本次沿用）。
       ⚠ 原来那套 `.r93-ctx` 的**面板 / 菜单项 / 分隔线样式一条都不用改** ——
         新旧两张菜单本来就共用同一个类名，退役后 CSS 反而只剩一个使用者。 */
    /* ★ r101 ⑦：「任务产物」卡的右键菜单 —— **照搬 AI 对话框右栏 `td-browse-slot` 那一套**
       （r54 / r57 落地在 `mg-work/r69/part-ctx.js`，本仓右键菜单的权威范本；图标也直接从它抽，
       见脚本头 `load_ow_icons()`）。邵先生本轮只要求给产物卡补这个菜单。
       ★ r101 第②批 ⑤：这张菜单现在是**全页唯一**的一张（上面 r99 ⑦ 那张 4 项菜单已退役）——
       变动汇总行的右键 / 左键 / 「⋯」三处都改用它。故下面那句「与 r69 版的两处差异」里，
       第一句提到的「本页既有右键菜单」已经不存在了，但「不做键盘导航」这条口径**照旧保留**。
       与 r69 版的两处差异（都是刻意的）：
         · **不做键盘导航**（↑/↓/←/→/Enter）—— 与邵先生此前对 Table 右键菜单的要求
           （不要键盘快捷选中态）保持一致；只留 Esc 关闭。
         · 二级菜单**同时挂 `.r93-ctx`** ⇒ 面板 / 菜单项 / 分隔线样式全部复用本页已内联的那套。 */
    var OW_ITEMS = [
      { id: 'vscode',   label: 'VS Code',        ic: 'owvscode' },
      { id: 'trae',     label: 'Trae',           ic: 'owtrae' },
      { id: 'chrome',   label: 'Google Chrome',  ic: 'owchrome' },
      { id: 'edge',     label: 'Microsoft Edge', ic: 'owedge' },
      { id: 'notes',    label: 'Notes',          ic: 'ownotes' },
      { id: 'explorer', label: '文件资源管理器',  ic: 'owexplorer' }
    ];
    var FCTX_ITEMS = [
      { id: 'open',     label: '打开',            ic: 'fopen' },
      { id: 'reveal',   label: '打开所在文件夹',   ic: 'ffolder' },
      { id: 'chat',     label: '添加到对话',       ic: 'fmsg' },
      { id: 'brand',    label: '添加到 GienCoder', ic: 'fbrand' },
      { id: 'path',     label: '复制路径',         ic: 'fcopy' },
      { divider: true },
      { id: 'openwith', label: '打开方式',         ic: 'fapps', children: OW_ITEMS }
    ];
    /* 通用建单：`extra` 给二级菜单加 `giencoder-dropdown-submenu-popup` 契约类。
       泛型到「每一项都挂 data-r93-fctx」⇒ 主 / 子菜单共用同一套事件委托。 */
    var buildFMenu = function (items, extra) {
      var box = document.createElement('div');
      box.className = 'giencoder-dropdown-popup r93-ctx' + (extra ? ' ' + extra : '');
      box.setAttribute('role', 'menu');
      items.forEach(function (it) {
        if (it.divider) {
          var d = document.createElement('div');
          d.className = 'giencoder-dropdown-divider';
          d.setAttribute('role', 'separator');
          box.appendChild(d);
          return;
        }
        var row = document.createElement('div');
        row.className = 'giencoder-dropdown-item'
          + (it.children ? ' giencoder-dropdown-submenu' : '');
        row.setAttribute('role', 'menuitem');
        row.setAttribute('tabindex', '-1');
        row.setAttribute('data-r93-fctx', it.id);
        if (it.children) row.setAttribute('aria-haspopup', 'menu');
        row.innerHTML = '<span class="r93-ctx-ico" aria-hidden="true">' + IC(it.ic) + '</span>'
          + '<span class="r93-ctx-label"></span>'
          + (it.children
              ? '<span class="giencoder-dropdown-arrow" aria-hidden="true">' + IC('fright') + '</span>'
              : '');
        row.querySelector('.r93-ctx-label').textContent = it.label;
        box.appendChild(row);
      });
      box.style.display = 'none';
      document.body.appendChild(box);
      box.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
      return box;
    };
    var fm = null, fsub = null, fSubRow = null, fArt = null;
    var closeFSub = function () {
      if (!fsub || !fSubRow) return;
      fSubRow.classList.remove('is-hover');
      fSubRow = null;
      fsub.classList.remove('giencoder-popup-open');
      setTimeout(function () { if (!fSubRow && fsub) fsub.style.display = 'none'; }, 200);
    };
    var openFSub = function (row) {
      if (!fsub) {
        fsub = buildFMenu(OW_ITEMS, 'giencoder-dropdown-submenu-popup');
        fsub.addEventListener('click', function (e) {
          var r = e.target && e.target.closest ? e.target.closest('[data-r93-fctx]') : null;
          if (r) runF(r.getAttribute('data-r93-fctx'));
        });
        fsub.addEventListener('pointerleave', closeFSub);
      }
      if (fSubRow === row && fsub.classList.contains('giencoder-popup-open')) return;
      closeFSub();
      fSubRow = row;
      row.classList.add('is-hover');
      var r = row.getBoundingClientRect();
      fsub.style.display = 'flex';
      fsub.style.visibility = 'hidden';
      var w = fsub.offsetWidth, h = fsub.offsetHeight;
      /* DS 契约 submenu-popup：left = calc(100% + 4px) / top = 0；右/下溢出时翻边并夹回 */
      var left = r.right + 4, top = r.top;
      if (left + w > window.innerWidth - 8) left = Math.max(8, r.left - 4 - w);
      if (top + h > window.innerHeight - 8) top = Math.max(8, window.innerHeight - 8 - h);
      if (top < 8) top = 8;
      fsub.style.left = left + 'px';
      fsub.style.top = top + 'px';
      fsub.style.visibility = '';
      fsub.classList.add('giencoder-popup-open');
    };
    var closeFM = function () {
      if (!fm) return;
      closeFSub();
      fm.classList.remove('giencoder-popup-open');
      fm.setAttribute('aria-hidden', 'true');
      fArt = null;
      setTimeout(function () { if (!fm) return; fm.style.display = 'none'; }, 200);
    };
    var openFM = function (art, x, y) {
      if (!fm) {
        fm = buildFMenu(FCTX_ITEMS);
        fm.setAttribute('aria-hidden', 'true');
        fm.addEventListener('click', function (e) {
          var r = e.target && e.target.closest ? e.target.closest('[data-r93-fctx]') : null;
          if (!r) return;
          if (r.getAttribute('data-r93-fctx') === 'openwith') {
            if (fSubRow === r && fsub && fsub.classList.contains('giencoder-popup-open')) closeFSub();
            else openFSub(r);
            return;
          }
          runF(r.getAttribute('data-r93-fctx'));
        });
        /* 悬停切换：移到别的项就收子菜单；指向「打开方式」本身或子菜单则保留 */
        fm.addEventListener('pointerover', function (e) {
          var r = e.target && e.target.closest ? e.target.closest('[data-r93-fctx]') : null;
          if (!r) return;
          if (r.getAttribute('data-r93-fctx') === 'openwith') { openFSub(r); return; }
          if (fSubRow && fSubRow !== r) closeFSub();
        });
      }
      fArt = art;
      fm.style.display = 'flex';
      fm.style.visibility = 'hidden';
      fm.style.left = '0px';
      fm.style.top = '0px';
      var w = fm.offsetWidth, h = fm.offsetHeight;
      var left = Math.min(x, window.innerWidth - w - 8);
      var top = Math.min(y, window.innerHeight - h - 8);
      fm.style.left = Math.max(8, left) + 'px';
      fm.style.top = Math.max(8, top) + 'px';
      fm.style.visibility = '';
      fm.setAttribute('aria-hidden', 'false');
      fm.classList.add('giencoder-popup-open');
    };
    /* 只有「复制路径」有真实副作用（写入剪贴板）；其余项一律**只关菜单、不造提示**
       （本页没有内联 DS Message / avToast，不为它临时造一个）。
       ★ r101 第②批 ⑤：触发器由「产物卡」扩到「改动汇总行」两类 ⇒ 文件名分两个来源取：
         产物卡 = `data-r93-artname`（r101 ⑦ 补的属性）；汇总行 = `data-r93-file`（r99 ⑦ 就有）。 */
    var runF = function (id) {
      var name = fArt ? (fArt.getAttribute('data-r93-artname')
        || fArt.getAttribute('data-r93-file') || '') : '';
      closeFM();
      if (id === 'path' && name) {
        try {
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(name).catch(function () {});
          }
        } catch (err) { /* 忽略 */ }
      }
    };
    /* 触发器①「任务产物卡」右键 · ②「改动汇总行」右键（r99 ⑦ 的入口，菜单换成同一张） */
    host.addEventListener('contextmenu', function (ev) {
      var t = ev.target;
      if (!t || !t.closest) return;
      var trig = t.closest('.r93-artcard, .r93-drow');
      if (!trig) return;
      ev.preventDefault();
      openFM(trig, ev.clientX, ev.clientY);
    });
    /* 触发器③「改动汇总行」**左键**（整行可点，r100 ④ 的行为保留）——
       点右侧那枚「⋯」时菜单贴按钮左下角、点行内其余位置时贴整行左下角
       （都是 DS dropdown「向下弹、左缘对齐触发器」口径；右/下溢出时 `openFM` 自己夹回来）。 */
    host.addEventListener('click', function (ev) {
      var t = ev.target;
      if (!t || !t.closest) return;
      var row = t.closest('.r93-drow');
      if (!row) return;
      var btn = t.closest('.r93-dmore');
      var r = (btn || row).getBoundingClientRect();
      openFM(row, btn ? r.left : r.left + 11, r.bottom + 4);
    });
    document.addEventListener('pointerdown', function (ev) {
      if (!fm || !fm.classList.contains('giencoder-popup-open')) return;
      if (fm.contains(ev.target)) return;
      if (fsub && fsub.contains(ev.target)) return;
      /* 右键在卡片 / 汇总行上重开：交给 contextmenu 分支，别在这里先关 */
      if (ev.button === 2) return;
      /* ★ r101 第②批 ⑤：左键触发器自己（汇总行 / 行内那枚「⋯」）也不关 ——
         否则同一次点击会「先关后开」闪一下（pointerdown 先到、click 后到，
         click 那边还会把菜单重新打开）。 */
      if (ev.target.closest && ev.target.closest('.r93-dmore, .r93-drow')) return;
      closeFM();
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') closeFM();
    });
    window.addEventListener('resize', closeFM);
    window.addEventListener('blur', closeFM);
    document.addEventListener('scroll', closeFM, true);
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
    # ★ r105 ③：文件预览栏的右键菜单段 + 本页控制器（同一个 script 块，控制器在后 ⇒ 注册顺序对）
    return '<script id="%s">\n%s\n\n%s\n</script>\n' % (JS_ID, js.strip(), BROWSE_JS.strip())


def build_css():
    # ★ r105 ③：文件预览栏的样式表（含右键菜单 + 移植时补的暗色档）；
    #   整块进 `r102-conv-css` ⇒ 被 converge() 原样跳过（不被 unscale/scale 派生）
    return '<style id="%s">\n%s\n\n%s\n\n%s\n\n%s\n</style>\n' % (
        CSS_ID, CSS.strip(), BROWSE_CSS.strip(), BROWSE_DARK.strip(), R106_CSS.strip())


# ---------------------------------------------------------------- 主流程

RE_STYLE = re.compile(r'<style id="(?:%s)">.*?</style>\n?' % _N_CSS, re.S)
RE_JS = re.compile(r'<script id="(?:%s)">.*?</script>\n?' % _N_JS, re.S)
RE_NAV = re.compile(r'<!-- (?:%s)-nav -->\n?<script id="(?:%s)">.*?</script>\n?'
                    r'<!-- /(?:%s)-nav -->\n?' % (_N_TAG, _N_NAV, _N_TAG), re.S)


def build_nav_js():
    return ('<!-- %s-nav -->\n<script id="%s">\n%s\n</script>\n<!-- /%s-nav -->\n'
            % (GENS[-1][0], NAV_ID, NAV_JS_TMPL.strip(), GENS[-1][0]))


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


def nav_patch(text):
    """给**独立页**插「点 aside 里的会话任务 → conversation.html」的捕获脚本（幂等：先摘再插）。

    ★ r105 ①：邵先生「在任何其他独立页面点击会话任务都要能跳转到 conversation.html」。
      该脚本 r93 就已写好（`NAV_JS_TMPL`），但当年只注入了 base.html —— 因为只有工作台是入口。
      现在 8 个独立页（dev / kanban / req-kanban / task-detail / avatar / automation / skills / settings）
      各来一份。**conversation.html 自己不插**：它页内已有「滚回顶部」的同款捕获监听
      （内容只有一份，跳自己等于重载），且它本身就是目的地。
    """
    out = invert_if_absent(text, RE_NAV, build_nav_js())
    return out


def nav_unpatch(text):
    out = RE_NAV.sub('', text)
    return out, (0 if out == text else 1)


def inject_tail(text, blob):
    idx = text.rfind('</body>')
    if idx < 0:
        sys.exit('!! 找不到 </body>')
    if len(text) - idx > 120:
        sys.exit('!! 最后一处 </body> 距文件尾 %d 字符（不像收尾标签）' % (len(text) - idx))
    return text[:idx] + blob + text[idx:]


def invert_if_absent(text, rx, blob):
    """幂等三态：块**已存在且内容一致** ⇒ 一字不动（含位置）；内容不同 ⇒ **原地**替换；
    不存在 ⇒ 追加到 `</body>` 前。

    ★ r105 ①：`r101-hdr-css` 与 nav 块**都往文件尾追加**，各自「先摘再插」会把对方的相对顺序
      顶来顶去 ⇒ 页面虽然最终内容稳定，脚本却每遍都报「改了」。这个helper 让「一致就不动」，
      `applyNN.py` 跑第二遍才真的静默（幂等判据也才可信）。
    """
    m = rx.search(text)
    if m:
        if m.group(0).rstrip('\n') == blob.rstrip('\n'):
            return text, 0
        return text[:m.start()] + blob + text[m.end():], 1
    return inject_tail(text, blob), 1


def hdr_patch(text):
    """插入 `r101-hdr-css`（顶栏装饰图 70%）。幂等：见 invert_if_absent。

    只对**带 `r92-hdr-css`** 的页面生效（不带顶栏装饰图的页面一律不动）。
    """
    if 'r92-hdr-css' not in text:
        return text, 0
    return invert_if_absent(text, RE_HDR, HDR_BLOB)


def hdr_unpatch(text):
    out = RE_HDR.sub('', text)
    return out, (0 if out == text else 1)


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

    # ---- 1) base.html：先摘净底（本代两块 + nav 块 + 顶栏图块），净底是两页的唯一来源 ----
    src = io.open(PAGE, encoding='utf-8').read()
    net = src
    for rx in (RE_STYLE, RE_JS, RE_NAV, RE_HDR):
        net = rx.sub('', net)
    if forward:
        for g in GENS:
            for tok in (g[1], g[2], g[3]) + (ATTR_HOST, HDR_ID):
                if tok in net:
                    sys.exit('!! 摘块后基线里仍残留标记 %r' % tok)
        for tok in (GENS[-1][0] + '-nav',):
            if tok in net:
                sys.exit('!! 摘块后基线里仍残留 nav 注释 %r' % tok)

    n_style0, n_end0 = net.count('<style'), net.count('</style>')
    n_scr0, n_es0 = net.count('<script'), net.count('</script>')

    if forward:
        # ---- 2a) ★ r101 第②批 ②：顶栏装饰图 background-size = 70% ----
        #     先落进**净底**（base.html 与 conversation.html 各继承一份），
        #     再把其余 4 个「带 r92-hdr-css」的页面逐个插上（同样是 `</body>` 前、幂等）。
        net, n = hdr_patch(net)
        if n:
            n_style0 += 1
            n_end0 += 1
            if HDR_ID not in src:
                changes.append('base 净底 注入 r101-hdr-css（顶栏图 70%）')
        for path in sorted(glob.glob(os.path.join(REPO, 'pages', '*.html'))):
            base_name = os.path.basename(path)
            if os.path.abspath(path) in (PAGE, PAGE_CONV):
                continue  # base 走 net；conversation 由 net 重建
            t = io.open(path, encoding='utf-8').read()
            t2, n = hdr_patch(t)
            if n:
                if not a.dry:
                    io.open(path, 'w', encoding='utf-8').write(t2)
                changes.append('%s 注入 r101-hdr-css（顶栏图 70%%）' % base_name)

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

        # ---- 2c) ★ r105 ①：其余 8 个独立页也挂上「点会话任务 → conversation.html」的捕获脚本 ----
        #      （base.html 已在 3) 里随净底注入；conversation.html 自己不需要，见 nav_patch 注释。）
        for path in sorted(glob.glob(os.path.join(REPO, 'pages', '*.html'))):
            if os.path.abspath(path) in (PAGE, PAGE_CONV):
                continue
            t = io.open(path, encoding='utf-8').read()
            t2, n = nav_patch(t)
            if n:
                if not a.dry:
                    io.open(path, 'w', encoding='utf-8').write(t2)
                changes.append('%s 注入会话跳转脚本' % os.path.basename(path))

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
        # ★ r105 ③：样式表 + **文件预览栏的静态片段** + 脚本（三件一块注入，与 avatar.html 同体位）
        conv = inject_tail(conv, build_css() + BROWSE_HTML + build_js())
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
            # ★ r101 第②批 ② 的逆操作：摘掉顶栏图块（幂等：摘不到就不报）
            t3, n = hdr_unpatch(t2)
            if n:
                if not a.dry:
                    io.open(path, 'w', encoding='utf-8').write(t3)
                changes.append('%s 摘除 r101-hdr-css' % os.path.basename(path))
            # ★ r105 ① 的逆操作
            t4, n = nav_unpatch(t3)
            if n:
                if not a.dry:
                    io.open(path, 'w', encoding='utf-8').write(t4)
                changes.append('%s 摘除会话跳转脚本' % os.path.basename(path))
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


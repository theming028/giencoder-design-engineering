# -*- coding: utf-8 -*-
"""r88 · 「设置」页两项修订 + 新增「已归档任务」页签内容

邵先生 r88 第 1/2 条（第 3 条「已归档任务」页在本块内一并落地）：
  ① 左侧导航 hover 底色 = **选中态底色**（同一块 #ECEEF2）
  ② 字号滑块 .r85-slider **拖动不顺滑/拖不动** ⇒ 重写为指针事件（pointerdown/move/up）
     + 整块 252×36 命中层（原来只有 1px 高的轨道接 click，几乎点不中）
  ③ 「已归档任务」页签内容按设计稿 1393:18344 精确还原（原先是 .r85-empty 空态占位）

本脚本是 r87 `apply87.py` 的**接续改写版**：CSS/JS 块整体换代（摘 r85 + r86 + r87 + r88 四代标记），
r85 自绘的导航与内容结构、类名（r85-nav-host / r85-page-host 等）保持不变。
⚠️ r85 手搓的 .r85-sel / .r85-menu 已整体移除，select 一律走 DS 标准组件。
⚠️ 落地后**必须再跑一次 `apply88b-fontsize.py`**？不需要 —— 本脚本末尾会自动调用它的
   `converge()`（固定点：只对「非本代块」做 unscale → scale），保证两块脚本的执行顺序不影响结果。

用法：
  python mg-work/r88/apply88.py                 # 应用（幂等：先摘旧块再插）
  python mg-work/r88/apply88.py --dry           # 只报告，不写盘
"""
import argparse
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
# 图标素材沿用 r85 的设计稿导出（导航/系统设置用的那 20 枚，本轮未变）；
# 「已归档任务」页新增的 4 枚（放大镜/文件夹/撤销/垃圾桶）设计稿未给 SVG 导出 ⇒ 按 16×16 手写同风格路径。
RAW = os.path.join(os.path.dirname(HERE), 'r85', 'raw')
PAGE = 'settings.html'

CSS_ID = 'r88-set-css'
JS_ID = 'r88-set-js'
ATTR = 'data-r85-set'   # 结构标记沿用 r85：DOM 类名与挂载点未变，本代只换 CSS/JS 块

# ---------------------------------------------------------------- 图标

ICON_FILES = {
    # 导航
    'arrow':  '1389-18609__svg_09f8c670.svg',   # ← 返回
    'gear':   '1389-18609__svg_d29f72b1.svg',   # 齿轮（系统设置，蓝）
    'cube':   '1389-18609__svg_0bbb2850.svg',   # 立方体（模型）
    'plug':   '1389-18609__svg_cda158bf.svg',   # 插头（连接器）
    'box':    '1389-18609__svg_d583d797.svg',   # 箱+勾（已归档任务）
    # 内容页行图标（20×20）
    'i_preset': '1389-18725__svg_f2347273.svg',
    'i_shield': '1389-18725__svg_8597c800.svg',
    'i_key':    '1389-18725__svg_6c581bda.svg',
    'i_wake':   '1389-18725__svg_6653ad12.svg',
    'i_bell':   '1389-18725__svg_a594e035.svg',
    'i_sound':  '1389-18725__svg_46d0fb4e.svg',
    'i_lang':   '1389-18725__svg_e89f4c09.svg',
    'i_aa':     '1389-18725__svg_55a12f17.svg',
    'i_tee':    '1389-18725__svg_6d318e41.svg',
    'i_update': '1389-18725__svg_feb00c56.svg',
    'i_acct':   '1389-18725__svg_4072e68f.svg',
    # 分段控件（16×16）
    'sun':      '1389-18725__svg_6dd63533.svg',
    'moon':     '1389-18725__svg_e64d56dd.svg',
    'display':  '1389-18725__svg_c702432c.svg',
}

VIEWBOX = {  # 每个图标的 viewBox（从素材抽，避免运行时解析）
}

# ---------------------------------------------------------------- 「已归档任务」新增图标（手写）
# 设计稿 1393:18344 只给了整块 PNG（本地 HTTP getScreenshot 通道），没有逐层 SVG 导出，
# 故按 16×16 viewBox + 1.5px stroke + currentColor 手写，与既有 20 枚导出图标同风格。
# 尺寸由 CSS 控（前缀 16px / 行内元信息 12px / 按钮内 16px）。
ICON_INLINE = {
    # 放大镜（搜索框前缀）
    'i_search': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
                '<circle cx="6.9" cy="6.9" r="4.6" stroke="currentColor" stroke-width="1.5"/>'
                '<path d="M10.4 10.4l2.9 2.9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
                '</svg>',
    # 文件夹（项目筛选下拉的前缀，渲染 16px）—— r90 ③ 重画（邵先生「这个图标也不对」）。
    #   设计稿实测（device 2x，脚本 mg-work/r88/ev/selprefix.py）：
    #     墨迹 26×24 device = **13×12 design px**；左上标签外宽 11 device = 5.5 design、墨迹高 6 device = 3；
    #     中部横线在距图标顶 10 device = 5 design（≈42% 高）。
    #   r88 的旧版是 16 网格的**扁形 + 斜边标签**（`l1.3 1.6` = 斜线），渲染到 16px 时：
    #     ① 整体偏扁（实测墨迹 14×11，设计 13×12）② 标签斜边经抗锯齿后在标签右缘留出亮缝（看起来「糊/断」）。
    #   现在 **1:1 建网格**：viewBox 16 + 渲染 16px ⇒ 1 单位 = 1px；直角台阶用 h/v（不用 l）；
    #   ★ 关键：**所有描边中心线都取 x.5 / y.5** —— 1px 描边才正好盖满「一整列/一整行」像素。
    #     落在整数中心线上会摊成两个 50% 灰像素（肉眼= 又细又虚），这是 r88 旧版「糊」的第二个原因。
    #   墨迹 14×12（设计 13×12，宽多 1px 是为「2 的整数倍才能左右对称对齐像素」让步；
    #   16 盒内左右各留 1.5/1，1x 下不可辨），横线在距图标顶 5px（设计 5，≈42% 高）。
    'i_folder': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
                '<path d="M1.5 2.5h5v2h8v9h-13z" stroke="currentColor" stroke-width="1"/>'
                '<path d="M1.5 7.5h13" stroke="currentColor" stroke-width="1"/>'
                '</svg>',
    # 文件夹（行内元信息，12px 档）—— r89 重画。
    #   r88 直接用 16 网格的 i_folder 缩到 12px（0.75 倍）⇒ ① 墨迹只有 8.6×6.5px（设计稿 10×10，**扁了**）
    #   ② 标签的斜边（l1.3 1.6 = 1.2px）在 0.75 倍下糊成一片 ③ 1.5 单位描边 = 1.125px 落在非整数像素上发虚。
    #   现在换成 **12 网格 1:1**（viewBox 12、渲染 12px ⇒ 1 单位 = 1px），坐标全部落在 x.5（1px 描边正好盖满整数像素区间）：
    #     · 外框 M1.5 1.5 → 5.5 1.5 → 5.5 3.5 → 10.5 3.5 → 10.5 10.5 → 1.5 10.5 → Z（标签是**直角台阶**，与设计稿一致，非斜边）
    #     · 中部横线 y=5.5（设计稿实测在 46% 高）
    #   实测设计稿：墨迹 21×20 device = 10.5×10 design；标签外宽 10 device = 5 design（占 48%）。
    'i_folder12': '<svg viewBox="0 0 12 12" fill="none" aria-hidden="true">'
                  '<path d="M1.5 1.5h4v2h5v7h-9z" stroke="currentColor" stroke-width="1"/>'
                  '<path d="M1.5 5.5h9" stroke="currentColor" stroke-width="1"/>'
                  '</svg>',
    # 撤销 / 恢复（环形左箭头 + 底部左伸的尾巴）
    'i_undo': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
              '<path d="M5.7 4.6L3.2 7l2.5 2.4" stroke="currentColor" stroke-width="1.5" '
              'stroke-linecap="round" stroke-linejoin="round"/>'
              '<path d="M3.5 7h5a3.3 3.3 0 1 1 0 6.6H4.2" stroke="currentColor" stroke-width="1.5" '
              'stroke-linecap="round"/>'
              '</svg>',
    # 垃圾桶
    'i_trash': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
               '<path d="M2.7 4.5h10.6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
               '<path d="M6.2 4.5V3h3.6v1.5" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>'
               '<path d="M4.1 4.5v9.2h7.8V4.5" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>'
               '<path d="M6.6 6.9v4.3M9.4 6.9v4.3" stroke="currentColor" stroke-width="1.5" '
               'stroke-linecap="round"/>'
               '</svg>',
}


def extract_icon(fname):
    """抽出 <svg> 的 viewBox + <path> 列表，剥掉 defs/clipPath（clip 恒等于整块 viewBox，无作用）。

    内联后 id 会重复（master_svg0_*），剥掉 defs 同时消除这个隐患。
    """
    p = os.path.join(RAW, fname)
    src = io.open(p, encoding='utf-8').read()
    vb = re.search(r'viewBox="([^"]+)"', src)
    vb = vb.group(1) if vb else '0 0 16 16'
    paths = re.findall(r'<path\b[^>]*/?>', src)
    body = []
    for pt in paths:
        # 设计稿里的单色图标：剥掉写死的 fill，改用 currentColor 交给 CSS 控色
        pt = re.sub(r'\sfill="#[0-9A-Fa-f]{3,8}"', '', pt)
        pt = re.sub(r'\sfill-opacity="[^"]*"', '', pt)
        pt = re.sub(r'^<path', '<path fill="currentColor"', pt)
        if not pt.endswith('/>'):
            pt = pt[:-1].rstrip() + '/>'
        body.append(pt)
    return '<svg viewBox="%s" fill="none" aria-hidden="true">%s</svg>' % (vb, ''.join(body))


def jsstr(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ') + "'"


def build_icon_js():
    parts = []
    for k in sorted(ICON_FILES):
        parts.append('  %s: %s' % (k, jsstr(extract_icon(ICON_FILES[k]))))
    for k in sorted(ICON_INLINE):
        parts.append('  %s: %s' % (k, jsstr(ICON_INLINE[k])))
    return 'var ICON = {\n' + ',\n'.join(parts) + '\n};'


# ---------------------------------------------------------------- 数据

DATA_JS = """
/* 设计稿文案逐条抄自 MasterGo 1389:18725（截图取证 mg-work/r85/ev/band_full.png） */
var NAV_GROUPS = [
  { title: '通用', items: [
    { id: 'system',    ic: 'gear', t: '系统设置' },
    { id: 'model',     ic: 'cube', t: '模型' },
    { id: 'connector', ic: 'plug', t: '连接器' }
  ]},
  { title: '已归档', items: [
    { id: 'archived',  ic: 'box',  t: '已归档任务' }
  ]}
];

/* 只有「系统设置」有设计稿；其余菜单暂无内容稿 → 给空态占位 */
var CARDS = {
  system: [
    { ic: 'i_preset', t: 'Agent 预设', d: '此前新建的会话生效。运行中的会话保持它开始时的预设。',
      ctl: { k: 'select', w: 98, v: '标准模式', o: ['标准模式', '计划模式', '自动模式'] } },
    { ic: 'i_shield', t: '权限', d: '选择新会话的默认权限模式',
      ctl: { k: 'select', w: 154, v: 'Workspace Write', o: ['Workspace Write', '只读', '完全访问'] } },
    { ic: 'i_key', t: '繁忙时 Enter 键行为', d: '仅在智能体运行时生效；Cmd/Ctrl+Enter 使用另一行为',
      ctl: { k: 'select', w: 98, v: '排队发送', o: ['排队发送', '立即发送', '中断当前'] } }
  ],
  __cards2: [
    { ic: 'i_wake',  t: '保持系统唤醒', d: '防止电脑在 Agent 工作时自动进入睡眠', ctl: { k: 'switch', on: true } },
    { ic: 'i_bell',  t: '桌面通知', d: 'Agent 等待处理或完成任务时，发送系统通知提醒你', ctl: { k: 'switch', on: false } },
    { ic: 'i_sound', t: '声音通知', d: 'Agent 等待处理或完成任务时播放不同的提示音', ctl: { k: 'switch', on: true } },
    { ic: 'i_lang',  t: '语言', d: '设置你的界面显示语言',
      ctl: { k: 'select', w: 70, v: '中文', o: ['中文', 'English', '日本語'] } },
    { ic: 'i_aa',    t: '字号', d: '设置你的界面文字大小', ctl: { k: 'slider' } },
    { ic: 'i_tee',   t: '外观', d: '设置你的界面外观风格', ctl: { k: 'seg' } }
  ],
  __cards3: [
    { ic: 'i_update', t: '版本更新', d: '当前版本 Ver.0.2.0-2', ctl: { k: 'update' } },
    { ic: 'i_acct',   t: '账号', d: '设置你的界面显示语言', ctl: { k: 'logout' } }
  ]
};
var CARDS_ALL = [CARDS.system, CARDS.__cards2, CARDS.__cards3];

/* ---- r88 ③「已归档任务」（设计稿 1393:18344）：文案/项目/时间逐条抄录，顺序即设计稿顺序 ---- */
var ARCH_ROWS = [
  { t: '每日AI简报',                 proj: '银行演练指挥系统', time: '刚刚' },
  { t: '任务创建方式改写',            proj: '银行演练指挥系统', time: '半小时前' },
  { t: '2019款iMac内存升级',         proj: '旅行助手',        time: '昨天 10:25' },
  { t: '自动批准API请求改写建议',      proj: '旅行助手',        time: '07/11 19:21' },
  { t: '三城周末性价比对比',          proj: '旅行助手',        time: '07/11 19:21' },
  { t: '自动任务手动触发对话创建',     proj: '我的坚果云',      time: '07/11 19:21' },
  { t: 'Git Worktree多分支并行开发',  proj: '旅行助手',        time: '07/11 19:21' }
];
var ARCH_FILTER_ALL = '全部项目';
var ARCH_SUB = '归档即存档，完整保留历史数据，支持随时查阅与恢复。';
"""

# ---------------------------------------------------------------- CSS

CSS = """
/* ★ 第 85 轮 · 「设置」页按设计稿重做（MasterGo 1389:18609 导航 + 1389:18725 系统设置内容）
   r86 四条修订（aside 定宽 / 分割线加深 / 换 DS select / 图标底加深）
   r87 三条修订（全局字号滑块 / 按钮全换 DS Button / 导航选中态文字变蓝加粗）
   规则：色值一律走 token；设计稿里没有对应 token 的色用最接近的语义 token 顶替（见注释）。
   ⚠️ 本块由 mg-work/r87/apply87.py 生成，勿手改。 */

/* ---------- 布局容器 ---------- */
/* 外壳原内容（React 渲染的既定导航与设置页）隐藏，由本块自绘节点接管 */
body[data-r85-set] [data-set-original],
body[data-r85-set] [data-set-hidden] { display: none !important; }
/* r90 ①：邵先生「设置页 aside 的左右内距要与基础工作台一致」。
   基础工作台（pages/base.html）实测：aside 256 宽且自身 padding=0，右内距由子滚动容器的
   尾风类 `pr-3` 提供 ⇒ 内容盒 = 256 − 12 = 244，会话项 relL 0 / relR 12（宽 244）。
   本页原来是「host 232 + margin:0 auto」，在 244 内容盒里居中 ⇒ relL 6 / relR 18（左右各偏 6）。
   现改为撑满内容盒：relL 0 / relR 12，与基础工作台逐像素对齐。 */
body[data-r85-set] .r85-nav-host { width: auto; margin: 0; }
body[data-r85-set] .r85-page-host { width: 860px; margin: 12px auto 0; padding: 0 10px; box-sizing: border-box; }

/* ---------- ① aside 定宽 + 禁拖拽（邵先生 r86） ----------
   外壳的 aside 宽由 React state 写成内联 style.width，右缘挂着一条 role=separator 的
   拖拽把手（实测 6px、紧贴 aside 右缘）。!important 能压住内联 style ⇒「拖了也不动」。
   收起态：外壳 JSX 写作 aria-hidden={!asideOpen} ⇒ 用 aria-hidden='true' 放行 0 宽。
   ⚠️ 不要用 :not([aria-hidden='true']) 之外的花招，也不要给 aside 设 min-width。 */
body[data-r85-set] aside { width: 256px !important; }
body[data-r85-set] aside[aria-hidden='true'] { width: 0 !important; }
body[data-r85-set] [role='separator'][aria-label='调整菜单宽度'] { display: none !important; }

/* ---------- 左侧导航 ---------- */
/* r90 ①：宽随宿主（内容盒 244），与基础工作台的会话列同宽 */
.r85-nav { display: flex; flex-direction: column; width: 100%; }
/* r92 ②：返回钮的图标与文字统一「深一级」。原来写的是字面 #6B6B6B —— 那是 DS 的
   gray-7（= --color-neutral-7 / 一级灰阶），比本页正文的 text-2(gray-8) 还浅一档。
   改取 var(--color-text-2)（#4E4E4E）。图标是 <svg fill="currentColor">、文案是
   <span> 自然继承 ⇒ 只改按钮这一处 color 即图标与文字同变，无需另写选择器。
   顺带消掉本页最后一处字面 hex（硬规则：页面内禁硬编码色值）。 */
.r85-back {
  display: flex; align-items: center; gap: 6px; width: 100%; height: 32px;
  padding: 5px 10px; box-sizing: border-box; border: 0; border-radius: 4px;
  background: none; cursor: pointer; color: var(--color-text-2);
  font-family: var(--font-family); font-size: var(--font-size-body-3); line-height: 22px; text-align: left;
  transition: background-color .12s ease;
}
/* r91 ①：返回钮的 hover 底 = 下方菜单项的 hover 底。原来写的是 --color-fill-2(#F2F2F2)，
   与本页导航 hover 的 --r88-navi-active(#ECEEF2) 不是一个色 ⇒ 两者刻意共用同一个变量，
   以后改一处即两处同步（含暗色档）。 */
.r85-back:hover { background: var(--r88-navi-active); }
.r85-back > svg { flex: none; width: 14px; height: 14px; }

.r85-group { display: flex; flex-direction: column; margin-top: 20px; }
/* r92 ③：组标题左间距 12px —— 与下方 .r85-navi 的**文字起始位**对齐
   （菜单项 padding 0 12px ⇒ 文字从 12px 起）。原为 margin: 0 2px 8px（左右各 2px），
   组标题比菜单文字左出 10px。只改左值，其余三个方向不动。 */
.r85-gt {
  margin: 0 2px 8px 12px; color: var(--color-text-3);
  font-family: var(--font-family); font-size: var(--font-size-body-1); line-height: 16px;
}
.r85-navi {
  display: flex; align-items: center; gap: 8px; width: 100%; height: 36px; padding: 0 12px;
  box-sizing: border-box; border: 0; border-radius: 8px; cursor: pointer;
  /* r91 ②：默认**不给背景色**（原为 --color-fill-1(#F7F7F7)，会让每个菜单项看着像"常亮按钮"）。
     hover / 选中仍各自有底，由下方两条高特异性规则给（:hover 与 [aria-current='true'] 的特异性
     都高于本基类 ⇒ 不会被这里的 background:none 盖掉）。 */
  background: none; color: var(--color-text-1);
  font-family: var(--font-family); font-size: var(--font-size-body-3); line-height: 22px; text-align: left;
  transition: background-color .12s ease;
}
.r85-navi + .r85-navi { margin-top: 2px; }
.r85-navi > svg { flex: none; width: 16px; height: 16px; color: var(--color-text-1); }
/* r88 ①：邵先生「hover 背景色要和选中态一致」⇒ hover 与选中同底；
   选中态只靠「图标+文字变主题蓝 + 加粗」区分，底色不再区分。

   ⚠️ 这个底色 #ECEEF2 是设计稿实测值，**DS 色板里没有这一档**（灰阶只有 247/242/229/201/…，
      蓝阶也不含）⇒ 按硬规则走「本页适配层变量」：字面 hex 只在这里出现一次，
      并在 [giencoder-theme=dark] 里补回；页面其它地方一律引用 var()。 */
:root { --r88-navi-active: #ECEEF2; }
:root[giencoder-theme=dark], [giencoder-theme=dark] { --r88-navi-active: #2E323A; }
.r85-navi:hover { background: var(--r88-navi-active); }
.r85-navi[aria-current='true'] { background: var(--r88-navi-active); }
.r85-navi[aria-current='true'] > svg { color: var(--color-primary-6); }
.r85-navi[aria-current='true'] > span { color: var(--color-primary-6); font-weight: 500; }

/* 本页「卡片」共用同一档圆角。r89：邵先生要求「已归档任务」列表卡的圆角与 .r85-card 一致（复用/共用），
   故把 .r85-card 原有的 8px 提成变量，.r85-card / .r88-arch-list / 空态三处一起引用；
   改档位只动这一行。 */
:root { --r88-card-radius: 8px; }

/* ---------- 内容区 ---------- */
.r85-page { display: flex; flex-direction: column; }
.r85-title {
  margin: 0; color: var(--color-text-1); font-weight: 500;
  font-family: var(--font-family); font-size: var(--font-size-title-2); line-height: 28px;
}
/* 卡片：底用 --color-fill-1（设计稿 #F8F9FA，差 1~3 阶肉眼不可辨，规避硬编码）；
   描边用 --color-border-1（设计稿 #EEEEEE）。
   ⚠ 设计稿是「内描边」（描边不吃内容盒：行宽 800 = 840 − 2×20）⇒ 必须用 outline + 负 offset，
   不能写 border —— 写 border 会让行宽 800→798、卡片高多 2px，并把整列 y 推低 2~3px。 */
.r85-card {
  margin-top: 16px; padding: 20px; box-sizing: border-box;
  background: var(--color-fill-1); border-radius: var(--r88-card-radius);
  outline: 1px solid var(--color-border-1); outline-offset: -1px;
}
.r85-card:first-of-type { margin-top: 24px; }
/* 设计稿实测：中间那张卡（6 行）底内距是 16（首/末张是 20），框高因此为 448 而非内容所需的 452。
   照设计稿落地后，卡片3 起点 762（设计 763）、页高 918（设计 919），均在 ±1 内。 */
.r85-card.is-mid { padding-bottom: 16px; }

.r85-row { position: relative; display: flex; align-items: center; min-height: 42px; }
.r85-row + .r85-row { margin-top: 32px; }
/* 分割线画在两行之间的空隙正中（设计稿：行底 +16），不占布局高度
   r86 ②：邵先生反馈「浅了」⇒ 加深一级（--color-fill-2 gray-2#F2F2F2 → --color-border-2 gray-3#E5E5E5） */
.r85-row + .r85-row::before {
  content: ''; position: absolute; left: 0; right: 0; top: -16px; height: 1px;
  background: var(--color-border-2);
}
/* r86 ④：行图标底同样加深一级（同 --color-fill-3 = gray-3 #E5E5E5） */
.r85-ic {
  flex: none; display: flex; align-items: center; justify-content: center;
  width: 40px; height: 40px; border-radius: 8px; background: var(--color-fill-3); color: #6B6B6B;
}
.r85-ic > svg { width: 20px; height: 20px; }
.r85-tx { flex: 1; min-width: 0; margin-left: 12px; display: flex; flex-direction: column; justify-content: center; }
/* 设计稿像素实测：末张卡片（版本更新/账号）两行的文字左缘在行内 56，其余卡片是 52（墨迹 77 vs 73） */
.r85-card.is-tail .r85-tx { margin-left: 16px; }
.r85-t {
  color: var(--color-text-1);
  font-family: var(--font-family); font-size: var(--font-size-body-3); line-height: 22px;
}
.r85-d {
  color: var(--color-text-3);
  font-family: var(--font-family); font-size: var(--font-size-body-1); line-height: 16px;
}
.r85-ctl { flex: none; margin-left: 12px; display: flex; align-items: center; gap: 8px; }
/* 设计稿实测：卡片3 首行「自动更新 → 更新日志」间距 12，两按钮之间是 8（差值 4 由复选框补，
   控件组总宽 76+12+104+8+104 = 304，右缘正好贴行右缘 820） */
.r85-ctl > .r85-cb { margin-right: 4px; }

/* ---------- ③ 选择器：DS 标准 select 组件（r86）+ r87 宽度自适应 ----------
   组件本体一个字不改（.giencoder-select* 的定义随页面内联，即 components.css「=== Select 选择器 ===」）。
   本页适配层只剩两件事：
   · flex: none —— .r85-ctl 是 flex 容器，不锁死会被压缩；
   · 给 option 补 :focus 视觉 —— 组件本体只有 :hover，键盘上下键移动时会看不见高亮。
   ⚠️ r87 起 select 的宽度是**自适应**的（DS 侧 width 已由 100% 改为 auto，JS 侧不再写死 px），
      r86 为了塞进设计稿的固定 98px 而加的 `padding-right: 8px` 已撤销 —— 不再有「文字被挤出省略号」的问题。 */
body[data-r85-set] .r85-ctl > .giencoder-select { flex: none; }
body[data-r85-set] .giencoder-select-popup .giencoder-select-option:focus {
  background: var(--color-fill-2); outline: none;
}

/* ---------- 开关（DS switch 类 + 本页适配层：设计稿 40×24，DS 默认 44×22） ---------- */
.r85-sw.giencoder-switch { width: 40px; height: 24px; border-radius: 12px; background: #6B6B6B; }
.r85-sw.giencoder-switch.giencoder-switch-checked { background: var(--color-success); }
.r85-sw .giencoder-switch-handle { width: 20px; height: 20px; top: 2px; left: 2px; }
.r85-sw.giencoder-switch-checked .giencoder-switch-handle { left: 18px; }

/* ---------- 字号滑块（设计稿 252×36）
   设计稿像素实测：轨道 rel x6 长 240；6 段刻度在 rel 6/54/102/150/198/246（每 48 一格，
   第 2 格的刻度被拇指盖住）；已选段 rel 6 → 当前档；拇指 4×12 rel y0；刻度 1×8 rel y2（比轨道顶 4px）。
   ⚠ 刻度挂 .r85-slider（不是 .r85-sl-track）——挂 track 会叠加 track 的 top:6，整条刻度下移 6px。
   ★ r88 ②：邵先生反馈「拖动和点击不够顺滑、存在拖不动」——
      根因：轨道本身只有 **1px 高**，而事件只挂在轨道上 ⇒ 可点区仅 1px，且完全没有拖拽实现。
      改法：命中层 = **整个 252×36 的 .r85-slider**（事件挂它），装饰子元素全部 pointer-events:none；
      交互改为 pointerdown/move/up + setPointerCapture（拖出滑块也不丢），touch-action:none 防滚动抢事件。 */
.r85-slider {
  position: relative; width: 252px; height: 36px;
  cursor: pointer; touch-action: none; -webkit-user-select: none; user-select: none;
}
.r85-slider > * { pointer-events: none; }
.r85-slider:focus-visible { outline: 2px solid var(--color-primary-6); outline-offset: 2px; border-radius: 4px; }
.r85-sl-track {
  position: absolute; left: 6px; top: 6px; width: 240px; height: 1px;
  background: var(--color-border-3);
}
.r85-sl-done { position: absolute; top: 6px; height: 1px; background: var(--color-text-1); }
.r85-sl-tick {
  position: absolute; top: 2px; width: 1px; height: 8px; background: var(--color-border-3);
}
.r85-sl-tick.is-on { background: var(--color-text-1); }
/* 拇指保持设计稿的 4×12（r88 只改交互，不改设计稿几何）；拖动中加一圈主题色外晕做「正在拖」的反馈 */
.r85-sl-thumb {
  position: absolute; top: 0; width: 4px; height: 12px; margin-left: -2px;
  border-radius: 8px; background: var(--color-text-1);
}
.r85-slider.is-drag .r85-sl-thumb { box-shadow: 0 0 0 3px var(--color-primary-light-2); }
.r85-sl-lbls { position: absolute; left: 6px; right: 6px; top: 20px; height: 16px; }
.r85-sl-lbls > span {
  position: absolute; top: 0; color: var(--color-text-3);
  font-family: var(--font-family); font-size: var(--font-size-body-1); line-height: 16px;
  transform: translateX(-50%);
}

/* ---------- 外观分段控件：改用 DS Button 组件（邵先生 r87 ③） ----------
   取 `giencoder-btn-secondary` + `giencoder-btn-size-large`
   —— DS 里「中性描边按钮」的正解；DS 的 `-dashed` 是 primary 蓝虚线的「添加」语义，
      与设计稿的「灰虚线选中框」不是同一类。
   表面层 / 悬停 / 按压内缩 / focus-ring / 尺寸档全部由 DS 组件提供，本页适配层只补：
   · 尺寸 128×40（设计稿）与图标间距 6；
   · 选中态 = 2px 虚线（--color-border-3，#C4C7C9 设计稿实测）—— DS 无此态，属本页适配。 */
body[data-r85-set] .r85-seg { display: flex; align-items: center; gap: 8px; }
body[data-r85-set] .r85-seg > .giencoder-btn { width: 128px; gap: 6px; }
body[data-r85-set] .r85-seg > .giencoder-btn > svg { flex: none; width: 16px; height: 16px; }
body[data-r85-set] .r85-seg > .giencoder-btn[aria-pressed='true'] { border: 2px dashed var(--color-border-3); }

/* ---------- 普通按钮（更新日志 / 检查更新 / 退出登录）：改用 DS Button 组件（邵先生 r87 ③） ----------
   更新日志 / 检查更新 → `giencoder-btn-secondary`；退出登录 → 同档 + 适配层红字
   （DS 没有「带边框 + 危险色文字」的组合：`-danger` 是实心红底、`-danger-text` 是纯文字按钮）。
   适配层只补两件事：等宽 104（设计稿三按钮等宽口径）+ danger 文字色。 */
body[data-r85-set] .r85-btn { min-width: 104px; }
body[data-r85-set] .r85-btn.is-danger { color: var(--color-danger); }

/* ---------- 复选框（自动更新） ---------- */
.r85-cb { display: inline-flex; align-items: center; gap: 6px; cursor: pointer; user-select: none; }
.r85-cb > .giencoder-checkbox-mask { border-width: 1.5px; }
.r85-cb > span:last-child {
  color: var(--color-text-1); font-family: var(--font-family);
  font-size: var(--font-size-body-3); line-height: 22px; white-space: nowrap;
}

/* ---------- 空态（其余菜单暂无设计稿） ---------- */
.r85-empty {
  margin-top: 24px; padding: 48px 0; text-align: center; color: var(--color-text-3);
  background: var(--color-fill-1); border: 1px solid var(--color-border-1); border-radius: 8px;
  font-family: var(--font-family); font-size: var(--font-size-body-3);
}
.r85-toast {
  position: fixed; left: 50%; bottom: 48px; transform: translateX(-50%); z-index: 1300;
  padding: 8px 16px; border-radius: 8px; background: var(--color-tooltip-bg);
  color: var(--color-white); box-shadow: var(--shadow2-down);
  font-family: var(--font-family); font-size: var(--font-size-body-1); line-height: 16px;
  opacity: 0; transition: opacity .16s ease;
}
.r85-toast.is-on { opacity: 1; }

/* ================================================================
   r88 ③ · 「已归档任务」页签内容（设计稿 MasterGo 1393:18344，容器 2× 导出）

   ★ 量测口径：PNG 1680×1316 device px，**scale = 2.0**（不是 2.011）。校验四连：
     · 画板尺寸 1680 = 840×2、1316 = 658×2（整数，直接定死 2.0）
     · 搜索框/下拉高 64 device = 32 design（DS 控件标准档）；行尾钮高 64 device = 32 design
     · 内容区宽 1680 device = 840 design —— 与「设置」页内容盒宽 840 **完全一致**
     · 行分隔线间距恒 148 device = 74 design；卡片顶 264 → 首线 418，正好 = 4 + 74
   设计稿实测关键坐标（design px，原点 = 内容区左上；扫描脚本 mg-work/r88/ev/）：
     标题 16px/28 + 副标题 12px/20 ⇒ 头部文本块 0..48；
       「清空归档任务」108×36，**底缘与文本块底对齐**（y 12..48）⇒ flex-end，右缘贴 840
     工具条 y 80..112：搜索框 x 0..632（32 高）· 间隙 8 · 项目下拉 x 640..840（200×32）
     列表卡 y 132..658 = padding 4px 0 + 7 行 ×74；行分隔线 1px、inset 20/20，落在 210/284/…/580
     行内：padding 15px 20px；标题 14px/22（text-1）；元信息 12px/18（neutral-7，margin-top 4）
           [文件夹图标] 4 [项目名] 8 [· 4×4] 8 [归档于] 6 [时间]
     行尾按钮：默认 28×28 图标钮（白底 + 描边 + r6）；**行 hover 时整组展开为 52×32 纯文字钮**
           （设计稿第 3 行画的就是 hover 态：两个钮一起变宽、右缘仍贴 820 ⇒ 整体向左长）
           52 = 1(边) + 11(内距) + 14px×2 文字 + 11 + 1；墨迹左缘距钮外缘 13 = 1+11+1（字形留白）
           28×28 + 8 间隙 + 20 右缩进：820−28−8−28 = 756 ⇒ device 1512/1584/1640，与实测 1511/1583/1640 吻合
           ⇒ r90 ②：几何口径不变，但实现改为 **DS Button 组件**（见下）

   ⚠️ 描边是「内描边」⇒ 必须用 outline + 负 offset，不能写 border（写 border 会让行内容盒变窄 2px）。
      这跟「设置」页 .r85-card 同一处理（那里已踩过：border 会把整列 y 推低 2~3px）。
   ⚠️ 色值全部落 DS token（**没有新增字面 hex**）：
       · 卡底设计稿 #F8F9FA、卡描边 #EEEEEE ⇒ 沿用 r85 已定的 `--color-fill-1` / `--color-border-1`
         （与「设置」页卡片同一档，两页观感一致；设计稿这两个值都不在 DS 灰阶里）
       · 分隔线 #F2F2F2 = `--color-border-1`（= gray-2，**精确命中**）
       · 搜索框描边 #E5E5E5 = `--color-border-2`（= gray-3，DS Input 默认档，精确命中）
       · 行标题 / hover 钮文字 #1F1F1F = `--color-text-1`（gray-10，精确命中）
       · 页副标题 #868686 = `--color-text-3`（gray-6，精确命中）
       · 行元信息 / 各图标 #6B6B6B —— DS 无此档文字 token（text-2=gray-8、text-3=gray-6）
         ⇒ 用 `--color-neutral-7`（= gray-7，**精确命中**，且暗色主题会自动翻转）
       · 「清空归档任务」#FFECE8 底 / #F53F3F 字 ⇒ `--color-danger-light-1` / `--color-danger-6`
         （分别 = red-1 / red-6，与设计稿**逐通道相等**）
   ⚠️ 圆角（r90 ② 后分两路）：
       · **按钮一律走 DS**（`border-radius-medium` = 4px）—— 邵先生「按钮必须用设计系统组件」是
         全局强制要求，圆角属组件身份 ⇒ 不再用适配层压成设计稿实测的 6px。
       · 容器类（搜索框 / 下拉 / 列表卡 / 空态）仍按设计稿实测：搜索框顶边曲线拟合 r = 14 device = 7 design
         （8 个深度残差 ≤0.5px），卡片面积法 13.5 device。实测落在 6~7px，DS 无 7px 档
         （medium=4 / large=8）⇒ 容器侧统一取 **6px**；列表卡与空态按 r89 指令共用 `--r88-card-radius`(8px)。
       ⚠️ 遗留待拍板：「设置」页卡片/下拉是 8px（r85/r87 定），本页设计稿实测偏 6~7px ⇒ 是否统一到 8px 由邵先生定。
   ⚠️ 字号一律走 token ⇒ 自动跟随 r87 的 `--ui-fs` 全局字号机制；
      尺寸/行高**不用 calc(--ui-fs-ratio) 手写**（会被 apply88b 的 unscale 还原，属 r87 挖过的坑），
      需要跟着长高的地方靠「行高派生 + 高度 auto」自然实现（行尾钮 hover 态即此法）。 */
.r88-arch { display: flex; flex-direction: column; }

/* ---- 头部：标题 / 副标题 / 清空按钮 ---- */
.r88-arch-head {
  display: flex; align-items: flex-start; justify-content: space-between;
  margin-bottom: 32px;
}
.r88-arch-ht { display: flex; flex-direction: column; min-width: 0; }
/* r89：邵先生要求标题与「系统设置」页的 .r85-title **字号一致** ⇒ 也用 title-2(20px)；
   行高两处本来就同为 28px，故头部块高恒 48（28 + 副标题 20）不变。
   （原 r88 按设计稿实测取 title-1(16px)，已按用户口径改回与 .r85-title 同档。） */
.r88-arch-title {
  margin: 0; color: var(--color-text-1); font-family: var(--font-family); font-weight: 500;
  font-size: var(--font-size-title-2); line-height: 28px;
}
.r88-arch-sub {
  margin: 0; color: var(--color-text-3); font-family: var(--font-family);
  font-size: var(--font-size-body-1); line-height: 20px;
}
/* 「清空归档任务」= DS Button 组件（邵先生 r90 ②「全局强制性要求」）
   类名 `giencoder-btn giencoder-btn-size-large`：高度 36 / 字号 body-3 / 内距 / 圆角 / 表面层动效
   全部由 DS 提供（这样也自动吃到 apply88b 的字号高度跟随）。
   ⚠️ 适配层**只补 DS 没有的那一层语义色**（浅底危险：设计稿 #FFECE8 底 / #F53F3F 字）——
      DS 无「浅底 + 危险字」的变体（`-danger` 是实心红底、`-danger-text` 是纯文字）。
      · 圆角：**不写** —— r73 的全局块已定「`.giencoder-btn:not(.giencoder-btn-size-small)` 圆角提到 8px」
        ⇒ 本钮（size-large 档）自动 = 8px，与设置页其它 DS 按钮一致。
      · 内距压到 11（设计稿总宽 108 = 11 + 1(DS 边框) + 14px×6 + 1 + 11；DS `-size-large` 默认 20）。 */
body[data-r85-set] .r88-arch-clear {
  flex: none; align-self: flex-end; padding: 0 11px;
  background: var(--color-danger-light-1); color: var(--color-danger-6);
}
body[data-r85-set] .r88-arch-clear:hover { background: var(--color-danger-light-2); }
body[data-r85-set] .r88-arch-clear:active { background: var(--color-danger-light-2); }

/* ---- 工具条：搜索框 + 项目筛选 ---- */
.r88-arch-bar { display: flex; align-items: center; gap: 8px; margin-bottom: 20px; }
/* 搜索框复用 DS Input（.giencoder-input-wrapper + .giencoder-input），只补圆角 6px 与左内距 8px
   （设计稿：放大镜墨迹左缘 11 ⇒ 16px 图标盒左缘 ≈ 8.5，减 1px 描边 = 7.5 ≈ 8；DS 默认 12）。
   图标 → 占位文字 8px 由 DS 的 .giencoder-input-prefix margin-right 提供，色用 DS 默认 text-3 ✓ */
body[data-r85-set] .r88-arch-search { flex: 1; min-width: 0; border-radius: 6px; padding: 0 12px 0 8px; }
.r88-arch-search .giencoder-input-prefix svg { width: 16px; height: 16px; }
/* 项目下拉：宽 200 定死（设计稿 400 device）；DS 的 select 圆角 r87 定的是 8px（border-radius-large），
   本页设计稿与搜索框同档 ⇒ 本页适配层压到 6px。
   ⚠️ 内距按设计稿实测调（DS 默认 0 12px）：
      · 左 10px ⇒ 前缀图标墨迹落在 x=653（与设计稿 653..664 **逐像素一致**）
      · 右 8px  ⇒ 右侧 chevron 墨迹落在 x≈821（设计稿 820..828；DS 默认 12px 会左偏 3px）
   ⚠️ DS 的 .giencoder-select-view 自带 gap:8px，会把我加的前缀槽与文字再撑开 8px；
      设计稿「图标盒右缘 → 文字 em」只留 6px ⇒ 用 margin-right:-2px 抵消（不改 DS 本体）。 */
body[data-r85-set] .r88-arch-proj { flex: none; width: 200px; }
body[data-r85-set] .r88-arch-proj .giencoder-select-view { padding: 0 8px 0 10px; border-radius: 6px; }
.r88-arch-proj .r88-sel-prefix {
  display: inline-flex; align-items: center; flex: none; margin-right: -2px;
  color: var(--color-neutral-7);
}
.r88-arch-proj .r88-sel-prefix > svg { width: 16px; height: 16px; }

/* ---- 列表卡 ---- */
/* 内描边：行分隔线 inset 20 ⇒ 内描边不吃内容盒，行宽恒 800（外层 840 − 2×20）
   r89：圆角与 .r85-card 共用 --r88-card-radius（原 6px）；分隔线按邵先生要求「深一级」
   ⇒ --color-border-1(gray-2 #F2F2F2) → --color-border-2(gray-3 #E5E5E5)，与 r86 ②「设置页行分隔线加深」同一处理。 */
.r88-arch-list {
  padding: 4px 0; background: var(--color-fill-1); border-radius: var(--r88-card-radius);
  outline: 1px solid var(--color-border-1); outline-offset: -1px;
}
/* 行高恒 74 = 15 + (22 + 4 + 18) + 15；分隔线绝对定位不占布局高 */
.r88-arch-row {
  position: relative; display: flex; align-items: center;
  padding: 15px 20px; box-sizing: border-box;
}
.r88-arch-row + .r88-arch-row::before {
  content: ''; position: absolute; left: 20px; right: 20px; top: 0; height: 1px;
  background: var(--color-border-2);
}
/* 设计稿 row1 的文字块整体右移 12px（其余 6 行都是 20px 左内距）；列扫描确认那 12px 里
   **没有任何元素**（该列最低亮度 = 底色 #F8F9FA）⇒ 判定设计稿笔误，本页统一 20px。 */
.r88-arch-main { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.r88-arch-t {
  color: var(--color-text-1); font-family: var(--font-family);
  font-size: var(--font-size-body-3); line-height: 22px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.r88-arch-m {
  display: flex; align-items: center; margin-top: 4px; color: var(--color-neutral-7);
  font-family: var(--font-family); font-size: var(--font-size-body-1); line-height: 18px;
  white-space: nowrap; overflow: hidden;
}
.r88-arch-mic { display: inline-flex; align-items: center; flex: none; margin-right: 4px; }
.r88-arch-mic > svg { width: 12px; height: 12px; }
/* 项目名可截断（长名优先让位给时间），其余分段不压缩 */
.r88-arch-mproj { overflow: hidden; text-overflow: ellipsis; }
.r88-arch-mu { flex: none; }
.r88-arch-dot {
  flex: none; width: 4px; height: 4px; margin: 0 8px; border-radius: 50%; background: currentColor;
}
.r88-arch-time { margin-left: 6px; flex: none; }
.r88-arch-row.is-hide { display: none; }

/* ---- 行尾操作按钮：DS Button 组件（邵先生 r90 ②「全局强制性要求」） ----
   类名 `giencoder-btn giencoder-btn-secondary giencoder-btn-icon giencoder-btn-size-small`
   —— DS 里「中性描边图标钮」的正解：高 28 / 白底 + border-2 描边 / text-1 字色 / 圆角 / 表面层
   FF 动效（`--btn-ring` 外扩补齐 + 按压内缩）全部由 DS 提供。
   ⚠️ 两处**按 DS 口径而非设计稿**（邵先生 r90 ②「用组件」是全局强制要求）：
      · 圆角：设计稿实测 ~6px，本钮走 DS `-size-small` ⇒ 4px（r73 的全局块把非 small 档提到 8px，
        small 档保持 DS 原值；即「large 8 / small 4」是全站既有口径）。
      · 图标色：DS `-secondary` 的 `color` 是 text-1(#1F1F1F)。按钮**文字**随它是设计稿值
        （设计稿 hover 态文字实测 #1F1F1F ✓，故不覆盖按钮 color）；
        但**图标**按邵先生 r91 ③「默认图标颜色有点深，浅一级」⇒ 只给 `> svg` 覆盖 text-2(#4E4E4E)。
        ⚠️ 设计稿图标逐像素实测 #6B6B6B(= neutral-7)，比 text-2 再浅一档；若要精确贴稿改这一行即可。
      描边同理走 DS 的 border-2(#E5E5E5)，不再用设计稿的 border-1(#F2F2F2)。
   适配层**只补两件几何事 + 一件颜色事**（不改组件本体）：
     ① 默认态压成 28×28 正方形 —— DS 靠 padding 撑宽（-size-small 是 0 12px），图标钮要方；
     ② 行 hover / focus-within ⇒ 两个钮一起展开为 52×32 纯文字钮（图标隐去、右缘不动、整组向左长）；
     ③ 图标色 text-1 ⇒ text-2（**只落在 `> svg` 上**，所以展开态的文字仍是 text-1，与设计稿一致）。
   ⚠️ 展开态高度**只写 min-height 不写 height**：DS 的 `-size-small` 给了 `height:28px`，
      而 CSS 里 min-height 本就优先于 height ⇒ 默认 28、展开 32，两全；
      且 apply88b 能把这条 min-height 派生成 calc(32px * ratio)（大字号档文字不撑爆）。
      为让派生规则（`body …`，特异性 0,3,1）压得住本规则，这里**刻意用不带 body 前缀的低特异性写法**。
   ⚠️ transition 重写：DS 的 4 项动效参数原样保留，仅追加 width/padding 让展开有过渡
      （DS 契约里没有几何过渡，属本页适配层追加）。 */
.r88-arch-acts { flex: none; display: flex; align-items: center; gap: 8px; }
body[data-r85-set] .r88-arch-act {
  width: 28px; padding: 0;
  transition: box-shadow 180ms cubic-bezier(0.23, 1, 0.32, 1),
              background-color 80ms ease, border-color 80ms ease, color 80ms ease,
              width .12s ease, padding .12s ease;
}
/* r91 ③：图标比按钮文字浅一级（text-1 → text-2）。
   刻意只落在 svg 上：展开态 svg 被 display:none、文字 span 继承按钮的 text-1 ⇒ 互不干扰。 */
.r88-arch-act > svg { flex: none; width: 16px; height: 16px; color: var(--color-text-2); }
.r88-arch-act > span { display: none; white-space: nowrap; }
.r88-arch-row:hover .r88-arch-act,
.r88-arch-row:focus-within .r88-arch-act { width: auto; min-height: 32px; padding: 0 11px; }
.r88-arch-row:hover .r88-arch-act > svg,
.r88-arch-row:focus-within .r88-arch-act > svg { display: none; }
.r88-arch-row:hover .r88-arch-act > span,
.r88-arch-row:focus-within .r88-arch-act > span { display: inline; }
/* 删除钮 hover 转危险色：DS 无「描边 + 危险字」组合（-danger 是实心红底）⇒ 本页适配 */
.r88-arch-act[data-act='delete']:hover { color: var(--color-danger-6); }

/* 清空/筛空后的空态：与列表卡同款（设计稿没画空态，沿用 .r85-empty 的做法：padding 撑高、不写 height
   —— 写 height 会被 apply88b 的 scale_block 派生成 calc，空态框会随字号一起长，属布局盒不该跟随） */
.r88-arch-empty {
  display: flex; align-items: center; justify-content: center; padding: 48px 0;
  background: var(--color-fill-1); border-radius: var(--r88-card-radius);
  outline: 1px solid var(--color-border-1); outline-offset: -1px;
  color: var(--color-text-3); font-family: var(--font-family);
  font-size: var(--font-size-body-3); line-height: 22px;
}
.r88-arch-empty.is-hide, .r88-arch-list.is-hide { display: none; }
"""

# ---------------------------------------------------------------- JS

JS_TMPL = r"""
/* SHELL-R87-SET v3 —— 「设置」页：左侧导航 + 「系统设置」内容（设计稿 1389:18609 / 1389:18725）
   ⚠ 勿手改此块；落地脚本 mg-work/r87/apply87.py。
   外壳原内容是 React 渲染的静态节点：本块**隐藏原节点 + 追加自绘节点**，
   并用 MutationObserver 兜底（React 若重渲染把我们的节点冲掉，自动补回）。 */
%(ICONS)s
%(DATA)s
(function () {
  var HOST_ATTR = 'data-r85-set';
  var mounted = false;

  function svgIcon(k, cls) {
    var s = ICON[k] || '';
    if (!cls) return s;
    return s.replace('<svg ', '<svg class="' + cls + '" ');
  }

  /* ---------- 导航 ---------- */
  function buildNav() {
    var nav = document.createElement('nav');
    nav.className = 'r85-nav';
    nav.setAttribute('aria-label', '设置导航');

    var back = document.createElement('button');
    back.type = 'button';
    back.className = 'r85-back';
    back.innerHTML = svgIcon('arrow') + '<span>返回</span>';
    back.addEventListener('click', function () {
      location.href = 'base.html';
    });
    nav.appendChild(back);

    NAV_GROUPS.forEach(function (g) {
      var box = document.createElement('div');
      box.className = 'r85-group';
      var t = document.createElement('div');
      t.className = 'r85-gt';
      t.textContent = g.title;
      box.appendChild(t);
      g.items.forEach(function (it) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'r85-navi';
        b.setAttribute('data-set-tab', it.id);
        b.setAttribute('aria-current', it.id === 'system' ? 'true' : 'false');
        b.innerHTML = svgIcon(it.ic) + '<span>' + it.t + '</span>';
        b.addEventListener('click', function () { selectTab(it.id, it.t); });
        box.appendChild(b);
      });
      nav.appendChild(box);
    });
    return nav;
  }

  /* ---------- 行控件 ---------- */
  /* ③ DS 标准 Select 的两枚内联图标（照官方 DOM：components/preview/component-select.html）
     —— 12×12 chevron + 12×12 清除 X，stroke=currentColor，颜色由 .giencoder-select-suffix 控。 */
  var SEL_ARROW = '<svg class="giencoder-select-arrow" viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M2 4l4 4 4-4"/></svg>';
  var SEL_CLEAR = '<button class="giencoder-select-clear" type="button" aria-label="清除选择"><svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M3 3l6 6M9 3l-6 6"/></svg></button>';

  /* 已挂载的 select 实例（供「点外部关闭」「切页关闭」使用） */
  var selects = [];
  var optSeq = 0;
  function closeAllSelects() { selects.forEach(function (s) { s.close(); }); }
  document.addEventListener('click', function () { closeAllSelects(); });

  /* 标准 anatomy：selector(.giencoder-select) > view[combobox] > view-text + suffix(arrow+clear)
     以及 popup > option-list > option（含 selected / disabled 态）。
     开合唯一开关 = .giencoder-popup-open（不写内联 display，靠 CSS 的 opacity+visibility 收放）。 */
  function ctlSelect(c, row) {
    var wrap = document.createElement('div');
    wrap.className = 'giencoder-select';
    /* r87 ②：宽度**自适应**（不写死 px）—— DS 侧 .giencoder-select 已由「撑满容器」改为 auto，
       inline-flex 会按内容收缩。c.w（设计稿实测 98/154/98/70）保留在数据里只作规格参考，
       不再写进 style；右对齐由 .r85-ctl 的 flex 行尾定位保证。 */

    var view = document.createElement('div');
    view.className = 'giencoder-select-view';
    view.tabIndex = 0;
    view.setAttribute('role', 'combobox');
    view.setAttribute('aria-haspopup', 'listbox');
    view.setAttribute('aria-expanded', 'false');
    view.setAttribute('aria-label', (row && row.t) || '选择器');

    var txt = document.createElement('span');
    txt.className = 'giencoder-select-view-text';
    txt.setAttribute('data-placeholder', c.o[0]);
    txt.textContent = c.v;

    var suf = document.createElement('span');
    suf.className = 'giencoder-select-suffix';
    /* r88 ③：项目筛选下拉不需要「清除 X」（DS 在 has-value 时 hover 会显示它）⇒ 可关掉 */
    suf.innerHTML = SEL_ARROW + (c.noClear ? '' : SEL_CLEAR);

    /* r88 ③：可选**前缀图标**槽位 —— DS Select 本体没有这个槽位，属本页适配层（.r88-sel-prefix） */
    if (c.ic) {
      var pre = document.createElement('span');
      pre.className = 'r88-sel-prefix';
      pre.innerHTML = svgIcon(c.ic);
      view.appendChild(pre);
    }
    view.appendChild(txt);
    view.appendChild(suf);

    var pop = document.createElement('div');
    pop.className = 'giencoder-select-popup';
    var ul = document.createElement('ul');
    ul.className = 'giencoder-select-option-list';
    ul.setAttribute('role', 'listbox');

    var lis = c.o.map(function (o) {
      var li = document.createElement('li');
      li.className = 'giencoder-select-option' + (o === c.v ? ' giencoder-select-option-selected' : '');
      li.setAttribute('role', 'option');
      li.setAttribute('aria-selected', o === c.v ? 'true' : 'false');
      li.id = 'r86opt-' + (++optSeq);
      li.tabIndex = -1;
      li.textContent = o;
      li.addEventListener('click', function (ev) { ev.stopPropagation(); pick(o); });
      ul.appendChild(li);
      return li;
    });
    pop.appendChild(ul);
    wrap.appendChild(view);
    wrap.appendChild(pop);

    var api = {
      close: function () {
        pop.classList.remove('giencoder-popup-open');
        view.setAttribute('aria-expanded', 'false');
        view.removeAttribute('aria-activedescendant');
      },
      open: function () {
        closeAllSelects();                      /* 一次只开一个 */
        pop.classList.add('giencoder-popup-open');
        view.setAttribute('aria-expanded', 'true');
      },
      isOpen: function () { return pop.classList.contains('giencoder-popup-open'); }
    };
    selects.push(api);

    function pick(v) {
      c.v = v;
      txt.textContent = v;
      wrap.classList.add('giencoder-select-has-value');   /* 有值 ⇒ hover 时箭头让位给清除 X */
      lis.forEach(function (li) {
        var on = li.textContent === v;
        li.classList.toggle('giencoder-select-option-selected', on);
        li.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      api.close();
      if (!c.quiet) toast('已切换为「' + v + '」');
      if (c.onPick) c.onPick(v);
    }

    /* 键盘高亮走 option 自身 :focus（组件本体只定义了 :hover，适配层在 CSS 里补了 :focus）
       ⚠️ 这里刻意不写取模运算符 —— 本段是 Python 模板串（JS_TMPL %% {...}），裸 %% 会被当格式化占位符 */
    function move(step) {
      var cur = lis.indexOf(document.activeElement);
      var nxt = cur < 0 ? (step > 0 ? 0 : lis.length - 1) : cur + step;
      if (nxt < 0) nxt = lis.length - 1;
      else if (nxt >= lis.length) nxt = 0;
      lis[nxt].focus();
      view.setAttribute('aria-activedescendant', lis[nxt].id);
    }

    view.addEventListener('click', function (ev) {
      ev.stopPropagation();
      if (api.isOpen()) api.close(); else api.open();
    });
    view.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') {
        ev.preventDefault();
        if (!api.isOpen()) api.open();
        move(ev.key === 'ArrowDown' ? 1 : -1);
      } else if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault();
        var cur = lis.indexOf(document.activeElement);
        if (api.isOpen() && cur >= 0) pick(lis[cur].textContent);
        else if (api.isOpen()) api.close();
        else api.open();
      } else if (ev.key === 'Escape') {
        if (api.isOpen()) { ev.stopPropagation(); api.close(); }
      } else if (ev.key === 'Tab') {
        api.close();
      }
    });
    pop.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') { ev.stopPropagation(); api.close(); view.focus(); }
      if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') { ev.preventDefault(); move(ev.key === 'ArrowDown' ? 1 : -1); }
      if (ev.key === 'Enter') { ev.preventDefault(); var c2 = lis.indexOf(document.activeElement); if (c2 >= 0) pick(lis[c2].textContent); }
    });

    /* ⚠️ c.noClear 时 suf 里只有箭头、没有清除钮 ⇒ 必须先判空
       （r88 踩过：直接 .addEventListener 会抛 TypeError，整个 buildPage 半途而废、页面白屏） */
    var clrBtn = suf.querySelector('.giencoder-select-clear');
    if (clrBtn) clrBtn.addEventListener('click', function (ev) {
      ev.stopPropagation();                     /* 清除按钮不触发展开/收起 */
      c.v = c.o[0];
      txt.textContent = c.o[0];
      wrap.classList.remove('giencoder-select-has-value');
      lis.forEach(function (li) {
        li.classList.remove('giencoder-select-option-selected');
        li.setAttribute('aria-selected', 'false');
      });
      api.close();
    });

    /* DS 约定：有值 ⇒ 挂 has-value（hover 时箭头让位给清除 X）。
       本页 select 都是「必选设置项」，当前值恒在选项里 ⇒ 恒为 true。
       ⚠️ 别写成 indexOf(c.v) > 0 —— 那会把"选中首项"误当无值。 */
    if (c.o.indexOf(c.v) >= 0) wrap.classList.add('giencoder-select-has-value');
    return wrap;
  }

  function ctlSwitch(c) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'r85-sw giencoder-switch' + (c.on ? ' giencoder-switch-checked' : '');
    b.setAttribute('role', 'switch');
    b.setAttribute('aria-checked', c.on ? 'true' : 'false');
    b.innerHTML = '<span class="giencoder-switch-handle"></span>';
    b.addEventListener('click', function () {
      c.on = !c.on;
      b.classList.toggle('giencoder-switch-checked', c.on);
      b.setAttribute('aria-checked', c.on ? 'true' : 'false');
    });
    return b;
  }

  /* ---------- 全局界面字号（邵先生 r87 ①） ----------
     设计稿把 .r85-slider 定为「字号调节器」，6 级：
       13 / 14（默认）/ 16 / 18 / 20 / 24 px。
     ⚠️ 它调的是**整个产品全局界面**的字号，不是本页局部 ⇒ 只改一个全局变量 `--ui-fs`，
        全站（页面自绘模块 + DS 组件 + 外壳 React 的顶栏/侧栏）都由它等比派生。
        机制见 apply87b-fontsize.py；各页在 <head> 里读了同一个 localStorage 键，
        所以本页调完，其余页面下次打开即生效。 */
  var FS_LEVELS = [13, 14, 16, 18, 20, 24];
  var FS_KEY = 'gi-ui-fs';
  var FS_DEFAULT_IDX = 1;            /* 14px = 默认档 */

  function fsReadIdx() {
    var v = null;
    try { v = localStorage.getItem(FS_KEY); } catch (e) {}
    var i = v === null ? -1 : FS_LEVELS.indexOf(v * 1);
    return i < 0 ? FS_DEFAULT_IDX : i;
  }
  function fsApply(i, persist) {
    var px = FS_LEVELS[i];
    document.documentElement.style.setProperty('--ui-fs', String(px));
    if (persist) { try { localStorage.setItem(FS_KEY, String(px)); } catch (e) {} }
    return px;
  }

  function ctlSlider() {
    var wrap = document.createElement('div');
    wrap.className = 'r85-slider';
    /* r88 ②：可聚焦 + ARIA —— 键盘也能调档（左右 / 上下 / HOME / END） */
    wrap.tabIndex = 0;
    wrap.setAttribute('role', 'slider');
    wrap.setAttribute('aria-label', '界面字号');
    wrap.setAttribute('aria-valuemin', '0');
    wrap.setAttribute('aria-valuemax', String(FS_LEVELS.length - 1));
    /* 设计稿实测：6 档刻度在容器内 x = 6 + n×48（轨道左缘 6、长 240） */
    var stops = [6, 54, 102, 150, 198, 246];
    /* 「小 / 默认 / 大」各自锚定的档位：首档 / 第 2 档 / 末档 */
    var lblStop = [0, 1, 5];
    /* 当前档：读全局存储（首次访问 = 第 2 档「默认」，与设计稿拇指 rel 52 一致） */
    var idx = fsReadIdx();
    fsApply(idx, false);
    var track = document.createElement('div');
    track.className = 'r85-sl-track';
    var done = document.createElement('div');
    done.className = 'r85-sl-done';
    var thumb = document.createElement('div');
    thumb.className = 'r85-sl-thumb';
    var lbls = document.createElement('div');
    lbls.className = 'r85-sl-lbls';
    var ticks = [];
    stops.forEach(function (x) {
      var tk = document.createElement('div');
      tk.className = 'r85-sl-tick';
      tk.style.left = x + 'px';
      wrap.appendChild(tk);
      ticks.push(tk);
    });
    ['小', '默认', '大'].forEach(function (t, i) {
      var s = document.createElement('span');
      s.textContent = t;
      /* lbls 的左缘 = 容器 x6，故 left = 档位 x − 6，再靠 translateX 左移半个字宽让中心落在档位上 */
      s.style.left = (stops[lblStop[i]] - 6) + 'px';
      lbls.appendChild(s);
    });
    function render() {
      thumb.style.left = stops[idx] + 'px';
      done.style.left = stops[0] + 'px';
      done.style.width = (stops[idx] - stops[0]) + 'px';
      ticks.forEach(function (t, i) { t.classList.toggle('is-on', i <= idx); });
      wrap.setAttribute('aria-valuenow', String(idx));
      wrap.setAttribute('aria-valuetext', FS_LEVELS[idx] + 'px');
    }
    render();

    /* ★ r88 ②：把「命中层」从 1px 高的轨道换成**整个 252×36 容器**（CSS 里装饰子元素全部 pointer-events:none），
       并用指针事件 + setPointerCapture 做真正的拖拽：
         · pointerdown 按下即跳到最近档，并锁住指针 —— 拖出滑块外也不丢事件；
         · pointermove 连续更新（只改视觉 `--ui-fs`，**不写 localStorage**，避免拖动中反复落盘）；
         · pointerup/cancel 才落盘 + 弹一次提示 ⇒ 拖过 6 档只提示一次，不会刷屏。 */
    var dragging = false, startIdx = idx;
    function pick(clientX) {
      var r = wrap.getBoundingClientRect();
      var x = clientX - r.left;      /* 容器坐标：stops 本来就是容器坐标，直接比，不做偏移换算 */
      var best = 0;
      for (var i = 1; i < stops.length; i++) {
        if (Math.abs(stops[i] - x) < Math.abs(stops[best] - x)) best = i;
      }
      return best;
    }
    function setIdx(i) {
      if (i === idx) return;
      idx = i;
      render();
      fsApply(idx, false);
    }
    wrap.addEventListener('pointerdown', function (ev) {
      if (ev.pointerType === 'mouse' && ev.button !== 0) return;
      ev.preventDefault();                       /* 同时挡掉文字选中 */
      dragging = true;
      startIdx = idx;
      wrap.classList.add('is-drag');
      if (wrap.setPointerCapture) { try { wrap.setPointerCapture(ev.pointerId); } catch (e) {} }
      setIdx(pick(ev.clientX));
    });
    /* ⚠️ move/up 挂 **window** 而不是 wrap：setPointerCapture 万一失败（合成事件 / 异常），
       只挂 wrap 的话指针一移出元素就收不到事件 ⇒ dragging 永远卡在 true（之后划过就误拖）。
       挂 window 两种情况下都收得到（捕获后的指针事件仍会冒泡到 window）。 */
    function onMove(ev) {
      if (!dragging) return;
      ev.preventDefault();
      setIdx(pick(ev.clientX));
    }
    function endDrag(ev) {
      if (!dragging) return;
      dragging = false;
      wrap.classList.remove('is-drag');
      if (wrap.releasePointerCapture) { try { wrap.releasePointerCapture(ev.pointerId); } catch (e) {} }
      if (idx !== startIdx) toast('界面字号已设为 ' + fsApply(idx, true) + 'px');
      else fsApply(idx, false);
    }
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', endDrag);
    window.addEventListener('pointercancel', endDrag);
    window.addEventListener('blur', endDrag);
    wrap.addEventListener('keydown', function (ev) {
      var d = 0;
      if (ev.key === 'ArrowRight' || ev.key === 'ArrowUp') d = 1;
      else if (ev.key === 'ArrowLeft' || ev.key === 'ArrowDown') d = -1;
      else if (ev.key === 'Home') { ev.preventDefault(); if (idx !== 0) { setIdx(0); toast('界面字号已设为 ' + fsApply(0, true) + 'px'); } return; }
      else if (ev.key === 'End') { ev.preventDefault(); var last = FS_LEVELS.length - 1; if (idx !== last) { setIdx(last); toast('界面字号已设为 ' + fsApply(last, true) + 'px'); } return; }
      else return;
      ev.preventDefault();
      var n = idx + d;
      if (n < 0) n = 0; else if (n >= FS_LEVELS.length) n = FS_LEVELS.length - 1;
      if (n === idx) return;
      setIdx(n);
      toast('界面字号已设为 ' + fsApply(idx, true) + 'px');
    });
    wrap.appendChild(track);
    wrap.appendChild(done);
    wrap.appendChild(thumb);
    wrap.appendChild(lbls);
    return wrap;
  }

  function ctlSeg() {
    var box = document.createElement('div');
    box.className = 'r85-seg';
    [['sun', '浅色'], ['moon', '深色'], ['display', '跟随系统']].forEach(function (pair, i) {
      var b = document.createElement('button');
      b.type = 'button';
      /* r87 ③：DS Button 组件（secondary 档 + large 尺寸），外观适配层在 CSS 里 */
      b.className = 'giencoder-btn giencoder-btn-secondary giencoder-btn-size-large';
      b.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
      b.innerHTML = svgIcon(pair[0]) + '<span>' + pair[1] + '</span>';
      b.addEventListener('click', function () {
        [].forEach.call(box.children, function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        toast('外观已设为「' + pair[1] + '」');
      });
      box.appendChild(b);
    });
    return box;
  }

  function ctlUpdate() {
    var box = document.createElement('div');
    box.className = 'r85-ctl';
    var cb = document.createElement('label');
    cb.className = 'r85-cb';
    cb.innerHTML = '<input type="checkbox" class="giencoder-checkbox-input" checked>' +
                   '<span class="giencoder-checkbox-mask"></span><span>自动更新</span>';
    cb.querySelector('input').addEventListener('change', function (e) {
      cb.querySelector('.giencoder-checkbox-mask').parentNode.classList.toggle('giencoder-checkbox-checked', e.target.checked);
    });
    cb.classList.add('giencoder-checkbox', 'giencoder-checkbox-checked');
    box.appendChild(cb);
    /* r87 ③：DS Button 组件（secondary = 中性描边按钮的 DS 正解） */
    var DS_BTN = 'giencoder-btn giencoder-btn-secondary giencoder-btn-size-default';
    var log = document.createElement('button');
    log.type = 'button'; log.className = 'r85-btn ' + DS_BTN; log.textContent = '更新日志';
    log.addEventListener('click', function () { toast('打开更新日志'); });
    var chk = document.createElement('button');
    chk.type = 'button'; chk.className = 'r85-btn ' + DS_BTN; chk.textContent = '检查更新';
    chk.addEventListener('click', function () { toast('当前已是最新版本'); });
    box.appendChild(log); box.appendChild(chk);
    return box;
  }

  function ctlLogout() {
    var b = document.createElement('button');
    b.type = 'button';
    /* r87 ③：DS Button 组件；danger 色走本页适配层（DS 无「带边框 + 危险色文字」组合） */
    b.className = 'r85-btn is-danger giencoder-btn giencoder-btn-secondary giencoder-btn-size-default';
    b.textContent = '退出登录';
    b.addEventListener('click', function () { toast('已退出登录'); });
    return b;
  }

  /* ---------- 内容 ---------- */
  function buildRow(r) {
    var row = document.createElement('div');
    row.className = 'r85-row';
    var ic = document.createElement('span');
    ic.className = 'r85-ic';
    ic.innerHTML = svgIcon(r.ic);
    var tx = document.createElement('div');
    tx.className = 'r85-tx';
    var t = document.createElement('div'); t.className = 'r85-t'; t.textContent = r.t;
    var d = document.createElement('div'); d.className = 'r85-d'; d.textContent = r.d;
    tx.appendChild(t); tx.appendChild(d);
    row.appendChild(ic); row.appendChild(tx);

    var c = r.ctl, el = null;
    if (c.k === 'select') el = ctlSelect(c, row);
    else if (c.k === 'switch') el = ctlSwitch(c);
    else if (c.k === 'slider') el = ctlSlider();
    else if (c.k === 'seg') el = ctlSeg();
    else if (c.k === 'update') el = ctlUpdate();
    else if (c.k === 'logout') el = ctlLogout();
    if (el) {
      if (c.k === 'update') row.appendChild(el);
      else {
        var box = document.createElement('div');
        box.className = 'r85-ctl';
        box.appendChild(el);
        row.appendChild(box);
      }
    }
    return row;
  }

  /* ---------- ③ 已归档任务 ---------- */
  /* 状态：当前项目筛选 + 当前搜索词（都只影响列表显隐，不改数据） */
  var ARCH_ST = { proj: ARCH_FILTER_ALL, q: '' };

  /* 搜索框：直接复用 DS Input anatomy（wrapper > prefix 图标 + input），只叠本页 .r88-arch-search */
  function ctlArchSearch() {
    var wrap = document.createElement('div');
    wrap.className = 'giencoder-input-wrapper r88-arch-search';
    var pre = document.createElement('span');
    pre.className = 'giencoder-input-prefix';
    pre.innerHTML = svgIcon('i_search');
    var inp = document.createElement('input');
    inp.className = 'giencoder-input';
    inp.type = 'search';
    inp.placeholder = '搜索已归档任务';
    inp.setAttribute('aria-label', '搜索已归档任务');
    inp.addEventListener('input', function () { ARCH_ST.q = inp.value; archFilter(); });
    wrap.appendChild(pre);
    wrap.appendChild(inp);
    return wrap;
  }

  /* 项目筛选：复用 DS Select（ctlSelect），补 ic 前缀槽 + 关掉清除 X + 静音 toast（本页筛选很频繁） */
  function ctlArchProj() {
    var opts = [ARCH_FILTER_ALL];
    ARCH_ROWS.forEach(function (r) { if (opts.indexOf(r.proj) < 0) opts.push(r.proj); });
    var c = {
      k: 'select', ic: 'i_folder', noClear: true, quiet: true,
      v: ARCH_FILTER_ALL, o: opts,
      onPick: function (v) { ARCH_ST.proj = v; archFilter(); }
    };
    var el = ctlSelect(c);
    el.classList.add('r88-arch-proj');
    return el;
  }

  /* 行尾两个操作钮：默认画图标，行 hover 时 CSS 换成文字（几何见 .r88-arch-act 注释） */
  function ctlArchActs(r) {
    var acts = document.createElement('div');
    acts.className = 'r88-arch-acts';
    [['restore', 'i_undo', '恢复'], ['delete', 'i_trash', '删除']].forEach(function (a) {
      var b = document.createElement('button');
      b.type = 'button';
      /* r90 ②：改用 DS Button 组件（secondary + icon + size-small）；
         本页 r88-arch-act 只承载几何适配（28×28 ↔ 展开 52×32）与删除钮的危险色 */
      b.className = 'r88-arch-act giencoder-btn giencoder-btn-secondary giencoder-btn-icon ' +
                    'giencoder-btn-size-small';
      b.setAttribute('data-act', a[0]);
      b.setAttribute('aria-label', a[2] + '「' + r.t + '」');
      b.innerHTML = svgIcon(a[1]) + '<span>' + a[2] + '</span>';
      b.addEventListener('click', function (ev) {
        ev.stopPropagation();
        var row = b.closest('.r88-arch-row');
        if (row) row.classList.add('is-hide');     /* 原型行为：就地移出列表 */
        toast(a[0] === 'restore' ? '已恢复「' + r.t + '」' : '已删除「' + r.t + '」');
      });
      acts.appendChild(b);
    });
    return acts;
  }

  function buildArchRow(r) {
    var row = document.createElement('div');
    row.className = 'r88-arch-row';
    row.setAttribute('data-proj', r.proj);
    row.setAttribute('data-t', r.t);

    var main = document.createElement('div');
    main.className = 'r88-arch-main';
    var t = document.createElement('div');
    t.className = 'r88-arch-t';
    t.textContent = r.t;
    t.title = r.t;

    var m = document.createElement('div');
    m.className = 'r88-arch-m';
    var mic = document.createElement('span');
    mic.className = 'r88-arch-mic';
    /* r89：行内元信息图标换成 12 网格专版（i_folder12），16 网格的 i_folder 仍给下拉前缀用（那里渲染 16px） */
    mic.innerHTML = svgIcon('i_folder12');
    var mp = document.createElement('span');
    mp.className = 'r88-arch-mproj';
    mp.textContent = r.proj;
    var dot = document.createElement('span');
    dot.className = 'r88-arch-dot';
    var mu = document.createElement('span');
    mu.className = 'r88-arch-mu';
    mu.textContent = '归档于';
    var mt = document.createElement('span');
    mt.className = 'r88-arch-time';
    mt.textContent = r.time;
    m.appendChild(mic); m.appendChild(mp); m.appendChild(dot); m.appendChild(mu); m.appendChild(mt);

    main.appendChild(t);
    main.appendChild(m);
    row.appendChild(main);
    row.appendChild(ctlArchActs(r));
    return row;
  }

  /* 筛选：项目 + 关键词同时生效；全空则显示空态 */
  function archFilter() {
    var list = document.querySelector('.r88-arch-list');
    if (!list) return;
    var q = (ARCH_ST.q || '').replace(/^\s+|\s+$/g, '').toLowerCase();
    var n = 0;
    [].forEach.call(list.querySelectorAll('.r88-arch-row'), function (row) {
      var okP = ARCH_ST.proj === ARCH_FILTER_ALL || row.getAttribute('data-proj') === ARCH_ST.proj;
      var okQ = !q || row.getAttribute('data-t').toLowerCase().indexOf(q) >= 0;
      var on = okP && okQ;
      row.classList.toggle('is-hide', !on);
      if (on) n++;
    });
    var em = document.querySelector('.r88-arch-empty');
    if (em) em.classList.toggle('is-hide', n > 0);
    list.classList.toggle('is-hide', n === 0);
  }

  function buildArchPage() {
    ARCH_ST.proj = ARCH_FILTER_ALL;      /* 每次重建都回到初始筛选，避免与残留在 DOM 外的旧状态不一致 */
    ARCH_ST.q = '';
    var page = document.createElement('div');
    page.className = 'r85-page r88-arch';
    page.setAttribute('data-set-page', 'archived');

    /* 头部：标题 + 副标题（左），清空按钮（右，底对齐） */
    var head = document.createElement('div');
    head.className = 'r88-arch-head';
    var ht = document.createElement('div');
    ht.className = 'r88-arch-ht';
    var h1 = document.createElement('h1');
    h1.className = 'r88-arch-title';
    h1.textContent = '已归档任务';
    var sub = document.createElement('p');
    sub.className = 'r88-arch-sub';
    sub.textContent = ARCH_SUB;
    ht.appendChild(h1); ht.appendChild(sub);

    var clr = document.createElement('button');
    clr.type = 'button';
    clr.className = 'r88-arch-clear giencoder-btn giencoder-btn-size-large';
    clr.textContent = '清空归档任务';
    clr.addEventListener('click', function () {
      [].forEach.call(page.querySelectorAll('.r88-arch-row'), function (r) { r.classList.add('is-hide'); });
      archFilter();
      toast('已清空归档任务');
    });
    head.appendChild(ht); head.appendChild(clr);
    page.appendChild(head);

    /* 工具条：搜索框 + 项目筛选 */
    var bar = document.createElement('div');
    bar.className = 'r88-arch-bar';
    bar.appendChild(ctlArchSearch());
    bar.appendChild(ctlArchProj());
    page.appendChild(bar);

    /* 列表卡 */
    var list = document.createElement('div');
    list.className = 'r88-arch-list';
    list.setAttribute('role', 'list');
    ARCH_ROWS.forEach(function (r) { list.appendChild(buildArchRow(r)); });
    page.appendChild(list);

    var em = document.createElement('div');
    em.className = 'r88-arch-empty is-hide';
    em.textContent = '没有符合条件的归档任务';
    page.appendChild(em);
    return page;
  }

  function buildPage(tabId, title) {
    if (tabId === 'archived') return buildArchPage();
    var page = document.createElement('div');
    page.className = 'r85-page';
    page.setAttribute('data-set-page', tabId);
    var h = document.createElement('h1');
    h.className = 'r85-title';
    h.textContent = title;
    page.appendChild(h);

    var groups = tabId === 'system' ? CARDS_ALL : null;
    if (!groups) {
      var em = document.createElement('div');
      em.className = 'r85-empty';
      em.textContent = '「' + title + '」的设计稿尚未提供';
      page.appendChild(em);
      return page;
    }
    groups.forEach(function (rows, gi) {
      var card = document.createElement('section');
      /* 设计稿实测的边距差异：末张卡片文字左缘 56（其余 52）；中间那张底内距 16（首/末 20） */
      var cls = 'r85-card';
      if (gi === groups.length - 1) cls += ' is-tail';
      if (gi === groups.length - 2) cls += ' is-mid';
      card.className = cls;
      rows.forEach(function (r) { card.appendChild(buildRow(r)); });
      page.appendChild(card);
    });
    return page;
  }

  /* ---------- 挂载 ---------- */
  function host(list) {
    for (var i = 0; i < list.length; i++) if (list[i]) return list[i];
    return null;
  }

  function findSlots() {
    var aside = document.querySelector('aside');
    var main = document.querySelector('main');
    if (!aside || !main) return null;
    var scroller = aside.querySelector(':scope > div[class*="overflow-y-auto"]') || aside;
    var mainInner = main.querySelector(':scope > div') || main;
    return { scroller: scroller, mainInner: mainInner };
  }

  var TAB = { id: 'system', title: '系统设置' };

  function mount() {
    var s = findSlots();
    if (!s) return false;

    /* 隐藏外壳原内容（保留 DOM，只做视觉让位；外壳自身的路由等逻辑不受影响） */
    [].forEach.call(s.scroller.children, function (c) {
      if (!c.classList.contains('r85-nav-host')) c.setAttribute('data-set-original', '1');
    });
    [].forEach.call(s.mainInner.children, function (c) {
      if (!c.classList.contains('r85-page-host')) c.setAttribute('data-set-hidden', '1');
    });

    if (!document.querySelector('.r85-nav-host')) {
      var navHost = document.createElement('div');
      navHost.className = 'r85-nav-host';
      navHost.appendChild(buildNav());
      s.scroller.appendChild(navHost);
    }
    if (!document.querySelector('.r85-page-host')) {
      var pageHost = document.createElement('div');
      pageHost.className = 'r85-page-host';
      pageHost.appendChild(buildPage(TAB.id, TAB.title));
      s.mainInner.appendChild(pageHost);
    }
    document.body.setAttribute(HOST_ATTR, '1');
    mounted = true;
    return true;
  }

  function selectTab(id, title) {
    TAB = { id: id, title: title };
    [].forEach.call(document.querySelectorAll('.r85-navi'), function (b) {
      b.setAttribute('aria-current', b.getAttribute('data-set-tab') === id ? 'true' : 'false');
    });
    var pageHost = document.querySelector('.r85-page-host');
    if (pageHost) {
      selects.length = 0;          /* 重建页面 ⇒ 旧 select 实例整体作废，别留僵尸引用 */
      pageHost.innerHTML = '';
      pageHost.appendChild(buildPage(id, title));
    }
  }

  /* ---------- ① aside 定宽：中和外壳的拖拽条 ----------
     外壳是 React 渲染的，改不到 JSX；CSS 已把把手 display:none 并锁死宽度。
     这里再在**捕获阶段**拦掉 mousedown / pointerdown 做双保险
     （文字选择也要挡：拖把手的同时会选中侧栏文字）。 */
  ['mousedown', 'pointerdown'].forEach(function (t) {
    document.addEventListener(t, function (ev) {
      var el = ev.target;
      if (el && el.closest && el.closest('[role="separator"][aria-label="调整菜单宽度"]')) {
        ev.stopPropagation();
        ev.preventDefault();
      }
    }, true);
  });

  /* ---------- 轻提示 ---------- */
  var toastEl = null, toastTimer = null;
  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'r85-toast';
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    requestAnimationFrame(function () { toastEl.classList.add('is-on'); });
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('is-on'); }, 1600);
  }

  /* ---------- 启动 + 兜底 ---------- */
  function boot() {
    if (mount()) return;
    var mo = new MutationObserver(function () {
      if (mount()) { mo.disconnect(); }
    });
    mo.observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();

  /* React 重渲染把我们的节点冲掉时补回 */
  var guard = new MutationObserver(function () {
    if (!mounted) return;
    if (!document.querySelector('.r85-nav-host') || !document.querySelector('.r85-page-host')) {
      mounted = false;
      mount();
    }
  });
  guard.observe(document.body, { childList: true, subtree: true });
})();
"""

JS = JS_TMPL % {'ICONS': build_icon_js(), 'DATA': DATA_JS}

CSS_BLOCK = '<style id="%s">%s</style>\n' % (CSS_ID, CSS)
JS_BLOCK = '<script id="%s">%s</script>\n' % (JS_ID, JS)

# 摘历代标记（r85 / r86 / r87 已交付；r88 = 本代）。任一命中 0 次都合法 ⇒ 脚本自愈：
# 页面处于 r85 态摘 2 件、r86 态摘 2 件、r87 态摘 2 件、r88 态摘 2 件、全新页面摘 0 件。
# ⚠️ 历代标记都要列全（r88 起有四代）—— 漏一代就会「两代并存」；
# ⚠️ **含本代自身**：否则重跑时 NEW_TOKENS 断言会因「基线上已存在本轮标记」直接报错（幂等失效）。
PRIOR = (
    (re.compile(r'<style id="r85-set-css">.*?</style>\n', re.S), None),
    (re.compile(r'<script id="r85-set-js">.*?</script>\n', re.S), None),
    (re.compile(r'<style id="r86-set-css">.*?</style>\n', re.S), None),
    (re.compile(r'<script id="r86-set-js">.*?</script>\n', re.S), None),
    (re.compile(r'<style id="r87-set-css">.*?</style>\n', re.S), None),
    (re.compile(r'<script id="r87-set-js">.*?</script>\n', re.S), None),
    (re.compile(r'<style id="r88-set-css">.*?</style>\n', re.S), None),
    (re.compile(r'<script id="r88-set-js">.*?</script>\n', re.S), None),
)

NEW_TOKENS = ['r88-set-css', 'r88-set-js', 'r85-nav-host', 'r85-page-host']

# r85 手搓件的类名：换代后必须彻底绝迹（防止新旧两套 select 并存）
DEAD_TOKENS = ['r85-sel', 'r85-menu']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()

    path = os.path.join(REPO, 'pages', PAGE)
    txt = io.open(path, encoding='utf-8').read()
    base = txt

    removed = 0
    for rx, n in PRIOR:
        base, k = rx.subn('', base)
        removed += k
        if k > 1:
            sys.exit('!! 摘除 %s 命中 %d 次（同一代标记不应多于 1 份）' % (rx.pattern[:44], k))

    blob = CSS_BLOCK + JS_BLOCK
    for tok in NEW_TOKENS:
        if tok in base:
            sys.exit('!! 基线上已存在本轮标记 %r' % tok)
    for tok in NEW_TOKENS:
        if tok not in blob:
            sys.exit('!! 新块缺少标记 %r' % tok)
    for tok in DEAD_TOKENS:
        if tok in base:
            sys.exit('!! 摘块后基线里仍残留上一代类名 %r' % tok)
        if tok in blob:
            sys.exit('!! 本代新块里不该再出现上一代类名 %r' % tok)

    anchor = '</body>'
    if base.count(anchor) != 1:
        sys.exit('!! </body> 命中 %d 次' % base.count(anchor))
    out = base.replace(anchor, blob + anchor)

    if args.dry:
        print('%s  %d → %d (%+d)  摘掉旧块 %d 件' % (PAGE, len(txt), len(out), len(out) - len(txt), removed))
        print('--dry：未写盘（上面这个数字未含字号派生）')
        return

    # 与 apply88b-fontsize.py 对齐：本块里的 line-height / height 同样要按 --ui-fs-ratio 派生。
    # 走「先还原再派生」的固定点操作 ⇒ 与 apply88b 谁先谁后都得到同一结果（顺序无关）。
    # ⚠ 必须用 converge() 而不是 scale_css(unscale(x))：后者会连 <style id="r87-ui-css"> 一起还原，
    #   把里面尾风的 line-height 与 .giencoder-select-view 的裸 min-height 永久吃掉（r87 踩过）。
    #   （字号块的 id 仍是 r87-ui-css / r87-ui-js：它是 r87 引入的**常驻机制**，内容每轮由 apply88b 重建，
    #     不随补丁代数改名 —— 改名需要额外摘旧块，净收益为 0 而多一处出错面。）
    import importlib.util
    spec = importlib.util.spec_from_file_location('fs88b', os.path.join(HERE, 'apply88b-fontsize.py'))
    fs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fs)
    out = fs.converge(out)

    print('%s  %d → %d (%+d)  摘掉旧块 %d 件' % (PAGE, len(txt), len(out), len(out) - len(txt), removed))
    io.open(path, 'w', encoding='utf-8').write(out)


if __name__ == '__main__':
    main()

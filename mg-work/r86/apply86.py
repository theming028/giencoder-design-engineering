# -*- coding: utf-8 -*-
"""r86 · 「设置」页四条修订（在 r85 落地的导航 + 系统设置内容上迭代）

邵先生 r86 四条：
  ① aside 定宽、禁拖拽（外壳那个 role=separator 的拖拽条要中和掉）
  ② 卡片内 item 间隔线加深一级（--color-fill-2 → --color-border-2）
  ③ 卡片右侧 .r85-ctl 改用 DS 标准 select 组件（.giencoder-select 全套要素）
  ④ 行图标底 .r85-ic 加深一级（--color-fill-2 → --color-fill-3）

本脚本是 r85 `apply85.py` 的**接续改写版**：CSS/JS 块整体换代（摘 r85 + r86 两代标记），
r85 自绘的导航与内容结构、类名（r85-nav-host / r85-page-host 等）保持不变。
⚠️ r85 手搓的 .r85-sel / .r85-menu 已整体移除，select 一律走 DS 标准组件。

用法：
  python mg-work/r86/apply86.py                 # 应用（幂等：先摘旧块再插）
  python mg-work/r86/apply86.py --dry           # 只报告，不写盘
"""
import argparse
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
# 图标素材沿用 r85 的设计稿导出（同一份设计稿 1389:18609 / 1389:18725，本轮未变）
RAW = os.path.join(os.path.dirname(HERE), 'r85', 'raw')
PAGE = 'settings.html'

CSS_ID = 'r86-set-css'
JS_ID = 'r86-set-js'
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
"""

# ---------------------------------------------------------------- CSS

CSS = """
/* ★ 第 85 轮 · 「设置」页按设计稿重做（MasterGo 1389:18609 导航 + 1389:18725 系统设置内容）
   规则：色值一律走 token；设计稿里没有对应 token 的色用最接近的语义 token 顶替（见注释）。
   ⚠️ 本块由 mg-work/r86/apply86.py 生成，勿手改。 */

/* ---------- 布局容器 ---------- */
/* 外壳原内容（React 渲染的既定导航与设置页）隐藏，由本块自绘节点接管 */
body[data-r85-set] [data-set-original],
body[data-r85-set] [data-set-hidden] { display: none !important; }
body[data-r85-set] .r85-nav-host { width: 232px; margin: 0 auto; }
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
.r85-nav { display: flex; flex-direction: column; width: 232px; }
.r85-back {
  display: flex; align-items: center; gap: 6px; width: 100%; height: 32px;
  padding: 5px 10px; box-sizing: border-box; border: 0; border-radius: 4px;
  background: none; cursor: pointer; color: #6B6B6B;
  font-family: var(--font-family); font-size: var(--font-size-body-3); line-height: 22px; text-align: left;
}
.r85-back:hover { background: var(--color-fill-2); }
.r85-back > svg { flex: none; width: 14px; height: 14px; }

.r85-group { display: flex; flex-direction: column; margin-top: 20px; }
.r85-gt {
  margin: 0 2px 8px; color: var(--color-text-3);
  font-family: var(--font-family); font-size: var(--font-size-body-1); line-height: 16px;
}
.r85-navi {
  display: flex; align-items: center; gap: 8px; width: 100%; height: 36px; padding: 0 12px;
  box-sizing: border-box; border: 0; border-radius: 8px; cursor: pointer;
  background: var(--color-fill-1); color: var(--color-text-1);
  font-family: var(--font-family); font-size: var(--font-size-body-3); line-height: 22px; text-align: left;
  transition: background-color .12s ease;
}
.r85-navi + .r85-navi { margin-top: 2px; }
.r85-navi > svg { flex: none; width: 16px; height: 16px; color: var(--color-text-1); }
.r85-navi:hover { background: var(--color-fill-2); }
/* 选中：底 #ECEEF2 + 图标 #3770F7（设计稿实测；两者均在设计系统既有色板内） */
.r85-navi[aria-current='true'] { background: #ECEEF2; }
.r85-navi[aria-current='true'] > svg { color: var(--color-primary-6); }

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
  background: var(--color-fill-1); border-radius: 8px;
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

/* ---------- ③ 选择器：改用 DS 标准 select 组件（邵先生 r86） ----------
   r85 那两条手搓规则（自制触发框 + 自制下拉条）已整块删除，本代不再出现它们的类名。
   这里只留「适配层」，组件本体一个字不动（.giencoder-select* 的定义随页面内联，
   即 components.css「=== Select 选择器 ===」那一节）。
   适配层只做三件事：
   · flex: none —— .r85-ctl 是 flex 容器，不锁死会被压缩（触发框定宽来自设计稿实测 98/154/70）；
   · 右内距 12 → 8 —— DS 默认左右对称 12px，但设计稿的箭头是**紧贴右侧**的：
     设计稿实测「文字左缘距框 13px（= 1px 边框 + 12px 内距）/ 箭头墨迹右缘距框 10px」。
     按 DS 的 12px 右内距算，98px 的框只给文字留 52px，而「标准模式」实测需 56px
     ⇒ 出省略号（70px 的「中文」更明显）。收到 8px 后文字区 56px 正好容纳，
     且箭头墨迹右距变成 11px ≈ 设计稿的 10px —— 比默认值**更贴合设计稿**。
   · 给 option 补 :focus 视觉 —— 组件本体只有 :hover，键盘上下键移动时会看不见高亮。 */
body[data-r85-set] .r85-ctl > .giencoder-select { flex: none; }
body[data-r85-set] .r85-ctl .giencoder-select-view { padding-right: 8px; }
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
   ⚠ 刻度挂 .r85-slider（不是 .r85-sl-track）——挂 track 会叠加 track 的 top:6，整条刻度下移 6px。 ---------- */
.r85-slider { position: relative; width: 252px; height: 36px; }
.r85-sl-track {
  position: absolute; left: 6px; top: 6px; width: 240px; height: 1px;
  background: var(--color-border-3);
}
.r85-sl-done { position: absolute; top: 6px; height: 1px; background: var(--color-text-1); }
.r85-sl-tick {
  position: absolute; top: 2px; width: 1px; height: 8px; background: var(--color-border-3);
}
.r85-sl-tick.is-on { background: var(--color-text-1); }
.r85-sl-thumb {
  position: absolute; top: 0; width: 4px; height: 12px; margin-left: -2px;
  border-radius: 8px; background: var(--color-text-1); cursor: grab;
}
.r85-sl-lbls { position: absolute; left: 6px; right: 6px; top: 20px; height: 16px; }
.r85-sl-lbls > span {
  position: absolute; top: 0; color: var(--color-text-3);
  font-family: var(--font-family); font-size: var(--font-size-body-1); line-height: 16px;
  transform: translateX(-50%);
}

/* ---------- 分段控件（外观：浅色 / 深色 / 跟随系统，各 128×40） ---------- */
.r85-seg { display: flex; align-items: center; gap: 8px; }
.r85-seg > button {
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  width: 128px; height: 40px; box-sizing: border-box;
  background: var(--color-white); border: 1px solid var(--color-border-1); border-radius: 8px;
  color: var(--color-text-1); cursor: pointer;
  font-family: var(--font-family); font-size: var(--font-size-body-3); line-height: 22px;
  transition: border-color .12s ease;
}
.r85-seg > button > svg { flex: none; width: 16px; height: 16px; }
.r85-seg > button:hover { border-color: var(--color-border-3); }
/* 选中态：虚线 2px（设计稿 #C4C7C9） */
.r85-seg > button[aria-pressed='true'] { border: 2px dashed var(--color-border-3); }

/* ---------- 普通按钮（更新日志 / 检查更新 / 退出登录） ---------- */
.r85-btn {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 104px; height: 32px; padding: 0 12px; box-sizing: border-box;
  background: var(--color-white); border: 1px solid var(--color-border-1); border-radius: 8px;
  color: var(--color-text-1); cursor: pointer;
  font-family: var(--font-family); font-size: var(--font-size-body-3); line-height: 22px;
  transition: border-color .12s ease, background-color .12s ease;
}
.r85-btn:hover { border-color: var(--color-border-3); background: var(--color-fill-2); }
.r85-btn.is-danger { color: var(--color-danger); }

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
"""

# ---------------------------------------------------------------- JS

JS_TMPL = r"""
/* SHELL-R86-SET v2 —— 「设置」页：左侧导航 + 「系统设置」内容（设计稿 1389:18609 / 1389:18725）
   ⚠ 勿手改此块；落地脚本 mg-work/r85/apply85.py。
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
    wrap.style.width = c.w + 'px';

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
    suf.innerHTML = SEL_ARROW + SEL_CLEAR;

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
      toast('已切换为「' + v + '」');
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

    suf.querySelector('.giencoder-select-clear').addEventListener('click', function (ev) {
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

  function ctlSlider() {
    var wrap = document.createElement('div');
    wrap.className = 'r85-slider';
    /* 设计稿实测：6 档刻度在容器内 x = 6 + n×48（轨道左缘 6、长 240） */
    var stops = [6, 54, 102, 150, 198, 246];
    /* 「小 / 默认 / 大」各自锚定的档位：首档 / 第 2 档 / 末档 */
    var lblStop = [0, 1, 5];
    /* 当前档 = 第 2 档（设计稿拇指在 rel 52，「默认」标签中心也在 rel 54） */
    var idx = 1;
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
    }
    render();
    track.addEventListener('click', function (ev) {
      var r = track.getBoundingClientRect();
      var x = ev.clientX - r.left + stops[0];   /* track 左缘 = 容器 x6，换算回容器坐标 */
      var best = 0;
      for (var i = 1; i < stops.length; i++) if (Math.abs(stops[i] - x) < Math.abs(stops[best] - x)) best = i;
      idx = best;
      render();
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
    var log = document.createElement('button');
    log.type = 'button'; log.className = 'r85-btn'; log.textContent = '更新日志';
    log.addEventListener('click', function () { toast('打开更新日志'); });
    var chk = document.createElement('button');
    chk.type = 'button'; chk.className = 'r85-btn'; chk.textContent = '检查更新';
    chk.addEventListener('click', function () { toast('当前已是最新版本'); });
    box.appendChild(log); box.appendChild(chk);
    return box;
  }

  function ctlLogout() {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'r85-btn is-danger';
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

  function buildPage(tabId, title) {
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

# 摘历代标记（r85 = 上一代已交付；r86 = 本代）。任一命中 0 次都合法 ⇒ 脚本自愈：
# 页面处于 r85 态时摘 2 件、处于 r86 态时摘 2 件、全新页面时摘 0 件。
PRIOR = (
    (re.compile(r'<style id="r85-set-css">.*?</style>\n', re.S), None),
    (re.compile(r'<script id="r85-set-js">.*?</script>\n', re.S), None),
    (re.compile(r'<style id="r86-set-css">.*?</style>\n', re.S), None),
    (re.compile(r'<script id="r86-set-js">.*?</script>\n', re.S), None),
)

NEW_TOKENS = ['r86-set-css', 'r86-set-js', 'r85-nav-host', 'r85-page-host']

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

    print('%s  %d → %d (%+d)  摘掉旧块 %d 件' % (PAGE, len(txt), len(out), len(out) - len(txt), removed))
    if args.dry:
        print('--dry：未写盘')
        return
    io.open(path, 'w', encoding='utf-8').write(out)


if __name__ == '__main__':
    main()

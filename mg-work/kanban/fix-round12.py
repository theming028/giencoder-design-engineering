# -*- coding: utf-8 -*-
"""round12 / kanban.html（任务看板 · 研发工作台）
1) 彻底移除外壳左上角「切换工作空间」模块（含侧边栏切换钮，终态本来就是 opacity:0）——首帧即隐藏，消除切换页签时的闪现
2) 泳道 .kb-col hover 背景加深一级（fill-1 → fill-2）
3) 智能助手悬浮球视觉升级（品牌渐变球 + 柔光晕 + 顶部高光，替换 Liquid Glass）
4) kb-coop 模态：仅覆盖 main、宽度 main 的 80%、顶对齐、距 main 底 48px、纵向自适应
   并补齐对设计稿实测的内层规格（表头 32px/#F8F9FA、行 36px/白底、容器 1px 边框+6px 圆角、
   筛选控件 220/120/120/265 + 8px 间距、关闭键裸 ×、列宽/首列内距）
幂等。
"""
import io, sys, re

P = r'E:\GienCoder\giencoder-design-engineering\pages\kanban.html'
s = io.open(P, encoding='utf-8').read()
orig = len(s)
log = []

# ================================================================ 1. 隐藏工作空间模块
WS_CSS = """/* r12: 研发工作台不含「切换工作空间」模块 —— 外壳把它包在一个带 transition:opacity .3s 的 div 里，
   切换页签时首帧可见、随后淡出，表现为"闪现"。这里在首帧就彻底移除（display:none 不参与绘制）。
   该块的终态本就是 opacity:0 / pointer-events:none，故移除不损失任何可见功能。 */
header > div.w-60 > div:nth-child(2),
header div:has(> div.relative > button[aria-label="切换侧边栏"]) { display: none !important; }
"""
if 'r12: 研发工作台不含' in s:
    log.append('[1] ws-hide 已存在，跳过')
else:
    m = re.search(r'<style>\s*svg\.animate-spin', s)
    if m:
        anchor = '</style>'
        idx = s.index(anchor, m.end())
        s = s[:idx] + WS_CSS + s[idx:]
        log.append('[1] ws-hide 写入首个 <style> 块')
    else:
        log.append('[1] !! 首个 <style> 块锚点未找到'); sys.exit(1)

# ================================================================ 2. 泳道 hover
LANE = """      /* r12: 泳道 hover —— 背景加深一级（fill-1 → fill-2，Token 驱动） */
      .kb-col { transition: background-color .12s ease; }
      .kb-col:hover { background: var(--color-fill-2); }
"""
if 'r12: 泳道 hover' in s:
    log.append('[2] 泳道 hover 已存在，跳过')
else:
    a = '      .kb-col { position: relative; flex: 1; min-width: 0; display: flex; flex-direction: column; background: var(--color-fill-1); border-radius: 8px; overflow: hidden; }\n'
    if a not in s:
        log.append('[2] !! .kb-col 锚点未找到'); sys.exit(1)
    s = s.replace(a, a + LANE, 1)
    log.append('[2] 泳道 hover 写入')

# ================================================================ 3. FAB 视觉升级
FAB_START = '      /* 可拖动：按住悬浮球在页面内自由移动 */'
FAB_END = '      /* ===== giencoder DatePicker'
FAB_NEW = """      /* ===== r12: 智能助手悬浮球（视觉升级）=====
         结构：品牌渐变球体（primary → purple）+ 顶部玻璃高光 + 主题色柔光晕 + 内高光/内底缘
         交互：idle 静置发光 → hover 上浮放大 + 光晕加强 → active 回落 → dragging 收缩
         保留 r11 的可拖动能力（.is-dragging 由 bindFab 维护） */
      .kb-fab {
        cursor: grab; touch-action: none; -webkit-user-select: none; user-select: none;
        background: linear-gradient(150deg, var(--color-primary-6) 0%, rgb(var(--purple-6)) 100%);
        border: none; color: var(--color-white);
        box-shadow:
          0 6px 16px rgba(var(--giencoderblue-6), 0.38),
          0 2px 6px rgba(15, 23, 42, 0.16),
          inset 0 1px 1px rgba(255, 255, 255, 0.45),
          inset 0 -2px 6px rgba(0, 0, 0, 0.14);
        transition: transform .18s cubic-bezier(0.23, 1, 0.32, 1), box-shadow .18s ease;
      }
      /* 顶部镜面高光：给球体体积感 */
      .kb-fab::after {
        content: ''; position: absolute; left: 14%; top: 8%; width: 72%; height: 38%;
        border-radius: 50%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.55), rgba(255, 255, 255, 0));
        pointer-events: none;
      }
      .kb-fab svg { position: relative; z-index: 1; width: 22px; height: 22px; }
      .kb-fab:hover {
        transform: translateY(-2px) scale(1.04);
        box-shadow:
          0 10px 24px rgba(var(--giencoderblue-6), 0.46),
          0 3px 8px rgba(15, 23, 42, 0.18),
          inset 0 1px 1px rgba(255, 255, 255, 0.50),
          inset 0 -2px 6px rgba(0, 0, 0, 0.14);
      }
      .kb-fab:active { transform: translateY(0) scale(0.98); }
      .kb-fab.is-dragging { cursor: grabbing; transform: scale(0.96); }
      @media (prefers-reduced-motion: reduce) { .kb-fab { transition: none; } }
      /* 深色主题：暗底上提高内高光占比、去掉彩色外投影偏移 */
      [giencoder-theme='dark'] .kb-fab {
        border: none;
        background: linear-gradient(150deg, rgb(var(--giencoderblue-6)) 0%, rgb(var(--purple-5)) 100%);
        box-shadow:
          0 6px 16px rgba(0, 0, 0, 0.50),
          0 1px 2px rgba(0, 0, 0, 0.35),
          inset 0 1px 1px rgba(255, 255, 255, 0.28),
          inset 0 -2px 6px rgba(0, 0, 0, 0.35);
      }
      [giencoder-theme='dark'] .kb-fab::after {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.24), rgba(255, 255, 255, 0));
      }
"""
if 'r12: 智能助手悬浮球（视觉升级）' in s:
    log.append('[3] FAB 已升级，跳过')
else:
    i = s.index(FAB_START); j = s.index(FAB_END, i)
    s = s[:i] + FAB_NEW + s[j:]
    log.append('[3] FAB 视觉升级写入')

# FAB 图标：换成 AI 四角星（大星 + 小星）
OLD_ICON = ('<svg viewBox="0 0 20 20" fill="none"><rect x="2.5" y="4.5" width="13" height="11" rx="3" stroke="currentColor" '
            'stroke-width="1.3"/><path d="M6.5 9.5v1.5M10 9.5v1.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>'
            '<path d="M14.5 2.5l.6 1.4 1.4.6-1.4.6-.6 1.4-.6-1.4-1.4-.6 1.4-.6.6-1.4Z" fill="currentColor"/></svg>')
NEW_ICON = ('<svg viewBox="0 0 20 20" fill="none" aria-hidden="true">'
            '<path d="M9 4.2C9.36 7.5 12.3 10.44 15.6 10.8C12.3 11.16 9.36 14.1 9 17.4C8.64 14.1 5.7 11.16 2.4 10.8'
            'C5.7 10.44 8.64 7.5 9 4.2Z" fill="currentColor"/>'
            '<path d="M16.2 1.2C16.35 2.55 17.55 3.75 18.9 3.9C17.55 4.05 16.35 5.25 16.2 6.6C16.05 5.25 14.85 4.05 13.5 3.9'
            'C14.85 3.75 16.05 2.55 16.2 1.2Z" fill="currentColor"/></svg>')
if 'M9 4.2C9.36 7.5' in s:
    log.append('[3b] FAB 图标已替换，跳过')
elif OLD_ICON in s:
    s = s.replace(OLD_ICON, NEW_ICON, 1)
    log.append('[3b] FAB 图标替换为 AI 四角星')
else:
    log.append('[3b] !! FAB 图标锚点未找到（继续）')

# ================================================================ 4a. 新增页面 token
TOK_OLD = """        --kb-coop-mask: rgba(0, 0, 0, 0.32);
        --kb-coop-top: 44px;"""
TOK_NEW = """        --kb-coop-mask: rgba(0, 0, 0, 0.32);
        --kb-coop-gap-bottom: 48px;          /* r12: 面板底与 main 底固定间距 */
        --kb-coop-width: 80%;                /* r12: 面板宽 = main 宽 × 80% */
        --kb-pg-active-bg: #E8F0FE;          /* 设计稿实测：分页当前页底 */
        --kb-pg-active-bd: #BBD1FB;          /* 设计稿实测：分页当前页描边 */"""
if '--kb-coop-gap-bottom' in s:
    log.append('[4a] token 已存在，跳过')
else:
    if TOK_OLD not in s:
        log.append('[4a] !! token 锚点未找到'); sys.exit(1)
    s = s.replace(TOK_OLD, TOK_NEW, 1)
    log.append('[4a] token 写入')

# ================================================================ 4b. 重写模态 CSS
MODAL_CSS = """/* r12-coop-modal-css */

      /* ===== r12: 待协作任务模态（仅覆盖 main；复用 giencoder-modal 契约类 + kb- 适配层）=====
         位置：绝对定位于 main（bindCoopModal 把节点提到 main 下），顶与 main 顶对齐，
               底距 main 底 48px（max-height 约束），高度随内容自适应。
         尺寸：宽 = main 的 80%。内层规格对齐设计稿实测值。 */
      main.kb-main-rel { position: relative; }
      .kb-coop[hidden] { display: none; }
      .kb-coop { position: absolute; inset: 0; z-index: 1200; }
      .kb-coop-mask {
        position: absolute; inset: 0; background: var(--kb-coop-mask);
        -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px);
      }
      .kb-coop-dialog {
        position: absolute; left: 50%; top: 0; transform: translateX(-50%);
        width: var(--kb-coop-width);
        height: auto; max-height: calc(100% - var(--kb-coop-gap-bottom));
        display: flex; flex-direction: column; overflow: hidden;
        background: var(--kb-coop-bg); border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
      }
      /* 头部：pad 16/24，标题与关闭键同轴居中（设计稿标题中心距顶 31px、关闭键中心 33.5px） */
      .kb-coop-head { flex: none; border-bottom: none; padding: 16px 24px 0; min-height: 32px; }
      .kb-coop-head .giencoder-modal-title { font-size: var(--font-size-title-1); font-weight: 600; line-height: 24px; }
      /* 关闭键：设计稿是裸 ×（10×10 字形、无边框无底色），32×32 命中区 */
      .kb-coop-close {
        width: 32px; height: 32px; padding: 0; border: none; background: none; border-radius: 6px;
        display: inline-flex; align-items: center; justify-content: center;
        color: var(--color-text-2); flex: none;
      }
      .kb-coop-close:hover { background: var(--color-fill-2); color: var(--color-text-1); }
      .kb-coop-content { flex: 1; min-height: 0; display: flex; flex-direction: column; padding: 18px 24px 20px; }
      /* 筛选行：设计稿实测 搜索 220 / 选择 120 / 日期 265，间距 8 */
      .kb-coop-filters { flex: none; display: flex; align-items: center; gap: 8px; margin-bottom: 16px; }
      .kb-coop-search, .kb-coop-search.giencoder-input-wrapper { width: 220px; min-width: 220px; height: 32px; border-radius: 6px; padding: 0 12px; }
      .kb-coop-search-input { width: 100%; border: none; outline: none; background: transparent; font-size: var(--font-size-body-3); color: var(--color-text-1); }
      .kb-coop-search-input::placeholder { color: var(--color-text-3); }
      .kb-coop-search-ico { color: var(--color-text-3); }
      /* 选择器：宽度按设计稿 120px 为下限、随内容自适应，
         避免 CJK 字宽差异把「优先级：全部」挤成两行/把箭头挤出（见 components/select.json 盒模型约定） */
      .kb-coop-sel { width: auto; min-width: 120px; }
      .kb-coop-sel .giencoder-select-view,
      .kb-coop-date .giencoder-input-wrapper {
        height: 32px; min-height: 32px; border-radius: 6px; border: 1px solid var(--color-border-2);
        background: var(--color-bg-1); box-shadow: none; padding: 0 12px;
      }
      .kb-coop-sel-lbl { color: var(--color-text-1); white-space: nowrap; flex: none; }
      .kb-coop-sel-val { color: var(--color-text-1); }
      .kb-coop-date, .kb-coop-date .giencoder-input-wrapper { width: 265px; min-width: 265px; }
      .kb-coop-date .kb-date-val { color: var(--color-text-1); }
      /* 表格容器：设计稿实测 = 白底卡片 + 1px #E5E5E5 边框 + 6px 圆角，含表头 */
      .kb-coop-tblwrap {
        flex: 1; min-height: 0; overflow: auto;
        background: var(--color-bg-1); border: 1px solid var(--color-border-2); border-radius: 6px;
      }
      .kb-coop-tbl { width: 100%; border-collapse: collapse; font-size: var(--font-size-body-3); }
      /* 表头：32px（6 + 20 + 6），底 #F8F9FA，其下 1px 行线 #EBECED */
      .kb-coop-tbl .giencoder-table-th {
        background: var(--kb-tbl-head-bg); color: var(--color-text-3); font-weight: 400;
        font-size: var(--font-size-body-3); padding: 6px 12px; line-height: 20px;
        border-bottom: 1px solid var(--kb-tbl-line); text-align: left;
      }
      /* 数据行：36px（6.5 + 22 + 6.5 + 1 行线） */
      .kb-coop-tbl .giencoder-table-td {
        padding: 6.5px 12px; line-height: 22px; color: var(--color-text-1);
        border-bottom: 1px solid var(--kb-tbl-line); white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis;
      }
      /* 首列内距 20px（设计稿：序号文字距容器内边 20px） */
      .kb-coop-tbl .giencoder-table-th:first-child,
      .kb-coop-tbl .giencoder-table-td:first-child { padding-left: 20px; }
      .kb-coop-tbl .giencoder-table-tr:hover .giencoder-table-td { background: var(--color-fill-1); }
      .kb-coop-tbl .kb-row-hover .giencoder-table-td { background: var(--color-fill-1); }
      .kb-coop-tbl .kb-row-hover .kb-td-title { color: var(--color-primary-6); }
      .kb-td-num { color: var(--color-text-3); }
      .kb-td-id { color: var(--color-text-3); }
      .kb-td-time { color: var(--color-text-3); }
      .kb-td-prio { font-weight: 500; }
      .kb-coop-tbl .kb-td-prio.kb-prio-high { color: var(--kb-prio-high); }
      .kb-coop-tbl .kb-td-prio.kb-prio-mid { color: var(--kb-prio-mid); }
      .kb-coop-tbl .kb-td-prio.kb-prio-low { color: var(--kb-prio-low); }
      .kb-coop-foot { flex: none; display: flex; align-items: center; justify-content: space-between; padding-top: 12px; }
      .kb-coop-stats { color: var(--color-text-2); font-size: var(--font-size-body-3); }
      .kb-coop-pager { display: flex; align-items: center; gap: 8px; }
      .kb-coop-pager .giencoder-pagination-item {
        width: 32px; height: 32px; border: 1px solid var(--color-border-2); border-radius: 6px;
        background: var(--color-bg-1); color: var(--color-text-1); font-size: var(--font-size-body-3);
        display: inline-flex; align-items: center; justify-content: center; cursor: pointer; line-height: 0;
      }
      .kb-coop-pager .giencoder-pagination-item-ellipsis { border: none; width: 24px; color: var(--color-text-3); }
      .kb-coop-pager .giencoder-pagination-item-active {
        background: var(--kb-pg-active-bg); border-color: var(--kb-pg-active-bd); color: var(--color-primary-6); font-weight: 500;
      }
      .kb-coop-pager .kb-pg-nav { color: var(--color-text-2); }
      .kb-coop-pageopt { width: 96px; min-width: 96px; }
      .kb-coop-pageopt .giencoder-select-view {
        height: 32px; min-height: 32px; border-radius: 6px;
        border: 1px solid var(--color-border-2); background: var(--color-bg-1); box-shadow: none; padding: 0 10px;
      }
      .kb-coop-jump { color: var(--color-text-2); font-size: var(--font-size-body-3); display: inline-flex; align-items: center; gap: 8px; }
      .kb-coop-jump .giencoder-input-wrapper { width: 48px; min-width: 48px; height: 32px; border-radius: 6px; padding: 0 8px; }
      .kb-coop-jump .giencoder-input { width: 100%; border: none; outline: none; background: transparent; text-align: center; }
      html.kb-coop-lock, html.kb-coop-lock body { overflow: hidden; }
      [giencoder-theme='dark'] .kb-coop-dialog { background: var(--color-bg-2); }
      [giencoder-theme='dark'] .kb-coop-tblwrap { background: var(--color-bg-3); }
      [giencoder-theme='dark'] .kb-coop-tbl .giencoder-table-th { background: var(--color-bg-4); }
"""
if 'r12-coop-modal-css' in s:
    log.append('[4b] 模态 CSS 已是 r12，跳过')
else:
    i = s.index('/* r11-coop-modal-css */')
    j = s.index('</style>', i)
    s = s[:i] + MODAL_CSS + s[j:]
    log.append('[4b] 模态 CSS 重写为 r12')

# ================================================================ 4c. 列宽对齐设计稿
CL_OLD = '<colgroup><col style="width:52px"><col style="width:132px"><col><col style="width:96px"><col style="width:110px"><col style="width:170px"></colgroup>'
CL_NEW = '<colgroup><col style="width:56px"><col style="width:115px"><col><col style="width:100px"><col style="width:120px"><col style="width:184px"></colgroup>'
if 'width:115px' in s and CL_OLD not in s:
    log.append('[4c] 列宽已是新值，跳过')
elif CL_OLD in s:
    s = s.replace(CL_OLD, CL_NEW, 1)
    log.append('[4c] 列宽对齐设计稿')
else:
    log.append('[4c] !! 列宽锚点未找到（继续）')

# ================================================================ 4d. JS：模态挂到 main 下 + main 打标
JS_OLD = """  function bindCoopModal(root) {
    var modal = root.querySelector('.kb-coop');
    var trigger = root.querySelector('.kb-stat--coop');
    if (!modal || !trigger) return;"""
JS_NEW = """  function bindCoopModal(root) {
    var modal = root.querySelector('.kb-coop');
    var trigger = root.querySelector('.kb-stat--coop');
    if (!modal || !trigger) return;
    /* r12: 面板只覆盖 main —— 把模态节点从 .kb-panel 内提到 <main> 下，
       否则绝对定位基准会是 .kb-panel（position:absolute），而不是 main */
    var host = document.querySelector('main');
    if (host) {
      host.classList.add('kb-main-rel');
      if (modal.parentElement !== host) host.appendChild(modal);
    }"""
if 'kb-main-rel' in s:
    log.append('[4d] JS 已处理，跳过')
elif JS_OLD in s:
    s = s.replace(JS_OLD, JS_NEW, 1)
    log.append('[4d] JS 模态提到 main 下')
else:
    log.append('[4d] !! bindCoopModal 锚点未找到'); sys.exit(1)

io.open(P, 'w', encoding='utf-8', newline='').write(s)
for l in log:
    print(l)
print('DONE  %d -> %d chars' % (orig, len(s)))

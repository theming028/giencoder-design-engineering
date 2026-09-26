# -*- coding: utf-8 -*-
"""构建 pages/task-detail.html：复用 kanban.html 的外壳与 DS，页面内容按设计稿重建。
设计依据：
  详情页画板 622:13950（1440x1080, bg #E5EDF5）
  左栏 1343:18534（936x1024）
  右栏 1343:18535（480x1024）
  折叠态 1343:18532（48x844, 竖排「展开 AI 会话」#57626D/14px/500/lh18）
"""
import io
import json
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
        --td-gap: 24px;              /* 两栏间隙，同时是拖动热区（设计稿 936+24+480=1440） */
        --td-right-w: 480px;         /* 右栏默认宽（设计稿实测） */
        --td-right-min: 320px;       /* 拖到此值以下，松手即自动折叠 */
        --td-left-min: 320px;        /* 左栏保底宽（与 JS LEFT_MIN 一致） */
        --td-collapsed-w: 48px;      /* 折叠条宽（设计稿实测） */
        --td-card: var(--color-fill-1);        /* #F7F7F7 卡片底 */
        --td-line: var(--color-fill-2);        /* #F2F2F2 分隔线 */
        --td-ink-2: #57626D;                   /* 折叠态文字（设计稿实测） */
        --td-surround: #E5EDF5;                /* 页面底（设计稿实测） */
        --td-bubble: #E5EDFE;                  /* 用户气泡（设计稿实测） */
        --td-meta: var(--color-text-3);
        --td-strong: var(--color-text-1);
      }
      /* 详情页注入口：撑满 main 的确定高度（main 为 844 高 / overflow:hidden） */
      .td-wrap { height: 100%; }
      .td-root {
        position: relative; width: 100%; height: 100%; min-height: 0;
        display: flex; background: var(--td-surround); overflow: hidden;
      }
      /* -------------------- 左栏 -------------------- */
      .td-left {
        flex: 1 1 auto; min-width: var(--td-left-min); box-sizing: border-box;
        display: flex; flex-direction: column; overflow: hidden;
        background: var(--color-bg-1); border-radius: 8px;
      }
      .td-bar {
        height: var(--td-bar); flex: none; box-sizing: border-box;
        display: flex; align-items: center; gap: 8px; padding: 0 20px;
        background: var(--color-bg-1);
      }
      .td-bar-title { font-size: var(--font-size-body-3); color: var(--td-strong); white-space: nowrap; }
      .td-bar-actions { margin-left: auto; display: flex; align-items: center; gap: 8px; }
      .td-btn { border-radius: 6px; }                       /* 设计稿 28 高 / radius 6 */
      /* 顶栏按钮宽度对齐设计稿：98(开始任务)/70(转派·协作·编辑) × 28，内边距 20px；
         图标按钮不参与（保持正方） */
      .td-bar-actions .giencoder-btn:not(.giencoder-btn-icon) { padding: 0 20px; }
      /* 适配层：DS Button(secondary + size-small + icon) → 设计稿 28×28 / radius 6 */
      .td-iconbtn { box-sizing: border-box; width: 28px; padding: 0; border-radius: 6px; line-height: 0; }
      .td-back { border-color: transparent; }
      .td-left-body { flex: 1; min-height: 0; display: flex; overflow: hidden; }
      .td-main {
        flex: 1 1 0; min-width: 0; overflow: auto; padding: 0 0 32px;
      }
      .td-title {
        margin: 0; box-sizing: border-box; padding: 16px 40px;
        background: var(--color-bg-2);                        /* #FAFAFA 标题区 */
        font-size: 18px; font-weight: 600; line-height: 28px; color: var(--td-strong);
      }
      .td-desc { padding: 24px 40px 0; font-size: var(--font-size-body-3); line-height: 24px; color: var(--color-text-2); }
      .td-desc p { margin: 0 0 12px; }
      .td-desc ul { margin: 0 0 12px; padding-left: 20px; }
      .td-desc li { margin-bottom: 4px; }
      .td-expand { display: flex; align-items: center; gap: 16px; margin-top: 12px; }
      .td-expand-line { flex: 1; height: 1px; background: var(--td-line); }
      .td-expand-btn { flex: none; }
      .td-sec { padding: 24px 40px 0; }
      .td-sec-head {
        display: inline-flex; align-items: center; gap: 4px; margin-bottom: 10px;
        font-size: var(--font-size-body-3); font-weight: 500; color: var(--td-ink-2);
      }
      .td-sec-head svg { width: 14px; height: 14px; flex: none; }
      .td-files { display: flex; flex-wrap: wrap; gap: 8px; }
      .td-file {
        box-sizing: border-box; display: flex; align-items: center; gap: 8px;
        height: 36px; padding: 0 12px; min-width: 0; max-width: 100%;
        background: var(--td-card); border-radius: var(--border-radius-large);
      }
      .td-file-ico { width: 16px; height: 16px; flex: none; color: var(--td-ink-2); line-height: 0; }
      .td-file-tx {
        font-size: var(--font-size-body-3); color: var(--td-strong);
        overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
      }
      .td-file--lg { width: 294px; height: 56px; padding: 0 12px; align-items: center; }
      .td-file--lg .td-file-body { display: flex; flex-direction: column; gap: 0; min-width: 0; }
      .td-file--lg .td-file-tx { font-size: var(--font-size-body-3); font-weight: 500; line-height: 22px; }
      .td-file-size { font-size: var(--font-size-body-1); line-height: 16px; color: var(--td-meta); }
      /* -------------------- 左栏右侧信息列 -------------------- */
      .td-side {
        flex: none; width: 240px; box-sizing: border-box; overflow: auto;
        padding: 20px 20px 32px 0; display: flex; flex-direction: column; gap: 24px;
      }
      .td-side h2 {
        margin: 0 0 16px; font-size: var(--font-size-body-3); font-weight: 500;
        color: var(--td-ink-2); line-height: 20px;
      }
      .td-attr { margin: 0; display: flex; flex-direction: column; gap: 16px; }
      .td-attr-row { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-3); }
      .td-attr-k { flex: none; color: var(--td-meta); }
      .td-attr-v { color: var(--td-strong); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .td-attr-link { display: inline-flex; align-items: center; gap: 4px; color: var(--td-strong); text-decoration: none; min-width: 0; }
      .td-attr-link svg { width: 14px; height: 14px; flex: none; color: var(--td-ink-2); }
      .td-tl { margin: 0; padding: 0; list-style: none; position: relative; }
      .td-tl::before {
        content: ''; position: absolute; left: 3px; top: 10px; bottom: 10px;
        width: 1px; background: var(--td-line);
      }
      .td-tl li { position: relative; padding: 0 0 16px 18px; }
      .td-tl li:last-child { padding-bottom: 0; }
      .td-tl li::before {
        content: ''; position: absolute; left: 0; top: 7px; width: 7px; height: 7px;
        border-radius: 50%; background: rgb(var(--gray-4)); box-sizing: border-box;
        border: 1px solid var(--color-bg-1);
      }
      .td-tl-line1 { display: flex; gap: 8px; font-size: var(--font-size-body-3); line-height: 20px; }
      .td-tl-who { color: var(--td-strong); flex: none; }
      .td-tl-what { color: var(--color-text-2); }
      .td-tl-time { display: block; margin-top: 2px; font-size: var(--font-size-body-1); line-height: 18px; color: var(--td-meta); }
      /* -------------------- 拖动条 -------------------- */
      .td-gutter {
        flex: none; width: var(--td-gap); position: relative; cursor: col-resize;
        display: flex; align-items: center; justify-content: center;
        background: transparent; border: none; padding: 0;
        transition: background-color 120ms var(--transition-timing-function-standard);
      }
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
      }
      .td-right-inner { flex: 1; min-height: 0; display: flex; flex-direction: column; }
      .td-right-bar {
        height: 64px; flex: none; box-sizing: border-box;
        display: flex; align-items: flex-start; gap: 8px; padding: 12px 20px 0;
      }
      .td-right-head { min-width: 0; flex: 1; }
      .td-right-title {
        font-size: var(--font-size-body-3); line-height: 24px; color: var(--td-strong);
        overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
      }
      .td-right-time { font-size: var(--font-size-body-1); line-height: 16px; color: var(--td-meta); }
      .td-right-acts { display: flex; align-items: center; gap: 8px; flex: none; }
      /* 适配层：DS Button(secondary + size-mini + icon) → 设计稿 24×24 / 无边 / radius 4 */
      .td-round-btn { box-sizing: border-box; width: 24px; padding: 0; border-color: transparent; line-height: 0; }
      .td-chat { flex: 1; min-height: 0; overflow: auto; padding: 16px 20px 8px; display: flex; flex-direction: column; gap: 16px; }
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
      .td-msg-ai p { margin: 0; font-size: var(--font-size-body-3); line-height: 24px; color: var(--color-text-2); }
      .td-ai-file {
        box-sizing: border-box; width: 281px; max-width: 100%; height: 56px;
        display: flex; align-items: center; gap: 8px; padding: 0 12px;
        background: var(--td-card); border-radius: var(--border-radius-large);
      }
      .td-ai-foot { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-body-3); color: var(--td-meta); }
      .td-ai-foot .td-sep { width: 1px; height: 12px; background: var(--color-border-2); }
      /* -------------------- 底部输入区 -------------------- */
      .td-composer {
        flex: none; box-sizing: border-box; margin: 8px 20px 20px; height: 112px;
        display: flex; flex-direction: column; padding: 12px;
        border: 1px solid var(--color-border-2); border-radius: var(--border-radius-large);
        background: var(--color-bg-1);
      }
      .td-composer:hover { border-color: var(--color-border-3); }
      .td-composer-input {
        flex: 1; min-height: 0; width: 100%; box-sizing: border-box;
        border: none; outline: none; resize: none; padding: 0; background: transparent;
        font-family: var(--font-family); font-size: var(--font-size-body-3);
        line-height: 22px; color: var(--td-strong);
      }
      .td-composer-input::placeholder { color: var(--color-text-3); }
      .td-composer-row { flex: none; height: 32px; display: flex; align-items: center; gap: 4px; }
      /* 适配层：DS Button(secondary + size-default) → 胶囊描边 / 设计稿 32 高 */
      .td-pill { box-sizing: border-box; height: 32px; gap: 4px; border-radius: 32px; color: var(--td-ink-2); }
      .td-pill svg { width: 14px; height: 14px; flex: none; }
      .td-composer-row .td-rightslot { margin-left: auto; }
      /* 适配层：DS Button(secondary + size-default + icon) → 设计稿 32×32 圆形 */
      .td-round {
        box-sizing: border-box; width: 32px; padding: 0; border-radius: 32px;
        color: var(--td-ink-2); line-height: 0;
      }
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
    </style>"""

# ============================== HTML ==============================
FILE_ICO = ('<svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" '
            'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M9 1.8H4.6a1.4 1.4 0 0 0-1.4 1.4v9.6a1.4 1.4 0 0 0 1.4 1.4h6.8a1.4 1.4 0 0 0 1.4-1.4V5.2z"/>'
            '<path d="M9 1.8v3.4h3.8"/></svg>')
LINK_ICO = ('<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" '
            'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M6.4 9.6a2.6 2.6 0 0 0 3.7 0l2-2a2.6 2.6 0 0 0-3.7-3.7l-1 1"/>'
            '<path d="M9.6 6.4a2.6 2.6 0 0 0-3.7 0l-2 2a2.6 2.6 0 0 0 3.7 3.7l1-1"/></svg>')


def fcard(name, size, big=False):
    cls = "td-file td-file--lg" if big else "td-file"
    if big:
        inner = ('<span class="td-file-body"><span class="td-file-tx">%s</span>'
                 '<span class="td-file-size">%s</span></span>' % (name, size))
    else:
        inner = '<span class="td-file-tx">%s</span>' % name
    return ('<div class="%s"><span class="td-file-ico">%s</span>%s</div>' % (cls, FILE_ICO, inner))


def tl(who, what, when):
    return ('<li><div class="td-tl-line1"><span class="td-tl-who">%s</span>'
            '<span class="td-tl-what">%s</span></div><span class="td-tl-time">%s</span></li>'
            % (who, what, when))


def attr(k, v):
    return ('<div class="td-attr-row"><span class="td-attr-k">%s</span>'
            '<span class="td-attr-v">%s</span></div>' % (k, v))


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
        <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn" type="button">转派</button>
        <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn" type="button">协作</button>
        <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn" type="button">编辑</button>
        <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn" type="button" aria-label="更多操作">
          <svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor"><circle cx="3.4" cy="8" r="1.3"/><circle cx="8" cy="8" r="1.3"/><circle cx="12.6" cy="8" r="1.3"/></svg>
        </button>
      </div>
    </header>
    <div class="td-left-body">
      <div class="td-main">
        <h1 class="td-title">端到端流程初始化：用户输入业务流程并触发全链路交付</h1>
        <div class="td-desc">
          <p>第二步：定义状态流转规则（启动整个流程）</p>
          <p>状态标识采用“交通灯”模式，方便直观管理：</p>
          <ul>
            <li>未开始：任务尚未启动。</li>
            <li>进行中：任务已启动，正在执行。</li>
            <li>已完成：任务成功完成并通过质量门禁。</li>
            <li>阻塞/异常：任务执行受阻，需要人工介入处理。</li>
          </ul>
          <div class="td-expand"><span class="td-expand-line"></span><button class="giencoder-btn giencoder-btn-text giencoder-btn-size-small td-expand-btn" type="button">展开全文</button><span class="td-expand-line"></span></div>
        </div>
        <section class="td-sec">
          <div class="td-sec-head">__LINKICO__2个附件</div>
          <div class="td-files">
            __ATT1__
            __ATT2__
          </div>
        </section>
        <section class="td-sec">
          <div class="td-sec-head">__LINKICO__3个 AI 产物</div>
          <div class="td-files">
            __AI1__
            __AI2__
            __AI3__
          </div>
        </section>
        <section class="td-sec">
          <div class="td-sec-head">__LINKICO__文件</div>
          <div class="td-files">
            __F1__
          </div>
        </section>
      </div>
      <aside class="td-side" aria-label="任务属性与动态">
        <section>
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
        <section>
          <h2>任务动态</h2>
          <ul class="td-tl">
            __T1__
            __T2__
            __T3__
            __T4__
            __T5__
          </ul>
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
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-mini giencoder-btn-icon td-round-btn" type="button" aria-label="历史会话"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M2.6 8a5.4 5.4 0 1 0 1.7-3.9"/><path d="M2.4 2.6v2.6h2.6"/><path d="M8 5.4V8l1.8 1.2"/></svg></button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-mini giencoder-btn-icon td-round-btn" type="button" aria-label="新建会话"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M8 3.4v9.2M3.4 8h9.2"/></svg></button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-mini giencoder-btn-icon td-round-btn" type="button" aria-label="更多"><svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><circle cx="3.6" cy="8" r="1.2"/><circle cx="8" cy="8" r="1.2"/><circle cx="12.4" cy="8" r="1.2"/></svg></button>
        </div>
      </header>
      <div class="td-chat">
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
          <div class="td-ai-file"><span class="td-file-ico">__FILEICO__</span><span class="td-file-body"><span class="td-file-tx">端到端初始化 - 任务分析报告.md</span><span class="td-file-size">128KB</span></span></div>
          <div class="td-ai-foot"><span>输出完成</span><span class="td-sep"></span><span>Token 速率：256/s</span></div>
        </div>
      </div>
      <div class="td-composer">
        <textarea class="td-composer-input" placeholder="提问、创建、搜索或@协作者" aria-label="输入消息"></textarea>
        <div class="td-composer-row">
          <button class="giencoder-btn giencoder-btn-secondary td-pill" type="button">__FILEICO__艾迪</button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round" type="button" aria-label="附件"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M10.6 5.4l-4.8 4.8a1.9 1.9 0 0 0 2.7 2.7l5-5a3.2 3.2 0 0 0-4.5-4.5l-5 5a4.5 4.5 0 0 0 6.4 6.4"/></svg></button>
          <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round" type="button" aria-label="更多设置"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><path d="M3 8h10M8 3v10"/></svg></button>
          <button class="giencoder-btn giencoder-btn-secondary td-pill td-rightslot" type="button">DeepSeek-V4-Pro<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M2.6 4.6L6 8l3.4-3.4"/></svg></button>
        </div>
      </div>
    </div>
    <button class="td-collapsed" type="button" aria-label="展开 AI 会话" data-td-expand="1">
      <span>展</span><span>开</span><span>AI</span><span>会</span><span>话</span>
    </button>
  </aside>
</div>"""

repl = {
    "__LINKICO__": LINK_ICO,
    "__FILEICO__": FILE_ICO,
    "__ATT1__": fcard("端到端流程初始化：用户输入业务流程并触发全链路交付.docx", ""),
    "__ATT2__": fcard("TaskBoard.png", ""),
    "__AI1__": fcard("prd-template.html", "128KB", True),
    "__AI2__": fcard("端到端初始化 - 任务分析报告.md", "128KB", True),
    "__AI3__": fcard("spec-template.md", "128KB", True),
    "__F1__": fcard("概要设计-Steps.md", "17KB", True),
    "__A1__": attr("状态", BADGE),
    "__A2__": attr("执行人", "邵禹铭"),
    "__A3__": attr("优先级", "高优先级"),
    "__A4__": attr("项目", "演练指挥系统"),
    "__A5__": attr("来源需求", '<a class="td-attr-link" href="#">GienX端到端初始化…%s</a>' % LINK_ICO),
    "__A6__": attr("实际开始", "2026/08/01 10:12"),
    "__A7__": attr("实际完成", "2026/08/12 15:27"),
    "__T1__": tl("Agent", "完成了任务开发", "刚刚"),
    "__T2__": tl("Agent", "已确认任务目标和优先级", "半小时前"),
    "__T3__": tl("邵禹铭", "状态更新为进行中", "昨天 10:02"),
    "__T4__": tl("邵禹铭", "补充了需求说明材料", "08/12 09:27"),
    "__T5__": tl("系统", "已同步最新处理进展", "08/11 16:51"),
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

    var gutter = wrap.querySelector('[data-td-gutter]');
    var right = wrap.querySelector('.td-right');
    if (!gutter || !right) return;

    var DEFAULT_W = 480;   /* 右栏默认宽（设计稿实测） */
    var MIN_W = 320;       /* 拖到此值以下，松手即自动折叠 */
    var COLLAPSED_W = 48;  /* 折叠条宽（设计稿实测） */
    var LEFT_MIN = 320;    /* 左栏保底 */
    var dragging = false, curW = DEFAULT_W;

    function setWidth(w) {
      curW = w;
      root.style.setProperty('--td-right-w', w + 'px');
      gutter.setAttribute('aria-valuenow', String(Math.round(w)));
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
      var box = root.getBoundingClientRect();
      var w = box.right - e.clientX;
      var maxW = box.width - LEFT_MIN;
      if (w > maxW) w = maxW;
      if (w < 0) w = 0;
      setWidth(Math.round(w));
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
    /* 键盘可达：← 变宽 / → 变窄（到阈值即折叠） */
    gutter.addEventListener('keydown', function (e) {
      var step = 24;
      var maxW = root.getBoundingClientRect().width - LEFT_MIN;
      if (e.key === 'ArrowLeft') { expand(Math.min(curW + step, maxW)); e.preventDefault(); }
      else if (e.key === 'ArrowRight') {
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
  }

  function inject() {
    var main = document.querySelector('main');
    if (!main || main.querySelector('.td-root')) return false;
    var wrap = document.createElement('div');
    wrap.className = 'td-wrap';
    wrap.innerHTML = KB_HTML;
    main.appendChild(wrap);
    bindDetail(wrap);
    return true;
  }
  if (!inject()) {
    var mo = new MutationObserver(function () { if (inject()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
</script>"""

lines = [l for l in HTML.split("\n")]
js_lines = ",\n".join('        ' + json.dumps(l, ensure_ascii=False) for l in lines)
JS = JS.replace("__LINES__", js_lines)

# ---- 尾部：主题同步 + 返回看板（替换原来的看板↔需求看板切换） ----
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
      /* 详情页：Esc 返回任务看板 */
      document.addEventListener('keydown', function (ev) {
        if (ev.key !== 'Escape') return;
        var tag = (ev.target && ev.target.tagName) || '';
        if (tag === 'TEXTAREA' || tag === 'INPUT') return;
        location.href = 'kanban.html';
      });
    </script>
  </body>
</html>
"""

out = head + mid + CSS + "\n" + JS + "\n" + TAIL
io.open(DST, "w", encoding="utf-8", newline="").write(out)
print("WROTE %s  %d chars (src %d)" % (DST, len(out), len(s)))
print("HTML lines:", len(lines))

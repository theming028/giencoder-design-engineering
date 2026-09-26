# -*- coding: utf-8 -*-
"""Round 15 / item 2 —— 按设计稿 875:13276 搭建「创建任务」弹窗。

设计稿基准（1440x900 画布 / 1280x820 面板，MasterGo file 193158744355579）：
  头部 48   ：标题 16/600 text-1 + 右侧 1x16 分隔线(#E5E5E5) + 28x28 关闭
  左列 880  ：任务类型 filled select 168x32 / 任务标题 input 880x40 r8 /
              富文本编辑器 880x320（工具条 36 高 fill-1 + 1px #F2F2F2 下边线）/ 附件 90
  右栏 320  ：任务属性条 320x40 #F5F6F7 + 6 行（label 80 + select 192x32，行距 12）
  页脚 56   ：取消 76 / 保存并继续创建 146 / 创建任务 104（secondary+primary，内边距 24）

组件一律使用 giencoder 契约类；kb-crt-* 仅做尺寸/位置视图适配。
"""
import io
import calendar

PATH = 'pages/kanban.html'

s = io.open(PATH, encoding='utf-8').read()
orig_len = len(s)


def esc(t):
    return t.replace('"', '\\"')


# ----------------------------------------------------------------- 复用片段
CARET = ('<svg class="giencoder-select-arrow" viewBox="0 0 12 12" width="12" height="12" fill="none" '
         'stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M2 4l4 4 4-4"/></svg>')
CLEAR = ('<button class="giencoder-select-clear" type="button" aria-label="清除选择">'
         '<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" '
         'stroke-width="1.4" stroke-linecap="round"><path d="M3 3l6 6M9 3l-6 6"/></svg></button>')
TB_CARET = ('<svg class="kb-crt-tbcaret" viewBox="0 0 10 10" width="10" height="10" fill="none" '
            'stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><path d="M1.6 3.4L5 6.8l3.4-3.4"/></svg>')


def select_field(extra_cls, label, placeholder, options, selected=None):
    """契约结构的选择器 + 可选右侧 label。"""
    opts = []
    for o in options:
        sel = ' giencoder-select-option-selected' if o == selected else ''
        aria = 'true' if o == selected else 'false'
        opts.append('<li class="giencoder-select-option%s" role="option" aria-selected="%s">%s</li>'
                    % (sel, aria, o))
    cls = 'giencoder-select ' + extra_cls
    if selected is None and extra_cls.startswith('kb-crt-fld'):
        cls += ' kb-crt-ph'
    has = ' giencoder-select-has-value' if selected else ''
    lbl = ('<span class="kb-crt-lbl">%s</span>' % label) if label is not None else ''
    val = selected if selected else placeholder
    return (
        '<div class="%s%s" data-component="select" data-variant="single" data-state="default">'
        '<div class="giencoder-select-view" tabindex="0" role="combobox" aria-expanded="false" aria-haspopup="listbox">'
        '%s'
        '<span class="giencoder-select-view-text" data-placeholder="%s">%s</span>'
        '<span class="giencoder-select-suffix">%s%s</span>'
        '</div>'
        '<div class="giencoder-select-popup" style="display:none;">'
        '<ul class="giencoder-select-option-list" role="listbox">%s</ul>'
        '</div></div>'
    ) % (cls, has, lbl, placeholder, val, CARET, CLEAR, ''.join(opts))


def disabled_select(label, value):
    return (
        '<div class="giencoder-select kb-crt-fld giencoder-select-disabled" data-component="select" '
        'data-variant="single" data-state="disabled">'
        '<div class="giencoder-select-view" role="combobox" aria-expanded="false" aria-haspopup="listbox" aria-disabled="true">'
        '<span class="kb-crt-lbl">%s</span>'
        '<span class="giencoder-select-view-text">%s</span>'
        '</div></div>'
    ) % (label, value)


def month_grid(year, month):
    """生成 6x7 日历格，跨月用 giencoder-calendar-cell-other。"""
    first_wd = (calendar.weekday(year, month, 1) + 1) % 7  # 周日=0
    days = calendar.monthrange(year, month)[1]
    prev_m = month - 1 if month > 1 else 12
    prev_y = year if month > 1 else year - 1
    prev_days = calendar.monthrange(prev_y, prev_m)[1]
    cells = []
    for i in range(first_wd):
        cells.append(('other', prev_days - first_wd + 1 + i))
    for d in range(1, days + 1):
        cells.append(('cur', d))
    nxt = 1
    while len(cells) < 42:
        cells.append(('other', nxt))
        nxt += 1
    out = []
    for kind, d in cells:
        cls = 'giencoder-calendar-cell' + ('' if kind == 'cur' else ' giencoder-calendar-cell-other')
        out.append('<span class="%s">%d</span>' % (cls, d))
    return ''.join(out)


def calendar_panel(year, month):
    return (
        '<div class="giencoder-calendar">'
        '<div class="giencoder-calendar-header">'
        '<button class="giencoder-calendar-nav" type="button" aria-label="上个月">'
        '<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" '
        'stroke-width="1.5" stroke-linecap="round"><path d="M7.5 2l-4 4 4 4"/></svg></button>'
        '<span class="giencoder-calendar-title">%d年%d月</span>'
        '<button class="giencoder-calendar-nav" type="button" aria-label="下个月">'
        '<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" '
        'stroke-width="1.5" stroke-linecap="round"><path d="M4.5 2l4 4-4 4"/></svg></button>'
        '</div>'
        '<div class="giencoder-calendar-weekdays"><span>日</span><span>一</span><span>二</span>'
        '<span>三</span><span>四</span><span>五</span><span>六</span></div>'
        '<div class="giencoder-calendar-grid">%s</div>'
        '</div>'
    ) % (year, month, month_grid(year, month))


# ----------------------------------------------------------------- 工具栏
def tb(left, width, inner, cls='kb-crt-tb', attrs=''):
    return ('<button class="%s" type="button" style="left:%dpx;width:%dpx"%s>%s</button>'
            % (cls, left, width, attrs, inner))


TB_GLYPH = '<span class="kb-crt-glyph">%s</span>'
TOOLBAR_ITEMS = [
    # 标题3 ▾
    tb(12, 41, '<span class="kb-crt-tb-title">标题3</span>' + TB_CARET, 'kb-crt-tb kb-crt-tb--sel'),
    # 单独的浅色 ▾（设计稿中的空态下拉）
    tb(104, 12, TB_CARET, 'kb-crt-tb kb-crt-tb--lone'),
    # B（设计稿为禁用态）
    tb(122, 28, TB_GLYPH % 'B', 'kb-crt-tb kb-crt-tb--b', ' disabled aria-label="加粗"'),
    tb(150, 28, TB_GLYPH % 'I', 'kb-crt-tb kb-crt-tb--i', ' aria-label="斜体"'),
    tb(177, 28, TB_GLYPH % 'S', 'kb-crt-tb kb-crt-tb--s', ' aria-label="删除线"'),
    tb(204, 28, TB_GLYPH % 'U', 'kb-crt-tb kb-crt-tb--u', ' aria-label="下划线"'),
    tb(241, 28, TB_GLYPH % 'T' + TB_CARET, 'kb-crt-tb kb-crt-tb--t', ' aria-label="清除格式"'),
    # 分隔线
    ('<span class="kb-crt-tbsep" style="left:277px"></span>'),
    tb(289, 28, TB_GLYPH % 'A' + TB_CARET, 'kb-crt-tb kb-crt-tb--a', ' aria-label="文字颜色"'),
    tb(329, 28,
       '<span class="kb-crt-tbico"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" '
       'stroke="currentColor" stroke-width="1.3" stroke-linejoin="round">'
       '<path d="M9.4 2.2l4.4 4.4-6.2 6.2H3.2v-4.4z"/><path d="M8 3.6l4.4 4.4" stroke-width="1.1"/>'
       '<path d="M2 13.6h8" stroke-width="1.6"/></svg></span>' + TB_CARET,
       'kb-crt-tb kb-crt-tb--hl', ' aria-label="高亮"'),
    ('<span class="kb-crt-tbsep" style="left:366px"></span>'),
    tb(379, 28,
       '<span class="kb-crt-tbico"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" '
       'stroke="currentColor" stroke-width="1.4" stroke-linecap="round">'
       '<path d="M2.4 3.6h11.2M2.4 8h7.4M2.4 12.4h11.2"/></svg></span>' + TB_CARET,
       'kb-crt-tb kb-crt-tb--align', ' aria-label="对齐"'),
    tb(410, 28,
       '<span class="kb-crt-tbico"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" '
       'stroke="currentColor" stroke-width="1.4" stroke-linecap="round">'
       '<path d="M5.6 4h8.4M5.6 8h8.4M5.6 12h8.4"/><circle cx="2.6" cy="4" r=".95" fill="currentColor" stroke="none"/>'
       '<circle cx="2.6" cy="8" r=".95" fill="currentColor" stroke="none"/>'
       '<circle cx="2.6" cy="12" r=".95" fill="currentColor" stroke="none"/></svg></span>',
       'kb-crt-tb kb-crt-tb--ul', ' aria-label="无序列表"'),
    tb(433, 28,
       '<span class="kb-crt-tbico"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" '
       'stroke="currentColor" stroke-width="1.4" stroke-linecap="round">'
       '<path d="M6.4 4h7.6M6.4 8h7.6M6.4 12h7.6"/><text x="1.2" y="5.6" font-size="5" fill="currentColor" '
       'stroke="none" font-family="Arial, sans-serif">1</text>'
       '<text x="1.2" y="9.9" font-size="5" fill="currentColor" stroke="none" font-family="Arial, sans-serif">2</text>'
       '<text x="1.2" y="14.2" font-size="5" fill="currentColor" stroke="none" font-family="Arial, sans-serif">3</text>'
       '</svg></span>',
       'kb-crt-tb kb-crt-tb--ol', ' aria-label="有序列表"'),
    # 插入图片（设计稿独立在图标条右侧）
    tb(464, 28,
       '<span class="kb-crt-tbico"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" '
       'stroke="currentColor" stroke-width="1.2" stroke-linejoin="round">'
       '<rect x="1.6" y="2.6" width="12.8" height="10.8" rx="1.6"/>'
       '<circle cx="5.4" cy="6.2" r="1.1"/>'
       '<path d="M2.4 11.4l3.6-3.2 3 2.6 2-1.8 2.6 2.4"/></svg></span>',
       'kb-crt-tb kb-crt-tb--img', ' aria-label="插入图片"'),
]

TOOLBAR = '<div class="kb-crt-toolbar" role="toolbar" aria-label="编辑器工具栏">%s</div>' % ''.join(TOOLBAR_ITEMS)

# ----------------------------------------------------------------- 弹窗标记
PLACEHOLDER_L1 = u'你可以通过用户故事的形式描述任务。'
PLACEHOLDER_L2 = u'基本格式：作为某个角色，我需要做某些事情，以便实现什么目标。'

HTML = u'''
<!-- r15: 创建任务弹窗（设计稿 875:13276；1280x820 面板，组件走 giencoder 契约类 + kb-crt- 视图适配） -->
<div class="kb-crt" hidden>
  <div class="giencoder-modal-mask kb-crt-mask" data-crt-close="1"></div>
  <div class="giencoder-modal kb-crt-dialog" role="dialog" aria-modal="true" tabindex="-1" aria-label="创建工作任务">
    <div class="giencoder-modal-header kb-crt-head">
      <div class="giencoder-modal-title">创建工作任务</div>
      <div class="kb-crt-head-act">
        <span class="kb-crt-head-line"></span>
        <button class="giencoder-modal-close-btn kb-crt-close" type="button" aria-label="Close" data-crt-close="1">
          <svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M4.2 4.2l7.6 7.6M11.8 4.2l-7.6 7.6"/></svg>
        </button>
      </div>
    </div>
    <div class="giencoder-modal-content kb-crt-body">
      <div class="kb-crt-main">
        __TYPE__
        <div class="giencoder-input-wrapper kb-crt-title" data-component="input" data-variant="default" data-size="large" data-state="default">
          <input class="giencoder-input" placeholder="请输入任务标题" aria-label="任务标题">
        </div>
        <div class="kb-crt-editor">
          __TOOLBAR__
          <div class="kb-crt-editor-body">
            <div class="kb-crt-editor-ph"><span>__PH1__</span><span>__PH2__</span></div>
          </div>
        </div>
        <div class="kb-crt-attach">
          <div class="kb-crt-attach-lbl">附件</div>
          <div class="giencoder-upload kb-crt-upload" data-component="upload" data-variant="click" data-state="default">
            <input class="kb-crt-file" type="file" multiple hidden aria-hidden="true">
            <button class="giencoder-btn giencoder-btn-size-default kb-crt-upbtn" type="button">
              <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M8 12V2.6M4.6 6L8 2.6 11.4 6"/><path d="M2.2 13.4h11.6"/></svg>
              上传文件
            </button>
            <div class="giencoder-upload-tip kb-crt-uptip">支持最多上传5个文件，单个文件不超过10MB</div>
            <ul class="giencoder-upload-list kb-crt-uplist" hidden></ul>
          </div>
        </div>
      </div>
      <aside class="kb-crt-aside" aria-label="任务属性">
        <div class="kb-crt-aside-head">任务属性</div>
        <div class="kb-crt-aside-body">
          __ROWS__
        </div>
      </aside>
    </div>
    <div class="giencoder-modal-footer kb-crt-foot">
      <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default kb-crt-btn" type="button" data-crt-close="1">取消</button>
      <button class="giencoder-btn giencoder-btn-secondary giencoder-btn-size-default kb-crt-btn" type="button" data-crt-keep="1">保存并继续创建</button>
      <button class="giencoder-btn giencoder-btn-primary giencoder-btn-size-default kb-crt-btn" type="button" data-crt-submit="1">创建任务</button>
    </div>
    <div class="kb-crt-msgs" hidden>
      <div class="giencoder-message kb-crt-msg" data-component="message" data-variant="error" data-state="default" role="alert" data-err="type" hidden>
        <span class="kb-crt-msg-ico"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="8" cy="8" r="6.5"/><path d="M5.6 5.6l4.8 4.8M10.4 5.6l-4.8 4.8"/></svg></span>
        <span class="kb-crt-msg-tx">「任务类型」不能为空</span>
      </div>
      <div class="giencoder-message kb-crt-msg" data-component="message" data-variant="error" data-state="default" role="alert" data-err="title" hidden>
        <span class="kb-crt-msg-ico"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="8" cy="8" r="6.5"/><path d="M5.6 5.6l4.8 4.8M10.4 5.6l-4.8 4.8"/></svg></span>
        <span class="kb-crt-msg-tx">「任务标题」不能为空</span>
      </div>
    </div>
  </div>
</div>
'''

TYPE_SELECT = u'''<div class="giencoder-select kb-crt-type" data-component="select" data-variant="single" data-state="default">
          <div class="giencoder-select-view" tabindex="0" role="combobox" aria-expanded="false" aria-haspopup="listbox">
            <span class="kb-crt-type-lbl">任务类型<i class="kb-crt-req" aria-hidden="true">*</i></span>
            <span class="giencoder-select-view-text" data-placeholder="请选择">请选择</span>
            <span class="giencoder-select-suffix">__CARET____CLEAR__</span>
          </div>
          <div class="giencoder-select-popup" style="display:none;">
            <ul class="giencoder-select-option-list" role="listbox">
              <li class="giencoder-select-option" role="option" aria-selected="false">拆分需求项</li>
              <li class="giencoder-select-option" role="option" aria-selected="false">拆分需求条目</li>
              <li class="giencoder-select-option" role="option" aria-selected="false">拆分子条目</li>
              <li class="giencoder-select-option" role="option" aria-selected="false">技术调研</li>
              <li class="giencoder-select-option" role="option" aria-selected="false">缺陷修复</li>
            </ul>
          </div>
        </div>'''.replace('__CARET__', CARET).replace('__CLEAR__', CLEAR)

ROWS = u''.join([
    u'<div class="kb-crt-row">',
    select_field('kb-crt-fld', u'状态', u'请选择', [u'待开始', u'进行中', u'已终止', u'已完成']),
    u'</div>',
    u'<div class="kb-crt-row">',
    select_field('kb-crt-fld', u'优先级', u'请选择', [u'高', u'中', u'低']),
    u'</div>',
    u'<div class="kb-crt-row">',
    select_field('kb-crt-fld', u'关联需求', u'请选择', [u'端到端流程初始化：用户输入业务需求…', u'读取业务方原始需求文档', u'生成结构化的 PRD 产品需求文档']),
    u'</div>',
    u'<div class="kb-crt-row">', disabled_select(u'前置任务', u'-'), u'</div>',
    u'<div class="kb-crt-row">',
    select_field('kb-crt-fld', u'责任人', u'请选择', [u'邵禹铭', u'张一鸣', u'李明轩', u'王思远']),
    u'</div>',
    u'''<div class="kb-crt-row"><span class="kb-crt-lbl">预期完成</span>
            <div class="giencoder-date-picker kb-crt-fld kb-crt-date" data-component="date-picker" data-variant="default" data-state="default">
              <div class="giencoder-input-wrapper" role="combobox" aria-expanded="false" tabindex="0">
                <input class="giencoder-input kb-crt-date-input" placeholder="选择日期" readonly aria-label="预期完成">
                <span class="giencoder-input-suffix"><svg viewBox="0 0 14 14" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="1.8" y="2.6" width="10.4" height="9.6" rx="1.6"/><path d="M1.8 5.6h10.4M4.8 1.4v2.4M9.2 1.4v2.4" stroke-linecap="round"/></svg></span>
              </div>
              <div class="giencoder-date-picker-popup" style="display:none;">
                <div class="giencoder-date-picker-panels">''' + calendar_panel(2026, 8) + u'''</div>
              </div>
            </div>
          </div>''',
])

markup = (HTML
          .replace('__TYPE__', TYPE_SELECT)
          .replace('__TOOLBAR__', TOOLBAR)
          .replace('__PH1__', PLACEHOLDER_L1)
          .replace('__PH2__', PLACEHOLDER_L2)
          .replace('__ROWS__', ROWS))

# ----------------------------------------------------------------- CSS
CSS = u'''      /* r15-create-modal-css */
      /* ===== r15: 创建任务弹窗 —— 设计稿 875:13276（1440x900 画布上的 1280x820 面板）。
         组件全部走 giencoder 契约类；kb-crt-* 只承担「设计稿尺寸/位置」的视图适配。
         设计稿中 DS 无对应 token 的色值集中声明为局部变量（来源见注释）。 */
      .kb-crt {
        --kb-crt-divider: #EBECED;      /* 页脚/右栏/标题条 1px 描边：svg_40e9e0d1 / svg_96228d69 / svg_db31979c */
        --kb-crt-aside-bar: #F5F6F7;    /* 任务属性标题条底色：svg_db31979c */
        --kb-crt-mask: rgba(0, 0, 0, 0.32);   /* 遮罩：svg_8e860390（#000 32% + backdrop blur 5px） */
        position: absolute; inset: 0; z-index: 60;
        display: flex; align-items: center; justify-content: center;
      }
      .kb-crt[hidden] { display: none; }
      .kb-crt-mask {
        position: absolute; inset: 0; background: var(--kb-crt-mask);
        -webkit-backdrop-filter: blur(5px); backdrop-filter: blur(5px);
        opacity: 0; transition: opacity 150ms var(--transition-timing-function-standard);
      }
      .kb-crt.is-open .kb-crt-mask { opacity: 1; }
      .kb-crt-dialog {
        position: relative; z-index: 1;
        width: min(1280px, calc(100% - 64px)); height: min(820px, calc(100% - 48px));
        display: flex; flex-direction: column;
        background: var(--color-bg-1); border-radius: var(--border-radius-xl);
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
        opacity: 0; transform-origin: top center;
        transform: translateY(-12px) scaleY(0.97);
        transition: opacity 130ms var(--transition-timing-function-standard),
                    transform 160ms var(--transition-timing-function-standard);
        will-change: transform, opacity;
      }
      .kb-crt.is-open .kb-crt-dialog { opacity: 1; transform: translateY(0) scaleY(1); }
      @media (prefers-reduced-motion: reduce) {
        .kb-crt-dialog, .kb-crt-mask { transition-duration: 1ms; }
      }
      /* --- 头部 48 高、左右 24（DS 默认 52 / 20），下边线 #E5E5E5 --- */
      .kb-crt-head { height: 48px; padding: 0 24px; border-bottom-color: var(--color-border-2); }
      .kb-crt-head-act { display: flex; align-items: center; gap: 11px; }
      .kb-crt-head-line { width: 1px; height: 16px; background: var(--color-border-2); flex: none; }
      .kb-crt-close { width: 28px; height: 28px; padding: 0; align-items: center; justify-content: center; }
      /* --- 主体：左列自适应 + 右栏 320 --- */
      .kb-crt-body { flex: 1; min-height: 0; display: flex; padding: 0; overflow: hidden; }
      .kb-crt-main {
        flex: 1; min-width: 0; display: flex; flex-direction: column;
        padding: 24px 40px 0; overflow: hidden;
      }
      /* 任务类型：设计稿为「填充」单选（fill-1 底、无描边、无投影，标签内联在值前） */
      .kb-crt-type { width: 168px; flex: none; }
      .kb-crt-type .giencoder-select-view { background: var(--color-fill-1); border-color: transparent; box-shadow: none; }
      .kb-crt-type .giencoder-select-view:hover { background: var(--color-fill-2); border-color: transparent; }
      .kb-crt-type .giencoder-select-view:active { background: var(--color-fill-2); }
      .kb-crt-type .giencoder-select-view[aria-expanded="true"] { background: var(--color-bg-2); border-color: var(--color-primary-6); }
      .kb-crt-type-lbl {
        color: var(--color-text-1); white-space: nowrap; flex: none;
        display: inline-flex; align-items: center; gap: 4px;
      }
      .kb-crt-req { color: var(--color-danger-6); font-style: normal; }
      /* 占位值灰色，选中后转正文色（绑定脚本会补 giencoder-select-has-value） */
      .kb-crt-type .giencoder-select-view-text,
      .kb-crt-fld .giencoder-select-view-text { color: rgb(var(--gray-5)); }
      .kb-crt-type.giencoder-select-has-value .giencoder-select-view-text,
      .kb-crt-fld.giencoder-select-has-value .giencoder-select-view-text { color: var(--color-text-1); }
      .kb-crt-type + .kb-crt-title { margin-top: 16px; }
      /* 任务标题：设计稿 880x40、圆角 8（DS 中为 36x4） */
      .kb-crt-title {
        width: 100%; max-width: 880px; height: 40px; flex: none;
        border-radius: var(--border-radius-large); padding: 0 12px;
      }
      .kb-crt-title .giencoder-input { color: var(--color-text-1); }
      .kb-crt-title .giencoder-input::placeholder { color: var(--color-text-3); }
      /* 富文本编辑器：设计稿 880x320，1px #F2F2F2 + 圆角 8；高度可随窗口收缩 */
      .kb-crt-editor {
        margin-top: 20px; width: 100%; max-width: 880px;
        flex: 1 1 320px; min-height: 140px;
        display: flex; flex-direction: column;
        border: 1px solid var(--color-border-1); border-radius: var(--border-radius-large);
        background: var(--color-bg-1); overflow: hidden;
      }
      .kb-crt-toolbar {
        position: relative; height: 36px; flex: none; box-sizing: border-box;
        background: var(--color-fill-1); border-bottom: 1px solid var(--color-border-1);
      }
      .kb-crt-tb {
        position: absolute; top: 4px; height: 28px; padding: 0;
        display: inline-flex; align-items: center; justify-content: center; gap: 2px;
        border: none; background: none; cursor: pointer; border-radius: var(--border-radius-medium);
        color: var(--color-text-1); font-size: var(--font-size-body-3); font-family: var(--font-family);
      }
      .kb-crt-tb:hover:not([disabled]) { background: var(--color-fill-2); }
      .kb-crt-tb[disabled] { color: rgb(var(--gray-4)); cursor: default; }
      .kb-crt-tb--lone { color: rgb(var(--gray-4)); }
      .kb-crt-tb--sel { padding: 0 4px; justify-content: space-between; }
      .kb-crt-tb-title { white-space: nowrap; }
      .kb-crt-tbcaret { color: rgb(var(--gray-6)); flex: none; }
      .kb-crt-tb--lone .kb-crt-tbcaret { color: inherit; }
      .kb-crt-glyph { font-family: Georgia, 'Times New Roman', serif; font-size: 15px; line-height: 1; }
      .kb-crt-tb--b .kb-crt-glyph { font-weight: 700; }
      .kb-crt-tb--i .kb-crt-glyph { font-style: italic; font-weight: 700; }
      .kb-crt-tb--s .kb-crt-glyph { text-decoration: line-through; }
      .kb-crt-tb--u .kb-crt-glyph { text-decoration: underline; text-underline-offset: 1px; }
      .kb-crt-tb--t .kb-crt-glyph { text-decoration: line-through; }
      .kb-crt-tb--a .kb-crt-glyph {
        font-family: var(--font-family); font-weight: 600;
        box-shadow: 0 2px 0 0 var(--color-danger-6);
      }
      .kb-crt-tb--hl .kb-crt-tbico { box-shadow: 0 2px 0 0 var(--color-warning-6); }
      .kb-crt-tbico { display: inline-flex; align-items: center; }
      .kb-crt-tbsep { position: absolute; top: 10px; width: 1px; height: 16px; background: var(--color-border-1); }
      .kb-crt-editor-body { flex: 1; min-height: 0; padding: 16px; overflow: auto; }
      .kb-crt-editor-ph { display: flex; flex-direction: column; font-size: var(--font-size-body-3); line-height: 24px; color: rgb(var(--gray-5)); }
      /* 附件：label 22 + 8 + 按钮 32 + 8 + 提示 20 = 90（设计稿容器 6） */
      .kb-crt-attach { margin-top: 20px; flex: none; padding-bottom: 24px; }
      .kb-crt-attach-lbl { font-size: var(--font-size-body-3); line-height: 22px; color: rgb(var(--gray-7)); }
      .kb-crt-upload { margin-top: 8px; }
      .kb-crt-upbtn {
        gap: 4px; padding: 0 16px; font-weight: 400;
        background: var(--color-fill-1); color: var(--color-text-1);
        border-color: transparent; box-shadow: none;
      }
      .kb-crt-upbtn:hover { background: var(--color-fill-2); border-color: transparent; box-shadow: none; }
      .kb-crt-upbtn:active { background: var(--color-fill-2); border-color: transparent; box-shadow: none; }
      .kb-crt-uptip { margin-top: 8px; font-size: var(--font-size-body-1); line-height: 20px; color: var(--color-text-3); }
      .kb-crt-uplist { margin: 8px 0 0; padding: 0; list-style: none; }
      .kb-crt-upitem { display: flex; align-items: center; gap: 8px; height: 28px; font-size: var(--font-size-body-1); color: var(--color-text-2); }
      .kb-crt-uprm { border: none; background: none; cursor: pointer; color: var(--color-text-3); padding: 0; line-height: 0; }
      .kb-crt-uprm:hover { color: var(--color-text-1); }
      /* --- 右栏：320 宽，左描边 #EBECED --- */
      .kb-crt-aside {
        width: 320px; flex: none; display: flex; flex-direction: column;
        border-left: 1px solid var(--kb-crt-divider);
      }
      .kb-crt-aside-head {
        height: 40px; flex: none; display: flex; align-items: center; padding: 0 24px;
        background: var(--kb-crt-aside-bar); border-bottom: 1px solid var(--kb-crt-divider);
        font-size: var(--font-size-body-3); color: var(--color-text-1);
      }
      .kb-crt-aside-body { padding: 24px; display: flex; flex-direction: column; gap: 12px; }
      .kb-crt-row { display: flex; align-items: center; }
      .kb-crt-lbl { width: 80px; flex: none; font-size: var(--font-size-body-3); color: var(--color-text-1); }
      .kb-crt-fld { width: 192px; flex: none; }
      .kb-crt-date, .kb-crt-date .giencoder-input-wrapper { width: 192px; min-width: 192px; }
      .kb-crt-date .kb-crt-date-input { color: var(--color-text-1); }
      .kb-crt-date .kb-crt-date-input::placeholder { color: rgb(var(--gray-5)); }
      .kb-crt-date .giencoder-date-picker-popup { left: auto; right: 0; }
      /* --- 页脚 56 高、左右 24、按钮内边距 24（设计稿 76/146/104） --- */
      .kb-crt-foot { height: 56px; flex: none; padding: 0 24px; border-top-color: var(--kb-crt-divider); }
      .kb-crt-btn { padding: 0 24px; }
      /* --- 校验错误：贴头部下方居中（设计稿 2 条 Message） --- */
      .kb-crt-msgs {
        position: absolute; top: 17px; left: 50%; transform: translateX(-50%);
        display: flex; gap: 12px; z-index: 2;
      }
      .kb-crt-msgs[hidden] { display: none; }
      .kb-crt-msg {
        display: flex; align-items: center; gap: 8px; height: 32px; padding: 0 16px;
        background: var(--color-bg-2); border-radius: var(--border-radius-medium);
        box-shadow: var(--shadow2-down); font-size: var(--font-size-body-3); white-space: nowrap;
      }
      .kb-crt-msg[hidden] { display: none; }
      .kb-crt-msg-ico { display: inline-flex; color: var(--color-danger-6); }
      .kb-crt-msg-tx { color: var(--color-danger-6); }
'''

# ----------------------------------------------------------------- 注入 CSS
css_anchor = (u'      @media (prefers-reduced-motion: reduce) {\n'
              u'        .kb-coop-dialog, .kb-coop-mask { transition-duration: 1ms; }\n'
              u'      }\n')
assert css_anchor in s, 'css anchor missing'
s = s.replace(css_anchor, css_anchor + CSS, 1)

# ----------------------------------------------------------------- 注入 HTML
ARR_END = u"].join('\\n');"
i = s.find(ARR_END)
assert i > 0, 'KB_HTML join anchor missing'
head = s[:i]
assert head.endswith(u'"        </div>"'), 'unexpected array tail: %r' % head[-40:]
lines = markup.strip(u'\n').split(u'\n')
block = u',\n'.join([u'        "%s"' % esc(l) for l in lines])
s = head + u',\n' + block + s[i:]

# ----------------------------------------------------------------- 注入 JS
JS_CALL_ANCHOR = u'    bindCoopModal(wrap);\n'
assert JS_CALL_ANCHOR in s, 'js call anchor missing'
s = s.replace(JS_CALL_ANCHOR, JS_CALL_ANCHOR + u'    bindCreateModal(wrap);\n', 1)

JS_FN = u'''  /* ===== r15: 创建任务弹窗（设计稿 875:13276）===== */
  function bindCreateModal(root) {
    var modal = root.querySelector('.kb-crt');
    var trigger = root.querySelector('.kb-create');
    if (!modal || !trigger) return;
    /* 面板只覆盖 main —— 与待协作模态同样把节点提到 <main> 下，绝对定位基准才正确 */
    var host = document.querySelector('main');
    if (host) {
      host.classList.add('kb-main-rel');
      if (modal.parentElement !== host) host.appendChild(modal);
    }
    var closeTimer = null;
    var typeSel = modal.querySelector('.kb-crt-type');
    var titleWrap = modal.querySelector('.kb-crt-title');
    var titleInput = titleWrap ? titleWrap.querySelector('.giencoder-input') : null;
    var msgs = modal.querySelector('.kb-crt-msgs');
    var list = modal.querySelector('.kb-crt-uplist');

    function resetPopups() {
      modal.querySelectorAll('.giencoder-select-popup, .giencoder-date-picker-popup').forEach(function (p) {
        p.classList.remove('giencoder-popup-open', 'giencoder-panel-open');
        p.style.display = 'none';
      });
    }
    function setErr(name, on) {
      if (msgs) {
        var m = msgs.querySelector('[data-err="' + name + '"]');
        if (m) m.hidden = !on;
        msgs.hidden = !msgs.querySelector('.giencoder-message:not([hidden])');
      }
      if (name === 'type' && typeSel) typeSel.classList.toggle('kb-crt-err', on);
      if (name === 'title' && titleWrap) titleWrap.classList.toggle('giencoder-input-error', on);
    }
    function clearErrs() { setErr('type', false); setErr('title', false); }
    function open() {
      if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }
      resetPopups();
      clearErrs();
      modal.hidden = false;
      void modal.offsetWidth; /* 让 display 生效并落定初始样式，再加类才会有过渡 */
      modal.classList.add('is-open');
      document.documentElement.classList.add('kb-coop-lock');
      var dlg = modal.querySelector('.kb-crt-dialog');
      if (dlg) dlg.focus({ preventScroll: true });
      if (titleInput) setTimeout(function () { try { titleInput.focus(); } catch (e) {} }, 190);
    }
    function close() {
      resetPopups();
      modal.classList.remove('is-open');
      document.documentElement.classList.remove('kb-coop-lock');
      if (closeTimer) clearTimeout(closeTimer);
      closeTimer = setTimeout(function () { closeTimer = null; modal.hidden = true; }, 190);
    }
    function valueOf(sel) {
      var t = modal.querySelector(sel + ' .giencoder-select-view-text');
      return t ? t.textContent.trim() : '';
    }
    function resetFields() {
      modal.querySelectorAll('.kb-crt-type, .kb-crt-fld').forEach(function (sel) {
        if (sel.classList.contains('giencoder-select-disabled')) return;
        sel.classList.remove('giencoder-select-has-value');
        var t = sel.querySelector('.giencoder-select-view-text');
        if (t) t.textContent = t.getAttribute('data-placeholder') || t.textContent;
        sel.querySelectorAll('.giencoder-select-option-selected').forEach(function (o) {
          o.classList.remove('giencoder-select-option-selected');
          o.setAttribute('aria-selected', 'false');
        });
      });
      if (titleInput) titleInput.value = '';
      var dv = modal.querySelector('.kb-crt-date-input');
      if (dv) dv.value = '';
      modal.querySelectorAll('.kb-crt-editor-body .giencoder-calendar-cell-selected').forEach(function (c) {
        c.classList.remove('giencoder-calendar-cell-selected');
      });
      if (list) { list.innerHTML = ''; list.hidden = true; }
    }
    function submit(keepOpen) {
      var okType = !!valueOf('.kb-crt-type') && valueOf('.kb-crt-type') !== '请选择';
      var okTitle = !!(titleInput && titleInput.value.trim());
      setErr('type', !okType);
      setErr('title', !okTitle);
      if (!okType || !okTitle) return false;
      if (keepOpen) { resetFields(); if (typeSel) typeSel.focus(); }
      else { close(); }
      return true;
    }

    trigger.addEventListener('click', open);
    trigger.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });
    modal.addEventListener('click', function (e) {
      var t = e.target;
      if (t && t.closest && t.closest('[data-crt-close]')) { close(); return; }
      if (t && t.closest && t.closest('.giencoder-select-option')) setErr('type', false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !modal.hidden) close();
    });
    /* 上传：按钮唤起文件选择，选中后列出文件名 */
    var upBtn = modal.querySelector('.kb-crt-upbtn');
    var fileInput = modal.querySelector('.kb-crt-file');
    if (upBtn && fileInput) {
      upBtn.addEventListener('click', function (e) { e.stopPropagation(); fileInput.click(); });
      fileInput.addEventListener('change', function () {
        if (!list) return;
        var fs = fileInput.files || [];
        for (var i = 0; i < fs.length; i++) {
          var li = document.createElement('li');
          li.className = 'giencoder-upload-list-item kb-crt-upitem';
          var nm = document.createElement('span');
          nm.className = 'giencoder-upload-file-name';
          nm.textContent = fs[i].name;
          li.appendChild(nm);
          var rm = document.createElement('button');
          rm.type = 'button';
          rm.className = 'giencoder-upload-remove kb-crt-uprm';
          rm.setAttribute('aria-label', '移除');
          rm.textContent = 'x';
          li.appendChild(rm);
          list.appendChild(li);
        }
        list.hidden = !fs.length;
      });
      if (list) {
        list.addEventListener('click', function (e) {
          var rm = e.target.closest ? e.target.closest('.kb-crt-uprm') : null;
          if (!rm) return;
          var li = rm.closest('li');
          if (li) li.remove();
          if (!list.children.length) list.hidden = true;
        });
      }
    }
    /* 输入即清错 */
    if (titleInput) {
      titleInput.addEventListener('input', function () {
        if (titleInput.value.trim()) setErr('title', false);
      });
    }
    var btnSubmit = modal.querySelector('[data-crt-submit]');
    var btnKeep = modal.querySelector('[data-crt-keep]');
    if (btnSubmit) btnSubmit.addEventListener('click', function () { submit(false); });
    if (btnKeep) btnKeep.addEventListener('click', function () { submit(true); });
  }
'''

JS_ANCHOR = u'  function bindCoopModal(root) {'
assert JS_ANCHOR in s, 'js fn anchor missing'
s = s.replace(JS_ANCHOR, JS_FN + JS_ANCHOR, 1)

io.open(PATH, 'w', encoding='utf-8', newline='').write(s)
print(u'[OK] %d -> %d chars' % (orig_len, len(s)))

# -*- coding: utf-8 -*-
"""
r13 补丁：kb-coop 待协作任务模态
 1. 面板顶角直角 + 纵向拉伸（顶贴 main 顶、底距 main 底 48px）
 2. 筛选行「优先级 / 负责人」选择器与「本月」日期选择器全部换成设计系统完整组件（含浮层）并可点击
 3. select 内部图标对齐原生契约（giencoder-select-arrow 单箭头，stroke-width 1.5）
 4. 打开「自上而下展开」、关闭「自下而上收回」的微动效
另：日历里 16 处自建同义类名 `giencoder-calendar-cell other` 归位为契约类 `giencoder-calendar-cell-other`
"""
import calendar
import datetime
import io
import sys

PATH = 'pages/kanban.html'
MARK_CSS = '/* r13-coop-modal-css */'
MARK_HTML = 'kb-coop-sel-lbl">优先级：'

s = io.open(PATH, encoding='utf-8').read()
orig_len = len(s)
done = []

if MARK_CSS in s and 'r13: 展开/收起微动效' in s:
    print('[SKIP] r13 已应用')
    sys.exit(0)


# ---------------------------------------------------------------- 1) CSS 注入
CSS = u'''      /* r13-coop-modal-css */
      /* ===== r13: 待协作任务模态 —— 直角顶角 / 纵向拉伸 / 展开收起微动效 ===== */

      /* r13-1 顶角直角：面板自 main 顶边展开，只有底角保留 12px 圆角 */
      /* r13-1 纵向拉伸：top:0 + bottom:48px ⇒ height 自动填满两者之间，
         内容不足时也保持"顶贴 main 顶、底距 main 底 48px"，表体撑满剩余空间 */
      .kb-coop-dialog {
        top: 0; bottom: var(--kb-coop-gap-bottom);
        height: auto; max-height: none;
        border-radius: 0 0 12px 12px;
        /* r13-4 展开/收起：基准点取顶边 —— 打开时自上而下展开，关闭时自下而上收回。
           位移只做 12px + 轻微 scaleY，投影与圆角不受影响（不用 clip-path，
           否则会把 box-shadow 一起裁掉） */
        opacity: 0;
        transform-origin: top center;
        transform: translateX(-50%) translateY(-12px) scaleY(0.97);
        transition: opacity 130ms var(--transition-timing-function-standard),
                    transform 160ms var(--transition-timing-function-standard);
        will-change: transform, opacity;
      }
      .kb-coop.is-open .kb-coop-dialog {
        opacity: 1;
        transform: translateX(-50%) translateY(0) scaleY(1);
      }
      /* 遮罩同步淡入淡出 */
      .kb-coop-mask { opacity: 0; transition: opacity 150ms var(--transition-timing-function-standard); }
      .kb-coop.is-open .kb-coop-mask { opacity: 1; }
      /* r13-2 选择器下拉：至少与触发器同宽，长选项不至于被截断 */
      .kb-coop-sel .giencoder-select-popup { min-width: 100%; width: max-content; }
      /* r13-2 双面板日历（约 532px）比触发器（265px）宽：靠右对齐，
         否则会越出面板右边界被 .kb-coop-dialog 的 overflow:hidden 裁掉 */
      .kb-coop-date .giencoder-date-picker-popup { left: auto; right: 0; }
      @media (prefers-reduced-motion: reduce) {
        .kb-coop-dialog, .kb-coop-mask { transition-duration: 1ms; }
      }
</style>'''

anchor_css = u"""      [giencoder-theme='dark'] .kb-coop-tbl .giencoder-table-th { background: var(--color-bg-4); }
</style>"""
assert s.count(anchor_css) == 1, 'css anchor count=%d' % s.count(anchor_css)
s = s.replace(anchor_css, u"""      [giencoder-theme='dark'] .kb-coop-tbl .giencoder-table-th { background: var(--color-bg-4); }
""" + CSS)
done.append('CSS')


# ------------------------------------------- 2) 日历自建同义类名归位（契约类）
n_other = s.count('giencoder-calendar-cell other')
s = s.replace('giencoder-calendar-cell other', 'giencoder-calendar-cell-other')
done.append('calendar-cell-other x%d' % n_other)


# --------------------------------------------------- 3) select 图标异常修复
OLD_PAGEOPT_SUFFIX = u'''<span class=\\"giencoder-select-suffix\\"><svg viewBox=\\"0 0 12 12\\" width=\\"12\\" height=\\"12\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"1.3\\" stroke-linecap=\\"round\\"><path d=\\"M2.6 4.4L6 8l3.4-3.6\\"/></svg></span>'''
NEW_PAGEOPT_SUFFIX = u'''<span class=\\"giencoder-select-suffix\\"><svg class=\\"giencoder-select-arrow\\" viewBox=\\"0 0 12 12\\" width=\\"12\\" height=\\"12\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"1.5\\" stroke-linecap=\\"round\\"><path d=\\"M2 4l4 4 4-4\\"/></svg></span>'''
assert s.count(OLD_PAGEOPT_SUFFIX) == 1, 'pageopt suffix count=%d' % s.count(OLD_PAGEOPT_SUFFIX)
s = s.replace(OLD_PAGEOPT_SUFFIX, NEW_PAGEOPT_SUFFIX)
done.append('pageopt icon')


# ------------------------------------------------------- 4) 筛选行整段替换
# 注意：这里用「普通双引号」写，统一交给 esc() 转义；不要预先写成 \\" 否则会被二次转义
ARROW = (u'<svg class="giencoder-select-arrow" viewBox="0 0 12 12" width="12" height="12" '
         u'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">'
         u'<path d="M2 4l4 4 4-4"/></svg>')
CLEAR_BTN = (u'<button class="giencoder-select-clear" type="button" aria-label="清除选择">'
             u'<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" '
             u'stroke-width="1.5" stroke-linecap="round"><path d="M3 3l6 6M9 3l-6 6"/></svg></button>')


def esc(line):
    """把一行纯 HTML 转成 KB_HTML 数组元素行"""
    return u'        "' + line.replace(u'"', u'\\"') + u'",\n'


def select_block(indent, label, value, placeholder, options):
    """按设计系统原生契约（preview/component-select.html）生成完整 Select：
       view（label + view-text + suffix[arrow+clear]）+ popup（option-list）"""
    p = u' ' * indent
    out = []
    out.append(p + u'<div class="giencoder-select kb-coop-sel" data-component="select" data-variant="single" data-state="default">')
    out.append(p + u'  <div class="giencoder-select-view" tabindex="0" role="combobox" aria-expanded="false" aria-haspopup="listbox">')
    out.append(p + u'    <span class="kb-coop-sel-lbl">' + label + u'</span>')
    out.append(p + u'    <span class="giencoder-select-view-text kb-coop-sel-val" data-placeholder="' + placeholder + u'">' + value + u'</span>')
    out.append(p + u'    <span class="giencoder-select-suffix">')
    out.append(p + u'      ' + ARROW)
    out.append(p + u'      ' + CLEAR_BTN)
    out.append(p + u'    </span>')
    out.append(p + u'  </div>')
    out.append(p + u'  <div class="giencoder-select-popup" style="display:none;">')
    out.append(p + u'    <ul class="giencoder-select-option-list" role="listbox">')
    for i, opt in enumerate(options):
        sel = u' giencoder-select-option-selected' if i == 0 else u''
        aria = u'true' if i == 0 else u'false'
        out.append(p + u'      <li class="giencoder-select-option' + sel + u'" role="option" aria-selected="' + aria + u'">' + opt + u'</li>')
    out.append(p + u'    </ul>')
    out.append(p + u'  </div>')
    out.append(p + u'</div>')
    return out


def month_grid(year, month, rng=None):
    first = datetime.date(year, month, 1)
    lead = (first.weekday() + 1) % 7          # 周日起始
    days = calendar.monthrange(year, month)[1]
    pm, py = (12, year - 1) if month == 1 else (month - 1, year)
    pd = calendar.monthrange(py, pm)[1]
    cells = []
    for i in range(lead):
        cells.append((pd - lead + 1 + i, True, u''))
    for d in range(1, days + 1):
        cls = u''
        if rng and rng[0] <= d <= rng[1]:
            if d == rng[0]:
                cls = u'giencoder-calendar-cell-range-start'
            elif d == rng[1]:
                cls = u'giencoder-calendar-cell-range-end'
            else:
                cls = u'giencoder-calendar-cell-in-range'
        cells.append((d, False, cls))
    n = 1
    while len(cells) % 7 != 0:
        cells.append((n, True, u''))
        n += 1
    return cells


def calendar_block(indent, year, month, rng=None):
    p = u' ' * indent
    out = [p + u'<div class="giencoder-calendar">']
    out.append(p + u'  <div class="giencoder-calendar-header">')
    out.append(p + u'    <button class="giencoder-calendar-nav" type="button" aria-label="上个月">'
                    u'<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" '
                    u'stroke-width="1.5" stroke-linecap="round"><path d="M7.5 2l-4 4 4 4"/></svg></button>')
    out.append(p + u'    <span class="giencoder-calendar-title">%d年%d月</span>' % (year, month))
    out.append(p + u'    <button class="giencoder-calendar-nav" type="button" aria-label="下个月">'
                    u'<svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" '
                    u'stroke-width="1.5" stroke-linecap="round"><path d="M4.5 2l4 4-4 4"/></svg></button>')
    out.append(p + u'  </div>')
    out.append(p + u'  <div class="giencoder-calendar-weekdays">'
                    u'<span>日</span><span>一</span><span>二</span><span>三</span><span>四</span><span>五</span><span>六</span></div>')
    out.append(p + u'  <div class="giencoder-calendar-grid">')
    lines = []
    for d, other, cls in month_grid(year, month, rng):
        c = u'giencoder-calendar-cell'
        if other:
            c += u' giencoder-calendar-cell-other'
        if cls:
            c += u' ' + cls
        lines.append(u'<span class="' + c + u'">' + str(d) + u'</span>')
    # 每行 7 个，便于阅读
    for i in range(0, len(lines), 7):
        out.append(p + u'    ' + u''.join(lines[i:i + 7]))
    out.append(p + u'  </div>')
    out.append(p + u'</div>')
    return out


def date_block(indent):
    p = u' ' * indent
    out = [p + u'<div class="giencoder-date-picker kb-coop-date" data-component="date-picker" data-variant="range" data-state="default">']
    out.append(p + u'  <div class="giencoder-input-wrapper" role="combobox" aria-expanded="false" tabindex="0">')
    out.append(p + u'    <span class="kb-coop-sel-lbl">本月：</span>')
    out.append(p + u'    <input class="giencoder-input kb-date-val" value="2026/08/01 - 2026/08/31" readonly>')
    out.append(p + u'    <span class="giencoder-input-suffix">'
                    u'<svg viewBox="0 0 14 14" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.2">'
                    u'<rect x="1.8" y="2.6" width="10.4" height="9.6" rx="1.6"/>'
                    u'<path d="M1.8 5.6h10.4M4.8 1.4v2.4M9.2 1.4v2.4" stroke-linecap="round"/></svg></span>')
    out.append(p + u'  </div>')
    out.append(p + u'  <div class="giencoder-date-picker-popup" style="display:none;">')
    out.append(p + u'    <div class="giencoder-date-picker-panels">')
    out += calendar_block(indent + 6, 2026, 8, rng=(1, 31))
    out += calendar_block(indent + 6, 2026, 9)
    out.append(p + u'    </div>')
    out.append(p + u'  </div>')
    out.append(p + u'</div>')
    return out


filter_lines = []
filter_lines += select_block(16, u'优先级：', u'全部', u'全部', [u'全部', u'高', u'中', u'低'])
filter_lines += select_block(16, u'负责人：', u'全部', u'全部', [u'全部', u'薛建林', u'廉杨', u'王建政', u'白东东'])
filter_lines += date_block(16)

new_filter = u''.join(esc(l) for l in filter_lines)

kb = s.index('var KB_HTML')
A = s.index(u'        "                <div class=\\"giencoder-select kb-coop-sel\\" data-component=\\"select\\" data-variant=\\"default\\">",', kb)
B = s.index(u'        "              <div class=\\"giencoder-table-container kb-coop-tblwrap\\">",', A)
old_filter = s[A:B]
assert u'优先级' in old_filter and u'负责人' in old_filter
assert u'kb-coop-date' in old_filter

# 保留「筛选行」自己的收尾 </div>
close_idx = old_filter.rindex(u'        "              </div>",')
new_seg = new_filter + old_filter[close_idx:]
s = s[:A] + new_seg + s[B:]
done.append('filter row -> 3 DS components')


# ------------------------------------------------------------- 5) JS：动效
OLD_OPEN_CLOSE = u'''    function open() {
      modal.hidden = false;
      modal.classList.add('is-open');
      document.documentElement.classList.add('kb-coop-lock');
      var dlg = modal.querySelector('.kb-coop-dialog');
      if (dlg) dlg.focus({ preventScroll: true });
    }
    function close() {
      modal.classList.remove('is-open');
      modal.hidden = true;
      document.documentElement.classList.remove('kb-coop-lock');
    }'''
NEW_OPEN_CLOSE = u'''    /* r13: is-open 驱动「自上而下展开 / 自下而上收回」；关闭要等动效播完再 display:none，
       否则会瞬隐、看不到收回过程 */
    var closeTimer = null;
    /* 收起面板内遗留的下拉/日历浮层，避免下次打开时残留在展开态 */
    function resetPopups() {
      modal.querySelectorAll('.giencoder-select-popup, .giencoder-date-picker-popup').forEach(function (p) {
        p.classList.remove('giencoder-popup-open', 'giencoder-panel-open');
        p.style.display = 'none';
      });
    }
    function open() {
      if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }
      resetPopups();
      modal.hidden = false;
      void modal.offsetWidth; /* 先让 display 生效并落定初始样式，下一步加类才会产生过渡 */
      modal.classList.add('is-open');
      document.documentElement.classList.add('kb-coop-lock');
      var dlg = modal.querySelector('.kb-coop-dialog');
      if (dlg) dlg.focus({ preventScroll: true });
    }
    function close() {
      resetPopups();
      modal.classList.remove('is-open');
      document.documentElement.classList.remove('kb-coop-lock');
      if (closeTimer) clearTimeout(closeTimer);
      closeTimer = setTimeout(function () { closeTimer = null; modal.hidden = true; }, 190);
    }'''
assert s.count(OLD_OPEN_CLOSE) == 1, 'open/close count=%d' % s.count(OLD_OPEN_CLOSE)
s = s.replace(OLD_OPEN_CLOSE, NEW_OPEN_CLOSE)
done.append('modal motion JS')


# ------------------------------------- 6) JS：结构不完整时不要锁定 _bound
OLD_SEL_GUARD = u'''      if (sel.classList.contains('giencoder-select-disabled') || sel._bound) return;
      sel._bound = true;
      var view = $('.giencoder-select-view', sel);
      var popup = $('.giencoder-select-popup', sel);
      if (!view || !popup) return;'''
NEW_SEL_GUARD = u'''      if (sel.classList.contains('giencoder-select-disabled') || sel._bound) return;
      var view = $('.giencoder-select-view', sel);
      var popup = $('.giencoder-select-popup', sel);
      /* r13: 先确认结构完整再打 _bound —— 否则缺浮层的选择器被永久标记为已绑定，后续补上浮层也不会再绑 */
      if (!view || !popup) return;
      sel._bound = true;'''
assert s.count(OLD_SEL_GUARD) == 1
s = s.replace(OLD_SEL_GUARD, NEW_SEL_GUARD)

OLD_DP_GUARD = u'''      if (picker._bound) return;
      picker._bound = true;
      var trigger = $('.giencoder-input-wrapper', picker);
      var popup = $('.giencoder-date-picker-popup', picker);
      var input = trigger ? $('.giencoder-input', trigger) : null;
      if (!trigger || !popup || !input) return;'''
NEW_DP_GUARD = u'''      if (picker._bound) return;
      var trigger = $('.giencoder-input-wrapper', picker);
      var popup = $('.giencoder-date-picker-popup', picker);
      var input = trigger ? $('.giencoder-input', trigger) : null;
      /* r13: 同上 */
      if (!trigger || !popup || !input) return;
      picker._bound = true;'''
assert s.count(OLD_DP_GUARD) == 1
s = s.replace(OLD_DP_GUARD, NEW_DP_GUARD)
done.append('binding guards')

io.open(PATH, 'w', encoding='utf-8', newline='').write(s)
print('[OK] %d -> %d chars' % (orig_len, len(s)))
for d in done:
    print('   -', d)

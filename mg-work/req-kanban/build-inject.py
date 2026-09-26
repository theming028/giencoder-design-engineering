# -*- coding: utf-8 -*-
# 需求看板组装脚本：_req_html.html → pages/req-kanban.html (KB_HTML + rq CSS + 交互 JS)
# 同时给 pages/kanban.html 的 topbar radio 补 data-goto 切换
import json, re, io, os

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(ROOT, '..', '..', 'pages')

# ---------- 1. 读取并变换 _req_html.html ----------
src = io.open(os.path.join(ROOT, '_req_html.html'), encoding='utf-8').read()

# 1a. boardhead 控件去绝对定位（改由 .rq-bh-filters flex 布局）
src = src.replace('style="position:absolute; left:120px; top:0; width:101px;"', 'style="width:101px;"')
src = src.replace('style="position:absolute; left:0; top:0; width:250px;"', 'style="width:250px;"')

# 1b. 表头去内联坐标（改 flex 列宽）：仅在 thead 区间内移除 style
i_th = src.find('<div class="rq-thead">')
i_tb = src.find('<div class="rq-tbody"')
thead = src[i_th:i_tb]
thead2 = re.sub(r'\s+style="left:[^"]*"', '', thead)
src = src[:i_th] + thead2 + src[i_tb:]

# 1c. 插入「状态」select（克隆类型 select，换标签与选项）
i_type = src.find('<!-- 类型选择')
i_date = src.find('<!-- 日期选择')
assert i_type > 0 and i_date > i_type, 'boardhead anchors missing'
type_block = src[i_type:i_date]
status_block = type_block.replace('<!-- 类型选择', '<!-- 状态选择')
status_block = status_block.replace('kb-type-select', 'kb-status-select')
status_block = status_block.replace('类型：', '状态：')
# 替换选项列表（全部/需求/任务/缺陷 → 全部/未开始/进行中/已取消/已终止/已完成）
opts_old = re.search(r'<ul class="giencoder-select-option-list".*?</ul>', status_block, flags=re.S)
assert opts_old, 'option list not found in cloned select'
opts_new = (
    '<ul class="giencoder-select-option-list" role="listbox">'
    '<li class="giencoder-select-option giencoder-select-option-selected" role="option" aria-selected="true">全部</li>'
    '<li class="giencoder-select-option" role="option" aria-selected="false">未开始</li>'
    '<li class="giencoder-select-option" role="option" aria-selected="false">进行中</li>'
    '<li class="giencoder-select-option" role="option" aria-selected="false">已取消</li>'
    '<li class="giencoder-select-option" role="option" aria-selected="false">已终止</li>'
    '<li class="giencoder-select-option" role="option" aria-selected="false">已完成</li>'
    '</ul>'
)
status_block = status_block[:opts_old.start()] + opts_new + status_block[opts_old.end():]
src = src[:i_date] + status_block + src[i_date:]

# ---------- 2. 编码为 KB_HTML JSON 数组 ----------
lines = src.split('\n')
kb_decl = 'var KB_HTML = [' + ', '.join(json.dumps(l, ensure_ascii=False) for l in lines) + "].join('\\n');"

# ---------- 3. 替换 req-kanban.html 的 KB_HTML ----------
req_path = os.path.join(PAGES, 'req-kanban.html')
page = io.open(req_path, encoding='utf-8').read()
i = page.find('var KB_HTML')
j = page.find('\n', i)
assert i > 0 and j > i
page = page[:i] + kb_decl + page[j:]

# ---------- 4. 注入 rq-* CSS ----------
RQ_CSS = '''      /* ===== 需求看板 rq-* (769:13709)：仅做视图适配，组件本体用 giencoder 契约类 ===== */
      .rq-panel { display: flex; flex-direction: column; padding: 48px 0 12px; }
      /* stats 行 */
      .rq-stats { flex: none; display: flex; gap: 16px; margin: 64px 20px 0; }
      .rq-stat {
        position: relative; flex: 1; min-width: 0; height: 64px;
        background: var(--color-bg-1); border: 1px solid var(--color-border-1);
        border-radius: 8px; cursor: pointer;
      }
      /* is-active 仅是 hover 态：默认无投影，悬停才深一级边框 + 浅投影 */
      .rq-stat:hover { border-color: var(--color-border-2); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }
      .rq-stat-tile {
        position: absolute; left: 12px; top: 12px; width: 40px; height: 40px; border-radius: 6px;
        display: flex; align-items: center; justify-content: center; line-height: 0;
      }
      .rq-stat-tile svg { width: 20px; height: 20px; }
      .rq-stat-vdiv { position: absolute; left: 60px; top: 20px; width: 1px; height: 24px; background: var(--color-border-2); }
      .rq-stat-label { position: absolute; left: 68px; top: 22px; color: var(--color-text-1); font-size: var(--font-size-body-3); font-weight: 500; line-height: 20px; white-space: nowrap; }
      .rq-stat-num { position: absolute; right: 16px; top: 16px; height: 32px; display: flex; align-items: center; gap: 8px; }
      .rq-stat-num b { color: var(--color-text-1); font-size: 24px; font-weight: 500; line-height: 32px; }
      .rq-stat-arrow { width: 16px; height: 16px; color: var(--color-text-1); line-height: 0; }
      .rq-stat-arrow svg { width: 16px; height: 16px; }
      .rq-panel .kb-divider { position: static; flex: none; margin: 20px 20px 0; }
      /* boardhead */
      .rq-boardhead { position: relative; flex: none; display: flex; align-items: center; height: 28px; margin: 19px 20px 0; }
      .rq-bh-title { flex: none; color: var(--color-text-1); font-size: 16px; font-weight: 500; line-height: 24px; white-space: nowrap; }
      .rq-boardhead .kb-vdiv { position: static; flex: none; margin: 0 12px; }
      .rq-bh-controls { display: flex; align-items: center; gap: 12px; margin-left: auto; }
      .rq-bh-filters { display: flex; align-items: center; gap: 12px; }
      .rq-bh-filters .giencoder-select, .rq-bh-filters .giencoder-date-picker { position: relative; flex: none; }
      .rq-bh-filters .giencoder-select[data-size="small"] .giencoder-select-view { min-height: 28px; height: 28px; padding: 0 8px 0 12px; border-radius: 6px; }
      /* popup 宽度跟随触发框（覆盖组件默认 min-width:200px，避免 101px 触发框被撑开错位） */
      .rq-bh-filters .giencoder-select .giencoder-select-popup { width: auto; min-width: 100%; }
      .rq-bh-filters .giencoder-select-view { gap: 4px; justify-content: flex-start; }
      .rq-bh-filters .giencoder-select-view .rq-sel-lbl { flex: none; color: var(--color-neutral-7); }
      .rq-bh-filters .giencoder-select-view-text { flex: 1; min-width: 0; }
      .rq-bh-filters .giencoder-select[data-size="small"] .giencoder-select-view { min-height: 28px; height: 28px; padding: 0 8px 0 12px; border-radius: 6px; }
      /* popup 宽度跟随触发框（覆盖组件默认 min-width:200px，避免 101px 触发框被撑开错位） */
      .rq-bh-filters .giencoder-select .giencoder-select-popup { width: auto; min-width: 100%; }
      .rq-bh-filters .giencoder-select-view { gap: 4px; justify-content: flex-start; }
      .rq-bh-filters .giencoder-select-view .rq-sel-lbl { flex: none; color: var(--color-neutral-7); }
      .rq-bh-filters .giencoder-select-view-text { flex: 1; min-width: 0; }
      .rq-search { flex: none; }
      /* 表格：设计系统 Table / borderless 变体（开放式：无外边框、无圆角、无斑马纹，仅行间分割线） */
      .rq-table {
        flex: 1; min-height: 0; display: flex; flex-direction: column; margin: 15px 20px 0;
      }
      .rq-tblscroll { flex: 1; min-height: 0; }
      .rq-tbl { table-layout: fixed; min-width: 940px; }
      /* borderless 契约：去掉表头底色与容器边框，仅保留行间 1px 分割线 */
      .rq-table.giencoder-table-borderless .giencoder-table-th {
        background: transparent; border-bottom: 1px solid var(--color-border-1);
      }
      .rq-table .giencoder-table-th { height: 32px; padding: 6px 12px; background: transparent; }
      .rq-table .giencoder-table-td { height: 36px; padding: 6px 12px; }
      .rq-table .giencoder-table-tr:last-child .giencoder-table-td { border-bottom: none; }
      /* 行 hover 高亮（契约 hover 态） */
      .rq-table tbody .giencoder-table-tr:hover .giencoder-table-td { background: var(--color-fill-1); }
      .rq-td { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
      .rq-td-idx { color: var(--color-text-3); }
      .rq-td-id { color: var(--color-text-2); }
      .rq-td-title { overflow: hidden; }
      .rq-title-txt { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .rq-type { margin-right: 8px; color: var(--color-neutral-7); }
      .rq-td-time { color: var(--color-text-3); }
      .rq-status { display: inline-flex; align-items: center; gap: 4px; height: 22px; padding: 0 8px; border-radius: 4px; font-size: var(--font-size-body-1); line-height: 22px; white-space: nowrap; }
      .rq-status svg { width: 12px; height: 12px; }
      .rq-status--todo { background: var(--color-fill-2); color: var(--color-neutral-7); }
      .rq-status--doing { background: #E3EEFF; color: #5592EB; }
      .rq-status--done { background: #E2F4E4; color: #009E61; }
      .rq-status--stop { background: #FDE2E3; color: var(--color-danger-5); }
      .rq-status--cancel { background: #FFECD9; color: #F3881E; }
      /* skeleton / empty */
      .rq-skeleton { display: none; flex: 1; min-height: 0; flex-direction: column; gap: 8px; padding: 12px 16px; }
      .rq-skel-row { display: flex; align-items: center; gap: 24px; height: 36px; }
      .rq-skeleton .giencoder-skeleton-line, .giencoder-skeleton-line { display: inline-block; height: 14px; border-radius: 4px; background: var(--color-fill-2); animation: rq-skel 1.2s ease-in-out infinite; }
      @keyframes rq-skel { 0%, 100% { opacity: 1; } 50% { opacity: 0.45; } }
      .rq-empty { display: none; flex: 1; min-height: 0; flex-direction: column; align-items: center; justify-content: center; gap: 4px; color: var(--color-text-3); }
      .rq-empty svg { width: 64px; height: 64px; }
      .rq-empty-text { margin: 8px 0 0; color: var(--color-text-2); font-size: var(--font-size-body-3); line-height: 22px; }
      .rq-empty-desc { margin: 0; color: var(--color-text-3); font-size: var(--font-size-body-1); line-height: 16px; }
      /* 分页：giencoder Pagination 组件 + 视图适配（矩形底 #FAFAFA h48） */
      .rq-pager {
        flex: none; display: flex; align-items: center; height: 48px; padding: 0 16px;
        background: #FAFAFA; border-top: 1px solid var(--color-border-1);
      }
      .rq-pager .giencoder-pagination { flex: 1; }
      .rq-pager .giencoder-pagination-stats { margin-right: auto; }
      .rq-pager .giencoder-pagination-item[disabled] { color: var(--color-text-4); cursor: not-allowed; }
      .rq-pager .giencoder-pagination-item[disabled]:hover { background: var(--color-bg-2); border-color: var(--color-border-2); color: var(--color-text-4); }
      .rq-pg-prev svg, .rq-pg-next svg { width: 14px; height: 14px; }
      /* 状态机：loading / empty */
      .rq-panel[data-state="loading"] .rq-tblscroll, .rq-panel[data-state="loading"] .rq-pager { display: none; }
      .rq-panel[data-state="loading"] .rq-skeleton { display: flex; }
      .rq-panel[data-state="empty"] .rq-tblscroll, .rq-panel[data-state="empty"] .rq-pager, .rq-panel[data-state="empty"] .rq-skeleton { display: none; }
      .rq-panel[data-state="empty"] .rq-empty { display: flex; }
      /* 响应式：<900 stats 换行（表格由 giencoder-table-container 自身横向滚动） */
      @media (max-width: 900px) {
        .rq-stats { flex-wrap: wrap; }
        .rq-stat { flex: 1 1 30%; }
        .rq-bh-controls { flex-wrap: wrap; }
      }
    '''

# 找 kb 样式块尾部（含 .kb-panel 的 style 块）
si = page.find('.kb-panel {')
style_end = page.rfind('</style>', 0, si)
style_end = page.find('</style>', si)
assert si > 0 and style_end > si
# rq-* 样式块整体替换（可重复执行：删旧块再插新块）
_old_i = page.find('/* ===== 需求看板 rq-*')
if _old_i > 0:
    _old_end = page.find('</style>', _old_i)
    page = page[:_old_i] + page[_old_end:]
    style_end = page.find('</style>', page.find('.kb-panel {'))
page = page[:style_end] + RQ_CSS + page[style_end:]

# ---------- 5. 注入交互 JS（切换/分页/加载状态机） ----------
REQ_JS = '''
  /* ===== 需求看板：radio 切换 / 分页 / 加载状态机 ===== */
  function bindReqPage(wrap) {
    wrap.addEventListener('click', function (ev) {
      var tab = ev.target.closest ? ev.target.closest('.kb-radio-btn[data-goto]') : null;
      if (tab && !tab.classList.contains('is-on')) {
        var g = tab.getAttribute('data-goto');
        if (g) { location.href = g; return; }
      }
      var pgItem = ev.target.closest ? ev.target.closest('.giencoder-pagination-item') : null;
      if (pgItem && !pgItem.classList.contains('giencoder-pagination-item-ellipsis')) {
        var pg = wrap.querySelector('.giencoder-pagination');
        if (pg) {
          var nums = Array.prototype.filter.call(pg.querySelectorAll('.giencoder-pagination-item'), function (n) {
            return !n.hasAttribute('aria-label') && !n.classList.contains('giencoder-pagination-item-ellipsis');
          });
          var max = nums.length ? parseInt(nums[nums.length - 1].textContent, 10) : 1;
          var curIdx = 0;
          nums.forEach(function (n, idx) { if (n.classList.contains('giencoder-pagination-item-active')) curIdx = idx; });
          var targetIdx = curIdx;
          if (pgItem.hasAttribute('aria-label')) {
            var isPrev = pgItem.getAttribute('aria-label') === '上一页';
            targetIdx = Math.min(nums.length - 1, Math.max(0, curIdx + (isPrev ? -1 : 1)));
          } else {
            nums.forEach(function (n, idx) { if (n === pgItem) targetIdx = idx; });
          }
          nums.forEach(function (n) { n.classList.remove('giencoder-pagination-item-active'); n.removeAttribute('aria-current'); });
          nums[targetIdx].classList.add('giencoder-pagination-item-active');
          nums[targetIdx].setAttribute('aria-current', 'page');
          var prev = pg.querySelector('.rq-pg-prev');
          var next = pg.querySelector('.rq-pg-next');
          if (prev) prev.disabled = (parseInt(nums[targetIdx].textContent, 10) === 1);
          if (next) next.disabled = (parseInt(nums[targetIdx].textContent, 10) === max);
        }
      }
      var th = ev.target.closest ? ev.target.closest('.giencoder-table-th-sortable') : null;
      if (th) {
        var nextSort = th.getAttribute('data-sort') === 'asc' ? 'desc' : 'asc';
        th.setAttribute('data-sort', nextSort);
        th.setAttribute('aria-sort', nextSort === 'asc' ? 'ascending' : 'descending');
      }
    });
    var panel = wrap.querySelector('.rq-panel');
    if (panel && panel.getAttribute('data-state') === 'loading') {
      setTimeout(function () { if (panel.isConnected) panel.setAttribute('data-state', 'ready'); }, 800);
    }
  }

  function inject() {'''
page = page.replace('  function inject() {', REQ_JS, 1)
page = page.replace('    bindComponents(wrap);\n    return true;', '    bindComponents(wrap);\n    bindReqPage(wrap);\n    return true;', 1)
assert 'bindReqPage(wrap);' in page

io.open(req_path, 'w', encoding='utf-8').write(page)
print('req-kanban.html written, KB_HTML lines:', len(lines))

# ---------- 6. kanban.html：radio 补 data-goto + 切换脚本 ----------
kb_path = os.path.join(PAGES, 'kanban.html')
kb = io.open(kb_path, encoding='utf-8').read()
old1 = '<span class=\\"kb-radio-btn\\" role=\\"tab\\" aria-selected=\\"false\\">需求看板</span>'
new1 = '<span class=\\"kb-radio-btn\\" role=\\"tab\\" aria-selected=\\"false\\" data-goto=\\"req-kanban.html\\">需求看板</span>'
old2 = '<span class=\\"kb-radio-btn is-on\\" role=\\"tab\\" aria-selected=\\"true\\">'
new2 = '<span class=\\"kb-radio-btn is-on\\" role=\\"tab\\" aria-selected=\\"true\\" data-goto=\\"kanban.html\\">'
if old1 in kb:
    kb = kb.replace(old1, new1, 1)
    kb = kb.replace(old2, new2, 1)
    print('kanban.html radio data-goto patched')
else:
    print('kanban.html radio already patched or pattern missed:', 'data-goto' in kb)

SWITCH_JS = '''<script>
      /* 看板切换：任务看板 ↔ 需求看板 */
      document.addEventListener('click', function (ev) {
        var tab = ev.target.closest && ev.target.closest('.kb-radio-btn[data-goto]');
        if (tab && !tab.classList.contains('is-on')) {
          var g = tab.getAttribute('data-goto');
          if (g) location.href = g;
        }
      });
    </script>
  </body>'''
if 'kb-radio-btn[data-goto]' not in kb:
    kb = kb.replace('</body>', SWITCH_JS, 1)
    print('kanban.html switch script added')
io.open(kb_path, 'w', encoding='utf-8').write(kb)
print('done')

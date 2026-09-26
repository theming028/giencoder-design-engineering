# -*- coding: utf-8 -*-
"""round11: 研发工作台(任务看板)两处修复
1) 卡片优先级标签颜色对齐设计稿（高 #F53F3F / 中 #F77234 / 低 #575757，取自模态设计稿零色偏实测）
2) kb-stat--coop 点击 → 非全屏模态（复用 giencoder-modal / table / pagination 契约类 + kb- 适配层）
幂等：重复执行只替换/跳过，不叠加。
"""
import json
import io
import sys

P = r'E:\GienCoder\giencoder-design-engineering\pages\kanban.html'
s = io.open(P, encoding='utf-8').read()
orig_len = len(s)

# ---------------------------------------------------------------- 1. token
old_tokens = """        --kb-tag-high-bg: rgb(var(--red-2)); --kb-tag-high-tx: rgb(var(--red-6));
        --kb-tag-mid-bg: rgb(var(--orange-2)); --kb-tag-mid-tx: rgb(var(--orange-6));
        --kb-tag-low-bg: var(--color-fill-2); --kb-tag-low-tx: var(--color-text-3);"""
new_tokens = """        /* r11: 优先级色对齐设计稿（模态设计稿字形核心像素实测，MasterGo 渲染零色偏）
           高 #F53F3F(=--red-6) / 中 #F77234 / 低 #575757；底色按设计稿 tint 规范 0.12 alpha */
        --kb-prio-high: #F53F3F; --kb-prio-mid: #F77234; --kb-prio-low: #575757;
        --kb-tag-high-bg: rgba(245, 63, 63, 0.12); --kb-tag-high-tx: var(--kb-prio-high);
        --kb-tag-mid-bg: rgba(247, 114, 52, 0.12); --kb-tag-mid-tx: var(--kb-prio-mid);
        --kb-tag-low-bg: rgba(87, 87, 87, 0.10); --kb-tag-low-tx: var(--kb-prio-low);
        /* r11: 待协作模态令牌（设计稿实测） */
        --kb-coop-bg: #FAFAFA;
        --kb-tbl-head-bg: #F8F9FA;
        --kb-tbl-line: #EBECED;
        --kb-coop-mask: rgba(0, 0, 0, 0.32);
        --kb-coop-top: 44px;"""
if old_tokens in s:
    s = s.replace(old_tokens, new_tokens, 1)
    print('[1] tokens replaced')
elif '--kb-prio-high' in s:
    print('[1] tokens already patched, skip')
else:
    print('[1] !! token anchor not found'); sys.exit(1)

# ---------------------------------------------------------------- 2. CSS
CSS = """
      /* ===== r11: 待协作任务模态（非全屏面板；复用 giencoder-modal 契约类 + kb- 适配层） ===== */
      .kb-coop[hidden] { display: none; }
      .kb-coop { position: fixed; inset: var(--kb-coop-top) 0 0 0; z-index: 1200; }
      .kb-coop-mask {
        position: absolute; inset: 0; background: var(--kb-coop-mask);
        -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px);
      }
      .kb-coop-dialog {
        position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
        width: 1200px; max-width: calc(100vw - 48px);
        height: 806px; max-height: calc(100% - 24px);
        display: flex; flex-direction: column;
        background: var(--kb-coop-bg); border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
      }
      .kb-coop-head { flex: none; border-bottom: none; padding: 16px 24px 0; }
      .kb-coop-head .giencoder-modal-title { font-size: var(--font-size-title-1); font-weight: 600; }
      .kb-coop-close { color: var(--color-text-1); }
      .kb-coop-content { flex: 1; min-height: 0; display: flex; flex-direction: column; padding: 16px 24px 14px; }
      .kb-coop-filters { flex: none; display: flex; align-items: center; gap: 11px; margin-bottom: 14px; }
      .kb-coop-search, .kb-coop-search.giencoder-input-wrapper { width: 217px; min-width: 217px; height: 32px; border-radius: 6px; padding: 0 12px; }
      .kb-coop-search-input { width: 100%; border: none; outline: none; background: transparent; font-size: var(--font-size-body-3); color: var(--color-text-1); }
      .kb-coop-search-input::placeholder { color: var(--color-text-3); }
      .kb-coop-search-ico { color: var(--color-text-3); }
      .kb-coop-sel .giencoder-select-view,
      .kb-coop-date .giencoder-input-wrapper {
        height: 32px; min-height: 32px; border-radius: 6px; border: 1px solid var(--color-border-2);
        background: var(--color-bg-1); box-shadow: none; padding: 0 12px;
      }
      .kb-coop-sel { width: 117px; }
      .kb-coop-sel .giencoder-select-view { width: 117px; }
      .kb-coop-sel-lbl { color: var(--color-text-2); white-space: nowrap; }
      .kb-coop-sel-val { color: var(--color-text-1); }
      .kb-coop-date, .kb-coop-date .giencoder-input-wrapper { width: 270px; }
      .kb-coop-tblwrap { flex: 1; min-height: 0; overflow: auto; }
      .kb-coop-tbl { width: 100%; border-collapse: collapse; font-size: var(--font-size-body-3); }
      .kb-coop-tbl .giencoder-table-th {
        background: var(--kb-tbl-head-bg); color: var(--color-text-3); font-weight: 400;
        font-size: var(--font-size-body-3); padding: 9px 12px; border-bottom: none; text-align: left;
      }
      .kb-coop-tbl .giencoder-table-td {
        padding: 7px 12px; line-height: 22px; color: var(--color-text-1);
        border-bottom: 1px solid var(--kb-tbl-line); white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis;
      }
      .kb-coop-tbl .giencoder-table-tr:hover .giencoder-table-td { background: var(--color-fill-1); }
      .kb-coop-tbl .kb-row-hover .giencoder-table-td { background: var(--color-fill-1); }
      .kb-coop-tbl .kb-row-hover .kb-td-title { color: var(--color-primary-6); }
      .kb-td-num { color: var(--color-text-3); }
      .kb-td-id { color: var(--color-text-3); }
      .kb-td-time { color: var(--color-text-3); }
      .kb-td-prio { font-weight: 500; }
      .kb-prio-high { color: var(--kb-prio-high); }
      .kb-prio-mid { color: var(--kb-prio-mid); }
      .kb-prio-low { color: var(--kb-prio-low); }
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
        background: #E8F0FE; border-color: #BBD1FB; color: var(--color-primary-6); font-weight: 500;
      }
      .kb-coop-pager .kb-pg-nav { color: var(--color-text-2); }
      .kb-coop-pageopt { width: 96px; }
      .kb-coop-pageopt .giencoder-select-view {
        width: 96px; height: 32px; min-height: 32px; border-radius: 6px;
        border: 1px solid var(--color-border-2); background: var(--color-bg-1); box-shadow: none; padding: 0 10px;
      }
      .kb-coop-jump { color: var(--color-text-2); font-size: var(--font-size-body-3); display: inline-flex; align-items: center; gap: 8px; }
      .kb-coop-jump .giencoder-input-wrapper { width: 48px; min-width: 48px; height: 32px; border-radius: 6px; padding: 0 8px; }
      .kb-coop-jump .giencoder-input { width: 100%; border: none; outline: none; background: transparent; text-align: center; }
      html.kb-coop-lock, html.kb-coop-lock body { overflow: hidden; }
      [giencoder-theme='dark'] .kb-coop-dialog { background: var(--color-bg-2); }
      [giencoder-theme='dark'] .kb-coop-tbl .giencoder-table-th { background: var(--color-bg-3); }
</style>"""
ANCHOR = "/* r11-coop-modal-css */"
if ANCHOR in s:
    print('[2] css already patched, skip')
else:
    idx = s.rindex('</style>', 0, s.index('var KB_HTML'))
    s = s[:idx] + '      ' + ANCHOR + '\n' + CSS.lstrip(' ') + s[idx + len('</style>'):]
    print('[2] css inserted')

# ---------------------------------------------------------------- 3. 模态 HTML
def q(line):
    return json.dumps(line, ensure_ascii=False)

SORTER = ('<span class="giencoder-table-sorter">'
          '<svg viewBox="0 0 12 12" width="12" height="12" fill="none">'
          '<path d="M3.9 5L3 4.1 6.1 1l.9.9L9.2 4.1 8.3 5 6.1 2.8 3.9 5Zm0 2l-.9.9 2.2 2.2.9.9 3.1-3.1-.9-.9-2.2 2.2L3.9 7Z" fill="#868686"/>'
          '</svg></span>')

ROWS = [
    ('1', 'TSK2026001', '生成产品需求文档：基于原始需求登记表，生成结构化的 PRD 产品需求文档。', '高', '薛建林', '刚刚', ''),
    ('2', 'TSK2026002', '业务需求分析：读取业务方原始需求文档，提炼生成原始需求登记表。', '高', '薛建林', '半小时前', ' kb-row-hover'),
    ('3', 'TSK2026003', '端到端流程初始化：用户输入业务需求，生成交付状态跟踪表，启动整个流程。', '高', '廉杨', '昨天 10:21', ''),
    ('4', 'TSK2026004', '状态标识采用“交通灯”模式，方便直观管理', '高', '王建政', '2026/07/26 13:58', ''),
    ('5', 'TSK2026005', '创建一条流程实例记录', '中', '白东东', '2026/07/26 13:58', ''),
    ('6', 'TSK2026006', '用户希望增加一个基于AI的智能报表生成模块，支持导出PDF和Excel格式', '中', '白东东', '2026/07/26 13:58', ''),
    ('7', 'TSK2026007', '端到端流程初始化：用户输入业务需求，生成交付状态跟踪表，启动整个流程。', '低', '王建政', '2026/07/26 13:58', ''),
    ('8', 'TSK2026008', '状态标识采用“交通灯”模式，方便直观管理', '低', '王建政', '2026/07/26 13:58', ''),
]
PRIO_CLS = {'高': 'kb-prio-high', '中': 'kb-prio-mid', '低': 'kb-prio-low'}

rows_html = []
for num, tid, title, prio, owner, time_, extra in ROWS:
    rows_html.append(
        '                    <tr class="giencoder-table-tr{ex}">'
        '<td class="giencoder-table-td kb-td-num">{n}</td>'
        '<td class="giencoder-table-td kb-td-id">{tid}</td>'
        '<td class="giencoder-table-td kb-td-title">{title}</td>'
        '<td class="giencoder-table-td kb-td-prio {pc}">{p}</td>'
        '<td class="giencoder-table-td">{o}</td>'
        '<td class="giencoder-table-td kb-td-time">{t}</td></tr>'.format(
            ex=extra, n=num, tid=tid, title=title, pc=PRIO_CLS[prio], p=prio, o=owner, t=time_)
    )

MODAL = [
    '        <!-- r11: 待协作任务模态（非全屏面板；giencoder-modal 契约类 + kb- 视图适配层） -->',
    '        <div class="kb-coop" hidden>',
    '          <div class="giencoder-modal-mask kb-coop-mask" data-close="1"></div>',
    '          <div class="giencoder-modal kb-coop-dialog" role="dialog" aria-modal="true" aria-label="待协作任务">',
    '            <div class="giencoder-modal-header kb-coop-head">',
    '              <div class="giencoder-modal-title">待协作任务</div>',
    '              <button class="giencoder-modal-close-btn kb-coop-close" type="button" aria-label="Close" data-close="1">',
    '                <svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M4.2 4.2l7.6 7.6M11.8 4.2l-7.6 7.6"/></svg>',
    '              </button>',
    '            </div>',
    '            <div class="giencoder-modal-content kb-coop-content">',
    '              <div class="kb-coop-filters">',
    '                <span class="giencoder-input-wrapper kb-coop-search" data-size="default">',
    '                  <span class="giencoder-input-prefix kb-coop-search-ico"><svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="7" cy="7" r="4.3"/><path d="M10.3 10.3L13.6 13.6" stroke-linecap="round"/></svg></span>',
    '                  <input class="giencoder-input kb-coop-search-input" placeholder="搜索工作任务">',
    '                </span>',
    '                <div class="giencoder-select kb-coop-sel" data-component="select" data-variant="default">',
    '                  <div class="giencoder-select-view" tabindex="0" role="combobox" aria-expanded="false" aria-haspopup="listbox">',
    '                    <span class="kb-coop-sel-lbl">优先级：</span>',
    '                    <span class="giencoder-select-value kb-coop-sel-val">全部</span>',
    '                    <span class="giencoder-select-suffix"><svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><path d="M4 2.6L6 4.8l2-2.2M4 9.4L6 7.2l2 2.2"/></svg></span>',
    '                  </div>',
    '                </div>',
    '                <div class="giencoder-select kb-coop-sel" data-component="select" data-variant="default">',
    '                  <div class="giencoder-select-view" tabindex="0" role="combobox" aria-expanded="false" aria-haspopup="listbox">',
    '                    <span class="kb-coop-sel-lbl">负责人：</span>',
    '                    <span class="giencoder-select-value kb-coop-sel-val">全部</span>',
    '                    <span class="giencoder-select-suffix"><svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><path d="M4 2.6L6 4.8l2-2.2M4 9.4L6 7.2l2 2.2"/></svg></span>',
    '                  </div>',
    '                </div>',
    '                <div class="giencoder-date-picker kb-coop-date" data-component="date-picker" data-variant="range">',
    '                  <div class="giencoder-input-wrapper" role="combobox" aria-expanded="false" tabindex="0">',
    '                    <span class="kb-coop-sel-lbl">本月：</span>',
    '                    <input class="giencoder-input kb-date-val" value="2026/08/01 - 2026/08/31" readonly>',
    '                    <span class="giencoder-input-suffix"><svg viewBox="0 0 14 14" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="1.8" y="2.6" width="10.4" height="9.6" rx="1.6"/><path d="M1.8 5.6h10.4M4.8 1.4v2.4M9.2 1.4v2.4" stroke-linecap="round"/></svg></span>',
    '                  </div>',
    '                </div>',
    '              </div>',
    '              <div class="giencoder-table-container kb-coop-tblwrap">',
    '                <table class="giencoder-table-content kb-coop-tbl">',
    '                  <colgroup><col style="width:52px"><col style="width:132px"><col><col style="width:96px"><col style="width:110px"><col style="width:170px"></colgroup>',
    '                  <thead>',
    '                    <tr class="giencoder-table-tr">',
    '                      <th class="giencoder-table-th">序号</th>',
    '                      <th class="giencoder-table-th">任务ID</th>',
    '                      <th class="giencoder-table-th giencoder-table-th-sortable">任务标题' + SORTER + '</th>',
    '                      <th class="giencoder-table-th giencoder-table-th-sortable">优先级' + SORTER + '</th>',
    '                      <th class="giencoder-table-th giencoder-table-th-sortable">负责人' + SORTER + '</th>',
    '                      <th class="giencoder-table-th giencoder-table-th-sortable">创建时间' + SORTER + '</th>',
    '                    </tr>',
    '                  </thead>',
    '                  <tbody>',
] + rows_html + [
    '                  </tbody>',
    '                </table>',
    '              </div>',
    '              <div class="kb-coop-foot">',
    '                <span class="giencoder-pagination-stats kb-coop-stats">共 256 条待协作任务</span>',
    '                <div class="giencoder-pagination kb-coop-pager" role="navigation" aria-label="分页">',
    '                  <button class="giencoder-pagination-item kb-pg-nav" type="button" aria-label="上一页"><svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M7.4 2.4L4 6l3.4 3.6"/></svg></button>',
    '                  <button class="giencoder-pagination-item giencoder-pagination-item-active" type="button" aria-current="page">1</button>',
    '                  <button class="giencoder-pagination-item" type="button">2</button>',
    '                  <button class="giencoder-pagination-item" type="button">3</button>',
    '                  <button class="giencoder-pagination-item" type="button">4</button>',
    '                  <button class="giencoder-pagination-item" type="button">5</button>',
    '                  <span class="giencoder-pagination-item giencoder-pagination-item-ellipsis">···</span>',
    '                  <button class="giencoder-pagination-item" type="button">20</button>',
    '                  <button class="giencoder-pagination-item kb-pg-nav" type="button" aria-label="下一页"><svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M4.6 2.4L8 6l-3.4 3.6"/></svg></button>',
    '                  <div class="giencoder-select kb-coop-pageopt" data-component="select" data-variant="default">',
    '                    <div class="giencoder-select-view" tabindex="0" role="combobox" aria-expanded="false" aria-haspopup="listbox">',
    '                      <span class="giencoder-select-value">15条/页</span>',
    '                      <span class="giencoder-select-suffix"><svg viewBox="0 0 12 12" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><path d="M2.6 4.4L6 8l3.4-3.6"/></svg></span>',
    '                    </div>',
    '                  </div>',
    '                  <span class="kb-coop-jump">前往<span class="giencoder-input-wrapper"><input class="giencoder-input" value=""></span></span>',
    '                </div>',
    '              </div>',
    '            </div>',
    '          </div>',
    '        </div>',
]

MARK_END = '"].join(\'\\n\');'
if '共 256 条待协作任务' in s:
    print('[3] modal markup already present, skip')
else:
    idx = s.index('var KB_HTML')
    idx_end = s.index(MARK_END, idx) + 1  # 跳过数组末元素的收尾引号，插到它之后
    payload = ',\n' + ',\n'.join('        ' + q(l) for l in MODAL)
    s = s[:idx_end] + payload + s[idx_end:]
    print('[3] modal markup inserted (%d lines)' % len(MODAL))

# ---------------------------------------------------------------- 4. JS
if 'bindCoopModal' in s:
    print('[4] js already patched, skip')
else:
    call_anchor = '    bindDashedCards(wrap);'
    s = s.replace(call_anchor, call_anchor + '\n    bindCoopModal(wrap);', 1)

    JS = """
  /* ===== r11: 待协作任务模态：kb-stat--coop 点击打开（非全屏面板 + 遮罩 + Esc/遮罩/× 关闭） ===== */
  function bindCoopModal(root) {
    var modal = root.querySelector('.kb-coop');
    var trigger = root.querySelector('.kb-stat--coop');
    if (!modal || !trigger) return;
    function open() {
      modal.hidden = false;
      modal.classList.add('is-open');
      document.documentElement.classList.add('kb-coop-lock');
      var first = modal.querySelector('.kb-coop-close');
      if (first) first.focus({ preventScroll: true });
    }
    function close() {
      modal.classList.remove('is-open');
      modal.hidden = true;
      document.documentElement.classList.remove('kb-coop-lock');
    }
    trigger.addEventListener('click', open);
    trigger.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });
    modal.addEventListener('click', function (e) {
      var t = e.target;
      if (t && t.closest && t.closest('[data-close]')) { close(); return; }
      var it = t && t.closest ? t.closest('.giencoder-pagination-item') : null;
      if (!it || it.classList.contains('kb-pg-nav') || it.classList.contains('giencoder-pagination-item-ellipsis')) return;
      modal.querySelectorAll('.kb-coop-pager .giencoder-pagination-item').forEach(function (el) {
        el.classList.remove('giencoder-pagination-item-active');
        el.removeAttribute('aria-current');
      });
      it.classList.add('giencoder-pagination-item-active');
      it.setAttribute('aria-current', 'page');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !modal.hidden) close();
    });
  }
"""
    js_end = s.index('})();\n</script>')
    s = s[:js_end] + JS + s[js_end:]
    print('[4] js inserted')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('DONE  %d -> %d chars' % (orig_len, len(s)))

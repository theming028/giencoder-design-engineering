# -*- coding: utf-8 -*-
# 把 _req_html.html 里自建的 .rq-table / .rq-pager 改写为设计系统组件：
#   Table:      div.giencoder-table > div.giencoder-table-container > table.giencoder-table-content
#               thead th.giencoder-table-th[.giencoder-table-th-sortable] + tbody tr.giencoder-table-tr > td.giencoder-table-td
#   Pagination: div.giencoder-table-pagination > div.giencoder-pagination[role=navigation]
#               > span.giencoder-pagination-stats + button.giencoder-pagination-item[.giencoder-pagination-item-active|-ellipsis]
import io, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(ROOT, '_req_html.html'), encoding='utf-8').read()

# ---- 1. 抽取现有 8 行数据（idx/id/type/title/owner/status(svg+label)/time）----
rows = []
for m in re.finditer(r'<div class="rq-row" tabindex="0">(.*?)</div>\s*(?=<div class="rq-row"|<span class="rq-scrollbar")', src, flags=re.S):
    b = m.group(1)
    rows.append({
        'idx': re.search(r'rq-td-idx">(.*?)<', b, re.S).group(1),
        'id': re.search(r'rq-td-id">(.*?)<', b, re.S).group(1),
        'type': re.search(r'rq-type">(.*?)<', b, re.S).group(1),
        'title': re.search(r'rq-title-txt">(.*?)<', b, re.S).group(1),
        'owner': re.search(r'rq-td-owner">(.*?)<', b, re.S).group(1),
        'status_svg': re.search(r'(<svg.*?</svg>)', b, re.S).group(1),
        'status_cls': re.search(r'class="rq-status (rq-status--[a-z]+)"', b).group(1),
        'status_txt': re.search(r'</svg>(.*?)</span>', b, re.S).group(1),
        'time': re.search(r'rq-td-time">(.*?)<', b, re.S).group(1),
    })
assert len(rows) == 8, 'row parse count=%d' % len(rows)

# ---- 2. 抽取排序图标 / 上一页下一页图标 ----
sort_svg = re.search(r'rq-th-sort"[^>]*>需求标题(<svg.*?</svg>)', src, re.S)
sort_svg = sort_svg.group(1) if sort_svg else ''
prev_svg = re.search(r'giencoder-pagination-prev"[^>]*>(\s*<svg.*?</svg>)', src, re.S).group(1)
next_svg = re.search(r'giencoder-pagination-next"[^>]*>(\s*<svg.*?</svg>)', src, re.S).group(1)

# ---- 3. 生成组件化表格 ----
COLS = [
    ('序号', '48px', False),
    ('需求ID', '127px', False),
    ('需求标题', 'auto', True),
    ('创建者', '68px', False),
    ('状态', '270px', True),
    ('创建时间', '180px', True),
]
colgroup = '\n'.join(
    '              <col style="width: %s" />' % w if w != 'auto' else '              <col />'
    for _, w, _ in COLS)
ths = []
for name, w, sortable in COLS:
    cls = 'giencoder-table-th' + (' giencoder-table-th-sortable' if sortable else '')
    sort_attr = ' data-sort="asc"' if sortable else ''
    sorter = '\n                <span class="giencoder-table-sorter">%s</span>' % sort_svg if sortable else ''
    ths.append('              <th class="%s"%s%s>%s%s</th>' % (cls, sort_attr, ('' if sorter else ''), name, sorter))
thead = ('            <thead>\n              <tr class="giencoder-table-tr">\n'
         + '\n'.join(ths) + '\n              </tr>\n            </thead>')

trs = []
for r in rows:
    trs.append(
        '              <tr class="giencoder-table-tr">\n'
        '                <td class="giencoder-table-td rq-td rq-td-idx">%s</td>\n'
        '                <td class="giencoder-table-td rq-td rq-td-id">%s</td>\n'
        '                <td class="giencoder-table-td rq-td rq-td-title"><span class="rq-type">%s</span><span class="rq-title-txt">%s</span></td>\n'
        '                <td class="giencoder-table-td rq-td rq-td-owner">%s</td>\n'
        '                <td class="giencoder-table-td rq-td rq-td-status"><span class="rq-status %s">%s%s</span></td>\n'
        '                <td class="giencoder-table-td rq-td rq-td-time">%s</td>\n'
        '              </tr>' % (r['idx'], r['id'], r['type'], r['title'], r['owner'],
                                 r['status_cls'], r['status_svg'], r['status_txt'], r['time']))
tbody = ('            <tbody>\n' + '\n'.join(trs) + '\n            </tbody>')

TABLE_TPL = '''        <!-- 需求表格 (restored 769:26731) —— 设计系统 Table 组件 (contract table.json v2.66.16) -->
        <div class="giencoder-table rq-table" role="table" aria-label="需求列表">
          <div class="rq-skeleton" aria-busy="true" aria-label="数据加载中">
            <div class="giencoder-skeleton rq-skel-row"><span class="giencoder-skeleton-line" style="width:40%"></span><span class="giencoder-skeleton-line" style="width:55%"></span></div>
            <div class="giencoder-skeleton rq-skel-row"><span class="giencoder-skeleton-line" style="width:40%"></span><span class="giencoder-skeleton-line" style="width:35%"></span></div>
            <div class="giencoder-skeleton rq-skel-row"><span class="giencoder-skeleton-line" style="width:40%"></span><span class="giencoder-skeleton-line" style="width:62%"></span></div>
            <div class="giencoder-skeleton rq-skel-row"><span class="giencoder-skeleton-line" style="width:40%"></span><span class="giencoder-skeleton-line" style="width:48%"></span></div>
            <div class="giencoder-skeleton rq-skel-row"><span class="giencoder-skeleton-line" style="width:40%"></span><span class="giencoder-skeleton-line" style="width:55%"></span></div>
            <div class="giencoder-skeleton rq-skel-row"><span class="giencoder-skeleton-line" style="width:40%"></span><span class="giencoder-skeleton-line" style="width:40%"></span></div>
          </div>
          <div class="giencoder-empty rq-empty">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 64 64" width="64" height="64"><rect x="8" y="14" width="48" height="36" rx="4" stroke="var(--color-border-3)" stroke-width="2"/><path d="M8 24h48" stroke="var(--color-border-3)" stroke-width="2"/><path d="M24 34h16" stroke="var(--color-border-3)" stroke-width="2" stroke-linecap="round"/></svg>
            <p class="rq-empty-text">暂无需求数据</p>
            <p class="rq-empty-desc">调整筛选条件或创建新的需求</p>
          </div>
          <div class="giencoder-table-container rq-tblscroll">
            <table class="giencoder-table-content rq-tbl">
              <colgroup>
{{COLGROUP}}
              </colgroup>
{{THEAD}}
{{TBODY}}
            </table>
          </div>
          <!-- 分页：设计系统 Pagination 组件 (contract pagination.json v2.66.16) -->
          <div class="giencoder-table-pagination rq-pager">
            <div class="giencoder-pagination" role="navigation" aria-label="分页">
              <span class="giencoder-pagination-stats">共 256 条需求</span>
              <button class="giencoder-pagination-item rq-pg-prev" type="button" aria-label="上一页" disabled>{{PREV}}</button>
              <button class="giencoder-pagination-item giencoder-pagination-item-active" type="button" aria-current="page">1</button>
              <button class="giencoder-pagination-item" type="button">2</button>
              <button class="giencoder-pagination-item" type="button">3</button>
              <button class="giencoder-pagination-item" type="button">4</button>
              <span class="giencoder-pagination-item giencoder-pagination-item-ellipsis">···</span>
              <button class="giencoder-pagination-item" type="button">32</button>
              <button class="giencoder-pagination-item rq-pg-next" type="button" aria-label="下一页">{{NEXT}}</button>
            </div>
          </div>
        </div>'''
table = (TABLE_TPL.replace('{{COLGROUP}}', colgroup)
         .replace('{{THEAD}}', thead)
         .replace('{{TBODY}}', tbody)
         .replace('{{PREV}}', prev_svg)
         .replace('{{NEXT}}', next_svg))

# ---- 4. 替换原表格段（需求表格注释 → floating action 之前）----
i0 = src.find('        <!-- 需求表格')
i1 = src.find('        <!-- floating action')
assert i0 > 0 and i1 > i0
src = src[:i0] + table + '\n' + src[i1:]
io.open(os.path.join(ROOT, '_req_html.html'), 'w', encoding='utf-8').write(src)
print('table/pager rewritten with giencoder components; rows=%d' % len(rows))

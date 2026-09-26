# -*- coding: utf-8 -*-
"""第 3 轮修复（6 项）：
1) 任务看板 select 与日历组件间隔统一 8px
2) 需求看板需求标题作为链接，hover 主题蓝
3) 需求看板表格「创建者 / 状态」互换位置并拉开距离
4) 两页组件内文字字号统一到 select 的 14px（--font-size-body-3）
5) 需求看板 .rq-stats 顶部间距对齐任务看板
6) 两页统计小卡片默认边框加深一级（border-1 -> border-2，hover -> border-3）
"""
import io, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
REQ = os.path.join(ROOT, 'pages', 'req-kanban.html')
KB = os.path.join(ROOT, 'pages', 'kanban.html')


def load(p):
    return io.open(p, encoding='utf-8').read()


def save(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


def rep(s, old, new, name):
    n = s.count(old)
    if n:
        s = s.replace(old, new)
    print(('OK  ' if n else 'MISS') + ' %-34s x%d' % (name, n), file=sys.stderr)
    return s, n


############################ 需求看板 ############################
s = load(REQ)

# --- 5) .rq-stats 顶部间距对齐任务看板（去掉 panel 多余的 48px 上内边距）---
s, _ = rep(s,
           '.rq-panel { display: flex; flex-direction: column; padding: 48px 0 12px; }',
           '.rq-panel { display: flex; flex-direction: column; padding: 0 0 12px; }',
           'rq-panel padding-top')

# --- 1) 筛选区间隔统一 8px ---
s, _ = rep(s,
           '.rq-bh-filters { display: flex; align-items: center; gap: 12px; }',
           '.rq-bh-filters { display: flex; align-items: center; gap: 8px; }',
           'rq-bh-filters gap 8px')

# --- 6) 统计小卡片默认边框加深一级 ---
s, _ = rep(s,
           'background: var(--color-bg-1); border: 1px solid var(--color-border-1);',
           'background: var(--color-bg-1); border: 1px solid var(--color-border-2);',
           'stat border-1 -> border-2')
s, _ = rep(s,
           '.rq-stat:hover { border-color: var(--color-border-2); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }',
           '.rq-stat:hover { border-color: var(--color-border-3); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }',
           'stat:hover -> border-3')
# 清掉从 kanban 复制来的失效规则
s, _ = rep(s, '      .kb-stat.is-active { box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }\n', '',
           'drop dead .kb-stat.is-active')

# --- 4) 组件内字号统一到 14px ---
s, _ = rep(s,
           '.rq-table .giencoder-table-th { height: 32px; padding: 6px 12px; background: transparent; }',
           '.rq-table .giencoder-table-th { height: 32px; padding: 6px 12px; background: transparent; font-size: var(--font-size-body-3); }',
           'table th -> 14px')
s, _ = rep(s,
           'border-radius: 4px; font-size: var(--font-size-body-1); line-height: 22px; white-space: nowrap; }',
           'border-radius: 4px; font-size: var(--font-size-body-3); line-height: 22px; white-space: nowrap; }',
           'rq-status badge -> 14px')

# --- 2) 标题链接 + 4) 日期选择器字号，追加适配 CSS ---
if '.rq-link:hover' not in s:
    s, _ = rep(s, '      /* skeleton / empty */',
               '      /* 需求标题：链接态，hover 主题蓝 */\n'
               '      .rq-link { cursor: pointer; color: var(--color-text-1); text-decoration: none; transition: color var(--transition-duration-1); }\n'
               '      .rq-link:hover { color: var(--color-primary-6); }\n'
               '      /* 组件内文字与 Select 保持全局统一（14px / --font-size-body-3） */\n'
               '      .rq-dp-lbl { flex: none; color: var(--color-neutral-7); font-size: var(--font-size-body-3); line-height: 20px; white-space: nowrap; }\n'
               '      .rq-bh-filters .giencoder-date-picker .giencoder-input { font-size: var(--font-size-body-3); }\n'
               '      /* skeleton / empty */',
               'append rq-link + font CSS')

# --- 4) 日期选择器行内 13px 清掉，改由适配层统一 ---
s, _ = rep(s,
           '<span class=\\"kb-lbl\\" style=\\"color:var(--color-neutral-7); font-size:13px; line-height:20px; white-space:nowrap; flex:none;\\">今天：</span>',
           '<span class=\\"kb-lbl rq-dp-lbl\\">今天：</span>',
           'datepicker label -> rq-dp-lbl')
s, _ = rep(s, ' readonly style=\\"font-size:13px;\\">', ' readonly>', 'datepicker input inline 13px')

# --- 2) 需求标题 -> 链接 ---
s, n_title = rep(s, '<span class=\\"rq-title-txt\\">',
                 '<span class=\\"rq-title-txt rq-link\\" role=\\"link\\" tabindex=\\"0\\">',
                 'title -> link')

# --- 3) 创建者 / 状态 互换 + 拉开距离 ---
s, _ = rep(s,
           '<col style=\\"width: 68px\\" />", "              <col style=\\"width: 270px\\" />',
           '<col style=\\"width: 150px\\" />", "              <col style=\\"width: 130px\\" />',
           'colgroup: status 150 / owner 130')

# 表头互换：定位「创建者」th 与「状态」th，整段 [创建者 + 分隔 + 状态] 替换为 [状态 + 分隔 + 创建者]
A = '<th class=\\"giencoder-table-th\\">创建者</th>'
a0 = s.find(A)
b0 = s.find('<th class=\\"giencoder-table-th giencoder-table-th-sortable\\" data-sort=\\"asc\\">状态', a0)
b1 = s.find('</th>', b0) + len('</th>')
if a0 > 0 and b0 > a0 and b1 > b0:
    status_th = s[b0:b1]
    sep = s[a0 + len(A):b0]
    s = s[:a0] + status_th + sep + A + s[b1:]
    print('OK   %-34s x1' % 'thead swap status/owner', file=sys.stderr)
else:
    print('MISS %-34s a0=%d b0=%d b1=%d' % ('thead swap status/owner', a0, b0, b1), file=sys.stderr)

# 数据行：owner 与 status 单元格互换
pat_td = re.compile(
    r'(<td class=\\"giencoder-table-td rq-td rq-td-owner\\">.*?</td>)(.*?)(<td class=\\"giencoder-table-td rq-td rq-td-status\\">.*?</td>)',
    re.S)
s, n_td = pat_td.subn(lambda m: m.group(3) + m.group(2) + m.group(1), s)
print(('OK  ' if n_td else 'MISS') + ' %-34s x%d' % ('tbody swap owner/status', n_td), file=sys.stderr)

save(REQ, s)

############################ 任务看板 ############################
k = load(KB)

# --- 1) select 与日历组件间隔 8px（120 + 112 + 8 = 240）---
k, _ = rep(k,
           'style=\\"position:absolute; left:229px; top:0; width:250px;\\"',
           'style=\\"position:absolute; left:240px; top:0; width:250px;\\"',
           'datepicker left 229 -> 240')

# --- 6) 统计小卡片默认边框加深一级 ---
k, _ = rep(k,
           'background: var(--color-bg-1); border: 1px solid var(--color-border-1);',
           'background: var(--color-bg-1); border: 1px solid var(--color-border-2);',
           'stat border-1 -> border-2')
k, _ = rep(k,
           '.kb-stat:hover { border-color: var(--color-border-2); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }',
           '.kb-stat:hover { border-color: var(--color-border-3); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }',
           'stat:hover -> border-3')

# --- 4) 组件内字号统一（日期选择器 + 泳道计数）---
k, _ = rep(k,
           '<span class=\\"kb-lbl\\" style=\\"color:var(--color-neutral-7); font-size:13px; line-height:20px; white-space:nowrap; flex:none;\\">本月：</span>',
           '<span class=\\"kb-lbl rq-dp-lbl\\">本月：</span>',
           'datepicker label -> rq-dp-lbl')
k, _ = rep(k, ' readonly style=\\"font-size:13px;\\">', ' readonly>', 'datepicker input inline 13px')
k, _ = rep(k,
           '.kb-col-cnt { color: var(--color-text-3); font-size: 13px; line-height: 20px; }',
           '.kb-col-cnt { color: var(--color-text-3); font-size: var(--font-size-body-3); line-height: 20px; }',
           'kb-col-cnt -> 14px')

if '.rq-dp-lbl {' not in k:
    k, _ = rep(k,
               '      .kb-boardhead .giencoder-select-view-text { flex: 1; min-width: 0; }\n',
               '      .kb-boardhead .giencoder-select-view-text { flex: 1; min-width: 0; }\n'
               '      /* 组件内文字与 Select 保持全局统一（14px / --font-size-body-3） */\n'
               '      .rq-dp-lbl { flex: none; color: var(--color-neutral-7); font-size: var(--font-size-body-3); line-height: 20px; white-space: nowrap; }\n'
               '      .kb-boardhead .giencoder-date-picker .giencoder-input { font-size: var(--font-size-body-3); }\n',
               'append font CSS')

save(KB, k)

print('--- req diagnose ---', file=sys.stderr)
s = load(REQ)
print('rq-panel padding: %s' % re.search(r'\.rq-panel \{[^}]*\}', s).group()[:90], file=sys.stderr)
print('link=%d  rq-dp-lbl=%d  th14=%d  badge14=%d' % (
    s.count('rq-title-txt rq-link'),
    s.count('rq-dp-lbl'),
    s.count('background: transparent; font-size: var(--font-size-body-3);'),
    s.count('border-radius: 4px; font-size: var(--font-size-body-3); line-height: 22px'),
), file=sys.stderr)
print('thead order: %s' % re.findall(r'<th class=\\"giencoder-table-th[^"]*\\">([^<\\"]{2,6})', s), file=sys.stderr)
print('DONE')

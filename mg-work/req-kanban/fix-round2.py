# -*- coding: utf-8 -*-
# 三项修复（req + kanban）：
# 1. select 错位：去掉行内 style 强改（size=small 走契约 28px）、popup 宽度跟触发框、kb-lbl 移出 .giencoder-select
# 2. rq-stat / kb-stat 的 is-active 改为 :hover
# 3. 需求看板表格 → 设计系统 Table borderless 变体（开放式：无外框无圆角，保留行间分割线）
import io, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.abspath(os.path.join(ROOT, '..', '..', 'pages'))


def clean_select(markup):
    """把 Select 的行内布局 style 收敛为 size 属性，标签保留但移出组件类元素。"""
    # 1) 容器：去掉 width 行内（由视图层 CSS 给），保留 data-size
    markup = re.sub(
        r'(class="giencoder-select[^"]*"[^>]*?)\s*style="[^"]*"\s*>',
        lambda m: m.group(1) + '>', markup)
    markup = markup.replace('data-size="small"', 'data-size="small"')
    # 2) view：去掉所有行内 style（size=small 契约 = 28px / padding 0 8px 0 12px / radius 6px）
    markup = re.sub(
        r'(<div class="giencoder-select-view"[^>]*?)\s*style="[^"]*"',
        lambda m: m.group(1), markup)
    # 3) 标签：保留文本，交给视图层用容器 :first-child 样式化（不塞在组件 view 里）
    markup = re.sub(
        r'<span class="kb-lbl"[^>]*>(.*?)</span>\s*',
        lambda m: '<span class="rq-sel-lbl">%s</span>\n              ' % m.group(1), markup)
    # 4) 值文本：去掉行内 style
    markup = re.sub(
        r'(<span class="giencoder-select-view-text"[^>]*?)\s*style="[^"]*"',
        lambda m: m.group(1), markup)
    return markup


# ---------- 1. 处理 _req_html.html ----------
src_path = os.path.join(ROOT, '_req_html.html')
src = io.open(src_path, encoding='utf-8').read()

# 1a. select 收敛（类型 / 状态 两个）——幂等：已清理则跳过
i0 = src.find('<div class="giencoder-select')
while i0 > 0 and 'rq-sel-lbl' not in src[i0:i0+2500]:
    i1 = src.find('<!-- 日期选择', i0)
    if i1 < 0:
        i1 = src.find('<div class="giencoder-date-picker', i0)
    block = src[i0:i1]
    new_block = clean_select(block)
    # 清理块尾多余的空白行
    new_block = re.sub(r'\n\s*\n\s*$', '\n', new_block)
    src = src[:i0] + new_block + src[i1:]
    i0 = src.find('<div class="giencoder-select', i1)

# 1b. 表格 → borderless 变体
src = src.replace('<div class="giencoder-table rq-table"',
                  '<div class="giencoder-table giencoder-table-borderless rq-table"')
# borderless：去掉容器自身的白底/边框/圆角，仅由外层卡片承载
src = src.replace('<div class="giencoder-table-container rq-tblscroll">',
                  '<div class="giencoder-table-container rq-tblscroll giencoder-table-container--borderless">')

# 1c. is-active → 仅保留为 hover 目标（视觉由 CSS 的 :hover 提供，去掉内联 is-active 语义）
src = src.replace('rq-stat rq-stat--todo is-active', 'rq-stat rq-stat--todo')

io.open(src_path, 'w', encoding='utf-8').write(src)
print('_req_html.html: select cleaned + table borderless + is-active removed')

# ---------- 2. 视图层 CSS 适配（写入 build-inject 的 RQ_CSS 源） ----------
bi = os.path.join(ROOT, 'build-inject.py')
s = io.open(bi, encoding='utf-8').read()

OLD_TABLE_CSS = '''      /* 表格：giencoder Table 组件 + 视图适配（矩形486 白底圆角8，容器裁切） */
      .rq-table {
        flex: 1; min-height: 0; display: flex; flex-direction: column; margin: 15px 20px 0;
        background: var(--color-bg-1); border: 1px solid var(--color-border-1); border-radius: 8px; overflow: hidden;
      }
      .rq-tblscroll { flex: 1; min-height: 0; }
      .rq-tbl { table-layout: fixed; min-width: 940px; }
      /* 表头底：设计稿 #FAFAFA（组件默认 --color-fill-1），行高 36 */
      .rq-table .giencoder-table-th { background: #FAFAFA; }
      .rq-table .giencoder-table-td { height: 36px; padding: 6px 12px; }
      /* stripe 变体：隔行变色（table.json variant=stripe） */
      .rq-table tbody .giencoder-table-tr:nth-child(even) .giencoder-table-td { background: var(--color-fill-1); }
      .rq-table tbody .giencoder-table-tr:hover .giencoder-table-td { background: var(--color-fill-1); }'''

NEW_TABLE_CSS = '''      /* 表格：设计系统 Table / borderless 变体（开放式：无外边框、无圆角、无斑马纹，仅行间分割线） */
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
      .rq-table tbody .giencoder-table-tr:hover .giencoder-table-td { background: var(--color-fill-1); }'''

if OLD_TABLE_CSS in s:
    s = s.replace(OLD_TABLE_CSS, NEW_TABLE_CSS)
elif 'borderless 变体' not in s:
    raise AssertionError('table css block not found')

# 追加 select 适配样式 + stat hover
OLD_STAT = '      .rq-stat:hover, .rq-stat.is-active { border-color: var(--color-border-2); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }'
NEW_STAT = '      /* is-active 仅是 hover 态：默认无投影，悬停才深一级边框 + 浅投影 */\n      .rq-stat:hover { border-color: var(--color-border-2); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }'
if OLD_STAT in s:
    s = s.replace(OLD_STAT, NEW_STAT)
elif '.rq-stat:hover { border-color' not in s:
    raise AssertionError('stat hover block not found')

# select 错位适配：popup 宽度跟触发框、标签独立样式
OLD_BH = '      .rq-bh-filters .giencoder-select, .rq-bh-filters .giencoder-date-picker { position: relative; flex: none; }'
NEW_BH = '''      .rq-bh-filters .giencoder-select, .rq-bh-filters .giencoder-date-picker { position: relative; flex: none; }
      .rq-bh-filters .giencoder-select[data-size="small"] .giencoder-select-view { min-height: 28px; height: 28px; padding: 0 8px 0 12px; border-radius: 6px; }
      /* popup 宽度跟随触发框（覆盖组件默认 min-width:200px，避免 101px 触发框被撑开错位） */
      .rq-bh-filters .giencoder-select .giencoder-select-popup { width: auto; min-width: 100%; }
      .rq-bh-filters .giencoder-select-view { gap: 4px; justify-content: flex-start; }
      .rq-bh-filters .giencoder-select-view .rq-sel-lbl { flex: none; color: var(--color-neutral-7); }
      .rq-bh-filters .giencoder-select-view-text { flex: 1; min-width: 0; }'''
if OLD_BH in s:
    s = s.replace(OLD_BH, NEW_BH)
elif 'rq-sel-lbl' not in s:
    raise AssertionError('select fit block not found')
io.open(bi, 'w', encoding='utf-8').write(s)
print('build-inject.py: table borderless + stat hover + select fit patched')

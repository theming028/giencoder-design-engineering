# -*- coding: utf-8 -*-
# kanban.html 同步修复：select 错位 + is-active → hover
import io, os, sys

P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pages', 'kanban.html'))
s = io.open(P, encoding='utf-8').read()
print('loaded', len(s), flush=True)

# --- 1. select 收敛：清掉 view 行内布局 style（size=small 走契约 28px）---
i0 = s.find('class=\\"giencoder-select kb-type-select')
guard = 0
while i0 > 0 and 'rq-sel-lbl' not in s[i0:i0 + 2600] and guard < 3:
    guard += 1
    start = s.rfind('<div class=\\"giencoder-select', 0, i0)
    end = s.find('<!-- 日期选择', i0)
    if end < 0:
        end = s.find('<div class=\\"giencoder-date-picker', i0)
    print('block', start, end, flush=True)
    block = s[start:end]
    before = block
    block = block.replace(' style=\\"position:absolute; left:120px; top:0; width:101px;\\"', '')
    block = block.replace(' style=\\"min-height:28px; height:28px; padding:0 8px 0 12px; border-radius:6px; font-size:13px;\\"', '')
    block = block.replace(' style=\\"font-size:13px; flex:none; padding-right:4px;\\"', '')
    block = block.replace(
        '<span class=\\"kb-lbl\\" style=\\"color:var(--color-neutral-7); font-size:13px; line-height:20px; white-space:nowrap; flex:none;\\">类型：</span>',
        '<span class=\\"rq-sel-lbl\\">类型：</span>')
    print('changed:', block != before, '| has lbl span:', 'rq-sel-lbl' in block, flush=True)
    if block == before:
        # 行内样式字符串不匹配：直接无条件替换 kb-lbl 为 rq-sel-lbl
        block = block.replace('class=\\"kb-lbl\\"', 'class=\\"rq-sel-lbl\\"')
        print('fallback lbl replace:', 'rq-sel-lbl' in block, flush=True)
    s = s[:start] + block + s[end:]
    i0 = s.find('class=\\"giencoder-select kb-type-select', start + 120)

# --- 2. is-active 移除（视觉交给 :hover）---
s = s.replace('kb-stat kb-stat--coop is-active', 'kb-stat kb-stat--coop')

# --- 3. CSS：stat hover + select 适配 ---
OLD_STAT = '      .kb-stat.is-active { box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }'
NEW_STAT = ('      /* is-active 仅是 hover 态：默认无投影；悬停才深一级边框 + 浅投影 */\n'
            '      .kb-stat:hover { border-color: var(--color-border-2); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }')
ADD = ('      /* select 错位修复：标签独立、popup 跟随触发框宽度 */\n'
       '      .kb-boardhead .giencoder-select[data-size="small"] .giencoder-select-view { min-height: 28px; height: 28px; padding: 0 8px 0 12px; border-radius: 6px; }\n'
       '      .kb-boardhead .giencoder-select .giencoder-select-popup { width: auto; min-width: 100%; }\n'
       '      .kb-boardhead .giencoder-select-view { gap: 4px; justify-content: flex-start; }\n'
       '      .kb-boardhead .giencoder-select-view .rq-sel-lbl { flex: none; color: var(--color-neutral-7); }\n'
       '      .kb-boardhead .giencoder-select-view-text { flex: 1; min-width: 0; }\n')

if OLD_STAT in s:
    s = s.replace(OLD_STAT, NEW_STAT, 1)
    print('stat css replaced', flush=True)
else:
    print('STAT CSS NOT FOUND', flush=True)

if ADD not in s:
    anchor = s.find('      .kb-boardhead ')
    if anchor > 0:
        s = s[:anchor] + ADD + s[anchor:]
        print('select css added', flush=True)
    else:
        print('BOARDHEAD ANCHOR NOT FOUND', flush=True)

io.open(P, 'w', encoding='utf-8').write(s)
print('DONE rq-sel-lbl=%d is-active=%d stat:hover=%d' % (s.count('rq-sel-lbl'), s.count('is-active'), s.count('.kb-stat:hover')), flush=True)

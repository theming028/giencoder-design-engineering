# -*- coding: utf-8 -*-
"""第 4 轮修复（5 项）：
1) 日历浮窗投影与 select 下拉统一（全局规范）
2) 需求看板页码栏：白底 + main 容器底部居中 + 去掉底部间距（贴边）
3) 表格表头字号回到设计系统统一的 12px
4) 表格加圆角 8px + 四边 1px 边框（对照 MasterGo 实测：左边框 x=29、上边框 y=265、
   下边框 y=485、左上圆角收敛于 y265→312），表头透明底
5) 类型标签 rq-type 按需求类型着色
"""
import io, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
REQ = os.path.join(ROOT, 'pages', 'req-kanban.html')
KB = os.path.join(ROOT, 'pages', 'kanban.html')

# select 下拉的投影（全局基线）
SHADOW = 'box-shadow: 0 8px 20px #0000001a;'


def load(p):
    return io.open(p, encoding='utf-8').read()


def save(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


def rep(s, old, new, name):
    n = s.count(old)
    if n:
        s = s.replace(old, new)
    print(('OK  ' if n else 'MISS') + ' %-36s x%d' % (name, n), file=sys.stderr)
    return s, n


print('########## req-kanban.html ##########', file=sys.stderr)
s = load(REQ)

# ---------- 1) 日历浮窗投影与 select 统一 ----------
s, _ = rep(s,
           'border-radius: var(--border-radius-large); box-shadow: var(--shadow2-down);',
           'border-radius: var(--border-radius-large); box-shadow: 0 8px 20px #0000001a;',
           'datepicker popup shadow -> select')

# ---------- 3) 表头字号回到 12px（组件统一值）----------
s, _ = rep(s,
           '.rq-table .giencoder-table-th { height: 32px; padding: 6px 12px; background: transparent; font-size: var(--font-size-body-3); }',
           '.rq-table .giencoder-table-th { height: 32px; padding: 6px 12px; background: transparent; font-size: var(--font-size-body-1); }',
           'table th -> 12px')

# ---------- 4) 表格：圆角 + 四边边框 ----------
# 容器：加圆角与四边边框；表头底分割线加深到 border-2（设计稿 #E5E5E5）
s, _ = rep(s,
           '      .rq-tblscroll { flex: 1; min-height: 0; }',
           '      /* 表格容器：四边 1px 边框 + 圆角（设计稿实测 左边框 x=29 / 上边框 y=265 / 下边框 y=485 / 圆角 8px） */\n'
           '      .rq-tblscroll {\n'
           '        flex: 1; min-height: 0;\n'
           '        border: 1px solid var(--color-border-1); border-radius: var(--border-radius-large);\n'
           '        background: var(--color-bg-1);\n'
           '      }',
           'table container border+radius')
s, _ = rep(s,
           '.rq-table.giencoder-table-borderless .giencoder-table-th {\n        background: transparent; border-bottom: 1px solid var(--color-border-1);\n      }',
           '.rq-table.giencoder-table-borderless .giencoder-table-th {\n'
           '        background: transparent; border-bottom: 1px solid var(--color-border-2);\n'
           '      }',
           'th bottom line -> border-2')
# 末行去掉底边（容器已有边框）
s, _ = rep(s,
           '.rq-table .giencoder-table-tr:last-child .giencoder-table-td { border-bottom: none; }',
           '.rq-table .giencoder-table-tr:last-child .giencoder-table-td { border-bottom: none; }\n'
           '      /* 圆角裁切：首行表头/末行的圆角随容器 */\n'
           '      .rq-tblscroll .giencoder-table-content { border-radius: inherit; overflow: hidden; }',
           'table content radius')
# 表头无底色（设计稿实测表头区为纯白）—— 已有 transparent，补充移除组件 fill
s, _ = rep(s,
           '.rq-table .giencoder-table-th { height: 32px; padding: 6px 12px; background: transparent; font-size: var(--font-size-body-1); }',
           '.rq-table .giencoder-table-th { height: 32px; padding: 6px 12px; background: transparent; font-size: var(--font-size-body-1); border-top: none; }',
           'th no top border')

# ---------- 2) 页码栏：白底 + 底部居中 + 贴边 ----------
s, _ = rep(s,
           '      .rq-pager {\n'
           '        flex: none; display: flex; align-items: center; height: 48px; padding: 0 16px;\n'
           '        background: #FAFAFA; border-top: 1px solid var(--color-border-1);\n'
           '      }',
           '      /* 页码栏：白底、无边框、内容居中 */\n'
           '      .rq-pager {\n'
           '        flex: none; display: flex; align-items: center; justify-content: center; height: 48px;\n'
           '        padding: 0 16px; background: var(--color-bg-1); border-top: none;\n'
           '      }',
           'pager white + center')
s, _ = rep(s,
           '      .rq-pager .giencoder-pagination { flex: 1; }',
           '      .rq-pager .giencoder-pagination { flex: none; }',
           'pager pagination not flex:1')
# 贴边：面板底内边距归零
s, _ = rep(s,
           '.rq-panel { display: flex; flex-direction: column; padding: 0 0 12px; }',
           '.rq-panel { display: flex; flex-direction: column; padding: 0; }',
           'rq-panel padding-bottom 0')

# ---------- 5) 类型标签着色 ----------
if '.rq-type--req' not in s:
    s, _ = rep(s,
               '      .rq-type { margin-right: 8px; color: var(--color-neutral-7); }',
               '      /* 类型标签：按需求类型着色（胶囊，浅底 + 彩色文字） */\n'
               '      .rq-type {\n'
               '        display: inline-flex; align-items: center; margin-right: 8px; padding: 0 6px;\n'
               '        height: 20px; border-radius: 4px; font-size: var(--font-size-body-1); line-height: 20px;\n'
               '        white-space: nowrap; flex: none;\n'
               '      }\n'
               '      .rq-type--req { background: #E3EEFF; color: #3770F7; }\n'
               '      .rq-type--item { background: #F0EBFF; color: #7766FD; }\n'
               '      .rq-type--entry { background: #FFECD9; color: #F3881E; }',
               'rq-type colors')

# 按类型打上修饰类
s, n = rep(s, '<span class=\\"rq-type\\">需求项</span>', '<span class=\\"rq-type rq-type--item\\">需求项</span>', 'type=需求项 -> item')
s, n2 = rep(s, '<span class=\\"rq-type\\">需求条目</span>', '<span class=\\"rq-type rq-type--entry\\">需求条目</span>', 'type=需求条目 -> entry')
s, n3 = rep(s, '<span class=\\"rq-type\\">需求</span>', '<span class=\\"rq-type rq-type--req\\">需求</span>', 'type=需求 -> req')

save(REQ, s)
print('--- req diagnose ---', file=sys.stderr)
s = load(REQ)
print('pill=%d item=%d entry=%d req=%d' % (
    s.count('rq-type--item'), s.count('rq-type--entry'), s.count('rq-type--req'),
    s.count('<span class=\\"rq-type ')), file=sys.stderr)

print('########## kanban.html ##########', file=sys.stderr)
k = load(KB)

# ---------- 1) 日历浮窗投影与 select 统一 ----------
k, _ = rep(k,
           'border-radius: var(--border-radius-large); box-shadow: var(--shadow2-down);',
           'border-radius: var(--border-radius-large); box-shadow: 0 8px 20px #0000001a;',
           'datepicker popup shadow -> select')

# 日期选择浮窗宽度对齐触发框（与 select popup 同规范）
if '.kb-boardhead .giencoder-date-picker .giencoder-date-picker-popup' not in k:
    k, _ = rep(k,
               '      .kb-boardhead .giencoder-date-picker .giencoder-input { font-size: var(--font-size-body-3); }',
               '      .kb-boardhead .giencoder-date-picker .giencoder-input { font-size: var(--font-size-body-3); }\n'
               '      /* 浮窗投影与 select 下拉统一（全局规范） */\n'
               '      .giencoder-date-picker-popup { box-shadow: 0 8px 20px #0000001a; }',
               'datepicker popup shadow rule (kb)')

save(KB, k)

print('--- kanban diagnose ---', file=sys.stderr)
k = load(KB)
print('shadow unified=%d  shadow2down left=%d' % (
    k.count('box-shadow: 0 8px 20px #0000001a;'), k.count('var(--shadow2-down)')), file=sys.stderr)
print('DONE')

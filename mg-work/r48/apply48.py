#!/usr/bin/env python3
# 第 48 轮：① 波点灰度化（base/dev 等 6 页 main 容器）② 会话栏与文件栏连成一体
#          ③ .td-browse-bar 补底部发丝线 ④ .td-browse-tree 内间距 20px
#
# 设计稿依据：节点 1350:18310 导出图 1190x1266 = 节点 793.3x844（缩放正好 1.5x）逐像素实测：
#   · 顶栏底线   node y 39~40，墨量合计 30/1.5 → 等效色 #EBEBEB（= 项目既有"结构发丝线"色）
#                项目既有约定：设计稿结构发丝线 #EBECED → 统一取 --td-hairline(=--color-border-1)
#   · 树/码分隔  node x 296.5 一条 1px 线（与 .td-browse 左边缘同为发丝线）
#   · 树容器     内间距 20px：搜索框外框 node x 20.0 ~ 275.3（宽 255.3≈256）→ 296 = 20 + 256 + 20
#                「文件目录」墨迹起点 28.7 = 20 + 8(+字距)，行缩进起点 30 = 20 + 8 + 2(箭头字距)
#                即：容器 padding 20，内部沿用既有 8px 内缩与 20px 缩进步长
import os, re, sys, shutil

ROOT = '/Users/shaoyuming/Documents/GienCoderDesignEngineering'
BK = '/tmp/r48-backup'
os.makedirs(BK, exist_ok=True)

DOT_OLD = 'radial-gradient(circle, rgba(55, 112, 247, 0.1) 1.5px, transparent 1.5px)'
DOT_NEW = 'radial-gradient(circle, rgba(var(--gray-7), 0.1) 1.5px, transparent 1.5px)'
# 说明：只换色相、不动明度 —— rgba(107,107,107,.1) 叠加白底后亮度与 rgba(55,112,247,.1) 等价
DOT_PAGES = ['base', 'dev', 'kanban', 'req-kanban', 'settings', 'task-detail']

TD = os.path.join(ROOT, 'pages/task-detail.html')
SUBS = [
    # ---- 第 2 项：去掉 8px 缝 + 左直边 + 一条发丝线（与右侧面板连成一体）----
    ('        flex-direction: column; overflow: hidden; margin-left: 8px;\n'
     '        background: var(--color-bg-1); border-radius: 8px; box-shadow: var(--td-panel-shadow);',
     '        flex-direction: column; overflow: hidden;\n'
     '        background: var(--color-bg-1); border-left: 1px solid var(--td-hairline);\n'
     '        border-radius: 0 8px 8px 0; box-shadow: var(--td-panel-shadow);'),
    # ---- 第 2 项：会话栏接缝侧改直角（仅展开态生效）----
    ('      .td-root.is-browse .td-left { display: none; }',
     '      /* 第 48 轮第 2 项：会话栏与文件预览栏连成一体 —— 接缝两侧直角，中间一条发丝线 */\n'
     '      .td-root.is-browse .td-right { border-top-right-radius: 0; border-bottom-right-radius: 0; }\n'
     '      .td-root.is-browse .td-left { display: none; }'),
    # ---- 第 3 项：顶栏底部发丝线 ----
    ('      .td-browse-bar {\n'
     '        height: 40px; flex: none; box-sizing: border-box;\n'
     '        display: flex; align-items: center; gap: 8px; padding: 4px 16px;\n'
     '      }',
     '      .td-browse-bar {\n'
     '        height: 40px; flex: none; box-sizing: border-box;\n'
     '        display: flex; align-items: center; gap: 8px; padding: 4px 16px;\n'
     '        border-bottom: 1px solid var(--td-hairline);\n'
     '      }'),
    # ---- 第 4 项：树容器内间距 20px（宽度 256→296 以保住设计稿的 256 内容宽）----
    ('        flex: none; width: 256px; box-sizing: border-box; padding: 4px 0 8px;\n'
     '        display: flex; flex-direction: column; gap: 8px; overflow: auto;',
     '        flex: none; width: 296px; box-sizing: border-box; padding: 20px;\n'
     '        display: flex; flex-direction: column; gap: 8px; overflow: auto;'),
    # ---- 第 4 项：搜索框改由容器 padding 定位（原 8px margin 会变成 20+8=28）----
    ('        margin: 0 8px; height: 32px; flex: none; box-sizing: border-box;',
     '        margin: 0; height: 32px; flex: none; box-sizing: border-box;'),
]

fails = []

# ============ 一、波点灰度化 ============
for p in DOT_PAGES:
    f = os.path.join(ROOT, 'pages/%s.html' % p)
    shutil.copy2(f, os.path.join(BK, 'pages__%s.html' % p))
    s = open(f, encoding='utf-8').read()
    if '--gray-7:' not in s:
        fails.append('%s: 缺 --gray-7 token' % p); continue
    n_old, n_new = s.count(DOT_OLD), s.count(DOT_NEW)
    if n_old == 0 and n_new > 0:
        print('  %-11s 波点: idem (灰度 x%d)' % (p, n_new)); continue
    if n_old == 0:
        fails.append('%s: 未找到波点声明' % p); continue
    s = s.replace(DOT_OLD, DOT_NEW)
    open(f, 'w', encoding='utf-8').write(s)
    chk = open(f, encoding='utf-8').read()
    bad = chk.count('rgba(55, 112, 247, 0.1) 1.5px')
    if bad or chk.count(DOT_NEW) != n_old:
        fails.append('%s: 替换后残留 %d / 新值 %d (期望 %d)' % (p, bad, chk.count(DOT_NEW), n_old))
    print('  %-11s 波点: 蓝→灰 x%d' % (p, n_old))

# ============ 二~四、task-detail ============
shutil.copy2(TD, os.path.join(BK, 'td-r48.html'))
s = open(TD, encoding='utf-8').read()
hits = []
for old, new in SUBS:
    if new in s and old not in s:
        hits.append('idem'); continue
    n = s.count(old)
    hits.append(str(n))
    if n != 1:
        fails.append('锚点异常 x%d: %r' % (n, old[:60])); continue
    s = s.replace(old, new, 1)
if not fails:
    open(TD, 'w', encoding='utf-8').write(s)
print('  task-detail 命中:', ','.join(hits))

# ============ 自检（只在「第 47 轮第 2 项」新增区块内断言）============
if not fails:
    c = open(TD, encoding='utf-8').read()
    a = c.find('/* ★ 第 47 轮第 2 项')
    b = c.find('.td-chat {', a)
    blk = c[a:b] if 0 <= a < b else ''
    if not blk:
        fails.append('未能切出 .td-browse 区块')
    else:
        for need in ['border-left: 1px solid var(--td-hairline)',
                     'border-bottom: 1px solid var(--td-hairline)',
                     'border-radius: 0 8px 8px 0',
                     'width: 296px', 'padding: 20px',
                     'margin: 0; height: 32px',
                     '.td-root.is-browse .td-right']:
            if need not in blk:
                fails.append('区块内缺少: %s' % need)
        for bad in ['margin-left: 8px', 'width: 256px', 'margin: 0 8px']:
            if bad in blk:
                fails.append('区块内残留: %s' % bad)
        o = open(os.path.join(BK, 'td-r48.html'), encoding='utf-8').read()
        for k in ['<style', '</style>', '<script', '</script>']:
            if c.count(k) != o.count(k):
                fails.append('结构漂移 %s' % k)
        print('  区块自检: 长度 %d / 波点残留 %d' % (len(blk), c.count(DOT_OLD)))

print('FAIL: ' + ' | '.join(fails) if fails else 'OK')
sys.exit(1 if fails else 0)

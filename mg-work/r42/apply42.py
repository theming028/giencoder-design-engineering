#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r42 · 链接图标 + 全站导航兜底
① task-detail.html：.td-attr-link 去掉前置链接图标 + 文字加下划线
② 9 个外壳页注入 SHELL-NAV-FIX v5（hashchange → 真跳转），修「点击无响应」
③ kanban.html / req-kanban.html 的 Tt() 补「非 file 协议按文件名回退」（同 r39 dev.html）
幂等 + 自检。
"""
import re, sys, shutil, os

PAGES = ['automation', 'avatar', 'base', 'dev', 'kanban', 'req-kanban', 'settings', 'skills', 'task-detail']
TD = 'pages/task-detail.html'
BAKDIR = '/tmp/r42-backup'
os.makedirs(BAKDIR, exist_ok=True)

ROUTE_JS = """    <!-- SHELL-NAV-FIX v5 —— 外壳导航通用兜底（公共模块修复，勿手改此块）
         背景：外壳 navigate() 在 http 下只改 hash 且无 hashchange 监听 → 侧栏「数字分身/自动化/技能/设置」、
         看板卡片、dev 页「进入研发工作台」等点击后 URL 变成 base.html#/avatar 但页面不动（「点了没反应」）。
         修复：监听 hashchange，把 #/route 还原成真实文件名跳转。用相对路径 → file:// 与 http 预览
         （/static-html/<id>/<file>）都能正确解析到同目录文件。
         路由表取全站并集：/task-detail 不在任何单页的 xt 里，只有本兜底能接住。 -->
    <script>
      (function () {
        var ROUTE = { '/': 'base.html', '/base': 'base.html', '/dev': 'dev.html', '/kanban': 'kanban.html',
                      '/req-kanban': 'req-kanban.html', '/task-detail': 'task-detail.html', '/avatar': 'avatar.html',
                      '/automation': 'automation.html', '/skills': 'skills.html', '/settings': 'settings.html' };
        var here = location.pathname.split('/').pop() || '';
        function go() {
          var r = location.hash.replace(/^#/, '').split('?')[0];
          if (!r) return;
          if (r.charAt(0) !== '/') r = '/' + r;
          var f = ROUTE[r];
          if (f && f !== here) location.replace(f);
        }
        window.addEventListener('hashchange', go);
        go();
      })();
    </script>
"""

# ---------- ① 链接图标 + 下划线 ----------
E1_OLD = '.td-attr-link { display: inline-flex; align-items: center; gap: 4px; color: var(--td-strong); text-decoration: none; min-width: 0; }'
E1_NEW = '.td-attr-link { display: inline-flex; align-items: center; gap: 4px; color: var(--td-strong); text-decoration: underline; text-underline-offset: 2px; min-width: 0; }'
E2_OLD = '.td-attr-link svg { width: 14px; height: 14px; flex: none; color: var(--td-ink-2); }'
E2_NEW = '.td-attr-link svg { display: none; }   /* ★ 第 42 轮：链接不再带前置图标 */'
E3_OLD = ('      .td-side .td-attr-row.is-wrap .td-attr-link svg {\n'
          '        display: inline-block; vertical-align: -2px; margin-right: 4px;\n'
          '      }\n')
E3_NEW = ('      .td-side .td-attr-row.is-wrap .td-attr-link svg {\n'
          '        display: none;   /* ★ 第 42 轮：去掉链接前置图标（原 inline-block + 垂直微调） */\n'
          '      }\n')

# ---------- ③ 路由兜底 ----------
TT_OLD = 'function Tt(){return St[window.location.pathname.split(`/`).pop()||``]||(Ct()?`/`:N())}'
TT_NEW = 'function Tt(){let p=window.location.pathname.split(`/`).pop()||``,f=St[p];return Ct()?f||`/`:(N()!==`/`?N():(f||`/`))}'

fails = []

# ---- ① task-detail.html ----
s = open(TD, encoding='utf-8').read()
if '第 42 轮：链接不再带前置图标' not in s:
    shutil.copy2(TD, f'{BAKDIR}/task-detail.html')
    for old, new, tag in [(E1_OLD, E1_NEW, '1a 下划线'), (E2_OLD, E2_NEW, '1b 通用 svg 隐藏'), (E3_OLD, E3_NEW, '1c is-wrap svg 隐藏')]:
        n = s.count(old)
        if n != 1:
            fails.append(f'{tag}: anchor count {n}'); continue
        s = s.replace(old, new, 1); print(f'  {tag}: ok')
    if 'text-decoration: underline' not in s or 'display: inline-block; vertical-align: -2px' in s:
        fails.append('1: 自检失败')
    open(TD, 'w', encoding='utf-8').write(s)
else:
    print('  ① 已应用，跳过')

# ---- ② + ③ 逐页 ----
for name in PAGES:
    f = f'pages/{name}.html'
    t = open(f, encoding='utf-8').read()
    orig = t
    acts = []
    if 'SHELL-NAV-FIX v5' not in t:
        i = t.find('<!-- SHELL-TABS-FIX')
        if i < 0:
            fails.append(f'{name}: 找不到 TABS 注入块'); continue
        j = t.find('</script>', i)
        if j < 0:
            fails.append(f'{name}: TABS 块未闭合'); continue
        j += len('</script>')
        t = t[:j] + '\n\n' + ROUTE_JS.rstrip('\n') + t[j:]
        acts.append('nav-fix')
    if name in ('kanban', 'req-kanban') and 'N()!==`/`?N()' not in t:
        if t.count(TT_OLD) != 1:
            fails.append(f'{name}: Tt 锚点数 {t.count(TT_OLD)}')
        else:
            t = t.replace(TT_OLD, TT_NEW, 1)
            acts.append('router')
    if t != orig:
        if not os.path.exists(f'{BAKDIR}/{name}.html'):
            shutil.copy2(f, f'{BAKDIR}/{name}.html')
        open(f, 'w', encoding='utf-8').write(t)
    print(f'  {name}: {acts or "已应用"}')

if fails:
    print('FAILED:'); [print('  -', x) for x in fails]; sys.exit(1)

# ---- 全局自检 ----
# 注意：bundle 内 JS 字符串里本来就含 1 处 "<script" 文本，各页 <script>/</script> 天然差 1，
# 故脚本标签校验按「相对备份的增量」判定，而非绝对配平。
bad = 0
for name in PAGES:
    t = open(f'pages/{name}.html', encoding='utf-8').read()
    o = open(f'{BAKDIR}/{name}.html', encoding='utf-8').read()
    for tag in ('<script', '</script>'):
        if t.count(tag) != o.count(tag) + 1:
            print(f'  !! {name} {tag} 增量异常 {t.count(tag)} vs {o.count(tag)}'); bad += 1
    if '<style' in t and t.count('<style') != t.count('</style>'):
        print(f'  !! {name} style 标签不配平'); bad += 1
    if t.count('SHELL-NAV-FIX v5') != 1:
        print(f'  !! {name} nav-fix 缺失或重复'); bad += 1
    if t.count('td-sec-head') != o.count('td-sec-head') or t.count('td-attr-row') != o.count('td-attr-row'):
        print(f'  !! {name} 结构漂移'); bad += 1
if bad:
    sys.exit(1)
print('ALL OK · 9 页 nav-fix 就位；kanban/req-kanban 路由已补')

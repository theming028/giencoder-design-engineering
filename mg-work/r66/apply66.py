#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r66 补丁
① 看板泳道：卡片区内滚 + 标题栏固定（+ 渐隐提示改为按滚动位置动态切换）
② 蒙层全局统一为「高斯模糊」：罩色 --color-mask-bg = rgba(0,0,0,.4) + backdrop-filter blur(10px)
   （口径来源：task-detail 里既有的「任务协作弹窗」.td-coop —— 它就是这个标准的范本）
③ .td-modal-panel 面板材质（用户指定）：radius 16 / rgba(255,255,255,.95) /
   backdrop-filter blur(12px) saturate(100%) / box-shadow 0 8px 16px rgba(0,0,0,.12)

幂等策略（沿用项目约定）：
  · 每条替换先判 newmark 是否已在文件中 —— 命中即 skip；
  · 未命中则要求 OLD 恰好出现 expect 次，否则 sys.exit 报锚点数；
  · 「声明增量」只累加**实际应用**的替换，保证复跑输出 Δ0。
自检只断言：① 标签级计数「改前改后差值」 ② 被改对象的精确出现次数。
"""
import os
import re
import sys

ROOT = '/Users/shaoyuming/Documents/GienCoderDesignEngineering'
PAGES = os.path.join(ROOT, 'pages')
DS = os.path.join(ROOT, 'giencoder-design-system')
BACKUP = '/tmp/r66-backup'

PAGE_FILES = ['automation.html', 'avatar.html', 'base.html', 'dev.html',
              'kanban.html', 'req-kanban.html', 'settings.html', 'skills.html',
              'task-detail.html']
TD = os.path.join(PAGES, 'task-detail.html')
KB = os.path.join(PAGES, 'kanban.html')

applied, skipped = [], []


def sub(path, label, old, new, newmark, expect=1):
    txt = open(path, encoding='utf-8').read()
    if newmark and newmark in txt:
        skipped.append((path, label))
        return False
    n = txt.count(old)
    if n != expect:
        sys.exit('✗ [%s] %s 锚点命中 %d 次（期望 %d）' % (os.path.basename(path), label, n, expect))
    open(path, 'w', encoding='utf-8').write(txt.replace(old, new, 1))
    applied.append((path, label, len(new) - len(old)))
    return True


def rd(p):
    return open(p, encoding='utf-8').read()


# ══════════════════════════════════════════════════════════════════
# ① 蒙层全局统一：罩色 rgba(0,0,0,.4) + blur(10px)
# ══════════════════════════════════════════════════════════════════
# ①-a 亮色罩色 token：#1f1f1f99 = rgba(31,31,31,.6) → #0006 = rgba(0,0,0,.4)
for f in PAGE_FILES:
    sub(os.path.join(PAGES, f), 'mask-token',
        '--color-mask-bg:#1f1f1f99', '--color-mask-bg:#0006', '--color-mask-bg:#0006')

# ①-b 页面内联遮罩规则加高斯模糊
MASK_BLUR = '-webkit-backdrop-filter:blur(10px) saturate(100%);backdrop-filter:blur(10px) saturate(100%)'
OLD_PAGE_MASK = '.giencoder-modal-mask,.giencoder-drawer-mask{background:var(--color-mask-bg)}'
NEW_PAGE_MASK = ('.giencoder-modal-mask,.giencoder-drawer-mask{background:var(--color-mask-bg);'
                 + MASK_BLUR + '}')
MASK_MARK = MASK_BLUR + '}'
for f in PAGE_FILES:
    sub(os.path.join(PAGES, f), 'mask-blur', OLD_PAGE_MASK, NEW_PAGE_MASK, MASK_MARK)

# ①-c DS 权威源 + gienx 模板副本
DS_OLD_MASK = '.giencoder-modal-mask, .giencoder-drawer-mask { background: var(--color-mask-bg); }'
DS_NEW_MASK = ('.giencoder-modal-mask, .giencoder-drawer-mask {\n'
               '  /* 全局统一的蒙层材质：罩色 --color-mask-bg + 高斯模糊 blur(10px)（与 .td-coop 同口径） */\n'
               '  background: var(--color-mask-bg);\n'
               '  -webkit-backdrop-filter: blur(10px) saturate(100%);\n'
               '  backdrop-filter: blur(10px) saturate(100%);\n'
               '}')
DS_MASK_MARK = '-webkit-backdrop-filter: blur(10px) saturate(100%);\n  backdrop-filter: blur(10px) saturate(100%);'
for rel in ['components.css', os.path.join('gienx-templates', '_shared', 'components.css')]:
    sub(os.path.join(DS, rel), 'mask-blur:ds', DS_OLD_MASK, DS_NEW_MASK, DS_MASK_MARK)

# ①-d DS 亮色 token 与文档
sub(os.path.join(DS, 'colors_and_type.css'), 'mask-token:ds',
    '--color-mask-bg: rgba(31, 31, 31, 0.6);',
    '--color-mask-bg: rgba(0, 0, 0, 0.4);',
    '--color-mask-bg: rgba(0, 0, 0, 0.4);')
sub(os.path.join(DS, 'tokens.md'), 'mask-token:doc',
    '| `--color-mask-bg` | rgba(31,31,31,0.6) | Modal/Drawer 遮罩（亮色） |',
    '| `--color-mask-bg` | rgba(0,0,0,0.4) | Modal/Drawer 遮罩（亮色）；统一配 `backdrop-filter: blur(10px)` 高斯模糊 |',
    '| `--color-mask-bg` | rgba(0,0,0,0.4) |')

# ①-e task-detail 自建弹窗遮罩（r65）
sub(TD, 'mask-blur:td-modal',
    ('.td-modal-mask { position: absolute; inset: 0; background: var(--color-mask-bg); '
     'opacity: 0; transition: opacity .2s cubic-bezier(0.34, 0.69, 0.1, 1); }'),
    ('.td-modal-mask { position: absolute; inset: 0; background: var(--color-mask-bg); '
     '-webkit-backdrop-filter: blur(10px) saturate(100%); backdrop-filter: blur(10px) saturate(100%); '
     'opacity: 0; transition: opacity .2s cubic-bezier(0.34, 0.69, 0.1, 1); }'),
    'background: var(--color-mask-bg); -webkit-backdrop-filter: blur(10px)')

# ①-f 任务协作弹窗（.td-coop）的蒙层去重：罩色/模糊改由全局规则承担，避免同一蒙层两套口径
COOP_MASK_OLD = ('.td-coop .giencoder-modal-mask {\n'
                 '        position: absolute; inset: 0; background: rgba(0, 0, 0, 0.4);\n'
                 '        -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);\n'
                 '        opacity: 0; transition: opacity .2s cubic-bezier(0.34, 0.69, 0.1, 1);\n'
                 '      }')
COOP_MASK_NEW = ('.td-coop .giencoder-modal-mask {\n'
                 '        /* ★ 第 66 轮：罩色与模糊改由全局 .giencoder-modal-mask 承担\n'
                 '           （--color-mask-bg = rgba(0,0,0,.4) + blur(10px)），此处不再重复声明。 */\n'
                 '        position: absolute; inset: 0;\n'
                 '        opacity: 0; transition: opacity .2s cubic-bezier(0.34, 0.69, 0.1, 1);\n'
                 '      }')
sub(TD, 'coop-mask-dedupe', COOP_MASK_OLD, COOP_MASK_NEW,
    '罩色与模糊改由全局 .giencoder-modal-mask 承担')

# ①-g 看板两个全局弹窗的蒙层也并入统一口径（罩色走同一 token，模糊 5/6px → 10px）
sub(KB, 'kb-mask-var:crt',
    '--kb-crt-mask: rgba(0, 0, 0, 0.32);', '--kb-crt-mask: var(--color-mask-bg);',
    '--kb-crt-mask: var(--color-mask-bg);')
sub(KB, 'kb-mask-var:coop',
    '--kb-coop-mask: rgba(0, 0, 0, 0.32);', '--kb-coop-mask: var(--color-mask-bg);',
    '--kb-coop-mask: var(--color-mask-bg);')
sub(KB, 'kb-mask-blur:crt',
    ('background: var(--kb-crt-mask);\n'
     '        -webkit-backdrop-filter: blur(5px); backdrop-filter: blur(5px);'),
    ('background: var(--kb-crt-mask);\n'
     '        -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);'),
    'background: var(--kb-crt-mask);\n        -webkit-backdrop-filter: blur(10px);')
sub(KB, 'kb-mask-blur:coop',
    ('background: var(--kb-coop-mask);\n'
     '        -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px);'),
    ('background: var(--kb-coop-mask);\n'
     '        -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);'),
    'background: var(--kb-coop-mask);\n        -webkit-backdrop-filter: blur(10px);')

# ══════════════════════════════════════════════════════════════════
# ② .td-modal-panel 面板材质（用户指定）
# ══════════════════════════════════════════════════════════════════
PANEL_OLD = '        background: var(--color-bg-2); border-radius: 16px; box-shadow: var(--shadow3-down);'
PANEL_NEW = '''        /* ★ 第 66 轮：面板材质（用户指定）
           border-radius: 16px; background: rgba(255,255,255,.95);
           backdrop-filter: blur(12px) saturate(100%);
           box-shadow: 0px 8px 16px 0px rgba(0,0,0,.12)
           颜色仍由 token 合成：rgba(255,255,255,.95) = color-mix(--color-bg-2 95%, transparent)；
           上一行保留不透明兜底，不支持 color-mix 的环境自动回退。
           投影 DS 无对应 token（--shadow3-down 是 0 8px 20px/10%），按指定值显式声明并注明来源。 */
        background: var(--color-bg-2);
        background: color-mix(in srgb, var(--color-bg-2) 95%, transparent);
        -webkit-backdrop-filter: blur(12px) saturate(100%);
        backdrop-filter: blur(12px) saturate(100%);
        box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.12);
        border-radius: 16px;'''
sub(TD, 'panel-material', PANEL_OLD, PANEL_NEW,
    '        background: color-mix(in srgb, var(--color-bg-2) 95%, transparent);')

# ══════════════════════════════════════════════════════════════════
# ③ 看板泳道：卡片区内滚 + 上下渐隐动态切换
# ══════════════════════════════════════════════════════════════════
sub(KB, 'col-body-scroll',
    ('.kb-col-body { flex: 1; overflow: hidden; padding: 0 8px; '
     'display: flex; flex-direction: column; gap: 8px; }'),
    '''/* ★ 第 66 轮：卡片区在泳道内纵向滚动。
           .kb-col-head 是它的兄弟节点、位于滚动区之外，所以标题栏天然固定不滚动。
           6px 滚动条（与页内 .skill-pop-list 同档，比全局 10px 更贴合 334px 宽的泳道）；
           overflow-x 保持 hidden，卡片横向溢出仍被裁掉。 */
      .kb-col-body { flex: 1; min-height: 0; overflow-y: auto; overflow-x: hidden; padding: 0 8px; display: flex; flex-direction: column; gap: 8px; }
      .kb-col-body::-webkit-scrollbar { width: 6px; }''',
    '.kb-col-body::-webkit-scrollbar { width: 6px; }')

sub(KB, 'col-body-fade',
    ('.kb-col-body.is-fade { -webkit-mask-image: linear-gradient(#000 82%, transparent 99%); '
     'mask-image: linear-gradient(#000 82%, transparent 99%); }'),
    '''/* ★ 第 66 轮：渐隐提示改为「按滚动位置动态切换」（见页尾 KB-COL-SCROLL 块）。
           固定 40px 渐隐带 —— 原先按 18% 比例，滚到底时最后一张卡仍被糊掉一大截。 */
      .kb-col-body.is-fade { -webkit-mask-image: linear-gradient(#000 calc(100% - 40px), transparent 100%); mask-image: linear-gradient(#000 calc(100% - 40px), transparent 100%); }
      .kb-col-body.is-fade-top { -webkit-mask-image: linear-gradient(transparent 0, #000 40px); mask-image: linear-gradient(transparent 0, #000 40px); }
      .kb-col-body.is-fade.is-fade-top { -webkit-mask-image: linear-gradient(transparent 0, #000 40px, #000 calc(100% - 40px), transparent 100%); mask-image: linear-gradient(transparent 0, #000 40px, #000 calc(100% - 40px), transparent 100%); }''',
    '.kb-col-body.is-fade.is-fade-top {')

sub(KB, 'col-scroll-js',
    '<!-- /SHELL-TABS-FIX -->\n</body>',
    '''<!-- /SHELL-TABS-FIX -->
<!-- KB-COL-SCROLL v1 · 泳道卡片区滚动渐隐（勿手改此块）
     滚动本身由 .kb-col-body{overflow-y:auto} 承担，标题栏在滚动区外天然不滚。
     本块只做一件事：按实际滚动位置切换 is-fade（下方还有内容）/ is-fade-top（上方还有内容），
     避免"滚到底最后一张卡还是糊的"。 -->
    <script>
      (function () {
        var SEL = '.kb-col-body';
        function sync(el) {
          var more = el.scrollHeight - el.clientHeight - el.scrollTop > 2;
          var above = el.scrollTop > 2;
          el.classList.toggle('is-fade', more);
          el.classList.toggle('is-fade-top', above);
        }
        function all() {
          var list = document.querySelectorAll(SEL);
          for (var i = 0; i < list.length; i++) sync(list[i]);
        }
        document.addEventListener('scroll', function (e) {
          var t = e.target;
          if (t && t.classList && t.classList.contains('kb-col-body')) sync(t);
        }, true);
        window.addEventListener('resize', all);
        window.addEventListener('load', all);
        if (window.MutationObserver) {
          var mo = new MutationObserver(function () { requestAnimationFrame(all); });
          var start = function () { mo.observe(document.body, { childList: true, subtree: true }); };
          if (document.body) start(); else document.addEventListener('DOMContentLoaded', start);
        }
        var boot = function () { all(); requestAnimationFrame(all); };
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
        else boot();
      })();
    </script>
<!-- /KB-COL-SCROLL -->
</body>''',
    '<!-- /KB-COL-SCROLL -->')

# ══════════════════════════════════════════════════════════════════
# 自检
# ══════════════════════════════════════════════════════════════════
print('=' * 68)
if applied:
    for p, l, d in applied:
        print('  应用 %-22s %-22s %+6d B' % (os.path.basename(p), l, d))
else:
    print('  应用 无（全部命中 newmark，已是最新）')
print('  跳过 %d 项' % len(skipped))
print('=' * 68)

errs = []
TAGS = ['<style>', '</style>', '<script>', '</script>', '<body', '</body>', '</html>']

# ① 标签级计数：只比「改前 vs 改后」的差值（页面里本就有 <style>/<script> 计数不对称的历史包袱）
for f in PAGE_FILES:
    a, b = rd(os.path.join(PAGES, f)), rd(os.path.join(BACKUP, 'pages', f))
    d = {k: (b.count(k), a.count(k)) for k in TAGS if b.count(k) != a.count(k)}
    ok = (d == {'<script>': (7, 8), '</script>': (7, 8)}) if f == 'kanban.html' else (d == {})
    print('  %s 标签计数 %-18s %s' % ('✓' if ok else '✗', f, d if d else '无变化'))
    if not ok:
        errs.append('%s 标签计数异常 %s' % (f, d))

DS_TAGS_OK = True
for rel in ['components.css', os.path.join('gienx-templates', '_shared', 'components.css')]:
    a = rd(os.path.join(DS, rel))
    if a.count('{') != a.count('}'):
        DS_TAGS_OK = False
        errs.append('%s 花括号不成对' % rel)
print('  %s DS css 花括号成对' % ('✓' if DS_TAGS_OK else '✗'))

# ② 被改对象的精确出现次数
def cnt(p, n):
    return rd(p).count(n)

checks = [
    ('9 页蒙层罩色已改 rgba(0,0,0,.4)',
     all(cnt(os.path.join(PAGES, f), '--color-mask-bg:#0006') == 1 and
         cnt(os.path.join(PAGES, f), '#1f1f1f99') == 0 for f in PAGE_FILES)),
    ('9 页蒙层已加 blur(10px)', all(cnt(os.path.join(PAGES, f), MASK_MARK) == 1 for f in PAGE_FILES)),
    ('DS components.css 蒙层', cnt(os.path.join(DS, 'components.css'), DS_MASK_MARK) == 1),
    ('DS gienx 模板蒙层', cnt(os.path.join(DS, 'gienx-templates', '_shared', 'components.css'), DS_MASK_MARK) == 1),
    ('DS 亮色 token', cnt(os.path.join(DS, 'colors_and_type.css'), '--color-mask-bg: rgba(0, 0, 0, 0.4);') == 1),
    ('tokens.md 已同步', cnt(os.path.join(DS, 'tokens.md'), 'rgba(0,0,0,0.4)') == 1),
    ('td-modal-mask blur10', cnt(TD, 'backdrop-filter: blur(10px) saturate(100%); opacity: 0;') == 1),
    ('td-coop 蒙层已去重', cnt(TD, '罩色与模糊改由全局 .giencoder-modal-mask 承担') == 1),
    (' kb-mask 走统一 token', cnt(KB, '--kb-crt-mask: var(--color-mask-bg);') == 1 and
                              cnt(KB, '--kb-coop-mask: var(--color-mask-bg);') == 1 and
                              cnt(KB, 'rgba(0, 0, 0, 0.32)') == 0),
    ('kb 蒙层 blur 已统一 10px', cnt(KB, 'blur(5px)') == 0 and cnt(KB, 'blur(6px)') == 0),
    ('td-modal-panel color-mix', cnt(TD, 'background: color-mix(in srgb, var(--color-bg-2) 95%, transparent);') == 1),
    ('td-modal-panel blur12', cnt(TD, 'backdrop-filter: blur(12px) saturate(100%);') == 3),  # 含注释 1 处 + webkit 包含子串 1 处
    ('td-modal-panel 新投影', cnt(TD, 'box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.12);') == 1),
    ('kb-col-body 已内滚', cnt(KB, 'overflow-y: auto; overflow-x: hidden') == 1),
    ('kb-col-body 旧 overflow:hidden 已消失', cnt(KB, '.kb-col-body { flex: 1; overflow: hidden;') == 0),
    ('kb-col-body 6px 滚动条', cnt(KB, '.kb-col-body::-webkit-scrollbar { width: 6px; }') == 1),
    ('is-fade 上渐隐规则', cnt(KB, '.kb-col-body.is-fade-top {') == 1),
    ('滚动脚本注入块', cnt(KB, '<!-- /KB-COL-SCROLL -->') == 1),
    ('kb-col-head 未被改动', cnt(KB, '.kb-col-head { flex: none; height: 44px;') == 1),
]
for name, ok in checks:
    print('  %s %s' % ('✓' if ok else '✗', name))
    if not ok:
        errs.append(name)

print('=' * 68)
print('✓ ALL PASS   （±%d 字节）' % sum(d for _, _, d in applied) if not errs else '✗ FAIL')
if errs:
    for e in errs:
        print('   -', e)
    sys.exit(1)

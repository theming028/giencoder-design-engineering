# -*- coding: utf-8 -*-
"""r69 落地补丁（幂等 + 自检）
需求 1：数字分身右栏标题 →「新会话」，并去掉下面的时间。
需求 2：把「研发工作台 › 任务详情页」的 .td-browse-slot 全要素移植到数字分身；
       展开时 shell 左导航栏宽度收拢到 0（200ms）。
用法：python3 mg-work/r69/apply69.py
回滚：cp /tmp/r69-backup/avatar.html pages/avatar.html
"""
import io, os, re, sys, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGE = os.path.join(ROOT, 'pages/avatar.html')
PART = os.path.join(ROOT, 'mg-work/r69')
BK = '/tmp/r69-backup'

def load(name):
    return io.open(os.path.join(PART, name), encoding='utf-8').read()

CSS = load('part-css.css')
HTML = load('part-html.txt')
JS = load('part-ctrl.js')

# ---------- 一、被改对象的 newmark（命中即跳过，防「NEW 超集」重复追加） ----------
J1_NEW = 'class="td-right-title">新会话</div>'
J2_NEW = 'id="av-browse-js"'

# ---------- 二、替换定义 ----------
J1_OLD = ('      <div class="td-right-title">端到端流程初始化：用户输入业务流程并触发全链路交付</div>\n'
          '          <div class="td-right-time">2026/08/01 11:26</div>\n'
          '        </div>')
J1_REP = ('      <div class="td-right-title">新会话</div>\n'
          '        </div>')

J2_ANCHOR = '<script id="av-chat-js">'
J2_REP = (
    '<!-- ===== AV-BROWSE-SLOT v1 —— 第 69 轮：任务详情页「文件预览栏」全要素移植（HTML + CSS + JS 三件套）===== -->\n'
    '<style id="av-browse-css">\n' + CSS + '\n</style>\n'
    + HTML + '\n'
    '<script id="av-browse-js">\n' + JS + '\n</script>\n\n'
    + J2_ANCHOR)

# ---------- 三、元守卫：载荷不得含会污染标签计数的字面量 ----------
for nm, x in (('css', CSS), ('js', JS), ('html', HTML)):
    for bad in ('</style', '</script', '</body>', '</html>'):
        if bad in x:
            sys.exit('元守卫失败：%s 载荷含 %s' % (nm, bad))
if J2_REP.count('<style id="av-browse-css">') != 1 or J2_REP.count('<script id="av-browse-js">') != 1:
    sys.exit('元守卫失败：包装标签计数异常')

# ---------- 四、备份 ----------
if not os.path.isdir(BK):
    os.makedirs(BK)
if not os.path.exists(os.path.join(BK, 'avatar.html')):
    shutil.copy2(PAGE, os.path.join(BK, 'avatar.html'))

s = io.open(PAGE, encoding='utf-8').read()
n0 = len(s)
c0 = {t: s.count(t) for t in ('<style', '</style>', '<script', '</script>')}

applied, skipped = [], []
jobs = [
    ('J1 右栏标题→新会话 + 去时间', J1_NEW, J1_OLD, J1_REP, 1),
    ('J2 移植文件预览栏三件套',      J2_NEW, J2_ANCHOR, J2_REP, 1),
]
out = s
for name, newmark, old, rep, want in jobs:
    if newmark in out:
        skipped.append(name); continue
    n = out.count(old)
    if n != want:
        sys.exit('锚点异常：%s 期望命中 %d 次，实际 %d 次' % (name, want, n))
    out = out.replace(old, rep, want)
    applied.append(name)

if out == s:
    print('应用: 0 项 | 跳过: %d 项  （幂等验证通过）' % len(skipped))
    for x in skipped: print('   跳过:', x)
    sys.exit(0)

# ---------- 五、自检：只允许「标签级计数」与「被改对象的精确增减量」 ----------
errs = []
for t in c0:
    d = out.count(t) - c0[t]
    if t in ('<style', '</style>', '<script', '</script>'):
        if 'J2' in ''.join(applied) and d != 1:
            errs.append('%s Δ=%d（应为 +1）' % (t, d))
        elif 'J2' not in ''.join(applied) and d != 0:
            errs.append('%s Δ=%d（应为 0）' % (t, d))
if 'J2' in ''.join(applied):
    for mid, want in (('id="av-browse-slot"', 1), ('id="av-browse-split"', 1),
                      ('id="av-browse-js"', 1), ('id="av-browse-css"', 1)):
        if out.count(mid) != want:
            errs.append('%s 计数=%d（应为 %d）' % (mid, out.count(mid), want))
    if out.count('class="td-bf') - s.count('class="td-bf') != 168:
        errs.append('class="td-bf Δ=%d（应为 +168）' % (out.count('class="td-bf') - s.count('class="td-bf')))
    if out.count('data-td-browse-toggle="1"') != s.count('data-td-browse-toggle="1"'):
        errs.append('顶栏「打开侧栏」按钮（data-td-browse-toggle="1"）计数变了')
    if out.find('id="av-browse-js"') > out.find('id="av-chat-js"'):
        errs.append('预览栏脚本没有排在抽屉脚本之前（Esc 裁决顺序会错）')
if 'J1' in ''.join(applied):
    if out.count(J1_NEW) != 1:
        errs.append('标题新文案计数=%d（应为 1）' % out.count(J1_NEW))
    if out.count('td-right-time') != s.count('td-right-time') - 1:
        errs.append('td-right-time 计数=%d（应 −1，CSS 里那条规则必须还在）' % out.count('td-right-time'))
    if out.count('.td-right-time {') != 1:
        errs.append('.td-right-time 的 CSS 规则被误删')
if errs:
    sys.exit('自检失败：\n  ' + '\n  '.join(errs))

io.open(PAGE, 'w', encoding='utf-8').write(out)
print('应用: %d 项 | 跳过: %d 项' % (len(applied), len(skipped)))
for x in applied: print('   落地:', x)
for x in skipped: print('   跳过:', x)
print('字节：%d → %d（%+d）' % (n0, len(out), len(out) - n0))
print('标签计数：', {t: out.count(t) - c0[t] for t in c0})

# -*- coding: utf-8 -*-
"""
r14 补丁：kb-coop 待协作任务模态
 1. 表头字号不再覆盖 —— 沿用设计系统契约 .giencoder-table-th 的全局 12px
    （--font-size-body-1）
 2. 表格任务标题改为设计系统 Link 元素（a.giencoder-link），补齐可点击/可聚焦/指针
    与链接蓝 hover（设计稿采样 #3770F7 = --color-link-6）
 3. 模态通用化：待协作 / 待评审 / 已延期 / 已取消 卡片共用同一个弹窗，
    标题由卡片上的 data-modal-title 决定
"""
import io
import re
import sys

PATH = 'pages/kanban.html'
s = io.open(PATH, encoding='utf-8').read()
orig = len(s)

if 'r14: 任务标题 = 设计系统 Link' in s and 'data-modal-title' in s:
    print('[SKIP] r14 已应用')
    sys.exit(0)

done = []

# ============================================================ 1) 表头字号
OLD_TH = u'''      .kb-coop-tbl .giencoder-table-th {
        background: var(--kb-tbl-head-bg); color: var(--color-text-3); font-weight: 400;
        font-size: var(--font-size-body-3); padding: 5.75px 12px; line-height: 20px;
        border-bottom: 1px solid var(--kb-tbl-line); text-align: left;
      }'''
NEW_TH = u'''      /* r14: 表头字号不做覆盖 —— 直接用设计系统契约 .giencoder-table-th 的
         font-size: var(--font-size-body-1)（全局 12px）；本表只保留实测的内距/行高/底色 */
      .kb-coop-tbl .giencoder-table-th {
        background: var(--kb-tbl-head-bg); color: var(--color-text-3); font-weight: 400;
        padding: 5.75px 12px; line-height: 20px;
        border-bottom: 1px solid var(--kb-tbl-line); text-align: left;
      }'''
assert s.count(OLD_TH) == 1, 'th rule count=%d' % s.count(OLD_TH)
s = s.replace(OLD_TH, NEW_TH)
done.append('header font-size -> DS contract token (12px)')


# ==================================================== 2) 任务标题 = Link
OLD_TITLE_CSS = u"      .kb-coop-tbl .kb-row-hover .kb-td-title { color: var(--color-primary-6); }"
NEW_TITLE_CSS = u'''      /* r14: 任务标题 = 设计系统 Link（a.giencoder-link）在表格里的视图适配。
         设计稿采样：#3770F7 = --color-link-6（= --color-primary-6），且标题常态无下划线，
         只在「行 hover」或「链接自身 hover」时转为链接蓝 */
      .kb-coop-tbl .kb-td-title {
        color: var(--color-text-1); text-decoration: none; cursor: pointer;
        transition: color var(--transition-duration-1) var(--transition-timing-function-standard);
      }
      .kb-coop-tbl .kb-td-title:hover,
      .kb-coop-tbl .kb-row-hover .kb-td-title { color: var(--color-link-6); }
      .kb-coop-tbl .kb-td-title:focus-visible {
        outline: none; border-radius: 2px; box-shadow: 0 0 0 2px var(--color-primary-light-2);
      }'''
assert s.count(OLD_TITLE_CSS) == 1, 'row-hover title css count=%d' % s.count(OLD_TITLE_CSS)
s = s.replace(OLD_TITLE_CSS, NEW_TITLE_CSS)

LINK_OPEN = (u'<a class=\\"giencoder-link\\" href=\\"#\\" data-component=\\"link\\" '
             u'data-variant=\\"default\\" data-state=\\"default\\">')
td_pat = re.compile(r'(<td class=\\"giencoder-table-td kb-td-title\\">)([^<]+)(</td>)')
found = td_pat.findall(s)
assert len(found) == 8, 'td-title count=%d' % len(found)
s = td_pat.sub(lambda m: m.group(1) + LINK_OPEN + m.group(2) + u'</a>' + m.group(3), s)
done.append('8 task titles -> a.giencoder-link')


# ============================================ 3) 模态通用化（4 个触发卡片）
for cls, title in [(u'kb-stat--coop', u'待协作任务'),
                   (u'kb-stat--review', u'待评审任务'),
                   (u'kb-stat--delay', u'已延期任务'),
                   (u'kb-stat--cancel', u'已取消任务')]:
    old = u'<div class=\\"kb-stat ' + cls + u'\\">'
    new = u'<div class=\\"kb-stat ' + cls + u'\\" data-modal-title=\\"' + title + u'\\">'
    assert s.count(old) == 1, '%s count=%d' % (cls, s.count(old))
    s = s.replace(old, new)
done.append('4 stat cards -> data-modal-title')

# --- JS：绑定全部触发卡片 + 按卡片切换标题
OLD_HEAD = u'''  /* ===== r11: 待协作任务模态：kb-stat--coop 点击打开（非全屏面板 + 遮罩 + Esc/遮罩/× 关闭） ===== */
  function bindCoopModal(root) {
    var modal = root.querySelector('.kb-coop');
    var trigger = root.querySelector('.kb-stat--coop');
    if (!modal || !trigger) return;'''
NEW_HEAD = u'''  /* ===== r11/r14: 任务列表面板（通用）=====
     待协作 / 待评审 / 已延期 / 已取消 四张卡片共用同一个弹窗，
     标题取自卡片上的 data-modal-title；非全屏面板 + 遮罩 + Esc/遮罩/× 关闭 ===== */
  function bindCoopModal(root) {
    var modal = root.querySelector('.kb-coop');
    var triggers = Array.prototype.slice.call(root.querySelectorAll('.kb-stat[data-modal-title]'));
    if (!modal || !triggers.length) return;
    var titleEl = modal.querySelector('.giencoder-modal-title');'''
assert s.count(OLD_HEAD) == 1, 'bind head count=%d' % s.count(OLD_HEAD)
s = s.replace(OLD_HEAD, NEW_HEAD)

OLD_OPEN_SIG = u'''    function open() {
      if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }'''
NEW_OPEN_SIG = u'''    function open(title) {
      /* r14: 通用面板 —— 用触发卡片的标题刷新面板标题/无障碍名称 */
      if (title) {
        if (titleEl) titleEl.textContent = title;
        modal.setAttribute('aria-label', title);
        var dlgEl = modal.querySelector('.kb-coop-dialog');
        if (dlgEl) dlgEl.setAttribute('aria-label', title);
      }
      if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }'''
assert s.count(OLD_OPEN_SIG) == 1, 'open sig count=%d' % s.count(OLD_OPEN_SIG)
s = s.replace(OLD_OPEN_SIG, NEW_OPEN_SIG)

OLD_BIND = u'''    trigger.addEventListener('click', open);
    trigger.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });'''
NEW_BIND = u'''    triggers.forEach(function (t) {
      var title = t.getAttribute('data-modal-title');
      t.addEventListener('click', function () { open(title); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(title); }
      });
    });'''
assert s.count(OLD_BIND) == 1, 'bind listeners count=%d' % s.count(OLD_BIND)
s = s.replace(OLD_BIND, NEW_BIND)
done.append('bindCoopModal -> 4 triggers + dynamic title')

io.open(PATH, 'w', encoding='utf-8', newline='').write(s)
print('[OK] %d -> %d chars' % (orig, len(s)))
for d in done:
    print('   -', d)

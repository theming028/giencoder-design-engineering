# -*- coding: utf-8 -*-
"""r53b：把预览栏微动效做得更「有方向感」。

r53 只做了外框的 clip-path 抹开 + 淡入，实测 28px 的抹开距离在 ~940px 宽的面板上
只占 3%，观感更接近纯淡入、方向感不足。本脚本：
  ① 外框抹开距离 28px → 40px；
  ② 再叠一层内层内容跟手位移（+24px → 0），被 .td-browse 的 overflow:hidden 裁掉，
     不产生任何页面溢出。

幂等：先判 NEW 标记，再判 OLD。
"""
import re, sys

PAGE = 'pages/task-detail.html'
s = open(PAGE, encoding='utf-8').read()
bef = len(s)

# ---- ① 抹开距离 28 → 40（共 2 处：tdBrowseIn 的 from、tdBrowseOut 的 to）
OLD_A = 'inset(0 0 0 28px round 0 8px 8px 0)'
NEW_A = 'inset(0 0 0 40px round 0 8px 8px 0)'
MARK_A = NEW_A

# ---- ② 内层内容跟手位移
OLD_B = """      @media (prefers-reduced-motion: reduce) {
        .td-root.is-browse .td-browse,
        .td-root.is-browse .td-browse.is-closing { animation: none; }
      }
"""
NEW_B = """      /* 内层再叠一层「跟手」位移：外框负责柔和出现，内容负责方向感 ——
         只有两者叠加才像「滑出来」，单靠淡入仍偏平。
         位移被 .td-browse 自身的 overflow:hidden 裁掉，不产生任何溢出。 */
      @keyframes tdBrowseContentIn {
        from { transform: translateX(24px); }
        to { transform: translateX(0); }
      }
      .td-root.is-browse .td-browse > .td-browse-bar,
      .td-root.is-browse .td-browse > .td-browse-body {
        animation: tdBrowseContentIn 260ms var(--transition-timing-function-standard, cubic-bezier(0.4, 0, 0.2, 1)) backwards;
      }
      @media (prefers-reduced-motion: reduce) {
        .td-root.is-browse .td-browse,
        .td-root.is-browse .td-browse.is-closing { animation: none; }
        .td-root.is-browse .td-browse > .td-browse-bar,
        .td-root.is-browse .td-browse > .td-browse-body { animation: none; }
      }
"""
MARK_B = '@keyframes tdBrowseContentIn {'

# ① 幂等：先判 OLD（未应用过）再判 NEW（已应用）
if OLD_A in s:
    n = s.count(OLD_A)
    s = s.replace(OLD_A, NEW_A)
    a_done = '替换 %d 处' % n
elif MARK_A in s:
    a_done = '已应用'
else:
    sys.exit('!! 抹开距离：OLD 与 NEW 均未命中')

if MARK_B in s:
    b_done = '已应用'
else:
    if s.count(OLD_B) != 1:
        sys.exit('!! 内容位移锚点匹配数 = %d（应为 1）' % s.count(OLD_B))
    s = s.replace(OLD_B, NEW_B, 1)
    b_done = '已应用'

open(PAGE, 'w', encoding='utf-8').write(s)

# ---------------- 自检
def cnt(p):
    return len(re.findall(p, s))

checks = [
    ('<style 3', cnt(r'<style'), 3),
    ('</style> 3', cnt(r'</style>'), 3),
    ('<script 9', cnt(r'<script'), 9),
    ('</script> 8', cnt(r'</script>'), 8),
    ('40px 抹开 ×2', cnt(re.escape('inset(0 0 0 40px round 0 8px 8px 0)')), 2),
    ('28px 残留 0', cnt(re.escape('inset(0 0 0 28px')), 0),
    ('ContentIn keyframes 1', cnt(re.escape('@keyframes tdBrowseContentIn {')), 1),
    ('bar/body 规则 2（含 reduce 分支）', cnt(re.escape('.td-root.is-browse .td-browse > .td-browse-body {')), 2),
    ('tdBrowseIn 仍在 1', cnt(re.escape('@keyframes tdBrowseIn {')), 1),
    ('tdBrowseOut 仍在 1', cnt(re.escape('@keyframes tdBrowseOut {')), 1),
    ('r53 内层未被误删：desc 渐隐 1', cnt(re.escape('--td-desc-fade: 56px')), 1),
    ('r53 日历仍在 1', cnt(re.escape('.giencoder-calendar-cell-empty { visibility: hidden; }')), 1),
    ('r53 下拉右对齐仍在 1', cnt(re.escape('.kb-crt-fld > .giencoder-select-popup { left: auto; right: 0; }')), 1),
]
bad = ['   ✗ %-30s 实测 %s，期望 %s' % (l, g, w) for l, g, w in checks if g != w]

print('① 抹开距离：%s   ② 内容位移：%s' % (a_done, b_done))
if bad:
    print('!! 自检未通过 %d 条：' % len(bad))
    print('\n'.join(bad))
    sys.exit(1)
print('✅ 全部自检通过，文件 %d 字符（%d 字节，Δ%+d）' % (len(s), len(s.encode('utf-8')), len(s) - bef))

# -*- coding: utf-8 -*-
"""
★ 第 58 轮：任务详情页「浏览态左栏收窄保留」

需求原文：
  当任务详情页右栏的 AI 对话框的 td-browse-slot 容器展开时，原任务详情页的左栏
  不会完全的隐藏，而是自动收窄到 600px 的宽度。

现状（改前实测）：
  .td-root.is-browse .td-left { display: none; }   ← 浏览态左栏整块消失
  1440 视口：root 1424 / left 0(none) / right 480 / slot 944
  1920 视口：root 1904 / left 0(none) / right 480 / slot 1424

改法（用户拍板：自动收窄 —— 600px 为上限，空间不足按可用宽继续收窄，保底 480）：
  ① CSS 新增 .td-root.is-browse.is-keep-left 下的左栏定宽规则（display:flex + flex:0 0 W
     + min/max-width 钳死 + margin-right:var(--td-gap) 补回被 display:none 的 gutter 让出的 8px）
  ② JS 新增 keptLeft() / applyLeft()：可分配宽 = rootW − AI会话栏 − 8 − 预览栏兜底(641)
     → ≥480 就保留（clamp 到 ≤600），否则摘 .is-keep-left 回落 display:none（旧行为）
  ③ maxTree() 改为按「左栏保留后的预览栏可用宽」计算
  ④ setRight() 里同步重算左栏；收起动画结束时一并摘掉 .is-keep-left

幂等：先判 mark（第 58 轮标记），再判 OLD；命中数不符即 FAIL。
"""
import io, re, sys

P = 'pages/task-detail.html'
MARK = '第 58 轮'

def sub1(s, label, old, new, mark, expect=1):
    if mark and mark in s:
        print('   [SKIP] %s（已含标记 %s）' % (label, mark))
        return s, True
    n = s.count(old)
    if n != expect:
        print('   [!!FAIL] %s：OLD 命中 %d 次（期望 %d）' % (label, n, expect))
        return s, False
    s = s.replace(old, new)
    print('   [OK]   %s（替换 %d 处）' % (label, n))
    return s, True

ok = True
s = io.open(P, encoding='utf-8').read()
before_len = len(s)
TAGS = ['<style>', '</style>', '<script>', '</script>']
BIZ = ['class=\\"td-bf is-file', '.td-sec-head', 'td-browse-files', 'data-td-browse-toggle']
TAG0 = {t: s.count(t) for t in TAGS}
BIZ0 = {b: s.count(b) for b in BIZ}

# ---------------------------------------------------------------- ① CSS
OLD_CSS = '''      .td-root.is-browse .td-left { display: none; }
      .td-root.is-browse .td-gutter { display: none; }
'''
NEW_CSS = '''      .td-root.is-browse .td-left { display: none; }
      .td-root.is-browse .td-gutter { display: none; }
      /* ★ 第 58 轮：浏览态左栏不再「整块消失」—— 空间允许时自动收窄到 600px 保留。
         分配规则（JS keptLeft）：可给左栏的宽 = 根容器宽 − AI 会话栏 − 8px 间隙 − 预览栏兜底
         (MIN_TREE+1+MIN_CODE = 641)；结果落到 [480, 600] 就保留（600 为上限，不足按可用宽收窄），
         连 480 都不到 → JS 摘掉 .is-keep-left，回落到上面那条 display:none（＝旧行为）。
         · flex: 0 0 <w> 定死宽度：不伸不缩，不与 .td-browse-slot 的 flex:1 抢空间；
           min/max-width 同值钳死，避免 CSS 既有 min-width:480px 参与计算后又被撑开。
         · margin-right = --td-gap：浏览态 .td-gutter 是 display:none（8px 间隙原本由它提供），
           左栏重新出现后必须自己补上这 8px，否则会与 AI 会话栏贴死。
         · 展开/收起动效不受影响：滑动裁剪窗口仍是 .td-browse-slot。 */
      .td-root.is-browse.is-keep-left .td-left {
        display: flex;
        flex: 0 0 var(--td-left-keep-w, 600px);
        min-width: var(--td-left-keep-w, 600px);
        max-width: var(--td-left-keep-w, 600px);
        margin-right: var(--td-gap);
      }
'''
s, r = sub1(s, 'CSS: 浏览态左栏收窄保留规则', OLD_CSS, NEW_CSS, 'is-keep-left'); ok &= r

# ---------------------------------------------------------------- ② JS 常量
OLD_C = "      var MIN_RIGHT = 400, MIN_TREE = 240, MIN_CODE = 400;\n"
NEW_C = ("      var MIN_RIGHT = 400, MIN_TREE = 240, MIN_CODE = 400;\n"
         "      /* ★ 第 58 轮：浏览态左栏「收窄保留」区间（px）+ 栏间距 */\n"
         "      var LEFT_KEEP_MIN = 480, LEFT_KEEP_MAX = 600, COL_GAP = 8;\n")
s, r = sub1(s, 'JS: 新增 LEFT_KEEP_MIN/MAX + COL_GAP 常量', OLD_C, NEW_C, 'LEFT_KEEP_MIN'); ok &= r

# ---------------------------------------------------------------- ③ JS keptLeft / applyLeft / maxTree
OLD_JS = '''        /* 面板宽 = 根容器宽 − AI 对话框宽（分隔条净占位 0，故不减） */
        function rootW() { return root.getBoundingClientRect().width; }
        function maxRight() { return Math.max(MIN_RIGHT, rootW() - (MIN_TREE + 1 + MIN_CODE)); }
        function maxTree() { return Math.max(MIN_TREE, rootW() - curRight - 1 - MIN_CODE); }
'''
NEW_JS = '''        /* 面板宽 = 根容器宽 − AI 对话框宽（分隔条净占位 0，故不减） */
        function rootW() { return root.getBoundingClientRect().width; }
        function maxRight() { return Math.max(MIN_RIGHT, rootW() - (MIN_TREE + 1 + MIN_CODE)); }

        /* ★ 第 58 轮：浏览态左栏「收窄保留」的宽度分配。
           能分给左栏的宽 = 根容器宽 − AI 会话栏 − 8px 间隙 − 预览栏兜底；
           < LEFT_KEEP_MIN(480) ⇒ 返回 0＝不保留，CSS 回落 display:none（旧行为）。 */
        function keptLeft() {
          if (!root.classList.contains('is-browse')) return 0;
          var avail = rootW() - curRight - COL_GAP - (MIN_TREE + 1 + MIN_CODE);
          if (avail < LEFT_KEEP_MIN) return 0;
          return Math.min(LEFT_KEEP_MAX, Math.round(avail));
        }
        function applyLeft() {
          var w = keptLeft();
          if (w) {
            root.style.setProperty('--td-left-keep-w', w + 'px');
            root.classList.add('is-keep-left');
          } else {
            root.classList.remove('is-keep-left');
          }
          return w;
        }
        /* 预览栏可用宽 = 根容器宽 − 左栏（保留时另扣 8px 间隙）− AI 会话栏 − 分隔条 1px */
        function maxTree() {
          var lw = keptLeft();
          return Math.max(MIN_TREE, rootW() - lw - (lw ? COL_GAP : 0) - curRight - 1 - MIN_CODE);
        }
'''
s, r = sub1(s, 'JS: keptLeft/applyLeft + maxTree 改用左栏保留后宽度', OLD_JS, NEW_JS, 'function keptLeft()'); ok &= r

# ---------------------------------------------------------------- ④ setRight 同步重算
OLD_SR = '''          /* AI 对话框变宽 → 面板变窄 → 树可能越界，同步钳位 */
          if (curTree > maxTree()) setTree(maxTree(), false);
'''
NEW_SR = '''          /* ★ 第 58 轮：AI 会话栏宽度变了 → 左栏可分配宽跟着变 → 先重算左栏保留 */
          applyLeft();
          /* AI 对话框变宽 → 面板变窄 → 树可能越界，同步钳位 */
          if (curTree > maxTree()) setTree(maxTree(), false);
'''
s, r = sub1(s, 'JS: setRight 内同步重算左栏保留', OLD_SR, NEW_SR, 'applyLeft();\n'); ok &= r

# ---------------------------------------------------------------- ⑤ 收起时一并清理
OLD_D = '''            root.classList.remove('is-browse');
            btn.setAttribute('aria-pressed', 'false');
'''
NEW_D = '''            root.classList.remove('is-browse');
            root.classList.remove('is-keep-left');   /* ★ 第 58 轮：左栏保留态随浏览态一起收掉 */
            btn.setAttribute('aria-pressed', 'false');
'''
s, r = sub1(s, 'JS: 收起动画结束时摘掉 is-keep-left', OLD_D, NEW_D, "remove('is-keep-left');   /* ★ 第 58 轮"); ok &= r

# ---------------------------------------------------------------- 自检
print('-' * 60)
def cnt(t):
    return s.count(t)

checks = [
    ('NEW CSS 规则 .is-browse.is-keep-left .td-left', cnt('.td-root.is-browse.is-keep-left .td-left {'), 1),
    ('NEW CSS var --td-left-keep-w', cnt('--td-left-keep-w'), 3 + 0),   # CSS 3 处（默认值）+ JS 1 处
    ('NEW JS function keptLeft()', cnt('function keptLeft()'), 1),
    ('NEW JS function applyLeft()', cnt('function applyLeft()'), 1),
    ('NEW JS 常量 LEFT_KEEP_MIN', cnt('LEFT_KEEP_MIN'), 3),             # 声明 1 + 注释 1 + keptLeft 比较 1
    ('NEW 左栏保留 CSS 选择器', cnt('.td-root.is-browse.is-keep-left'), 1),
]
# --td-left-keep-w：CSS 出现 3 次（flex/min/max）+ JS setProperty 1 次 = 4
checks[1] = ('NEW CSS/JS --td-left-keep-w', cnt('--td-left-keep-w'), 4)
# LEFT_KEEP_MIN: 声明 1 + keptLeft 比较 1 = 2 ; LEFT_KEEP_MAX: 声明 1 + keptLeft 1 = 2
checks[5] = ('NEW JS LEFT_KEEP_MAX', cnt('LEFT_KEEP_MAX'), 2)

for name, got, exp in checks:
    flag = 'OK  ' if got == exp else 'FAIL'
    if got != exp:
        ok = False
    print('   [%s] %s = %d（期望 %d）' % (flag, name, got, exp))

# 结构计数（标签级，改前改后必须相等）
for t in TAGS:
    c = cnt(t)
    same = (c == TAG0[t])
    print('   [%s] tag %-10s = %d（改前 %d）' % ('OK  ' if same else 'FAIL', t, c, TAG0[t]))
    if not same:
        ok = False

for b in BIZ:
    c = cnt(b)
    same = (c == BIZ0[b])
    print('   [%s] biz %-28s = %d（改前 %d）' % ('OK  ' if same else 'FAIL', b, c, BIZ0[b]))
    if not same:
        ok = False

# 未动的锚点
assert cnt('--td-left-min: 480px') == 1, 'CSS --td-left-min 被破坏'
assert cnt('var LEFT_MIN = 480;') == 1, 'JS r35 LEFT_MIN 被破坏'
assert cnt('.td-root.is-browse .td-gutter { display: none; }') == 1, 'gutter 隐藏规则被破坏'

if not ok:
    print('\n>>> FAIL：未写盘')
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('\n>>> ALL PASS：已写盘 %s（%d → %d 字节，+%d）' % (P, before_len, len(s), len(s) - before_len))

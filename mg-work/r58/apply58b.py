# -*- coding: utf-8 -*-
"""
★ 第 58 轮 · 补丁 2：拖动换算基准 + AI 会话栏拖动上限

背景（补丁 1 落地后实测发现）：
  左栏保留后，AI 会话栏的位置不再从根容器左缘起算 —— 其右缘 = 根左缘 + 左栏占位
  (左栏宽 + 8px 间隙)。原拖动换算 `setRight(x - root.left)` 直接把它当成 AI 栏宽度，
  实测「拖 +420px」会一步顶到 maxRight(1443px)，光标与分隔条完全脱节。

修法：
  ① 新增 leftBasis()：左栏在根容器左缘占用的宽度（保留时 = 宽 + 8，否则 0）
  ② maxRight()：浏览态加一道上限 —— AI 会话栏不得把「左栏保底 480 + 预览栏兜底 641」挤破
  ③ splitMain 的 pointerdown 冻结 leftBasis，applyFrom 换算时减去它
     （不冻结会形成「拖宽 AI 栏 → 左栏自动收窄 → 基准漂移」的正反馈）

幂等：先判 mark（第 58 轮标记），再判 OLD；命中数不符即 FAIL。
"""
import io, sys

P = 'pages/task-detail.html'

def sub1(s, label, old, new, mark, expect=1):
    if mark and mark in s:
        print('   [SKIP] %s（已含标记）' % label)
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

# ---------------------------------------------------------------- ① maxRight 加浏览态上限
OLD_MR = "        function maxRight() { return Math.max(MIN_RIGHT, rootW() - (MIN_TREE + 1 + MIN_CODE)); }\n"
NEW_MR = '''        /* ★ 第 58 轮：浏览态给 AI 会话栏加一道拖动上限 ——
           不得把「左栏保底 LEFT_KEEP_MIN(480) + 8px 间隙 + 预览栏兜底(641)」挤破，
           否则拖到一半左栏会突然消失、分隔条位置跳变。 */
        function maxRight() {
          var avail = rootW() - (MIN_TREE + 1 + MIN_CODE);
          if (root.classList.contains('is-browse')) {
            avail = Math.min(avail, rootW() - LEFT_KEEP_MIN - COL_GAP - (MIN_TREE + 1 + MIN_CODE));
          }
          return Math.max(MIN_RIGHT, avail);
        }
'''
s, r = sub1(s, 'JS: maxRight 增加浏览态上限', OLD_MR, NEW_MR, 'function maxRight() {\n          var avail'); ok &= r

# ---------------------------------------------------------------- ② leftBasis()
OLD_LB = '''            root.classList.remove('is-keep-left');
          }
          return w;
        }
'''
NEW_LB = '''            root.classList.remove('is-keep-left');
          }
          return w;
        }
        /* 左栏在根容器左缘占用的宽度（含 8px 间隙）；未保留时为 0 */
        function leftBasis() { var w = keptLeft(); return w ? w + COL_GAP : 0; }
'''
s, r = sub1(s, 'JS: 新增 leftBasis()', OLD_LB, NEW_LB, 'function leftBasis()'); ok &= r

# ---------------------------------------------------------------- ③ 拖动基准冻结 + 换算
OLD_DR = '''        draggable(splitMain, function (x) { setRight(x - root.getBoundingClientRect().left, false); },
                  function () { writeStore({ browseRightW: curRight }); });
'''
NEW_DR = '''        /* ★ 第 58 轮：左栏保留后 AI 会话栏不再从根容器左缘起算，拖动换算必须先减去左栏占位；
           占位在 pointerdown 时**冻结** —— 否则「拖宽 AI 栏 → 左栏自动收窄 → 基准漂移」
           会形成正反馈，光标与分隔条脱节（实测补丁 1 落地后拖 +420px 会一步顶到上限）。 */
        var dragLeftBase = 0;
        if (splitMain) {
          splitMain.addEventListener('pointerdown', function () {
            if (root.classList.contains('is-browse')) dragLeftBase = leftBasis();
          });
          splitMain.addEventListener('pointerup', function () { dragLeftBase = 0; });
          splitMain.addEventListener('pointercancel', function () { dragLeftBase = 0; });
        }
        draggable(splitMain, function (x) {
          setRight(x - root.getBoundingClientRect().left - dragLeftBase, false);
        }, function () { writeStore({ browseRightW: curRight }); });
'''
s, r = sub1(s, 'JS: splitMain 拖动基准冻结 + 换算修正', OLD_DR, NEW_DR, 'var dragLeftBase = 0;'); ok &= r

# ---------------------------------------------------------------- 自检
print('-' * 60)
def cnt(t):
    return s.count(t)

checks = [
    ('NEW JS function leftBasis()', cnt('function leftBasis()'), 1),
    ('NEW JS leftBasis() 调用', cnt('leftBasis()'), 2),                 # 定义 1 + pointerdown 1
    ('NEW JS dragLeftBase', cnt('dragLeftBase'), 5),                    # 声明1 + 赋值3(冻结/up/cancel) + 使用1
    ('NEW JS maxRight 上限', cnt('LEFT_KEEP_MIN - COL_GAP'), 1),
    ('旧拖动换算已清除', cnt('setRight(x - root.getBoundingClientRect().left, false)'), 0),
]
for name, got, exp in checks:
    if got != exp:
        ok = False
    print('   [%s] %s = %d（期望 %d）' % ('OK  ' if got == exp else 'FAIL', name, got, exp))

for t in TAGS:
    c = cnt(t)
    if c != TAG0[t]:
        ok = False
    print('   [%s] tag %-10s = %d（改前 %d）' % ('OK  ' if c == TAG0[t] else 'FAIL', t, c, TAG0[t]))
for b in BIZ:
    c = cnt(b)
    if c != BIZ0[b]:
        ok = False
    print('   [%s] biz %-28s = %d（改前 %d）' % ('OK  ' if c == BIZ0[b] else 'FAIL', b, c, BIZ0[b]))

assert cnt('      var LEFT_KEEP_MIN = 480, LEFT_KEEP_MAX = 600, COL_GAP = 8;') == 1, '常量行被破坏'
assert cnt('function keptLeft()') == 1, 'keptLeft 被破坏'
assert cnt('function applyLeft()') == 1, 'applyLeft 被破坏'

if not ok:
    print('\n>>> FAIL：未写盘')
    sys.exit(1)

io.open(P, 'w', encoding='utf-8').write(s)
print('\n>>> ALL PASS：已写盘 %s（%d → %d 字节，+%d）' % (P, before_len, len(s), len(s) - before_len))

# -*- coding: utf-8 -*-
"""
第 67 轮 B（v2 · 鼠标版）：pages/base.html 的 main 容器（.dot-bg）→ 动态波点

用户口径（本轮原话）：
  「旧版的波点的色彩和位置不变，深色的波点会跟随鼠标移动」
  ⇒ A 层（r12 的浅点阵）：色彩与位置**完全不变**，取消一切动画；
     D 层（深一档的点阵 + 光斑 mask）：光斑圆心由**指针位置**驱动，CSS 过渡做平滑跟随。

两处改动：
  ① CSS：在 r12 原有两条 .dot-bg 规则**之后**追加新块（原规则一字未动）；
  ② JS：在页尾 <!-- /SHELL-TABS-FIX --> 与 </body> 之间注入 DOT-SPOT v1 块。

关键技术点：
  · @property 注册圆心类型 ⇒ 否则 transition 对自定义属性不插值、会瞬间跳变；
  · inherits: true ⇒ JS 无法直接改伪元素样式，必须把变量写在 .dot-bg 上再由 ::before 继承；
  · 过渡写在 .dot-bg 上（主元素值平滑变化，伪元素读继承值）；
  · 层级：main 是 static 无 stacking context、其唯一子元素是 relative；
    ::before 在 tree order 上位于内容之前 ⇒ 与内容同属绘制步骤 6，内容压在其上。
    ⚠️ 刻意不用 isolation:isolate —— 页内有 .skills-popup-overlay{position:fixed;z-index:9999}。

幂等三要素：先判 newmark 命中即 SKIP；未命中要求 OLD 恰好 N 次否则 sys.exit；
「声明增量」只累加实际应用的替换。
自检铁律：只断言 ① 标签级计数（用改前 vs 改后差值，不假设成对）② 被改对象的精确出现次数。
"""
import os
import re
import sys

PATH = 'pages/base.html'
BACKUP = '/tmp/r67-backup/base.html'

CSS_OLD = '.dot-bg{background-image:radial-gradient(circle, rgba(var(--gray-7), 0.1) 1.5px, transparent 1.5px);background-size:20px 20px;}\n' \
          "[giencoder-theme='dark'] .dot-bg{background-image:radial-gradient(circle, rgba(var(--gray-7), 0.1) 1.5px, transparent 1.5px);background-size:20px 20px;}"

CSS_NEWMARK = '/* ★ 第 67 轮：main 容器背景升级为「动态波点」（方案 A+D 鼠标版）'

CSS_BLOCK = """/* ★ 第 67 轮：main 容器背景升级为「动态波点」（方案 A+D 鼠标版）
   A 层 = 上面两条 r12 规则里的浅点阵：色彩与位置**完全不变**（无任何动画）；
   D 层（::before）：再叠一层深一档的点阵，用 mask 圆形光斑把可见范围收进光斑内，
        光斑圆心由指针位置驱动（见页尾注入的脚本块），配 CSS 过渡 ⇒ 平滑跟随。
   注意 @property 的两点：
     ① 必须注册为 <percentage> 类型，否则 transition 对自定义属性不插值、会瞬间跳变；
     ② inherits 必须是 true —— JS 无法直接改伪元素样式，圆心变量只能写在 .dot-bg 上、
        再由 ::before 继承下来。
   层级：main 是 static、无 stacking context，其唯一子元素是 relative；
        ::before 在 tree order 上位于内容之前 ⇒ 与内容同属绘制步骤 6，内容压在其上。
   仅动 mask 圆心，不改任何布局尺寸。 */
@property --dot-x { syntax: '<percentage>'; inherits: true; initial-value: 50%; }
@property --dot-y { syntax: '<percentage>'; inherits: true; initial-value: 46%; }
/* position:relative 只作为 ::before 的定位参照，不改变 flex item 的布局尺寸；
   过渡写在主元素上：值平滑变化后由 ::before 继承，比写在伪元素上更可靠 */
.dot-bg { position: relative; transition: --dot-x 260ms ease-out, --dot-y 260ms ease-out; }
/* D 层：深一档点阵 + 光斑 mask。inset:0 与 main 的 padding box 对齐 ⇒ 两层网格原点一致，
   深色点阵与旧版浅点阵逐点重合，只是"被照亮"。 */
.dot-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image: radial-gradient(circle, rgba(var(--gray-8), 0.22) 1.5px, transparent 1.5px);
  background-size: 20px 20px;
  -webkit-mask-image: radial-gradient(circle 420px at var(--dot-x) var(--dot-y), #000 0%, rgba(0, 0, 0, 0.55) 42%, transparent 78%);
  mask-image: radial-gradient(circle 420px at var(--dot-x) var(--dot-y), #000 0%, rgba(0, 0, 0, 0.55) 42%, transparent 78%);
}
@media (prefers-reduced-motion: reduce) {
  /* 指针跟随属交互响应、保留；只去掉缓动，让光斑瞬时到位。 */
  .dot-bg { transition: none; }
}"""

JS_OLD = '<!-- /SHELL-TABS-FIX -->\n</body>'
JS_NEWMARK = '<!-- /DOT-SPOT -->'

JS_BLOCK = """<!-- DOT-SPOT v1 · main 的深色点阵光斑跟随指针（勿手改此块）
     圆心变量写在 .dot-bg 上（CSS 侧已注册类型并配好过渡），靠 inherits:true 传给 ::before
     —— JS 无法直接改伪元素样式。
     用文档级事件委托、而不是直接给 main 绑定：本块在页面末尾同步执行时，外壳的 main
     还没渲染出来（React 异步挂载），此时 querySelector 只会拿到 null、监听器永远绑不上。
     只在指针落到 main 内时更新；移出后保持最后位置，不回弹。
     仅写入两个百分比变量；指针移动事件用 rAF 节流，每帧至多一次。 -->
    <script>
      (function () {
        var raf = 0, px = null, py = null, host = null;
        function apply() {
          raf = 0;
          if (!host || px === null) return;
          host.style.setProperty('--dot-x', px.toFixed(2) + '%');
          host.style.setProperty('--dot-y', py.toFixed(2) + '%');
        }
        document.addEventListener('pointermove', function (e) {
          var t = e.target;
          var m = t && t.closest ? t.closest('main.dot-bg') : null;
          if (!m) return;
          var r = m.getBoundingClientRect();
          if (!r.width || !r.height) return;
          host = m;
          px = (e.clientX - r.left) / r.width * 100;
          py = (e.clientY - r.top) / r.height * 100;
          if (!raf) raf = requestAnimationFrame(apply);
        }, { passive: true });
      })();
    </script>
    <!-- /DOT-SPOT -->
</body>"""

applied, skipped = [], []


def sub(label, old, new, expect=1):
    txt = open(PATH, encoding='utf-8').read()
    mark = JS_NEWMARK if label.startswith('JS') else CSS_NEWMARK
    if mark in txt:
        skipped.append(label)
        return False
    n = txt.count(old)
    if n != expect:
        sys.exit('✗ [%s] 锚点命中 %d 次（期望 %d）' % (label, n, expect))
    open(PATH, 'w', encoding='utf-8').write(txt.replace(old, new, 1))
    applied.append((label, len(new) - len(old)))
    return True


before = open(BACKUP, encoding='utf-8').read() if os.path.exists(BACKUP) else None
n0 = os.path.getsize(PATH)

sub('CSS dot-bg 动态波点块', CSS_OLD, CSS_OLD + '\n' + CSS_BLOCK + '\n')
sub('JS DOT-SPOT 指针跟随块', JS_OLD, JS_BLOCK)

s = open(PATH, encoding='utf-8').read()
n1 = len(s.encode())

print('应用 %d 项 / 跳过 %d 项' % (len(applied), len(skipped)))
for lab, d in applied:
    print('  ✓ %-26s %+d B' % (lab, d))
for lab in skipped:
    print('  · %-26s (已存在，跳过)' % lab)
print('字节 %d → %d (%+d)' % (n0, n1, n1 - n0))
print()

fails = []


def chk(name, got, want):
    ok = got == want
    print('  %-44s got=%-4s want=%-4s %s' % (name, got, want, '✓' if ok else '✗'))
    if not ok:
        fails.append(name)


print('自检 A：被改对象的精确出现次数')
chk('.dot-bg{（r12 原有两条，一字未动）', s.count('.dot-bg{'), 2)
chk('.dot-bg {（主规则 + reduced-motion 兜底）', s.count('.dot-bg {'), 2)
chk('.dot-bg::before', s.count('.dot-bg::before'), 1)
chk('@property --dot-x', s.count('@property --dot-x'), 1)
chk('@property --dot-y', s.count('@property --dot-y'), 1)
chk('inherits: true（两条 @property 各一）', s.count('inherits: true'), 2)
chk('var(--dot-x)（webkit + 标准 mask 各一）', s.count('var(--dot-x)'), 2)
chk('var(--dot-y)（webkit + 标准 mask 各一）', s.count('var(--dot-y)'), 2)
chk('DOT-SPOT 起止注释', s.count('DOT-SPOT'), 2)
chk('pointermove 新增（改前→改后差值）', s.count('pointermove') - (before.count('pointermove') if before else 0), 1)
chk('prefers-reduced-motion 兜底', s.count('prefers-reduced-motion: reduce'), 1)

print()
print('自检 B：上一版的自动漂移/巡游必须清零')
for k in ('dotDrift', 'dotTour', '@keyframes dotDrift', '@keyframes dotTour'):
    chk('残留 %s' % k, s.count(k), 0)

print()
print('自检 C：标签级计数「改前 vs 改后」差值（本页本就不成对，只比差值）')
if before is None:
    print('  (无改前备份，跳过)')
else:
    # 本轮**有意**注入一个脚本块 ⇒ <script>/</script> 各精确 +1
    # （这正是铁律里允许的"被改对象的精确增减量"），其余标签必须零变化。
    want_delta = {'<style': 0, '</style>': 0, '<script>': 1, '</script>': 1,
                  '<div': 0, '</div>': 0, '</body>': 0}
    for t, wd in want_delta.items():
        a, b = before.count(t), s.count(t)
        ok = (b - a) == wd
        print('  %-12s %-6d → %-6d Δ%+d (期望 %+d) %s' % (t, a, b, b - a, wd, '✓' if ok else '✗'))
        if not ok:
            fails.append('tag ' + t)

print()
print('自检 D：本块 token 化质量')
a = s.find(CSS_NEWMARK)
b = s.find('</style>', a)
blk = s[a:b]
chk('CSS 块锚点有效', len(blk) > 200, True)
hexes = [h for h in re.findall(r'#[0-9a-fA-F]{3,8}\b', blk) if h.lower() != '#000']
chk('本块裸 hex 色值（#000 遮罩黑除外）', len(hexes), 0)
if hexes:
    print('     →', hexes)
chk('本块 var(--gray-8)（D 层点阵色）', blk.count('var(--gray-8)'), 1)

print()
print('自检 E：新增块内不得掺入「被断言的标签字面量」')
# 本轮同一类坑踩了 3 次（注释里复述 SHIMMER_SPREAD / DOT-SPOT v1 / </body>），
# 每次都会让词频类断言误报。这里做一次元层面的守卫，自动拦下复发。
for nm, body, allow_body in (('CSS_BLOCK', CSS_BLOCK, 0), ('JS_BLOCK', JS_BLOCK, 1)):
    for tag, allow in (('</body>', allow_body), ('</html>', 0), ('<body', 0),
                       ('<style', 0), ('</style>', 0), ('<div', 0), ('</div>', 0)):
        cnt = body.count(tag)
        ok = cnt == allow
        print('  %-10s %-10s got=%d allow=%d %s' % (nm, tag, cnt, allow, '✓' if ok else '✗'))
        if not ok:
            fails.append('%s 内含 %s' % (nm, tag))

print()
if fails:
    sys.exit('✗ 自检失败 %d 项：%s' % (len(fails), fails))
print('ALL PASS ✓')

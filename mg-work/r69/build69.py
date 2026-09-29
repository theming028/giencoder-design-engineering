# -*- coding: utf-8 -*-
"""r69 构建：从 task-detail.html 抽取 .td-browse 全要素（HTML / CSS / JS），
改造成数字分身（avatar.html）可用的独立片段，落 mg-work/r69/part-*.{html,css,js}。
不修改任何页面。"""
import re, sys, os, io, json

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = io.open(os.path.join(ROOT, 'pages/task-detail.html'), encoding='utf-8').read()
OUT = os.path.join(ROOT, 'mg-work/r69')

# ---------------------------------------------------------------- 1. HTML
START = '"  <div class=\\"td-split\\" data-td-split=\\"main\\"'
a = T.find(START)
assert a > 0, 'split(main) start not found'
b = T.find('"</aside>"', a)
assert b > 0, 'slot end not found'
e = T.find('"</div>"', b)                      # </aside> 后面紧跟的那一行 = .td-browse-slot 的闭合
assert 0 < e - b < 40, '.td-browse-slot 收尾结构变了，请复核抽取范围'
raw = T[a:e + len('"</div>"')]
# 反解 JS 字符串数组 → 真实 HTML
# ⚠️ 不能用 encode('utf-8').decode('unicode_escape')：会把非 ASCII 按 Latin-1 逐字节解释，
#    整段中文变成 mojibake（aria-label / 可见文案全毁）。逐行 json.loads 才是对的做法。
html_parts = []
for ln in raw.split('\n'):
    t = ln.strip()
    if not t:
        continue
    if t.endswith(','):
        t = t[:-1]
    assert t.startswith('"') and t.endswith('"'), '元素不是单行字符串字面量：' + t[:60]
    html_parts.append(json.loads(t))
html = ''.join(html_parts)
assert '文件目录' in html and '摘要' in html and 'æ' not in html, 'HTML 中文解码异常'
for tg in ('div', 'section', 'aside', 'button', 'span', 'svg', 'header'):
    o, c = html.count('<' + tg), html.count('</' + tg + '>')
    assert o == c, '片段标签不配平：<%s> %d vs </%s> %d' % (tg, o, tg, c)
assert '<div class="td-browse-slot">' in html and html.count('<aside') == 1, 'html decode guard'
# 加 id，便于 JS 定位；并把 td-split(main) 的语义改成「文件预览栏宽度」（见报告说明）
html = html.replace('<div class="td-browse-slot">', '<div class="td-browse-slot" id="av-browse-slot">', 1)
html = html.replace('aria-label="拖动调整 AI 对话框宽度"', 'aria-label="拖动调整文件预览栏宽度"', 1)
html = html.replace('<div class="td-split" data-td-split="main"', '<div class="td-split" id="av-browse-split" data-td-split="main"', 1)
assert 'id="av-browse-split"' in html and 'id="av-browse-slot"' in html, 'id 注入失败'
io.open(os.path.join(OUT, 'part-html.txt'), 'w', encoding='utf-8').write(html)
print('HTML  part bytes=%d  aside=%d  td-bf=%d' % (len(html), html.count('<aside'), html.count('class="td-bf')))

# ---------------------------------------------------------------- 2. CSS
CSS_A, CSS_B = 335694, 452120                     # 本页 <style> 第 3 块
css = T[CSS_A:CSS_B]

def chunks(src):
    i, out = 0, []
    while i < len(src):
        if src.startswith('/*', i):
            j = src.find('*/', i + 2)
            if j < 0: break
            out.append(('c', src[i:j + 2])); i = j + 2
        elif src[i] in ' \n\t\r':
            j = i
            while j < len(src) and src[j] in ' \n\t\r': j += 1
            out.append(('w', src[i:j])); i = j
        else:
            j = src.find('{', i)
            if j < 0: break
            d, k = 1, j + 1
            while k < len(src) and d:
                if src[k] == '{': d += 1
                elif src[k] == '}': d -= 1
                k += 1
            out.append(('r', src[i:k])); i = k
    return out

CH = chunks(css)
KEEP = re.compile(r'td-browse|td-bf|td-code|td-split|is-browse|is-col-dragging|td-ctx|giencoder-dropdown|tdBrows')
DROP_HEADS = [  # 详情页三栏布局专用，avatar 无对应对象 → 整体丢弃
    '.td-root.is-browse .td-left',
    '.td-root.is-browse .td-gutter',
    '.td-root.is-browse .td-side',
    '.td-root.is-browse',
    '.td-root.is-browse, .td-root.is-browse.is-swapped',
    '.td-root.is-browse .td-right-inner, .td-root.is-browse.is-collapsed .td-right-inner',
    '.td-root.is-browse .td-collapsed, .td-root.is-browse.is-collapsed .td-collapsed',
    '.td-root.is-browse.is-keep-left .td-left',
]
DROP_HEADS = {re.sub(r'\s+', ' ', h).strip() for h in DROP_HEADS}
def norm(head):
    return re.sub(r'\s+', ' ', head).strip()

kept, n_drop, n_rules = set(), [], 0
for idx, (kind, txt) in enumerate(CH):
    if kind != 'r':
        continue
    head = txt.split('{', 1)[0]
    if not KEEP.search(head):
        continue
    n_rules += 1
    n = norm(head)
    if '.td-more' in n:            # 详情页「更多操作」菜单（r59/r64）专用，avatar 无此对象
        n_drop.append(n); continue
    if n in DROP_HEADS:
        n_drop.append(n); continue
    if n == '.td-root.is-browse .td-right' and 'border-top-right-radius' not in txt:
        n_drop.append(n + ' (width 版，avatar 走 --av-chat-w)'); continue
    kept.add(idx)
    # 带上紧邻的注释块
    j = idx - 1
    while j >= 0 and CH[j][0] == 'w': kept.add(j); j -= 1
    if j >= 0 and CH[j][0] == 'c': kept.add(j)

out = ''.join(CH[i][1] for i in range(len(CH)) if i in kept)
# 状态前缀改写
out = out.replace('.td-root.is-browse.is-keep-left', '.av-browse-on')
out = out.replace('.td-root.is-browse', '.av-browse-on')
out = out.replace('.td-root.is-col-dragging', '.av-browse-on.is-col-dragging')
# .td-gutter(详情页那条 8px 缝) → 数字分身的 .av-chat-gutter
out = out.replace('.av-browse-on .td-gutter', '.av-browse-on .av-chat-gutter')
# 预览栏宽度策略：固定 641px（树 240 + 分栏条 1 + 代码 400），main 吃剩余
out = out.replace('.td-browse-slot { display: none; flex: 1 1 auto; min-width: 0; overflow: hidden; }',
                  '.td-browse-slot { display: none; flex: 0 0 var(--av-browse-w, 641px); min-width: 0; overflow: hidden; }')

# 注释里残留的 .td-root 措辞一并改写（本页没有 .td-root；避免注释与实际选择器不一致）
out = out.replace('⚠️ 必须套一层裁剪窗口 .td-browse-slot：.td-root 是 overflow:visible\n'
                  '            （第 24 轮为放两栏投影特意放开的），直接给 .td-browse 加 translateX\n'
                  '            会让整栏溢出到外壳右侧、撑出横向滚动条。',
                  '⚠️ 必须套一层裁剪窗口 .td-browse-slot：shell 的 flex 行是 overflow:visible，\n'
                  '            直接给 .td-browse 加 translateX 会让整栏溢出到外壳右侧、撑出横向滚动条。')

hdr = """/* ================================================================================
   ★ 第 69 轮：文件预览栏（.td-browse / .td-bf / .td-code / .td-split / .td-ctx）
   来源 = 研发工作台 › 任务详情页（task-detail.html）同名模块，**逐条抽取 + 最小改造**：
     · 状态前缀 `.td-root.is-browse` → `.av-browse-on`（挂在 shell 的 flex 行上，见 JS 段）；
     · 丢弃详情页三栏布局专用规则（.td-left / .td-gutter 让位、is-keep-left、--td-browse-right-w
       宽度接管、is-collapsed 复位）—— 数字分身没有这些对象；
     · `.td-gutter` 的浏览态隐藏改指本页的 `.av-chat-gutter`；
     · `.td-browse-slot` 由 flex:1 改为 `flex: 0 0 var(--av-browse-w, 641px)`（口径：预览栏保底 641）。
   其余（配色 / 尺寸 / 圆角 / 动效 / 右键菜单）一字未改，token 全部沿用 var()。
   ================================================================================ */
:root { --td-panel-line: #DAE3ED; --td-hairline: var(--color-border-1); }
/* ★ 左导航让位（本轮口径）：预览栏展开时，shell 的左导航栏宽度平滑收拢到 0。
   导航宽度是 React 内联 style ⇒ 必须 !important；元素自带 overflow:hidden，
   收拢过程中内容被裁掉，无需额外处理；过渡沿用外壳自带的 200ms transition-all。
   摘掉类名时内联宽度原样恢复，同样走 200ms 动画。 */
.av-browse-on > aside:first-child {
  width: 0 !important; min-width: 0 !important;
  padding-left: 0 !important; padding-right: 0 !important;
  opacity: 0; pointer-events: none;
}
"""
hdr += '''/* ---- 轻提示（DS Message）：右键菜单结果回执（同详情页 .td-dp-msg 口径） ---- */
.td-dp-msg { position: fixed; top: 64px; left: 50%; transform: translateX(-50%); z-index: 1100; }
.td-dp-msg[hidden] { display: none; }
.td-dp-msg .giencoder-message-icon { display: inline-flex; color: var(--color-success-6); }
'''
io.open(os.path.join(OUT, 'part-css.css'), 'w', encoding='utf-8').write(hdr + out)
print('CSS   rules=%d kept=%d dropped=%d bytes=%d' % (n_rules, len(kept), len(n_drop), len(out) + len(hdr)))
for x in n_drop: print('   drop:', x)
_nocomment = re.sub(r'/\*.*?\*/', '', out, flags=re.S)
assert '.td-root' not in _nocomment, 'CSS 仍残留 .td-root（非注释）'
assert 'is-browse' not in _nocomment, 'CSS 仍残留 is-browse'
assert 'flex: 0 0 var(--av-browse-w, 641px)' in out, 'slot 宽度策略未生效'
print('--- 产出选择器 ---')
for m in re.finditer(r'(?m)^([^\n{}][^{}\n]*?)\{', out):
    print('   ', m.group(1).strip()[:110])
print()

# ---------------------------------------------------------------- 3. JS: 右键菜单
C0 = T.rfind('  function bindBrowseContextMenu', 0, 636600)
j = T.find('{', C0); d, k = 1, j + 1
while k < len(T) and d:
    if T[k] == '{': d += 1
    elif T[k] == '}': d -= 1
    k += 1
ctx = T[C0:k]
assert ctx.count('td-ctx-bound') == 2 and 'OPEN_WITH' in ctx, 'ctx fn guard'
ctx = ctx.replace("var root = document.querySelector('.td-root');",
                  "var root = document.querySelector('.td-browse-slot');")
ctx = ctx.replace("root.classList.contains('is-browse')", 'avBrowseOpen()')
ctx = ctx.replace('tdToast(', 'avToast(')
assert '.td-root' not in ctx and 'is-browse' not in ctx and 'tdToast' not in ctx, 'ctx substitutions incomplete'
io.open(os.path.join(OUT, 'part-ctx.js'), 'w', encoding='utf-8').write(ctx)
print('CTX   bytes=%d  avBrowseOpen uses=%d  avToast uses=%d' % (len(ctx), ctx.count('avBrowseOpen()'), ctx.count('avToast(')))

# ---------------------------------------------------------------- 4. JS: 控制器（骨架抄自 task-detail，按 avatar 布局改写）
tp = os.path.join(OUT, 'ctrl-template.js')
if os.path.exists(tp):
    CTRL = io.open(tp, encoding='utf-8').read()
    CTX = io.open(os.path.join(OUT, 'part-ctx.js'), encoding='utf-8').read()
    assert CTRL.count('/*__CTX__*/') == 1, 'ctrl 模板缺 __CTX__ 占位'
    CTRL = CTRL.replace('/*__CTX__*/', CTX)
    io.open(os.path.join(OUT, 'part-ctrl.js'), 'w', encoding='utf-8').write(CTRL)
    print('CTRL  bytes=%d (含 ctx %d)' % (len(CTRL), len(CTX)))
    for bad in ('</script', '</style', '<script', '<style'):
        assert bad not in CTRL, 'ctrl 含非法标签字面量: ' + bad
else:
    print('CTRL  skipped (ctrl-template.js 未就绪)')

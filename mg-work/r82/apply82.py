# -*- coding: utf-8 -*-
"""
r82 · 四条修订（邵先生 2026-09-29 第二轮反馈）

  1. 「切换工艺流程空间」触发器的**激活态**背景色与 hover 一致（#DAE3ED）。
     → 落在 r81 块里追加一条 `[aria-expanded="true"]` 规则（不改 r81 其余内容）。
  2. 研发工作台「需求看板 / 任务看板」两个 tab 切换要有**滑动动效**。
     → kanban.html / req-kanban.html 注入 .kb-radio-thumb 滑动指示器 + 跨页续滑。
  3. 「待协作任务」弹窗加**装饰性界面元素**。
     → 高保真设计稿 layer 1389:18525（== 本地落盘 vc875:31526，逐字节相同）：
        面板上缘左右角各一枚「外扩玻璃翼」——24 × 10.75，白色 95% + 投影，
        形状 = 24×24 凹角圆角片（path M0 0 L24 0 L24 24 C24 10.745 13.25 0 0 0 Z）纵向压到 10.75。

落地方式沿用 r73/r74/r80/r81 前例：`<style id="rNN-…-css">` + `<script id="rNN-…-js">`
注入到 `</body>` 前。本脚本先把**上一版同名块**摘掉再插新的，故可反复跑（幂等）。

r81 块的 CSS/JS 主体**直接从 r81/apply81.py 导入**（单一事实来源），只在其后追加第 1 条规则。

用法：
  python mg-work/r82/apply82.py
  cp mg-work/r82/before/<page>.html pages/<page>.html      # 回滚
"""
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))                       # mg-work/r82
ROOT = os.path.dirname(os.path.dirname(HERE))                           # 仓库根


# ────────────────────────────────────────────────────────────────
# 0. 复用 r81 的块（单一事实来源），并追加第 1 条规则
# ────────────────────────────────────────────────────────────────
def _load_apply81():
    p = os.path.join(ROOT, 'mg-work', 'r81', 'apply81.py')
    spec = importlib.util.spec_from_file_location('apply81_src', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


A81 = _load_apply81()

WS_EXTRA_CSS = """
/* ── r82 追加（邵先生 2026-09-29 第 1 条）──────────────────────────────
   触发器「激活态」（浮窗已展开）的背景色与 hover 一致。
   aria-expanded 由本块的 JS 在 show()/hide() 里同步，无额外状态类。 */
.r81-ws-trigger[aria-expanded="true"] {
  background-color: var(--r81-hover-bg);
}
"""

WS_CSS = A81.CSS + WS_EXTRA_CSS
WS_JS = A81.JS


# ────────────────────────────────────────────────────────────────
# 1. 看板 tab 滑动动效（kanban / req-kanban）
# ────────────────────────────────────────────────────────────────
TABS_CSS = """
/* ★ 第 82 轮：研发工作台「需求看板 ↔ 任务看板」切换的滑动动效。
   背景：两个 tab 各占一页（data-goto 跳转），原先只有 is-on 的硬切换，没有过渡。
   做法：在 .kb-radio 里加一个绝对定位的 .kb-radio-thumb（白底 + 1px 描边 + radius 8），
        由 JS 按当前 is-on 按钮的 offset 就位；点击时先把它滑到目标按钮、再跳转；
        新页面加载时读 sessionStorage 里的来源 tab，使指示器「从来源滑到当前」——
        跨页看起来是一段连续的滑动。
   ⚠ .kb-radio 自身是 position:absolute（既有），故 thumb 的包含块就是它，
     left/top 直接取按钮的 offsetLeft/offsetTop，与容器 left 被 JS 改写无关。 */
.kb-radio-thumb {
  position: absolute;
  left: 0;
  top: 0;
  width: 0;
  height: 0;
  box-sizing: border-box;
  border: 1px solid var(--color-border-2);
  border-radius: 8px;
  background: var(--color-bg-1);
  pointer-events: none;
  z-index: 0;
  opacity: 0;
  transition: left 220ms cubic-bezier(.4, 0, .2, 1), top 220ms cubic-bezier(.4, 0, .2, 1),
              width 220ms cubic-bezier(.4, 0, .2, 1), height 220ms cubic-bezier(.4, 0, .2, 1),
              opacity 120ms linear;
}
/* 指示器就位后才显示，避免首帧闪一下 */
.kb-radio--thumbed .kb-radio-thumb {
  opacity: 1;
}
/* 指示器接管视觉，原 is-on 自身的底/描边让位（保留 1px 边框占位，布局零变化） */
.kb-radio--thumbed .kb-radio-btn {
  position: relative;
  z-index: 1;
}
.kb-radio--thumbed .kb-radio-btn.is-on {
  background: transparent;
  border-color: transparent;
}
"""

TABS_JS = """
/* SHELL-KBTAB-SLIDE v1 —— 看板 tab 滑动动效（勿手改此块；落地脚本 mg-work/r82/apply82.py） */
/* 只改「怎么切」，不改「切换到哪」：data-goto / 目标页一律沿用既有标记。 */
(function () {
  if (window.__r82tabs) return;
  window.__r82tabs = 1;

  var KEY = 'giencoder-kb-tab-from';   /* 记「从哪个 tab 出发」，供目标页续滑 */
  var EASE = 220;                      /* 与 CSS transition 时长一致 */

  var host = null, thumb = null, busy = false;

  function q(sel, root) { return (root || document).querySelector(sel); }
  function onBtn() { return host && q('.kb-radio-btn.is-on', host); }
  function rectOf(b) { return { l: b.offsetLeft, t: b.offsetTop, w: b.offsetWidth, h: b.offsetHeight }; }

  function put(r, animate) {
    if (!thumb) return;
    if (!animate) thumb.style.transition = 'none';
    thumb.style.left = r.l + 'px';
    thumb.style.top = r.t + 'px';
    thumb.style.width = r.w + 'px';
    thumb.style.height = r.h + 'px';
    if (!animate) {
      void thumb.offsetWidth;          /* 强制回流，让「无动画落位」立即生效 */
      thumb.style.transition = '';
    }
  }

  /* 让指示器就位（无动画），用于首次挂载 / 尺寸变化 / 兜底 */
  function settle() {
    if (busy) return;
    var b = onBtn();
    if (b) put(rectOf(b), false);
  }

  function init() {
    host = q('.kb-radio');
    if (!host) return false;
    var btns = host.querySelectorAll('.kb-radio-btn');
    if (btns.length < 2) return false;
    if (q('.kb-radio-thumb', host)) { settle(); return true; }

    thumb = document.createElement('span');
    thumb.className = 'kb-radio-thumb';
    thumb.setAttribute('aria-hidden', 'true');
    host.insertBefore(thumb, host.firstChild);
    host.classList.add('kb-radio--thumbed');

    var cur = onBtn();
    if (!cur) return true;

    /* 上一页留下的来源 tab → 先落到来源位置，再滑到当前（跨页续滑） */
    var from = null;
    try { from = sessionStorage.getItem(KEY); sessionStorage.removeItem(KEY); } catch (e) {}
    if (from) {
      var src = null;
      for (var i = 0; i < btns.length; i++) {
        if (btns[i] !== cur && btns[i].getAttribute('data-goto') === from) { src = btns[i]; break; }
      }
      if (src) {
        put(rectOf(src), false);
        requestAnimationFrame(function () {
          requestAnimationFrame(function () { put(rectOf(cur), true); });
        });
        /* 字体/选择器宽度稳定后再纠一次位 */
        if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { settle(); });
        return true;
      }
    }
    put(rectOf(cur), false);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { settle(); });
    return true;
  }

  /* 点击：先把指示器滑到目标，再跳转（capture 先于页面既有的 location.href 处理器） */
  document.addEventListener('click', function (ev) {
    var t = ev.target && ev.target.closest ? ev.target.closest('.kb-radio-btn[data-goto]') : null;
    if (!t || !host || !host.contains(t)) return;
    if (t.classList.contains('is-on')) { ev.preventDefault(); ev.stopPropagation(); return; }
    var goto = t.getAttribute('data-goto');
    if (!goto) return;
    ev.preventDefault();
    ev.stopPropagation();

    try { sessionStorage.setItem(KEY, goto); } catch (e) {}

    var cur = onBtn();
    busy = true;
    if (cur) {
      /* 图标（.kb-radio-ico）只在激活态的按钮上；整体搬过去，按钮宽度才与激活态一致 */
      var ico = q('.kb-radio-ico', cur);
      cur.classList.remove('is-on');
      cur.setAttribute('aria-selected', 'false');
      t.classList.add('is-on');
      t.setAttribute('aria-selected', 'true');
      if (ico && !q('.kb-radio-ico', t)) t.appendChild(ico);
    }
    if (thumb) {
      var r = rectOf(t);
      requestAnimationFrame(function () {
        thumb.style.left = r.l + 'px';
        thumb.style.top = r.t + 'px';
        thumb.style.width = r.w + 'px';
        thumb.style.height = r.h + 'px';
      });
    }
    setTimeout(function () { location.href = goto; }, EASE + 40);
  }, true);

  if (!init()) {
    var mo = new MutationObserver(function () { if (init()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
  }
  /* 容器尺寸变化（项目选择器变宽 / 字体就绪）→ 纠位 */
  if (window.ResizeObserver) {
    window.addEventListener('load', function () {
      if (host) new ResizeObserver(function () { settle(); }).observe(host);
    });
  }
})();
"""


# ────────────────────────────────────────────────────────────────
# 2. 【已弃用 · 保留备查】「待协作任务」弹窗的装饰性界面元素（kanban）
#    —— 高保真设计稿 layer 1389:18525（== 落盘 vc875:31526）
#    ⚠️ 2026-09-29 邵先生反馈「装饰翼效果很差，干脆去掉」⇒ **已从装配链摘除**：
#       不再进 BLOCK_IDS / BLOCK_SRC / PAGE_BLOCKS / TOKENS / ANCHORS，
#       但 PRIOR 里保留 r82-coop-* 的摘除规则 ⇒ 复跑本脚本会把页面里既有
#       的两枚翼自动清掉（幂等，无需手改 pages/kanban.html）。
#       下面这段常量只是留档（含反解出的几何与落位公式），**不参与任何注入**。
# ────────────────────────────────────────────────────────────────
COOP_CSS = """
/* ★ 第 82 轮：「待协作任务」弹窗的装饰性界面元素（邵先生 2026-09-29 第 3 条）。
   设计稿 layer 1389:18525（与落盘 vc875:31526 逐字节相同）：
     面板上缘左右角各一枚「外扩玻璃翼」，组尺寸 1278 × 39.1，贴合 1200 宽面板
     （面板 120,48,1200,804 ⇒ 翼的左缘 81 = 120 − 39、右缘 1359 = 1320 + 39）。
     单枚形状 path「M0 0 L24 0 L24 24 C24 10.745 13.25 0 0 0 Z」，即 24×24 的凹角圆角片；
     组高 39.1 对应 viewBox 高 87.096 ⇒ 纵向压缩比 0.4479，故实高 = 24 × 0.4479 ≈ 10.75。
     实心 #FFFFFF / 95%，投影 dy 8 blur 8 rgba(0,0,0,.12)。
   实测（设计稿 PNG 1440×900 逐像素）：面板上缘 48，左翼在 y=50 时左伸到 x=107、
     y=53 → 112、y=56 归位 120 ⇒ 与上式算得的弧线逐点吻合（差 2~3px 为 95% 白 + 投影的抗锯齿）。
   ⚠ 必须挂在 .kb-coop 上而不是 .kb-coop-dialog：后者是 overflow:hidden，翼会被裁掉。 */
.r82-coop-wing {
  position: absolute;
  width: 24px;
  height: 10.75px;
  z-index: 2;
  pointer-events: none;
  filter: drop-shadow(0 8px 8px rgba(0, 0, 0, .12));
  /* 未就位前不显示 —— 弹窗收起时 rect 为 0，量不出位置，避免闪在左上角 */
  opacity: 0;
  transition: opacity 160ms linear;
}
.r82-coop-wing[data-placed] {
  opacity: 1;
}
.r82-coop-wing svg {
  display: block;
  width: 100%;
  height: 100%;
}
.r82-coop-wing path {
  fill: #FFFFFF;
  fill-opacity: .95;
}
/* 右翼 = 左翼镜像 */
.r82-coop-wing--r {
  transform: scaleX(-1);
}
"""

# 单枚「翼」的形状：24×24 凹角圆角片，纵向压缩到 10.75
WING_PATH = 'M0 0 L24 0 L24 10.75 C24 4.8125 13.25 0 0 0 Z'
WING_SVG = ('<svg viewBox="0 0 24 10.75" width="24" height="10.75" aria-hidden="true">'
            '<path d="%s"/></svg>' % WING_PATH)

COOP_JS = """
/* SHELL-COOP-WINGS v1 —— 「待协作任务」弹窗上缘装饰翼（勿手改此块；落地脚本 mg-work/r82/apply82.py） */
/* 设计稿 layer 1389:18525。挂在 .kb-coop（非 .kb-coop-dialog，后者 overflow:hidden 会裁掉）。
   位置由弹窗面板实时几何推出：左翼右缘贴面板左缘，右翼左缘贴面板右缘，顶边同高。 */
(function () {
  if (window.__r82coop) return;
  window.__r82coop = 1;

  var WING = '__WING__';
  var host = null, dlg = null, lw = null, rw = null, mo = null;

  function make(cls) {
    var e = document.createElement('span');
    e.className = 'r82-coop-wing ' + cls;
    e.setAttribute('aria-hidden', 'true');
    e.innerHTML = WING;
    return e;
  }

  /* 弹窗面板：left 50% + translateX(-50%) 居中，top 0；翼贴在面板上缘两端，
     左翼右缘 = 面板左缘、右翼左缘 = 面板右缘、顶边与面板顶边同高。
     用 rect 相减（含 transform 的视觉真值）再减掉 .kb-coop 的 border，
     得到相对 .kb-coop padding box 的偏移 —— 与绝对定位子元素的包含块一致。 */
  function place() {
    if (!host || !dlg || !lw || !rw) return false;
    var dr = dlg.getBoundingClientRect();
    if (!dr.width) return false;                  /* 收起态量不出，跳过 */
    var cr = host.getBoundingClientRect();
    var L = dr.left - (cr.left + host.clientLeft);
    var T = dr.top - (cr.top + host.clientTop);
    lw.style.left = Math.round(L - 24) + 'px';
    lw.style.top = Math.round(T) + 'px';
    rw.style.left = Math.round(L + dr.width) + 'px';
    rw.style.top = Math.round(T) + 'px';
    if (!lw.hasAttribute('data-placed')) {
      lw.setAttribute('data-placed', '');
      rw.setAttribute('data-placed', '');
    }
    return true;
  }

  /* 开合/尺寸变化都在多个时间点补量：弹窗有 240ms 出场动效，且收起态量不到。 */
  function schedule() {
    [0, 60, 200, 420].forEach(function (d) { setTimeout(place, d); });
  }

  function init() {
    host = document.querySelector('.kb-coop');
    if (!host) return false;
    dlg = host.querySelector('.kb-coop-dialog');
    if (!dlg) return false;
    lw = host.querySelector('.r82-coop-wing--l');
    rw = host.querySelector('.r82-coop-wing--r');
    if (!lw || !rw) {
      lw = make('r82-coop-wing--l');
      rw = make('r82-coop-wing--r');
      host.appendChild(lw);
      host.appendChild(rw);
    }
    if (!mo && window.MutationObserver) {
      /* hidden / class 变化 = 弹窗开合，重新落位 */
      mo = new MutationObserver(schedule);
      mo.observe(host, { attributes: true, attributeFilter: ['hidden', 'class'] });
    }
    place();
    return true;
  }

  if (!init()) {
    var boot = new MutationObserver(function () { if (init()) boot.disconnect(); });
    boot.observe(document.body, { childList: true, subtree: true });
  }
  window.addEventListener('resize', schedule);
  /* 点触发器等入口时提前排几次补量（click 与 pointerdown 都挂，兼容程序化调用） */
  ['click', 'pointerdown', 'keydown'].forEach(function (t) {
    document.addEventListener(t, function (e) {
      if (!host) return;
      var tg = e.target;
      if (!tg || !tg.closest) return;
      if (tg.closest('.kb-stat--coop, .kb-coop-close, .kb-coop-mask')) schedule();
    }, true);
  });
})();
""".replace('__WING__', WING_SVG)


# ────────────────────────────────────────────────────────────────
# 3. 拼块
# ────────────────────────────────────────────────────────────────
def style_block(bid, css):
    return '<style id="%s">\n%s\n</style>' % (bid, css)


def script_block(bid, js):
    return '<script id="%s">\n%s\n</script>' % (bid, js)


BLOCK_IDS = {
    'ws': ('r81-ws-css', 'r81-ws-js'),
    'tabs': ('r82-tabs-css', 'r82-tabs-js'),
}
BLOCK_SRC = {
    'ws': (WS_CSS, WS_JS),
    'tabs': (TABS_CSS, TABS_JS),
}
BLOCKS = {k: (style_block(BLOCK_IDS[k][0], BLOCK_SRC[k][0]),
              script_block(BLOCK_IDS[k][1], BLOCK_SRC[k][1])) for k in BLOCK_IDS}

# 每页要装配的块（顺序 = 注入顺序）
PAGE_BLOCKS = {
    'dev.html': ['ws'],
    'kanban.html': ['ws', 'tabs'],
    'req-kanban.html': ['ws', 'tabs'],
    'task-detail.html': ['ws'],
}

# 上一版留下的块（先摘后插，保证内容可迭代）
PRIOR = (
    (r'<style id="r81-ws-css">.*?</style>', '</style>'),
    (r'<script id="r81-ws-js">.*?</script>', '</script>'),
    (r'<style id="r82-tabs-css">.*?</style>', '</style>'),
    (r'<script id="r82-tabs-js">.*?</script>', '</script>'),
    (r'<style id="r82-coop-css">.*?</style>', '</style>'),
    (r'<script id="r82-coop-js">.*?</script>', '</script>'),
)

# 每页改前必须存在的锚点（防呆：被别的轮次改过就停手）
# ⚠ 看板/弹窗的标记写在页面里那份「注入用 HTML 字符串」中，属性引号是**转义**形态
#   （源码里是 class=\"kb-radio\"），故锚点必须按转义形态写。
KB_RADIO = 'class=\\"kb-radio\\"'
KB_COOP = 'class=\\"kb-coop\\"'

ANCHORS = {
    'dev.html': ['justify-end gap-1', 'bg-[#FF5F57]'],
    'kanban.html': ['justify-end gap-1', 'bg-[#FF5F57]', KB_COOP, KB_RADIO],
    'req-kanban.html': ['justify-end gap-1', 'bg-[#FF5F57]', KB_RADIO],
    'task-detail.html': ['justify-end gap-1', 'bg-[#FF5F57]'],
}

MARKERS = ('</style>', '</script>', '<style', '<script', '</body>', '</html>', '</head>', '<body')

# 每个块独有的类名锚点（用于精确计数断言）
TOKENS = {
    'ws': ['r81-ws-trigger', 'r81-ws-panel', 'r81-ws-ibadge'],
    'tabs': ['kb-radio-thumb', 'kb-radio--thumbed'],
}


def meta_guard():
    """护身符：新块里不得出现会破坏 HTML 结构的标签字面量。

    CSS 块只允许自己那一对 <style>/</style>；JS 块只允许自己那一对 <script>/</script>；
    两者都不允许出现 body/head/html 级的标签（否则会截断当前文档）。
    """
    common = (('</body>', 0), ('</html>', 0), ('</head>', 0), ('<body', 0), ('<html', 0), ('<head', 0))
    rules = {
        'css': common + (('</style>', 1), ('<style', 1), ('</script>', 0), ('<script', 0)),
        'js': common + (('</script>', 1), ('<script', 1), ('</style>', 0), ('<style', 0)),
    }
    for kind, (cssb, jsb) in BLOCKS.items():
        for part, name, key in ((cssb, kind + '/css', 'css'), (jsb, kind + '/js', 'js')):
            for bad, allowed in rules[key]:
                n = part.count(bad)
                if n != allowed:
                    sys.exit('!! 元守卫失败：%s 里 %r 出现 %d 次（应为 %d）' % (name, bad, n, allowed))
        if '<div' in cssb or '</div>' in cssb:
            sys.exit('!! 元守卫失败：%s 的 CSS 里出现 div 标签字面量' % kind)


def apply_page(fname):
    page = os.path.join(ROOT, 'pages', fname)
    with open(page, encoding='utf-8') as f:
        s = f.read()
    n_orig = len(s)

    # —— 先摘旧块 ——
    dropped = 0
    for pat, _ in PRIOR:
        s, k = re.subn(pat, '', s, count=1, flags=re.S)
        dropped += k
    if dropped not in (0, 2, 4, 6):
        sys.exit('!! %s 旧块删除数量异常：%d' % (fname, dropped))
    for tok in ('id="r81-ws-css"', 'id="r81-ws-js"', 'id="r82-tabs-css"',
                'id="r82-tabs-js"', 'id="r82-coop-css"', 'id="r82-coop-js"'):
        if tok in s:
            sys.exit('!! %s 摘除旧块后仍残留 %s' % (fname, tok))

    # —— 锚点防呆 ——
    for a in ANCHORS[fname]:
        if a not in s:
            sys.exit('!! %s 缺少锚点 %r' % (fname, a))
    if s.count('</body>') != 1:
        sys.exit('!! %s 的 </body> 不是恰好 1 个（%d）' % (fname, s.count('</body>')))

    # —— 基线计数 ——
    n0 = len(s)
    base = dict(
        script=s.count('<script'),
        escript=s.count('</script>'),
        style=s.count('<style'),
        estyle=s.count('</style>'),
        body=s.count('</body>'),
        right=s.count('justify-end gap-1'),
        mh=s.count('maxHeight:480'),
        lights=s.count('bg-[#FF5F57]'),
        kbra=s.count(KB_RADIO),
        kbco=s.count(KB_COOP),
    )
    for m in MARKERS:
        base['m_' + m] = s.count(m)

    parts = []
    for kind in PAGE_BLOCKS[fname]:
        parts.append(BLOCKS[kind][0])
        parts.append(BLOCKS[kind][1])
    BLOCK = ''.join(parts)
    n_style = sum(1 for k in PAGE_BLOCKS[fname])
    n_script = n_style

    s2 = s.replace('</body>', BLOCK + '</body>', 1)

    # —— 自检 1：标签级精确增减 ——
    checks = (('<script', base['script'] + n_script), ('</script>', base['escript'] + n_script),
              ('<style', base['style'] + n_style), ('</style>', base['estyle'] + n_style),
              ('</body>', base['body']))
    for tok, want in checks:
        got = s2.count(tok)
        if got != want:
            sys.exit('!! %s %r 计数 %d（应为 %d）' % (fname, tok, got, want))

    # —— 自检 2：被改对象的精确计数 ——
    for m in MARKERS:
        if s2.count(m) != base['m_' + m] + BLOCK.count(m):
            sys.exit('!! %s 标记 %r 增量异常' % (fname, m))
    for k, v in (('justify-end gap-1', base['right']), ('maxHeight:480', base['mh']),
                 ('bg-[#FF5F57]', base['lights']), (KB_RADIO, base['kbra']),
                 (KB_COOP, base['kbco'])):
        if s2.count(k) != v:
            sys.exit('!! %s 既有锚点 %r 被改动' % (fname, k))
    # 注入块 id 各恰好一份
    for kind in PAGE_BLOCKS[fname]:
        for bid in BLOCK_IDS[kind]:
            if s2.count('id="%s"' % bid) != 1:
                sys.exit('!! %s 注入块 id %s 计数异常' % (fname, bid))
    # 块内独有 token 的精确计数（既校验块内容未偏移，也校验只注入了这一份）
    for kind in PAGE_BLOCKS[fname]:
        for tok in TOKENS[kind]:
            want = BLOCK.count(tok)
            if want == 0:
                sys.exit('!! %s/%s 的 token %r 在块内不存在' % (fname, kind, tok))
            if s2.count(tok) != want:
                sys.exit('!! %s token %r 计数 %d（块内 %d）' % (fname, tok, s2.count(tok), want))
    # 新块紧贴 </body>（即排在全部既有注入块之后）
    i = s2.find(BLOCK)
    if i < 0 or s2[i + len(BLOCK):i + len(BLOCK) + 7] != '</body>':
        sys.exit('!! %s 新块未紧贴 </body>（可能不是最后一块）' % fname)
    # 第 1 条：激活态规则必须在 WS 块里恰好一条
    if 'ws' in PAGE_BLOCKS[fname]:
        if WS_CSS.count('r81-ws-trigger[aria-expanded="true"]') != 1:
            sys.exit('!! WS CSS 缺激活态规则')
    # 字节数增量
    if len(s2) != n0 + len(BLOCK):
        sys.exit('!! %s 字符数增量异常' % fname)

    with open(page, 'w', encoding='utf-8') as f:
        f.write(s2)
    return (fname, n_orig, n0, len(s2), dropped, PAGE_BLOCKS[fname])


def main():
    meta_guard()
    rows = []
    for fname in PAGE_BLOCKS:
        rows.append(apply_page(fname))
    print()
    for fname, n_orig, n0, n1, dropped, kinds in rows:
        note = '（摘掉上一版块 %d 件：%d → %d）' % (dropped, n_orig, n0) if dropped else ''
        print('%-18s %d → %d (%+d)  块=%s %s' % (fname, n0, n1, n1 - n0, '+'.join(kinds), note))


if __name__ == '__main__':
    main()

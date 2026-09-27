# -*- coding: utf-8 -*-
"""第 34 轮第 2 项 —— 在 pages/avatar.html 上挂载「通过对话完善数字分身」的右侧 AI 对话栏抽屉。

设计原则（沿用仓内既有惯例）：
  1. 页面是外部 Vite 工程的 `viteSingleFile` 产物（源工程不在本仓），只能在产物上打补丁
     → 与 `mg-work/r25/apply-shell-tabs.py` 同法：在 `</body>` 前追加一段自建
     `<style>` + DOM + `<script>`，用成对注释标记包裹以实现「幂等 + 可升级」。
  2. AI 对话栏本体**完全复用** `pages/task-detail.html` 里已验证的右栏模块 ——
     同名类、不改名、不新增同义视觉类；构建期从 task-detail.html **实时抽取**，
     保证本页与详情页永远同源同步（详情页改了，重跑本脚本即同步）。
  3. 只允许一层「视图适配层」，前缀 `av-`，作用在组件类上，不改组件本体：
       · 几何：把详情页的「右栏固定列」变成「贴右侧的抽屉」；
       · 状态：把详情页的 `.td-root.is-fullscreen / .is-collapsed`
               原样改写成 `.av-chat-drawer.is-fullscreen / .is-collapsed`
               （于是详情页「全屏后内容 860px 居中」的规则被原封不动继承下来）。
  4. 触发器落点：内容标题行。实测全页 `div.flex.items-start.justify-between` **只有 1 个**
     （数字分身页的「数字分身」标题 + 新建分身），故可按该结构选择器安全定位；
     页头右侧已被搜索框 + 头像占满（`div.flex.w-60` 起 x=1184），不能放页头。

幂等：页内已有 `<!-- AV-CHAT-DRAWER ... -->` … `<!-- /AV-CHAT-DRAWER -->` 时整块替换。

用法：C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe mg-work/r34/build-avatar.py
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "pages", "task-detail.html")     # 模块权威源
DEST = os.path.join(ROOT, "pages", "avatar.html")          # 目标页
START = "<!-- AV-CHAT-DRAWER"
END = "<!-- /AV-CHAT-DRAWER -->"
VERSION = ("v2 —— 复用详情页右栏 AI 对话栏；第 36 轮第 5 项：由覆盖式抽屉改为 "
           "main 的同级侧栏（间隔 8px、可左右拉伸）")

# 组成 AI 对话栏所需的类名前缀（含只在全屏态 / 文件卡里用到的几条）
PREFIXES = (
    ".td-right", ".td-chat", ".td-msg-", ".td-ai-", ".td-composer", ".td-add-",
    ".td-skill", ".td-round-btn", ".td-sep", ".td-ico-",
    ".td-file", ".td-collapsed", ".td-root.is-collapsed", ".td-root.is-fullscreen",
)

s = io.open(SRC, encoding="utf-8").read()


# ============================== 工具 ==============================
def top_rules(css):
    """按「花括号配平」切出顶层规则文本列表（注释原样保留在规则前面）。"""
    out, buf, depth, i = [], [], 0, 0
    while i < len(css):
        if css.startswith("/*", i):
            j = css.find("*/", i + 2)
            if j < 0:
                buf.append(css[i:])
                break
            buf.append(css[i:j + 2])
            i = j + 2
            continue
        c = css[i]
        buf.append(c)
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                out.append("".join(buf).strip())
                buf = []
        i += 1
    if "".join(buf).strip():
        out.append("".join(buf).strip())
    return out


# ============================== 1. CSS ==============================
styles = re.findall(r"<style[^>]*>(.*?)</style>", s, re.S)
page_css = [x for x in styles if ".td-right" in x]
assert len(page_css) == 1, "页面 CSS 段定位异常：%d 个" % len(page_css)
page_css = page_css[0]

keep, seen = [], set()
for r in top_rules(page_css):
    if r.startswith("@media"):
        continue                       # 模块不依赖任何 @media
    head = r.split("{")[0]
    if any(p in head for p in PREFIXES):
        if r in seen:
            continue
        seen.add(r)
        keep.append(r)

# 剔除「两栏拖动 / 左右互换 / 左栏」专属规则 —— 抽屉没有拖动分栏，也没有左栏与信息列。
# ⚠️ 抽取时规则**前面的注释**也属于该条文本，故判断选择器前必须先剥注释。
DROP = ("is-dragging", "is-swapped", ".td-left", ".td-gutter")
_SEL = lambda r: re.sub(r"/\*.*?\*/", "", r.split("{")[0], flags=re.S)
dropped = [r for r in keep if any(d in _SEL(r) for d in DROP)]
keep = [r for r in keep if not any(d in _SEL(r) for d in DROP)]

# ★ 状态类改写：详情页的「两栏根容器 .td-root」在抽屉语境里就是抽屉本体。
#   改写后 `.td-root.is-fullscreen .td-chat-inner{max-width:860px}` 等规则被原样继承。
before_rewrite = sum(1 for r in keep if ".td-root." in _SEL(r))
keep = [r.replace(".td-root.", ".av-chat-drawer.") for r in keep]
module_css = "\n".join(keep)

# 自检：模块段只能是「规则」，不能夹带 token 定义（token 由上方 :root 统一给）
assert not re.search(r"^\s*--td-[a-z0-9-]+\s*:", module_css, re.M), \
    "模块 CSS 里出现了 --td-* 的定义（应只有使用）"
assert not re.search(r"\.td-root\b",
                     "\n".join(_SEL(r) for r in keep)), "仍有未改写的 .td-root 选择器"

# ============================== 2. HTML ==============================
opener = '"  <aside class=\\"td-right\\" aria-label=\\"AI 会话\\">",'
start = s.find(opener)
assert start > 0, "找不到 AI 会话 aside"
m_end = re.compile(r'</aside>",\n').search(s, start)
assert m_end, "找不到 aside 的收尾"
block = s[start:m_end.end() - 2]          # 去掉行尾的  ",

lines = []
for ln in block.split("\n"):
    t = ln.strip()
    if t.endswith(","):
        t = t[:-1]
    if t.startswith('"') and t.endswith('"'):
        lines.append(json.loads(t))       # 还原 \" → "
    else:
        lines.append(t)
assert lines[0].strip().startswith('<aside class="td-right"'), "模块 HTML 首行异常：%s" % lines[0][:60]
assert lines[-1].strip() == "</aside>", "模块 HTML 末行异常：%s" % lines[-1][:60]
inner_html = "\n".join(lines[1:-1])        # 去掉外层 <aside>（抽屉本体自己带）

# ============================== 3. JS ==============================
JS_A = "/* ================= 对话框三个弹层"
JS_B = "var gutter = wrap.querySelector('[data-td-gutter]')"
# ⚠️ JS_A 在页面 CSS 里也有一条同文案注释（占位说明），必须从 bindDetail 之后开始找
_anchor = s.find("function bindDetail(")
assert _anchor > 0, "找不到 bindDetail"
js_start = s.find(JS_A, _anchor)
assert js_start > 0, "找不到对话框三弹层绑定段"
js_end = s.find(JS_B, js_start)
assert js_end > js_start, "找不到绑定段结尾"
module_js = s[js_start:js_end].rstrip()
assert len(module_js) < 6000, "绑定段长度异常：%d" % len(module_js)

# ============================== 4. 组装 ==============================
TRIGGER_ICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round" class="lucide size-3.5" aria-hidden="true">'
    '<path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2z"/>'
    '<path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/></svg>'
)

CSS_TMPL = """<style id="av-chat-css">
  /* ============================================================
     AV-CHAT-DRAWER @@VER@@
     · 上半段 = 从 pages/task-detail.html 逐条抽取的右栏 AI 对话栏 CSS（禁手改，改源重跑脚本）
     · 下半段 = 视图适配层 `av-`（抽屉几何 / 遮罩 / 触发器落点）
     ============================================================ */

  /* ---------- 模块所需 token（与 task-detail.html 的 :root 同值） ---------- */
  :root {
    --td-bar: 48px;
    --td-gap: 8px;
    --td-right-w: 480px;          /* 抽屉默认宽 = 详情页右栏宽 */
    --td-collapsed-w: 48px;
    --td-fs-content: 860px;       /* 全屏态内容最大宽（与详情页一致） */
    --td-radius-card: 6px;
    --td-card: var(--color-fill-1);
    --td-line: var(--color-fill-2);
    --td-meta: var(--color-text-3);
    --td-strong: var(--color-text-1);
    --td-ink-2: #57626D;
    --td-bubble: #E5EDFE;
    --td-panel-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    --td-ico-gray: #6B6B6B;
    --td-ico-web: #327FCB;
    --td-ico-md: #167AB8;
    --td-ico-md-fold: #4196D6;
    --td-ico-skill: #7766FD;
    /* 视图适配层几何 */
    --av-chat-w: var(--td-right-w);
    --av-chat-gap: 8px;             /* 与 <main> 之间的间隔（.av-chat-gutter 的宽度） */
    --av-chat-ease: var(--transition-timing-function-standard);
  }

  /* ---------- 模块本体（source: pages/task-detail.html） ---------- */
@@CSS@@

  /* ============================ 视图适配层 av- ============================ */
  /* (1) ★ 第 36 轮第 5 项：由「覆盖在页面上的抽屉」改为「与 <main> 平级的侧栏」。
         · 挂载：脚本把本节点移进外壳的 flex 行 `div:has(> main)`，紧跟在 <main> 之后；
         · 宽度：行内 flex 分配 —— main 是外壳自带的 `flex:1`，本节点 `flex:none` + 宽度变量，
           打开时 main 被真正挤窄（不再遮住内容）；
         · 间隔 8px：由 `.av-chat-gutter`（同行的拉伸把手）承担，它就是 main 与侧栏之间的间隙；
         · 关闭：宽度 0 + 不占位（`display:none` 的把手），完全不影响排版。 */
  .av-chat-drawer {
    flex: none; width: 0; margin: 0; align-self: stretch;
    height: auto; min-height: 0; z-index: 1;
    overflow: hidden; opacity: 0; visibility: hidden;
    transition: width 240ms var(--av-chat-ease), opacity 180ms var(--av-chat-ease),
                visibility 0s linear 240ms;
  }
  /* 关闭态宽度动画期间内部保持设计宽，避免内容被横向压扁 */
  .av-chat-drawer > .td-right-inner { width: var(--av-chat-w); }
  .av-chat-drawer.is-xdrag { transition: none; }
  html[data-av-chat-open] .av-chat-drawer {
    width: var(--av-chat-w); opacity: 1; visibility: visible;
    transition: width 240ms var(--av-chat-ease), opacity 180ms var(--av-chat-ease), visibility 0s;
  }

  /* (2) 拉伸把手 = main 与侧栏之间的 8px 间隔本身（热区外扩，视觉仍是 8px 间隙） */
  .av-chat-gutter {
    flex: none; width: var(--av-chat-gap); align-self: stretch;
    position: relative; cursor: col-resize; touch-action: none;
  }
  html:not([data-av-chat-open]) .av-chat-gutter { display: none; }
  .av-chat-gutter::before {
    content: ""; position: absolute; left: 50%; top: 0; bottom: 0; width: 4px;
    transform: translateX(-50%); border-radius: 2px; background: transparent;
    transition: background-color 140ms var(--av-chat-ease);
  }
  .av-chat-gutter:hover::before, .av-chat-gutter.is-dragging::before { background: var(--color-fill-3); }

  /* (3) 全屏：侧栏吃满整行（main 让位），沿用模块里「内容 860px 居中」的规则 */
  .av-chat-drawer.is-fullscreen { flex: 1 1 auto; width: auto; }
  .av-chat-drawer.is-fullscreen > .td-right-inner { width: auto; }
  body:has(.av-chat-drawer.is-fullscreen) div:has(> main) > main { display: none; }
  body:has(.av-chat-drawer.is-fullscreen) .av-chat-gutter { display: none; }

  /* (4) 关闭态不参与命中测试 */
  html:not([data-av-chat-open]) .av-chat-drawer { pointer-events: none; }

  /* (5) ★ 第 36 轮第 4 项：侧栏里的链接同样 hover 转主题蓝（文件卡 `a.td-file` 的标题） */
  .av-chat-drawer .td-file:hover .td-file-tx,
  .av-chat-drawer .td-file:focus-visible .td-file-tx { color: var(--color-primary-6); }
</style>"""

HTML_TMPL = """<!-- ===== AV-CHAT-DRAWER @@VER@@ ===== -->
  <aside class="td-right av-chat-drawer" id="av-chat-drawer" aria-label="AI 会话" aria-hidden="true">
@@INNER@@
  </aside>"""

JS_TMPL = """<script id="av-chat-js">
(function () {
  var drawer = document.getElementById('av-chat-drawer');
  if (!drawer) return;
  var root = document.documentElement;
  var wrap = drawer;            /* 模块本体用 wrap 作用域，这里指向侧栏 */

  /* ==================================================================
     模块本体：对话框三个弹层（add / skill / select）
     构建期从 pages/task-detail.html 的 bindDetail() 原样抽出，禁手改。
     行为：点「添加」→ 上方弹出菜单；点「技能」→ 上方技能面板；
           点「标准模式 / 大模型」→ DS Select 弹层（唯一开关类 .giencoder-popup-open）；
           点外部 → 全关；Esc 由本脚本统一裁决（见下）。
     ================================================================== */
@@JS@@

  /* ==================== 开合（★ 第 36 轮第 5 项：侧栏，不是抽屉） ====================
     ⚠️ 属性必须分成两个，不能共用一个（第 34 轮踩坑）：
       · `html[data-av-chat-open]`  = **开合状态**，写在 <html> 上，供 CSS 驱动宽度动画；
       · `[data-av-chat-toggle]`    = **触发器**标记，只写在按钮上。
     若两者共用一个属性名，`e.target.closest('[data-av-chat-open]')` 会顺着祖先链
     命中 <html> 本身 —— 于是「侧栏打开时，栏内任何一次点击都会把它关掉」
     实测栈：closeChat ← toggleChat ← 点击「技能」按钮。 */
  function isOpen() { return root.hasAttribute('data-av-chat-open'); }
  function syncTriggers() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-av-chat-toggle]'), function (b) {
      b.setAttribute('aria-expanded', isOpen() ? 'true' : 'false');
    });
  }
  /* 关闭后焦点会随 visibility:hidden 落到 body，交还触发器更符合键盘习惯 */
  var lastTrigger = null;
  function openChat() {
    root.setAttribute('data-av-chat-open', '');
    drawer.setAttribute('aria-hidden', 'false');
    syncTriggers();
  }
  function closeChat() {
    closePops();                       /* 模块内：关掉可能开着的弹层 */
    root.removeAttribute('data-av-chat-open');
    drawer.setAttribute('aria-hidden', 'true');
    syncTriggers();
    if (lastTrigger && lastTrigger.isConnected) lastTrigger.focus();
  }
  function toggleChat() { isOpen() ? closeChat() : openChat(); }

  /* 触发器：事件委托，兼容脚本注入的按钮 */
  document.addEventListener('click', function (e) {
    var t = e.target && e.target.closest && e.target.closest('[data-av-chat-toggle]');
    if (!t) return;
    e.preventDefault();
    lastTrigger = t;
    toggleChat();
  }, true);

  /* ==================== 挂载：成为 <main> 的同级侧栏 ====================
     外壳的 flex 行 = `div:has(> main)`（`flex min-h-0 flex-1 pb-2 pl-3 pr-2`，内含左导航 + main）。
     React 不认识本节点，故每次 DOM 变化都检查一次：一旦被协调移除就重新插回。
     插入顺序：… <main> → [gutter 8px] → <aside>。 */
  var GAP = 8;                        /* 与 --av-chat-gap 同值 */
  /* MIN_W=480：侧栏可用宽 = MIN_W − 40（.td-composer 左右 20），必须 ≥ 输入区工具栏自然宽 380，
     否则工具栏溢出（实测 420 → 差 8px；360 → 差 68px）。
     MAIN_MIN=480：main 低于此宽后卡片只剩 ~90px，不可用。（1440 下范围 = 480 ~ 676） */
  var DEFAULT_W = 480, MIN_W = 480, MAIN_MIN = 480;
  var hostRow = null, hostMain = null, gutter = null;

  function place() {
    if (hostRow && hostRow.isConnected && drawer.parentElement === hostRow
        && gutter && gutter.nextElementSibling === drawer) return true;
    hostRow = document.querySelector('div:has(> main)');
    if (!hostRow) return false;
    hostMain = hostRow.querySelector(':scope > main') || hostRow.querySelector('main');
    if (!hostMain) return false;
    if (!gutter) {
      gutter = document.createElement('div');
      gutter.className = 'av-chat-gutter';
      gutter.setAttribute('data-av-chat-gutter', '1');
      gutter.setAttribute('role', 'separator');
      gutter.setAttribute('aria-orientation', 'vertical');
      gutter.setAttribute('aria-label', '调整 AI 对话栏宽度');
      bindGutter();
    }
    hostRow.insertBefore(gutter, hostMain.nextSibling);
    hostRow.insertBefore(drawer, gutter.nextSibling);
    clampNow();
    return true;
  }

  /* ==================== 宽度拉伸（只改侧栏宽度，main 由 flex:1 自动让位） ==================== */
  /* ⚠️ 可用宽 ≠ 行宽：同一行里还有外壳自带的**左导航栏**（本次实测 256px）。
     用 hostRow.clientWidth 会把它算进来 → 上限偏大 256px、main 被压到 204。
     故必须扣掉「除 main / gutter / 本侧栏之外」的其它 flex 子项。 */
  function availW() {
    if (!hostRow) return 0;
    var cs = getComputedStyle(hostRow);
    var w = hostRow.clientWidth - parseFloat(cs.paddingLeft || 0) - parseFloat(cs.paddingRight || 0);
    Array.prototype.forEach.call(hostRow.children, function (c) {
      if (c === hostMain || c === gutter || c === drawer) return;
      w -= c.getBoundingClientRect().width;
    });
    return w;
  }
  function curW() {
    var v = parseFloat(getComputedStyle(root).getPropertyValue('--av-chat-w'));
    return isNaN(v) ? DEFAULT_W : v;
  }
  /* 上限 = 可用宽 − 间隔 − main 最小宽；下限 MIN_W。宽度不够时下限优先。 */
  function clampW(w) {
    var max = Math.max(MIN_W, availW() - GAP - MAIN_MIN);
    return Math.max(MIN_W, Math.min(Math.round(w), max));
  }
  function setW(w) { root.style.setProperty('--av-chat-w', clampW(w) + 'px'); }
  /* 视口变化后重新钳位（沿用详情页第 35 轮第 1 项的做法：运行中改视口必须重夹） */
  var raf = 0;
  function clampNow() {
    var w = curW();
    var c = clampW(w);
    if (c !== w) root.style.setProperty('--av-chat-w', c + 'px');
  }
  window.addEventListener('resize', function () {
    if (raf) return;
    raf = requestAnimationFrame(function () { raf = 0; clampNow(); });
  });

  function bindGutter() {
    gutter.addEventListener('pointerdown', function (e) {
      if (e.button !== 0) return;
      e.preventDefault();
      var startX = e.clientX;
      var startW = Math.round(drawer.getBoundingClientRect().width) || DEFAULT_W;
      gutter.classList.add('is-dragging');
      drawer.classList.add('is-xdrag');
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
      function onMove(ev) { setW(startW - (ev.clientX - startX)); }
      function onUp() {
        window.removeEventListener('pointermove', onMove, true);
        window.removeEventListener('pointerup', onUp, true);
        window.removeEventListener('pointercancel', onUp, true);
        gutter.classList.remove('is-dragging');
        drawer.classList.remove('is-xdrag');
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
      }
      window.addEventListener('pointermove', onMove, true);
      window.addEventListener('pointerup', onUp, true);
      window.addEventListener('pointercancel', onUp, true);
    });
    /* 双击 = 复位默认宽 */
    gutter.addEventListener('dblclick', function () { setW(DEFAULT_W); });
  }

  if (!place()) {
    /* React 首帧可能晚于本脚本 */
    var mo0 = new MutationObserver(function () { if (place()) mo0.disconnect(); });
    mo0.observe(document.body, { childList: true, subtree: true });
  }
  /* 常驻观察：React 若把节点移除/移动，立刻插回（place() 命中即早退，开销可忽略） */
  var moKeep = new MutationObserver(function () { place(); });
  moKeep.observe(document.body, { childList: true, subtree: true });

  /* ==================== 全屏（复用模块顶栏的全屏按钮） ==================== */
  var fsBtn = drawer.querySelector('[data-td-fullscreen]');
  function setFs(on) {
    drawer.classList.toggle('is-fullscreen', !!on);
    if (fsBtn) {
      fsBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
      fsBtn.setAttribute('title', on ? '退出全屏' : '全屏');
      fsBtn.setAttribute('aria-label', on ? '退出全屏' : '全屏');
    }
  }
  if (fsBtn) fsBtn.addEventListener('click', function () {
    setFs(!drawer.classList.contains('is-fullscreen'));
  });
  /* 抽屉没有可拖动的分栏，故不提供「折叠」入口；此处只保证模块自带的
     折叠态按钮（.td-collapsed）若被程序置态后仍可恢复。 */
  var expBtn = drawer.querySelector('[data-td-expand]');
  if (expBtn) expBtn.addEventListener('click', function () {
    drawer.classList.remove('is-collapsed');
  });

  /* ==================== Esc 裁决（捕获阶段，先于外壳的全局快捷键） ====================
     顺序：① 模块弹层 → ② 全屏 → ③ 抽屉。每级只吃掉一层，避免一次 Esc 全关。 */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (opAdd || opSkill || opSel) { closePops(); e.preventDefault(); e.stopPropagation(); return; }
    if (drawer.classList.contains('is-fullscreen')) { setFs(false); e.preventDefault(); e.stopPropagation(); return; }
    if (isOpen()) { closeChat(); e.preventDefault(); e.stopPropagation(); }
  }, true);

  /* ==================== 触发器注入（内容标题行，全页唯一） ==================== */
  var ICON = '@@ICON@@' + '通过对话完善数字分身';
  function injectTrigger() {
    /* ★ 第 35 轮第 2 项：主内容还原后，触发器已直接写在主内容模板里
       （mg-work/r35/build-avatar-main.py 的 AV_MAIN 段），此处只要确认它已在页面上即可。 */
    if (document.querySelector('[data-av-chat-toggle]')) return true;
    var row = document.querySelector('div.flex.items-start.justify-between');
    if (!row) return false;
    if (row.querySelector('[data-av-chat-toggle]')) return true;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'giencoder-btn giencoder-btn-secondary giencoder-btn-size-default av-chat-trigger';
    btn.setAttribute('data-av-chat-toggle', '1');
    btn.setAttribute('aria-controls', 'av-chat-drawer');
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = ICON;
    var primary = row.querySelector('.giencoder-btn-primary');
    if (primary) row.insertBefore(btn, primary); else row.appendChild(btn);
    return true;
  }
  if (!injectTrigger()) {
    /* React 首帧可能晚于本脚本：等它挂载完再注入（注入成功即断开观察器） */
    var mo = new MutationObserver(function () {
      if (injectTrigger()) mo.disconnect();
    });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
</script>"""


def fill(tmpl, **kw):
    for k, v in kw.items():
        tmpl = tmpl.replace("@@%s@@" % k, v)
    return tmpl


css_block = fill(CSS_TMPL, VER=VERSION, CSS=module_css)
html_block = fill(HTML_TMPL, VER=VERSION, INNER=inner_html)
js_block = fill(JS_TMPL, JS=module_js, ICON=TRIGGER_ICON)

for nm, blk in (("CSS", css_block), ("HTML", html_block), ("JS", js_block)):
    assert "@@" not in blk, "%s 段仍有未替换占位符：%s" % (nm, re.findall(r"@@[A-Z]+@@", blk))

# 自检：注入段里 CSS 注释定界符必须成对且不嵌套（第 33 轮踩坑：CSS 注释不嵌套，
#       内层 */ 会提前闭合外层注释，把紧随其后的规则整块吞成声明块）
for pos in (m.start() for m in re.finditer(r"/\*", css_block)):
    seg = css_block[pos:]
    body = seg[2:seg.find("*/", 2)]
    assert "/*" not in body, "CSS 注释内嵌套了 /*（位置 %d）：%s" % (pos, body[:80])
assert css_block.count("/*") == css_block.count("*/"), \
    "CSS 注释定界符不成对：/*=%d */=%d" % (css_block.count("/*"), css_block.count("*/"))
assert js_block.count("/*") == js_block.count("*/"), \
    "JS 注释定界符不成对：/*=%d */=%d" % (js_block.count("/*"), js_block.count("*/"))

# ⚠️ 结束标记必须放在**最末**（script 之后）。曾误放在 </aside> 与 <script> 之间，
#    导致重复构建时只替换到标记为止、旧的 <script> 残留在页尾（出现两个 av-chat-js）。
INJECT = ("  " + START + " " + VERSION + " -->\n"
          + css_block + "\n"
          + html_block + "\n"
          + js_block + "\n"
          + "  " + END + "\n")
assert INJECT.count(START) == 1 and INJECT.count(END) == 1, "注入段标记数异常"
assert INJECT.rstrip().endswith(END), "注入段未以结束标记收尾"

# ============================== 5. 幂等写入 ==============================
dst = io.open(DEST, encoding="utf-8").read()
a = dst.find(START)
if a >= 0:
    b = dst.find(END, a)
    assert b > a, "有开启标记但找不到结束标记"
    b += len(END)
    # 消费区间要对齐到「行首缩进 + 结束标记后的换行」，否则每次复跑都多留一份空白（曾 +3 chars/次）
    while a > 0 and dst[a - 1] in " \t":
        a -= 1
    if dst[b:b + 1] == "\n":
        b += 1
    new = dst[:a] + INJECT + dst[b:]
    # 真·幂等自检：对结果再替换一次，必须逐字节不变（不能拿总长度比 —— 注入内容本身升级时长度会变）
    a2 = new.find(START)
    while a2 > 0 and new[a2 - 1] in " \t":
        a2 -= 1
    b2 = new.find(END, a2) + len(END)
    if new[b2:b2 + 1] == "\n":
        b2 += 1
    assert new[:a2] + INJECT + new[b2:] == new, "幂等自检失败：重复替换后内容发生变化"
    action = "REPLACED  %+d chars（幂等自检通过）" % (len(new) - len(dst))
else:
    idx = dst.rfind("</body>")
    assert idx > 0, "找不到 </body>"
    new = dst[:idx] + INJECT + dst[idx:]
    action = "PATCHED   %+d chars" % (len(new) - len(dst))

io.open(DEST, "w", encoding="utf-8", newline="").write(new)

print("源        : pages/task-detail.html")
print("目标      : pages/avatar.html")
print("动作      : %s" % action)
print("模块 CSS  : %d 条 / %d chars（%d 条做了 .td-root. → .av-chat-drawer. 状态改写；剔除 %d 条拖动/互换/左栏专属）"
      % (len(keep), len(module_css), before_rewrite, len(dropped)))
print("模块 HTML : %d chars" % len(inner_html))
print("模块 JS   : %d chars" % len(module_js))
print("注入段    : %d chars" % len(INJECT))
print("页面      : %d → %d chars" % (len(dst), len(new)))

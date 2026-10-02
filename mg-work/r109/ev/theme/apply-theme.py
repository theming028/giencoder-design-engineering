# -*- coding: utf-8 -*-
"""r109 第三拍 ③-a：**全站主题开关（浅色 / 深色 / 跟随系统）** —— 机制层。

★ 为什么这是「一层」而不是「逐页改色」：
  底座**早就在了**。`giencoder-design-system/colors_and_type.css` 里写着完整的暗色档
  —— `body[giencoder-theme='dark'], [giencoder-theme='dark'] { … }`：12 组色阶 × 10 级
  （蓝/红/绿/橙/黄/金/紫/品红/青/蓝/莱姆/灰）+ `--color-bg-{1..5}` / `--color-text-{1..4}`
  / `--color-fill-{1..4}` / `--color-border-{1..4}` / `--color-mask-bg` 等语义色，
  而且这段**已经内联进了全部 10 个页面**（实测：每页各有 1 处
  `body[giencoder-theme=dark],[giencoder-theme=dark]`）。
  ⇒ 「切主题」= **在 `<html>` 上挂/摘一个 `giencoder-theme="dark"` 属性**，
    不需要在页面里另造一套暗色变量、也不需要写 `@media (prefers-color-scheme: dark)`。
  本脚本只做三件事：① 注入 `color-scheme`（浏览器原生控件跟随）② 注入首帧应用脚本
  ③ 注入设置页「外观」三档的接线。**一个字节的色值都不碰。**

★ 属性挂 `<html>` 而不是 `<body>`，两条硬理由：
  · 实测全站 10 页的暗色规则**没有一条**用 `body[...]` 前缀（业务规则全是
    `[giencoder-theme='dark'] X` 形式，唯一那处 `body[…]` 在 token 块里且与裸选择器并列）
    ⇒ 挂 `<html>` 一律命中。若挂 `<body>`，`html` 上的 `:root` token 就得跟 body 的
    属性选择器比特异性，反而多一层风险。
  · React 只重渲染 `body` 内的子树，`<html>` 上的属性不会被它冲掉 —— 与 r87 的
    `--ui-fs`（同样写在 `<html>` 的内联 style 上）同一体位。
  ⚠ conversation.html 的 `<html>` 本来就挂着 `data-r93-page="conversation"`
    ⇒ 「把状态写在 html 属性上」是本工程的既有做法，不是新发明的花样。

★ 幂等：先按 `RE_THEME` 把旧块整段剥掉、再插 ⇒ 重跑逐字节不变。
  ⚠ 本块**不在** `mg-work/r109/apply109.py` 的 `RE_STYLE` / `RE_JS` 剥离名单里
    （那两条正则是**精确 id 列表**），所以它不会跟本代的会话详情注入链打架。
  ⚠ 但 `conversation.html` 是 `apply109.py` 从 **`base.html` 的净底**重建的
    ⇒ **必须给 `base.html` 也注入**，否则重跑 `apply109.py` 会把 conversation 的主题块冲掉。
    本脚本对全部 10 页一视同仁地注入，这一条自然满足。

★ 落点锚：紧跟 `<script id="r87-ui-js">` 之后 ——
  · 那个块是 10/10 页共享、且**逐字节一致**（md5 全同）的 `<head>` 内首帧脚本（管字号防闪），
    本块与它同一体位、同一目的（首帧前落地，不闪）；
  · 锚它而不是锚 `</head>`：`</head>` 在不同页里的前文不同，而 r87 块的结尾是唯一且稳定的。
  ⚠ 本脚本**不改 `r87-ui-js` 本体** —— r87 / r88 那两个补丁重跑时仍是幂等的。

用法： python mg-work/r109/ev/theme/apply-theme.py            # 全站注入（幂等）
      python mg-work/r109/ev/theme/apply-theme.py --check    # 只报会改什么，不落盘
      python mg-work/r109/ev/theme/apply-theme.py --revert   # 全站剥块（回滚）
"""
import argparse
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PAGES = os.path.join(REPO, 'pages')

CSS_ID = 'r109-theme-css'
JS_ID = 'r109-theme-js'

THEME_CSS = """<style id="r109-theme-css">
  /* ★ r109 第三拍 ③：**全站主题开关**（浅色 / 深色 / 跟随系统）的样式半边。
     底座是 DS 自己的暗色档 —— `colors_and_type.css` 早就写好了
     `body[giencoder-theme='dark'], [giencoder-theme='dark'] { … }`（12 组色阶 × 10 级
     + `bg/text/fill/border/mask` 语义色），并且**已内联进本页**。所以「切主题」= 在 `<html>`
     上挂/摘一个 `giencoder-theme="dark"` 属性 —— 页面里不需要另造一套暗色变量。
     本块只补一件 DS 没管的事：`color-scheme`。它管的是**浏览器原生部件**的明暗
     （滚动条、`<select>` 下拉、`<input type=checkbox>`、表单自动填充底色、默认焦点环）
     —— 不写的话，暗色页面里会横出一条刺眼的白色滚动条。
     ⚠ 不用 `@media (prefers-color-scheme: dark)`：档位由用户显式选定（可能是 light 配深色系统），
       媒体查询会把「用户选择了浅色但系统是深色」这一格判错。属性选择器永远跟着**用户的档**走。 */
  html[giencoder-theme='dark'] { color-scheme: dark; }
  html:not([giencoder-theme='dark']) { color-scheme: light; }
</style>
"""

THEME_JS = """<script id="r109-theme-js">
(function () {
  /* ★ r109 第三拍 ③：**首帧前把用户选定的主题档落到 `<html>` 上**，避免「先画浅色再跳暗色」。
     与 `r87-ui-js`（字号）同一体位、同一条链：本块紧跟它之后，仍在 `<head>` 内、仍早于首次绘制。
     档位存 `localStorage['gi-ui-theme']`，取值 `light` / `dark` / `auto`；
     **缺省 = `auto`（跟随系统）** —— 邵先生 2026-10-02 定的默认档。
     ⚠ 本块是 10 页共享的**机制层**：只管「读存储 → 定档 → 挂属性 → 跟随系统变化」，
       不做任何 UI。设置页那三枚按钮的接线也在这里（见文件末尾），
       因为它必须**先于**设置页自己的渲染脚本改 `aria-pressed`，否则会「显示浅色被选、实际跟随系统」。 */
  var KEY = 'gi-ui-theme';
  var root = document.documentElement;
  var MQ = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  var mode = 'auto';

  /* ★★ 适配护栏（防「半暗半亮」）：
     本拍暗色**适配层只覆盖基础工作台 5 页**（研发工作台 5 页下一轮）。
     机制层却是全局的 ⇒ 若不设护栏，未适配页会出现「DS token 翻暗、外壳仍是浅色」
     （外壳底是 React 写死的内联样式 + Tailwind 字面类，都不吃 token）
     ⇒ 近白文字压浅底 = 不可读，直接破坏稳定性。
     故：**页面上没有适配标记时一律按浅色渲染**（不挂属性、不翻 token）。
     ⚠ 标记取 `<html data-gi-dark="1">`（由 `apply-dark.py` 在**实际适配的页面**上挂、
       与 `#r109-dark-css` 同进同出）⇒ 两个脚本天然同步，不存在「改了机制忘了改护栏」。
     ⚠ 用 `<html>` 属性而**不是**去查 DOM 里的 `#r109-dark-css`：本脚本在 `<head>` 里
       **同步执行**，此刻它后面的那张样式表还没被解析出来，查不到（会误判成未适配，
       从而在已适配页上也永远不生效）。
     ⚠⚠ 本注释里**绝不能出现裸的 \"<\" + \"style\"**（或 \"<\" + \"script\"）字面 ——
       check-syntax.py 的 `STYLE_RE` 是纯文本正则，会把注释里的那个开标签当真，
       于是整块被它吞到下一个闭合标签，报「花括号/注释不配对」。 */
  var DARK_OK = root.getAttribute('data-gi-dark') === '1';

  function ok(m) { return m === 'light' || m === 'dark' || m === 'auto'; }
  function isDark(m) { return DARK_OK && (m === 'dark' || (m === 'auto' && !!MQ && MQ.matches)); }
  function paint() {
    if (isDark(mode)) root.setAttribute('giencoder-theme', 'dark');
    else root.removeAttribute('giencoder-theme');
    /* 档位本身也留个可读标记（探针 / 以后可能的顶栏快捷入口用；不参与任何样式）。 */
    root.setAttribute('data-gi-theme', mode);
  }
  function set(m) {
    if (!ok(m)) return;
    mode = m;
    try { localStorage.setItem(KEY, m); } catch (e) {}
    paint();
    syncSeg();
  }

  var v = null;
  try { v = localStorage.getItem(KEY); } catch (e) {}
  mode = ok(v) ? v : 'auto';
  paint();

  /* `auto` 档要跟着系统走 —— 监听媒体查询变化。
     ⚠ Safari < 14 只有已废弃的 `addListener`，两条都兜。 */
  if (MQ) {
    var onMQ = function () { if (mode === 'auto') paint(); };
    if (MQ.addEventListener) MQ.addEventListener('change', onMQ);
    else if (MQ.addListener) MQ.addListener(onMQ);
  }

  /* 机制出口：设置页的按钮与（探针 / 以后的顶栏入口）共用这一个口子。 */
  window.__giTheme = {
    get: function () { return mode; },
    set: set,
    isDark: function () { return isDark(mode); },
    /* ★ 本页是否已适配暗色（探针 / 设置页做「未适配则置灰」时用）。 */
    supported: function () { return DARK_OK; }
  };

  /* ---- 设置页「外观」三档接线 ----
     那三枚按钮（浅色 / 深色 / 跟随系统）由 r85/r87 拍的 `ctlSeg()` 生成，此前是**纯装饰**：
     点击只切 `aria-pressed` + toast，不写任何状态、也不改任何东西。
     这里在 **document 捕获阶段**接一手 —— 先于 `ctlSeg()` 自己那个冒泡 handler 跑
     ⇒ 我们负责「落盘 + 切主题」，它照旧负责「pressed 与 toast」，两边不抢。 */
  document.addEventListener('click', function (e) {
    var t = e.target;
    var b = t && t.closest ? t.closest('.r85-seg > .giencoder-btn') : null;
    if (!b || !b.parentElement) return;
    var kids = b.parentElement.children, k = 0, i;
    for (i = 0; i < kids.length; i++) { if (kids[i] === b) k = i; }
    set(['light', 'dark', 'auto'][k]);
  }, true);

  /* 初始 `aria-pressed` 回填：`ctlSeg()` 生成时**写死**「第 0 枚（浅色）= 真」，
     而默认档是 `auto` ⇒ 不回填的话，设置页会「显示浅色被选中、实际跟随系统」。
     ⚠ 面板是 React 晚挂的：脚本执行时 `.r85-seg` 还不存在 ⇒ 用一个**短命**的
       MutationObserver 等它出现，回填成功后立刻断开（最长 5s 兜底）。
     ⚠ 只在「没找到就重试」这条路上挂观察器：常规情况下 `syncSeg()` 一次就中，零开销。 */
  function syncSeg() {
    var seg = document.querySelector('.r85-seg');
    if (!seg || seg.children.length < 3) return false;
    var want = mode === 'light' ? 0 : (mode === 'dark' ? 1 : 2);
    for (var i = 0; i < seg.children.length; i++) {
      seg.children[i].setAttribute('aria-pressed', i === want ? 'true' : 'false');
    }
    return true;
  }
  if (!syncSeg()) {
    var mo = new MutationObserver(function () { if (syncSeg()) mo.disconnect(); });
    mo.observe(root, { childList: true, subtree: true });
    setTimeout(function () { mo.disconnect(); syncSeg(); }, 5000);
  }
})();
</script>
"""

THEME_BLOCK = THEME_CSS + THEME_JS

RE_R87JS = re.compile(r'<script id="r87-ui-js">.*?</script>\n', re.S)
RE_THEME = re.compile(
    r'<style id="%s">.*?</style>\n?<script id="%s">.*?</script>\n?' % (CSS_ID, JS_ID), re.S)


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def strip(t):
    return RE_THEME.sub('', t)


def patch(t):
    t = strip(t)                       # 先剥旧块 ⇒ 幂等
    m = RE_R87JS.search(t)
    if not m:
        return t, False
    return t[:m.end()] + THEME_BLOCK + t[m.end():], True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='只报会改什么，不落盘')
    ap.add_argument('--revert', action='store_true', help='把主题块整段剥掉')
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(PAGES, '*.html')))
    if not files:
        sys.exit('!! %s 下没有 html' % PAGES)

    print('=== r109 全站主题块：%s ===' % ('回滚' if a.revert else ('检查' if a.check else '注入')))
    n_ok = n_skip = n_bad = 0
    changed = []
    for p in files:
        name = os.path.basename(p)
        t, nl = rd(p)
        before = len(t)
        has = bool(RE_THEME.search(t))
        has_anchor = bool(RE_R87JS.search(t))

        if a.revert:
            if not has:
                n_skip += 1
                continue
            t2 = strip(t)
            verb = '剥除'
        else:
            if not has_anchor:
                print('   !! %-20s 找不到锚点 `<script id="r87-ui-js">` —— 跳过' % name)
                n_bad += 1
                continue
            t2, ok = patch(t)
            if not ok:
                n_bad += 1
                continue
            if t2 == t:
                n_skip += 1
                print('   =   %-20s 已是目标态' % name)
                continue
            verb = '注入'

        if not a.check:
            io.open(p, 'wb').write(t2.replace('\n', nl).encode('utf-8'))
        n_ok += 1
        changed.append(name)
        print('   %s %-20s %7d → %7d（%+d 字符）%s'
              % ('*' if a.check else '√', name, before, len(t2), len(t2) - before,
                 '（已有旧块，先剥后插）' if has and not a.revert else ''))

    print()
    print('   变更 %d 页 / 已是目标态 %d 页 / 失败 %d 页' % (n_ok, n_skip, n_bad))
    if changed:
        print('   变更清单：%s' % ', '.join(changed))
    if n_bad:
        sys.exit('!! 有页面找不到注入锚点')


if __name__ == '__main__':
    main()

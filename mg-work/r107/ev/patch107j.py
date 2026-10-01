# -*- coding: utf-8 -*-
"""r107 第九拍（2026-10-01 13:1x 邵先生两条）—— **就地返工，不另起代数**。

体位：改序 part107/* → （不需 splice107 / make107）→ apply107.py。
      ⚠ apply107.py 运行时 `_read_part()` 读 browse.css / browse.html / browse.js /
        ctrl-conv.js / panel.css / panel.js；本轮只动 **panel.js**（就地改）与
        **新建 part107/ctrl-conv.js**（覆盖件），`_mods.html` / `browse.html` 一字未动
        ⇒ 不必重跑 splice107/make107。

两条 → 改动落点：
  ① 全屏后按钮图标不翻（还是「最大化」那套四角框）
       → panel.js：抽出 `setMax(on, silent)` + 新增 `setMaxIcon(on)`，切内联 SVG 的 `d`
         （MAX = 从 DOM 读出来缓存的原始四角朝外字形；MIN = 四角朝内折角）。
  ② 全屏后拖分栏条「一按就复位」
       → 两个因，两处修：
         (a) `ctrl-conv.js` 的 `bindSplit` 里 `startPanel = panelW` 取的是**内部缓存**，
             而 panel.js 的「最大化」是**绕过控制器直接写 `--av-browse-w`** ⇒ 缓存停在 641，
             全屏 1040 时一按下拖动就按 641±dx 算 ⇒ 宽度猛跳（实测 -120 ⇒ 761）。
             改为**读实际渲染宽**（先落 `.is-col-dragging` 停过渡，再取几何=终值），并把
             缓存同步回来。
         (b) 同处 `pointermove` / `pointerup` 挂的是**元素**（只靠 setPointerCapture 兜）⇒
             指针离开分栏条/捕获失效时拖动**中途断掉**。改挂 **window**（站内其它拖拽同口径）
             + `blur` 兜底。
       → 另：panel.js 里「全屏态下按下分栏条 = 放弃全屏」（`setMax(false, true)`，**不动宽度**，
         宽度交给控制器从实际宽起算）；侧栏收起时也退出全屏 —— 搭在既有的 resize handler 上
         （ctrl-conv 的 `setOpen(false)` 必定 dispatch 一次 resize），**不观察 DOM**：
         那条 flex 行与分栏条都是 ctrl-conv 后插的，本文件跑得更早、初次观察会挂错元素（本拍踩过）。

为什么 part107 里放一份 ctrl-conv.js 副本而不是直接改 part105：
  `part105/*` 是**跨代资产**（源页 avatar.html 的移植源，历代刻意不回头动它 —— 见 apply107.py
  第 128 行同款约定）。`_read_part()` 按 `PART_DIRS = (part107, part105)` **顺序**取件 ⇒
  把覆盖版放在 part107 即可，part105 与 avatar.html 零影响。
  ⚠ 代价是「副本会漂移」（part105 日后改动不会自动跟），已在副本头部写明。

幂等：① 每处 `edit()` 先查新串特征子串；② 覆盖件存在且含标记就跳过，存在但不含标记则**报错退出**
      （防误覆盖人工改过的文件）。
"""
import io, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(os.path.dirname(HERE), 'part107')
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
JS = os.path.join(PART, 'panel.js')
CV_DST = os.path.join(PART, 'ctrl-conv.js')
CV_SRC = os.path.join(REPO, 'mg-work', 'r102', 'part105', 'ctrl-conv.js')
BAK = os.path.join(HERE, 'bak9')

MARK_CV = 'r107 第九拍 ②'

APPLIED = []
SKIPPED = []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace('\n', nl).encode('utf-8'))


def edit(p, old, new, label, mark):
    t, nl = rd(p)
    if mark in t:
        SKIPPED.append(label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1）' % (label, n))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)


# ============================================================ 备份（只做一次）
if not os.path.isdir(BAK):
    os.makedirs(BAK)
for src, name in ((JS, 'panel.js.bak'), (CV_SRC, 'ctrl-conv.part105.bak')):
    dst = os.path.join(BAK, name)
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)

# ============================================================ A. 覆盖件：part107/ctrl-conv.js
CV_HEAD = u"""/* ================================================================================
   ★ r107 第九拍（2026-10-01 13:1x）：本文件 = `mg-work/r102/part105/ctrl-conv.js` 的**逐字副本**
     + `bindSplit()` 里的一处修正（搜索 `r107 第九拍 ②` 可见两段注释与改动点）。

     为什么复制而不直接改 part105：`part105/*` 是**跨代资产**（源页 avatar.html 的移植源，
     历代刻意不回头动它 —— 见 apply107.py 第 128 行的同款约定）。apply107.py 的 `_read_part()`
     按 `PART_DIRS = (part107, part105)` **顺序**取件 ⇒ 覆盖版放在 part107 即可，
     part105 原文与 avatar.html 零影响。
     ⚠ 漂移提醒：part105 那份日后若有改动，本副本**不会自动跟**，需人工同步。
   ================================================================================ */
"""

CV_OLD = u"""      startX = e.clientX; startPanel = panelW; startTree = treeW;
      el.classList.add('is-dragging');
      hostRow.classList.add('is-col-dragging');
      if (el.setPointerCapture) { try { el.setPointerCapture(e.pointerId); } catch (err) {} }
      e.preventDefault();
    });
    el.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      if (kind === 'panel') setPanelW(startPanel - (e.clientX - startX), false);
      else setTree(startTree + (e.clientX - startX), false);
    });
    function end() {
      if (!dragging) return;
      dragging = false;
      el.classList.remove('is-dragging');
      hostRow.classList.remove('is-col-dragging');
      writeStore(kind === 'panel' ? { panelW: wantPanel } : { treeW: wantTree });
    }
    el.addEventListener('pointerup', end);
    el.addEventListener('pointercancel', end);
"""

CV_NEW = u"""      startX = e.clientX;
      el.classList.add('is-dragging');
      hostRow.classList.add('is-col-dragging');
      /* ★ r107 第九拍 ②(a)：起点取**实际渲染宽**，不取内部缓存 `panelW`。
         `panelW` 只在「恢复记忆 / 拖动 / 双击复位 / 键盘」时更新；宿主若**绕过本控制器**
         直接写 `--av-browse-w`（r107 面板的「最大化」就是这么干的，见 part107/panel.js），
         缓存就与实况脱节 ⇒ 全屏 1040 时一按下拖动，宽度按 641±dx 算、猛跳到 761
         （报障现象：「一按就复位」）。这里先落 `.is-col-dragging`（= `transition:none`）
         再取几何，拿到的就是**终值**而不是过渡中间值。 */
      var declared = parseFloat(slot.style.getPropertyValue('--av-browse-w'));
      startPanel = Math.round(slot.getBoundingClientRect().width) || declared || panelW;
      panelW = startPanel;                          /* 把缓存同步回实况 */
      startTree = treeW;
      if (el.setPointerCapture) { try { el.setPointerCapture(e.pointerId); } catch (err) {} }
      e.preventDefault();
    });
    /* ★ r107 第九拍 ②(b)：`pointermove` / `pointerup` 一律挂 **window**（站内其它拖拽同口径，
       见 panel.js 的标签重排）。原来挂 `el`、只靠 `setPointerCapture` 兜底 —— 全屏后分栏条
       紧贴窗口左缘，往左拖时指针很快离开元素；一旦捕获没生效（元素被 React 重挂 / pointerId
       失配），拖动就**中途断掉**，现象同「拖不动 / 一放就弹回」。`blur` 兜底防「切走窗口后
       一直卡在 dragging」。三个监听一次性绑好，由 `dragging` 守门 ⇒ 重复调用无副作用。 */
    function onMove(e) {
      if (!dragging) return;
      if (kind === 'panel') setPanelW(startPanel - (e.clientX - startX), false);
      else setTree(startTree + (e.clientX - startX), false);
    }
    function end() {
      if (!dragging) return;
      dragging = false;
      el.classList.remove('is-dragging');
      hostRow.classList.remove('is-col-dragging');
      writeStore(kind === 'panel' ? { panelW: wantPanel } : { treeW: wantTree });
    }
    window.addEventListener('pointermove', onMove, true);
    window.addEventListener('pointerup', end, true);
    window.addEventListener('pointercancel', end, true);
    window.addEventListener('blur', end, true);
"""

if os.path.exists(CV_DST):
    _t, _ = rd(CV_DST)
    if MARK_CV in _t:
        SKIPPED.append(u'part107/ctrl-conv.js（覆盖件已存在）')
    else:
        sys.exit(u'!! part107/ctrl-conv.js 已存在但不含本拍标记 —— 先人工核对再动')
else:
    src_t, nl = rd(CV_SRC)
    if src_t.count(CV_OLD) != 1:
        sys.exit(u'!! ctrl-conv.js 锚点命中 %d 次（应 1）' % src_t.count(CV_OLD))
    wr(CV_DST, CV_HEAD + src_t.replace(CV_OLD, CV_NEW, 1), nl)
    APPLIED.append(u'part107/ctrl-conv.js（新建覆盖件 1 处修正）')

# ============================================================ B. panel.js：setMax + 图标 + 拖拽/收起联动
JS_OLD = u"""  var maxBtn = bar.querySelector('[data-td-max]');
  if (maxBtn) {
    maxBtn.addEventListener('click', function () {
      var on = maxBtn.getAttribute('aria-pressed') !== 'true';
      if (on) {
        applyMaxW();
        maxBtn.setAttribute('aria-pressed', 'true');
        maxBtn.setAttribute('title', '还原侧栏宽度');
        maxBtn.setAttribute('aria-label', '还原侧栏宽度');
      } else {
        slot.removeAttribute('data-td-maxw');
        slot.style.setProperty('--av-browse-w', storedPanelW() + 'px');
        maxBtn.setAttribute('aria-pressed', 'false');
        maxBtn.setAttribute('title', '最大化侧栏');
        maxBtn.setAttribute('aria-label', '最大化侧栏');
      }
    });
  }
"""

JS_NEW = u"""  /* ★ 第九拍 ①：按钮上的**字形**也得跟着翻。原实现只翻 aria-pressed / 文案，内联 SVG 的 `d`
     一直是最初那套「四角朝外」⇒ 全屏后按钮看着根本没变（邵先生报的①）。
     两套字形同口径（24 viewBox / stroke-width 2 / 四角折角）：
       MAX = 四角朝外的框角 —— 就是 HTML 里写死那套，运行时**从 DOM 读出来缓存**（不另抄一份免得漂移）；
       MIN = 四角朝内的折角（Lucide `minimize` 的四条，与本页其余图标同源）。
     ⚠ 只改 `d` 属性、不重建节点 ⇒ 不碰 React，按钮的 hover / focus / 键盘可达性一字不变。 */
  var ICON_MIN = ['M8 3v3a2 2 0 0 1-2 2H3', 'M21 8h-3a2 2 0 0 1-2-2V3',
                  'M3 16h3a2 2 0 0 1 2 2v3', 'M16 21v-3a2 2 0 0 1 2-2h3'];
  var maxBtn = bar.querySelector('[data-td-max]');
  var maxPaths = maxBtn ? [].slice.call(maxBtn.querySelectorAll('svg path')) : [];
  var ICON_MAX = maxPaths.map(function (p) { return p.getAttribute('d'); });
  function setMaxIcon(on) {
    var d = on ? ICON_MIN : ICON_MAX;
    for (var i = 0; i < maxPaths.length && i < d.length; i++) maxPaths[i].setAttribute('d', d[i]);
  }
  /* on=true → 最大化；on=false → 还原。
     silent=true：**只退状态、一个像素都不动宽**（拖拽接管时用，见下），否则把宽度写回记忆值。 */
  function setMax(on, silent) {
    if (!maxBtn) return;
    if (on) {
      applyMaxW();
      maxBtn.setAttribute('aria-pressed', 'true');
      maxBtn.setAttribute('title', '还原侧栏宽度');
      maxBtn.setAttribute('aria-label', '还原侧栏宽度');
    } else {
      slot.removeAttribute('data-td-maxw');
      if (!silent) slot.style.setProperty('--av-browse-w', storedPanelW() + 'px');
      maxBtn.setAttribute('aria-pressed', 'false');
      maxBtn.setAttribute('title', '最大化侧栏');
      maxBtn.setAttribute('aria-label', '最大化侧栏');
    }
    setMaxIcon(on);
  }
  if (maxBtn) {
    maxBtn.addEventListener('click', function () {
      setMax(maxBtn.getAttribute('aria-pressed') !== 'true');
    });
  }
  /* ★ 第九拍 ②：**全屏态下按下分栏条 = 放弃全屏**（语义：接下来手动调宽）。
     ⚠ 只清标记 / 还原字形，**不动宽** —— 宽度交给 ctrl-conv 从**实际宽**起算；这里若先把宽度
       写回 641，就变成「一按先跳回默认宽」（正是邵先生看到的「一下就复位」）。
     ⚠ 用**文档级捕获委托**：分栏条由 ctrl-conv 在 place() 时才插进 flex 行，本文件跑得更早，
       那时它可能还不在 DOM 里（同款先例：页头那枚「打开侧栏」也是委托绑的）。 */
  document.addEventListener('pointerdown', function (e) {
    if (!e.target || !e.target.closest || !e.target.closest('#av-browse-split')) return;
    if (slot.hasAttribute('data-td-maxw')) setMax(false, true);
  }, true);
"""

edit(JS, JS_OLD, JS_NEW, u'panel.js · setMax + 字形切换 + 拖拽/收起联动', 'setMaxIcon')

# ---- ② （续）侧栏收起时退出全屏：搭在既有的 resize handler 上 ----
JS_RS_OLD = u"""  /* ctrl-conv 的 resize 处理走单层 rAF ⇒ 本处退两层 rAF，保证「最大化态」在它之后落定 */
  window.addEventListener('resize', function () {
    if (!slot.hasAttribute('data-td-maxw')) return;
    requestAnimationFrame(function () { requestAnimationFrame(applyMaxW); });
  });
"""

JS_RS_NEW = u"""  /* ctrl-conv 的 resize 处理走单层 rAF ⇒ 本处退两层 rAF，保证「最大化态」在它之后落定。
     ★ 第九拍 ②（续）：同一个 handler 里顺手清掉「收起后残留的全屏态」。三个收起入口
       （页头开关 / 侧栏 × / Esc）最终都走 ctrl-conv 的 `setOpen(false)`，而它**必定**
       dispatch 一次 resize ⇒ 在这儿判一下就够了（此时 `.av-browse-on` 已被摘掉）。
       不清的话会留下「宽度是记忆值、按钮却仍是"还原"字形」的错位，且下次 resize 会把右栏
       突然弹回全屏宽。⚠ 用 silent：收起态下写 `--av-browse-w` 没有意义，下次打开时
       ctrl-conv 的 `setOpen(true)` 会按记忆值重设。
       ⚠ 别改成「观察 hostRow 的 class」：那条 flex 行与分栏条都是 ctrl-conv 在 place() 里
         **后插**的，本文件跑得更早 ⇒ 初次观察很可能挂在旧父级上、永不触发（本拍踩过）。 */
  window.addEventListener('resize', function () {
    var row = slot.parentElement;
    if (row && !row.classList.contains('av-browse-on') && slot.hasAttribute('data-td-maxw')) {
      setMax(false, true);
      return;
    }
    if (!slot.hasAttribute('data-td-maxw')) return;
    requestAnimationFrame(function () { requestAnimationFrame(applyMaxW); });
  });
"""

edit(JS, JS_RS_OLD, JS_RS_NEW, u'panel.js · 收起侧栏退出全屏（搭 resize）', 'silent：收起态下写')

# ============================================================ 汇报
print(u'应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
for x in APPLIED:
    print(u'  ✔ ' + x)
for x in SKIPPED:
    print(u'  · 跳过 ' + x)

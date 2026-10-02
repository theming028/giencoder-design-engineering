# -*- coding: utf-8 -*-
"""r109 第三拍（第三层补丁）—— 邵先生 2026-10-02 10:2x 三条：

  ① **批注原点对齐 + 编辑态文案**（邵先生：「添加批注的点击触发点与输入批注的容器 "td-elnote"
     没有在一个原点，位置漂移太远，需要做到**在哪里点击就在哪里添加**，包括预览批注的也是一样，
     另外编辑态时原来的"添加"文案需变为"保存"」）。落点 = `part109/panel.js`。
     · 现状三个原点各在一处：锚点按「被标注元素的**右上角** −12」落（r93 起的读法）、
       气泡 `left` 是 CSS 里写死的 `12px`、而用户点的是**元素上任意一处** ⇒ 点长段落左端时，
       锚点跑到段落右端、气泡钉在视图左边，三者互不相干。
     · 本拍把「**本次点击点**」定成唯一原点（`noteAt`，`.td-view` 的**内容坐标**）：
         锚点 24×24 的**中心**咬住它；气泡**左边缘**对齐它。
     · 「预览批注的也是一样」：点锚点看详情时，原点 = **锚点自己**（`anchorOpen` 里写 `noteAt`）。
     · 编辑态（`noteCur` 查得到记录）⇒ 按钮文案恒为「保存」，`noteCtrl()` 里统一收口
       —— 免得「编辑态下按一下 Ctrl 就翻回『添加』」。
  ② **对话卡片两端对齐**（邵先生：「对话内容中的类似 "r93-card r93-card--edge" 这样的容器前面的
     缩进都取消，两端都对齐吧」）。⚠ 落点**不在 `part109/*`** —— `.r93-card` 的 CSS 长在
     `apply109.py` 的内联样式里，而 `apply109.py` 是 `ev/make109.py` 从 `apply108.py`
     **逐字生成**的 ⇒ 与第二拍 ③（图标）同路：改 `ev/make109.py` 的 EDITS 表，本层新增 **E9**。
  ③ **全站暗色模式** —— **不在本补丁内**。它是全站 10 页的机制层（独立脚本
     `ev/theme/apply-theme.py`：`r109-theme-css` + `r109-theme-js`），与本代「会话详情页」
     的注入链（`part109/*` → `splice109` → `make109` → `apply109`）是两条**正交**的线；
     且它注入的是**产物**、不走 `make109` 的 EDITS 表，放这里只会把两条链缠在一起。

★ 体位与硬规则（与 patch109l1/l2.py 同）：
  · r108 已交付并封板（`172e580`）⇒ 本拍属**新代数 r109**、未交付期 ⇒ 返工**就地改**本层补丁。
  · 硬规则 22「双层产物只能下→上改」⇒ 本层改序：
      1. `part109/panel.js`  ← 本补丁 ①
      2. `ev/make109.py`     ← 本补丁 ②（E9）+ ③-d（E10）
      3. `ev/splice109.py`   → 重建 `part109/browse.html`
      4. `ev/make109.py`     → 重生成 `apply109.py`（含 ① 的注入 + ② 的 E9 + ③-d 的 E10）
      5. `apply109.py`       → 落 `pages/base.html` + `pages/conversation.html`
      6. `ev/theme/apply-theme.py` → 全站 10 页注入主题块
      7. `ev/theme/apply-dark.py`  → 基础工作台 5 页注入适配层（+ 越界清扫）
    ★ ⑥⑦ **必须最后跑**：apply109 会从 `base.html` 的净底**重建** `conversation.html`
      （主题块落在 `base.html` 上就会跟着过去；适配块也会跟着过去，由 ⑦ 的越界清扫摘掉）。
      ⚠ 反过来「先 ⑥⑦ 后 ⑤」会让 ⑤ 拿着**带适配块的** base 去重建 conversation
      ⇒ E10 已保证 conversation 拿不到护栏标记（`data-gi-dark`），观感安全。
  · 「各层 mark 是后一层必须替前一层保住」—— 本层只插 `r109-l3` 标记，`r107-l1` … `r109-l2`
    的标记一个不碰（收尾有跨层兜底断言）。
  · ⚠ **本层动了 `noteDrop()` 的形参**（`(el, n)` → `(el, n, at)`）⇒ `patch109l2.py` 里那条
    `j_bare.split('function noteDrop(el, n) {')` 的判据会失配（命中 0 次 ⇒ 上一层复跑整块报错）。
    按「后一层必须替前一层保住」，那条判据在本层**同步放宽**成 `'function noteDrop(el'`
    （两种签名都命中），改动记录在 `acceptance.md`。

用法： python mg-work/r109/ev/patch109l3.py           # 应用（幂等）
      python mg-work/r109/ev/patch109l3.py --check   # 只验锚点，不落盘
      python mg-work/r109/ev/patch109l3.py --bak     # 落盘前把两个源件备份到 ev/bak-l3/
"""
import ast
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P109 = os.path.join(REPO, 'mg-work', 'r109', 'part109')
PCS = os.path.join(P109, 'panel.css')
PJS = os.path.join(P109, 'panel.js')
MODS = os.path.join(P109, '_mods.html')
BAK = os.path.join(HERE, 'bak-l3')
MAKE = os.path.join(HERE, 'make109.py')
L2 = os.path.join(HERE, 'patch109l2.py')

APPLIED = []
SKIPPED = []
STRICT = True
CHECK = False      # --check：只验锚点，不落盘


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    if CHECK:
        return
    io.open(p, 'wb').write(t.replace('\n', nl).encode('utf-8'))


def edit(p, old, new, label, mark, strict=None):
    t, nl = rd(p)
    strict = STRICT if strict is None else strict
    if mark and mark in t:
        if strict and old in t:
            sys.exit('!! %s：mark 歧义 —— `old` 与 `mark` 同时存在 ⇒ mark 不是「改完才出现」的串\n'
                     '   mark=%r\n   old=%r' % (label, mark, old[:200]))
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1 次）\n   old=%r' % (label, n, old[:240]))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)
    print('   %s  %s（%d → %d 字符）'
          % ('校验' if CHECK else '应用', label, len(t), len(t) - len(old) + len(new)))


# ================================================================================
# ① 批注原点对齐（panel.js）—— 1/7：新增 `noteAt`
# ================================================================================
JS_AT_OLD = """    var noteCur = null;       /* 气泡此刻挂在哪个 `[data-td-el]` 上 */
    var noteCtrlOn = false;
"""

JS_AT_NEW = """    var noteCur = null;       /* 气泡此刻挂在哪个 `[data-td-el]` 上 */
    var noteCtrlOn = false;
    /* ★ r109-l3 ①：**本次批注的唯一原点**。
       邵先生：「添加批注的点击触发点与输入批注的容器 `td-elnote` 没有在一个原点，位置漂移
       太远，需要做到**在哪里点击就在哪里添加**，包括预览批注的也是一样」。
       口径 = `.td-view` 的**内容坐标**（`clientX/Y − view.getBoundingClientRect() + scroll`），
       与锚点内联 `left/top`、与气泡内联 `left/top` **同一套坐标系** ⇒ 三者可以直接加减。
       两个写入点：
         · 点元素发起批注（`.td-view` 的 click 监听）⇒ 写**点击点**；
         · 点已有锚点看详情（`anchorOpen`）      ⇒ 写**锚点自己的位置**（「预览批注的也是一样」）。
       读出点：`noteEdit()`（气泡左边缘）与 `noteDrop()`（锚点中心）。
       ⚠ 缺省 `null` ⇒ 两条老路径都退回 r93 起的读法（被标注元素右上角），只在非点选路径下发生。 */
    var noteAt = null;
"""

# ================================================================================
# ① 批注原点对齐（panel.js）—— 2/7：`noteCtrl()` 的文案收口
# ================================================================================
JS_CTRL_OLD = """    function noteCtrl(on) {
      noteCtrlOn = on;
      noteCard.classList.toggle('is-ctrl', on);
      if (noteOk) noteOk.textContent = on ? '发送' : '添加';
    }
"""

JS_CTRL_NEW = """    function noteCtrl(on) {
      noteCtrlOn = on;
      noteCard.classList.toggle('is-ctrl', on);
      /* ★ r109-l3 ①（邵先生：「编辑态时原来的"添加"文案需变为"保存"」）：
         已经是**编辑一条既有批注**（`noteCur` 查得到记录）⇒ 按钮恒为「保存」，
         与 Ctrl 无关 —— Ctrl 那档是「把一条**新**意见发送进对话」的语义，不是「改一条老意见」。
         ★ 文案统一在这**一个函数**里收口：`noteEdit()` 与文档级的 Ctrl keydown / keyup
           都只调它 ⇒ 不存在「编辑态下按一下 Ctrl 就翻回『添加』」的漏洞。
         ⚠ 调用顺序依赖：`noteEdit()` 里是「先 `noteCur = el`、后 `noteCtrl(...)`」，
           所以这里查 `noteCur` 已经是最新的那条。 */
      if (noteOk) {
        noteOk.textContent = (noteCur && noteFind(noteCur)) ? '保存' : (on ? '发送' : '添加');
      }
    }
"""

# ================================================================================
# ① 批注原点对齐（panel.js）—— 3/7：点选监听记下点击点
# ================================================================================
JS_PICK_OLD = """    if (view) {
      view.addEventListener('click', function (e) {
        if (!brw.classList.contains('is-annotating')) return;
        var el = e.target && e.target.closest ? e.target.closest('[data-td-el]') : null;
        if (!el) return;
        noteEdit(el);
      });
    }
"""

JS_PICK_NEW = """    if (view) {
      view.addEventListener('click', function (e) {
        if (!brw.classList.contains('is-annotating')) return;
        var el = e.target && e.target.closest ? e.target.closest('[data-td-el]') : null;
        if (!el) return;
        /* ★ r109-l3 ①：**记下点击点**（转成 `.td-view` 的内容坐标）—— 它就是本条批注的原点。
           ⚠ `e.clientX/Y` 是**视口坐标**，锚点与气泡用的是**内容坐标** ⇒ 必须 `− viewRect + scroll`。
           ⚠ 键盘 Enter 触发的合成 `click` 两个坐标都是 0 ⇒ 认作「没有点击点」，退回旧读法
             （否则锚点会被扔到 `.td-view` 的左上角）。 */
        if (e.clientX || e.clientY) {
          var vr0 = view.getBoundingClientRect();
          noteAt = { x: e.clientX - vr0.left + view.scrollLeft,
                     y: e.clientY - vr0.top + view.scrollTop };
        } else {
          noteAt = null;
        }
        noteEdit(el);
      });
    }
"""

# ================================================================================
# ① 批注原点对齐（panel.js）—— 4/7：气泡水平也跟原点走
# ================================================================================
JS_BLEFT_OLD = """      elnote.style.top = Math.round(top) + 'px';
    }
"""

JS_BLEFT_NEW = """      elnote.style.top = Math.round(top) + 'px';
      /* ★ r109-l3 ①：**水平也跟同一原点走**（邵先生：「没有在一个原点，位置漂移太远」）。
         原状：`.td-elnote` 的 `left` 是 CSS 里写死的 `12px`（`left: 12px;`）⇒ 不论锚点在哪、
         点的是哪儿，气泡**永远贴着 `.td-view` 的左边**，与原点能差出几百 px。
         本拍：气泡**左边缘**对齐原点 `noteAt.x`（缺省则退回参照物 `ref` 的左边缘），
         再夹进 `.td-view` 的可视带 —— 与上面 `top` 的夹取同一口径、同一坐标系。
         ⚠ 只加一条内联 `left`（内联优先于 CSS 的 `12px`），CSS 那条保留为**未定位时的初值**；
           气泡的宽度 / radius / 内距 / 三稿几何一字未动。
         ⚠ 宽度在**摘掉 `[hidden]` 之后**量（同 `top` 那条的教训：隐藏态 `offsetWidth` 恒为 0）。 */
      var vLeft = view.scrollLeft, vRight = view.scrollLeft + view.clientWidth;
      var left = noteAt ? noteAt.x : (er.left - vr.left + view.scrollLeft);
      var w = elnote.offsetWidth;
      if (w && view.clientWidth && left + w > vRight) left = vRight - w;
      if (left < vLeft) left = vLeft;
      elnote.style.left = Math.round(left) + 'px';
    }
"""

# ================================================================================
# ① 批注原点对齐（panel.js）—— 5/7：预览走「锚点即原点」
# ================================================================================
JS_AOPEN_OLD = """    function anchorOpen(a) {
      var rec = noteOfAnchor(a);
      if (rec) noteEdit(rec.el, a);
    }
"""

JS_AOPEN_NEW = """    function anchorOpen(a) {
      var rec = noteOfAnchor(a);
      if (!rec) return;
      /* ★ r109-l3 ①：**「预览批注的也是一样」** —— 点锚点看详情时，原点就是**锚点自己**。
         既有的 r109-l2 ④ 已经把「定位参照物」传成锚点（气泡落在锚点**下方**），
         但水平那一路当时还是 CSS 的 `left: 12px` ⇒ 锚点拖到右侧时，气泡仍在左边弹出来。
         这里把 `noteAt` 覆盖成锚点位置 ⇒ 与「点元素发起批注」共用**同一条定位路径**
         （`noteEdit()` 里那两个夹取完全一致），不再分叉。 */
      var ar = a.getBoundingClientRect(), vr = view.getBoundingClientRect();
      noteAt = { x: ar.left - vr.left + view.scrollLeft,
                 y: ar.top - vr.top + view.scrollTop };
      noteEdit(rec.el, a);
    }
"""

# ================================================================================
# ① 批注原点对齐（panel.js）—— 6/7：`noteDrop` 加原点形参
# ================================================================================
JS_DROPSIG_OLD = """    function noteDrop(el, n) {
"""

JS_DROPSIG_NEW = """    function noteDrop(el, n, at) {
"""

JS_DROP_OLD = """      view.appendChild(a);                  /* 先入 DOM —— `anchorPlace` 要量它的几何 */
      var er = el.getBoundingClientRect(), vr = view.getBoundingClientRect();
      anchorPlace(a, er.right - vr.left + view.scrollLeft - 12,
                  er.top - vr.top + view.scrollTop - 12);
      bindAnchor(a);
      return a;
    }
"""

JS_DROP_NEW = """      view.appendChild(a);                  /* 先入 DOM —— `anchorPlace` 要量它的几何 */
      /* ★ r109-l3 ①：**锚点落在「本次点击点」**（`at` = 内容坐标，见 `noteAt`）。
         锚点 24×24 ⇒ `−12` = 让它的**中心**咬住那个点（「在哪里点击就在哪里添加」）。
         ⚠ 旧读法（r93 起）= 被标注元素的**右上角 −12**：它假设「用户点的是元素右上角」，
           点长段落左端时锚点就飘到了段落右端 —— 正是邵先生说的「位置漂移太远」。
         ⚠ `at` 缺省 ⇒ 退回旧读法，只在「非点选路径」下发生（防御，正常不会命中）。
         ⚠ `anchorPlace` 的夹取照旧：拖/落到 `.td-view` 可视区边界会被夹住。 */
      if (at) {
        anchorPlace(a, at.x - 12, at.y - 12);
      } else {
        var er = el.getBoundingClientRect(), vr = view.getBoundingClientRect();
        anchorPlace(a, er.right - vr.left + view.scrollLeft - 12,
                    er.top - vr.top + view.scrollTop - 12);
      }
      bindAnchor(a);
      return a;
    }
"""

# ================================================================================
# ① 批注原点对齐（panel.js）—— 7/7：`noteCommit` 把原点交给 `noteDrop`，并在收尾清空
# ================================================================================
JS_COMMIT_OLD = """        rec.anchor = noteDrop(noteCur, rec.n);
"""

JS_COMMIT_NEW = """        rec.anchor = noteDrop(noteCur, rec.n, noteAt);
"""

JS_CLEAR_OLD = """      elnote.setAttribute('hidden', '');
      noteCur = null;
"""

JS_CLEAR_NEW = """      elnote.setAttribute('hidden', '');
      noteCur = null;
      /* ★ r109-l3 ①：原点用完即弃 —— 下一次批注一定由「新的点击」或「新的锚点」重写它，
         不清就会让「先点 A 处提交、再键盘触发一次编辑」这类路径误用上一处坐标。 */
      noteAt = null;
"""


def do_js():
    print('--- ① 批注原点对齐 + 编辑态「保存」（part109/panel.js）---')
    # ⚠ ①-1 与 ①-7b 是**追加式**编辑（old 一字不动、只在后面接新内容）⇒ `old in new` 恒真，
    #   STRICT 的「mark 与 old 同存 = 歧义」判据必然误报（patch109l2.py 上踩过同款）。
    #   这两条显式 `strict=False`；幂等性仍由 mark 保证（第二次跑命中 mark ⇒ 跳过）。
    edit(PJS, JS_AT_OLD, JS_AT_NEW, '①-1 新增 noteAt（原点）',
         mark='var noteAt = null;\n', strict=False)
    edit(PJS, JS_CTRL_OLD, JS_CTRL_NEW, '①-2 noteCtrl 文案收口（编辑态 ⇒ 保存）',
         mark="(noteCur && noteFind(noteCur)) ? '保存'")
    edit(PJS, JS_PICK_OLD, JS_PICK_NEW, '①-3 点选监听记下点击点',
         mark='noteAt = { x: e.clientX - vr0.left')
    edit(PJS, JS_BLEFT_OLD, JS_BLEFT_NEW, '①-4 气泡左边缘跟原点',
         mark='elnote.style.left = Math.round(left)')
    edit(PJS, JS_AOPEN_OLD, JS_AOPEN_NEW, '①-5 预览：锚点即原点',
         mark='noteAt = { x: ar.left - vr.left')
    edit(PJS, JS_DROPSIG_OLD, JS_DROPSIG_NEW, '①-6a noteDrop 加原点形参',
         mark='function noteDrop(el, n, at) {')
    edit(PJS, JS_DROP_OLD, JS_DROP_NEW, '①-6b noteDrop 按原点落位',
         mark='anchorPlace(a, at.x - 12, at.y - 12)')
    edit(PJS, JS_COMMIT_OLD, JS_COMMIT_NEW, '①-7a noteCommit 把原点交给 noteDrop',
         mark='noteDrop(noteCur, rec.n, noteAt)')
    # ⚠ ①-7b 的 mark 有两个坑，都真踩到了：
    #   1) 不能写成 `'noteCur = null;\n      noteAt = null;'` —— 新串在这两行**之间**插了说明注释
    #      ⇒ 跨注释的 mark 永不命中 ⇒ 第二次跑**重复注入**（首跑实测：panel.js 里出现两份）。
    #   2) 也不能写成 `'      noteAt = null;\n'` —— ①-3 的新代码里有一行 **10 空格缩进**的
    #      `noteAt = null;`（`else` 分支），而**子串匹配下 6 空格版是 10 空格版的子串**
    #      ⇒ ①-3 跑完后 mark 就假命中、①-7b 被静默跳过。
    #      （与「判据不能写裸词 / 裸前缀 / 裸后缀」同族，这是**缩进前缀**那一支。）
    #    改用这句只可能出现在本层新代码里的中文注释当 mark。
    edit(PJS, JS_CLEAR_OLD, JS_CLEAR_NEW, '①-7b noteCommit 收尾清空原点',
         mark='原点用完即弃', strict=False)


# ================================================================================
# ② `.r93-card` 取消 18px 左缩进（落在 make109.py 的 EDITS 表 = E9）
# ================================================================================
CARD_OLD = """/* 卡片 \u2605 r95 \u2460\uff1a\u5bbd\u5ea6\u6539\u4e3a**\u6d41\u5f0f + \u53f3\u4fa7\u6491\u6ee1** \u2014\u2014 \u4fdd\u7559\u8bbe\u8ba1\u7a3f 18px \u5de6\u7f29\u8fdb\uff0c\u53f3\u4fa7\u586b\u6ee1\u5185\u5bb9\u5217\u3002
   \uff08\u539f\u5148\u5199\u6b7b 822px \u662f\u6309\u8bbe\u8ba1\u7a3f\u91cf\u6b7b\uff1a\u5bb9\u5668\u6070 840 \u65f6\u521a\u597d\uff0c\u5bb9\u5668\u4e00\u53d8\u5bbd\u53f3\u4fa7\u5c31\u7559\u767d\u3002\uff09 */
.r93-card {
  position: relative; width: calc(100% - 18px); margin-left: 18px; border-radius: 8px;
"""

CARD_NEW = """/* \u2605 r109 \u7b2c\u4e09\u62cd \u2461\uff1a**\u53d6\u6d88 18px \u5de6\u7f29\u8fdb \u21d2 \u4e24\u7aef\u5bf9\u9f50**\uff08\u90b5\u5148\u751f\uff1a\u300c\u5bf9\u8bdd\u5185\u5bb9\u4e2d\u7684\u7c7b\u4f3c
   `r93-card r93-card--edge` \u8fd9\u6837\u7684\u5bb9\u5668\u524d\u9762\u7684\u7f29\u8fdb\u90fd\u53d6\u6d88\uff0c\u4e24\u7aef\u90fd\u5bf9\u9f50\u5427\u300d\uff09\u3002
   \u6cbf\u9769\uff1ar95 \u2460 \u628a\u5199\u6b7b\u7684 822px \u6539\u6210\u300c\u6d41\u5f0f + \u53f3\u4fa7\u6491\u6ee1\u300d\uff0c\u540c\u65f6**\u4fdd\u7559\u8bbe\u8ba1\u7a3f\u7684 18px \u5de6\u7f29\u8fdb**
   \uff08`width: calc(100% - 18px)` + `margin-left: 18px`\uff09\u2014\u2014 \u89c6\u89c9\u4e0a\u662f\u4e00\u5217\u53f3\u4fa7\u8d34\u8fb9\u3001\u5de6\u4fa7\u7559\u767d 18px \u7684\u5361\u3002
   \u672c\u62cd\u6309\u9700\u6c42\u6539\u6210**\u6ee1\u884c\u7b49\u5bbd**\uff1a\u5de6\u53f3\u4e24\u7aef\u90fd\u8d34\u5185\u5bb9\u5217\u3002
   \u26a0 \u53ea\u52a8\u5bbd\u5ea6\u8fd9\u4e24\u9879\uff1a`border-radius` / `background` / `padding` / \u5b57\u53f7 / \u9ad8\u5ea6\u4e00\u5b57\u672a\u52a8
     \u21d2 \u5361\u5185\u7684\u6362\u884c\u4f4d\u7f6e\u4f1a\u968f\u5bbd\u5ea6\u53d8\u5316\uff08\u53ef\u7528\u5bbd\u5ea6 +18px\uff09\uff0c\u8fd9\u662f\u672c\u9700\u6c42\u7684\u5e94\u6709\u7ed3\u679c\u3002
   \u26a0 `.r93-card--full`\uff08\u4e0b\u9762\u90a3\u6761 `width:100%; margin-left:0`\uff09\u4ece\u6b64\u6210\u4e3a**\u672c\u89c4\u5219\u7684\u5197\u4f59**\uff0c
     \u4f46\u5b83\u662f\u300c\u663e\u5f0f\u6ee1\u5bbd\u300d\u7684\u8bed\u4e49\u58f0\u660e\u3001\u4e14\u88ab\u591a\u5904\u8c03\u7528\uff0c**\u4fdd\u7559\u4e0d\u52a8**\u3002 */
.r93-card {
  position: relative; width: 100%; margin-left: 0; border-radius: 8px;
"""

CARD_HEAD = (
    "# ---------------------------------------------------------------- \u2461 \u5361\u7247\u4e24\u7aef\u5bf9\u9f50\n"
    "# \u2605 r109 \u7b2c\u4e09\u62cd \u2461\uff1a\u90b5\u5148\u751f\u300c\u5bf9\u8bdd\u5185\u5bb9\u4e2d\u7684\u7c7b\u4f3c `r93-card r93-card--edge` \u8fd9\u6837\u7684\u5bb9\u5668\u524d\u9762\u7684\n"
    "#   \u7f29\u8fdb\u90fd\u53d6\u6d88\uff0c\u4e24\u7aef\u90fd\u5bf9\u9f50\u5427\u300d\u3002`.r93-card` \u7684 CSS \u957f\u5728 `apply109.py` \u7684\u5185\u8054\u6837\u5f0f\u91cc\uff0c\n"
    "#   \u800c `apply109.py` \u662f\u672c\u811a\u672c\u4ece `apply108.py` **\u9010\u5b57\u751f\u6210**\u7684 \u21d2 \u4e0e\u7b2c\u4e8c\u62cd \u2462\uff08\u56fe\u6807\uff09\u540c\u8def\uff1a\n"
    "#   \u6539\u672c\u811a\u672c\u7684 EDITS \u8868\uff08\u91cd\u8dd1\u81ea\u6108\uff09\u3002\u26a0 \u53ea\u6539\u5bbd\u5ea6\u4e24\u9879\uff0c\u5176\u4f59\u58f0\u660e\u4e00\u5b57\u672a\u52a8\u3002\n"
)

# ================================================================================
# ③-d 配套：conversation 的 `<html>` 开标签必须**属性宽容**，且不得外溢适配护栏
#
# 起因（拍 3 真踩）：③ 的暗色适配层给**被适配的 5 页**在 `<html>` 上挂了 `data-gi-dark="1"`
#   （护栏标记）。而 `conversation.html` 由 `apply109.py` 从 `pages/base.html` 的**净底**重建
#   ⇒ 原来那条**逐字**锚点 `HTML_OLD = '<html lang="zh-CN">'` 会命中 **0** 次（标签里多出一个属性）
#   ⇒ 整条 apply 链当场 `sys.exit`（"<html> 锚点命中 0 次"）。
#   就算放过去，conversation 也会**丢掉** `data-r93-page`（暗色块的作用域锚）、并把护栏标记
#   **外溢**成「已适配」⇒ 未适配页拿到护栏 = 机制层真给它切暗、而适配层没有它 ⇒ **半暗半亮**。
#
# ⇒ E10：① 只认 `<html` 开标签（属性任意）；② 落 `data-r93-page` 前先摘掉
#   `data-gi-dark` 与旧 `data-r93-page`（护栏只属于被适配页，绝不随净底外溢）。
# ⚠ 本段**刻意不写任何反斜杠**：它要经 `_py_lit()` 再转义一层写进 `ev/make109.py`。
# ================================================================================
E10_LABEL = 'E10 net 底 `<html>` 锚点属性宽容'
E10_OLD = """        # ---- 4) conversation.html = 净底（带 data-r93-page） + 详情块 ----
        if net.count(HTML_OLD) != 1:
            sys.exit('!! <html> 锚点命中 %d 次（应 1 次）' % net.count(HTML_OLD))
        conv = net.replace(HTML_OLD, HTML_NEW)"""

E10_NEW = """        # ---- 4) conversation.html = 净底（带 data-r93-page） + 详情块 ----
        # ★ r109 第三拍 ③-d（E10）：`<html>` 开标签改**属性宽容**匹配，并在落标记前
        #   **摘掉适配护栏**（起因见 patch109l3.py 里 E10 那段注释）。
        #   ① 只认**文档里第一个** `<html` 开标签（净底的第一行就是它，位置必然很小）；
        #   ② 落 `data-r93-page` 前先摘 `data-gi-dark` 与旧 `data-r93-page`
        #      —— 护栏只属于被适配页，绝不随净底外溢。
        #   ⚠ 不能用 `<html[^>]*>` 之类的**全串正则**：注入的 CSS/JS 注释里也写了
        #     `<html>` / `<html data-gi-dark="1">` 这类字面 ⇒ 会命中 8 次（本拍真踩）。
        _i = net.find('<html')
        if _i < 0 or _i > 200:
            sys.exit('!! `<html` 开标签位置异常（%d）' % _i)
        _j = net.find('>', _i)
        _attrs = re.sub(' *data-(?:gi-dark|r93-page)="[^"]*"', '', net[_i + 5:_j])
        conv = (net[:_i] + '<html' + _attrs + ' data-r93-page="conversation">'
                + net[_j + 1:])"""

E10_HEAD = (
    "# ------------------------------------------- \u2462-d \u51c0\u5e95 `<html>` \u951a\u70b9\u5c5e\u6027\u5bbd\u5bb9\n"
    "# \u2605 r109 \u7b2c\u4e09\u62cd \u2462-d\uff1a\u9002\u914d\u5c42\u7ed9\u88ab\u9002\u914d\u9875\u7684 `<html>` \u6302\u4e86 `data-gi-dark=\"1\"`\uff0c\n"
    "#   \u800c\u672c\u811a\u672c\u4ee5 `base.html` \u51c0\u5e95\u91cd\u5efa `conversation.html` \u21d2 \u9010\u5b57\u951a\u70b9\u5931\u914d\u3002\n"
    "#   \u89e3\u6cd5\u89c1 `patch109l3.py` \u91cc E10 \u90a3\u6bb5\u6ce8\u91ca\u3002\u26a0 \u672c\u6bb5\u523b\u610f\u65e0\u53cd\u659c\u6760\u3002\n"
)


def _mk_insert(mk, label, old_name, new_name, head, consts_body):
    """在 `EDITS = [` 表头插一条，并把常量块插到 `EDITS = [` 之前（与 REGEN_* 同层）。"""
    if mk.count('EDITS = [\n') != 1:
        sys.exit('!! make109.py：`EDITS = [` 命中 %d 次' % mk.count('EDITS = [\n'))
    entry = ("EDITS = [\n"
             "    (\n"
             "        '%s',\n"
             "        %s,\n"
             "        %s,\n"
             "        1,\n"
             "    ),\n" % (label, old_name, new_name))
    mk2 = mk.replace('EDITS = [\n', entry, 1)
    i = mk2.find('EDITS = [\n')
    return mk2[:i] + head + consts_body + '\n' + mk2[i:]


def do_make():
    print('--- ② 卡片两端对齐（E9）· ③-d 净底锚点（E10）（ev/make109.py 的 EDITS 表）---')
    mk, nl = rd(MAKE)

    # ---- E9 ----
    if 'E9 对话卡片取消 18px 左缩进' in mk:
        SKIPPED.append('② E9 卡片两端对齐')
        print('   跳过  ② E9 卡片两端对齐（已应用）')
    else:
        mk2 = _mk_insert(
            mk, 'E9 对话卡片取消 18px 左缩进 ⇒ 两端对齐', 'CARD_OLD', 'CARD_NEW',
            CARD_HEAD,
            "CARD_OLD = (\n" + _py_lit(CARD_OLD) + ")\nCARD_NEW = (\n" + _py_lit(CARD_NEW) + ")\n")
        ast.parse(mk2)
        if 'E9 对话卡片取消 18px 左缩进' not in mk2:
            sys.exit('!! make109.py：E9 未进入 EDITS 表')
        mk = mk2
        wr(MAKE, mk, nl)
        APPLIED.append('② E9 卡片两端对齐')
        print('   %s  ② E9 卡片两端对齐' % ('校验' if CHECK else '应用'))

    # ---- E10（③-d）----
    if E10_LABEL in mk:
        SKIPPED.append('③-d E10 净底 <html> 锚点属性宽容')
        print('   跳过  ③-d E10 净底 <html> 锚点属性宽容（已应用）')
        return
    mk2 = _mk_insert(
        mk, E10_LABEL, 'E10_OLD', 'E10_NEW', E10_HEAD,
        "E10_OLD = (\n" + _py_lit(E10_OLD) + ")\nE10_NEW = (\n" + _py_lit(E10_NEW) + ")\n")
    ast.parse(mk2)
    if E10_LABEL not in mk2:
        sys.exit('!! make109.py：E10 未进入 EDITS 表')
    if not CHECK:
        wr(MAKE, mk2, nl)
    APPLIED.append('③-d E10 净底 <html> 锚点属性宽容')
    print('   %s  ③-d E10 净底 <html> 锚点属性宽容（%d → %d 字符）'
          % ('校验' if CHECK else '应用', len(mk), len(mk2)))
    print('   ⚠ E10 改了生成器 ⇒ 必须重跑 `python mg-work/r109/ev/make109.py`，'
          '再跑 `apply109.py`、最后 `apply-theme.py` → `apply-dark.py`')



def _py_lit(s):
    """把一段原文转成 Python 字面量（2 空格缩进的 `\\n` 续行），只转义 \\ 与 "。"""
    out = []
    lines = s.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    for ln in lines:
        e = ln.replace('\\', '\\\\').replace('"', '\\"')
        out.append('        "%s\\n"\n' % e)
    return ''.join(out)


# ================================================================================
# 上一层判据同步放宽（后一层必须替前一层保住）
# ================================================================================
L2_OLD = """    seg_drop = j_bare.split('function noteDrop(el, n) {')"""
L2_NEW = """    # \u26a0 r109-l3 \u2460 \u628a\u5f62\u53c2\u6539\u6210 `(el, n, at)` \u21d2 \u8fd9\u91cc\u6309**\u524d\u7f00**\u5206\u5272\uff0c\u4e24\u79cd\u7b7e\u540d\u90fd\u547d\u4e2d
    #   \uff08\u540e\u4e00\u5c42\u5fc5\u987b\u66ff\u524d\u4e00\u5c42\u4fdd\u4f4f\u5224\u636e\uff1b\u540c l2 \u5bf9 l1 \u90a3\u6761\u7684\u505a\u6cd5\uff09\u3002
    seg_drop = j_bare.split('function noteDrop(el')"""


def do_l2():
    print('--- 上一层判据同步（ev/patch109l2.py）---')
    edit(L2, L2_OLD, L2_NEW, 'l2 noteDrop 判据放宽（el, n[, at]）',
         mark="j_bare.split('function noteDrop(el')")


# ================================================================================
# 跨层自检
# ================================================================================
def verify():
    j, _ = rd(PJS)
    mk, _ = rd(MAKE)
    l2, _ = rd(L2)
    j_bare = re.sub(r'/\*.*?\*/', '', re.sub(r'^\s*//[^\n]*', '', j, flags=re.M), flags=re.S)
    bad = []

    # ---- ① ----
    if 'var noteAt = null;' not in j_bare:
        bad.append('panel.js：① 缺 `noteAt`')
    # 原点必须在「摘 hidden」之后用（隐藏态量不出几何）
    seg_edit = j_bare.split('function noteEdit(el')
    if len(seg_edit) != 2:
        bad.append('panel.js：① `noteEdit()` 命中 %d 次' % (len(seg_edit) - 1))
    else:
        body = seg_edit[1].split('\n    }')[0]
        i_h = body.find('elnote.offsetHeight')
        i_t = body.find('elnote.style.top =')
        i_w = body.find('elnote.offsetWidth')
        i_l = body.find('elnote.style.left =')
        if i_t < 0 or i_l < 0:
            bad.append('panel.js：① 气泡缺 `top` / `left` 定位')
        if i_h < 0 or i_h > i_t:
            bad.append('panel.js：① 高必须在写 `top` 之前量（h=%d top=%d）' % (i_h, i_t))
        if i_w < 0 or i_w > i_l:
            bad.append('panel.js：① 宽必须在写 `left` 之前量（w=%d left=%d）' % (i_w, i_l))
        if 'noteAt ? noteAt.x :' not in body:
            bad.append('panel.js：① 气泡水平没有跟 `noteAt`')
        if 'view.scrollLeft + view.clientWidth' not in body:
            bad.append('panel.js：① 气泡水平缺可视带夹取')
        # r109-l2 的契约必须还在
        if 'var ref = at || el;' not in body:
            bad.append('panel.js：①（回归）`noteEdit()` 里丢了 `var ref = at || el;`')
        i_un = body.find("removeAttribute('hidden')")
        i_gr = body.find('noteGrow()')
        if i_un < 0 or i_gr < 0 or i_gr < i_un:
            bad.append('panel.js：①（回归）`noteGrow()` 不在摘 `[hidden]` 之后')
    # noteCtrl：编辑态 ⇒ 保存，且只有一个收口点
    seg_ctrl = j_bare.split('function noteCtrl(on) {')
    if len(seg_ctrl) != 2:
        bad.append('panel.js：① `noteCtrl()` 命中 %d 次' % (len(seg_ctrl) - 1))
    else:
        body = seg_ctrl[1].split('\n    }')[0]
        if "'保存'" not in body or 'noteFind(noteCur)' not in body:
            bad.append('panel.js：① `noteCtrl()` 里没有「编辑态 ⇒ 保存」的收口')
    for s in ("textContent = '保存'", "= prev ? '保存' : '添加'", "'保存' : '添加'"):
        if s in j_bare:
            bad.append('panel.js：① 文案切换散落在别处（`%s`）—— 必须只在 noteCtrl 里' % s)
    # 点选监听写了点击点
    # ⚠ 判据**不能**用裸串 `view.addEventListener('click', ...)` ——
    #   `gitReview.addEventListener('click', function (e) {` 的**尾部**正好含它
    #   （`gitReview` 以 `view` 结尾）⇒ 假报「命中 2 次」。这是与「判据不能写裸词」同族的
    #   **裸后缀**坑。带上前面那行 `if (view) {` 就唯一了。
    seg_pick = j_bare.split("if (view) {\n      view.addEventListener('click', function (e) {")
    if len(seg_pick) != 2:
        bad.append('panel.js：① `.td-view` click 监听命中 %d 次' % (len(seg_pick) - 1))
    else:
        body = seg_pick[1].split('\n    }')[0]
        if 'noteAt = { x: e.clientX' not in body:
            bad.append('panel.js：① 点选监听没记点击点')
        if 'e.clientX || e.clientY' not in body:
            bad.append('panel.js：① 点选监听没防「键盘触发 click 时坐标为 0」')
    # anchorOpen 覆盖 noteAt
    seg_ao = j_bare.split('function anchorOpen(a) {')
    if len(seg_ao) != 2:
        bad.append('panel.js：① `anchorOpen()` 命中 %d 次' % (len(seg_ao) - 1))
    else:
        body = seg_ao[1].split('\n    }')[0]
        if 'noteAt = { x: ar.left' not in body:
            bad.append('panel.js：① `anchorOpen()` 没把原点设成锚点（预览路径）')
    # noteDrop 三参 + 中心咬点
    if 'function noteDrop(el, n, at) {' not in j_bare:
        bad.append('panel.js：① `noteDrop` 没加 `at` 形参')
    if 'anchorPlace(a, at.x - 12, at.y - 12)' not in j_bare:
        bad.append('panel.js：① `noteDrop` 没按原点落位（−12 = 半锚点 ⇒ 中心咬点）')
    if 'noteDrop(noteCur, rec.n, noteAt)' not in j_bare:
        bad.append('panel.js：① `noteCommit` 没把原点交给 `noteDrop`')
    # l2 的契约：锚点仍先入 DOM 再落位
    seg_drop = j_bare.split('function noteDrop(el, n, at) {')
    if len(seg_drop) != 2:
        bad.append('panel.js：① `noteDrop(el, n, at)` 命中 %d 次' % (len(seg_drop) - 1))
    else:
        body = seg_drop[1].split('\n    }')[0]
        i_app = body.find('view.appendChild(a)')
        i_pl = body.find('anchorPlace(a,')
        if i_app < 0 or i_pl < 0 or i_pl < i_app:
            bad.append('panel.js：①（回归）`anchorPlace` 不在 `appendChild` 之后')
        for s in ("role', 'button'", "tabindex', '0'", 'bindAnchor(a)'):
            if s not in body:
                bad.append('panel.js：①（回归）`noteDrop` 里少了 `%s`' % s)
        if 'aria-hidden' in body:
            bad.append('panel.js：①（回归）锚点又挂回了 `aria-hidden`')

    # ---- ② ----
    if 'E9 对话卡片取消 18px 左缩进' not in mk:
        bad.append('make109.py：② 缺 E9')
    if 'CARD_OLD = (' not in mk or 'CARD_NEW = (' not in mk:
        bad.append('make109.py：② 缺 CARD_OLD / CARD_NEW 常量')

    # ---- ③-d（E10：净底 `<html>` 锚点属性宽容 + 摘掉适配护栏）----
    if E10_LABEL not in mk:
        bad.append('make109.py：③-d 缺 E10')
    if 'E10_OLD = (' not in mk or 'E10_NEW = (' not in mk:
        bad.append('make109.py：③-d 缺 E10_OLD / E10_NEW 常量')
    try:
        ast.parse(mk)
    except SyntaxError as e:
        bad.append('make109.py：② 生成器自己编译不过（%s）' % e)
    if "width: calc(100% - 18px); margin-left: 18px" not in mk:
        bad.append('make109.py：② E9 的 old 串里没有那对「18px 缩进」')
    if "width: 100%; margin-left: 0; border-radius: 8px;" not in mk:
        bad.append('make109.py：② E9 的 new 串里没有「两端对齐」')
    # ⚠ CARD_OLD 里**本来就含**旧值（它就是被替换的 old 串）⇒ 不能拿「旧值还在 make109 里」
    #   当失败判据；真正的判据在 `apply109.py` / 产物侧（见 `tools/check-card.py` 与真机实测）。

    # ---- 上一层判据放宽 ----
    if "j_bare.split('function noteDrop(el')" not in l2:
        bad.append('patch109l2.py：noteDrop 判据没放宽（上一层复跑会报错）')

    if bad:
        sys.exit('!! 跨层自检失败：\n   ' + '\n   '.join(bad))
    print('   全部存活 ✓')
    print()
    print('应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for s in SKIPPED:
        print('   跳过  %s' % s)


def main():
    global CHECK
    if '--check' in sys.argv:
        CHECK = True
    if '--bak' in sys.argv:
        if not os.path.isdir(BAK):
            os.makedirs(BAK)
        for src, name in ((PJS, 'panel.js.before'), (PCS, 'panel.css.before'),
                          (MAKE, 'make109.py.before'), (L2, 'patch109l2.py.before')):
            if os.path.exists(src):
                shutil.copyfile(src, os.path.join(BAK, name))
        print('   备份 → %s' % BAK)
    do_js()
    do_make()
    do_l2()
    verify()


if __name__ == '__main__':
    main()

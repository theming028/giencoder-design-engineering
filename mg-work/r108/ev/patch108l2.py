# -*- coding: utf-8 -*-
"""r108 第十三拍（第二层补丁）—— 邵先生六条里的第 1~4 + 6 条（第 5 条在别的页，见 `patch108td.py`）：

  ① `.td-sum-sec` hover 时边框加深一级（border-1 → border-2）
  ② 去掉 `.td-sum-h` 标题前的图标（4 处）+ 清掉随它一起死的 `.td-sum-h svg` 规则
  ③ `.td-diff-toggle` 的图标（`.td-diff-cv`）改正文色 + 尺寸 13px
  ④ `.td-sum-art` 产物卡片整体可点击（`data-td-art` 从内部按钮上移到整张卡）
  ⑥ 复刻 ZCode 对话界面右上角的「实时任务信息面板」到会话详情页右上角

改序（只能下→上）：
    1. `mg-work/r108/part108/_mods.html`   ④ 两处 data 属性 + ⑥ 面板静态 DOM（末尾追加）
    2. `mg-work/r108/part108/panel.css`    ①②③④ 的小改 + ⑥ 第 19 节
    3. `mg-work/r108/part108/panel.js`     ⑥ 面板控制器（末尾追加一个 IIFE）
    4. `python mg-work/r108/ev/splice108.py`   → `part108/browse.html`
    5. `python mg-work/r108/apply108.py`       → 落 `pages/conversation.html`

★ 为什么另起一层（l2）而不是就地改 l1：l1 已跑过且已验证，`mark` 各自独立 ⇒ 两层互不干扰，
  复跑各自「应用 0 / 跳过 N」。本代（r108）内叠加，**不另起代数**（r108 未提交）。

幂等判据：每处都带 `mark`（**只有改完之后才存在**的串）⇒ 复跑「应用 0 项 / 跳过 N 项」。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P108 = os.path.join(REPO, 'mg-work', 'r108', 'part108')
MODS = os.path.join(P108, '_mods.html')
PCS = os.path.join(P108, 'panel.css')
PJS = os.path.join(P108, 'panel.js')

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
    if mark and mark in t:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1 次）' % (label, n))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)
    print('   应用  %s（%d → %d 字符）' % (label, len(t), len(t) - len(old) + len(new)))


def edit_all(p, old, new, label, mark, expect):
    """整篇替换 N 处（N 由调用方断言）。"""
    t, nl = rd(p)
    if mark and mark in t:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != expect:
        sys.exit('!! %s：锚点命中 %d 次（应 %d 次）' % (label, n, expect))
    wr(p, t.replace(old, new), nl)
    APPLIED.append(label)
    print('   应用  %s（%d 处，%d → %d 字符）' % (label, n, len(t), len(t) + n * (len(new) - len(old))))


def drop_re(p, pat, label, expect, rep=''):
    """按正则删掉 N 处（`rep` 默认空 ⇒ 纯删除）。**幂等判据 = 模式不再命中**
    （删除类改动没有「改完才出现」的 mark）。"""
    t, nl = rd(p)
    n = len(re.findall(pat, t))
    if n == 0:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    if n != expect:
        sys.exit('!! %s：正则命中 %d 次（应 %d 次）' % (label, n, expect))
    wr(p, re.sub(pat, rep, t), nl)
    APPLIED.append(label)
    print('   应用  %s（%d 处）' % (label, n))


def del_once(p, old, label):
    t, nl = rd(p)
    if old not in t:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    if t.count(old) != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1 次）' % (label, t.count(old)))
    wr(p, t.replace(old, '', 1), nl)
    APPLIED.append(label)
    print('   应用  %s（删 %d 字符）' % (label, len(old)))


def tail(p, mark, new, label):
    t, nl = rd(p)
    if mark in t:
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    if not t.endswith('\n'):
        t += '\n'
    wr(p, t + new, nl)
    APPLIED.append(label)
    print('   应用  %s（追加 %d 字符）' % (label, len(new)))


# ================================================================================
# ⑥ 面板静态 DOM
# ================================================================================
SVG_CV = ('<svg class="zd-cv" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="12" '
          'height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
          'stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>')

MIN_BTN = ('            <button class="td-browse-ico" type="button" title="收起为胶囊" '
           'aria-label="收起为胶囊" data-zd-min="1"><svg xmlns="http://www.w3.org/2000/svg" '
           'viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
           'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<path d="m6 15 6-6 6 6"/></svg></button>')

PAUSE_BTN = ('<button class="td-browse-ico" type="button" title="暂停目标" aria-label="暂停目标">'
             '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" '
             'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true"><path d="M9 4v16"/><path d="M15 4v16"/></svg>'
             '</button>')

ICO = {
    # 24 网格 / stroke-width 2 / 渲染 16px（与本页既有图标同口径）
    'diff': ('<path d="M4 2h11.5l3.5 5.5v13a1.5 1.5 0 0 1-1.5 1.5H4a1.5 1.5 0 0 1-1.5-1.5v-17'
             'A1.5 1.5 0 0 1 4 2Z"/><path d="M14 10v6"/><path d="M11 13h6"/>'),
    'branch': ('<circle cx="6" cy="6" r="2.5"/><circle cx="6" cy="18" r="2.5"/>'
               '<circle cx="18" cy="6" r="2.5"/><path d="M6 8.5v7"/>'
               '<path d="M18 8.5a6 6 0 0 1-6 6H9"/>'),
    'commit': ('<circle cx="12" cy="12" r="3"/><path d="M3 12h6"/><path d="M15 12h6"/>'),
    'goal': '<path d="M5 21V3"/><path d="M5 4h12l-2.5 3.5L17 11H5"/>',
    'checks': ('<path d="m3 6 1.5 1.5L7 5"/><path d="m3 12 1.5 1.5L7 11"/>'
               '<path d="m3 18 1.5 1.5L7 17"/><path d="M11 7h9"/><path d="M11 12h9"/>'
               '<path d="M11 17h9"/>'),
}


def svg(name, cls=''):
    c = ' class="%s"' % cls if cls else ''
    return ('<svg%s xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" '
            'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">%s</svg>' % (c, ICO[name]))


TODO = [
    ('is-done', '拆出侧栏骨架的三段式结构（标签栏 / 模块工具条 / 正文）'),
    ('is-done', '落地审查模块：diff 折叠、统一⇄并排、行内评论'),
    ('is-done', '落地终端与浏览器模块（含元素标注）'),
    ('is-doing', '补全审查模块的显示选项与 staging 动作'),
    ('', '补一轮暗色档与字号杠杆的回归'),
]
TODO_HTML = '\n'.join(
    '                <li%s>%s</li>' % ((' class="%s"' % k) if k else '', v) for k, v in TODO)

PANEL_HTML = '''
    <!-- ★ 第十三拍 ⑥：任务信息面板 —— 复刻 ZCode 对话界面右上角的实时状态面板。
         上游 = `zai-org/ZCode`（Apache-2.0）`packages/ui/src/v4/ConversationStatusPanel.tsx`
         + `conversationStatusPanelModel.ts` + `packages/ui/src/i18n/locales/zh-CN.ts` 的
         `chat.statusPanel.*` / `chat.summaryPanel.*` 两组文案；四个分区与行结构逐条对齐上游：
           · `environment` → 「Git 工具」（更改 / 分支 / 提交·推送）
           · `goal`        → 「目标」（迭代行：序号圈 + 标题 + 完成比，trailing = 用时 + 暂停）
           · `sessionPlans`→ 「计划」
           · `plan`        → 「进程」（待办清单，trailing = 已完成/总数）
         体位照上游：容器 `absolute top-0 right-4 pt-4`、不参与文档流、卡片自身收事件；
         收起态 = 一枚胶囊（上游 `chat.summaryPanel.showMini`「收起为胶囊」）。
         ⚠ 本块挂在 右栏容器 `aside.td-browse` 内只是为了跟随「静态 DOM 注入」的体位，
           `panel.js` 初始化时会把它整体搬进 `<main>`（`<main>` 的右上角才是「对话界面右上角」）。 -->
    <div class="zd-host" id="av-zd-status" data-zd="1">
      <div class="zd-card" data-zd-card="1" role="region" aria-label="任务状态">
        <div class="zd-head">
          <span class="zd-name">状态</span>
          <span class="zd-acts">
''' + MIN_BTN + '''
          </span>
        </div>
        <div class="zd-body">

          <section class="zd-sec" data-zd-sec="git">
            <div class="zd-sec-h">
              <button class="zd-sec-t" type="button" aria-expanded="true">Git 工具''' + SVG_CV + '''</button>
              <span class="zd-sec-x"><span class="zd-add">+566</span><span class="zd-del">−228</span></span>
            </div>
            <div class="zd-sec-b">
              <div class="zd-rows">
                <button class="zd-row" type="button"><span class="zd-row-i">''' + svg('diff') + '''</span><span class="zd-row-n">更改</span><span class="zd-row-v"><span class="zd-add">+566</span> <span class="zd-del">−228</span></span></button>
                <button class="zd-row" type="button"><span class="zd-row-i">''' + svg('branch') + '''</span><span class="zd-row-n">分支</span><span class="zd-row-v">main</span></button>
                <button class="zd-row" type="button"><span class="zd-row-i">''' + svg('commit') + '''</span><span class="zd-row-n">提交 / 推送</span></button>
              </div>
            </div>
          </section>

          <section class="zd-sec" data-zd-sec="goal">
            <div class="zd-sec-h">
              <button class="zd-sec-t" type="button" aria-expanded="true">目标''' + SVG_CV + '''</button>
              <span class="zd-sec-x">2 分 18 秒''' + PAUSE_BTN + '''</span>
            </div>
            <div class="zd-sec-b">
              <div class="zd-rows">
                <div class="zd-it"><span class="zd-it-no">1</span><p class="zd-it-t">拆出侧栏骨架的三段式结构（标签栏 / 模块工具条 / 正文）</p><span class="zd-it-c">3/3</span></div>
                <div class="zd-it"><i class="zd-it-i">''' + svg('goal') + '''</i><p class="zd-it-t">落地审查、终端、浏览器、摘要四个面板</p><span class="zd-it-c">3/4</span></div>
              </div>
            </div>
          </section>

          <section class="zd-sec" data-zd-sec="plan">
            <div class="zd-sec-h">
              <button class="zd-sec-t" type="button" aria-expanded="true">计划''' + SVG_CV + '''</button>
            </div>
            <div class="zd-sec-b">
              <div class="zd-rows">
                <button class="zd-row" type="button"><span class="zd-row-i">''' + svg('checks') + '''</span><span class="zd-row-n">右栏复刻方案.md</span></button>
              </div>
            </div>
          </section>

          <section class="zd-sec" data-zd-sec="todo">
            <div class="zd-sec-h">
              <button class="zd-sec-t" type="button" aria-expanded="true">进程''' + SVG_CV + '''</button>
              <span class="zd-sec-x">3/5</span>
            </div>
            <div class="zd-sec-b">
              <ul class="zd-todo">
''' + TODO_HTML + '''
              </ul>
            </div>
          </section>

        </div>
      </div>
      <button class="zd-mini" type="button" data-zd-mini="1" hidden aria-label="展开任务状态">
        <span class="zd-mini-i">''' + svg('checks') + '''</span>
        <span class="zd-mini-t">进程</span>
        <span class="zd-mini-v">3/5</span>
      </button>
    </div>
'''

# ================================================================================
# ⑥ 面板 CSS（第 19 节）
# ================================================================================
CSS_NEW = '''
/* ---------------------------------------------------------------- 19.0 第十三拍 ①~④ 的小改 */
/* ① 摘要卡片 hover：边框加深一级（border-1 = gray-2 #F2F2F2 → border-2 = gray-3 #E5E5E5）。
   `.td-sum-sec` 的基态 border 写在 shorthand 里，这里只覆盖 `border-color` 就够。 */
.td-sum-sec:hover { border-color: var(--color-border-2); }
/* ④ 产物卡整体可点：`data-td-art` 已从内部「预览」按钮上移到卡片本身（见 `_mods.html`）；
   按钮保留（视觉锚点 + 键盘入口），点击靠冒泡落到卡片上。 */
.td-sum-art[data-td-art] { cursor: pointer; }

/* ================================================================================
   19. 任务信息面板（第十三拍 ⑥）—— 复刻 ZCode 对话界面右上角的实时任务信息卡片
   --------------------------------------------------------------------------------
   上游：`zai-org/ZCode`（Apache-2.0）`packages/ui/src/v4/ConversationStatusPanel.tsx`。
   上游体位 = `absolute top-0 right-4 pt-4 z-20` + 外壳 `rounded-2xl border shadow-md w-80`、
   内层 `p-2 gap-2`；分区头 `h-8 px-2` + 标题 `foreground-subtle` + hover 才显形的 chevron。
   本页把「2xl 圆角 / tailwind 色」换成我仓 DS：圆角 large 8、token 色、`--shadow3-down`。
   ⚠ 卡片挂进 `<main>` 后才算「对话界面右上角」⇒ 先把 main 变成包含块（本页只有一个 main）。
   ============================================================================ */
main { position: relative; }

.zd-host {
  /* ⚠ `top` 不能是 0：`<main>` 顶部有一条 .r93-bar（`position:absolute; height:44px; z-index:10`，
     r106 定的固定档，不随字号杠杆变），右上角那两枚「全屏 / 打开侧栏」按钮就在里面 ——
     面板若从 main 顶起就会**把它盖住**（实测 elementFromPoint 命中的是面板自己的 .zd-acts）。
     ⇒ 从栏下沿起排，再留 12px 间距。 */
  position: absolute; top: 44px; right: 16px; z-index: 20;
  display: flex; justify-content: flex-end;
  box-sizing: border-box; padding-top: 12px;
  pointer-events: none;              /* 容器不吃事件（上游同款）—— 只有卡片自己吃 */
  max-width: calc(100% - 32px);
}
.zd-card {
  pointer-events: auto;
  box-sizing: border-box;
  width: 320px; max-width: 100%;
  max-height: min(64vh, 512px);
  display: flex; flex-direction: column; overflow: hidden;
  border: 1px solid var(--color-border-2); border-radius: 8px;
  background: var(--color-bg-2); box-shadow: var(--shadow3-down);
  font-size: var(--font-size-body-2); color: var(--color-text-1);
}
.zd-card[hidden] { display: none; }

.zd-head {
  flex: none; display: flex; align-items: center; gap: 8px;
  box-sizing: border-box; padding: 0 4px 0 12px;
  height: calc(36px * var(--ui-fs-ratio));
  min-height: calc(36px * var(--ui-fs-ratio));
  border-bottom: 1px solid var(--color-border-1);
  font-size: var(--font-size-body-2);
}
.zd-name {
  flex: 1 1 auto; min-width: 0; font-weight: 500; color: var(--color-text-1);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.zd-acts { flex: none; display: flex; align-items: center; gap: 2px; }

.zd-body {
  min-height: 0; flex: 1 1 auto;
  display: flex; flex-direction: column; gap: 8px;
  box-sizing: border-box; padding: 8px;
  overflow-x: hidden; overflow-y: auto;
}

.zd-sec { min-width: 0; flex: none; }
.zd-sec + .zd-sec { border-top: 1px solid var(--color-border-1); padding-top: 8px; }
.zd-sec-h {
  display: flex; align-items: center; gap: 6px;
  box-sizing: border-box; padding: 0 8px;
  height: calc(28px * var(--ui-fs-ratio));
  min-height: calc(28px * var(--ui-fs-ratio));
  font-size: var(--font-size-body-1); color: var(--color-text-3);
}
.zd-sec-t {
  flex: none; display: inline-flex; align-items: center; gap: 4px;
  padding: 0; border: 0; background: transparent;
  font-family: inherit; font-size: inherit; color: inherit;
  cursor: pointer;
}
.zd-sec-t:hover { color: var(--color-text-1); }
.zd-sec-x {
  flex: 1 1 auto; min-width: 0;
  display: flex; align-items: center; justify-content: flex-end; gap: 6px;
  font-size: var(--font-size-body-1); color: var(--color-text-3);
  font-variant-numeric: tabular-nums;
}
/* 折叠 chevron：上游默认 opacity-0、hover / focus 才显形（含方向切换） */
.zd-cv { flex: none; width: 12px; height: 12px; opacity: 0; transition: opacity 120ms, transform 120ms; }
.zd-sec-t:hover .zd-cv, .zd-sec-t:focus-visible .zd-cv { opacity: 1; }
.zd-sec.is-closed .zd-cv { transform: rotate(-90deg); }
.zd-sec.is-closed .zd-sec-b { display: none; }

.zd-rows { display: flex; flex-direction: column; }
.zd-row {
  display: flex; align-items: center; gap: 8px;
  box-sizing: border-box; padding: 0 8px;
  min-height: calc(32px * var(--ui-fs-ratio));
  border-radius: 4px; text-align: left;
  font-size: var(--font-size-body-2); color: var(--color-text-1);
}
/* ⚠ 只继承 font-family 不写 `font: inherit` —— 后者会把上面的 font-size 一起重置掉（字号会被
   继承值顶替、且 `scan-flatten.py` 也认不出它受 token 管辖）。 */
button.zd-row {
  width: 100%; border: 0; background: transparent;
  font-family: inherit; cursor: pointer;
}
button.zd-row:hover { background: var(--color-fill-1); }
.zd-row-i {
  flex: none; width: 16px; height: 16px;
  display: inline-flex; align-items: center; justify-content: center;
  color: var(--color-text-2);
}
.zd-row-n { flex: 1 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.zd-row-v { flex: none; color: var(--color-text-2); font-variant-numeric: tabular-nums; }
/* 增删色沿用本页审查模块的既有口径（`.td-rv-stat .is-add/.is-del`）：增 = success-6、删 = danger-6 */
.zd-add { color: var(--color-success-6); }
.zd-del { color: var(--color-danger-6); }

/* 「目标」分区的迭代行（上游：已完成 = 绿圈序号；未完成 = GoalIcon + 标题 + 完成比） */
.zd-it {
  display: flex; align-items: flex-start; gap: 8px;
  box-sizing: border-box; padding: 6px 8px;
  border-radius: 4px;
  font-size: var(--font-size-body-2); color: var(--color-text-1);
}
.zd-it-no {
  flex: none; box-sizing: border-box;
  width: 16px; height: 16px; border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center;
  border: 1px solid var(--color-success-6); color: var(--color-success-6);
  font-size: var(--font-size-body-1); font-variant-numeric: tabular-nums;
}
.zd-it-i { flex: none; width: 16px; height: 16px; color: var(--color-text-3); }
.zd-it-t {
  flex: 1 1 auto; min-width: 0; margin: 0;
  font-size: var(--font-size-body-2);
  line-height: calc(20px * var(--ui-fs-ratio));
}
.zd-it-c {
  flex: none; color: var(--color-text-3);
  font-size: var(--font-size-body-1); font-variant-numeric: tabular-nums;
}

/* 「进程」分区：待办清单（三态与右栏摘要模块同口径：空环 / 蓝环 / 绿勾） */
.zd-todo { display: flex; flex-direction: column; gap: 4px; margin: 0; padding: 0; list-style: none; }
.zd-todo li {
  position: relative; box-sizing: border-box; padding-left: 22px;
  font-size: var(--font-size-body-2); line-height: calc(22px * var(--ui-fs-ratio));
  color: var(--color-text-2);
}
.zd-todo li::before {
  content: ''; position: absolute; left: 2px; top: 5px;
  width: 12px; height: 12px; box-sizing: border-box;
  border: 1.5px solid var(--color-border-3); border-radius: 50%;
}
.zd-todo li.is-done { color: var(--color-text-3); }
.zd-todo li.is-done::before { background: var(--color-success-6); border-color: var(--color-success-6); }
.zd-todo li.is-done::after {
  content: ''; position: absolute; left: 5.5px; top: 9px;
  width: 5px; height: 2.5px;
  border-left: 1.5px solid var(--color-white);
  border-bottom: 1.5px solid var(--color-white);
  transform: rotate(-45deg);
}
.zd-todo li.is-doing { color: var(--color-text-1); }
.zd-todo li.is-doing::before { border-color: var(--color-primary-6); background: var(--color-primary-light-2); }

/* 收起态胶囊（上游 `chat.summaryPanel.showMini`「收起为胶囊」） */
.zd-mini {
  pointer-events: auto;
  box-sizing: border-box; display: inline-flex; align-items: center; gap: 8px;
  max-width: 100%; padding: 0 12px;
  height: calc(32px * var(--ui-fs-ratio));
  min-height: calc(32px * var(--ui-fs-ratio));
  border: 1px solid var(--color-border-2); border-radius: 999px;
  background: var(--color-bg-2); box-shadow: var(--shadow3-down);
  font-family: inherit; font-size: var(--font-size-body-2); color: var(--color-text-1);
  cursor: pointer;
}
.zd-mini[hidden] { display: none; }
.zd-mini:hover { border-color: var(--color-border-3); }
.zd-mini-i {
  flex: none; width: 16px; height: 16px;
  display: inline-flex; align-items: center; justify-content: center;
  color: var(--color-text-2);
}
.zd-mini-t { flex: none; }
.zd-mini-v { flex: none; color: var(--color-text-3); font-variant-numeric: tabular-nums; }
/* r108-l2 */
'''

# ================================================================================
# ⑥ 面板控制器 JS
# ================================================================================
JS_NEW = '''
/* ==================== 任务信息面板（第十三拍 ⑥） ==================== */
/* 复刻 ZCode 右上角状态面板的**交互骨架**：① 每个分区标题可折/展；② 头部「收起为胶囊」；
   ③ 点胶囊摊回面板。面板本体是 `_mods.html` 里的静态 DOM（`#av-zd-status`），初始挂在右栏
   `<aside class="td-browse">` 内（跟随静态注入的体位）—— 这里把它**整体搬进 `<main>`**，
   这样 `absolute top-0 right-16 pt-16` 量到的才是「对话界面右上角」（上游同款体位）。 */
(function () {
  var host = document.getElementById('av-zd-status');
  if (!host) return;
  if (host.getAttribute('data-zd-ready') === '1') return;   /* 幂等：同一份 DOM 只初始化一次 */
  host.setAttribute('data-zd-ready', '1');

  function place() {
    var main = document.querySelector('main');
    if (!main) return false;
    if (host.parentNode !== main) main.appendChild(host);
    return true;
  }
  /* React 首帧可能还没渲染出 <main> ⇒ 等一次 DOM 变化再挂（与右栏补挂同一范式）。 */
  if (!place()) {
    var mo = new MutationObserver(function () { if (place()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
    window.setTimeout(function () { place(); mo.disconnect(); }, 4000);
  }

  var card = host.querySelector('[data-zd-card]');
  var mini = host.querySelector('[data-zd-mini]');

  /* ① 分区折/展：只切 `.is-closed`（可见性由 CSS 裁决，JS 不写内联 display） */
  var secs = host.querySelectorAll('[data-zd-sec]');
  for (var i = 0; i < secs.length; i++) {
    (function (sec) {
      var t = sec.querySelector('.zd-sec-t');
      if (!t) return;
      t.addEventListener('click', function () {
        var closed = sec.classList.toggle('is-closed');
        t.setAttribute('aria-expanded', closed ? 'false' : 'true');
      });
    })(secs[i]);
  }

  /* ②/③ 面板 ⇄ 胶囊 互斥切换 */
  function toMini() {
    if (!card || !mini) return;
    card.setAttribute('hidden', '');
    mini.removeAttribute('hidden');
  }
  function toCard() {
    if (!card || !mini) return;
    mini.setAttribute('hidden', '');
    card.removeAttribute('hidden');
  }
  var minBtn = card ? card.querySelector('[data-zd-min]') : null;
  if (minBtn) minBtn.addEventListener('click', toMini);
  if (mini) mini.addEventListener('click', toCard);
})();
'''


def main():
    print('=== 1/3  _mods.html ===')
    # ② 去掉 `.td-sum-h` 标题前的图标（4 个分区标题各一枚 ⇒ 4 处）。
    #    正则只在**行内**匹配（不加 DOTALL）：4 枚 svg 都在各自那一行里，删完只剩纯文字标题。
    drop_re(MODS, r'(<h4 class="td-sum-h">)<svg\b[^>]*>.*?</svg>',
            '② 去掉 `.td-sum-h` 标题前的图标', 4, rep=r'\1')
    # ④ 产物卡整体可点：`data-td-art` 从内部按钮上移到整张卡。
    #    `prevShow(btn)` 用的是 `btn.closest('.td-sum-art')`（closest 含自身）⇒ 换成卡片自己照样取值，
    #    点卡内任何位置（含那枚「预览」按钮，靠冒泡）都会触发。
    edit_all(MODS,
             '<div class="td-sum-art"><i class="td-sum-arti">',
             '<div class="td-sum-art" data-td-art="1"><i class="td-sum-arti">',
             '④ 产物卡挂 data-td-art（整卡可点）',
             '<div class="td-sum-art" data-td-art="1"><i class="td-sum-arti">',
             expect=2)
    edit_all(MODS,
             '<button class="td-diff-btn" type="button" data-td-art="1">预览</button>',
             '<button class="td-diff-btn" type="button">预览</button>',
             '④ 内部「预览」按钮卸掉 data（保留视觉与键盘入口）',
             '<button class="td-diff-btn" type="button">预览</button>',
             expect=2)
    # ⑥ 面板静态 DOM
    tail(MODS, 'id="av-zd-status"', PANEL_HTML, '⑥ 任务信息面板静态 DOM')

    print('=== 2/3  panel.css ===')
    # ① `.td-sum-sec` hover 边框加深一级（border-1 = gray-2 #F2F2F2 → border-2 = gray-3 #E5E5E5）
    tail(PCS, '/* r108-l2 */', CSS_NEW, '⑥ 第 19 节（含 ①②③④ 的小改）')
    # ② 标题前的图标删掉后，那条 `svg` 规则成了死代码 ⇒ 一并清掉
    del_once(PCS, '.td-sum-h svg { flex: none; color: var(--color-text-3); }\n',
             '② 清掉 `.td-sum-h svg` 死规则')
    # ③ 图标改正文色 + 尺寸 13px
    edit(PCS,
         '.td-diff-cv { flex: none; color: var(--color-text-3); transition: transform 160ms; }',
         '.td-diff-cv { flex: none; width: 13px; height: 13px; color: var(--color-text-1); '
         'transition: transform 160ms; }',
         '③ `.td-diff-cv` 正文色 + 13px',
         'width: 13px; height: 13px; color: var(--color-text-1);')

    print('=== 3/3  panel.js ===')
    tail(PJS, 'av-zd-status', JS_NEW, '⑥ 面板控制器（折展 / 胶囊 / 搬进 main）')

    print()
    print('应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))


if __name__ == '__main__':
    main()

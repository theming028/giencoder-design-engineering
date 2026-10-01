# -*- coding: utf-8 -*-
"""r108 第十六拍（第五层补丁）—— 邵先生三条：

  ① **产物预览换载体**：`td-sum-art` 卡片点出来的预览，从「覆盖整块摘要的浮层」
     改成「`.td-browse-bar` 里的一个新页签」。
     · 旧载体 = `.td-sum-prev`（`position:absolute; inset:0` 盖在 `.td-mod.td-sum` 上）——
       它自成一套开关（`[hidden]` + 两个自绘按钮），与标签栏状态机各说各话：
       切到别的模块、或把摘要页签关掉，那层浮层还在原地，而 `.td-mod.td-sum` 的
       `position: relative` 只为它一个人存在。
     · 新载体 = `#av-browse-pane-preview`（`data-td-pane="preview"`）—— 开合 / 切换 /
       关闭 / 拖拽重排全部交给标签栏那一套（`openTab` / `activate` / `closeTab`）。
       两套骨架（md / xlsx）与文案填充逻辑**一字未改**，只是换了宿主。
     · 页签名 = 产物文件名，图标 = 产物行那枚 `.td-sum-arti svg`（`openTab` 新增 `opts.ico`
       通道：预览页签没有对应的 `+` 模块菜单项，`src` 恒为 null）。

  ② **面板 ⇄ 胶囊的动效换成「从右上角收进去 / 从右上角摊出来」**。
     · 上一版：`transform-origin` 默认（50% 50%）⇒ 居中微缩 + 上移 6px，看不出与哪个角有关。
     · 这一版：`transform-origin: 100% 0`（= 面板右上角，正是头部那枚「收起为胶囊」按钮
       所在的角）⇒ 缩小时几何体朝该角坍缩、放大时从该角向左下摊开；位移只做**同向补强**
       （`+12px / -12px`，朝右上角再走一点），不做反方向拉拽，否则会读成「向右上飞走」。
     · ⚠ 出场三属性全压到 170ms：`panel.js` 的 `zdSwap()` 在 **180ms** 就摘 `hidden`，
       上一版 `scale/translate` 是 300ms ⇒ 面板在半缩状态下被摘掉，肉眼「跳一下」。

  ③ **`.zd-host` 整个容器改毛玻璃**。
     `.zd-host` 本身是个**定位壳**（`position:absolute` + `display:flex`，无底色、
     `pointer-events:none`）⇒ 视觉上的「容器」是它里面那四件：卡片 `.zd-card`、
     折叠后的胶囊 `.zd-mini`、两枚下拉 `.zd-menu`、轻提示 `.zd-toast`。
     四件一起换才读得出「整块面板是一面玻璃」。底色用 `color-mix` 就地取透（不新增 hex），
     并各自沿用各自的原底色 token（`.zd-menu` / `.zd-toast` 是 `--color-bg-popup`）；
     另给不支持 `backdrop-filter` 的引擎留 `@supports not (...)` 的不透明兜底。

改序（只能下→上，硬规则 22）：
    1. `mg-work/r108/part108/_mods.html`   ① 的 DOM（浮层 → 页签面板）
    2. `mg-work/r108/part108/panel.css`    ① 的样式 + ② 的动效 + ③ 的毛玻璃 + l5 标记
    3. `mg-work/r108/part108/panel.js`     ① 的两处（`openTab` 支持 `opts.ico` / `prevShow` 改开页签）
    4. `python mg-work/r108/ev/splice108.py`  → 重建 `part108/browse.html`（因为 _mods.html 变了）
    5. `python mg-work/r108/apply108.py`      → 落 `pages/conversation.html`

★ 为什么另起一层（l5）而不是就地改 l1~l4：r108 未提交 ⇒ **不另起代数**，但在代内分层。
  ★★ 各层的 `mark` 是「**后一层必须替前一层保住**」的契约：本层把 `/* r108-l5 */` 插在
     `/* r108-l4 */` **之前**、并把 l4 标记**原样接回**；l1~l4 的标记本层一个不碰
     （收尾有跨层兜底断言）。

幂等判据：每处都带 `mark`（**只有改完之后才存在的串**）；三处删除类改动（`.td-mod.td-sum`
          的定位、旧浮层样式、页签里已删的 `data-td-prev-x` / `is-primary` 消费者）
          一并折进各自 `old` 的整块替换里 ⇒ 复跑时 `old` 不再命中、靠 `mark` 判「已应用」。
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
# ★ 打开「mark 歧义」硬断言（本层除末尾那条「插在锚点前 + 接回锚点」外，mark 都是独有串）
STRICT = True


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    return raw.replace('\r\n', '\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace('\n', nl).encode('utf-8'))


def edit(p, old, new, label, mark, strict=None):
    t, nl = rd(p)
    strict = STRICT if strict is None else strict
    if mark and mark in t:
        # ★★ 「mark 歧义」硬断言：`mark` 的语义是**只有改完才存在**。
        #    若 `old` 与 `mark` **同时**出现在同一份文件里，只可能是 mark 选得不唯一
        #    （r108 第十五拍真踩：mark 与上文某条声明逐字相同 ⇒ 首跑被误判成「已应用」
        #     而**静默跳过**整条改动，末行还照样打印「应用 N 项」）。
        #    ⚠ 合法例外：末尾那条「插在 `/* r108-l4 */` 之前、并把该标记原样接回」的写入
        #      —— 锚点**必须**留下来（否则 l4 复跑找不到它）⇒ 该步骤显式传 `strict=False`。
        if strict and old in t:
            sys.exit('!! %s：mark 歧义 —— `old` 与 `mark` 同时存在 ⇒ mark 不是「改完才出现」的串\n'
                     '   mark=%r\n   old=%r' % (label, mark, old[:160]))
        SKIPPED.append(label)
        print('   跳过  %s（已应用）' % label)
        return
    n = t.count(old)
    if n != 1:
        sys.exit('!! %s：锚点命中 %d 次（应 1 次）\n   old=%r' % (label, n, old[:220]))
    wr(p, t.replace(old, new, 1), nl)
    APPLIED.append(label)
    print('   应用  %s（%d → %d 字符）' % (label, len(t), len(t) - len(old) + len(new)))


# ================================================================================
# 共用片段：产物行那枚「文档」图标（页签与面板头用它，与 `.td-sum-arti` 同字形）
# ================================================================================
ICO_DOC = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" '
           'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
           'stroke-linejoin="round" aria-hidden="true">'
           '<path d="M4 2h11.5l3.5 5.5v13a1.5 1.5 0 0 1-1.5 1.5H4a1.5 1.5 0 0 1-1.5-1.5v-17A1.5 1.5 0 0 1 4 2Z"/>'
           '<path d="M7.5 9.5h6.5"/><path d="M6.5 13h3.5"/></svg>')

# ================================================================================
# ① _mods.html：旧浮层（`.td-sum-prev`）→ 新的「预览」页签面板
#   ⚠ 锚点是「浮层整块 + 摘要 section 的收尾 `</section>`」⇒ 一次替换同时完成
#     「删旧载体」与「在摘要之后挂新面板」，不会出现中间态。
# ================================================================================
MODS_OLD = (
    '      <!-- ★ 第十一拍 ④（r107-l2）：产物预览层（对照官方「产物查看器」）。\n'
    '           点摘要「产物」里的「预览」打开；绝对定位覆盖整块摘要、不参与文档流。\n'
    '           两套骨架（文档 / 表格）由 `data-td-prev-kind` 切，JS 只做显示切换与文案填充。 -->\n'
    '      <div class="td-sum-prev" data-td-prev="1" hidden>\n'
    '        <div class="td-sum-prev-h">\n'
    '          <i class="td-sum-arti" data-td-prev-ico="1">' + ICO_DOC + '</i>\n'
    '          <span class="td-sum-prev-t">\n'
    '            <b data-td-prev-name="1">产物</b>\n'
    '            <i data-td-prev-meta="1">—</i>\n'
    '          </span>\n'
    '          <button class="td-browse-ico" type="button" aria-label="关闭预览" title="关闭预览" data-td-prev-x="1"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg></button>\n'
    '        </div>\n'
    '        <div class="td-sum-prev-b">\n'
    '          <div class="td-pv-md" data-td-prev-kind="md">\n'
    '            <div class="td-pv-h1">右栏复刻方案</div>\n'
    '            <div class="td-pv-p">把会话详情页右栏升级为标签式 Side Panel：模块可多开、切换、关闭与拖拽重排，并补齐审查 / 终端 / 浏览器 / 摘要四个面板。</div>\n'
    '            <div class="td-pv-h2">一、体位</div>\n'
    '            <span class="td-pv-bar"></span>\n'
    '            <span class="td-pv-bar is-w80"></span>\n'
    '            <span class="td-pv-bar is-w60"></span>\n'
    '            <div class="td-pv-h2">二、缺口与补齐</div>\n'
    '            <span class="td-pv-bar"></span>\n'
    '            <span class="td-pv-bar is-w40"></span>\n'
    '          </div>\n'
    '          <div class="td-pv-sheet" data-td-prev-kind="xlsx" hidden>\n'
    '            <div class="td-pv-row"><span class="td-pv-cell is-head">模块</span><span class="td-pv-cell is-head">宽 (px)</span><span class="td-pv-cell is-head">占比</span><span class="td-pv-cell is-head">状态</span></div>\n'
    '            <div class="td-pv-row"><span class="td-pv-cell">文件</span><span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span><span class="td-pv-cell">已交付</span></div>\n'
    '            <div class="td-pv-row"><span class="td-pv-cell">审查</span><span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span><span class="td-pv-cell">本轮新增</span></div>\n'
    '            <div class="td-pv-row"><span class="td-pv-cell">终端</span><span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span><span class="td-pv-cell">本轮新增</span></div>\n'
    '            <div class="td-pv-row"><span class="td-pv-cell">浏览器</span><span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span><span class="td-pv-cell">本轮新增</span></div>\n'
    '            <div class="td-pv-row"><span class="td-pv-cell">摘要</span><span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span><span class="td-pv-cell">默认页签</span></div>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="td-sum-prev-f">\n'
    '          <button class="td-prev-btn" type="button" data-td-prev-open="1">在系统打开</button>\n'
    '          <button class="td-prev-btn is-primary" type="button" data-td-prev-close="1">关闭</button>\n'
    '        </div>\n'
    '      </div>\n'
    '    </section>\n'
)
MODS_NEW = (
    '    </section>\n'
    '\n'
    '    <!-- ★ 第十六拍 ①：产物预览改挂**右栏自己的一个页签**（不再覆盖摘要的浮层）。\n'
    '         载体换成 `[data-td-pane="preview"]` ⇒ 开关 / 切换 / 关闭 / 拖拽重排全部交给\n'
    '         标签栏那套状态机（`openTab` / `activate` / `closeTab`），不再自成一套开关。\n'
    '         两套骨架（md / xlsx）由 `data-td-prev-kind` 切，JS 只做显示切换与文案填充。\n'
    '         ⚠ 标题行刻意**单行并排**（`<b>` 与 `<span>` 不同行），不叠两行 —— 详见\n'
    '           panel.css 18-③ 那段注释（叠两行会把工具条从 40px 撑到 ~51px）。 -->\n'
    '    <section class="td-mod td-pv" id="av-browse-pane-preview" data-td-pane="preview" role="tabpanel" aria-label="产物预览" hidden>\n'
    '      <div class="td-mod-bar">\n'
    '        <i class="td-sum-arti" data-td-prev-ico="1">' + ICO_DOC + '</i>\n'
    '        <b class="td-pv-name" data-td-prev-name="1">产物</b>\n'
    '        <span class="td-pv-hint" data-td-prev-meta="1">—</span>\n'
    '        <div class="td-mod-bar-acts">\n'
    '          <button class="td-prev-btn" type="button" data-td-prev-open="1">在系统打开</button>\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="td-mod-body td-pv-body">\n'
    '        <div class="td-pv-md" data-td-prev-kind="md">\n'
    '          <div class="td-pv-h1">右栏复刻方案</div>\n'
    '          <div class="td-pv-p">把会话详情页右栏升级为标签式 Side Panel：模块可多开、切换、关闭与拖拽重排，并补齐审查 / 终端 / 浏览器 / 摘要四个面板。</div>\n'
    '          <div class="td-pv-h2">一、体位</div>\n'
    '          <span class="td-pv-bar"></span>\n'
    '          <span class="td-pv-bar is-w80"></span>\n'
    '          <span class="td-pv-bar is-w60"></span>\n'
    '          <div class="td-pv-h2">二、缺口与补齐</div>\n'
    '          <span class="td-pv-bar"></span>\n'
    '          <span class="td-pv-bar is-w40"></span>\n'
    '        </div>\n'
    '        <div class="td-pv-sheet" data-td-prev-kind="xlsx" hidden>\n'
    '          <div class="td-pv-row"><span class="td-pv-cell is-head">模块</span><span class="td-pv-cell is-head">宽 (px)</span><span class="td-pv-cell is-head">占比</span><span class="td-pv-cell is-head">状态</span></div>\n'
    '          <div class="td-pv-row"><span class="td-pv-cell">文件</span><span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span><span class="td-pv-cell">已交付</span></div>\n'
    '          <div class="td-pv-row"><span class="td-pv-cell">审查</span><span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span><span class="td-pv-cell">本轮新增</span></div>\n'
    '          <div class="td-pv-row"><span class="td-pv-cell">终端</span><span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span><span class="td-pv-cell">本轮新增</span></div>\n'
    '          <div class="td-pv-row"><span class="td-pv-cell">浏览器</span><span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span><span class="td-pv-cell">本轮新增</span></div>\n'
    '          <div class="td-pv-row"><span class="td-pv-cell">摘要</span><span class="td-pv-cell">641</span><span class="td-pv-cell">44.5%</span><span class="td-pv-cell">默认页签</span></div>\n'
    '        </div>\n'
    '      </div>\n'
    '    </section>\n'
)
MODS_MARK = 'id="av-browse-pane-preview"'

# ================================================================================
# ① panel.css：旧浮层的样式 → 页签版的样式
#   ⚠ 一次替换同时做完：删 `.td-mod.td-sum{position:relative}`（只为浮层存在）、
#     删 `.td-sum-prev*` 全套 + `.td-prev-btn.is-primary*`（页签里没有主色按钮了）、
#     `.td-sum-prev-b` → `.td-pv-body`（配合通用 `.td-mod-body`）、新增页签标题行两条。
# ================================================================================
PREV_OLD = (
    '/* 18-③ 产物预览层（覆盖整块摘要；`.td-mod.td-sum` 当包含块 ⇒ 不参与文档流、不撑高） */\n'
    '.td-mod.td-sum { position: relative; }\n'
    '.td-sum-prev {\n'
    '  position: absolute; inset: 0; z-index: 6;\n'
    '  display: flex; flex-direction: column;\n'
    '  background: var(--color-bg-2);\n'
    '}\n'
    '.td-sum-prev[hidden] { display: none; }\n'
    '.td-sum-prev-h {\n'
    '  flex: none; box-sizing: border-box;\n'
    '  display: flex; align-items: center; gap: 8px;\n'
    '  min-height: calc(40px * var(--ui-fs-ratio)); padding: 6px 12px;\n'
    '  border-bottom: 1px solid var(--color-border-1);\n'
    '  font-size: var(--font-size-body-1);\n'
    '}\n'
    '.td-sum-prev-t { flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; }\n'
    '.td-sum-prev-t b {\n'
    '  font-size: var(--font-size-body-3); font-weight: 500; color: var(--color-text-1);\n'
    '  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;\n'
    '}\n'
    '.td-sum-prev-t i { font-style: normal; font-size: var(--font-size-body-1); color: var(--color-text-3); }\n'
    '.td-sum-prev-b { flex: 1 1 auto; min-height: 0; overflow: auto; padding: 14px 16px; }\n'
    '.td-sum-prev-f {\n'
    '  flex: none; box-sizing: border-box;\n'
    '  display: flex; align-items: center; justify-content: flex-end; gap: 8px;\n'
    '  min-height: calc(48px * var(--ui-fs-ratio)); padding: 8px 12px;\n'
    '  border-top: 1px solid var(--color-border-1);\n'
    '  font-size: var(--font-size-body-1);\n'
    '}\n'
    '.td-prev-btn {\n'
    '  flex: none; height: calc(28px * var(--ui-fs-ratio)); padding: 0 14px;\n'
    '  border: 1px solid var(--color-border-2); border-radius: 6px;\n'
    '  background: transparent; color: var(--color-text-1);\n'
    '  font-family: inherit; font-size: var(--font-size-body-2); cursor: pointer;\n'
    '  transition: background-color 120ms, border-color 120ms;\n'
    '}\n'
    '.td-prev-btn:hover { background: var(--color-fill-1); border-color: var(--color-border-3); }\n'
    '.td-prev-btn.is-primary {\n'
    '  border-color: transparent; background: var(--color-primary-6); color: var(--color-white);\n'
    '}\n'
    '.td-prev-btn.is-primary:hover { background: var(--color-primary-5); }\n'
)
PREV_NEW = (
    '/* 18-③ 产物预览（★ 第十六拍 ①：从「覆盖整块摘要的浮层」改为**右栏自己的一个页签**）。\n'
    '   ⚠ 载体换了、尺码不变：下面两套骨架（`.td-pv-md` / `.td-pv-sheet`）与 `.td-prev-btn`\n'
    '     原样复用；这里只保留「页签版标题行」特有的三条（文件名 / 元信息 / 正文内距）。\n'
    '   ⚠ 标题行必须**单行并排**（`b` 与 `span` 不同行）：`.td-mod-bar` 是 `min-height: 40px`\n'
    '     + `padding: 6px 12px` ⇒ 内容盒只有 28px；叠两行会把它撑到 ~51px，与「审查 / 终端 /\n'
    '     浏览器 / 摘要」那四条工具条对不齐（旧浮层就是这么高的 —— 它不是 `.td-mod-bar`）。\n'
    '   ⚠ 上一版给 `.td-mod.td-sum` 挂的 `position: relative` 已随浮层一起删掉：它是那层的\n'
    '     包含块，浮层没了它就是一条没有任何消费者的死规则。 */\n'
    '.td-pv-name {\n'
    '  flex: none; max-width: 62%;\n'
    '  font-size: var(--font-size-body-3); font-weight: 500; color: var(--color-text-1);\n'
    '  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;\n'
    '}\n'
    '.td-pv-hint {\n'
    '  flex: 1 1 auto; min-width: 0;\n'
    '  font-size: var(--font-size-body-1); color: var(--color-text-3);\n'
    '  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;\n'
    '}\n'
    '/* `.td-mod-body` 自带 `overflow: auto`，内距是本模块自己的事（沿用旧浮层那份 14/16） */\n'
    '.td-pv-body { padding: 14px 16px; }\n'
    '.td-prev-btn {\n'
    '  flex: none; height: calc(28px * var(--ui-fs-ratio)); padding: 0 14px;\n'
    '  border: 1px solid var(--color-border-2); border-radius: 6px;\n'
    '  background: transparent; color: var(--color-text-1);\n'
    '  font-family: inherit; font-size: var(--font-size-body-2); cursor: pointer;\n'
    '  transition: background-color 120ms, border-color 120ms;\n'
    '}\n'
    '.td-prev-btn:hover { background: var(--color-fill-1); border-color: var(--color-border-3); }\n'
)
PREV_MARK = '.td-pv-hint {'

# ================================================================================
# ① panel.css（续）：工具条高度的 1px 对齐
#   ★★ 首轮真机实测逮到：预览工具条 **41px**，而「摘要」工具条 **40px**（`bars` 相位）。
#      算式：`.td-mod-bar` = `min-height: 40px` + `padding: 6px 12px` + `border-bottom: 1px`
#      ⇒ 内容盒上限 = 40 − 6 − 6 − 1 = **27px**；而 `.td-sum-arti`（图标砖）是 28×28、
#        `.td-prev-btn` 原来也是 28 ⇒ 谁都能把它顶成 41。
#      ⇒ 本模块内两件各收到 26px（`.td-sum-arti` 只在**本模块**收，产物行那两个保持 28）。
#      ⚠ 图标砖写成裸 `26px`（不跟 `--ui-fs`）：它与按钮同高才对齐，而按钮是
#        `calc(26px * ratio)`；字号杠杆拉大时两者都**不会**超过 `.td-mod-bar` 自己的
#        `min-height × ratio`，所以条高仍与其余四条一致（fs18 实测两条都是 51.43px）。
# ================================================================================
BARH_OLD = (
    '.td-prev-btn {\n'
    '  flex: none; height: calc(28px * var(--ui-fs-ratio)); padding: 0 14px;\n'
)
BARH_NEW = (
    '/* ⚠ 工具条高度必须与「审查 / 终端 / 浏览器 / 摘要」四条**逐像素对齐**（都是 40px）：\n'
    '   `.td-mod-bar` = `min-height: 40px` + `padding: 6px 12px` + `border-bottom: 1px`\n'
    '   ⇒ 内容盒上限 = 40 − 6 − 6 − 1 = **27px**。28px 的图标砖与 28px 的按钮都会把它顶成\n'
    '   41px（首轮实测 41 ⇄ 40，差 1px）⇒ 本模块内两件各收到 26px。\n'
    '   ⚠ 图标砖只在本模块收（`.td-pv` 作用域）：产物行那两个 `.td-sum-arti` 保持 28px。 */\n'
    '.td-pv .td-sum-arti { width: 26px; height: 26px; }\n'
    '.td-pv .td-sum-arti svg { width: 14px; height: 14px; }\n'
    '.td-prev-btn {\n'
    '  flex: none; height: calc(26px * var(--ui-fs-ratio)); padding: 0 14px;\n'
)
BARH_MARK = '.td-pv .td-sum-arti { width: 26px; height: 26px; }'

# ================================================================================
# ② panel.css：面板 ⇄ 胶囊 —— 锚点钉在**右上角**
# ================================================================================
ANIM_OLD = (
    '/* ④ 面板 ⇄ 胶囊：出场（快速淡出 + 微缩）/ 入场（spring 回弹）。\n'
    '   两边都常驻文档流、只有 `hidden` 那一刻才摘 ⇒ 过渡看得见（摘除时机由 panel.js 掐）。 */\n'
    '.zd-card, .zd-mini {\n'
    '  transition: opacity 170ms ease,\n'
    '              scale 300ms var(--transition-timing-function-spring),\n'
    '              translate 300ms var(--transition-timing-function-spring);\n'
    '}\n'
    '.zd-card.is-zd-out, .zd-mini.is-zd-out {\n'
    '  opacity: 0; scale: 0.94; translate: 0 -6px; pointer-events: none;\n'
    '}\n'
    '@keyframes zd-panel-in {\n'
    '  from { opacity: 0; scale: 0.94; translate: 0 -6px; }\n'
    '  to   { opacity: 1; scale: 1;    translate: 0 0; }\n'
    '}\n'
    '.zd-card.is-zd-in, .zd-mini.is-zd-in {\n'
    '  animation: zd-panel-in 300ms var(--transition-timing-function-spring) both;\n'
    '}\n'
)
ANIM_NEW = (
    '/* ④ 面板 ⇄ 胶囊（★ 第十六拍 ②：**从右上角收进去 / 从右上角摊出来**）。\n'
    '   上一版的 `transform-origin` 是默认的 50% 50% ⇒ 居中微缩 + 上移 6px，看不出跟哪个角\n'
    '   有关。这一版把锚点钉在 `100% 0` —— **面板右上角**，正是头部那枚「收起为胶囊」按钮\n'
    '   所在的那个角 ⇒ 缩小时几何体朝该角坍缩、放大时从该角向左下摊开，与按钮的空间关系自洽。\n'
    '   ⚠ 位移只做**同向补强**（`+12px / -12px`，朝右上角再走一点）：反方向拉拽会读成\n'
    '     「向右上飞走」，而不是「收进右上角」。12px 也刻意小于 `.zd-host` 到视口右缘的 16px\n'
    '     ⇒ 全程不出画面。\n'
    '   ⚠ 出场三属性全压到 170ms：`panel.js` 的 `zdSwap()` 在 **180ms** 就摘 `hidden`，\n'
    '     上一版 `scale/translate` 是 300ms ⇒ 面板在半缩状态下被摘掉，肉眼「跳一下」。\n'
    '   ⚠ 入场走关键帧（`animation`）而不是过渡：`hidden` 是**硬开关**，元素从 `display:none`\n'
    '     回到可见的那一刻过渡不会播，只有关键帧会。 */\n'
    '.zd-card, .zd-mini {\n'
    '  transform-origin: 100% 0;\n'
    '  transition: opacity 160ms ease,\n'
    '              scale 170ms cubic-bezier(0.4, 0, 1, 1),\n'
    '              translate 170ms cubic-bezier(0.4, 0, 1, 1);\n'
    '}\n'
    '.zd-card.is-zd-out, .zd-mini.is-zd-out {\n'
    '  opacity: 0; scale: 0.62; translate: 12px -12px; pointer-events: none;\n'
    '}\n'
    '@keyframes zd-panel-in {\n'
    '  from { opacity: 0; scale: 0.62; translate: 12px -12px; }\n'
    '  to   { opacity: 1; scale: 1;    translate: 0 0; }\n'
    '}\n'
    '.zd-card.is-zd-in, .zd-mini.is-zd-in {\n'
    '  animation: zd-panel-in 260ms var(--transition-timing-function-spring) both;\n'
    '}\n'
)
ANIM_MARK = 'translate: 12px -12px'

# ================================================================================
# ③ panel.css：毛玻璃（追加在文件尾 —— 必须晚于 `.zd-toast`(19.3) 与四枚弹层骨架(第 1 节)，
#    否则同特异性下会被它们各自那条 `background` 压回去）
# ================================================================================
GLASS = (
    '/* ---------------------------------------------------------------- 19.5 第十六拍 ③ */\n'
    '/* ③ 「整个容器」= 毛玻璃表面。\n'
    '   `.zd-host` 自己只是个 `position: absolute` + `display: flex` 的**定位壳**：没有底色、\n'
    '   `pointer-events: none`、宽高全由内容撑 ⇒ 视觉上的「容器」其实是它里面那四件：\n'
    '   卡片 `.zd-card` / 折叠后的胶囊 `.zd-mini` / 两枚下拉 `.zd-menu` / 轻提示 `.zd-toast`。\n'
    '   四件一起换，才读得出「整块面板是一面玻璃」；只改卡片会出现「卡片是玻璃、\n'
    '   菜单是实心白」的割裂。\n'
    '   ⚠ 要「模糊背景」，底色就必须**半透明**：用 `color-mix` 就地取透（不新增 hex，硬规则 5）——\n'
    '     亮色 = 78% 白、暗色沿用 `--color-bg-2` 的深灰 ⇒ 一个 token 覆盖两套主题，不必另写暗色块。\n'
    '   ⚠ `backdrop-filter` 模糊的是**本件背后那一层**（卡片背后 = 对话正文；菜单背后 = 卡片 + 正文）\n'
    '     ⇒ 面板浮在内容之上时才出「磨砂」感，正是要的效果。\n'
    '   ⚠ 四件各自沿用**各自的原底色 token**（`.zd-menu` / `.zd-toast` 原本是 `--color-bg-popup`）\n'
    '     —— 一律换成 `--color-bg-2` 会让暗色下的弹层比面板白一档。 */\n'
    '.zd-card, .zd-mini, .zd-toast {\n'
    '  background: color-mix(in srgb, var(--color-bg-2) 78%, transparent);\n'
    '}\n'
    '.zd-menu.giencoder-dropdown-popup {\n'
    '  background: color-mix(in srgb, var(--color-bg-popup) 82%, transparent);\n'
    '}\n'
    '.zd-card, .zd-mini, .zd-menu.giencoder-dropdown-popup, .zd-toast {\n'
    '  -webkit-backdrop-filter: blur(18px) saturate(160%);\n'
    '  backdrop-filter: blur(18px) saturate(160%);\n'
    '}\n'
    '/* 引擎不支持 `backdrop-filter`（或系统关掉了「透明效果」）⇒ 退回不透明 token 底，\n'
    '   否则 78% 的半透明会让正文糊在一起。`or` 一并覆盖两种前缀写法。 */\n'
    '@supports not ((-webkit-backdrop-filter: blur(2px)) or (backdrop-filter: blur(2px))) {\n'
    '  .zd-card, .zd-mini, .zd-toast {\n'
    '    background: var(--color-bg-2);\n'
    '  }\n'
    '  .zd-menu.giencoder-dropdown-popup {\n'
    '    background: var(--color-bg-popup);\n'
    '  }\n'
    '}\n'
)
GLASS_MARK = '/* r108-l5 */'
TAIL_OLD = '/* r108-l4 */\n'
TAIL_NEW = GLASS + '/* r108-l5 */\n/* r108-l4 */\n'

# ================================================================================
# ① panel.js （a）`openTab` 支持 `opts.ico`
# ================================================================================
OPENTAB_OLD = (
    "    var mi = src && src.querySelector('.td-mm-ico');\n"
    '    if (mi) ico.innerHTML = mi.innerHTML;\n'
)
OPENTAB_NEW = (
    "    var mi = src && src.querySelector('.td-mm-ico');\n"
    '    /* ★ 第十六拍 ①：`opts.ico`（一段 svg 字符串）优先 —— 「产物预览」这个页签没有\n'
    '       对应的 `+` 模块菜单项（`src` 恒为 null），图标只能由调用方给（取自产物行\n'
    '       自己的 `.td-sum-arti svg`）。 */\n'
    "    if (opts && opts.ico) ico.innerHTML = opts.ico;\n"
    '    else if (mi) ico.innerHTML = mi.innerHTML;\n'
)
OPENTAB_MARK = "    if (opts && opts.ico) ico.innerHTML = opts.ico;"

# ================================================================================
# ① panel.js （a2）`openTab` 命中已有页签时**同步页签名与图标**
#   ★★ 首轮真机 + 截图逮到：连点两个产物时，`openTab` 走「已存在 ⇒ 直接 activate」
#      分支就 `return` 了，**不更新 `nm` / `ico`** ⇒ 出现「页签写着 `右栏复刻方案.md`、
#      正文已经是 `sidepanel-metrics.xlsx` 的表格」这种自相矛盾的画面（探针 `pvB` 的
#      `tabs[].name` 与 `prev.name` 对不上，截图同样能肉眼看出）。
#      其余调用方（`+` 菜单 / 右键菜单）**都不传 `opts`** ⇒ 加了 `if (opts)` 守卫后
#      对它们完全无影响（不会把「文件 / 审查 / 终端」的页签名改掉）。
# ================================================================================
REUSE_OLD = '    if (ex) { activate(mod); ensureOpen(); return ex; }\n'
REUSE_NEW = (
    '    if (ex) {\n'
    '      /* ★ 第十六拍 ①：**复用已有页签时要同步页签名与图标**。产物预览是「同一枚页签\n'
    '         承载多个文件」（连点两个产物只更新内容），不同步就会出现「页签写着 .md、\n'
    '         正文是 .xlsx 表格」的自相矛盾。\n'
    '         ⚠ 只在本调用方给了 `opts` 时才改：`+` 菜单 / 右键菜单那几处不传 `opts`\n'
    '           ⇒ 不会误改「文件 / 审查 / 终端 / 浏览器」的页签名。 */\n'
    '      if (opts) {\n'
    "        var nmx = ex.querySelector('.td-tab-name');\n"
    '        if (nmx && opts.name) nmx.textContent = opts.name;\n'
    "        var icx = ex.querySelector('.td-tab-ico');\n"
    '        if (icx && opts.ico) icx.innerHTML = opts.ico;\n'
    "        var xx = ex.querySelector('[data-td-tab-x]');\n"
    "        if (xx && opts.name) xx.setAttribute('aria-label', '关闭「' + opts.name + '」标签');\n"
    '      }\n'
    '      activate(mod); ensureOpen(); return ex;\n'
    '    }\n'
)
REUSE_MARK = 'if (opts) {\n        var nmx = ex.querySelector'

# ================================================================================
# ① panel.js （b）`prevShow` 改为「填内容 → openTab('preview')」
# ================================================================================
PREVJS_OLD = (
    '  /* ★ 第十一拍 ④（r107-l2）：产物预览层 —— 对照官方「产物查看器」。\n'
    '     原来「预览」只弹一句 toast、没有任何视觉，属于真缺口；现在打开一层覆盖整块摘要的\n'
    '     只读预览（文件名 + 元信息 + 骨架：文档 / 表格两套），并给「在系统打开」「关闭」。 */\n'
    "  var prevEl = pane.querySelector('[data-td-prev]');\n"
    "  function prevHide() { if (prevEl) prevEl.setAttribute('hidden', ''); }\n"
    '  function prevShow(btn) {\n'
    '    if (!prevEl) return;\n'
    "    var host = btn && btn.closest ? btn.closest('.td-sum-art') : null;\n"
    "    var nmEl = host && host.querySelector('.td-sum-artt b');\n"
    "    var mtEl = host && host.querySelector('.td-sum-artt i');\n"
    "    var ico = host && host.querySelector('.td-sum-arti svg');\n"
    "    var name = nmEl ? nmEl.textContent : '产物';\n"
    "    var kind = (/\\.(xlsx|xls|csv|tsv)$/i).test(name) ? 'xlsx' : 'md';\n"
    "    var pn = prevEl.querySelector('[data-td-prev-name]');\n"
    "    var pm = prevEl.querySelector('[data-td-prev-meta]');\n"
    "    var pi = prevEl.querySelector('[data-td-prev-ico]');\n"
    '    if (pn) pn.textContent = name;\n'
    "    if (pm) pm.textContent = (mtEl ? mtEl.textContent : '') + ' · 只读预览';\n"
    '    if (pi && ico) pi.innerHTML = ico.outerHTML;\n'
    "    var bodies = prevEl.querySelectorAll('[data-td-prev-kind]');\n"
    '    for (var q = 0; q < bodies.length; q++) {\n'
    "      if (bodies[q].getAttribute('data-td-prev-kind') === kind) bodies[q].removeAttribute('hidden');\n"
    "      else bodies[q].setAttribute('hidden', '');\n"
    '    }\n'
    "    prevEl.removeAttribute('hidden');\n"
    '  }\n'
    "  var artBtns = pane.querySelectorAll('[data-td-art]');\n"
    '  for (var ar = 0; ar < artBtns.length; ar++) {\n'
    '    (function (b) {\n'
    "      b.addEventListener('click', function () { prevShow(b); });\n"
    '    })(artBtns[ar]);\n'
    '  }\n'
    '  if (prevEl) {\n'
    "    var prevXs = prevEl.querySelectorAll('[data-td-prev-x], [data-td-prev-close]');\n"
    '    for (var px = 0; px < prevXs.length; px++) prevXs[px].addEventListener(\'click\', prevHide);\n'
    "    var prevOpenBtn = prevEl.querySelector('[data-td-prev-open]');\n"
    '    if (prevOpenBtn) {\n'
    "      prevOpenBtn.addEventListener('click', function () { say('已在系统应用中打开（视觉演示）'); });\n"
    '    }\n'
    '  }\n'
)
PREVJS_NEW = (
    '  /* ★ 第十六拍 ①：产物预览从「覆盖整块摘要的浮层」改为**右栏自己的一个页签**。\n'
    '     上一版是 `.td-sum-prev`（`position: absolute; inset: 0` 盖住 `.td-mod.td-sum`）——\n'
    '     那种载体自带一套开关，跟标签栏状态机各说各话：切到别的模块、或把摘要页签关掉，\n'
    '     它还在原地（而 `.td-mod.td-sum { position: relative }` 只为它一个人存在）。\n'
    '     这一版把预览做成 `#av-browse-pane-preview`（`data-td-pane="preview"`）：\n'
    '     开关 / 切换 / 关闭 / 拖拽重排全部由标签栏那一套（`openTab` / `activate` /\n'
    '     `closeTab`）裁决。两套骨架（md / xlsx）与文案填充逻辑**一字未改**，只换了宿主。\n'
    '     ⚠ 「同一枚预览页签复用」：连点两个产物不会开出两枚标签，第二个只更新页签名与\n'
    '       正文（`openTab` 命中同名 `mod` 时走 `activate` 分支，与「文件 / 审查 …」同口径）。 */\n'
    "  var prevPane = pane.querySelector('#av-browse-pane-preview');\n"
    '  function prevShow(btn) {\n'
    '    if (!prevPane) return;\n'
    "    var host = btn && btn.closest ? btn.closest('.td-sum-art') : null;\n"
    "    var nmEl = host && host.querySelector('.td-sum-artt b');\n"
    "    var mtEl = host && host.querySelector('.td-sum-artt i');\n"
    "    var ico = host && host.querySelector('.td-sum-arti svg');\n"
    "    var name = nmEl ? nmEl.textContent : '产物';\n"
    "    var kind = (/\\.(xlsx|xls|csv|tsv)$/i).test(name) ? 'xlsx' : 'md';\n"
    "    var pn = prevPane.querySelector('[data-td-prev-name]');\n"
    "    var pm = prevPane.querySelector('[data-td-prev-meta]');\n"
    "    var pi = prevPane.querySelector('[data-td-prev-ico]');\n"
    '    if (pn) pn.textContent = name;\n'
    "    if (pm) pm.textContent = (mtEl ? mtEl.textContent : '') + ' · 只读预览';\n"
    '    if (pi && ico) pi.innerHTML = ico.outerHTML;\n'
    "    var bodies = prevPane.querySelectorAll('[data-td-prev-kind]');\n"
    '    for (var q = 0; q < bodies.length; q++) {\n'
    "      if (bodies[q].getAttribute('data-td-prev-kind') === kind) bodies[q].removeAttribute('hidden');\n"
    "      else bodies[q].setAttribute('hidden', '');\n"
    '    }\n'
    '    /* ⚠ 顺序：**先把内容填好再 `openTab`** —— 后者会 `activate()` 让面板显形，\n'
    '       反过来的话会闪一帧「旧文件名 / 旧骨架」。 */\n'
    "    openTab('preview', { name: name, ico: ico ? ico.outerHTML : '' });\n"
    '  }\n'
    "  var artBtns = pane.querySelectorAll('[data-td-art]');\n"
    '  for (var ar = 0; ar < artBtns.length; ar++) {\n'
    '    (function (b) {\n'
    "      b.addEventListener('click', function () { prevShow(b); });\n"
    '    })(artBtns[ar]);\n'
    '  }\n'
    '  /* 面板工具条上的「在系统打开」—— 关闭改由页签自己的 `×`（`closeTab` 那段现有逻辑） */\n'
    '  if (prevPane) {\n'
    "    var prevOpenBtn = prevPane.querySelector('[data-td-prev-open]');\n"
    "    if (prevOpenBtn) prevOpenBtn.addEventListener('click', function () { say('已在系统应用中打开（视觉演示）'); });\n"
    '  }\n'
)
PREVJS_MARK = "openTab('preview', { name: name, ico: ico ? ico.outerHTML : '' });"

# ================================================================================
# ① panel.js （c）Esc 裁决：预览**不再占一层**
#   ★★ 这一步是本层的「真 bug 修复」，跨层自检逮到的：`prevEl` / `prevHide` 由摘要模块那段
#      定义，却被**下面**的 Esc 裁决（第 12xx 行）引用 —— 只删定义不删引用，
#      按一次 Esc 就会在 window 捕获段抛 `ReferenceError`（整条侧栏的 Esc 也随之失效）。
#      预览既已是页签（与审查 / 终端 / 浏览器 / 摘要同级），就不该再占 Esc 的一层。
# ================================================================================
ESCOWN_OLD = (
    '    /* ★ 第十一拍 ④（r107-l2）：产物预览层也占一层（不接进来的话，开着预览按 Esc 会\n'
    '       直接把**整条侧栏**关掉 —— 那是 ctrl-conv.js 的 Esc 在处理）。 */\n'
    "    var prevOpen = prevEl && !prevEl.hasAttribute('hidden');\n"
)
ESCOWN_NEW = (
    '    /* ★ 第十六拍 ①：产物预览**不再占一层** —— 它已经是右栏的一个页签（`data-td-pane`），\n'
    '       与「审查 / 终端 / 浏览器 / 摘要」同级，Esc 一律落到 ctrl-conv 那条（关整条侧栏）。\n'
    '       ⚠ 上一版这里是 `var prevOpen = prevEl && ...`：浮层删掉后 `prevEl` 就成了解析不到\n'
    '         的标识符 ⇒ 按一次 Esc 直接抛 `ReferenceError`（本层跨层自检逮到）。 */\n'
)
ESCOWN_MARK = '产物预览**不再占一层**'

ESCCHAIN_OLD = (
    '    if (!modal && !menuOpen && !noteOpen && !selOpen && !prevOpen && !treeOpen) return;\n'
    '    e.preventDefault();\n'
    '    e.stopPropagation();\n'
    '    if (selOpen) { selHide(); return; }\n'
    "    if (modal) { commitModal.setAttribute('hidden', ''); return; }\n"
    '    if (treeOpen) { treeHide(); return; }\n'
    '    if (menuOpen) { closeMenus(null); return; }\n'
    "    if (noteOpen) { elnote.setAttribute('hidden', ''); return; }\n"
    '    if (prevOpen) prevHide();\n'
)
ESCCHAIN_NEW = (
    '    if (!modal && !menuOpen && !noteOpen && !selOpen && !treeOpen) return;\n'
    '    e.preventDefault();\n'
    '    e.stopPropagation();\n'
    '    if (selOpen) { selHide(); return; }\n'
    "    if (modal) { commitModal.setAttribute('hidden', ''); return; }\n"
    '    if (treeOpen) { treeHide(); return; }\n'
    '    if (menuOpen) { closeMenus(null); return; }\n'
    "    if (noteOpen) { elnote.setAttribute('hidden', ''); return; }\n"
    '    /* ★ 第十六拍 ①：原 `if (prevOpen) prevHide();` 已随浮层一并删掉 —— 预览成了页签，\n'
    '       这一层不再有它的活儿；继续往下走 = ctrl-conv 关整条侧栏，正是模块页签该有的行为。 */\n'
)
ESCCHAIN_MARK = '原 `if (prevOpen) prevHide();` 已随浮层一并删掉'


def main():
    print('=== 1/4  _mods.html ===')
    edit(MODS, MODS_OLD, MODS_NEW, '① 浮层 → 预览页签面板', MODS_MARK)

    print('=== 2/4  panel.css ===')
    edit(PCS, PREV_OLD, PREV_NEW, '① 预览层样式 → 页签版', PREV_MARK)
    edit(PCS, BARH_OLD, BARH_NEW, '① 工具条 41px → 40px（与其余四条对齐）', BARH_MARK)
    edit(PCS, ANIM_OLD, ANIM_NEW, '② 面板 ⇄ 胶囊锚到右上角', ANIM_MARK)
    # ★ strict=False：这一步是「插在锚点前 + 把锚点原样接回」⇒ `old` 与 `mark` 同时存在是**对的**
    edit(PCS, TAIL_OLD, TAIL_NEW, '③ 毛玻璃（并把 l4 标记原样接回）', GLASS_MARK, strict=False)

    print('=== 3/4  panel.js ===')
    edit(PJS, OPENTAB_OLD, OPENTAB_NEW, '① openTab 支持 opts.ico', OPENTAB_MARK)
    edit(PJS, REUSE_OLD, REUSE_NEW, '① openTab 复用页签时同步页签名/图标', REUSE_MARK)
    edit(PJS, PREVJS_OLD, PREVJS_NEW, '① prevShow 改为开页签', PREVJS_MARK)
    edit(PJS, ESCOWN_OLD, ESCOWN_NEW, "① Esc 裁决：删掉预览那一层（引用已悬空）", ESCOWN_MARK)
    edit(PJS, ESCCHAIN_OLD, ESCCHAIN_NEW, "① Esc 优先级链：摘掉 prevOpen", ESCCHAIN_MARK)

    print('=== 4/4  跨层标记兜底断言 ===')
    # ★★ 各层的 mark 是「后一层必须替前一层保住」的契约：谁把它删掉，谁就会让**上一层**
    #    复跑时误判「还没写过」而整块重挂。这里把五层的存活性一次盯住。
    marks = [
        (MODS, 'id="av-zd-status"', 'l2 · 面板静态 DOM'),
        (PCS, '/* r108-l2 */', 'l2 · 第 19 节'),
        (PCS, '/* r108-l3 */', 'l3 · 第 19.1~19.3 节'),
        (PCS, '/* r108-l4 */', 'l4 · 第十五拍'),
        (PCS, '/* r108-l5 */', 'l5 · 第十六拍'),
        (MODS, 'class="zd-menu giencoder-dropdown-popup zd-menu-branch"', 'l3 · 两枚下拉'),
        (MODS, 'data-zd-git="commit"', 'l3 · Git 三行'),
        (MODS, 'class="zd-cv"', 'l2 · 折叠箭头'),
        (PCS, '.zd-sec.is-closed .zd-sec-x { display: flex; }', 'l4 · ⑥ trailing 仅折叠可见'),
        (PCS, '@keyframes zd-todo-spin {', 'l4 · ④ loading 弧'),
        (MODS, 'data-td-art="1"', '① 产物行仍在（两行 = 两个产物）'),
    ]
    bad = []
    for p, mk, label in marks:
        if mk not in rd(p)[0]:
            bad.append('%s：%s（在 %s 里找不到）' % (label, mk, os.path.basename(p)))
    # ⚠ 计数判据一律取「块首那几行」：短片段会被同层新规则一起命中（l4 踩过）
    t = rd(PCS)[0]
    for name, cnt in (('19. 任务信息面板', t.count('19. 任务信息面板')),
                      ('html:has(.r93-sk) .zd-host', t.count('html:has(.r93-sk) .zd-host')),
                      ('.zd-card {', t.count('.zd-card {\n  pointer-events: auto;')),
                      ('.zd-pv-name {', t.count('.td-pv-name {')),
                      ('.td-pv-hint {', t.count('.td-pv-hint {')),
                      ('.td-pv-body {', t.count('.td-pv-body {')),
                      ('.td-pv .td-sum-arti {', t.count('.td-pv .td-sum-arti {')),
                      ('@keyframes zd-panel-in', t.count('@keyframes zd-panel-in {')),
                      ('transform-origin: 100% 0;', t.count('transform-origin: 100% 0;')),
                      # 两处 `color-mix`：卡片族走 `--color-bg-2`、弹层族走 `--color-bg-popup`
                      ('color-mix(', t.count('color-mix('))):
        if cnt != (2 if name == 'color-mix(' else 1):
            bad.append('panel.css：%s 出现 %d 次（应 %d）'
                       % (name, cnt, 2 if name == 'color-mix(' else 1))
    # 旧浮层的残留：DOM / CSS 两头都必须归零（CSS 注释里提到旧类名是正常的 ⇒ 先剥注释再数）
    m = rd(MODS)[0]
    if m.count('td-sum-prev') != 0:
        bad.append('_mods.html：td-sum-prev 残留 %d 处（应 0）' % m.count('td-sum-prev'))
    if m.count('data-td-prev-x') != 0 or m.count('is-primary" type="button" data-td-prev-close') != 0:
        bad.append('_mods.html：旧浮层的关闭按钮残留')
    nocmt = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
    if re.findall(r'\.td-sum-prev', nocmt):
        bad.append('panel.css：.td-sum-prev 残留 %s' % re.findall(r'\.td-sum-prev\S*', nocmt)[:3])
    if '.td-mod.td-sum { position: relative; }' in nocmt:
        bad.append('panel.css：.td-mod.td-sum 的定位仍在（只服务旧浮层，应删）')
    if 'td-prev-btn.is-primary' in nocmt:
        bad.append('panel.css：.td-prev-btn.is-primary 残留（页签里已无主色按钮）')
    # ① 的 1px 对齐：28px 那版按钮必须已经不存在（0 次才是对的目标态）
    if 'height: calc(28px * var(--ui-fs-ratio)); padding: 0 14px' in nocmt:
        bad.append('panel.css：`.td-prev-btn` 仍是 28px（会把工具条顶成 41px）')
    j = rd(PJS)[0]
    # ★ 残留判据必须**先剥注释**：本层的注释里为了留痕，主动写了 `prevEl` / `prevOpen`
    #   / `if (prevOpen) prevHide();` 这些旧标识符（说明「为什么删」）⇒ 裸串搜索必误报。
    jcode = re.sub(r'/\*.*?\*/', '', j, flags=re.S)
    jcode = re.sub(r'(?m)^\s*//.*$', '', jcode)
    for pat in (r"'\[data-td-prev\]'", r'\bprevEl\b', r'\bprevHide\b', r'\bprevOpen\b'):
        if re.search(pat, jcode):
            bad.append('panel.js：旧浮层的 %s 引用残留（代码里，不是注释）' % pat)
    if j.count('openTab(') < 1 or j.count("openTab('preview'") != 1:
        bad.append('panel.js：openTab(\'preview\') 应恰好 1 处')
    # ① 复用页签时同步页签名/图标 —— 这条守卫必须恰好 1 处（多了会把别的调用方也改了）
    if jcode.count('if (opts) {') != 1:
        bad.append('panel.js：`if (opts) {` 出现 %d 次（应 1 = 只有复用分支那一处）'
                   % jcode.count('if (opts) {'))
    if bad:
        sys.exit('!! 跨层标记自检失败：\n   ' + '\n   '.join(bad))
    print('   全部存活 ✓')

    print()
    print('应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for s in SKIPPED:
        print('   跳过  %s' % s)


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""r107 第五拍 · panel.css 第 1 节（四枚下拉）与第 8 节（右键菜单）重写。"""
import io

P = 'mg-work/r107/part107/panel.css'
raw = io.open(P, 'rb').read().decode('utf-8')
crlf = raw.count('\r\n')
s = raw.replace('\r\n', '\n')

A = '/* ---------------------------------------------------------------- 1. 下拉菜单'
B = '/* ---------------------------------------------------------------- 2. '
C = '/* ---------------------------------------------------------------- 8. 右键菜单'
D = '/* ---------------------------------------------------------------- 9. 划词浮条'

for k in (A, B, C, D):
    assert s.count(k) == 1, 'anchor miss %r => %d' % (k[:60], s.count(k))

SEC1 = '''/* ---------------------------------------------------------------- 1. 下拉菜单
   （模块选择 / 审查显示选项 / 对比范围 / 提交·推送 —— 四枚共用一套盒子样式，
     与第 8 节右键菜单同源，故「面板 + 条目 + 分隔线」三条规则三处共用一套选择器组）
   ★★ 第五拍返工：原挂 `.giencoder-select-popup` + `.giencoder-menu` 是**串了两个族** ——
     前者是 **Select 组件**的弹层，后者 `menu.json` 的 `mapsFrom` = `sidenav/topnav`
     （**主导航菜单**，不是下拉）⇒ 邵先生判「还没应用设计系统的组件」。
     本类交互是「点 / 右键触发的**弹出菜单**，项可含图标与快捷键」⇒ 契约正主是
     `dropdown.json`：`variants.contextMenu` = 右键展开；`states.selected` = 文字
     `--color-primary-6` 或勾选图标；`interaction.hover` = 背景 `--color-fill-2`。
     与**本页既有的行右键菜单**（r93 ⑦ `.r93-ctx`，同一套 DS Dropdown 取值）口径一致。
   ⚠ 本页只内联了 `.giencoder-dropdown-popup` 的**骨架**（`transform-origin:top` /
      `min-width:168px` / `padding:6px` + 一条 0.2s entry 动画），`-item` / `-divider` 的
      编译样式**不存在** ⇒ 面板与条目按契约 + r93 实测值**按需自补**（r93 头注释里的既定做法），
      并用「双类提权」把自己的类与 DS 类写在一起（同 `.r93-ctx` 的用法）。
   ⚠⚠ 骨架里那条 `animation: giencoder-popup-in` **必须显式 `animation: none` 掉**：
      它播完 `opacity` 会回落 0 ⇒ 菜单「闪一下就不见」；开合一律走契约状态类
      `.giencoder-popup-open`（与站内其它 DS 弹层同口径，见 PLAYBOOK 规则 6）。 */
.td-mod-menu.giencoder-dropdown-popup,
.td-rv-menu.giencoder-dropdown-popup,
.td-ctxmenu.giencoder-dropdown-popup {
  box-sizing: border-box;
  display: flex; flex-direction: column; gap: 2px;
  min-width: 168px; max-width: 320px; padding: 6px;
  background: var(--color-bg-popup);
  border: 1px solid var(--color-border-2);
  border-radius: 8px;
  box-shadow: var(--shadow3-down);
  transform-origin: top left;
  animation: none;
  opacity: 0; visibility: hidden; translate: 0 4px; scale: 0.96;
  transition: opacity 0.15s cubic-bezier(0.34, 0.69, 0.1, 1),
              translate 0.15s cubic-bezier(0.34, 0.69, 0.1, 1),
              scale 0.15s cubic-bezier(0.34, 0.69, 0.1, 1),
              visibility 0s 0.15s;
}
.td-mod-menu.giencoder-dropdown-popup.giencoder-popup-open,
.td-rv-menu.giencoder-dropdown-popup.giencoder-popup-open,
.td-ctxmenu.giencoder-dropdown-popup.giencoder-popup-open {
  opacity: 1; visibility: visible; translate: 0 0; scale: 1;
  transition: opacity 0.2s cubic-bezier(0.34, 0.69, 0.1, 1),
              translate 0.2s var(--transition-timing-function-spring, cubic-bezier(0.34, 0.69, 0.1, 1)),
              scale 0.2s var(--transition-timing-function-spring, cubic-bezier(0.34, 0.69, 0.1, 1)),
              visibility 0s;
}
/* 四枚下拉：定位参照是 `.td-browse`（有 position: relative），不是各自的父元素 ——
   `.td-rv-opts` 挂在**审查模块自己的工具条**里，若以工具条为包含块会被 `.td-mod{overflow:hidden}` 裁掉。
   四枚同用 `top: 42px`（= 标签栏 44px 下方）。右键菜单（`.td-ctxmenu`）改 `position: fixed` 跟随指针。 */
.td-mod-menu.giencoder-dropdown-popup,
.td-rv-menu.giencoder-dropdown-popup { position: absolute; top: 42px; z-index: 30; }
.td-ctxmenu.giencoder-dropdown-popup { position: fixed; top: 0; left: 0; z-index: 60; }
.td-mod-menu { left: 64px; right: auto; }
.td-rv-scope-menu { left: 8px; right: auto; }
.td-rv-opts, .td-commit-menu { right: 8px; left: auto; }
/* ⚠ `[hidden]` 的 `display:none` 这次**能生效**了：上一版挂的是 `.giencoder-select-popup`，
   而本页 r75 有一条 `.giencoder-select-popup { display: block !important }`（给浮窗过渡留起点）
   ⇒ 连 `[hidden]` 都压不过；换成 `.giencoder-dropdown-popup` 后没有这条通配，兜底可用。 */
.td-mod-menu.giencoder-dropdown-popup[hidden],
.td-rv-menu.giencoder-dropdown-popup[hidden],
.td-ctxmenu.giencoder-dropdown-popup[hidden] { display: none; }
/* 条目：DS Dropdown 契约（`padding:5px 8px` / 圆角 4 / `gap:8px` / 行高 22 × `--ui-fs-ratio`）。
   ⚠ 宿主是 `<button>`（DS 按 `<div>` 写的）⇒ 四条 UA 差异必须补：
     ① `background: transparent`（按钮自带 `buttonface` 灰底；DS 只在 `:hover` 改底色）
     ② `border: 0`（按钮自带 2px outset 边）③ 字体 / 字号**不继承**（会掉回 UA 的 13.33px Arial）
     ④ `box-sizing` + 撑满 + 左对齐。
   ★★ hover 必须在本块**显式写出来**（本页没有 `.giencoder-dropdown-item:hover` 裸规则，
      `-item` 的编译样式不存在）⇒ 只有本块写了才有 hover。
   ★ 第五拍修的真 bug：上一版基态写成 `.td-mm-item:not(.giencoder-menu-item-selected)` (0,2,0)，
     与本页 DS 的 `:hover` / `-selected` **同特异性但文档序在后** ⇒ 两态一起被压掉
     ⇒ 实测「四枚下拉 + 右键菜单 hover 全无」（真鼠标悬停、`matches(':hover')` 为 true，
     底色仍是 `rgba(0,0,0,0)`）。本版把基态与 `:hover` 写在同一块、基态在前 ⇒ 顺序自洽。 */
.td-mod-menu .giencoder-dropdown-item,
.td-rv-menu .giencoder-dropdown-item,
.td-ctxmenu .giencoder-dropdown-item {
  box-sizing: border-box; width: 100%; border: 0;
  display: flex; align-items: center; gap: 8px;
  padding: 5px 8px; border-radius: 4px;
  font-family: var(--font-family); font-size: var(--font-size-body-3);
  line-height: calc(22px * var(--ui-fs-ratio));
  color: var(--color-text-1); white-space: nowrap; cursor: pointer;
  text-align: left; background: transparent;
}
.td-mod-menu .giencoder-dropdown-item:hover,
.td-rv-menu .giencoder-dropdown-item:hover,
.td-ctxmenu .giencoder-dropdown-item:hover { background: var(--color-fill-2); }
/* 选中态：DS Dropdown **没有** `-selected` 类（不虚构）⇒ 按契约给的两种表达取
   「勾选图标 + 主色文字」；✓ 由 HTML 里的 `.td-mm-mark` 承载，显隐由 panel.js 按
   `aria-checked` 打的 `is-checked` 控制（radio / checkbox 两类都吃这一条）。 */
.td-mod-menu .giencoder-dropdown-item.is-checked,
.td-rv-menu .giencoder-dropdown-item.is-checked { color: var(--color-primary-6); }
.td-mod-menu .giencoder-dropdown-item.is-checked .td-mm-mark,
.td-rv-menu .giencoder-dropdown-item.is-checked .td-mm-mark { opacity: 1; }
/* 分组标题：DS Dropdown 无此子部件 ⇒ 借用 Menu 的 `giencoder-menu-group-title`（仍是 DS 类，
   不自绘）；但它自带 `padding:8px 16px 4px` 的左 16px 与 Dropdown 条目的左 8px 不齐 ⇒ 压到 8px。 */
.td-mm-cap.giencoder-menu-group-title { padding-left: 8px; }
/* DS 没覆盖的三个槽位：名称吃掉剩余宽度（保证省略号）、右侧快捷键、右侧 ✓ */
.td-mm-name { flex: 1 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.td-mm-key, .td-ctx-key { flex: none; font-size: var(--font-size-body-1); color: var(--color-text-4); }
/* DS 的 `.giencoder-menu-icon` 只写 `display:inline-flex`，没写 `flex` ⇒ 图标在窄菜单里会被压扁；
   本版改挂 Dropdown（无 icon 子部件）⇒ 图标位收回自绘，两条一起给。 */
.td-mm-ico { display: inline-flex; flex: none; }
/* 复选 / 单选型条目的 ✓（`.is-checked` 时显形；颜色取主色，与文字同族） */
.td-mm-mark {
  flex: none; width: 14px; text-align: center;
  font-size: var(--font-size-body-1); color: var(--color-primary-6);
  opacity: 0; transition: opacity 120ms;
}
/* 分隔线 → DS Dropdown 的 divider 子部件（契约：1px + `--color-border-1`） */
.td-mod-menu .giencoder-dropdown-divider,
.td-rv-menu .giencoder-dropdown-divider,
.td-ctxmenu .giencoder-dropdown-divider {
  display: block; height: 1px; margin: 4px 2px; background: var(--color-border-1);
}

'''

SEC8 = '''/* ---------------------------------------------------------------- 8. 右键菜单
   一份容器（`.td-ctxmenu`）承载八类目标的菜单（标签栏 / 审查文件 / 审查代码行 / 终端 /
   浏览器元素 / 浏览器空白 / 摘要来源 / 摘要产物 / 计划条目），条目由 panel.js 按目标现场填。
   面板 / 条目 / 分隔线**与四枚下拉共用第 1 节那套选择器组**（同源 DS Dropdown），
   本节点只放右键菜单独有的两件事：① 跟随指针的 `fixed` 定位（坐标走自定义属性）
   ② 顶部「目标名」行 + 危险项 / 禁用项。 */
/* ★ 坐标走两个自定义属性（而不是直接写行内 `top/left`）：本页存在 `!important` 级的
   页面适配层，它连行内样式也压得过 ⇒ 只能靠「自定义属性 + 同块 `!important`」这条通道落位。 */
.td-ctxmenu.giencoder-dropdown-popup {
  top: var(--td-ctx-y, 0px); left: var(--td-ctx-x, 0px);
}
html[data-r93-page='conversation'] .td-browse .td-ctxmenu.giencoder-dropdown-popup {
  top: var(--td-ctx-y, 0px) !important;
  left: var(--td-ctx-x, 0px) !important;
  bottom: auto !important;
}
/* 顶部「目标名」行：不可点，只说明这份菜单作用于谁 */
.td-ctx-head {
  padding: 6px 8px 4px;
  font-size: var(--font-size-body-1); color: var(--color-text-3);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.td-ctxmenu .giencoder-dropdown-item.is-danger { color: var(--color-danger-6); }
.td-ctxmenu .giencoder-dropdown-item.is-disabled { color: var(--color-text-4); cursor: not-allowed; }

'''

s = s[:s.index(A)] + SEC1 + s[s.index(B):]
s = s[:s.index(C)] + SEC8 + s[s.index(D):]

# 残留断言：先剥掉 CSS 注释（注释里会提旧类名做说明），再查旧族类名；
# `giencoder-menu` 需排除仍借用的 `-group-title`（DS Menu 的分组标题，本处有意保留）。
import re as _re
nocmt = _re.sub(r'/\*.*?\*/', '', s, flags=_re.S)
for bad in ['giencoder-menu-item', 'giencoder-select-popup', 'td-mm-item', 'td-ctx-item']:
    n = nocmt.count(bad)
    assert n == 0, 'RESIDUE %s => %d' % (bad, n)
rest = _re.findall(r'giencoder-menu(?!-group-title)', nocmt)
assert not rest, 'RESIDUE giencoder-menu(非 group-title) => %d %r' % (len(rest), rest[:3])

io.open(P, 'wb').write((s.replace('\n', '\r\n') if crlf else s).encode('utf-8'))
print('panel.css chars %d -> %d (LF-normalized)' % (len(raw.replace('\r\n', '\n')), len(s)))

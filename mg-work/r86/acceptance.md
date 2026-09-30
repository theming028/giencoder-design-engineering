# r86 验收 —— 「设置」页四条修订

> 邵先生 2026-09-30 四条（对象 = r85 落地的「设置」页）：
> 1. 设置页面的 aside 的宽度是固定的，不允许拖拽宽度；
> 2. 设置页面的卡片 `class="r85-card"` 内的 item 间隔线的颜色浅了，需要加深一级；
> 3. 设置页面卡片右侧的 `r85-ctl` 要使用设计系统的标准 select 组件，要全要素还原；
> 4. `.r85-ic` 的背景色浅了，需要使用深一级的。

页面：`pages/settings.html`　**420820 → 426029 字符（+5209）**
补丁：`mg-work/r86/apply86.py`（r85 `apply85.py` 的接续改写版）
回滚：`cp mg-work/r86/settings.before.html pages/settings.html`
基线：`mg-work/r86/settings.before.html`（= r85 交付态）

---

## 一、四条落地

### ① aside 定宽 + 禁拖拽

**现状查明**：aside 是**外壳 React 渲染**的（源码里没有 `<aside>`），宽度由 state 写成内联 `style.width`，
右缘挂着一条 `role="separator" aria-label="调整菜单宽度"` 的拖拽把手（实测 6px、紧贴 aside 右缘 262）。
外壳里本来有 `asideDisabled` 概念（`asideDisabled: !(路由 === '/dev')`）——**只有研发工作台才禁用**，设置页是可拖的。

**做法**（两层，都不碰 React）：

```css
body[data-r85-set] aside { width: 256px !important; }                    /* !important 压住内联 style ⇒ 拖了也不动 */
body[data-r85-set] aside[aria-hidden='true'] { width: 0 !important; }    /* 收起态：外壳 JSX 是 aria-hidden={!asideOpen} */
body[data-r85-set] [role='separator'][aria-label='调整菜单宽度'] { display: none !important; }
```

```js
['mousedown', 'pointerdown'].forEach(function (t) {
  document.addEventListener(t, function (ev) {
    if (ev.target.closest && ev.target.closest('[role="separator"][aria-label="调整菜单宽度"]')) {
      ev.stopPropagation(); ev.preventDefault();      /* 捕获阶段拦截，双保险 + 挡掉拖拽时的文字选择 */
    }
  }, true);
});
```

**实测**：`wBefore 256 → wAfter 256`（模拟 mousedown+mousemove 在把手坐标）、`sepDisplay: none`、把手 box 全 0。

### ② 卡片内间隔线加深一级

`.r85-row + .r85-row::before { background: var(--color-fill-2) → var(--color-border-2) }`
即 `#F2F2F2`（gray-2）→ `#E5E5E5`（gray-3）。**实测 8 条分割线全部 `rgb(229,229,229)`**。
（用 `--color-border-2` 而非 `--color-fill-3`：两者同值，但分割线用 border 语义更准。）

### ③ `.r85-ctl` 改用 DS 标准 select 组件（全要素）

**删净 r85 手搓件**（`.r85-sel` 4 条规则 + `.r85-menu` 4 条规则 + `openMenu()` 函数 + 其唯一调用点），
改用页面里**早已内联但从未被使用**的 DS 组件（`components.css`「=== Select 选择器 ===」34 条规则）。

**标准 anatomy 逐要素落实**（照 `components/preview/component-select.html` 官方示例）：

| 要素 | 实现 |
|---|---|
| selector | `.giencoder-select`（容器定宽 `style.width`） |
| view | `.giencoder-select-view` + `tabindex=0` + `role=combobox` + `aria-haspopup=listbox` + `aria-expanded` |
| 值文本 | `.giencoder-select-view-text`（自带 `data-placeholder`） |
| arrow-icon | `.giencoder-select-arrow`（官方 12×12 chevron，`stroke=currentColor`） |
| clear | `.giencoder-select-clear`（官方 12×12 X）+ `has-value` 类驱动「hover 时箭头让位」 |
| option-list / option | `.giencoder-select-option-list` > `.giencoder-select-option`（含 `-selected` / `-disabled` 态） |
| popup | `.giencoder-select-popup`，开合唯一开关 **`.giencoder-popup-open`**（不写内联 display） |
| 键盘 | ArrowDown/Up 移动（`:focus` 高亮）、Enter 选中、Esc 关闭并回焦、Tab 关闭 |
| 关闭 | 点击外部关闭；**一次只开一个**（`closeAllSelects()`）；切导航菜单时清实例 |

**实测 8 项交互全过**（真鼠标 hover/click/press）：

| 项 | 结果 |
|---|---|
| A. hover 触发框 | 箭头 `display:none`、清除 X `display:flex`、底色 `rgb(247,247,247)`=fill-1、投影 none ✓ |
| B. 点击展开 | `aria-expanded=true`、`.giencoder-popup-open` 在、visibility visible、边框 `rgb(55,112,247)`=primary-6、面板 200×114、选项高 32 ✓ |
| C. 点选第 3 项 | 文本同步「标准模式→自动模式」、4 个 select 各自 selected 互斥、面板收起 ✓ |
| D. 键盘 | ArrowDown 展开并高亮首项（`aria-activedescendant=r86opt-1`、`:focus` 底色 `rgb(242,242,242)`）、再 ArrowDown 到次项、Enter 选中并收起 ✓ |
| E. Esc | 关闭 ✓ |
| F. 点外部 | 关闭 ✓ |
| G. 一次只开一个 | s0=false / s1=true ✓ |
| H. 拖拽尝试 | aside 仍 256 ✓ |

**⚠️ 改动后立刻暴露的坑（已修）**：DS 默认 `padding: 0 12px` 左右对称，但 **98px 的框只给文字留 52px，而「标准模式」实测需 56px** ⇒ 直接出省略号（70px 的「中文」更明显）。
加一条最小适配层 `padding-right: 8px` 后文字区 56px 正好容纳，且箭头墨迹右距变成 11px ≈ 设计稿的 10px —— 比默认值更贴合设计稿。

而且**这个 8px 恰好反证了设计稿的真实内距**：
`1(边框) + 12(左内距) + 56(文字) + 8(gap) + 12(箭头) + 8(右内距) + 1(边框) = 98` —— 与设计稿实测宽度 **98 完全吻合**。

### ④ 行图标底加深一级

`.r85-ic { background: var(--color-fill-2) → var(--color-fill-3) }`，即 `#F2F2F2` → `#E5E5E5`。**实测 `rgb(229,229,229)`**。

---

## 二、四查

| 项 | 结果 |
|---|---|
| **几何对照（r85 那套 67 项）** | **67 项 0 偏差**（±1px）⇒ r86 未破坏 r85 的任何几何（`mg-work/r85/ev/cmp85.py` 原样复跑） |
| **幂等** | 复跑 `+0`，`sha256 49f826cd…c94c` |
| **语法** | `ALL_OK settings.html  script=6 style=7` |
| **门禁（本次）** | `✅ 通过`（warning 0 / info 1 / critical 0） |
| **门禁（HEAD 基线逐条 diff）** | **`diff` 无输出 = 零新增**；`gaps.log` 无 settings.html 条目，跑完已 `git checkout --` 还原 |

---

## 三、⚠️ DS 标准组件 vs 设计稿的 3 处固有差异（本轮**按 DS 标准**落地，请拍板）

| 项 | 设计稿实测 | DS 标准组件 | 说明 |
|---|---|---|---|
| 边框色 | `#F2F2F2`（gray-2 / `--color-border-1`） | **`#E5E5E5`**（gray-3 / `--color-border-2`） | 组件 CSS 写死 border-2；改它就得动组件本体 |
| 圆角 | ≈ **6px**（像素实测） | **4px**（`--border-radius-medium`） | |
| 表面层 | 无投影 | `0 1px 2px #0f172a0a, 0 0 0 1px var(--select-ring)` | DS 的「按钮表面层」机制，hover 时消失 |

本轮按「使用设计系统的标准 select 组件」执行，**未覆盖上述三项**。
若要以设计稿为准，三条都可以在 `.r85-ctl` 作用域内加适配层解决（各 1 行）。

---

## 四、其余偏差说明

1. 页面字符数 `+5209` 是「摘 r85 块 + 插 r86 块」的净值（r85 手搓 select 的 CSS/JS 一并删除）。
2. 侧栏宽度锁 256px 是**外壳默认值**（实测 `inlineW: 256px`）；若将来外壳改默认宽，需同步改这行。
3. 页高 918 / 导航 232×268 / 三张卡片 230·448·156 与 r85 完全一致（已复测）。

---

## 五、待拍板

1. **③ 的 3 处样式差异**（见第三节）：按 DS 标准（现状）还是按设计稿？
2. **清除按钮的行为**：本页 select 都是「必选设置项」，当前「清除」= 回落到首项（`data-placeholder` 也取首项）。
   若要「清除后显示『请选择』的空态」需另定（设置项通常不允许空）。
3. r85 遗留四条照旧（非选中导航项常显底色 / 字号滑块 6 档 vs 3 档 / 其余菜单空态 / 窗口 chrome）。
4. r84 遗留提问仍未答（会话历史确认态按钮组是否再挪 8px）。

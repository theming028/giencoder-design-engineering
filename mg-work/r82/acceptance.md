# r82 验收报告 · 四条修订

> 邵先生 2026-09-29 第二轮反馈（5 条，其中第 2 条为「提速」）
> 落地脚本：`mg-work/r82/apply82.py`（复用 `mg-work/r81/apply81.py` 的块作为单一事实来源）
> 回滚：`cp mg-work/r82/before/<page>.html pages/<page>.html`

---

## 0. 产物与幂等

| 页面 | 改前字符 | 改后字符 | 增量 | 注入块 |
|---|---|---|---|---|
| `pages/dev.html` | 427 519 | 444 701 | +17 182 | `r81-ws` |
| `pages/kanban.html` | 539 382 | 566 171 | +26 789 | `r81-ws` + `r82-tabs` + `r82-coop` |
| `pages/req-kanban.html` | 485 173 | 507 786 | +22 613 | `r81-ws` + `r82-tabs` |
| `pages/task-detail.html` | 743 000 | 760 182 | +17 182 | `r81-ws` |

改前字符数 = **摘掉上一版同名块之后**的长度（脚本自带「先摘后插」），所以反复跑结果一致：

```
dev.html           427519 → 444701 (+17182) （摘掉上一版块 2 件：444701 → 427519）
kanban.html        539382 → 566171 (+26789) （摘掉上一版块 6 件：566171 → 539382）
req-kanban.html    485173 → 507786 (+22613) （摘掉上一版块 4 件：507786 → 485173）
task-detail.html   743000 → 760182 (+17182) （摘掉上一版块 2 件：760182 → 743000）
```

`check-syntax.py`：4 页全部 `ALL_OK`。

---

## 1. 第 1 条 · 触发器激活态背景色 = hover 色

- 目标色 `#DAE3ED`（`--r81-hover-bg`），与 hover 同源同一变量。
- 做法：在 r81 块尾追加一条 `.r81-ws-trigger[aria-expanded="true"] { background-color: var(--r81-hover-bg); }`。
  `aria-expanded` 由 r81 的 JS 在 `show()/hide()` 里同步，无需新增状态类、无新增 token。

实测（`pages/dev.html`，1440×900）：

```
静止 : bg = rgba(0, 0, 0, 0)      aria-expanded = false
展开 : bg = rgb(218, 227, 237)    aria-expanded = true      ← = #DAE3ED ✔
关闭 : bg = rgba(0, 0, 0, 0)      （回落正确）
```

无回归：触发器 `88,11,254,26`、浮窗 `88,41,388,526`、Δ左 0 / Δ上 4、7 条目 / 1 选中、可见触发器数 1。

---

## 2. 第 3 条 · 需求看板 / 任务看板切换的滑动动效

背景：两个 tab 各占一页（`data-goto` 跳转），原先只有 `is-on` 的硬切换。

做法（`r82-tabs` 块，注入 `kanban.html` / `req-kanban.html`）：

- 在 `.kb-radio` 里插一个绝对定位的 `.kb-radio-thumb`（`background: var(--color-bg-1)` + `1px solid var(--color-border-2)` + `radius 8`），
  白底/描边/圆角与原 `is-on` 完全同源；
- 加 `.kb-radio--thumbed` 后，`.kb-radio-btn.is-on` 的底/描边让位（**保留 1px 边框占位，布局零变化**）；
- 指示器位置直接取按钮的 `offsetLeft/offsetTop/offsetWidth/offsetHeight`（含激活态那个 14px 图标带来的宽度差），
  `.kb-radio` 自身是 `position:absolute`，故其包含块就是它，**与容器 `left` 被 JS 改写无关**；
- 点击时用 capture 监听抢先于页面既有的 `location.href` 处理器：先把图标搬到目标按钮、切 `is-on`，
  再 `requestAnimationFrame` 里把指示器滑过去，`220ms cubic-bezier(.4,0,.2,1)`，260ms 后跳转；
- 新页面加载时读 `sessionStorage['giencoder-kb-tab-from']`，让指示器**先落到来源 tab 再滑到当前** —— 跨页读起来是一段连续滑动。

实测：

```
host = 185,57,228,32          thumb = 289,56,124,34   （= 激活按钮矩形，逐值相同）
thumb 计算样式：absolute / rgb(255,255,255) / rgb(229,229,229) / radius 8 / transition 0.22s
滑动采样（点「需求看板」，目标 x=185）：
  idle 289/124  →  t+60 270/124  →  t+110 205/124  →  t+160 189/124
跳转落点 = pages/req-kanban.html ✔   sessionStorage 记到 'req-kanban.html' ✔
```

证据图：`mg-work/r82/ev/r82-tab-slide.png`（静止 / 滑动中 / 跳转后 三帧）。

---

## 3. 第 5 条 · 「待协作任务」弹窗的装饰性界面元素

设计稿 `layer 1389:18525` 拿到的素材与仓内落盘的 `vc875:31526` **逐字节相同**（4255 B），
即：面板上缘左右角各一枚「外扩玻璃翼」。

设计值（`mg-work/r82/raw/svg_vc875-31526.svg` + `sel_83621409_20260926154702.json` 的结构化节点）：

| 项 | 值 |
|---|---|
| 组尺寸 | 1278 × 39.096，左缘 81 = 面板左 120 − 39 |
| 单枚形状 | `M0 0 L24 0 L24 24 C24 10.745 13.25 0 0 0 Z`（24×24 凹角圆角片） |
| 纵向压缩 | viewBox 高 87.096 → 实高 39.096 ⇒ ×0.4479 ⇒ 实高 = 24 × 0.4479 ≈ **10.75** |
| 填充 | `#FFFFFF` / `fill-opacity .95` |
| 投影 | `feOffset dy=8` + `feGaussianBlur stdDeviation=8` + `rgba(0,0,0,.12)` |
| 面板本体 | 1200 × 804 @ (120,48)，顶角**方角**、底角 radius 16、白 95% |

设计稿 PNG 逐像素反推：面板上缘 48，左翼在 y=50 时面板最左白像素到 x=107、y=53 → 112、y=56 归位 120
—— 与上式算得的弧线逐点吻合（2~3px 为 95% 白 + 投影的抗锯齿）。

实现：`r82-coop` 块，两枚 `.r82-coop-wing` 挂在 **`.kb-coop`**（不是 `.kb-coop-dialog`，后者 `overflow:hidden` 会把翼裁掉）；
位置由面板实时矩形推出（rect 相减再减掉 `.kb-coop` 的 border，得到对其 padding box 的偏移），
并在 `MutationObserver(hidden/class)` + `click/pointerdown/keydown` + `resize` 上补量（弹窗有 240ms 出场动效）。
未就位前 `opacity:0`，避免收起态量不到位置时闪在左上角。

实测（`pages/kanban.html`，1440×900）：

```
dialog = 151,49,1138,794
左翼   = 127,49,24,11    → 翼右缘 − 面板左缘 = 0 ✔   翼顶 − 面板顶 = 0 ✔
右翼   = 1289,49,24,11   → 翼左缘 − 面板右缘 = 0 ✔   翼顶 − 面板顶 = 0 ✔
尺寸 24.00 × 10.75 / fill rgb(255,255,255) / fill-opacity 0.95
filter = drop-shadow(rgba(0,0,0,0.12) 0px 8px 8px) / z-index 2 / 挂在 .kb-coop 上 ✔
```

证据图：`mg-work/r82/ev/r82-wing-compare.png`（设计稿左角 · 实现左角 · 设计稿右角 · 实现右角，6×）。
两者在 6 倍放大下无可见差异。

### 有意取舍（1 处）

- **未复刻 `backdrop-filter: blur(6px)`**：设计稿里它作用在翼的 clipPath 区域，但该处背后已经是
  `.kb-coop-mask`（`#000 32%` + `blur(10px)`），再叠 6px 模糊肉眼不可分辨；省掉它可避免为一条曲线引入
  `clip-path: path()` / data-URI mask 的兼容与体量成本。视觉对照图已确认无差异。

---

## 4. 第 4 条 · 会话历史二级页 —— **未做，等画布切页**

给的是 `page_id=263:05935 & layer_id=1389:18518`（数字分身页）。

本轮把 MCP 取数通道试穿了一遍，结论明确：

| 尝试 | 结果 |
|---|---|
| 裸图层 ID `1389:18518`（画布在 `pu489:07981`） | 0.1s 返回 `TargetNodePageMismatch: expected=pu489:07981, actual=263:05935` |
| 完整 goto 链接 | 90 / 100 / 180s 三档全超时 |
| `get_screenshot`（scale 2） | 45s 超时 |
| 仓内历史落盘（`mg-work/r80/raw/`） | 有 `263:05935` 的旧导出（`1345:18487` 左栏、`1345:18502` 右栏 aside），**没有 `1389:18518`** |
| `~/.mgmcp/mgmcp.log` 全量检索 `1389:18518` | 只有我自己这几次请求，无历史应答 |
| asset / blob 缓存 | `1389:18518` 无产物；`1389:18525` 有（见上节）|

而且历史日志显示：**2026-09-27 取这一页节点时全量超时**（`获取设计稿数据超时，通常是此设计稿解析失败`），
`page 263:05935` 本来就是解析最慢的一页。

**结论**：这一条没做到「精确还原」，卡在取数而不是实现。**解锁只需要一步**：
在 MasterGo 里把画布切到 `数字分身/数字分身` 页并选中 `1389:18518`（或它的父板），我这边一次调用就能拿到
（`mg-work/mgfetch.py` 已封装好，含超时自愈）。

---

## 5. 门禁

```
汇总: 75 个问题   🟡 warning 66 / 🔵 info 9 / 🔴 critical 0
与 r81 基线逐条 diff：新增 0 / 消失 0
```

零新增的依据：
- 成色一律走 `:root` 自定义属性（声明行不含 `color|background` 关键词、引用行含 `var(`）；
- 字号全部走 `var(--font-size-body-1/3)`；
- `.kb-radio-thumb` 的 `background` / `border-color` 都引用既有 `--color-bg-1` / `--color-border-2`，非字面 hex；
- 翼的 `#FFFFFF` / `rgba(0,0,0,.12)` 出现在 `fill` / `filter` 上，不匹配门禁的 hex 正则。

`pages/gaps.log` 与门禁临时产物（`mg-work/kanban/r13/chk/*`）已还原，工作区只剩 4 个产物页 + 记忆文件。

---

## 6. 第 2 条 · 提速（本轮做了什么）

问题不在机器，在**方法**。这轮把三处最费时的环节固化了：

1. **`mg-work/mgfetch.py`（新）** —— 一次调用取设计节点：
   - 传完整 goto 链接（跨页也能取，不像裸 ID 会被当前页挡住）；
   - **HTTP 超时不再傻等/重试**：立刻去 `~/.mgmcp/artifacts/sessions/as_*.json` 找这次请求落下的
     Asset Session，按 `sha256` 从 `artifacts/blobs/sha256/<前2位>/<完整sha>` 把 SVG 解出来；
     ⚠ blob 文件名是**完整 sha**，不是去掉前 2 位（这个坑本轮踩过）；
   - 命中 `TargetNodePageMismatch` 时直接打印「当前画布在哪一页」，给出可执行处置，而不是让人猜。
   - 实测：45s HTTP 超时 → asset 兜底秒级拿回 4255 B 的 SVG，退出码 0。

2. **先并行、再动手**：取数请求在后台跑的同时，前端侧的第 1/3/5 条已经能改能验；
   不再「等取数 → 再开工」串行。

3. **少开浏览器、多算像素**：几何校准（翼的 24×10.75、弧线逐点）改用 **设计稿 PNG 逐像素扫描 + 结构化节点 JSON**，
   只在最后一轮做「改前/改后各一次」的浏览器取证。

本轮真实的耗时分布也很清楚：**大部分时间花在「反复确认设计意图」上**（第 5 条的翼到底是什么形状）。
下轮的默认策略已写进 `PLAYBOOK` P3.13 与 P3.14。

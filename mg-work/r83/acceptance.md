# r83 验收报告 · 2026-09-29

> ⚠ **本报告的 2.2/2.3 两处已被 r84 取代**（2026-09-29 晚，邵先生四条修正）：
> · 「删除」图标在 r83 是**照 PNG 手搓**的（设计稿那枚是未展开的 DS 组件、没有导出 SVG）⇒ r84 换回真矢量；
> · 「点击删除 → 确认态」(`.is-confirm`) 整套撤掉 ⇒ r84 改为 **hover 整张卡片即替换**成 [取消][确定删除]。
> 见 `mg-work/r84/acceptance.md`。本报告其余内容（表头 / 列表 / 行几何 / 取数事实）仍然有效。

> 本轮两条需求（邵先生原话）：
> 1. 「装饰翼的效果很差，干脆去掉吧」→ 撤销 r82 第 5 条交付物
> 2. 「我已经在mastergo客户端里选中了"需求4"的对象」→ 解除 r82 第 4 条阻塞，**精确还原** `layer_id=1389:18518` 的「会话历史」二级页
>
> 产物：`pages/avatar.html` `541277 → 553997 (+12720)`。**未 commit / 未 push**（沿用 2026-09-28 起的约定）。

---

## 一、需求 1：装饰翼摘除

不再往页面注入 `r82-coop` 的 CSS/JS；`mg-work/r82/apply82.py` 里
`BLOCK_IDS` / `BLOCK_SRC` / `PAGE_BLOCKS['kanban.html']` / `TOKENS` 均已删掉 `'coop'` 项，
但 **`PRIOR` 保留 `r82-coop-css` / `r82-coop-js` 的摘除规则** ⇒ 复跑即把页面里既有的两枚翼自动清掉。

| 判据 | 结果 |
|---|---|
| `grep -c "r82-coop" pages/*.html` | **全部 0**（9 页） |
| `apply82.py` 复跑 | `kanban 566171 → 539382`（摘掉上一版块 6 件后回落到 `ws+tabs` 稳态），再跑字符数一致 |
| 幂等 | 复跑第二遍增量恒为 `+22613`（kanban / req-kanban）、`+17182`（dev / task-detail） |

`COOP_CSS` / `COOP_JS` 常量与反解出的翼几何**保留在 `apply82.py` 里备查**（注释已标注「已从装配链摘除」），
将来若要重做不用重新反解。

---

## 二、需求 2：会话历史二级页

### 2.1 取数（★ 本轮最关键的工具事实）

`layer_id=1389:18518` 在 r82 里是**死锁**（裸 ID 报 `TargetNodePageMismatch`、完整 goto 链接 90~1200s 全超时）。
本轮邵先生在客户端选中该对象后，**两条通道的方向正好相反**：

| 工具 | 传参 | 结果 |
|---|---|---|
| `get_selection_node` | **裸图层 ID** | ❌ `TargetNodePageMismatch`（画布不在该页时） |
| `get_selection_node` | **完整 goto 链接** | ✅ 跨页可用 |
| `get_screenshot` | **裸图层 ID** | ✅ **18.4s 拿到 488×990 PNG** |
| `get_screenshot` | 完整 goto 链接 | ❌ 200s 超时（`timeout 200` 被 SIGTERM） |

⇒ **用户已在客户端选中对象时，`get_screenshot` 传裸 ID 拿设计稿 PNG 是最快通道。**
落盘 PNG 带 3~4px 外边距：节点原点在 PNG `(3,2)`，内容 482×984（右侧 0.5px 描边在 PNG x484，x485 是投影）。
**所有像素量测必须先加 `DX,DY = 3,2` 偏移。**

素材（5 件，`mg-work/r83/raw/`）：面板本体 / 表头 / 竖分隔线 / 导出图标 / 返回箭头，
全部按 `logicalPath` 的 basename 落盘（`1389-18518__svg_xxxxxxxx.svg`）——
⚠ 修了 `mgfetch.py` 一个真 bug：同一节点的多件素材原先共用 `asset_<nid>.<ext>` 名，后写覆盖（r83 实测 5 件只剩 1 件）。

### 2.2 实现

`mg-work/r83/apply83.py`（新建，幂等）：注入 3 件 —— 视图块 `<div class="av-hs" id="av-hs">`（插在 `.td-right-inner` 之后）
+ `<style id="r83-hs-css">` + `<script id="r83-hs-js">`（插在 `</body>` 前）。

- **视图切换不依赖原始块的位置**：`#av-chat-drawer[data-av-hs] > .td-right-inner > .av-hs { display:flex }`
  且 `> :not(.av-hs) { display:none }` ⇒ 只靠一个属性开关，不动对话视图的任何结构。
- 入口 = `.td-right-acts [aria-label="会话历史"]`；返回 → 回到对话视图并把焦点还给入口。
- 行内确认态 = `.av-hs-item.is-confirm`（图标组 `display:none`，`[取消][确定删除]` 顶上来）。
- 事件委托挂在**整个视图**（`view`）上 —— ⚠ 返回按钮在 `.av-hs-bar` 里、不在 `.av-hs-list` 内，
  委托挂列表上会「点了没反应」。

### 2.3 设计稿实测 vs 实现实测（全项，单位 = 节点内 CSS px）

| 项 | 设计稿 | 实现实测 | 判 |
|---|---|---|---|
| 面板 | 482 × 984 | 478 × 944（抽屉 480 含 2px 边框） | △ 见 2.4-③ |
| 表头 | 高 48，padding 0 20 | `[0,0,478,48]` | ✔ |
| 表头底线 | `rgb(231,235,241)` | `rgb(231,235,241)` | ✔ |
| 返回按钮 | 24×24 @(20,12)、图标 14×14 | `[20,12,24,24]` / `14px` | ✔ |
| 竖分隔线 | 1×16 @x52、`#C9C9C9` | `[52,16,1,16]` / `rgb(201,201,201)` | ✔ |
| 标题 | x65、16px、600、lh24 | `[65,12,64,24]` / `16px 600 24px` | ✔ |
| 列表 | padding 20、行距 2 | `20px`×4 / `2px` | ✔ |
| 行 | 442 × 56 @y20、圆角 4、行内边距 0 10 | `[20,20,438,56]` / `4px` / `10px 10px` | △ 见 2.4-② |
| 行底 | 白；悬停 / 当前会话 / **确认态** = `242,242,242` | `rgba(0,0,0,0)` / `rgb(242,242,242)` / 确认态 `rgb(242,242,242)` | ✔ |
| 名称 | 14px / 500 / lh22 / `#1F1F1F` | `14px 500 22px` / `rgb(31,31,31)` | ✔ |
| 时间 | 12px / lh16 / `#868686`；首行为空 | `12px 16px` / `rgb(134,134,134)`；首行 `""` | ✔ |
| 图标按钮 | 24×24 @行内 (372,16)/(404,16)，间距 8，padding 5，图标 14×14 | `[372,16,24,24]`/`[404,16,24,24]`/`5px`/`14px` | ✔ |
| 确认态按钮 | 取消 48×28、确定删除 72×28、间距 8、右缘距行右缘 10 | `50×28` / `74×28` / `confirmRight=10`（+2px = 描边） | ✔ |
| 确定删除底 | `#F53F3F` | `rgb(245,63,63)` | ✔ |
| 交互 | 删除 → 确认态 → 取消复原 → 返回回对话 | `confirmOn/confirmBg/confirmOff/attrAfterBack=null/displayAfterBack=none/composerAfterBack=block/reopen=flex` | ✔ |
| 滚动条 | 6px 宽、`#D6D6D6`(= `rgba(0,0,0,.16)`)、圆角、右内缩 4px、thumb 320 高 | 6px / `rgba(0,0,0,.16)` / 圆角 3px / **无溢出不渲染** | △ 见 2.4-① |

### 2.4 已知偏差（三条，都是环境/容器差异，非遗漏）

① **滚动条**：设计稿画的是 **overlay 滚动条**（不占布局，6px、右内缩 4px、只画了 320 高的一段假 thumb）；
Windows Chrome 的 `::-webkit-scrollbar` 是 **classic**（占 6px 布局、贴右、无溢出时不渲染）。
实现按仓内既有约定（同页 `.av-card .giencoder-card-body` 同款 6px + `rgba(0,0,0,.16)` + 圆角）。
当前 7 行内容 444px < 视口 896px ⇒ **静态无滚动条**；真实数据变多后按上述样式出现。

② **行宽 438 vs 442**：设计稿面板 482、行 = 482 − 20×2 = 442；实现抽屉 `--av-chat-w = 480`、
`.td-right-inner{width: calc(var(--av-chat-w) - 2px)}` = 478 ⇒ 行 438。差的 4px 全部来自抽屉总宽 480 vs 482，
是该抽屉既有的既定尺寸（上一轮对照表已按 ✔ 接受），未动。

③ **面板高 944 vs 984**：设计稿画板高 984，实现随视口（1920×1000 ⇒ 1000 − 56 = 944）。对照图**顶对齐**。

### 2.5 门禁三查

| 项 | 命令 | 结果 |
|---|---|---|
| 幂等 | `python mg-work/r83/apply83.py` 复跑 | `541277 → 553997`，复跑一致（摘掉上一版块 3 件）；`strip_all()` 摘回后逐字节等于本轮基线 |
| 语法 | `python mg-work/check-syntax.py pages/{avatar,dev,kanban,req-kanban,task-detail}.html` | **5/5 ALL_OK**（avatar `script=10 style=13`） |
| 门禁（本次） | `python verify-design.py ./pages` | 75 项（66🟡 / 9🔵 / **0🔴**） |
| 门禁（HEAD 基线） | `git archive HEAD pages` → /tmp 同口径复跑 → 逐条 diff | **新增 0 / 消失 0**（唯一 diff 行是 `gaps.log` 路径，非问题） |

收尾：`git checkout -- pages/gaps.log` 已还原；`/tmp/headpages` 已删。

---

## 三、交付物清单

| 路径 | 内容 |
|---|---|
| `mg-work/r83/apply83.py` | 本轮补丁（视图块 + CSS + JS + `PRIOR` + `meta_guard` + `strip_all` 幂等自证） |
| `mg-work/r83/avatar.before.html` | 改前基线（541 277 字符） |
| `mg-work/r83/raw/design_1389-18518.png` | ★ 权威视觉参考（488×990，裸 ID 取的） |
| `mg-work/r83/raw/1389-18518__svg_*.svg` | 5 件设计素材 |
| `mg-work/r83/raw/{c_header,c_icons_r1,c_ico_delete,c_ico_right,c_confirm_r3,c_scrollbar}.png` | 逐项放大图 |
| `mg-work/r83/ev/p_hs.js` | 全项探针（几何 + 交互，返回 JSON） |
| `mg-work/r83/ev/open_view.js` | 只开栏进视图的最小探针（给截图用） |
| `mg-work/r83/ev/impl_hs.png` | 实现侧截图（`screenshot "#av-chat-drawer"` = 元素截图，480×944） |
| `mg-work/r83/ev/cmp_hs.png` | 对照图：设计稿 \| 实现 \| 50% 叠图 |
| `mg-work/r83/acceptance.md` | 本文件 |

⚠ `mg-work/check-syntax.py`、`mg-work/mgfetch.py` 仍是**未提交的常驻工具**（`?? `）。

---

## 四、下一轮待办

1. **r83 的 `ROWS` 是占位数据**（照抄设计稿 7 条文案）—— 真实数据接入后只改 `apply83.py` 的 `ROWS` 一个数组。
2. r82 遗留的 r81 三条未拍：① 触发器 logo `#3491FA` + 白「P」；② 浮窗 7 条用设计稿新 7 色；③ 浮窗右缘对齐触发器右缘。
3. r81 的 7 条空间文案仍是占位（设计稿 14 个 `text/title` 全是 `props="{}"`）→ 真名给出后只改 `apply81.py` 的 `SPACES`。
4. 既有遗留：r79 `r74-ripple` 死代码；r77 滚动条 hover 无反馈 + `.td-browse` 未跟随 `#DAE3ED`；
   r74 摇晃 / X 自转 300ms 上限；r72 全屏 + 浏览态 `Esc#1` 关两层；`pages/gaps.log` 与页面不同步。
5. **r80–r83 全部未 commit / push**，等邵先生发起。

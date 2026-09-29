# r72 验收证据 · Esc 层级裁决

**日期**：2026-09-29
**改动**：`pages/task-detail.html`（+13 行，纯 JS，零 CSS 改动）
**补丁**：`mg-work/r72/apply72.py`（幂等，复跑 `应用 0 项 / 跳过 2 项`）

---

## 一、问题与根因（已复核，HANDOFF 原表述修正）

**现象**：浏览态（右侧文件预览栏展开）按真实 `Esc` → 直接跳 `kanban.html`，预览栏关不掉。

**根因**：两条监听同在 document 冒泡段，执行顺序＝注册顺序。

| 监听 | 注册时机 | 行为 |
|---|---|---|
| 页尾 Esc 链 | 同步 `<script>`，**页面初始化即注册**（最早） | 链尾 `location.href = 'kanban.html'` 直接导航 |
| 浏览侧栏 Esc | **懒注册**（首次开侧栏才挂） | `setOpen(false)` |

⇒ 页尾链先跑并开始导航，`setOpen(false)` **根本没机会执行**（不是"条件不满足"，是页面已在跳走）。

> HANDOFF 原写"顺序更晚，setOpen(false) 永远跑不到"——方向对，但更准确的说法是"页尾链先触发导航"。
> 旁证：同页 `data-td-ctx-open` 分支被同一问题逼出 `e.__tdCtxHandled` 事件标记补丁（第 54 轮）。

---

## 二、改法（为何不用「捕获段 + stopPropagation」）

捕获段能抢优先级，但要**新引入一条捕获段监听**，且必须自己重排"谁是最高层浮层"
（编辑弹窗 / 更多菜单 / 协作模态 / 转派浮窗 / 右键菜单 / 对话框弹层…各占一条捕获监听），
条件漏一项就会出现"一次 Esc 关两层"。

**改用：复用页尾链既有的派发模式。** 页尾链本来就用
`document.dispatchEvent(new CustomEvent('td:close-*'))` 通知各浮层侧
（`td:close-image-preview` / `-edit` / `-coop` / `-dispatch` / `-ctx` / `-popovers`）。
本轮新增一层 `td:close-browse`，插在**「全屏」分支之后、「跳转」分支之前**：

- 位置即优先级 —— 链上所有浮层都关完，最后才轮预览栏；再按一次才真的回看板 → 符合「Esc 逐层关闭」
- **全屏态既有语义一字未动**
- 不新增捕获段监听 → 零优先级冲突面
- 与链上其他分支同样只 `return`（不 `stopPropagation`），风格一致

浏览侧栏侧新增 `document.addEventListener('td:close-browse', () => setOpen(false))`。
连按两次安全：第一次进 `pane.is-closing`（240ms 后才摘 `is-browse`），第二次被
`if (pane.classList.contains('is-closing')) return;` 挡住；第三次 `is-browse` 已摘 → 正常回看板。

---

## 三、行为验收矩阵（`file://` 直开 + **真实按键** `agent-browser press Escape`）

| # | 场景 | 改前基线 | 改后 | 判定 |
|---|---|---|---|---|
| A | 浏览态 · Esc#1 | `page:""`（**已在跳转**） | `isBrowse:true→isClosing:true`，`page:task-detail.html` | ✅ 修复 |
| B | 浏览态 · Esc#1 后等 2s | 已跳 kanban | `isBrowse:false`，`page:task-detail.html` | ✅ 收起完成 |
| C | 浏览态 · Esc#2 | — | `page:kanban.html` | ✅ 回看板 |
| R1 | **非浏览态** · Esc#1 | 跳 kanban | `page:kanban.html` | ✅ 未破坏 |
| R2 | **全屏态**（非浏览）· Esc#1 | 退全屏不跳页 | `fs:false`，`page:task-detail.html` | ✅ 未破坏 |
| R3 | 全屏 + 浏览态 · Esc#1 | `fs:false` + `isBrowse:false`（**一次关两层**） | 同左 | ⚠️ **既有问题，非本轮引入** |

原始 JSON 采样：
```
[A] 开预览栏:      {"isBrowse":true, "isClosing":false,"page":"task-detail.html"}
[A] Esc#1 后立即:  {"isBrowse":true, "isClosing":true, "page":"task-detail.html"}   ← 改前此处置为 page:""
[B] Esc#1 后等 2s: {"isBrowse":false,"isClosing":false,"page":"task-detail.html"}
[C] Esc#2 后等 2s: {"isBrowse":false,"isClosing":false,"page":"kanban.html"}
[R3] Esc#1:        {"fs":false,"isBrowse":false,"page":"task-detail.html"}
改前 R3 Esc#1:     {"fs":false,"isBrowse":false,"page":"task-detail.html"}   ← 与改后一致 ⇒ 既有
```

---

## 四、静态校验（`verify-design.py ./pages`）

| | 改前 | 改后 |
|---|---|---|
| 问题总数 | **75** | **75** |
| critical | **0** | **0** |
| `gaps.log` 条目（归一化去行号） | 68 行 / 28 类 | 68 行 / 28 类 |

**归因 diff（改前跑 vs 改后跑，去行号归一化）：新增 0 类 / 消失 0 类 ⇒ 零新增条目。**
> ⚠️ 坑：直接 diff 仓库版 `gaps.log` 会失真 —— 仓库那份是 **r71 之前**的快照（r71 收尾时
> `git checkout` 还原过），差异里混着 r71 的改动。必须用「本轮改前 / 改后」各跑一次。

`pages/gaps.log` 已 `git checkout` 还原，工作区不再有它的改动。

---

## 五、截图

| 文件 | 内容 |
|---|---|
| `01-browse-open-1920.png` | 1920 视口，浏览态展开（改后渲染正常） |
| `02-after-esc1-still-task-detail.png` | Esc#1 后：预览栏收起、**仍在任务详情页**（未跳看板） |

---

## 六、触及的脚本标签计数

插入载荷不含任何 `<style` / `</style` / `<script` / `</script` / `</body` / `</html` 字面
（脚本内置 `guard()` 强制校验）。标签计数 Δ 全为 0。

> 本页基线 `<script` = 9 / `</script` = 8，**本身就是 9v8**（React bundle 内有转义的
> `<\/script>` 字面量）→ 故断言只做「与基线一致」，不做「配平」。

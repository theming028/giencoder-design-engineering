# r73 · 需求 3 验收：顶栏 tablist 的 tab 切换「跨页接力滑动」

口径（用户拍板）：**跨页接力滑动** —— 目标页加载后滑块先渲染在旧位置、再滑到新位置。
改动：9 页各注入 `<script id="r73-tab-relay">`（`mg-work/r73/apply73d.py`，幂等 99/99 自检通过）。

---

## 〇、先纠一个错（本轮的方法论教训）

排查时我先读的是 `span.style.left`（**内联**值），据此报告「task-detail 滑块错位、高亮在研发但滑块停在基础」。
**这个结论是错的。** task-detail.html 里另有一条上一轮留下的规则：

```css
body:has(.td-wrap) [role="tablist"] > span[aria-hidden] { left: 62px !important; width: 124px !important; }
```

它用 `!important` 把滑块**钉**在 dev 位（同时另两条钉了 `base`/`dev` 的文字色）。
React 的内联值虽然停在 `2px`，**渲染位置一直是 62px（正确）**。

> **规则**：判断视觉位置只看 `getBoundingClientRect()` / `getComputedStyle()`，
> **不能看 `element.style.*`** —— 内联样式会被 `!important` 规则压掉。

因此本块**不做任何纠偏/对齐**，纯加动效；经用户确认后 `4px→8px`、浮窗动效等 r73 其余改动不受影响。

### 9 页滑块渲染位置：改前 = 改后（零位移）

| 页面 | 选中 | 改前 滑块渲染 | 改后 滑块渲染 | 内联 left |
| --- | --- | --- | --- | --- |
| base.html | base | 2/124 | 2/124 | 2px |
| dev.html | dev | 62/124 | 62/124 | 62px |
| kanban.html | dev | 62/124 | 62/124 | 62px |
| req-kanban.html | dev | 62/124 | 62/124 | 62px |
| **task-detail.html** | dev | **62/124** | **62/124** | **2px**（被 !important 压住） |
| avatar / automation / skills / settings | base | 2/124 | 2/124 | 2px |

（`滑块渲染 = 相对 tablist 的 left/width`，取自 `getBoundingClientRect()`）

---

## 一、为什么原来「没有动效」

外壳组件 `On()` 里滑块本来就带弹簧过渡：

```js
useLayoutEffect(() => h(activeTab), [activeTab]);
// h(): { left: btn.offsetLeft, width: btn.offsetWidth }
// style: transition: left .2s cubic-bezier(.34,1.56,.64,1), width .2s 同曲线
// onClick: n!==e && (h(n), setTimeout(() => navigate(t.to), 200))   ← 「先滑 200ms 再跳页」
```

但页尾「页签跳转兜底」脚本在 document **捕获阶段**就 `preventDefault + stopPropagation + location.href`，
React 的 `onClick` 收不到事件 ⇒ **直接跳页**，200ms 的滑动永远播不出来。
用户看到的「没有动效」= 目标页冷启动时滑块**直接出现在终点**。

## 二、做法（不跟 `!important` 抢 left/width）

| 阶段 | 动作 |
| --- | --- |
| 出发页 | `window` 捕获阶段（**早于** document 捕获的跳转兜底）记下滑块的**渲染矩形** + 当前页签 key → `sessionStorage`（带时间戳，10s 内有效） |
| 到达页 | 算位移 `dx = 出发位置 - 当前位置` → `transition:none` + `translate: dx 0`（**摆回旧位置**）→ 隔两帧 `transition: <弹簧>` + `translate: 0 0`（**滑到目标**） |

**为什么用 `translate` 而不改 `left/width`**：task-detail 的 `left/width` 被 `!important` 钉死，内联值写不动；
`translate` 不在那些规则的管辖范围内 ⇒ 同一套逻辑 9 页通用，也**不用去动上一轮留下的钉位规则**。

**为什么用 sessionStorage**：`file://` 下 origin 是 `"file://"`，实测可读写且**跨页面导航保持**
（base.html 写 → dev.html 读到）；`http://127.0.0.1` 预览同源同样可用；取不到时 try/catch 静默降级为「无接力」。

**不动 React**：React 的 style 对象是 `{left,width,transform,transition,opacity}`，**不含 `translate`**，
本块写的 translate 不会被回写；但 `transition` 必须交还（React 认为值没变不会重写）。

## 三、实机证据（agent-browser，file:// 直开，1920×1080）

### 1. 端到端（真点击 → 真跳页）

`sessionStorage` 里是否出现我们的 `translate` 串，是「接力是否命中」的判据（React 从不写 translate）：

| 场景 | 落点页 | 滑块渲染 | 命中接力 |
| --- | --- | --- | --- |
| A 裸开 base.html | base.html | 2/124 | no（`translate` 为空） |
| B base → dev | dev.html | **62/124** | **YES** |
| C dev → base | base.html | **2/124** | **YES** |
| D base → dev（再来一次） | dev.html | **62/124** | **YES** |
| E task-detail → base（含 `!important` 钉位页） | base.html | **2/124** | **YES** |
| F kanban → base | base.html | **2/124** | **YES** |

### 2. 弹簧曲线采样（把过渡拉长到 3000ms 才采得到；200ms 窗口截图工具抓不住）

在真实 dev.html 上复演「钉位 → rAF×2 → 交还过渡并滑向目标」（dx = 2−62 = −60）：

```
anims = ["translate 3000ms"]
相对 tablist 的 left:
  3.5 5 6.5 8 … 30.7 31.8 32.9 33.9 35 … → 过冲到 152.6 → 回落到 62 → 62 62 62 62 62…
```

**过冲到 152.6 再收回 62** 正是 `cubic-bezier(.34,1.56,.64,1)` 的弹性特征；终点**精确落在 62**（= 目标页签 offsetLeft）。

### 3. 中间帧截图（真实渲染）

| 文件 | 白滑块相对 tablist | 说明 |
| --- | --- | --- |
| `08-relay-midflight.png` | left ≈ 33（白像素起点 899，含圆角内缩 ~4px） | 滑块**骑在两个标签之间**——飞行中 |
| `09-relay-settled.png` | left ≈ 66（= 62 + 圆角内缩 ~4） | 落定在「研发工作台」 |

`08c-relay-mid-crop2x.png` 可直接看到白胶囊跨在「基础」与「研发工作台」中间。

### 4. 9 页监听与解析检查

逐页点「非当前选中」的页签，同步读回接力数据 —— 9/9 均写入且 `from` 正确
（base 组页面记 `left:868`，dev 组页面记 `left:928`），说明脚本解析无误、捕获监听已挂上。

## 四、全量回归

```
verify-design.py  ——  r73 前: 75 个问题 / 0 critical
                     r73 后: 75 个问题 / 0 critical
gaps.log 归因 diff ——  归一化后 新增 0 条 / 消失 0 条
```

> ⚠️ 仓库里提交的 `pages/gaps.log` 与 HEAD 的页面**不同步**（缺 20 条），
> 直接拿它当基线会得出「新增 22 条」的假结论。
> 正确基线 = 从当前页去掉 r73 三个注入块（base.html 取 `mg-work/r73/before/base.html`）重建的 `/tmp/r73-pre/pages`。

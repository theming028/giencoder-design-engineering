# r75 验收 · 基础工作台下拉菜单与浮窗的「显示 / 关闭」动效（需求 7 补齐）

**需求原文**
> 基础工作台的所有下拉菜单和浮窗（比如"giencoder-select-popup giencoder-popup-open"之类的）都没有研发工作台里的那种显示/关闭的动效，需要与研发工作台那边的保持一致；

**用户拍板的两项范围口径**
1. 页面范围 → **仅基础工作台 `pages/base.html`**（改动最小、回滚最快）
2. 动效参数 → **保留设计系统原生**（开 200ms + 弹性缓动 / 关 150ms），不另造数值

| 项 | 值 |
|---|---|
| 补丁 | `mg-work/r75/apply75.py`（**纯 CSS**，注入 `<style id="r75-base-css">`；三版迭代，v2 留档 `apply75.v2.py`） |
| 改前基线 | `mg-work/r75/before/base.html` |
| 改动页数 | **1**（base.html） |
| 状态 | ✅ 落地 + 逐帧实测；**未 commit / 未 push** |

---

## 一、根因（全部实机取证，非推断）

### 1.1 base.html 的浮层完整清单（口径：`[aria-haspopup]/[aria-expanded]/[role=combobox]`）

恰好 **6 个触发器**：

| # | 控件 | 载体 | 修前状态 |
|---|---|---|---|
| 0 | 「+」添加内容 | `[role=menu]` 180×92 | ✅ 进场已有 `r74-pop-in`（r74 落地） |
| 1 | 「技能」面板 | `[role=listbox]` 760×320 | ✅ 进场已有 `r74-pop-in` |
| 2 | 标准模式 | `.giencoder-select-popup` | ❌ 硬跳 |
| 3 | DeepSeek-V4-Pro（模型） | `.giencoder-select-popup` | ❌ 硬跳 |
| 4 | 工作目录 | `.giencoder-select-popup` | ❌ 硬跳 |
| 5 | 默认权限 | 自研 `[role=listbox]` | ❌ 完全无动效 |

另有 1 处顶栏门户（`body > div[position:fixed][z-index:1000]`，无 `aria-haspopup`）：✅ 进场已有 `r74-pop-in`。

### 1.2 三个标准下拉为什么「硬跳」——过渡没起跑

实测该元素**关闭态带一条内联样式**，值就是 `display: none;`（`getAttribute('style')` 原文如此）。
⇒ 元素**从来没有被渲染过** ⇒ 打开那一帧没有可插值的起点 ⇒ 整条过渡**不启动**
（实测 `getAnimations()` 全程为空、首帧即到终值，**进、出两个方向都是硬跳**）。

### 1.3 「默认权限」为什么完全没动效

它是**按需挂载**：打开才插入 DOM、关闭即被移除，自身只有一条**无时长**的 transition。

### 1.4 ★ 关于「研发工作台里的那种动效」——用户前提需要更正的一处

- 研发工作台（`task-detail.html`）里的 **`.giencoder-select-popup` 打开同样是硬跳** ——
  同一套设计系统过渡在那边**也没跑起来**（变量隔离实验：手动只加开态类、不碰内联样式，
  `getAnimations()` 仍是空，`opacity` 直接为 1）。
- 研发工作台里**真正在动**的是 r73 给**自研**浮层 `.td-add-pop` / `.td-skill-pop` 加的那套配方：
  `[hidden]` 目标值 + `transition: … display 160ms allow-discrete` + `@starting-style`。
- 而**数字分身页（`avatar.html`）里同一个 `.giencoder-select-popup` 是有进/退过渡的** ——
  它没有那条内联 `display:none`。⇒ base 的缺动效属于**「同组件跨页不一致」的真问题**，修得对。

---

## 二、修法（三版迭代，最终纯 CSS 声明式）

### 2.1 v1 失败并回滚
首版用**脚本**在 ghost 里修克隆体的定位 ⇒ 实测退场 ghost **全程不可见**（`op=0`），
且同一原因波及 r74 原有的 ghost。`cp before/base.html pages/base.html` 回滚，改为纯 CSS。

### 2.2 v2（三段落，落地）
```css
/* A. 让设计系统原生过渡起跑：把内联 display:none 让位给「不可见态」 */
.giencoder-select-popup { display: block !important; }

/* B. 「默认权限」进场：复用 r74 已有关键帧 */
[role="listbox"][aria-label="权限选择"] { animation: r74-pop-in 160ms cubic-bezier(0.34,0.69,0.1,1) both; }

/* C. 退场 ghost：外壳与内容一律静止，内容再铺满外壳 */
[data-r74-ghost] * { animation: none !important; transition: none !important; }
[data-r74-ghost] > * { position:absolute !important; left/top:0 !important; width/height:100% !important;
                       right/bottom:auto !important; margin:0 !important; transform:none !important;
                       max-height:none !important; }
```

### 2.3 v3（本轮补的一行，**根因是新查清的**）
```css
[data-r74-ghost] { animation: none !important; }   /* ← 外壳自己也要静止 */
```

**为什么必须补这一行**：ghost 外壳是「挂在 `body` 下 + 内联含 `position: fixed`」的容器，
而 r74 的 ① 号进场规则正是**按内联样式特征**写的：

```css
body > div[style*="position: fixed"][style*="z-index: 1000"] { animation: r74-pop-in … }
```

JS 写的 `cssText` 是 `position:fixed;…;z-index:1000`（**无空格**），
但**浏览器会把 `style` 属性序列化后回写**（`position: fixed; …; z-index: 1000`，**带空格**），
而**属性选择器匹配的是序列化后的值** ⇒ 只要被克隆浮层的层级值恰好是 1000，外壳就会命中这条规则。

实测（空壳实验，最干净的对照）：

```
A 空壳（z-index:1000）        anims=1  animationName=r74-pop-in   ← 命中
B 带 listbox 内胆的空壳       anims=1  effect.target===shell      ← 命中（与内胆无关）
真 ghost 外壳                 matches(fixed+1000)=true            ← 命中
```

后果：外壳同时挂「r74-pop-in 淡入」与脚本的「退场淡出」两条动画，**都作用于 opacity**。
当前浏览器把**后创建**的脚本动画排在合成顺序更后 ⇒ 脚本退场胜出 ⇒ 看上去是对的，
但这属于**「靠顺序侥幸正确」**，不能留。加入 v3 那一行后 `animationName=none`、只剩 1 条脚本动画。

> 顺带纠正 v2 注释里的一处**错误归因**：v2 曾把「退场不可见」写成「淡入 × 淡出相乘恒为 0」。
> 实测外壳的 `opacity` 一直就是**纯退场曲线**（`1 → 0.757 → 0.441 → …`，与无该动画的场景逐帧吻合），
> 不是乘积。**v1 退场不可见的真主因是克隆体定位漂移后被外壳 `overflow:hidden` 裁掉**。
> 注释已在 v3 一并改正。

### 2.4 为什么不做「关掉节点就不动」的判断
- **3 个标准 select 本来就不产生 ghost**：关闭时 React 只是给**祖先**加内联 `display`，
  **节点不移除** ⇒ 不触发 r74 的快照机制 ⇒ 退场天然由设计系统原生过渡承担（150ms）。
- **「默认权限」会产生 ghost**：React 按需卸载、节点真被摘掉。
- ⇒ ghost 修正只服务于「React 卸载型」浮层，不影响 select 的路径。**两条路各自都是对的。**

---

## 三、验收证据

### 3.1 三个标准下拉 · 进场（rAF 逐帧，三者曲线一致）

| 时刻(ms) | 3 | 19 | 36 | 52 | 69 | 86 | 103 | 121 | 136 | 153 |
|---|---|---|---|---|---|---|---|---|---|---|
| `opacity` | 0 | 0 | **0.188** | 0.425 | 0.675 | 0.821 | 0.894 | 0.936 | 0.962 | 0.978 |
| `translateY` | 4px | 4px | 2.62px | 1.55px | 0.74px | 0.17px | **−0.174px** | −0.350px | **−0.390px** | −0.340px |

- 过渡属性 = `opacity + scale + translate`；时长 ≈ **200ms**
- `translateY` **越过 0 到 −0.39px 再回落** ⇒ 弹簧（过冲）特征，与设计系统原生一致
- 三个下拉（标准模式 / 模型 / 工作目录）数值**逐位相同**

### 3.2 三个标准下拉 · 退场（≈150ms，多带 `visibility`）

| 时刻(ms) | 16 | 32 | 49 | 66 | 82 | 99 | 117 | 132 | 149 |
|---|---|---|---|---|---|---|---|---|---|
| `opacity` | 0.727 | 0.386 | 0.173 | 0.085 | 0.043 | 0.019 | 0.007 | 0.001 | **0** |
| `translateY` | 0.87px | 2.32px | 3.24px | 3.62px | 3.81px | 3.91px | 3.97px | 3.99px | **4px** |

`transitionProperty` 比进场多一项 `visibility` ⇒ 150ms 后落到不可见；无过冲（单调回位）。

### 3.3「默认权限」进场（`r74-pop-in`，196ms 到 1）

`0 → 0.241 → 0.559 → 0.793 → … → 1`（与同页「添加内容」「技能面板」同一套参数）

### 3.4 退场 ghost（修后）

| 帧 | 外壳 `opacity` | 外壳 `anims` | 内胆 `opacity` | 内胆 `anims` | 内胆定位 | 内胆在外壳内 |
|---|---|---|---|---|---|---|
| f0 | 1 | **1** | 1 | **0** | `absolute / 0px / 0px` | ✅ |
| f1 | 0.759 | 1 | 1 | 0 | 同上 | ✅ |
| f2 | 0.439 | 1 | 1 | 0 | 同上 | ✅ |
| f3 | 0.206 | 1 | 1 | 0 | 同上 | ✅ |
| … | … | 1 | 1 | 0 | 同上 | ✅ |
| f9 | 0.000 | 1 | 1 | 0 | 同上 | ✅ |
| f13 | 已自毁 | — | — | — | — | — |

- v2 时该场景外壳 `anims=2`、首帧 `opacity=0`；**v3 降到 `anims=1`、首帧 `opacity=1`** ✅
- 场景覆盖：`[0] 添加内容 180×92`、`[1] 技能面板 760×320`、`[5] 默认权限 280×126` 均有 ghost；
  `[2][3][4]` 三个标准 select **无 ghost**（走原生过渡，见 2.4）。

### 3.5 视觉取证（冻结帧逐像素比对）

打开态与 ghost 首帧（`a.pause(); a.currentTime=0`）截图裁同一区域：

| 区域 | 尺寸 | 有差异像素 | 平均通道差 | 最大通道差 |
|---|---|---|---|---|
| 浮层实体（280×126） | 280×126 | **2.12%** | **0.029 / 255** | **4 / 255** |
| 内部（内缩 12px） | 256×102 | 0.56% | 0.016 / 255 | 4 / 255 |

差异**全部集中在边缘**（左右列、顶边、底边）⇒ 抗锯齿 + ghost 外壳 `overflow:hidden` 裁掉投影所致；
**浮层本体近乎逐像素一致**。几何亦完全重合（ghost 与外壳 rect 逐位相同：`517,532,280,126`）。
> 首版曾报 20.8% 差异，是因为裁剪框含浮层**之外**的桌面背景（那时 ghost 整体不可见），已重做。

### 3.6 误伤检查

- 正常态 `document.querySelectorAll('[data-r74-ghost]').length` = **0**
- 正常态 `[data-r74-ghost] *` 命中元素数 = **0** ⇒ 该规则**只对 ghost 生效**，不碰正常 DOM
- 顶栏门户：`height` 恒为 0 且**关闭后节点不移除** ⇒ 从不产生 ghost ⇒ 与 v3 无交集；
  其进场 `r74-pop-in` 实测正常（`opacity 0.89 → 1`）
- r74 的三处进场（顶栏门户 / 添加内容 / 技能面板）：`[0][1]` 场景 OPEN 行确认浮层正常出现，未受影响

---

## 四、门禁

`verify-design.py`（必须传目录）：

| | base.html 条目 |
|---|---|
| 改前（`mg-work/r75/before`） | `1 issues` / `🔵 [CRAFT-SLOP] 检测到 55 处渐变` |
| 改后（`./pages`） | `1 issues` / `🔵 [CRAFT-SLOP] 检测到 55 处渐变` |

⇒ **逐条完全一致，零新增**（本轮注入的 CSS 不含任何 `gradient` 字样，渐变计数未变）。
其余页面的 warning（avatar / dev / kanban / req-kanban / task-detail）属 r74 及更早轮次遗留，本轮文件未动。
跑完已 `git checkout -- pages/gaps.log` 还原。

---

## 五、本轮新踩的坑（已沉淀 `PLAYBOOK.md` P3.7 / skill）

1. ★ **ghost 外壳会被「按内联样式特征写」的选择器误命中** —— 因为**属性选择器匹配序列化后的 `style` 值**
   （JS 写的无空格 `z-index:1000` 会被回写成带空格的 `z-index: 1000`）。
2. **r74 注释里「相乘恒为 0」是错误归因**；真主因是**定位漂移被 `overflow:hidden` 裁掉**。
3. **同一元素上 WAAPI 与 CSS 动画争同一属性**时按创建顺序合成、**脚本动画（后创建）胜出** ——
   但这是隐式依赖，要在选择器层面直接排除，别靠顺序。
4. **r74 的 `live()` 门槛（`rect > 12px`）让顶栏门户从不进快照**（其 `height` 恒 0）⇒
   SEL 里那条 `body > div[style*="position: fixed"]` 实际是**防御性**的，不要被注释误导。
5. **`agent-browser eval` 支持 `await Promise`** ⇒ 探针写成 `async` IIFE 可**一次调用内闭环**
   （点击 → 等待 → 逐帧 rAF 采样），彻底绕开「跨调用丢状态」。本轮全部探针已改此写法。
6. **`DOMRect` 不可迭代** —— `[...el.getBoundingClientRect()]` 抛 `TypeError`，要逐字段取。
7. **原生 select 浮层「关闭不移除节点」** ⇒ 不进 ghost 通路；ghost 只服务 React 卸载型浮层。

---

## 六、材料清单

- 补丁：`mg-work/r75/apply75.py`（当前版）、`apply75.v2.py`（留档）、`before/base.html`（改前基线）、`base.v2.html`（v2 产物留档）
- 探针：`mg-work/r75/ev/` —— `dbg2.js`（select 关闭后节点状态）、`dbg3.js`（**6 场景全量普查**）、
  `dbg4/5/6.js`（ghost 动画构成 / 空壳对照 / v3 候选验证）、`dbg7/8/9.js`（顶栏门户）、
  `v1.js`（3 个 select 逐帧）、`shot.js`（冻结帧截图）
- 证据图：`ev/crop/open-full.png`、`ev/crop/frozen-full.png`、`ev/crop/gh-AB-v3.png`、`ev/crop/gh-AB-v3-3x.png`
- 原始输出：`ev/out-dbg3-v3.txt`、`ev/out-v1-v3.txt`、`ev/out-dbg7/8/9.txt`

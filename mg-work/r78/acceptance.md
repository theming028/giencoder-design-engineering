# r78 验收报告

**需求（邵先生一次给 2 项）**

1. 基础工作台 main 容器的波点效果：点击 `class="flex flex-1 flex-col items-center justify-center px-6"` 容器范围及相关元素时，**不应该触发涟漪动效**。
2. 该涟漪效果**还是太明显，还要减半**。

**改动文件**：`pages/base.html`（**仅此一页** —— 涟漪脚本与涟漪样式都只存在于 base.html）

**补丁**：`mg-work/r78/apply78.py`（2 项；复跑 = `应用: 0 项 | 跳过: 2 项`，md5 不变）
**改前基线**：`mg-work/r78/before/*.html`（9 页，= r77 交付态）

---

## 一、需求 1 · 欢迎态主内容块不触发涟漪

### 1.1 取证

**这个容器是什么** —— 实测 `main.dot-bg` 的结构：

```
main.dot-bg  (268,48 1164×844)   class="min-w-0 flex-1 h-full overflow-hidden rounded-lg border bg-white dot-bg border-[#ECEEF2]"
└─ div.relative.flex.h-full.min-w-0.flex-col.overflow-hidden  (269,49 1162×842)   ← main 的**唯一**直系子
   ├─ div.flex.flex-1.flex-col.items-center.justify-center.px-6   (269,49 1162×760)  ← ★ 邵先生点名
   │  ├─ div.pointer-events-none.text-center        → LOGO img + h1「有什么工作任务要处理？」
   │  └─ div.mt-8.flex.w-full.flex-col.items-center.gap-2 → 输入卡（composer 白卡）+ 技能胶囊 + 文件/权限行
   └─ div.pb-6.text-center.text-xs                  (269,809 1162×83)   ← 版权区三行（r77 需求 3 那一段）
```

即：**main 只有两块** —— 点名容器（760px，含全部正文内容）+ 版权带（83px）。点名容器占 main 的 90%。

**触发链**（r74 页尾脚本，`document` capture 阶段监听 `pointerdown`）：

```js
if (!t.closest('main.dot-bg')) return;                       // ① 必须在 main 内
if (t.closest('button, a, input, textarea, select, ...')) return;  // ② 不在可交互控件上 ⇒ 视为「空白处」
```

判定只有这两条 ⇒ 欢迎态里**除输入卡本身外的一切空白**（LOGO 上方、问候语四周、卡片两侧 181px 边距、卡片下方）
都算子 ② 的「空白处」，都会起涟漪。而涟漪层是 `position:absolute; inset:0; z-index:0`（定位元素），
LOGO / 问候语是 `static` ⇒ **涟漪点会画在它们之上**，观感就是"点哪儿都在内容上泛点"。

### 1.2 修法

在页尾脚本里**追加一条提前返回**（放在 ② 之后，不改原有任何判定）：

```js
/* 第 78 轮 · 需求 1：欢迎态主内容块（LOGO + 问候语 + 输入卡 + 技能胶囊）整块不算「空白处」 */
if (t.closest('.flex.flex-1.flex-col.items-center.justify-center.px-6')) return;
```

- 用**点名的 class 串**做复合选择器（`closest()` 会同时命中容器自身**及其任意后代** ⇒ 覆盖"及相关元素"）。
- 源码里该 class 串**恰 1 处**；运行时 `querySelectorAll` 命中 **1 个**，且就在 `main.dot-bg` 内 ⇒ 无误伤面。
- 不新增元素、不新增事件、不改判定顺序；CSS 零改动。

### 1.3 实机验证

用 `document.elementFromPoint(x, y)` 取**真实命中元素**再 dispatch（关键：直接 dispatch 在 `main` 上会让
`e.target = main`，绕过整条判定链，测出来全是假阳性 —— 见 PLAYBOOK P3.10）。

| # | 点击点 | 实际命中元素 | 在点名容器内 | 涟漪节点数 |
|---|---|---|---|---|
| 1 | (715,120) 容器上空白 | `DIV.flex.flex-1.flex-col.items-center…` | ✅ | **0** |
| 2 | (715,285) LOGO 上 | `DIV.flex.flex-1.flex-col.items-center…` | ✅ | **0** |
| 3 | (715,327) 问候语上 | `DIV.flex.flex-1.flex-col.items-center…` | ✅ | **0** |
| 4 | (300,400) 容器左空白 | `DIV.mt-8.flex.w-full.flex-col.items-center.gap-2` | ✅ | **0** |
| 5 | (715,465) 输入卡内 | `TEXTAREA.min-w-0 resize-none…` | ✅ | **0** |
| 6 | (715,570) 技能胶囊行 | `DIV.flex.items-center.gap-[8px].pt-[6px]` | ✅ | **0** |
| 7 | (715,855) 版权带 | `P` | ❌ | **1** |
| 8 | (300,860) 版权带 | `P` | ❌ | **1** |
| 9 | (275,850) 版权带 | `P` | ❌ | **1** |

- 点 1~6（含空白、LOGO、问候语、输入卡、胶囊行、容器 padding）**全部 0**；连续点 5 个容器内点后
  `main` 内**无任何残留节点**（`[0,0,0,0,0]`）。
- 点 7~9（点名容器**之外**）仍正常起涟漪 ⇒ 功能没有被整页关掉。
- 容器内点击前后整帧比对：除**既有时间噪声**外无差异（见 §3.2）。

> ⚠️ **可起涟漪的区域只剩底部 83px 版权带**（`y 809~892`）—— 因为点名容器占 main 的 90%。
> 若邵先生要的是"欢迎态完全不触发"，再排除版权带即可（等于关闭本页涟漪），一句锚点的事。

---

## 二、需求 2 · 涟漪强度再减半

### 2.1 修法

新增页尾块 `<style id="r78-base-css">`（**注入在 `</body>` 前、r77 块之后** —— 同为 `.r74-ripple` 0-1-0，
只能靠文档顺序取胜），只改点色 α 一项：

```css
.r74-ripple {
  background-image: radial-gradient(circle, rgba(var(--gray-9), 0.14) 1.7px, transparent 1.7px);
}
```

`0.28 → 0.14`。**其余全部不动**：点径 1.7px、环带 mask（r76 那套 `max(比例×r, r−固定值)` 整流公式）、
半径上限 480px、时长 300ms。

### 2.2 强度核算

描点色 `gray-9` = `rgb(43,43,43)`，底色点阵白底合成 `rgb(247.5)`（实测）。α 与「逐点色差 Δ」在本组合下**成正比**
（Δ = (底色 − 描点色) × α，两项都不变）：

| 版本 | α | 白底合成 | Δ（理论） |
|---|---|---|---|
| r76 | 0.62 | rgb(166) | ~116 |
| r77 | 0.28 | rgb(196) | ~55 |
| **r78** | **0.14** | **rgb(212)** | **~28** |

### 2.3 实机 A/B（同点、同帧、各用各页基线）

点击点 `(715,860)`（版权带内），`t = 160ms`，视口 1440×900，两版基线帧 **md5 完全相同**
（`0d04bd3d5198230da6253edb23a06d3e` ⇒ 帧间无噪声，可比）。

| 指标 | before（r77，α0.28） | after（r78，α0.14） | 比值 |
|---|---|---|---|
| 环带逐点 Δ | 37.0 | **19.8** | **53.5%** |
| 全画幅平均通道差 | 0.1522 | **0.0780** | **51.3%** |
| 变化像素数（≥6） | 5218 | 4877 | 93% |
| 峰值 | 70 | **40** | 57% |

- 计算属性回读：`rgba(43, 43, 43, 0.14) 1.7px`，`background-size 16px 16px`，`z-index 0` ✓
- 环带**形态保持**（差分×4 放大呈空心环，逐帧扩大），只是每点更淡。

---

## 三、回归

### 3.1 通过项

| 项 | 结果 |
|---|---|
| 涟漪节点播放完自毁 | before 0 → during 1 → after **0** ✓ |
| `prefers-reduced-motion` 降级 | `animation-duration` = `0.001s`，节点仍自毁（after 0）✓ |
| 涟漪层级 | `z-index` 仍为 **0**（仍在对话框之下，r77 需求 5a 未破）✓ |
| 涟漪点阵网格 | 仍 `16px 16px`（与底色点阵对齐，r77 需求 4 未破）✓ |
| 其他 8 页 | **零改动**（涟漪脚本/样式只在 base.html）✓ |
| 交互控件仍不触发涟漪 | 原判定 ② 原样保留 ✓ |

### 3.2 一个需要说明的"假差异"

容器内点击前后整帧比对出现 **164 个像素**差异，bbox = `x 236~249, y 275~447`（**在 main 之外**，落在 aside 内）。

- 定位：该点命中 `SPAN.shrink-0 text-[11px] [color:var(--color-text-3)]`（aside 里的时间/角标行）。
- 判定：**同一次会话连拍两张、不做任何操作**，同一区域照样差 **172 个像素**（峰值 165）⇒ **既有时间噪声**
  （页面自带的一处微弱动效/闪烁），**与本次改动无关**。
- ⇒ "容器内点击零效果"成立。

---

## 四、门禁

```
./pages         : 75 个问题（66🟡 / 9🔵 / 0🔴）
./mg-work/r78/before : 75 个问题（66🟡 / 9🔵 / 0🔴）
```

逐条 diff（剥目录前缀 + 剥行号）后**只剩 2 行差异**：

1. base 的 `🔵 CRAFT-SLOP`：渐变 **61 → 62**（r78 新增的那条 `radial-gradient`；info 级、非阻断）；
2. `📄 Token 缺口记录` 的**路径行**（`./pages/gaps.log` vs `./mg-work/r78/before/gaps.log`）。

⇒ **零新增问题**。`git checkout -- pages/gaps.log` 已还原，`before/gaps.log` 已清理。

---

## 五、回滚

```bash
cp mg-work/r78/before/base.html pages/base.html     # ⚠️ 文件名必须与原页面同名
```
（其余 8 页本轮未改，无需回滚。）

---

## 六、材料清单

| 类型 | 路径 |
|---|---|
| 补丁 | `mg-work/r78/apply78.py`（幂等，2 项） |
| 改前基线 | `mg-work/r78/before/*.html`（9 页） |
| 探针 | `mg-work/r78/ev/rip78.js`（`__MODE='enum'` 逐点枚举 / `'fire'` 取帧） |
| 证据 | `ev/cmp.png`（涟漪 A/B 并排：实帧 + 差分×4）、`ev/before-*.png` / `ev/after-*.png`（原始帧）、`ev/base-full-1440x900.png`（欢迎态全屏） |
| 门禁 | `ev/gate-after.txt` / `ev/gate-before.txt` |

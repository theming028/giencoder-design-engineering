# -*- coding: utf-8 -*-
"""
r67 记忆维护：
① 把 MEMORY.md §5.2~5.4 的量测方法论**移入** skill `design-pixel-measure`（知识不丢，只是换更合适的载体）
② MEMORY.md §5.2~5.4 精简为「指针 + 本项目已定值」
③ 把本轮新得的 4 条取证技法追加进 skill `css-pseudo-state-evidence`
"""
import io
import os
import sys

MEM = '.workbuddy/memory/MEMORY.md'
SK_DPM = '/Users/shaoyuming/.workbuddy/skills/design-pixel-measure/SKILL.md'
SK_EVD = '/Users/shaoyuming/.workbuddy/skills/css-pseudo-state-evidence/SKILL.md'

OLD = """### 5.2 逐像素回推 SVG 图标的换算法
设计稿导出图常是 1.5×。若图标最终以 `viewBox="0 0 24 24"` 渲染在 16px 盒里，则 **1 逻辑 px = 1 viewBox 单位**
（16/24 × 1.5 = 1，正好抵消）。所以：
```
viewBox_x = device_x − 锚点_device_x        # 锚点取图标最左/最上的描边中线
viewBox_y = device_y − 锚点_device_y
```
读形方法：把目标区域 **ASCII 化打印**（`#` < 150 / `+` < 210 / `.` < 243 / 空格 白），比看放大 PNG 精确得多
—— 斜切 vs 圆角、圆弧圆心、线段端点都能一次读准。
**圆角 vs 斜切**：量同一段对角线的 Δx/Δy，≈ 则圆角；如 3:5 则直斜切（r51 的 tab 图标右上角）。

### 5.3 设计稿量测口径（详见 skill `design-pixel-measure`）
- 导出 PNG 常为**非整数倍缩放**且**带 alpha** → 必须先 `Image.alpha_composite(纯白底, src)`，
  否则 `convert('RGB')` 把透明区变黑、误判成"黑色色块"；坐标一律 `/缩放比`。
- ⚠️ **同一份设计稿里不同节点的缩放比可能不同**（r52：`836:26404` 是 **3×**、`1350:18310` 是 **1.5×**）
  → **不要跨节点套用**。判定：拿节点已知逻辑尺寸除 PNG 像素（492/164 = 3.000 ✓）；
  交叉验证：中文墨迹高 ÷ 缩放 = 字号（42/3 = 14px = body-3 ✓）。
- **结构量测**：逐行/逐列打印"颜色变化点" → 分隔线位置、面板边界、内间距、缩进步长一次读全，
  比看图目测可靠得多。
- **线条等效色反推**：1px 线在 1.5× 下摊到 2 行 → `C = 255 − 两行墨量合计 / 1.5`
  （顶栏底线墨量 30 → 235 ≈ #EBEBEB，正合项目既有"结构发丝线"档）。
- **半倍（0.5×）合成色反解**：低分辨率图上取色会与底色混合 → `原色 = 合成读数 × 2 − 底色`。
  **判定优先级：DOM `getComputedStyle` 读数 > 设计稿像素反推**（前者永远是真理）。
- **文本墨迹定位**：在某 x 区间内取暗像素的 min/max x = 文字盒起点（含字距），可反推 padding。
- ⚠️ **正文有换行时先做纵向 shift 微扫找最优偏移**再解读残差（r65：`sy=16` 是最优解）。
- ⚠️ **设计稿说"内间距 N px"时务必同时核对容器总宽**：padding 与内容宽是一对约束
  （树容器 296 = 20 + 内容 256 + 20）；只给 256 宽的容器加 20 padding 会把内容压到 216。
  遇这种歧义 → 按设计稿还原并**显式标注宽度也改了**，同时给回退口径。
- ⚠️ **`get_screenshot` 导出节点图默认 2×**：量测前先用**边框像素 #E5E5E5（229±3 灰阶）**定位卡片外框，
  不要用 `<250` 阈值（会把投影光晕算进去）。
  **口径陷阱**：量到的"白区宽"是**内容区**，CSS `width` 默认 `border-box` —— 1px 边框各少 1px
  → 实测 180 要写 `182px`（r54 写 180 导致少 2px，r55 修正）。

### 5.4 圆角定值只能「渲染标定 + SSD 反查」（r65 定稿）
先渲染已知半径（2/4/5/6/7/8/10/12/14/16）的 fill+border / fill / panel+shadow 三种块做 2× 截图，
再把设计稿角部区块与各标定块**逐像素 SSD 取最小**。
⚠️ 实测**首行偏移法系统性偏小 0.5~0.9px、角部面积法在小半径完全失真**，两者都**不可用于定值**
（r65 结论：面板 16 / 卡片与输入框 8 / 按钮 6，且与 Tailwind 默认档位无关）。
⚠️ **「设计稿 vs 实现」对比图必须先对齐锚点再裁**：先量出各自栅格里的同名锚点，再以该锚点为心按**相同逻辑尺寸**
各裁一块。❌ 各自按"墨迹 bbox"裁 —— 抗锯齿会把浅像素算进 bbox，两端膨胀量不同 → 宽高比不同 → 形状一致却看着"不一样"。"""

NEW = """### 5.2~5.4 量测口径 → **已提升为 skill `design-pixel-measure`**（r67 移出本文件）
原 5.2（逐像素回推 SVG 的换算）/ 5.3（量测口径 10 条）/ 5.4（圆角 SSD 反查）已整段移入该 skill
（含 alpha 合成、非整数倍缩放比、结构量测、线条等效色反推、半倍合成色反解、文本墨迹定位、
 换行 shift 微扫、容器总宽与 padding 的配对约束、`get_screenshot` 默认 2× 与 #E5E5E5 边框定位、
 border-box 差 1px、圆角渲染标定法、对比图须先对齐锚点再裁）。
👉 **接这类活儿之前先读该 skill**，本文件不再复述。

**本项目已定值（直接可用，不必重推）**
- 圆角：**面板 16 / 卡片与输入框 8 / 按钮 6**，与 Tailwind 默认档位无关。
- 图标：`viewBox="0 0 24 24"` 渲染进 16px 盒时 **1 逻辑 px = 1 viewBox 单位**（16/24 × 1.5 = 1 正好抵消）；
  锚点取图标最左/最上的描边中线。
- ⚠️ **同一份设计稿不同节点的缩放比可能不同**（`836:26404` = 3×、`1350:18310` = 1.5×）→ **不要跨节点套用**。
- ⚠️ 判定优先级永远：**DOM `getComputedStyle` 读数 > 设计稿像素反推**。"""

txt = io.open(MEM, encoding='utf-8').read()
c = txt.count(OLD)
if c != 1:
    sys.exit('✗ MEMORY.md §5.2~5.4 锚点命中 %d 次' % c)
n0 = len(txt.encode())
txt = txt.replace(OLD, NEW, 1)
s2 = txt.encode()
io.open(MEM, 'w', encoding='utf-8').write(txt)
print('MEMORY.md §5.2~5.4 → 指针：%d → %d 字节 (%+d)' % (n0, len(s2), len(s2) - n0))

# ---------- ① 方法论移入 skill ----------
SK_ADD = """

---

## 6. 量测口径细则（r67 从项目 MEMORY 提升，原样保留）

### 6.1 逐像素回推 SVG 图标的换算法
设计稿导出图常是 1.5×。若图标最终以 `viewBox="0 0 24 24"` 渲染在 16px 盒里，则 **1 逻辑 px = 1 viewBox 单位**
（16/24 × 1.5 = 1，正好抵消）。所以：
```
viewBox_x = device_x − 锚点_device_x        # 锚点取图标最左/最上的描边中线
viewBox_y = device_y − 锚点_device_y
```
读形方法：把目标区域 **ASCII 化打印**（`#` < 150 / `+` < 210 / `.` < 243 / 空格 白），比看放大 PNG 精确得多
—— 斜切 vs 圆角、圆弧圆心、线段端点都能一次读准。
**圆角 vs 斜切**：量同一段对角线的 Δx/Δy，≈ 则圆角；如 3:5 则直斜切。

### 6.2 通用量测口径（10 条）
- 导出 PNG 常为**非整数倍缩放**且**带 alpha** → 必须先 `Image.alpha_composite(纯白底, src)`，
  否则 `convert('RGB')` 把透明区变黑、误判成"黑色色块"；坐标一律 `/缩放比`。
- ⚠️ **同一份设计稿里不同节点的缩放比可能不同**（`836:26404` 是 **3×**、`1350:18310` 是 **1.5×**）
  → **不要跨节点套用**。判定：拿节点已知逻辑尺寸除 PNG 像素（492/164 = 3.000 ✓）；
  交叉验证：中文墨迹高 ÷ 缩放 = 字号（42/3 = 14px = body-3 ✓）。
- **结构量测**：逐行/逐列打印"颜色变化点" → 分隔线位置、面板边界、内间距、缩进步长一次读全，
  比看图目测可靠得多。
- **线条等效色反推**：1px 线在 1.5× 下摊到 2 行 → `C = 255 − 两行墨量合计 / 1.5`
  （顶栏底线墨量 30 → 235 ≈ #EBEBEB，正合"结构发丝线"档）。
- **半倍（0.5×）合成色反解**：低分辨率图上取色会与底色混合 → `原色 = 合成读数 × 2 − 底色`。
  **判定优先级：DOM `getComputedStyle` 读数 > 设计稿像素反推**（前者永远是真理）。
- **文本墨迹定位**：在某 x 区间内取暗像素的 min/max x = 文字盒起点（含字距），可反推 padding。
- ⚠️ **正文有换行时先做纵向 shift 微扫找最优偏移**再解读残差（实测 `sy=16` 是最优解）。
- ⚠️ **设计稿说"内间距 N px"时务必同时核对容器总宽**：padding 与内容宽是一对约束
  （树容器 296 = 20 + 内容 256 + 20）；只给 256 宽的容器加 20 padding 会把内容压到 216。
  遇这种歧义 → 按设计稿还原并**显式标注宽度也改了**，同时给回退口径。
- ⚠️ **`get_screenshot` 导出节点图默认 2×**：量测前先用**边框像素 #E5E5E5（229±3 灰阶）**定位卡片外框，
  不要用 `<250` 阈值（会把投影光晕算进去）。
- **口径陷阱**：量到的"白区宽"是**内容区**，CSS `width` 默认 `border-box` —— 1px 边框各少 1px
  → 实测 180 要写 `182px`（某次写 180 导致少 2px）。

### 6.3 圆角定值 = 渲染标定 + SSD 反查
先渲染已知半径（2/4/5/6/7/8/10/12/14/16）的 fill+border / fill / panel+shadow 三种块做 2× 截图，
再把设计稿角部区块与各标定块**逐像素 SSD 取最小**。
⚠️ 实测**首行偏移法系统性偏小 0.5~0.9px、角部面积法在小半径完全失真**，两者都**不可用于定值**
（本项目结论：面板 16 / 卡片与输入框 8 / 按钮 6，且与 Tailwind 默认档位无关）。
⚠️ **「设计稿 vs 实现」对比图必须先对齐锚点再裁**：先量出各自栅格里的同名锚点，再以该锚点为心按
**相同逻辑尺寸**各裁一块。❌ 各自按"墨迹 bbox"裁 —— 抗锯齿会把浅像素算进 bbox，两端膨胀量不同
→ 宽高比不同 → 形状一致却看着"不一样"。
"""

with io.open(SK_DPM, 'a', encoding='utf-8') as f:
    f.write(SK_ADD)
print('skill design-pixel-measure 已追加 §6（%d 字节）' % len(SK_ADD.encode()))

# ---------- ② 本轮取证技法移入取证 skill ----------
EVD_ADD = """

---

## 6. 过渡/缓动的取证（r67 新增）

- ⚠️ **验证"过渡是渐进的"必须用「页内一次性采样」**：`派发事件 → sleep → eval` 会误判 ——
  实测 agent-browser 每次 eval 的 CDP 往返有 50~150ms，足以吃掉 260ms 的过渡，读到的永远是终值、
  被误判成"瞬间跳变"。正解：**同一个 eval 里**派发事件 + 用 `setTimeout` 采 8 个点写进 `window.__s`，
  再另起一次 eval 取回。实测曲线 `10% → 18.39 → 33.79 → 47.78 → 65.89 → 83.53 → 90%`
  （5 个中间态 + 明显 ease-out 前快后慢特征）。
- **「某一层零变化」的最强证明 ＝ 把它推到画布外再逐像素比**：验证"原有效果没被动过"时，
  把新增层的圆心/位置设成 `-500%` 让它彻底移出 ⇒ 画面只剩原层，与改前对比
  **目标容器内最大差异 = 0**；若剩余差异与「同页连拍两张」的对照实验**行数 / y 区间完全一致**，
  即可判定是页面自身噪声、与改动无关。
- **diff 热力图**：以"目标特效被移除"的那张为基线，对多个状态的截图求 `ImageChops.difference`
  并**增强 N×**（原始差异很淡 → `point(lambda v: min(255, v*7))`），一眼看出特效的作用范围与位置是否跟随。
- ℹ️ **`agent-browser set media` 可直接模拟媒体特性**（比手写 CDP 省事）：
  `agent-browser set media [dark|light] [reduced-motion]` —— 实测 `transitionProperty` 由
  `--dot-x, --dot-y` / `0.26s` 变为 `none` / `0s`；恢复用 `set media light`。

## 7. `@property` 驱动的指针跟随（r67 完整配方）

用于「某层跟随鼠标」的效果（点阵光斑跟随指针、聚光灯、跟随高亮等）。三个硬约束：

1. 想让 **transition 对自定义属性生效** ⇒ 必须 `@property` 注册**类型**，否则值瞬间跳变；
2. **JS 改不了伪元素样式** ⇒ 变量必须写在**主元素**上，且该属性 **`inherits` 必须为 `true`**
   才能传给 `::before/::after`；
3. transition 写在**主元素**上才可靠（值先平滑、再被伪元素继承），别写在伪元素上。

```css
@property --dot-x { syntax: '<percentage>'; inherits: true; initial-value: 50%; }
.dot-bg { position: relative; transition: --dot-x 260ms ease-out, --dot-y 260ms ease-out; }
.dot-bg::before {
  content: ''; position: absolute; inset: 0; pointer-events: none;
  background-size: 20px 20px;
  -webkit-mask-image: radial-gradient(circle 420px at var(--dot-x) var(--dot-y), #000 0%, rgba(0,0,0,.55) 42%, transparent 78%);
          mask-image: radial-gradient(circle 420px at var(--dot-x) var(--dot-y), #000 0%, rgba(0,0,0,.55) 42%, transparent 78%);
}
@media (prefers-reduced-motion: reduce) { .dot-bg { transition: none; } }  /* 交互响应保留，只去掉缓动 */
```

⚠️ **页尾同步脚本取不到还没渲染的 DOM**：单页 React 产物里，注入的 `<script>` 在文档末尾
**同步执行**时外壳的 `main` 还不存在 → `document.querySelector(...)` 返回 **null**、监听器永远绑不上。
症状极具迷惑性：CSS 全绿、`transitionProperty` 也对、伪元素 mask 也在，**就是不动、变量恒为初始值**。
⇒ 正解＝**文档级事件委托**（`document.addEventListener('pointermove', e => e.target.closest('main.dot-bg'))`），
不必等渲染、也不必 `MutationObserver`；再配 rAF 节流（每帧至多写一次变量）。

⚠️ **层级**：若目标容器 `position: static` 且无 stacking context、其唯一子元素是 `relative`，
则 `::before`（positioned、z-index auto）在 tree order 上位于内容之前 ⇒ 与内容同属绘制步骤 6、
**内容压在其上**，不需要负 z-index。此处**不要**用 `isolation: isolate` 图省事 ——
若页内有 `position:fixed; z-index:9999` 的弹窗，隔离会把 9999 困在容器内、可能被外层元素盖住。
"""

with io.open(SK_EVD, 'a', encoding='utf-8') as f:
    f.write(EVD_ADD)
print('skill css-pseudo-state-evidence 已追加 §6/§7（%d 字节）' % len(EVD_ADD.encode()))

final = io.open(MEM, encoding='utf-8').read()
print()
print('MEMORY.md 现 %d 字节 / %d 行' % (len(final.encode()), len(final.split('\n'))))

# r74 验收报告（8 项需求 · 9 页）

- **轮次**：r74
- **状态**：8/8 落地并实机取证通过；**未 commit / 未 push**
- **设计系统门禁**：`verify-design.py ./pages` = **75 项 / 0 critical**，与改前基线**逐条一致**（唯一差异见 §4.2）；
  `gaps.log` 归一化 diff = **新增 0 类 / 消失 0 类 / 计数零变化**
  ⚠️ 基线口径已修正：**不能取仓库版 `pages/gaps.log`**（那份与 HEAD 页面不同步，见 §4.3）
- **补丁**：`mg-work/r74/apply74.py`（A·9 页）、`apply74b.py`（B·base）、`apply74c.py`（C·avatar / D·task-detail），三者均已复跑验幂等（`应用: 0 页`）

---

## 一、逐项结论

| # | 需求 | 结论 | 关键证据 |
|---|---|---|---|
| 1 | 「新会话」按钮外观全局统一 | ✅ | 4 页按钮盒 `x12 y48 w244 h32` 全同；像素比对 12800 px 仅 180 px 差（均在气泡图标/⌘K 字形边缘），**文字与盒体零差异** |
| 2 | 版权区改三行 | ✅ | 实测三行 `["内容由 AI 生成，请核实重要信息","© 2026 中电金信","中电金信研究院 · 数字构建平台实验室（PAA） · 版本：1.2.5"]`，`data-r74-cr` = `[null,"1","1"]` |
| 3 | 对话框打开→按钮变「关闭对话窗口」+ X 自转一圈 | ✅ | 开：`label="关闭对话窗口"`、`path=[M18 6 6 18, m6 6 12 12]`、`r74-x-spin` 运行中；关：文案与气泡图标均还原 |
| 4 | 头像 hover → 脸摇晃几下 | ✅ | hover 即 `animationName=r74-face-wiggle`、`dur=0.3s`、`origin=50% 78%`；冻结帧 18%/48% 明显左右倾、100% 回正 |
| 5 | 点 main 空白 → 波点水波纹涟漪 | ✅ | 波前半径 54→162→259→340px 线性推进；**径向剖面**证明是环：t=120ms 差异只在 `r120~180`（峰 58 灰阶），`r<120` 与 `r>180` 全 0 |
| 6 | 顶栏两触发器互换 | ✅ | 6 个实际渲染该顶栏的页实测顺序 `侧边栏@0(w24,order1) → 线@36(w1,order2) → 空间@49(w165,order3)` |
| 7 | 基础工作台浮窗补显/隐动效 | ✅ | 进场 `r74-pop-in@160ms`；退场 ghost 抓到（`w175 h89 anims1`），400ms 后自动销毁 |
| 8 | 任务详情 td-right 与 td-browse-slot 同步 | ✅ | 进/出均 200ms 平滑；React 摘类时**所有采样值零变化**；普通态↔一次开合循环后截图**像素完全一致** |

---

## 二、需求 8 的根因与改法（本轮最花功夫的一项）

### 2.1 改前实测（1920×1080，rAF 逐帧采样）

```
展开:  t=0  slot 0    left 1416  rr 8px   bw 1px
       t=9  slot 816  left 600   rr 0px   bw 0px     ← 一帧内到位
收起:  t=0   slot 816  left 600  rr 0px  CLS
       t=195 slot 0    left 600  rr 0px  CLS          ← 预览栏平滑关完，左栏却钉在 600
       t=245 slot 0    left 1416 rr 8px   -            ← React 摘类，三件事一起硬跳
```

**根因（与最初猜测不同，已实测纠正）**：预览栏的**实用宽**并不由它自己的 `flex-basis` 决定，
而是「行宽 − 左栏 − 8px − AI 栏」的余量（`flex: 0 1 0px` + basis 恒大于余量 ⇒ 永远被压到余量）。
展开那一帧左栏被 `min/max-width` 钳死在 600，可用余量当帧就是 816 ⇒ 看着像瞬变；
（其 flex-basis 的 CSS 过渡其实是存在的 —— 冻结帧里能查到。）

### 2.2 改法：只驱动左栏，其余自动跟随

```css
/* ① 展开：左栏从普通态整行宽收窄到 600（放开 min/max 夹子，from 用普通态公式反推） */
@keyframes r74-left-fold { from { flex-basis: calc(100% - var(--td-gap,8px) - var(--td-right-w,480px)); } }
.td-root.is-browse.is-keep-left .td-left { min-width:0; max-width:none; animation: r74-left-fold 200ms var(--td-browse-ease); }

/* ② 收起：左栏改「可伸」的同宽 basis —— 预览栏缩 1px，左栏就长 1px */
.td-root.is-browse.is-keep-left:has(> .td-browse-slot > .td-browse.is-closing) .td-left { flex-grow:1; flex-shrink:0; }

/* ③ AI 栏右缘的圆角/描边：把「还原」的触发点提前到 is-closing 那一帧（原规则 `border-right:0` 会把 style 置 none，必须改写成简写才可插值） */
.td-root.is-browse:has(> .td-browse-slot > .td-browse.is-closing) .td-right { border-right:1px solid var(--td-panel-line); border-top-right-radius:8px; border-bottom-right-radius:8px; }
```

### 2.3 改后实测

```
展开  t=0   slot 0    left 1416 rr 8px   ← 起点 = 普通态，零跳变
      t=8   slot 486  left 930  rr 3.23
      t=24  slot 624  left 792  rr 1.89
      t=57  slot 756  left 660  rr 0.59
      t=214 slot 816  left 600  rr 0px    ← 200ms 到位
收起  t=0   slot 816  left 600  rr 0px  CLS
      t=23  slot 574  left 842  rr 4.78
      t=57  slot 190  left 1226 rr 6.93
      t=197 slot 0    left 1416 rr 8px    CLS ← 200ms 到位
      t=250 slot 0    left 1416 rr 8px    -   ← 摘类：全部数值零变化
```

冻结帧像素坐标（证明三者同帧联动，行内总和恒 1904）：`t=0 chat 1432..1912 → t=200 chat 616..1096`。

---

## 三、需求 5 的形态取证（证明是「环」不是「盘」）

以点击点 (388,932) 为圆心，统计各半径环带「与无涟漪基线的最大通道差」：

```
t=120ms（波前 162px）    t=200ms（波前 259px）
 r<120   0.00 / 峰 5       r<210   0.00
 r120~150 0.23 / 峰 58     r210~240 0.09 / 峰 33
 r150~180 0.28 / 峰 58     r240~270 0.20 / 峰 41
 r>180   0.00              r>300   0.00
```

→ 差异只出现在当前波前附近，**内圈外圈全 0** = 波环在点阵上扩散。
生命周期：`t0=1 → t120=1 → t500=0`（300ms 动画结束自动移除）。

---

## 四、本轮自查出的回归（已修）

第一次跑全量静态校验时，自己的补丁**新增了 21 条告警**：

| 类型 | 数量 | 来源 | 修法 |
|---|---|---|---|
| `TOKEN-GAP` 硬编码字号 | 18（9 页 ×2） | 需求 1 的注入块里写了 `font-size:13px/14px` | 改 `var(--font-size-body-2)`（=13px）/ `var(--font-size-body-3)`（=14px），计算值不变、像素比对仍零差异 |
| `CRAFT-ANIM` >300ms | 3 | 涟漪 900ms、摇晃 640ms、X 自转 520ms | 全部收到 **300ms**；涟漪的半径上限从「扫到最远角（1086px）」改为**固定 360px**，波前速度仍是 1.2px/ms ⇒ 观感不变的同时满足 craft.md |

修完后 `75 项 / 0 critical` 与改前完全一致。**教训：补丁跑完必须自己先跑门禁，别把新告警留给用户。**

### 4.2 唯一残留差异：base.html 渐变计数 52 → 55（`CRAFT-SLOP`，info 级）

三门禁报告逐行 diff（剥行号后）**只有 1 行不同**：`base.html` 的「检测到 N 处渐变」由 52 变 55。
三条全部来自本轮注入的 `r74-base-css`，且**是几何基元不是装饰**：

| # | 声明 | 用途 |
|---|---|---|
| 1 | `background-image: radial-gradient(...1.5px...)` | **画波点本身**（1.5px 圆点 / 20px 间距） |
| 2 | `-webkit-mask-image: radial-gradient(...)` | **环形遮罩**（只露波前一圈） |
| 3 | `mask-image: radial-gradient(...)` | 同上（标准属性版） |

判据结论：该检查的意图是「品牌色一屏不超过 3 处 / 无意义渐变背景」，这三处是**遮罩与点阵的必需基元**，
且该文件改前（52）就已越过 `>=3` 阈值 ⇒ **门禁结论不变，只是计数数字变化**，判定为**可接受**，不做规避
（去掉 `-webkit-` 前缀只能降到 54，仍越阈值，纯属为凑数牺牲兼容性）。

### 4.3 ⚠️ 基线口径纠错：仓库版 `pages/gaps.log` 与 HEAD 页面**不同步**

收尾复核时发现：`mg-work/r74/gaps-before-r74.log` 与 `git show HEAD:pages/gaps.log` **逐字节相同**，
而那份 45 条记录里**根本没有 `avatar.html` / `task-detail.html` 的条目** —— 但这两个文件在 HEAD 就存在。
即：**仓库里提交的 `gaps.log` 是更早轮次的快照，从未随页面同步**。
⇒ 拿它当"改前基线"会得出「新增 21 条」的假结论（本轮一度触发）。

**更正后的正确流程**（与 `PLAYBOOK.md` 里 r72 那条一致）：
把 `mg-work/r74/before/`（9 页改前备份）当目录跑一次 `verify-design.py` ⇒ 得到**真基线** ⇒
归一化（剥 `:行号`）后与当前 `pages/gaps.log` 做**集合 + 多重集**双口径 diff。
实测结果：**新增 0 类 / 消失 0 类 / 计数零变化**（两边各 65 条）—— **结论"零新增"成立，但先前引用的工件是错的**。

- 真基线：`mg-work/r74/gaps-before-r74.log`（68 行，由 `before/` 重建）
- 被误用的陈旧版：`mg-work/r74/gaps-before-r74-REPO-STALE.log`（48 行）
- **待办建议**：`pages/gaps.log` 要么重新提交一次与页面同步的版本，要么加进 `.gitignore`，
  否则每轮都会重复踩这个坑。

---

## 五、待用户拍板 / 已知边界

1. **涟漪尺度**：本轮把涟漪从「扫满整个 main」改为「固定 360px 水珠涟漪」（原因见 §4）。
   若你更想要"整片背景一起晃"的观感，可以调大上限 —— 但那会突破 300ms 上限（需同时把速度压回来）。
2. **摇晃时长 300ms**：craft.md 的硬上限。若想要更慢更"黏"的摇晃（如 600ms），会打红 `CRAFT-ANIM`，需你确认是否接受例外。
3. **涟漪叠加多个点**：每次点击叠一层，各自 300ms 后自行销毁（实测无残留）。
4. 仍挂着的两项历史待拍板（r72 起）：全屏+浏览态 Esc#1 一次关两层；avatar 双开 + 视口 ≤1100 时 main 被压到 ~0。

---

## 六、材料清单

| 内容 | 路径 |
|---|---|
| 补丁 A/B/C+D | `mg-work/r74/apply74.py` / `apply74b.py` / `apply74c.py` |
| 改前基线（r74 起始） | `mg-work/r74/before/*.html`（9 页） |
| 补丁 C/D 前基线 | `mg-work/r74/beforeC/{avatar,task-detail}.html` |
| 改前静态校验基线 | `mg-work/r74/gaps-before-r74.log`（**真基线**，由 `before/` 重建；勿用 `gaps-before-r74-REPO-STALE.log`）+ `/tmp/r74-pre/` |
| 证据脚本 | `mg-work/r74/ev/`（td-seq/td-out/td-pose/td-slowmo、rip2、av-probe-anim、nc-detail/nc-rect、head-order …） |
| 证据截图 | `mg-work/r74/ev/`（tdopen-*、tdclose-*、ncP-*、rz4-*、avp-*、avs-* 及 `crop/` 拼图） |

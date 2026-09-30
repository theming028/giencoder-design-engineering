# r92 验收档案 · 顶栏背景图 / 返回钮深一级 / r85-gt 左距 12px / 完全访问转红

> 日期：2026-09-30 ｜ 落地脚本：`mg-work/r92/apply92.py`（① ④）+ `mg-work/r88/apply88.py`（② ③，r88 未提交 ⇒ 就地返工）
> 工作区：**r88/r89/r90/r91/r92 全部未提交**（按长期约定，不自动 commit / push）

---

## 一、邵先生四条

| # | 原话 | 落地 |
|---|---|---|
| ① | 在基础工作台顶栏 header 上加上一张背景图，图片居右，不重复（`assets/images/bg-img-1.png`） | `header[class*="h-12"]` 加 `background-image / no-repeat / position:right center`（**不写 background-size**）。落 **基础工作台 5 页**：base / settings / avatar / skills / automation |
| ② | 设置页面的「返回」按钮的图标和文字颜色要使用深一级的颜色 | `.r85-back`：`color: #6B6B6B`（gray-7 / neutral-7）→ **`var(--color-text-2)`**（gray-8 `#4E4E4E`）。图标 `fill="currentColor"`、文案 `<span>` 继承 ⇒ 一处改、两件同变 |
| ③ | 设置页面 aside 的「r85-gt」的左间距应该是 12px | `.r85-gt`：`margin: 0 2px 8px` → **`margin: 0 2px 8px 12px`**（只改左值） |
| ④ | 基础工作台 main 容器对话框的「默认权限」如果选择的是「完全访问」，在外面显示的「完全访问」与其图标都要呈现为红色 | base.html **React 源**两处锚点加条件（见第三节）+ 注入 `.r92-perm-danger` |

---

## 二、① 顶栏背景图

### 素材实测（`mg-work/r92/ev/img-analyze.py` / `dot-size.py`）

| 项 | 值 |
|---|---|
| 尺寸 | **1580 × 134**（RGBA，但整幅不透明） |
| 平底 | `#F6F8FA`（246,248,250）—— 占图宽 **67.5%** |
| 点阵 | `#DDE3EB`（221,227,235）—— **4px 方点 / 8px 点距**（4 点 + 4 隙），密度自左向右递增 |
| 点阵起点 | 源图 `x = 1067`（占 32.5%） |
| 顶栏自身底色 | `#F4F5F6`（244,245,246）—— 与素材平底 **Δ=(2,3,4)** |

### 铺法

```css
header[class*="h-12"] {
  background-image: url("../assets/images/bg-img-1.png");
  background-repeat: no-repeat;
  background-position: right center;
}
```

* **不写 `background-size`** = CSS 默认 `auto` = 素材原尺寸 —— 与邵先生「居右、不重复」两句原话一一对应（没提尺寸就不动尺寸）。
* 视口 1440 时素材 1580 宽 ⇒ 图片铺满整条顶栏（多出的左 140px 被裁掉）；视口比 1580 更宽时右对齐，左端露出素材外的顶栏底色。
* **选择器刻意不是裸 `header`**：`avatar.html` 有 5 个 `<header>`（av-main-head / av-hs-bar / td-right-bar / td-browse-bar），`task-detail.html` 有 4 个 —— 裸标签会误伤。
* **范围只落基础工作台 5 页**：研发工作台 4 页顶栏底色是 `#E5EDF5`，素材平底是不透明的 `#F6F8FA`，铺上去会把那一档蓝调整块抹掉。

### 实测（`mg-work/r92/ev/p92-hdr-out.txt`，视口 1920×900）

| 页面 | 分组 | `background-image` | repeat | position | size | 顶栏底色 |
|---|---|---|---|---|---|---|
| base / settings / avatar / skills / automation | 基础工作台 | **有**（`bg-img-1.png`） | no-repeat | 100% 50% | auto | #F4F5F6 |
| dev / kanban / req-kanban / task-detail | 研发工作台 | **无** | repeat | 0% 0% | auto | #E5EDF5 |

改前（`mg-work/r92/before/*.html` 实测）：`backgroundImage = none`。

### 像素实证（`hdr-dot.py` 在真实顶栏元素截图里量）

* 右缘最暗像素 = `(221,227,235)` = **素材点色 `#DDE3EB`，逐通道相等**。
* 竖直游程 = `DOT 2 / gap 4 / DOT 4 / gap 4 …` ⇒ 点阵**竖直方向被裁掉半格**（素材 134px 高于顶栏 48px，竖直居中取中段 48px；顶/底各留 2px 半格 DOT）。
  1x 下不可辨（见 `raw/r92-hdr-ab.png` 与 `raw/web-hdr-r92-base-zoom.png`）。

### ⚠ 已知几何副作用（待邵先生拍板）

素材平底 `#F6F8FA` ≠ 顶栏底色 `#F4F5F6`（Δ 2~3~4）⇒ 视口宽于 1580 时，图片左缘会留下一条**接缝**：

* 实测（1920 视口）接缝在 **x = 340**：左侧 `(244,245,246)`，右侧 `(246,248,250)`。
* 三种消法（都是一行）：
  1. 把顶栏底色改成素材平底（`header[class*="h-12"]{background-color:#F6F8FA}` —— 但违反「禁硬编码 hex」，需先提 token）；
  2. `background-size: 100% auto`（素材横向铺满，接缝消失，点径变 4×(视口/1580)）；
  3. `background-size: auto 100%`（素材缩到顶栏高 48px ⇒ 566 宽，点阵只占最右 186px，接缝移到 x=1354）。

---

## 三、②③ 设置页两处

### 改前 → 改后（同一视口 1440×900，同一探针 `ev/p92-nav.js`）

| 量 | 改前 | 改后 |
|---|---|---|
| `.r85-back` 的 `color` | `rgb(107,107,107)` = `#6B6B6B` | **`rgb(78,78,78)` = `#4E4E4E`** |
| `.r85-back > svg` 的 `color` | `rgb(107,107,107)` | **`rgb(78,78,78)`** |
| `.r85-back > span` 的 `color` | `rgb(107,107,107)` | **`rgb(78,78,78)`** |
| `.r85-gt` 的 `margin-left` | `2px` | **`12px`** |
| `.r85-gt` 的 `margin-right` | `2px` | `2px`（未动） |
| `.r85-gt` 视口 x（「通用」） | 14 | **24** |
| `.r85-gt` 视口 x（「已归档」） | 14 | **24** |
| `.r85-navi > span` 视口 x | 48 | 48（未动） |

* 颜色阶梯：`#6B6B6B` = `--color-neutral-7`（gray-**7**）→ `--color-text-2` = `--gray-8`（gray-**8**），正好「深一级」。
* 顺带消掉本页**最后一处字面 hex**（硬规则：页面内禁硬编码色值）。
* `.r85-gt` 从 x=14 移到 x=24 后，与 `.r85-navi` 的**图标左缘（x=24）** 对齐（菜单项 `padding: 0 12px`）。

---

## 四、④ 完全访问转红

### 为什么只能改 React 源

触发器是 React 条件渲染，两半色的来源都**不吃后置 CSS**：

| 部位 | 原实现 | 后置 CSS 能否覆盖 |
|---|---|---|
| 图标 | 尾风任意类 `[color:var(--color-text-1\|2)]` | ❌ 任意类是**构建期产物** —— 新增 `[color:var(--color-danger-6)]` 不会进产物 CSS |
| 文字 | 内联 `style={{color: …}}` | ❌ 内联优先级最高（要 `!important`） |

⇒ 就地改压缩后的 React 字符串（先例：r77 需求 3 改 base.html 版权行序）。

```diff
- `size-[14px] shrink-0 `+(l===`perm`?`[color:var(--color-text-1)]`:`[color:var(--color-text-2)]`)
+ `size-[14px] shrink-0 `+(s===`完全访问`?`r92-perm-danger`:(l===`perm`?`[color:var(--color-text-1)]`:`[color:var(--color-text-2)]`))
```
```diff
- style:{color:l===`perm`?`var(--color-text-1)`:`var(--color-text-2)`,lineHeight:`19px`,…},children:s}
+ style:{color:s===`完全访问`?`var(--color-danger-6)`:(l===`perm`?`var(--color-text-1)`:`var(--color-text-2)`),lineHeight:`19px`,…},children:s}
```
外加注入块：`.r92-perm-danger { color: var(--color-danger-6); }`（`#F53F3F` = `--red-6`）。

* 只改**触发器（外面显示的）**；浮层里那两行选项不动。
* 尾风 `chevron`（后缀箭头）不动 —— 邵先生说的是「「完全访问」与其图标」，即文案 + 它前面那把锁。

### 实测（`ev/run-perm.sh`，真鼠标 5 步走）

| 步 | 状态 | 文案 | 文字色 | 图标色 | 图标 class |
|---|---|---|---|---|---|
| T0 | 默认权限（收起） | 默认权限 | `rgb(78,78,78)` | `rgb(78,78,78)` | `…[color:var(--color-text-2)]` |
| T1 | 默认权限（展开） | 默认权限 | `rgb(31,31,31)` | `rgb(31,31,31)` | `…[color:var(--color-text-1)]` |
| **T2** | **完全访问（收起）** | **完全访问** | **`rgb(245,63,63)`** | **`rgb(245,63,63)`** | **`… r92-perm-danger`** |
| **T3** | **完全访问（展开）** | **完全访问** | **`rgb(245,63,63)`** | **`rgb(245,63,63)`** | **`… r92-perm-danger`** |
| T4 | 切回默认权限 | 默认权限 | `rgb(78,78,78)` | `rgb(78,78,78)` | `…[color:var(--color-text-2)]` |

* ✅ 红色 = `rgb(245,63,63)` = `#F53F3F` = `--color-danger-6`，文字与图标**逐通道相等**。
* ✅ 展开态也红（T3），切回即复原（T4）⇒ 是**条件**而非一次性涂抹。
* ✅ **反证（没误伤）**：同页「工作目录 (可选)」那一支在 T0~T4 全程 `rgb(78,78,78)` 不变。
* 取证坑留痕：`.ws-dropdown-hover` 有 **2 个**（工作目录 / 默认权限）⇒ 必须 `.ws-dropdown-hover:has(svg.lucide-lock)` 才精确；第一版探针命中「工作目录」，全部读数都是错的。

---

## 五、「只改了该改的」证据

### 1. 页面级：摘掉本代注入块后与前置基线对比（`ev/localdiff.py`）

| 页面 | 字符数 | r92 注入块 | 摘块后 |
|---|---|---|---|
| avatar / skills / automation | +1113 | 1113 | ✅ **逐字节相同** |
| base.html | 468689 → 470215（+1526） | 1458 | 仅 1 个改动窗口 @241268 = 两处 React 锚点 |
| settings.html | 455725 → 457287（+1562） | 1113 | 仅 1 个改动窗口 = ② 与 ③ 两处（+注释） |

### 2. 像素级：设置页 aside 改前/改后同条件元素截图逐行分组 diff（`ev/diffgrp.py`）

`web-aside-r91sat.png` vs `web-aside-r92-def.png`（均 256×844，同视口 1440×900、同「刚打开、无 hover」状态）：

* 差异 **959 / 72021 = 1.332%**，**共 3 个行组**：
  * `y 10..21  x 11-22, 31-42, 45-56` = 返回钮**箭头 + 返 + 回** 三件变色（②）
  * `y 55..65  x 2-34` = 「通用」右移（③）
  * `y 211..221 x 2-47` = 「已归档」右移（③）
* **零意外**：菜单项、选中底、图标、滚动条全部不在差异里。

---

## 六、四查

| 查 | 结果 |
|---|---|
| 幂等 | `apply88.py` 复跑 `457287 → 457287 (+0)`；`apply88b-fontsize.py` 复跑 **9 页全部「已是目标态」**；`apply92.py` 复跑 **应用 0 / 跳过 8** |
| 语法/配平 | `check-syntax.py pages/*.html` → **9/9 ALL_OK**（style 计数：base 12→14、settings 8→9、avatar 14→15、skills 8→9、automation 8→9，各 +1/+2 与注入数一致） |
| 零影响 | `verify-design.py ./pages` → **75 条**，与 r91 基线 `vd-r91.txt` **逐字节零 diff**（`ev/vd-diff.txt` 为空） |
| 视觉/像素 | ① 9 页范围正确 + 点色逐通道相等；②③ 改前改后表逐项；④ 5 态表 + 反证；aside 逐行 diff 1.332% 三组全对应 |

跑完已清理：`git checkout -- pages/gaps.log`、`git checkout -- mg-work/kanban/r13/chk/ && git clean -f mg-work/kanban/r13/chk/`。

---

## 七、待拍板

1. ★ **① 的范围**：现落**基础工作台 5 页**（按「基础工作台」字面 + 研发工作台顶栏是 `#E5EDF5` 会被素材平底盖掉）。若邵先生要**全站 9 页**，说一声即可（研发页需同时决定要不要把顶栏底色也换掉）。
2. ★ **① 的尺寸**：现为**素材原尺寸**（点径 4px）。若要更细的点或不要那条 x=340 接缝，见第二节三种一行改法。
3. **④ 的红色档位**：现取 `--color-danger-6`（`#F53F3F`，DS 危险色标准档）。若觉得太艳，可降 `--color-danger-5`（`#F76160`）。
4. 沿袭未决：r91 行尾图标色是否精确贴稿（`text-2` vs `--color-neutral-7`）；r90 三处「按 DS 而非设计稿」；24px 极限档工具条溢出 18px；返回钮（高 32 / 圆角 4px）与菜单项（高 36 / 圆角 8px）几何不一致。

---

## 八、文件清单

```
改：pages/base.html      468689 → 470215  sha 0e96b76d884a
    pages/settings.html  455725 → 457287  sha 9905b3fd7fc6
    pages/avatar.html    565038 → 566151  sha a2e0d29caa3c
    pages/skills.html    358535 → 359648  sha 26c11367c9fa
    pages/automation.html 358648 → 359761 sha 09b52bae2f7c
    （dev / kanban / req-kanban / task-detail 本轮零改动）
改：mg-work/r88/apply88.py        ② ③ 就地返工（+ 两段说明注释）
新：mg-work/r92/apply92.py        ① ④
新：mg-work/r92/before/*.html     r92 前置基线（5 页）
新：mg-work/r92/ev/               侦察 / 探针 / 量测 / 拼图 21 个脚本与读数
新：mg-work/r92/raw/r92-aside-ab.png   设置页 aside 改前|改后（2x）
     mg-work/r92/raw/r92-hdr-ab.png     顶栏右 700px 改前|改后（2x）
     mg-work/r92/raw/r92-perm-ab.png    权限触发器 默认|完全访问（3x）
     mg-work/r92/raw/web-hdr-r92-{base,settings,dev}.png
     mg-work/r92/raw/web-aside-r92-{def,backhover,navihover}.png
     mg-work/r92/raw/web-perm-{def,full,full-open,back}-r92.png
```

# HANDOFF · 会话交接卡

> **滚动更新**：每轮收尾时**覆盖重写**（不是 append）。
> **用途**：新会话开局只读这一个文件，就能对齐「现在在哪、下一步做什么」。
> 分工：历史详情 → `YYYY-MM-DD.md`；稳定工作法 → `PLAYBOOK.md`；页面事实 → `PAGES.md`；
> 每次都必知 → `MEMORY.md`。**本文件不占注入预算**（只在需要时 grep/Read）。

- **最后更新**：2026-09-29（**r79 涟漪范围定案 + 目录清理第二轮**；两项**待一并入库**）
- **HEAD**：`1673adf` = `origin/main`（`chore(cleanup): 交接卡同步 …`）—— 之后的工作**尚未提交**。
- **工作区（待入库）**：
  - `M pages/base.html` —— r79 唯一改动页（涟漪排除链加第 4 道闸）
  - `D mg-work/r78/before/*.html` × 8 —— 清理第二轮 T2（与当前页逐字节相同）
  - `?? mg-work/r79/`（apply79.py + before/ + ev/ + acceptance.md）
  - `M mg-work/cleanup-audit-2026-09-29.md`（新增第六章）· `M .workbuddy/memory/{2026-09-29,HANDOFF,PLAYBOOK,PAGES}.md`
- **已入库**：`fde6473`（r72~r78 全量 447 files / 91413 ins）· `27f342c`（补记）· `042e669`（清理第一轮 62 删除）
- **本卡数据源**：`mg-work/r79/acceptance.md`（r79）+ `mg-work/cleanup-audit-2026-09-29.md`（清理审计）

---

## 一、r79 做了什么（涟漪触发范围 · 定案「欢迎态完全不触发」）

| # | 指令 | 修法要点 | 关键实测 |
|---|---|---|---|
| ① | **连版权带也排除** | 在 r74 页尾脚本排除链**再加一道闸**：`if (t.closest('div[class*="pb-6"][class*="text-center"]')) return;`（选择器与脚本 ① 段抓版权容器的**同一个**；源码命中 1、运行时命中 1） | 9 点 A/B：BEFORE 版权带 3 点 `ripple=1` → AFTER **全 0**；**96 点全视口网格 `fired=0`**、最大涟漪数 0 |
| ② | **涟漪点阵加密到 16px** | **无需改动** —— 实测 `.r74-ripple` `background-size` 已是 **`16px 16px`**，与 `.dot-bg` **同值** | 涟漪点 `rgba(43,43,43,.14)` / `1.7px`；cap `480px` / `300ms` / `z-index 0` 全未动 |

**补丁（1 个，幂等：连跑 3 次 = 1 / 0 / 0）**：`mg-work/r79/apply79.py`

### ★★ 范围后果（接手必看，已与邵先生确认）

**真实血缘**（r79 实测）：
```
MAIN.dot-bg                                                   [268,48,1164,844]
  └ DIV.relative flex h-full min-w-0 flex-col overflow-hidden [269,49,1162,842]  ← children 只有这 1 个
      ├ 内容块  DIV.flex flex-1 … px-6                        [269,49,1162,759]
      └ 版权带  DIV.pb-6 text-center text-xs leading-relaxed  [269,808,1162,82]
```
**闸 3（内容块）+ 闸 4（版权带）把 main 内两块全覆盖 ⇒ 本页不再有任何区域能起涟漪，
波点涟漪特效在 base.html 实际已停用。脚本与样式保留不删，便于随时回退。**
⇒ **"要不要顺手删掉这套死代码"是新挂出来的待办**（见第四节）。

---

## 二、★ r79 新踩的坑（已进 PLAYBOOK **P3.11**）

1. **`main.dot-bg.children.length === 1`** —— 唯一子元素是个 flex 外壳，内容块与版权带是**它的**子元素。
   r78 笔记写"main 只有 2 块"，指的是**外壳的子元素**。若按 `host.children` / `matches()` 去匹配版权带
   会**全 false**，从而误判成"选择器写错"。**正解：逐层 dump `getBoundingClientRect` 核血缘 +
   对候选选择器数命中个数（`querySelectorAll(...).length` 必须 = 1）**。
2. **`agent-browser eval` 没有 `--pre`** —— `eval "$(cat probe.js)" --pre "…"` 直接报
   `SyntaxError: Unexpected identifier 'pre'`。**正解：`{ echo "window.__MODE='x'; window.__PTS=[…];"; cat probe.js; } | $AB eval --stdin`**。
3. （沿用 r78 P3.10）**测「点这儿该不该触发」必须 `document.elementFromPoint` 复刻真实 target**；
   改 `<script>` 正文时标签级断言口径 = **计数不变**。

---

## 三、验收结论摘要（全部实机取证）

- **门禁逐条零差异**：`./pages` **75（66🟡 / 9🔵 / 0🔴）**；与 r78 `gate-after.txt` 剥前缀+行号后
  **新增 0 条 / 消失 0 条**（集合 102 = 102）。base 的 `CRAFT-SLOP` 渐变 **62 = 62**（未新增渐变）。
- **标签级计数不变**：`<script` 8→8 · `</script>` 7→7 · `<style` 11→11 · `</style>` 11→11。
- **视觉量化**：版权带裁区（`260,780`–`1440,900`）总绝对差 **83 769**（均 0.2212/像素）；
  **差分包围盒 `(191,11,748,111)`（裁区内）= 绝对 x `451..1008`、y `791..891`**，以点击点 x=715 为中心、
  落在版权带内 ⇒ **差异是涟漪环带，不是页面噪声**（噪声带在 aside `x236–249`，裁区从 x=260 起已避开）。
- `apply79.py` 幂等 ✓；基线 md5 `6f509d2d…` → `c4cb03c4…`；`pages/gaps.log` 已 `git checkout --` 还原。
- 明细见 `mg-work/r79/acceptance.md`。

---

## 四、待用户拍板 / 遗留

1. **★ 新挂出：`r74-ripple` 死代码是否清理** —— 涟漪已无任何触发路径（第 1 节范围后果）。
   可删的是：`<style>` 里 `.r74-ripple` 相关规则 + `@property --r74-rip-r` + `@keyframes r74/r76-ripple-out`
   + `<script id="r74-base-js">` 里的 ② 段。**删了能去掉约 4 KB 与一处 `@property`，但失去"一键恢复特效"的能力。**
   处理纪律（P3.11 ③）：本卡与 `PAGES.md P3.10` 已记净效果，**默认不删**，等拍板。
2. **已定案（不用再问）**：
   - ~~涟漪触发范围~~ → **欢迎态完全不触发**（r79 落地）
   - ~~涟漪点阵 16px~~ → **16px 是有意的**，保持
   - ~~目录清理档 2/3/4/5~~ → **停在这里，都不做**（`git gc` 已无空间可压）
3. **r77 待确认**：滚动条 hover 与默认档同值（**悬停无视觉反馈**）。
   > 旁证：`av-{default,hover,off}-crop` 三张图**像素完全相同** ⇒ 现状确实"静止"。要反馈就得给 hover 一个值。
4. **r77 遗留**：`.td-browse` 未跟随 `#DAE3ED`（只浏览态相接才可见）。
5. **r74 遗留**：摇晃 / X 自转收到 300ms 仍挂着（craft 硬上限，不能再加长）；涟漪半径 cap 480px。
6. **r72 遗留**：全屏 + 浏览态时 `Esc#1` 一次关两层；avatar 双开 + 视口 ≤1100 时 main 被压到 ~0。
7. **可选增强**：把 r75 的「DS 原生过渡配方」推广到 task-detail 的 `.giencoder-select-popup`（一直硬跳）。
8. **目录清理已执行两轮、已停**：第一轮 66 个（1.80 MB）；第二轮 `git gc` `.git` **111→97 MB** +
   9 个 `.DS_Store` + 空目录 + 8 个 `r78/before/*.html` ⇒ **总计 257M → 240M**。
   第二轮 T1（同轮同内容截图 4.16 MB）**逐组复核后驳回 0 个可删** —— 「内容相同」本身常常就是结论。
   ⚠️ **`git gc` 收益必须实测**：预估 30–40 MB、实际 **14 MB**（PNG 已压缩，打包收益≈0）。

---

## 五、下一轮接手清单

- **范围先核实**：同名同构模块（顶栏 / 浮窗 / 下拉 / 滚动条 / 技能浮窗 / **aside 会话项** / **main 的内容块**）
  在多页各有一份，先 `getBoundingClientRect()` + `getComputedStyle()` 核实现状，**不读 `element.style.*`**（P3.5）。
  ⚠️ 实例：涟漪只在 `base.html`（其余 8 页 `r74-ripple` 计数 = 0）。
- ★ **碰"命中判定 / 排除链"前先 dump 真实血缘**，别按"块数"推断层级（**P3.11 ①**）。
- **改页面一律走 `mg-work/rNN/applyNN*.py`** 幂等脚本：先判 NEW/稳定标记 → 再判 `count(OLD)` 精确 → 复跑确认 `应用: 0`。
- **新注入块纪律**：① 注入到 **`</body>` 前**；② 字号/颜色全走 token；③ 动画与 `animation-delay` 都 ≤300ms；
  ④ 新增注释里不得出现被断言的 token / 标签名。
- ★ **动到某个元素前，先 grep 它的文本/标记有没有被页尾脚本 `querySelector` / `closest` 抓过**（P3.9 坑 2）。
- ★ **验证「点 X 不触发 / 触发」类需求，一律用 `elementFromPoint` 复刻真实 target**（P3.10 坑 1）。
- 收尾三件套：`verify-design.py ./pages` **逐条 diff**（剥目录前缀 + 行号）+ `git checkout -- pages/gaps.log`
  + 覆盖更新本文件 + 追加当日 `YYYY-MM-DD.md` + 新坑进 `PLAYBOOK.md`。
- ⚠️ **跨轮复跑整链的已知现象**：旧轮脚本的锚点若已被后续轮次覆盖（如 r76 滚动条 `.24→.20` 被 r77 的
  `.20→.16` 吃掉），旧脚本会**硬退出**（`!! 锚点缺失`）—— **预期行为，不是回归**。
  验证"整链幂等"的正确做法：**比较复跑前后的页面 md5**。要重放历史轮次，必须**从该轮基线按序跑**。
- ⚠️ **仓库卫生待办（已挂 7 轮）**：`pages/gaps.log` 在 HEAD 就与页面**不同步** → 建议**重提同步版**或**加 `.gitignore`**，
  否则每轮收尾都要重建基线绕坑。（每轮只做 `git checkout -- pages/gaps.log` 还原，**刻意没动它**。）
- **默认不自动 commit / push**（2026-09-28 起），需邵先生明确要求。

---

## 六、回滚与取证材料

- **r79 改前基线**：`mg-work/r79/before/base.html` → `cp mg-work/r79/before/base.html pages/base.html`
  （⚠️ 文件名**必须与原页面同名**，否则 file:// 下外壳按名字查路由表会落回 base 壳）
- **r79 补丁 / 探针 / 证据**：`apply79.py`；`ev/rip79.js`（`struct` / `enum` / `grid` / `size` 四模式）；
  `ev/cmp.png`（三栏 = BEFORE / AFTER / 差分×14）· `before-click-160.png` · `after-click-160.png` ·
  `base-full-1440x900.png` · `gate-after.txt`
- **r78**：`mg-work/r78/acceptance.md` + `apply78.py` + `before/*.html` 9 页 + `ev/`
  （⚠️ 其中 8 个 `before/*.html` 已在清理第二轮删掉——它们与当前页逐字节相同；**只剩 `before/base.html`**，
  即 r78 唯一真基线）
- **r77**：`apply77{,b}.py` + `before/*.html`；**r76**：`apply76{,b,c,d,e,f}.py` + `ev/`、`ev2/`；
  **r75**：`apply75.py`；**r74**：`apply74{,b,c}.py`
- **清理审计**：`mg-work/cleanup-audit-2026-09-29.md`（体积构成 / 分级档位 / 截图引用判据 / 两轮执行记录）
- ⚠️ `/tmp/rNN-*` 与 `/tmp/cleanup-backup-*` 是**临时目录，重启即丢** —— 长期回滚请用 `mg-work/` 内材料

---

## 七、环境速记（新会话最容易踩）

- 预览**一律 `file://` 直开**，别用内置预览面板（URL 不带 hash → 渲染出错误的壳）
  ⚠️ **改完页面要带 cache-buster**：`file://.../pages/base.html?v=<ts>`，否则可能读到旧内容
- `verify-design.py` 必须传目录：`python verify-design.py ./pages`；用
  `/Users/shaoyuming/.workbuddy/binaries/python/envs/default/bin/python`
  （系统 python3 无 PIL；managed venv 里 **numpy 已装**）
- ⚠️ **`gaps.log` 的"改前基线"绝不能取仓库版** → 用 `before/` 重建基线目录再 diff
- ⚠️ **`:hover` 在多次独立 agent-browser 调用之间会丢失**（P3.6）
- ⚠️ **CSS transition 无法 `pause()` + `currentTime=` seek**（CSSAnimation 可以）→ 过程帧用「时长放大 20×」慢放法
- ✅ **`agent-browser eval` 支持 `await Promise`**：探针写 `async` IIFE，一次调用内闭环
- ⚠️ **`agent-browser eval` 没有 `--pre`** → 传变量用 `--stdin` 前置拼接（**P3.11 ②**）；也支持 `-b/--base64`
- ⚠️ **`set viewport` 必须排在 `open` 之后**；每次改视口前重新 `open`（上一档残留会污染读数）
- ⚠️ **`$AB open` 之后立刻 `screenshot` 可能拍到上一张页面** → 先 `eval location.pathname` 回读
- ⚠️ **`screenshot` 出来的是 1× 图**（1440×900）—— 裁图坐标直接用 **CSS 像素**，别再 ×2
- ⚠️ **本机 `grep` 查中文一律返回空** → 中文内容用 python 读，`grep` 只用于纯 ASCII 锚点
- ⚠️ **DS 的 CSS 是多行格式**，页面是压缩单行 → 同一处改动的锚点串**在两边不一样**
- CSS 动画时长被 `CRAFT-ANIM` 卡 **≤300ms**（`animation-delay` 也算）；
  `CRAFT-SLOP` 的「N 处渐变」是**纯正则、不区分用途**（`mask-image` 也算）

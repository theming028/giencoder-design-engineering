# HANDOFF · 会话交接卡

> **滚动更新**：每轮收尾时**覆盖重写**（不是 append）。
> **用途**：新会话开局只读这一个文件，就能对齐「现在在哪、下一步做什么」。
> 分工：历史详情 → `YYYY-MM-DD.md`；稳定工作法 → `PLAYBOOK.md`；页面事实 → `PAGES.md`；
> 每次都必知 → `MEMORY.md`。**本文件不占注入预算**（只在需要时 grep/Read）。

- **最后更新**：2026-09-29（**r72–r78 入库 + 目录清理均已推送成功**；工作区干净、已与远程同步）
- **HEAD**：`042e669` = `origin/main`（`chore(cleanup): 删除早期轮次临时截图 …`）——
  平时本卡**不存 hash**（易变），此处因"入库刚发生、下一轮开工前要知道已同步"而记一次。
- **工作区**：**干净**（`git status` 0 项）。已入库三批：
  ① `fde6473` r72~r78 全量（447 files / 91413 ins，约 45MB）
  ② `27f342c` 补记入库结果 ③ `042e669` 目录清理（64 files：62 删除 + 审计报告 + 日志）
- **本卡数据源**：`mg-work/r78/acceptance.md`（r78 逐项结论）+ `mg-work/cleanup-audit-2026-09-29.md`（清理审计）

---

## 一、r78 做了什么（2 项需求，涟漪的「触发范围」+「强度」）

| # | 需求 | 修法要点 | 关键实测 |
|---|---|---|---|
| 1 | 欢迎态主内容块内点击**不触发涟漪** | 在 r74 页尾脚本的排除链后**追加一条提前返回**：`if (t.closest('.flex.flex-1.flex-col.items-center.justify-center.px-6')) return;`（用邵先生点名的 class 串做复合选择器，`closest()` 同时覆盖容器自身 + 其后代） | 容器内 6 个点（空白/LOGO/问候语/输入卡两侧/胶囊行）涟漪节点 **全 0**、连续点完无残留；容器外版权带 3 个点仍 **1** |
| 2 | 涟漪「还要减半」 | 新增页尾块 `r78-base-css`，只改点色 α：`0.28 → 0.14`（点径 1.7px / 环带 mask / cap 480px / 300ms 全不动） | 环带逐点 Δ **37.0 → 19.8（53.5%）**、全画幅平均差 **51.3%**、峰值 70→40 |

**补丁链（1 个，幂等：复跑 = 0 应用 / 全 skip）**：`mg-work/r78/apply78.py`

**★ 本轮的"范围"事实（接手必看）**：`main.dot-bg` 只有 **2 块** ——
① 点名容器 `flex flex-1 … px-6`（`269,49 1162×760`，含 LOGO + 问候语 + 输入卡 + 技能胶囊，**占 main 的 90%**）；
② 版权带 `pb-6 text-center text-xs`（`269,809 1162×83`）。
⇒ 排除 ① 之后，**欢迎态可起涟漪的区域只剩底部 83px 版权带**。这是邵先生明确点的范围；
若他想"完全不触发"，再排版权带即可（等于关掉本页涟漪）。

---

## 二、★ 本轮新踩的坑（已进 PLAYBOOK P3.10，接手前务必看）

1. **测涟漪触发必须 dispatch 到「真实命中元素」**：直接用 `host.dispatchEvent(...)`（host = `main.dot-bg`）
   会让 `e.target = main` ⇒ `closest()` 全返回 null ⇒ **绕过整条排除判定链，测出来全是假阳性**。
   正解：`const hit = document.elementFromPoint(x, y); hit.dispatchEvent(...)` —— 这才是真实点击的 target。
   （顺带自动覆盖了 `pointer-events:none` 的穿透：LOGO 那层是 `pointer-events-none`，
   到点命中就已经是外层容器。）
2. **"点击前后整帧不变"不能只看 md5**：page 自带一处**时间噪声**（aside 内 `x236~249, y275~447` 一条窄竖带，
   同会话连拍两张照样差 ~170 像素）⇒ **必须做"同会话连拍两张"的对照实验**才能把噪声与真实影响分开。
3. **改了脚本正文要断言的标签级计数**：这次改的是 `<script>` 内部 ⇒ 断言口径是
   `<script` / `</script>` **计数不变**（不是风格里常用的 ±1）。别把"插入 style 块"的断言套到逻辑改动上。

---

## 三、验收结论摘要（全部实机取证）

- **门禁零新增**：`./pages` 75（66🟡/9🔵/0🔴）**= `before/` 75**。逐条 diff 后唯一差异：
  ① base 的 `🔵 CRAFT-SLOP` 渐变 `61→62`（新块那条 `radial-gradient`，info 级非阻断）；② gaps.log 的**路径行**。
  `git checkout -- pages/gaps.log` 已还原，`before/gaps.log` 已清理。
- **回归全绿**：涟漪自毁（0→1→0）/ `prefers-reduced-motion`（`0.001s`，仍自毁）/ `z-index` 仍 0（对话框之下）/
  点阵仍 16px（与底色对齐）/ 其余 8 页零改动 —— 均未受影响。
- 明细见 `mg-work/r78/acceptance.md`。

---

## 四、待用户拍板 / 遗留

1. **★ 涟漪触发范围**：排除点名容器后，欢迎态**只剩底部 83px 版权带**能起涟漪。
   若本意是"欢迎态完全不触发"，再排版权带即可；若本意是"涟漪别画在内容上、但仍可点"，
   那应当改**绘制层级**（而不是排除触发）—— 说一声我换方案。
2. **r77 待确认项仍在**：滚动条 hover 与默认档同值（悬停无视觉反馈）；涟漪点阵随波点一起加密到 16px。
3. **r77 遗留**：`.td-browse` 未跟随 `#DAE3ED`（只浏览态相接才可见）。
4. **r74 遗留**：摇晃 / X 自转收到 300ms 仍挂着（craft 硬上限）；涟漪半径 cap 480px。
5. **历史遗留（r72 起）**：全屏 + 浏览态时 `Esc#1` 一次关两层；avatar 双开 + 视口 ≤1100 时 main 被压到 ~0。
6. **可选**：把 r75 的「DS 原生过渡配方」推广到 task-detail 的 `.giencoder-select-popup`（一直是硬跳）。
7. **目录清理的追加档位（已出报告，等拍板）**：见 `mg-work/cleanup-audit-2026-09-29.md`。
   已执行档 = 66 个早期裁剪图/垃圾（1.80 MB，已进废纸篓，`/usr/bin/trash` 可"放回原处"）。
   待选：① **`git gc`**（唯一真能省磁盘的一步，`.git` 72MB loose → 回收 30–40 MB，零风险不删文件）；
   ② 加删 r01–r68 整页截图 61.94 MB；③ 全部零引用截图 87.52 MB；④ ③+`before/` 基线 ≈108 MB（丢回滚能力）。
   ⚠️ ②③④ **不释放磁盘**（blob 仍在 `.git`），要真释放只有重写历史 + `force push`（SOUL 红线，不建议）。

---

## 五、下一轮接手清单

- **范围先核实**：同名同构模块（顶栏 / 浮窗 / 下拉 / 滚动条 / 技能浮窗 / **aside 会话项** / **main 的内容块**）
  在多页各有一份，先 `getBoundingClientRect()` + `getComputedStyle()` 核实现状，**不读 `element.style.*`**（PLAYBOOK P3.5）。
  ⚠️ 本轮实例：`main.dot-bg` 的涟漪**只在 base.html**（其余 8 页 `r74-ripple` 计数为 0）。
- **改页面一律走 `mg-work/rNN/applyNN*.py`** 幂等脚本：先判 NEW/稳定标记 → 再判 `count(OLD)` 精确 → 复跑确认 `应用: 0`。
- **新注入块纪律**：① 注入到 **`</body>` 前**（与既有块对齐，见 P3.9 坑 1）；② 字号/颜色全走 token；
  ③ 动画与 `animation-delay` 都 ≤300ms；④ 新增注释里不得出现被断言的 token / 标签名。
- ★ **动到某个元素前，先 grep 它的文本/标记有没有被页尾脚本 `querySelector` / `closest` 抓过**（P3.9 坑 2）。
- ★ **验证「点 X 不触发 / 触发」类需求，一律用 `elementFromPoint` 复刻真实 target**（P3.10 坑 1）。
- 收尾三件套：`verify-design.py ./pages` 逐条 diff + `git checkout -- pages/gaps.log`
  + 覆盖更新本文件 + 追加当日 `YYYY-MM-DD.md` + 新坑进 `PLAYBOOK.md`。
- ⚠️ **跨轮复跑整链的已知现象**：旧轮脚本的锚点若已被后续轮次覆盖（如 r76 的滚动条 `.24→.20` 被
  r77 的 `.20→.16` 吃掉），旧脚本会**硬退出**（`!! 锚点缺失`）—— **这是预期行为，不是回归**。
  验证"整链幂等"的正确做法是：**比较复跑前后的页面 md5**（r78 实测：`apply76` 退出 + 其余全 skip，
  `base/avatar/task-detail` 的 md5 逐字节不变）。要重放历史轮次，必须**从该轮基线按序跑**。
- ⚠️ **仓库卫生待办（已挂 6 轮 → 本轮仍未处理）**：`pages/gaps.log` 在 HEAD 就与页面**不同步** →
  建议**重新提交一份同步版**或**加 `.gitignore`**，否则每轮收尾都要重建基线绕坑。
  （本次全量入库**刻意没动它**：`git checkout -- pages/gaps.log` 已把它还原到 HEAD 版。）
- **r72~r78：已全量入库** —— commit `fde6473` + push 成功（`6d75a17..fde6473`，34s，无 443 超时）。
  默认仍是**不自动推**，需邵先生明确要求。

---

## 六、回滚与取证材料

- **r78 改前基线**：`mg-work/r78/before/*.html`（9 页）→ `cp mg-work/r78/before/base.html pages/base.html`
  （⚠️ 文件名**必须与原页面同名**，否则 file:// 下外壳按名字查路由表会落回 base 壳）
- **补丁**：`mg-work/r78/apply78.py`（幂等）
- **探针**：`mg-work/r78/ev/rip78.js`（`__MODE='enum'` 逐点枚举触发与否 / `'fire'` 取帧）
- **证据**：`ev/cmp.png`（涟漪 A/B 并排 = 实帧 + 差分×4）、`ev/before-160.png` / `ev/after-160.png` /
  `ev/before-base.png` / `ev/after-base.png`、`ev/base-full-1440x900.png`、`ev/gate-*.txt`
- **r77 材料**：`mg-work/r77/acceptance.md` + `before/*.html` + `apply77.py` / `apply77b.py` + `ev/`
- **r76**：`mg-work/r76/acceptance.md` + `apply76{,b,c,d,e,f}.py` + `ev/`、`ev2/`
- **r75**：`mg-work/r75/acceptance.md` + `apply75.py`；**r74**：`mg-work/r74/acceptance.md` + `apply74{,b,c}.py`
- ⚠️ `/tmp/rNN-*` 是**临时目录，重启即丢** —— 长期回滚请用 `mg-work/` 内的材料

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
- ⚠️ **`set viewport` 必须排在 `open` 之后**；每次改视口前重新 `open`（上一档残留会污染读数）
- ⚠️ **`$AB open` 之后立刻 `screenshot` 可能拍到上一张页面** → 先 `eval location.pathname` 回读
- ⚠️ **本机 `grep` 查中文一律返回空** → 中文内容用 python 读，`grep` 只用于纯 ASCII 锚点
- ⚠️ **DS 的 CSS 是多行格式**，页面是压缩单行 → 同一处改动的锚点串**在两边不一样**
- CSS 动画时长被 `CRAFT-ANIM` 卡 **≤300ms**（`animation-delay` 也算）；
  `CRAFT-SLOP` 的「N 处渐变」是**纯正则、不区分用途**（`mask-image` 也算）

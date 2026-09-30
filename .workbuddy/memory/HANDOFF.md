# HANDOFF · 下一轮接手卡

> **每轮覆盖重写。新会话开局先读这一页，再按需 grep `PLAYBOOK.md` / `PAGES.md`。**
> 最后更新：2026-09-30 20:1x（**r86 ~ r100 已 commit + push：`6a4b0ea..d7e2151`（776 文件 / +156039 行）；r101 两批（十一条 + 七条）已落地并通过四查 + 双视口实测取证，🚫 未提交**）
> ⚠️ **最新一拍 = r101 第二批七条**（同一代**就地返工** `mg-work/r101/apply101.py`；r93 代已提交 ⇒ r101 仍是新一代）：
> ② **`.r93-bar` 毛玻璃**（宿主 `position:relative` + 标题栏 `absolute/backdrop-filter` + 滚动口 `padding-top:44px`）·
> ② 顶栏装饰图 `background-size: 70%`（新块 `r101-hdr-css`，落 **6 页**）· ③ 骨架屏去掉浅灰容器 · ④ 渐隐 40→56px ·
> ⑤ 汇总卡菜单与产物卡**合一**（r99 ⑦ 那张 4 项菜单退役）· ⑥ 折叠头 hover 右箭头（间距 8px）· ⑦ 展开回弹动效。
> 逐条实测见 `mg-work/r101/acceptance.md` 第八~十二节。
> ★★ 本轮最要紧的三条经验（都已进 PLAYBOOK P3.32）：
>   ① **跨行块的剥离正则必须带 `re.S`** —— 漏了不会「摘不掉」，而是自检报「摘块后基线里仍残留标记」（极易误判成检测写错）；
>   ② **`agent-browser click` 会被毛玻璃标题栏接住**（标题栏盖住滚动口最上 44px）⇒ 触点先 `scrollIntoView({block:'center'})`；
>   ③ 上一代已提交时**别回改旧补丁** —— 新起一块同特异性、靠文档顺序取胜的块（`r101-hdr-css` 压 `r92-hdr-css` 就是这么干的）。
> 工作区：**未提交**（6 页 ` M`：base / conversation / avatar / skills / automation / settings + `?? mg-work/r101/`）。`origin/main` 仍在 **`d7e2151`**。
> ⚠ **r89 / r90 / r91 / r92 对设置页的改动、r93 需求 1 对字号机制的改动，全都是 r88 的就地返工**（r88 未提交 ⇒ 按硬规则不另起代数，直接改 `mg-work/r88/apply88.py` 与 `apply88b-fontsize.py`）。
> ⚠ **r94 ~ r100 全部是 r93 代就地返工**（落在 `mg-work/r93/apply93.py`）；**r101 起是新代**（`mg-work/r101/apply101.py`，承接 r93 代的产物）。
> ⚠ **★ `pages/` 下每个页面都是「完全自包含」的独立 html**（顶栏 + aside + 外壳各一份，**没有共享布局、没有真实路由**）⇒ 新开一页 = **由源页净底重建（不复制）**；页面间跳转靠每页内嵌 `<!-- SHELL-NAV-FIX v5 -->` 的 `ROUTE` 表 + `hashchange`（见第十节）。

---

## 一、当前工作区状态

**当前未提交 = 仅 r101**（会话详情页十一条微调）。r86 ~ r100 已于 18:2x 提交并推送（`6a4b0ea..d7e2151`，776 文件 / +156039 −532）。

| 改动 | 内容 |
|---|---|
| ` M pages/conversation.html` | **634719 → 671386 字符**（+36667；LF 文本 `sha 544ed8156a78`；`script=9 style=15`）；注入块 id 换代 `r93-conv-*` → **`r101-conv-css` / `r101-conv-js`**；r101 十一条见下 |
| ` M pages/base.html` | **471444 → 471447 字符**（+3；LF 文本 `sha f35fd612df52`）＝只有当页 nav 脚本 id 由 `r93-nav-js` 换成 **`r101-nav-js`**（注释对同步换名），功能逐字不变 |
| `?? mg-work/r101/` | `apply101.py`（含 `--revert` / `--dry`）/ `acceptance.md`（**七节**：十一条逐条实测 + 设计稿取数 + `GENS` 逐代摘除 + 四查 + 待拍板 + 本轮踩坑）/ `before/`（2 份 r101 前置基线：`conversation-r101.html` / `base-r101.html`）/ `ev/`（`p101*` 探针 + `p101fin.sh/.log` 终态取证 + `vd-r101a/b.txt` + `check_ow.py` / `sample_t12l.py`）/ `raw/`（骨架屏 / 右键菜单 / 渐隐带 / 投影剖面 / 设计稿对照裁片） |
| `?? .workbuddy/memory/2026-09-30.md` | 当日原始日志（含 r92 / r93 / **r93 ④** / r94~**r101** 各段） |

> 历史（已提交的那批，仅供追溯）：`settings.html` 457805 字符（r88~r93①）；`{avatar,skills,automation}` = 566669 / 360166 / 360279；
> `{dev,kanban,req-kanban,task-detail}` = 449491 / 567338 / 513077 / 766714；`assets/images/bg-img-1.png`（顶栏装饰）；`giencoder-design-system/components.css` + `.gienx-templates/_shared/components.css` + `components/select.json`（r87 select）。
> `?? mg-work/r92/` · `?? mg-work/r93/`（`apply93.py` + `acceptance.md` 十三节 + `before/` 25 份 + `ev/` + `raw/`）—— **均已提交**。

`origin/main` @ **`d7e2151`**（r86~r100 已推送；上一站 `1ecc7ee` = r80–r85）。**长期约定「默认不自动 commit / push」（2026-09-28 起）；邵先生显式说「commit and push」时才执行**。

⚠ `.gitignore`：`mg-work/r80/raw/sel_*.json`、`mg-work/*/gate/*/pages/`。`before/` 与 `raw/` **是**入库惯例。
⚠ **推送凭据**：PAT 已写入 `~/.git-credentials`，推送带 `-c credential.helper=store`（详见第九节）。
⚠ **安全（r100 首推被拒时查明）**：该 PAT **就是当前在用的推送凭据**（与 `~/.git-credentials` 同一枚），它曾出现在对话记录里、
又被明文抄进 `mg-work/r87/acceptance.md:174` 的「安全备忘」（那行自己写着「建议 Revoke」，却从没执行）⇒ 首推被 **GitHub Push Protection** 拒。
已就地打码 + `commit --amend` + `reflog expire --all` + `gc --prune=now` 清干净（详见 PLAYBOOK **P5.1**）。
**⚠ 但「已泄露」打码是解决不了的 —— 请尽快 Revoke 该 token 并换发新 PAT**（换发后只需覆盖 `~/.git-credentials`，推送命令不用改）。

`.workbuddy/memory/` 两份：**仓库内（权威，随 git 走）** 与工作区 `E:/GienCoder/.workbuddy/memory/`（速记）。改记忆**以仓库内为准**。

---

## 二、★ r93 + r94 + r95 + r96 + r97 + r98 + r99 + r100（前情 · 需求 1 + 需求 2 + ④「独立页 + 全要素复用」+ r94 五条微调 + r95 两条「右侧撑满」+ r96 五条「字号/色/速率行」+ r97 四条「卡内字号统一 / 胶囊 / **宽度基准** / 统计行」+ r98 三条「内容区 14→15px / rateline 下 48px / **差分卡逐像素还原**」+ r99 十四条「假滚动条 / 按钮态 / 右键菜单 / 图标修复」+ **r100 八条「更名 / 卡内 14px / hover 口径 / 整行可点 / ndesc 胶囊 / 调用 5 个工具层级树」**）

零字面 hex（新色一律进 `--r93-*` 本地变量 + 暗色档）；幂等可复跑。
> 追记：需求 2 落地后邵先生又问了两件事（记为 **④**，见下）——「会话页面该不该是独立 html、要注意路由」「底部对话框要**完全全要素复用**基础工作台 main 里那个真组件」。用户拍板：**做成独立页** + **保留状态条/agent 卡、只换输入卡**。

### 需求 1 —— aside 分组标题行高被改坏（应 32px）

**根因**：`<style id="r87-ui-css">` 里 `body .text-xs{font-size;line-height}` 特异性 **(0,1,1)** > 尾风 `.leading-\[32px\]` 的 **(0,1,0)** ⇒ 行高 32→16、整行腰斩。**r87 字号机制引入的回归**。

修法（`mg-work/r88/apply88b-fontsize.py` 就地返工）：
1. `text-*` 的行高**只在无 `leading-*` 类时**派生 → `body .text-xs:not([class*="leading-"]){line-height:…}`；
2. 新增 `LEADING_DERIVE = [(.leading-\[19px\],19), (.leading-\[22px\],22), (.leading-\[32px\],32)]`，**写在 text-\* 之后**（同 (0,1,1)，后写者胜）。

实测 4 个分组标题 `h 16→32`、`lh 21px→32px`；顺带 `textarea` 20→22、页脚 16→19.5。

### 需求 2 —— 点 aside 会话标题 ⇒ main 展示该会话的用户/AI 对话详情（设计稿 `1393:18748`）

> ④ 之后**主载体从 base.html 搬到 `pages/conversation.html`**（独立页），注入机制**逐字不变**（同一份 CSS/JS 只是换了承载文件 + 判据由 `[data-r93-conv='1']` 改为根级 `<html data-r93-page="conversation">`）。下面这段描述的是内容本体，两页通用。

**`<main>` 在 base.html 里出现 0 次**（React 运行时渲染）⇒ **不动 React 源**，只在 `mainInner` 尾部追加 `.r93-conv-host`，用 `[data-r93-conv='1'] > *:not(.r93-conv-host){display:none!important}` 藏掉「欢迎空态 + 版权页脚」。

* **点击分流**：`document` **捕获阶段** 监听 `aside button`：
  `min-w-0 + flex-1`（会话项）⇒ 打开；`rounded-md + py-0`（分组标题）⇒ 只折叠、不切换；其余 ⇒ 关回空态。
* `MutationObserver` 兜底补回被 React 冲掉的节点。
* **25 个块**：页头 44 / 用户气泡 / 助手头 / 上下文注入 / 深度思考 / AI 文本 ×2 / Bash / 网页搜索 / 需求采访 / 更新任务清单 / 文件写入 / SKILL / Tool call / 重试 / 调用 5 工具 / 压缩上下文 / 上下文已压缩 / 搜索资料 / 告警 ×2 / 未知 surface / 模型已切换 / 改动汇总 / 任务产物 / Token 速率行 + composer（状态条 + 4 张 agent 卡 + 输入框）。
* 用户拍板：**全量还原** / 所有会话都渲染这一份设计稿内容 / 轨迹页签切**统一空态** / 折叠可点 + 关键 hover·popover 做。

**三点自行拍板**（用户未回，按工程判断）：
| 项 | 结论 |
|---|---|
| 定位 | **居中**：`width:840px; margin:0 auto`（实机 main 内宽 1162 ⇒ 左右各 161，**不照搬设计稿 164**） |
| 硬编码色 | 全部进页面 `:root` 的 `--r93-*` 变量，并补 `[giencoder-theme='dark']` 档 |
| 字体 | 沿用页面 `Mona Sans VF` |

**★ 变体叠加陷阱**：导出图里**每个折叠块容器内同时叠放了「折叠态(T0 H22)」与「展开态(T34 H184)」两个变体** ⇒ **真机块高 = 容器高 − 34**（逐块固定，不累积）⇒ **导出 PNG 的绝对 y 不可当设计坐标**。去掉 offset 逐块累加 ⇒ 设计真机内容总高 **4106px** = 实机实测 **4106px** ✅

**★ 字号体系**（`ui-component` 不带 font-size，靠「框高 × 墨迹行距 × 文本宽度反推」三角验证）：

| 用途 | fs/lh |
|---|---|
| 折叠头标题 / 气泡正文 / 需求采访 | 14 / 22 |
| 折叠头 meta（skill-catalog / 2s / deepwiki） | 12 / 22 |
| **卡内正文 / 代码** | **12 / 20** |
| 上下文注入卡正文 | 12 / 16 |
| Bash 卡代码 | 12 / 16 |
| 居中提示卡片下说明行 | 12 / 24 |
| 深度思考正文 | 12 / 22 |

> 初版统一写 `14/22` ⇒ 上下文注入 190(应150)、SKILL 90(应64)、深度思考 222(应200)、网页搜索 200(应184)，全错。已建 `.r93-t12c` / `.r93-t12s` / `.r93-t12h` 工具类逐块替换。

**逐块几何核对**（实机 1440×900）：块高 0/1/2/3/5/6/7/8/9/10/11/12/14/15/16/17/18/19/20/22/23/24 全一致；仅 2 处 Δ2（搜索资料 152→150、改动汇总 302→300）。横向全对齐（host 1162 / wrap 840 / 气泡 728 / 卡 822 / diff 840 / 告警 840）。

**结构级修正**（尺寸对不上只是表象）：
* **更新任务清单**：设计稿**没有 40px 卡头**，1px 分隔线在卡内 `y=181` ⇒ 重写 `.r93-todocard`（padding 16/20/12），JSON 改 9 行截断式。
* **网页搜索**：8 行**整行是蓝色下划线链接**（`#3770F7` = `--color-primary-6`），不是灰文本。
* **搜索资料**：蓝下划线标题 + 灰描述，组内 gap 3 / 组间 6。
* **任务产物**：Token 速率行是**独立容器**（840×24 @ +20），不在卡内。
* **深度思考列表项**：导出图渲染为 **「1. 2. 3.」**，不是私有区图标 `󰀐`（实机缺字形 ⇒ 会变豆腐块并多折 1 行）。

**暗色适配**：r93 画面 CSS 里 11 处字面 `background:#FFFFFF` + `#F5F6F7` 卡底在暗色下会「白屏」⇒ 白底一律换 `var(--color-bg-2)`（浅 `#fff` / 暗 `#232324`，浅色视觉零变化），`--r93-*` 全套补暗色档。

### ④ 会话详情**独立成页** + 底部 composer **全要素复用**外壳真组件

**邵先生两问 + 拍板**：① 「这个 AI 对话页该不该是独立 html？若是，注意与其它页的跳转路由」→ 答：**应是**（理由见 PLAYBOOK P3.24⑦），用户拍板**做成独立页**；② 「底部对话框要**完全全要素复用** main 里那个 `relative flex w-full flex-col rounded-[16px] border bg-white p-3 transition-colors`」→ 用户拍板**保留状态条 + agent 卡、只换输入卡**。

**① 独立页落地（`pages/conversation.html`，604806 字符）**

- **体位**：`conversation.html` **每次从 base 净底重建**（`net = base 摘掉 r93 三块` ⇒ 换 `<html>`/`<title>` ⇒ 尾部注入 `r93-conv-css`+`r93-conv-js`），**不靠复制**；`base.html` 只留 `<!-- r93-nav --><script id="r93-nav-js">`（点 aside 会话项 ⇒ `location.href='conversation.html'`）。
- **根级判据**：`<html lang="zh-CN" data-r93-page="conversation">` ⇒ 页面级 CSS 全部挂 `html[data-r93-page='conversation'] …`（不再用 `[data-r93-conv='1']`）。
- **路由（10 页各 1 条，含新页自身）**：每页 `ROUTE` 表尾插 `, '/conversation': 'conversation.html'`（+38 字符/页）。顶栏「工作台切换」页签（`SHELL-TABS-FIX v4`）**不受影响** —— conversation 不在 `DEV_PAGES`，在它上面点「基础工作台」是空操作（实测确认）。
- **点会话 ⇒ 跳页**：`r93-nav-js` 在 `document` **捕获阶段**拦 `aside button`，只认 `min-w-0 + flex-1`（会话项），**不拦分组标题/导航项**。

**② composer 全要素复用（纯 CSS，零复制、零重绘）**

不动 React 源，靠 5 条同页选择器改**视觉顺序**，让真组件自己长在会话详情底部：

```css
/* 宿主前置于 hero 之前 */
html[data-r93-page='conversation'] .r93-conv-host { display:flex; flex-direction:column; flex:1 1 auto; min-height:0; order:-1; background:var(--color-bg-2); overflow:hidden; }
/* hero 贴底、去掉顶住的 mt-8、藏掉问候语与版权页脚 */
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center { flex:0 0 auto!important; justify-content:flex-end!important; padding-bottom:12px!important; }
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > .pointer-events-none { display:none!important; }
html[data-r93-page='conversation'] main > div > div.flex-1.justify-center > div.mt-8 { margin-top:0!important; }
html[data-r93-page='conversation'] main > div > div.pb-6 { display:none!important; }
```

- **保留**：状态条 `.r93-sb`（「执行 第 2/5 个待办」）+ 4 张 `.r93-agent` 卡（在**我们的宿主 DOM** 内，hover popover 也仍在宿主内）；**删掉**宿主里自绘的 `.r93-input`/`.r93-ta`/`.r93-itools`/`.r93-perm`/`.r93-model`/`.r93-send`（整段）。
- **实测最终视觉顺序** = 设计稿：内容 → Token 速率 → 滚动到底部 → 状态条 → agent 卡行 → **输入卡（真组件）** → 工作目录/默认权限行。
- **实测 rect（1440）**：host 1162×628（`order:-1`）/ hero 1162×214 / outer **860×214** / card **836×154** / 问候语 + 页脚 `display:none` / `doc 900 = win 900`（无纵向滚动）。
- **★ 真组件下拉「必须翻向」**：真 select 默认**向下**弹（`top:calc(100% + 4px)`），composer 钉在 main 底部（`main` 是 `overflow:hidden`）⇒ 被裁（实测「默认权限」popup y **871..997** 而 main 底 **892**，只剩 21px）。页面级适配翻成向上：

```css
html[data-r93-page='conversation'] .giencoder-select-popup { top:auto!important; bottom:calc(100% + 4px)!important; transform-origin:bottom; }
html[data-r93-page='conversation'] [aria-label='权限选择'] { top:auto!important; bottom:calc(100% + 4px)!important; }
```

  修后 4 个 popup 全部完整可见：标准模式 200×80 / 模型 194×207 / 工作目录 194×109 / 默认权限 280×126；「＋添加」（180×92）与三个 select 全部走外壳自己的 handler（实测可点）。
- **`.r93-cp` 简化**：由「灰底 + 描边 + padding」改为只有 `margin-top:12px`（灰壳交给真组件，避免两层灰壳）；`.r93-tbsticky` 保持 `bottom:44px`（壳体 bottom = 滚动口底 − 药丸底边 − 32，实测按钮底 541 / 状态条顶 553 / 间距 12px）。
- ⚠ **`apply88b-fontsize.py` 的 `unscale()` 正则只认 `calc(<数字>px * var(--ui-fs-ratio))` 或裸 `Npx` 结尾** ⇒ 我们的 `calc(100% + 4px)`（含 `%`）**安全**；且 `converge()` 会把整个注入 `<style>` 块原样跳过 ⇒ **新块 id 必须唯一**（`r93-conv-css` / `r93-conv-js` 不与旧块同名）。

**★ 独立页由 base 净底重建的判据（④ 幂等体位）**

`python mg-work/r93/apply93.py` 把「**base 摘块后的净底**」当作**两页的唯一来源** ⇒ 第二遍任何一页都「已是目标态（无改动）」（实测连跑两遍均如此）。`--revert` = 删 `conversation.html` + 摘 base 的 `r93-nav-js` + **10 页 `ROUTE` 各 −1 条**。

### r94（同日第四轮）—— 会话详情页 5 条微调（**就地返工 `apply93.py`**）

> r93 未提交 ⇒ 就地在 `mg-work/r93/apply93.py` 的 `r93-conv-css` / `r93-conv-js` 上改（不另起代数）。

| # | 需求 | 做法 |
|---|---|---|
| ① | `r93-seg-cap` 在 `r93-bar` 内**居中** | `left:396px`（设计稿 1168 面板的固定值，换视口即偏）→ **`left:50%; transform:translateX(-50%)`**；实测 `capCenterDelta = 0` |
| ② | `r93-wrap` 宽 = **main 的 50%**、**min 860px** | `.r93-wrap { width:50%; min-width:860px; box-sizing:border-box; padding:32px 10px 24px; }` ★ 内容块固定宽（728/822/840）⇒ 靠**左右各 10px 内距**把内容盒保持 840 ⇒ 横向位置与 r93 口径（425..1265）**零位移** |
| ③ | 对话框**只留输入卡本体** | outer 去灰壳（`background:none; padding:0; border-radius:0`）+ 隐藏底排（`> div:not(:has(textarea))` ⇒ 工作目录/默认权限行）；**DOM 血缘不动** |
| ④ | `div.mt-8` 内的**波点**全去 | ★ 侦查：**mt-8 里只有 1 个子（composer 外壳）**，没有波点子节点；点阵真源 = **`main.dot-bg` 本体 + `::before` 光斑层** ⇒ 页面级 `main.dot-bg{background-image:none}` + `::before{display:none}` |
| ⑤ | `r93-card--ctx` **max-height 240 + 内滚**；`r93-vsb` 假滚动条去掉 | `.r93-card--ctx` 加 `max-height:240px; overflow-y:auto; overflow-x:hidden`；**删** `.r93-vsb` 规则 + **5 处 DOM**（ctx / Bash / diff / 改动汇总 / 任务产物） |

**实测**：`wrap [415,93,860,…]`（原 840）、outer `[420,725,860,154]`（bg 透明 / pad 0 / br 0，子② `display:none`）、`main.backgroundImage=none`、`::before` display none、`.r93-vsb` 计数 **0**、ctx 溢出取证 `scrollHeight 244 > clientHeight 240 ⇒ scrollable`（运行时临时塞内容、测完移除、不落盘）。

**★ 踩到的一次假阳性**：首跑 `verify-design` 时 conversation 的渐变计数 **62→63** —— 根因是我在**新注释里写了被扫描的关键词**（`radial-gradient`）⇒ 改措辞后与 r93 基线**逐字节相同**。**这是「新增注释里不得出现被断言的 token」的又一次实例。**

**产物**：`pages/conversation.html` **604806 → 606073**（字节 sha `acb485be7385`）；`pages/base.html` **471444 未变**；`ev/p94b~e.js` + `.sh` + `vd-r94*.txt`；`raw/r94-hero.png` `r94-full.png`。

### r95（同日第五轮）—— 会话详情页 2 条「右侧撑满」（**就地返工 `apply93.py`**）

> 需求：① 「类似 `r93-card r93-card--ctx` 这种容器的**右侧要撑满**」；② 「**底部对话框相关的内容模块也要自适应撑满**」。

**侦查（`ev/p95a.js`，1440 实测）—— 三组元素三条右边界打架**：

| 组 | 元素 | rect | 右边界 |
|---|---|---|---|
| 内容 | `.r93-wrap` 外沿 / 内容盒 / `--ctx` 卡 / `bub` / `todocard` | `[415,93,860]` / 425..1265 / 1265 / 1265 / 1265 | **1265~1275** |
| 底部 | `.r93-sb` / `.r93-cp`（`width:840px; margin:0 auto`） | `[430,·,840,·]` | **1270** |
| 对话框 | composer `outer` / 输入卡 | `[420,725,860,154]` | **1280** |

根因两条：**(a) 滚动条占位** —— `.r93-scroll` 出现滚动条后内容盒收窄（单侧 10px），`margin:0 auto` 的 wrap 相对「无滚动条」的底部/composer **左偏 5px**；**(b) r94 给 wrap 加的 10px 内距**（为保内容盒 840）让块比 composer 窄 10px。

**落地（14 处）**：

| 类别 | 改动 |
|---|---|
| ① 居中同轴 | `.r93-scroll` 加 **`scrollbar-gutter: stable both-edges`**（两侧各让等量 gutter ⇒ 内容恒居中，不再偏 5px） |
| ② 内容盒 | `.r93-wrap` padding `32px 10px 24px` → **`32px 0 24px`**（块改流式后不需要内距） |
| ③ 卡片 | `.r93-card` / `.r93-todocard`：`width:822px` → **`calc(100% - 18px)`**（**左缩进保留、右侧撑满**） |
| ④ 整行块 | `.r93-card--full` / `.r93-note` / `.r93-ndesc` / `.r93-alert` / `.r93-diff` / `.r93-arts`：`840px` → **`100%`** |
| ⑤ 产物卡 | `.r93-artcard` `414px` → **`calc(50% - 6px)`**（两列等分撑满） |
| ⑥ 底部列 | `.r93-bottom` 加 `width:50%; min-width:860px; box-sizing:border-box; margin:0 auto`；`.r93-bottom > *` `840px + auto` → **`100% + 0`** |
| ⑦ 对话框壳 | `… > div.mt-8 > div` 补 **`width:50% !important; min-width:860px !important`**（原先 Tailwind 写死） |

⚠ **刻意未动**：`.r93-bub`（728px 气泡 —— 右对齐 ⇒ 自动跟随新右边界；设计稿语义本就是「不满宽」）；`.r93-agent`（4 张 agent 卡按内容宽左对齐，属设计稿固定排版，**不是「容器」**）。
⚠ **收敛安全**：`calc(100% - 18px)` / `calc(50% - 6px)` / `100%` / `50%` 都不含「裸 `Npx` 结尾」⇒ 不匹配 `apply88b` 任一 `RE_*`，不会被 `unscale()` 改坏。

**实测（`ev/p95b.js`，1440 / 1920 双档）—— 全块 Δ=0**：

```
.r93-scroll    clientWidth 1142 / offsetWidth 1162（gutter stable both-edges）
.r93-wrap      [420,860] → 右 1280        .r93-bottom/[sb]/[cp] [420,860] → 右 1280
composer outer [420,860] → 右 1280        inputCard     [420,860] → 右 1280
ctx/todocard   [438,842] → 右 1280 Δ=0    bub [552,728] → 右 1280 Δ=0
alert/diff/arts/note [420,860] → 右 1280 Δ=0   artcard [420,424]（两列 ⇒ 第二张右边界 1280）
tbsticky 药丸 [790,120] 中心 850 = 内容列中心          doc/win 双 1440/1920（无横向溢出）
```

**产物**：`pages/conversation.html` **606073 → 606949**（+876；字节 sha `247c6c1e040e`）；`pages/base.html` **471444 未变**（`c16308a00915`）；`ev/p95a.js/.sh`（侦察）+ `ev/p95b.js/.sh`（实测）+ `vd-r95.txt`（= r93 基线）；`raw/r95-full.png` `r95-hero.png`。

### r96（同日第六轮）—— 会话详情页 5 条（**就地返工 `apply93.py`**）

| # | 用户原文 | 落地 |
|---|---|---|
| ① | `r93-bubi` 容器最大高度 240px，溢出就内滚 | `.r93-bubi` 加 `max-height:240px; overflow-y:auto; overflow-x:hidden`（只改「体」，不动 `.r93-bub` 气泡列） |
| ② | 类似 `r93-card` 的容器默认字号调整为 13px | `.r93-card` 加 `font-size: var(--font-size-body-2)`（= **13px**）。⚠ 该规则**不得**声明裸 `height`（converge 约束）—— 本规则无 height ✓；卡内 `.r93-pre` 等自带 12px 的不受影响 |
| ③ | `r93-t14` 文字颜色浅两级；`r93-t14 r93-c2` 用正文颜色 | `.r93-t14` 默认色 → `--color-text-3`；**新增** `.r93-t14.r93-c2 { color: var(--color-text-1) }`（(0,2,0) 压过 `.r93-c2` 的 (0,1,0)，与书写顺序无关） |
| ④ | `r93-card r93-card--edge` 的宽度还没调整 | 嵌套 Tool call 卡**拉丢内联 `w:804`**（改走 `.r93-card` 的 `calc(100% - 18px)`）；另两处 `style="width:840px"` 的 AI 文本块一并改流式 |
| ⑤ | `r93-rateline` 各元素还原度很低，请对比设计稿精确还原 | 整行重写（下详） |

**★ ⑤ 的设计稿取数（两份权威源，非目测）**：
- **源 1** `raw/design-1393-18748.html`（设计稿导出的带样式 HTML）：节点 `1393:18599`「容器 247」= 256×24 @ (164,4664)；
  `1393:18598`「容器 246」56×24 = **2 个 24×24 `icon-wrapper`（图标 14，gap 8）**；两根「直线」是
  `viewBox="0 0 2 14"` 的 svg ⇒ **1px × 14px 竖线**（#E5E5E5）；`fw647:19591` Link 142×24 @80 `gap:4` =
  时钟 14×14 + 「Token 速率：256/s」（**14px / lh24 / #868686**）。
- **源 2** `raw/design-rgb.png`（1x 整页导出，**色值已验证准确**：同一张图上量的前两枚图标 = (107,107,107) = #6B6B6B，
  与该 HTML 里其它 `style="color:#6B6B6B"` 逐字一致）逐像素列扫描：图标1 x 6..18 · 图标2 x 40..49 ·
  线1 **@68**（y 4670..4683 ⇒ 高 14）· 时钟 x 82..93 · 文字 x 99..221 · 线2 **@234** · 省略号三点 x 240..249（点间距 4）。
- ⚠ **旧实现两处硬错**：① 把「容器 246 的 **56 宽**」误当成**线宽** ⇒ `.r93-nline{width:56px}` 画出 **56×1 横线**；
  ② `gap:16`，而设计各段间距是 **12**（56→68→80→222→234）。

**⑤ 新实现**（`.r93-rgrp`[gap8] + `.r93-rline`[1×14 竖线] + `.r93-rrate`[gap4] + `.r93-rbtn`[24×24 盒 / 图标 14 居中]）：
```css
.r93-rateline { display:flex; align-items:center; gap:12px; }
.r93-rgrp  { display:inline-flex; align-items:center; gap:8px; flex:none; }
.r93-rbtn  { width:24px; height:24px; color:var(--r93-ioc2); border-radius:4px; }
.r93-rline { flex:none; width:1px; height:14px; background:var(--color-border-2); position:relative; z-index:1; }
.r93-rrate { display:inline-flex; align-items:center; gap:4px; color:var(--color-text-3); }
.r93-rateline > .r93-rline + .r93-rbtn { margin-left:-16px; color:var(--color-text-3); }
```
新变量 `--r93-ioc2: #6B6B6B`（浅）/ `#C9C9C9`（暗色档 —— DS 暗色色阶是反的，gray-7 取 #C9C9C9）。
新图标 **`branch`**：设计稿里它是 DS `icon-wrapper` 实例（**没有导出独立 svg**）⇒ 按 `design-rgb.png` 的
14×14 点阵逐像素反推（三个**空心**圆节点 + 贯通主线 + 自右节点下沿并入主线的曲线），换算到 16 网格写入 `ICON_INLINE`。

**⑤ 逐元素对位（行左 = 视口 420）**：图标1 盒 0..24 / 图标2 盒 32..56 / **线1 @68** 均**逐像素对齐**；
线2 实测 227 vs 设计 234（−7）、省略号盒 224 vs 231.5（−7.5）—— **唯一原因是字体度量**
（实机 Mona Sans 下「Token 速率：256/s」宽 116，设计稿 MiSans 下 123 ⇒ Link 总宽 134 vs 142）；
**省略号相对第 2 根线的位置关系一致**（实测盒在线左 3px / 设计 2.5px）⇒ 同套间距的自然位移，不是间距错。

**实测（1440×900，`ev/p96a~c`）**：① `maxHeight 240px / overflowY auto`，**溢出取证**正文撑 25 倍 ⇒
`scrollHeight 590 > clientHeight 240`、`scrollable:true`、`scrollTop` 可到 350 ｜② `.r93-card` = **13px**（3 个无类名文本同落 13px）｜
③ 问题行 **rgb(134,134,134)** / 回答行 **rgb(31,31,31)** ✔ ｜④ 4 张 edge 卡 **842/842/842/824**，**右界全 1280**（改前第 4 张 804/右界 1260）｜
⑤ 线 = **1×14 竖线**（bg rgb(229,229,229)）、图标 = 复制+分支（rgb(107,107,107)）、省略号 rgb(134,134,134)、gap **12**。

**产物**：`pages/conversation.html` **606949 → 609969**（+3020；字节 sha `e032e8913bf1`）；`pages/base.html` **471444 未变**（`c16308a00915`）；
`ev/p96a~d.js|.sh` + `vd-r96.txt`；`raw/r96-ic12big.png`（图标 18× 放大）· `r96-rate-ctx.png` · **`r96-cmp2.png`（设计 vs 实机同尺度上下对照）** · `r96-ratepage.png` · `r96-after-full.png`。

### r97（同日第七轮）—— 会话详情页 4 条（**就地返工 `apply93.py`**）

| # | 用户原文 | 落地 |
|---|---|---|
| ① | 所有 `r93-card` 容器内的字号统一调整为 13px | 新增 **`.r93-card.r93-card, .r93-card.r93-card * { font-size: var(--font-size-body-2) }`** —— 实测**卡内 42 处文本全落 13px**（r96 只调了「裸文本」的默认档，卡内仍混 12px/14px） |
| ② | 「滚动到底部」应是胶囊按钮 + 文字色与图标一致 | `.r93-tobottom`：圆角 `8px` → **`999px`**（DS 无胶囊半径 token，最大 xl=12px）；前景色 → **`--r93-ioc2`**（#6B6B6B）+ 新增 `.r93-tobottom .r93-t14 { color: inherit }` ⇒ 图标与文案同色（设计稿实测两者都是 #6B6B6B） |
| ③ | 底部对话框相对上方内容两端都短了一截，要求等宽 | ★ **三者宽度基准统一** + agent 卡行撑满（下详） |
| ④ | 底部对话框下面还有一行小灰色文字 | `div.mt-8::after` 纯 CSS 补回（`content` = 「2 轮 · 27 步 · … · 输出 31.1K token」，12px / lh16 / 新变量 **`--r93-meta: rgb(var(--gray-5))`** = #A9A9A9）；hero `padding-bottom` 12 → 8 |

**★ ③ 的根因（「两端各短一截」只在宽视口出现）**：三块都写百分比，却挂在**宽度不同的父盒**上 ——

| 元素 | 父盒 | 与 main 内宽的差 | 2560 实测（改前） |
|---|---|---|---|
| `.r93-wrap` | `.r93-scroll` 滚动内容盒 | `both-edges` 左右各让 10 ⇒ **−20** | `[845,1131]` |
| `.r93-bottom` | `.r93-pane` | **0**（基准正确） | `[840,1141]` |
| composer | `div.mt-8`（hero `w-full` 子盒） | hero `px-6` ⇒ **−48** | **`[852,1117]`** |

⇒ 1440 下三者都取 `min-width:860` 看不出问题；2560 下**输入卡比状态条两端各短 12px**。修法三条：
① `.r93-scroll::-webkit-scrollbar { width: 10px }`（把滚动条宽度**显式钉死**，全站默认也是 10）
② `.r93-wrap { width: calc(50% + 10px) }`（补回 both-edges 的一半）③ hero `padding: 0 0 8px 0 !important`（清掉 `px-6`）。
⇒ 三者恒等于 `max(50% × main 内宽, 860px)`。**实测 1440 / 2560 双档 wrap / bottom / sb / composer 右边界全等**（1280 / 1981）。
**顺带**：4 张 agent 卡 `flex:none` → **`flex: 1 1 auto; min-width:0`**（设计稿 PNG 实测该行第 4 张**顶到内容列右缘** ⇒ 本来就该填满；改前 2560 右端空 365px）。

**★ `*` 不贡献特异性（本轮踩到）**：首跑「卡内 37 处 13px、唯独 5 处 `.r93-pre` 仍 12px」——
`.r93-card *` 其实只有 **(0,1,0)**，`.r93-pre` 与它同级且写在**后面** ⇒ 后写者胜。修法：类名写两遍抬到 (0,2,0)。

**产物**：`pages/conversation.html` **609969 → 613441**（+3472；字节 642788；**LF 文本 sha `481d929d89bd`**）；`pages/base.html` **471444 未变**；
新增 `ev/p97a`（侦查）· `p97c.sh`（宽视口）· `p97d`（实测，1440/2560）· `p97f`（字号回归隔离）· `vd-r97.txt`；
新增 `raw/r97-cmp.png`（设计 vs 实机上下对照）· `r97-pill2.png` · `r97-bottom2.png` · `r97-agentrow.png` · `r97-after-full.png`；
新增 `before/conversation-r96.html` · `base-r96.html`。详见 `mg-work/r93/acceptance.md` 第十章。

### r98（同日第八轮）—— 会话详情页 3 条（**就地返工 `apply93.py`**）

| # | 用户原文 | 落地 |
|---|---|---|
| ① | 整个对话内容部分的 **14px 字号统一调整为 15px** | 新增 `.r93-t14, .r93-t14m, .r93-t14b { font-size: calc(15px * var(--ui-fs-ratio)) }`（写在三条定义**之后**、**只写 font-size**）⇒ 内容区 **59 处落 15px**；`.r93-card.r93-card *`（0,2,0）仍把卡内压回 13px ✓ |
| ② | 单轮末尾 `r93-rateline` 模块**下面间距 48px** | `.r93-wrap` `padding: 32px 0 24px` → **`32px 0 48px`**（rateline 是本轮最后一个 `.r93-it`：实测 `isLast=true`、无 `nextSibling` ⇒「下面间距」就是内容盒下内距） |
| ③ | `r93-diff` 样式还原不到位（颜色 / 间距…），对比设计稿像素级还原 | 整卡重做（下详） |

**★ ③ 差分卡逐像素还原（设计稿 `1393:18681`「容器 252」= 840×300；双源 = `raw/design-1393-18748.html` + `raw/design-rgb.png` 逐像素扫描；坐标一律卡内相对值）**：

| 部位 | 设计稿 | 旧实现 → 本轮 |
|---|---|---|
| 卡底 | 表头带 `#F5F6F7` + **列表纯白面板** | 整卡 `#F5F6F7` → `.r93-diff{bg-2}` + `.r93-dhead{--r93-card}` |
| 表头 | **40 高** + **底部 1px `#ECEEF2` 分隔线** | `height:28` 无分隔线 → `40 + border-bottom` |
| 行 | 高 36、**首行无上边线** | 7 行全带边线 → `:first-of-type{border-top:0}` |
| 行内距 | **左 11 / 右 13** | `0 36 0 8` → `0 13 0 11` |
| 数字列 | 与 ⋯ 之间 **17**、右沿距卡内右 **54** | gap 8 → `gap:17` |
| ⋯ 字色 / 悬停 | **(31,31,31)** = text-1；悬停 **白底 + 1px 描边** | text-2 / fill-2 → `text-1` + `bg-2 + inset 描边 border-2` |
| +800 | **(48,149,59)** = `--r93-ok` | `--color-success-6`(59,179,70) 偏亮 → `--r93-ok` |
| 按钮 | **70×28** | 72 → `padding: 0 11px` |
| 表头图标槽 | 槽宽 **24**、标题落卡内 **36** | 图标盒 14 ⇒ 标题 39 → `margin-right:-3px` ⇒ **456** ✓ |
| 表头数字组 | gap **8** | 全 12 → 新增 `.r93-dh2{gap:8}` |
| 滚动条 | `矩形 219` = **6×128**、rgba(0,0,0,.16)、r6、卡内**右 4 / 顶 4** | 无 → 新增 `<i class="r93-dsb">` + `.r93-dsb`（**静态装饰**，见待拍板） |

★ 设计稿那行 `app.json` 是**叠出来的 hover 态**（行底 + 文件名 primary + ⋯ 白底描边盒）⇒ 本页保持**真 CSS `:hover`**，不静态写死（同 r93「变体叠放」教训）。

**★ 顺带修掉的真 bug —— `.r93-alink` 一直不是 12px**：`.r93-bt { font: inherit }`（第 412 行）与 `.r93-t12`（第 363 行）**同为 (0,1,0)** 但**写在后面** ⇒ 后写者胜，把「任务完成，耗时28m12s」撑成 14px。设计稿墨迹 x166..325 = **160px ≈ 11 汉字 + 5 半角 @12px**（@14px 要 189px）⇒ 在 `.r93-alink`（写在 `.r93-bt` 之后）补 `font-size: var(--font-size-body-1)`。

**★ 踩坑 —— 门禁对注释的双重标准**：`check_hardcoded_hex` 遇到 `<!--` / `/*` 会 `continue` **跳过注释行**，但 `check_hardcoded_px_fontsize` **不跳** ⇒ 我在新增注释里写了裸 `font-size: 15px` 导致门禁 **77（应 76）**，改措辞后归零（`vd-r98.txt` 与 `vd-r93c.txt` 逐字节相同）。**另**：`.r93-drow:first-child` 失效（`.r93-dlist` 首子元素是 `<i class="r93-dsb">`）⇒ 改 `:first-of-type` + 把 `<i>` 从列表头挪到尾部（双保险）。

**★ r98 复查（同日第八轮）**：全绿 —— 幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` **76 条**与 `vd-r93c.txt` **逐字节相同**（21882 字节 `equal:True`，`vd-r98.txt`）｜实测 `ev/p98b.js` **1440 / 2560** 双档（内容区字号分布 12×49 / 13×42 / **15×59** / 14×2；wrap pb **48**；差分卡右对齐账 ⋯−13 / 数字−54 / 名+11 全对）＋ `raw/r98-cmp.png`（设计 vs 实机对照）。

**产物**：`pages/conversation.html` **613441 → 616773 字符**（+3332；字节 647842；**LF 文本 sha `6cbeff3a126c`**）；`pages/base.html` **471444 未变**（sha `c16308a00915`）；
新增 `ev/p98a.js/.sh` · `p98b.js` · `vd-r98.txt`；新增 `raw/r98-design-diff.png` · `r98-design-below-rateline.png` · `r98-live-diff.png` · **`r98-cmp.png`** · `r98-after-full.png` · `r98-rateline.png` / `r98-rateline-crop.png`；
新增 `before/conversation-r97.html` · `base-r97.html`。详见 `mg-work/r93/acceptance.md` 第十一章。

### r99（同日第九轮）—— 会话详情页 14 条（**就地返工 `apply93.py`**）

邵先生原话十四条（`.r93-conv-host`）：①去掉 `r93-dsb` 假滚动条、需要时显示真滚动条；②`r93-tobottom r93-bt is-on` 默认图标/文字深一级 + 整钮 hover 底色；③`r93-rbtn r93-bt` 与间隔线贴在一起；④`r93-iblk r93-i14` 图标异常；⑤底部还有波点涟漪；⑥`r93-artlabel` 字号也是 15px；⑦`r93-drow` 行要支持右键菜单、且与右侧「更多」是同一个菜单；⑧`r93-fc r93-bt` 开合有跳动；⑨复制按钮 hover 底色不对 + 点击后变绿勾；⑩`r93-t14 r93-c2` 顶距 4px + `r93-card` 字号 15px；⑪`r93-alink` 15px；⑫`r93-pill` 尺寸细节不符；⑬`r93-asst` 底线深一级；⑭`r93-iblk r93-i14` 图标不对 + 与左侧时间间距不对。

**逐条落地与实测（1440）**：①`dsbCount=0` / `overflow-y:auto` / 7 行 258 不溢出 ②`rgb(78,78,78)` + `fill-1/border-3` ③线1 **68** / 速率 81..224 / 线2 **234** / ⋯ 盒 233..257 ④SKILL 渲出完整**扳手**（见下「踩坑一」）⑤`.r74-ripple` `background-image:none` ⑥`fs=15px` ⑦面板 182×153 / 4 项 + 1 分隔线 / `viaMoreBtn=true`、`sameNode=true`（**同一点击节点**）/ `Esc` 可关 ⑧三态 `headH` 恒 22、`icW/H` 恒 14、`txX` 恒 18、`headTop` 恒 0、`reopenMatches=true` ⑨`color=rgb(48,149,59)` 绿勾 ⑩`c2MarginTop=4px` / `cardFs=15px` / `quizPad=20px` / **`quizH=208` = 设计稿** ⑪`fs=15px` ⑫盒 158×22 / `pad=1px 6px` / `radius=3px` / `color=rgb(52,145,250)` ⑬`rgb(229,229,229)` ⑭**regen 图标重画为 14 栅格** / `gapTB1=13` / `gapB1B2=6`。

**★ 踩坑一（本轮最大，已写进补丁注释 + PLAYBOOK P3.30①）**：我先写了 `fit_viewbox()`（按「字形 bbox 越出 viewBox > 35%」自动重算），
它报 `svg_1d5c65e3`（SKILL）越界 90%、`svg_e08b0fbd` 越界 92% ⇒ 我把两者的 viewBox 改成 `11.784 -0.05 14.225 14.225` 等。
**真相是假警报**：这两个文件的 `<path>` 挂着 `transform="matrix(-1,0,0,1,26,0)"`（x → 26−x 镜像），镜像后字形正好落在 x[1,13]，
**原 `viewBox="0 0 14 14"` 本来就对**；我的 `glyph_bbox()` 只读 `d` 数字、不认 transform ⇒ 一改反而把字形推出框外，**只剩左沿 1px 残片**。
处置：**整段删除** `glyph_bbox`/`fit_viewbox`/`_r3`（原处留复盘注释）。按 transform 感知重体检 78 个源文件 ⇒ 真越界的只有 4 件未引用的 DS 内部结构图。
⚠️ **本页共 8 个源文件带 matrix**（含 4 个 `matrix(0,1,-1,0,1,-1)` 的 90° 旋转）⇒ **以后别用「按裸坐标推算」的方式改图标几何**。
★ 元教训：**改了「自动修正/自动体检」逻辑后，必须目视复核一个受影响的样本** —— 只看探针数字会以为修好了（我这次就是靠肉眼才发现）。
判「图标本体坏 or 宿主 CSS 坏」的利器 = 隔离测试页 `mg-work/r93/ev/icontest.html`。

**★ 踩坑二**：`.r93-ctx` 探针报 175px（应 182）—— 是 `scale(.96→1)` 的 0.2s 过渡中取值（`182×0.96=174.72`），**不是 bug**。

**★ r99 复查（全绿）**：幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` **76 条**与 `vd-r93c.txt` **逐字节相同**（21882 字节）｜双视口 1440 + 1500 全页 + 逐区域滚动裁片 + 设计稿并排对照（`raw/r99-final-umeta-cmp2.png`）。

**产物**：`pages/conversation.html` 616773 → 631381 → **631287 字符**（r99 两拍：+14608 / −35 / −59）；`pages/base.html` **未变**。
新增 `ev/p99a~j`（14 条复查 / umeta 几何 / 菜单截图 / 全元素矩形 / 逐区域滚动 / 图标隔离渲染）· `vd-r99b/c.txt`；
新增 `raw/r99-*.png` 与 `raw/r99v-*.png`（含 `r99v-m1~m3` 拼图）；新增隔离测试页 `ev/icontest.html`。
**回滚**：`before/` 里**没有 r98 终态快照**（该代只存了 r96/r97）⇒ 只能①定点删 `apply93.py` 里标 `★ r99` 的段落（改完直接重跑即自愈）或②`apply93.py --revert` 回 r93c 快照。
已补存 **`before/conversation-r99.html`**（= 本轮终态，作为下一轮基线）。详见 `mg-work/r93/acceptance.md` 第十二章。

### r100（同日第十轮 · **最新**）—— 会话详情页 8 条（**就地返工 `apply93.py`**）

邵先生原话八条：①「GienX」改成「GienCoder」；②所有 `r93-card` 容器内的字号都改成 14px；③「滚动到底部」hover 时**边框颜色不要变化**，图标和文字颜色再**深一级**即可；④`r93-dlist` 的 item **整行都应该可点击**、注意鼠标指针形态；⑤`r93-agent` / `r93-agent2` 这类小卡 hover **加个浅灰底色即可、边框颜色不要变**；⑥`r93-ndesc r93-t12h` 这种文字行**是有背景底色的**、对比设计稿；⑦`class="r93-fh r93-bt"` 这个**折叠后前面的图标异常**；⑧「调用 5 个工具」这个分组下面**是分层级的**、可以**一级一级**点击展开折叠、并且有**层级连接线**。

**逐条落地与实测（1440，`ev/p100b.log`）**：①`gienxCount=0` / `giencoderCount=4` / 助手名 `GienCoder`（另把 `task-detail.html` 那处 `GienX端到端初始化` 一并改掉）②卡内字号直方图 `{"14px":106}` ③hover `color=rgb(31,31,31)`（默认 78）；**`border` 与默认完全一致 rgb(229,229,229) ✓** ④7 行 `cursor` 全 `pointer`；点整行 ⇒ 菜单 182×159 开、`Escape` 关 ⑤hover `bg=rgb(242,242,242)`、**`border` 未变 ✓** ⑥`bg=rgb(247,247,247)` / `radius=12` / `pad=0 12px` / `h=24`，两行中心 x=849.5 / 850 居中 ✓ ⑦⑧内层 Tool call 改真折叠（展开头/折叠头槽**都是 i14**；点一下 `foldH 166→22`、`cardH 132→0`）；层级缩进 **L0=420 / L1=438 / L2=456**（相对 0 / 18 / 36，与设计稿一致），竖导线 1px + 每个 L1 子项 8px 横向肘节。

**★ 本轮新增权威取数（已写入 PAGES P3.11g ⑩ / PLAYBOOK P3.31）**：
- ⚠️ **设计稿 HTML 导出会丢掉 DS 实例自身的底色与圆角**（`容器 225` 的两行 ndesc 只有 `width/height`）⇒ **必须回 PNG 逐像素扫**。
- `.r93-ndesc` 胶囊 = **文字宽 + 两侧 12px 内距**、**24 高**、底 **rgb(247,247,247) = `--color-fill-1`**、圆角 **12px = `--border-radius-xl`**（两行实测 778×24 / 300×24，墨迹内距 13/13 与 13/14）。
- `1393:18521 容器 221` 缩进：折叠/展开头 **0**；`容器 218`（内嵌 Tool call 822×200）**18**、其代码卡 `容器 217`（804×132）**36**；`容器 219`（4 行清单 305×124 @top246）**18**。**设计稿没有画连接线** ⇒ 连接线是本轮新增要求。
- `容器 218` 内两个 `Link`（`fw647:18138` 折叠态 / `fw647:18151` 展开态）是**同一节点的两态叠加**（又一次「变体叠加」陷阱）。

**★ 本轮三个坑**：①`fold()` 工厂的 `o.mt ? …` 把 `mt:0` 当假值 ⇒ 已改 `o.mt != null`；②**绝对定位伪元素不算 flex item** ⇒ 肘节必须 `::before + position:absolute` 才不会把列向 flex 的折叠头挤下去；③`.r93-sumlist::before` 原来是**局部**竖线 ⇒ 本轮把画线职责上移到 `.r93-tree`，避免接缝断线。

**★ r100 复查（全绿）**：幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` 输出与 `ev/vd-r93c.txt` **二进制逐字节相同**（`cmp` 通过，21882 字节）｜1440 全量读数 + 真鼠标 hover×3 + 真鼠标点击（整行开菜单 / 内层折叠）+ 视觉裁片。

**产物**：`pages/conversation.html` 631287 → **634719 字符**；`pages/base.html` **471444 未变**；`pages/task-detail.html` 766710 → **766714**。
新增 `ev/p100a` ~ `p100shot2` 探针 + `vd-r100.txt`；新增 `raw/r100-*.png`（含 `r100-tree-line-zoom.png` 连接线放大、`r100-tools5-open/-collapsed-crop.png` 两态、`r100-d-note2.png` 设计稿对照）。
补存 **`before/conversation-r100.html`**（本轮终态，作为下一轮基线）。详见 `mg-work/r93/acceptance.md` 第十三章。

**待拍板**：③ 底色（`--color-fill-1`）**保留** —— 邵先生只点了「描边」与「前景色」两条，未要求撤底色；若要「连底色也不要」改 1 行。⑧ 的**横向肘节是新增的**（设计稿没画线），若只想要一条竖线、不要 `├─` 肘节，删 2 条选择器即可。

### 执行顺序

```bash
python mg-work/r88/apply88.py             # 设置页（含 PRIOR 四代，自动 converge）
python mg-work/r88/apply88b-fontsize.py   # 字号机制层（含 r93 需求 1 的 LEADING_DERIVE）
python mg-work/r92/apply92.py             # ① 五页顶栏图 + ④ base 权限红
python mg-work/r93/apply93.py             # 需求 2 + ④（**必须最后跑**：写 base + conversation + 9 页 ROUTE，尾部调 apply88b 做 converge）
# 顺序无关的部分：apply88 / apply92 互不影响；apply93 收尾统一过一遍 apply88b
```

---

## 二·b ★ r101（最新一拍 · 会话详情页十一条 · 2026-09-30）—— **新一代，非就地返工**

> 完整版见 `mg-work/r101/acceptance.md`；细则见 PLAYBOOK **P3.32**、PAGES **P3.11g ⑪**。

**① 体位变化（最要紧）**：r93 代**已提交**（`d7e2151`）⇒ 本代**新建** `mg-work/r101/apply101.py`，
注入块 id 换代 `r93-conv-*` → **`r101-conv-css` / `r101-conv-js` / `r101-nav-js`**。
页面里仍留着 r93 的三块注入物 ⇒ 脚本引入 **`GENS` 逐代摘除表**（r93 + r101 一起摘、注入用本代 id），
自检改两层循环。★ `ATTR_HOST='r93-conv-host'` / `ATTR_PAGE='data-r93-page'` **跨代沿用** ⇒ 页面级 CSS 选择器**一字未改**。

**② 十一条**（实测见 acceptance 第一节）：

| # | 落地 | 关键实测 |
|---|---|---|
| ① | `.r93-fh:hover` / `.r93-fc:hover` → `background:transparent` + 前景提到 text-1 | `hov=true` / `bg=rgba(0,0,0,0)` / `color=rgb(31,31,31)` |
| ② | `.r93-t12l` 补 `color:var(--color-text-3)` | 「深度思考」正文 text-1 → text-3（**主动下调**，设计稿实测是 text-1） |
| ③ | `.r93-ib:hover{background:var(--color-fill-2)}`、无边框（撤 r99⑨） | `bg=rgb(242,242,242)` / `sh=none` |
| ④ | `.r93-iblk.r93-cv > svg{10px}`（**槽仍 14×14**） | `slotW=14` / `svgW=10`；折叠前后 `dx=0` |
| ⑤ | Bash 卡头删绿勾 | `.r93-okc` 2→1（「上下文已压缩」保留） |
| ⑥ | `.r93-tbsticky::after` 40px 渐隐（`bottom:-44px` / `z:-1`） | `bg=linear-gradient(rgba(0,0,0,0), rgb(255,255,255))` |
| ⑦ | 产物卡右键菜单（r69 `part-ctx.js` 那套 + 打开方式▸6 项） | 主菜单 6 项 + 1 分隔线 + 子菜单 6 项（彩色品牌图标） |
| ⑧ | `@keyframes r93-spin` 1.2s linear infinite | `state=running` |
| ⑨ | `.r93-fm.r93-ell` + **`.r93-sumrow .r93-t12l`** = 13px | 直方图 `{13px:17, 14px:1, 15px:1}` |
| ⑩ | `.r93-sb` 补 `box-shadow:0 2px 9px rgba(0,0,0,0.07)`（**自造档**） | 剖面 vs 设计稿 **Σ\|Δ\|=3** |
| ⑪ | 骨架屏 Skeleton（复用 DS `giencoder-skeleton-*`，1.1s 后淡出移除） | t≈350ms `n=1`（8 线/1 标题/1 头像）；t≈2000ms **`n=0`** |

**③ 本轮新沉淀的三条规矩**（PLAYBOOK P3.32）：
- **hover 类需求必须带 `matches(':hover')` 读数** —— 只看 `backgroundColor` **不可判定**（透明既可能是命中规则、也可能是默认态）。
- **脚本内注释会原样注入页面** ⇒ 别在 `applyNN.py` 的 `CSS/JS_TMPL/docstring` 里写裸 `<style>`（打爆计数自检）、
  裸 hex（TOKEN-GAP）、裸 `linear-gradient` / 裸字号（页面级计数 +1）。
- **1.1s 级的骨架屏 CLI 截图抓不到**（`open` 本身耗时 ≈1~2s）⇒ 目视取证只能临时改大延时、截完立即还原（并 grep 核对还原）。

**④ 产物**：`conversation.html` 634719 → **671386**（+36667；`sha 544ed8156a78`）；`base.html` 471444 → **471447**（+3，仅 nav id 换名）；
`task-detail.html` **未改**。回滚：`python mg-work/r101/apply101.py --revert` 或 `cp mg-work/r101/before/conversation-r101.html pages/conversation.html`。

**⑤ 待拍板 3 条 + 需复核 0 条**：见第六节 #32~#35（⑤ 删哪枚绿勾 / ⑧ 是否常转 / ⑩ 投影档位；r99 遗留的「hover 无法直证」已闭环）。

---

## 三、r88 ~ r92 做了什么（前情提要）

| 轮 | 需求 | 落地要点 |
|---|---|---|
| r88 | 导航 hover 底 = 选中底；字号滑块重写；新增「已归档任务」页签 | 共享变量 `--r88-navi-active`(#ECEEF2，暗色 #2E323A)；滑块换成整块命中层 + pointer 事件（move/up 挂 **window**）；新页签按 `1393:18344` 还原 |
| r89 | 标题字号与 `.r85-title` 一致；列表卡圆角共用；分隔线深一级 + 图标重画 | `--r88-card-radius:8px` 三处共用；`i_folder12`（12 网格 1:1、坐标 x.5） |
| r90 | aside 内距与基础工作台一致；容器内按钮**必须用 DS 按钮组件**；下拉前缀图标不对 | `.r85-nav-host` 撑满内容盒（244）；行尾钮换 `giencoder-btn -secondary -icon -size-small`；`i_folder` 16 网格重画 |
| r91 | 返回钮 hover 底 = 菜单 hover 底；菜单默认无背景；行尾图标浅一级 | `.r85-back:hover` 共用 `--r88-navi-active` + 补 transition；`.r85-navi` 基类 `background:none`；**`.r88-arch-act > svg`** 单独给 `text-2` |
| r92 | 顶栏装饰背景图；返回钮深一级；`.r85-gt` 左距 12px；「完全访问」转红 | 见 `## 二` 与 `PLAYBOOK P3.23`；④ 只能改 React 源（尾风任意类 + 内联 style 两个盲区） |

★ **r73 全局规则**：`.giencoder-btn:not(.giencoder-btn-size-small){border-radius:8px}` ⇒ 全站按钮口径 **large 8px / small 4px**，别再按设计稿压 6px。
★ **展开态只写 `min-height` 不写 `height`**：DS 给 `height:28px`，min-height 优先 ⇒ 默认 28 / 展开 32 两全；该规则**刻意不带 `body` 前缀**，好让 apply88b 派生 `calc(32px * ratio)`。

---

## 四、★★ 已修掉的真 bug / 陷阱（PLAYBOOK P3.21 ~ P3.24 有细则）

1. **`noClear` 的 DS select** ⇒ `suf.querySelector('.giencoder-select-clear')` 为 null ⇒ TypeError ⇒ 内容区整块空白。**修法：凡"可选子部件"一律判空。**
2. **拖拽的 `pointermove/up` 必须挂 `window`**（挂元素时 `setPointerCapture` 失败就永远收不到 up）。
3. **1px 描边中心线必须落 `.5`** ⇒ 落整数会摊成两列 50% 灰像素（肉眼=又细又虚）。
4. **元素截图超出视口的部分渲染成空白** ⇒ 截图前必须 `set viewport` 并在同链路 `eval window.innerHeight` 核对。
5. **元素截图内取色的坐标 = 元素内相对坐标** ⇒ 先 `eval` 拿「元素 rect − 容器 rect」。
6. ★ **`inject_tail` 别断言 `count('</body>') == 1`**：`base.html` 的 r76 CSS 注释里也出现过一次 ⇒ 改用 **`rfind`** 并要求它就在文件尾部。
7. ★ **裸 `header` 标签选择器在多页会误伤**：avatar 5 个 / task-detail 4 个 ⇒ 用 `header[class*="h-12"]`。
8. ★ **尾风任意类 `[color:var(--x)]` 是构建期产物** ⇒ 新增类名不会进产物 CSS ⇒ 想给 React 渲染元素加新色，要么挂自定义类（自己写样式），要么改 React 源。
9. ★ **`.ws-dropdown-hover` 这类混用类名会重名**（工作目录 / 默认权限各一个）⇒ 探针先枚举，或用 `:has(<独有特征>)`。
10. ★★ **改字号机制后要防「特异性反噬」**：`body .text-xs` 是 **(0,1,1)**，会压掉所有 **单类** arbitrary 工具类（`.leading-[32px]` = (0,1,0)）⇒ 机制层给 size 类派行高时，必须 `:not([class*="leading-"])` 让位，并对要支持的 `leading-[Npx]` **补一条同特异性的派生规则写在后面**（r93 需求 1 根因）。
11. ★★ **导出设计稿的「状态变体」是叠放的** ⇒ 真机块高 = 容器高 − 变体偏移（r93 = 34）；**导出 PNG 的绝对 y 不可当设计坐标**，量总高必须先去掉这层 offset。
12. ★★ **`ui-component` 是不带字号的纯框** ⇒ 字号只能「框高 × 墨迹行距 × 文本宽度反推」三角验证；单看框高会把 12/20 误判成 14/22。
13. ★ **私有区图标字符（U+F0xxx）在实机无字形** ⇒ 退化成豆腐块并改变折行；导出图里的「图标」可能只是 Nerd Font 渲染的数字/符号，**先裁图看清再决定用不用**。

---

## 五、四查（全绿，详见 `mg-work/r93/acceptance.md` 第三 / 六 / 七 / 八 / **九**节）

> ★ 下表是 **r93 ④ 之后**、按官方顺序复跑实测（日志 `mg-work/r93/ev/rerun-④.log` + `vd-r93d.txt`）。

**★ r94 复查（同日第四轮）**：`apply93.py` 幂等 ✓（第二遍 base + conversation 双「已是目标态」）｜`check-syntax` **10/10**（conversation `script=9 style=15`）｜`verify-design` **76 条**（66 warning / 10 info / 0 critical）与 r93 基线 `vd-r93c.txt` **逐字节相同**（首跑曾因我在新注释里写了被扫描的关键词而 +1，改措辞后归零）；读数 `vd-r94.txt`（含假阳性）/ `vd-r94b.txt`（修后）。

**★ r95 复查（同日第五轮）**：同上口径全绿 —— 幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` **76 条**与 `vd-r93c.txt` **逐字节相同**（`vd-r95.txt`）｜视觉/几何 `ev/p95b.js` 全块 **Δ=0**。

**★ r96 复查（同日第六轮）**：同上口径全绿 —— 幂等 ✓（第二遍 base + conversation 双「已是目标态」）｜`check-syntax` **10/10**（conversation `script=9 style=15`）｜`verify-design` **76 条**（66 warning / 10 info / 0 critical）与 `vd-r93c.txt` **逐字节相同**（`vd-r96.txt`）｜视觉 `raw/r96-cmp2.png`（设计 vs 实机同尺度上下对照，前三段逐像素对齐）。

**★ r97 复查（同日第七轮）**：同上口径全绿 —— 幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` **76 条**与 `vd-r93c.txt` **逐字节相同**（17148 字节，`equal: True`，`vd-r97.txt`）｜几何 `ev/p97d.sh` 在 **1440 / 2560** 双档实测（wrap/bottom/sb/composer 右边界全等）＋ `raw/r97-cmp.png`。**回归排除**：`ev/p97f.sh` 把卡内字号临时强制回 12px 再测，12 张卡的高度与溢出量逐项相同 ⇒ 那 2px 溢出是 r96 及更早就有的。

**★ r98 复查（同日第八轮）**：同上口径全绿 —— 幂等 ✓（第二遍 base + conversation 双「已是目标态」）｜`check-syntax` **10/10**（conversation `script=9 style=15`）｜`verify-design` **76 条**（66 warning / 10 info / 0 critical）与 `vd-r93c.txt` **逐字节相同**（21882 字节，`equal: True`，`vd-r98.txt`）｜几何 `ev/p98b.js` 在 **1440 / 2560** 双档实测（内容区 **15px × 59**、卡内 `.r93-t14` 仍 13px、wrap pb **48**、差分卡右对齐账 ⋯−13 / 数字−54 / 名+11）＋ `raw/r98-cmp.png`。⚠ 首跑曾 **77 条**：新增注释里写了裸字号写法（`font-size: 15px`）⇒ **字号检查不跳注释行**（hex 检查会跳）⇒ 改措辞后归零。

**★ r99 复查（同日第九轮）**：同上口径全绿 —— 幂等 ✓（第二遍 base + conversation 双「已是目标态」）｜`check-syntax` **10/10**（conversation `script=9 style=15`）｜`verify-design` **76 条**（66 warning / 10 info / 0 critical）与 `vd-r93c.txt` **逐字节相同**（21882 字节，`equal: True`，`vd-r99b.txt` / `vd-r99c.txt`）｜探针 `ev/p99b.js` 复测十四条（读数见上）+ `ev/p99c.js` 量 umeta 图标几何与 rateline 线↔⋯ + `ev/p99d.sh` 右键菜单展开截图 + `ev/p99f.sh` 逐区域滚动裁片 + **隔离测试页 `ev/icontest.html`**（定位 SKILL 图标的镜像 transform）。

**★ r100 复查（同日第十轮）**：同上口径全绿 —— 幂等 ✓（第二遍 base + conversation 双「已是目标态」，`task-detail` 更名也已收敛）｜`check-syntax` **10/10**（conversation `script=9 style=15`）｜`verify-design` **76 条**与 `vd-r93c.txt` **逐字节相同**（`vd-r100.txt`）｜探针 `ev/p100b.js` 八条逐条复测 + 三处**真鼠标 hover** + 整行点击开菜单 + 层级树开合。

**★ r101 复查（同日第十一轮 · 最新）**：同上口径全绿 —— 幂等 ✓（第二遍 base + conversation 双「已是目标态」）｜`check-syntax` **10/10**｜`verify-design` **76 条**，与 `vd-r93c.txt` **逐行 diff 只剩 1 条**（conversation 渐变 `62 → 63` = ⑥ 的渐隐层，info 级页面统计）｜★ **新增决定性探针 `ev/p101hov.js`**（连查 `matches(':hover')`）⇒ 三个 hover 目标全部 `hov=true`｜**终态一次性取证 `ev/p101fin.sh` + `p101fin.log`**（骨架屏两拍 / 11 条静态读数 / 3 个 hover / dx=0 / 右键菜单）｜双视口 1440 + 2560｜像素：投影剖面 Σ\|Δ\|=3、渐隐带 `r101-fin-fadezoom.png`。

| 查 | 结果 |
|---|---|
| 幂等 | `apply88.py` `457805 → 457805 (+0)`（**且未摘掉 settings 的 ROUTE 条目**）；`apply88b` **10 页全「已是目标态」**（含新页 `conversation.html`）；`apply92.py` **应用 0 / 跳过 8**；`apply93.py` 第二遍起 **base + conversation 双「已是目标态（无改动）」**；**`apply101.py` 第二遍「已是目标态（无改动）」**；`base` / `conversation` 字节 sha 复跑前后一致 |
| 语法/配平 | `check-syntax.py pages/*.html` → **10/10 ALL_OK**（base `script=9 style=14` / conversation `script=9 style=15`） |
| 零影响 | `verify-design.py ./pages` → **76 条**（66 warning / 10 info / 0 critical）；r101 与 `vd-r93c.txt` **逐行 diff 只剩 1 条**（渐变 62→63）；④ 前 9 页 = **75 条**（`vd-r93c-base.txt`）⇒ **唯一新增 = `conversation.html` 的 1 条 `CRAFT-SLOP`**（info 级页面级统计，非缺陷），**warning 66 / critical 0 不变**；base 原有 2 条 `TOKEN-GAP`（`#E2D3F9`/`#30953B`）随块搬到新页（同型同量、只换文件名） |
| 代数标记 | r101 起必查残留：`conversation` 的 `r101-conv-css`/`r101-conv-js` 各 **1**、`base` 的 `r101-nav-js` **1**；**`r93-conv-*` / `r93-nav-js` 必须 0** |
| 路由 | 10 页 `ROUTE` 表各含 `'/conversation'` **恰好 1 次**（counted 断言） |
| 视觉/像素 | 会话详情 `raw/v3-conv-top.png` `v3-conv-bottom.png`（+ `v3-base.png` 对照）；composer 复用 `raw/q-real-composer.png`(真组件 1114×214) vs `raw/q-design-composer.png` / `q-design-bottom.png`；下拉翻向取证 `raw/v3-perm-up.png`；r101 新增 `raw/r101-fin-*.png`（骨架屏 / 右键菜单 / 渐隐带 2× / 全页） |

⚠ 跑完必须还原工作区：`git checkout -- pages/gaps.log` + `git checkout -- mg-work/kanban/r13/chk/ && git clean -f mg-work/kanban/r13/chk/`。

---

## 六、待拍板 / 待确认（邵先生）

1. ★ **r92 ① 的范围**：现落**基础工作台 5 页**。若「全站 9 页」也要，需同时决定研发页顶栏底色（`#E5EDF5`）是否一起换掉。
2. ★ **r92 ① 的尺寸**：现为素材原尺寸（点径 4px）+ 视口 >1580 时 x=340 接缝。
3. **r92 ④ 的红色档**：现 `--color-danger-6`（`#F53F3F`）；嫌艳可降 `--color-danger-5`。
4. **r90 三处「按 DS 组件口径、偏离设计稿」**：行尾钮圆角 6→4px、清空钮 8px、行尾钮描边 `border-2`。
5. ★ **r91 行尾图标色**：现 `text-2`(#4E4E4E)，设计稿实测是 `#6B6B6B`（`--color-neutral-7`）⇒ 要精确贴稿就改 `.r88-arch-act > svg` 一行。
6. **r89 遗留**：24px 极限字号档工具条溢出卡片右缘 18px（默认档无此问题）。
7. **返回钮与菜单项几何不一致**：`.r85-back` 高 32 / 圆角 4px，`.r85-navi` 高 36 / 圆角 8px（r91 只统一了底色）。
8. **`#ECEEF2` 是否提到 DS 色板**：现为页面级变量，使用面已扩到 3 处。
9. **「清空归档任务」无二次确认**；**全站 Input 圆角是否统一 8px**；**r90「全局强制用 DS 按钮」是否贯彻到全站**。
10. **r93 结转 —— Δ2 级微差**：搜索资料卡 152→150、改动汇总卡 302→300（均在 1 行行高内，疑似字体度量）。
11. **r93 结转 —— 字体度量差异**：上下文注入卡设计稿（MiSans）5 行 vs 实机（Mona Sans）4 行 ⇒ 现用 `min-height:150px` 保高；若要严格 5 行需换字体或调 `letter-spacing`。
12. **r93 ④ 新页上下文丢失**：`conversation.html` 是**整页重载** ⇒ 从 aside 点会话项跳过去后，**选中态/滚动位置回到默认**（React 重新渲染）。要不要「hash 带会话 id + 落地后回高亮该会话」？
13. **r93 ④ 新页标题**：现 `<title>会话 · 基础工作台</title>`；是否要跟「会话名」联动（需外壳暴露会话数据）。
14. **r95 结转 —— `.r93-agent` 那 4 张 agent 卡要不要也「均分撑满」**：现按内容宽**左对齐**（设计稿固定排版），
    r95 只把它们的**容器**（`.r93-bottom > *`）改成撑满；若要求 4 张卡 `flex:1` 平分 860，说一声即可（一行 CSS）。
15. **r95 结转 —— `.r93-bub`（用户气泡 728px）要不要也撑满**：现**右对齐不满宽**（设计稿语义）。
16. **r95 结转 —— 超宽视口的理论 10px 差**：`.r93-wrap` 的 `50%` 基数是**滚动容器内容盒**（带 `both-edges` gutter ⇒ 1142），
    而 `.r93-bottom` / composer 的基数是 **1162** ⇒ **仅当 `50% > 860px`（视口 ≈2000px 以上）**时两者会差 ~10px；
    1440 / 1920 实测**完全一致**。要彻底消掉需给 wrap 补 `calc(50% + 10px)`（依赖滚动条宽度常量，**脆**，暂不做）。
17. **r96 结转 —— 「调用 5 个工具」汇总清单（`.r93-sumrow`）标题色**：设计稿 `fw647:16189`「更新任务清单」= **#1F1F1F（text-1）**，
    而我们 `.r93-sumrow` 给的是 `text-3` ⇒ 4 行标题偏浅。**本轮刻意未动**（用户只提了 `.r93-t14` 的默认色与 `.r93-t14.r93-c2`），
    要不要按稿改成 text-1？
18. **r96 结转 —— rateline 后两段 −7px**：因实机字体比设计稿窄 7px（Link 134 vs 142）。
    若要**逐像素钉死**就必须写死 `width:142px`（但会 `overflow:hidden` 截断长字），**不建议**。
19. **r96 结转 —— `.r93-dmore`（任务产物区右上「更多」）色 / 盒**：现 24×24 + `text-2`，与 rateline 新按钮（`text-3`）不一致；
    设计稿该处未核。要不要统一成 `.r93-rbtn` 口径？
20. ★ **r97 结转 —— 「整个内容的模块元素等宽」还剩两处按设计稿**：现在**全宽块**（wrap / 状态条 / agent 行 / 输入卡 / 告警 / 改动汇总 / 产物区）已全部等宽；仍**刻意未动**两处（都是设计稿的固定排版）：
    ① `.r93-card` / `.r93-todocard` = `calc(100% - 18px)` + `margin-left:18px`（设计稿 `容器 185` = `width:822px; left:18px`，右缘贴齐、左侧缩进 18）；
    ② `.r93-bub` 用户气泡 = `728px` 右对齐不满宽（设计稿语义如此）。
    若邵先生要「连卡带气泡也全部拉到 860」，分别改 2 行 / 1 行即可 —— 但那会**偏离设计稿**，故等发话。
21. **r97 结转 —— `.r93-pre--tight`（Bash 卡代码）现为 13px / 行高 16px**：统一字号后代码行高与字号之比 1.23，偏紧（卡高不变、不裁切，仅观感）。若嫌挤，给 `.r93-pre` 单独留 12px（改 1 行）。
22. **r97 结转 —— agent 卡宽度比例**：现 `flex:1 1 auto` 按内容宽比例吃余量（实测 1440 = 229/205/217/191）；设计稿是 190/169/197/**255**（第 4 张明显更宽）。若要逐张对齐设计稿宽度需写死 basis（脆），暂不做。
24. ✅ **[r99 已解决]** ~~`.r93-dsb`（差分卡里那条 6×128 滚动条）是本轮唯一「静态装饰」~~ ⇒ **r99 ① 已按邵先生要求删掉**（规则 + 模板 `<i>` 双删），`.r93-dlist` 改 `overflow-y:auto`。
25. **r98 结转 —— 15px 是字号档位之外的值**：DS 只有 body-3=14 / title-1=16，15px 只在本页适配层用 `calc(15px * var(--ui-fs-ratio))`，**未动 token**。
26. **r98 结转 —— 卡内文案比设计稿大 1px**（设计 14 → 本页 15）：这是 ①「内容区统一 15px」的必然结果，③ 只覆盖颜色 / 间距 / 结构。
27. **r99 结转 —— 差分卡行的右键菜单「刻意不做键盘导航」**：只实现 `pointerdown` / `blur` / `resize` / `scroll` / `Escape` 关闭，**未做** ↑/↓/Enter 移动焦点与 focus trap（与 `task-detail` 的 `.td-ctx` 保持一致）。若要无障碍完整版，说一声即可（约 20 行）。
28. **r99 结转 —— `regen`（重新生成）图标是手写 14 栅格**：设计稿 `1393:18477` 里该图标是 DS 实例（`fw647:14503`），**源文件里没有可复用的 path**（结构树只给节点名）⇒ 按 `design-rgb.png` 逐像素分离后手写（弧 + 左下实心箭头）。若 DS 后续产出官方图标，替换即可。
29. **r100 ③ 结转 —— 「滚动到底部」hover 的底色**：本轮只按原话撤掉了**描边**变化并把前景色深一级，`--color-fill-1` 底色**保留**（原话没提底色）。若要「连底色也不变」，把 `.r93-tobottom:hover` 里的 `background` 删掉即可（1 行）。
30. **r100 ⑧ 结转 —— 层级树的横向肘节是新增的**：设计稿 `1393:18521` 没有画连接线（PNG 该区间只扫到卡片底与描边）⇒ 竖导线 + `├─` 肘节都是本轮按原话补的。若只要一条竖线：删 `.r93-tree > .r93-fold::before, .r93-tree > .r93-sumlist > .r93-sumrow::before` 那条规则。
31. **r100 ① 结转 —— 更名范围**：`task-detail.html` 的「来源需求」示例标题也一并改了（`GienX端到端初始化…` → `GienCoder端到端初始化…`）；该文件里另两条**历史注释**中的 `GienX` 字样**刻意保留未动**（不进产物）。若要全库抹净说一声。
32. ★ **r101 ⑤ 结转 —— 删的是哪一枚绿勾**：全页 `.r93-okc` 共 2 处，本代删的是 **Bash 卡头**那枚（判据：它无文案可指、且与 ④ 的箭头同块相邻）；
    **「上下文已压缩」行首那枚保留**（带文案「已压缩 24 条历史记录」）。若指的是后者，一行改。
33. ★ **r101 ⑧ 结转 —— 图标是否要常转**：现**常转**（`r93-spin` = `1.2s linear infinite`）。若只要 hover 时转，去掉模板里的 `r93-spin` 类即可（CSS 留着无害）。
34. ★ **r101 ⑩ 结转 —— 投影档位**：现 `0 2px 9px rgba(0,0,0,0.07)`（像素剖面 Σ\|Δ\|=3，与 10px 档打平，选 9px 因上方外溢更小）。这是唯一的旋钮。
35. ✅ **[r101 已闭环]** ~~r99 ① 结转：折叠头 hover 色无法运行时直证~~ ⇒ **r101 新增 `matches(':hover')` 决定性探针**，展开头 / 折叠头 / 图标按钮三个 hover 目标全部 `hov=true` 且读数正确。
36. ★ **r101 第二批 ⑤ 结转 —— 菜单是「替换」不是「合并」**：r99 ⑦ 那张 4 项菜单（查看文件 / 查看改动 / 复制文件路径 /
    撤销此文件改动）**已整段删除**，现在汇总行右键 / 左键 / 「⋯」三处与产物卡共用同一张 6 项菜单。若其实想要**并集**，说一声即可。
37. ★ **r101 第二批 ⑦ 结转 —— 折叠动效只做了单向**：展开有 0.34s 回弹，**收起仍是瞬收**（反向要高度动画 + `overflow:hidden`，
    会剪掉卡内向上翻的 `.r93-pop`）。若要反向也动，说一声。
38. ★ **r101 第二批 ① 结转 —— 毛玻璃参数 + 一个副作用**：`--r93-glass` = `rgba(255,255,255,0.72)` / 暗色 `rgba(35,35,36,0.72)` + `blur(12px)`；
    **无设计稿依据**（设计稿没有「滚动时标题栏压住内容」这一帧）。嫌重/嫌轻改这一处即可。
    副作用：标题栏盖住的滚动口**最上 44px** 里界面元素**点不到**（滚过去的内容能滚、但点击被标题栏接住）——判定可接受，写进验收了。
39. ★ **r101 第二批 ② 结转 —— 70% 落在 6 页**：base / conversation / avatar / skills / automation / settings
    （= 所有带 `r92-hdr-css` 的页面）；研发工作台 4 页（dev / kanban / req-kanban / task-detail）本来没铺这张图 ⇒ 未动。
40. **`.r93-dmore:hover`（灰卡上那枚「⋯」）仍是「白底 + 1px 描边」**（r99 ⑨ 的设计稿实测值）：本批只点了「菜单内容一致」，
    没点按钮的 hover ⇒ 与 `.r93-ib:hover`（浅灰底、无边框）**仍不统一**。要统一说一声（一行）。
23. 更早遗留：r86 三处 DS-vs-设计稿差异；r84 avatar 确认态按钮组是否再挪 8px；r83 三条；r81 三条；r79 `r74-ripple` 死代码；r77 滚动条 hover；r74 动效 300ms 上限；`pages/gaps.log` 与页面不同步。

---

## 七、下一轮接手清单（按顺序）

1. 读本卡 → `git status` → 复跑补丁确认幂等：
   `mg-work/r88/apply88.py` → `mg-work/r88/apply88b-fontsize.py` → `mg-work/r92/apply92.py` → `mg-work/r93/apply93.py`
   → `mg-work/r87/apply87a-select.py` → `mg-work/r86/apply86.py`（**后两个被 r88 的 PRIOR 涵盖，重复跑也是 `+0`**）。
2. 改页面**一律走 `mg-work/rNN/applyNN.py`**，体位 = 「先 `strip_all(当前页)` 取净底 → 再注入」⇒ **改完直接重跑即自愈**。
   **例外**：上一轮尚未提交时的即时返工 ⇒ **就地修订原补丁、不另起代数**（判据：`git status` 里仍是 ` M`）。
   ★ 现状（2026-09-30 20:1x）：`r86 ~ r100` **已提交**（`d7e2151`）；**`r101` 是未提交的新一代**
   （`mg-work/r101/apply101.py`，承接 r93 代的产物、覆盖 `pages/{base,conversation}.html` + 6 页顶栏图块）⇒
   邵先生下一轮若仍针对**会话详情 / 新页 / 顶栏图 70%**，**就地改 `mg-work/r101/apply101.py`**（不另起代数）；
   若针对**设置页 / 字号机制 / 其它页**，回到 `apply88.py` / `apply88b-fontsize.py` / 新起 `r102`。
3. 收尾四件套：`check-syntax.py` → `verify-design.py ./pages`（**必须传目录**）→ 与上一轮读数**逐条 diff** → 清理 → 覆盖更新本卡 + `mg-work/rNN/acceptance.md`。
4. 🚫 **默认不 commit / 不 push**：干完只汇报改动清单。

---

## 八、回滚与取证

```bash
# ★ r93 回滚（首选：脚本自带）
python mg-work/r93/apply93.py --revert     # ④：删 pages/conversation.html + 摘 base 的 r93-nav-js + 9 页 ROUTE 各 −1 条（base 回到「需求 2 后」= 608256）
# 或按文件回滚（④ 前的快照，文件名必须与原页面同名）
cp mg-work/r93/before/base-r93c.html      pages/base.html        # base → ④ 前（608256）
cp mg-work/r93/before/settings-r93c.html  pages/settings.html    # 其余 8 页 → ④ 前（各少 1 条 ROUTE）；同型还有 avatar/dev/kanban/req-kanban/skills/automation/task-detail 的 *-r93c.html
rm -f pages/conversation.html                                     # 摘掉 ④ 新建页
# 再回到 r93 需求 2 之前
cp mg-work/r93/before/base-r93pre.html    pages/base.html        # base → r92/r93① 态（471920）
cp mg-work/r93/before/base.html           pages/base.html        # base → r92 收尾态（含 r87-ui-css 块 r92 态）
# r92 回滚
cp mg-work/r92/before/<page>.html pages/<page>.html        # base/settings/avatar/skills/automation
# r88 系回滚（设置页 → r87 态）
cp mg-work/r88/before/settings.html pages/settings.html
# 其余 8 页的 r88 增量（仅 r87-ui-css 块内高度跟随）→ 用 r87 脚本收敛回 r87 态
python mg-work/r87/apply87b-fontsize.py
# ⚠ 若只想回滚 r93 需求 1（不动需求 2/④）：把 apply88b-fontsize.py 里的 LEADING_DERIVE 与 :not([class*="leading-"]) 撤掉后重跑
# r86 / r85 / r84 / r82 回滚
cp mg-work/r86/settings.before.html pages/settings.html
cp mg-work/r85/settings.before.html pages/settings.html
cp mg-work/r84/avatar.before.html   pages/avatar.html
cp mg-work/r82/before/<page>.html   pages/<page>.html
```

| 目录 | 关键内容 |
|---|---|
| `mg-work/r93/apply93.py` | ★ 需求 2 + ④ 全量（25 块 + composer + 44 内联 SVG；**④**：独立页 `conversation.html` 由 base 净底重建 + 9 页 `ROUTE` 各 +1 + base 的 `r93-nav-js` + 下拉翻向 + `--revert`）；需求 1 在 `r88/apply88b-fontsize.py` |
| `mg-work/r93/acceptance.md` | ★ r93 验收档案（需求 1 根因/修法/实测；需求 2 三点拍板/变体叠加/字号体系表/逐块几何核对/结构级修正/暗色；**⑥ r93 ④：侦察结论 / 落地方式 / 四查 / 回滚**；改动文件；遗留） |
| `mg-work/r93/before/` | **r93 前置基线 10 页** + **9 个 `*-r93c.html`（④ 前快照）** + `base-r93pre.html` |
| `mg-work/r93/ev/` | `p93-dom/open/geo/geo2/click/lh`（需求 2 探针）/ **`p94-dom.js` `p94-outer2.js` `p94-conv.js`**（④ 侦察）/ `vd-r93.txt` `vd-r93c-base.txt`(75) `vd-r93c.txt`(76) `vd-r93d.txt`(复核) `rerun-④.log` / `base04/` |
| `mg-work/r93/raw/` | ★ 设计稿导出（`design-1393-18748-s1.png` `design-rgb.png` `spec.json` `sel-1393-18748.json` `asset/`）+ 8 个量测脚本（`parse-spec` `flatten-spec` `extract-text` `scan-type` `scan-lines` `measure-pad` `list-icons`）+ 取证裁剪图（`q-*.png` `crop-band*` `d9-s2..s9`）+ `v2-*.png` 实机分段截图 |
| `mg-work/r92/apply92.py` | ① 五页顶栏图 + ④ base 权限红；含可复用的 `replace_once` / `inject_tail`（`rfind('</body>')` 版） |
| `mg-work/r92/acceptance.md` | r92 验收档案（四条 / 素材实测 / 改前改后表 / 5 态表 / diff / 四查 / 待拍板） |
| `mg-work/r92/before/` `ev/` `raw/` | r92 基线 5 页 / 21 个探针与脚本 / 汇报三图 |
| `mg-work/r88/apply88.py` `apply88b-fontsize.py` | 设置页全量（r88~r93 需求 1 六代标记 + `PRIOR` + select 判空）+ **全局字号机制层** |
| `mg-work/r88/ev/` `raw/` | r88~r91 的 50+ 探针与截图；`diffgrp.py`（逐行分组 diff）通用 |
| `mg-work/r85/raw/design_1389-18725.png` | 设置页内容设计稿（2x / 1680×1838 / RGBA） |

⚠ `mg-work/r80/raw/` 里的设计素材（`svg/`）**别删**，是取不到数时的唯一退路。
⚠ `assets/icons/*.svg` 是仓内 DS 图标库；`assets/images/` 是画面素材。
⚠ 页面 bundle 里**早已内联 DS 全套组件 CSS** ⇒ **新增控件前先 grep 组件类名**。

---

## 九、环境速记（Windows，逐条都是踩过的）

- 预览一律 **`file://` 直开**（内置预览面板不带 hash ⇒ 渲染出错误的壳）；改完带 `?v=<ts>` 防缓存。
- ⚠ `file://` 下「改前基线」**文件名必须与原页面同名**（否则外壳按名查路由表落回 base 壳）—— `mg-work/rNN/before/*.html` 已按此命名。
- ⚠ **同一时刻只能有一个 agent-browser 链路**（共用标签页，并发必串味：症状「元素不存在 / url=blank / probe 缺失」）。
  整条链路（`set viewport` → `open` → `wait` → `eval/screenshot`）**要在一次 bash 调用里跑完**；长脚本 `run_in_background`。
- ⚠ ★ **鼠标"按住"跨 bash 调用 / `batch` / 长链会 SIGTERM 掉 daemon** ⇒ 拖拽用「单次 `eval` 内合成 PointerEvent 序列」。
- ✅ `screenshot <选择器> <路径>` = **元素截图**（位置参数；`--selector` 不认；`""` = 全页）。**`--full-page` 会静默失败，别用**。
- ⚠ **元素截图超出视口部分渲染成空白** ⇒ 先 `set viewport 1440 900` 并 `eval window.innerHeight` 核对。
- ⚠ **元素截图内取色 = 元素内相对坐标**（先减容器 rect）；**截浮层要全页截图再 Pillow 裁**（元素截图会裁到元素边界）。
- ⚠ **程序化 `el.click()` 的 `detail === 0` 会被当键盘触发**（按 `detail` 分流焦点的逻辑会因此飘出焦点光圈）⇒ 取证一律用真鼠标 `agent-browser click <sel>`。
- ⚠ `agent-browser eval` 返回**双层 JSON 字符串**（`json.loads` 两次）；**每次量测前必须重新 `open`**。
- ⚠ `eval "$(cat probe.js)"` **路径写错会静默返回 null** —— 链路照跑却几何全 0，**先查脚本文件在不在**。
- ⚠ **`getComputedStyle(el)['--custom-prop']` 恒为 `undefined`** ⇒ 用 `getPropertyValue('--x')`。
- ⚠ **沙箱 heredoc 会吞反斜杠** ⇒ 复杂正则/脚本一律**用 Write 工具落文件再跑**（本代又踩）。
- ⚠ Python 里 `/tmp` **不存在**（Windows）⇒ 临时文件写仓内或 `mg-work/rNN/ev/`。
- ⚠ **超长链式 bash 命令会报 `sandbox-center cmd decisionRecord missing actual resource subject`** ⇒ 拆成单条命令。
- ⚠ **大文件上 `difflib.SequenceMatcher` 会跑到 SIGTERM**（500KB 单行 bundle）⇒ 改用「公共前缀/后缀」或「按注入块 id 摘掉」定位窗口。
- 禁整文件 Read `pages/*.html`（单行 bundle 600+ KB）→ 用 Python 只打印目标片段。
- ⚠ 本机 `grep` 查中文一律返回空 → 中文用 Python 读（`grep` 只用于纯 ASCII 锚点）。
- ⚠ **`pages/*.html` 是 CRLF**：`wc -c` 报字节数、Python 文本模式读转 LF ⇒ 字符数与字节数差异巨大（本轮 base.html 字节 629434 / 字符 605980，**勿混用**）。
- 收尾跑 `check-syntax.py` / `verify-design.py` 会**污染工作区**（`mg-work/kanban/r13/chk/*.js`、`pages/gaps.log`）
  ⇒ 跑完必须 `git checkout -- pages/gaps.log && git checkout -- mg-work/kanban/r13/chk/ && git clean -f mg-work/kanban/r13/chk/`。
  ⚠ `chk/*.js` 是**被跟踪的文件**，别 `rm -f` 一把梭。
  ⚠ `verify-design.py` 在**仓库根**（不在 `mg-work/`），且**必须传目录** `./pages`。
- **推 GitHub**（三步）：
  ① `env | grep -i proxy` **现查** —— 注入代理端口每轮会变（实测 53395 / 62399），对 `github.com:443` 稳定 502 ⇒ 先清掉 `env -u https_proxy -u HTTPS_PROXY -u http_proxy -u HTTP_PROXY`；
  ② 出口 `http://127.0.0.1:7890`；③ 认证：PAT 在 `~/.git-credentials`（`icacls` 收紧过），推送带 **`-c credential.helper=store`**：

  ```bash
  env -u https_proxy -u HTTPS_PROXY -u http_proxy -u HTTP_PROXY \
    git -c credential.helper=store \
        -c http.proxy=http://127.0.0.1:7890 -c https.proxy=http://127.0.0.1:7890 \
        -c http.version=HTTP/1.1 push origin main
  ```

  判据：出现 `main -> main`。⚠ 认证缺失时报 `could not read Username … terminal prompts disabled`（非交互不弹窗）—— **别误判成网络问题**。
- agent-browser CLI 绝对路径：`C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js`
  （用 `C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe` 跑；**不在 PATH**）。
- ★ **容器宽度：先分清「要流式」还是「要保内容盒」**（★ r95 定论，取代 r94 旧做法）
  - **要流式（首选）**：子块写 `width:100%`、要留左缩进就 `calc(100% - 18px)`，容器 padding 只留纵向 ⇒ **右侧自动撑满**；
  - （旧·r94）子元素固定像素宽时用 `box-sizing:border-box` + 左右对称 padding 把「内容盒」保回原宽 ——
    ⚠ 这只在容器宽**恰等于设计稿**时才对，**容器一变宽右侧就留白**（r95 用户就是为此提的需求）。
  - ⚠ **`overflow` 容器的滚动条会占宽** ⇒ 同一页里「有滚动条的列」与「无滚动条的列」各自 `margin:auto` 居中会
    **差半个滚动条宽**（r95 实测 5px ⇒ 三组元素三条右边界 1265/1270/1280 打架）
    ⇒ 用 **`scrollbar-gutter: stable both-edges`**（两侧各让等量 gutter，内容恒同轴）。
  - 取证口径：**以不会被改动的锚元素**（本页 = composer 外壳）右边界为基准，逐块算 Δ ⇒ **全块 Δ=0 才算对齐**（`ev/p95b.js`）。
- ⚠ **容器里的「同类卡片」要分清是不是「容器」**：本页 `.r93-bub`（728 气泡，右对齐）与 `.r93-agent`
  （4 张按内容宽左对齐）**不属于**「右侧要撑满」的容器 ⇒ r95 **刻意未动**（它们是设计稿固定排版）。
  反之：把「设计稿里的**假滚动条**」（绝对定位色条 `.r93-vsb`）换成真 `overflow-y:auto` 时，⚠ **只给纯文本卡加**
  （`.r93-card--ctx`）；`.r93-card` 基类**刻意不写 overflow**（卡内路径 popover 要溢出卡片）。
- ⚠ **门禁会把注释里的 CSS 关键词也算进去**（r94 实测：新注释里写 `radial-gradient` ⇒ `verify-design` 的「渐变处数」+1，
  以致与基线 diff 非零）⇒ **新注释别写** `gradient` 这类被扫描的字面（同「断言 token 不进注释」）。
- ★ **把外壳真实组件（React 渲染）钉在容器底部复用时，它的下拉/弹层要「翻向」**（r93 ④）：
  真 select 默认**向下**弹（`top:calc(100% + 4px)`），容器若是 `overflow:hidden` 的 `main` 底部 ⇒ 弹层被裁
  （实测「默认权限」popup y 871..997 而 main 底 892，只剩 21px）⇒ 页面级适配写
  `top:auto!important; bottom:calc(100% + 4px)!important`（`.giencoder-select-popup` + `[aria-label='权限选择']`）；
  ⚠ `calc(100% + 4px)` **含 `%`** ⇒ 不会被 `apply88b` 的 `unscale()` 正则改坏（它只认 `calc(<数字>px * var(--ui-fs-ratio))` 或裸 `Npx`）。
- MasterGo：MCP 在 **20678**；**截图 HTTP 接口在 30678**（详见 PLAYBOOK P7）。设计稿取数 scale 用 **2.0**。
  ⚠ **导出 PNG 是 RGBA，未绘制处 `alpha=0`** ⇒ 取色前先 `alpha_composite` 白底（否则 `convert('RGB')` 变纯黑，误判成"标签条盖住内容"）。
  ⚠ ★ **设计稿导出图里「状态变体」是叠放的**（r93 实测每块 +34px）；`ui-component` **不带 font-size**；私有区图标字符实机**无字形**。
- ★★ **设计稿取数有两个源，别只会用 PNG**（r96 ⑤ 的重大提速）：
  1. **`raw/design-1393-18748.html`（设计稿导出的带样式 HTML）＝ 权威源**：`data-node-id` / `data-name` /
     `style="width;height;left;top;gap;color;font-size;line-height"` 全是**精确值**，还有 `props='{"尺寸":"14"}'` 这类
     DS 实例参数 ⇒ **先 grep 它**（`S.find('Token 速率')` / 按 `data-name` 搜），比逐像素扫图快一个数量级。
  2. **`raw/design-rgb.png`（1x 整页导出）＝ 校验源**：只用来①**验色值**（该图色值准确，r96 实测图中图标 = (107,107,107)
     与该 HTML 里其它 `#6B6B6B` 逐字一致）②**反推形状**（`ui-component` 这种**没导出独立 svg** 的实例只能靠点阵还原）
     ③量**渲染后的实际位置**（导出时缺 `left/top` 的元素）。
  ⚠ 两者**必须交叉验证**：只信 HTML 会漏掉「导出缺 left/top」的元素；只信 PNG 会把「相邻元素宽度」当成「线宽」
  （r96 ⑤ 就是把「容器 246 的 56 宽」当成了分隔线宽度 ⇒ 画出 56×1 横线）。
- ★ **改「工具类的默认色」前先枚举它的全部使用点**（r96 ③）：`.r93-t14` 在 14 处被用、其中 9 处由**别的类**
  （`.r93-ft` / `.r93-nt` / `.r93-dname` / `.r93-c1` / `.r93-fc` / `.r93-sumrow` …）给色 ⇒ 改默认值只影响「裸用」的那几处。
  做法：跑一个探针**按 `computed color + className` 分组计数**（`ev/p96a.js` 的 `t14dist`）⇒ 一眼看出改动波及面。
  ⚠ 同特异性 (0,1,0) 的规则**后定义者胜** ⇒ 新默认值要写在所有覆盖类**之前**（或直接提高特异性，如 `.r93-t14.r93-c2`）。
- ⚠ **给基类加 `font-size` 的波及面 = 「无类名文本」**（r96 ②）：`.r93-card { font-size:13px }` 后，
  卡内自带 `--font-size-*` 的（`.r93-pre` 12px、`.r93-t12*`、`.r93-t14*`）**统统不受影响** ⇒ 只有裸文本会变。
- ★★ **`*` 的通配符不贡献特异性**（r97 ①）：`.r93-card *` 看着像 (0,1,1)，其实是 **(0,1,0)**，与
  `.r93-pre` 同级 ⇒ **被写在它后面的同级规则反超**（实测：37 处变 13px，唯独 5 处 `.r93-pre` 仍 12px）。
  想「后代通配 + 压过所有单类」就把类名写两遍：**`.r93-card.r93-card, .r93-card.r93-card *`** = (0,2,0)。
  （不用 `!important`；也不要靠「把它挪到块末尾」—— 那正是「后写者胜」的脆弱写法。）
- ★★ **`width: N%` 的基数 = 父盒**（r97 ③）：同一页里想让「内容列 / 底部列 / 复用来的真组件」等宽，
  只要它们**父盒不同宽**（滚动内容盒 vs pane vs 带 `px-*` 的 hero 子盒），`50%` 算出来就**不是同一个数**
  —— 1440 下被 `min-width` 兜住看不出来，**视口一宽就露馅**（2560 实测差 24px，用户看到的是「两端各短一截」）。
  排查口径：在**两个视口**（如 1440 + 2560）各测一遍 `getBoundingClientRect()`，看右边界是否全等。
  修法二选一：① 把父盒的基准差补回去（`calc(50% + Δ)`；Δ 依赖滚动条宽时要**先把滚动条宽显式钉死**）
  ② 清掉父盒的横向内距（`padding-left/right: 0`）让父盒 = 目标基准。**优先 ②**（不引入魔数）。

---

## 十、★ 页面路由表 / 新开一页的范式（r93 ④ 查明）

**`pages/` 下每一个页面都是完全自包含的独立 html**（顶栏 + aside + 外壳在**每份文件里各有一份**）——
**没有共享布局文件、没有真实的客户端路由**。页间跳转靠每页内嵌 `<!-- SHELL-NAV-FIX v5 -->` 脚本里的 `ROUTE` 表 + `hashchange`：

```js
var ROUTE = { '/': 'base.html', '/base': 'base.html', '/dev': 'dev.html', '/kanban': 'kanban.html',
              '/req-kanban': 'req-kanban.html', '/task-detail': 'task-detail.html', '/avatar': 'avatar.html',
              '/automation': 'automation.html', '/skills': 'skills.html', '/settings': 'settings.html',
              '/conversation': 'conversation.html' /* ← r93 ④ 新增，10 页各一份、逐字相同 */ };
```
> 外壳自己的 `navigate()` 在 **`file://`** 下才真跳页；**`http://`** 下只改 hash（⇒ 预览用 `file://` 直开）。

- **顶栏「工作台切换」页签**由另一段 `<!-- SHELL-TABS-FIX v4 -->` 管（`FILE={base,dev}`、`DEV_PAGES={dev,kanban,req-kanban,task-detail}`）；「某页属哪个工作台」**grep 每页 bundle 里的 `DEV_PAGES`**，别凭页面名推断。
- **新增一页的范式**（r93 ④ 即是）：
  1. **由某页净底重建**（`base.html` 摘掉本代注入块后的净底 = 新页的唯一来源），**不要手工复制**；
  2. 换 **根级判据**：`<html lang="zh-CN" data-rNN-page="<slug>">` + 改 `<title>`；
  3. 页面级 CSS 全部挂 `html[data-rNN-page='<slug>'] …`；
  4. 在**全部页**（含新页自身）的 `ROUTE` 表尾插一条 `'/slug': 'slug.html'`（幂等 `replace_once` + counted 断言）；
  5. 若「从 X 页跳过去」是交互需求 ⇒ 在 **X 页**注入一个小 nav 脚本（捕获阶段拦目标 widget ⇒ `location.href`）。
- ⚠ **`file://` 下 localStorage 不跨页面共享**（独立页天然拿不到「源页的选中状态」）⇒ 需要传参就用 hash。
- ⚠ `--revert` 必须把「新页文件 + 源页 nav 脚本 + N 页 ROUTE 条目」**一起**退掉（`apply93.py --revert` 即如此）。

# GienCoder Design Engineering

> GienCoder 设计工程 — 基于 MasterGo 设计稿 + GienCoder Design System 的页面还原交付物。

## 快速开始

每个 HTML 文件都是**完全独立的静态页面**（CSS/JS 全部内联），双击即可在浏览器中打开预览，无需安装任何依赖、无需启动服务器。

```
pages/
├── base.html           ← 基础工作台（对话框 + 工作空间切换 + 会话列表）
├── dev.html            ← 研发工作台（代码仓库 + 构建流水线）
├── avatar.html         ← 数字分身（人格 / 画像 / 工作风格 / 工作流程 + AI 对话栏）
├── automation.html     ← 自动化（定时任务编排）
├── skills.html         ← 技能 Skills（能力与工作流管理）
├── settings.html       ← 设置（外观 / 账户 / 通知 / 版本信息）
├── kanban.html         ← 任务看板 · 研发工作台（四泳道任务卡）
├── req-kanban.html     ← 需求看板 · 研发工作台（需求拆分任务卡）
├── task-detail.html    ← 任务详情 · 研发工作台（左：描述/属性/动态，右：AI 会话）
└── conversation.html   ← 会话详情（对话/轨迹双页签 + 工具调用树 + 全屏/文件预览侧栏）
```

> 共 **10 个独立页面**。左栏「会话任务」在**任意页面**点击都会跳到 `conversation.html`（r105）。

## 页面说明

| 文件 | 页面 | 主要功能 |
|------|------|----------|
| `base.html` | 基础工作台 | 对话输入框、大模型选择、工作目录选择、权限选择、会话操作下拉菜单、工作空间切换浮窗 |
| `dev.html` | 研发工作台 | 代码仓库入口、构建流水线、依赖扫描、发布管理 |
| `avatar.html` | 数字分身 | 人格/画像/工作风格/工作流程四卡（卡体可滚动）、长期记忆/知识库/存储位置三行卡、「通过对话完善数字分身」拉出与 main 平级的 AI 侧栏（可拖动改宽） |
| `automation.html` | 自动化 | 定时任务列表、运行状态、调度计划 |
| `skills.html` | 技能 Skills | 技能卡片网格、内置/可安装标签 |
| `settings.html` | 设置 | 返回链接、设置分组、通用/关于 |
| `kanban.html` | 任务看板 | 「待办 / 进行中 / 待确认 / 已完成」四泳道、卡片 hover 出现「执行 / 转派」、创建任务弹窗、看板协作弹窗、日期选择器 |
| `req-kanban.html` | 需求看板 | 需求拆分任务卡（拆分需求项 / 条目 / 子条目三级标签）、与任务看板同一套卡片与弹窗 |
| `task-detail.html` | 任务详情 | 左栏任务描述（可折叠）+ 任务属性 / 任务动态 / 创建者卡，右栏 AI 会话（含全屏、折叠、左右栏拖动互换、栏宽记忆），编辑任务弹窗复用看板创建弹窗 |
| `conversation.html` | 会话详情 | 「对话 / 轨迹」双页签（切换带**滑块滑动动效**）、工具调用层级树（可逐级开合）、消息折叠、右键菜单（12 项）、标题栏右侧**全屏**与**文件预览侧栏**（文件树 + 代码预览 + 可拖分栏条）两枚按钮；顶栏毛玻璃、骨架屏、暗色全量适配；右栏**多页签浏览器**（摘要 / 终端 / 浏览器 / 预览四模块 + 批注锚点），**一个文件一枚独立页签** |

## 打开方式

### 方式一：直接打开（推荐）

用浏览器（Chrome / Edge / Safari）直接打开任意 HTML 文件：

- macOS：`open pages/base.html`
- 或在 Finder 中双击 HTML 文件

### 方式二：本地服务器（可选）

如果需要模拟完整路由跳转：

```bash
cd pages
python3 -m http.server 8080
# 浏览器打开 http://localhost:8080/base.html
```

## 页面间跳转

页面之间通过导航链接互相跳转：
- **Header Tab**：基础工作台 ↔ 研发工作台（带 pill 滑动动效）
- **左侧菜单**：数字分身 / 自动化 / 技能 Skills / 设置
- **任务看板 / 需求看板 → 任务详情**：点卡片进入 `task-detail.html`；详情页左上角可返回看板
- **左栏会话任务 → 会话详情**：在**任意页面**点击左栏的会话条目都会跳到 `conversation.html`
  （分组标题与「新会话」按钮不参与跳转）
- **设置页**：左上角"返回基础工作台"链接

所有跳转在各 HTML 文件之间进行，无需服务器支持。
⚠️ 外壳顶栏的页签导航只有在 `file:` 协议下才会真正跳页（`http://` 下只改 hash 且外壳无监听），
故本机预览请用「方式一：直接打开」。

## 设计还原规范

- **设计稿来源**：MasterGo（layer_id 逐个拉取 DSL + extractSvg）
- **样式代码**：严格使用 MasterGo DevMode 提供的现成 CSS，不自我发挥
- **SVG 图标**：path data 由 extractSvg 原样内联，禁止手绘近似
- **坐标定位**：`position: absolute` + `left/top`，按设计稿像素级还原
- **设计系统**：唯一依赖 GienCoder Design System（giencoder），不引入外部 CSS 框架
- **边框补偿**：容器有 `border` + `box-sizing: border-box` 时，子元素 `left/top` 减去 border 宽度补偿偏移
- **禁止硬编码色值**：一律走 `colors_and_type.css` 的 token；设计稿里的非 token 色必须收敛成
  页面 `:root` 的适配层变量并注明出处

## 交付约定（组件复用与视图适配层）

页面是外部 Vite（`viteSingleFile`）产物，**只能在产物上打补丁**。补丁必须遵守：

1. **组件复用**：表格 / 分页 / 选择器 / 日期 / 按钮 / 标签等一律使用
   `giencoder-design-system/components/{slug}.json` 的 `anatomy` 契约类，
   **禁止自建同义类名结构**；契约里的 `element` 字段是硬约束。
2. **只允许一层「视图适配层」**：前缀 `rq-` / `kb-` / `td-` / `av-`，作用在组件类**之上**，
   **不得改写组件本体**。适配层里禁止裸 `.giencoder-*` 选择器、禁止 `!important`。
3. **改 DS 必须同时改页面内联的压缩版 CSS**：页面内联的是压过的 `components.css`
   （属性顺序与源文件不同），只改源文件页面不会变化（参考 `mg-work/r36/apply36.py`）。
4. **弹层分工**：静态结构 → `components.css`；全屏定位 + 开合动效 → `gienx-templates/ui-controls.css`。
   开合的唯一开关是 `.giencoder-popup-open`，**不要用内联 `style.display`**。
5. **幂等注入**：补丁用成对注释标记 `<!-- X --> … <!-- /X -->` 包裹，结束标记必须包住 `<script>`；
   幂等自检 = 对结果再替换一次，断言逐字节不变。

改完产物必跑两个自检：

```bash
python mg-work/kanban/r13/check-syntax.py pages/<page>.html   # 按 <script> 配对切块 → ALL_OK
python mg-work/r30/check-classes.py    pages/<page>.html      # 类名 × 契约 anatomy 差集 → ALL_OK
```

## 项目铁律（standing rules · 最高优先级）

> 跨轮永久有效。任何一轮开工前先读一遍；与「本轮需求」冲突时**以铁律为准**并当场确认。

1. **只动该动的地方** —— 绝对不得改动其他不必涉及的模块；确保整体产品稳定性不被破坏；仅落地静态交互。
2. **色值一律走 DS 变量** —— 除特别声明外，全局界面色值一律使用 giencoder 设计系统已有的色彩变量，**不得写死绝对色值**（前提：不影响已正确的浅色模式）。
3. **浅 / 暗色必须彻底适配** —— 所有页面所有 UI 元素浅暗都要到位，**不得出现浅暗混杂**。
4. **聚焦任务主线，不过度发散** —— 只做本轮明确要求的那几件事；不顺手改别的、不主动扩展范围。动手前问自己一句：「这一步是本轮需求要求的吗？」

> 完整规则集（P3.1 → P3.65 共 60+ 条踩坑红线）见 `.workbuddy/memory/PLAYBOOK.md`。

## 技术栈（源工程）

> 注意：本仓库仅包含**构建产物**和设计系统规范，React/Vite 源工程不在本仓库中。
> `build.sh` 需指定外部源工程目录才能重新构建。

- React 18 + TypeScript
- Vite 8（构建工具，`viteSingleFile` 内联输出）
- Tailwind CSS 3（样式框架，已清理所有 Tailwind 原生文件，仅保留构建产物）
- GienCoder Design System（自研设计令牌 + 组件样式）

## 目录结构

```
giencoder-design-engineering/
├── pages/                          ← 交付页面（10 个独立 HTML）
│   ├── base.html / dev.html / avatar.html
│   ├── automation.html / skills.html / settings.html
│   └── kanban.html / req-kanban.html / task-detail.html / conversation.html
├── giencoder-design-system/       ← 设计系统规范
│   ├── components/                 ← 组件 JSON 契约（anatomy 是唯一真值）
│   ├── preview/                    ← 组件预览页
│   ├── gienx-templates/            ← 外壳模板与弹层动效（ui-controls.css 等）
│   ├── components.css              ← 组件样式（源文件；页面内联的是压缩版）
│   ├── colors_and_type.css         ← 色彩与字体样式（Token 唯一权威来源）
│   ├── tokens.md                   ← 设计令牌文档
│   └── ...
├── assets/                         ← 图标资源（icons/）
├── docs/                           ← 设计文档（GienCoder-DESIGN.md、Playbook 等）
├── mg-work/                        ← 分轮工作记录
│   ├── r32 … r105/                 ← 每轮：生成/补丁脚本、实测脚本、截图、探针
│   │   └── rNN/applyNN.py          ← 幂等注入补丁（改页面一律走这里，不手改产物）
│   ├── r109/                       ← 现役代（10 页主题/token/交互）
│   │   ├── part109/                ← 权威源片段（panel.js / panel.css / _mods.html）
│   │   ├── raw/                    ← 真机取证（每拍一个子目录：截图 + JSON 读数）
│   │   └── ev/theme/               ← r109 全部补丁层 + 探针（链序见上）
│   ├── check-syntax.py             ← 产物语法自检（10/10）
│   └── r30/check-classes.py        ← 组件类名合规自检
├── verify-design.py                ← 构建后质量验证脚本（74 问题 / 0 critical）
├── build.sh                        ← 构建脚本（需外部源工程）
└── README.md                       ← 本文件
```

## 工作方式

页面改动一律**改生成/补丁脚本 → 重跑脚本 → 跑自检 → 实测截图**，不手改产物：

| 页面 | 生成 / 补丁脚本 |
|------|----------|
| `task-detail.html` | `mg-work/r21/build-detail.py` |
| `kanban.html` / `req-kanban.html` | `mg-work/req-kanban/build-table.py` → `build-inject.py` |
| `avatar.html` 主内容 | `mg-work/r35/build-avatar-main.py` |
| `avatar.html` AI 对话栏 | `mg-work/r34/build-avatar.py` |
| 外壳顶栏页签修复（全站） | `mg-work/r25/apply-shell-tabs.py` |
| 全局字号机制 / 设置页 | `mg-work/r88/apply88.py` · `apply88b-fontsize.py` |
| `conversation.html` 会话详情 + 全站会话跳转 | `mg-work/r102/apply102.py`（r93 起的会话详情改动都在此脚本内就地返工） |
| **r109 全代（10 页 · 主题 / token / 交互）** | `mg-work/r109/ev/theme/` —— 见下方「r109 链序」 |

> **体位要点**：补丁是「先 `strip_all(当前页)` 取净底 → 再注入」⇒ **改完直接重跑即自愈**，
> 不必先回滚；跑两遍 sha 不变即幂等。回滚用 `cp mg-work/rNN/before/<page>.html pages/<page>.html`。

### r109 链序（14 层，**顺序不可乱、不可中途停**）

```bash
cd mg-work/r109/ev/theme
python make109.py && python splice109.py && python apply109.py   # 整页重建（净底）
python apply-theme.py   && python apply-dark.py                  # 主题机制 + 暗色适配
python apply-tokens.py  && python apply-literals.py              # DS token 化
python apply-popup.py   && python apply-border.py
python apply-zcode.py   && python apply-menuwhite.py && python apply-dots.py
python make12.py && python apply12.py                            # 第 13 层
python apply14.py                                                # 第 14 层（批注模块 + 独立页签）
```

> ⚠ **`apply109.py` 是「整页重建」性质** ⇒ 它之后的每一层注入都可能被它冲掉。
> **改完必须把整链跑到尾**；中途停 = 页面处于损坏态（实测：批注模块曾因此整段退回旧版）。
> 整链稳定性用「**连跑两轮比 md5**」验证，判据必须**规范化换行**再比（`autocrlf` 会让逐字节比对永远为假）。

改完产物必跑两个自检：

```bash
python mg-work/check-syntax.py pages/*.html   # 按 <script> 配对切块 → 期望 10/10 通过
python verify-design.py ./pages               # Token / 类名合规 → 期望 74 问题 / 0 critical
```

实测统一走 `agent-browser`（1440×900，另跑 2560 与暗色档），脚本与落地截图都放 `mg-work/rNN/`。

## 版本

- **交付日期**：2026-09-24
- **最近更新**：2026-10-02 —— **r109 全代（10 页）**
  - **全局字号机制**（`--ui-fs` 杠杆）+ **设置页重做**
  - **全站浅 / 暗色彻底适配**：DS 13 族 × 10 级阶梯镜像（暗色 = 浅色逐级镜像 `N ↔ 11−N`）+ 90 枚语义 token；硬编码色值统一收敛到 DS 变量
  - **全站下拉菜单统一**：浅色档纯白、暗色档 `rgba(31,31,31,0.88)`，一律以基础工作台「默认权限」为基准
  - **`conversation.html` 右栏多页签浏览器**：摘要 / 终端 / 浏览器 / 预览四模块，**批注锚点**（点「标注」→ 逐元素批注 → Ctrl 提交、锚点常驻可拖动）
  - **卡片即入口**：用户上传的本地文件卡（`.r93-att`）、任务产物卡（`.r93-artcard`）、任务产物卡组（`r93-artgrid`）点击即开右栏预览；**一个文件一枚独立页签**，切换不互相覆盖
  - 会话详情页此前各轮：对话/轨迹双页签滑块动效、工具调用层级树、全屏 + 文件预览侧栏、顶栏毛玻璃、骨架屏
- **构建工具**：Vite 8 + viteSingleFile
- **设计稿**：MasterGo file=193158744355579

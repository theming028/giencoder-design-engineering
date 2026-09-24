---
name: "yuanqi-design-router"
description: >-
  GienCoder 设计系统 (Yuanqi Design System) 的 AI 协作入口。设计师和前端开发者在 yuanqi 项目中使用 AI 时触发，
  按角色路由到对应工作流：设计师模式（选型/Token/规范审查/原型）、前端模式（实现/契约/迁移/验证）。
  触发词：源启、yuanqi、设计系统、按 yuanqi 实现、设计 token、规范审查、AI 写组件、契约同步
---

# yuanqi-design-router · AI 协作入口

> 项目根：`YuanqiDesignSystem/` ｜ 规范层：`yuanqi/`（71 组件契约 + 72 preview 模板）
> 设计系统版本：源启 Design React 2.66.16 ｜ Token 体系：yuanqi tokens（详见 `yuanqi/tokens.md`）

---

## 🏗️ 架构（先理解两层 skill）

```
┌─ 规范层（跨 IDE 共用）───────────────────────┐
│  yuanqi/SKILL.md                             │
│  ↳ install.sh 建立 symlink 到：              │
│     ~/.claude/skills/yuanqi-design-spec      │
│     ~/.codex/skills/yuanqi-design-spec       │
│     ~/.cursor/rules/yuanqi-design-spec       │
│     ~/.config/zed/skills/yuanqi-design-spec  │
│  改 yuanqi/SKILL.md = 所有 IDE 立即生效      │
└──────────────────────────────────────────────┘
                    ▲ 引用
┌─ 路由层（WorkBuddy 专用）────────────────────┐
│  .workbuddy/skills/yuanqi-design-router/     │
│  ↳ 本文件：双角色路由 + 入口决策             │
└──────────────────────────────────────────────┘
                    ▲ 外部参考
┌─ 参考层（可选，非 yuanqi）───────────────────┐
│  ~/.workbuddy/skills/semi-design-guide/      │
│  ↳ via semi-mcp（4 个查询工具）              │
└──────────────────────────────────────────────┘
```

**关键规则**：
- 改**规范** → 改 `yuanqi/`（symlink 自动生效所有 IDE），再 `rsync` 到 `yuanqi-delivery/`
- 改**路由** → 改本文件（仅 WorkBuddy 生效）
- **不要**把 Semi 的 API 写进 yuanqi 规范

---

## 🚨 路由铁律

1. **角色判定先于一切**：用户意图是「设计」还是「实现」？先分流，不要混合输出。
2. **yuanqi 优先于一切**：任何组件/Token/规范问题，先查 yuanqi 内部契约，禁止凭记忆臆造。
3. **yuanqi 是唯一主体系**：本仓库 UI 一律用 yuanqi token 与 class。CloudAI-UI（`.agents/skills/CloudAI-UI/`）
   是**备选风格语境**，仅当用户明确要「CloudAI / Harness / 字节 Cloud 风格」页面时使用，且走它自己的独立
   CloudAI 工程（`node .agents/skills/CloudAI-UI/setup/create-app.mjs` 新建）。**禁止**在两套间互相换色值、
   或在同一页面混排两套 token；互借仅限走查判断规则。见仓库根 `DESIGN-CONTEXT-ROUTING.md`。
4. **Semi 是对照源，不是替代品**：仅在 yuanqi 未覆盖或需字节系对照时调 `semi-design-guide`；产出物必须用 yuanqi class 与 Token。
5. **preview 是代码模板，不是参考图**：`preview/component-{slug}.html` 可直接复制（详见 `preview-format.md`），不要只看不抄。
6. **契约驱动**：改实现必须改契约，改契约必须双目录同步。

---

## 🧭 主路由判定

| 用户意图关键词 | 模式 |
|----------------|------|
| 「设计」「规范」「选型」「审查」「原型」「视觉」「交互」「页面」「PRD」 | → 🎨 **设计师模式** |
| 「实现」「写代码」「vue」「组件」「props」「事件」「绑定」「契约」「迁移」「验证」 | → 💻 **前端模式** |
| 模糊 / 不明确 / 跨角色 | → 🤝 **兜底引导** |

---

## 🗺️ 子场景路由（细分动作 → 关键资产）

| 子场景 | 触发关键词 | 归属 | 关键动作与资产 |
|--------|-----------|------|----------------|
| **组件选型** | 选哪个组件 / 用什么组件 | 🎨 | `component-registry.json`（71 组件，covered 28 → mapped 4 → new 39 优先级） |
| **页面组装** | 页面 / PRD / 布局 / 模式 | 🎨 | `patterns.md` 六大模式（骨架/列表/详情/表单/看板/配置）+ `ui_kits/{type}/` |
| **规范审查** | 审查 / 合规 / 违规 / 对比度 | 🎨 | 三对照：`components/{slug}.json` + `tokens.md` + `a11y.md §7` → 输出 P0/P1/P2 |
| **组件实现** | 实现 / 写组件 / 加 props | 💻 | `components/{slug}.json` + `preview/component-{slug}.html` + `components.css` |
| **契约维护** | 契约 / schema / 补字段 / props 索引 | 💻 | `schema-contract.md`（v3 规范）+ `scripts/sync-props.py`（自动同步） |
| **组件迁移** | 迁移 / 转码 / 像素级还原 / Ardot / MasterGo / 设计稿 | 💻 | Token 映射表 + 组件替换（原型 class 保留 + 追加 yuanqi class） |
| **Token 维护** | token / 色阶 / 颜色变量 / 改色 / 字号 / 间距 | 🎨💻 | `tokens.md` + `colors_and_type.css` + `tokens-visual.html` + 双目录同步 |
| **Preview 模板** | 模板 / preview / 代码模板 / 交互动效 | 💻 | `preview-format.md`（含零依赖 JS 脚本规范 5.2 + 动效规范 5.4） |
| **本地验证** | 验证 / 截图 / serve.py / puppeteer | 💻 | `serve.py`(8866) + agent-browser/puppeteer-core 截图 |
| **页面 DSL** | DSL / yq build / 页面描述 / 编译页面 / AI 生成页面 | 💻 | `yuanqi/dsl/schema.json` + `yuanqi/scripts/yq-build.py` + `yuanqi/dsl/examples/` |
| **双目录同步** | 同步 / delivery / 快照 | 💻 | `rsync -a yuanqi/ yuanqi-delivery/` + diff 校验（见「已知坑」） |
| **外部对照** | 半选 / 字节系 / Semi / 对照 | 🎨💻 | `semi-design-guide` via `semi-mcp` |

---

## 🎨 设计师模式

**读取路径**：

```
yuanqi/SKILL.md                    ← 总体硬规则（5 条）
  ├ component-registry.json        ← 71 组件清单 + 分类 + covered/mapped/new
  ├ components/{slug}.json         ← 单组件契约（variants/sizes/states/anatomy/a11y）
  ├ tokens.md                      ← Token 全量值表
  ├ patterns.md                    ← 六大页面模式 + 组合禁止项 §9
  ├ a11y.md                        ← 无障碍规范（§7 检测清单）
  ├ ui_kits/{type}/index.html      ← 6 类页面样板
  └ preview/component-{slug}.html  ← 72 个代码模板（可直接复制）
```

**工作流**：

1. 理解需求 → 拆解页面区块与交互状态（空/错/载/权限/弹窗/展开收起）
2. 按 `component-registry.json` 选组件（**status 优先级：covered → mapped → new**）
3. 每个组件读 `components/{slug}.json` → 确认 variants/sizes/states/anatomy
4. 视觉 Token 全部走 `var(--color-*)` / `var(--spacing-N)` / `var(--border-radius-*)`
5. 页面模式按 `patterns.md` 六大类；参考 `ui_kits/{type}/index.html`
6. **外部参考**（可选）：需字节系对照 → 调 `semi-design-guide` MCP `get_semi_document`
7. **产出**：组件选型清单 + Token 引用 + 原型 HTML（serve.py 验证）+ 设计说明

**禁止**：
- ❌ 不引入外部 CSS 框架 / Lucide / Heroicons / FontAwesome / CDN 框架 / 自造 SVG
- ❌ 硬编码 hex（除 SVG fill 外）
- ❌ 杜撰 yuanqi 不存在的变体
- ❌ 输出代码（前端模式的事）

详细 SOP：`yuanqi/docs/ai-for-designers.md`

---

## 💻 前端模式

**读取路径**：

```
yuanqi/SKILL.md                    ← 总体硬规则（5 条）
  ├ component-registry.json        ← 组件 slug 映射
  ├ components/{slug}.json         ← 契约（propsIndex/anatomy/states/interaction）
  ├ schema-contract.md             ← 契约 v3 schema 规范
  ├ preview-format.md              ← preview 模板 + JS 脚本规范 + 动效规范
  ├ components.css                 ← 组件 CSS（组件段有 @component-css-start 标记）
  ├ preview/component-{slug}.html  ← 72 个可复制模板
  ├ scripts/sync-props.py          ← props 自动同步工具
  └ yuanqi-delivery/               ← 快照（rsync 同步）
```

**工作流**：

1. 需求拆解 → 组件清单
2. 每个组件读 `components/{slug}.json` → 提取 propsIndex + anatomy + states
3. 从 `preview/component-{slug}.html` **原样复制**结构（72 个模板基本覆盖全部组件），仅改文字与数据
4. 颜色/间距/圆角/阴影/动效 全走 Token
5. 交互组件按 `preview-format.md §5.2` 加零依赖原生 JS（IIFE 包裹、空指针防护、不抛异常）
6. 动效按 `preview-format.md §5.4`（**禁止 display 硬切换**，0.2s standard）
7. **契约同步**：props 用 `python3 yuanqi/scripts/sync-props.py <package_dir>` 自动同步
8. **双目录同步**：`rsync -a yuanqi/ yuanqi-delivery/`（注意已知坑）
9. **验证**：serve.py(8866) + agent-browser/puppeteer-core 截图 + JSON schema 校验

### DSL 页面生成子模式

当用户意图是「用 DSL 生成页面」或「把设计稿/需求转成可编译页面描述」时：

**工作流**：

1. 确定页面模式（`patterns.md` 六大类，P0 优先 `list-page`）
2. 手写或让 LLM 生成 `yuanqi/dsl/examples/<name>.yq.yaml`（schema：`yuanqi/dsl/schema.json`）
3. 运行编译：`python3 yuanqi/scripts/yq-build.py yuanqi/dsl/examples/<name>.yq.yaml`
4. 校验失败时以 `--json` 输出错误，回喂 LLM 修正；结构错误在编译期拦截
5. 产物为 `yuanqi/dsl/output/<name>.html`，用 serve.py(8866) + puppeteer 截图与金标 `ui_kits/{pattern}/index.html` 像素级对比
6. 同步到 `yuanqi-delivery/`、提交、推送

**约束**：
- DSL 只描述结构 + 组件引用 + props + 数据，**不描述样式**（样式全部走 token/契约）
- `c:` 值必须是 `component-registry.json` 内的 slug 或 DSL 页面级组件（top-nav/sidenav-menu/filter-bar/filter-item）
- P0 实现 emitter 白名单，超出白名单的组件会在校验期报错

**禁止**：
- ❌ 在 DSL 里写内联 style / 硬编码 hex
- ❌ 在 DSL 里杜撰 registry 不存在的组件或 props
- ❌ 不引入外部 CSS 框架 / Lucide / CDN / jQuery
- ❌ 硬编码 hex
- ❌ 跳过契约更新 / 跳过双目录同步 / 跳过验证
- ❌ 把 Semi 的 API / 事件名直接搬到 yuanqi
- ❌ display 硬切换（动效必须走 transition）

详细 SOP：`yuanqi/docs/ai-for-developers.md`

---

## 🔗 外部参考：semi-design-guide

### 何时调用

| 场景 | 调用 |
|------|------|
| yuanqi 文档/契约缺失或不清晰 | ❌ 先补 yuanqi 契约，不要查 Semi |
| 用户明确要"对照半选"或"字节系设计语言" | ✅ `get_semi_document` |
| 复杂组件（Table / Form / Tree / Cascader）实现模式参考 | ✅ `get_file_code` / `get_function_code` |
| 主题定制 / Design Token 最佳实践 | ✅ `get_semi_document componentName="customize-theme"` |
| React 19 兼容性参考 | ✅ `get_semi_document componentName="react19"` |

### 如何调用

`semi-design-guide` 已装到 `~/.workbuddy/skills/semi-design-guide/`，配合 `semi-mcp`（已在 `~/.workbuddy/mcp.json` 配置，需连接器管理页 Trust）。

```json
{ "name": "get_semi_document", "arguments": { "componentName": "Table" } }
{ "name": "get_component_file_list", "arguments": { "componentName": "Form" } }
{ "name": "get_file_code", "arguments": { "filePath": "@douyinfe/semi-ui/table/Table.tsx" } }
{ "name": "get_function_code", "arguments": { "filePath": "...", "functionName": "render" } }
```

### 约束

- **参考 ≠ 复制**：Semi 的 API/事件名不能直接搬到 yuanqi。参考的是「设计意图」和「交互模式」。
- **最终代码用 yuanqi class**：`<button class="yuanqi-btn yuanqi-btn-primary">`，不是 `<SemiButton>`。
- **同步回写**：参考 Semi 学到的模式若 yuanqi 缺，补到 `components/{slug}.json` 的 `interaction` 或 `usage`。

---

## 🤝 兜底引导（意图模糊时）

不要猜。按序问**一个问题**：

1. 你要**设计**还是**实现**？（角色分流）
2. 涉及哪个**组件**？（定位契约）
3. 是**新做**还是**改现有**？（决定是否走迁移/契约维护）

如果用户说"随便看看"→ 直接给 `component-registry.json` 的 71 组件分类概览 + `ui_kits/` 6 类页面清单，让他挑。

---

## 📂 引用清单（按需加载）

| 需求 | 读取 |
|------|------|
| 总体规范 | `yuanqi/SKILL.md` |
| 项目全貌 / 目录结构 | `yuanqi/README.md` |
| 组件清单（71） | `yuanqi/component-registry.json` |
| 范围冻结报告（缺口 + 命名映射） | `yuanqi/PHASE0-范围冻结.md` |
| 单组件契约 | `yuanqi/components/{slug}.json` |
| 编写新契约 | `yuanqi/schema-contract.md` |
| Token 值 | `yuanqi/tokens.md` |
| 颜色/字号 CSS | `yuanqi/colors_and_type.css` |
| Token 可视化 | `yuanqi/tokens-visual.html` |
| 组件 CSS | `yuanqi/components.css` |
| 页面模式（六大类） | `yuanqi/patterns.md` |
| 无障碍 | `yuanqi/a11y.md` |
| **Preview 模板规范** | `yuanqi/preview-format.md`（含 JS 脚本 + 动效规范） |
| 可复制模板（72 个） | `yuanqi/preview/component-{slug}.html` |
| 页面样板（6 类） | `yuanqi/ui_kits/{config-page,detail-page,form-page,dashboard,list-page,result-page}/index.html` |
| **props 自动同步工具** | `yuanqi/scripts/sync-props.py` |
| **跨 IDE 安装器** | `yuanqi/install.sh`（symlink 到 5 个 IDE） |
| 设计师 SOP | `yuanqi/docs/ai-for-designers.md` |
| 前端 SOP | `yuanqi/docs/ai-for-developers.md` |
| 页面 DSL 方案 | `yuanqi/docs/dsl-proposal.md` |
| DSL schema | `yuanqi/dsl/schema.json` |
| DSL 编译器 | `yuanqi/scripts/yq-build.py` |
| DSL 金标示例 | `yuanqi/dsl/examples/resource-list.yq.yaml` |
| 外部参考 | `~/.workbuddy/skills/semi-design-guide/`（via `semi-mcp`） |

---

## ⚠️ 已知坑（来自项目实战）

### 双目录同步（rsync）

```bash
# ✅ 正确：整体同步
rsync -a yuanqi/ yuanqi-delivery/

# ❌ 错误：多源路径会把文件放错位置
rsync -av yuanqi/components.css yuanqi/components/table.json yuanqi-delivery/
# → table.json 会落到 yuanqi-delivery/ 根目录（应为 components/）
# 正确做法：逐文件指定完整目标路径
rsync -a yuanqi/components/table.json yuanqi-delivery/components/table.json

# 验证一致性
diff -r yuanqi/ yuanqi-delivery/ | head
```

**🚫 硬规则：本工程同步一律用 `rsync -a`，禁止加 `--delete`。**
`yuanqi-delivery/` 存在独有目录（如 `giencoder-task-ui.design/`），`--delete` 会将其整体删除
（已两次踩坑，需 `git checkout --` 才能恢复）。只同步被改文件时用：
`rsync -a yuanqi/components.css yuanqi-delivery/components.css`（逐文件指定完整目标路径）。

### 改组件级样式时，先扫内联覆盖

组件 spec（圆角/内边距/颜色）改动后，`preview/` 与 `ui_kits/` 里可能有**内联 style 覆盖**同组件的该属性，
导致"组件级改了但用法没改"的 spec 不一致。改前先扫：

```bash
grep -rn "yuanqi-<slug>" yuanqi/preview/ yuanqi/ui_kits/ | grep -i "<被改属性>"
```

（例：改 Tag 圆角时发现 `component-grid.html` 有 2 处内联 `border-radius`；改 padding 时同 2 处内联已是 8px 无需动。）

### 并行 Edit 竞争

同一文件的多处 Edit **并行执行会竞争回滚**。必须**串行**执行，改完 `grep` 验证。

### 坚果云 git 锁 + push 真伪判定

本仓库根是整个坚果云，客户端会**持续生成**各类锁文件，且不止 `index.lock`
（实测还有 `refs/remotes/origin/main.lock`、`objects/maintenance.lock`）。任何 git 写操作前递归清理：

```python
import os, shutil, tempfile
for root, dirs, files in os.walk('.git'):
    for f in files:
        if f.endswith('.lock'):
            p = os.path.join(root, f)
            try:
                if f'{os.sep}refs{os.sep}' in p:
                    # ⚠️ refs/ 下不能留任何文件——会被 git 当成一个合法 ref 显示
                    shutil.move(p, os.path.join(tempfile.gettempdir(), os.path.basename(p) + '.stale'))
                else:
                    os.rename(p, p + '.stale')   # 重命名而非删除，可回溯
            except Exception: pass
```

> **坑**：早期把 `.git/refs/remotes/origin/main.lock` 重命名为 `main.lock.stale` 留在原目录，
> 结果 `git log` 把它显示成一个远程分支 `origin/main.lock.stale`。refs/ 下的锁必须**移出 .git**。

清理后**立刻**串联执行 git 命令（`python清锁 && git add ... && git commit ...`），减少被重新生成的窗口。

**判定推送是否成功，只看 `git ls-remote origin main` 与本地 `git rev-parse HEAD` 是否一致。**
`git push` 输出 `error: update_ref failed for ref 'refs/remotes/origin/main'` 属本地 remote-tracking
ref 被锁，**不代表推送失败** —— 只要上一行有 `旧sha..新sha  main -> main`，远端即已更新。

---

## 🎯 交付前自检

### 设计师产物
- [ ] 选型组件都在 `component-registry.json`（71 个内）
- [ ] Token 全部 `var(--*)`，无硬编码 hex
- [ ] 弹层组件注明 focus trap / Esc / 遮罩
- [ ] 每个交互状态有视觉说明
- [ ] 原型 HTML 用 serve.py(8866) 可渲染

### 前端产物
- [ ] `components/{slug}.json` 契约已同步（props 走 `sync-props.py`）
- [ ] `rsync -a yuanqi/ yuanqi-delivery/` 已执行 + `diff` 校验通过
- [ ] 交互组件有零依赖 JS（`preview-format.md §5.2`）
- [ ] 动效无 display 硬切换（`§5.4`）
- [ ] 无外部 CSS 框架 / Lucide / CDN
- [ ] serve.py 验证 + agent-browser 截图通过

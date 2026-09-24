# GienCoder 设计系统 · 设计师 AI 协作手册

> 本手册面向设计师。当你在 giencoder 设计任务中需要 AI 协助时，按本手册触发和引导 AI。
> 入口 skill：`giencoder-design-router`（项目根 `.workbuddy/skills/`）

---

## 一、什么时候召唤 AI

| 场景 | 召唤方式 | 适合的 AI 任务 |
|------|----------|----------------|
| 新页面选型 | "我要做一个 [场景] 页面设计" | 推荐组件组合 + Token 引用 |
| 视觉规范审查 | "审查这份 HTML 是否符合 giencoder 规范" | 输出违规清单 P0/P1/P2 |
| 组件选型咨询 | "[场景] 该用哪个组件？" | 读契约返回变体/状态/适用场景 |
| 原型生成 | "按 giencoder 规范生成 [页面] 高保真原型" | 输出 HTML + Token 变量清单 |
| 对照字节系设计 | "对比 giencoder 和半选的 [模式]" | 调用 semi-design-guide MCP |

---

## 二、AI 协作流程（标准 5 步）

### Step 1：清晰描述需求

把场景说具体，避免"我想做个好看的页面"：

```
✅ 好的需求：
"我要做一个 [审批列表页]，需要：
- 顶部筛选区（按状态/时间）
- 中部列表（带标签 + 操作列）
- 空状态/加载状态/错误状态都要
- 桌面端 1440 宽"

❌ 模糊需求：
"做个审批页面"
```

### Step 2：等 AI 输出选型清单

AI 应返回：

```markdown
## 组件选型
| 区块 | 组件 slug | 变体 | 说明 |
|------|-----------|------|------|
| 顶部筛选 | input, select, button | outline + medium | 按需 |
| 列表 | table | bordered + hover | 49 行示例 |
| 标签 | tag | success/warning/danger | 状态色 |
| 空状态 | empty | image + primary | 标准空态 |

## Token 引用
- 主色：var(--color-primary-6) #3770F7
- 间距：var(--spacing-12) 12px
- 圆角：var(--border-radius-medium) 4px

## 页面模式
按 patterns.md §3 列表类组合：FilterBar + Table + Pagination
```

### Step 3：审查选型（如有疑义）

如果 AI 推荐了你不熟的组件：

```
"列出 tag 组件的全部 variants 和 states"
```

AI 应读 `giencoder/components/tag.json` 返回。

### Step 4：生成原型

```
"按上面选型生成高保真原型 HTML，用 giencoder class + Token，输出到 outputs/"
```

AI 会：
1. 从 `giencoder/preview/component-{slug}.html` **原样复制**结构（72 个模板基本覆盖全部组件）
2. 参考 `giencoder/gienx-templates/{type}/index.html` 页面样板（6 类）
3. 写自包含 HTML 到 `outputs/`
4. 启动 serve.py(8866) 让你预览

> **认知要点**：`preview/` 里的 HTML 是**代码模板**（可直接复制的源码），不是参考截图。
> AI 应当**原样复制**组件结构，只改文字与数据，不要重新发明 HTML。
> 格式规范见 `giencoder/preview-format.md`。

### Step 5：规范审查（交付前必做）

```
"审查 outputs/{file}.html 是否符合 giencoder 规范，输出违规清单"
```

AI 应读 HTML → 对照 `component-registry.json` + `tokens.md` + `a11y.md §7` → 输出 P0/P1/P2 分级问题。

**推荐进阶：六维度放行评估**（用于方向探索或交付验收）：
```
"对 outputs/{file}.html 运行六维度评估：
 判定页面类型（对照 patterns），六维度评分（引用 contract/tokens/a11y 依据），
 检查阻断问题（EVALUATOR §5.2），输出放行结论 + 优化指令"
```
详见 `giencoder/EVALUATOR.md`。评审只看交付物不看生成器意图。

---

## 三、典型场景示例

### 场景 A：从 PRD 到选型清单

```
你：「这是 PRD（贴出）」  
AI：[读 PRD，拆解区块]  
AI：[读 component-registry.json 选组件]  
AI：[输出选型表 + Token 引用清单]  
你：审查 + 调整
```

### 场景 B：审查现有原型

```
你：「审查 outputs/xxx.html 是否符合 giencoder 规范」  
AI：[读 HTML]  
AI：[对照契约 + Token + a11y 输出违规清单]  
   - P0: Modal 缺 focus trap
   - P1: 颜色硬编码 #0052D9，未走 var(--color-primary-*)
   - P2: 按钮组超过 3 个未用 Space 组件
你：修复 + 让 AI 复审
```

### 场景 C：对照半选设计模式

```
你：「giencoder 的 Table 和半选的 Table 在筛选交互上有什么区别？」  
AI：[读 giencoder/components/table.json]  
AI：[调 semi-mcp get_semi_document componentName="Table"]  
AI：[对比设计意图差异，输出要点]
```

---

## 四、设计 Token 速查（必备）

| 类别 | 关键 Token | 值 |
|------|-----------|-----|
| 主色 | `--color-primary-6` | #3770F7（弧蓝） |
| 成功 | `--color-success-6` | #3BB346 |
| 警告 | `--color-warning-6` | #FF7D00 |
| 危险 | `--color-danger-6` | #F53F3F |
| 文字 | `--color-text-1..4` | 标题→禁用 |
| 背景 | `--color-bg-1..5` | 页面→浮层 |
| 边框 | `--color-border-1..4` | 分割→强调 |
| 间距 | `--spacing-1..22` | 2px 步进 |
| 圆角 | `--border-radius-small/medium/large` | 2/4/8px |
| 阴影 | `--shadow1/2/3-down` | 轻/中/重 |

完整 Token 表见 `giencoder/tokens.md`；可视化色板见 `giencoder/tokens-visual.html`。

---

## 四点五、页面样板与代码模板（重要）

### 6 类页面样板（`giencoder/gienx-templates/`）

| 页面类型 | 路径 | 适用场景 |
|----------|------|---------|
| 列表页 | `gienx-templates/list-page/index.html` | 数据列表 + 筛选 + 分页 |
| 详情页 | `gienx-templates/detail-page/index.html` | 单条记录详情 + 操作区 |
| 表单页 | `gienx-templates/form-page/index.html` | 新建/编辑表单 |
| 看板 | `gienx-templates/dashboard/index.html` | 数据概览 + 统计卡 |
| 配置页 | `gienx-templates/config-page/index.html` | 系统设置分组 |
| 结果页 | `gienx-templates/result-page/index.html` | 成功/失败/异常反馈 |

### 72 个组件代码模板（`giencoder/preview/`）

`preview/component-{slug}.html` 是**可直接复制的代码模板**，不是参考图。72 个文件基本覆盖全部 71 组件。

**AI 使用规则**（见 `preview-format.md`）：
- **原样复制**组件 HTML 结构，只改文字与数据
- class 遵循 `giencoder-{component}-{part}-{modifier}` 体系
- 状态用 class 表达（`-selected` / `-disabled` / `-loading`）
- 交互组件自带零依赖原生 JS（可直接演示点击）
- 动效走 CSS transition，禁止 display 硬切换

**审查原型时重点看**：
1. 组件 HTML 是否来自 preview 模板（而非 AI 自造）
2. class 是否为 giencoder 体系
3. 状态是否用 class 表达
4. 动效是否有过渡（不是硬切换）

---

## 五、禁止做的事（AI 触犯时立即反驳）

1. ❌ 输出外部 CSS 框架 class（`bg-blue-500` 这种）
2. ❌ 引入 Lucide / Heroicons / FontAwesome 图标
3. ❌ 硬编码 hex（`color: #3770F7` 必须改成 `color: var(--color-primary-6)`）
4. ❌ 杜撰 giencoder 不存在的变体（如 Button 的 capsule shape、Tabs 的 vertical-line）
5. ❌ 输出代码（前端模式的事）
6. ❌ 重新发明组件 HTML（应从 `preview/component-{slug}.html` 原样复制）

---

## 六、协作节奏建议

- **先生成选型清单**（30 秒可完成）→ 你审查 → 再生成原型（避免一上来写大段 HTML 跑偏）
- **每次小步迭代**：原型出 80% → 你指出 1-2 个细节调整 → AI 修
- **每个交付必走规范审查**：哪怕只改一个色值

---

## 七、问题反馈

发现 giencoder 契约/Token 缺失或不准确时，告诉 AI：
```
"giencoder/components/{slug}.json 缺 [字段]，请按 schema-contract.md 补全"
```

AI 会更新契约，并做**双目录同步**：
`giencoder/`（权威源）改完 → `rsync -a giencoder/ giencoder-delivery/` 同步到快照 → `diff -r` 校验一致。

> 注：`giencoder/` 通过 `install.sh` 的符号链接同步到 5 个 IDE 环境，改一次即全局生效。

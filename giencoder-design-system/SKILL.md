---
name: "GienCoder 设计系统 (GienCoder Design System)"
description: >-
  基于 源启 Design React 2.66 的完整 UI/UX 设计规范系统：71 个组件契约 + 设计 Token + 页面模式 + 无障碍规范。
  当用户要求生成 源启风格页面、按 源启规范实现组件、审查页面是否符合 源启规范、或咨询 源启组件用法时使用。
  触发词：源启、源启设计规范、按 源启生成页面、giencoder 组件
---

# GienCoder 设计系统 (GienCoder Design System)

> 权威源目录：`giencoder/`（本 skill 目录）｜ 源启 React 版本：2.66.16
> 硬规则：本规范是唯一权威。生成任何 UI 时，先查契约与 Token，禁止凭记忆臆造 源启不存在的变体/状态/class。

---

## 🚨 硬规则（最高优先级，不可覆盖）

1. **组件以契约为准**：任何组件先读 `giencoder/components/{slug}.json`（或 `giencoder/component-registry.json` 查 slug），获取变体/状态/交互/anatomy 后再实现
2. **Token 禁硬编码**：颜色一律 `var(--color-*)` / `var(--{palette}-{level})`；间距/圆角/阴影/动效用 Token（见 `giencoder/tokens.md`）
3. **禁止替换类库**：不引入外部 CSS 框架、不用 Lucide/Heroicons/FontAwesome、不用 CDN 框架、不自造 SVG 路径
4. **弹层三要素**：Modal/Drawer/Select/Dropdown 等弹层必须实现 focus trap + Esc 关闭 + 遮罩点击关闭（见 `giencoder/a11y.md` §4）
5. **页面模式**：页面结构按 `giencoder/patterns.md` 六大模式（骨架/列表/详情/表单/看板/配置）组合，不自由发明布局

---

## 📂 读取顺序（按需取用）

| 需求 | 读取 |
|------|------|
| 查组件清单/分类/映射 | `giencoder/component-registry.json` |
| 单个组件全部规范 | `giencoder/components/{slug}.json` |
| 编写新组件契约 | `giencoder/schema-contract.md` |
| Token 值 | `giencoder/tokens.md` |
| 页面结构模式 | `giencoder/patterns.md` |
| PRD→DSL 转换引导 | `giencoder/docs/prd-to-dsl.md` |
| 无障碍要求 | `giencoder/a11y.md` |
| 评估器（六维度走查/放行判断） | `giencoder/EVALUATOR.md` |
| Preview 模板规范（JS + 动效） | `giencoder/preview-format.md` |
| 可复制代码模板（72 个） | `giencoder/preview/component-{slug}.html` |
| 现有页面样板（6 类） | `giencoder/gienx-templates/{type}/index.html` |
| props 自动同步工具 | `giencoder/scripts/sync-props.py` |
| 设计师 AI 协作手册 | `giencoder/docs/ai-for-designers.md` |
| 前端 AI 协作手册 | `giencoder/docs/ai-for-developers.md` |
| 外部参考（字节系对照） | `~/.workbuddy/skills/semi-design-guide/` + `semi-mcp`（见下方「外部参考」段） |

---

## 🔗 外部参考：semi-design-guide（可选）

> ⚠️ **Semi 是对照源，不是替代品**。giencoder 优先；只有 giencoder 契约未覆盖或需对照字节系设计语言时，才查 Semi。

| 场景 | 调用 |
|------|------|
| giencoder 契约完整、问题已明确 | ❌ 不查 Semi |
| 复杂组件（Table/Form/Tree/Cascader）实现模式参考 | ✅ `get_file_code` / `get_function_code` |
| 主题定制 / Design Token 最佳实践 | ✅ `get_semi_document componentName="customize-theme"` |
| React 19 兼容性参考 | ✅ `get_semi_document componentName="react19"` |
| 用户明确要"对照半选"或"字节系设计语言" | ✅ `get_semi_document` |

**最终产出物仍用 giencoder class 与 Token**，不引入 Semi API。参考 Semi 学到的模式若 giencoder 缺，应补到 `components/{slug}.json` 的 `interaction` 或 `usage` 字段。

详细工作流见项目根 `.workbuddy/skills/giencoder-design-router/SKILL.md`。

---

## 🧭 工作流

### 0. PRD → DSL → 编译（推荐路线，生成可交付页面的首选）
> 本路线由编译器保证"组件装配 + Token + 自包含",产出最稳定，压制 AI 味。  
> 转换规则见 `docs/prd-to-dsl.md`；schema 见 `dsl/schema.json`；金标见 `dsl/examples/resource-list.yq.yaml`。

1. 按 `docs/prd-to-dsl.md` 五步：拆页面清单 → 判 pattern → 映射骨架 → 列交互状态 → 产出 YAML
2. 校验：`python3 scripts/yq-build.py --json <page.yq.yaml>`（失败据结构化错误回流重试）
3. 编译：产出 `dsl/output/<name>.html` 自包含文件
4. 编译前查 emitter 白名单：非 P0 emitter 的组件（form/modal/drawer/tabs/statistic 等 57 个暂缺）标出，确认是否用手动拼 HTML 兜底
5. 交付前跑六维度评估（见工作流 3）

### 1. 生成 源启页面（PRD → HTML 直接拼，兜底路线）
> 编译器（工作流 0）未覆盖的模式/组件时用本路线。

1. 精读 PRD，提取页面清单与所有交互状态（空/错/载/权限/弹窗/展开收起）
2. 按 `patterns.md` 匹配页面类型 → 骨架（Layout+Menu）
3. 逐区块实现：读 `components/{slug}.json` 确认变体 → 从 `preview/component-{slug}.html` **原样复制**模板（72 个模板基本覆盖全部组件；无则按契约 anatomy 构建，class 用 `giencoder-*` 体系）
4. 交互组件按 `preview-format.md §5.2` 加零依赖原生 JS；动效按 `§5.4`（禁止 display 硬切换）
4. 状态完备：每个交互状态都有对应实现
5. 自查：`a11y.md` §7 检测清单 + 组合禁止项（`patterns.md` §9）

### 2. 组件咨询
- 读 `components/{slug}.json`，返回：适用变体、状态、交互（键盘/动效）、Token 引用

### 3. 规范审查（事实层 + 放行判断）
- **先跑浏览器事实层 QA**：`python3 scripts/preview-audit.py <page.html> --out _audit` —— 产出 DOM/CSS QA + 联动烟测 + 1440 桌面截图，自动标出阻断项与 P1。此为证据链事实层（`EVALUATOR.md §4`），不可省。
- 再读目标 HTML → 对照注册表 + 契约 + tokens.md → 输出违规清单（缺 Token/臆造 class/对比度不足/缺焦点管理等），分级 P0/P1/P2
- **放行判断**：参照 `giencoder/EVALUATOR.md` 跑六维度评估——
  1. 判定页面类型（对照 `patterns.md`）
  2. 六维度评分（产品意图/业务可信/信息架构/交互就绪/系统工艺/视觉品牌，引用 contract/tokens/a11y 依据）
  3. 检查阻断问题（`EVALUATOR.md §5.2`，如 `generic_template_output` / `disconnected_controls_or_states` / `broken_key_task_path`）
  4. 输出放行结论（通过/退回）+ 优化指令（证据在哪/先改什么/影响维度）
- 评审只看交付物，不看生成器意图；页面有占位按钮就按占位处理

---

## 🎨 Token 速查（详见 tokens.md）

| 类别 | 示例 | 说明 |
|------|------|------|
| 主色 | `--color-primary-6` = #3770F7 | 弧蓝，主操作色 |
| 功能色 | `--color-success/warning/danger-6` | 绿 #3BB346 / 橙 #FF7D00 / 红 #F53F3F |
| 文字 | `--color-text-1..4` | 标题→禁用四级 |
| 背景 | `--color-bg-1..5` | 页面→浮层五级 |
| 边框 | `--color-border-1..4` | 分割→强调 |
| 填充 | `--color-fill-1..4` | hover/选中底色 |
| 圆角 | `--border-radius-small/medium/large` | 2/4/8px |
| 阴影 | `--shadow1/2/3-down` | 轻/中/重浮起 |
| 间距 | `--spacing-1..22` | 2px 步进 |
| 字号 | `--font-size-title/body/caption` | 正文基准 14px |
| 动效 | `--transition-duration-1..5` + timing | 0.1-0.5s，默认 standard 曲线 |

---

## 🧪 交付前质量门禁

- [ ] 组件 slug 存在于 `component-registry.json`（71 个）
- [ ] 无外部 CSS 框架/Lucide/CDN 框架
- [ ] 颜色全部走 Token，无硬编码 hex（SVG fill 除外）
- [ ] 弹层组件有 focus trap + Esc + 遮罩关闭
- [ ] 每个 PRD 页面与交互状态都有实现
- [ ] 键盘可达（Tab 流转）+ 焦点可见
- [ ] **六维度评估通过**（见 `EVALUATOR.md`）：页面类型判定 + 六维度评分达标 + 无阻断问题
- [ ] **主任务首屏可辨**（非 `generic_template_output`）

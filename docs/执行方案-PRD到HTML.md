# 执行方案 · 从 PRD 到高可用 HTML（GienCoder 生成管线）

> 最终目的：基于融合后的 GienCoder 设计系统，**根据产品经理提供的 PRD 直接生成高可用的 HTML 页面**。
> 本文是这条管线的「作战地图」：现状盘点 → 目标链路 → 缺口清单 → 分步执行 → 验收标准。

---

## 一、现状盘点（我已核实的资产）

> **本次已修复**：`yq-build.py` 编译器原有两个环境阻塞（① Py3.9 f-string 语法 bug ② 缺 `jsonschema` 依赖），均已解决，**已验证可从金标 YAML 编译出 239 行自包含 HTML**。构建方法见文末「附：如何跑通编译器」。

| 环节 | 现有资产 | 状态 |
| :-- | :-- | :-- |
| 设计规范（声明层） | `tokens.md` / `components/{slug}.json`(72) / `patterns.md` / `a11y.md` | ✅ 完整 |
| AI 消费入口（契约层） | `SKILL.md` / `docs/ai-for-designers.md` / `giencoder-design-router` | ✅ 完整 |
| 代码模板 | `preview/`(73) + `gienx-templates/` 6 类样板 | ✅ 完整 |
| 页面编译器 | `dsl/schema.json` + `scripts/yq-build.py` | ✅ 已修复并扩展，**15 → 24 emitters**（补表单/弹窗/指标） |
| 评估回流 | `EVALUATOR.md`（六维度） | 🆕 已建，待接入 |
| **PRD 输入侧** | `docs/prd-to-dsl.md`（引导，新增） | 🆕 已建，接入 SKILL |
| 产物验证 | 无自动化截图/点击证据 | ❌ 缺失 |

---

## 二、目标链路（要跑通的样子）

```
 ┌──────────┐   Step 1    ┌──────────┐   Step 2   ┌──────────┐   Step 3   ┌──────────┐
 │  PRD 文档  │ ─────────► │ DSL YAML │ ─────────► │ yq-build │ ─────────► │  HTML ✓  │
 │ (PM 提供) │   PRD→DSL   │  (schema)│   emitter  │ /compiler│  构建+验证  │ 可交付    │
 └──────────┘  引导规则    └──────────┘   补齐      └──────────┘            └──────────┘
       ▲                                                      │                │
       └──────── EVALUATOR 六维度回流（不达标打回重建）──────────┴──── 截图+DOM 证据 │
```

**关键性质**：这是「受控生成」——页面不是 AI 自由发挥，而是 `schema 约束 + emitter 装配 + 模板同源`。
这条路线天然压制 AI 的"分布收敛/AI 味"，正是 Vibe 方法论第二章倡导的做法。

---

## 三、缺口清单（含方案与优先级）

### 🔴 缺口 1｜DSL emitters 覆盖不足 —— 历史最大瓶颈（已大幅缓解）
- **现状**：`P0_EMITTERS` 从 15 个 → **24 个**。已补齐 P0.1 高频：`checkbox`、`radio`、`switch`、`tabs`、`form`、`form-item`、`modal`、`drawer`、`statistic`（含 compare/status 语义色）。弹窗带开合交互（`openTarget`/`data-close`）。
- **验证**：`dsl/examples/form-detail.yq.yaml` 综合示例（表单+Tab+指标+弹窗+抽屉）编译通过，产物含全部新组件 DOM。示例见 `dsl/examples/form-detail.yq.yaml`。
- **影响**：表单页、详情页、配置页、结果页（弹窗/确认类）、看板（statistic）**现在都能编译**。
- **仍缺**：`chart`（图表）暂无 emitter——P0 用表格+statistic 呈现，P1 再考虑图表库。其余有契约无 emitter 的组件见 `component-registry.json`。
- **做法**：照现有 `emit_*` 模式，从 `preview/component-{slug}.html` 提取结构 → 装配进 codegen。

### 🔴 缺口 2｜没有「PRD→DSL」这一层 —— 目标的起点
- **现状**：DSL foresees AI 已产出 YAML，但没有把 PRD 转成 DSL 的引导。
- **方案**：不写解析器，写一套**手把手 PRD→DSL 转换引导**（规则 + 实例），接入 `SKILL.md` 作为工作流 **Step 0**。
- **转换逻辑**：
  1. 读 PRD → 拆页面清单
  2. 每页 → 判 `pattern`（六类之一）
  3. 该页结构 → 映射到对应模式骨架（`patterns.md`）
  4. 交互状态（空/错/载/权限/弹窗/展开收起）→ 列出，确保 DSL 覆盖
  5. 产出 YAML（符合 `dsl/schema.json`）→ 校验 → 编译

### 🟡 缺口 3｜无自动化产物验证 —— 缺"高可用"的最后一道 ✅ 已闭环（Step 3）
- **现状**：产出后仅人工看 / SKILL P0/P1/P2 审查。
- **已落地**：`scripts/preview-audit.py`（纯 Python stdlib + 系统 Chrome headless，无 node 依赖）——
  - 打开生成的 HTML → 截桌面图 1440×1000
  - DOM/CSS QA：标签平衡 / token 与 hex / 交互元素命名 / 弹层默认隐藏
  - 联动 Click Smoke：openTarget 是否指向存在的弹层、可关闭
  - 输出 Markdown 报告（放行结论/P1/截图/优化指令）+ `--json` 供 LLM 回喂
- **验证记录**：`giencoder/_audit/`（resource-list + form-detail 均通过、0 阻断、截图正常；顺带修出 modal/drawer 的一个 style 位置 bug）
- **优先级**：已完结。

### 🟡 缺口 4｜缺"标准维护"案例库
- `EVALUATOR.md §7` 已定义方法，但缺 `_review-cases/` 好/坏/混合/边界/品类五类样本。
- **做法**：积累每次"被打回的页面"为坏案例，沉淀 doNotInvent。

---

## 四、分步执行计划（每步独立可交付）

### Step 1｜打通 PRD→DSL 入口（最高杠杆）
**产出**：新增 `docs/prd-to-dsl.md`（转换引导）→ 接入 `SKILL.md` 工作流 Step 0。
**验收**：拿任一 PRD 走引导，能稳定产出合法 DSL YAML；`yq-build.py` 编译成功。

### Step 2｜补齐高频 emitters ✅
**产出**：`yq-build.py` 已新增 9 个 emitter（checkbox/radio/switch/tabs/form/form-item/statistic/modal/drawer），P0_EMITTERS 15 → 24；弹窗/抽屉支持开合（openTarget + data-close）。
**验收**：✅ 综合示例 `dsl/examples/form-detail.yq.yaml` 编译通过（221 行），产物含全部新组件 DOM；statistic 语义色验证正确。

### Step 3｜自动化验证闭环 ✅
**产出**：`scripts/preview-audit.py`（纯 Python + Chrome headless 截图）对齐 EVALUATOR 四层证据。行为：DOM/CSS QA（token/hex/class/命名/弹层联动）→ Click Smoke（openTarget 指向联通）→ Screenshot（1440×1000 桌面首屏）。
**用法**：`python3 scripts/preview-audit.py <page.html> [more...] --out DIR [--json] [--no-shot]`
**验收**：✅ 两个编译产物（resource-list / form-detail）跑通，放行结论「通过(过程稿)」、0 阻断、0 P1，截图生成且 CSS 正确加载。`--json` 输出供 LLM 回喂复用。

### Step 4（可选）｜标准维护案例库
**产出**：`_review-cases/` 首批案例（含 1-2 个被打回的坏案例）。

---

## 五、质量门禁（产出 HTML 是否"高可用"）

对齐 `EVALUATOR.md` + `SKILL.md`：
1. ✅ 217? 无外部 CSS 框架 / Lucide / CDN / 外部依赖 —— 自包含单文件
2. ✅ 全部走 Token，无硬编码 hex
3. ✅ 弹层 focus trap + Esc + 遮罩关闭
4. ✅ 每个 PRD 声明的交互状态（空/错/载/权限/…）都有实现
5. ✅ 键盘可达 + 焦点可见
6. ✅ 六维度评估通过，无阻断问题
7. ✅ 主任务首屏可辨（非 `generic_template_output`）
8. ✅ 自包含离线可开

---

## 六、与 Vibe 方法论的对齐（为什么这样设计）

- **声明 vs 契约**：你的 `components/{slug}.json` + `tokens.md` + `patterns.md` 是"声明"；`SKILL.md` + PRD→DSL 引导是"契约"（何时读、怎么用、做完怎么查）。本方案把它们串成可执行链路。
- **受控生成**：DSL + emitter 编译 = 受控生成，压制 AI 味。
- **证据链式评估**：Step 3 的截图/DOM/click = Vibe 的"让 AI 像人一样评估"。评审只看交付物，不看生成器意图。
- **从失败反推**：Step 4 案例库 = 标准在案例里长出来。

---

*由调研 Vibe + 盘点 giencoder 现有资产得出。待确认后逐项执行。*

---

## 附：如何跑通编译器（可复现）

> 问题：本机 Python 是 3.9.6，而 `yq-build.py` 原含 Py3.12 专属 f-string 语法 + 缺 `jsonschema` 依赖，直接跑报错。

**已做的修复**：
1. `scripts/yq-build.py` `emit_select` 的嵌套同引号 f-string 改为独立 helper `_select_option_html()`（避开 Py3.9 引号冲突）。
2. 建 venv 装依赖：`jsonschema` + `pyyaml`。

**复现命令**：
```bash
# 1) 建 venv（一次性）
python3 -m venv /tmp/gcvenv
/tmp/gcvenv/bin/pip install jsonschema pyyaml

# 2) 编译（每次）
cd giencoder
/tmp/gcvenv/bin/python scripts/yq-build.py dsl/examples/resource-list.yq.yaml --out /tmp/gc-test
# → ✓ resource-list.yq.yaml -> /tmp/gc-test/resource-list.html（239 行）

# 3) 校验单（编译失败时输出结构化 JSON，便于喂回 AI 重试）
/tmp/gcvenv/bin/python scripts/yq-build.py --json <page.yq.yaml>
```

> 建议后续把 venv 固化进 `scripts/requirements.txt`，避免换机器重复排查。
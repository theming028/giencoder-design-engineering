# GienCoder 设计系统 · 前端开发者 AI 协作手册

> 本手册面向前端开发者。当你在 giencoder 实现任务中需要 AI 协助时，按本手册触发和引导 AI。
> 入口 skill：`giencoder-design-router`（项目根 `.workbuddy/skills/`）

---

## 一、什么时候召唤 AI

| 场景 | 召唤方式 | 适合的 AI 任务 |
|------|----------|----------------|
| 实现新组件 | "按 giencoder 规范实现 [组件]" | 生成 .vue + 更新契约 |
| 修复组件 bug | "[组件] 有 [现象]，排查并修复" | 读契约 + CSS + 定位修复 |
| 组件扩展 | "给 [组件] 加 [新 props]" | 更新契约 propsIndex + 实现 |
| 像素级还原 | "按设计稿实现 [页面]"（设计稿通常为 Ardot/HTML） | 提取 token + 生成代码 |
| 对照半选实现 | "对比 giencoder 和半选的 [功能] 实现" | 调用 semi-design-guide MCP |

---

## 二、AI 协作流程（标准 6 步）

### Step 1：明确组件 + 契约

```
"我要实现 Affix 组件，需求：
- 吸顶后底边 1px 硬线
- 滚动到目标位置时触发
- 支持 offset 自定义
- 严格遵循 giencoder 契约"
```

### Step 2：AI 读契约 → 输出实现方案

AI 应：

1. 读 `giencoder/components/affix.json`（如不存在 → 告诉你"需先创建契约"）
2. 检查 `component-registry.json` 确认 affix 的 status
3. 读 `giencoder/preview/component-affix.html`（如存在）复制结构
4. 读 `giencoder/components.css` 确认 CSS 体系
5. 输出方案：
   ```markdown
   ## 实现方案
   - 文件：components/affix.json（契约更新）
   - HTML 结构：div.affix > div.affix-content
   - Token 引用：--color-border-1, --shadow1-down
   - 状态：default / fixed
   - 交互：滚动监听 + position: fixed 切换
   ```

### Step 3：审查方案

如方案有问题：

```
"用 inset box-shadow 实现 1px 硬线，不要用 border + shadow 双重（视觉冗余）"
"参考 Table 分页器的 pattern：box-shadow: inset 0 -1px 0 var(--color-border-1)"
```

### Step 4：生成代码 + 同步契约

```
"按上面方案实现，输出到 giencoder/components/affix.vue + giencoder/components/affix.json"
```

AI 会：
1. 写 `.vue`（class 用 `giencoder-affix` 等）
2. 更新 `affix.json` 的 `anatomy` / `propsIndex` / `states` / `interaction`
3. **双目录同步**：自动同步到 `giencoder-delivery/components/affix.json`

### Step 5：本地验证

```
"起 serve.py(8866) 验证，用 agent-browser 截图"
```

AI 会：
1. 启动 `python serve.py`（已在 giencoder 根目录）
2. 用 puppeteer-core 截图
3. 检查 box-shadow、border 等关键样式
4. 输出验证截图 + 通过/失败结论

### Step 6：契约 schema 校验

```
"按 schema-contract.md 校验 affix.json 通过校验"
```

AI 会：
1. 读 `giencoder/schema-contract.md` 确认 schema 字段
2. 用 jq 或 Python 校验 JSON 结构
3. 输出通过/缺失字段清单

---

## 三、典型场景示例

### 场景 A：实现新组件

```
你："按 giencoder 规范实现 BackTop 组件"
AI：[读 component-registry.json 确认 back-top status=new]
AI：[读 schema-contract.md 写契约]
AI：[生成 back-top.json 契约]
AI：[生成 back-top.html + back-top.css]
AI：[更新 component-registry.json]
你：审查 + 让 AI 用 serve.py 验证
```

### 场景 B：修复组件 bug

```
你："Affix 吸顶后视觉有 1px 跳变，是 border + shadow 双层问题"
AI：[读 giencoder/components/affix.json]
AI：[读 giencoder/components.css 中 .giencoder-affix 定义]
AI：[诊断：border-bottom 1px + box-shadow 同时存在，视觉重叠]
AI：[修复方案：去掉 border，改用 inset 0 -1px 0 模拟 1px 硬线]
AI：[生成修复后的 CSS]
AI：[puppeteer 截图验证]
```

### 场景 C：组件扩展（加 props）

```
你："给 Tag 组件加 closable 属性，支持关闭"
AI：[读 giencoder/components/tag.json 当前 propsIndex]
AI：[读 interaction 段]
AI：[扩展契约：propsIndex 加 closable、states 加 closing、interaction 加 onClose]
AI：[生成 HTML + CSS + JS]
AI：[serve.py + 截图验证]
```

### 场景 D：对照半选实现

```
你："giencoder Table 的列筛选和半选 Table 有什么实现差异？"
AI：[读 giencoder/components/table.json]
AI：[调 semi-mcp get_semi_document componentName="Table"]
AI：[调 semi-mcp get_file_code filePath="@douyinfe/semi-ui/table/foundation.ts"]
AI：[对比设计意图，输出要点]
```

---

## 四、契约同步规则（必读）

> giencoder 是**契约驱动**设计系统。改实现必须同步改契约。

| 操作 | 必须同步 |
|------|---------|
| 新增 props | `propsIndex.props` 数组 + `syncDate` 字段 |
| 新增状态 | `states` 数组 |
| 修改 anatomy | `anatomy` 数组 |
| 修改交互 | `interaction` 字段 |
| 新增使用场景 | `usage` 数组 |
| 禁用某些用法 | `doNotInvent` 数组 |

### 4.1 props 自动同步（优先用工具，别手抄）

`giencoder/scripts/sync-props.py` 从 npm 包 `.d.ts` 自动提取 props 并写入契约，避免手工抄错：

```bash
# 1. 下载并解压源启 npm 包
npm pack @giencoder-design/web-react@2.66.16
tar -xzf giencoder-design-web-react-2.66.16.tgz
# → 得到 package/ 目录

# 2. 运行同步脚本
python3 giencoder/scripts/sync-props.py /path/to/package

# 输出：每个 components/{slug}.json 追加 propsIndex 字段
#   propsIndex: { "interface": "ButtonProps", "props": [...], "total": N, "syncDate": "2026/08/28" }
```

**脚本逻辑**：slug → 驼峰目录名（`time-picker` → `TimePicker`）→ 读 `es/{Name}/interface.d.ts` 或 `index.d.ts` → 正则提取 interface props → 合并进契约。

**手动补 props 的场景**：契约里的 `anatomy` / `states` / `interaction` / `usage` / `doNotInvent` 是人工撰写的语义字段，脚本不管，需手工维护。

### 4.2 双目录同步（rsync）

```bash
# ✅ 正确：整体同步（推荐）
rsync -a giencoder/ giencoder-delivery/

# ❌ 错误：多源路径会把文件放错位置
rsync -av giencoder/components.css giencoder/components/table.json giencoder-delivery/
# → table.json 落到 giencoder-delivery/ 根目录（应为 components/）
# 正确做法：逐文件指定完整目标路径
rsync -a giencoder/components/table.json giencoder-delivery/components/table.json

# 验证一致
diff -r giencoder/ giencoder-delivery/ | head
```

**⚠️ 坑**：`rsync --delete` 会删掉 `giencoder-delivery/` 独有内容（如 `giencoder-task-ui.design/`）。用之前先确认快照独有目录策略。

---

## 五、禁止做的事（AI 触犯时立即反驳）

1. ❌ 引入外部 CSS 框架（`class="bg-blue-500"`）
2. ❌ 引入 Lucide / Heroicons / FontAwesome（用 `giencoder-icon` SVG 体系）
3. ❌ 引入外部 CDN 框架（jQuery / Bootstrap / Element UI）
4. ❌ 硬编码 hex 色值（`#3770F7` 必须走 `var(--color-primary-6)`）
5. ❌ 跳过契约更新（实现改了，契约没改）
6. ❌ 跳过双目录同步
7. ❌ 跳过 serve.py + puppeteer 验证
8. ❌ 把半选的 API / 事件名直接搬到 giencoder
9. ❌ **display 硬切换显隐**（必须走 `-open` class + transition，详见 `preview-format.md §5.4`）
10. ❌ 交互动效用第三方库（必须零依赖原生 JS，详见 `preview-format.md §5.2`）

---

## 六、组件开发工作流（详细版）

```
1. 需求拆解
   └ 组件功能 / 状态清单 / 交互清单

2. 查契约
   ├ 元件是否已存在？查 component-registry.json
   ├ 已存在 → 读 components/{slug}.json
   └ 不存在 → 读 schema-contract.md 创建契约

3. 实现
   ├ 从 preview/component-{slug}.html 原样复制结构（72 个模板基本全覆盖）
   ├ class 用 giencoder-* 体系（preview-format.md §2.1）
   ├ 颜色/间距/圆角/阴影/动效 全部 Token
   ├ 状态完备（default/hover/active/focus/disabled）
   ├ 交互组件加零依赖原生 JS（IIFE + 空指针防护，preview-format.md §5.2）
   └ 动效走 transition，禁止 display 硬切换（preview-format.md §5.4）

4. 同步契约
   ├ props 用 scripts/sync-props.py 自动同步（优先）
   ├ anatomy/states/interaction/usage/doNotInvent 手工维护
   ├ component-registry.json 状态更新（如有）
   └ rsync -a giencoder/ giencoder-delivery/ 双目录同步

5. 验证
   ├ serve.py(8866) 起服务
   ├ agent-browser / puppeteer-core 截图
   ├ 检查关键 Token 应用（computed style）
   └ JSON 契约 schema 校验

6. 交付
   ├ 提交到 giencoder/ 权威源
   ├ 确认 giencoder-delivery/ 快照一致（diff -r 校验）
   └ 输出验证截图
```

---

## 六点五、交互动效规范（交互组件必读）

> 完整规范见 `giencoder/preview-format.md §5`。以下是速查。

### 脚本（§5.2 硬性要求）

- 纯原生 JS，零依赖，IIFE 包裹
- 空指针防护（`querySelectorAll` + `forEach` 天然安全）
- 不抛异常（缺元素时静默返回）
- 状态切换复用模板已有 class，不发明新 class
- 不改既有 HTML 结构，只加 `<script>`

### 动效（§5.4 硬性要求）

| 场景 | 时长 | 内容 |
|------|------|------|
| hover / 按下 | 0.1s | 背景/边框/透明度过渡 |
| 弹层展开 | 0.2s | opacity 0→1 + scale(0.96→1) + translateY(4px→0) |
| 弹层收起 | 0.15s | opacity 1→0 + scale(1→0.98) |
| Modal/Drawer | 0.3s | mask 淡入 + 面板 scale/滑入 |
| 状态切换 | 0.15s | 背景/边框/勾选过渡 |

**禁止 display 硬切换**。正确模式：

```css
.popup { opacity: 0; visibility: hidden; transform: scale(0.96) translateY(4px);
         transition: opacity .2s, transform .2s, visibility .2s; }
.popup.open { opacity: 1; visibility: visible; transform: scale(1) translateY(0); }
```

```js
// 展开
popup.style.display = 'block';
requestAnimationFrame(function () { popup.classList.add('open'); });
// 收起
popup.classList.remove('open');
setTimeout(function () { popup.style.display = 'none'; }, 200);
```

---

## 七、工具链速查

| 工具 | 用途 | 启动方式 |
|------|------|---------|
| serve.py | 本地预览 | `python serve.py`（端口 8866） |
| agent-browser / puppeteer-core | 自动化截图 | AI 调用，输出到 `outputs/` |
| **sync-props.py** | **props 自动同步** | `python3 giencoder/scripts/sync-props.py <package_dir>` |
| **rsync** | **双目录同步** | `rsync -a giencoder/ giencoder-delivery/` |
| schema-contract.md | 契约 v3 规范 | 人工 + AI 校验 |
| preview-format.md | 模板 + JS + 动效规范 | 人工 + AI 对照 |
| install.sh | 跨 IDE 安装（symlink 到 5 个 IDE） | `bash giencoder/install.sh [--force]` |
| semi-mcp | 外部参考 | 需连接器管理页 Trust |

---

## 八、协作节奏建议

- **契约先行**：先读/写契约，再写实现。避免实现跑偏后才发现契约不匹配
- **小步迭代**：每改一个 props / state，先让 AI 更新契约 + 实现 + 验证
- **每步要可验证**：每个交付物都能用 serve.py 或 puppeteer 看一眼
- **Token 优先于记忆**：遇到不确定的色值/间距，让 AI 查 `tokens.md`，不要凭记忆

---

## 九、问题反馈

发现 giencoder 契约/Token/CSS 错误时：
```
"giencoder/components/{slug}.json [字段] 与实现不一致，请按 schema-contract.md 修复并双目录同步"
```

AI 会自动修契约 + 同步 giencoder-delivery/，并起 serve.py 验证。

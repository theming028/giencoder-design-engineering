# 设计语境路由：GienCoder 设计系统 与 CloudAI-UI 并存说明

> 本仓库同时存在两套相互独立的 UI 设计语境。**它们不混装、不互相覆盖**。
> 本文件说明何时用哪套，避免误用造成样式冲突。

## 两套体系的定位

| | **GienCoder 设计系统** | **CloudAI-UI** |
|---|---|---|
| 位置 | `giencoder/`（进入点 `giencoder/SKILL.md`） | `.agents/skills/CloudAI-UI/`（进入点 `SKILL.md`） |
| 设计语言 | 源启（Semi/字节系源启 Design） | 字节 CloudAI / Harness UI 风格 |
| 技术栈 | 自研 HTML/CSS + CSS 变量 token、JSON 契约、Python 工具 | 已移除，唯一依赖 GienCoder Design System |
| 硬规则 | 不引入外部 CSS 框架、不用 Lucide；token 禁硬编码 | 只用语义 token；禁手搓组件 |
| 本仓库角色 | **主体系、唯一权威** | **备选风格语境、独立存放** |

## 决策规则：什么时候用哪套

1. **默认走 GienCoder**。本仓库生成任何 UI，都先查 `giencoder/SKILL.md` →
   `components/{slug}.json` → `tokens.md`，按源启规范实现。
2. **只有用户明确要求「要字节/CloudAI/Harness 风格的页面」时，才用 CloudAI-UI**，
   且场景要在独立的 CloudAI 工程里（`node …/create-app.mjs` 新建），**不要**在
   GienCoder 工程的页面里混排两套 token。
3. **两套不许互相桥接换取色值**。GienCoder 的 `--color-primary-6` 与 CloudAI 的
   `bg-primary` 是不同的设计语言，语义不同（Brand ≠ Primary 等规则互不通用）。
4. **可互相借用的只有「判断规则」**：
   - GienCoder 页面需要走查层级/间距/状态齐全度时，可参考 CloudAI 的
     `design-review.md`（它看层级/间距/状态，不看类名）——这不是桥接 token。
   - 反之亦同。

## 维护

- 各自按各自的演进路线更新，互不改对方文件。
- 若想移除 CloudAI-UI，删 `.agents/skills/CloudAI-UI/` 与本说明即可；GienCoder 体系不受影响。
- 若未来某页要双风格对照评审，各自在各自工程里出稿，再并排比较，不要在同一份 HTML 里混装。
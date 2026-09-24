# 组件契约 v3 Schema 编写规范（Schema Contract Spec）

> 用途：Phase 2 并行生成 71 个组件契约 JSON 的**唯一格式依据**。所有生成的 `components/{slug}.json` 必须严格遵循本 schema，字段完整、值域受限。
> 版本：schemaVersion = 3 ｜ 库：源启 Design React 2.66.16 ｜ 文件位置：`GienCoder 设计系统/giencoder/components/{slug}.json`

---

## 1. 顶层结构

```json
{
  "schemaVersion": 3,
  "slug": "button",
  "name": "Button",
  "category": "general",
  "giencoderSource": { "component": "Button", "version": "2.66.16" },
  "summary": "一句话说明组件用途与典型场景",
  "variants": [],
  "sizes": [],
  "states": [],
  "anatomy": [],
  "interaction": {},
  "a11y": {},
  "usage": [],
  "doNotInvent": [],
  "tokensConsumed": [],
  "assetsConsumed": []
}
```

## 2. 字段规范

### slug / name / category
- `slug`：源启官方组件名 kebab-case（`page-header`、`time-picker`、`tree-select`）
- `category`：枚举 `general | layout | navigation | data-entry | data-display | feedback | other`（对齐 component-registry.json）

### giencoderSource（必填）
```json
"giencoderSource": { "component": "Button", "version": "2.66.16" }
```
`component` 为 源启官方组件导出名；映射组件（layout/menu/radio/tag）注明 `mapsFrom`：如 `{"component":"Tag","version":"2.66.16","mapsFrom":"status-tag"}`。

### variants（变体，≥1 项）
每个变体对象：
```json
{ "name": "primary", "description": "主操作按钮，强调页面中最主要的行动", "whenToUse": "页面主 CTA、提交、确认" }
```
变体必须覆盖该组件 源启官方所有视觉形态（如 Button: primary/secondary/outline/dashed/text；Tag: 默认/描边/亮色/暗色/可关闭；Menu: 垂直/水平/内嵌/弹出）。

### sizes（尺寸，≥1 项）
```json
{ "name": "medium", "value": "32px", "usage": "默认尺寸" }
```
组件尺寸命名统一：`mini | small | medium | large`（无尺寸变体的组件省略该字段或填 `[{ "name": "default" }]`）。

### states（状态，≥2 项）
```json
{ "name": "hover", "description": "鼠标悬停时的视觉反馈", "visual": "背景/边框色变化，0.1s 过渡" }
```
状态枚举：`default | hover | active | focus | disabled | loading | error | empty | checked | selected | expanded`，按组件实际覆盖。

### anatomy（结构，≥1 项）
```json
{ "part": "prefix-icon", "element": "span/icon", "description": "前缀图标位" }
```
列出组件 DOM 关键结构部件。

### interaction（交互契约，必填）
```json
"interaction": {
  "hover": "…",
  "focus": "…",
  "keyboard": ["Enter: 触发", "Space: 触发", "Tab: 焦点进入"],
  "motion": { "duration": "0.1s", "easing": "standard", "description": "按下态 0.1s 过渡" },
  "behaviorNotes": "…"
}
```
- `keyboard`：数组，每项 `"按键: 行为"`
- `motion.duration/easing` 取值必须来自 tokens.md（0.1s~0.5s / linear|standard|overshoot|decelerate|accelerate）
- 弹层类组件（Select/Dropdown/Tooltip/Popover/Modal/Drawer 等）必须写 `focusTrap`、`escClose`、`clickOutsideClose` 行为

### a11y（无障碍，必填）
```json
"a11y": {
  "role": "button",
  "ariaAttrs": ["aria-label", "aria-disabled"],
  "contrastNote": "文字/背景对比度 ≥ 4.5:1",
  "focusNote": "可见焦点环"
}
```

### usage / doNotInvent
- `usage`：正确使用要点（数组）
- `doNotInvent`：**禁止**项——不得新增官方不存在的变体/状态/class；不得用外部 CSS 框架/Lucide 替代

### tokensConsumed / assetsConsumed
- `tokensConsumed`：该组件实际消费的 token 名数组（从 tokens.md 取）
- `assetsConsumed`：图标等资源（无则 `[]`）

### propsIndex（自动同步，勿手改）
```json
"propsIndex": {
  "interface": "ButtonProps",
  "props": ["disabled", "loading", "onClick", "type", "..."],
  "total": 40,
  "syncDate": "2026/08/28"
}
```
- 由 `scripts/sync-props.py` 从官方包 .d.ts 自动提取（含接口继承链）
- **不要手改**：重新运行脚本即覆盖同步

## 3. 生成规则（硬约束）

1. **如实反映 源启官方设计**：variants/states/interaction 必须对应 源启 React 2.66 真实能力，不得虚构
2. **interaction.keyboard 必须非空**：至少覆盖 Enter/Space/Tab 的合理行为；无键盘交互的纯展示组件（如 Divider、Statistic）写 `["无键盘交互（纯展示）"]`
3. **a11y 必须非空**：role/ariaAttrs 至少一项
4. **category 必须与 component-registry.json 一致**
5. **语言**：description/summary/usage 用中文；technical 字段（keyboard/role）用英文枚举
6. **文件大小**：单个契约 ≤ 8KB，追求精炼完整而非冗余

## 4. 生成顺序与分组

按 component-registry.json 的组件顺序，建议每组 6–8 个组件并行生成（详见 workflow 调度）。生成完成后人工抽查 10%（抽查重点：弹层类组件的交互契约、映射组件的 mapsFrom 字段）。

# 源启全量规范目录（giencoder/）

> 本目录是 **GienCoder 设计系统规范层**，以源启官方命名为唯一标准。
> 目标：覆盖源启 Design React 2.66.16 全部 71 个组件的 UI 与交互要素，供人类设计师与 AI agent 共同消费。

## 目录结构

```
giencoder/
├── component-registry.json   # 全量 71 组件注册表（分类/覆盖状态/映射）— Phase 0
├── PHASE0-范围冻结.md         # 范围冻结报告：缺口分析 + 命名映射表 — Phase 0
├── tokens.md                 # Design Token 全量规范（色板/字体/间距/圆角/阴影/动效/z-index）— Phase 1
├── schema-contract.md        # 组件契约 v3 Schema 编写规范 — Phase 2
├── components/               # 71 个组件契约 JSON（schemaVersion 3）— Phase 2
│   ├── index.json            # 组件索引（自动生成）
│   └── {slug}.json           # 每个组件的契约（含 interaction/a11y/giencoderSource）
├── patterns.md               # 页面模式规范（列表/详情/表单/空错载态）— Phase 4
├── a11y.md                   # 无障碍规范 — Phase 4
└── preview/                  # 核心组件代码模板 HTML — Phase 3
```

## 消费入口

> 人类设计师与 AI agent 均从 [`SKILL.md`](./SKILL.md) 进入：读取顺序、工作流、质量门禁单一收敛于此。

## 覆盖状态（Phase 0 统计）

- ✅ covered 28：现有组件直接同名覆盖（契约升级至 v3）
- 🔄 mapped 4：自研命名 → 源启官方（layout/menu/radio/tag）
- 🆕 new 39：全新补齐

## 版本

- 源启 Design React：`2.66.16`
- Schema 版本：`3`

---

** 作者：Ming / PAA **

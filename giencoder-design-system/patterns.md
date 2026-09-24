# 页面模式规范（Patterns）

> 层级：L4 ｜ 用途：定义企业级 B2B 页面的标准结构与组合规则，对齐现有 `gienx-templates/` 样板，规范覆盖 **列表/详情/表单/看板/配置/结果** 六大模式。
> 原则：页面 = 骨架（Layout+Menu）+ 区块（Card/PageHeader/Table/Form…）+ 状态（空/错/载）+ 反馈（Modal/Drawer/Message…）

---

## 1. 后台骨架（Layout Pattern）

```
┌────────────────────────────────────────────┐
│ Layout.Header（48px）  Logo | 搜索 | 用户区  │
├──────────┬─────────────────────────────────┤
│          │                                 │
│ Layout.  │  Content（内边距 20px，区块间距   │
│ Sider    │  16-24px，栅格 24 列）           │
│ 200px    │                                 │
│ Menu     │                                 │
│          │                                 │
├──────────┴─────────────────────────────────┤
│ Layout.Footer（可选）                       │
└────────────────────────────────────────────┘
```

| 区域 | 规格 | Token |
|------|------|-------|
| Header | 高 48px，通栏 | `--color-bg-2`，底 `--shadow1-down` |
| Sider | 宽 200px（可折叠至 48px） | `--color-menu-light-bg` |
| Content | flex:1，内边距 20px，overflow-y:auto | `--color-bg-1` |
| 模块间距 | 区块间 16-24px | `--spacing-6`~`--spacing-9` |

**规则**：Sider 内 Menu mode=vertical + selectedKeys 与路由联动；折叠态 Sider 宽 48px 仅图标。

---

## 2. 列表页（List Page）

### 结构
```
PageHeader（标题 + 操作区）
├─ FilterBar（筛选行：Input/Select/DatePicker + 查询/重置）
├─ Card
│  ├─ Table（列/排序/分页）
│  ├─ BatchBar（批量操作，选中行后出现）
│  └─ Pagination（pageSize 切换 + 快速跳转）
```

### 规范
- 筛选项 ≤ 6 个，超过折叠进"更多筛选"（Collapse）
- Table 行操作 ≤ 3 个，超过收进 Dropdown
- 批量操作出现时主表格首列出现 Checkbox
- 空数据显示 Empty；加载显示 Skeleton 行；失败显示 Alert + 重试

---

## 3. 详情页（Detail Page）

### 结构
```
Breadcrumb + PageHeader（返回按钮 + 标题 + 操作）
├─ Tabs（overview/参数/日志…）
├─ Descriptions（基础信息，2-4 列）
├─ Card 组（分区块展示）
└─ 右侧信息栏（可选，300px）
```

### 规范
- 只读信息用 Descriptions，禁用表单模拟只读
- 主操作（编辑）放 PageHeader extra；危险操作（删除）放页尾或 Dropdown，需 Popconfirm
- 区块加载用 Skeleton；失败用 Result(status=error) + 重试

---

## 4. 表单页（Form Page）

### 结构
```
PageHeader（标题 + 提交/取消）
├─ Card（Form 单列/双列/分组）
│  ├─ FormItem（label + 控件 + help + 校验）
│  └─ 分区标题（Divider withText）
└─ 底部操作条（取消 + 提交）
```

### 规范
- 单列表单字段 ≤ 8 个；超过按逻辑分组
- 必填项 label 加星号；校验错误红字 + 红框（`--color-danger-*`）
- 提交按钮 loading 防重复提交；成功 Message.success，失败 Alert 汇总
- 长表单（>2 屏）用 Steps 分步

---

## 5. 数据看板（Dashboard）

### 结构
```
PageHeader + 时间筛选条
├─ Statistic 行（4 个核心指标卡）
├─ 图表区（Grid 24 列栅格：图表 Card）
└─ 明细区（Table/List）
```

### 规范
- 核心指标用 Statistic 卡（前缀图标 + 数值 + 环比）
- 图表用 `--color-data-1..20` 序列配色，保持系列色一致
- 图表 Card 统一标题 + 溢出 Dropdown
- 数据加载用 Skeleton 区块，避免布局跳动

---

## 6. 配置页（Config Page）

### 结构
```
PageHeader（标题 + 保存）
├─ Tabs（基础配置/高级配置…）
└─ Form（分区卡片：Switch 开关配置项 + 说明）
```

### 规范
- 配置项用 Switch + 说明文字组合
- 保存反馈：成功 Message.success；失败 Alert 定位出错分区
- 危险配置（重置/删除）红色警示 + Popconfirm 二次确认

---

## 7. 状态模式（空/错/载）

| 状态 | 组件 | 规范 |
|------|------|------|
| 空 | Empty | 图标 + 说明 + 可选操作（新建/刷新） |
| 加载 | Skeleton / Spin | 区块用 Skeleton，整页用 Spin 包裹 |
| 失败 | Result / Alert | 整页失败用 Result(status=error)+重试；局部失败用 Alert 行内 |
| 无权限 | Result(status=403) | 提示 + 返回首页操作 |

---

## 8. 反馈规范

| 场景 | 组件 | 规范 |
|------|------|------|
| 全局成功提示 | Message.success | 简短，2-3s 自动消失 |
| 全局错误 | Notification.error | 带详情，可关闭 |
| 二次确认 | Popconfirm | 破坏性操作必须使用 |
| 大表单/详情编辑 | Drawer / Modal | 内容 <1 屏用 Modal，≥1 屏用 Drawer |
| 局部提示 | Tooltip / Popover | hover 提示用 Tooltip，带操作内容用 Popover |

---

## 9. 组合禁止项

1. 禁止页面内混用旧版 class（`.btn`、`.data-table`）与 源启官方 class（`.giencoder-btn`）——统一用一套（新页面用 源启官方）
2. 禁止在 Table 单元格堆叠超过 2 个主操作
3. 禁止弹窗套弹窗超过两层
4. 禁止页面内超过一个 primary 主按钮
5. 禁止用自定义 div 模拟组件（一律用规范组件）

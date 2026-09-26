# COMPONENTS.md — 需求看板组件树

## 复用状态图例
- **直接用** = giencoder 设计系统已有组件，bundle 内联样式直接套 class
- **wrap** = 基于现有组件包一层局部适配（kb-/rq- 前缀）
- **自建** = 设计稿特有，本页新建

## 组件清单

### Token（已在 colors_and_type.css / bundle，无需新建）
全部颜色/字号/圆角/间距走 `var(--*)`，见 PLAN.md token 表。

### Primitive 原子
| 名字 | 类型 | node_id | 复用状态 | props/variants |
|---|---|---|---|---|
| 状态点图标 | Icon | 817:12171等 | 直接用(SVG内联) | status: todo/doing/done/stop/cancel |
| 排序图标 | Icon | 817:11738 | 直接用(SVG) | — |
| 统计卡图标 | Icon | 769:13140等 | 直接用(SVG) | status 5种 |
| 状态标签 | Badge | 817:12057 | 自建 `.rq-status` | status 5色(bg+dot+文字) |
| 需求类型标签 | Tag | 769:27109 | 自建 `.rq-type` | 纯文本 |

### Composite 复合
| 名字 | 类型 | node_id | 复用状态 | 说明 |
|---|---|---|---|---|
| 统计卡 | Card | 组10369 | 自建 `.rq-stat` | tile图标+竖线+标签+数字(+箭头) |
| 表格行 | Row | 769:23096 | 自建 `.rq-row` | 7列: 序号/ID/类型+标题/创建者/状态/时间 |
| 表头 | Header | 矩形490 | 自建 `.rq-thead` | 列标题+排序图标 |
| 类型筛选 | Select | 769:32911 | **直接用** giencoder-select | single, small |
| 状态筛选 | Select | 817:14088 | **直接用** giencoder-select | single, small |
| 日期筛选 | DatePicker | 769:32905 | **直接用** giencoder-date-picker | range, small |
| 搜索框 | Input | 817:11794 | **直接用** giencoder-input-wrapper | prefix搜索图标 |
| 分页 | Pagination | 817:13850 | **直接用** giencoder-pagination | medium |
| 加载骨架 | Skeleton | — | **直接用** giencoder-skeleton | 6行 |
| 空状态 | Empty | — | **直接用** giencoder-empty | 图标+标题+描述 |

### Layout/Module 页面级
| 名字 | node_id | 复用状态 | 说明 |
|---|---|---|---|
| topbar | 1333:18255 | **wrap** kanban KB_HTML | radio 选中态切换 |
| panel | 769:13709 | wrap kanban `.kb-panel` | 同构容器 |
| stats行 | 组10369×5 | 自建 `.rq-stats` | flex 均分 |
| boardhead | 769:32931 | 自建 `.rq-boardhead` | 标题+控件区 |
| 表格区 | 矩形486 | 自建 `.rq-table` | thead+tbody+pager |
| fab | 同kanban | **直接用** `.kb-fab` | 共享 |

## 构建顺序
1. token（已有，跳过）
2. primitive：状态标签 `.rq-status`、类型标签 `.rq-type`、图标内联
3. composite：统计卡 `.rq-stat`、表格行/表头、复用 giencoder select/date-picker/pagination/skeleton/empty/input
4. module：topbar(wrap) → stats行 → boardhead → 表格区 → 分页 → fab
5. 整页拼接 + 切换交互 + 边界状态 + 响应式

## 交互脚本（复用 kanban.html 的 bindComponents）
- select 展开/选项互斥/清除/外部收起
- date-picker range 两击/月份导航/外部收起
- **新增** radio 切换 `data-goto` 跳转
- **新增** 分页按钮 active 切换
- **新增** 状态机 loading→ready（演示 800ms）

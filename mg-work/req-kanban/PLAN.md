# PLAN.md — 需求看板 (769:13709) 还原规划

## 概览（项目上下文，前序任务已确定，不再询问）
- **设计稿来源**：MasterGo file=193158744355579, layer=769:13709「需求看板 - 1」, 1440×900
- **目标产物**：`pages/req-kanban.html` —— 单文件独立页（CSS/JS 全内联），与 `pages/kanban.html`（任务看板）构成 radio 切换关系
- **技术模式**：沿用前序约定 —— 以 `dev.html` 为公共外壳骨架（React bundle 渲染 appbar/header/侧栏 + `<main>`），页面增量内容通过注入脚本塞入 `<main>`
- **样式规范**：严格使用 GienCoder Design System token 变量（`var(--color-*)`），禁止硬编码 hex（设计稿 DevMode 直出值除外，需在白名单）
- **组件复用**：giencoder select / date-picker / pagination / skeleton / empty / input，契约见 `giencoder-design-system/components/*.json`
- **基准宽度**：1440（设计稿），内容区自适应
- **交互态范围**：hover / 选中 / 加载(skeleton) / 空(empty) / 切换

## 设计 Token（取自 colors_and_type.css + DSL）
| 角色 | token | 值(light) |
|---|---|---|
| 页面底色 | — | #E5EDF5（React 外壳 dev 模式已给） |
| panel 白底 | --color-bg-1 | #FFFFFF |
| 表头底 | — | #FAFAFA (DSL 矩形490) |
| 行白底 | --color-bg-1 | #FFFFFF (矩形487) |
| 行斑马底 | --color-fill-1 | #F7F7F7 (矩形488) |
| 主文字 | --color-text-1 | #1F1F1F |
| 次文字 | --color-neutral-7 | #6B6B6B |
| 弱文字 | --color-text-3 | #868686 |
| 边框 | --color-border-2 | #E5E5E5 |
| 分隔线 | --color-border-1 | #F2F2F2 |
| 品牌蓝 | --color-primary-6 | #3770F7 |
| 状态-未开始 | — | 灰 #6B6B6B / bg #F2F2F2 |
| 状态-进行中 | — | 蓝 #5592EB / bg #E3EEFF |
| 状态-已完成 | — | 绿 #009E61 / bg #E2F4E4 |
| 状态-已终止 | — | 红 #F76560 / bg #FDE2E3 |
| 状态-已取消 | — | 橙 #F3881E / bg #FFECD9 |
| 字号阶梯 | --font-size-body-1/2/3 | 12/13/14px |
| 圆角 | --border-radius-medium/large | 4/8px（卡片6、按钮6、弹层8） |

## 模块清单（自上而下，node_id → 尺寸）
| # | 模块 | node_id | 尺寸/位置 | 说明 |
|---|---|---|---|---|
| M1 | panel 容器 | 769:13709 | 1424×842 内容区 | 白底圆角8，与任务看板同构 |
| M2 | topbar | 1333:18255 同源 | 1424×48 | 搜索框+radio(需求看板选中)+更新时间，**与 kanban.html 共享** |
| M3 | stats 行 | 组10369/10370/10371/10372/10339 | 5×264×64, top112 | 未开始5/进行中1/已取消7/已终止40/已完成40 |
| M4 | 分隔线 | 直线43 | 1384×1, top196 | #F2F2F2 |
| M5 | boardhead | 769:32931/32910/组10378 | top216 | 「我的需求」+搜索框(220)+类型select+状态select+日期(250) |
| M6 | 表格 | 矩形486区 | 1384×~565, top259 | 表头(序号/需求ID/需求标题/创建者/状态/创建时间)+8行+滚动条 |
| M7 | 分页 | 组10379 | 1384×48, top824 | 共256条需求 + giencoder pagination |
| M8 | fab | 同 kanban | 右下 | 智能助手悬浮按钮，**共享** |

## 复用现有部分（不重新造）
- **React 公共外壳**：appbar(红绿灯/工作空间/基础·研发工作台 tab)、dev 配色 —— bundle 已渲染，路由补丁 `/req-kanban`
- **topbar / panel / divider / fab**：直接复用 kanban.html 的 KB_HTML 对应段（radio 换选中态）
- **giencoder Select**：类型/状态筛选（bundle 已内联样式）
- **giencoder DatePicker(range)**：日期筛选（calendar CSS 已在 kanban 注入，本页复制）
- **giencoder pagination / skeleton / empty / input**：bundle 已内联样式

## 切换交互
- topbar radio「需求看板」↔「任务看板」：`data-goto` 属性 + 点击 `location.href` 跳转（file:// 与 http 双模式可用）
- 两页共享同一 React 外壳 + 同一 topbar 结构 → 切换时布局连贯无跳变

## 边界状态
- **加载中**：`data-state="loading"` → 显示 skeleton 行（6 行），隐藏表格/分页
- **空数据**：`data-state="empty"` → 显示 giencoder-empty（图标+文案）
- **正常**：`data-state="ready"`（默认演示态，800ms 后由 loading 切入）

## 响应式
- panel 宽度 100% 自适应（跟随 main）
- stats 卡 flex:1 均分；表格列宽百分比 + 标题列弹性；min-width 保护横向滚动
- 断点：<1200 表格横向滚动；<900 stats 换行

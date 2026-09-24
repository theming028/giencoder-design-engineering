# PRD 梳理 · 智能软件工厂「任务清单」单页原型

> 输入：`.dsh-uploads/prototype.zip`（tasks 原型，index.html + styles.css + app.js）
> 目的：为「PRD→DSL→HTML→验证→评估」全链路提供信息底稿；先梳理，再下结论。

## 1. 页面定位

- **产品**：GienCoder「智能软件工厂」——软件工厂化生产平台
- **页面**：任务清单（主视图），单页应用
- **一句话**：一级工作项（业务归口）→ 二级任务（唯一执行单元）的两级任务管理面板，支持状态流转、指标下钻、DevOps 双写同步。
- 页面类型判定：`list_page`（列表/管理类，含统计带 + 表格 + 工具条）。符合 Vibe 六类。

## 2. 页面结构

| 区块 | 内容 | DSL 组件映射 |
| :-- | :-- | :-- |
| 顶栏 | logo / 项目切换 / 全局搜索(⌘/) / 通知badge / 头像 | `top-nav`（compiler 有） |
| 左导航 | 任务清单/我的任务/已完成/已取消/回收站 + 迁移管理 + 状态图例 | `sidenav-menu`（有） |
| 页面头 | 标题「任务清单」+ 副文案 + 「新建一级工作项」primary | `page-header` |
| 统计带 | 工作项数 / 待开发/开发中/已完成/已取消 / 同步异常 | `statistic` ×N（有） |
| 工具栏 | 4 个筛选 chip（一级类型/业务状态/来源/任务分类）+ 全部展开/折叠 | `filter-bar`（有，静态版） |
| 表格 | **两级树形**：一级行 + 可展开的二级任务行，各列含 tag/状态/指标/操作 | `table`（有，但无树形） |
| 分页 | 共 N 个一级工作项 + 每页条数 + 翻页 | `pagination`（有） |
| 弹窗×4 | 新建一级工作项 / 确认删除 / 新增二级任务 / 分配执行人 | `modal`（有） |
| 抽屉×2 | 指标下钻 / 同步异常详情 | `drawer`（有） |
| Toast | 操作反馈 | 无 emitter |

## 3. 数据模型

- **一级工作项** `w`：id, type(business/tech/defect), title, source(devops/ai/default), status, extStatus, tasks[]
- **二级任务** `t`：id, title, source, category(dev/design/test/other), status, assignee, sync, lines, aiGen, aiAdopt, aiMerge, hours
- **一级状态 = 聚合函数**（PRD 第7章）：全 canceled→cancelled；全 done→done；有 doing→doing；ready+done 混合→doing；有 ready→ready；否则 unassigned
- **同步状态** sync：none/ing/ok/fail/conflict/map（fail/conflict/map 算"同步异常"）

## 4. 交互状态清单（EVALUATOR 交互就绪维度）

| 状态 | 触发 | DSL 覆盖 |
| :-- | :-- | :-- |
| 展开/折叠一级行 | 点击行 | ❌ 无树形 emitter（标注） |
| 筛选 | 勾选 chip | ⚠️ 静态展示，无动态过滤 |
| 全局搜索 | 输入 `/` | ⚠️ 静态展示 |
| 新建一级工作项弹窗 | 点击 primary | ✅ modal 可开合 |
| 二级任务状态流转（开始/停止/完成/取消） | 行内操作 | ⚠️ 静态按钮 |
| 分配执行人弹窗 | 行内"分配执行人" | ✅ modal 骨架 |
| 删除确认弹窗 | 行内"删除" | ✅ modal（danger 确认） |
| 指标下钻抽屉 | 行内"指标下钻" | ✅ drawer 可开合 |
| 同步异常抽屉 | 行内"同步异常" | ✅ drawer 可开合 |
| Toast 反馈 | 各类操作 | ❌ 无 emitter |
| 空态 | 无匹配任务 | ✅ empty |

## 5. 组件覆盖结论

- **DSL 可精确还原（静态可交互）**：顶栏/左导航/页面头/统计带/表格（平面列）/过滤条/分页/弹窗×4/抽屉×2 —— 页面的"骨架 + 弹窗联动"全闭环。
- **超出编译器能力，需标注**：
  1. **树形表格**（两级展开）—— 无 emitter，用 `tree` 契约待补
  2. **动态聚合/筛选/搜索**（JS 状态逻辑）
  3. **Toast** 反馈
  4. **加权进度/迷你图表**（订单/指标可视化，本页新增了统计但未含 chart）

## 6. 评审注意点（Vibe 模式）

- 两种来源双写（AI 平台 vs DevOps）是**领域核心**，`同步异常`状态差异提示（⚠ 状态差异）是业务可信维度的关键证据，重建不得丢失。
- 一级状态聚合算法、危险操作（删除级联）的确认，是信息架构/交互就绪维度重点。
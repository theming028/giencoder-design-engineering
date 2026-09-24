# GienCoder Design Engineering

> GienCoder 设计工程 — 基于 MasterGo 设计稿 + GienCoder Design System 的页面还原交付物。

## 快速开始

每个 HTML 文件都是**完全独立的静态页面**（CSS/JS 全部内联），双击即可在浏览器中打开预览，无需安装任何依赖、无需启动服务器。

```
pages/
├── base.html           ← 基础工作台（对话框 + 工作空间切换 + 会话列表）
├── dev.html            ← 研发工作台（代码仓库 + 构建流水线）
├── avatar.html         ← 数字分身（AI 分身创建与管理）
├── automation.html     ← 自动化（定时任务编排）
├── skills.html         ← 技能 Skills（能力与工作流管理）
└── settings.html       ← 设置（外观 / 账户 / 通知 / 版本信息）
```

## 页面说明

| 文件 | 页面 | 主要功能 |
|------|------|----------|
| `base.html` | 基础工作台 | 对话输入框、大模型选择、工作目录选择、权限选择、会话操作下拉菜单、工作空间切换浮窗 |
| `dev.html` | 研发工作台 | 代码仓库入口、构建流水线、依赖扫描、发布管理 |
| `avatar.html` | 数字分身 | AI 分身列表、新建分身、状态标签 |
| `automation.html` | 自动化 | 定时任务列表、运行状态、调度计划 |
| `skills.html` | 技能 Skills | 技能卡片网格、内置/可安装标签 |
| `settings.html` | 设置 | 返回链接、设置分组、通用/关于 |

## 打开方式

### 方式一：直接打开（推荐）

用浏览器（Chrome / Edge / Safari）直接打开任意 HTML 文件：

- macOS：`open pages/base.html`
- 或在 Finder 中双击 HTML 文件

### 方式二：本地服务器（可选）

如果需要模拟完整路由跳转：

```bash
cd pages
python3 -m http.server 8080
# 浏览器打开 http://localhost:8080/base.html
```

## 页面间跳转

页面之间通过导航链接互相跳转：
- **Header Tab**：基础工作台 ↔ 研发工作台（带 pill 滑动动效）
- **左侧菜单**：数字分身 / 自动化 / 技能 Skills / 设置
- **设置页**：左上角"返回基础工作台"链接

所有跳转在各 HTML 文件之间进行，无需服务器支持。

## 设计还原规范

- **设计稿来源**：MasterGo（layer_id 逐个拉取 DSL + extractSvg）
- **样式代码**：严格使用 MasterGo DevMode 提供的现成 CSS，不自我发挥
- **SVG 图标**：path data 由 extractSvg 原样内联，禁止手绘近似
- **坐标定位**：`position: absolute` + `left/top`，按设计稿像素级还原
- **设计系统**：唯一依赖 GienCoder Design System（giencoder），不引入外部 CSS 框架
- **边框补偿**：容器有 `border` + `box-sizing: border-box` 时，子元素 `left/top` 减去 border 宽度补偿偏移

## 技术栈

- React 18 + TypeScript
- Vite 8（构建工具，`viteSingleFile` 内联输出）
- Tailwind CSS 3（样式框架，已清理所有 Tailwind 原生文件，仅保留构建产物）
- GienCoder Design System（自研设计令牌 + 组件样式）

## 目录结构

```
GienCoderDesignEngineering/
├── pages/                          ← 交付页面（6 个独立 HTML）
│   ├── base.html
│   ├── dev.html
│   ├── avatar.html
│   ├── automation.html
│   ├── skills.html
│   └── settings.html
├── giencoder-design-system/       ← 设计系统规范
│   ├── components/                 ← 组件 JSON 规范（48 个）
│   ├── preview/                    ← 组件预览页（48 个 HTML）
│   ├── components.css              ← 组件样式
│   ├── colors_and_type.css        ← 色彩与字体样式
│   ├── tokens.md                   ← 设计令牌文档
│   └── ...
├── assets/                         ← 图标资源
│   └── icons/
├── GienCoder-DESIGN.md             ← 设计规范主文档
├── GETTING-STARTED.html           ← 使用说明书
└── README.md                       ← 本文件
```

## 版本

- **交付日期**：2024-09-24
- **构建工具**：Vite 8 + viteSingleFile
- **设计稿**：MasterGo file=193158744355579

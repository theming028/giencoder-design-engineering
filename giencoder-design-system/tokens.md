# Design Token 规范 — 源启设计全量 Token 体系

> 来源：`@giencoder-design/web-react@2.66.16` 主题定义（`es/style/theme/`，官方编译产物）
> 版本：v3 ｜ 用途：本文件是设计系统 Token 层的**唯一权威**；CSS 变量实现见 `colors_and_type.css`
> 命名约定：CSS 变量使用 `--` 前缀（如 `--color-primary-6`）；本文档统一用无前缀形式描述
> **gray 色板说明**：10 阶为**纯灰度色阶（R=G=B，零色偏）**，已从原 Arco Design 偏蓝中性灰校正为真正灰度。亮度梯度贴近原值，暗色主题为同色阶反向映射。

---

## 1. 色板系统（13 个基础色板 × 10 阶）

每个色板 10 级（1 最浅 → 10 最深），**6 级为基准色**，1–5 为浅色梯度（hover/light 背景），7–10 为深色梯度（active/按下）。色值经源启官方 palette 算法生成。

### 1.1 亮色模式色板

| 色板 | -1 | -2 | -3 | -4 | -5 | **-6** | -7 | -8 | -9 | -10 |
|------|----|----|----|----|----|----|----|----|----|-----|
| **giencoderblue 弧蓝** | #F5F8FF | #DAE4FE | #B4C9FC | #8EAEFA | #6692F9 | **#3770F7** | #346AE9 | #2E5ECE | #2851B4 | #22469A |
| **red 红** | #FFECE8 | #FDC5C5 | #FBACA3 | #F98981 | #F76560 | **#F53F3F** | #CB272D | #A1151E | #770813 | #4D000A |
| **green 绿** | #ECF7EC | #D0F0D1 | #A4E0A7 | #7DD182 | #5AC262 | **#3BB346** | #30953B | #25772F | #1B5924 | #113C18 |
| **orange 橙** | #FFF7E8 | #FFE4BA | #FFCF8B | #FFB65D | #FF9A2E | **#FF7D00** | #D25F00 | #A64500 | #792E00 | #4D1B00 |
| **yellow 黄** | #FEFFE8 | #FEFEBE | #FDFA94 | #FCF26B | #FBE842 | **#FADC19** | #CFAF0F | #A38408 | #785D03 | #4D3800 |
| **gold 金** | #FFFCE8 | #FDF4BF | #FCE996 | #FADC6D | #F9CC45 | **#F7BA1E** | #CC9213 | #A26D0A | #774B04 | #4D2D00 |
| **purple 紫** | #F5E8FF | #DDBEF6 | #C396ED | #A871E3 | #8D4EDA | **#722ED1** | #551DB0 | #3C108F | #27066E | #16004D |
| **pinkpurple 粉紫** | #FFE8FB | #F7BAEF | #F08EE6 | #E865DF | #E13EDB | **#D91AD9** | #B010B6 | #8A0993 | #650370 | #42004D |
| **magenta 品红** | #FFE8F1 | #FDC2DB | #FB9DC7 | #F979B7 | #F754A8 | **#F5319D** | #CB1E83 | #A11069 | #77064F | #4D0034 |
| **cyan 青** | #E8FFFB | #B7F4EC | #89E9E0 | #5EDFD6 | #37D4CF | **#14C9C9** | #0DA5AA | #07828B | #03616C | #00424D |
| **blue 蓝** | #E8F7FF | #C3E7FE | #9FD4FD | #7BC0FC | #57A9FB | **#3491FA** | #206CCF | #114BA3 | #063078 | #001A4D |
| **lime 青柠** | #FCFFE8 | #EDF8BB | #DCF190 | #C9E968 | #B5E241 | **#9FDB1D** | #7EB712 | #5F940A | #437004 | #2A4D00 |
| **gray 灰** | #F7F7F7 | #F2F2F2 | #E5E5E5 | #C9C9C9 | #A9A9A9 | **#868686** | #6B6B6B | #4E4E4E | #2B2B2B | #1F1F1F |

### 1.2 暗色模式色板（[giencoder-theme='dark']）

暗色模式色阶采用官方暗色 Blue 色阶算法生成（非简单反转），-1 最深 → -10 最浅。以 giencoderblue 为例：`--giencoderblue-1: #052670` … `--giencoderblue-10: #EFF6FF`。

| 色板 | -1 | -2 | -3 | -4 | -5 | -6 | -7 | -8 | -9 | -10 |
|------|----|----|----|----|----|----|----|----|----|-----|
| **gray 灰** | #1F1F1F | #2B2B2B | #4E4E4E | #6B6B6B | #868686 | #A9A9A9 | #C9C9C9 | #E5E5E5 | #F2F2F2 | #F7F7F7 |

> 其余 12 个彩色板暗色值：色阶反转，-1 ≈ 亮色 -10，-10 ≈ 亮色 -1（例：red 暗色 -1 #4D000A → -10 #FFF0EC）。完整 RGB 值见 `colors_and_type.css` 暗色段。

---

## 2. 语义色（Semantic Colors）

### 2.1 功能色（映射到基础色板）

| 语义 | 基准(-6) | 映射 | 说明 |
|------|----------|------|------|
| **primary 主色** | #3770F7 | giencoderblue-6 | 全局主操作色（按钮、选中态、链接） |
| **success 成功** | #3BB346 | green-6 | 正向反馈 |
| **warning 警告** | #FF7D00 | orange-6 | 警示信息 |
| **danger 危险** | #F53F3F | red-6 | 错误/删除等危险操作 |
| **link 链接** | #3770F7 | giencoderblue-6 | 文本链接 |

每个功能色有 10 级色阶（`--color-primary-1..10` 等）+ 4 级浅色背景（`--color-primary-light-1..4`，用于选中底色/标签底色）。

### 2.2 中性色语义层（亮色模式）

| Token | 值 | 用途 |
|-------|-----|------|
| `--color-white` | #FFFFFF | 纯白 |
| `--color-black` | #000000 | 纯黑 |
| `--color-bg-1` | #FFFFFF | 整体页面背景 |
| `--color-bg-2` | #FFFFFF | 一级容器背景（卡片/内容区） |
| `--color-bg-3` | #FFFFFF | 二级容器背景 |
| `--color-bg-4` | #FFFFFF | 三级容器背景 |
| `--color-bg-5` | #FFFFFF | 浮层背景（下拉/Tooltip 面板） |
| `--color-bg-white` | #FFFFFF | Radio/Switch 等白色底 |
| `--color-bg-popup` | var(--color-bg-5) | 弹层背景 |
| `--color-text-1` | #1F1F1F (gray-10) | 标题、正文（最高层级文字） |
| `--color-text-2` | #4E4E4E (gray-8) | 语句（次级文字） |
| `--color-text-3` | #868686 (gray-6) | 次要信息（说明文字） |
| `--color-text-4` | #C9C9C9 (gray-4) | 禁用态文字 |
| `--color-fill-1` | #F7F7F7 (gray-1) | 填充-最浅（hover 底色） |
| `--color-fill-2` | #F2F2F2 (gray-2) | 填充-浅 |
| `--color-fill-3` | #E5E5E5 (gray-3) | 填充-中 |
| `--color-fill-4` | #C9C9C9 (gray-4) | 填充-深 |
| `--color-border-1` | #F2F2F2 (gray-2) | 边框-最浅（分割线） |
| `--color-border-2` | #E5E5E5 (gray-3) | 边框-浅（默认输入框边框） |
| `--color-border-3` | #C9C9C9 (gray-4) | 边框-中 |
| `--color-border-4` | #868686 (gray-6) | 边框-深 |
| `--color-secondary` | gray-2 | 次级按钮背景 |
| `--color-secondary-hover` | gray-3 | 次级按钮 hover |
| `--color-secondary-active` | gray-4 | 次级按钮 active |
| `--color-secondary-disabled` | gray-1 | 次级按钮禁用 |
| `--color-neutral-1..10` | gray-1..10 | 中性色阶别名 |

### 2.3 组件专用色

| Token | 值 | 用途 |
|-------|-----|------|
| `--color-tooltip-bg` | #1F1F1F (gray-10) | Tooltip 深色底 |
| `--color-spin-layer-bg` | rgba(255,255,255,0.6) | Spin 遮罩 |
| `--color-menu-dark-bg` | #232324 | 暗色菜单背景 |
| `--color-menu-light-bg` | #FFFFFF | 亮色菜单背景 |
| `--color-menu-dark-hover` | rgba(255,255,255,0.04) | 暗色菜单 hover |
| `--color-mask-bg` | rgba(31,31,31,0.6) | Modal/Drawer 遮罩（亮色） |
| `--color-data-1..20` | 多色板引用 | 图表/数据可视化配色序列（giencoderblue-5, red-5, orange-5, green-5, cyan-6, …） |

---

## 3. 字体（Typography）

### 3.1 字体族

```
--font-family: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans Backtick Fix",
  "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
--code-family: Consolas, Menlo;
--line-height-base: 1.5715;
--font-size-body: 14px;   /* 全局基准字号 */
```

### 3.2 字号层级（字体大小 + 对应行高）

| Token | 字号 | 典型用途 |
|-------|------|---------|
| `--font-size-display-3` | 56px | 大数字展示（数据大屏） |
| `--font-size-display-2` | 48px | 展示标题 |
| `--font-size-display-1` | 36px | 展示标题/大标题 |
| `--font-size-title-3` | 24px | 页面级大标题 |
| `--font-size-title-2` | 20px | 区块标题 |
| `--font-size-title-1` | 16px | 卡片标题/表单标题 |
| `--font-size-body-3` | 14px | **正文/默认**（按钮、输入框、表格） |
| `--font-size-body-2` | 13px | 次级正文 |
| `--font-size-body-1` | 12px | 辅助文字 |
| `--font-size-caption` | 12px | 说明/标注 |

### 3.3 字重

`--font-weight-100..900`（100/200/300/400/500/600/700/800/900）。常用：400 正文、500 强调、600 标题。

---

## 4. 间距（Spacing）

源启间距体系为 **2px 步进递增**（`--spacing-1: 2px` 起），高频使用 8px 倍数。

| Token | 值 | Token | 值 |
|-------|-----|-------|-----|
| `--spacing-none` | 0 | `--spacing-11` | 36px |
| `--spacing-1` | 2px | `--spacing-12` | 40px |
| `--spacing-2` | 4px | `--spacing-13` | 48px |
| `--spacing-3` | 6px | `--spacing-14` | 56px |
| `--spacing-4` | 8px | `--spacing-15` | 60px |
| `--spacing-5` | 10px | `--spacing-16` | 64px |
| `--spacing-6` | 12px | `--spacing-17` | 72px |
| `--spacing-7` | 16px | `--spacing-18` | 80px |
| `--spacing-8` | 20px | `--spacing-19` | 84px |
| `--spacing-9` | 24px | `--spacing-20` | 96px |
| `--spacing-10` | 32px | `--spacing-21/22` | 100px/120px |

**尺寸阶梯** `--size-1..29`：4px × n（4/8/12/16/20/24/28/32/36/40/…/116px），用于组件高度、图标尺寸等。

---

## 5. 圆角（Border Radius）

| Token | 值 | 用途 |
|-------|-----|------|
| `--border-radius-none` | 0 | 无圆角 |
| `--border-radius-small` | **2px** | 标签、小元素 |
| `--border-radius-medium` | **4px** | 按钮、输入框、卡片（默认） |
| `--border-radius-large` | **8px** | 弹窗、抽屉、大容器 |
| `--border-radius-xl` | **12px** | Modal 面板等更大容器（上游定制档） |
| `--border-radius-circle` | 50% | 圆形头像、圆形按钮 |

---

## 6. 阴影（Shadow）

三层阴影，每层 9 个方向变体（center/up/down/left/right/四角）；常用 down 变体。

| Token | 值 | 用途 |
|-------|-----|------|
| `--shadow-none` | none | 无阴影 |
| `--shadow-special` | 0 0 1px rgba(0,0,0,0.3) | 特殊细边 |
| `--shadow1-down` | 0 2px 5px rgba(0,0,0,0.1) | 轻微浮起（卡片、hover 提示） |
| `--shadow2-down` | 0 8px 20px rgba(31,41,55,0.10) | 下拉浮层投影（Select/Dropdown/Popover/Cascader 等） |
| `--shadow3-down` | 0 8px 20px rgba(0,0,0,0.1) | 强浮起（Modal、Drawer、Notification） |

方向变体：`--shadow{1-3}-{center|up|down|left|right|left-up|left-down|right-up|right-down}`。

---

## 7. 动效（Motion）

### 7.1 时长

| Token | 值 | 用途 |
|-------|-----|------|
| `--transition-duration-1` | 0.1s | 即时反馈（hover、按下） |
| `--transition-duration-2` | 0.2s | 默认过渡（面板展开、状态切换） |
| `--transition-duration-3` | 0.3s | 较大过渡（抽屉、Modal 出入场） |
| `--transition-duration-4` | 0.4s | 慢速过渡 |
| `--transition-duration-5` | 0.5s | 慢速演示 |
| `--transition-duration-loading` | 1s | 加载动画循环 |

### 7.2 缓动曲线

| Token | 曲线 | 用途 |
|-------|------|------|
| `--transition-timing-function-linear` | cubic-bezier(0,0,1,1) | 线性 |
| `--transition-timing-function-standard` | cubic-bezier(0.34,0.69,0.1,1) | **标准**（默认） |
| `--transition-timing-function-overshoot` | cubic-bezier(0.3,1.3,0.3,1) | 过冲（弹跳感） |
| `--transition-timing-function-decelerate` | cubic-bezier(0.4,0.8,0.74,1) | 减速（入场） |
| `--transition-timing-function-accelerate` | cubic-bezier(0.26,0,0.6,0.2) | 加速（退场） |
| `--transition-timing-function-spring` | cubic-bezier(0.34,1.56,0.64,1) | 弹性（弹层/浮层进入，过冲≈10%） |

---

## 8. 层级（Z-Index）

| Token | 值 | 用途 |
|-------|-----|------|
| `--z-index-affix` | 999 | 固钉 |
| `--z-index-popup` | 1000 | 弹层基准（下拉、Tooltip、Popover） |
| `--z-index-drawer` | 1001 | 抽屉 |
| `--z-index-modal` | 1001 | 对话框 |
| `--z-index-message` | 1003 | 全局消息 |
| `--z-index-notification` | 1003 | 通知提醒 |
| `--z-index-image-preview` | 1001 | 图片预览 |

---

## 9. 不透明度（Opacity）

`--opacity-none..10`：0% / 10% / 20% / 30% / 40% / 50% / 60% / 70% / 80% / 90% / 100%，用于遮罩与降级态。

---

## 10. Token 使用规则（硬规则）

1. **颜色禁止硬编码 hex**：一律使用语义变量（`--color-primary` 系列、`--color-text-*`、`--color-border-*`）；色阶（`--primary-6`、`--danger-6`）仅用于状态与品牌语境
2. **间距用 2px/8px 体系**：组件内边距、元素间距取 `--spacing-*`，不写魔法数字
3. **圆角分级**：按钮/输入框/卡片 4px（medium），弹窗/抽屉 8px（large），小标签 2px（small）
4. **动效统一**：hover/按下 0.1s、面板 0.2s、浮层出入 0.2–0.3s，曲线默认 standard
5. **暗色模式**：`body[giencoder-theme='dark']` 下语义变量自动切换，规范支持亮暗双模式
6. **语义优先**：先找语义层（bg/text/border/fill），再退到色阶，最后才允许直接引用基础色板（图表、品牌场景）

---

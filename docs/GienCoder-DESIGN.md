---
version: 3
name: "GienCoder Design System"
description: >-
  GienCoder 设计系统（GienCoder Design System）V3 规范 —— 面向中后台/B2B 产品的企业级设计语言与
  组件契约体系。本文件为机器可读 + AI 可执行的双重规范：YAML frontmatter 提供全部设计令牌
  （颜色 / 字体 / 圆角 / 间距 / 组件），正文提供页面生成与评审需遵循的确定性规则。
  基于 @giencoder-design/web-react@2.66.16 官方编译产物（es/style/theme + component contracts）。
assets:
  colorsCss: "giencoder/colors_and_type.css"     # 颜色/字体/圆角/间距/阴影/动效 CSS 变量（亮暗双主题）
  componentsCss: "giencoder/components.css"      # 核心组件样式实现（唯一 249 处 giencoder-* class，含重复出现共 473 次），48KB / 681 行
  registry: "giencoder/component-registry.json"  # 71 组件注册表
  contractsDir: "giencoder/components/"          # 组件契约（schemaVersion 3），每个组件一个 .json
  previewDir: "giencoder/preview/"               # 71 个可直接复制的组件 HTML 代码模板
  scaffoldCss: "giencoder/preview/preview-scaffold.css"  # preview 模板骨架样式
  deliveryDir: "giencoder-delivery/"             # 交付快照（与 giencoder/ 双目录同步）
usage:
  # AI 生成高保真页面时，必须优先复用以下现成资产，而非自由发挥样式细节：
  # 1) 先查 components/{slug}.json 契约确定组件结构/状态/令牌
  # 2) 从 giencoder/preview/component-{slug}.html 原样复制 HTML 骨架（只改文字/数据）
  # 3) class 一律用 giencoder-{component}-{part}-{modifier} 命名空间，禁止臆造变体
  # 4) 页面必须按序引入 colors_and_type.css → components.css（见 §8.7 引入片段）
  # 5) 样式细节冲突时以 giencoder/components.css 当前实现为准
colors:
  # ---- 13 个基础色板 × 10 阶（1 最浅 → 10 最深，6 为基准）----
  giencoderblue: ["#F5F8FF", "#DAE4FE", "#B4C9FC", "#8EAEFA", "#6692F9", "#3770F7", "#346AE9", "#2E5ECE", "#2851B4", "#22469A"]
  red:        ["#FFECE8", "#FDC5C5", "#FBACA3", "#F98981", "#F76560", "#F53F3F", "#CB272D", "#A1151E", "#770813", "#4D000A"]
  green:      ["#ECF7EC", "#D0F0D1", "#A4E0A7", "#7DD182", "#5AC262", "#3BB346", "#30953B", "#25772F", "#1B5924", "#113C18"]
  orange:     ["#FFF7E8", "#FFE4BA", "#FFCF8B", "#FFB65D", "#FF9A2E", "#FF7D00", "#D25F00", "#A64500", "#792E00", "#4D1B00"]
  yellow:     ["#FEFFE8", "#FEFEBE", "#FDFA94", "#FCF26B", "#FBE842", "#FADC19", "#CFAF0F", "#A38408", "#785D03", "#4D3800"]
  gold:       ["#FFFCE8", "#FDF4BF", "#FCE996", "#FADC6D", "#F9CC45", "#F7BA1E", "#CC9213", "#A26D0A", "#774B04", "#4D2D00"]
  purple:     ["#F5E8FF", "#DDBEF6", "#C396ED", "#A871E3", "#8D4EDA", "#722ED1", "#551DB0", "#3C108F", "#27066E", "#16004D"]
  pinkpurple: ["#FFE8FB", "#F7BAEF", "#F08EE6", "#E865DF", "#E13EDB", "#D91AD9", "#B010B6", "#8A0993", "#650370", "#42004D"]
  magenta:    ["#FFE8F1", "#FDC2DB", "#FB9DC7", "#F979B7", "#F754A8", "#F5319D", "#CB1E83", "#A11069", "#77064F", "#4D0034"]
  cyan:       ["#E8FFFB", "#B7F4EC", "#89E9E0", "#5EDFD6", "#37D4CF", "#14C9C9", "#0DA5AA", "#07828B", "#03616C", "#00424D"]
  blue:       ["#E8F7FF", "#C3E7FE", "#9FD4FD", "#7BC0FC", "#57A9FB", "#3491FA", "#206CCF", "#114BA3", "#063078", "#001A4D"]
  lime:       ["#FCFFE8", "#EDF8BB", "#DCF190", "#C9E968", "#B5E241", "#9FDB1D", "#7EB712", "#5F940A", "#437004", "#2A4D00"]
  gray:       ["#F7F7F7", "#F2F2F2", "#E5E5E5", "#C9C9C9", "#A9A9A9", "#868686", "#6B6B6B", "#4E4E4E", "#2B2B2B", "#1F1F1F"]
  # ---- Primary 状态映射（default=6，hover=5，active=7）----
  primary_default: "#3770F7"
  primary_hover:   "#6692F9"
  primary_active:  "#346AE9"
  primary_disabled: "text-4 on fill-2"   # 文字用 gray-4 #C9C9C9，底用 gray-2 #F2F2F2
  primary_light_1:  "#F5F8FF"             # 选中/标签底色
  primary_light_2:  "#DAE4FE"
  primary_light_3:  "#B4C9FC"
  primary_light_4:  "#8EAEFA"
  # ---- 功能色（基准 -6，hover -5，active -7）----
  success:  { default: "#3BB346", hover: "#5AC262", active: "#30953B", light_1: "#ECF7EC" }
  warning:  { default: "#FF7D00", hover: "#FF9A2E", active: "#D25F00", light_1: "#FFF7E8" }
  danger:   { default: "#F53F3F", hover: "#F76560", active: "#CB272D", light_1: "#FFECE8" }
  link:     { default: "#3770F7", hover: "#6692F9" }
  # ---- 四级文字 ----
  text_1: "#1F1F1F"   # 标题、正文（最高层级）
  text_2: "#4E4E4E"   # 语句（次级）
  text_3: "#868686"   # 次要/说明
  text_4: "#C9C9C9"   # 禁用态
  # ---- 四级填充 ----
  fill_1: "#F7F7F7"   # hover 底色
  fill_2: "#F2F2F2"   # 浅填充
  fill_3: "#E5E5E5"   # 中填充
  fill_4: "#C9C9C9"   # 深填充
  # ---- 四级边框 ----
  border_1: "#F2F2F2" # 分割线
  border_2: "#E5E5E5" # 默认输入框边框
  border_3: "#C9C9C9" # 中
  border_4: "#868686" # 深
  # ---- 页面 / 容器 / 浮层 / 遮罩 / Tooltip ----
  bg_page: "#FFFFFF"          # bg-1 整体页面背景
  bg_container_1: "#FFFFFF"   # bg-2 卡片/内容区
  bg_container_2: "#FFFFFF"   # bg-3 二级容器
  bg_container_3: "#FFFFFF"   # bg-4 三级容器
  bg_popup:      "#FFFFFF"    # bg-5 / bg-popup 下拉、Tooltip 面板
  bg_white:      "#FFFFFF"    # Radio/Switch 白色底
  mask:          "rgba(31,31,31,0.6)"       # 亮色 Modal/Drawer 遮罩
  tooltip_bg:    "#1F1F1F"    # Tooltip 深色底
  tooltip_text:  "#FFFFFF"
  spin_layer:    "rgba(255,255,255,0.6)"    # 亮色 Spin 遮罩
  # ---- 数据可视化色（图表序列，20 档）----
  data: ["#6692F9", "#F76560", "#FF9A2E", "#5AC262", "#14C9C9", "#722ED1", "#F7BA1E", "#F5319D", "#D91AD9", "#9FDB1D", "#3491FA", "#2E2E30", "#A1151E", "#A64500", "#25772F", "#07828B", "#8D4EDA", "#CC9213", "#A11069", "#5F940A"]
  # ---- 暗色主题 ----
  dark:
    bg_1: "#17171A"
    bg_2: "#232324"
    bg_3: "#2E2E30"
    bg_4: "#484849"
    bg_5: "#5F5F60"
    bg_white: "#F6F6F6"
    text_1: "#F7F7F7"
    text_2: "#E5E5E5"
    text_3: "#A9A9A9"
    text_4: "#6B6B6B"
    fill_1: "#1F1F1F"
    fill_2: "#2B2B2B"
    fill_3: "#4E4E4E"
    fill_4: "#6B6B6B"
    border_1: "#2B2B2B"
    border_2: "#4E4E4E"
    border_3: "#6B6B6B"
    border_4: "#A9A9A9"
    mask:      "rgba(0,0,0,0.6)"
    primary_6: "#5497FF"      # 暗色弧蓝基准
    menu_bg:   "#232324"
typography:
  fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'noto sans', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif"
  codeFamily: "Consolas, Menlo, monospace"
  lineHeightBase: 1.5715
  fontSizeBase: "14px"
  # ---- 层阶：size / weight / lineHeight / letterSpacing ----
  display_3: { fontSize: "56px", fontWeight: 600, lineHeight: 1.2,  letterSpacing: "-0.02em" }
  display_2: { fontSize: "48px", fontWeight: 600, lineHeight: 1.25, letterSpacing: "-0.02em" }
  display_1: { fontSize: "36px", fontWeight: 600, lineHeight: 1.3,  letterSpacing: "-0.02em" }
  title_3:   { fontSize: "24px", fontWeight: 600, lineHeight: 1.33, letterSpacing: "0" }
  title_2:   { fontSize: "20px", fontWeight: 600, lineHeight: 1.4,  letterSpacing: "0" }
  title_1:   { fontSize: "16px", fontWeight: 600, lineHeight: 1.5,  letterSpacing: "0" }
  body_3:    { fontSize: "14px", fontWeight: 400, lineHeight: 1.5715, letterSpacing: "0.01em" }
  body_2:    { fontSize: "13px", fontWeight: 400, lineHeight: 1.5715, letterSpacing: "0.01em" }
  body_1:    { fontSize: "12px", fontWeight: 400, lineHeight: 1.5715, letterSpacing: "0.01em" }
  caption:   { fontSize: "12px", fontWeight: 400, lineHeight: 1.5, letterSpacing: "0.02em", color: "#868686" }
  button:    { fontSize: "14px", fontWeight: 500, lineHeight: 1.5715, letterSpacing: "0.01em" }
  code:      { fontFamily: "Consolas, Menlo, monospace", fontSize: "13px", fontWeight: 400, lineHeight: 1.5715 }
  fontWeight: { light: 300, regular: 400, medium: 500, semibold: 600, bold: 700 }
rounded:
  none:   "0"
  small:  "2px"    # 标签、小元素
  medium: "4px"    # 按钮、输入框、卡片（默认）
  large:  "8px"    # 弹窗、抽屉、大容器
  circle: "50%"    # 圆形头像、开关、圆形按钮
spacing:
  none: "0"
  1: "2px"
  2: "4px"
  3: "6px"
  4: "8px"
  5: "10px"
  6: "12px"
  7: "16px"
  8: "20px"
  9: "24px"
  10: "32px"
  11: "36px"
  12: "40px"
  13: "48px"
  14: "56px"
  15: "60px"
  16: "64px"
  17: "72px"
  18: "80px"
  19: "84px"
  20: "96px"
  21: "100px"
  22: "120px"
components:
  # ===== 通用 =====
  button_panel:
    height_default: "32px"
    heights: { mini: "24px", small: "28px", medium: "32px", large: "36px" }
    borderRadius: "{rounded.medium}"      # 4px
    primary:      { backgroundColor: "{colors.primary_default}", textColor: "#FFFFFF", hoverBackgroundColor: "{colors.primary_hover}", activeBackgroundColor: "{colors.primary_active}" }
    secondary:    { backgroundColor: "{colors.bg_white}", textColor: "{colors.text_1}", borderColor: "{colors.border_2}", shadow: "0 1px 2px rgba(15,23,42,0.04)" }
    outline:      { backgroundColor: "transparent", textColor: "{colors.primary_default}", borderColor: "{colors.primary_default}" }
    dashed:       { backgroundColor: "transparent", textColor: "{colors.text_1}", borderStyle: "dashed", borderColor: "{colors.border_3}" }
    text:         { backgroundColor: "transparent", textColor: "{colors.primary_default}" }
    danger:       { backgroundColor: "{colors.danger.default}", textColor: "#FFFFFF", hoverBackgroundColor: "{colors.danger.hover}", activeBackgroundColor: "{colors.danger.active}" }
    disabled:     { textColor: "{colors.text_4}", backgroundColor: "{colors.fill_2}", borderColor: "transparent" }
    paddingInline: "15px"
  typography: { role: "文本排版容器" }
  divider:    { role: "分割线", color: "{colors.border_1}" }
  grid:       { role: "栅格", cols: 24 }
  space:      { role: "间距容器" }
  link:       { role: "链接", defaultColor: "{colors.link.default}", hoverColor: "{colors.link.hover}" }
  # ===== 布局 =====
  layout:
    header_height: "48px"
    sider_width: "200px"
    sider_width_collapsed: "48px"
    content_padding: "20px"
    content_bg: "{colors.bg_page}"
  # ===== 导航 =====
  menu:
    selected_text: "{colors.primary_default}"
    light_bg: "{colors.bg_page}"
    dark_bg: "{colors.dark.menu_bg}"  # #232324
  tabs:
    line_active_color: "{colors.primary_default}"
    card_height: "36px"
  pagination:
    heights: { mini: "24px", small: "28px", default: "32px", large: "36px" }
    borderRadius: "{rounded.small}"
  breadcrumb: { linkColor: "{colors.link.default}", currentText: "{colors.text_1}", separator: "{colors.text_3}" }
  page_header: { titleSize: "{typography.title_2}", titleColor: "{colors.text_1}", bg: "{colors.bg_container_1}" }
  # ===== 数据录入 =====
  input:
    heights: { mini: "24px", small: "28px", medium: "32px", large: "36px" }
    borderColor: "{colors.border_2}"
    hoverBorder: "{colors.border_3}"
    errorBorder: "{colors.danger.default}"
    disabledBg: "{colors.fill_2}"
    textColor: "{colors.text_1}"
    placeholder: "{colors.text_3}"
    borderRadius: "{rounded.medium}"
  select:
    heights: { mini: "24px", small: "28px", medium: "32px", large: "36px" }
    dropdownBg: "{colors.bg_popup}"
    dropdownShadow: "shadow2-down"
    borderColor: "{colors.border_2}"
    borderRadius: "{rounded.medium}"
  checkbox:
    boxSize: "16px"
    labelSize: "14px"
    checkedColor: "{colors.primary_default}"
  radio:
    heights: { mini: "24px", small: "28px", medium: "32px", large: "36px" }
    checkedColor: "{colors.primary_default}"
  switch:
    sizes: { small: "28 × 16px", default: "40 × 22px" }
    onColor: "{colors.primary_default}"
    offColor: "{colors.fill_3}"
  form:
    layout: ["horizontal", "vertical", "inline"]
    controlHeights: { mini: "24px", small: "28px", medium: "32px", large: "36px" }
    errorColor: "{colors.danger.default}"
  # ===== 数据展示 =====
  card:
    bg: "{colors.bg_container_1}"
    borderColor: "{colors.border_2}"
    radius: "{rounded.medium}"
    defaultShadow: "shadow1-down"
    hoverShadow: "shadow2-down"
  table:
    rowHeight: "40px"
    headerBg: "{colors.bg_container_1}"
    headerText: "{colors.text_2}"
    rowBg: "#FFFFFF"
    borderColor: "{colors.border_1}"
    hoverRowBg: "{colors.fill_1}"
    selectedRowBg: "{colors.primary_light_1}"
    fontSize: "{typography.body_3}"
  tag:
    sizes: { small: {h: "20px", size: "12px"}, default: {h: "24px", size: "14px"}, large: {h: "28px", size: "14px"} }
    borderRadius: "{rounded.medium}"
  empty: { textColor: "{colors.text_3}" }
  skeleton: { bg: "{colors.fill_2}", highlight: "{colors.fill_1}", radius: "{rounded.small}" }
  progress:
    heights: { line: "8px", circle_mini: "60px", circle_small: "80px", circle_default: "100px", circle_large: "120px" }
    trackColor: "{colors.fill_2}"
    primary: "{colors.primary_default}"
  # ===== 反馈 =====
  message:   { bg: "{colors.bg_popup}", shadow: "shadow2-down", radius: "{rounded.small}", zIndex: 1003 }
  notification: { width: "300px", bg: "{colors.bg_container_1}", shadow: "shadow3-down", radius: "{rounded.medium}", zIndex: 1003 }
  alert:     { textColor: "{colors.text_1}", radius: "{rounded.small}" }
  tooltip:   { bg: "{colors.tooltip_bg}", textColor: "#FFFFFF", radius: "{rounded.medium}", zIndex: 1000, maxWidth: "320px" }
  popover:   { bg: "{colors.bg_popup}", shadow: "shadow2-down", radius: "{rounded.medium}", zIndex: 1000 }
  modal:     { widthDefault: "520px", widthSimple: "464px", bg: "{colors.bg_container_1}", mask: "{colors.mask}", shadow: "shadow3-down", radius: "{rounded.medium}", padding: "20/24px", zIndex: 1001 }
  drawer:    { bg: "{colors.bg_container_1}", mask: "{colors.mask}", shadow: "shadow3-down", radius: "{rounded.large}", zIndex: 1001 }
  # ===== 组件样式锚点（AI 生成页面必须复用的 class 命名空间）=====
  # class 一律为 giencoder-{component}-{part}-{modifier}；实现见 giencoder/components.css
  # 每个组件完整代码模板见 giencoder/preview/component-{slug}.html
  componentStyles:
    Button:       { class: "giencoder-btn",          variants: ["-primary","-secondary","-outline","-dashed","-text","-danger","-disabled","-loading"], sizes: ["-size-mini","-size-small","-size-default","-size-large"], preview: "component-button.html", cssRef: "{assets.componentsCss}" }
    Input:        { class: "giencoder-input",        variants: ["-wrapper","-prefix","-suffix","-error","-disabled","-clear-btn"], preview: "component-input.html", cssRef: "{assets.componentsCss}" }
    Checkbox:     { class: "giencoder-checkbox",     variants: ["-checked","-indeterminate","-disabled"], preview: "component-checkbox.html", cssRef: "{assets.componentsCss}" }
    Radio:        { class: "giencoder-radio",        variants: [], preview: "component-radio.html", cssRef: "{assets.componentsCss}" }
    Switch:       { class: "giencoder-switch",       variants: [], preview: "component-switch.html", cssRef: "{assets.componentsCss}" }
    Form:         { class: "giencoder-form",         variants: [], preview: "component-form.html", cssRef: "{assets.componentsCss}" }
    Select:       { class: "giencoder-select",       variants: [], preview: "component-select.html", cssRef: "{assets.componentsCss}" }
    Tag:          { class: "giencoder-tag",          variants: [], preview: "component-tag.html", cssRef: "{assets.componentsCss}" }
    Tabs:         { class: "giencoder-tabs",         variants: [], preview: "component-tabs.html", cssRef: "{assets.componentsCss}" }
    Pagination:   { class: "giencoder-pagination",   variants: [], preview: "component-pagination.html", cssRef: "{assets.componentsCss}" }
    Menu:         { class: "giencoder-menu",         variants: [], preview: "component-menu.html", cssRef: "{assets.componentsCss}" }
    Breadcrumb:   { class: "giencoder-breadcrumb",   variants: ["-item","-item-current","-item-link","-item-separator"], preview: "component-breadcrumb.html", cssRef: "{assets.componentsCss}" }
    PageHeader:   { class: "giencoder-page-header",  variants: [], preview: "component-page-header.html", cssRef: "{assets.componentsCss}" }
    Card:         { class: "giencoder-card",         variants: ["-header","-body","-hoverable"], preview: "component-card.html", cssRef: "{assets.componentsCss}" }
    Table:        { class: "giencoder-table",        variants: ["-container","-content","-th","-td","-tr","-tr-checked","-sorter","-checkbox"], preview: "component-table.html", cssRef: "{assets.componentsCss}" }
    Message:      { class: "giencoder-message",      variants: ["-close-btn"], preview: "component-message.html", cssRef: "{assets.componentsCss}" }
    Notification: { class: "giencoder-notification", variants: [], preview: "component-notification.html", cssRef: "{assets.componentsCss}" }
    Alert:        { class: "giencoder-alert",        variants: ["-title","-description","-icon","-action","-close-btn","-info","-success","-warning","-error"], preview: "component-alert.html", cssRef: "{assets.componentsCss}" }
    Tooltip:      { class: "giencoder-tooltip",      variants: [], preview: "component-tooltip.html", cssRef: "{assets.componentsCss}" }
    Popover:      { class: "giencoder-popover",      variants: [], preview: "component-popover.html", cssRef: "{assets.componentsCss}" }
    Modal:        { class: "giencoder-modal",        variants: ["-mask","-header","-title","-content","-footer","-close-btn"], preview: "component-modal.html", cssRef: "{assets.componentsCss}" }
    Drawer:       { class: "giencoder-drawer",       variants: [], preview: "component-drawer.html", cssRef: "{assets.componentsCss}" }
    Progress:     { class: "giencoder-progress",     variants: [], preview: "component-progress.html", cssRef: "{assets.componentsCss}" }
    Skeleton:     { class: "giencoder-skeleton",     variants: [], preview: "component-skeleton.html", cssRef: "{assets.componentsCss}" }
    Empty:        { class: "giencoder-empty",        variants: [], preview: "component-empty.html", cssRef: "{assets.componentsCss}" }
    Avatar:       { class: "giencoder-avatar",       variants: ["-group"], preview: "component-avatar.html", cssRef: "{assets.componentsCss}" }
    Badge:        { class: "giencoder-badge",        variants: ["-count","-dot","-status","-status-success","-status-danger","-status-warning"], preview: "component-badge.html", cssRef: "{assets.componentsCss}" }
    Dropdown:     { class: "giencoder-dropdown",     variants: [], preview: "component-dropdown.html", cssRef: "{assets.componentsCss}" }
---

# GienCoder Design System — 机器可读 + AI 可执行设计规范（V3）

> 版本：**v3**（设计 Token 规范版）｜ 底层实现：`@giencoder-design/web-react@2.66.16`（`es/style/theme` 官方编译产物）
> 权威源：本仓库 `giencoder/tokens.md`、`giencoder/colors_and_type.css`、`giencoder/component-registry.json`、`giencoder/components/*.json`、`giencoder/patterns.md`、`giencoder/a11y.md`、`giencoder/SKILL.md`
> 关系：本文档是本仓库 `Design Token 规范 v3` 的**机器可解析导出**，与源码保持同一份事实；如与历史/第三方资料冲突，一律以当前源码为准（见 [13. Known Gaps](#12-known-gaps)）。

---

## 1. Overview

**GienCoder Design System（GienCoder 设计系统）** 是一套面向 **中后台 / B2B / 企业级 SaaS** 产品的企业级组件与设计语言体系，由底层 `@giencoder-design/web-react` 提供 71 个组件契约，覆盖通用、布局、导航、数据录入、数据展示、反馈、其他七大分类。其设计语境是：**数据密集、操作高频、任务明确的业务工作台** —— 例如研发协同空间、审批列表、数据看板、配置后台等。

四项核心价值：

| 价值 | 含义（对 AI 生成的约束） |
|------|--------------------------|
| **Clear（清晰）** | 信息层级一目了然：标题 → 正文 → 说明四级文字；状态用色语义化；表头/行/选中态对比度达标。不堆叠装饰。 |
| **Consistent（一致）** | 组件只认 `giencoder-*` 官方 class 与 Token；同一颜色、圆角、间距、动效全站统一；禁止混用旧 class 或臆造变体。 |
| **Rhythmic（节奏）** | 间距严格走 2px/8px 体系（`--spacing-*`），区块间距 16–24px；24 栏栅格布局；空白有规律、可预见。 |
| **Open（开放）** | 组件支持代理/扩展（可通过 props 定制、可组合成六大页面模式），但扩展不破坏既有契约；鼓励组合而非发明。 |

**语义优先原则（硬规则）**：颜色一律引用语义层（`bg/text/border/fill` 系列）→ 缺省再退到功能色/色阶 → 最后才允许直接引用基础色板（仅图表、品牌场景）。禁止硬编码 hex。

所有尺寸、间距、圆角、阴影、动效、层级均有对应 Token，见 YAML frontmatter。正文以下用 `{colors.primary_default}` / `{typography.body_3}` / `{rounded.medium}` / `{components.button_panel}` 的形式引用令牌，**每个正文引用都能在 YAML 中找到对应定义**（本章说明性的四类泛称 `{colors.}` / `{typography.}` / `{rounded.}` / `{components.}` 仅为名称空间前缀，不作为实际引用）。

---

## 2. Colors

### 2.1 主色（GienCoder Blue / 弧蓝）

基准色为 **6 级** `{colors.primary_default}` = **#3770F7**。状态映射（不是罗列色值，是"什么状态用哪一级"）：

| 状态 | 令牌 | 值 | 规则 |
|------|------|-----|------|
| Default | `--color-primary-6` | #3770F7 | 全局主操作（主按钮、选中、链接） |
| Hover | `--color-primary-5` | #6692F9 | 指针悬停，主色向浅档过渡 |
| Active | `--color-primary-7` | #346AE9 | 按下瞬间，主色向深档过渡 |
| Disabled | 文字 `--color-text-4` + 底 `--color-fill-2` | #C9C9C9 / #F2F2F2 | 禁用态，不使用彩色 |
| Light | `--color-primary-light-1..4` | #F5F8FF … #8EAEFA | 选中底色 / 标签底色 / 按压浅底 |

### 2.2 功能色（Success / Warning / Danger / Link）

各功能色遵循「基准 -6、hover -5、active -7」同构映射（详见 YAML `colors.` 下 success/warning/danger/link 对象）：

| 语义 | Default | Hover | Active | Light-1 |
|------|---------|-------|--------|---------|
| Success（成功的正向反馈） | #3BB346 | #5AC262 | #30953B | #ECF7EC |
| Warning（警示需留意） | #FF7D00 | #FF9A2E | #D25F00 | #FFF7E8 |
| Danger（错误/删除） | #F53F3F | #F76560 | #CB272D | #FFECE8 |
| Link（文本链接） | #3770F7 | #6692F9 | — | — |

### 2.3 中性色语义层

- **四级文字**（由深到浅）：`{colors.text_1}` 标题/正文 → `{colors.text_2}` 次级 → `{colors.text_3}` 说明 → `{colors.text_4}` 禁用。
- **四级填充**（由浅到深）：`{colors.fill_1}` hover 底 → `{colors.fill_2}` 浅 → `{colors.fill_3}` 中 → `{colors.fill_4}` 深。
- **四级边框**：`{colors.border_1}` 分割线 → `{colors.border_2}` 默认输入框 → `{colors.border_3}` 中 → `{colors.border_4}` 深。
- **页面/容器/浮层/遮罩/Tooltip**：页面 `{colors.bg_page}`、一级容器 `{colors.bg_container_1}`、二级 `{colors.bg_container_2}`、三级 `{colors.bg_container_3}`、浮层 `{colors.bg_popup}`、遮罩 `{colors.mask}`、Tooltip 底 `{colors.tooltip_bg}`（深 #1F1F1F）+ 白字 `{colors.tooltip_text}`。

### 2.4 数据可视化色

图表系列色 `{colors.data}`（20 档）以 `giencoderblue-5, red-5, orange-5, green-5, cyan-6, purple-6 …` 依色板序列生成。规则：**同图系列色一致、跨图保持一致**；看板图表统一用 `--color-data-1..20`，不擅自取无关品牌色。参见 `patterns.md §5`。

### 2.5 暗色主题

通过 `body[giencoder-theme='dark']`（或任意 `[giencoder-theme='dark']` 容器）自动切换。暗色语义映射见 YAML `colors.dark`：页面 `#17171A`、容器一级 `#232324` → 五级 `#5F5F60`、文字一级 `#F7F7F7`（近似白）→ 四级 `#6B6B6B`、边框 `#2B2B2B → #A9A9A9`、遮罩 `rgba(0,0,0,0.6)`、主色基准 `#5497FF`。规范要求亮暗双模式均可用；生成页面时若含暗色，需同步覆盖全部语义变量。

**对比度约定（a11y.md §1）**：正文/图标与背景 ≥ 4.5:1；大字号（≥24px）或粗体 ≥ 3:1；输入框边框 ≥ 3:1；焦点环 ≥ 3:1。`text_3`(#868686) ≈ 3.24:1 仅限次要信息（连 3:1 大字号基线都未达，页面内只作**装饰性/非必要文字**使用，不作可读正文）；`text_4` 为禁用态豁免。功能色主按钮白字对比度见 §2.4 / Known Gaps #8 说明：`danger.default`(#F53F3F) 对白字 3.71:1、`primary.default`(#3770F7) 对白字 4.36:1，前者不达 AA 正文标准，高风险语义按钮需按 Known Gaps #8 的例外处理。

---

## 3. Typography

> 源码字体栈与层级见 YAML `typography.*`。基准正文 **14px**，行高基准 `lineHeightBase` = **1.5715**。中文优先 `PingFang SC / Hiragino Sans GB / noto sans / Microsoft YaHei`，西文优先 `Inter`，代码用 `Consolas / Menlo`。

| 角色 | Token | fontSize | fontWeight | lineHeight | letterSpacing | 典型用途 |
|------|-------|----------|-----------|------------|---------------|----------|
| Display-3 | `{typography.display_3}` | 56px | 600 | 1.2 | -0.02em | 数据大屏大数字 |
| Display-2 | `{typography.display_2}` | 48px | 600 | 1.25 | -0.02em | 展示标题 |
| Display-1 | `{typography.display_1}` | 36px | 600 | 1.3 | -0.02em | 大标题 |
| Heading/Title-3 | `{typography.title_3}` | 24px | 600 | 1.33 | 0 | 页面级大标题 |
| Heading/Title-2 | `{typography.title_2}` | 20px | 600 | 1.4 | 0 | 区块标题（PageHeader） |
| Heading/Title-1 | `{typography.title_1}` | 16px | 600 | 1.5 | 0 | 卡片/表单标题 |
| Body-3（正文默认） | `{typography.body_3}` | 14px | 400 | 1.5715 | 0.01em | 按钮/输入框/表格正文 |
| Body-2 | `{typography.body_2}` | 13px | 400 | 1.5715 | 0.01em | 次级正文 |
| Body-1 | `{typography.body_1}` | 12px | 400 | 1.5715 | 0.01em | 辅助文字 |
| Caption | `{typography.caption}` | 12px | 400 | 1.5 | 0.02em | 说明/标注（text_3） |
| Button | `{typography.button}` | 14px | 500 | 1.5715 | 0.01em | 按钮文字 |
| Code | `{typography.code}` | 13px | 400 | 1.5715 | — | 代码/标识符 |

字重表 `{typography.fontWeight}`：300/400/500/600/700（light/regular/medium/semibold/bold）。规则：正文 400、强调用 500、标题 600；标题建议用粗体而非斜体（对齐代码风格偏好）。

---

## 4. Layout

### 4.1 后台骨架

配色 `{components.layout}`：

```
┌──────────────────────────────────────────┐
│ Layout.Header（高 48px，通栏，shadow1）   │
├──────────┬───────────────────────────────┤
│ Sider    │  Content                      │
│ 200px    │  内边距 20px，overflow-y auto  │
│ Menu 纵向 │  区块间距 16–24px，24 栏栅格  │
│ 折叠 48px │                               │
├──────────┴───────────────────────────────┤
│ Layout.Footer（可选）                     │
└──────────────────────────────────────────┘
```

Header 用 `--color-bg-2` + 底 `--shadow1-down`；Sider 宽 200px（可折叠 48px 仅图标），亮色底 `--color-menu-light-bg`；Content `--color-bg-1`，内边距 `--spacing-8`(20px)，区块间 `--spacing-6`~`--spacing-9`(12–24px)。

### 4.2 24 栏栅格

Form 的 `labelCol`/`wrapperCol` 与看板图表区均基于 **24 列栅格**。栅格由 `{components.grid}` 表达。规则：
- 表单双列常用 `labelCol=8 / wrapperCol=16` 或等价 24 分栏；
- 看板图表 Card 按 24 列切分（如 2×12、3×8、1×24），保持块间间距一致。

### 4.3 六大页面模式

页面 = 骨架 + 区块（Card/PageHeader/Table/Form…）+ 状态（空/错/载）+ 反馈（Modal/Drawer/Message…）。见 `patterns.md` 与 [8. Components](#8-components) 里的模式清单（列表/详情/表单/看板/配置/结果）。

---

## 5. Elevation & Depth

三层阴影，每层 9 个方向变体（center/up/down/left/right/四角），常用 **down**：

| 令牌 | 值 | 用途 |
|------|-----|------|
| `--shadow-none` | none | 无阴影 |
| `--shadow-special` | 0 0 1px rgba(0,0,0,0.3) | 细强调边 |
| `--shadow1-down` | 0 2px 5px rgba(0,0,0,0.1) | 轻微浮起：卡片默认、hover 提示 |
| `--shadow2-down` | 0 8px 20px rgba(31,41,55,0.10) | 下拉浮层投影：Select/Dropdown/Popover/Cascader 等 |
| `--shadow3-down` | 0 8px 20px rgba(0,0,0,0.1) | 强浮起：Modal、Drawer、Notification |

方向变体范式：`shadow{1-3}-{center|up|down|left|right|left-up|left-down|right-up|right-down}`。层级（z-index）：Affix 999 < Popup/Tooltip/Popover 1000 < Drawer/Modal/ImagePreview 1001 < Message/Notification 1003。

使用规则（patterns.md §8）：
- 内容 **< 1 屏** 用 Modal，**≥ 1 屏** 用 Drawer；
- 全局成功提示用 `Message.success`（短、2–3s 自动消失）；全局错误带详情用 `Notification.error`（可关闭）；
- 破坏性操作必须 `Popconfirm` 二次确认；
- 局部 hover 纯文字说明用 `Tooltip`，带操作/富内容用 `Popover`。

---

## 6. Shapes

圆角分级（`rounded.*`）：

| 令牌 | 值 | 用法 |
|------|-----|------|
| none | 0 | 无圆角（banner 公告） |
| small | 2px | 标签、Message、小元素 |
| **medium** | **4px** | **按钮、输入框、卡片、Modal（默认）** |
| large | 8px | 弹窗/抽屉/大容器（Drawer 用 large） |
| circle | 50% | 圆形头像、开关、圆形按钮 |

对齐 tokens.md Token 使用规则 #3：按钮/输入框/卡片 = medium(4px)，弹窗/抽屉 = large(8px)，小标签 = small(2px)。

---

## 7. Motion

### 7.1 时长

| 令牌 | 值 | 用途 |
|------|-----|------|
| `--transition-duration-1` | 0.1s | 即时反馈（hover、按下） |
| `--transition-duration-2` | 0.2s | 默认过渡（面板展开、状态切换） |
| `--transition-duration-3` | 0.3s | 较大过渡（抽屉、Modal 出入场） |
| `--transition-duration-4` | 0.4s | 慢速过渡 |
| `--transition-duration-5` | 0.5s | 慢速演示 |
| `--transition-duration-loading` | 1s | 加载动画循环 |

### 7.2 缓动曲线

| 令牌 | 曲线 | 用途 |
|------|------|------|
| linear | cubic-bezier(0,0,1,1) | 线性 |
| **standard** | cubic-bezier(0.34,0.69,0.1,1) | **标准（默认）** |
| overshoot | cubic-bezier(0.3,1.3,0.3,1) | 过冲（弹跳感） |
| spring | cubic-bezier(0.34,1.56,0.64,1) | 弹性（弹层/浮层进入，过冲≈10%） |
| decelerate | cubic-bezier(0.4,0.8,0.74,1) | 减速（入场） |
| accelerate | cubic-bezier(0.26,0,0.6,0.2) | 加速（退场） |

规则：hover/按下 0.1s、面板 0.2s、浮层出入 0.2–0.3s，曲线默认 standard；所有动效 ≤ 0.5s，闪烁 ≤ 3 次/秒，并尊重 `prefers-reduced-motion`（a11y.md §6）。**动效走 CSS transition，禁止 `display` 硬切换**（SKILL.md / preview-format.md）。

---

## 8. Components

> 每个核心组件给出 bg / text / border / typography / rounded / padding / height / width / size。令牌请以 YAML `components.*` 为权威；此处列出可执行的选型与规格。

### 8.1 通用

**Button** `{components.button_panel}`：四尺寸 mini/small/medium/large = 24/28/32/36px 高，默认 **32px**；圆角 medium(4px)。变体状态映射（button.json）：
- **primary**：实心 `{colors.primary_default}` 白字；hover → `--color-primary-5`，active → `--color-primary-7`。每屏至多一个主按钮。
- **secondary**：白底 `--color-bg-5` + `shadow1`（0 1px 2px rgba(15,23,42,0.04)）；hover 变灰底 `--color-fill-1`。
- **outline**：透明底 + 主题色描边；active 描边环内移 1px。
- **dashed**：虚线边框 `--color-border-2/3`，用于添加/上传等次要创建。
- **text**：无边框无底，仅主色文字；用于表格行内低层级操作。
- **danger**：实心 `{colors.danger.default}` 白字。
- **disabled**：`{colors.text_4}` 文字 + `{colors.fill_2}` 底，屏蔽交互。
- **loading**：内容替换为旋转图标并禁点（`aria-busy`/`aria-disabled`）。
- 按压动效：实心/描边/虚框/文本各变体实现 1px 表面内缩（box-shadow spread 收起），press 80ms ease、release 180ms cubic-bezier(0.23,1,0.32,1)，不用 scale。

**Icon**：装饰性图标 `aria-hidden`，信息性图标提供 `aria-label`；禁用外部图标库（禁止 Lucide/Heroicons/FontAwesome）。

**Link**：默认 `{colors.link.default}`，hover `{colors.link.hover}`。

**Grid / Space / Typography / Divider**：Grid=24 列栅格；Space 用于同组间距一致（超出 3 个按钮必须用 Space）；Divider 色 `{colors.border_1}`，带文字用 `withText`。

### 8.2 布局

**Layout** `{components.layout}`：见 [4. Layout](#4-layout)。

### 8.3 导航

- **Menu** `{components.menu}`：模式 vertical/horizontal/pop/collapse，主题 dark/light。选中态文字 `{colors.primary_default}` + 左侧指示条；浅色主题 hover `--color-fill-2`、深色 `--color-menu-dark-hover`；禁用 `{colors.text_4}`。菜单项与路由 selectedKeys 联动，折叠态宽 48px 仅图标。
- **Tabs** `{components.tabs}`：line（默认，底部主色横线）/card（标签高 36px）/subtle/button/capsule/text。未激活文字 `{colors.text_2}`，hover `{colors.text_1}`+`--color-fill-2`，激活主色。嵌套不超过 2 层，文案简短不换行；roving tabindex + 方向键。
- **Pagination** `{components.pagination}`：mini/small/default/large = 24/28/32/36px 高，圆角 small(2px)。支持 pageSize 切换、快速跳转、总数。主色 `--color-primary-6`、`--color-bg-2` 页码底。
- **Breadcrumb**：当前页 `{colors.text_1}` 不可点击，上级链接 `{colors.link.default}`，分隔符 `{colors.text_3}`；仅在有上级页面语义时使用。
- **PageHeader** `{components.page_header}`：标题 `--font-size-title-2`(20px/600)、`{colors.text_1}`；返回按钮 + 面包屑 + 标题 + extra 操作区 + footer。不虚构吸顶/折叠；返回逻辑需业务实现 onBack。

### 8.4 数据录入

- **Input** `{components.input}`：四尺寸 24/28/32/36px（默认 medium 32px），圆角 medium。边框 `{colors.border_2}`、hover `--color-border-3`、错误 `--color-danger-6` + 光晕、禁用 `--color-fill-2`，文字 `{colors.text_1}`、placeholder `{colors.text_3}`。错误控件需 `aria-invalid` + `aria-describedby` 关联错误文本。
- **Select** `{components.select}`：四尺寸 24/28/32/36px，下拉面板 `{colors.bg_popup}` + `shadow2-down` + `z-index-popup`，含单选/多选(标签展示)/搜索/分组/远程/可清除；combobox 语义。
- **Checkbox / Radio**：选框 16px + 标签 14px，选中 `{colors.primary_default}`；Radio.Group(type=button) 映射 SegmentedPicker。
- **Switch** `{components.switch}`：small 28×16px、default 40×22px，开 `{colors.primary_default}`、关 `{colors.fill_3}`，圆形滑块；loading 禁响应。
- **Form** `{components.form}`：布局 horizontal（标签左，标准）/vertical（标签上，窄屏）/inline（筛选区）；控件尺寸 24/28/32/36px；必填星号、错误 `{colors.danger.default}` 红字红框、成功可 `{colors.success.default}`；提交按钮 loading 防重复、`Message.success`、失败汇总。字段 ≤8 个/单列，超过分组或 Steps 分步；校验走 rules，不虚构表单级错误聚合条。

### 8.5 数据展示

- **Card** `{components.card}`：`--color-bg-2` 底 + `--color-border-2` 边框 + medium 圆角；默认 `shadow1-down`，hoverable 悬停提升 `shadow2-down`；支持封面/Card.Meta/actions/loading 骨架。
- **Table** `{components.table}`：行高约 40px（含边框），表头 `--color-bg-2` 浅灰、行间 `--color-border-1` 分割；hover 行 `--color-fill-1`（0.2s），选中行 `--color-primary-1` 底 + 主色竖条；支持排序/筛选/固定列/行选择/展开/树形/虚拟滚动/列宽拖拽。正文 `--font-size-body-3`。规则：行操作 ≤3 个（超过收 Dropdown），首列 Checkbox 出现于批量操作时，禁止单元格堆叠 >2 个主操作。
- **Tag** `{components.tag}`：small/default/large = 20/24/28px 高；预设色浅底 `--color-{*}-light-1` + 深色文字 `--color-{*}-6`；solid 实心底白字；可关闭/可选中。
- **Empty** `{components.empty}`：图标 + 说明 + 可选操作，文字 `{colors.text_3}`。
- **Skeleton** `{components.skeleton}`：占位 `--color-fill-2` + 高光 `--color-fill-1`，圆角 small/medium；small/medium/large 头像 28/40/56px。整块用 Skeleton 防布局跳动。
- **Progress** `{components.progress}`：线形条高 8px、圆形直径 60/80/100/120px；轨道 `{colors.fill_2}`、填充状态色（primary/success/danger/warning）。

### 8.6 反馈

- **Message**：顶部/底部轻量浮层，`--color-bg-popup` + `shadow2-down` + small 圆角 + `z-index-message`；info/success/error/warning/loading/normal，自动消失。
- **Notification**：四角卡片，宽 **300px**，`--color-bg-2` + `shadow3-down` + medium 圆角；标题+正文+操作+关闭；可自动消失。
- **Alert**：页面内提示（info/success/warning/error/banner），类型色浅底 `--color-{*}-light-1` + `--color-{*}-6` 图标；原生 `role=alert`；banner 全宽无圆角；可关闭；不虚构展开收起。
- **Tooltip**：hover 纯文字说明，深底 `{colors.tooltip_bg}` 白字 + 箭头，medium 圆角，最大宽约 320px，`z-index-popup`。
- **Popover**：带操作/富内容的气泡，`--color-bg-5` + `shadow2-down` + medium 圆角；默认 `trigger=click` 更稳；非模态不启用 focus trap。
- **Modal** `{components.modal}`：遮罩 `{colors.mask}` + 居中面板，宽默认 **520px**（simple 464px），`--color-bg-2` + `shadow3-down` + medium 圆角；标题栏/正文/页脚，右上关闭；**必须实现 focus trap + Esc 关闭 + 遮罩点击关闭**（a11y §4）。
- **Drawer**：侧滑抽屉，宽/高可配，`--color-bg-2` + `shadow3-down` + large 圆角；弹层三要素同 Modal。

### 8.7 组件样式规范（AI 必读 · 可执行）

> 这就是「样式细节对不上」的根因所在：**Token 只定义了「颜色是多少」，而「组件长什么样」由一组 `giencoder-*` class 命名空间 + 现成 CSS 资产决定。** 生成高保真页面时必须**复用它，而不是自己凭直觉重写样式**。

**A. class 命名空间（唯一）**
所有可复用组件样式采用 `giencoder-{component}-{part}-{modifier}` 命名，例如 `.giencoder-btn-primary`、`.giencoder-table-tr-checked`、`.giencoder-modal-mask`。完整的 class 清单与每个组件可复制的代码模板索引见 YAML `components.componentStyles.*`。
- 节拍：`giencoder-<组件>` → `giencoder-<组件>-<部件>`（如 `-th`/`-td`/`-header`）→ `giencoder-<组件>-<部件>-<修饰>`（如 `-checked`/`-error`/`-hoverable`）。
- **禁止臆造变体**：组件没有的 class 不去发明；不确定就查 `components/{slug}.json` 契约。

**B. 现成资产引用（优先级从高到低）**
1. **组件契约** `<repo>/giencoder/components/{slug}.json` — 结构 / 状态 / 令牌的机器权威。
2. **组件代码模板** `<repo>/giencoder/preview/component-{slug}.html` — 从模板原样复制骨架，只改文字与数据。
3. **组件样式实现** `<repo>/giencoder/components.css`（唯一 249 处 class，含重复出现共 473 次）— 全部样式细节最终以此为准。
4. **颜色/字体/阴影基础** `<repo>/giencoder/colors_and_type.css` — 必须最先引入。

**C. 标准引入片段（页面 `<head>` 必须按序）**
```html
<link rel="stylesheet" href="giencoder/colors_and_type.css">
<link rel="stylesheet" href="giencoder/components.css">
```

**D. 关键样式必守契约（最容易出细节偏差处）**
- **Button 按压动效**：用「同色 spread 收起」实现 1px 表面内缩，**不用 scale**；press 80ms、release 180ms `cubic-bezier(0.23,1,0.32,1)`；hover 背景向浅一档（primary-6→primary-5），active 向深一档 + 收起 spread。`.giencoder-btn:focus-visible` 必须给出可见焦点环 `box-shadow: 0 0 0 2px var(--color-primary-light-2)`。
- **Table 选中/斑马**：选中行 = `.giencoder-table-tr-checked`，`--color-primary-1` 底 + 主色竖条；表头 `.giencoder-table-th` 用 `--color-bg-2`、行间分割 `--color-border-1`、hover 行 `--color-fill-1`（0.2s）。
- **Modal / Drawer 弹层三要素（硬规则）**：`focus trap` + `Esc 关闭` + `遮罩点击关闭`；遮罩用 `--color-mask-bg`（亮 rgba(31,31,31,.6) / 暗 rgba(0,0,0,.6)），面板 `--color-bg-2` + `shadow3-down` + `--border-radius-medium`（Modal）/ `--border-radius-large`（Drawer）。关闭后焦点归还触发元素。
- **z-index 堆叠（不得随意改）**：Affix 999 < Popup/Tooltip/Popover 1000 < Drawer/Modal/ImagePreview 1001 < Message/Notification 1003。
- **表单错误态**：错误控件 `.giencoder-input-error`，`--color-danger-6` 边框 + 光晕 + 红字，并 `aria-invalid` + `aria-describedby` 关联错误文本。
- **间距/圆角/阴影视死**：一律走 `--spacing-*`、`--border-radius-*`、`--shadow{1-3}-*` Token，不写魔法数字。

### 8.8 页面骨架 HTML 范例（后台列表页 · 可作起点模板）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>示例 · 列表页</title>
  <link rel="stylesheet" href="giencoder/colors_and_type.css">
  <link rel="stylesheet" href="giencoder/components.css">
</head>
<body>
  <div class="giencoder-layout">
    <header class="giencoder-layout-header">Header · 高 48px · bg-2 · shadow1-down</header>
    <div class="giencoder-layout-has-sider">
      <aside class="giencoder-layout-sider giencoder-layout-sider-light">
        <nav class="giencoder-menu giencoder-menu-vertical giencoder-menu-light">
          <a class="giencoder-menu-item giencoder-menu-item-selected" href="#">工作台</a>
          <a class="giencoder-menu-item" href="#">项目管理</a>
          <a class="giencoder-menu-item" href="#">成员管理</a>
        </nav>
      </aside>
      <main class="giencoder-layout-content" style="padding:20px">
        <!-- PageHeader -->
        <div class="giencoder-page-header">
          <div class="giencoder-page-header-title">项目列表</div>
          <div class="giencoder-page-header-extra">
            <button class="giencoder-btn giencoder-btn-secondary">取消</button>
            <button class="giencoder-btn giencoder-btn-primary">新建项目</button>
          </div>
        </div>
        <!-- 筛选 Form（≤6 项，24 栏栅格） -->
        <form class="giencoder-form giencoder-form-inline">
          <div class="giencoder-row" style="gap:var(--spacing-4)">
            <input class="giencoder-input" placeholder="搜索项目名称">
            <button class="giencoder-btn giencoder-btn-primary" type="submit">查询</button>
          </div>
        </form>
        <!-- 表格 Card -->
        <div class="giencoder-card">
          <div class="giencoder-card-header"><div class="giencoder-card-header-title">数据列表</div></div>
          <div class="giencoder-card-body">
            <table class="giencoder-table">
              <thead class="giencoder-table-head">
                <tr class="giencoder-table-tr">
                  <th class="giencoder-table-th">项目名称</th>
                  <th class="giencoder-table-th">状态</th>
                  <th class="giencoder-table-th">操作</th>
                </tr>
              </thead>
              <tbody class="giencoder-table-body">
                <tr class="giencoder-table-tr">
                  <td class="giencoder-table-td">GienCoder 设计系统</td>
                  <td class="giencoder-table-td"><span class="giencoder-tag giencoder-tag-success">进行中</span></td>
                  <td class="giencoder-table-td"><a class="giencoder-link" href="#">详情</a></td>
                </tr>
              </tbody>
            </table>
            <div class="giencoder-table-pagination"><span>共 12 条</span></div>
          </div>
        </div>
      </main>
    </div>
  </div>
</body>
</html>
```

**校验清单（生成后自检）**：head 是否按序引入两个 CSS；class 是否全部为 `giencoder-*` 命名；有无硬编码 hex；弹层是否满足三要素；间距/圆角/阴影是否用 Token；有无引入外部框架/图标。

---

## 9. Do's and Don'ts

以下规则**可直接执行**，均来自源码契约/patterns/a11y：

**Do（照做）**
- 颜色一律用语义 Token（`--color-*`），优先 bg/text/border/fill 语义层，再退色阶，禁止硬编码 hex（SVG fill 除外）。
- 间距用 2px/8px 体系（`--spacing-*`），组件内边距/元素间距不写魔法数字；区块间距用 16–24px。
- 圆角按分级：按钮/输入框/卡片 4px、弹窗/抽屉 8px、小标签 2px、圆形 50%。
- 用 24 栏栅格排版表单列与图表区；Sider 折叠态 48px 仅图标。
- 每个弹层组件（Modal/Drawer/Select/Dropdown）实现 **focus trap + Esc 关闭 + 遮罩点击关闭**，关闭后焦点归还触发元素。
- 破坏性操作（删除/重置）加 `Popconfirm` 二次确认；成功的破坏操作要有明确反馈。
- 各类数据/操作页都要覆盖**空 / 错 / 载**三态：Empty / Result(或 Alert) / Skeleton(或 Spin)。
- 表单必填加星号，错误控件 `aria-invalid` + 错误文本关联；提交按钮 loading 防重复。
- 纯图标按钮/信息性图标提供 `aria-label`；装饰性图标 `aria-hidden`。
- 键盘可达：Tab 流转、焦点可见（不删 `:focus-visible`）；菜单/Tabs/树用 roving tabindex + 方向键。
- 一个页面至多一个 primary 主按钮；同组按钮 >3 个用 Space 组件。

**Don't（禁止）**
- 不引入外部 CSS 框架、不引入 Lucide/Heroicons/FontAwesome/CDN 框架、不自造 SVG 路径。
- 不臆造源启不存在的组件变体/状态/class（如 Button capsule、Tabs vertical-line）；一律先查 `components/{slug}.json` 再实现。
- 不用自定义 `div` 冒充组件（如用 div 模拟 Button/Tooltip）；不用表单模拟只读（只读用 Descriptions）。
- 不在 Table 单元格堆叠 >2 个主操作。
- 不允许弹窗套弹窗超过两层。
- 不用 `display` 硬切换做显隐动效；动效 ≤0.5s、尊重 `prefers-reduced-motion`。
- 不引入 Google / Material Design 等其他设计系统的规则、令牌或组件。

---

## 10. Responsive Behavior

现有源码契约中，响应式主要由 **24 栏栅格** 与 Form 布局承担；`component-registry.json` 未给出显式 CSS breakpoint 常量，因此以下断点与折叠顺序属于**团队约定的推荐基准**（已记录到 Known Gaps，确认官方值后应替换）。

| 端 | 断点（建议） | 关键行为 |
|----|--------------|----------|
| 桌面 Desktop | ≥ 1200px（常用 1440 设计稿基准） | Sider 展开 200px；多列表格/多列栅格完整展示 |
| 平板 Tablet | 768 – 1199px | Sider 折叠至 48px（仅图标）；表单从双列收为单列；筛选区折叠进"更多筛选" |
| 手机 Mobile | < 768px | Sider 隐藏或抽屉式；Table 横向滚动或卡片化；Form 用 vertical 布局 |

**折叠顺序（建议）**：
- **侧栏**：桌面展开 → 平板折叠（图标）→ 手机隐藏/抽屉。
- **表格**：桌面全列 → 平板减少次要列（固定关键列）→ 手机横向滚动或卡片。
- **表单**：桌面双列（labelCol/wrapperCol 24 分栏）→ 平板单列 → 手机 vertical。
- **多列布局**：桌面 N 栏 →（24 栅格整除）平板减半 → 手机单列。
- 筛选项 ≤6 个，超过折叠进"更多筛选"（Collapse）；表格行操作 ≤3 个，超过收 Dropdown。

> 注意区分：数据看板图表系列（多图表）已由 patterns §5 约束，与页面响应式折叠是两件事。

---

## 11. Iteration Guide

1. **先选型清单，再生成原型**（30 秒出选型，用户审查后再生成长 HTML，避免一上来跑偏）。
2. **生成原型**：从 `giencoder/preview/component-{slug}.html` **原样复制**组件结构，只改文字与数据；class 用 `giencoder-{component}-{part}-{modifier}` 体系；状态用 class（`-selected/-disabled/-loading`）。
3. **逐区块实现**：按 `patterns.md` 六大模式组合（骨架 + 区块 + 状态 + 反馈），不自由发明布局。
4. **每次交付走规范审查**：读目标 HTML → 对照 `component-registry.json` + `tokens.md` + `a11y.md §7` → 输出 P0/P1/P2 分级问题；哪怕只改一个色值都要复审。
5. **修正**后复用同一 Source 复检；发现契约/Token 缺失时补齐 `components/{slug}.json` 并做双目录同步（`giencoder/` → `giencoder-delivery/`，`diff -r` 校验）。
6. 交付前门禁：slug 存在注册表、无外部 CSS 框架/外部图标/硬编码 hex、弹层三要素齐全、每个 PRD 页面与交互状态都实现、键盘可达 + 焦点可见。

---

## 12. Known Gaps

以下差异在本规范基于当前源码导出时已确认；历史文档/第三方资料若与当前源码冲突，**以当前源码为准**，此处记录差异与缺失：

1. **响应式断点未官方声明**：`component-registry.json` / `tokens.md` 未给出显式 CSS breakpoint 数值。本文 §10 的 1200/768 断点与折叠顺序为团队建议值，**非官方常量**，需官方确认后替换。
2. **letterSpacing 无官方 Token**：源码 `tokens.md`/`colors_and_type.css` 只定义了字号 + 行高，未定义 letterSpacing。YAML `typography.*.letterSpacing` 为排版约定值（display 负字距、正文 0.01em、caption 0.02em），非源码常量。
3. **组件属性细节**：register 中 status=new 的组件（Typography/Divider/Grid/Space/Link/Affix/DatePicker/Notification/Spin/Result/ConfigProvider/Portal/ResizeBox/Trigger/Watermark/ColorPicker/InputNumber/Rate/Mentions/AutoComplete 等）在 `components/*.json` 里部分仅有摘要级契约（source：注册表 status 字段），正文按摘要+通用 Token 描述，深粒度的 padding/height 规格待补全。
4. **灰度说明**：10 阶 gray 沿用 Arco 官方中性灰原版色值（见 tokens.md 第 6 行），暗色为同色阶反向映射；本规范未做二次调整。
5. **历史文档 vs 源码**：仓库历史 `DESIGN.md`（父目录）为更早版本品牌叙述，与当前 `tokens.md`（v3）部分品牌用语不同；本文档只采用当前源码 Token，未混用旧版语言/色值。若有其它历史文档与本文冲突，一律以 `giencoder/tokens.md` + `colors_and_type.css` 为准。
6. **暗色数据可视化系列**：`--color-data-*` 在暗色下的独立映射源码未展开定义（仅亮色给出 1–5 与说明“20 档”），本文档 YAML 只给出亮色序列，暗色图表系列待官方补充。
7. **组件样式规范已索引、未全量内嵌**：本文档以「索引 + 关键契约 + 骨架范例」形式纳入组件样式（§8.7 / §8.8、YAML `assets`/`componentStyles`），完整 249 处唯一 `giencoder-*` class（含重复出现共 473 次）实现保留在仓库 `giencoder/components.css`。生成页面时必须能访问该 CSS 文件；若在无法加载外部 CSS 的离线场景下生成，需另取方案 B（将核心组件 CSS 全量内嵌），文档体量将明显增加（预计 +200~300 行）。
8. **功能色主按钮白字对比度例外**：实测 `primary.default`(#3770F7) 对白字 **4.36:1**、`danger.default`(#F53F3F) 对白字 **3.71:1**，均低于正文级 4.5:1（AA）。`danger-6` 是 14px 非大字号、非粗体场景，3.71:1 亦未达 3:1 大字号基线。这是源码既定的高语义按钮用色，属**产品层面的有意识选择**而非缺陷，但需显式声明例外并遵守以下使用纪律，方可保留：① 实心 danger 按钮为高风险语义，保持高可辨识度，必要时搭配**加粗文字或前置图标**以补偿可读性，而非仅靠色相；② 若需达标备用值，可改用 `danger-7`(#CB272D)（对白字 5.43:1，可过 AA）作为替代或深色文字方案；③ 该例外不豁免正文/图标文字的 4.5:1 约束，仅适用于按钮底色承载短促操作文案的场景。是否上调色阶为全局常量需产品与研发确认后记录，本文不擅自改动源码 Token。
9. **preview 模板依赖顺序**：`giencoder/preview/component-*.html` 以相对路径引用 `../colors_and_type.css` 与 `../components.css`。若页面不在仓库根目录同层级部署，需按 §8.7-B 调整相对路径或直接内联。

---

## 13. Reference Sources

按优先级排列（官方优先）：

1. **官方代码仓库（当前实现）** — 本工作区 `giencoder/`：
   - `giencoder/tokens.md` — Design Token 规范 v3（唯一权威层）✅ 已读
   - `giencoder/colors_and_type.css` — Token CSS 实现（亮/暗、色板、字体、阴影、动效）✅ 已读
   - `giencoder/components.css` — **核心组件样式实现（唯一 249 处 `giencoder-*` class，含重复出现共 473 次）** ✅ 已读（§8.7 索引来源）
   - `giencoder/component-registry.json` — 71 组件注册表/分类 ✅ 已读
   - `giencoder/components/*.json` — 组件契约（含 button/input/form/table/card/tag/modal/drawer/message/notification/tooltip/popover/switch/radio/menu/pagination/tabs/breadcrumb/page-header/empty/progress/skeleton 等）✅ 已读
   - `giencoder/patterns.md` — 六大页面模式与组合规则 ✅ 已读
   - `giencoder/a11y.md` — 无障碍（对比度/键盘/焦点管理/检测清单）✅ 已读
   - `giencoder/SKILL.md` — Skill 说明、硬规则、Token 速查 ✅ 已读
   - `giencoder/docs/ai-for-designers.md` — 设计师 AI 协作手册 ✅ 已读
   - `giencoder/preview/component-*.html` — **71 个可复制组件代码模板**（§8.8 骨架范例取自 component-button/table/menu 等组合）✅ 已读
2. **官方代码仓库（交付快照）** — `giencoder-delivery/`（与 `giencoder/` 双目录同步，快照一致）。
3. **官方 AI Skill** — 组件清单 / 响应式 / 主题说明：同上 `SKILL.md`、`patterns.md`、`a11y.md`（已并入本文）。
4. **第三方资料** — 仅用于线索，未覆盖官方实现；仓库历史 `DESIGN.md` 仅作差异对照，不正为规则来源（见 Known Gaps #5）。

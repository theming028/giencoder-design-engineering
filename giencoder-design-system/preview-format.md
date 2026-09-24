# 源启 Preview 代码模板规范（preview/）

> 用途：Phase 3 生成 `giencoder/preview/component-{slug}.html` 的格式依据。
> 原则：preview HTML 是 **CODE TEMPLATE**（可直接复制的代码模板），不是视觉参考图。AI agent 生成页面时从模板原样复制组件 HTML，仅改文字与数据。

## 1. 文件结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{组件中文名} {组件名}</title>
  <link rel="stylesheet" href="preview-scaffold.css">
  <link rel="stylesheet" href="../colors_and_type.css">
  <link rel="stylesheet" href="../components.css">
</head>
<body>
  <div class="pv-header">
    <h1>{组件名}</h1>
    <p>{一句话说明}</p>
  </div>
  <!-- 每个变体一个 pv-section -->
  <div class="pv-section">
    <div class="pv-section__title">{变体名} {变体描述}</div>
    <div class="row">
      <!-- 组件代码模板，原样可复制 -->
    </div>
  </div>
</body>
</html>
```

## 2. 组件代码模板规则

### 2.1 class 命名（源启官方体系）

```
giencoder-{component} 根元素
giencoder-{component}-{part} 部件
giencoder-{component}-{modifier} 修饰/变体
```

示例：
- Button: `giencoder-btn` `giencoder-btn-primary` `giencoder-btn-size-large` `giencoder-btn-loading`
- Input: `giencoder-input` `giencoder-input-inner-wrapper` `giencoder-input-prefix` `giencoder-input-suffix`
- Table: `giencoder-table` `giencoder-table-th` `giencoder-table-td` `giencoder-table-row` `giencoder-table-cell-fixed-left`

### 2.2 状态表达

状态通过 class 表达（与 源启官方一致）：

| 状态 | class |
|------|-------|
| hover | `:hover` 伪类（CSS 内） |
| active | `:active` 伪类 |
| focus | `:focus` / `:focus-visible` |
| disabled | `disabled` 属性 / `-disabled` class |
| selected/checked | `-selected` / `-checked` class |
| loading | `-loading` class + 内置动画图标 |

### 2.3 属性约定（延续现有类名体系）

每个组件模板根元素标注数据属性，便于 agent 识别与自动化检查：

```html
data-component="{slug}" data-variant="{variant}" data-size="{size}" data-state="{state}"
```

## 3. CSS 边界

- **组件 CSS 只写进 components.css 的组件段**（`/* @component-css-start */` 标记约定延续现有体系）
- 页面级布局/间距写在页面 `<style>` 中，用 `var(--token)` 引用
- 禁止：外部 CSS 框架工具类、Lucide/Heroicons 图标、CDN 框架、self-invented SVG 路径
- 颜色一律 `var(--color-*)` / `var(--{palette}-{level})`，禁止硬编码 hex

## 4. 生成顺序

P0 高频组件先行（card/date-picker/upload/tree-select/radio/tag/input-number/result/spin/empty/skeleton/statistic/timeline/list/menu/layout），随后 P1（typography/divider/grid/space/link/collapse/popover/notification/transfer/tree/calendar/image/auto-complete/input-tag/mentions/rate/back-top/affix），P2 工具型从简。

## 5. 点击交互脚本规范（交互式模板必读）

> 所有**带点击交互行为**的组件模板必须内置原生 JS 交互脚本（放在 `</body>` 前），使预览页可直接点击演示。纯展示组件（icon/divider/grid/space/watermark/affix/skeleton/statistic/timeline/progress 等）不需要。

### 5.1 脚本骨架（统一格式）

```html
<script>
  (function () {
    'use strict';
    // 组件名（slug）——点击交互
    // 交互清单：1.xxx 2.xxx
    document.querySelectorAll('.xxx-trigger').forEach(function (el) {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        // 切换逻辑
      });
    });
  })();
</script>
```

### 5.2 硬性要求（不满足 = 不合格）

1. **纯原生 JS**：零依赖、零库，全部 `document.querySelectorAll` + `addEventListener`，IIFE 包裹防全局污染
2. **空指针防护**：任何 `querySelector` 结果都要判空或直接 forEach（forEach 对空 NodeList 天然安全）；访问 `el.parentElement` 等前判断存在
3. **不抛异常**：脚本执行中任何分支不得因缺元素/缺 class 抛错；点击不存在的目标应静默返回
4. **状态切换用既有 class**：激活/选中/展开等状态复用模板已有 class（如 `giencoder-tabs-tab-active`、`giencoder-select-option-selected`、`giencoder-modal` 显隐用 `style.display`），不得发明新 class
5. **弹层显隐**：`display` 切换用 `style.display = 'block'/'none'`，或切换 `-open/-hidden` 语义 class（须在页面 `<style>` 中定义对应规则）
6. **互斥高亮**：同类单选组（tabs/menu/dropdown 项/radio）切换时先移除同组其他项的高亮 class，再加到当前项
7. **注释**：脚本开头注释写明组件 slug 与交互清单，便于维护与复制
8. **不动结构**：只加 `<script>`，不改既有 HTML 结构与 class；不得在脚本中注入新 DOM（除非模板本来就有隐藏面板）

### 5.3 各类组件交互要点

| 组件类型 | 点击交互 |
|---------|---------|
| tabs / menu / steps / breadcrumb | 点击切换激活项（互斥高亮） |
| dropdown / select / popover / tooltip / trigger | 点击触发器展开弹层，点击外部或选项关闭（互斥展开） |
| modal / drawer / image 预览 | 点击遮罩/关闭按钮关闭；示例内触发按钮打开 |
| checkbox / radio / switch / rate / tag-checkable | 点击切换选中态（class 切换 + aria-checked 同步） |
| collapse / tree / cascader / menu-submenu | 点击展开/收起（display 切换） |
| pagination / carousel / back-top / input-number 步进 | 点击切换页码/幻灯/回顶/数值 |
| table 排序 / 多选 | 点击表头切换排序图标；点击行 checkbox 切换选中与批量条 |
| alert / message / notification / tag-close | 点击关闭按钮隐藏 |
| input 清除 / typography 复制 / upload 触发 | 点击清空/复制/触发文件选择 |
| anchor / link | 点击平滑滚动或跳转（原生链接行为，加 preventDefault 后自行处理时须有等效反馈） |
| slider / transfer / tree-select / date-picker / time-picker / color-picker / auto-complete / mentions / input-tag | 复杂交互：至少实现「弹层/面板展开收起 + 选项点击高亮」两级，不需完整拖拽/键盘 |

### 5.4 点击过渡动效规范（交互式模板必读）

> 所有点击导致的**显隐/展开/收起**必须带过渡动效，禁止硬切换（`display` 直接跳变）。以下为统一动效标准。

#### 5.4.1 通用动效参数

| 场景 | 时长 | 缓动 | 内容 |
|------|------|------|------|
| hover / 按下反馈 | 0.1s | standard | 背景/边框/透明度过渡 |
| 弹层展开 | **0.2s** | standard (cubic-bezier(0.34,0.69,0.1,1)) | opacity 0→1 + scale(0.96→1) + translateY(4px→0) |
| 弹层收起 | **0.15s** | standard | opacity 1→0 + scale(1→0.98) |
| 菜单/面板展开 | 0.2s | standard | opacity 0→1 + translateY(4px→0) |
| Modal/Drawer 出入场 | 0.3s | standard | mask 淡入 + 面板 scale(0.95→1) / 滑入滑出 |
| 状态切换（选中/勾选） | 0.15s | standard | 背景/边框/勾选过渡 |

#### 5.4.2 实现模板（弹层类通用）

```css
/* 弹层：默认隐藏 + 展开动画（配合脚本加 -open class） */
.popup { opacity: 0; visibility: hidden; transform: scale(0.96) translateY(4px); transition: opacity .2s standard, transform .2s standard, visibility .2s; }
.popup.open { opacity: 1; visibility: visible; transform: scale(1) translateY(0); }
```

```js
// 展开
popup.style.display = 'block';
requestAnimationFrame(function(){ popup.classList.add('open'); });
// 收起
popup.classList.remove('open');
setTimeout(function(){ popup.style.display = 'none'; }, 200);
```

#### 5.4.3 各类组件动效要点

| 组件 | 必须的过渡动效 |
|------|----------------|
| dropdown/select/popover/tooltip/popconfirm/trigger/cascader/tree-select/auto-complete/mentions | 弹层展开 scale+fade+slide（5.4.2 模板），收起反向 |
| date-picker/time-picker/color-picker | 面板展开 fade+scale，收起反向 |
| modal | mask opacity 淡入 + 弹窗 scale(0.95→1)，关闭反向 |
| drawer | mask 淡入 + 抽屉 translateX 滑入/滑出（已有，保持一致） |
| menu 子菜单 | 展开 opacity+translateY(4px→0) |
| tabs | 内容切换淡入（可选）；ink 滑动已有 |
| message/notification | 出现淡入+滑下，消失淡出 |
| alert/tag-close | 消失淡出（opacity + 高度折叠可选） |
| checkbox/radio/switch/rate/tag-checkable | 选中态 0.15s 过渡（背景/勾选/圆点） |
| carousel | 幻灯切换 fade（opacity 过渡，替代硬显隐） |
| collapse | 内容展开 height/opacity 过渡（0.2s） |

#### 5.4.4 硬性要求

1. **禁止 display 硬切换**：所有显隐必须走 `-open` class + transition（收起时 setTimeout 延迟隐藏）
2. 动效时长/缓动取自 tokens（0.1-0.3s / standard），禁止自造大数值
3. `visibility` 与 `opacity` 配合，避免隐藏元素仍可点击/读屏
4. 动画结束后清理（收起时 display:none；避免残留 open class）
5. 新增样式标注「交互动效用」

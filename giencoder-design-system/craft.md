# craft.md — 工艺约束

> 参考 Vibe Designing Playbook craft-animation 规范，适配 GienCoder Design System。

## 状态反馈

| 等待时长 | 处理方式 | 原因 |
|---|---|---|
| < 300ms | 不展示加载 | 避免闪烁 |
| 300ms - 2s | 骨架屏 | 稳定布局 |
| > 2s | Loader + 进度说明 | 明确等待 |
| > 10s | 超时提示 + 重试 | 用户可恢复 |

## 动效约束

- UI 动画不超过 300ms
- 只动画 `transform` 和 `opacity`（不触发 reflow）
- 每个动画必须说明目的
- 键盘触发动作不做额外装饰动画
- `transition` 属性必须显式指定（不依赖 `all`）

## 色彩克制

- 品牌色（`var(--color-primary-6)`）一屏不超过 3 处重点使用
- 避免等大白卡和无层级网格
- 中性色承载主要层级，品牌色仅用于关键操作和选中态
- 深色主题禁用蓝色强调色（trae 偏好）

## 字体与排版

- 中文 UI 默认使用 `var(--font-family)`（Mona Sans VF）
- 回退 Helvetica / Arial / Noto Sans
- 粗体标题，禁用斜体（UI 与文档均禁用）
- 文本字重最小 400

## 避免分布收敛

- 不使用统一的浅色背景配紫色渐变
- 不使用四平八稳的布局模板
- 每个页面要有明确的视觉焦点和层级差异
- 避免无意义动效和重度 Canvas 特效

# r73 · 需求 5 验收：下拉菜单 / 浮窗「显隐」通用微动效

口径（用户拍板）：**进场覆盖全部浮窗；退场只做页面自定义浮窗**（DS 组件库浮层保持原开合机制）。
改动：9 页各注入 `<style id="r73-popup-css">`（`mg-work/r73/apply73c.py`，幂等 81/81 自检通过）。

## 一、范围取证：先证明「哪些真缺动效」

用 `ev/enum-popups.js` 在每个页面实机读 **computed** `transitionProperty / transitionDuration / animationName`
（不用正则搜压缩产物——`giencoder-popup-open` 之类会被 `giencoder-popup` 子串误算进来）。

| 页面 | 元素 | 改前 computed | 判定 |
| --- | --- | --- | --- |
| task-detail | `.td-add-pop` | `transition-property: all` / `0s`，无 animation | ✗ 缺 |
| task-detail | `.giencoder-select td-skill-pop` | `transition-property: all` / `0s` | ✗ 缺 |
| avatar | `.td-add-pop` / `.td-skill-pop` | 同上 | ✗ 缺 |
| 全 9 页 | `.giencoder-tooltip-popup` | 只有 `box-shadow`，无 transition / animation | ✗ 缺 |
| task-detail / avatar / base | `.avatar-tooltip` | `transition-property: opacity` / `.15s`，无位移、退场秒隐 | ⚠️ 半 |
| 全 9 页 | `.giencoder-select-popup` | `opacity, translate, scale, visibility` / `.15s` | ✓ 已有，不动 |
| kanban / req-kanban | `.giencoder-date-picker-popup` | `opacity, transform, visibility` / `.2s` | ✓ 已有，不动 |
| kanban / task-detail | `.giencoder-modal *-dialog` | `opacity, transform` / `.13s,.16s` | ✓ 已有（模态不属「下拉浮窗」） |
| task-detail | `.td-ctx` / `.td-more` | r54/r59 已按契约做全开合过渡 | ✓ 已有，不动 |

> 结论：**「全局所有下拉/浮窗」里，真正缺动效的只有 3 处**（2 个页面自定义浮窗 + DS Tooltip），
> 其余早已统一。因此本需求是一次「补缺口」，不是「全量重做」——避免重复定义、避免覆盖组件库既有参数。

## 二、改后实机证据（agent-browser，file:// 直开，1920×1080）

### 进场（打开瞬间同步取 computed，应停在 from 值）
`task-detail` 与 `avatar` 两页结果一致：

```
.td-add-pop    hidden=false display=block opacity=0 translate=0px 4px scale=0.97
               running transitions = [opacity, scale, translate]
.td-skill-pop  hidden=false display=flex  opacity=0 translate=0px 4px scale=0.97
               running transitions = [opacity, scale, translate]
.avatar-tooltip  translate = 0px 2px
                 transition = opacity, translate, visibility / .15s,.15s,0s / delay 0s,0s,.15s
```

### 退场（关闭瞬间同步取 computed，display 必须"撑着"不塌）
```
.td-add-pop    hidden=true  displayDuringClose=block  opacity=1 translate=0px scale=1
               running transitions = [display, opacity, scale, translate]
.td-skill-pop  hidden=true  displayDuringClose=flex   opacity=1 translate=0px scale=1
               running transitions = [display, opacity, scale, translate]
```
`display` 出现在运行中的过渡列表里 ⇒ `transition-behavior: allow-discrete` 生效：
先播完 160ms 动效，再真正落到 `display:none`。

### 几何无回归（稳定态对照改前基线 /tmp/r73c-backup）
| | 技能面板 skill | 添加菜单 add |
| --- | --- | --- |
| 改前 | 1454, 596, **436×320** | 1466, 910, **180×92** |
| 改后（稳定态） | 1454, 596, **436×320** | 1466, 910, **180×92** |
| 改后（进场中） | 1467, 605, 423×310（= 436×320 × 0.97） | — |

稳定态 `translate: none / scale: none` ⇒ 位移与缩放只是"起跑点"，落点与设计稿完全一致。

## 三、为什么不用 JS

`.td-add-pop` / `.td-skill-pop` 原本由 `pop.hidden = true/false` 开关（`closeAdd()` / `closeSkill()`）。
本轮用 **CSS 原生 `@starting-style` + `allow-discrete`** 一次拿到进场与退场，
**没有改动任何一行 JS** —— 少了状态机、少了 `transitionend` 兜底、少了"动画中途再点一次"的竞态。

支持性实测：`CSSStartingStyleRule in window` → `true`；`CSS.supports('transition-behavior','allow-discrete')` → `true`。

## 四、截图
- `05-addpop-open-1920.png` — 添加菜单展开态（右侧对话框上方）
- `06-skillpop-open-1920.png` — 技能面板展开态

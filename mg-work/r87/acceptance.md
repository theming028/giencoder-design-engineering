# r87 验收档案 · 「设置」页四条（全局字号机制 / select 三项全站 / 设置页按钮换 DS / 导航选中态）

> 迭代对象：`pages/settings.html`（r85 落地的设置页），其中第 2 条是**全站组件级**改动。
> 时间：2026-09-30 ｜ 执行：艾迪 ｜ 状态：**已落地 + 四查通过 + 实测取证完成；按约定未 commit / push**

---

## 一、需求（邵先生原文）与落地结果

| # | 需求原文 | 落地 | 实测判据 |
|---|---|---|---|
| 1 | 「`r85-slider` 是字号调节器，6 级字号 13/14(默认)/16/18/20/24。这个字号的调整是**针对整个产品全局界面**的，请帮我想想具体如何实现」 | **变量等比缩放**：`:root{--ui-fs}` 唯一旋钮 + 11 个 DS 字号 token 全部 `calc(Npx * var(--ui-fs-ratio))` + 尾风 px 类逐条覆盖 + 文字控件高度跟随 + `<head>` 引导脚本读 `localStorage` 写成 `<html>` 内联样式（首帧生效不闪） | 6 档实测：导航高 33/36/41/46/51/62（=36×k）、select 高 30/32/37/41/46/55（=32×k）、分段高 38/40/46/51/57/69（=40×k）**全等比**；默认档页面几何 `[510,85,840,918]`、卡片 `[230,448,156]` 与 r85/r86 **完全一致** |
| 2 | 「`.giencoder-select-view` 里的 `--select-ring` 要**全局去掉**，同时组件的圆角度调整为 **8px**，宽度**自适应**，右对齐」 | ①删 ring 变量 + 删 `, 0 0 0 1px var(--select-ring)` spread 项（保留极淡 `0 1px 2px` 轻投影）②圆角 4px（medium）→ 8px（large）③`.giencoder-select` `width:100%` → `width:auto;max-width:100%` ④另 4 条**页面级**适配规则写死的 6px 一并抬到 8px | 三份 DS 源 + 9 页：`select-ring` 命中 **0**；全站 select 触发框 radius 实测 **8px**；设置页 select 无内联 width、`ctlRight = rowRight = 1330`（右缘贴行右缘）；4 页回归 `overflowX=0`、零新增裁切 |
| 3 | 「设置页面里的全部按钮也都要使用设计系统里的同类型按钮组件」 | 内容区操作按钮（更新日志/检查更新/退出登录）→ `giencoder-btn giencoder-btn-secondary giencoder-btn-size-default`；外观分段控件 → `-secondary -size-large`；删除原手搓 `.r85-btn` / `.r85-seg > button` 的**全部外观声明**，只留 `rq-` 级适配层 | 三按钮实测 `cls` = DS Button 全要素、**104×32**、radius 8px；分段三颗 **128×40**、radius 8px；CSS 里已无 `.r85-btn{…外观…}` 手搓块 |
| 4 | 「左栏 aside 菜单被选中时，文字也要变成**主题蓝色**，字重**中粗 500**」 | `.r85-navi[aria-current='true'] > span{color:var(--color-primary-6);font-weight:500}` | 系统设置 `spanColor=rgb(55,112,247)`、`spanWeight=500`；未选中项 `rgb(31,31,31)` / `400` |

---

## 二、第 1 条为什么不是 `html{font-size}`（方案论证留痕）

先做结构性取证，再定方案：

| 通道 | 事实 | 结论 |
|---|---|---|
| 外壳（React 渲染的顶栏/侧栏） | 用**尾风 px 类**：`.text-sm{font-size:14px;line-height:20px}` —— **不是 rem** | `html{font-size}` 这根常规杠杆**不成立** |
| 页面自绘 + DS 组件 | 走 `var(--font-size-*)`，而 token 在 `:root` 里是**字面 px** | 改 token 定义即可等比 |
| 全站文字类总量 | 仅 6 种（text-xs 12/16、text-sm 14/20、text-lg 18/28、text-2xl 24/32、text-[13px]、text-[11px]） | 外壳逐条覆盖**有限且可穷举** |

⇒ 用户答复「我不太懂，使用你推荐的方式」后采纳**变量等比缩放**。关键设计点：

1. `--ui-fs`（px 无单位，14 = 默认档）是唯一旋钮；`--ui-fs-ratio: calc(var(--ui-fs) / 14)`。
   ⚠ `--ui-fs` / `--ui-fs-ratio` **只允许在 `:root` 声明一次**，否则会盖掉 `<html>` 上的内联值。
2. 引导脚本必须写在 `<head>`（首帧前）并 `documentElement.style.setProperty('--ui-fs', …)` ——
   内联与 `:root` 同特异性，**内联后写赢**。
3. 覆盖规则**一律加 `body` 前缀** ⇒ 特异性高于任何后置的普通规则，**与脚本执行顺序无关**。
4. 行高/高度**只在「自身声明了 token 字号」的规则内派生**（否则字大行高不变会裁字）；
   派生写法 `height:calc(Npx*R);min-height:calc(Npx*R)` 成对，保证可逆幂等。
5. **图标盒与布局盒刻意不跟随** —— 本设置只缩放「文字相关」尺寸。

---

## 三、本轮修掉的两个自身缺陷（重要）

### ① `unscale()` 把本代自己注入的块一起还原（真 bug，会导致永久损毁）

`apply87.py` 末尾原为 `scale_css(unscale(out))`，而 `out` 已含 `<style id="r87-ui-css">`。
该块里有两类**无法被 `scale_block` 重新派生**的声明（所在规则不含 `var(--font-size-*)`）：

| 声明 | 被还原成 | 后果 |
|---|---|---|
| 尾风 `.text-xs/.text-sm/.text-lg/.text-2xl` 的 `line-height:calc(Npx*R)` | 字面 `16/20/28/32px` | **外壳（React 顶栏/侧栏）放大字号时裁字** |
| `.giencoder-select-view{min-height:calc(32px*R)}` | 字面 `32px` | **select 不跟着长高**（24px 档：按钮 54.8 而 select 只 38） |

（`height:calc(...)` 那些**侥幸存活**：`unscale` 的三条正则里 `RE_SCALED_H2` 要求 height+min-height 成对、
`RE_SCALED_MH`/`RE_SCALED_LH` 只认裸的 min-height / line-height。）

**修复**：在 `apply87b-fontsize.py` 新增 `converge(css)` —— 先把本代样式块用哨兵**摘出**，
只对「其余 CSS」做 `unscale → scale`，再把块原样放回。`apply87.py` 改调 `converge()`。
修复后实测：`body .text-sm{font-size:calc(14px*R);line-height:calc(20px*R)}` ✔、
`body .giencoder-select-view{min-height:calc(32px*R)}` ✔、24px 档 select 高 54.8 = 按钮高 ✔。

### ② 第 3 份 DS 源漏改

DS 组件样式在仓库里有**三份**：`giencoder-design-system/components.css`（主源）、
`giencoder-design-system/gienx-templates/_shared/components.css`（模板层副本，`build.py` 用）、
以及 `pages/*.html` 内联的构建产物。首轮只改了主源 + 页面 ⇒ 模板层副本会**回潮**。
已把 `_shared/components.css` 纳入 `apply87a-select.py`。

---

## 四、决策留痕（邵先生拍板）

| 议题 | 选项 | 决定 |
|---|---|---|
| 4 条页面级 6px 适配规则（kanban 3 + req-kanban 1，其中 1 条与「日期输入框」共用） | 全改 8px（输入框同改）/ 只改 select / 不动 | **全部改 8px，输入框同改** ⇒ 共用规则整体抬到 8px，同行两控件圆角一致 |
| task-detail / avatar 的 4 个胶囊形 select（`.select-view-ghost`，内联写死 `border-radius:32px`，用于「标准模式 / DeepSeek-V4-Pro」芯片） | 保持不动 / 也改 8px | **保持胶囊形不动**（有意做的另一变体；仅同步去掉 ring） |

---

## 五、四查（全绿）

| 查 | 方法 | 结果 |
|---|---|---|
| ① 幂等 | `apply87a` / `apply87b` / `apply87` 各连跑两遍 | 第二遍全部「已是目标态」/ `+0`；`settings.html` sha256 `19a8406f…1881` 不变 |
| ② 语法 / 配平 | `python mg-work/check-syntax.py pages/*.html` | **9/9 通过**（`ALL_OK`，script/style 计数正常） |
| ③ 设计规范零影响 | `python verify-design.py ./pages` + 与 **HEAD 基线同口径**逐条归一化 diff | 汇总恒为 `75 / 66 warning / 9 info / 0 critical`；**全量 75 条零新增零消除**；`gaps.log` 去行号后 65 → 65，集合完全一致（⚠ HEAD 里那份 `gaps.log` 是陈旧产物，脚本站位有位移，**必须同口径复跑再定性**） |
| ④ 视觉回归 | agent-browser 1600×1100，真鼠标/真渲染 + 像素级前后 diff | 见下 |

### ④ 视觉回归明细

* **默认 14px 零回归（像素级确证）**：`.r85-page` 元素截图 before/now 逐行 diff ——
  仅 7 处差异区，**全部落在右侧控件列**（三个 select 行 / 分段控件 / 版本按钮 / 退出登录），
  其余 0 像素变化；`.r85-nav-host` 仅 1 处差异区（行 87..99 · 列 36..91 = 系统设置文字）✔
* **6 档不溢出**：24px 档 `documentElement` `overflowX = 0`、`lineTightCount = 0`；
  唯一「scroll > client」项是主滚动容器（内容变高，属正常）。
* **全站 select 回归**：settings / kanban / req-kanban / task-detail / avatar **五页 `overflowX = 0`**；
  `--select-ring` 命中 0；`ringInlineHolders` 为空数组；select 宽度未换算处（kanban `.kb-proj-select` 148×32、
  `.kb-type-select` 112×28）**前后完全一致** ⇒ 未误伤既有定宽。
* **既存裁切未新增**：task-detail（`td-desc-body` / `td-attr-v` / `td-right-title ox=56`）与
  avatar（`td-bf-name ox=8..31` / `td-browse-pre ox=24`）的 clipped 列表 **before/after 逐字相同**。
* **DS 自身预览页**：`preview/component-select.html` 5 个 select 全部 8px / 无 ring / 渲染正常。
* **遗留提示（非本轮引入）**：kanban 24px 档 `.giencoder-input.kb-date-val` 溢出 137px（定宽日期框 + 字放大）；
  `.giencoder-select` 类名被 task-detail/avatar 当**通用 flex 容器**复用（包「添加」按钮与技能弹层），
  属既存命名问题。

---

## 六、改动清单（工作区 · **未 commit**）

### 新增脚本（`mg-work/r87/`）

| 文件 | 职责 |
|---|---|
| `apply87a-select.py` | 第 2 条：三份 DS 源 + 9 页的 ring / 圆角 / 宽度 + 4 条页面适配层。支持 `--revert` / `--dry` |
| `apply87b-fontsize.py` | 第 1 条机制层：token 派生 + 尾风覆盖 + 高度跟随 + 引导脚本 + **`converge()`**。支持 `--revert` / `--dry` |
| `apply87.py` | 第 1/3/4 条设置页层（接续 `apply86.py`，SHELL 标记 `SHELL-R87-SET v3`，`PRIOR` 收 3 代旧块） |

> 执行顺序：`apply87a` → `apply87b` → `apply87`（`apply87` 末尾自动 `converge`，与 `apply87b` 顺序无关）。

### 被改文件（15 个）

| 文件 | 改动 |
|---|---|
| `pages/*.html` ×9 | select 三项（各 −62 字符）+ 4 条适配层 + 字号机制（各 +3.6K~12K）+ 设置页四条 |
| `giencoder-design-system/components.css` | select ring / 圆角 large / width auto |
| `giencoder-design-system/gienx-templates/_shared/components.css` | 同上（模板层副本） |
| `giencoder-design-system/components/select.json` | 契约 token：`--border-radius-medium` → `--border-radius-large` |

**最终 sha256**（关键）

```
pages/settings.html                                        19a8406fc3d2f945e7d0667bd452fae72434c226f23440dd4666ee38e1e01881
pages/kanban.html                                          fb8bfad47858c83b585e23225bb19a26807c8cae0ca3fabd4432f267ac49d6db
giencoder-design-system/components.css                     fb88c17e27d853e987707254e61c6e827c5b3c5f51cbeb6a388b228cabeb84bb
giencoder-design-system/gienx-templates/_shared/components.css  a57607afb68f1d9a0f8e3a76175e6d5ba19879820614a3c15f957b91dbf06032
giencoder-design-system/components/select.json              ab2251b8a6bbec5445eb789d96076c3b401cadc161ead88fa2f5e9aabac06298
```

**体积变化**（字节，CRLF）

| 页面 | HEAD | 现在 | Δ |
|---|---|---|---|
| settings.html | 428753 | 443356 | +14603 |
| task-detail.html | 816859 | 829197 | +12338 |
| avatar.html | 589195 | 597849 | +8654 |
| kanban.html | 580079 | 588171 | +8092 |
| req-kanban.html | 519299 | 526480 | +7181 |
| base.html | 479792 | 484988 | +5196 |
| dev.html | 452344 | 458150 | +5806 |
| automation.html | 360798 | 365592 | +4794 |
| skills.html | 360729 | 365523 | +4794 |

### 取证素材（`mg-work/r87/ev/`）

`cmp_r87.png`（分区前后对照）· `cmp_r87_zoom.png`（4× 细节）· `fs6_levels.png`（6 档实测条）·
`a_default_full.png` / `b_fs24_full.png` / `c_fs13_full.png` · `d_*.png`（4 页回归）·
`e_kanban24.png` · `preview_select.png` · `p87a-final.txt` / `p87c.out.txt` / `d_*.txt` / `e_kanban24.txt` /
`rect_{before,now}.txt` · 脚本 `p87a/p87c/p87d/p87e/p87rect.js`、`shots87.sh` / `el-shots.sh` / `fs6.sh` /
`base-run.sh`、`cmp87.py` / `mkcmp87.py` / `mkzoom87.py` / `mkfs6.py` / `diff-gaps.py` / `diff-vd.py`

---

## 七、遗留 / 下一步

1. **未 commit / push**（2026-09-28 起约定：默认不自动提交，由邵先生发起）。
2. 待拍板（本轮已问、已按答复落地）：无。
3. 本轮新发现、供下轮取舍：
   * `.giencoder-input-wrapper`（Input）在 kanban 合排行里已随 select 一起抬到 8px；
     其他页面的 Input 仍是 `--border-radius-medium`(4px)/页面自定 6px ⇒ **全站 Input 圆角是否统一**未定。
   * kanban 定宽日期框 `.kb-date-val` 在大字号档会截断（137px 溢出）。
   * `.giencoder-select` 类名被当作通用 flex 容器复用（task-detail / avatar）。
4. 更早遗留：r86 的选择器 3 处 DS vs 设计稿差异、清除按钮行为；r85 四条；r84 提问；r83 `ROWS`；
   r81 三条；r79 `r74-ripple`；r77 滚动条；r74 动效上限；r72 `Esc#1`；`pages/gaps.log` 不同步。
5. ⚠ 安全：曾有一枚 PAT（`ghp_` 前缀 · 40 位）明文出现在对话记录里，且与推送用的凭据同源。
   **本仓文档/探针日志自此一律不记录 token 明文**（本次入库前已打码）；该 token 待邵先生 Revoke 并换发。

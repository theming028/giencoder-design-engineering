# r84 验收报告 · 2026-09-29

> 邵先生四条修正（对象 = r83 落地的「会话历史」二级视图）：
> 1. `av-hs-name` 文字都用常规字重
> 2. 「删除会话」的 SVG 图标不对（对比设计稿修复），且图标按钮 hover 时通过 tooltip 显示名称
> 3. 卡片 `av-hs-item` **hover** 时，右侧两个图标替换成「取消」「确定删除」
> 4. 第一个卡片默认不要浅灰底色（白底即可），且卡片整体都是可点击热区
>
> **轮内修订（③ 的触发方式）**：邵先生随后改为
> 「**点击**了会话历史里的删除按钮后，那一块才会变成俩按钮」⇒ 已按此定稿（详见第三节）。
>
> 产物：`pages/avatar.html`。两个口径别混（★ 易读错）：
> - **脚本口径**：`541277 → 559978` —— 541277 是把 r83/r84 注入块**全部摘净后的"净底"**（= r82 终态），
>   差额 **+18701** = 本轮三块注入的字符总量（与 r83 的 `541277 → 553997 (+12720)` 同口径，可比）。
> - **改动口径**：r84 基线（= r83 终态，`mg-work/r84/avatar.before.html`）**553997** → **559978**，
>   本轮相对上一轮**净增 +5981**。
>
> **未 commit / 未 push。**

---

## 一、★ 本轮最大的取证发现：设计稿那枚「删除」图标**没有导出 SVG**

第 2 条说「图标不对」，先要搞清设计稿里到底长什么样。

`get_selection_node` 拿回的结构树（`mg-work/r83/raw/node_1389-18518.json`）里，每张卡片右侧是**两个不同性质的节点**：

| 位置 | 节点 | 类型 | 能否拿到矢量 |
|---|---|---|---|
| 左（行内 x376..400） | `div.icon-wrapper` → `img src=svg_5f4f2e22.svg` | 普通图层 | ✅ 已导出 |
| 右（行内 x408..432） | `ui-component name="icon-wrapper" props={"尺寸":"14"}` | **未展开的 DS 组件实例** | ❌ **没有 asset** |

⇒ mgfetch 只捞到 2 个图标 asset（导出 + 返回），**删除图标压根没有导出 SVG** —— r83 那枚是我「照 PNG 灰度矩阵手搓」的，形状当然不对。

**定位真身**：把候选矢量渲染出来与设计稿 PNG 并排（`mg-work/r83/raw/cmp_icon.png`），一眼确认
设计稿那枚 = 仓内 DS 的 **`assets/icons/delete.svg`**（12 单位 viewBox 按 14px 渲染 ⇒ ×1.1667）。
三处关键坐标逐像素全中：

| 特征 | 设计稿 PNG 实测（节点坐标） | `delete.svg` @14px 换算 |
|---|---|---|
| 盖（含把手） | 把手 x437..442 / y90；盖 x434..445 / y91..92 | x438.3..442.8 / y90.5；x434.7..445.3 / y91.4..92.2 ✔ |
| 桶身竖边 | x435..436 与 x443..444 / y93..101 | x435.0 与 x444.9 ✔ |
| 双肋 | x438 与 x441（两肋相距 ≈2.6） | x438.6..439.2 与 x440.9..441.4 ✔ |
| 桶底 | y100..101 | y101.1 ✔ |

⇒ **直接搬真矢量**：`viewBox="0 0 12 12" width="14" height="14"` + `fill="currentColor"`。

### 顺带修的一处（未在四条之内，请复核）

左枚「导出」在 r83 也是我手搓的近似版。真 asset 是 `raw/1389-18518__svg_5f4f2e22.svg`
（mastergo 导出带 `matrix(0,1,1,0,.2417,-.2417)` 转置 ⇒ 转置后是「托盘 ⊓ + 下箭头」）。
真矢量托盘宽 **11.08**、右壁中段断开让箭头穿过；手搓版是 9.92 宽的闭合 ⊓ —— 差了 1px/侧。
⇒ 一并换回真矢量（去掉原 clipPath：路径本就在 14×14 框内，留着反而产生重复 id）。
真矢量换算：托盘 x402.5..413.5 / y90.2..97.8、箭头尖 y101.5，与设计稿实测 x403..414 / y90..101 **逐像素吻合**。
头部的「返回」箭头**没动**（不在本轮四条内）。

---

## 二、③ 的触发方式：两次定稿，最终「点击删除图标」

### 2.1 首版（已废弃）：hover 整张卡片就替换

第 3 条（卡片 hover → 换成按钮）与第 2 条（图标按钮 hover → tooltip）**落在同一个 hover 上互斥**：
鼠标一进卡片，图标就被替换掉，tooltip 无处可显示。当时向邵先生列出三种触发方式，他选了「hover 整张卡片就替换」。

### 2.2 定稿：**点击**「删除会话」图标才替换

邵先生随后改口径：「点击了会话历史里的删除按钮后，那一块才会变成俩按钮」。
这一改把两条需求彻底解开 —— **图标不再被 hover 掉，tooltip 立即可用**（本报告第四节实测）。

```css
.av-hs-confirm { display: none; flex: none; align-items: center; gap: 8px; margin-right: -2px; }
.av-hs-item.is-confirm .av-hs-acts { display: none; }
.av-hs-item.is-confirm .av-hs-confirm { display: flex; }
.av-hs-item.is-confirm { background: var(--color-fill-2); }   /* 确认态自持底色 */
```

首版那套 `.is-cancel`（悬停内退出确认态）与 `:hover` 触发**整套撤销** —— 点击驱动下不需要它了。

**点击触发引入的新状态机分支（首版不存在，必须定义）**：

| 情形 | 行为 |
|---|---|
| 点 A 行删除 → 再点 B 行删除 | A 行**自动复位**，只允许一行处于确认态 |
| 确认态下点该行其他地方 | **只放弃**（退出确认态），**不会**顺手打开会话 —— 否则太意外 |
| 点「取消」 | 退出确认态，图标组回来 |
| 点「确定删除」 | 移除该行 + 轻提示 `已删除「…」` |
| 键盘触发（`click.detail === 0`） | 焦点交给「取消」：被 `display:none` 的删除按钮会把焦点丢回 body，下一个 Tab 会从页面开头重来；**鼠标触发不动焦点**（免得飘出光圈） |
| 关闭视图（返回 / Esc / 关会话栏） | 复位所有确认态 |

**几何按设计稿对齐**（设计稿那组是绝对定位 `left:306; top:14; 128×28`）：

| 项 | 设计稿实测 | r84 实现实测 | 判 |
|---|---|---|---|
| 行底（确认态） | `#F2F2F2` | `rgb(242,242,242)` | ✔ |
| 取消 | 48 × 28、白底、描边 `#E5E5E5`、字 12px | `[302,14,48,28]`、`rgb(255,255,255)`、`rgb(229,229,229)`、`12px` | ✔ |
| 确定删除 | 72 × 28、底 `#F53F3F`、字白 | `[358,14,72,28]`、`rgb(245,63,63)`（静置）/ `rgb(247,101,96)`（DS 悬停色） | ✔ |
| 组内间距 | 8 | `gapBetween = 8` | ✔ |
| 组右缘距行右缘 | **8**（图标组是 10，设计稿这两处本身差 2） | `confirmRight = 8` | ✔ |
| 文本收窄 | 设计稿第 3 行名字框 235（比常规行 310 窄） | 354 → **284**（按钮组进布局流，不收窄会与按钮重叠） | ✔ 方向一致 |

按钮尺寸用的是**适配层** `padding: 0 11px`（48 = 12×2 字宽 + 11×2 内边距 + 1×2 描边），未改 DS Button 本体。

> ⚠️ 一处**照设计稿保留**的观察（不是 bug）：按钮组窗口（行内 x306..430）**覆盖**原图标位置（x372..428）
> —— 设计稿本身就是这么画的。所以点完删除图标，鼠标正落在「确定删除」上；快速连点两下会直接删除。
> 若要规避，只能偏离设计稿把按钮组右移，**留待拍板**。

---

## 三、第 1 / 2 / 4 条

| # | 需求 | 落地 | 实测 |
|---|---|---|---|
| 1 | 名字常规字重 | `.av-hs-name` `font-weight: 500 → 400` | `["14px","400","22px"]` ✔ |
| 2 | 图标 = 设计稿真矢量 | 见第一节 | `trashPathHead = "M7.463 1.125c.269 0 .487.2"`、`viewBox 0 0 12 12`；`exportTransform = matrix(0,1,1,0,.2417,-.2417)` ✔ |
| 2 | 图标按钮 tooltip | 新增 `.av-tip`（照 DS `giencoder-tooltip-popup` 观感，全 token）+ `data-av-tip` | 见第四节 ★ 实测 ✔ |
| 4 | 首行默认白底 | `.av-hs-item:hover` 从 `.av-hs-item:hover, .av-hs-item.is-on, …` 里**摘掉 `.is-on`**（类与 `aria-current` 保留语义，不再着色） | 首行 `bg = rgba(0,0,0,0)` ✔ |
| 4 | 整卡热区 | `.av-hs-item{position:relative;cursor:pointer}` + `.av-hs-name::after{inset:0}` 铺满整行；`.av-hs-acts / .av-hs-confirm{z-index:1}` 压在热区之上 | `elementFromPoint`：行内名字框**上方空白** / 行**左内边距** / 时间行右侧空白 → 全部 `av-hs-name`；**图标区** → `av-hs-ibtn`（仍可单独点） ✔ |

---

## 四、★ 运行时实测（agent-browser，2400×1000，抽屉元素截图 480×944）

### 4.1 默认态 —— 图标必须**可见**（这是点击触发换来的）

```json
{"rows":7,"actsDisplay":["flex"],"confirmDisplay":["none"],"rowBgDefault":["rgba(0, 0, 0, 0)"],
 "nameW":354,"delVisible":"flex","expVisible":"flex","delTip":"删除会话","expTip":"导出会话",
 "firstRowBg":["rgba(0, 0, 0, 0)"],"firstRowHasIsOn":true,"isConfirmCount":0,"tipExistsIdle":false}
```

### 4.2 ★★ 悬停「删除会话」图标 —— tooltip **可达了**（首版方案下这里必然为空）

```json
{"delExists":true,"delHovered":true,"delVisible":"flex","expVisible":"flex",
 "tipExists":true,"tipHidden":false,"tipText":"删除会话","tipClass":"av-tip is-top",
 "tipFont":"12px","tipPad":["4px","8px"],"tipBg":"rgb(31, 31, 31)","tipColor":"rgb(255, 255, 255)",
 "tipRadius":"8px","tipGap":4,
 "delRect":[2337,249,24,24],"tipRect":[2317,221,64,24],"drawerRect":[1912,48,480,944]}
```

对照 r84 首版：同样的图标在 hover 整卡方案下 `display:none`，`tipExists` 永远 `false`。

### 4.3 点击链（真鼠标点击 + 程序化点击各跑一遍）

| 步骤 | 期望 | 实测 |
|---|---|---|
| 点删除图标 | 该行进确认态 | `isConfirm:true / acts:"none" / confirm:"flex" / bg:"rgb(242,242,242)" / nameW 354→284` ✔ |
| 真鼠标点击后焦点 | 不该被抢走 | `activeEl:"BODY"`、`activeIsCancelBtn:false` ✔ |
| 点「取消」 | 复原 | `isConfirm:false / acts:"flex" / confirm:"none" / nameW 354` ✔ |
| A 行删除 → B 行删除 | A 行自动复位 | `row3:{isConfirm:false,acts:"flex"}`、`row5:{isConfirm:true,confirm:"flex"}` ✔ |
| 确认态下点该行名字 | 只放弃，**不打开会话** | `isConfirm:false / acts:"flex" / viewStillOpen:true` ✔ |
| 点「确定删除」 | 行消失 + 轻提示 | `rowsBefore:7 → rowsAfter:6`、`toastText:"已删除「可视化工作流编排可视化工作流…」"` ✔ |
| 确认态 → 点返回 / 按 Esc | 关视图同时复位确认态 | `viewClosed:true / confirmLeft:0`；再进视图 `isConfirm:false / acts:"flex" / confirm:"none"` ✔ |

### 4.4 落地时踩到并修掉的两个真问题

1. **`.focus()` 会触发 `focusin` ⇒ tooltip 凭空弹出**：tooltip 最初同时绑 `focusin`，而 `openView()` 里
   给返回按钮 `.focus()` ⇒ **每次打开视图都立刻弹出「返回」tooltip**（实测 `tipExistsIdle:true,tipHiddenIdle:false`）。
   ⇒ 去掉 focus 触发，**只走 hover**；键盘用户的名称交给 `aria-label`。复查空闲态 `tipExistsIdle:false` ✔。
2. **`.av-tip{font-size:12px}` 被门禁抓成 1 条 `[TOKEN-GAP]`** ⇒ 改 `var(--font-size-body-1)`（同为 12px），
   回到「逐条 diff 新增 0」。
3. **程序化 `.click()` 的 `detail === 0` 会被当成键盘触发** ⇒ 截图里「取消」多出一圈焦点光圈。
   取证一律用 agent-browser `click`（真鼠标、`detail=1`）重拍，顺带验证了「鼠标触发不抢焦点」。

---

## 五、四查

| 项 | 命令 | 结果 |
|---|---|---|
| 幂等 | `python mg-work/r84/apply84.py` 复跑 | `541277 → 559978 (+18701)` 两次一致；复跑后 `sha256` 不变；`strip_all()` 摘回后**逐字节等于基线 553997** |
| 语法 | `python mg-work/check-syntax.py pages/avatar.html` | `ALL_OK avatar.html script=10 style=13` |
| 门禁（本次） | `python verify-design.py ./pages` | **66🟡 / 9🔵 / 0🔴** |
| 门禁（HEAD 基线） | `git archive HEAD pages` → /tmp 同口径复跑 → **逐条 diff `gaps.log`** | **完全一致 = 新增 0 / 消失 0** |

残留自查：`is-cancel` 0 / `data-av-hs-confirm` 0 / `r83-hs-*` 0 / `av-hs-item:hover .av-hs-acts` 0。
收尾：`pages/gaps.log` 已 `git checkout --` 还原；`/tmp/headcheck`、`/tmp/hp` 已清。

---

## 六、交付物

| 路径 | 内容 |
|---|---|
| `mg-work/r84/apply84.py` | 本轮补丁（块 id `r84-hs-*`；`PRIOR` **同时摘 r83 与 r84 两代标记** ⇒ 谁复跑都是「先摘后插」，永不会两代并存） |
| `mg-work/r84/avatar.before.html` | 改前基线 = **r83 终态 553997 字符**（585392 B）—— ⚠ 不是脚本输出的 541277，后者是"净底" |
| `mg-work/r84/ev/cmp_r84.png` | ★ 取证图：① 两枚图标（设计稿 \| 实现，×7）② **点击后**的确认态（设计稿 \| 实现，×5） |
| `mg-work/r84/ev/s1_default.png` | 默认态（抽屉 480×944）：首行白底 + 两枚图标常显 |
| `mg-work/r84/ev/s2_click.png` | 点「删除会话」后的确认态（抽屉 480×944，真鼠标点击） |
| `mg-work/r84/ev/s3_tip.png` | ★ tooltip「删除会话」特写（×5，从全页图裁） |
| `mg-work/r84/ev/s3_full.png` | 含 tooltip 的全页 2400×1000 |
| `mg-work/r84/ev/{p84a,p84b,p84tip,open_view}.js` | 探针（默认态 / 点击链 / 悬停 tooltip / 进视图） |
| `mg-work/r83/raw/cmp_icon.png` | 图标真身比对页的渲染结果（候选矢量 vs 设计稿） |

## 七、待拍板

1. **按钮组覆盖图标位**（第三节末的观察）：设计稿本身如此，连点两下会直接删除。要偏离设计稿把按钮组右移吗？
2. 「导出」图标换真矢量是**超出四条**的改动，若要保留 r83 的手搓版，说一声即回退。
3. r83 遗留：`ROWS` 仍是占位数据（7 条）；三条已知偏差（滚动条 overlay / 行宽 438 vs 442 / 面板高随视口）。
4. r80–r84 全部未 commit / push。

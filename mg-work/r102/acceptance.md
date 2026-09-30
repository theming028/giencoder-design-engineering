# r102 验收报告 · 会话详情页十一条微调

> **体位**：r101 代**已提交**（`9f252e5`）⇒ 本代**新建** `mg-work/r102/apply102.py`，
> 注入块 id 换代 `r102-conv-css` / `r102-conv-js` / `r102-nav-js`；`GENS` 表扩到**三代**
> （r93 / r101 / r102，三条剥离正则各摘三支、注入只用 r102）。
> 宿主标记 `r93-conv-host` / `data-r93-page` 跨代沿用；`HDR_ID` **保持 `r101-hdr-css`**
> （顶栏图 70% 本轮无改动，继续「摘后重注」维护，无需换名）。
>
> **产物**：`pages/conversation.html` **672845 → 683044**（+10199）、`pages/base.html`
> **472150 → 472150**（+0，只换 nav 脚本 id，长度相同）；其余 4 页（avatar/skills/automation/settings）**未动**。
> **四查**：幂等 ✓（第二遍双「已是目标态」）｜`check-syntax` **10/10**｜
> `verify-design` 与 r101 终态 `vd-r101e.txt` **逐字节相同**（21882 字节，**零新增**）｜
> 1440 + 2560 双视口实测 + 截图目视 ✓
> **代数标记**：真·注入块 `r102-*` 各 1；**历代 id 残留 0**（`r93-conv-*` / `r101-conv-*` 全清）。

---

## 一、十一条逐条实测（1440×900）

| # | 邵先生原话 | 落点 | 实测读数 | 判定 |
|---|---|---|---|---|
| ① | `"r93-t14"` 的字号 13px，**里面的数字要有动效** | `.r93-t14` 字号 + `.r93-num` 结构（CSS + JS） | **字号**：直方图由 `{15px:58, 14px:6}` → **`{13px:58, 14px:6}`**（卡外 58 处全 13；卡内 6 处仍 14，被 `.r93-card.r93-card *` 钉住）。**数字**：全页包出 **13 个 `.r93-num`**；`animation=r93-num-in` / `0.46s` / `delay 1.5s` / `fill both`；**真实时间轴两拍**：骨架屏仍在 DOM 时 `op=0`、`transform=translateY(9.8px)`；+1.4s（骨架屏已移除）`op=1`、`transform=none` | ✓ |
| ② | `r93-fc r93-bt` 右边的箭头间距调整为 **4px** | `.r93-fc .r93-fchev` | hover 态：父级 `gap=4px`、箭头 `margin-left=0px` ⇒ 标题右缘 503 → 箭头左缘 507 = **4px** ✓（`chevOp` 0→1） | ✓ |
| ③ | `r93-fh` 展开有动效，**收起没有，需补充** | `.r93-fb` 的 `max-height` 过渡 + `setFold()`（CSS + JS） | **收起** rAF 逐帧曲线：`222 → 220 → 188 → 162 → 132 → 103 → 78 → 59 → 44 → 33 → 23 → 16 → 11 → 7 → 4 → 2 → 0`（0.32s 全程平滑）。**展开**反向：`0 → 1 → 6 → 16 → 33 → 58 → 89 → 119 → 144 → 163 → 178 → 189 → 199 → 206 → 211 → 215 → 218 → 220 → 222`。终态 `overflow: visible`、`class="r93-fb is-free"`（放行 popover） | ✓ |
| ④ | `r93-t12 r93-nm` 也调整为 **13px** | `.r93-t12.r93-nm` | 2 处（改动汇总表头的 `已压缩 N 条历史记录（约 N tokens）`）**12px → 13px** ✓ | ✓ |
| ⑤ | `r93-iblk r93-i14 r93-cv` 箭头**加大一号** | `.r93-iblk.r93-cv > svg` | svg **10 → 12px**（档位 10→12）；槽仍 `14×14`、`n=14` | ✓ |
| ⑥ | `r93-fh` hover 时后面的小字（`r93-t12l r93-fm r93-ell`）变**正文色** | `.r93-fh:hover` / `.r93-fc:hover` + `.r93-fm` / `.r93-t12l` | **展开头**：`hov=true`、`metaColor=rgb(31,31,31)`（原 `rgb(134,134,134)`）✓。**折叠头**：`hovFc=true`、`metaColor=rgb(31,31,31)` ✓（`metaTxt="str_replace_editor · …"`） | ✓ |
| ⑦ | `r93-asst` 底部线条**浅一级** | `.r93-asst` 的 `border-bottom` | `--color-border-2` → **`--color-border-1`**，实测 `rgb(229,229,229)` → **`rgb(242,242,242)`** | ✓ |
| ⑧ | `.r93-drow` 的 `padding: 0 16px` | `.r93-drow` | 原 `0px 13px 0px 11px` → **`0px 16px`**；文件名左缘 432 → **437**（卡 x421 ⇒ 相对 16）、「⋯」右缘 13 → 16；`gap: 17px`、行高 36 不变 | ✓ |
| ⑨ | `r93-dhead` 左侧 padding 调 **16px** | `.r93-dhead` | 原 `6px 6px 5px 12px` → **`6px 6px 5px 16px`**；图标槽 433 → **437**（相对 16）；表头 40px 定高不变 | ✓ |
| ⑩ | 「滚动到底部」按钮也调**毛玻璃** | `.r93-tobottom`（+ `--r93-glass-h`） | `background: rgba(255,255,255,0)**.72**`、`backdrop-filter: **blur(12px)**`（原 `rgb(255,255,255)` + `bf: none`）；`border-radius` 仍 999px。裁片可见**背后文字被洗淡** | ✓ |
| ⑪ | `.r93-seg…radio-group-button` **总高 28px**、标题栏内**垂直居中** | `.r93-seg .giencoder-radio-button` | 基线高 **34px**（上 8 / **下 2**，不居中）→ **28px**（上 **8** / 下 **8**，真居中）；`btnH=26px`、`btnMinH=26px`、`padding=1px` | ✓ |

---

## 二、三个值得说的技术点

### 1. ⑪ 的坑：`height` 覆盖率了，`min-height` 没覆盖
基线实测 `.r93-seg` 高 **34px** 而页面写的是 `height: 24px` —— 根因是 DS 的
`.giencoder-radio-button { height: calc(32px * ratio); **min-height: calc(32px * ratio)** }`
里 `min-height` **从来没被覆盖**，一直顶在 32px 上。
⇒ 本代把 `height` 与 `min-height` **两条一起**改成 26px（1 + 26 + 1 = 28），
`top: 8px` 不动即 `(44−28)/2 = 8` ⇒ 顺带把「上 8 下 2」的偏心一并修掉。
**教训**：改这类组件的尺寸，先 `getComputedStyle` 读一遍 `height / minHeight / padding` 三项，
别只按「页面写了多少」推算。

### 2. ③ 的坑：同一帧里「写 CSS 变量 + 改属性」会被浏览器合并
第一版实现在**点击那一刻**才写 `--r93-fbh = scrollHeight`，再改 `data-open`。
实测 rAF 曲线：`222 222 222 … 194 120 66 30 8 0` —— **前 230ms 高度纹丝不动**。
根因：两次 style 变更落在同一帧，浏览器只比较「上一帧的计算值」（展开态 = 兜底 4000px）
与「本帧的计算值」（0），过渡从 4000px 起步 ⇒ 前 2/3 时间里 `max-height` 还大于内容高。
试过 `void fb.offsetHeight` **强制 style flush，实测无效**（曲线不变）。
**改对的做法**：把变量在**展开态、字体就绪时提前维护好**（wire 里写 + 1.8s 后再写一次），
折叠时**不写变量**、直接改 `data-open` ⇒ 起点天然是真实值，曲线立刻变成全程平滑。

### 3. ③ 的 `overflow` 取舍：只在过渡期裁剪，稳定后必须放行
`max-height` 收起需要 `overflow: hidden`，但常驻会**剪掉卡内向上翻的 popover**（`.r93-pop`）。
⇒ 拆成「过渡期 hidden + 稳定后放行」：展开落定 360ms 后挂 `.is-free`（`overflow: visible`）；
初始加载时所有折叠块都是展开态，`wire()` 开头统一给它们挂 `.is-free`。

---

## 三、① 的基线 A/B（包装数字有没有挤动排版）

把 `.r93-num` 的 `overflow/vertical-align` 临时内联改回默认，读同一元素的 rect：

| | left, top, w, h | Δ |
|---|---|---|
| 包装态（`overflow:hidden; vertical-align:bottom`） | `574, 1475, 8, 22` | — |
| 撤掉包装样式 | `574, 1475, 8, 22` | **dx=0, dy=0** |

2560 视口复测同样 **dy=0 / dx=0** ⇒ 「`overflow != visible` 的 inline-block 基线会退化」
这个经典坑**被 `vertical-align: bottom` + 与外层同 `line-height` 的组合挡住了**，数字没有偏移。

---

## 四、四查与门禁

| 查 | 结果 |
|---|---|
| 幂等 | 第二遍 **base + conversation 双「已是目标态（无改动）」** ✓ |
| 语法/配平 | `check-syntax.py pages/*.html` → **10/10 ALL_OK** |
| 零影响 | `verify-design.py ./pages` → 与 r101 终态 `vd-r101e.txt` **逐字节相同**（21882 字节，`diff` 空）⇒ **零新增**（warning/critical 均不变） |
| 视觉/像素 | 1440 与 2560 双视口读数一致；裁片 `raw/z102-top.png`（seg 28px 居中）、`raw/z102-pill.png`（药丸毛玻璃，背后文字被洗淡）、`raw/z102-fchover.png`（折叠头 hover：标题+meta 同色正文色 + 右箭头）、`raw/z102-folded.png`（收起后无残留内容） |
| 代数标记 | 真·注入块 `r102-conv-css/js` 各 1（conversation）+ `r102-nav-js` 1（base）+ `r101-hdr-css` 1（6 页）；**历代 id 残留 0** |
| 回滚通路 | `--revert` / `--dry` 分支随 `GENS` 表自动涵盖三代 |

---

## 五、待邵先生拍板（5 条）

1. **① 只改了 `.r93-t14` 本类**：`-m` / `-b` 两个变体仍 15px（全页只有 `.r93-ahd .r93-t14b` 这类少数几处）。
   要与本类一起 13px 说一声。
2. **① 数字动效的覆盖范围** = **全部卡外 `.r93-t14` 里的数字串**（共 13 处），
   包括正文里的数字（如需求采访卡「环境中已装了一个 **5** 泳道…」）。
   若只想让「数值型」（如 `1/3 已完成`）动、正文里的数字不动，说一声 —— 那是另一套筛选口径。
3. **① 的基础延迟 1.5s**：必须 ≥ 骨架屏完整生命周期（1.1s 淡出 + 320ms 移除 = 1.42s），
   否则动效在骨架屏后面白播。嫌慢可以缩骨架屏而不是缩它。
4. **⑩ hover 档**：原 hover 底色是**不透明**的 `--color-fill-1`，改毛玻璃后一 hover 就会「失去毛玻璃」
   ⇒ 换成自造的 `--r93-glass-h`（白度 72% → 86%，仍透+糊），**无设计稿依据**。
5. **③ 的 `overflow: hidden`** 现在常驻在 `.r93-fb` 上（展开稳定后靠 `.is-free` 放行）。
   若将来卡内新增「需要长期溢出显示」的浮层，记得它也在 `.is-free` 生效之前会被裁 360ms。

---

## 六、本轮新踩的坑（→ PLAYBOOK P3.34）

1. **`min-height` 比 `height` 更能顶住**：改组件尺寸前把 `height / minHeight / padding` 三项一起读。
2. **同一帧「写 CSS 变量 + 改属性」会被合并** ⇒ 变量必须**提前维护**（在稳定态写），
   不能在「改变发生的那一刻」才写；`void el.offsetHeight` 强制 flush **实测无效**。
3. **`max-height` 收起动画必须用「精确高度」**：用兜底大值（4000px）会让前 2/3 时间里内容假死。
4. **断言 hover 要用「不被遮挡的」目标**：折叠头中心点可能被同页叠加元素（本例是同文本的另一张 codecard）
   命中 ⇒ `elementFromPoint` 先探一次，或改用其**子标题**做 hover 目标（`:hover` 会冒泡到祖先）。
5. **`.r93-num` 数字包装的基线**：`overflow:hidden` 的 inline-block 会退化基线，
   用 `vertical-align: bottom` + 与外层同 `line-height` 解决，并用「临时内联撤销样式再读 rect」做 A/B 自证。

---
---

# ★ r103 六条（2026-09-30 20:5x）—— **就地返工**（r102 未提交 ⇒ 仍改 `apply102.py`、注入块 id 不变）

> 邵先生原话：
> 1. 「`r93-t14 r93-c1`」这种正文字号默认是 **15px**；
> 2. 「`r93-t14 r93-ell`」这种同类型的字号也是 **15px**；
> 3. 「滚动到底部」按钮的模糊透明度可以**再透一点**；
> 4. 「`r93-agents`」这一行的内容都去掉吧；
> 5. 底部对话框点击时的**激活态的外发光效果的顶部被截断**，需修复；
> 6. 「`r93-fh r93-bt`」这种同类型的**展开折叠效果要一致**，且目前**折叠时会发生闪动**，需修复。

**产物**：`pages/conversation.html` **683044 → 685465**（+2421）、`pages/base.html` **472150（+0）**；
其余 4 页未动。终态 LF `sha 249fbc984716 → a340b6a9e89f`。

## 一、六条逐条实测（1440×900）

| # | 落地 | 实测读数 | 判定 |
|---|---|---|---|
| ① | `.r93-t14` 13 → **15px**（撤销 r102 ① 的字号部分，**数字动效保留**） | 全页 `.r93-t14` 直方图 `{13px:58, 14px:6}` → **`{15px:58, 14px:6}`**（卡外 58 处全 15；卡内 6 处仍 14，被 `.r93-card.r93-card *` 钉住）；`.r93-num` 仍 13 个、`animation: r93-num-in 0.46s` ✓ | ✓ |
| ② | `.r93-t14.r93-ell` 同类型 15px | 35 处 **全部 15px**（`.r93-ell` 只声明 `overflow/text-overflow/white-space`，**不含 font-size** ⇒ 随 ① 自动生效）；`.r93-t14.r93-c1` 2 处也全 **15px** | ✓ |
| ③ | 「滚动到底部」药丸毛玻璃**再透一档** | 新增 `--r93-glass-pill: rgba(255,255,255,0.60)` / `--r93-glass-pill-h: rgba(255,255,255,0.74)`（暗色 `rgba(35,35,36,...)`）；药丸实测 `bg=rgba(255,255,255,0.6)` + `bf=blur(12px)`；**标题栏不动**（仍 `rgba(255,255,255,0.72)`，`--r93-glass` 未改）。A/B 像素（同一滚动位、同一 rect，仅改回 0.72）：药丸内部灰度均值 **235.5（0.60）< 236.2（0.72）** ⇒ 更透 | ✓ |
| ④ | `.r93-agents` 整行退役 | `.r93-agents` / `.r93-cp` 元素 **均不存在**；`.r93-bottom` 由 `{y:593,h:112}` → **`{y:653,h:52}`**，子元素只剩 `.r93-sb`（1 个）。底部整块上移 **60px**，状态条与真实 composer 之间不再有 agent 卡行。⚠ CSS 一族（`.r93-agents` / `.r93-agent*`）**保留未删**（可随时恢复；删掉会让 `--r93-a*-bg` 变未使用变量、可能触发门禁） | ✓ |
| ⑤ | 底部对话框激活态外发光**顶部恢复** | 根因 = 宿主 `.r93-conv-host` 的 `position: relative`（r101 加的）让它从「非定位 flex 项（按 order-modified 顺序 = 在 hero 之前绘制）」变成「**定位后代（按树序绘制）**」，而宿主是 `appendChild` 追加、排在 hero 之后 ⇒ **宿主改绘在 composer 之上**，把它顶部 3px 的光盖掉。修法 = hero 补 `position: relative; z-index: 1`。**中轴 y=702/703/704 实测**：基线 `255,255,255`（无光）→ 修后 **`230,237,253` / `231,238,254` / `231,238,254`**（光恢复）；对照实验：宿主 `overflow:visible` **无效**、宿主 `position:static` **有效**、hero 提层 **有效** | ✓ |
| ⑥ | 折叠开合两态**统一** + 修**闪动** | ① 撤掉 `@keyframes r93-fold-in` 与那条单向 `animation` ⇒ 实测 **14 个折叠块 `animationName !== 'none'` 的数量 = 0**；统一走 `.r93-fb` 的四条 transition（`max-height` / `margin-top` / `opacity` 各 0.32s 标准曲线 + `transform` 0.34s back-out 回弹）。② **闪动根因**：`animation` 会抢占属性、而 CSS Transitions 规定「属性被运行中的动画影响时不启动过渡」⇒ 折叠时动画被移除，`opacity` **一帧硬切**（旧 rAF：t=33 `op=1` → t=134 `op=0`，此时 `max-height` 还停在 150px）⇒ 「内容瞬间消失、空盒子再慢慢收」。修后 rAF 曲线：**收起** `h 150→149→111→89→69→53→40→30→22→16→11→7→4→2→1→0`、`op 1→0.993→0.737→0.596→…→0`、`transform 0 → -1.79 → -6.45 → … → -8`（末段轻微超调后落定 -8）；**展开** 反向 `h 0→1→4→11→24→…→150`、`op 0→…→1`、`transform -8→…→+0.779（超调）→0` ⇒ **两态镜像**。③ 另修一处**陈旧高度**：`--r93-fbh` 在嵌套折叠收起后不更新（实测 fold#10 = `314px` 而真实只有 170px ⇒ 收起前 46% 时长高度不动）⇒ `setFold` 改「本帧写变量 → `requestAnimationFrame` 里再翻 `data-open`」，过渡起点**恒为真实高度** | ✓ |

## 二、本轮两个技术点

### 1. ⑤ 的定性靠「同页 5 组 A/B」，不是猜 `overflow`
第一反应会怀疑 `overflow: hidden`（宿主确实有）。实测**宿主 `overflow:visible` 完全无效**，
而**宿主改成 `position:static` 立刻恢复** ⇒ 立刻锁定是**绘制顺序**而非裁剪。
根因链：`position: relative` 把宿主从 in-flow flex item 提升为 positioned descendant，
而 positioned descendants 按**树序**绘制（`order` 不参与）—— 宿主是后 `appendChild` 的 ⇒ 压住 hero。
**教训**：给宿主加 `position: relative` 会**连带改变绘制顺序**，「谁在谁上面」要重新算一遍。

### 2. ⑥ 的「闪动」= 动画移除不触发过渡
CSS Transitions 有一条例外：**属性正被运行中的 animation 影响时，不启动 transition**
（`animation-fill-mode: both` 会让它「永远在影响」）。
所以「展开用 keyframes、收起用 transition」这套混合写法，在**收起**那一步必然硬切。
⇒ 要么两态都用 animation（那另一向又会硬切），要么**两态都用 transition**（本轮选择）。
好处是顺带把「单向」变成「镜像」，正好满足「效果要一致」。

## 三、四查与门禁（终态）

| 查 | 结果 |
|---|---|
| 幂等 | 第二遍 **base + conversation 双「已是目标态（无改动）」** ✓ |
| 语法/配平 | `check-syntax.py pages/*.html` → **10/10 ALL_OK**（conversation `script=9 style=16`） |
| 零影响 | `verify-design.py ./pages` → 与 r101 终态 `vd-r101e.txt` **逐字节相同**（17148 字符 / md5 `84f552c5b5a6` / `diff_exit=0`，76 条 = 66 warning + 10 info + 0 critical）⇒ **零新增**（`ev/vd-r103a.txt`） |
| 双视口 + 暗色 | 2560：药丸 `0.60` + `blur(12px)`、标题栏 `0.72`、`.r93-t14` `{15:58,14:6}`、`seg` 28px、agents 已无、hero `z=1`、折叠 `hasAnim=0`；1440 暗色：药丸 `rgba(35,35,36,0.6)`、标题栏 `rgba(35,35,36,0.72)`、其余同 ⇒ **全一致** |
| 视觉 | `raw/h103-1440.png`（agent 行已消失、状态条直接接 composer）、`raw/g103-focus-1440.png`（发光顶部完整）、`raw/k103-A60.png` vs `k103-B72.png`（药丸透明度 A/B）、`raw/i103-2560.png` / `i103-dark-1440.png` |

⚠ **`style=16` 不是回归**：对 HEAD（r101 交付态）跑同一脚本同样是 `style=16`
（`<style rel="stylesheet" crossorigin>` 是外壳 bundle 里的既有产物，`<style` 字面量共 16 处）。
此前 r102 验收里写的「style=15」是笔误，**以本表为准**。

## 四、待邵先生拍板（r103 新增 2 条）

1. **③ 透明度取 0.60**：比 0.72 明显更透，但「再透一点」是主观量 —— 想更透（如 0.5）说一声，
   `--r93-glass-pill` 一行即可调。**标题栏仍是 0.72**（它是横贯整条 44px 的压顶容器，透太多糊不住滚过的内容）；
   若希望两者一起变，也只需把 `.r93-bar` 的 `background` 改成 `var(--r93-glass-pill)`。
2. **④ 摘掉 agents 行后**底部整块上移 60px，状态条与 composer 之间现为 **44px** 空档
   （= `.r93-bottom` 的 12px 下内距 + 外壳 `div.mt-8` 的 32px）。觉得偏松可以再压。

（r102 遗留的 5 条待拍板仍见本文件第五节。）


---

# r104 四条（2026-09-30 21:2x~22:0x · 会话详情页）—— **就地返工**

**体位**：r102 + r103 **均未提交** ⇒ 仍改 `mg-work/r102/apply102.py`，注入块 id 不变
（`r102-conv-css` / `r102-conv-js` / `r102-nav-js`），**不另起代数**。

**邵先生原话（四条）**：
> 1. 底部对话框的所有弹出的浮窗（技能列表浮窗、大模型下拉菜单等）**都被遮挡了**，他们的**层级**应该是最高的；
> 2. **刷新页面后，在骨架屏显示之前总会有对话框出现**，但是不应该出现；
> 3. **对话和轨迹 tab 切换时需要有滑动动效**，且**切换到轨迹页面后，不应该再显示底部的对话框**；
> 4. 完成上述任务后进行**全局全要素的代码审查**（冗余 / 命名规范 / 是否引用 GienCoder 设计系统要求的规范与组件 /
>    token 变量命名方式是否统一），**大前提是务必保证整个产品的质量和稳定性**。

**产物**：`pages/conversation.html` **685465 → 691648**（+6183；LF `sha a340b6a9e89f → 05b899bd4366`）、
`pages/base.html` **472150（+0）**；其余 4 页未动。

## 一、四条逐条落地与实测（1440×900 为主，2560 + 暗色复核）

| # | 落地 | 实测读数 | 判定 |
|---|---|---|---|
| ① | **宿主 `.r93-conv-host` 补 `z-index: 0`**（与 hero 的 `z-index: 1` **成对存在**，**不动 hero** ⇒ r103 ⑤ 的外发光保住） | 根因 = r103 ⑤ 给 hero 加的**正 z-index 创建了层叠上下文**，而 composer 的所有浮窗（`.giencoder-select-popup` z1000 / 技能浮窗 z9999 …）都是 hero 的**定位后代** ⇒ 它们被整体**封顶在 hero 这一层（=1）**，反而落到宿主内部数值更小的 `.r93-tbsticky` 3 / `.r93-sk` 9 / `.r93-bar` 10 **之下**。实测（1440，点开模型下拉）：下拉 rect `{x1039,y594,w202,h216}` 与 `.r93-tbsticky::after` 渐隐带（`y597~653`，z3）重叠 ⇒ 第 2/3 项「GLM-5.2-公司共用 / 异常不能用的大模型」被白渐变洗掉。**修后像素 A/B**（第 2 项行 `box=(1070,634,1250,664)`）：暗像素(<160) **122 → 383**、均值 **249.7 → 240.7**。**2560 复核**：下拉 `{x1739,y1134,w202,h216}`、`z=1000`，**6 项全部完整可见**（第 3 项「异常不能用的大模型」是**禁用态灰字**，故暗像素为 0 属正常） | ✓ |
| ② | **`.mt-8` 首帧守卫**：默认 `opacity: 0; pointer-events: none`，由 `data-r93-app='ready'` 放行 | 外壳是 `<head>` 里的 `type="module"` 脚本（**延迟执行**），注入的样式表在文档尾 —— 两者**都在首次绘制之前**解析 ⇒ 只要默认 `opacity: 0`，「React 先画对话框、骨架屏后到」那个窗口**从根上不存在**（不靠时序抢跑）。放行 = JS 在**骨架屏退场同一拍（1100ms）**写 `document.documentElement.setAttribute('data-r93-app','ready')`，**刻意独立于 `if (sk)`**（骨架屏节点缺失也不能把对话框永久锁死）。**1440 首帧实测**：`app=null, sk=true, box.op=0, box.pe=none` → 就绪 `app=ready, box.op=1, pe=auto, sk=false`；**2560 复测同值**。用 `opacity` 不用 `display`（保占位、零重排）；`pointer-events: none` 是必须的（否则能点出「凭空出现的下拉」） | ✓ |
| ③ | **滑动交接 + 轨迹页收起对话框**：`data-r93-slide` 四态 + `r93SetTab()` 交接时序；轨迹页额外把 hero `display: none` | 状态用**正交两维**：`data-r93-app`（loading ⇄ ready）× `data-r93-tab`（chat ⇄ trace），只有 **`ready + chat`** 才显对话框。交接 = 「旧 pane 先滑干净（`R93_SWAP = 220ms`）→ 改高度 → 新 pane 滑入」，**高度突变那一拍画面里恰好没有内容**（新 pane 还是 `in-*` 的 `opacity: 0`）⇒ 看不到跳。**逐帧实测（去轨迹）**：`chat opacity 1 → 0.85 → 0.69 → … → 0.11`、`translateX 0 → -18.4`；`t803` 交接时 `heroD=none, hostH 656→842`、`box.op 1→0`，随后 `trace` 从 `translateX 22 → 0.008` 淡入；回对话镜像（`chat` 从 `-22 → 0`、`box.op 0.02→1`）。**切到轨迹后对话框 rect `{0,0,0,0}`（已消失）**；**2560**：`heroDisp=none, hostH=1382, boxRect=[0,0], tab=trace`，页签「轨迹」为选中态（蓝字 + 药丸） | ✓ |
| ⑤ 回归 | r103 ⑤ 的外发光**未被 ① 破坏** | 中轴 y702/703/704 = `(230,237,253)` / `(231,238,254)` / `(231,238,254)`、y705 描边 `(160,186,247)` —— **与 r103 终态逐字节相同** | ✓ |

## 二、① / ⑤ 为什么能两全（本轮最关键的一次定性）

r103 ⑤ 的结论是「hero 必须提层」（否则激活态外发光被宿主盖掉），r104 ① 的现象是「浮窗被宿主内部压住」——
看起来互斥。**实测 A/B 证明两者并不冲突**：浮窗被封顶的**真凶是宿主自己**（它把 hero 整块降成一个 0 成本上下文，
内部 3/9/10 才爬不出来）。所以：

* 修法**不去动 hero**（保住 ⑤），只在**宿主**上补 `z-index: 0` ⇒ 宿主内元素**再也压不到 hero / composer 之上**。
* 两处**必须成对存在**：单独拿掉任一条，另一个问题就复发。
* **副作用（已记录）**：宿主内任何元素都不能再「越过」hero 或 composer 去遮挡 —— 这正是我们想要的语义。

## 三、④ 全局全要素代码审查

只读扫描器 `mg-work/r102/ev/audit104.py`（六组：A 硬编码色 / B `var()` 引用完整性 / C `--r93-*` 命名一致性 /
D 冗余 / E 命名规范与 DS 复用 / F 稳定性断言），产出 `ev/audit104.log`。**发现并采纳 7 项修正**：

| # | 问题 | 严重度 | 修正 |
|---|---|---|---|
| 1 | `data-open` 未做命名空间化（全页已有 81 处 `data-r93-*`） | P2 规范 | 全文替换为 **`data-r93-open`**（23 处） |
| 2 | 3 处**字面 hex** 与 DS 色阶**逐字节同值**（`#D25F00` = orange-7 / `#30953B` = green-7 / `#6B6B6B` = gray-7） | P1 规范 | 改引色阶 `rgb(var(--orange-7))` / `rgb(var(--green-7))` / `rgb(var(--gray-7))`，**计算值逐字节不变** |
| 3 | 2 处 `box-shadow` 用字面 `rgba` | P2 冗余 | 提为 `--r93-sh: 0 4px 8px 0 rgba(0,0,0,0.08)` / `--r93-sbsh: 0 2px 9px rgba(0,0,0,0.07)`（浅暗同值、只声明一次） |
| 4 | **暗色档缺 3 条**——最严重的是 `--r93-ioc: #333333` 压在 `#232324` 上 = **隐形图标** | **P1 质量** | `[giencoder-theme='dark']` 补 `--r93-ioc: rgb(var(--gray-10))` / `--r93-dim: rgb(var(--gray-4))` / `--r93-tag-ic: rgb(var(--orange-6))`；并删掉 `--r93-warn-ic/-ok/-ioc2/-meta/-sb/--r93-glass-h/--r93-a*-*` 的重复声明（改随主题自动翻转） |
| 5 | 僵尸变量 `--r93-blue` / `--r93-sb` / `--r93-glass-h`（全页零引用） | P2 冗余 | 删除（各留说明注释） |
| 6 | **死代码一族**：`.r93-agents` / `.r93-agent*` / `.r93-a*` 20 条规则 + 15 个变量（≈2.3 KB） | P2 冗余 | 整族删除（r103 ④ 摘 DOM 时「CSS 保留」的理由是「删了会让 `--r93-a*-bg` 变未使用变量、可能触发门禁」；r104 ④ 采取**变量与规则同进同出**，该理由不成立） |
| 7 | 「按需自补 DS 组件 CSS」是否为缺陷 | — | **判定为非缺陷**：这是本工程**既有手法**（页面 bundle 里早已内联 DS 全套组件 CSS，缺失部分按需补），r102 起一直如此 |

**修正后复核**：
* `agentsCSS = 0`（`document.styleSheets` 里 agent / cp 规则数）
* 浅色 `--r93-ok = rgb(48,149,59)`、`--r93-warn-ic = rgb(210,95,0)`、`--r93-ioc2 = rgb(107,107,107)` —— **与改前逐字节相同**
* 暗色 `--r93-ok = rgb(127,209,132)`、`--r93-warn-ic = rgb(255,182,93)`、`--r93-ioc = rgb(247,247,247)`、
  `--r93-ioc2 = rgb(201,201,201)`、`--r93-tag-ic = rgb(255,154,46)`、`--r93-dim = rgb(107,107,107)`、
  `--r93-meta = rgb(134,134,134)`
* `sbShadow / tbShadow / popShadow` 三条计算值与改前相同

## 四、稳定性回归扫查（r104 收尾）

| 项 | 结果 |
|---|---|
| **折叠块开合往返**（14 块） | 全部 **收起 → 展开 → 回到初始** 成功；`scrollHeight` 逐块比对 **14/14 OK**（含嵌套块 #10：收起时 `314 → 170` 的**实时重算**、展开回 `314`） |
| 探针自伤（已澄清） | 早期 `p104k/p104l` 报「第 2 次点击无效」= **探针把自己坑了**：每轮把标签打在「当前可见头」时，**旧标签仍留在隐藏的 `.r93-fh` 上** ⇒ `[data-p104l="1"]` 命中两个元素，真鼠标点了 DOM 靠前的那个 `display:none` 元素（rect 归零）。改用唯一 `.r93-fc` 后**一次成功**；另用 `eval` 直接派发验证 handler 本身无缺陷（收起 → 展开 → 复原） |

## 五、四查与门禁（终态）

| 查 | 结果 |
|---|---|
| 幂等 | 第二遍 **base + conversation 双「已是目标态（无改动）」** ✓ |
| 语法/配平 | `check-syntax.py pages/*.html` → **10/10 ALL_OK**（conversation `script=9 style=16`） |
| 零影响 | `verify-design.py ./pages` → 与 r101 终态 `vd-r101e.txt` **逐字节相同**（17148 字符 / md5 `84f552c5b5a6` / diff lines 0）⇒ **零新增**（`ev/vd-r104b.txt`、`ev/vd-r104c.txt`） |
| 双视口 + 暗色 | **2560**：`hostZ=0 / heroZ=1`、`app=ready / boxOp=1 / pe=auto`、`.r93-t14` `15px`、`.r93-pill` `15px/rgb(52,145,250)`、下拉 6 项全可见、轨迹页 `heroDisp=none / hostH=1382 / boxRect=[0,0]`；**2560 首帧**：`app=null, sk=true, boxOp=0, boxPe=none` → 就绪 `app=ready, boxOp=1, pe=auto`；**2560 暗色**：`--r93-ioc=rgb(247,247,247)`（改前 `#333333` = 隐形）、`--r93-ok=rgb(127,209,132)`、`--r93-warn-ic=rgb(255,182,93)`、`--r93-tag-ic=rgb(255,154,46)`、`--r93-dim=rgb(107,107,107)`、`--r93-meta=rgb(134,134,134)`、`--r93-line=#333335`、`--r93-pillc=#6BA6FF`；暗色下拉底色 `rgb(95,95,96)` = **DS `--color-bg-5`（暗色档 `#5f5f60`）**，**不是缺陷**（bg-1→bg-5 为 `#17171a / #232324 / #2e2e30 / #484849 / #5f5f60` 的单调色阶） |
| 视觉 | `raw/z2560-pop.png` + `c2560-pop.png`（浅色下拉 6 项完整）、`raw/z2560-dark-pop.png` + `c2560-dark-pop.png`（暗色下拉可读）、`raw/z2560-trace.png` + `c2560-tabs-trace.png`（轨迹页无对话框、页签选中态）、`raw/z2560-dark.png`、`raw/f2560-early.png` |

## 六、待邵先生拍板

**r104 无新增待拍板项**。r103 遗留 2 条（③ 药丸透明度 0.60、④ 摘行后 44px 空档）与 r102 遗留 5 条仍见上文。

**状态**：🚫 **未提交**（r102 十一条 + r103 六条 + r104 四条 = **同一次交付**；等邵先生发话 commit / push）。


---

# r105 三条（2026-09-30 深夜 · 会话详情页 + 8 个独立页）—— **就地返工**

> **体位**：r102 / r103 / r104 **均未提交** ⇒ 本代**就地返工**，仍改 `mg-work/r102/apply102.py`
> （现 **163605 字符 / 220815 字节**），注入块 id **不变**（`r102-conv-css` / `r102-conv-js` / `r102-nav-js`），
> **不另起代数**、不新建 `apply105.py`。静态片段走**新增** `mg-work/r102/part105/` 四件
> （`browse.css` / `browse.html` / `browse.js` / `ctrl-conv.js`），在 `inject_tail` 里拼进同一次注入。
>
> **产物**：`pages/conversation.html` **691648 → 793028**（② **+2173**、③ **+99207**）；
> `pages/base.html` **472150（+0，本轮未变）**；其余 **8 页各 +714**（同一块 `r102-nav-js`）。
> **四查**：幂等 ✓（第二遍双「已是目标态」）｜`check-syntax pages/*.html` **10/10 ALL_OK**
> （conversation `script=9 style=16`）｜`verify-design ./pages` 与基线 `vd-r101e.txt`
> **逐字节相同**（17148 字符 / md5 `84f552c5b5a6`）⇒ **零新增**｜1440 + 2560 + 暗色实测 + 截图目视 ✓。

## 一、三条逐条实测

| # | 邵先生原话 | 落点 | 实测读数 | 判定 |
|---|---|---|---|---|
| ① | 在任何其他独立页面点击会话任务**都要能跳转到 `conversation.html`** | 把 `base.html` 里已有的 `r102-nav-js` 扩到**其余 8 页**（`nav_patch` → `invert_if_absent`） | 真鼠标点击：`base` / `avatar` / `automation` / `skills` 均 **`file:///…/conversation.html`** ✓。**负例**：点 aside **分组标题**、点**「新会话」按钮** → 两例均**留在原页** ✓。`task-detail` 的壳 `aside` 实为 `display:none`（rect `[0,0,0,0]`，可见左栏是 `.td-left` 任务面板、**无会话列表**）⇒ **无对象，非缺陷**；`kanban`（筛选面板）/ `settings`（设置导航）aside **无会话项**；`dev` / `req-kanban` **无 `<aside>`** —— 5 页均**无对象**。各页 nav 块**各 1 块**，`conversation.html` **0 块**（自身不需要） | ✓ |
| ② | `"r93-seg giencoder-radio-group giencoder-radio-group-button"` 切换要有**滑动动效** | 改用 **DS 官方滑块** `.giencoder-radio-button-slider`（DS `components.css` 本来就带 `transition: transform .28s, width .28s`，且**已在页面内联**）；HTML 加滑块 span、CSS 让滑块承担白底/描边、JS `r93SegMove()` 写行内几何 | **逐帧**（rAF 采样）：`0 → 38.79(82ms) → 49.58(148ms) → 51.75(215ms) → 51.999(282ms) → 52(348ms 稳定)`，**宽恒 52**；反向点回「对话」**镜像回 0** ✓。根因：当年页面把 `.giencoder-radio-button-checked` **自绘**成白底 + 描边 ⇒ **位移没有载体**、只能硬切 | ✓ |
| ③ | 「`r93-bar`」右侧按钮**替换为「全屏」和「打开侧栏」**，即数字分身的 `td-right-acts` | ①按钮本体逐字对齐 `.td-right-acts`（`giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon` + `.r93-baract`），原单枚 `.r93-morebtn`（⋯，**本来无任何行为**）**整枚退役**；②全屏 = `<html data-r93-full='1'>` ⇒ 左导航收拢 0、对话区吃满；③「打开侧栏」= 数字分身 **AV-BROWSE-SLOT v1** 三件套**整块移植** | **③a**：rect `[1359,57,64,28]`（两枚 28×28 + gap 8，右缘 1431 = bar 右缘 − 8）｜`border-color rgba(0,0,0,0)`、`border-radius 8px`（随 DS）、hover `rgb(247,247,247)`、图标 **14px**。**③b** 1440：`aside 256 → 0`、`main 1164 → 1420`、`icoMax none / icoMin flex`、`aria-label 全屏 → 退出全屏`；2560 **同构** ✓。**③c**：点开 ⇒ `aside 0 / main 779 / split [791,48,9,844] display block / pane 641`；右键菜单 rect `[1000,400,182,227]`、**12 项**、`data-td-ctx-open`；文件树 **28 行**、点目录 `is-closed` + **27 行 `is-hidden`**；拖分栏条 **641 → 701px** 并落盘 `{"panelW":701}`；关闭按钮**完全复原**。**③d** 暗色（源页没有，本模块**首次落到有暗色分支的页面**）：`panelBorder rgb(78,78,78)`、`codeKey rgb(86,156,214)`、`panelBg rgb(23,23,26)`；**浅色档逐字节不变** | ✓ |

## 二、三条的关键实现

### ① 扩展而非重写
同一块 `r102-nav-js`（**捕获阶段**委托 `document.addEventListener('click', …, true)` —— aside 是外壳 React 渲染的、拿不到它的 onClick，先例 r86/r88）。
`nav_patch` 统一走 `invert_if_absent`：**内容一致 ⇒ 一字不动、只保位置**；不同 ⇒ 原地替换；不存在 ⇒ 追加。
这正是修掉「两块都往 `</body>` 前追加、每遍报『改了』」那个幂等瑕疵的同一把刀。

### ② 三处手势 + 四处重定位
* **首帧不播动画**：`.r93-seg` 带 `data-r93-seg-init="0"` ⇒ 该态下 `transition: none`（否则滑块会从 **0 宽「长」出来**）；JS **两帧后**摘掉该属性放开过渡。
* **四处重定位**：页签 `click` / `document.fonts.ready` / `window.resize` / **1200ms 兜底**（字体晚到 ⇒ `offsetWidth` 会变）。
* 滑块几何 = `width: offsetWidth`、`translateX: offsetLeft − 1`；`checked` 改 `background: transparent; border: 0`（**只留文字色与字重**）。

### ③ 三层结构
1. **按钮**：⚠ `border-color: transparent` **必须写**（avatar 的 `.td-round-btn` 就是靠它去掉 DS 默认描边的）；**圆角不覆盖**，随 DS **8px**；图标三枚 `fsmax` / `fsmin` / `panel` **逐字取自 avatar**（24 网格 / stroke-width 2）。两枚图标**共用一枚按钮**，靠 `html[data-r93-full='1'] .r93-baracts .r93-ico-max/-min` 切显隐（选择器**带前缀**是为胜过 `.r93-iblk { display: inline-flex }`，避免同特异性靠顺序取胜）。
2. **全屏**：做法与浏览态**完全同款** —— `width: 0 !important; min-width: 0 !important; padding-*: 0 !important; opacity: 0; pointer-events: none`（外壳给 aside 的宽度是 React **内联** style ⇒ 必须 `!important`；它自带 `overflow: hidden`）。
3. **预览栏**：挂载 = `hostRow.insertBefore(splitMain, hostMain.nextSibling)` + `insertBefore(slot, splitMain.nextSibling)`（`hostRow` = `div:has(> main)`）。宽度变量 `--av-browse-w`（**默认 641**，`MIN_PANEL 561`、`MAIN_MIN 380`）；记忆 key 换成 **`giencoder:r105-browse:v1`**（与数字分身**分开**）。
   ▲ **Esc 裁决链**（本轮新增第 ③ 级）：右键菜单 → 预览栏 → **全屏**，每级 `stopImmediatePropagation`。
   ▲ 第 ③ 级**不直接改 `<html data-r93-full>`** —— 状态由 r102 主脚本持有（它还要翻按钮 `aria-pressed`/`title`/`aria-label` 并派发 `resize`）；控制器**比主脚本更晚注册**，直接调函数会**反序** ⇒ 走自定义事件 **`r93:fullscreen`**（主脚本 `document.addEventListener('r93:fullscreen', …)`）。

### ③-d 补的「暗色档」
`browse.css` 有 **7 个字面 hex**，全部是**自定义属性定义**。源页 avatar / task-detail **都没有**本模块暗色分支，但本模块**第一次落到有暗色分支的页面**（conversation r93 一族全量做了暗色）⇒ 按 PLAYBOOK 规则 5 **必须补**。
不补的实测后果：面板外缘线 `#ECEEF2` 成**亮框**、代码主色 `#0451A5` 对 `#17171a` 对比度 ≈ **2.0**（远低于 4.5）、激活行 `#ECF2FF` 成**整块白**。
修法只覆盖那 **7 个自定义属性**、**不动几何**（源件保持**逐字不动** ⇒ 同源校验仍成立）：`--td-panel-line: rgb(var(--gray-3))`；`--td-code-key/str/num: #569CD6 / #CE9178 / #B5CEA8`（VSCode **Dark+** 同位置三色）；激活行 `rgba(var(--blue-7), .20) / rgba(var(--blue-7), .38)`；`--td-crumb-line: var(--color-border-1)`。

### 注入体位与守卫
CSS 进 `r102-conv-css`、JS 进 `r102-conv-js`、**HTML 作为同一次 `inject_tail` 的静态片段**（与 avatar 同体位：样式表之后、脚本之前）。
`apply102.py` 新增守卫：三件里出现 `<script` / `</script` / `<style` / `</style` **一律 `sys.exit`**（会打乱 `<script>` 计数断言 / 提前闭合标签）。

## 三、四查终态

| 项 | 读数 |
|---|---|
| 幂等 | ✓ 第二遍双「已是目标态」（`conversation.html` sha 不变） |
| JS/CSS 语法 | `python mg-work/check-syntax.py pages/*.html` ⇒ **10/10 ALL_OK**（conversation `script=9 style=16`） |
| 设计回归 | `python verify-design.py ./pages` 与 `ev/vd-r101e.txt` **逐字节相同**（17148 字符 / md5 `84f552c5b5a6`）⇒ **零新增** |
| 死代码 | `r93-morebtn` 全仓 **3 处、全在注释**（活规则 0 条） |
| 终态 | `pages/conversation.html` **793028** / sha `e67474395502`；`pages/base.html` **472150（+0）** |

## 四、本轮探针与裁片（`mg-work/r102/`）

* **探针** `ev/`：`extract105.py`（抽取三件套并与 r69 存档比对）｜`p105a/b.sh`（骨架 / avatar 侧栏几何）｜`p105c/d.sh`（跳转实测 / 9 页 aside 普查）｜`p105e/f.js` + `p105f.sh`（按钮 / 侧栏 / 全屏**五态**）｜`p105g1.js` + `p105g.sh`（**滑块逐帧** + 按钮态）｜`p105h.sh`（2560 + 暗色）｜`p105i.sh`（**逐页跳转 + 负例**）｜`p105j.sh`（预览栏自身交互：菜单 / 树 / 拖拽 / 关闭）｜`vd-r105a.txt` / `vd-r105b.txt`（均与基线 **IDENTICAL**）｜`p105-tokens.log`（浅暗两档色阶读数）。
* **裁片** `raw/`：`x105-0-init.png` / `x105-0b-init.png` / `y105-btn.png` / `y105-btn2.png` / `x105-1-browse.png` / `x105-2-both.png` / `x105-3-fsonly.png` / `x105-4-ctx.png` / `y105-ctx.png` / `z2560-browse.png` / `z2560-browse-fs.png` / `z2560-dark-browse.png` / `z1440-dark-105.png` / `y105-avatar.png` / `y105-avatar-btn.png`。
* **新增源件** `part105/`：`browse.css` **15937**｜`browse.html` **31688**（静态片段，3 行：头/主体/尾）｜`browse.js` **47410**（**只用前半段** 31498，切分点 `\n(function () {\n  var KEY`）｜`ctrl-conv.js` **15465**（本页控制器，**按本页布局改写**）。

## 五、待邵先生拍板

**r105 三条本身均已落地**，下面 3 条是**顺手替他做的判断**，请确认要不要改口径：
1. **全屏 = 收拢左导航**（`aside → 0`、对话区吃满整行），与数字分身全屏「让 main 让位」**同语义** —— 若希望全屏时保留一条**可点回来的窄条**（如 0 → 12px 抓边），说一声即改。
2. **预览栏默认宽 641**（沿用数字分身），本页内容更宽 ⇒ 若希望本页另给一个默认值（如 720），可单独调。
3. **预览栏与「全屏」可同时开**（实测 `x105-2-both.png`：aside 0 + 预览栏在右侧）—— 若希望二者**互斥**（开全屏自动收预览栏），说一声即改。

r103 遗留 2 条（③ 药丸透明度 0.60、④ 摘行后 44px 空档）与 r102 遗留 5 条仍见上文。

**状态**：🚫 **未提交**（r102 十一条 + r103 六条 + r104 四条 + r105 三条 = **同一次交付**；等邵先生发话 commit / push）。

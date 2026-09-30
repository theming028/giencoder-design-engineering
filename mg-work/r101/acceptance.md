# r101 验收报告 · 会话详情页线上宿主十一条微调

> 载体：`pages/conversation.html` 的 `.r93-conv-host`（会话详情独立页）。
> 补丁：`mg-work/r101/apply101.py`（幂等可复跑）。
> ⚠️ **体位**：r93 代**已提交**（`d7e2151`）⇒ r101 是**新一代**，新建 `mg-work/r101/apply101.py`；
> 但页面里仍留着 r93 的三块注入物 ⇒ 脚本用 **`GENS` 逐代摘除表**（r93 + r101 一起摘），注入用本代 id。
> 设计稿：MasterGo `193158744355579` · `page_id=fw647:12809` · `layer_id=1393:18748`。

---

## 一、十一条 → 落点 → 实测读数（1440×900，`ev/p101fin.log`）

| # | 需求（原话要点） | 落点 | 实测（**终态**） |
|---|---|---|---|
| ① | `r93-fh r93-bt` 这类容器再 hover **不显示浅灰背景色**，图标和文字变成正文颜色即可 | CSS：删 `.r93-fh:hover{background:fill-2}` / `.r93-fc:hover{background:…}`；改 `{background:transparent}` + 新增 `.r93-fc:hover, .r93-fc:hover .r93-c3, .r93-fc:hover .r93-t14{color:text-1}`、`.r93-fh .r93-cv{color:text-1}` | ★ **决定性读数**（探针直接查 `matches(':hover')`，不再靠「透明=没生效」猜）：<br>展开头 `hov=true` / `bg=rgba(0,0,0,0)` / `color=rgb(31,31,31)` / `ico=rgb(31,31,31)` ✓<br>折叠头 `hov=true` / `bg=rgba(0,0,0,0)` / `color=ico=t14=rgb(31,31,31)` ✓ |
| ② | `r93-t12l` 的文字颜色要「浅两级」 | CSS：`.r93-t12l` 补 `color: var(--color-text-3)` | 「深度思考」正文由 `rgb(31,31,31)` → **`rgb(134,134,134)`** ✓（全页 `.r93-t12l` 唯一因此变色的 1 处；其余 18 处本就被后写规则定为 text-3） |
| ③ | `r93-ib` hover 底色不对，**不要边框** | CSS：`.r93-ib:hover{background:var(--color-fill-2)}`（撤掉 r99⑨ 的白底 + `inset 0 0 0 1px` 内描边） | hover `hov=true` / `bg=rgb(242,242,242)` / **`sh=none`** ✓ |
| ④ | 折叠箭头（`r93-iblk r93-i14 r93-cv`）图标偏大 | CSS：`.r93-iblk.r93-cv > svg{width:10px;height:10px}` —— **只缩 svg，槽仍 14×14** | `slot=[420,433,14,14]` / `slotW=14px` / `svgW=10px` / `svgRect=[422,435,10,10]` ✓；**折叠前后标题左缘 `dx=0`**（`ftX=438 → labelX=438`）✓ |
| ⑤ | 去掉 Bash 卡头那枚绿勾 | JS：`fold()` 的 Bash 分支删掉 `<span class="r93-iblk r93-i14 r93-okc">` | `.r93-okc` 全页 **2 → 1**；`okcInBash=0` / `copyInBash=1`（复制按钮完好）；`headText="launch-rootls -la …"` ✓ |
| ⑥ | `.r93-pane` 与底部对话框相切处要**渐隐** | CSS：`.r93-tbsticky::after`（40px `linear-gradient(to bottom, transparent, var(--color-bg-2))`，`bottom:-44px` / `z-index:-1`） | `content:'""'` / `pos=absolute` / `h=40px` / `bottom=-44px` / `z=-1` / `bg=linear-gradient(rgba(0,0,0,0), rgb(255,255,255))`；`tbsBox=[279,549,1142,0]`；滚动口 `[269,93,1162,500]`、`pillOn=true` ✓<br>像素验证（`r101-fin-fadezoom.png`）：滚动口最下 ~2 行文字线性收干净 ✓ |
| ⑦ | 「任务产物」卡支持**右键菜单**（= AI 对话框右栏 `td-browse-slot` 那一套） | JS：`OW_ITEMS`/`FCTX_ITEMS`/`buildFMenu`/`openFM`/`closeFM`/`runF` + `host.addEventListener('contextmenu', …closest('.r93-artcard')…)`；CSS：`.r93-ctx*` 约 20 行适配层 | `labels=["打开","打开所在文件夹","添加到对话","添加到 GienCoder","复制路径","打开方式"]`、`arrows=[F,F,F,F,F,true]`、`divider=1`、`menuBox=175×218`、`rowPad=5px 8px`、`rowFs=14px`、`icoW=14px`；子菜单 `open=true` / `box=175×207` / `labels=["VS Code","Trae","Google Chrome","Microsoft Edge","Notes","文件资源管理器"]` ✓（`r101-fin-ctx.png` 目视：主菜单 + 子菜单 + 右向箭头 + 彩色品牌图标全对） |
| ⑧ | 「压缩上下文」前面的图标**转起来** | CSS：`@keyframes r93-spin{to{transform:rotate(360deg)}}` + `.r93-spin{animation:r93-spin 1.2s linear infinite}`；JS：该图标补 `r93-spin` 类 | `anim=r93-spin` / `dur=1.2s` / `state=running` / `cls="r93-iblk r93-i14 r93-c3 r93-spin"` ✓ |
| ⑨ | 折叠头 meta 与「调用 N 个工具」汇总值字号 12 → **13px** | CSS：`.r93-t12l.r93-fm.r93-ell, .r93-sumrow .r93-t12l{font-size:calc(13px*var(--ui-fs-ratio))}` | `.r93-t12l` 字号直方图 **`{13px:17, 14px:1, 15px:1}`** —— 非 13 的两处**都是刻意的**：「深度思考」正文 14px（由 `.r93-card` 钉死）+「任务产物」标签 15px（由 `.r93-artlabel` 定）⇒ 17/19 全部归位 ✓<br>（★ 首版只改 `.r93-fm.r93-ell`，实测卡内 `deepwiki / 1/3 已回答 / 0/5 已完成 / gienx-taskboard-` 4 处仍 12px、与折叠头 13px **同卡混档** ⇒ 扩到 `.r93-sumrow .r93-t12l`） |
| ⑩ | `.r93-sb`（状态条）少了投影 | CSS：`.r93-sb` 补 `box-shadow: 0 2px 9px rgba(0,0,0,0.07)`（**不照搬 DS token**，见 2.3） | `sh="rgba(0, 0, 0, 0.07) 0px 2px 9px 0px"`；状态条 `box=[420,593,860,40]` / `bd=rgb(229,229,229)` ✓<br>像素剖面（`r101-fin-sb.png`，全宽平均，rel+1..+10）**`244 245 247 248 250 251 252 253 254 254`** vs 设计稿 `244 245 246 248 249 251 252 253 254 255` ⇒ **Σ\|Δ\| = 3** ✓ |
| ⑪ | 进入页面时「对话内容模块」要显示**骨架屏 Skeleton** | 复用 DS 已编译进本页的 `.giencoder-skeleton-line/-title/-avatar`；CSS `.r93-sk*`；JS：`SKEL` 模板 + `wire()` 里 1.1s 后加 `.is-out`、再 320ms 移除 | t≈350ms：`n=1`、`box=[269,93,1162,612]`（= `.r93-pane` 同框同轴）、`z=9`、`bg=rgb(255,255,255)`、`lines=8 / titles=1 / avs=1`、`lineAnim=giencoder-skeleton-loading 1.4s`、`innerW=860 = wrapW=860` ✓<br>t≈2000ms：**`n=0`**（已移除）✓<br>目视 `raw/r101-sk-on.png`：右侧整块灰条骨架（2 条右对齐气泡 + 头像/标题 + 3 条正文 + 灰卡）✓ |

---

## 二、设计稿取数（本轮新增的权威结论）

### 2.1 ② 的取数：**「浅两级」是邵先生的主动下调，不是还原设计稿**

量设计稿「深度思考」卡（祖先链 `1393:18487 容器 188` left18/top34/822×200，在 `1393:18489 容器 190`(left164/top592) 内 ⇒ 绝对 `board(182,660)`；脚本 `ev/sample_t12l.py`）：

卡内深色像素 Top 命中：`(138,138,139)×1523`、`(191,192,193)×1279`、`(84,84,84)×1223`、**(31,31,31)×425**、…
⇒ **正文主笔画是 #1F1F1F（= `--color-text-1`）**，与 r93 实现一致。
⇒ 故 ② 的 `--color-text-3`（#868686，比 text-1 浅两级）是**邵先生主动要求的再下调**，实现里已注明。
（另：该卡在 PNG 上**无可见底色卡片**，视觉是普通文本块 —— 与 r93 的灰底实现有差异，本轮未动。）

### 2.2 DS 灰阶阶梯（②「两级」的换算依据）

`text-1 = gray-10(#1F1F1F)` / `text-2 = gray-8(#4E4E4E)` / `text-3 = gray-6(#868686)` / `text-4 = gray-4(#C9C9C9)`
—— **每级跨两个色阶** ⇒ 「浅两级」= `--color-text-3` ✓（不是 text-4）。

### 2.3 ⑩ 的投影取数：**实测比 DS token 弱一半以上，故不照搬**

设计稿状态条 `board(164,4876)` 840×40 下方逐行平均灰度（rel+0..+9）= `244 245 246 248 249 251 252 253 254 255`（峰值 Δ=11、**10px 收干**）；
左方 `249 251 252 253 254`（5px，Δ≈6）；上方 `254 / 254.8`（2px，极弱）。
DS `--shadow1-down`（`0 2px 5px #0000001a`）峰值 Δ≈26 ⇒ **强了一半以上**，直接用会明显偏重。
⇒ 在同一次浏览器会话内联试 4 档，取 Σ|Δ| 最小者（`ev/p101shadow.sh`）：

| 候选 | Σ\|Δ\| |
|---|---|
| `0 2px 6px rgba(0,0,0,0.06)`（首版） | 剖面 `245 246 249 250 252 253 254 255 255 255` ⇒ 早 2 行收干，偏大 |
| **`0 2px 9px rgba(0, 0, 0, 0.07)`（采用）** | **3** ✓ |
| `0 2px 10px α=.07` | 3（打平；选 9px 因**上方外溢更小**） |

### 2.4 ⑦ 的取数：本页产物**没有**子菜单的编译样式

`conversation.html` / `task-detail.html` 里都**没有** `.giencoder-dropdown-submenu` / `-submenu-popup` / `-arrow` 的编译样式
（`task-detail.html` 的 `.td-ctx` 纯靠 r69 的 JS 摆 `left/top`）⇒ r101 自补这三条适配层规则（`r93-` 前缀叠在组件类之上，未改组件本体）。

### 2.5 ⑪ 的取数：DS Skeleton **已编译进本页**

```
.giencoder-skeleton-line  { background:linear-gradient(90deg,var(--color-fill-2) 25%,var(--color-fill-3) 37%,var(--color-fill-2) 63%);
                            background-size:400% 100%; border-radius:4px; height:14px; margin-bottom:12px;
                            animation:1.4s infinite giencoder-skeleton-loading; display:block }
.giencoder-skeleton-title { … height:20px; margin-bottom:16px }
.giencoder-skeleton-avatar{ … border-radius:50%; width:40px; height:40px }
```
⇒ 直接复用（只覆盖尺寸），不新造动画。

---

## 三、★ 一个跨代的工程改动：`GENS` 逐代摘除表

r93 已提交 ⇒ 页面里留着 `r93-conv-css` / `r93-conv-js` / `r93-nav-js` 三块。若只摘本代：
① 摘块后基线里会残留上一代标记（自检炸）；② 两代并存 = 双份生效。故 `apply101.py` 引入：

```python
GENS = (('r93',  'r93-conv-css',  'r93-conv-js',  'r93-nav-js'),
        ('r101', 'r101-conv-css', 'r101-conv-js', 'r101-nav-js'))
CSS_ID, JS_ID, NAV_ID = GENS[-1][1:]          # 注入用**本代** id
_N_CSS = '|'.join(g[1] for g in GENS)        # 剥离正则对**每一代**都生成一条分支
```

* `ATTR_HOST = 'r93-conv-host'` / `ATTR_PAGE = 'data-r93-page'` **跨代沿用**（只出现在被整块重写的 CSS/JS 里，无残留风险）⇒ 页面级 CSS 选择器**一个字都没改**。
* `main()` 自检改为**两层循环**：对 `GENS` 每一代的三个 id + `ATTR_HOST` 逐个查残留，再单查 `'r101-nav'` 字符串。
* **实测残留**：`pages/base.html` 只有 `r101-nav-js ×1` + `<!-- r101-nav --> ×1`；`pages/conversation.html` 只有 `r101-conv-css ×1` + `r101-conv-js ×1`；**r93 代标记 0 残留** ✓

---

## 四、验收四查

| 项 | 结果 |
|---|---|
| 幂等 | `apply101.py` 连跑两遍 → 第二遍报「**已是目标态（无改动）**」✓ |
| 语法/配平 | `python mg-work/check-syntax.py pages/*.html` → **10/10 通过** |
| 零影响 | `python verify-design.py ./pages` → **76 条**（66 🟡 / 10 🔵 / 0 🔴），与基线 `mg-work/r93/ev/vd-r93c.txt` **逐行 diff 只剩 1 条**（见下）✓ |
| 双视口 + 视觉 | 1440 全量读数（`ev/p101fin.log`）+ 2560 复核（`ev/p101e.log`，`pane=[269,93,2282,912]` / `sb=[840,893,1141,40]` / `art[0]=[840,4003,565,56]` / `cv[0]={slot 14×14, svgW 10px}`）+ 裁片目视 ✓ |

**门禁唯一差异（预期内）**：

```
34c34
<   问题: 检测到 62 处渐变，可能过度装饰（…）
---
>   问题: 检测到 63 处渐变，可能过度装饰（…）
```
⇒ +1 渐变 = **⑥ 的渐隐层**（`linear-gradient`），是**页面级统计的 info**，非缺陷。`汇总: 76 个问题` 两侧相同。
⚠ 跑完已 `git checkout -- pages/gaps.log`。

---

## 五、产物 / 探针 / 回滚

* 产物：`pages/conversation.html` **634719 → 671386 字符**（+36667；LF 文本 sha **`544ed8156a78`**）；`pages/base.html` **471444 → 471447**（+3，仅 nav 脚本 id 换名）。
* `pages/task-detail.html` **未改**（766714 / `d84c1f6f8e01`）。
* 主改：`mg-work/r101/apply101.py`（`GENS` 表 + ①~⑪ 十一条 + ⑦ 的 r69 图标抽取 + ⑪ 的 SKEL）。
* 新增探针：`ev/p101a.js`（侦查）· `p101b.js/.sh`（静态 11 条）· `p101h.js`（hover 读数，非决定性）· **`p101hov.js`（决定性 hover：查 `matches(':hover')`）** · `p101jump.js`（折叠 dx）· `p101sk.js/.sh`（骨架屏）· `p101ctx.js`（右键菜单）· `p101tag.js`（打标）· `p101shot.js`（Bash 卡头）· `p101shadow.sh`（投影 4 档 Σ\|Δ\| 比对）· **`p101fin.sh/.log`（终态一次性取证）** · `check_ow.py`（r69 图标抽取校验：线条 7 / 品牌 6 / 18345 字符）· `sample_t12l.py`（② 的设计稿取数）。
* 新增裁片：`raw/r101-sk-on.png`（骨架屏，临时把延时改 60s 取证后已还原）· `r101-fin-sk.png` · `r101-fin-ctx.png`（右键菜单）· `r101-fin-sb.png` · `r101-fin-fadezoom.png`（渐隐带 + 投影 2× 放大）· `r101-fin-1440.png` · `r101-after-bashhead.png` · `r101-d-bashhead.png`（设计稿对照）。
* 回滚：`python mg-work/r101/apply101.py --revert`（整代），或 `cp mg-work/r101/before/conversation-r101.html pages/conversation.html`（= r101 前置基线）；脚本是「先 `strip_all(当前页)` 取净底再注入」⇒ **定点删掉标 `★ r101` 的段落再重跑即自愈**。

---

## 六、待拍板 / 需人工复核

1. **⑤ 删的是哪一枚绿勾** —— 全页 `.r93-okc` 有 2 处：本代删的是 **Bash 卡头**那枚（判据：它无文案可指，且与 ④ 的箭头同块相邻）；
   **「上下文已压缩」行首那枚保留**（带文案「已压缩 24 条历史记录」）。**若指的是后者，请说一声，一行改**。
2. **⑧ 是否常转** —— 目前**常转**（`1.2s linear infinite`）。若只要 hover 时转，去掉 `r93-spin` 类即可（CSS 保留无害）。
3. **⑩ 投影档位** —— 取 `0 2px 9px rgba(0,0,0,0.07)`（Σ\|Δ\|=3，与 10px 打平，选 9px 因上方外溢更小）。若觉得偏弱/偏强，这是唯一的旋钮。
4. **① 的 hover 口径已闭环** —— 本轮改用「查 `matches(':hover')`」的决定性探针复测：展开头 / 折叠头 **`hov=true` 且底色全透明、文字提到 `rgb(31,31,31)`**，r99 遗留的「无法直证」已消除。

---

## 七、★ 本轮踩坑（脚本内注释会**原样注入页面**）

`apply101.py` 里 `CSS = r"""…"""` / `JS_TMPL = r"""…"""` / docstring 的文本**会原样进入产物 html**，故：

1. 注释里写裸 `` `<style>` `` / `` `</style>` `` 会打乱 `main()` 的 `<style>` / `<script>` **计数自检**（`!! <style> 计数异常`）⇒ 注释里一律写「页面样式块」。
2. 注释里写 `color:#30953B` 这类**字面 hex** 会被 `verify-design.check_hardcoded_hex` 判 **TOKEN-GAP**（该行含 `/*` 会走 CSS 注释豁免，但 JS 行注释 `//` **不豁免**）⇒ 注释里一律写「色 = `--r93-ok`」。
3. 门禁跳行条件 = `if '<!--' in line or '/*' in line: continue` ⇒ **CSS 注释豁免、JS `//` 不豁免**（与 PLAYBOOK P3.29① 同源）。

> 与前代同类教训一起记：**「新增注释里不得出现被断言的 token」**（r94 的渐变词、r98 的裸字号、r101 的裸 hex / 裸标签）。

---
---

# ★ 第二批（同日 19:50 · 邵先生再发七条）

> **体位**：r101 代**仍未提交** ⇒ 按硬规则**就地返工 `mg-work/r101/apply101.py`**，不另起代数；
> `GENS` 表 / 注入 id（`r101-conv-css|js` / `r101-nav-js`）/ 宿主标记 `r93-conv-host` 全部不动。
> **产物**：`conversation.html` 671386 → **672845**、`base.html` 471447 → **472150**；
> 另 4 页（avatar / skills / automation / settings）各 **+703** —— 只多一块 `r101-hdr-css`。

## 八、七条 → 落点 → 实测读数（1440×900）

| # | 需求（节选） | 落点 | 实测读数 |
|---|---|---|---|
| ① | 「对话内容滚动时，`r93-bar` 这个标题栏容器要呈现高斯模糊的毛玻璃效果」 | CSS `.r93-bar`（`position:absolute` + `backdrop-filter`）· 宿主 `position:relative` · `.r93-scroll{padding-top:44px}` · `.r93-sk-in` 上内距 32→76 | 静态：`barPos=absolute` / `barBg=rgba(255,255,255,0.72)` / `barZ=10` / `barBd=blur(12px)`；`bar=[269,49,1162,44]`、`scroll=[269,49,1162,544]`、`scrollPad="44px 0px 0px"`。**滚动到 1200 的 A/B**（同一屏人工把 `backdrop-filter` 关掉再拍一张）：x[400,680] 带内平均\|Δ\|=**19.75**、变化像素 **85.8%**、梯度能 **12.32 → 2.86（降 76.8%）** ⇒ 内容确实从标题栏底下穿过并被糊掉（裁片 `raw/r101-frost-ab.png` / `r101-frost-zoom.png`） |
| ② | 「`header[class*="h-12"]` 的 background-size 要设为 70%」 | 新起一块 `r101-hdr-css`，注入**全部 6 个带 `r92-hdr-css` 的页面** | `getComputedStyle(header).backgroundSize = "70% auto"`（1440 → 图宽 1008px；2560 → 1792px），`backgroundPosition` 仍 `100% 50%`；像素侧：x1100..1440 的点阵像素数 **7097 → 4720**（点距 8 → 5.6px，见 `raw/r101-hdr-ab.png`） |
| ③ | 「骨架屏显示时有一个浅灰色的容器，需去掉」 | CSS `.r93-sk-card` 撤掉 `background` / `border-radius` / `padding` | 临时把退场延时改 60s 取证（已还原）：`cardBg=rgba(0,0,0,0)` / `cardPad=0px` / `cardRadius=0px` / `cardShadow=none`；3 条灰条仍在，且与上面 3 条正文条**同左缘 x=420**（`[420,321,860,14]/[420,347,…]/[420,373,…]`）。截图 `raw/r101-sk2.png` |
| ④ | 「上轮任务中"衔接处"的渐隐效果的距离需要稍微加大一点」 | CSS `.r93-tbsticky::after` 高度 **40 → 56px** | `fade={h:"56px", bottom:"-44px"}`。A/B（人工 `display:none` 掉伪元素再拍一张）裁片 `raw/r101-fadeab-crop.png`：同一屏里「滚动到底部」药丸**依旧清晰**、它下面的 `detail.js / +800 -125 / ⋯` 明显洗淡 ⇒ 层级「滚动内容 < 渐隐层 < 药丸」未变 |
| ⑤ | 「`r93-diff` 里的右键菜单和更多菜单，要和任务产物卡片的右键菜单保持一致」 | JS：**r99 ⑦ 那张 4 项菜单整段退役**，三处触发器改接同一张 FMenu | 汇总行右键 → `["打开","打开所在文件夹","添加到对话","添加到 GienCoder","复制路径","打开方式"]`（与产物卡右键**逐字相同**）；点「⋯」→ 同上，面板 `[1242,337,182,227]`、`dx=0 / dy=+4`；hover「打开方式」→ 子菜单 6 项（彩色品牌图标）；**整行左键**（r100 ④ 行为）也仍是这一套（`box=[432,343,182,227]`）；全页 `.r93-ctx` 元素**恒 1 个**。截图 `raw/r101-diff-menu2-zoom.png` / `-sub2-zoom.png` |
| ⑥ | 「`r93-fc.r93-bt` 在折叠时的 hover 状态，需要在右边显示向右的箭头图标，间距 8px」 | JS 折叠头末尾补 `.r93-fchev`（复用子菜单那枚 `fright` 图标）+ CSS | 折叠后 `fc` 子女 = `[图标 14×14, 标题 75×22, 箭头 14×14]`、按钮宽 **115**（= 14+4+75+4+4+14）；**静止 `arrowOp=0`**；真鼠标 hover → `hov=true` / `arrowOp=1` / **`gap=8`** / 箭头右缘贴按钮右缘；`fcColor` 仍 `rgb(31,31,31)`（① 的口径未回退）。裁片 `raw/r101-fc-hover2-zoom.png` |
| ⑦ | 「`r93-fc.r93-bt` 的展开折叠需要给点弹性微动效」 | CSS `@keyframes r93-fold-in` + `.r93-cv` 换曲线 | `.r93-fb` 的 anim = `r93-fold-in / 0.34s / cubic-bezier(0.34, 1.56, 0.64, 1)`；点展开的**同一 tick** 读 `getAnimations()`：`{name:"r93-fold-in", dur:340, state:"running", ct:0, fill:"both"}`；chevron `transition: transform 0.34s cubic-bezier(0.34, 1.56, 0.64, 1)` |

## 九、第二批的四查

| 查 | 结果 |
|---|---|
| 幂等 | 连跑两遍：第一遍 `base 471447 → 472150` / `conversation 671386 → 672845` + 4 页各注入一次；第二遍 base / conversation **双「已是目标态（无改动）」**、4 页 0 变动 |
| 语法 / 配平 | `python mg-work/check-syntax.py pages/*.html` → **10/10 ALL_OK** |
| 零影响 | `python verify-design.py ./pages` → **21882 字节，与上批终态 `ev/vd-r101b.txt` 逐字节相同**（`diff_exit=0`）⇒ **零新增**；`pages/gaps.log` 已 `git checkout` 还原 |
| 回归 | `.r93-t12l` 字号直方图仍 `{13px:17, 14px:1, 15px:1}`；真实内容首块仍 `[420,125,860,4178]`（静止态与改前逐像素一致）；「滚动到底部」药丸底边距滚动口底仍 **12px** |
| 自适应 | 2560：`bar=[269,49,2282,44]`、`scroll=[269,49,2282,844]`、`hdrSize="70% auto"`、`firstReal=[840,125,1141,…]` |
| 回滚通路 | `apply101.py --revert --dry` 打印正常（4 页摘 `r101-hdr-css` + 路由表逆操作），`--dry` 未写盘 |

## 十、第二批的取舍（代码注释里都写了，这里摘出来给邵先生）

1. **⑤ 是「替换」不是「合并」**：r99 ⑦ 的 4 项（查看文件 / 查看改动 / 复制文件路径 / 撤销此文件改动）**整段删掉**，
   现在汇总行与产物卡共用同一张 6 项菜单。若其实想要「并集」（= 10 项），说一声即可。
2. **⑦ 只做了「展开」的回弹，折叠仍是瞬收**：`.r93-fb` 是 `display` 开关，要让「收起」也动就得改高度动画
   （`grid-template-rows: 0fr→1fr` + 内层 `overflow:hidden`），而那个 `overflow:hidden` 会剪掉卡内向上翻的
   `.r93-pop`（文件路径 hover popover）⇒ 得不偿失。折叠方向的手感由 chevron 回弹承担。
3. **① 的已知副作用**：标题栏现在盖住滚动口**最上 44px** ⇒ 内容滚进那一条带时**点不到**（被标题栏接住），
   滚动条最上 44px 也会被毛玻璃洗淡 —— 与 macOS「滚动条滑到标题栏底下就淡出」同观感，判定可接受。
   毛玻璃参数（`rgba(255,255,255,0.72)` + `blur(12px)`）**无设计稿依据**，是自定的；嫌重/嫌轻改 `--r93-glass` 与那一行 `blur()`。
4. **② 落在 6 个页面** = 所有铺了 r92 装饰图的页面；研发工作台那 4 页（dev / kanban / req-kanban / task-detail）
   本来就没铺这张图 ⇒ 未动。
5. **`.r93-dmore:hover`（灰卡上那枚「⋯」）仍是「白底 + 1px 描边」**（r99 ⑨ 定的，设计稿实测值）——
   本批只点了「菜单内容要一致」，没点这枚按钮的 hover ⇒ 保持原样，两处口径仍**不统一**（等发话）。

## 十一、第二批的踩坑

1. **`re.compile` 漏 `re.S`** —— `RE_HDR` 第一次写成 `re.compile(r'<style id="…">.*?</style>\n?')`（**没有 `re.S`**）
   ⇒ `.` 不跨行、块永远摘不掉；症状不是「摘不掉」而是第二遍跑时自检先炸 `!! 摘块后基线里仍残留标记 'r101-hdr-css'`，
   极易误判成「残留检测写错了」。**凡跨行块的剥离正则一律 `re.S`**（本文件其它三条 RE 都有，就这条漏了）。
2. **`%` 格式化字符串** —— `changes.append('%s 注入 r101-hdr-css（顶栏图 70%）' % name)` 直接 `TypeError`
   ⇒ 字面百分号要写 `%%`，或别用 `%` 拼接。
3. **`agent-browser click` 会被毛玻璃标题栏接住** —— ① 落地后标题栏盖住滚动口最上 44px，
   `click` 若把目标滚进那一条带就点在标题栏上（症状 = `eval` 读不到菜单，容易误判成「点击没绑上」）。
   修法：先 `scrollIntoView({block:'center'})` 再点（见 `ev/p101o2.sh`）。
4. **hover 类读数一律「真鼠标 + 查 `matches(':hover')`」**（承第一批教训）；本批 ⑥ 的 `gap=8` 就是这么量出来的
   —— 静止读数会小 2px（`.r93-fchev` 基态带 `translateX(-2px)` 的滑入位），别把那 6px 当答案。

## 十二、第二批的新增资产

* 探针：`ev/p101m.js/.sh`（基线几何：确认 `.r93-bar` 原是**流内兄弟**，与滚动口相切）· `ev/p101n.js`（七条静态读数）·
  `ev/p101n2.sh`（**毛玻璃 A/B**）· `ev/p101o.sh`（折叠头 hover + 回弹 + 菜单）· `ev/p101o2.sh`（补验「⋯」真点击 + 起播瞬间）·
  `ev/p101r.sh`（骨架屏，临时 60s）· `ev/p101fadeab.sh`（渐隐 A/B）· `ev/p101fin2.sh`（1440 + 2560 终态）·
  `ev/p101hdr.sh`（跨页 `background-size`）· `ev/patch_menus.py`（菜单合一的文本切片改造脚本，**用完即删**）。
* 裁片：`raw/r101-frost-{on,off}-{1200,1800}.png` · `r101-frost-ab.png` · `r101-frost-zoom.png` ·
  `r101-fc-hover2.png(+zoom)` · `r101-fold-spring.png` · `r101-diff-menu2.png(+zoom)` · `r101-diff-menu-sub2.png(+zoom)` ·
  `r101-sk2.png` · `r101-fin2-{1440,2560,bottom}.png` · `r101-fadeab-{on,off}.png` · `r101-fadeab-crop.png` ·
  `r101-fade2-{3325,3300}.png` · `r101-hdr-ab.png` · `r101-hdr-{avatar,conv}.png`。

---
name: compiled-bundle-jsx-patch
description: >-
  给**已构建的 SPA / 单行压缩 bundle 页面**里 React 渲染的元素改样式（尤其是「某个状态下换成另一种颜色 / 图标」这类
  条件外观）时的配方：先判断 CSS 到底能不能覆盖（尾风任意类与内联 style 是两个盲区），不能覆盖就用幂等的
  `replace_once` 在原源码串上打补丁 + 注入自定义类，并用「逐态计算样式 + 兄弟控件反证」验收。
  当用户说「这个按钮选到 X 的时候要变红 / 变粗 / 换图标」「某个交互态的颜色改不了」「改了 CSS 没生效」
  「这是构建产物，源码在 bundle 里」「JS 定位的弹层位置改不动 / 跑到屏幕外 / 新加的弹层看不见」
  「这段小字框选不到 / 选不中 / 复制不了」「右栏展开后这个浮窗 / 提示条宽度不自适应、文字被裁或压出圆角盒」
  「分栏条按下拖不动 / 一拖就复位 / 拖到一半不动」「全屏（最大化）之后按钮图标不跟着变」
  「全屏后拖拽失效」「折叠 / 收起之后按钮状态没回退」时使用。
  触发词：压缩 bundle、minified、构建产物、React 渲染、条件样式、内联 style 覆盖不了、尾风任意类、
  Tailwind arbitrary class、改了没生效、replace_once 补丁、幂等改源码、!important 压过行内样式、
  自定义属性穿透、页面级通配适配层、弹层跑到视口外、getBoundingClientRect 才是判据、
  选不中文字、框选不到、伪元素 content 不是 DOM、CSS 生成内容、MutationObserver 自收敛、
  定高容器折行溢出、min(原值, 100%) !important、
  DS 组件宽度不拉通、inline-flex width auto、这一栏要拉通、联动显隐、状态类挂在哪一级、
  能纯 CSS 就别写 JS、展开时隐藏反之显示、
  元素居中改不动、fit-content 没生效、盒子宽度钉死、文字真实盒中心、Range.selectNodeContents、
  mark 选错静默跳过、幂等补丁跳过了一项、mark 一律等于 new、重复追加、同一选择器改多稿、按选择器整块替换、
  拖拽起点读实际几何、一拖就复位、pointermove 挂 window、把事件派发到 body 当判据、
  独占态退出路径、全屏按钮图标不切换、图标两态 d 不同、跨代资产同名覆盖件、
  观察后插节点父级不触发、收起时状态没回退、
  菜单位置不对、应该在触发按钮下方、下拉跑到按钮上方、弹层锚点、触发器实际几何、
  一条 top 服务两种锚点高度、offsetWidth 不受 transform 影响、入场 scale 乘进 rect、
  写行内 left 要清 right、clamp 到容器内边、裁剪祖先、静态 top calc 算不住、
  DS 按钮默认主色、-text 按钮、浮条文字变黑、输入框聚焦没反应、focus-within、激活态、
  inset 描边会把盒子撑高、覆盖层跟着滚动跑了、闪一下看不见、hidden 没生效、display flex 压过 hidden、
  Esc 关掉了整个侧栏、新浮层要接进 Esc 裁决、
  新控件点了没反应、原控件被带坏、querySelector 只取第一个、同构控件打架、独立类名隔离、
  覆盖层挡住自己的按钮、遮罩挡住了触发器、动作循环多弹了一个提示、
  派生高度被压平、带行高 / 高度的规则要配字号 token
agent_created: true
---

# 压缩 bundle 里的 React 条件样式补丁

> 适用：**页面是构建产物**（`pages/x.html` 里一段单行 minified JS，React 用 `jsx/jsxs` 建元素），
> 你要改的是**某个状态下**才出现的外观（颜色 / 图标 / 粗细 / 显隐）。
> 核心顺序：**先证明 CSS 覆盖不到 → 再选「挂类」或「改源」→ 锚点幂等打补丁 → 逐态实测 + 反证**。

## 一、★ 第一步永远是：判断 CSS 能不能覆盖（两个盲区）

在动手改源码之前，先把目标元素的**取值来源**查清楚：

| 来源 | 长什么样 | 后置 CSS 能否覆盖 |
|---|---|---|
| 普通类 | `class="perms-trigger"` | ✅ 能 |
| **尾风任意类** | `class="… [color:var(--color-text-2)]"` | ❌ **任意类是构建期产物** ⇒ 你新写一个 `[color:var(--color-danger-6)]` 这个类名**不会进产物 CSS**，写上去等于没写 |
| **内联 style** | `style="color: var(--color-text-2)"` | ❌ 内联优先级最高（除非 `!important`，而 `!important` 还会被同层 `!important` 抢） |
| 组件传参 | `<X color="…" />` | ❌ 同上，取决于 X 内部怎么用 |

**判据**：
```bash
# 目标类名到底在不在产物 CSS 里？（找不到 ⇒ 是构建期产物，新增同类无效）
grep -o '\[color\\:var(--color-[a-z0-9-]*)\]' pages/x.html | sort -u
```

⇒ 如果命中的是后两种，出路只有两条：

1. **挂自定义类**（不走尾风）：改源码把 className 尾巴换成 `my-thing-danger`，再由注入块给
   `.my-thing-danger{color:var(--color-danger-6)}`。
2. **直接改内联值**：改源码里那处 `style={{color: X?A:B}}`，把值换成 `var(--color-danger-6)`
   （**内联里写 `var()` 是合法的**，只要该变量在 `:root` 有定义）。

★ 两条常**同时用**：图标走类（因为它是尾风任意类）、文字走内联（因为它本来就是内联）—— 一个元素的两半各走各的路。

### ★★ 覆盖「DS 组件基类的默认外观」⇒ 先读基类，别照需求字面写

需求常是「这个浮条的图标和文字**默认应该是正文黑**」「输入框少了**输入中激活态**」——
这类「默认值不对」的需求，**根因都在 DS 基类里**，先读基类再写覆盖，比试错快十倍：

| 现象 | 基类给的值 | 覆盖写法 |
|---|---|---|
| 文字按钮 / 图标浮条**默认是主色蓝** | `.giencoder-btn-text { color: var(--color-primary-6) }` | `.my-selbar .giencoder-btn { color: var(--color-text-1) }`（(0,2,0) + 文档序在后即可；**SVG 走 `currentColor` 自动跟**，不必单独点图标） |
| 聚焦后**零视觉变化**（只有 `input:focus{outline:none}`） | 无 `:focus-within` 规则 | 照 DS `.giencoder-input-wrapper:focus-within` 的口径：`border-color: primary-6` + `box-shadow: 0 0 0 2px primary-light-2` |

★ **Pill / 定高形态改用 `inset` 描边**（`box-shadow: inset 0 0 0 1px primary-6, 0 0 0 2px primary-light-2`）
—— 写 `border` 会把定高胶囊**撑高 2px**（本站 26 → 28），必须量 `getBoundingClientRect().height` 反证「高度未变」。

★ 验收照 `css-state-pixel-evidence` 第五节那条：**`focus → 等 400ms → 读 → blur → 等 400ms → 读`**
（`focus()` 后**同步**读 `getComputedStyle` 拿到的是**过渡起点** ⇒ 会误判「样式没生效」）。

### ★★ 覆盖物 / 闪烁层**别挂进滚动容器**；给自带 `display` 的类加 `[hidden]` 要显式写规则

* 挂在 `overflow: auto` 的容器上时，绝对定位子元素会**跟着内容滚走** ⇒ 用户滚动后就**什么都看不见**。
  挂到**最近的、非滚动的**祖先（给模块根补 `position: relative`，把 `::after` 闪在整块面板上，
  语义反而更贴切）。★ 判据是「**滚动一段距离后再触发，仍然可见**」，别只在顶部试一次。
* **自带 `display` 的类会压过 UA 的 `[hidden] { display: none }`**（`.my-pane { display: flex }`）
  ⇒ 凡是切换显隐的面板一律补 `[hidden] { display: none }`；判据读**两套面板的 `hidden` 属性 + 各自 rect**，
  而不是「看着只剩一个」。
* ★ 新开的浮层 / 覆盖层**必须接进既有的 Esc 裁决链**：本站漏接一次 ⇒「开着预览按 Esc」
  落到了下一层处理器上、**把整条侧栏关掉**。判据 = 开着它 `press Escape` 后断言
  「它已关 **且** 外层仍在」。

### ★★ 反过来的坑：页面级 `!important` 规则会**压过行内 style**（含 JS 定位坐标）

上表说「内联优先级最高」**只在没有 `!important` 时成立**。老页面里常有一条**页面级通配适配层**（如
`html[data-*-page='x'] .some-ds-class { top: auto !important; bottom: … !important }`）—— 它**连行内 `style.top/left` 也压得过**。

**症状**：JS 明明写了 `el.style.left = x + 'px'`，量出来却纹丝不动，**且不报错**。
**解法（把自定义属性当「穿透通道」）**：

```js
el.style.setProperty('--my-x', x + 'px');   // ★ 自定义属性本身不是声明，不会被 !important 压制
el.style.setProperty('--my-y', y + 'px');
```
```css
html[data-*-page='x'] .my-float { top: var(--my-y, 0px) !important; left: var(--my-x, 0px) !important; }
```

**伴生坑（同一类元凶）**：往老页面里**新挂一个「本来就带全局适配层」的 DS 类**（弹层类名是重灾区）之前，
先 `grep` 该类的**页面级规则**（`html[data-*-page=…]` / 通配）—— 它会把新元素一起带走（实测把新弹层
`top` 翻到锚点上方、`rect.y = -170` 推出视口）。**★ 最坑的是「除位置外一切属性看起来都对」**
（`hidden` 摘了 / 开合类加了 / `visibility:visible` / `transform:none` / `scale:1`）⇒
**只量 `getComputedStyle` 会得出「它是好的」，必须量 `getBoundingClientRect()`**。
修法 = **在同名规则上叠一层容器类提特异性**，别去改那条老的全局规则。

### ★★★ 反向：某段文字「框选不到 / 复制不了」⇒ 先查它是不是 `::after` 的 `content`

**生成内容（`::before` / `::after` 的 `content`）不是 DOM 的一部分** ⇒ 选区落不进去、复制不到。
它**看起来**和真文字一模一样（字体 / 颜色 / 位置都能算出来），所以极易被误判成「文本层有 bug」，
而真源常常是**上一个迭代为了省结构**用纯 CSS 挂上去的一行文案。

**判据三条**（先真的拖选过那段文字，再量）：

| 量什么 | 生成内容的表现 |
|---|---|
| `Selection.toString().length` | **0**（怎么拖都是空） |
| `document.caretRangeFromPoint(x,y).startContainer` | 退回**宿主元素**（`DIV`）且 `offset === 0` —— 没有可落的文本节点 |
| `Range.selectNodeContents(宿主)` 拿到的文字长度 | **少掉那一段**（只有真正的子节点文案） |

★ **隔离对照（决定性的一步）**：临时往页面塞最小复现 —— `#zzA::after{content:"PSEUDO-SELECT-ME"}` 与
`#zzB`（**真文本**），**同一次运行、同一套拖选手法** ⇒ 前者 `""`、后者 `"REAL-SELECT-ME"`。
这一步是为了**排除「探针写错了」**，别一上来就怀疑产品代码。
⚠ 对照物**别用 `<textarea>` / `<input>`**（表单控件内部不是普通文本节点 ⇒ 两边都取到空串，对照直接失效）。

**修法**（要「可框选」就只能换成真节点）：

```css
/* 同选择器 + 文档序在后 ⇒ 关掉伪元素那条（别去删原来的规则，那条可能还被别处引） */
html[data-*-page='x'] .host::after { content: none; }
```
```js
/* 宿主是 React 的地盘 ⇒ MutationObserver「自收敛」：只做「判存 + 不在末尾就 appendChild」 */
function sync() {
  var host = document.querySelector(HOST_SEL); if (!host) return;
  var el = host.querySelector(':scope > .my-stats');
  if (!el) { el = document.createElement('div'); el.className = 'my-stats'; el.textContent = TXT; }
  if (host.lastElementChild !== el) host.appendChild(el);   // ← 只管末尾 ⇒ 自己造成的 mutation 再进回调即返回
}
sync(); new MutationObserver(sync).observe(document.body, { childList: true, subtree: true });
```

* 只判「存在 + 位置」两件事 ⇒ **不会死循环**，同时兜住 React 的两件事：**重渲染摘掉要补回**、
  **重挂后被插到中间要挪回末尾**（否则那行字会跑到输入卡上面）。
* 换完**逐项对照旧伪元素的计算样式**（字号 / 行高 / 颜色 / `white-space`）确保版式一字不差；
  再量新节点 `rect` 与旧伪元素是否**同一行** —— 宿主的 `gap` 会参与定位，别忘算它。

> **反向复用**：伪元素恰好是「给 React 容器补一行文案」的最省事手段（挂在 `flex-col gap-*` 上天然居中、还吃 `gap`），
> 只是**不可框选**。要可复制 → 真节点 + observer；纯装饰 → 伪元素更省。

### ★★ 尺寸类：行内写死的 `width`、定高的 `height`，同样只有 `!important` 压得住

* **行内写死 `width: 760`** ⇒ 容器一窄就**两端溢出被裁**（左对齐的块更隐蔽：**左边字头被吃掉**）。
  修法 = `width: min(760px, 100%) !important`。
  ⚠ `100%` 的基数 = **最近定位祖先**（不是父盒）⇒ 先确认那个祖先的 `position`，否则 `100%` 会算到视口上。
* **写死 `height: 44px` 的容器** ⇒ 内容折行后**溢出圆角盒**、压住上下相邻行。
  修法 = `height: auto; min-height: 44px;` + **把竖内距凑到「单行态完全等价」的值**（这一步最容易翻车）：
  先算单行内容高（文字 `line-height 22` + 上下内距 `8 + 8 = 38 < 44`）⇒ 单行**仍顶到 `min-height`**、
  `align-items: center` 照样居中 ⇒ **单行宽度逐像素不变**，只有折行才真正长高。
* ★ **判据是「容器可用宽」，不是视口分辨率**（1440 下看不出来、1280 / 1100 才现形）⇒ 至少量三档，
  并在汇报里写明「**哪个分辨率才看得见**」。
* ★ 改完**必须补一条「单行态零变化」的实测**（改前 `h:44`、`clientHeight === scrollHeight` 与改后**逐值相同**），
  否则容易「修好了折行、弄坏了单行」。

### ★★★ 「居中」改不动 ⇒ 先查「谁在管这个 `width`」（多半是页面级 `!important`）

需求形如「这一行小字要居中」。**第一版很容易写成死代码**：

```css
/* ❌ 死代码：width / min-width / max-width 全被别处 !important 钉住 */
.mine-stats { width: fit-content; max-width: 100%; margin: 0 auto; }
```

**根因**：它的盒宽由**页面级两条 `!important`** 决定（同一选择器 `main > … > div.mt-8 > div`
的两个历史版本，两条都带 `!important`）⇒ 盒宽**恒等于那个基准元素**（实测三档全等），
`width / min-width / max-width` **一条都改不动**。

**诊断路径（可照抄）**：
1. 先怀疑 `min-width: auto` 撑住了 ⇒ **注入 `min-width: 0` / `width: 100%` 做反证**；
2. 三种状态盒宽**都不变** ⇒ 说明**有更高优先级的东西在管它**（不是你改的那几条）；
3. 翻页面级规则 ⇒ 找到那两条 `!important` ⇒ 定性。

**正解**：`text-align: center`（**它没有任何 `!important` 竞争者**）。

★ **真节点 ≠ 伪元素**：`::after` 是 shrink-wrap 的（盒随文走），换成的真节点在**满宽盒**里默认靠左；
而宿主的 `items-center` 对这个满宽子项**不生效**（原基准元素自己就是齐左的）
⇒ 靠 `margin: auto` 会比基准**偏 32px**。

★ **判据 = 取「文字真实盒」的中心，不是盒子盒**：

```js
var r = document.createRange(); r.selectNodeContents(el);
var tb = r.getBoundingClientRect();                        // ★ 文字真实盒（盒可能满宽、文字不是）
var hb = document.querySelector(BASE_SEL).getBoundingClientRect();
Math.round((tb.left + tb.right) / 2 - (hb.left + hb.right) / 2);   // ★ 期望 0
```

★ **「居中」和「溢出省略」可以共存**：实测 Chromium 在「居中 + 溢出」时对齐**退化为 `start`**
（文字盒仍自盒左缘起算）⇒ **省略号照常落在行尾**（`white-space: nowrap` + `overflow: hidden` 仍在起作用）。
别凭「应该是这样」写进注释 —— **看截图再写**，写反了会让下一个人照着做错取舍。

### ★★ 想给 DS 组件「拉通 / 撑满」宽度 ⇒ 先读它自己的 `display`，别急着叠 `width`

DS 组件的根类常自带 **`display: inline-flex; width: auto`**（实测 `.giencoder-input-wrapper` 就是）。
此时只写 `width: 100%` 往往**仍然不拉通** —— 行内盒在 flex 行里由内容撑宽，
且**它和外层兄弟的收缩/基线行为根本不是一套**，你以为在改宽度，其实是在跟它的 `display` 打架。

**正解两选一，都要量证**：

* 要它在行内**撑满** ⇒ **把 `display` 一起改掉**（`flex` 是块级 ⇒ `width: auto` 自动撑满父行）：
  ```css
  .giencoder-input-wrapper.td-commit-in { display: flex; }   /* 不必也不该再写 width */
  ```
* 只想**加宽但保持行内** ⇒ 写 `width` 时**顺带核父容器的 `align-items` / `gap`**（它们会吃掉可用宽）。

★ **判据是「同一容器里同级兄弟宽度逐值相等」，不是「自己变宽了」**：

```js
var card = document.querySelector('.td-commit');
[...card.children].map(function (c) { return Math.round(c.getBoundingClientRect().width); });
// ★ 期望全等：[308,308,308,308,308]；有一项偏小 ⇒ 那一个还被自己的 display 卡着
```

### ★★ 联动显隐（A 开 ⇒ B 藏、反之显示）⇒ 先量「状态类挂在哪一级」，**能纯 CSS 就别写 JS**

需求形如「右栏展开时，页头那个全屏按钮隐藏；收起时显示」。**第一步不是写 observer，是量架构**：

```js
var on  = document.querySelector('.av-browse-on');                    // 状态类挂在哪
var btn = document.querySelector('.r93-baract[data-r93-fullscreen]');  // 要跟着变的元素
console.log(on.tagName, on.className, on.contains(btn));               // ★ 关键一问
```

| `on.contains(btn)` | 结论 | 做法 |
|---|---|---|
| **`true`** | 状态类是按钮的**祖先** | **一条纯 CSS 搞定**，别写 JS |
| `false` | 兄弟 / 远亲 | 才轮到 JS 挂类 |

```css
/* contains === true 时的全部代码量 */
.av-browse-on .r93-baract[data-r93-fullscreen] { display: none; }
```

★ 实测本仓 `.av-browse-on` 挂在 **shell 的 flex 行**上（`main` 与预览栏的**共同父级**），
页头按钮是其后代 ⇒ 纯 CSS 可行，**省掉一整个 `MutationObserver`（也省掉它自带的一类风险）**。

★ **判据：开 / 关两态各量一次，量 `display` 字符串（不是「看着没了」）**：

```
右栏关 ⇒ getComputedStyle(btn).display === 'flex'、rect 有值（如 [1359,57,28,28]）
右栏开 ⇒ 'none'、rect 归零
```
顺手**数一下同容器其它子元素没被误伤**（`.r93-baracts` 仍应有 2 枚子元素）。
⚠ 题面里用户会点名一长串类名（`r93-baract giencoder-btn giencoder-btn-secondary …`）——
**别拿整串当选择器**，取其中**真正区分它**的那一段（如 `[data-r93-fullscreen]`）更稳。

## 二、锚点：从 bundle 里「左右各带一截」截取

单行 bundle 里锚点必须**长到唯一**。方法：先用 Python 打印目标位置前后各 300 字符，
取「左邻 + 目标 + 右邻」一整段当 `OLD`，并**先断言 `s.count(OLD) == 1`**。

```python
OLD = "`size-[14px] shrink-0 `+(l===`perm`?`[color:var(--color-text-1)]`:`[color:var(--color-text-2)]`)"
assert src.count(OLD) == 1, src.count(OLD)
```

### ★ 三目式加档务必保括号

```js
X ? A : B                        // 原
新条件 ? 新值 : (X ? A : B)      // 新 —— 括号不能省（?: 右结合，省了会让原逻辑走样）
```

## 三、幂等：`replace_once` + `inject_tail`

见 `mg-work/r92/apply92.py` 头部，两个函数可直接抄。

```python
def replace_once(path, old, new, label):     # ★ 不留 mark 参数
    s = rd(path)
    if new in s:                      # ① 新串已在 ⇒ 跳过（幂等的根）
        skipped += 1; return False
    if s.count(old) != 1:             # ② 锚点必须唯一
        sys.exit('!! %s：锚点 %d 次' % (label, s.count(old)))
    wr(path, s.replace(old, new, 1))
```

* ★★★ **不要给 `mark` 留参数位 —— `mark` 一律恒等于 `new`**（`new` 天然只可能「改后才存在」）。
  留了参数位就一定会有人（包括你）手抄，而**手抄必错**（下面那张表全是这么来的）。
  唯一代价：`new` 改一个空格 mark 就跟着变 —— 但那本来就是**对的**（目标态改了，就该重新应用）。
* 改完**必须复跑一次**，确认输出是 `应用 0 项 / 跳过 N 项`。
* 光跑两遍**不能**证明没损毁：如果补丁还会被别的「派生/归一化」脚本二次加工，要额外用
  「摘掉本代块后与基线逐字节比对」来证明只改了该改的（见第六节）。

### ★★★ 幂等 `mark` 必须是「**只有改后才存在**」的串 —— 否则**静默跳过**

`mark` 的语义是「**目标态特征**」，不是「这段代码长什么样」。**踩过的坑（删列表中间一项）**：

```python
# ❌ 这段在改前就已存在 ⇒ 第一遍就判「已应用」，整条删除被静默跳过
mark = "'展开全部' : '折叠全部', ico: t ? 'plus' : 'close'"
# ✅ 用「删完后才相邻」的两端
mark = "'-',\n      { label: t ? '展开全部'"
```

⚠ 最阴的地方：**同批另一处改动（删失去引用的变量）已经执行**了 ⇒ 变量变未定义，
**页面不报错、只是那条判断恒假**，肉眼极难发现。**所以「跳过」也要逐条打印出来核对**，
别只看末行「应用 0 项 / 跳过 N 项」。

* **删中间项** ⇒ mark = 「**删完后才相邻**的两端」；**改值** ⇒ mark = 「**改完后才出现的**新值」。
* 落笔顺序：**先把 `NEW` 写出来，再从 `NEW` 里摘 `mark`** —— 别凭「这段代码长什么样」选。
  ⚠ 本仓在 r107 第八拍、第九拍**连续两拍各犯一次**（第二次是给一个「表格加两行」的步骤选了
  上一拍那行的特征串 ⇒ 整步被静默跳过，末行还显示「应用 15 项」看着挺正常）。
* ★★ **手抄 `mark` 必错 —— 一律从 `new` 里「切片」出来**。本仓 r107 第十一拍的 doc 脚本
  **一轮内连犯三次**，全是「凭印象手抄」惹的：
  | 手抄的 mark | 实际文本 | 结果 |
  |---|---|---|
  | `**⑪ 对照 Codex 官方补缺（三件）**` | `**⑪ 对照 Codex 官方补缺（三件）+ 划词浮条正文黑 + …**`（「（三件）」后面**没有** `**`） | 复跑时判「未应用」⇒ 回头找锚点、锚点已被自己改掉 ⇒ `sys.exit` |
  | `**Esc 层级** \| window 捕获段…` | `\| Esc 层级 \| window 捕获段…`（那一格**没有**加粗） | 同上 |
  | `｜官方 SSH / 多窗口 / 托盘不在静态页范围` | `｜官方 SSH（alpha，不在侧栏）/ 多窗口 / 系统托盘 **不在静态页范围**` | 同上 |
  | `**已推送 \`e9c9498\`**（…邵先生发话）` | 实际写进文件的是 `…邵先生发话 **commit and push**）` | 复跑时 mark 不命中 ⇒ 顺带把 `old` 也判成 0 次 ⇒ `sys.exit`（**同一种「凭印象漏字」，一轮里犯 2 次**）|
  | （**追加型**）`## 十七、交付（…` 整段 | 首版 `new` 与新版差「推送输出」4 个字 | **同一节被追加进文件两次** ⇒ 事后手工去重（`+961` 字符）|
  ⇒ **配方**：`mark = new.split(...)[i]` 或 `mark = 新串里那段独一无二的子串（用 Python 从 new 变量里取）`；
  实在要手写，**写完立刻在终端里 `t.count(mark)` 验一遍**（对已被改过的文件跑，期望 ≥1）。
  ★★ **最省事的配方：干脆别传 mark，函数里写死 `mark = new`**（见上面第三节的签名）。
* ⚠ ★★ **改了 `new` 的措辞之后，要么同步改已写入的文件，要么让 `mark` 兼容两种措辞** ——
  改了 `new` 却让文件停在旧措辞 ⇒ 复跑判「未应用」、回头查 `old`（也已被上一版改掉）⇒ `sys.exit`。
  本轮就这样卡了一次（把「见第 198 行说明」改成「见 `mg-work/r107/` 那行说明」，忘了回头改文件）。
* ⚠ ★★ **追加型步骤（append，`old=None`）的 `mark` 必须 = 整段 `new`**，否则会**重复追加**：
  判据 `t.count(节标题) == 1`；**清理别手工 Edit**（两份内容近似、`old` 不唯一）——
  用 Python 删「第 1 份起点 → 第 2 份起点」（先 `rstrip('\n')` 再接 `\n\n---\n\n` + 第 2 份）。
* ★★ **幂等验证必须是「改完之后再跑一次」，而且要把「跳过」列表当待核对清单逐条读**：
  本轮正是靠复跑逐条抓出上面三处 —— **每一次报错都发生在第二次运行**，第一次全绿。
  修完 mark 后**再跑一次**，直到输出是 `应用 0 项 / 跳过 N 项`（本轮最终 26 项全跳过）。
* ⚠ 还有一类「改完 mark 后**锚点已被自己消耗**」的死锁：mark 修好了、但 `old` 已经不在文件里 ⇒
  第 4 项那种「修正上一版错误输出」的步骤，`old` 要写成**当前（错误）状态**的串，
  `new` 写成目标态的串，`mark` 取**目标态**独有的串。
* 通用兜底：`mark` 为空时，「`OLD` 不在了 **且** `NEW` 在」⇒ 判「已应用」；
  两者都不在 ⇒ `sys.exit`（**不静默**）。本仓 `mg-work/r107/ev/doc107i.py` 的 `patch()` 就是这么写的。
* **多条 `step` 批量跑时，「跳过」列表要当成「待核对清单」读**：逐条问自己「它本来就该是目标态吗？」
  拿不准的那条，直接 grep 产物确认（本仓第九拍正是这样抓到漏插的）。

### ★★ 同一处（同一选择器）改多稿 ⇒ 用「**按选择器整块替换**」，别逐版字符串匹配

一条规则改了三稿（`fit-content` → `text-align` → 更正注释）后，补丁脚本给三个历史版本各写一份
常量 ⇒ **全部匹配失败**（`new 0 / mid 0 / old 0`）。**改成按选择器定位、整块替换**：

```python
def replace_block(t, sel, new_block, label):
    i = t.find(sel)
    if i < 0: return t
    j = t.find('\n}\n', i)                      # 首个块尾
    cur = t[i:j + 3]
    if cur == new_block: return t               # 已是目标态 ⇒ 幂等
    return t[:i] + new_block + t[j + 3:]
```

⇒ **与历史版本彻底解耦**：不管中间改过几稿，只要「选择器定位到的那块」不等于目标文本就重写。

### ⚠ `</body>` 注入点的经典陷阱

```python
# ❌ 不要断言 count('</body>') == 1 —— 页面里的 CSS 注释/字符串也可能含这个字面量
# ✅ 取最后一处，并要求它就在文件尾部
idx = s.rfind('</body>')
if len(s) - idx > 80: sys.exit('!! 最后一处 </body> 距文件尾太远，不像收尾标签')
```
注入点选**文件尾部**（不是 `</head>`）：同特异性规则「后者胜」，页尾块才压得住前面的规则。

## 四、验收：逐态计算样式 + ★ 兄弟控件反证

**一个状态读数对了不算数** —— 条件是「切换到另一个值时才变」，所以要把**全状态迁移链**走一遍，
而且**用真鼠标点击**（合成 `el.click()` 的 `detail === 0` 会被业务代码当**键盘**触发）。

```
T0 默认值（收起）→ T1 默认值（展开）→ T2 换成目标值（收起）→ T3 目标值（展开）→ T4 切回默认值
```

每态读：`textContent` / `getComputedStyle(文字).color` / `getComputedStyle(图标).color` / 图标的 `class`。

★ **反证（本配方最有价值的一步）**：把**同页结构一模一样的另一个控件**也读一遍，
断言它**全程不变**。没有反证，你无法排除「选择器打偏了，恰好读到另一个元素」。

> 真实教训：探针选了 `.ws-dropdown-hover`，而页面上**有两个**同类的下拉触发器（工作目录 / 默认权限）。
> `querySelector` 返回第一个 ⇒ 五个态的读数**全都打在错元素上，且彼此自洽**（看起来完全正常）。
> **正解**：先跑一次「枚举所有候选」（打印 text / 父级 style / 图标 class），再用 `:has(<独有特征>)` 精确定位，
> 例如 `.ws-dropdown-hover:has(svg.lucide-lock)`。

## 五、压缩 bundle 上的静态分析小抄

* **只打印目标片段**，禁整文件读（单行 300–800 KB）。
* **正则量词必须有界**（`[^{}]{0,300}?`），否则回溯跑到超时被 SIGTERM。
* **不要用 `difflib.SequenceMatcher`** 跑大文件：500 KB 单行会直接 SIGTERM。
  改用「**摘已知注入块 + 公共前缀/后缀**」定位改动窗口：

```python
# 用已知的块 id 摘掉本代注入物，再用公共前后缀夹出剩余改动窗口
b = re.sub(r'\n?<style id="mine-css">.*?</style>', '', after, flags=re.S)
i = 0
while i < min(len(a), len(b)) and a[i] == b[i]: i += 1
j = 0
while j < min(len(a), len(b)) - i and a[-1-j] == b[-1-j]: j += 1
```

* 窗口 == 0 ⇒ **「除注入块外逐字节相同」**，比行级 diff 更强的断言；窗口 <1 KB ⇒ 直接打印人工核。
* 改前基线文件**必须与原页面同名**（`before/x.html` 而不是 `x.before.html`）：有些外壳按文件名查路由表，
  名字不对会渲染成另一套壳，量出来的数全错。

## 六、行为补丁：拖拽 / 独占态 / 跨代件

> 改的是 **JS 行为**（不是外观）时用这一节。下面五条每一条都是真踩过的。

### ★★ 拖拽 / 缩放类：第一帧读「**实际几何**」，别读闭包缓存

* 症状：**按下分栏条一拖，宽度猛跳回旧值**（用户会说成「一下就复位 / 拖不动」）。
* 根因：内层控制器用 `startPanel = panelW`（**闭包缓存**）；而**宿主脚本绕过它**直接
  `slot.style.setProperty('--av-browse-w', …)`（本站的「最大化」就是这么干的）⇒ 缓存停在 641、
  实际已是 1040 ⇒ `pointermove` 一算就是 `641 ± dx`（实测 1040 → **761**，正好≈记忆宽）。
* 配方（**两步，缺一不可**）：
  1. 先落**拖拽态类**（本站 = `.is-col-dragging`，规则带 `transition: none`）⇒ **停掉过渡**；
  2. 再 `getBoundingClientRect()` ⇒ 此时才是**终值**，否则读到的是**过渡中间值**。
  顺手把缓存同步回来（`panelW = startPanel`）。
* 判据：`pointermove` 之后断言**声明值**（`el.style.getPropertyValue('--x')`）== `实际起点 ± dx`，
  **不要**用 rect 当判据（过渡会把读数搅浑）。

### ★★ 拖拽的 `pointermove` / `pointerup` 挂 **`window`**，别挂元素

挂元素 + `setPointerCapture` **平时能跑**，但「元素贴边 / 元素被 React 重挂 / `pointerId` 失配」时就断，
表现是**拖到一半突然不动**。**判据配方**：合成 `PointerEvent` 时把 move / up **派发到 `document.body`**
—— 挂 `window` 的照样响应，挂元素的**静默失效**（比「按住鼠标跨多次命令拖」快且可复现）。
顺带补 `blur` 兜底（防切窗口后一直卡在 dragging）。

### ★★ 「独占态」（全屏 / 最大化 / 沉浸）必须把**退出路径列全**

* 本仓一例，应有的三条：① 点按钮还原 ② **拖拽接管**（新发现）③ **容器收起**（新发现）。
  漏 ② ⇒ 用户拖一下宽度，按钮状态就与实际不符；漏 ③ ⇒「收起再打开按钮仍是"还原"字形、宽度却是记忆值」，
  而且**下一次 resize 会突然弹回全屏宽**。
* 配方：写这类状态之前，先把「谁会结束它」列成清单、逐条挂上；
  **退出用 `silent` 变体**（只改状态、不动尺寸），免得「退出动作」本身又触发一次布局跳变。

### ★★★ 别用 `MutationObserver` 盯「**后插节点**」的父级 —— 会绑在错的元素上

* 场景：想实现「A 收起时退出某状态」，于是观察 `el.parentElement` 的 class。
* 坑：那个父级是**另一个脚本在 `place()` 里后插**的，本脚本跑得更早 ⇒ 初次观察挂在**旧父级**、
  **永不触发**（症状：状态残留、按钮文案没回退 —— 且**完全不报错**）。
* 正解：**搭已有的事件流** —— 三个收起入口最终都走同一个 `setOpen(false)`，而它**必定
  `dispatchEvent(new Event('resize'))`** ⇒ 在同一条 resize handler 里判一下即可（**零新监听**、
  也不必等 DOM 就位）。
* 通用化：**「某状态该退出」优先挂「已有的确定性事件」，而不是去观察 DOM 的副作用。**

### ★★ 要改「跨代资产」⇒ 放**本代同名覆盖件**，别在原目录动刀

* 本仓形态：`_read_part()` 按 `PART_DIRS = (part107, part105)` **顺序回退** ⇒ 在 `part107/` 放**同名文件**
  即可**遮蔽**上游 —— 源页（另一个页面）与已交付的产物**零影响**。
* ⚠ 代价 = **副本会漂移** ⇒ 副本头部必须写明「来自哪份、差异点、日后人工同步」。
* 适用判据：要改的代码在跨代件里、且**行为对所有消费页都是改善**（本例 = 拖拽起点更准）。
* **反例**：若改的是**视觉**、且要求与源页**逐字节同源** ⇒ 走页内**多一级类数覆盖**，别做覆盖件。

### ★★★ 浮层的锚点是「**触发器的实际几何**」，不是「容器的固定偏移」

* 症状：同一个基类里的多枚下拉，**有的位置对、有的跑到触发按钮上方**（本站实测**上方 35px**，
  用户描述成「菜单位置不对，应该在触发按钮下方」）。
* 根因：几枚共用一条 `{ position: absolute; top: 42px }`（相对面板容器）。触发器在**标签栏**里的那枚
  ⇒ 42px 恰好是「按钮下方」；触发器在**工具条**（标签栏之下 40px）里的那几枚 ⇒ 同一个 42px
  就变成「按钮**上方**」。★ **一条 `top` 服务两种锚点高度 ⇒ 必然错一半。**
* 配方：**打开瞬间**按 `trigger.getBoundingClientRect()` 现场摆位（本站既有口径：右键菜单的
  `ctxShow()`、划词浮条的 `selShow()` 都这么写）。**同一基类里只要触发器分属不同容器，就必须逐个算。**
* ★ 判据 = 量 **`dy = 菜单 top − 触发器 bottom`**（应恒为一个 gap）+ `coversH`（水平是否覆盖触发器）；
  **「看着像在下面」不算数**，而且**同级菜单要逐枚量**（本拍就是「1 枚对、3 枚错」）。
* ★★ **别改成静态 `top: calc(...)` 图省事**：本站的诱惑写法
  `calc(44px + 40px * var(--ui-fs-ratio) + 6px)` —— 工具条高度确实是 `calc(40px * ratio)`，
  但**标签栏高度来自跨代资产**（写死 `height: 40px`、**实测 44**）⇒ 算式里的两个数**来源不同、
  缩放行为不同**。**「看起来能算」不等于「算得住」。**
* ★ 想「包含块换成工具条 + `top: 100%`」也要先查**祖先有没有 `overflow: hidden`** ——
  本站 `.td-mod{overflow:hidden}` 会把菜单裁掉（这正是当年改用面板当参照的原因）。

### ★★ 浮层摆位的三条硬规矩（每一条都踩过）

1. **在摘掉 `[hidden]` 之后**再量 / 再摆 —— 隐藏元素的 `offsetWidth` / `rect` **全是 0**。
2. **量尺寸用 `offsetWidth` / `offsetHeight`，不要用 `getBoundingClientRect()`** ——
   入场动画若带 `scale(0.96)`，rect 会把 0.96 **乘进去**（读数偏小 4%）。`offset*` 不受 transform 影响。
3. **写行内 `left` 必须同时 `right: 'auto'`** —— absolute 元素同时有 `left` 与 `right` 会被**拉宽**；
   基类里那半条 `right: 8px` 不清掉，纵向就算摆对了、横向仍会变形。

★ **顺手做掉窄栏降级**：菜单宽度固定（168~172）而触发器靠近右缘时右缘必然溢出 ⇒
`left = Math.min(left, host.clientWidth - menu.offsetWidth - 4)`。
判据要量**「是否仍在裁剪祖先之内」**（本站菜单挂在 `.td-mod{overflow:hidden}` 里 ⇒ 必须量
「左/右/上/下四条都在祖先盒内」），**不能只量「在面板内」**。

### ★★★ 给「既有控制器」加一个同构控件 ⇒ **一律换独立类名**

* 症状：新增的控件**点了没反应**，或操作新控件时**原模块的选中态乱跳**（且**完全不报错**）。
* 根因：老控制器的作用域是**整个容器**，取子树用的是 `querySelector`（**只返回第一个**）——
  本站 `ctrl-conv.js` 里 `pane = slot.querySelector('.td-browse')`（= 整块 side panel）、
  `pane.querySelector('.td-browse-files')`（**只绑第一棵**）、`pane.querySelectorAll('.td-bf')`（会扫到新加的那棵）
  ⇒ 新件若复用同一套类名，两边互相接管。
* ★ 配方：**新增同构件就换一套独立类名**（本站：抽屉树 `td-tf*`，与「文件」模块的 `td-bf*` 完全分离），
  并把几何逐条对齐老件（`height: calc(28px * ratio)` / `padding-left` 同口径）以保视觉一致。
* ★★ **判据 = 操作新件之后，老模块的「选中项 / 行数 / 折叠数」计数一字未变**
  （本站实测 `filesActive` / `filesRows 28` / `filesHidden 9` 全程不动）。
* ⚠ 同族指纹：**先数一遍 `document.querySelectorAll('.cls').length`** —— `> 1` 就是撞车
  （另一种形态是「容器类名与内部件重名」⇒ `querySelector` 取到外层、`tabIndex` 为 null）。
* ⚠ 二式：新控件若走老代码的**通用动作循环**（本站 `[data-td-rv-act]` 那段会 `say('已执行')`），
  记得在循环里**提前 `return` 跳过它**（但保留它该做的收尾，如 `closeMenus()`），否则会多弹一个假提示。

## 七、交付前自检清单

```
□ 产物 CSS 里确实没有那个类名 ⇒ 已确认「CSS 覆盖不到」
□ 每处锚点都断言过 count(OLD) == 1
□ 三目加档保了括号
□ replace_once 复跑输出「应用 0 / 跳过 N」
□ 真鼠标走完全状态迁移链，每态都有计算样式读数
□ 有同页兄弟控件的「全程不变」反证
□ 摘掉本代注入块后与基线逐字节比对（或只剩预期的 1 个改动窗口）
□ 语法/配平自检 + 设计规范自检的读数与上一轮基线逐条 diff（汇总数相同 ≠ 零影响）
□ 若目标是 JS 定位的浮层：判据用 **`getBoundingClientRect()`**（不是 `getComputedStyle`），且已确认没被页面级 `!important` 规则改写位置
□ 若新增了「自带全局适配层的 DS 类」：已 grep 页面级通配规则，并加了更高特异性的本页适配
□ 若某段文字「选不中」：已用三条判据确认它是不是 CSS 生成内容（并跑过 `#zzA/#zzB` 隔离对照）
□ 若给 React 宿主注入真节点：`MutationObserver` 只做「判存 + 不在末尾就 append」（无死循环，且已验 React 重渲染后仍在末尾）
□ 若把「行内写死的尺寸 / 定高的容器」改成自适应：已量「容器可用宽」≥ 3 档 + 「单行态零变化」对照，并写明哪个分辨率才看得见
□ 若是给 DS 组件「拉通 / 撑满」宽度：先读过它自己的 `display`，改的是 `display`（不是硬叠 `width`），且已断言**同级兄弟宽度逐值相等**
□ 若是两元素联动显隐：**先量 `状态类.contains(目标)`** —— 为 `true` 就只写纯 CSS、不写 JS；并量过开 / 关两态 `display` + 「同容器其它子元素未误伤」
□ 若目标是「某元素居中」：先确认没人用 `!important` 钉它的盒宽（`min-width:0`/`width:100%` 反证三态盒宽不变即为铁证）；**判据用 `Range.selectNodeContents` 取「文字真实盒」的中心，差 0 才算过**
□ 若目标元素的外观来自 **DS 组件基类**（如 `-text` 按钮默认主色、输入框缺 `:focus-within`）：已**先读基类**再写覆盖；Pill / 定高形态用 **`inset` 描边**（不是 `border`），并量过「高度未变」
□ 若新增了覆盖层 / 闪烁层：**没有挂在 `overflow:auto` 的容器里**（已验「滚动后再触发仍可见」）；带 `display` 的切换面板已显式补 `[hidden]{display:none}`；**已接进既有 Esc 裁决链**（开着它按 Esc 只关它、不关外层）
□ 幂等 `mark` **不留参数位、恒等于 `new`**（不留 = 不会手抄）；复跑时**逐条核对「跳过」项**（不是只看末行「应用 0 项」）；追加型步骤另验 `t.count(节标题)==1`；同一选择器改过多稿的，已改用「按选择器整块替换」
□ 若改的是拖拽 / 缩放：起点读的是**实际几何**（且先落 `transition:none` 再取 rect），并用「把 move 派发到 `document.body`」证明事件确实挂在 `window`
□ 若涉及「独占态」（全屏 / 沉浸 / 最大化）：**退出路径已列全**（按钮 / 拖拽接管 / 容器收起），且退出动作走 **`silent` 变体**（只改状态、不动尺寸）
□ 若用 `MutationObserver` 观察某元素的 class：已确认**该元素不是别的脚本后插的**（否则改挂「已有的确定性事件流」）
□ 若改了跨代移植件：走的是**本代同名覆盖件**（没在原目录动刀），且副本头部写明「来源 + 差异点 + 漂移提醒」
□ 若改的是「图标随状态切换」：已断言两态 **`<path d>` 串不同**，并**目视复核过一张实拍图**（只看 DOM 字符串不算数）
□ 若是**浮层摆位**：锚点取自**触发器的实际几何**（`trigger.getBoundingClientRect()`），**不是容器的固定偏移**；判据 = 量 `dy = 菜单 top − 触发器 bottom` + `coversH`，且**同级菜单逐枚都量**（别只验一枚）
□ 若是**浮层摆位**：**摘掉 `[hidden]` 之后**才量 / 才摆；量尺寸用 **`offsetWidth`**（不是 rect —— 入场 `scale` 会乘进去）；写行内 `left` 时**同时 `right:'auto'`**；有 clamp 到容器内边，并量过「仍在**裁剪祖先**之内」
□ 若给「已有控制器」管着的容器加了同构控件：**新件用了独立类名**（没复用老件的类），并用「操作新件后老模块的选中项 / 行数 / 折叠数计数**一字未变**」反证；走老代码通用动作循环的新按钮已 `return` 跳过（不再多弹假提示）
□ 若新加了**铺满面板的覆盖层 / 遮罩**：探针里点它外面的按钮之前**必须先关掉它**（遮罩会挡住自己的触发器，症状 = 把「切视图失败」误判成 bug）；且**别写 `q() || fn().click()` 这种短路表达式**（左侧命中就短路、动作根本没执行）
□ 若新规则声明了 `height` / `line-height: calc(Npx * var(--ratio))`：**同一条规则里必须有 `var(--font-size-*)` token**（否则收尾的 `converge()` 会把它压平成裸 px、门禁多报一条），并用「放大字号后量派生值」验证（默认档下看不出来）
```

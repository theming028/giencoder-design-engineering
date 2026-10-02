---
name: css-state-pixel-evidence
description: >-
  用「元素截图 + 逐像素取色 + 逐行分组 diff」证明一次 CSS 视觉改动「改对了」且「只改了该改的」。
  当用户报「hover 底色和选中态不一致 / 默认不该有背景色 / 这个图标颜色有点深，浅一级 /
  圆角不一样 / 颜色不对」这类**纯视觉状态**问题时使用；也用于任何改完 hover / active / focus /
  图标色 / 描边 / 圆角后需要出前后对照取证的场景。
  触发词：hover 背景色、选中态底色、常显背景色、默认没背景、颜色深一级浅一级、圆角不一致、改前改后对照、
  只改了该改的、逐像素取色、元素截图、diff 取证、视觉回归、
  点了没反应、展开折叠失效、display 没生效、状态互斥、特异性打平、
  统一字体族、不要单独设定字体、子树里还有残留、整片区域字体不一样、注释里写了被清理的词、
  文字没居中、居中改不动、盒宽钉死、谁在管这个 width、文字真实盒、Range.selectNodeContents、
  居中同时还要省略号、fit-content 没生效、margin auto 不居中、
  菜单位置不对、应该在触发按钮的下方、下拉跑到按钮上方、弹层锚定、dy 判据、浮层位置取证、
  动效太慢、数字动效、还以为没有数字、延迟太久、骨架屏挡住了、遮罩退场、空窗时间、
  输入框聚焦没反应、focus-within、激活态、描边把盒子撑高、inset 描边、
  覆盖层跟着滚动跑了、闪一下看不见、hidden 没生效、display flex 压过 hidden、
  DS 按钮默认主色、-text 按钮、点了只弹 toast、
  覆盖层挡住自己的触发器、遮罩挡住了按钮、短路表达式没执行、
  新件与老件共用类名、操作新控件把老控件带坏、派生高度被压平、门禁多报一条
agent_created: true
---

# CSS 状态改动的像素级取证配方

> 适用：任何「改一个 CSS 视觉属性 → 要证明视觉上确实改了、且没误伤别处」的场景。
> 核心三件套：**① 真鼠标态元素截图 ② 同坐标取色断言 ③ 逐行分组 diff**。
> 三者缺一不可：① 给人看，② 证明「色值精确相等」，③ 证明「改动范围可控」。

## 一、总流程（一次 bash 调用内跑完整条链）

```bash
NODE="<node 绝对路径>"; AB="<agent-browser CLI 绝对路径>"; URL="file:///<page>.html"
"$NODE" "$AB" set viewport 1440 900                      # ★ 必须在 open 前，且必须设
"$NODE" "$AB" open "$URL"
"$NODE" "$AB" wait 900
"$NODE" "$AB" eval "$(cat probe-default.js)"  > t0.txt    # 默认态
"$NODE" "$AB" hover "<selector-A>"                        # ★ 真鼠标悬停
"$NODE" "$AB" wait 400
"$NODE" "$AB" eval "$(cat probe-default.js)"  > t1.txt    # A hover 态
"$NODE" "$AB" screenshot "<container>" shot-A.png         # 元素截图
```

★ **hover / click 必须是真鼠标命令**，不要用 `el.click()` / 程序化派发：
合成事件的 `event.detail === 0`，会被业务代码当**键盘**触发，焦点环、激活态全都不对。
★ 需要「按住拖动」时**不要跨 bash 调用保持鼠标按下** —— 浏览器守护进程会被回收。
改用**单次 `eval` 内派发完整合成事件序列**（down → move… → up）。

## 二、取色：★★ 坐标口径（最容易踩的一条）

`screenshot "<sel>"` 得到的图，**原点 = 该元素自身的左上角**，**不是视口原点**。
直接拿视口坐标去 `im.getpixel((x, y))` 会全部落到「元素外的页面背景 / 相邻元素」上 ——
而**容器自身的底色看起来和"透明"一模一样**，于是会把「无底」误读成「有底」，或把
「真正的高亮色」误读成「过渡动画没收敛」。

**正解**：先 `eval` 打一次「元素 rect − 容器 rect」的差值，得到**元素内相对坐标**，再据此取色。

```js
// 在页面里跑：返回「容器内相对坐标」表
(function () {
  var c = document.querySelector('<container>'), R = c.getBoundingClientRect();
  function rel(el) { var r = el.getBoundingClientRect();
    return [r.x - R.x, r.y - R.y, r.width, r.height]; }
  return JSON.stringify({
    containerBg: getComputedStyle(c).backgroundColor,          // ★ 先量容器底色！
    back: rel(document.querySelector('<selector-A>')),
    item: rel(document.querySelector('<selector-B>'))
  });
})()
```

**取色点选择**：取元素的**净区** —— 水平方向避开图标与文字（取靠右的空白处），
垂直方向取**元素竖向中心**。写死之前先用上面的 rect 表核对一遍。

### 判定「透明 / 无背景」的唯一正确判据

**取到的像素 == 容器自身的底色**。所以 `containerBg` 必须先量出来。
（常见陷阱：容器底色是 `#F4F5F6` 这类浅灰，与「浅灰底 hover」肉眼几乎没法分辨。）

### 判定「两处底色一致」

在**同一相对坐标**上分别截 A 与 B 两种状态，断言取到的像素元组**逐通道相等**：

```python
assert pb.getpixel((X, Y)) == ph.getpixel((X, Y)) == ps.getpixel((X, Y))   # 逐通道相等
```

三条都要取：**A-hover / B-hover / B-选中**，一次证明「hover 之间一致、hover 与选中也一致」。

### hover 动画没收敛的排查

带 `transition` 的属性，`hover` 后立刻截图可能拿到**中间帧**（介于起始色与目标色之间）。
`wait 400` 通常够（`.12s` 过渡），不够就加到 `1200`；
⚠ 但**先排除第二节的坐标错位**再说 —— 坐标取错时读出的"中间色"往往其实是**容器底色**。

## 三、逐行分组 diff：证明「只改了该改的」

把改动前后的**同态同元素截图**做像素差，按行聚类成「差异行组」，再逐组归因：

```python
# 阈值 >8 的差异像素，按行聚合 → 连续行合并成组 → 打印每组的 y 范围 / 像素数 / x 范围
```

**判据**：**每个差异行组都必须能指到某一条具体改动**，数量要对得上，不能有「意外组」。

非常有用的两个特例：
- **只动了圆角** ⇒ 差异应**只出现在四角的极小区域**（一行就能证明「盒子没动，只动了角」）。
- **只动了「图标 → 文字」形态切换里图标那一半的颜色** ⇒ 差异应**只出现在未 hover 的行**；
  **被 hover 的那一行反而不该出现在差异里**（那一态它已 `display:none`）。
  这反过来证明「`color` 只下移到 `> svg` 上」的写法正确。

## 四、一行技巧：同一控件里「图标」比「文字」浅一档

需求「图标颜色浅一级、文字别动」时，**不要改按钮自身的 `color`**（那会连文字一起改），
把 `color` 下移到图标节点上：

```css
.act > svg { color: var(--color-text-2); }   /* 只作用图标；按钮 color 保持 text-1 ⇒ 文字不变 */
```

前提是图标用 `currentColor` 描边。若该控件的态切换是「默认显示图标 / hover 显示文字」，
两者天然互斥，这一招等价于「同一按钮两种深浅」。

## 五、坑清单

| 坑 | 症状 | 对策 |
|---|---|---|
| **元素截图原点搞错** | 取到的像素全是相邻元素/容器底，误判成「过渡未收敛」 | 先打 `el.rect − 容器 rect` |
| **没量容器底色** | 分不清「透明」与「浅灰底」 | 同一次 eval 里带出 `containerBg` |
| **视口没设** | 元素截图**超出视口的部分渲染成空白** ⇒ diff 出现巨大假差异（曾报 7.5%，真值 1.5%） | `set viewport 1440 900`（或更高），并 `eval window.innerHeight` 核对 |
| **合成 `click()` 取态** | 焦点/激活态不对（被当键盘触发） | 一律真鼠标 `click` / `hover` |
| **跨调用保持按下** | 守护进程被回收，后续命令全失败 | 单次 eval 内派发完整事件序列 |
| **改完不重开页面** | `eval` 报 `Cannot read properties of null` | 每次量测前重新 `open` |
| **读自定义属性用错 API** | `getComputedStyle(el)['--x']` 恒 `undefined` | 用 `getPropertyValue('--x')` |
| **只看汇总数** | 「问题总数没变」≠「零影响」 | 汇总数相同也要**逐条 diff** 明细 |
| **点在 `display:none` 的元素上** | 命令 exit 0、页面毫无变化 ⇒ 静默假失败（会误判成「功能坏了」） | 点前先过滤 `offsetParent !== null`，或改点可见的那条选择器分支 |
| **先点后读分成两次 `eval`** | 读到的是**已自动消失**的态（如 toast 1.4s 自隐）⇒ 报「没出现」而实际出现过 | 点击与读取写在**同一次 `eval` 内部** |
| **选择器层级选错** | 拿外层容器（如 `<article>`）量 `display`，量不到里层互斥态 ⇒ 误判「改了没生效」 | 量之前先数 `querySelectorAll` 匹配数、确认命中层与预期一致 |
| **只改写死的那几处** | 子树里靠**继承**的节点漏改（实测 153 个 `.td-code*`），改完看着「应该是好了」 | 判据遍历 `root.querySelectorAll('*')` 与 `body` 的取值比对，残留**按 `tagName+className` 分组**定位父级 |
| **自己在注释里写了被清理的词** | 全页字面量计数**永远归不了零** ⇒ 被误判成「漏改一处」 | 注释用中性表述、**不写字面值**；探针/日志别写进页面本体 |
| **`bad.slice(0, N)` 后输出** | 报「只有 N 个」而真实远大于 N ⇒ 漏掉整类残留 | 用**独立计数器**，列表另存 |
| **假设同族组件样式一致** | 给了一个选中类底色、另几个下拉还是裸的 | 判据数**命中数 vs `.is-checked` 总数**（期望全等） |
| **过渡中取值** | 写死 `182px` 却量到 `174.72`（弹层尺寸）；拖拽起点量到**中间值** ⇒ 判据对不上 | ① 等过渡结束再量；② **更稳：改读「声明值」** —— `el.style.getPropertyValue('--x')` 不受过渡影响；③ 若要量几何，先落「拖拽 / 无过渡态」类（`transition:none`）再取 rect |
| **`focus()` / `blur()` 后「同步」读 `getComputedStyle`** | 读到的是**过渡起点**（实测 `rgba(0,0,0,0) 0px 0px 0px 0px inset`、恒为旧值）⇒ 误判「样式没生效」，回头乱改 CSS | 等过渡走完再读：`focus → setTimeout(…, 400) → 快照 → blur → setTimeout(…) → 快照`，存 `window.__X` 再另一次 eval 取回（`transition: 120ms` 时 400ms 足够）—— ★ **这是「改完没生效」误报的头号来源** |
| **覆盖层挡住了「它自己的触发器」** | 想点覆盖层**外面**的按钮（如工具条上的 `⋯`），却点到**遮罩** ⇒ 覆盖层被关掉、切换动作根本没发生 ⇒ 误判成「新改动把旧功能弄坏了」 | 点之前**先断言覆盖层已关闭**（`layer.hidden === true`），关掉再点；报告里把「先关 A 再点 B」写成显式步骤 |
| **`q(sel) \|\| (fn)().click()` 短路表达式** | 左侧 `querySelector` 命中（**哪怕元素是 `hidden` 的**）就短路 ⇒ 右侧动作**根本没执行**，读数看起来却「点过了」 | 别用短路：`const el = q(sel); if (el) el.click(); else fn().click();` |
| **新写的规则声明了派生高度却没配字号 token** | 收尾的收敛脚本把 `calc(Npx * var(--ratio))` unscale 成裸 px、又不再重派生 ⇒ 门禁「可疑条目数」**多出 1 条**（汇总数变化 ⇒ 进回归 diff） | 同一条规则里补一条 `var(--font-size-*)`；并用**放大字号档**验证派生值确实跟着变（默认档下 `calc(Npx × 1) = Npx`，看不出） |

## 五·b、行为类改动（拖拽 / 缩放）的取证

这类改动**没有像素可看**，判据要换成「**声明值 + 事件是否收到**」：

* **声明值**：`el.style.getPropertyValue('--x')` 前后各取一次，断言增量 == 鼠标位移（声明值不受
  CSS 过渡影响，比 rect 可靠）。
* **事件是否收到**：合成 `PointerEvent` 时把 `pointermove` / `pointerup` **派发到 `document.body`**
  —— 正确挂在 `window` 上的实现照样响应，挂在元素上的**静默失效**。这一招同时验了「起点对不对」
  与「事件挂在哪」，比真鼠标拖拽快且可复现。
* ⚠ **同一个函数可能被绑到多个元素**（如「预览栏分栏条」与「文件树分栏条」共用一份 `bindSplit`）
  ⇒ 两处都要各跑一遍；且要知道**有些档位本来就拖不动**（clamp 下限，如右栏 561 = 树 240 + 1 + 代码 320
  ⇒ 树已无空间）—— 别把「正确的钳位」当成 bug。验之前先**把容器拉到有空间**。

## 六、改了 `display` 却「没生效」⇒ 先查特异性打平

互斥态（展开/折叠、显示/隐藏、统一视图/并排视图）常被写成两条**同特异性**的 `display` 规则。
此时胜负**只看文档顺序**，后写的那条永久胜出 —— 症状是「点了没反应」**且控制台零报错**。

```css
/* (0,3,0) 统一视图：折叠态藏起来 */
.td-diff:not(.is-open) .td-diff-rows { display: none; }
/* (0,3,0) 并排视图：非并排版藏起来 —— 打平，谁在后面谁赢 */
.td-split .td-diff-rows:not(.td-split) { display: none; }
/* 正解：给该赢的那条再挂一层类，提到 (0,4,0) */
.td-split .td-diff.is-open .td-split-rows { display: block; }
```

**验证必须走四象限实测**，不要只测一路：
`{默认视图, 并排视图} × {展开, 折叠}` 四格逐格量 `display`。
只测「并排 + 展开」会通过，而**「并排 + 折叠」才是坏的那格**。

## 七、统一「一整片子树」的某个属性（字体族 / 字号）⇒ 判据要覆盖整棵子树，并分组定位残留

需求形如「XX 区域所有字体统一用全局默认字体族，不要单独设定」。**逐个改写死的地方是不够的** ——
老页面里同一属性常有三层来源：**本代样式 / 跨代移植件（历史代已交付、本轮按规定不复改）/ 内联**。

**判据（一层都不能少）**：

```js
var root = document.querySelector('.td-browse');
var bodyFont = getComputedStyle(document.body).fontFamily;
var all = 0, badN = 0, bad = [];
root.querySelectorAll('*').forEach(function (el) {
  all++;
  if (getComputedStyle(el).fontFamily !== bodyFont) { badN++; bad.push(el); }
});
console.log(all, badN);      // ★ 目标：badN === 0
```

* ★ **别把 `bad` 截断后再输出**（`bad.slice(0, 8)` 会让人误读成「只有 8 个」）⇒ 用**独立计数器**。
* ★ **残留必须按 `tagName + className` 分组**，否则定位不到「残留的父级」：
  ```js
  var g = {};
  bad.forEach(function (el) { var k = el.tagName + '.' + el.className; g[k] = (g[k] || 0) + 1; });
  ```
  实测一跑就暴露出 **153 个 `.td-code*`** —— 它们的字体来自**跨代移植件里的一条父级规则**
  （`browse.css` 的 `.td-browse-pre`），子节点全靠**继承** ⇒ 逐个给子节点补 `font-family` 纯属白费功夫。
* **跨代移植件不复改**（动了会污染已交付代）⇒ 在**当代样式里用「多一级类数」覆盖**：
  ```css
  .td-browse .td-browse-pre { font-family: var(--font-family); }   /* 比 .td-browse-pre 多一层 ⇒ 必胜 */
  ```
* ★ 改完**再跑一次同一判据**（子树计数归零）+ **抽样几个代表节点打印 `fontFamily`** 交叉确认。
* ⚠ 字体族的比较是**字符串全等**：`var(--font-family)` 算得的值必须和 `body` 算出的**逐字相同**
  （引号、空格、`-apple-system` 这类保留字都不能差）⇒ 别手工拼字体串，一律用同一个 token。

### ⚠ 自己新写的「注释 / 探针 / 日志」里不要出现被断言的 token

做**全页字面量清理**（如「把 A 词全替换成 B 词」）时，断言是「A 的计数 == 0」。
若你在**同一次改动里新写的 CSS 注释**中提到了 A（哪怕是「A / B → C」这种说明性写法），
**计数就永远归不了零**，看起来像「漏改了一处」，其实是自己造的。
**对策**：注释里用**中性表述**（「竞品名 → 本产品名」），**禁写字面值**；探针与日志也一律别写进被断言的页面本体。

### ⚠ 「选中态要常显底色」⇒ 别假设同族组件行为一致，也别让它被 `:hover` 抢走

* **别假设同一个 DS 里两个选中类长一样**：实测 `.giencoder-menu-item-selected` **自带** `background`，
  而下拉的 `.giencoder-dropdown-item.is-checked` **只有 `color` + 左侧 3px 条**（没有底色）。
  要「常显底色」就得自己补 —— **一个候选都不能漏**（本仓同一页有 3 个下拉：`.td-mod-menu` / `.td-rv-menu` / `.td-ctxmenu`）。
* **写在更靠后的文档序里**（或提特异性），并确认**不会被 `:hover` 规则盖掉**（hover 一走开底色就消失 = 写错位置）。
* **判据是逐个量色值，不是「看着有底了」**：对**每一个** `.is-checked` 量
  `getComputedStyle(el).backgroundColor`，断言**逐通道等于目标 token**（实测 `rgba(0,0,0,0)` → `rgb(245,248,255)`）。
  ⇒ **数「命中了几个」**，期望 = 页面上 `.is-checked` 的**总数**（实测 4 / 4），少一个就是漏了一个下拉。

## 八、★ 对齐类需求（居中 / 靠右 / 贴边）的取证：量**文字真实盒**，不是盒子盒

「这段文字要居中」这类需求，**盒子对了不代表文字对了** —— 盒子可能满宽而文字靠左。

### 8.1 先查「谁在管这个盒子」

改不动时**别继续叠 `width`**：多半是**页面级 `!important`** 把盒宽钉死了。
**反证手法**（一条就定性）：

```js
// 依次注入这三种状态，每次重新量盒宽
// a) 原样  b) min-width: 0  c) width: 100%
// ★ 三态盒宽全等 ⇒ 盒宽不由你改的这几条决定 ⇒ 去翻页面级规则里的 !important
```

实测教训：`.r107-stats` 的盒宽由**两条页面级 `!important`**（同一选择器 `main > … > div.mt-8 > div`
的两个历史版本）钉住 ⇒ 盒宽**恒等于输入卡**（860 / 714 / 315 三档全等），
`fit-content + margin: auto` 那一版是**纯死代码**。

### 8.2 判据 = `Range.selectNodeContents` 取文字盒，与基准元素比中心

```js
function textBox(el) {
  var r = document.createRange(); r.selectNodeContents(el);
  return r.getBoundingClientRect();            // ★ 文字真实盒
}
var t = textBox(el), h = document.querySelector(BASE_SEL).getBoundingClientRect();
console.log(Math.round((t.left + t.right) / 2 - (h.left + h.right) / 2));   // ★ 期望 0
```

* 同时打印 `盒.left / 盒.width / 文字.left / 文字.width` —— 一眼能看出「盒对、文字偏」。
* ★ **真节点 ≠ 伪元素**：`::after` 是 shrink-wrap 的（盒随文走）；换成真节点后是**满宽盒**，
  文字默认靠左，而宿主的 `items-center` 对满宽子项**不生效** ⇒ 靠 `margin: auto` 会比基准**偏 32px**
  （实测：输入卡自己就是齐左的）。
  ⇒ 这类场景**正解是 `text-align: center`**（它没有 `!important` 竞争者）。

### 8.3 「居中」与「溢出省略」可以共存 —— 别凭常识下结论

同一条规则里既要 `text-align: center` 又要 `text-overflow: ellipsis` 时，别想当然写「互相打架」。
**实测（Chromium）**：内容宽 > 盒宽时，居中**退化为 `start`**（文字盒仍自盒左缘起算）
⇒ **省略号照常落在行尾**（截图尾部实测为「首 token 平…」）。

★ **写进代码注释里的实测结论必须来自截图 / 取值**，不能来自「应该是这样」——
本仓就发生过一次：注释把上面的关系写反了，看截图后**整块更正**。写反的注释比没有注释更危险。

## 九、★ 浮层「位置不对」类需求的取证：量 **dy**，别只看截图

用户说「菜单位置不对，应该显示在触发按钮的下方」时，**先量后改** —— 同一基类里的多枚浮层
很可能「一枚对、几枚错」，瞟一眼截图一定会漏。

```js
/* 对每一枚 [菜单, 触发器] 输出：dy / 水平覆盖 / 所在容器 */
var dy      = +(mRect.top  - tRect.bottom).toFixed(1);   // > 0 = 在下方；期望 ≈ 一个 gap
var dxLeft  = +(mRect.left - tRect.left).toFixed(1);     // 0 = 左缘对齐
var coversH = (mRect.left <= tRect.left + 0.5) && (mRect.right >= tRect.right - 0.5);
```

* ★★ **必须逐枚量、列表对比**：本站 4 枚下拉里 1 枚 `dy = +6.5`（对）、3 枚
  `dy = −35 / −34 / −36`（跑到**按钮上方**）。**只验用户点名的那一枚，会漏掉同因的另外两枚。**
* ★ **判据写「相对量」不写「绝对坐标」**：`dy` 与 gap 比、`dxLeft` 与 0 比 ——
  绝对 y 随视口 / 滚动 / 面板宽度变，比不了。
* ★ **改完在同一张表里复量，并把「不该动的那枚」也带上当回归**（本站 `.td-mod-menu` 全程
  `top 42 / left 64` 不变 —— 这才是「没改别的模块」的证据）。
* ★ **窄栏压力测试**：把宽度变量（`--av-browse-w` 之类）压到最小值，量**「是否仍在裁剪祖先之内」**
  —— 菜单挂在 `overflow: hidden` 的祖先里时，溢出会被**无声裁掉**，只量「在面板内」发现不了。
* ★ **行为回归三步，一步都别省**：① `press Escape` 关 ② 点空白关 ③ **关了再开，位置是否一致**
  （验「内联样式不被上一次的残留值污染」）。再顺带验一个**同类但没改**的浮层（本站 = 右键菜单
  `.td-ctxmenu`）没被带坏。

## 十、★ 「动效太慢 / 根本没看见」⇒ 先量「**遮罩退场**」的时间线，再两边一起改

用户说「这个数字动效实在是太慢，还以为没有数字呢」——**别先去调 `duration`**。

**第一步：量真实时间线**（在页面里装一个 rAF 轮询器，记录三个时刻，相对 `performance.now()`）：

```js
var t0 = performance.now(), R = { tSkOut: null, tSkGone: null, tNumVisible: null };
(function tick() {
  var sk = document.querySelector('.r93-sk');
  var num = document.querySelector('.r93-num-i');
  if (!R.tSkOut && sk && sk.classList.contains('is-out')) R.tSkOut = performance.now() - t0;
  if (!R.tSkGone && sk && !sk.isConnected) R.tSkGone = performance.now() - t0;
  if (!R.tNumVisible && num && +getComputedStyle(num).opacity > 0.5) R.tNumVisible = performance.now() - t0;
  if (!(R.tSkGone && R.tNumVisible) && performance.now() - t0 < 5000) requestAnimationFrame(tick);
  else window.__TL = R;
})();
```

★ **判据取「遮罩移除时刻」与「内容首见时刻」这对量** —— 别用「遮罩开始淡出」：
轮询器**装得太晚**会漏掉早段（本站实测 `tSkOut = null` / `late = 1`，纯属探针自己的人为产物，
却最容易被误读成「产品问题」）。

**本站实测**：骨架屏 2012 淡出 → 2326 移除 → 数字 **2493** 首见（**2.5 秒**）。

**第二步：找「为什么延迟」** —— 本站是 `animation-delay: calc(1.5s + ni*55ms)` + `fill: both`：
延迟期停在 `from`（`opacity: 0`），而数字容器是 `inline-block` ⇒ **空位一直占着、窗口是空的**。
那个 1.5s 的语义是「**等骨架屏退场**」：`.r93-sk` = `position:absolute; inset:0` + **不透明**底色
⇒ **早于它退场的任何动效都白做**。

**第三步：两边一起改**（只改一边必然无效）：

| 只改哪边 | 结果 |
|---|---|
| 只提前动效 | 被遮罩盖着 ⇒ 白做 |
| 只提前遮罩 | 动效还在等 ⇒ 依旧慢 |
| **两边一起** | 空窗 **167ms → 0**，整体 ~1.66s ✓ |

* 遮罩侧：`setTimeout(→ 加 is-out, 1100)` → `380`（**保留末尾那条 `320`**：CSS 的
  `transition: opacity .3s` 走完正好 300ms，再早移除会跳一下）。
* 动效侧：`duration: 0.46s → 0.30s`、`delay: 1.5s → calc(0.44s + ni*26ms)`
  —— **只覆写这两条长属性**，别动 `animation-name` / `fill-mode`（改错会变成完全不同的一套动效）。
* ★ 判据 = **`tSkGone === tNumVisible`**（空窗归零）+ 回读 `getComputedStyle(num)` 的
  `animationDelay / animationDuration / animationFillMode` 确认只有该改的变了。

⚠ **同一处动画只要超过 `300ms`**，很多设计规范自检脚本会直接报「动画时长超限」——
改延迟时顺手把 `duration` 收到 `≤300ms`（本站 260 / 300 都是刻意卡在线上）。

## 十一、★ 三张「态与覆盖物」的口径（都踩过）

### 11.1 DS 的 `-text` 按钮默认是**主色**；DS 输入框的激活态有固定口径

* 需求「这个浮条的图标和文字**默认应该是正文黑**」→ 先读基类：DS 的 `.giencoder-btn-text`
  把 `color` 定成 `--color-primary-6`（实测 `rgb(55,112,247)`）。
  修法 = 后置同特异性更高的规则 `.td-selbar .giencoder-btn { color: var(--color-text-1) }`
  （SVG 走 `currentColor`，**自动跟着变、不必单独点图标**）。
  判据：逐枚量 `color` + 图标 `stroke` / `color`，期望**全等于正文 token**（实测 `rgb(31,31,31)`）。
* 需求「输入框少了『输入中激活态』」→ DS 的现成口径是
  `.giencoder-input-wrapper:focus-within { border-color: primary-6; box-shadow: 0 0 0 2px primary-light-2 }`。
  **但 Pill / 定高形态要改用 `inset` 描边**：

```css
.td-url-pill:focus-within {
  background: var(--color-bg-2);
  box-shadow: inset 0 0 0 1px var(--color-primary-6), 0 0 0 2px var(--color-primary-light-2);
}
```
  ★ 写 `border` 会把**定高胶囊撑高 2px** ⇒ 判据必须同时量 `boxH`（改前 26 / 改后**恒 26**）。
  取证照第 5 节那条走：**focus → 等 400ms → 读 → blur → 等 400ms → 读**（同步读会拿到起点值）。

### 11.2 覆盖层**别放进滚动容器**；给自带 `display` 的类加 `[hidden]` 必须**显式写规则**

* 「点一下整块闪一下」这类覆盖层，若挂在 `overflow: auto` 的容器上（本站 `.td-view`），
  绝对定位子元素会**跟着内容滚走** ⇒ 用户滚动之后**什么都看不见**。
  ⇒ 挂到**最近的、非滚动的**祖先（本站 = 给 `.td-mod.td-brw` 补 `position: relative`，
  覆盖层 `::after` 挂在模块上，反而「闪整个面板」更符合语义）。
* 另一半是同一个坑：**自带 `display` 的类会压过 UA 的 `[hidden] { display: none }`**
  （本站 `.td-pv-md { display: flex }` 与 `.td-mod { display: flex }`）
  ⇒ 凡是切换显隐的覆盖层 / 分栏，一律补 `[hidden] { display: none }`。
  判据：切完量**两套骨架的 `hidden` 属性 + 各自 rect**，而不是「看着只剩一个」。

### 11.3 「有入口、点了只弹一句 toast」= 真缺口

做「对照某产品的官方功能清单补缺」这类任务时，**缺口判据不是「有没有这个按钮」，
而是「点了之后有没有真的视觉 / 结构变化」**。本站两个实例：「产物 · 预览」只 `say()`
一句提示、「新建终端标签」只弹 toast ⇒ 都算缺口。
补的时候**优先补视觉 / 结构**（预览层 / 新标签页），不是补文案。

★ 顺带一条：**新开的浮层 / 覆盖层必须接进既有的 Esc 裁决链**，否则「开着它按 Esc」会落到
下一层的处理器上（本站 = 直接把**整条侧栏**关掉）。判据 = 开着目标层 `press Escape` 后断言
「目标层已关 **且** 外层仍在」（`prevHidden=true` **且** `paneOpen=true`）。

### 11.4 ★★ 覆盖层会挡住「它自己的触发器」⇒ 探针里必须先关掉再点

* 场景：新加一块**铺满面板**的覆盖层（抽屉 / 全屏层 / 模态），遮罩 `inset: 0` + `z-index` 高于面板内容。
* 坑：**开着它的时候，面板里任何按钮都点不到** —— 想点工具条上的 `⋯` 切视图，实际点到的是**遮罩**
  （覆盖层被关掉、切换动作**根本没发生**）⇒ 探针读数 `isSplit:false` ⇒ 误判成「新改动把旧功能弄坏了」。
* ★ 正解：点之前**先断言目标层已关闭**（`layer.hidden === true`）再点，并在报告里把
  「先关 A 再点 B」写成显式步骤（否则下一个人还会再踩）。
* ⚠ 同一族的**探针自伤**：别写 `document.querySelector(sel) || (fn)().click()` —— 左侧命中
  （**哪怕元素是 `hidden` 的**）就短路，右侧动作**根本没执行**，读数却看起来「点过了」。
* ⚠ 另一个自伤面：**点覆盖层里的行**却断言外层模块的选中态 —— 新件若与老件**共用类名**，
  两边会互相接管（`querySelector` **只返回第一枚**）⇒ 见 `compiled-bundle-jsx-patch` 六·同构控件。
  判据 = **操作新件后，老模块的选中项 / 行数 / 折叠数计数一字未变**。


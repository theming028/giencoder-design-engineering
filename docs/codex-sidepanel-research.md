# Codex 右栏（Side Panel）调研速报

> 目的：为「复刻 Codex 右栏（展开后全部内容）」做前置调研 —— 功能 / 布局 / 交互。
> 结论当前为**初稿**，待邵先生拍板后再进入落地规划。
> 证据：12 张实机截图存于 `docs/codex-refs/`（来源见文末「来源」），机器版本 = Codex app 26.x（2026-09 截图）。
> 状态：**未提交**。创建日期 2026-10-01。

---

## 0. 一句话结论

Codex 右栏**不是一个面板，是一套「可多开的标签式侧栏（Side Panel）」**：
它把「Review(diff) / Terminal / Browser / Files / Side chat」五类内容装进**同一个右侧容器**，
每个模块只在**同一个骨架**里换掉「第二行工具条 + 正文」；
用户从顶栏右上角一个按钮 → 弹出四选一菜单来「展开」它，其余全靠快捷键与对话里的入口卡。

**对我们的直接价值**：`pages/conversation.html` 里 r105 ③ 已经有一个右栏骨架
（`aside.td-browse` + 44px bar + 单标签「摘要」+ 「新建标签」+ 拖拽分隔 + 全屏 + 文件树 + 代码视图 + 暗色档），
**骨架 ≈ 已经到位 70%**，缺的是「多模块、多标签、diff / 终端 / 浏览器 / 侧边聊天」这四块内容件。

---

## 1. 整体框架：右栏在哪儿

Codex App 是**三栏 + 两条可选边**：

| 区域 | 内容 | 可收起 |
|---|---|---|
| 左 任务管理框 | New chat / Pull requests / Scheduled(自动化) / Plugins / Explore；Pinned / Projects / Recents 分组；底部账号行 | `Ctrl+B` |
| 中 对话交互区 | 回复、计划、命令、工具调用、审批卡、产物卡；底部 composer（= 任务控制台，不只是输入框） | — |
| 右 **Side Panel** | Review / Terminal / Browser / Files / Side chat（标签式） | `Ctrl+Alt+B`（Review）/ `Ctrl+Shift+B`（Browser） |
| 底 底部面板 | 终端等；**设置项 `Default terminal location`** 决定终端开在底部还是右侧 | `Ctrl+J` |

顶栏（对话区上方一条）左端 = 会话名 + `⋯`；右端 = `模型 pill ⌄` `ⓘ` **`▭`（底部面板）** **`◧`（右栏）**。
两个面板按钮是**同一种 1.5px 描边圆角矩形字形**，激活态 = 深色反白 —— 截图 `docs/codex-refs/00-app-frame-3pane-empty.webp`。

---

## 2. 右栏的骨架（★ 三段式，五个模块完全共用）

```
┌──────────────────────────────────────────────────────────────┐
│ ① 标签栏  [▤ Review] [🌐 Flavio Copes ×] [ ] +   ⤢  ▭  ◧    │  44px 级
├──────────────────────────────────────────────────────────────┤
│ ② 模块工具条  ← 只有当前激活模块自己的操作（可无）              │  约 40px
├──────────────────────────────────────────────────────────────┤
│ ③ 正文   模块内容，独立滚动，不带动外层                       │
└──────────────────────────────────────────────────────────────┘
   ▲ 左缘 = 拖拽分隔条（改宽）；tab 可拖拽重排；⤢ = 全屏
```

- **① 标签栏**：`[模块图标] 标签名 [×]` + 末尾 **`+`（新建标签）**；右端固定三个全局按钮：`⤢`（展开/全屏）、`▭`（底部面板）、`◧`（右栏开关，当前激活则深色）。
  - 标签名会「自带上下文」：Terminal 标签显示 `~/w/flaviocop`（路径），Browser 标签显示 `🌐 Favicon + 页面标题`。
  - **一个容器里可同时挂多个标签**（Files 模块里就出现 `config.ts | # global.css ×` 两个代码文件标签）。
  - changelog 26.409 明确：**标签可拖拽重排（drag-and-drop tab reordering）**。
- **② 模块工具条**：每个模块一行自己的动作，例如 Review 是「范围选择器 + 增删计数 + ⋯ + 复制 + 打开于 + Commit ⌄ + Open PR」；Terminal / 纯文本类**没有这一行**。
- **③ 正文**：占满剩余高度、自己滚。面板宽度可拖，实测约占窗口 **45%~55%**（比中栏还宽）；`⤢` 后铺满。

---

## 3. 五个模块逐个拆

### 3.1 Review —— 文件 diff（★ 信息密度最高，也是用户点名要的「文件 diff」）

**工具条（第二行）**：`Last turn ⌄`（或 `Branch ⌄` / `All changes`，切范围）+ **`+566 -228`（增/删行计数，绿/红）**
右端：`⋯`（显示选项菜单）、`复制`、`在窗口打开`、`在文件树中定位`、**`⑂ Commit ⌄`**、**`◐ Open PR`**。
`Commit ⌄` → 下拉两项：`⑂ Commit` / `⬆ Push`（截图 `05-...`）。

**正文**：文件为单位折叠块
```
src/content/lessons/astro-basics/7-css.md                    +24 -23  ⌃
  ⌃ 41 unmodified lines            ← 「未改动行」折叠条，可展开
  42 │ 42   In this case, the CSS file needs to be in the `public` folder.
  45 │ 45   To use Tailwind CSS, run the command:          ← 旧行（红底）/ 新行（绿底）
  51 │ 51   ![](img/Screenshot-...png)                      ← 分隔的两段大块
```
- **两列行号**（旧 / 新）+ 左缘**绿红变更条**；整块红底/绿底；行内词级高亮（Enable word diffs）。
- **视图形制可切**：`split`（左右对照，截图 `04-...`）/ `unified`（上下）。
- **`⋯` 菜单**（截图 `03-...`）：Refresh / Enable word wrap / **Collapse all diffs** / Don't load full files / Enable rich preview / **Enable word diffs** / Hide white space / Copy git apply command。
- **行内评论**：可在具体代码行旁留 comment（26.406 起支持「折叠 inline comment」+「inline/detached 两种模式」）。
- **`Commit` 弹窗**（截图 `06-...`）：标题 `Commit your changes`；字段 `Branch`(⑂ 仓库名) / `Changes`(20 files +1,900 -1,736) / 开关 `Include unstaged` / `Commit message` 文本域（placeholder「Leave blank to autogenerate a commit message」，右侧 `Custom instructions` 链接）；主按钮 `Continue`。
- 空态/加载态：截图未覆盖 ⇒ **待补**（见 §7）。

### 3.2 Terminal —— 集成终端

- 标签名 = **当前工作目录缩写**（`~/w/flaviocop`），带 `×` 与 `+`；**每个任务线程一套终端标签**。
- 正文极简：一整块等宽字体，只有一行提示符
  `➜ flavicopes.com git:(master) ✗` + 光标 —— **没有额外装饰条**（截图 `07-...`）。
- 可跑任何命令；**Codex 能读当前终端输出**（所以「读终端报错并修」这条工作流成立）。
- 默认位置由设置决定（底部 / 右侧）⇒ 「右栏里的终端」与「底部面板里的终端」是**同一组标签的两种落位**。

### 3.3 Browser —— 内置浏览器（★ 含「注释模式」这个杀招）

- 标签名 = `🌐 favicon + 页面标题`（例：`Flavio Copes`）。
- **URL 行**：`← → ⟳` + 居中地址（只显示域名，如 `flavicopes.com`）+ 右端 `⊕`(缩放) `⤓`(下载/发送) `⋮`；**注释模式开启时右端多一枚蓝色 `⊙ Annotating` 药丸**。
- 正文 = 真实渲染的网页（独立 profile，不带你的 Chrome 登录态）。
- **注释模式**：点元素 → 元素被高亮 + 就地弹出一个**注释输入浮条**：
  `[元素 chip: flavicopes.com] [⇄ 属性图标] [输入框 "make this uppercase|"] [✓ 圆形发送]`
  发送后该元素 + 截图 + DOM 路径一起进 composer ⇒ 直接「指哪儿改哪儿」。
  （截图 `08-...` 普通态 / `09-...` 注释态）
- 还有：⚙ Developer mode 可看 DOM / console / network / performance。

### 3.4 Files —— 项目文件

- 这个模块**内部自己又分两栏**：左 = 代码视图（`config.ts | # global.css ×` 文件标签 + 面包屑 `flavicopes.com > src > styles > global.css` + `⧉` + `Open ⌄`）；右 = **文件树**（`Filter files...` 搜索框 + 可折叠目录 + 按文件类型着色的图标 + 当前文件高亮）。
- 等价于把「文件树 + 只读代码预览 + 富预览（图片/PDF/Markdown，26.410 起）」塞进右栏（截图 `10-...`）。
- 快捷键 `Ctrl+P` 直接路由到工作区文件搜索；`Ctrl+Shift+E` 单独切换文件树。

### 3.5 Side chat —— 侧边聊天

- 触发：**对话里划词选中任意内容 → 选区旁的浮动工具条 → 选 Side Chat**；或 `/side`、`/btw`；或快捷键 **`Ctrl+Alt+S`**。
- 形态：**在右侧边栏打开一个「从主会话分叉出来的」会话**，与主会话并行、互不污染；
  选中的那段文字成为它的起始上下文；它**有权把结论同步回主会话**；关掉即回到主会话。
- 官方文档的措辞值得抄进我们的设计说明：`/new` = 新任务 · `/fork` = 平行实验 · `/side` = **临时提问（Ephemeral Fork）**。
- 限制：**不能嵌套**（side chat 里不能再开 side chat）；**代码审查模式下可能不可用**。
- 26.x 补强：**从转录里划词直接「在 side chat 中提问」**、主任务运行中 side chat 与排队提示的可见性。

### 3.6 附：右栏还能装的东西（本轮不在需求内，但会撞上）

- **Summary / Sources / Artifacts**：26.406 起右栏加了 `Git summary` 与 `Sources` 段；26.415 起「计划、来源、产物、摘要」统一进任务侧栏，产物（PDF/表格/文档/PPT）可在右栏**预览**。
- 底部面板（`Ctrl+J`）与右栏是**两套**，终端可二选一落位。

---

## 4. 「展开右栏」的四条入口（复刻时必须都做出来）

1. **顶栏右上角 `◧` 按钮 → 浮动菜单**（截图 `01-...`，锚在右上角、白底圆角卡）：

   | 项 | 图标 | 快捷键 |
   |---|---|---|
   | Review | 方框内「打开」字形 | `⇧⌘G` |
   | Terminal | 方框内 `>_` | `` ⌃` `` |
   | Browser | 地球 | `⌘T` |
   | Files | 文件夹 | `⌘P` |

2. **对话里的产物/改动卡**：`Edited 22 files / Review changes ↗ / +896 -135 / [Undo] [Review]`，
   点 `Review` 或整卡即开右栏 Review；卡片获焦时是**蓝色描边**（截图 `02-...`）。
3. **快捷键**：见 §5。
4. **划词浮动工具条 → Side Chat**（§3.5）。

---

## 5. 快捷键（`Panels & Layout` / `Built-in Browser` 两段，Mac → Win）

| 动作 | Mac | Win |
|---|---|---|
| 切换左栏 | ⌘B | Ctrl+B |
| **切换底部面板** | ⌘J | Ctrl+J |
| **切换审查面板** | ⌥⌘B | Ctrl+Alt+B |
| 打开审查标签 | ⇧⌘G | Ctrl+Shift+G |
| **打开终端** | ⌃` | Ctrl+` |
| **打开浏览器标签** | ⌘T | Ctrl+T |
| 切换浏览器面板 | ⇧⌘B | Ctrl+Shift+B |
| **打开侧边聊天** | ⌥⌘S | Ctrl+Alt+S |
| 切换文件树 | ⇧⌘E | Ctrl+Shift+E |
| 搜索文件 | ⌘P | Ctrl+P |
| 浏览器地址栏 / 刷新 / 后退 / 前进 | ⌘L / ⌘R / ⌘[ / ⌘] | Ctrl+L / Ctrl+R / Ctrl+[ / Ctrl+] |

---

## 6. 交互清单（一句话版）

| 交互 | 行为 |
|---|---|
| 开 / 关 | 顶栏 `◧` 或对应快捷键；关闭后中栏**回收宽度**（不是盖住） |
| 换模块 | ① 标签栏点标签 ② 标签栏 `+` → 面板菜单 ③ 快捷键 |
| 多开 | 同一容器挂多个标签，**可拖拽重排**，标签可关闭 |
| 调宽 | 拖左缘分隔条；`⤢` 全屏；宽度**记忆**（26.406 修过「right-panel reset」） |
| 滚动 | 右栏**自己滚**，中栏位置不丢（26.406：per-conversation 滚动位置保持） |
| 折叠 | 文件块 / `N unmodified lines` / inline comment 三级可折叠 |
| 就地浮层 | 注释浮条、`⋯` 菜单、`Commit ⌄` 下拉、`Commit` 模态 |
| 注释 | 点元素 → 高亮 + 输入 → 送进 composer |

---

## 7. 待确认 / 截图没覆盖到的（需要邵先生或有 Codex 的机器补）

1. **空态**：右栏刚展开但没内容时长什么样（有没有引导页 / 空文件树）。
2. **加载态**：Review 计算中、Browser 首屏、Terminal 启动中的骨架/转圈。
3. **Review 的 `⋯` 里「split / unified」到底在哪切换** —— 截图里 `⋯` 菜单没出现该项，怀疑在 `Last turn ⌄` 的展开项里。
4. **`⤢` 全屏**是「右栏铺满中栏」还是「真·窗口全屏」。
5. **红绿口径**：Codex 是 **加绿 / 删红**（GitHub 惯例）。我们项目在做金融类视觉时用的是**红涨绿跌** —— diff 该跟哪边，**必须显式拍板**（我倾向 diff 沿用 加绿/删红，因为它是代码语义不是行情）。
6. **侧边聊天的完整视觉**：本轮只有文字描述（无截图），其标签栏长什么样、有没有独立的 composer、关掉后的回收态，都需要补一次实机。

---

## 8. 我们已有资产 vs Codex 右栏（★ 决定工作量的那张表）

现状能力来自 `mg-work/r102/part105/`（r105 ③ 预览栏，落在 `conversation.html` / `avatar.html`）：

| Codex 右栏要素 | 我们已有 | 差什么 |
|---|---|---|
| 右侧容器 + 左缘拖拽分隔 | ✅ `aside.td-browse` + `#av-browse-split`（`role=separator`） | — |
| 顶栏 44px 一条 | ✅ `.td-browse-bar`（r106 ② 已对齐 44px） | — |
| 标签栏 + `+` 新建标签 | 🟡 有**单标签「摘要」** + `新建标签` 按钮 | 多标签、激活态、关闭、拖拽重排 |
| 全屏 / 收起 | ✅ `data-r93-full` / `data-td-browse-close` | `⤢` 与「底部面板 `▭`」两颗按钮字形 |
| 面板菜单（四选一） | ❌ | 全缺（含快捷键提示） |
| 模块第二行工具条 | ❌ | 全缺 |
| Review / diff 渲染 | ❌ | 全缺（含两列行号、变更条、折叠、词级高亮、行内评论） |
| Commit 下拉 + 提交模态 | ❌ | 全缺 |
| Terminal | ❌ | 全缺（含标签名 = cwd、提示符） |
| Browser + URL 行 | 🟡 有「打开浏览器」入口（`data-td-open-browser`） | URL 行、地址、Annotating 药丸、注释浮条 |
| Files（树 + 代码） | ✅ 文件树 + 代码视图（静态） | 文件标签 + 面包屑 + `Open ⌄` |
| Side chat | ❌ | 全缺（划词浮条 + 分叉会话） |
| Sources / Summary | ❌ | 不在本轮需求 |

---

## 9. 初步结论（3 条）

1. **不要做成 5 个页面，要做成 1 个容器 + 5 个模块**。
   Codex 的右栏本质是「标签容器（骨架）+ 可插拔模块」，我们照抄这个抽象即可；
   现有 `td-browse` 骨架已经是同一形状，**扩展比重建便宜**。
2. **优先级建议**：`Review(diff)` → `Terminal` → `Browser(+注释)` → 标签多开/拖拽 → `Side chat`。
   理由：diff 是 Codex 右栏的「主叙事」且视觉密度最高（最需要设计还原）；Terminal 最便宜（几乎零样式）；
   Browser 我们已有浏览器件，只差 URL 行与注释态；Side chat 依赖「划词浮条 + 分叉会话」两套新机制，最贵。
3. **两条必须先拍板的**：
   - (a) **落在哪**：`conversation.html` 就地扩右栏，还是新开一个独立页（按仓库范式 = 由源页净底重建）？
   - (b) **代数**：r106 六条**尚未提交**。按硬规则「未提交期一律就地返工」⇒ 这批新需求会被并进 `r106`；
     若希望它单独成代，就得**先把 r106 提交**，再开 `mg-work/r107/`。**这条只有邵先生能定。**

---

## 10. 来源

| 用途 | 链接 |
|---|---|
| 实机截图（12 张，2026-09 拍摄） | https://www.worldprogramming.org/posts/the-complete-guide-to-codex-ghdafz |
| 官方 changelog（模块/标签/终端落位/注释） | https://developers.openai.com/codex/changelog · https://learn.chatgpt.com/docs/changelog |
| 右栏 = 运行结果框 / 三栏结构 | https://aicoding.csdn.net/6a9cf59348977663a5dd6579.html |
| Side chat = 右侧边栏分叉会话（划词触发） | http://7dot9.com/ |
| Side chat 语义（/new vs /fork vs /side） | https://blog.csdn.net/lb654509656/article/details/163733217 |
| 快捷键全表（Panels & Layout / Browser） | https://linuru.com/codex-app |
| 面板菜单四选一 / Files / Terminal / Browser | 同「实机截图」 |

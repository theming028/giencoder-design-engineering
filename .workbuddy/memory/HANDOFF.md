# HANDOFF · 接手卡（r109 · 第十六拍 · 2026-10-02 22:20）

> **新会话先读本文件**。每拍结束整体覆盖。细节见 `PLAYBOOK.md`（铁律 + P3.1→P3.65）/ `PAGES.md`（各页固定事实）/ `acceptance.md`（分拍实录，现到第三十六节）。

## 一、当前体位

- **现役代**：**r109**，🔴 **未交付期** —— 返工**就地**改 `mg-work/r109/ev/theme/*.py`，**不新建 r110**。
- **页面基线（定稿）**：`pages/conversation.html` md5 **`c90e66dc65313f94cfa6b1f2c570ba70`**（第十六拍后），
  其余 9 页与 `ev/bak-r109-l14/` 逐字节 **SAME**。
- **快照**：`ev/bak-r109-l16/`（含 `FINAL.md5`）；上一拍 `ev/bak-r109-l15/`。
- **回滚点**：`ev/bak-l15pre/conversation.html.before16`（第十六拍前）。

## 二、链序（★ 14 层，顺序不可乱、不可中途停）

```
make109 → splice109 → apply109          # 整页重建（净底）
  → apply-theme → apply-dark            # 主题机制 + 暗色适配
  → apply-tokens → apply-literals       # DS token 化
  → apply-popup → apply-border
  → apply-zcode → apply-menuwhite → apply-dots
  → make12 → apply12                    # 第 13 层
  → apply14                             # 第 14 层（批注模块 + 一文件一独立页签）
  → apply16                             # 第 15 层（产物卡可点开右栏）
```

> ⚠ **`apply109.py` 是「整页重建」** ⇒ 它之后的每一层都可能被它冲掉。
> **改完必须跑到尾**；整链稳定性用「连跑两轮比 md5」（判据先规范化换行）。

## 三、本条链上「谁在管什么」

| 层 | 脚本 | 职责 |
|---|---|---|
| 净底 | `make109/splice109/apply109.py` | 从 `part109/`（panel.js / panel.css / _mods.html）重建整页 |
| 主题 | `apply-theme.py` / `apply-dark.py` | `<html giencoder-theme="dark">` 开关 + 暗色档 |
| token | `apply-tokens.py` / `apply-literals.py` | 硬编码 → DS 变量；DS 13 族 × 10 级阶梯镜像 |
| 面板 | `apply-popup.py` / `apply-border.py` | 下拉面板统一 + 暗色描边降级 |
| 文本 | `apply-zcode.py` | `ZCode` → `GienCoder` |
| 下拉 | `apply-menuwhite.py` | 浅色档纯白 / 暗色档 `rgba(31,31,31,0.88)` |
| 波点 | `apply-dots.py` | settings 页去波点 |
| 12/13 | `make12.py` / `apply12.py` | 第 13 拍（`zd-host` 延后 + `.r93-card` 去缩进） |
| 14 | `apply14.py` | **第 15 拍**：批注模块恢复（12 条 EDIT）+ 右栏一文件一独立页签 |
| 16 | `apply16.py` | **第 16 拍**：产物卡 `r93-artgrid` 可点开右栏（4 处替换） |

## 四、右栏浏览器（conversation.html）★ 关键事实

- **页签 id = 二元组 `(mod, file)`**：`data-td-mod` + `data-td-file`。`openTab(mod, opts)` 收 `opts.file`；
  `activate(mod, file)` 精确点亮；`tabActivate(tab)` 读两个属性后调 `activate`。
  面板集合 = `.td-browse-body, [data-td-pane]`；`panes[i]` 的 `m` = `td-browse-body` ? `'files'` : `data-td-pane`。
- **预览面板单块** `#av-browse-pane-preview`（`data-td-pane="preview"`），内含
  `[data-td-prev-ico]` / `[data-td-prev-name]` / `[data-td-prev-meta]` / `[data-td-prev-kind="md"|"xlsx"]` /
  `[data-td-prev-save]` / `[data-td-prev-reveal]`。
- **`prevShow` 家族**（本拍抽出的可复用件）：
  `prevFill(name, meta, icoSvg, kind)` · `prevKindOf(name)` · `prevFiles{}` · `prevRemember(...)` · `prevShowFile(name)`。
- **三类「卡片即入口」全部走 `attShow(el)` 同一套**（第十六拍完成收敛）：
  | 来源 | 属性 | 图标选择器 |
  |---|---|---|
  | 用户上传附件卡 | `data-r93-att-file` | `.r93-iblk svg` |
  | 任务产物卡（`td-sum-art`） | `data-td-art`（走 `prevShow`） | `.td-sum-arti svg` |
  | **任务产物卡组（`r93-artgrid`）** | **`data-r93-artname`** | **`.r93-artic svg`**（回退 `.r93-iblk svg`） |
  - 委托锚点（document，click + keydown 各一处）：**`[data-r93-att-file],[data-r93-artname]`**。
  - ⚠ `查看所有产物 (12)` **没有** `data-r93-artname`（r101 ⑦ 就没打）⇒ 天然不会被命中，**不要给它补属性**。
- **批注模块**：`.td-elnote`（pin / card / input / hint / acts / ok / cancel）+ `.td-anchor`（`cursor:grab`）。
  点「标注」→ `is-annotating:true` 文案转「退出批注」；提交后 **`stillAnnotating:true`（锚点常驻）**；
  点已有锚点 → 编辑态 `okText="保存"` + 原文回填；Ctrl → `cardCtrl:true`。
  ★ **l3 原点对齐**：气泡左边缘 = 点击点（实测 `clickContentX:30 / noteLeftPx:30`）。

## 五、收尾固定动作（每拍必做）

1. 幂等：`applyNN.py` **连跑两遍**（第一遍 N / 第二遍 **0**），md5 不变。
2. 门禁：`python mg-work/check-syntax.py pages/*.html` → **10/10**；
   `python verify-design.py ./pages` → **74 问题 / 0 critical**。
3. `git checkout -- pages/gaps.log`（`verify-design.py` 会改它）。
4. 影响面：其余 9 页与上一拍快照 **md5 SAME**。
5. 快照：`cp pages/conversation.html ev/bak-r109-lNN/` + 写 `FINAL.md5`。
6. 记忆同步：本文件（覆盖）+ `PLAYBOOK.md`（新 P3.xx）+ `PAGES.md` + 两份 `2026-10-02.md` + `MEMORY.md`。

## 六、常踩的坑（速查，详见 PLAYBOOK）

- 🚨 **`bash -c` / `python -c` 里带中文或反引号** ⇒ 反引号内容被 shell **静默执行掉**（`exit 0` 但正文残缺）。
  **一律写脚本文件再跑**，落盘后**回读校验**。（P3.65-A）
- 🚨 生成含 `{}` 的正文**别用 `str.format`**（CSS 块 / JS `prevFiles{}` 会被当占位符）⇒ 用 **token 替换** + 残留断言。（P3.65-B）
- 🚨 探针脚本顶层 `return` 非法 ⇒ `Illegal return statement`，输出只剩 60 字节。去掉外层 `return` 即可。（P3.65-C）
- 🚨 `agent-browser` stdout **禁接管道**，一律 `>` 重定向到文件；**同时只跑一个实测进程**。
- 🚨 预览用 `file://` 直开 + `?v=<ts>` 防缓存；「改前基线」文件名**必须与原页同名**。
- 🚨 本机 `grep` 查中文返回空 ⇒ 用 Python；禁整文件 Read `pages/*.html`。
- 🚨 `autocrlf=true` ⇒ blob LF / 工作区 CRLF ⇒ `wc -c` 与 `git diff --numstat` **禁混用**。
- 🚨 推 GitHub 裸调 `git` + `-c credential.helper=store -c http.proxy=… -c http.version=HTTP/1.1`。

## 七、待裁决（未做，已量化，不擅自落地）

~150 处硬编码：类型/状态标签前景（Δ15~56）· 语法高亮（Δ9~37）· 头像色板 · 冷灰外壳 `#E5EDF5`（Δ16）· `.avatar-tooltip` 磨砂深底。

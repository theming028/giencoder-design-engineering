# r79 验收报告 · 2026-09-29

> 指令原文（4 条）：
> 1. 本轮清理要入库；2. **连版权带也排除**；3. 目录清理停在这里，都不做；4. **涟漪点阵加密到 16px**。

**改动面**：**仅 `pages/base.html` 一页**（涟漪脚本与样式只存在于该页 —— 其余 8 页 `r74-ripple` 计数 = 0）。
**补丁**：`mg-work/r79/apply79.py`（1 项，幂等）。

---

## 需求 1（编号 2）· 涟漪触发范围再排除「版权带」⇒ 欢迎态完全不触发

### 改前判定链（r78 现状）

```js
if (!t.closest('main.dot-bg')) return;                                   // 闸 1
if (t.closest('button, a, input, textarea, select, label, …')) return;   // 闸 2 交互控件
if (t.closest('.flex.flex-1.flex-col.items-center.justify-center.px-6')) return;  // 闸 3 (r78) 内容块
```

### 改后（r79 新增闸 4）

```js
if (t.closest('div[class*="pb-6"][class*="text-center"]')) return;        // 闸 4 (r79) 版权带
```

选择器与脚本 ① 段抓版权容器用的是**同一个**表达式（`main` 里 class 含 `pb-6` + `text-center` 的 div）。
源码命中数与运行时命中数**都为 1**（实测：`querySelectorAll(...).length === 1`，rect `[269,808,1162,82]`）。

### ★ 范围后果（实现前已与邵先生确认，此处存档）

真实血缘（r79 实测）：

```
MAIN.dot-bg                                             [268,48,1164,844]
  └ DIV.relative flex h-full min-w-0 flex-col overflow-hidden [269,49,1162,842]  ← children 只有 1 个
      ├ 内容块  DIV.flex flex-1 flex-col items-center justify-center px-6  [269,49,1162,759]
      └ 版权带  DIV.pb-6 text-center text-xs leading-relaxed              [269,808,1162,82]
```

**闸 3 + 闸 4 把 main 内两块全覆盖 ⇒ 本页不再有任何区域能起涟漪，涟漪特效在 base.html 实际已停用。**
脚本与样式**保留不删**（死代码清理另行拍板），便于随时回退。

> ⚠️ 注意 `main.dot-bg.children.length === 1` —— r78 笔记里"main 只有 2 块"指的是**外壳的子元素**。
> 按 `host.children` 去匹配版权带会全 false。已沉淀为 PLAYBOOK P3.11 ①。

### 实测证据（A/B · 均用 `document.elementFromPoint` 复刻真实 target 后再 dispatch）

**① 逐点枚举（9 点 · 1440×900 · `mg-work/r79/ev/rip79.js` `__MODE='enum'`）**

| 点 | 区域 | BEFORE（`before/base.html`） | AFTER（`pages/base.html`） |
|---|---|---|---|
| `715,120` 上空白 | 内容块 | 0 | **0** |
| `715,285` LOGO | 内容块 | 0 | **0** |
| `715,327` 问候语 | 内容块 | 0 | **0** |
| `300,400` 左空白 | 内容块 | 0 | **0** |
| `715,465` 输入卡 | 内容块 | 0 | **0** |
| `715,570` 技能胶囊行 | 内容块 | 0 | **0** |
| **`715,845`** | **版权带** | **1** ← 现状 | **0** ← 已排除 |
| **`300,845`** | **版权带** | **1** | **0** |
| **`275,840`** | **版权带** | **1** | **0** |

BEFORE `fired=3` → AFTER **`fired=0`**。

**② 全视口网格扫描（步长 120 → 96 点 · `__MODE='grid'`）**

- 命中分布：`main/内容块 54` + `main/版权带 9` + `main 之外 33`
- **起涟漪 0 个；最大涟漪节点数 0** ⇒ 「本页无任何区域可触发」成立

**③ 视觉与量化（`ev/cmp.png` 三栏：BEFORE / AFTER / 差分×14）**

- 同点 `715,845`、同刻 `t=160ms`：
  - BEFORE：`hit=P.`，涟漪节点存在，`opacity 0.983`、`bgSize 16px 16px`、点色 `rgba(43,43,43,0.14) 1.7px`
  - AFTER：**`{"err":"NO RIPPLE"}`**
- 版权带裁区（`260,780`–`1440,900`）总绝对差 **83 769**（平均每像素 **0.2212**）
- **差分包围盒（裁区内）`(191,11,748,111)`** → 绝对坐标 x `451..1008`、y `791..891`，
  以点击点 x=715 为中心、落在版权带 y 808–890 内 ⇒ **差异就是涟漪环带，不是页面噪声**
  （页面自带时间噪声在 aside `x236–249`，裁区从 x=260 起，**已排除**）

---

## 需求 2（编号 4）· 涟漪点阵确认为 16px —— **无需改动**

| 项 | 实测值 | 与底色关系 |
|---|---|---|
| `.r74-ripple` `background-size` | **`16px 16px`** | **= `.dot-bg` 的 `16px 16px`** ✓ 逐点对齐 |
| `.dot-bg` 底色点 | `rgba(107,107,107,0.1)` · `1.5px` | — |
| `.r74-ripple` 涟漪点 | `rgba(43,43,43,0.14)` · `1.7px` | r78 由 0.28 减半 |
| `--r76-rip-cap` / 时长 / z-index | `480px` / `300ms` / `0` | 未动 |

r76 把底色从 20px 加密到 16px 时，涟漪点数随之 ×1.56（两层必须同 `background-size` 才能对齐）。
邵先生本轮确认 **16px 是有意的**，代码不动。
> 附带事实：本项在需求 1 落地后已属"休眠参数"——涟漪不再触发，但值仍按要求保持 16px。

---

## 门禁与回归

- **`verify-design.py ./pages` → 75 个问题（66🟡 / 9🔵 / 0🔴，0 critical）**
- 与 r78 的 `gate-after.txt` **逐条 diff（剥目录前缀 + 行号）**：**新增 0 条、消失 0 条**（集合 102 = 102）
- `base.html` 的 `🔵 CRAFT-SLOP` 渐变计数 **62 = 62**（本次只改 `<script>` 正文，**未新增渐变**）
- **标签级断言**（改脚本正文的口径 = 计数不变）：
  `<script` **8 → 8** · `</script>` **7 → 7** · `<style` **11 → 11** · `</style>` **11 → 11**
- `pages/gaps.log` 已 `git checkout --` 还原；`mg-work/r79/before/` 内无 `gaps.log`
- **幂等**：`apply79.py` 连跑 3 次 → `应用 1 / 0 / 0`，第 2、3 次均为 `应用: 0 项 | 跳过: 1 项`
- 基线 md5 `6f509d2dd4ec65c530cc3ecd379636ed` → 改后 `c4cb03c4cd75be3ef0d484a59d75f328`

---

## 未做 / 按指令停下的

- **需求 3（编号 3）· 目录清理停在这里**：档 2（早期整页截图 61.94 MB）/ 档 3（全部零引用截图 87.52 MB）/
  档 4（档3 + `before` ≈104 MB）/ 档 5（重写历史 + `force push`）**全部不执行**。
  `git gc` 已在本轮之前跑完且**已无空间可压**（对象库完全打包收敛）。
- **死代码清理**：`r74-ripple` 脚本与样式现已无触发路径，是否删除**另行拍板**（本报告不做）。
- 其余遗留（r77 滚动条 hover 无反馈、`.td-browse` 色值、r74 摇晃/X 自转 300ms、r72 Esc 层级、
  avatar 窄视口）**均未动**，见 `HANDOFF.md` 第四节。

---

*探针：`mg-work/r79/ev/rip79.js`（struct / enum / grid / size 四模式）*
*证据：`ev/cmp.png`（三栏对照）· `ev/before-click-160.png` · `ev/after-click-160.png` · `ev/base-full-1440x900.png` · `ev/gate-after.txt`*
*基线：`mg-work/r79/before/base.html`（与改前页面逐字节相同）*

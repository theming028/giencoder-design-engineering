# HANDOFF · 会话交接卡

> **滚动更新**：每轮收尾时**覆盖重写**（不是 append）。
> **用途**：新会话开局只读这一个文件，就能对齐「现在在哪、下一步做什么」。
> 分工：历史详情 → `YYYY-MM-DD.md`；稳定工作法 → `PLAYBOOK.md`；页面事实 → `PAGES.md`；
> 每次都必知 → `MEMORY.md`。**本文件不占注入预算**（只在需要时 grep/Read）。

- **最后更新**：2026-09-29（r71 收尾）
- **基线 HEAD**：`8ee17f6` = r66 全量入库。**r67 / r68 / r69 / r70 / r71 五轮产出全部未提交、未推送**
- **未提交清单**：9 页 `pages/*.html`（其中 base / avatar / task-detail 是 r71 主力）+ 记忆三件套

---

## 一、r67–r71 五轮做了什么

| 轮 | 主题 | 落点 |
|---|---|---|
| r67 | 看板卡片标题去文字流光；基础工作台 main 容器 → **鼠标跟随动态波点背景** | base / kanban |
| r68 | 详情页右栏 AI 对话框**全要素移植**到数字分身右栏 | avatar |
| r69 | 数字分身右栏标题改名 + 预览栏 `.td-browse-slot` **全要素跨页移植** | avatar |
| r70 | 数字分身 AI 对话框 / 预览栏四项调整 + 全站按钮 ring 清理 | 多页 |
| r71 | ① base「新会话」→ 液态玻璃 ② 详情页预览栏动效与 avatar 对齐 ③ 全局弹层圆角统一 8px ④ avatar 双开 main 响应式 + 预览栏让位 | base / avatar / task-detail + 6 页共享 CSS |

## 二、r71 四项已验收（结论存档）

1. **液态玻璃**：`base.html` 尾部 `<style id="r71-glass-css">`。`backdrop-filter: blur(18px) saturate(180%) brightness(1.04)`，基底「上厚下薄」白渐变 + 顶部镜面棱 + `::before` 棱边色散 + `::after` hover 扫光（760ms，由 `--nc-glass-dur` 承载）。**按钮几何 244×32 未变**。
2. **预览栏动效**：`task-detail` 与 `avatar` **完全一致** —— 展开/收起都是 **200ms + `cubic-bezier(.22,1,.36,1)`**，`flex-basis` 在 `0 ↔ calc(100% - var(--td-browse-right-w,480px))` 过渡；收起靠 `:has(> .td-browse.is-closing)` 把 basis 打回 0（不依赖 JS 摘类）。
3. **弹层圆角 8px**：4 处例外全部归位（权限弹层 12→8 / 更多操作 5→8 / 技能浮窗 12→8 / 数字分身浮窗 6→8）+ **补漏 `.skills-popup-bg`**（9 页共享 CSS，760×320，与 `.td-skill-pop` 同一面板）。
4. **main 响应式**：1440 双开 → `main 371 / .av-main 310`、卡片转**单列**；1920 → `.av-main 710`、容器查询**正确关闭**回 2×2。预览栏让位：`1440→561 / 1920→641 自动回弹 / 2560→641`，无横向溢出。
   - 三档容器查询 **560 / 420 / 300**，**必须排在 `<style>` 块末尾**（基础规则之后，否则被同特异性压掉）。

**校验**：`verify-design.py ./pages` = **75 项 / 0 critical**，与「本轮改前」基线逐条 diff = **−1（零新增）**；`gaps.log` 已还原；9 页冒烟全过。

## 三、待用户拍板（2 项 · 都是产品决定，我没擅自改）

1. **详情页浏览态按真实 Esc 会跳 `kanban.html`**。
   根因：第 26 轮「Esc 返回任务看板」的监听在**页面初始化就注册（冒泡段）**，而浏览栏自己的 Esc 监听是**懒注册**（首次开侧栏才注册）→ 顺序更晚，`setOpen(false)` 永远跑不到。改法同页已有两处先例（`@685800` / `@691824`：捕获段 + `stopPropagation`）。
   ⚠️ 属行为变更（Esc 到底「关预览栏」还是「返回看板」），**等用户定**。
2. **avatar 双开 + 视口 ≤1100 时 main 被压到 ~0**（预览栏 561 是硬下限）。可考虑让 AI 会话栏（480）也参与让位 —— 同样是产品决定。

## 四、下一轮（r72）接手清单

- 接到新需求先按 `MEMORY.md` 的「三条硬规则」走：**改前先问范围** → 走 `mg-work/r72/apply72.py` 幂等脚本 → 跑完复跑验证。
- 若用户要先落地 r67–r71：**只 commit 不 push**（默认约定），完事汇报改动清单。
- 收尾时**更新本文件**（覆盖）+ 追加当日 `YYYY-MM-DD.md`。

## 五、回滚与取证材料

- **改前基线（仓库内，安全）**：`mg-work/r71/before/{base,avatar,task-detail}.html`（**必须同名**，否则 `file://` 下落回 base 壳）
- **补丁链**：`mg-work/r71/apply71{,b,c,d,e,f}.py`（6 个，全部幂等，复跑均为 `应用 0 项`）
- **证据图**：`mg-work/r71/ev/`（含 `60-compare-responsive-1440.png` 改前改后对照、`14-glass-zoom.png` 玻璃定稿）
- ⚠️ `/tmp/r71*-backup/` 是**临时目录，重启即丢** —— 只用于改前回滚，实际回滚请用上面 `mg-work/r71/before/`

## 六、环境速记（新会话最容易踩）

- 预览**一律 `file://` 直开**，别用内置预览面板（URL 不带 hash → 渲染出错误的壳）
- `python3 verify-design.py` 用 `/Users/shaoyuming/.workbuddy/binaries/python/envs/default/bin/python`（系统 python3 无 PIL）
- `agent-browser` 的 `eval` **变量不跨调用保留** → 采样 + 回读必须写在**同一条** Bash 命令里
- `Escape` 必须用 `agent-browser press Escape`（**真实按键**）；合成的 `KeyboardEvent` 不带 `isTrusted`，结论可能是错的

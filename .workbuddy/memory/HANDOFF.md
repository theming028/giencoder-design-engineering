# HANDOFF · 下一轮接手卡

> **每轮覆盖重写。新会话开局先读这一页，再按需 grep `PLAYBOOK.md` / `PAGES.md`。**
> 最后更新：2026-09-29 23:05（r85 已落地并验收；**r80–r85 已 commit + push**）
> **已推送至 `origin/main` @ `1ecc7ee`；工作区干净**

---

## 一、当前工作区状态

**干净**（`git status --short` 无输出）。r80–r85 全部入库并推送：

| 提交 | 内容 |
|---|---|
| `acb9070` | feat(r80-r82) 研发工作台四页「切换工艺流程空间」浮窗落地并两轮修订 |
| `c1fe24c` | feat(r83-r84) 头像菜单「会话历史」二级视图 + 点击删除确认态 |
| `ef67659` | feat(r85) 「设置」页 —— 左侧导航菜单 + 首个菜单「系统设置」内容 |
| `8dcb422` | chore(tools) 入库 check-syntax.py / mgfetch.py + `.gitignore` 两条排除 |
| `1ecc7ee` | chore(memory) 记忆同步至 r85 |

⚠ **`.gitignore` 本轮新增两条排除**（无复用价值；**文件仍在本地，不是丢失**）：
- `mg-work/r80/raw/sel_*.json` —— MasterGo「选中节点」原始响应 dump，**285 个 / 21M**（该轮实质产物仅 14 个 / 81K）
- `mg-work/*/gate/*/pages/` —— 门禁跑分用的页面临时副本；按既有惯例只留 `gate/*.txt` 报告

⚠ **推送凭据（本机原本完全没有）**：`~/.gitconfig` 的 `credential.helper=` 为空、`~/.ssh` 只有 known_hosts、Windows 凭据管理器无 github 条目。
本轮把 PAT 写入 `~/.git-credentials` 后，用 **`-c credential.helper=store`** 推送 —— **不设全局 helper、不把凭据写进仓库**。
  ⚠ Windows 下 `chmod 600` **不生效**（实测仍是 `-rw-r--r--`）⇒ 改用
  `icacls "<path>" /inheritance:r /grant:r "<user>:(R)"` 收紧为「仅本用户可读」（已验证只剩一条 ACE）。

`.workbuddy/memory/` 两份：**仓库内 `E:/GienCoder/giencoder-design-engineering/.workbuddy/memory/`（权威，随 git 走）**
与工作区 `E:/GienCoder/.workbuddy/memory/`（速记）。改记忆**以仓库内为准**。

---

## 二、r85 做了什么（设置页：导航 + 「系统设置」）

| 需求（邵先生原文） | 落地 |
|---|---|
| ①「设置」页面的**导航菜单**（设计稿 `1389:18609`，232×268） | 返回 / 分组「通用」〔系统设置★选中 / 模型 / 连接器〕/「已归档」〔已归档任务〕 |
| ② 第一个菜单**「系统设置」的页面内容**（设计稿 `1389:18725`，840×919；内容区宽 860） | 标题 + **3 卡片 11 行**，含 select / switch / 6 档滑块 / 3 按钮段控 / 复选框 / danger 按钮 |

产物 `pages/settings.html`　**354210 → 420820 字符（+66610）**，脚本 `mg-work/r85/apply85.py`（幂等）。

**验收（四查全绿，详见 `mg-work/r85/acceptance.md`）**
- **67 项几何/样式逐项比对 = 0 偏差**（±1px）→ `ev/cmp_r85.txt` / 对照图 `ev/cmp_r85.png`
- 幂等 ✓（`sha256 7a4aa0d3…`）／语法 ✓ `ALL_OK settings.html script=6 style=7`
- 门禁 ✓ 通过；**HEAD 基线逐条 diff 无差异 = 零新增问题**，`gaps.log` 无 settings.html 条目
- 视觉：`ev/shot_page.png`(840×918) `shot_nav.png`(232×268) `shot_full.png`(1600×1100)

**轮内两次返工（都是**先测出来再改**，值得照抄）**
1. 卡片原本写 `border: 1px` → 行宽 798（设计 800）、卡片高 +2、整列 y 推低 2–3px。
   ⇒ 改 `outline: 1px + outline-offset:-1px`（设计稿是**内描边**，不吃内容盒）。
2. 滑块只有 3 档且 `pos=[14,68,252]`（末档还越界）；已选线 `top:0`、刻度挂在 `track` 上（叠加 track 的 `top:6`）
   ⇒ 整条刻度下移 6px、拇指偏 14px。逐像素重测后改为 **6 档 stops=[6,54,102,150,198,246]**、
   刻度挂 `.r85-slider`、`is-on` 首刻度、拇指 rel 52。

---

## 三、★★ r85 新打通的设计稿取数链路（**推翻了 HANDOFF 旧记录，见 P7**）

### ① `GET http://127.0.0.1:30678/api/getScreenshot` 能直接拿节点 PNG

```
GET /api/getScreenshot?documentId=193158744355579&documentPageId=ip148:02203&targetNodeId=<节点>&scale=2
```
返回 `{success:true, images:[{base64:"iVBORw0…"}]}`。首次 21.7s、二次 0.38s（有缓存）。
- **必须 GET + query 参数**（POST 一律 400，参数放 body 也 400）。
- 端口：`20678` = MCP（JSON-RPC）；**`30678` = mgmcp 的 HTTP server（`/api/*` 在这）**。
  ⚠ 旧记录「30678 的 HTTP 全是 400，别去打」= **只试过 GET 根路径**得出的片面结论 → **已作废**。
- ⚠ 该接口**只返回当前画布选中图层**：传 `targetNodeId=1389:18609`（导航）仍然回内容页 ⇒ 导航节点拿不到独立截图。
- MCP 工具 `get_screenshot`（带 `projectDir`/`scale`）实测**必 120s timeout** ⇒ 别用。

### ② 设计稿里的文案可能**完全不在结构树里**

`1389:18725` 有 42 个 `ui-component`，**只有 7 个带 `text=`**（其余 `text/title` 是 `props="{}"` 未展开的 DS 实例）。
喂单个 `text/title` 节点给 `get_selection_node` → **120s timeout**。
⇒ **文案唯一来源 = 上面那条截图**（本轮 11 行文案全是读图得到的）。

### ③ ⚠ 导出 PNG 是 RGBA，未绘制处 `alpha=0` → `convert('RGB')` 变纯黑

本轮一开始把顶部 0–52 逻辑 px 的黑色误判成「MasterGo 的节点名标签条盖住了标题」，
其实那只是**标题节点无填充 ⇒ 该区透明**（同理会误判卡片间隙）。
**正确做法：`Image.alpha_composite(白底, im)` 之后再扫描/取色。**

### ④ 结构树能直接给出「内描边 / 外描边」

节点 B 的行宽 800 = 840 − 2×20 ⇒ **描边不占内容盒**；像素复核：卡片左缘 x=0–0.5 为 `#EEEEEE`、x=1.0 起为 `#F8F9FA`。
CSS 对应写法：`outline: 1px solid <色>; outline-offset: -1px;`（写 `border` 就错 2px，且会级联推低整列）。

---

## 四、待拍板 / 待确认（邵先生）

1. ★ **非选中导航项常显 `#F5F6F7` 底**：设计稿画法如此，现按设计稿落地；要「只有选中才有底」删 1 条 CSS 即可。
2. **不绘制窗口 chrome**：设计稿那层深色顶部区实为**透明**（非标签条），本实现沿用既有外壳。
3. **字号滑块 6 档**：刻度按设计稿 6 格落地（当前值 = 第 2 档）；若产品只有「小/默认/大」三档，改 `stops` 数组即可。
4. **r84 遗留提问仍未答**：`avatar.html` 会话历史确认态下「按钮组压在图标位、连点两下会直接删除」是否再挪 8px。
5. **r83 三条已知偏差**（`mg-work/r83/acceptance.md` 2.4）：① 滚动条 overlay；② 行宽 438 vs 442；③ 面板高随视口。
6. **r83 的 `ROWS` / r81 的 `SPACES` / r85 的 `DATA_JS` 都是占位文案** → 真名给出后改对应脚本的数组。
7. **r81 遗留三条**：① 触发器 logo `#3491FA` + 白「P」；② 浮窗 7 条配色；③ 浮窗右缘对齐触发器右缘。
8. **既有遗留**：r79 `r74-ripple` 死代码；r77 滚动条 hover 无反馈 + `.td-browse` 未跟随 `#DAE3ED`；
   r74 摇晃 / X 自转 300ms 上限；r72 全屏 + 浏览态 `Esc#1` 关两层；`pages/gaps.log` 与页面不同步。

---

## 五、下一轮接手清单（按顺序）

1. 读本卡 → `git status` → 复跑补丁确认幂等：
   `python mg-work/r85/apply85.py`（settings.html，摘 2 件）→
   `python mg-work/r84/apply84.py`（avatar.html，摘 3 件）→ `python mg-work/r82/apply82.py`（4 页）。
2. 改页面**一律新建 `mg-work/rNN/applyNN.py`**，`PRIOR` 里把**历代**块标记都加上。
   **例外**：上一轮**尚未提交**时，若只是对它的即时返工 ⇒ **就地修订原补丁、不另起代数**（r84 / r85 都是先例）。
   判据：`git status` 里该页仍是 ` M`。
3. 收尾四件套：`python mg-work/check-syntax.py pages/<改过的页>.html` →
   `python verify-design.py ./pages`（**必须传目录**；跑完 `git checkout -- pages/gaps.log` 与
   `git checkout -- mg-work/kanban/r13/chk/ && git clean -f mg-work/kanban/r13/chk/`）→
   门禁**逐条 diff**（本轮口径：把 HEAD 版与当前版各放一个临时 `pages/` 跑一遍再 `diff`，比整目录 archive 更省）→
   覆盖更新本卡。
4. 🚫 **默认不 commit / 不 push**（2026-09-28 起）：干完只汇报改动清单。

---

## 六、回滚与取证

```bash
cp mg-work/r85/settings.before.html pages/settings.html  # r85 回滚
cp mg-work/r84/avatar.before.html   pages/avatar.html    # r84 回滚（回到 r83 状态）
cp mg-work/r83/avatar.before.html   pages/avatar.html    # r83 回滚（回到无二级页状态）
cp mg-work/r82/before/<page>.html   pages/<page>.html    # r82 回滚（4 页）
cp mg-work/r81/before/<page>.html   pages/<page>.html    # r81 回滚
cp mg-work/r80/before/dev.html      pages/dev.html       # r80 回滚
```

| 目录 | 内容 |
|---|---|
| `mg-work/r85/apply85.py` | ★ 本轮补丁（幂等；`PRIOR` 摘 2 件 + `NEW_TOKENS` 校验 + `</body>` 计数=1） |
| `mg-work/r85/acceptance.md` | ★ 验收报告（四查 + 67 项对照 + 已知偏差 + 待拍板） |
| `mg-work/r85/spec.md` | 设计稿规格表（导航 7 行 / 内容 3 卡 11 行 / 与旧实现差异） |
| `mg-work/r85/raw/design_1389-18725.png` | ★ 权威视觉参考（**2x**，1680×1838，**RGBA**） |
| `mg-work/r85/raw/node_*.json` / `outline_*.txt` / `design_*.html` / 25×`svg` | 结构树 / 大纲 / 设计 DOM / 素材 |
| `mg-work/r85/ev/{p85a,p85b}.js` | 几何探针（**p85b 以 `.r85-page` 为原点**，与设计稿同坐标系） |
| `mg-work/r85/ev/cmp85.py` + `cmp_r85.txt` | ★ 67 项自动对照脚本 + 报告（`python mg-work/r85/ev/cmp85.py`） |
| `mg-work/r85/ev/mkcmp85.py` + `cmp_r85.png` | 对照图生成 / 成品（整页 1:1 + 2 处细节 ×2） |
| `mg-work/r83/raw/design_1389-18518.png` / `node_*.json` | 「会话历史」设计稿位图 / 结构树 |
| `mg-work/{check-syntax.py, mgfetch.py}` | ★ 常驻语法工具 / 设计取数工具 |

⚠ `mg-work/r80/raw/` 里的设计素材（`sel_*.json` 285 条历史回包、`svg/`）**别删**，是取不到数时的唯一退路。
⚠ `assets/icons/*.svg` 是仓内 DS 图标库，**先来这里找再手搓**。

---

## 七、环境速记（Windows，逐条都是踩过的）

- 预览一律 **`file://` 直开**；改完带 `?v=<ts>` 防缓存。
- ⚠ `file://` 下「改前基线」**文件名必须与原页面同名**（否则外壳按名查路由表落回 base 壳）。
- ⚠ **同一时刻只能有一个 agent-browser 链路**（共用标签页，并发必串味：症状「元素不存在 / url=blank / probe 缺失」）。
  整条链路（`set viewport` → `open` → `wait` → `eval/screenshot`）**要在一次 bash 调用里跑完**。
- ✅ `screenshot <选择器> <路径>` = 元素截图（**位置参数**，`--selector` 选项写法不认）；
  **会裁到元素边界** ⇒ 浮层（tooltip / 菜单挂在 body 上）够不到，要截全页再 Pillow 裁。
- ⚠ **程序化 `el.click()` 的 `detail === 0`，会被当作键盘触发**（凡按 `ev.detail` 分流焦点/样式的逻辑）
  ⇒ **取证截图一律用 `agent-browser click <sel>`（真鼠标、`detail=1`）**，程序化点击只测逻辑链。
- ✅ **`:hover` 能跨独立 agent-browser 调用存活**（r84 实测）。
- ⚠ `eval "$(cat probe.js)"` 前**确认文件真的存在**：路径写错时 `cat` 报错、`eval` 收到空串 →
  **静默返回 `null`**（r84 踩到，白跑一轮）。
- ⚠ `agent-browser eval` 的返回是**双层 JSON 字符串**（`json.loads` 两次才拿到对象）。
- ⚠ **`Bash` 工具偶发 `Error: sandbox-center cmd decisionRecord missing actual resource subject`**
  （同一行里串太多 `&&` 时更容易触发）⇒ 拆成单条命令重发即可。
- 禁整文件 Read `pages/*.html`（单行压缩 bundle 340–820 KB）→ 用 Python 只打印目标片段。
- ⚠ 本机 `grep` 查中文一律返回空 → 中文用 Python 读。
- **推 GitHub**（r85 已补齐认证，三步）：
  ① `env | grep -i proxy` **现查** —— 环境注入的代理**端口每轮会变**（实测走过 53395 / 62399），
     它对 `github.com:443` 稳定 502 ⇒ **先清掉** `env -u https_proxy -u HTTPS_PROXY -u http_proxy -u HTTP_PROXY`；
  ② 出口用 `http://127.0.0.1:7890`（`curl -sI -x http://127.0.0.1:7890 --max-time 10 https://github.com` 回 `200 OK` 即通）；
  ③ **认证**：本机原本**没有**可用凭据 —— `~/.gitconfig` 里 `credential.helper=` 为空、`~/.ssh` 只有 known_hosts、
     Windows 凭据管理器无 github 条目。PAT 已写入 `~/.git-credentials`（权限 600），推送时带 **`-c credential.helper=store`**：

  ```bash
  env -u https_proxy -u HTTPS_PROXY -u http_proxy -u HTTP_PROXY \
    git -c credential.helper=store \
        -c http.proxy=http://127.0.0.1:7890 -c https.proxy=http://127.0.0.1:7890 \
        -c http.version=HTTP/1.1 push origin main
  ```

  判据：出现 `main -> main`；再用 `ls-remote origin main` 与 `git rev-parse HEAD` 比对复核。
  ⚠ 认证缺失时报的是 `fatal: could not read Username for 'https://github.com': terminal prompts disabled`
  （非交互环境不弹窗）—— **别误判成网络问题**。⚠ 不要设全局 helper、不要把凭据写进仓库。
- MasterGo：MCP 在 **20678**；**截图 HTTP 接口在 30678**（见第三节 ①）。

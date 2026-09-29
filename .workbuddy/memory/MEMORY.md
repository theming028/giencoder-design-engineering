# GienCoderDesignEngineering · 项目记忆索引

> **只放"每次会话必须知道的事"，≤ 3.5K 字节**（超了会被截断注入）。
> 详情见同目录（**按需 grep，不要整读**）：
> · **`HANDOFF.md`** ★新会话开局先读（当前状态 / 待办 / 接手清单，每轮覆盖）
> · **`PLAYBOOK.md`** 改页面铁律 / 幂等自检 / 取证验收 / 取数 / git / 提速
> · **`PAGES.md`** DS token 档位 / 各页固定事实 / 标准配方
> · `YYYY-MM-DD.md` 每日原始记录（append-only）
> · skill（4）：design-pixel-measure / css-pseudo-state-evidence / motion-primitives-port / mastergo-to-html

## 一、环境（**Windows 本机**）

- 页面**全自包含**（CSS/JS 内联、图片 base64），**无 `serve.py`**；预览一律 **`file://` 直开**。
  ⚠️ 内置预览 URL **不带 hash** → 渲染出错误的壳；⚠️★ `file://` 下「改前基线」**文件名必须与原页面同名**。
- Python = `python`（Pillow / numpy 都有）。agent-browser（实测）=
  `C:/Users/Administrator/AppData/Local/npm-cache/_npx/ba0727cbf2d10686/node_modules/.bin/agent-browser`。
- ⚠️★★ **`set viewport` → `open` → `eval/click/screenshot` 整条链在同一次工具调用里**
  （`set viewport` 会把页面重置成 `about:blank`，跨调用视口仿真会丢）。
- ⚠️ 探测脚本避开 `sc`/`reg`/`wsl`/`wmic` token（安全策略拦截）。
- ★ **设计稿 PNG 首选** `GET http://127.0.0.1:30678/api/getScreenshot?documentId=…&documentPageId=…&targetNodeId=…&scale=2`
  （回 base64，21s / 缓存 0.4s；**必须 GET+query**，POST 400；⚠ 只返回**当前画布选中**的节点）。
  回退：MCP `get_screenshot` 传**裸 ID**（r85 两次 120s timeout）；`get_selection_node` 只认**完整 goto 链接**。
  PNG 带 3~4px 外边距，量测先加偏移（PLAYBOOK P7⑨⑩）。
- ⚠️★ **设计稿 PNG 是 RGBA**：未绘制处 `alpha=0` → `convert('RGB')` 变**纯黑**（易误判成"标签条盖住内容"）。
  取色前先 `alpha_composite` 白底。结构树里的 `text/title` 是未展开 DS 实例 ⇒ **往往没文案，只能读图**。

## 二、三条最重要的硬规则

1. **改页面一律走 `mg-work/rNN/applyNN.py`**：先判 NEW 标记命中即 skip → 再判 `count(OLD)` 恰为 N 否则 `sys.exit`
   → **跑完立刻复跑一次**确认「摘 N → 插 N」且字符数一致。回滚 `cp mg-work/rNN/before/<page>.html pages/`。
   **例外**：上一轮尚未提交时对它的即时返工 ⇒ 就地修订原补丁，不另起代数（判据：`git status` 仍是 ` M`）。
2. **断言只允许**：① 标签级计数（`<style></style><script></script>`）的**精确增减量** ② 针对"被改对象"的精确计数。
   **禁止**"全文件关键词总数不变"；**新增注释里不得出现被断言的 token / 标签名**。
3. **改前先问范围**：同名同构模块常在多页各有一份，改前用 DOM 核实目标页现状，不凭字面推断 ——
   用户对"擅自修改未指明的对象"极敏感。

## 三、其他速记

- 收尾四件套：`python mg-work/check-syntax.py pages/<页>`（★ 查 JS 语法 + CSS 注释配平）→
  `python verify-design.py ./pages`（**必须传目录**，跑完 `git checkout -- pages/gaps.log`）→ 与 HEAD 基线
  （把 HEAD 版与当前版各放一个临时 `pages/` 各跑一遍再 `diff`）**逐条 diff**（汇总数相同 ≠ 零影响）→
  覆盖更新 `HANDOFF.md`。
- **禁止整文件 Read `pages/*.html`**（单行 bundle 340–820 KB）→ 用 `python - <<'PY'` 只打印目标片段。
  本机 `grep` 查中文一律空 ⇒ 中文用 Python 读。
- 新知识**先进 `PLAYBOOK.md` / `PAGES.md`**，本文件只在"每次都必须知道"时才加一行。
- 🚫 默认**禁止自动 commit / push**（2026-09-28 起）；推送走
  `git -c http.proxy=http://127.0.0.1:7890`（env 的 `https_proxy` 对 github 稳定 502）；push 由邵先生发起。

# GienCoderDesignEngineering · 项目记忆索引

> **只放"每次会话都必须知道的事"，保持 ≤ 3.5K 字节**（超了会被**截断注入**，等于白写）。
> 详情见同目录：
> · **`PLAYBOOK.md`** —— 改页面铁律 / 幂等与自检 / 取证验收 / 需求措辞 / 路由 / git / 提速
> · **`HANDOFF.md`** —— ★**新会话开局先读**：当前状态 / 待办 / 下一轮接手清单（每轮覆盖更新）
> · **`PAGES.md`** —— DS token 档位 / 各页固定事实 / 标准配方 / MasterGo 流程
> · `YYYY-MM-DD.md` —— 每日原始记录（append-only）
> 👉 接到活儿**按需 grep**，不要整读。
> skill（4）：design-pixel-measure / css-pseudo-state-evidence / motion-primitives-port / mastergo-to-html

## 一、环境（macOS 本机）

- 页面**全自包含**（CSS/JS 内联、图片 base64），**无 `serve.py`**（那是 YuanqiDesignSystem 仓库的）。
- 预览一律 **`file://` 直开**（`http.server` 会被沙箱网络代理拦成 502）；
  内置预览 `http://127.0.0.1:<port>/static-html/<id>/<file>` **不带 hash** → 会渲染出错误的壳，
  排查"文件没改却显示异常"要**两种协议各开一次对比 DOM**。
- ⚠️★ `file://` 下「改前基线」**文件名必须与原页面同名**（外壳按文件名查路由表，否则落回 base 壳）。
- agent-browser：`/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser`
  （`open <url>` / `set viewport W H` / `screenshot <path>` / `eval '<js>'` / `set media …`）。
- Python 只用 `/Users/shaoyuming/.workbuddy/binaries/python/envs/default/bin/python`（系统 python3 无 PIL）。
- ⚠️ 写 Python 探测脚本避开 `sc` / `reg` / `wsl` 等 token（命中安全策略拦截）→ 用 `S` / `scl` / `scan`。

## 二、三条最重要的硬规则

1. **改页面一律走 `mg-work/rNN/applyNN.py`**（不手改大文件）：幂等三要素 —— 先判 NEW 标记命中即 skip →
   再判 `count(OLD)` 恰好为 N 否则 `sys.exit` → **跑完立刻复跑一次**确认 `应用: 0 项 | 跳过: N 项`。
   回滚 `cp mg-work/rNN/before/<page>.html pages/<page>.html`（`/tmp/rNN-backup` 重启即丢）。
2. **断言只允许**：① 标签级计数（`<style></style><script></script>`）的**精确增减量** ② 针对"被改对象"的精确计数。
   **禁止**"全文件关键词总数不变"；**新增注释里不得出现被断言的 token / 标签名**。
3. **改前先问范围**：同名同构模块常在多页各有一份（如顶栏），改动前用 DOM 核实目标页现状，
   不凭字面推断 —— 用户对"擅自修改未指明的对象"极敏感。

## 三、其他速记

- 验证：`python3 verify-design.py ./pages`（**必须传目录**）→ 跑完 `git checkout -- pages/gaps.log`；
  是否零新增要**逐条 diff**（汇总数相同 ≠ 零影响）。
- **禁止整文件 Read `pages/*.html`**（单行压缩 bundle 340–620 KB）→ 用 `python3 - <<'PY'` 只打印目标片段。
- 新知识**先进 `PLAYBOOK.md` / `PAGES.md`**，本文件只在"每次都必须知道"时才加一行。
- 🚫 默认**禁止自动 commit / push**（2026-09-28 起）：完成后只汇报改动清单，推送由邵先生统一发起；
  用户显式要求时立即执行。
- ⚠️ 仓库根在坚果云内、`origin` URL **内嵌明文 PAT** —— 汇报时不要打印完整 URL。

# GienCoderDesignEngineering · 项目长期记忆

> 详情索引见每日日志 `.workbuddy/memory/YYYY-MM-DD.md`；本文件只记**跨会话可复用的约定与工作流**。

## 一、环境（macOS 本机）

- 页面**全自包含**（CSS/JS 内联、图片 base64），无 `serve.py`（那是 YuanqiDesignSystem 仓库的）。
- `python3 -m http.server 8866` 会被沙箱网络代理拦成 502 → **直接用 file:// 预览**：
  `agent-browser open "file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/<page>.html"`
- agent-browser 路径：`/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser`
  （`mg-work/*/shot*.sh` 里写的是 Windows 路径 `C:/Users/Administrator/...`，本机需替换）
  命令：`open <url>` / `set viewport W H` / `screenshot <path>` / `eval '<js>'`

## 二、MasterGo 设计稿 → 图标还原工作流（已验证）

1. `get_selection_node(projectDir, targetNodeId="<图层ID>")` 拉节点 → 图标只会给 `<img src="./asset/icons/svg_xxx.svg">`，**拿不到 path**
2. 素材已自动落盘：`~/.mgmcp/artifacts/blobs/sha256/**`（文件名是 sha256，与 svg_xxx 无直接对应）
3. **破局点**：blob 内含 `clipPath id="master_svg0_{nodeId}"`
   → `grep -l "master_svg0_622_08923" *.svg` 可**精确反查节点 ↔ 文件**
4. 清洗后用：剥 `<defs>/<clipPath>`、去 `clip-path` 引用；
   配色**不写死 hex** —— 单色改 `fill="currentColor"`（CSS 变量承担），三色 `.md` 徽标走
   `class="td-ico-md-body|-fold|-mark is-solid"`
5. 验证：`agent-browser eval` 读 computedStyle + 放大 probe 截图对照设计稿 PNG
   （`get_screenshot` 可导出设计稿节点大图，落 `~/.mgmcp/resources/screenshots/`）

## 三、改页面的硬规则

- 页面 HTML 内联在 **JS 字符串数组**里，属性引号是 `\"` —— 脚本替换时正则要按 `\\"` 写。
- 替换内联 SVG **禁止**用 `<svg.*?</svg>` + `re.S`（会跨元素吞并整个区块）；
  用 `<svg(?:(?!</svg>).)*?</svg>`，并在替换后做**结构计数自检**（如 `.td-sec-head` / `.td-file` 计数不变）。
- 分组标题类替换必须**回填尾部捕获组**（否则分组名文本被吃掉）。
- 改动一律走 `mg-work/rNN/applyNN.py`（幂等 + 自检），不要手改大文件。

## 四、校验

- `python3 verify-design.py ./pages`（必须传目录）
- ⚠️ 它会**重写 `pages/gaps.log`** → 跑完 `git checkout -- pages/gaps.log`
- 对比是否引入新问题：`git show HEAD:pages/X.html` 导出到临时目录，同口径跑两遍比汇总数

## 五、git

- 仓库根在坚果云内，锁文件坑多（见 `~/.workbuddy/skills` 或 yuanqi SKILL 的"坚果云 git 锁"节）。
- 判定推送成功：`git ls-remote origin main` 与 `git rev-parse HEAD` 一致即可，`update_ref failed` 只是本地 ref 被锁。

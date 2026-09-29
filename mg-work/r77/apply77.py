# -*- coding: utf-8 -*-
"""r77 六项需求补丁（幂等）。

需求：
  1. 基础工作台 aside 会话项「更多」图标的下拉菜单补进场动效（4 页缺失）
  2. 任务详情页 td-left / td-right 的 1px 描边色 = #DAE3ED
  3. 基础工作台 main 底部版权区两行互换（AI 提示句放最下）
  4. 基础工作台 main 波点密度 20px -> 16px（三层同改）
  5. 涟漪：层级回到对话框之下（z-index 10 -> 0）、强度按「至少减半」削弱
  6. 全局滚动条 hover 再浅一级：.20 -> .16（默认档 .16 按邵先生确认保持不变）

幂等三要素：
  ① 先判 NEW 标记命中即 skip；
  ② 再判 count(OLD) 恰好为 N，否则 sys.exit；
  ③ 跑完立刻复跑一次确认「应用: 0 项 / 跳过: N 项」。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = os.path.join(ROOT, "pages")
DS = os.path.join(ROOT, "giencoder-design-system")

applied = 0
skipped = 0


def rd(p):
    return io.open(p, encoding="utf-8").read()


def wr(p, s):
    io.open(p, "w", encoding="utf-8").write(s)


def replace_once(path, old, new, label, mark=None):
    """幂等单处替换。mark 默认取 new（新串特征）。"""
    global applied, skipped
    s = rd(path)
    mm = new if mark is None else mark
    if mm in s:
        print("  skip  %-34s 已应用" % label)
        skipped += 1
        return False
    n = s.count(old)
    if n != 1:
        sys.exit("!! %s：锚点出现 %d 次（期望 1）\n   old=%r" % (label, n, old[:140]))
    s = s.replace(old, new, 1)
    wr(path, s)
    print("  ok    %-34s 1 处" % label)
    applied += 1
    return True


def inject_tail(path, style_id, css, label):
    """在唯一 </body> 前注入 <style id=...>；带标签级计数断言。

    ⚠️ 落点必须在 </body> 前（而不是 </head> 前）：第 76 轮那两块也是注入在
       </body> 前，同特异性规则「后者胜」才成立。第一版误注入到 </head> 前，
       结果 .r74-ripple 的 z-index / 点色被页尾的 r76 块反向压回去（实测
       zIndex 仍是 10、点色仍是 0.62/1.8px），改成页尾后正常。
    """
    global applied, skipped
    s = rd(path)
    mark = '<style id="%s">' % style_id
    if mark in s:
        print("  skip  %-34s 已应用" % label)
        skipped += 1
        return False
    if s.count("</body>") != 1:
        sys.exit("!! %s：</body> 出现 %d 次（期望 1）" % (label, s.count("</body>")))
    n_style = s.count("<style")
    n_end = s.count("</style>")
    block = '<style id="%s">\n%s\n</style>\n' % (style_id, css)
    s = s.replace("</body>", block + "</body>", 1)
    # 自检：标签级计数只允许 +1
    if s.count("<style") != n_style + 1:
        sys.exit("!! %s：<style> 计数 %d → %d（期望 +1）" % (label, n_style, s.count("<style")))
    if s.count("</style>") != n_end + 1:
        sys.exit("!! %s：</style> 计数 %d → %d（期望 +1）" % (label, n_end, s.count("</style>")))
    wr(path, s)
    print("  ok    %-34s 1 处（标签 %d→%d）" % (label, n_style, n_style + 1))
    applied += 1
    return True


# ---------------------------------------------------------------- 需求 6
print("\n=== 需求 6：滚动条 hover .20 -> .16（9 页内联 + 3 处局部 + DS 2 源）===")
SC_PAGES = ["automation", "avatar", "base", "dev", "kanban",
            "req-kanban", "settings", "skills", "task-detail"]
SC_OLD = "::-webkit-scrollbar-thumb:hover{background-color:rgba(var(--gray-10), .20)}"
SC_NEW = "::-webkit-scrollbar-thumb:hover{background-color:rgba(var(--gray-10), .16)}"
for pg in SC_PAGES:
    replace_once(os.path.join(PAGES, pg + ".html"), SC_OLD, SC_NEW, "%s.html 全局 hover" % pg)

# task-detail 局部变量（.td-root 内的滚动条走变量而非上面的内联规则）
replace_once(
    os.path.join(PAGES, "task-detail.html"),
    "--scrollbar-thumb-bg-hover: rgba(0, 0, 0, 0.20);",
    "--scrollbar-thumb-bg-hover: rgba(0, 0, 0, 0.16);",
    "task-detail.html 局部变量 hover",
)

# avatar 卡片体内的滚动条（自定义规则，不走全局）
replace_once(
    os.path.join(PAGES, "avatar.html"),
    ".av-card .giencoder-card-body::-webkit-scrollbar-thumb:hover { background: rgba(0, 0, 0, 0.20); }",
    ".av-card .giencoder-card-body::-webkit-scrollbar-thumb:hover { background: rgba(0, 0, 0, 0.16); }",
    "avatar.html 卡内 hover",
)

# DS 源两文件（这两个文件是多行格式，不像页面那样压成一行）
DS_HOVER_OLD = "::-webkit-scrollbar-thumb:hover {\n    background-color: rgba(var(--gray-10), 0.20);\n  }"
DS_HOVER_NEW = "::-webkit-scrollbar-thumb:hover {\n    background-color: rgba(var(--gray-10), 0.16);\n  }"
replace_once(
    os.path.join(DS, "colors_and_type.css"),
    DS_HOVER_OLD, DS_HOVER_NEW,
    "colors_and_type.css 全局 hover",
)
replace_once(
    os.path.join(DS, "colors_and_type.css"),
    "--scrollbar-thumb-bg-hover: rgba(0, 0, 0, 0.20);",
    "--scrollbar-thumb-bg-hover: rgba(0, 0, 0, 0.16);",
    "colors_and_type.css 变量 hover",
)
replace_once(
    os.path.join(DS, "gienx-templates", "_shared", "tokens.css"),
    DS_HOVER_OLD, DS_HOVER_NEW,
    "tokens.css 全局 hover",
)

# ---------------------------------------------------------------- 需求 1
print("\n=== 需求 1：aside 会话「更多」下拉菜单补进场动效（4 页）===")
POP_CSS = """  /* 第 77 轮 · 需求 1：左边栏 aside 会话项「更多」图标（hover 时出现的 ⋯）弹出
     「会话操作」菜单时补进场动效。该菜单由 React 条件渲染 + createPortal 挂到 body
     （role=menu / aria-label=会话操作），自身只有一条无时长的 background-color
     transition —— 弹出时是「啪」地出现，没有任何过渡。

     base.html 在第 74 轮已配过同一套参数（r74-pop-in），其余页仅剩这几页缺；
     本轮按同一组参数补齐：进场 = 淡入 + 下移 4px 复位 + 0.97 微缩放。
     关键帧另起名（r77-pop-in）：这几页没有 r74 段，同名会让「本页已应用」的判据
     与其它轮次的标记混淆。

     ⚠️ 该菜单是常驻条件渲染（打开才插入 DOM），因此只在挂载时播一次进场 ——
        与「添加内容」「技能选择」那类靠属性选择器触发的方式不同，这里直接按
        role / aria-label 命中即可。退场仍由 React 直接卸载，本轮不动。 */
  @keyframes r77-pop-in {
    from {
      opacity: 0;
      translate: 0 4px;
      scale: 0.97;
    }
  }
  [role="menu"][aria-label="会话操作"] {
    animation: r77-pop-in 160ms cubic-bezier(0.34, 0.69, 0.1, 1) both;
  }"""
for pg in ["automation", "avatar", "skills", "task-detail"]:
    inject_tail(os.path.join(PAGES, pg + ".html"), "r77-pop-css", POP_CSS, "%s.html 更多菜单动效" % pg)

# ---------------------------------------------------------------- 需求 2
print("\n=== 需求 2：td-left / td-right 描边色 -> #DAE3ED ===")
TD = os.path.join(PAGES, "task-detail.html")
replace_once(
    TD,
    "--td-panel-line: #ECEEF2;",
    "--td-panel-line: #ECEEF2;\n  /* 第 77 轮 · 需求 2：td-left / td-right 的 1px 描边色按设计稿取 #DAE3ED。\n"
    "     第 70 轮曾把 --td-panel-line 统一为 #ECEEF2（与主区那一档色一致），本轮邵先生\n"
    "     指定这两个容器回到设计稿取值。DS 没有该色 token ⇒ 按本页既有惯例\n"
    "     （同 --td-appbar、--td-ico-gray）落成本页 token，不改 --td-panel-line 本身，\n"
    "     以免波及 .td-browse（文件预览栏，浏览态才出现）与阅读器外壳那一档。 */\n"
    "  --td-pane-line: #DAE3ED;",
    "task-detail.html --td-pane-line 定义",
    mark="--td-pane-line: #DAE3ED;",
)
# 左栏
replace_once(
    TD,
    "/* ★ 第 52 轮第 3 项：设计稿容器边缘是 1px #DAE3ED 描边，不是投影 */\n"
    "        border: 1px solid var(--td-panel-line);",
    "/* ★ 第 52 轮第 3 项：设计稿容器边缘是 1px #DAE3ED 描边，不是投影；\n"
    "           第 77 轮需求 2：色值回到设计稿的 #DAE3ED（原 --td-panel-line #ECEEF2） */\n"
    "        border: 1px solid var(--td-pane-line);",
    "task-detail.html .td-left 描边",
)
# 右栏
replace_once(
    TD,
    "/* ★ 第 52 轮第 3 项：同左栏 —— 投影改为 1px #DAE3ED 描边 */\n"
    "        border: 1px solid var(--td-panel-line);",
    "/* ★ 第 52 轮第 3 项：同左栏 —— 投影改为 1px #DAE3ED 描边；\n"
    "           第 77 轮需求 2：色值回到设计稿的 #DAE3ED */\n"
    "        border: 1px solid var(--td-pane-line);",
    "task-detail.html .td-right 描边",
)
# 浏览态右缘端点两条（都作用在 .td-right 上）
replace_once(
    TD,
    "    border-right: 0px solid var(--td-panel-line);",
    "    border-right: 0px solid var(--td-pane-line);",
    "task-detail.html .td-right 浏览态右缘",
)
replace_once(
    TD,
    "    border-right: 1px solid var(--td-panel-line);",
    "    border-right: 1px solid var(--td-pane-line);",
    "task-detail.html .td-right 收起态右缘",
)

# ---------------------------------------------------------------- 需求 3
print("\n=== 需求 3：版权区两行互换 ===")
BASE = os.path.join(PAGES, "base.html")
replace_once(
    BASE,
    "children:[(0,A.jsx)(`p`,{children:`内容由 AI 生成，请核实重要信息`}),"
    "(0,A.jsx)(`p`,{children:`© 2026 中电金信研究院 · 数字构建平台实验室（PAA） · 版本：1.2.5`})]",
    "children:[(0,A.jsx)(`p`,{children:`© 2026 中电金信研究院 · 数字构建平台实验室（PAA） · 版本：1.2.5`}),"
    "(0,A.jsx)(`p`,{children:`内容由 AI 生成，请核实重要信息`})]",
    "base.html 版权区行序",
)

# ---------------------------------------------------------------- 需求 4 + 5
print("\n=== 需求 4（波点密度 20→16px）+ 需求 5（涟漪层级与强度）===")
BASE_CSS = """  /* 第 77 轮 · 需求 4：main 波点「稍微密一点」——网格间距 20px -> 16px。
     波点由三层构成，三层用同一个 background-size 才能保持点阵逐点对齐：
       ① .dot-bg 本身的浅点阵（浅色主题 + 深色主题各一条）；
       ② .dot-bg::before 的深一档点阵（指针光斑照亮的那层）；
       ③ .r74-ripple 点击涟漪的点阵层。
     只收紧间距、点径与色值一律不动 ⇒ 密度由 400px²/点 提到 256px²/点。
     ⚠️ 深色主题那条选择器特异性是 0-2-0，必须原样带上 [giencoder-theme='dark']
        前缀才压得住，否则深色主题下仍是 20px。 */
  .dot-bg,
  [giencoder-theme='dark'] .dot-bg,
  .dot-bg::before,
  .r74-ripple {
    background-size: 16px 16px;
  }

  /* 第 77 轮 · 需求 5：涟漪两层调整。
     ① 层级：第 76 轮把它提到 z-index: 10（画在内容之上），邵先生要求
        「涟漪不能置于对话框之上，对话框层级应该最高」。涟漪由页尾脚本
        insertBefore 插在 main 的最前面，与内容同属 z-index:auto 组时按
        tree order 天然压在内容之下 —— 即对话框（composer 白卡）会盖住它。
        故把层级还原成 0（第 74 轮原值），只改这一处即可。
     ② 强度：第 76 轮为了「明显」把点色 α 提到 0.62、点径提到 1.8px，
        邵先生反馈「新的涟漪效果太过明显，至少需要减半」。
        点色取 #2B2B2B（gray-9）不变，按「白底合成色差」折算：
          第 76 轮 α 0.62 ⇒ 合成 rgb(124)，对底色点阵 rgb(240) 的 Δ=116；
          本轮  α 0.28 ⇒ 合成 rgb(196)，Δ=59 —— 恰为上一轮的一半。
        点径顺手由 1.8px 收 1.7px（环更细一点，更像水面），环带形态
        （第 76 轮那套 max(比例, 固定值) 的整流 mask）与 300ms 时长不动。 */
  .r74-ripple {
    z-index: 0;
    background-image: radial-gradient(circle, rgba(var(--gray-9), 0.28) 1.7px, transparent 1.7px);
  }"""
inject_tail(BASE, "r77-base-css", BASE_CSS, "base.html 波点密度 + 涟漪")

print("\n应用: %d 项 | 跳过: %d 项" % (applied, skipped))

# -*- coding: utf-8 -*-
u"""make12.py —— 生成第 13 层补丁 apply12.py（r109 第十二拍四条 + 第十三拍两条）。

第十二拍四条（邵先生原话）：
  1) 标题栏 `.r93-bar` 背景色应该是白色；
  2) `.r93-att.r93-t14` 卡片是用户上传的本地文件，需支持点击卡片展开右栏浏览文件内容；
  3) `.r93-card--ctx` 这种卡片的内间距调整为 16px；
  4) `.zd-sec-h` 这个标题栏支持整行点击展开和折叠。

第十三拍两条（邵先生原话）：
  5) `r93-card r93-card--edge` 这种卡片都去掉前面的缩进；
  6) `zd-host` 这个容器要在骨架屏加载完成后，和对话内容主体一起显示，不要提前显示。

★ 铁律 #2：不得写死绝对色值 ⇒ 白一律走 DS 的 `var(--color-bg-1)`（浅 = #fff / 暗 = #17171a）。
★ 只动这四处，其余一字不改。
★ CRLF：页面的换行一律是 `\\r\\n` ⇒ 运行期先把全文规范化成 LF 再匹配/替换，收尾转回 CRLF。
   （apply12.py 里统一处理；本文件的字面量一律写 LF，可读性优先。）
"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))

# ============================================================================ ⑤ 卡去缩进（第十三拍追加）
# 邵先生：「`r93-card r93-card--edge` 这种卡片都去掉前面的缩进」。
# 真相：`.r93-card` 至今仍是 `width: calc(100% - 18px); margin-left: 18px`
#   （r109 第三拍的「取消缩进」其实**只落在 `.r93-todocard`**，`.r93-card` 从未改掉 ——
#    全页 grep「r109 第三拍」标记数 = 0 为铁证）。
# ⇒ 归零缩进：`width: 100%; margin-left: 0;`（= 与既有的 `.r93-card--full` 同值）。
# ⚠ 同时把 `.r93-card--full` 那句降为注释：它从此与 `.r93-card` 同值（保留选择器不动，
#   零风险 —— 调用点仍写在 HTML 里，删规则反而会改变特指度链条）。
CARD_OLD = (
    u'.r93-card {\n'
    u'  position: relative; width: calc(100% - 18px); margin-left: 18px; border-radius: 8px;\n'
)
CARD_NEW = (
    u'.r93-card {\n'
    u'  position: relative; border-radius: 8px;\n'
    u'  /* \u2605 r109 \u7b2c\u5341\u4e09\u62cd \u2461\uff1a\u90b5\u5148\u751f\u300c`r93-card r93-card--edge` \u8fd9\u79cd\u5361\u7247\u90fd\u53bb\u6389\u524d\u9762\u7684\u7f29\u8fdb\u300d\u3002\n'
    u'     \u672c\u6761\u539f\u4e3a `width: calc(100% - 18px); margin-left: 18px`\uff08\u5de6\u7f29\u8fdb 18px\uff09\u3002\n'
    u'     \u26a0 \u4e4b\u524d\u90a3\u8f6e\u7684\u300c\u53d6\u6d88\u7f29\u8fdb\u300d\u5176\u5b9e**\u53ea\u843d\u5728 `.r93-todocard`**\uff0c`.r93-card` \u4ece\u672a\u6539\u6389 \u2014\u2014\n'
    u'       \u672c\u6761\u7684\u5b50\u7c7b\uff08`.r93-card--edge` \u7b49\uff09\u81ea\u8eab\u65e0\u5bbd\u5ea6\u9879 \u21d2 \u5168\u90e8\u7ee7\u627f\u8fd9 18px\u3002\u73b0\u5f52\u96f6\u3002 */\n'
)
CARD_FULL_OLD = u'.r93-card--full { width: 100%; margin-left: 0; }'
CARD_FULL_NEW = (
    u'/* \u2605 r109 \u7b2c\u5341\u4e09\u62cd \u2461\uff1a\u4e0a\u9762 `.r93-card` \u5df2\u5f52\u96f6\u7f29\u8fdb \u21d2 \u672c\u6761\u4e0e\u4e4b\u540c\u503c\u3002\n'
    u'   \u4fdd\u7559\u9009\u62e9\u5668\u4e0d\u52a8\uff08\u8c03\u7528\u70b9\u4ecd\u5728 HTML \u91cc\uff1b\u5220\u89c4\u5219\u4f1a\u6539\u7279\u6307\u5ea6\u94fe\uff0c\u4e0d\u5fc5\u5192\u8fd9\u4e2a\u9669\uff09\u3002 */\n'
    u'.r93-card--full { width: 100%; margin-left: 0; }'
)

# ============================================================================ ⑥ zd-host 延后到就绪（第十三拍追加）
# 邵先生：「`zd-host` 这个容器要在**骨架屏加载完成**后，**和对话内容主体一起**显示，不要提前显示」。
# 现状：只有一条「骨架屏在屏期间不显示面板」的后手
#   `html:has(.r93-sk) .zd-host { display: none; }`
#   ⇒ 骨架屏在 380+320=700ms **从 DOM 移除**，规则随即失效，面板**立刻**冒出来；
#     而对话主体（`div.mt-8`）要等 `data-r93-app` 置为 `ready` 才 `opacity: 1`（0.2s 过渡）
#     ⇒ 面板比主体**早到**，正是邵先生说的「提前显示」。
# 修法：把「显示」也接到**同一个就绪开关**上（不新造状态、不加 JS 计时）
#   `html[data-r93-app='ready'] .zd-host { display: flex; }`
#   ⇒ 与对话主体同一拍显形；骨架屏期那条后手仍在（`display:none` 先手，同源不冲突）。
# ⚠ 那条 JS 的 380ms 就是「骨架屏开始退场」的时刻，即 `ready` —— 无需改动任何时序。
HOST_OLD = (
    u'html:has(.r93-sk) .zd-host { display: none; }\n'
    + u'.zd-card {'
)
HOST_NEW = (
    u'html:has(.r93-sk):has(.r93-sk) .zd-host { display: none; }\n'
    + u'/* ★ r109 第十三拍 ①：邵先生「`zd-host` 要在**骨架屏加载完成**后，\n'
    + u'   **和对话内容主体一起**显示，不要提前显示」。\n'
    + u'   现状：原来只有上面那条 `:has()` 管「骨架屏在屏期间不显示」；\n'
    + u'   骨架屏 380+320ms 从 DOM 移除后它就失效，面板**立刻**出来 —— 而对话主体还在等\n'
    + u'   `data-r93-app` 置为 `ready`（`.mt-8` 那条的 `opacity: 1` + 0.2s 过渡）⇒ 面板比主体早到 = 「提前显示」。\n'
    + u'   修法：把「显示」也接到**同一个就绪开关**上 —— `data-r93-app` 置为 `ready` 正是脚本在\n'
    + u'   **骨架屏开始退场的那一拍（380ms）**打上的（见下方 JS）⇒ 与主体同拍显形。\n'
    + u'   ⚠ **两条规则同特指度**（都是 0,1,0）⇒ 后者胜 ⇒ 骨架屏期必须用更高优先级压住它\n'
    + u'   （这里叠**两个 `:has()`**）—— 否则 `ready` 一到、骨架屏还在屏上面板就冒出来了（实测踩中）。\n'
    + u'   ★ 不新造状态、不加 JS 计时 ⇒ 与骨架屏时长、主体过渡都不耦合。 */\n'
    + u"html[data-r93-app='ready'] .zd-host { display: flex; }\n"
    + u'.zd-card {'
)



# ============================================================================ ① 标题栏纯白
# 原规则：
#   .r93-bar { … border-bottom: …; background: var(--r93-glass);
#              -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px); }
# 需求「背景色应该是白色的」⇒ 换成**不透明白**（`--color-bg-1`，浅 #fff / 暗 #17171a），
# 并把 backdrop-filter 一并关掉（底已不透明，留着毛玻璃会透出内容虚影 —— 与「纯白」矛盾）。
# ⚠ `--r93-glass` 变量本身 **保留不动**：「滚动到底部」药丸 `.r93-tobottom` 仍在用它。
# ⚠ 暗色档 `--r93-glass: rgba(35,35,36,0.72)` 也一字不动（这里只改 `.r93-bar` 的取值）。
BAR_OLD = (
    u'.r93-bar {\n'
    u'  position: absolute; top: 0; left: 0; right: 0; z-index: 10; height: 44px;\n'
    u'  border-bottom: 1px solid var(--r93-line);\n'
    u'  background: var(--r93-glass);\n'
    u'  -webkit-backdrop-filter: blur(12px);\n'
    u'  backdrop-filter: blur(12px);\n'
    u'}'
)
BAR_NEW = (
    u'.r93-bar {\n'
    u'  position: absolute; top: 0; left: 0; right: 0; z-index: 10; height: 44px;\n'
    u'  border-bottom: 1px solid var(--r93-line);\n'
    u'  /* \u2605 r109 \u7b2c\u5341\u4e8c\u62cd \u2460\uff1a\u90b5\u5148\u751f\u300c\u6807\u9898\u680f `.r93-bar` \u7684\u80cc\u666f\u8272\u5e94\u8be5\u662f\u767d\u8272\u7684\u300d\u3002\n'
    u'     \u539f\u6765\u8d70 `--r93-glass`\uff0872% \u900f\u7684\u767d + 12px \u6bdb\u73bb\u7483\uff09\u21d2 \u5185\u5bb9\u662f\u900f\u51fa\u6765\u7684\u3001\u4e0d\u662f\u300c\u767d\u8272\u300d\u3002\n'
    u'     \u73b0\u5728\u6539\u6210**\u4e0d\u900f\u660e\u767d**\uff08`--color-bg-1`\uff1a\u6d45 = #fff / \u6697 = #17171a\uff09\uff0c\n'
    u'     \u5e76\u5c06 `backdrop-filter` \u4e00\u5e76\u5173\u6389 \u2014\u2014 \u5e95\u5df2\u4e0d\u900f\u660e\uff0c\u7559\u7740\u6bdb\u73bb\u7483\u53ea\u4f1a\u767d\u62ff\u4e00\u5c42\u5408\u6210\u5f00\u9500\uff0c\n'
    u'     \u4e14\u4f1a\u8ba9\u6eda\u52a8\u65f6\u900f\u51fa\u5185\u5bb9\u865a\u5f71\uff08\u4e0e\u300c\u7eaf\u767d\u300d\u81ea\u76f8\u77db\u76fe\uff09\u3002\n'
    u'     \u26a0 `--r93-glass` \u53d8\u91cf\u672c\u8eab**\u4fdd\u7559\u4e0d\u52a8**\uff1a\u300c\u6eda\u52a8\u5230\u5e95\u90e8\u300d\u836f\u4e38\uff08`.r93-tobottom`\uff09\u8fd8\u5728\u7528\u5b83\u3002\n'
    u'     \u26a0 \u6697\u8272\u6863\u7684 `--r93-glass: rgba(35,35,36,0.72)` \u4e5f\u4e00\u5b57\u4e0d\u52a8\u3002 */\n'
    u'  background: var(--color-bg-1);\n'
    u'  -webkit-backdrop-filter: none;\n'
    u'  backdrop-filter: none;\n'
    u'}'
)

# ============================================================================ ③ 上下文卡内距 16
# `.r93-card--ctx` 原先**没有 padding 声明** ⇒ 吃 `.r93-card` 的 `padding: 12px`。
# ⇒ 显式声明 `padding: 16px`（四边同值）。`min-height` / `max-height` 一字不动 ⇒ 卡高上限 240 不变。
CTX_OLD = u'.r93-card--ctx { min-height: 150px; max-height: 240px; overflow-y: auto; overflow-x: hidden; }'
CTX_NEW = (u'/* \u2605 r109 \u7b2c\u5341\u4e8c\u62cd \u2462\uff1a\u90b5\u5148\u751f\u300c`.r93-card--ctx` \u8fd9\u79cd\u5361\u7247\u7684\u5185\u95f4\u8ddd\u8c03\u6574\u4e3a 16px\u300d\u3002\n'
           u'   \u539f\u5148\u672c\u6761**\u6ca1\u6709 padding \u58f0\u660e** \u21d2 \u5b9e\u5f97\u5403 `.r93-card` \u7684 `padding: 12px`\u3002\n'
           u'   \u26a0 `min-height: 150px` / `max-height: 240px` / `overflow` \u4e00\u5b57\u672a\u52a8 \u21d2 \u5361\u9ad8\u4e0a\u9650\u4e0d\u53d8\u3002 */\n'
           u'.r93-card--ctx { min-height: 150px; max-height: 240px; overflow-y: auto; overflow-x: hidden; padding: 16px; }')

# ============================================================================ ④ zd-sec-h 整行可点
# 原实现只有 `.zd-sec-t`（标题按钮，`flex: none`，宽 = 文字宽）绑 click
# ⇒ 标题右侧那一大片 `.zd-sec-x`（`flex: 1 1 auto`）是死区。
# 修法：把同一个处理器再绑到 `.zd-sec-h` 行本身，并用 `closest('.zd-sec-h')` 去重
# （点到按钮上时不重复 toggle 两次 —— 两次 = 看着没反应）。
# ⚠ 既有按钮那套**不重写**，只加行级监听（最小侵入）。
SEC_JS_OLD = (
    u'      var t = sec.querySelector(\'.zd-sec-t\');\n'
    u'      if (!t) return;\n'
    u'      t.addEventListener(\'click\', function () {\n'
    u'        var closed = sec.classList.toggle(\'is-closed\');\n'
    u'        t.setAttribute(\'aria-expanded\', closed ? \'false\' : \'true\');\n'
    u'      });'
)
SEC_JS_NEW = (
    u'      var t = sec.querySelector(\'.zd-sec-t\');\n'
    u'      if (!t) return;\n'
    u'      var row = sec.querySelector(\'.zd-sec-h\');\n'
    u'      function r109SecToggle() {\n'
    u'        var closed = sec.classList.toggle(\'is-closed\');\n'
    u'        t.setAttribute(\'aria-expanded\', closed ? \'false\' : \'true\');\n'
    u'      }\n'
    u'      t.addEventListener(\'click\', function (ev) {\n'
    u'        /* \u2605 r109 \u7b2c\u5341\u4e8c\u62cd \u2463\uff1a\u6574\u884c\u53ef\u70b9 \u21d2 \u4e8b\u4ef6\u4f1a\u4ece `.zd-sec-h` \u5192\u6ce1\u4e0a\u6765\u3002\n'
    u'           \u70b9\u5728\u6807\u9898\u6309\u94ae\u4e0a\u65f6\u7531**\u884c**\u90a3\u4e00\u4efd\u8d1f\u8d23\uff0c\u8fd9\u91cc\u65e9\u9000\uff0c\u907f\u514d toggle \u4e24\u6b21\u3002 */\n'
    u'        if (row && ev.target && ev.target.closest && ev.target.closest(\'.zd-sec-h\') === row) return;\n'
    u'        r109SecToggle();\n'
    u'      });\n'
    u'      /* \u2605 r109 \u7b2c\u5341\u4e8c\u62cd \u2463\uff1a\u90b5\u5148\u751f\u300c`.zd-sec-h` \u8fd9\u4e2a\u6807\u9898\u680f\u652f\u6301\u6574\u884c\u70b9\u51fb\u5c55\u5f00\u548c\u6298\u53e0\u300d\u3002\n'
    u'         \u539f\u6765\u53ea\u6709\u6807\u9898\u6309\u94ae\u5403\u70b9\u51fb\uff0c\u884c\u53f3\u4fa7\uff08`.zd-sec-x` \u90a3\u4e00\u5927\u7247\uff09\u662f\u6b7b\u533a\u3002 */\n'
    u'      if (row && row !== t) row.addEventListener(\'click\', function (ev) {\n'
    u'        /* \u884c\u5185\u7684**\u72ec\u7acb\u6309\u94ae**\uff08\u5982\u300c\u6682\u505c\u76ee\u6807\u300d\u90a3\u679a `.zd-ico`\uff09\u81ea\u5df1\u5403\u4e8b\u4ef6\uff0c\u4e0d\u89e6\u53d1\u6298\u5c55\u3002 */\n'
    u'        if (ev.target && ev.target.closest && ev.target.closest(\'button\') && ev.target.closest(\'button\') !== t) return;\n'
    u'        r109SecToggle();\n'
    u'      });'
)
SEC_CSS_OLD = (
    u'.zd-sec-h {\n'
    u'  display: flex; align-items: center; gap: 6px;\n'
    u'  box-sizing: border-box; padding: 0 8px;'
)
SEC_CSS_NEW = (
    u'.zd-sec-h {\n'
    u'  display: flex; align-items: center; gap: 6px;\n'
    u'  box-sizing: border-box; padding: 0 8px;\n'
    u'  /* \u2605 r109 \u7b2c\u5341\u4e8c\u62cd \u2463\uff1a\u6574\u884c\u53ef\u70b9 \u21d2 \u7ed9\u6574\u884c\u4e00\u4e2a\u624b\u578b\uff08\u539f\u6765\u662f\u6b7b\u533a\u3001\u9f20\u6807\u4e0d\u53d8\u5f62\uff09\u3002 */\n'
    u'  cursor: pointer;'
)

# ============================================================================ ② 附件卡可点
# `.r93-att` 是 `<span>`、零交互 ⇒ 挂 `data-r93-att-file`，由 document 级委托接管。
ATT_JS_OLD = (
    u'    \'<span class="r93-att r93-t14"><span class="r93-iblk r93-i16">\' + IC(\'fmd\') + \'</span>\u90e8\u95e8\u4eba\u5458\u540d\u5355.xlsx</span>\',\n'
    u'    \'<span class="r93-att r93-t14"><span class="r93-iblk r93-i16">\' + IC(\'fmd\') + \'</span>\u4ea7\u54c1\u521d\u7248\u8bbe\u8ba1\u65b9\u6848.md</span>\','
)
ATT_JS_NEW = (
    u'    \'<span class="r93-att r93-t14" data-r93-att-file="\u90e8\u95e8\u4eba\u5458\u540d\u5355.xlsx" role="button" tabindex="0"><span class="r93-iblk r93-i16">\' + IC(\'fmd\') + \'</span>\u90e8\u95e8\u4eba\u5458\u540d\u5355.xlsx</span>\',\n'
    u'    \'<span class="r93-att r93-t14" data-r93-att-file="\u4ea7\u54c1\u521d\u7248\u8bbe\u8ba1\u65b9\u6848.md" role="button" tabindex="0"><span class="r93-iblk r93-i16">\' + IC(\'fmd\') + \'</span>\u4ea7\u54c1\u521d\u7248\u8bbe\u8ba1\u65b9\u6848.md</span>\','
)
ATT_JS_OLD2 = u'    \'<span class="r93-att r93-t14"><span class="r93-iblk r93-i16">\' + IC(\'fxls\') + \'</span>vscode-light-modern-color-system.xlsx</span>\','
ATT_JS_NEW2 = u'    \'<span class="r93-att r93-t14" data-r93-att-file="vscode-light-modern-color-system.xlsx" role="button" tabindex="0"><span class="r93-iblk r93-i16">\' + IC(\'fxls\') + \'</span>vscode-light-modern-color-system.xlsx</span>\','

ATT_CSS_OLD = (
    u'.r93-att {\n'
    u'  display: inline-flex; align-items: center; gap: 8px; height: 40px; padding: 0 12px;\n'
    u'  border-radius: 8px; border: 1px solid var(--color-border-1);\n'
    u'  background: var(--r93-card); color: var(--color-text-1);\n'
    u'}'
)
ATT_CSS_NEW = (
    u'.r93-att {\n'
    u'  display: inline-flex; align-items: center; gap: 8px; height: 40px; padding: 0 12px;\n'
    u'  border-radius: 8px; border: 1px solid var(--color-border-1);\n'
    u'  background: var(--r93-card); color: var(--color-text-1);\n'
    u'}\n'
    u'/* \u2605 r109 \u7b2c\u5341\u4e8c\u62cd \u2461\uff1a\u9644\u4ef6\u5361 = **\u7528\u6237\u4e0a\u4f20\u7684\u672c\u5730\u6587\u4ef6**\uff0c\u53ef\u70b9\u5f00\u53f3\u680f\u6d4f\u89c8\u5185\u5bb9\u3002\n'
    u'   hover \u53ea\u63d0\u8fb9\u6846\u4e00\u7ea7\uff08\u4e0e `.td-sum-art` \u540c\u53e3\u5f84\uff09\uff0c\u4e0d\u52a0\u5e95\u8272 \u2014\u2014 \u5361\u672c\u8eab\u5df2\u6709 `--r93-card` \u5e95\u3002 */\n'
    u'.r93-att[data-r93-att-file] { cursor: pointer; transition: border-color 140ms ease; }\n'
    u'.r93-att[data-r93-att-file]:hover { border-color: var(--color-border-2); }\n'
    u'.r93-att[data-r93-att-file]:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }'
)

# 附件 → 右栏预览：与产物卡（`prevShow`）**同一条链路**，只换数据源。
# ⚠ `.r93-att` 在 `<main>` 里、右栏在 `#av-browse-slot` 里 ⇒ 委托挂 `document` 而不是 `pane`。
ATT_JS_DRIVE_OLD = u'  var artBtns = pane.querySelectorAll(\'[data-td-art]\');'
ATT_JS_DRIVE_NEW = (
    u'  /* \u2605 r109 \u7b2c\u5341\u4e8c\u62cd \u2461\uff1a\u7528\u6237\u4e0a\u4f20\u7684\u672c\u5730\u6587\u4ef6\uff08`.r93-att[data-r93-att-file]`\uff09\n'
    u'     \u2014\u2014 \u70b9\u5361\u7247\u5f00\u53f3\u680f\u300c\u9884\u89c8\u300d\u9875\u7b7e\u6d4f\u89c8\u5185\u5bb9\u3002\u590d\u7528\u4e0a\u9762 `prevShow` \u7684**\u540c\u4e00\u5957**\u9aa8\u67b6\u5207\u6362\u4e0e\u6587\u6848\u586b\u5145\uff0c\n'
    u'     \u53ea\u662f\u6570\u636e\u6e90\u6362\u6210\u5361\u7247\u81ea\u5df1\u7684 `data-r93-att-file`\uff08\u6587\u4ef6\u540d\uff09\uff0c\u4e0d\u4f9d\u8d56 `.td-sum-art` \u90a3\u68f5\u5b50\u6811\u3002\n'
    u'     \u26a0 \u9644\u4ef6\u5361\u5728 `<main>` \u91cc\u3001\u53f3\u680f\u5728 `#av-browse-slot` \u91cc\uff0c\u4e24\u8005\u4e0d\u540c\u5b50\u6811 \u21d2 \u59d4\u6258\u6302 document\u3002 */\n'
    u'  (function () {\n'
    u'    var SIZE_BY_EXT = { xlsx: \'\u8868\u683c \u00b7 34 KB\', xls: \'\u8868\u683c \u00b7 34 KB\', csv: \'\u8868\u683c \u00b7 8 KB\',\n'
    u'                        md: \'Markdown \u00b7 12 KB\' };\n'
    u'    function attShow(el) {\n'
    u'      if (!prevPane) return;\n'
    u'      var name = el.getAttribute(\'data-r93-att-file\') || \'\u6587\u4ef6\';\n'
    u'      var ext = (name.split(\'.\').pop() || \'\').toLowerCase();\n'
    u'      var kind = (/^(xlsx|xls|csv|tsv)$/).test(ext) ? \'xlsx\' : \'md\';\n'
    u'      var ico = el.querySelector(\'.r93-iblk svg\');\n'
    u'      var pn = prevPane.querySelector(\'[data-td-prev-name]\');\n'
    u'      var pm = prevPane.querySelector(\'[data-td-prev-meta]\');\n'
    u'      var pi = prevPane.querySelector(\'[data-td-prev-ico]\');\n'
    u'      if (pn) pn.textContent = name;\n'
    u'      if (pm) pm.textContent = (SIZE_BY_EXT[ext] || \'\u6587\u4ef6\') + \' \u00b7 \u53ea\u8bfb\u9884\u89c8\';\n'
    u'      if (pi && ico) pi.innerHTML = ico.outerHTML;\n'
    u'      var bodies = prevPane.querySelectorAll(\'[data-td-prev-kind]\');\n'
    u'      for (var q = 0; q < bodies.length; q++) {\n'
    u'        if (bodies[q].getAttribute(\'data-td-prev-kind\') === kind) bodies[q].removeAttribute(\'hidden\');\n'
    u'        else bodies[q].setAttribute(\'hidden\', \'\');\n'
    u'      }\n'
    u'      /* \u26a0 \u4e0e `prevShow` \u540c\u5e8f\uff1a**\u5148\u586b\u5185\u5bb9\u518d `openTab`**\uff0c\u5426\u5219\u95ea\u4e00\u5e27\u65e7\u6587\u4ef6\u540d\u3002 */\n'
    u'      openTab(\'preview\', { name: name, ico: ico ? ico.outerHTML : \'\' });\n'
    u'    }\n'
    u'    document.addEventListener(\'click\', function (ev) {\n'
    u'      var el = ev.target && ev.target.closest ? ev.target.closest(\'[data-r93-att-file]\') : null;\n'
    u'      if (el) attShow(el);\n'
    u'    });\n'
    u'    document.addEventListener(\'keydown\', function (ev) {\n'
    u'      if (ev.key !== \'Enter\' && ev.key !== \' \') return;\n'
    u'      var el = ev.target && ev.target.closest ? ev.target.closest(\'[data-r93-att-file]\') : null;\n'
    u'      if (!el) return;\n'
    u'      ev.preventDefault();\n'
    u'      attShow(el);\n'
    u'    });\n'
    u'  })();\n'
    u'  var artBtns = pane.querySelectorAll(\'[data-td-art]\');'
)

EDITS = [
    (u'card-flush', CARD_OLD,         CARD_NEW,         1),
    (u'card-full',  CARD_FULL_OLD,    CARD_FULL_NEW,    1),
    (u'zdhost-ready', HOST_OLD,       HOST_NEW,         1),
    (u'bar-white',  BAR_OLD,          BAR_NEW,          1),
    (u'ctx-pad16',  CTX_OLD,          CTX_NEW,          1),
    (u'sec-css',    SEC_CSS_OLD,      SEC_CSS_NEW,      1),
    (u'sec-js',     SEC_JS_OLD,       SEC_JS_NEW,       1),
    (u'att-css',    ATT_CSS_OLD,      ATT_CSS_NEW,      1),
    (u'att-js1',    ATT_JS_OLD,       ATT_JS_NEW,       1),
    (u'att-js2',    ATT_JS_OLD2,      ATT_JS_NEW2,      1),
    (u'att-drive',  ATT_JS_DRIVE_OLD, ATT_JS_DRIVE_NEW, 1),
]

HEADER = u'''# -*- coding: utf-8 -*-
u"""apply12.py \u2014\u2014 \u2605 \u751f\u6210\u7269\uff0c\u8bf7\u52ff\u624b\u6539\uff1b\u6539\u52a8\u843d make12.py \u7684 EDITS \u8868\u3002

r109 \u7b2c\u5341\u4e8c\u62cd\uff08\u90b5\u5148\u751f\u56db\u6761\uff09\uff1a
  1) \u6807\u9898\u680f `.r93-bar` \u80cc\u666f\u8272 = \u767d\uff08\u8d70 `--color-bg-1`\uff1b\u53d8\u91cf `--r93-glass` \u4fdd\u7559\u7ed9\u836f\u4e38\uff09
  2) `.r93-att.r93-t14` \u9644\u4ef6\u5361\u53ef\u70b9 \u21d2 \u5f00\u53f3\u680f\u300c\u9884\u89c8\u300d\u9875\u7b7e\u6d4f\u89c8\u6587\u4ef6\u5185\u5bb9
  3) `.r93-card--ctx` \u5185\u95f4\u8ddd = 16px
  4) `.zd-sec-h` \u6574\u884c\u53ef\u70b9\u5c55\u5f00 / \u6298\u53e0

\u53ea\u843d `pages/conversation.html`\u3002
\u2605 CRLF\uff1a\u9875\u9762\u6362\u884c\u5168\u4e3a `\\r\\n` \u21d2 \u8fd0\u884c\u671f\u5148\u89c4\u8303\u5316\u6210 LF \u518d\u5339\u914d / \u66ff\u6362\uff0c\u6536\u5c3e\u8f6c\u56de CRLF\u3002
\u2605 \u5e42\u7b49\uff1a\u6bcf\u6761 EDIT \u5148\u5224\u201c\u662f\u5426\u5df2\u542b\u65b0\u4e32\u201d\u3002
"""
import io, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, u'..', u'..', u'..', u'..'))
PAGES = os.path.join(ROOT, u'pages')

EDITS = [
'''

FOOTER = u''']


def run():
    p = os.path.join(PAGES, u'conversation.html')
    raw = io.open(p, 'rb').read()
    t = raw.decode('utf-8').replace(u'\\r\\n', u'\\n')   # \u2190 \u5168\u6587\u89c4\u8303\u5316\u6210 LF
    total = 0
    for name, old, new, want in EDITS:
        # ★ 幂等判据（关键，两次踩坑后定稿）：
        #   纯追加型 EDIT（sec-css / att-css / att-drive）的 `new` = `old` + 追加行
        #   ⇒ `old` 是 `new` 的**严格前缀**，两边计数恒等（都 = 1）
        #   ⇒ 无论用「old 是否消失」还是「old 计数是否等于 new 里的计数」都会**误判为已完成**（第一遍就 [skip]，CSS 根本没落上，实测翻车）。
        #   唯一正确的判据 = **`new` 整体是否已在文里**（追加型跑完后 new 必在；未跑则新增行还没出现）。
        #   ⚠ 反例相反：非追加型（替换型）的 `new` 也可能早就存在（比如 bar-white 的
        #     `background: var(--color-bg-1)` 别处就有）⇒ 必须**两者合取**：
        #     `new in t` **且** `old` 在本 EDIT 的作用域内已归零。
        #   实践（本层 EDITS 全部 `want == 1`）⇒ 判据取：`new in t and t.count(old) == new.count(old)`。
        if (new in t) and (t.count(old) == new.count(old)):
            print(u'  [skip] %-12s \u5df2\u662f\u76ee\u6807\u6001' % name)
            continue
        if (old not in t) and (old not in new):
            print(u'  [skip] %-12s \u5df2\u662f\u76ee\u6807\u6001' % name)
            continue
        c = t.count(old)
        if c != want:
            print(u'  [FAIL] %-12s \u547d\u4e2d %d \u5904\uff08\u671f\u671b %d\uff09' % (name, c, want))
            sys.exit(1)
        t = t.replace(old, new)
        total += c
        print(u'  [ok]   %-12s \u66ff\u6362 %d \u5904' % (name, c))
    out = t.replace(u'\\n', u'\\r\\n').encode('utf-8')     # \u2190 \u6536\u5c3e\u8f6c\u56de CRLF
    if out != raw:
        io.open(p, 'wb').write(out)
    print(u'  >> \u5171\u66ff\u6362 %d \u5904\uff1bmd5 = %s' % (total, hashlib.md5(out).hexdigest()))


if __name__ == u'__main__':
    run()
'''


def main():
    lines = [HEADER]
    for name, old, new, want in EDITS:
        lines.append(u'    (u%r,\n     u%r,\n     u%r,\n     %d),\n' % (name, old, new, want))
    lines.append(FOOTER)
    src = u''.join(lines)
    dst = os.path.join(HERE, u'apply12.py')
    io.open(dst, 'w', encoding='utf-8', newline=u'').write(src)
    print(u'make12.py \u2192 %s (%d bytes)' % (dst, len(src.encode('utf-8'))))


if __name__ == u'__main__':
    main()

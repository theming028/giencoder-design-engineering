# -*- coding: utf-8 -*-
"""r107 第二拍 · 侧边聊天对齐主对话（r93-scroll）
   ① _mods.html：助手标记去掉写死的「A」，改由 JS 注入与主对话同源的 GienX logo
   ② panel.js  ：新增 AV_SVG 常量 + 初始化填充 + pushMsg 用它
   —— 全部用「命中数断言」的方式改，命中数不符即退出（不写任何文件）。
"""
import io, os, sys

P107 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PART = os.path.join(P107, 'part107')
REPO = os.path.dirname(os.path.dirname(P107))
PAGE = os.path.join(REPO, 'pages', 'conversation.html')


def read(p):
    return io.open(p, 'r', encoding='utf-8', newline='').read()


def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


# ---------- 0. 从页面里抽出助手 logo（与主对话 `.r93-ahd > .r93-i24` 同一枚） ----------
pg = read(PAGE).replace('\r\n', '\n')
i = pg.find("gienx: '")
j = pg.find("',", i)
if i < 0 or j < 0:
    sys.exit('!! 抽不到 gienx 图标')
AV = pg[i + len("gienx: '"):j]
if not AV.startswith('<svg') or not AV.endswith('</svg>'):
    sys.exit('!! gienx 片段不完整：%r' % AV[:40])
if "'" in AV:
    sys.exit('!! gienx 片段含单引号，不能直接当 JS 单引号字符串')
for tok in ('<script', '</script', '<style', '</style'):
    if tok in AV:
        sys.exit('!! gienx 片段含注入守卫禁止的 %r' % tok)
print('   抽出助手 logo：%d 字符' % len(AV))

# ---------- 1. _mods.html：清掉写死的「A」 ----------
p = os.path.join(PART, '_mods.html')
s = read(p)
old, new = '<span class="td-side-av">A</span>', '<span class="td-side-av" aria-hidden="true"></span>'
n = s.count(old)
if n != 2:
    sys.exit('!! _mods.html 命中 %d 次（应 2 次）' % n)
s = s.replace(old, new)
write(p, s)
print('   _mods.html：清掉写死的「A」%d 处' % n)

# ---------- 2. panel.js：AV_SVG + 初始化填充 + pushMsg ----------
p = os.path.join(PART, 'panel.js')
s = read(p)
s = s.replace('\r\n', '\n')

# 2a 常量（插在「标签栏」分节注释之前）
anchor = '\n  /* ==================== 标签栏 ==================== */'
if s.count(anchor) != 1:
    sys.exit('!! panel.js 常量锚点命中 %d 次' % s.count(anchor))
const = (
    "\n  /* ★ r107 返工：助手标记 —— 与主对话助手头（`.r93-ahd > .r93-i24`）**同一枚 logo**、\n"
    "     同为 24px 原生尺寸（零缩放）。原来写死一个字母「A」+ `--color-primary-1` 圆底，\n"
    "     那套视觉在主对话里不存在 ⇒ 侧边聊天看起来像另一个产品。 */\n"
    "  var AV_SVG = '" + AV + "';\n"
)
s = s.replace(anchor, const + anchor, 1)

# 2b pushMsg 里创建的头像
old = ("      var av = document.createElement('span');\n"
       "      av.className = 'td-side-av';\n"
       "      av.textContent = 'A';\n")
new = ("      var av = document.createElement('span');\n"
       "      av.className = 'td-side-av';\n"
       "      av.setAttribute('aria-hidden', 'true');\n"
       "      av.innerHTML = AV_SVG;\n")
if s.count(old) != 1:
    sys.exit('!! panel.js pushMsg 头像锚点命中 %d 次' % s.count(old))
s = s.replace(old, new, 1)

# 2c 初始化：把 markup 里两个空标记填上
anchor2 = "  var askBtn = selbar.querySelector('[data-td-side-ask]');"
if s.count(anchor2) != 1:
    sys.exit('!! panel.js 初始化锚点命中 %d 次' % s.count(anchor2))
init = ("  /* markup 里那两枚 `.td-side-av` 是空的（避免把 5KB 的 logo 路径在任何地方复制多份）\n"
        "     ⇒ 这里统一注入同一枚 logo；`pushMsg` 新建的消息直接用同一个常量。 */\n"
        "  var avHosts = pane.querySelectorAll('.td-side-av');\n"
        "  for (var a0 = 0; a0 < avHosts.length; a0++) {\n"
        "    if (!avHosts[a0].firstChild) avHosts[a0].innerHTML = AV_SVG;\n"
        "  }\n")
s = s.replace(anchor2, init + anchor2, 1)

write(p, s)
print('   panel.js：AV_SVG 常量 + 初始化填充 + pushMsg 注入  ✓')
print('   命中明细：`.td-side-av` 残留在 panel.js 里 %d 处（应 0 处写死字母）' % s.count("textContent = 'A'"))

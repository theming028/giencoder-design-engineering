# -*- coding: utf-8 -*-
"""第 34 轮第 2 项断言器：数字分身页「通过对话完善数字分身」→ 右侧 AI 对话栏抽屉。

输入：
  · pages/avatar.html                 —— 静态结构 / 契约类名 / token / 幂等标记
  · pages/task-detail.html            —— 参照真值（模块来源）
  · mg-work/r34/probe34.jsonl         —— 实测探针（开合 / 弹层 / 全屏 / Esc 分级）
  · mg-work/r34/cmp2.jsonl            —— 详情页 vs 分身页 内部几何逐项对照
  · mg-work/r34/cmp-detail.jsonl      —— 详情页同名弹层尺寸

用法：C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe mg-work/r34/check34.py
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PASS, FAIL = [], []


def chk(tag, desc, cond, detail=""):
    (PASS if cond else FAIL).append("%s %s" % (tag, desc))
    if not cond:
        print("  ✗ %s %s  %s" % (tag, desc, detail))


def load_jsonl(p):
    out = {}
    for ln in io.open(os.path.join(ROOT, p), encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        d = json.loads(ln)
        out[d["step"]] = d["data"]
    return out


P = load_jsonl("mg-work/r34/probe34.jsonl")
C = load_jsonl("mg-work/r34/cmp2.jsonl")
D = load_jsonl("mg-work/r34/cmp-detail.jsonl")
AV = io.open(os.path.join(ROOT, "pages", "avatar.html"), encoding="utf-8").read()
TD = io.open(os.path.join(ROOT, "pages", "task-detail.html"), encoding="utf-8").read()
DS = io.open(os.path.join(ROOT, "giencoder-design-system", "components.css"), encoding="utf-8").read()

START = "<!-- AV-CHAT-DRAWER"
END = "<!-- /AV-CHAT-DRAWER -->"

# ══════════════════════════ 1. 静态结构 ══════════════════════════
a, b = AV.find(START), AV.find(END)
chk("1a", "注入段标记唯一且成对（START/END 各 1 次）",
    AV.count(START) == 1 and AV.count(END) == 1 and a < b)
inject = AV[a - 2:b + len(END)]
css_seg = inject[inject.find("<style"):inject.find("</style>")]   # 注入段里的 CSS 段（供多处断言复用）
chk("1b", "注入段以结束标记收尾（script 在标记之内，避免重复构建残留旧脚本）",
    inject.rstrip().endswith(END) and '<script id="av-chat-js">' in inject
    and inject.index('<script id="av-chat-js">') < inject.index(END))
for tag, pat in (("1c1", 'id="av-chat-js"'), ("1c2", 'id="av-chat-css"'),
                 ("1c3", 'class="av-chat-mask"'), ("1c4", 'id="av-chat-drawer"')):
    chk(tag, "注入段内 %s 只出现 1 次（无重复注入）" % pat, AV.count(pat) == 1,
        "count=%d" % AV.count(pat))

# 模块类名齐备（抽查每条链路上的关键类）
MOD = [".td-right", ".td-right-inner", ".td-right-bar", ".td-right-title", ".td-right-time",
       ".td-right-acts", ".td-round-btn", ".td-chat", ".td-chat-inner", ".td-msg-user",
       ".td-msg-ai", ".td-ai-head", ".td-ai-avatar", ".td-ai-name", ".td-ai-meta",
       ".td-ai-foot", ".td-ai-foot-item", ".td-ai-foot-ico", ".td-ai-foot-ico .td-ico-check",
       ".td-composer", ".td-add-pop", ".td-add-item", ".td-add-sep",
       ".td-skill-pop", ".td-skill-list", ".td-skill-row", ".td-skill-ico", ".td-skill-txt",
       ".td-skill-name", ".td-skill-desc", ".td-skill-tag", ".td-skill-group",
       ".td-skill-foot", ".td-skill-x", ".td-file", ".td-file--lg", ".td-file-ico",
       ".td-file-sep", ".td-file-tx", ".td-file-size", ".td-file-body", ".td-sep",
       ".td-ico-md-body", ".td-ico-md-fold", ".td-ico-md-mark", ".td-ico-min"]
missing = [c for c in MOD if c not in inject]
chk("1d", "模块 %d 个关键类全部落地" % len(MOD), not missing, "缺失 %s" % missing)

for tag, cls in (("1e1", ".td-composer .min-h-\\[96px\\]"), ("1e2", ".td-composer .gap-\\[2px\\]"),
                 ("1e3", ".td-composer .bg-\\[var\\(--color-fill-3\\)\\]"),
                 ("1e4", ".td-composer .giencoder-select-popup")):
    chk(tag, "补丁类 %s 已随模块带入" % cls, cls in inject)

# 状态改写 / 剔除
chk("1f", "详情页 11 处 .td-root. 状态选择器全部改写为 .av-chat-drawer.",
    ".av-chat-drawer.is-fullscreen .td-chat-inner" in inject
    and ".av-chat-drawer.is-fullscreen .td-composer" in inject
    and ".av-chat-drawer.is-collapsed .td-collapsed" in inject)
body_only = re.sub(r"/\*.*?\*/", "", inject, flags=re.S)
chk("1g", "注入段内不再残留 .td-root 选择器（注释除外）",
    not re.search(r"\.td-root\b", body_only))
for tag, bad in (("1h1", "is-dragging"), ("1h2", "is-swapped"), ("1h3", ".td-left")):
    chk(tag, "两栏专属规则 %s 已剔除（抽屉无拖动分栏/左栏）" % bad, bad not in body_only)

# 属性语义分离（第 34 轮踩坑）
js_seg = inject[inject.find('<script id="av-chat-js">'):]
js_code = re.sub(r"/\*.*?\*/", "", js_seg, flags=re.S)           # 去注释后再判（注释里有反例示例）
chk("1i", "触发器标记与开合状态分离：closest 用 data-av-chat-toggle（代码里不得出现 data-av-chat-open）",
    "closest('[data-av-chat-toggle]')" in js_code
    and "closest('[data-av-chat-open]')" not in js_code)
chk("1j", "触发器按钮写 data-av-chat-toggle，状态写在 <html> 上（data-av-chat-open）",
    "btn.setAttribute('data-av-chat-toggle', '1')" in inject
    and "root.setAttribute('data-av-chat-open', '')" in inject
    and "querySelectorAll('[data-av-chat-toggle]')" in inject)
n_all = css_seg.count("[data-av-chat-open]")
n_qual = css_seg.count("html[data-av-chat-open]") + css_seg.count("html:not([data-av-chat-open])")
chk("1k", "CSS 里 %d 处 [data-av-chat-open] 全部带 html 元素限定（不会误命中后代）" % n_all,
    n_all == n_qual and n_all >= 4, "all=%d qualified=%d" % (n_all, n_qual))

# CSS 注释定界符（第 33 轮踩坑）
bad_cmt = []
for m in re.finditer(r"/\*", css_seg):
    seg = css_seg[m.start():]
    inner = seg[2:seg.find("*/", 2)]
    if "/*" in inner:
        bad_cmt.append(inner[:60])
chk("1l", "CSS 注释无嵌套 /*（不会把紧随其后的规则吞成声明块）", not bad_cmt, str(bad_cmt[:2]))
chk("1m", "CSS 注释定界符成对", css_seg.count("/*") == css_seg.count("*/"))

# token
TOK = ["--td-bar", "--td-right-w: 480px", "--td-collapsed-w", "--td-fs-content: 860px",
       "--td-radius-card", "--td-card", "--td-line", "--td-meta", "--td-strong",
       "--td-ink-2", "--td-bubble", "--td-panel-shadow", "--td-ico-gray", "--td-ico-web",
       "--td-ico-md", "--td-ico-md-fold", "--td-ico-skill",
       "--av-chat-w", "--av-chat-top", "--av-chat-gap: 8px", "--av-chat-ease"]
miss_tok = [t for t in TOK if t not in inject]
chk("1n", "模块与适配层所需 %d 个 token 全部定义" % len(TOK), not miss_tok, "缺失 %s" % miss_tok)
used = set(re.findall(r"var\((--(?:td|av)-[a-z0-9-]+)", inject))
chk("1o", "注入段内 var(--td-*/--av-*) 均有定义", not [
    v for v in used if not re.search(re.escape(v) + r"\s*:", inject)], "未定义 %s" % [
    v for v in used if not re.search(re.escape(v) + r"\s*:", inject)])

# 无残留占位符
_no_cmt = re.sub(r"/\*.*?\*/", "", inject, flags=re.S)
chk("1p", "注入段无残留骨架占位符 __XXX__（注释中的历史说明不计）",
    not re.findall(r"__[A-Z][A-Z_]*__", _no_cmt),
    str(re.findall(r"__[A-Z][A-Z_]*__", _no_cmt)[:5]))

# 原页面内容：第 35 轮第 2 项已按设计稿 1345:18487 还原主内容，
# 旧的「数字分身列表」容器与文案被**有意**替换（原断言 1q/1r 的语义随之更新）。
chk("1q", "主内容已还原：bundle 的 Dt() 渲染体换成 .av-main 空壳（旧 max-w-3xl 容器已不在）",
    "mx-auto flex w-full max-w-3xl flex-col gap-5" not in AV
    and 'className:`av-main`,id:`av-main`' in AV)
chk("1r", "旧列表文案已移除，第 35 轮第 2 项注入段 AV-MAIN 成对存在",
    "新建分身" not in re.sub(r"/\*.*?\*/", "", AV, flags=re.S)
    and "自动化观察员" not in AV
    and AV.count("<!-- AV-MAIN") == 1 and AV.count("<!-- /AV-MAIN -->") == 1)
chk("1s", "外壳 SHELL-TABS-FIX 段未被破坏", "<!-- /SHELL-TABS-FIX -->" in AV)

# 契约类名自检：注入段用到的 giencoder-* 必须都在 DS components.css 里
gc = set(re.findall(r'class="([^"]*giencoder-[^"]*)"', inject))
names = set()
for c in gc:
    names.update(x for x in c.split() if x.startswith("giencoder-"))
undef = sorted(n for n in names if ("." + n) not in DS)
chk("1t", "注入段 %d 个 giencoder-* 契约类全部在 components.css 中定义" % len(names),
    not undef, "未定义 %s" % undef)

# ══════════════════════════ 2. 实测探针 ══════════════════════════
t = P.get("trig", {})
chk("2a", "触发器落在内容标题行右侧：[926,73,192,32]（secondary + size-default）",
    t.get("rect") == [926, 73, 192, 32]
    and t.get("cls") == "giencoder-btn giencoder-btn-secondary giencoder-btn-size-default av-chat-trigger",
    str(t.get("rect")))
chk("2b", "触发器文案与 a11y：通过对话完善数字分身 + aria-controls=av-chat-drawer",
    t.get("txt") == "通过对话完善数字分身" and t.get("aria", [None])[0] == "av-chat-drawer", str(t.get("txt")))
chk("2c", "标题行左对齐 + 8px gap，子项顺序 [标题组][触发器][新建分身]",
    t.get("rowJC") == "flex-start" and t.get("rowGap") == "8px"
    and [k.get("txt", "")[:4] for k in t.get("rowKids", [])] == ["数字分身", "通过对话", "新建分身"],
    str(t.get("rowKids")))
chk("2d", "目标行全页唯一（结构选择器安全）：allRows == 1", t.get("allRows") == 1)
chk("2e", "标记属性分离：触发器有 data-av-chat-toggle，<html> 没有",
    t.get("toggleAttr") is True and t.get("htmlHasToggle") is False)
chk("2f", "初始 <html> 属性干净（仅 lang，无残留 aria-expanded/data-av-chat-open）",
    t.get("htmlAttrsBefore") == ["lang"], str(t.get("htmlAttrsBefore")))

c = P.get("closed", {})
chk("3a", "关闭态：完全移出视口 [1440,48,480,844] + translateX(488=100%+8gap)",
    c.get("rect") == [1440, 48, 480, 844] and c.get("tf") == "matrix(1, 0, 0, 1, 488, 0)", str(c.get("rect")))
chk("3b", "关闭态：aria-hidden=true、遮罩 opacity 0 / pointer-events none",
    c.get("ariaHidden") == "true" and c.get("maskOp") == "0" and c.get("maskPE") == "none")
chk("3c", "抽屉定位形态：position fixed / width 480（=--td-right-w）/ radius 8",
    c.get("pos") == "fixed" and c.get("w") == "480px" and c.get("radius") == "8px")

o = P.get("opened", {})
chk("4a", "★ 打开态盒子 [952,48,480,844] —— 与详情页 .td-right 完全相同（含外壳 8px gutter）",
    o.get("rect") == [952, 48, 480, 844], str(o.get("rect")))
chk("4b", "打开态：transform 归零、aria-hidden=false、遮罩 opacity 1 / 可点、z-index 70",
    o.get("tf") == "matrix(1, 0, 0, 1, 0, 0)" and o.get("ariaHidden") == "false"
    and o.get("maskOp") == "1" and o.get("maskPE") == "auto" and o.get("z") == "70")
chk("4c", "触发器 aria-expanded 同步为 true", o.get("trigExpanded") == "true")
chk("4d", "顶栏 64 高，3 个 32×32 圆角按钮（新会话/会话历史/全屏）",
    o.get("bar") == [952, 48, 480, 64]
    and [r[0] for r in o.get("roundBtns", [])] == ["新会话", "会话历史", "全屏"]
    and all(r[1][2:] == [32, 32] for r in o.get("roundBtns", [])), str(o.get("roundBtns")))
chk("4e", "★ 打开后 <html> 只有 data-av-chat-open，未被写入 aria-expanded（第 34 轮修复回归）",
    o.get("htmlAttrs") == ["lang", "data-av-chat-open"] and o.get("htmlAria") is None,
    str(o.get("htmlAttrs")) + " aria=" + str(o.get("htmlAria")))

m = P.get("composer", {})
chk("5a", "对话框白卡 [972,718,440,154] / 圆角 16 / 描边 --color-border-2(229)",
    m.get("card") == [972, 718, 440, 154] and m.get("cardRadius") == "16px"
    and m.get("cardBorder") == "rgb(229, 229, 229)", str(m.get("card")))
chk("5b", "textarea [985,731,414,96] / min-height 96px / 文案「描述你的任务，/ 调用技能，@引用文件」",
    m.get("ta", {}).get("rect") == [985, 731, 414, 96]
    and m.get("ta", {}).get("minH") == "96px"
    and m.get("ta", {}).get("ph") == "描述你的任务，/ 调用技能，@引用文件", str(m.get("ta")))
chk("5c", "★ 工具栏不破版：[985,827,414,32] 且 scrollWidth == clientWidth == 414（overflow 0）",
    m.get("toolbar", {}).get("rect") == [985, 827, 414, 32]
    and m.get("toolbar", {}).get("sw") == m.get("toolbar", {}).get("cw") == 414,
    str(m.get("toolbar")))
chk("5d", "艾迪胶囊 70×32（--td-right-w 480 下收敛后的正确尺寸）",
    m.get("avatar") == "艾迪" and m.get("avatarRect") == [1057, 827, 70, 32], str(m.get("avatarRect")))
chk("5e", "模式与大模型两项选择器：['标准模式','DeepSeek-V4-Pro']；发送按钮 disabled",
    m.get("models") == ["标准模式", "DeepSeek-V4-Pro"] and m.get("sendDisabled") is True)
chk("5f", "消息区（用户气泡 + AI 消息头）随模块带入",
    m.get("msgs", {}).get("user") == "请帮我先分析一下这个任务"
    and m.get("msgs", {}).get("aiName") == "艾迪")

ap = P.get("addpop", {})
chk("6a", "★ 添加上下文菜单 180×92 @ [985,731]（与详情页实测完全一致）+ 圆角 8 + 白底",
    ap.get("vis") is True and ap.get("rect") == [985, 731, 180, 92]
    and ap.get("radius") == "8px" and ap.get("bg") == "rgb(255, 255, 255)", str(ap.get("rect")))
chk("6b", "菜单两项：添加本地文件 / 知识库",
    ap.get("items") == ["添加本地文件", "知识库"], str(ap.get("items")))
chk("6c", "再点触发器 → 菜单关闭（hidden=true，且不遗留 data-td-pop-open）",
    P.get("addpopClosed", {}).get("hidden") is True
    and P.get("addpopClosed", {}).get("htmlAttr") is False)

sp = P.get("skillpop", {})
chk("7a", "★ 技能面板 438×320 @ [973,391]（与详情页实测完全一致）+ 圆角 12",
    sp.get("vis") is True and sp.get("rect") == [973, 391, 438, 320]
    and sp.get("radius") == "12px", str(sp.get("rect")))
chk("7b", "面板内容：Goal 行 + 技能 Skills 分组 + 6 行技能 + 底部 安装技能/管理技能",
    sp.get("rows") == 6 and sp.get("groups") == ["技能 Skills"]
    and sp.get("foot") == ["安装技能", "管理技能"], str(sp.get("rows")))
chk("7c", "关闭技能面板后 hidden=true", P.get("skillpopClosed", {}).get("hidden") is True)

sl = P.get("selpop", {})
chk("8a", "DS Select 弹层用 .giencoder-popup-open 打开（不是内联 display）",
    sl.get("open") is True and sl.get("vis") is True, str(sl.get("open")))
chk("8b", "大模型 4 个选项齐备（含 1 个 disabled）",
    sl.get("opts") == ["标准模式", "专家模式", "DeepSeek-V4-Pro", "GLM-5.2-公司共用",
                       "Qwen 3.8-max", "Kimi-2.6"], str(sl.get("opts")))
pk = P.get("selpick", {})
chk("8c", "点选项 2 → 文案回写为 GLM-5.2-公司共用，且弹层全关（openCount 0）",
    pk.get("model") == "GLM-5.2-公司共用" and pk.get("openCount") == 0, str(pk))
chk("8d", "「标准模式」选择器在 480 宽下按详情页同一约定收起（display none）",
    pk.get("stdModeDisplay") == "none")

fs = P.get("fullscreen", {})
chk("9a", "★ 全屏：抽屉铺满外壳内容区 [8,48,1424,844]（左右各留 8px gutter）",
    fs.get("cls") is True and fs.get("drawer") == [8, 48, 1424, 844]
    and fs.get("drawerW") == "1424px", str(fs.get("drawer")))
chk("9b", "★ 全屏：内容最大宽 860px 且水平居中（消息列 [290,128,860,290]、输入区 [290,718,860,154]）",
    fs.get("chatAlign") == "center"
    and fs.get("chatInner", {}).get("maxW") == "860px"
    and fs.get("chatInner", {}).get("rect") == [290, 128, 860, 290]
    and fs.get("composer", {}).get("maxW") == "860px"
    and fs.get("composer", {}).get("rect") == [290, 718, 860, 154], str(fs.get("composer")))
chk("9c", "全屏态遮罩让位（opacity 0），按钮语义切到「退出全屏」+ 图标互换",
    fs.get("maskOp") == "0" and fs.get("fsLabel") == "退出全屏"
    and fs.get("icoMax") == "none" and fs.get("icoMin") == "block")

chk("10a", "★ Esc 分级①：先退全屏、抽屉保持打开",
    P.get("esc1", {}).get("fullscreen") is False and P.get("esc1", {}).get("open") is True
    and P.get("esc1", {}).get("rect") == [952, 48, 480, 844], str(P.get("esc1")))
chk("10b", "★ Esc 分级②：再按才关闭抽屉（translateX 488 + 遮罩归零）",
    P.get("esc2", {}).get("open") is False
    and P.get("esc2", {}).get("tf") == "matrix(1, 0, 0, 1, 488, 0)"
    and P.get("esc2", {}).get("maskOp") == "0")
chk("11a", "可再次打开（reopen [952,48,480,844]）",
    P.get("reopen", {}).get("open") is True and P.get("reopen", {}).get("rect") == [952, 48, 480, 844])
chk("11b", "点遮罩关闭抽屉",
    P.get("maskClose", {}).get("open") is False
    and P.get("maskClose", {}).get("tf") == "matrix(1, 0, 0, 1, 488, 0)")

pi = P.get("pageIntact", {})
chk("12a", "页面本体未受影响：内容容器仍 [466,73,768,285] / maxW 768px / 3 张卡片",
    pi.get("content", {}).get("rect") == [466, 73, 768, 285]
    and pi.get("content", {}).get("maxW") == "768px" and pi.get("cards") == 3, str(pi.get("content")))
chk("12b", "外壳 main 与左侧导航栏不变：[268,48,1164,844] + aside[12,48,256,844]，抽屉为其后新增",
    pi.get("main") == [268, 48, 1164, 844] and pi.get("asides") == [["", [12, 48, 256, 844]],
                                                                 ["av-chat-drawer", [1440, 48, 480, 844]]],
    str(pi.get("asides")))
chk("12c", "脚本/样式块数量：4 个 script（多出 av-chat-js）、3 个 style（未新增 style 块，靠内联追加）",
    pi.get("scripts") == 4 and pi.get("styleBlocks") == 3, str(pi))

# ══════════════════════════ 3. 与详情页逐项对照 ══════════════════════════
KEYS = ["rightPanel", "card", "ta", "taMinH", "toolbar", "sw", "cw", "avatar", "bar"]
dt, av = json.loads(C.get("detail", "{}")), json.loads(C.get("avatar", "{}"))
chk("13a", "★ 详情页 vs 分身页抽屉：%d 项内部几何逐位相等" % len(KEYS),
    all(dt.get(k) == av.get(k) for k in KEYS),
    str({k: (dt.get(k), av.get(k)) for k in KEYS if dt.get(k) != av.get(k)}))
chk("13b", "对照真值本身成立：rightPanel [952,48,480,844] / textarea minH 96px / toolbar 414 不溢出",
    dt.get("rightPanel") == [952, 48, 480, 844] and dt.get("ta") == [985, 731, 414, 96]
    and dt.get("taMinH") == "96px" and dt.get("sw") == dt.get("cw") == 414, str(dt))
chk("13c", "★ 详情页技能面板 438×320 与分身页相同（定位仅差外壳 gutter 位移）",
    D.get("detailSkill", {}).get("rect") == sp.get("rect") == [973, 391, 438, 320],
    "%s vs %s" % (D.get("detailSkill", {}).get("rect"), sp.get("rect")))
chk("13d", "★ 详情页添加上下文菜单 180×92 与分身页相同",
    D.get("detailAdd", {}).get("rect") == ap.get("rect") == [985, 731, 180, 92],
    "%s vs %s" % (D.get("detailAdd", {}).get("rect"), ap.get("rect")))
chk("13e", "详情页同项圆角一致（技能面板 12px、添加菜单 8px）",
    D.get("detailSkill", {}).get("radius") == "12px" and D.get("detailAdd", {}).get("radius") == "8px")

# ══════════════════════════ 4. 与详情页同源同步 ══════════════════════════
chk("14a", "模块 HTML 与详情页同源：AI 消息/文件卡/技能行文案逐条一致",
    all(x in AV for x in ("端到端初始化 - 任务分析报告.md", "请帮我先分析一下这个任务",
                          "系统atic-debugging" if False else "systematic-debugging",
                          "subagent-driven-development")))
chk("14b", "详情页仍保有同名模块（未因本轮改动被破坏）",
    '<aside class="td-right" aria-label="AI 会话">' in TD.replace('\\"', '"')
    or 'td-right" aria-label=\\"AI 会话\\"' in TD)

print()
print("=" * 74)
print("PASS %d / FAIL %d" % (len(PASS), len(FAIL)))
for f in FAIL:
    print("  FAIL  " + f)
print("ALL_OK" if not FAIL else "HAS_FAIL")

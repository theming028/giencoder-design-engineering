# -*- coding: utf-8 -*-
"""第31轮断言器：读取 mg-work/r31/probe31.jsonl，逐项核对设计稿真值与契约。
设计稿真值来源：mg-work/r31/design/dispatch.{txt,png} + measure5~17.py（覆盖率 0.5 亚像素法）
"""
import io
import json
import sys

PROBE = "mg-work/r31/probe31.jsonl"
rows = {}
for ln in io.open(PROBE, encoding="utf-8"):
    ln = ln.strip()
    if not ln:
        continue
    o = json.loads(ln)
    rows[o["step"]] = o["data"]

OK = []
BAD = []
def chk(step, name, cond, got, want):
    (OK if cond else BAD).append((step, name, got, want))
    print("  %s %-6s %-34s got=%s  want=%s" % ("✓" if cond else "✗ FAIL", step, name, got, want))

def g(step):
    d = rows.get(step)
    if d is None:
        BAD.append((step, "<missing>", None, "probe 缺失"))
        print("  ✗ FAIL %-6s probe 步骤缺失" % step)
        return {}
    if "__parse_error__" in d:
        BAD.append((step, "<parse_error>", d.get("raw"), "解析失败"))
        print("  ✗ FAIL %-6s __parse_error__ %s" % (step, str(d.get("raw"))[:120]))
        return {}
    return d

def near(a, b, tol=1.0):
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False

def rgbs(v):
    """把 computed color 归一成 (r,g,b)；兼容 'rgb(a, b, c)' / 'rgba(a,b,c,al)'"""
    if v is None:
        return None
    s = str(v).replace("rgba(", "").replace("rgb(", "").replace(")", "")
    parts = [p.strip() for p in s.split(",")]
    try:
        return tuple(int(round(float(p))) for p in parts[:3])
    except Exception:
        return None

def rgbv(v):
    t = rgbs(v)
    return None if t is None else "rgb(%d, %d, %d)" % t

def is_clear(v):
    """透明底判定：computed backgroundColor 的透明形态"""
    return str(v or "").replace(" ", "") in ("rgba(0,0,0,0)", "transparent")

print("=" * 108)
print("1a. 基线 / 触发按钮契约")
d = g("1a")
chk("1a", "触发按钮存在", d.get("hasBtn") is True, d.get("hasBtn"), True)
chk("1a", "按钮文案", d.get("btnText") == "转派", d.get("btnText"), "转派")
chk("1a", "按钮尺寸 70x28", near(d.get("btnRect", [0,0,0,0])[2], 70, 1) and near(d.get("btnRect", [0,0,0,0])[3], 28, 1), d.get("btnRect"), "[*,*,70,28]")
chk("1a", "触发按钮包在 popover-reference 内", "giencoder-popover-reference" in (d.get("refClass") or ""), d.get("refClass"), "含 giencoder-popover-reference")
chk("1a", "aria-expanded=false", d.get("ariaExpanded") == "false", d.get("ariaExpanded"), "false")
chk("1a", "aria-haspopup=dialog", d.get("ariaHasPopup") == "dialog", d.get("ariaHasPopup"), "dialog")
chk("1a", "打开前浮窗 DOM 不存在", d.get("popExistsBefore") is False, d.get("popExistsBefore"), False)
chk("1a", "打开前 <html> 无标记", d.get("htmlFlagBefore") is False, d.get("htmlFlagBefore"), False)

print("=" * 108)
print("1b. 点击 → 打开（class / 标记 / aria / 位置 / 尺寸）")
d = g("1b")
chk("1b", "popover + td-dp 类名", "giencoder-popover" in (d.get("cls") or "") and "td-dp" in (d.get("cls") or ""), d.get("cls"), "含 giencoder-popover / td-dp")
chk("1b", "DS 展开态 .giencoder-popup-open", d.get("hasOpen") is True, d.get("hasOpen"), True)
chk("1b", "面板 320x480", near(d.get("rect", [0,0,0,0])[2], 320) and near(d.get("rect", [0,0,0,0])[3], 480), d.get("rect"), "[*,*,320,480]")
chk("1b", "opacity=1", d.get("opacity") == "1", d.get("opacity"), "1")
chk("1b", "visibility=visible", d.get("visibility") == "visible", d.get("visibility"), "visible")
chk("1b", "z-index=1000(--z-index-popup)", d.get("zIndex") == "1000", d.get("zIndex"), "1000")
chk("1b", "渲染到 body（契约 popupContainer）", d.get("parentTag") == "BODY", d.get("parentTag"), "BODY")
chk("1b", "水平左对齐触发按钮", near(d.get("leftOffset"), 0), d.get("leftOffset"), 0)
chk("1b", "与按钮间距 4px（DS 弹层约定）", near(d.get("topGap"), 4), d.get("topGap"), 4)
chk("1b", "<html> 标记 data-td-dp-open", d.get("htmlFlag") is True, d.get("htmlFlag"), True)
chk("1b", "aria-expanded=true", d.get("ariaExpanded") == "true", d.get("ariaExpanded"), "true")
chk("1b", "role=dialog", d.get("role") == "dialog", d.get("role"), "dialog")
chk("1b", "focus 落在浮层本身（不是输入框）", d.get("activeIsPop") is True, d.get("activeIsPop"), True)
chk("1b", "细滚动条 scrollbar-width=thin", d.get("scrollbarWidth") == "thin", d.get("scrollbarWidth"), "thin")

print("=" * 108)
print("1c. 内部结构契约（DS 类名 / role / 尺寸档 / 数量）")
d = g("1c")
chk("1c", "popover-title / -content / -footer", all([d.get("title"), d.get("content"), d.get("footer")]), [d.get("title"), d.get("content"), d.get("footer")], [True]*3)
chk("1c", "input-wrapper + data-size=medium", d.get("wrap") and d.get("wrapDataSize") == "medium", d.get("wrapDataSize"), "medium")
chk("1c", "input-prefix + input（占位「搜索成员」）", d.get("prefix") and d.get("input") and d.get("inputPlaceholder") == "搜索成员", d.get("inputPlaceholder"), "搜索成员")
chk("1c", "list role=listbox + giencoder-scroll-thin", d.get("list") and d.get("listRole") == "listbox" and "giencoder-scroll-thin" in (d.get("listCls") or ""), [d.get("listRole"), d.get("listCls")], "[listbox, 含 giencoder-scroll-thin]")
chk("1c", "主按钮 giencoder-btn-primary「确定转派」", "giencoder-btn-primary" in (d.get("okCls") or "") and d.get("okText") == "确定转派", [d.get("okCls"), d.get("okText")], "[含 -primary, 确定转派]")
chk("1c", "成员行 7 条", d.get("rowCount") == 7, d.get("rowCount"), 7)
chk("1c", "行 = list-item + hoverable", "giencoder-list-item" in (d.get("rowCls") or "") and "giencoder-list-item-hoverable" in (d.get("rowCls") or ""), d.get("rowCls"), "含 -item / -item-hoverable")
chk("1c", "行 role=option / data-size=small", d.get("rowRole") == "option" and d.get("rowSize") == "small", [d.get("rowRole"), d.get("rowSize")], "[option, small]")
chk("1c", "头像 = avatar + circle + text（单字）", all(k in (d.get("avatarCls") or "") for k in ("giencoder-avatar", "giencoder-avatar-circle", "giencoder-avatar-text")) and len(d.get("avatarText") or "") == 1, [d.get("avatarCls"), d.get("avatarText")], "[三件套, 1 字]")
chk("1c", "行内 -item-meta / -item-title / -item-action", all([d.get("metaCls"), d.get("titleCls"), d.get("actionCls")]), [d.get("metaCls"), d.get("titleCls"), d.get("actionCls")], [True]*3)
chk("1c", "对勾用 svg（不是字母）", d.get("checkSvgCount") == 1, d.get("checkSvgCount"), 1)

print("=" * 108)
print("1d. 几何真值（相对面板；设计稿实测）")
d = g("1d")
chk("1d", "标题内容盒（= 设计稿「容器 145」）相对面板 x16 y16 w288", near(d.get("titleContent", {}).get("x"), 16) and near(d.get("titleContent", {}).get("y"), 16) and near(d.get("titleContent", {}).get("w"), 288), d.get("titleContent"), "{x:16,y:16,w:288}")
chk("1d", "面板精确尺寸 320.00 / 480（±1 亚像素）", near((d.get("panelRaw") or [0, 0])[0], 320, 0.01) and near((d.get("panelRaw") or [0, 0])[1], 480, 1.0), d.get("panelRaw"), "[320, 480]")
chk("1d", "副标题 x16 y42 h16", near(d.get("sub", {}).get("x"), 16) and near(d.get("sub", {}).get("y"), 42) and near(d.get("sub", {}).get("h"), 16), d.get("sub"), "{x:16,y:42,h:16}")
chk("1d", "搜索框 x16 y70 288x32", near(d.get("search", {}).get("x"), 16) and near(d.get("search", {}).get("y"), 70) and near(d.get("search", {}).get("w"), 288) and near(d.get("search", {}).get("h"), 32), d.get("search"), "{x:16,y:70,w:288,h:32}")
chk("1d", "放大镜 14x14 起 x27 y79", near(d.get("prefix", {}).get("x"), 27) and near(d.get("prefix", {}).get("y"), 79) and near(d.get("prefix", {}).get("w"), 14), d.get("prefix"), "{x:27,y:79,w:14}")
chk("1d", "输入框文字起 x52（设计稿 ink x53）", near(d.get("input", {}).get("x"), 52), d.get("input"), "{x:52}")
chk("1d", "列表 x16 y118 288x297", near(d.get("list", {}).get("x"), 16) and near(d.get("list", {}).get("y"), 118) and near(d.get("list", {}).get("w"), 288) and near(d.get("list", {}).get("h"), 297), d.get("list"), "{x:16,y:118,w:288,h:297}")
chk("1d", "第1行 y118 32 高", near(d.get("row0", {}).get("y"), 118) and near(d.get("row0", {}).get("h"), 32), d.get("row0"), "{y:118,h:32}")
chk("1d", "行 pitch 34（32 + 2 间距）", near(d.get("pitch"), 34), d.get("pitch"), 34)
chk("1d", "第2行 y152 / 第3行 y186", near(d.get("row1", {}).get("y"), 152) and near(d.get("row2", {}).get("y"), 186), [d.get("row1", {}).get("y"), d.get("row2", {}).get("y")], [152, 186])
chk("1d", "头像 x24 y124 20x20", near(d.get("avatar", {}).get("x"), 24) and near(d.get("avatar", {}).get("y"), 124) and near(d.get("avatar", {}).get("w"), 20), d.get("avatar"), "{x:24,y:124,w:20}")
chk("1d", "名字起 x52（头像右 8）", near(d.get("name", {}).get("x"), 52), d.get("name"), "{x:52}")
chk("1d", "对勾 x282 y124 14x14", near(d.get("check0", {}).get("x"), 282) and near(d.get("check0", {}).get("w"), 14), d.get("check0"), "{x:282,w:14}")
chk("1d", "底栏 y415 h64（1px 分隔线 + 16/15 内距 + 32 按钮）", near(d.get("footer", {}).get("y"), 415) and near(d.get("footer", {}).get("h"), 64), d.get("footer"), "{y:415,h:64}")
chk("1d", "按钮 x16 y432 288x32", near(d.get("ok", {}).get("x"), 16) and near(d.get("ok", {}).get("y"), 432) and near(d.get("ok", {}).get("w"), 288) and near(d.get("ok", {}).get("h"), 32), d.get("ok"), "{x:16,y:432,w:288,h:32}")
chk("1d", "按钮底距面板底 16（设计稿 y464→480）", near((d.get("panelRaw") or [0, 0])[1] - (d.get("ok", {}).get("y", 0) + d.get("ok", {}).get("h", 0)), 16), [(d.get("panelRaw") or [0, 0])[1], d.get("ok", {}).get("y", 0) + d.get("ok", {}).get("h", 0)], "差 16")
chk("1d", "7 行内容 236（7×32 + 6×2）+ 视口 297 不溢出（scrollHeight 恒 ≥ clientHeight）", near(d.get("rowContentH"), 236) and near(d.get("listScrollH"), 297) and near(d.get("listClientH"), 297), [d.get("rowContentH"), d.get("listScrollH"), d.get("listClientH")], [236, 297, 297])

print("=" * 108)
print("1e. 配色 / 字号 / 圆角 / 投影真值")
d = g("1e")
for name, key, want in [
    ("面板底 #FFFFFF", "panelBg", "rgb(255, 255, 255)"),
    ("面板边框 #E5E5E5", "panelBorder", "rgb(229, 229, 229)"),
    ("副标题/占位/工号 #868686", "subColor", "rgb(134, 134, 134)"),
    ("放大镜 #6B6B6B", "prefixColor", "rgb(107, 107, 107)"),
    ("搜索框边框 #E5E5E5", "searchBorder", "rgb(229, 229, 229)"),
    ("名字 #1F1F1F(text-1)", "nameColor", "rgb(31, 31, 31)"),
    ("工号 text-3", "idColor", "rgb(134, 134, 134)"),
    ("对勾 primary-6", "checkColor", "rgb(55, 112, 247)"),
    ("按钮底 primary-6", "okBg", "rgb(55, 112, 247)"),
    ("选中行底 #ECF2FF", "selBg", "rgb(236, 242, 255)"),
]:
    got = d.get(key)
    chk("1e", name, rgbv(got) == want, got, want)
chk("1e", "面板圆角 6px", d.get("panelRadius") == "6px", d.get("panelRadius"), "6px")
chk("1e", "搜索框圆角 6px", d.get("searchRadius") == "6px", d.get("searchRadius"), "6px")
chk("1e", "行圆角 6px", d.get("rowRadius") == "6px", d.get("rowRadius"), "6px")
chk("1e", "按钮圆角 6px", d.get("okRadius") == "6px", d.get("okRadius"), "6px")
chk("1e", "头像圆角 50%", d.get("avRadius") == "50%", d.get("avRadius"), "50%")
chk("1e", "投影 = shadow2-down(0 4px 10px rgba(0,0,0,.1))", "0px 4px 10px" in (d.get("panelShadow") or "") and "0.1" in (d.get("panelShadow") or ""), d.get("panelShadow"), "含 0px 4px 10px / 0.1")
chk("1e", "标题 14px/lh22/400", d.get("titleFs") == "14px" and d.get("titleLh") == "22px" and d.get("titleWeight") == "400", [d.get("titleFs"), d.get("titleLh"), d.get("titleWeight")], ["14px", "22px", "400"])
chk("1e", "标题 #1F1F1F", rgbv(d.get("titleColor")) == "rgb(31, 31, 31)", d.get("titleColor"), "rgb(31, 31, 31)")
chk("1e", "副标题 12px/lh16", d.get("subFs") == "12px" and d.get("subLh") == "16px", [d.get("subFs"), d.get("subLh")], ["12px", "16px"])
chk("1e", "搜索框高 32", d.get("searchH") == "32px", d.get("searchH"), "32px")
chk("1e", "占位/输入 14px", d.get("inputFs") == "14px", d.get("inputFs"), "14px")
chk("1e", "行高 32 / 内距 8", d.get("rowH") == "32px" and d.get("rowPadding") == "8px", [d.get("rowH"), d.get("rowPadding")], ["32px", "8px"])
chk("1e", "名字 14px", d.get("nameFs") == "14px", d.get("nameFs"), "14px")
chk("1e", "头像 20x20 / 白字 11px", d.get("avW") == "20px" and d.get("avH") == "20px" and d.get("avFs") == "11px", [d.get("avW"), d.get("avH"), d.get("avFs")], ["20px", "20px", "11px"])
chk("1e", "头像白字色", rgbv(d.get("avColor")) == "rgb(255, 255, 255)", d.get("avColor"), "rgb(255, 255, 255)")
chk("1e", "头像底色走 --avatar-bg-2(#E88B4D)", rgbv(d.get("avBg")) == "rgb(232, 139, 77)", d.get("avBg"), "rgb(232, 139, 77)")
chk("1e", "选中行描边 inset 1px #D3E2FF", "inset" in (d.get("selRing") or "") and "rgb(211, 226, 255)" in (d.get("selRing") or ""), d.get("selRing"), "含 inset / rgb(211, 226, 255)")
chk("1e", "对勾可见（flex item 块化 → 写 flex）", d.get("checkDisplay") in ("flex", "inline-flex"), d.get("checkDisplay"), "flex")
chk("1e", "分隔线 1px #F2F2F2(border-1)", d.get("footBorderW") == "1px" and rgbv(d.get("footBorderTop")) == "rgb(242, 242, 242)", [d.get("footBorderW"), d.get("footBorderTop")], ["1px", "rgb(242, 242, 242)"])
chk("1e", "底栏按钮 14px", d.get("okFs") == "14px", d.get("okFs"), "14px")
chk("1e", "列表可滚动 overflow-y=auto", d.get("listOverflowY") == "auto", d.get("listOverflowY"), "auto")

print("=" * 108)
print("1f. 默认选中 + 唯一对勾")
d = g("1f")
chk("1f", "唯一选中行", d.get("selectedCount") == 1, d.get("selectedCount"), 1)
chk("1f", "默认选中 邵禹铭 (P0098602)", "邵禹铭" in (d.get("selectedName") or "") and "P0098602" in (d.get("selectedName") or ""), d.get("selectedName"), "含 邵禹铭/P0098602")
chk("1f", "可见对勾 1 个", d.get("checkVisibleCount") == 1, d.get("checkVisibleCount"), 1)

print("=" * 108)
print("1g. 真实 hover 行底色")
d = g("1g")
chk("1g", "hover 到 顾帆 行", "顾帆" in (d.get("hoveredText") or ""), d.get("hoveredText"), "含 顾帆")
chk("1g", "hover 底 #F7F7F7(fill-1)", rgbv(d.get("bg")) == "rgb(247, 247, 247)", d.get("bg"), "rgb(247, 247, 247)")
chk("1g", "cursor=pointer", d.get("cursor") == "pointer", d.get("cursor"), "pointer")
chk("1g", "hover 不影响选中行底", rgbv(d.get("selBgUnchanged")) == "rgb(236, 242, 255)", d.get("selBgUnchanged"), "rgb(236, 242, 255)")

print("=" * 108)
print("1h. 点击行 → 选中转移")
d = g("1h")
chk("1h", "唯一选中 = 秦怡", d.get("selectedCount") == 1 and "秦怡" in (d.get("selectedName") or ""), d.get("selectedName"), "含 秦怡")
chk("1h", "row0 取消选中 / row1 选中", d.get("row0Sel") == "false" and d.get("row1Sel") == "true", [d.get("row0Sel"), d.get("row1Sel")], ["false", "true"])
chk("1h", "新选中行底 #ECF2FF", rgbv(d.get("row1Bg")) == "rgb(236, 242, 255)", d.get("row1Bg"), "rgb(236, 242, 255)")
chk("1h", "旧选中行恢复透明底", is_clear(d.get("row0Bg")) or rgbv(d.get("row0Bg")) == "rgb(255, 255, 255)", d.get("row0Bg"), "透明/白")
chk("1h", "对勾跟随（row1 可见 / row0 隐藏）", d.get("check1") in ("flex", "inline-flex") and d.get("check0") == "none", [d.get("check0"), d.get("check1")], ["none", "flex"])
chk("1h", "浮窗内操作未触发两栏拖动", d.get("dragging") is False, d.get("dragging"), False)

print("=" * 108)
print("1i. 搜索过滤 + 空态")
d = g("1i_han")
chk("1i", "搜「韩」命中 1 行", d.get("visCount") == 1 and "韩佳毅" in (d.get("visText") or [""])[0], [d.get("visCount"), d.get("visText")], [1, "含 韩佳毅"])
d = g("1i_id")
chk("1i", "搜「P00986」命中 7 行", d.get("visCount") == 7, d.get("visCount"), 7)
d = g("1i_none")
chk("1i", "搜「zzz」0 行 + 显示空态", d.get("visCount") == 0 and d.get("noneHidden") is False, [d.get("visCount"), d.get("noneHidden")], [0, False])
chk("1i", "空态用 DS Empty（12px text-3）", "未找到匹配成员" in (d.get("noneText") or "") and d.get("noneFs") == "12px" and rgbv(d.get("noneColor")) == "rgb(134, 134, 134)", [d.get("noneText"), d.get("noneFs"), d.get("noneColor")], ["未找到匹配成员", "12px", "rgb(134, 134, 134)"])
d = g("1i_reset")
chk("1i", "清空后恢复 7 行 / 空态隐藏", d.get("visCount") == 7 and d.get("noneHidden") is True, [d.get("visCount"), d.get("noneHidden")], [7, True])

print("=" * 108)
print("1j. 确定转派 → 关闭 + 执行人写回 + DS Message")
d = g("1j")
chk("1j", "浮窗已关闭", d.get("popOpen") is False and d.get("visibility") == "hidden", [d.get("popOpen"), d.get("visibility")], [False, "hidden"])
chk("1j", "标记/aria 复位", d.get("htmlFlag") is False and d.get("ariaExpanded") == "false", [d.get("htmlFlag"), d.get("ariaExpanded")], [False, "false"])
chk("1j", "aside 执行人写回为选中项", d.get("assignee") == "秦怡", d.get("assignee"), "秦怡")
chk("1j", "DS Message 出现（role=status）", d.get("msgExists") and d.get("msgRole") == "status" and "giencoder-message" in (d.get("msgCls") or ""), [d.get("msgExists"), d.get("msgRole"), d.get("msgCls")], "[True, status, 含 giencoder-message]")
chk("1j", "提示文案含成员名", "秦怡" in (d.get("msgText") or ""), d.get("msgText"), "含 秦怡")
_c = rgbs(d.get("msgIconColor")) or (0, 0, 0)
chk("1j", "提示图标语义色（success 绿）", _c[1] > _c[0] and _c[1] > _c[2], d.get("msgIconColor"), "绿色系")

print("=" * 108)
print("1k/1l. 关闭途径：点外部 / Esc（含输入框内 Esc）")
d = g("1k_open")
chk("1k", "重开成功且选中国保持", d.get("openAfterReopen") is True and any("秦怡" in s for s in (d.get("selectedStill") or [])), [d.get("openAfterReopen"), d.get("selectedStill")], [True, "含 秦怡"])
d = g("1k")
chk("1k", "点浮窗外 → 关闭", d.get("openAfterOutside") is False and d.get("htmlFlag") is False, [d.get("openAfterOutside"), d.get("htmlFlag")], [False, False])
chk("1k", "未跳页", d.get("url") == "task-detail.html", d.get("url"), "task-detail.html")
d = g("1l")
chk("1l", "Esc → 只关浮窗", d.get("openAfterEsc") is False and d.get("htmlFlag") is False, [d.get("openAfterEsc"), d.get("htmlFlag")], [False, False])
chk("1l", "Esc 未跳看板", d.get("url") == "task-detail.html", d.get("url"), "task-detail.html")
d2 = g("1l2_focus")
chk("1l2", "焦点在搜索框内", d2.get("activeIsInput") is True, d2.get("activeIsInput"), True)
d = g("1l2")
chk("1l2", "输入框内 Esc 同样关闭（未被 INPUT 判定吞掉）", d.get("openAfterEscInInput") is False, d.get("openAfterEscInInput"), False)

print("=" * 108)
print("1m/1n. 浮窗内拖动不夺权 + 滚动条")
d = g("1m_drag")
chk("1m", "拖动中无 is-xdrag", d.get("isXdrag") is False, d.get("isXdrag"), False)
chk("1m", "拖动中无 is-swapped", d.get("isSwapped") is False, d.get("isSwapped"), False)
chk("1m", "左栏未位移（仍在 8）", near((d.get("leftRect") or [0])[0], 8), (d.get("leftRect") or [None])[0], 8)
d = g("1m")
chk("1m", "松手后仍未互换 + 浮窗保持打开", d.get("afterUp_isSwapped") is False and d.get("openStill") is True, [d.get("afterUp_isSwapped"), d.get("openStill")], [False, True])
d = g("1n")
chk("1n", "list overflow-y=auto 且无横向溢出", d.get("overflowY") == "auto" and d.get("scrollWidth") == d.get("clientWidth"), [d.get("overflowY"), d.get("scrollWidth"), d.get("clientWidth")], "[auto, 相等]")
_rules = " ".join(d.get("thumbRules") or [])
chk("1n", "细滚动条规则已定义（--scrollbar-size 6px + scrollbar-thumb）", d.get("scrollbarSize") == "6px" and "scrollbar-thumb" in _rules and "var(--scrollbar-size)" in _rules, [d.get("scrollbarSize"), _rules[:70]], "6px / 含 scrollbar-thumb")
chk("1n", "滑块色 rgba(0,0,0,.16) 叠白 = #D6D6D6（设计稿实测）", "0.16" in (d.get("thumbVar") or ""), d.get("thumbVar"), "含 0.16")

print("=" * 108)
print("回归（第 28/29/30 轮）")
d = g("R1")
chk("R1", "左栏 [8,48,936,844]", d.get("left") == [8, 48, 936, 844], d.get("left"), [8, 48, 936, 844])
chk("R1", "右栏 x952 w480", near((d.get("right") or [0])[0], 952) and near((d.get("right") or [0])[2], 480), d.get("right"), "[952,48,480,844]")
chk("R1", "间隙 8", near((d.get("gutter") or [0])[2], 8), d.get("gutter"), "w=8")
chk("R1", "标题栏 48 高", near((d.get("bar") or [0])[3], 48), d.get("bar"), "h=48")
chk("R1", "标题区底色 fill-1", rgbv(d.get("titleBg")) == "rgb(247, 247, 247)", d.get("titleBg"), "rgb(247, 247, 247)")
d = g("R2")
chk("R2", "图片预览层 1440x900 / z1000 / opacity1", d.get("exists") and near((d.get("rect") or [0,0,0,0])[2], 1440) and d.get("z") == "1000" and d.get("opacity") == "1", [d.get("rect"), d.get("z"), d.get("opacity")], "[1440x900, 1000, 1]")
chk("R2", "大图 1240x620", near((d.get("imgRect") or [0,0,0,0])[2], 1240) and near((d.get("imgRect") or [0,0,0,0])[3], 620), d.get("imgRect"), "[*,*,1240,620]")
d = g("R2b")
chk("R2", "Esc 关预览且未跳页", d.get("previewOpen") is False and d.get("url") == "task-detail.html", [d.get("previewOpen"), d.get("url")], [False, "task-detail.html"])
d = g("R3_mid")
chk("R3", "拖动进入 is-xdrag / is-xarmed", (d.get("isXdrag") or d.get("isArmed")) is True, [d.get("isXdrag"), d.get("isArmed")], "至少一个 True")
d = g("R3")
chk("R3", "松手后互换（row-reverse）", d.get("isSwapped") is True, d.get("isSwapped"), True)
chk("R3", "换位后左栏 x=496 / 右栏 x=8（宽度不变）", near((d.get("left") or [0])[0], 496) and near((d.get("right") or [0])[0], 8) and near((d.get("left") or [0,0,0])[2], 936), [d.get("left"), d.get("right")], "[x496 w936, x8]")
d = g("R4")
chk("R4", "全屏态 + 内容列 860", d.get("fs") is True and near((d.get("rect") or [0,0,0,0])[2], 860), [d.get("fs"), d.get("rect")], "[True, w=860]")
d = g("R5")
for k in ("attr", "tl1", "tlTime"):
    v = d.get(k) or []
    chk("R5", "%s 字号唯一值 = 13px" % k, v == ["13px"], v, ["13px"])
d = g("R6")
chk("R6", "第二次 Esc 返回看板", d.get("url") == "kanban.html", d.get("url"), "kanban.html")

print("=" * 108)
print("总断言 %d 项：PASS %d / FAIL %d" % (len(OK) + len(BAD), len(OK), len(BAD)))
if BAD:
    print("失败明细：")
    for s, n, got, want in BAD:
        print("  [%s] %s  got=%s want=%s" % (s, n, got, want))
    print("RESULT: HAS_FAIL")
    sys.exit(1)
print("RESULT: ALL_OK")

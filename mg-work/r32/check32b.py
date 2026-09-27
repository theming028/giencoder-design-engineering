# -*- coding: utf-8 -*-
"""第32轮第 5 项断言器：读 mg-work/r32/probe32b.jsonl。
真值来源：mg-work/r32/design/coop.png（1440×900 1x；量取见 measure3/4/5.py + compare.py）。
面板 left=400 / top=130（1440×900 居中）→ 断言前统一换算成「相对面板」坐标。
"""
import io
import json
import re
import sys

PROBE = "mg-work/r32/probe32b.jsonl"
PAGE = "pages/task-detail.html"

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
    print("  %s %-6s %-46s got=%s  want=%s" % ("✓" if cond else "✗ FAIL", step, name, got, want))


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


def rel(rect, ox=400, oy=130):
    """视口坐标 → 相对面板左上角"""
    if not rect:
        return None
    return [rect[0] - ox, rect[1] - oy, rect[2], rect[3]]


def eqr(rect, want, tol=0.5):
    r = rel(rect) if rect else None
    if not r or len(r) != 4:
        return False
    return all(near(r[i], want[i], tol) for i in range(4))


# ---------- 5a 初始 ----------
print("=" * 118)
print("5a. 初始态：弹窗存在但未打开")
d = g("5a_init")
chk("5a", "顶栏有 [data-td-coop] 按钮", d.get("btn") is True, d.get("btn"), True)
chk("5a", ".td-coop 根节点存在", d.get("root") is True, d.get("root"), True)
chk("5a", "初始 hidden（不占屏幕）", d.get("hidden") is True and d.get("open") is False, [d.get("hidden"), d.get("open")], [True, False])
chk("5a", "初始 aria-expanded=false", d.get("aria") == "false", d.get("aria"), "false")
chk("5a", "初始 <html data-td-coop-open> 不存在", d.get("flag") is False, d.get("flag"), False)

# ---------- 5b 打开：遮罩 + 面板 ----------
print("=" * 118)
print("5b. 点「协作」→ 打开（遮罩 + 面板 640×640 / r16 / shadow3）")
d = g("5b")
chk("5b", "已打开（is-open + 非 hidden）", d.get("open") is True, d.get("open"), True)
chk("5b", "写入 <html data-td-coop-open>", d.get("flag") is True, d.get("flag"), True)
chk("5b", "按钮 aria-expanded=true", d.get("aria") == "true", d.get("aria"), "true")
chk("5b", "★ 面板 640×640 @(400,130)", d.get("panel") == [400, 130, 640, 640], d.get("panel"), [400, 130, 640, 640])
chk("5b", "★ 面板圆角 16px（设计稿 r16）", d.get("radius") == "16px", d.get("radius"), "16px")
chk("5b", "面板底 rgba(255,255,255,.95)", d.get("bg") == "rgba(255, 255, 255, 0.95)", d.get("bg"), "rgba(255, 255, 255, 0.95)")
chk("5b", "★ 面板投影 = --shadow3-down（与 Select 弹层一致）", "0px 8px 20px" in (d.get("shadow") or "") and "0.1" in (d.get("shadow") or ""), d.get("shadow"), "0 8px 20px rgba(0,0,0,.1)")
chk("5b", "开合动画结束（transform 归位 none）", d.get("transform") == "none", d.get("transform"), "none")
chk("5b", "遮罩铺满视口 1440×900", d.get("maskR") == [0, 0, 1440, 900], d.get("maskR"), [0, 0, 1440, 900])
chk("5b", "★ 遮罩色 rgba(0,0,0,.4)", d.get("maskBg") == "rgba(0, 0, 0, 0.4)", d.get("maskBg"), "rgba(0, 0, 0, 0.4)")
chk("5b", "★ 遮罩 backdrop blur(10px)", "blur(10px)" in (d.get("maskBlur") or ""), d.get("maskBlur"), "含 blur(10px)")
chk("5b", "遮罩淡入完成（opacity=1）", d.get("maskOpacity") == "1", d.get("maskOpacity"), "1")
chk("5b", "wrapper 走 DS 结构 class", d.get("wrapper") == [0, 0, 1440, 900], d.get("wrapper"), "[0,0,1440,900]")
chk("5b", "★ 契约语义 role=dialog / aria-modal=true", d.get("dialogRole") == "dialog" and d.get("ariaModal") == "true", [d.get("dialogRole"), d.get("ariaModal")], ["dialog", "true"])

# ---------- 5c 纵向节奏 ----------
print("=" * 118)
print("5c. 纵向节奏：header 46 + 18 + steps 32 + 19 + divider 24 + 11 + content 410 + footer 80 = 640")
d = g("5c")
chk("5c", "header 640×46", eqr(d.get("header"), [0, 0, 640, 46]), rel(d.get("header")), [0, 0, 640, 46])
chk("5c", "header 内距 18px 24px 0（无分隔线，与设计稿一致）", d.get("headerPad") == "18px 24px 0px" and d.get("headerBorder") == "0px", [d.get("headerPad"), d.get("headerBorder")], "18px 24px 0px / 0px")
chk("5c", "标题 16px/600 @(24,18)", near(rel(d.get("title"))[0], 24) and near(rel(d.get("title"))[1], 18) and d.get("titleFs") == "16px" and d.get("titleFw") == "600", [rel(d.get("title")), d.get("titleFs"), d.get("titleFw")], "(24,18) 16px/600")
chk("5c", "关闭 X 28×28 @(588,18)（右内距 24）", eqr(d.get("close"), [588, 18, 28, 28]), rel(d.get("close")), [588, 18, 28, 28])
chk("5c", "★ 步骤条 592×32 @(24,64)", eqr(d.get("steps"), [24, 64, 592, 32]), rel(d.get("steps")), [24, 64, 592, 32])
chk("5c", "步骤条外边距 18px 24px 0", d.get("stepsMargin") == "18px 24px 0px", d.get("stepsMargin"), "18px 24px 0px")
chk("5c", "两段（steps-item）", d.get("stepCount") == 2, d.get("stepCount"), 2)
chk("5c", "★ 两段各 296×32（首尾相接合计 592，无重叠）", d.get("stepRects") == [[424, 194, 296, 32], [720, 194, 296, 32]], d.get("stepRects"), "各自 296×32")
chk("5c", "当前段底 #ECF2FF + 1px #D3E2FF，字 primary-6", d.get("step0Bg") == "rgb(236, 242, 255)" and d.get("step0Border") == "rgb(211, 226, 255) / 1px" and d.get("step0Color") == "rgb(55, 112, 247)", [d.get("step0Bg"), d.get("step0Border"), d.get("step0Color")], ["rgb(236, 242, 255)", "rgb(211, 226, 255) / 1px", "rgb(55, 112, 247)"])
chk("5c", "未开始段底 fill-2 + 字 text-2", d.get("step1Bg") == "rgb(242, 242, 242)" and d.get("step1Color") == "rgb(78, 78, 78)", [d.get("step1Bg"), d.get("step1Color")], ["rgb(242, 242, 242)", "rgb(78, 78, 78)"])
chk("5c", "★ 衔接处 = 向右箭头：段1 右凸尖 7px + 段2 左凹口 5px（第33轮第2项改版，原对称咬合 6px 已废弃）",
    ("calc(100% - 7px) 0px" in (d.get("step0After") or "") and "100% 50%" in (d.get("step0After") or "")
     and "5px 50%" in (d.get("step1Clip") or "") and "100% 50%" not in (d.get("step1Clip") or "")),
    [d.get("step0After"), d.get("step1Clip")], "段1 …calc(100% - 7px) 0px, 100% 50%… / 段2 …5px 50%")
chk("5c", "段1 为当前态（is-active + aria-current=step），无对勾", d.get("step0Active") is True and d.get("step0Current") == "step" and d.get("step0Icon") == "none", [d.get("step0Active"), d.get("step0Current"), d.get("step0Icon")], [True, "step", "none"])
chk("5c", "段2 未开始（无 is-active / 无对勾）", d.get("step1Icon") == "none", d.get("step1Icon"), "none")
chk("5c", "★ 分割线行 592×24 @(24,115)（线心 y126）", eqr(d.get("dvd"), [24, 115, 592, 24]), rel(d.get("dvd")), [24, 115, 592, 24])
chk("5c", "说明文字 14px text-3，文案 Step1", d.get("dvdTextFs") == "14px" and d.get("dvdTextColor") == "rgb(134, 134, 134)" and d.get("dvdTx") == "选择需要流转到下一阶段的协作产物", [d.get("dvdTextFs"), d.get("dvdTextColor"), d.get("dvdTx")], "14px / gray-6 / Step1 文案")
chk("5c", "说明文字水平居中（镜像留白）", near(rel(d.get("dvdText"))[0], 208, 2), rel(d.get("dvdText")), "[208,*,224,*]")
chk("5c", "★ 内容区 592×410 @(24,150)", eqr(d.get("content"), [24, 150, 592, 410]), rel(d.get("content")), [24, 150, 592, 410])
chk("5c", "内容区 内距 15 / 1px border / r6 / 纯白底", d.get("contentPad") == "15px" and d.get("contentBorder") == "1px" and d.get("contentRadius") == "6px" and d.get("contentBg") == "rgb(255, 255, 255)", [d.get("contentPad"), d.get("contentBorder"), d.get("contentRadius"), d.get("contentBg")], "15px / 1px / 6px / rgb(255,255,255)")
chk("5c", "内容区不出现内部滚动（Step1 8 行全展示）", d.get("contentScrollH") == d.get("contentClientH"), [d.get("contentScrollH"), d.get("contentClientH")], "两者相等")
chk("5c", "底栏 640×80 @(0,560)（内距 24、无上分隔线）", eqr(d.get("footer"), [0, 560, 640, 80]) and d.get("footerPad") == "24px" and d.get("footerBorder") == "0px", [rel(d.get("footer")), d.get("footerPad"), d.get("footerBorder")], "[0,560,640,80] / 24px / 0px")
chk("5c", "计数文字 14px text-3 @(24,589)", near(rel(d.get("count"))[0], 24) and near(rel(d.get("count"))[1], 589) and d.get("countFs") == "14px" and d.get("countColor") == "rgb(134, 134, 134)", [rel(d.get("count")), d.get("countFs"), d.get("countColor")], "(24,589) 14px / gray-6")
chk("5c", "计数文案 = 已选 8/8 个产物", d.get("countText") == "已选 8/8 个产物", d.get("countText"), "已选 8/8 个产物")

# ---------- 5d Step1 行 ----------
print("=" * 118)
print("5d. Step1 产物行：560×32 / pitch 34 / 勾选框 14×14 @(48,175)")
d = g("5d")
chk("5d", "8 个产物行", d.get("rowCount") == 8, d.get("rowCount"), 8)
chk("5d", "★ 行 560×32 @(40,166)，pitch=34", eqr(d.get("row0"), [40, 166, 560, 32]) and d.get("pitch") == 34, [rel(d.get("row0")), d.get("pitch")], "[40,166,560,32] / 34")
chk("5d", "行 内距 0 8px / gap 16px / r6", d.get("rowPad") == "0px 8px" and d.get("rowGap") == "16px" and d.get("rowRadius") == "6px", [d.get("rowPad"), d.get("rowGap"), d.get("rowRadius")], "0px 8px / 16px / 6px")
chk("5d", "★ 勾选框 14×14 @(48,175)", eqr(d.get("cb"), [48, 175, 14, 14]), rel(d.get("cb")), [48, 175, 14, 14])
chk("5d", "勾选框 2px 边 + r2 + 选中填充 primary-6", d.get("cbBorder") == "2px / rgb(55, 112, 247)" and d.get("cbRadius") == "2px" and d.get("cbBg") == "rgb(55, 112, 247)", [d.get("cbBorder"), d.get("cbRadius"), d.get("cbBg")], "2px/primary-6, r2, 填充 primary-6")
chk("5d", "★ 文件名 14px @x68", near(rel(d.get("tx"))[0], 68) and d.get("txFs") == "14px", [rel(d.get("tx")), d.get("txFs")], "x68 / 14px")
chk("5d", "产物默认全选（8/8）", d.get("checked") is True and d.get("checked0") == 8, [d.get("checked"), d.get("checked0")], [True, 8])

# ---------- 5e 计数实时 ----------
print("=" * 118)
print("5e. 取消 1 个产物 → 计数实时更新（change 冒泡）")
d = g("5e")
chk("5e", "取消后 7/8", d.get("checked1") == 7, d.get("checked1"), 7)
chk("5e", "计数文案同步为「已选 7/8 个产物」", d.get("count") == "已选 7/8 个产物", d.get("count"), "已选 7/8 个产物")
d = g("5e_back")
chk("5e", "重新勾回 → 8/8", d.get("checked1") == 8 and d.get("count") == "已选 8/8 个产物", [d.get("checked1"), d.get("count")], [8, "已选 8/8 个产物"])

# ---------- 5f Step2 ----------
print("=" * 118)
print("5f. 下一步 → Step2（搜索框 + 7 成员行 + 底栏按钮切换 + 文案切换）")
d = g("5f")
chk("5f", "面板切换到 pane2", d.get("pane1Hidden") is True and d.get("pane2Hidden") is False, [d.get("pane1Hidden"), d.get("pane2Hidden")], [True, False])
chk("5f", "段1 → 已完成（is-finish，收起 is-active，显示对勾）", d.get("step0Finish") is True and d.get("step0Active") is False and d.get("step0Icon") != "none", [d.get("step0Finish"), d.get("step0Active"), d.get("step0Icon")], [True, False, "非 none"])
chk("5f", "段2 → 当前态（is-active + aria-current=step）", d.get("step1Active") is True and d.get("step1Current") == "step", [d.get("step1Active"), d.get("step1Current")], [True, "step"])
chk("5f", "分割线文案切到 Step2", d.get("hint") == "将当前任务 (含产物) 流转给下一位协作者", d.get("hint"), "Step2 文案")
chk("5f", "计数切到「已选 0/7 位协作者」", d.get("count") == "已选 0/7 位协作者", d.get("count"), "已选 0/7 位协作者")
chk("5f", "底栏按钮切换：下一步隐藏 / 上一步+提交显示", d.get("nextHidden") is True and d.get("prevHidden") is False and d.get("submitHidden") is False, [d.get("nextHidden"), d.get("prevHidden"), d.get("submitHidden")], [True, False, False])
chk("5f", "★ Step2 底栏：取消 60 @(406,584) / 上一步 74 @(474,584) / 提交 60 @(556,584)", eqr(d.get("cancel"), [406, 584, 60, 32]) and eqr(d.get("prev"), [474, 584, 74, 32]) and eqr(d.get("submit"), [556, 584, 60, 32]), [rel(d.get("cancel")), rel(d.get("prev")), rel(d.get("submit"))], "[406,584,60,32] / [474,584,74,32] / [556,584,60,32]")
chk("5f", "★ 搜索框 560×32 @(40,166)，内距 0 12 0 10，1px #E5E5E5，r4", eqr(d.get("iwBox"), [40, 166, 560, 32]) and d.get("iwPad") == "0px 12px 0px 10px" and d.get("iwBorder") == "1px / rgb(229, 229, 229)" and d.get("iwRadius") == "4px", [rel(d.get("iwBox")), d.get("iwPad"), d.get("iwBorder"), d.get("iwRadius")], "[40,166,560,32] / 0 12 0 10 / 1px #E5E5E5 / 4px")
chk("5f", "放大镜 14×14 @(51,175)（左内距 10）", eqr(d.get("prefix"), [51, 175, 14, 14]), rel(d.get("prefix")), "[51,175,14,14]")
chk("5f", "占位文案「搜索协作者」，输入 14px", d.get("inpPh") == "搜索协作者" and d.get("inpFs") == "14px", [d.get("inpPh"), d.get("inpFs")], ["搜索协作者", "14px"])
chk("5f", "7 位协作者", d.get("rowCount") == 7 and d.get("visRows") == 7, [d.get("rowCount"), d.get("visRows")], [7, 7])
chk("5f", "★ 成员行 560×32 @(40,214)，pitch=34", eqr(d.get("row0"), [40, 214, 560, 32]) and d.get("rowPitch") == 34, [rel(d.get("row0")), d.get("rowPitch")], "[40,214,560,32] / 34")
chk("5f", "★ 头像 20×20 圆形 @(78,220)（勾选框→16px→头像）", eqr(d.get("av"), [78, 220, 20, 20]) and d.get("avRadius") == "50%", [rel(d.get("av")), d.get("avRadius")], "[78,220,20,20] / 50%")
chk("5f", "头像用 DS --avatar-bg-1（#E57470）", d.get("avBg") == "rgb(229, 116, 112)", d.get("avBg"), "rgb(229, 116, 112)")
chk("5f", "★ 姓名 14px @x106（头像→8px→姓名）", near(rel(d.get("nm"))[0], 106, 1.5) and d.get("nmFs") == "14px", [rel(d.get("nm")), d.get("nmFs")], "x106 / 14px")
chk("5f", "成员行勾选框与 Step1 同位（14×14 @x48）", eqr(d.get("cbR"), [48, 223, 14, 14]), rel(d.get("cbR")), "[48,223,14,14]")

# ---------- 5g 搜索过滤 ----------
print("=" * 118)
print("5g. 搜索过滤（按姓名 / 工号，去空格小写匹配）")
chk("5g", "输入「邵」→ 仅 1 行", g("5g").get("visRows") == 1, g("5g").get("visRows"), 1)
chk("5g", "输入「P00986」→ 7 行（工号命中）", g("5g_multi").get("visRows") == 7, g("5g_multi").get("visRows"), 7)
chk("5g", "输入「zzzz」→ 0 行", g("5g_none").get("visRows") == 0, g("5g_none").get("visRows"), 0)
chk("5g", "清空 → 恢复 7 行", g("5g_reset").get("visRows") == 7, g("5g_reset").get("visRows"), 7)

# ---------- 5h/5i/5j ----------
print("=" * 118)
print("5h/5i/5j. 计数 / 上一步状态保留 / 点步骤条跳转")
d = g("5h")
chk("5h", "勾选 2 位 → 计数「已选 2/7 位协作者」", d.get("mChecked") == 2 and d.get("count") == "已选 2/7 位协作者", [d.get("mChecked"), d.get("count")], [2, "已选 2/7 位协作者"])
d = g("5i")
chk("5i", "上一步 → 回 Step1（pane1 显示、底栏回切）", d.get("pane1Hidden") is False and d.get("nextHidden") is False and d.get("prevHidden") is True and d.get("submitHidden") is True, [d.get("pane1Hidden"), d.get("nextHidden"), d.get("prevHidden"), d.get("submitHidden")], [False, False, True, True])
chk("5i", "回 Step1 后文案/计数同步（8/8 产物）", d.get("hint") == "选择需要流转到下一阶段的协作产物" and d.get("count") == "已选 8/8 个产物", [d.get("hint"), d.get("count")], "Step1 文案 / 8/8")
chk("5i", "未提交前不影响已选协作者（保留 2）", d.get("keepM") == 2, d.get("keepM"), 2)
d = g("5j")
chk("5j", "★ 点步骤条直接跳 Step2（steps.json clickable）", d.get("pane2Hidden") is False and d.get("step1Active") is True and d.get("count") == "已选 2/7 位协作者", [d.get("pane2Hidden"), d.get("step1Active"), d.get("count")], [False, True, "已选 2/7 位协作者"])

# ---------- 5k 提交 ----------
print("=" * 118)
print("5k. 提交 → 关闭 + DS Message 提示（复用 tdToast）")
d = g("5k")
chk("5k", "提交后弹窗关闭 + 开关复位", d.get("open") is False and d.get("rootHidden") is True and d.get("flag") is False, [d.get("open"), d.get("rootHidden"), d.get("flag")], [False, True, False])
chk("5k", "★ 提示文案回填「已流转 8 个产物给 2 位协作者」", d.get("msgText") == "已流转 8 个产物给 2 位协作者", d.get("msgText"), "已流转 8 个产物给 2 位协作者")
chk("5k", "提示为 DS Message（role=status + giencoder-message）", d.get("msgRole") == "status" and d.get("msgCls") == "giencoder-message", [d.get("msgRole"), d.get("msgCls")], ["status", "giencoder-message"])

# ---------- 5l/5m/5n/5o/5p 五种关闭 ----------
print("=" * 118)
print("5l~5p. 关闭途径：取消 / X / 遮罩 / Esc / 外部事件")
chk("5l", "重开后回到 Step1（pane1 显示）", g("5l_pre").get("open") is True and g("5l_pre").get("step1") is True, [g("5l_pre").get("open"), g("5l_pre").get("step1")], [True, True])
d = g("5l")
chk("5l", "「取消」关闭 + 开关复位 + display:none", d.get("open") is False and d.get("rootHidden") is True and d.get("flag") is False and d.get("display") == "none", [d.get("open"), d.get("flag"), d.get("display")], [False, False, "none"])
d = g("5m")
chk("5m", "右上 X 关闭", d.get("open") is False and d.get("rootHidden") is True and d.get("flag") is False, [d.get("open"), d.get("flag")], [False, False])
d = g("5n")
chk("5n", "点遮罩关闭", d.get("open") is False and d.get("rootHidden") is True and d.get("flag") is False, [d.get("open"), d.get("flag")], [False, False])
chk("5o", "Esc 前处于打开态（开关在）", g("5o_pre").get("open") is True and g("5o_pre").get("flag") is True, [g("5o_pre").get("open"), g("5o_pre").get("flag")], [True, True])
d = g("5o")
chk("5o", "★ Esc 关闭（页尾 Esc 链 → td:close-coop）", d.get("open") is False and d.get("rootHidden") is True and d.get("flag") is False, [d.get("open"), d.get("flag")], [False, False])
d = g("5p")
chk("5p", "外部派发 td:close-coop 亦可关闭", d.get("open") is False and d.get("rootHidden") is True, [d.get("open"), d.get("rootHidden")], [False, True])

# ---------- 5q 复位 ----------
print("=" * 118)
print("5q. 重新打开 = 完全复位（步骤 / 勾选 / 搜索 / 文案）")
d = g("5q")
chk("5q", "回到 Step1 + pane2 隐藏", d.get("open") is True and d.get("step1Active") is True and d.get("pane2Hidden") is True, [d.get("open"), d.get("step1Active"), d.get("pane2Hidden")], [True, True, True])
chk("5q", "★ 勾选态复位（产物 8/8、成员 0）", d.get("checked1") == 8 and d.get("mChecked") == 0, [d.get("checked1"), d.get("mChecked")], [8, 0])
chk("5q", "文案/计数复位", d.get("hint") == "选择需要流转到下一阶段的协作产物" and d.get("count") == "已选 8/8 个产物", [d.get("hint"), d.get("count")], "Step1 / 8/8")

# ---------- 静态：Esc 链顺序 ----------
print("=" * 118)
print("静态检查：页尾 Esc 链优先级 + DS 契约引用")
src = io.open(PAGE, encoding="utf-8").read()
i_img = src.find("hasAttribute('data-td-img-preview')) {")
i_coop = src.find("data-td-coop-open')) {")
i_dp = src.find("data-td-dp-open')) {")
i_pop = src.find("data-td-pop-open')) {")
chk("esc", "Esc 链含 coop 分支", i_coop > 0, i_coop, ">0")
chk("esc", "★ 优先级：图片预览 > 协作弹窗 > 转派浮窗 > 对话框弹层", 0 < i_img < i_coop < i_dp < i_pop, [i_img, i_coop, i_dp, i_pop], "递增")
for slug in ["modal", "steps", "checkbox", "list", "avatar", "input"]:
    c = io.open("giencoder-design-system/components/%s.json" % slug, encoding="utf-8").read()
    chk("ds", "契约 components/%s.json 可读且含 anatomy" % slug, '"anatomy"' in c, "anatomy" in c, True)

print("=" * 118)
print("总断言 %d 项：PASS %d / FAIL %d" % (len(OK) + len(BAD), len(OK), len(BAD)))
if BAD:
    print("失败明细：")
    for s, n, got, want in BAD:
        print("  [%s] %s  got=%s want=%s" % (s, n, got, want))
    print("RESULT: HAS_FAIL")
    sys.exit(1)
print("RESULT: ALL_OK")

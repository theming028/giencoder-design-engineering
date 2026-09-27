# -*- coding: utf-8 -*-
"""第30轮检查器：读 mg-work/r30/probe30.jsonl，逐项断言并打印 PASS/FAIL 表。
用法: python check30.py [probe.jsonl]
"""
import io
import json
import re
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "mg-work/r30/probe30.jsonl"

STEP = {}
for ln in io.open(PATH, encoding="utf-8"):
    ln = ln.strip()
    if not ln:
        continue
    o = json.loads(ln)
    STEP[o["step"]] = o["data"]

RESULTS = []


def check(item, name, fn):
    try:
        ok, detail = fn()
    except Exception as e:  # noqa
        ok, detail = False, "EXC %s: %s" % (type(e).__name__, e)
    RESULTS.append((item, name, bool(ok), detail))


def d(step):
    v = STEP.get(step)
    if v is None:
        raise AssertionError("缺少 probe 步骤 %s" % step)
    return v


def nums(t):
    if not t or t == "none":
        return []
    return [float(x) for x in re.findall(r"-?\d+\.?\d*(?:[eE]-?\d+)?", t)]


def tx(t):
    """从 computed transform 取 translateX"""
    if not t or t == "none":
        return None
    n = nums(t)
    if t.startswith("matrix3d"):
        return n[12]
    if t.startswith("matrix"):
        return n[4]
    return None


def sc(t):
    if not t or t == "none":
        return None
    n = nums(t)
    return n[0]


def near(a, b, tol=1.5):
    return a is not None and abs(a - b) <= tol


def eq(actual, expect):
    return actual == expect, "actual=%r expect=%r" % (actual, expect)


# ---------------------------------------------------------------- 第 1 项
def i1a():
    v = d("1a")
    out = []
    for k, exp in [("hasImage", True), ("hasWrapper", True), ("role", "button"),
                   ("tabindex", "0"), ("complete", True),
                   ("previewExistsBefore", False), ("htmlFlagBefore", False)]:
        out.append("%s=%r" % (k, v.get(k)))
        assert v.get(k) == exp, "%s 期望 %r，实测 %r" % (k, exp, v.get(k))
    assert v.get("natural") == [1240, 620], "naturalSize=%r" % (v.get("natural"),)
    assert v.get("wrapCursor") == "zoom-in", "cursor=%r" % v.get("wrapCursor")
    assert v.get("maskOpacity") == "0", "hover mask 初始 opacity=%r" % v.get("maskOpacity")
    assert v.get("imgClass") == "giencoder-image-img", "img.class=%r" % v.get("imgClass")
    assert "预览大图" in (v.get("ariaLabel") or ""), "aria-label=%r" % v.get("ariaLabel")
    return True, "契约结构 OK；缩略框=%s 自然尺寸=%s cursor=zoom-in" % (v.get("wrapRect"), v.get("natural"))


def i1b():
    v = d("1b")
    assert v.get("maskOpacity") == "1", "hover 后 opacity=%r（期望 1）" % v.get("maskOpacity")
    assert v.get("maskVisible") == "visible", "visibility=%r" % v.get("maskVisible")
    assert v.get("svgCount") == 1, "hover mask 内 svg 数=%r" % v.get("svgCount")
    return True, "hover 蒙层 opacity=1 / 内容=「预览」+1 个 svg / 命中目标=%s" % v.get("hitClass")


def i1c():
    v = d("1c")
    assert v.get("exists"), "预览层 DOM 不存在"
    for k, exp in [("display", "flex"), ("isOpen", True), ("htmlFlag", True),
                   ("position", "fixed"), ("srcMatch", True), ("altMatch", True)]:
        assert v.get(k) == exp, "%s 期望 %r，实测 %r" % (k, exp, v.get(k))
    # overlay 覆盖 1440x900 视口
    ol = v.get("overlayRect")
    assert ol and ol[0] == 0 and ol[1] == 0 and ol[2] == 1440 and ol[3] == 900, \
        "overlayRect=%r（期望 [0,0,1440,900]）" % (ol,)
    assert v.get("zIndex") == "1000", "z-index=%r" % v.get("zIndex")
    assert v.get("opacity") in ("1", "1.0") or float(v.get("opacity")) > 0.99, "opacity=%r" % v.get("opacity")
    im = v.get("imgRect")
    assert im and im[2] >= 1200, "大图宽=%r（期望 ~1240）" % (im,)
    cr, zr = v.get("closeRect"), v.get("zoomRect")
    assert cr and cr[0] > 1200 and cr[1] < 120, "关闭按钮位置异常 %r" % (cr,)
    assert zr and zr[0] < 120 and zr[1] > 780, "缩放工具位置异常 %r" % (zr,)
    return True, ("遮罩 1440x900 fixed z=1000 opacity=%s；大图 %s；src/alt 与缩略图一致；"
                  "关闭 %s / 缩放 %s" % (v.get("opacity"), im, cr, zr))


def i1d():
    v = d("1d")
    assert near(sc(v.get("transform")), 1.25, 0.02), "缩放后 scale=%r（期望 1.25）" % sc(v.get("transform"))
    assert v.get("scaleVar") == "1.25", "--giencoder-image-scale=%r" % v.get("scaleVar")
    assert v.get("stillOpen"), "点缩放按钮后预览被误关"
    return True, "点放大 → transform=%s（scale=%s）；预览仍打开" % (v.get("transform"), v.get("scaleVar"))


def i1e():
    v = d("1e")
    assert v.get("display") == "none", "关闭后 display=%r" % v.get("display")
    assert v.get("isOpen") is False, "关闭后仍带 is-open"
    assert v.get("htmlFlag") is False, "关闭后 <html> 仍带 data-td-img-preview"
    assert v.get("url") == "task-detail.html", "url=%r" % v.get("url")
    return True, "关闭按钮 → display=none / is-open 已摘 / html 标记已摘 / url 未变"


def i1f():
    v1, v2 = d("1f1"), d("1f2")
    assert v1.get("reopened") and v1.get("htmlFlag"), "第二次打开失败：%r" % v1
    assert v2.get("display") == "none", "点空白后 display=%r" % v2.get("display")
    assert v2.get("isOpen") is False, "点空白后仍带 is-open"
    assert v2.get("htmlFlag") is False, "点空白后 html 标记未摘"
    return True, "二次打开 OK；点 20,20（命中 %s）→ 关闭" % v2.get("hitAt2020")


def i1g():
    v = d("1g")
    assert v.get("display") == "none", "Esc 后 display=%r" % v.get("display")
    assert v.get("isOpen") is False, "Esc 后仍带 is-open"
    assert v.get("htmlFlag") is False, "Esc 后 html 标记未摘"
    assert v.get("url") == "task-detail.html", "Esc 关预览却跳走了：url=%r" % v.get("url")
    assert v.get("detailStillThere"), "详情页被卸载"
    return True, "Esc → 只关预览；url 仍 task-detail.html；activeElement=%s" % v.get("activeEl")


def i1h():
    v = d("1h")
    assert v.get("url") == "kanban.html", "第二次 Esc 未回看板：url=%r" % v.get("url")
    return True, "第二次 Esc → kanban.html（Esc 链层级正确）"


check("1", "1a 契约结构与基线", i1a)
check("1", "1b 悬停出现「预览」蒙层", i1b)
check("1", "1c 点击打开全屏预览遮罩", i1c)
check("1", "1d 工具栏缩放", i1d)
check("1", "1e 关闭按钮", i1e)
check("1", "1f 点空白处关闭", i1f)
check("1", "1g Esc 关预览且不误跳", i1g)
check("1", "1h Esc 链回归", i1h)

# ---------------------------------------------------------------- 第 2 项
def i2a():
    v = d("2a")
    assert v.get("swapped") is False, "初始就是 is-swapped"
    assert v.get("flex") == "row", "初始 flexDirection=%r" % v.get("flex")
    assert v.get("gapW") == 8, "拖动条宽=%r" % v.get("gapW")
    assert v.get("cursor") == "grab", "标题栏 cursor=%r" % v.get("cursor")
    assert v.get("touchAction") == "none", "touch-action=%r" % v.get("touchAction")
    tp = v.get("transitionProp") or ""
    assert "outline-color" in tp and "box-shadow" in tp, "transition-property=%r" % tp
    assert v.get("leftTransform") == "none", "初始 transform=%r" % v.get("leftTransform")
    return True, ("left=%s right=%s gap=%s cursor=%s transition=%s/%s"
                  % (v.get("leftRect"), v.get("rightRect"), v.get("gapW"), v.get("cursor"),
                     tp, v.get("transitionDur")))


def i2b():
    v = d("2b")
    a20, a40, rel = v.get("at20"), v.get("at40"), v.get("released")
    assert a20.get("xdrag") is True, "移动 20px 后未进入拖动态"
    assert a20.get("cursor") == "grabbing", "拖动态 cursor=%r" % a20.get("cursor")
    assert near(tx(a20.get("left")), 20), "跟手位移 tx=%r（期望 20）" % tx(a20.get("left"))
    assert near(tx(a20.get("peer")), -2), "让位栏 tx=%r（期望 -2）" % tx(a20.get("peer"))
    assert a40.get("armed") is False, "40px 就 armed 了（阈值 72）"
    assert near(tx(a40.get("left")), 40), "40px 跟手 tx=%r" % tx(a40.get("left"))
    assert near(tx(a40.get("peer")), -5), "40px 让位 tx=%r" % tx(a40.get("peer"))
    assert sc(a40.get("left")) > 1.0, "主动栏未浮起 scale=%r" % sc(a40.get("left"))
    assert rel.get("swapped") is False, "未达阈值却换位了"
    assert rel.get("fly") is False, "未达阈值却进入 FLIP 飞行态"
    assert rel.get("xdrag") is False, "松手后拖动态未清理"
    assert tx(rel.get("left")) is not None, "松手后没有回弹动画（transform=none）"
    return True, ("跟手 20→tx=%s / 让位 %s；40→tx=%s scale=%.3f armed=%s outline=%s；"
                  "松手回弹 transform=%s"
                  % (round(tx(a20.get("left")), 2), round(tx(a20.get("peer")), 2),
                     round(tx(a40.get("left")), 2), sc(a40.get("left")), a40.get("armed"),
                     a40.get("outline"), str(rel.get("left"))[:40]))


def i2b2():
    v = d("2b2")
    assert v.get("left") == "none", "回弹结束后 transform=%r（应清空）" % v.get("left")
    assert v.get("peer") == "none", "让位栏残留 transform=%r" % v.get("peer")
    assert v.get("swapped") is False and v.get("xdrag") is False and v.get("armed") is False, \
        "回弹后状态未复位：%r" % v
    return True, "回弹结束 → 两栏 transform 均清空、is-swapped/is-xdrag/is-xarmed 全复位"


def i2c():
    v, b, rel = d("2c"), d("2c1b"), d("2c1c")
    dr, far = v.get("dragging"), v.get("draggingFar")
    cap = tx(dr.get("left"))
    t120, t400 = tx(dr.get("left")), tx(far.get("left"))
    assert dr.get("xdrag") is True, "越阈值时不在拖动态"
    assert cap is not None and 90 <= cap <= 110, "cap 附近跟手 tx=%r（cap = 两栏中心距*14% ≈ 100）" % cap
    # 橡皮筋：|dx|=120 时 100 + 20*0.18 = 103.6 → 104；|dx|=400 时 100 + 300*0.18 = 154
    assert abs(t120 - 104) <= 2, "|dx|=120 → tx=%r（橡皮筋期望 ~104）" % t120
    assert abs(t400 - 154) <= 3, "|dx|=400 → tx=%r（橡皮筋期望 ~154）" % t400
    assert t400 > t120 + 30, "远拖未继续跟手（tx120=%r tx400=%r）→ 疑似硬限幅" % (t120, t400)
    assert t400 < 0.5 * 400, "远拖阻尼不足（tx400=%r，应远小于 400）" % t400
    assert near(tx(far.get("peer")), round(-t400 * 0.12)), \
        "远拖让位 tx=%r（期望 %r）" % (tx(far.get("peer")), round(-t400 * 0.12))
    assert dr.get("armed") is True, "越阈值后未 armed"
    assert sc(dr.get("left")) > 1.0, "主动栏未浮起 scale=%r" % sc(dr.get("left"))
    assert sc(dr.get("left")) <= 1.007, "浮起幅度失控 scale=%r（k 未收敛到 1）" % sc(dr.get("left"))
    # 描边色 / 让位透明度必须等过渡跑完再读（140ms / 180ms）
    assert b.get("held") and b.get("armed"), "读取过渡结果时拖动已中断：%r" % b
    assert "55, 112, 247" in (b.get("outline") or ""), "armed 描边色=%r（期望 primary-6）" % b.get("outline")
    assert b.get("outlineWidth") == "2px", "armed 描边宽=%r" % b.get("outlineWidth")
    assert float(b.get("peerOpacity")) < 0.95, "让位栏未降透明：%r" % b.get("peerOpacity")
    assert "transform" in (b.get("willChange") or ""), "拖动期未开 will-change：%r" % b.get("willChange")
    assert rel.get("swapped") is True, "越阈值松手未换位"
    assert rel.get("xdrag") is False and rel.get("armed") is False, "松手后交互态未清理：%r" % rel
    assert rel.get("fly") is True, "未进入 FLIP 飞行态"
    assert rel.get("flyLeft") is True and rel.get("flyRight") is False, \
        "被拖的 .td-left 未成为飞行期上层：%r" % rel
    assert rel.get("flex") == "row-reverse", "换位后 flexDirection=%r" % rel.get("flex")
    assert rel.get("zLeft") == "3" and rel.get("zRight") == "1", \
        "飞行期层级 zLeft=%r zRight=%r（被拖的应是 3）" % (rel.get("zLeft"), rel.get("zRight"))
    assert rel.get("boxLeft") is True, "飞行期被拖栏未加深投影"
    assert tx(rel.get("left")) not in (None, 0), "FLIP 起手位移为空：%r" % rel.get("left")
    return True, ("跟手 tx: 120px→%s / 400px→%s（橡皮筋 cap≈%s + 超出×0.18，非硬停）；"
                  "armed 描边=%s/%s 让位 opacity=%s；松手 → row-reverse + is-fly-left(z L=%s/R=%s,投影加深) + FLIP 起手 %s"
                  % (round(t120, 1), round(t400, 1), round(cap, 1), b.get("outline"), b.get("outlineWidth"),
                     b.get("peerOpacity"), rel.get("zLeft"), rel.get("zRight"), str(rel.get("left"))[:30]))


def i2c2():
    v, a = d("2c2"), d("2a")
    assert v.get("fly") is False, "FLIP 飞行态未清理"
    assert v.get("swapped") is True, "换位状态丢失"
    assert v.get("flex") == "row-reverse", "最终 flexDirection=%r" % v.get("flex")
    assert v.get("leftTransform") == "none" and v.get("rightTransform") == "none", \
        "飞行结束后残留 transform：%r" % (v.get("leftTransform"), v.get("rightTransform"))
    assert v.get("zLeft") == "auto" and v.get("zRight") == "auto", \
        "飞行结束后层级未复位：%r / %r" % (v.get("zLeft"), v.get("zRight"))
    L, Rt = v["leftRect"], v["rightRect"]
    # 两栏宽度不变，只是「视觉左右」对调：row-reverse 下 .td-left 落到 .td-right 右侧
    assert L[2] == a["leftRect"][2], "换位后 .td-left 宽=%r（应保持 %r）" % (L[2], a["leftRect"][2])
    assert Rt[2] == a["rightRect"][2], "换位后 .td-right 宽=%r（应保持 %r）" % (Rt[2], a["rightRect"][2])
    exp_lx = v["rootX"] + Rt[2] + a["gapW"]
    assert near(L[0], exp_lx, 2), "换位后 .td-left x=%r（期望 %r）" % (L[0], exp_lx)
    assert near(Rt[0], v["rootX"], 2), "换位后 .td-right x=%r（期望 %r）" % (Rt[0], v["rootX"])
    assert L[0] > Rt[0], "换位后 .td-left 未落到 .td-right 右侧"
    return True, ("落位：.td-left %s→x=%s（宽 %s 不变），.td-right %s→x=%s（宽 %s 不变）；"
                  "transform/z-index 全复位"
                  % (a["leftRect"][:2], L[0], L[2], a["rightRect"][:2], Rt[0], Rt[2]))


def i2d():
    v = d("2d")
    assert v.get("swappedAfter") == v.get("swappedBefore"), "纯点击竟换位了"
    assert v.get("xdrag") is False, "2px 位移就进入拖动态（阈值应为 6px）"
    assert v.get("armed") is False, "纯点击 armed"
    assert v.get("left") == "none", "纯点击产生了位移 %r" % v.get("left")
    return True, "位移 2px（<6px 死区）→ 不进拖动态、不 armed、不位移、不换位"


def i2e():
    v = d("2e")
    assert v["mid"].get("xdrag") is False, "点按钮却进入拖动态"
    assert v["mid"].get("left") == "none", "点按钮产生位移 %r" % v["mid"].get("left")
    assert v["mid"].get("armed") is False, "点按钮 armed"
    assert v["after"].get("swapped") == v.get("swappedBefore"), "点按钮换位了"
    assert v["after"].get("url") == "task-detail.html", "点按钮跳页了：%r" % v["after"].get("url")
    return True, "在「%s」按钮上按下并拖 160px → 无拖动态、无位移、无换位、未跳页" % v.get("target")


def i2f():
    v = d("2f")
    assert v["mid"].get("armed") is True, \
        "40px 位移（<72）未被甩动判定 armed：%r" % v["mid"]
    assert v.get("swappedAfter") != v.get("swappedBefore"), "甩动未换位"
    assert v.get("fly") is True, "甩动换位未走 FLIP 飞行态"
    v2 = d("2f2")
    assert v2.get("swapped") == v.get("swappedAfter"), "甩动后最终状态不一致：%r" % v2
    return True, ("位移仅 40px（<阈值 72）但速度 ≥0.6px/ms → armed=%s，换位 %s→%s（row=%s）"
                  % (v["mid"].get("armed"), v.get("swappedBefore"), v.get("swappedAfter"),
                     v2.get("flex")))


def i2g():
    v = d("2g")
    assert v.get("fullscreen") is True, "未能进入全屏态"
    assert v["mid"].get("xdrag") is False, "全屏态下仍进入拖动态"
    assert v["mid"].get("left") == "none", "全屏态下产生位移 %r" % v["mid"].get("left")
    assert v["mid"].get("armed") is False, "全屏态下 armed"
    assert v.get("fullscreenAfterExit") is False, "退出全屏失败"
    return True, "全屏态 → is-xdrag/armed 均未触发、无位移；退出全屏正常"


def i2h():
    v = d("2h")
    assert v.get("rightW") == 1424, "全屏右栏宽=%r" % v.get("rightW")
    assert v.get("inner")[2] == 860 and v.get("composer")[2] == 860, \
        "内容宽 inner=%r composer=%r" % (v.get("inner"), v.get("composer"))
    assert abs(v.get("innerVsRightCenter", 9)) <= 0.5, "inner 未居中：偏差 %r" % v.get("innerVsRightCenter")
    assert abs(v.get("composerVsRightCenter", 9)) <= 0.5, "composer 未居中：偏差 %r" % v.get("composerVsRightCenter")
    assert v.get("innerEqComposer") is True, "inner 与 composer 边界不一致"
    return True, ("第 29 轮回归：右栏 %s 宽，内容列 [%s,%s] 宽 %s 居中（偏差 %s / %s）"
                  % (v.get("rightW"), v["inner"][0], v["inner"][1], v["inner"][2],
                     v.get("innerVsRightCenter"), v.get("composerVsRightCenter")))


check("2", "2a 基线（过渡/游标/gap）", i2a)
check("2", "2b 跟手位移 + 回弹", i2b)
check("2", "2b2 回弹复位", i2b2)
check("2", "2c 限幅跟手+armed+FLIP", i2c)
check("2", "2c2 换位落位与清理", i2c2)
check("2", "2d 纯点击不触发", i2d)
check("2", "2e 点按钮不触发", i2e)
check("2", "2f 甩动可换位", i2f)
check("2", "2g 全屏态互斥", i2g)
check("2", "2h 全屏 860 居中回归", i2h)

# ---------------------------------------------------------------- 第 3 项
def i3():
    v = d("3")
    assert v.get("tokenBody2") == "13px", "--font-size-body-2=%r" % v.get("tokenBody2")
    assert v.get("tokenBody3") == "14px", "--font-size-body-3=%r" % v.get("tokenBody3")
    groups = ["attrFs", "sideAttrFs", "kFs", "vFs", "tl1Fs", "sideDynFs", "whoFs", "whatFs",
              "tltFs", "footFs"]
    for g in groups:
        vals = v.get(g)
        assert vals == ["13px"], "%s=%r（期望全部 13px）" % (g, vals)
    assert v.get("h2Fs") == ["14px"], "小节标题 h2=%r（应保持 14px）" % v.get("h2Fs")
    assert v.get("prioFs") == ["12px"], "优先级标签=%r（应保持契约 12px）" % v.get("prioFs")
    assert v.get("attrLh") == ["20px"] and v.get("tl1Lh") == ["20px"] and v.get("tltLh") == ["20px"], \
        "行高不等于 20px：%r / %r / %r" % (v.get("attrLh"), v.get("tl1Lh"), v.get("tltLh"))
    cnt = "attr=%s sideAttr(含)=%s tl1=%s tlTime=%s foot=%s h2=%s prio=%s" % (
        v.get("attrCount"), v.get("sideAttrFs"), v.get("tl1Count"), v.get("tltCount"),
        v.get("footCount"), v.get("h2Count"), v.get("prioCount"))
    assert v.get("attrCount", 0) >= 7, "属性行数异常 %r" % v.get("attrCount")
    assert v.get("tltCount", 0) >= 3, "动态时间行数异常 %r" % v.get("tltCount")
    return True, "10 组选择器全部 13px/行高 20px；h2 仍 14px；优先级标签仍 12px（%s）" % cnt


check("3", "3  属性/动态文字 13px", i3)

# ---------------------------------------------------------------- 回归
def r1():
    v = d("R1")
    assert v.get("barH") == 48, "标题栏高=%r" % v.get("barH")
    assert v.get("leftW") == 936 and v.get("rightW") == 480, \
        "1440 布局 %r/%r（期望 936/480）" % (v.get("leftW"), v.get("rightW"))
    assert v.get("gap") == 8, "间隙=%r" % v.get("gap")
    assert v.get("titleBg") == "rgb(247, 247, 247)", "标题底色=%r" % v.get("titleBg")
    return True, "1440：左栏 %s + 间隙 %s + 右栏 %s；标题栏 %s 高；标题底色 %s" % (
        v.get("leftW"), v.get("gap"), v.get("rightW"), v.get("barH"), v.get("titleBg"))


def r2():
    v = d("R2")
    assert v.get("before") == 374, "描述折叠高=%r（期望 374）" % v.get("before")
    assert v.get("open") is True, "展开后未加 is-open"
    return True, "描述区折叠高 %s → 点「%s」展开成功" % (v.get("before"), v.get("label"))


def r3():
    v = d("R3")
    assert v.get("fullscreenBtn") == 1, "全屏按钮数=%r" % v.get("fullscreenBtn")
    return True, "全屏按钮存在（%s 个）" % v.get("fullscreenBtn")


check("R", "R1 布局基线回归", r1)
check("R", "R2 描述折叠回归", r2)
check("R", "R3 全屏按钮回归", r3)

# ---------------------------------------------------------------- 输出
print("")
print("=" * 108)
cur = None
fail = 0
for item, name, ok, detail in RESULTS:
    if item != cur:
        print("")
        print("---- 第 %s 项 ----" % item)
        cur = item
    print("  %s  %-28s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        fail += 1
print("")
print("=" * 108)
print("TOTAL %d 项，FAIL %d 项 → %s" % (len(RESULTS), fail, "ALL_OK" if fail == 0 else "HAS_FAIL"))
sys.exit(0 if fail == 0 else 1)

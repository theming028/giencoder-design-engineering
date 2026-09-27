# -*- coding: utf-8 -*-
"""第33轮断言器：读 mg-work/r33/probe33.jsonl + 静态自检 pages/task-detail.html。

真值来源：
  · 第 1~3 项 —— 设计稿协作弹窗（第 32 轮已逐像素量取，面板 left=400/top=130，640 宽）
  · 第 4 项   —— 与看板「创建任务」弹窗**同一份 CSS**（构建期抽取），故几何以看板实测为基准
  · 第 6 项   —— 橙色虚线「降两级」= --color-warning-6 → --color-warning-4
"""
import io
import json
import re

PROBE = "mg-work/r33/probe33.jsonl"
PAGE = "pages/task-detail.html"
KANBAN = "pages/kanban.html"

rows = {}
for ln in io.open(PROBE, encoding="utf-8"):
    ln = ln.strip()
    if not ln:
        continue
    o = json.loads(ln)
    rows[o["step"]] = o["data"]

OK, BAD = [], []


def chk(step, name, cond, got, want):
    (OK if cond else BAD).append((step, name, got, want))
    print("  %s %-6s %-50s got=%s  want=%s" % ("✓" if cond else "✗ FAIL", step, name, got, want))


def g(step):
    d = rows.get(step)
    if d is None:
        BAD.append((step, "<missing>", None, "probe 缺失"))
        print("  ✗ FAIL %-6s probe 步骤缺失" % step)
        return {}
    if "__parse_error__" in d:
        BAD.append((step, "<parse_error>", None, d.get("raw")))
        print("  ✗ FAIL %-6s __parse_error__ %s" % (step, str(d.get("raw"))[:150]))
        return {}
    return d


def near(a, b, tol=1.0):
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False


def rgb_tuple(s):
    """把 #hex / #rgb / rgb(a) 统一成 (r,g,b)；token 取回来通常是 rgb(...) 形式。"""
    if not s:
        return None
    s = s.strip()
    m = re.match(r"rgba?\(([^)]+)\)", s)
    if m:
        parts = [p.strip() for p in m.group(1).split(",")]
        try:
            return tuple(int(round(float(p))) for p in parts[:3])
        except Exception:
            return None
    if s.startswith("#"):
        h = s[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        try:
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        except Exception:
            return None
    return None


def same_rgb(a, b):
    ta, tb = rgb_tuple(a), rgb_tuple(b)
    return ta is not None and ta == tb


WARN4 = (255, 182, 93)     # --color-warning-4 = orange-4 = #FFB65D
WARN6 = (255, 125, 0)      # --color-warning-6 = orange-6 = #FF7D00


# ============================ 第 1~3 项：协作弹窗 ============================
print("=" * 118)
print("1. .giencoder-modal-content 白底 + 边框加深一级（border-1 #F2F2F2 → border-2 #E5E5E5）")
d = g("A1")
chk("A1", "内容区背景 = 白", d.get("bg") == "rgb(255, 255, 255)", d.get("bg"), "rgb(255, 255, 255)")
chk("A1", "背景取自 token（--color-bg-5）", d.get("bg5", "").lower() in ("#fff", "#ffffff"),
    d.get("bg5"), "#fff")
chk("A1", "--color-border-2 = #E5E5E5", same_rgb(d.get("b2"), "#E5E5E5"), d.get("b2"), "rgb(229, 229, 229)")
chk("A1", "--color-border-1 = #F2F2F2（对照）", same_rgb(d.get("b1"), "#F2F2F2"), d.get("b1"), "rgb(242, 242, 242)")
chk("A1", "边框色 = --color-border-2", same_rgb(d.get("border"), d.get("b2")),
    d.get("border"), d.get("b2"))
chk("A1", "边框色 ≠ --color-border-1（确实加深了一级）", not same_rgb(d.get("border"), d.get("b1")),
    d.get("border"), "≠ " + str(d.get("b1")))
chk("A1", "边框宽 1px", d.get("bw") == "1px", d.get("bw"), "1px")

print("-" * 118)
print("2. .giencoder-steps-item 衔接处 = 向右箭头（段1 右凸尖 + 段2 左凹口，非对称）")
d = g("A3")
G0 = d.get("g0") or {}
G1 = d.get("g1") or {}
C0 = (G0.get("clip") or "").replace(" ", "")
C1 = (G1.get("clip") or "").replace(" ", "")
chk("A3", "步骤数 = 2", d.get("n") == 2, d.get("n"), 2)
chk("A3", "段1 右凸尖：右边缘收敛到 100% 50%", "100%50%" in C0 and "calc(100%-7px)0px" in C0, C0, "含 100% 50% + calc(100% - 7px) 0px")
chk("A3", "段1 左边缘为平边（不左凸）", C0.startswith("polygon(0px0px,"), C0, "polygon(0 0, ...)")
chk("A3", "段2 左凹口：5px 50% 内凹顶点", "5px50%" in C1, C1, "含 5px 50%")
chk("A3", "段2 右边缘为平边（不右凸）", "100%100%," in C1 and "100%50%" not in C1, C1, "无 100% 50%")
chk("A3", "已去掉旧的对称伪元素尖角", (G0.get("margin") == "0px" and G1.get("margin") == "0px"),
    [G0.get("margin"), G1.get("margin")], ["0px", "0px"])
chk("A3", "两段等宽（flex:1）", near(G0.get("rect", [0, 0, 0, 0])[2], G1.get("rect", [0, 0, 0, 0])[2], 1.5),
    [G0.get("rect", [0, 0, 0])[2], G1.get("rect", [0, 0, 0])[2]], "相等")
chk("A3", "两段宽度之和 = 容器宽（无重叠/无溢出）",
    near(G0.get("rect", [0, 0, 0])[2] + G1.get("rect", [0, 0, 0])[2],
         d.get("wrap", [0, 0, 0])[2], 2.0),
    [G0.get("rect", [0, 0, 0])[2], G1.get("rect", [0, 0, 0])[2], d.get("wrap", [0, 0, 0])[2]], "相等")
chk("A3", "段1 尖顶点 = 段2 左缘（方向一致，两段首尾相接）",
    near(G0.get("rect", [0, 0, 0, 0])[0] + G0.get("rect", [0, 0, 0, 0])[2],
         G1.get("rect", [0, 0, 0, 0])[0], 1.0),
    G0.get("rect", [0, 0, 0, 0])[0] + G0.get("rect", [0, 0, 0, 0])[2], G1.get("rect", [0, 0, 0, 0])[0])
chk("A3", "段1 底色 = primary-1 浅蓝（选中态）", G0.get("bg") == "rgb(236, 242, 255)", G0.get("bg"), "rgb(236, 242, 255)")
chk("A3", "段2 底色 = fill-2 灰（未选中态）", G1.get("bg") == "rgb(242, 242, 242)", G1.get("bg"), "rgb(242, 242, 242)")

print("-" * 118)
print("3. .td-coop-dvd-tx 字号 = 14px")
d = g("A2")
chk("A2", "--font-size-body-3 = 14px", d.get("body3") == "14px", d.get("body3"), "14px")
chk("A2", "实测字号 14px（= token）", d.get("fs") == "14px" == d.get("body3"), d.get("fs"), "14px")
chk("A2", "行高 20px", d.get("lh") == "20px", d.get("lh"), "20px")

# ============================ 第 4 项：编辑弹窗 ============================
print("=" * 118)
print("4a. 初始态：编辑按钮与弹窗就位但未打开")
d = g("B0")
chk("B0", "顶栏有 [data-td-edit] 按钮", d.get("btn") is True, d.get("btn"), True)
chk("B0", "页面内含 .kb-crt（与看板同一份 DOM）", d.get("modal") is True, d.get("modal"), True)
chk("B0", "已绑定（data-td-edit-bound=1）", d.get("bound") == "1", d.get("bound"), "1")
chk("B0", "初始 hidden", d.get("hidden") is True, d.get("hidden"), True)
chk("B0", "初始 aria-expanded=false", d.get("aria") == "false", d.get("aria"), "false")

print("-" * 118)
print("4b. 点「编辑」→ 打开：与看板创建弹窗**同一形态**（含关键回归：.kb-crt 必须 position:absolute）")
d = g("B1")
k = g("C1")
chk("B1", "已打开（is-open + 非 hidden）", d.get("open") is True and d.get("hidden") is False,
    [d.get("open"), d.get("hidden")], [True, False])
chk("B1", "写入 <html data-td-edit-open>", d.get("flag") is True, d.get("flag"), True)
chk("B1", "aria-expanded=true", d.get("aria") == "true", d.get("aria"), "true")
chk("B1", "★ .kb-crt 定位 = absolute（注释吞规则的回归点）", d.get("crtPos") == "absolute", d.get("crtPos"), "absolute")
chk("B1", "★ --kb-crt-width 解析为 80%（同上）", d.get("varW") == "80%", d.get("varW"), "80%")
chk("B1", ".kb-crt 铺满 main（宽 = 1424）", near((d.get("crt") or [0, 0, 0])[2], 1424, 2), (d.get("crt") or [0, 0, 0])[2], 1424)
chk("B1", "挂载宿主 = 与看板同一个 <main>（shell 内容区）",
    "min-w-0 flex-1" in (d.get("host") or ""), d.get("host"), "min-w-0 flex-1 …")
chk("B1", ".kb-crt 铺满宿主（= main 的 padding box 8,48,1424,844）",
    [x for x in (d.get("crt") or [])] == [8, 48, 1424, 844], d.get("crt"), [8, 48, 1424, 844])
chk("B1", "dialog 宽 = 看板 dialog 宽 (±2，差在 main 无 1px 边框)",
    near((d.get("dlg") or [0, 0, 0])[2], (k.get("dlg") or [0, 0, 0])[2], 2),
    (d.get("dlg") or [0, 0, 0])[2], (k.get("dlg") or [0, 0, 0])[2])
chk("B1", "dialog 高 = 看板 dialog 高 (±2)",
    near((d.get("dlg") or [0, 0, 0, 0])[3], (k.get("dlg") or [0, 0, 0, 0])[3], 2),
    (d.get("dlg") or [0, 0, 0, 0])[3], (k.get("dlg") or [0, 0, 0, 0])[3])
chk("B1", "dialog 水平居中（中心 = 视口中心 720）",
    near((d.get("dlg") or [0, 0, 0])[0] + (d.get("dlg") or [0, 0, 0])[2] / 2.0, 720, 1.5),
    (d.get("dlg") or [0, 0, 0])[0] + (d.get("dlg") or [0, 0, 0])[2] / 2.0, 720)
chk("B1", "圆角 = 顶角直角 + 底角 12（0 0 12px 12px）",
    d.get("rTL") == "0px" and d.get("rBR") == "12px" and d.get("rBR") == k.get("radius", "").split()[-1],
    [d.get("rTL"), d.get("rBR")], ["0px", "12px"])
chk("B1", "白底", d.get("bg") == "rgb(255, 255, 255)", d.get("bg"), "rgb(255, 255, 255)")
chk("B1", "含首帧黑边修复的 1px 同色 spread", "0px 0px 0px 1px" in (d.get("shadow") or ""),
    (d.get("shadow") or "")[:60], "含 0 0 0 1px")
chk("B1", "role=dialog / aria-modal=true", d.get("role") == "dialog" and d.get("ariaModal") == "true",
    [d.get("role"), d.get("ariaModal")], ["dialog", "true"])
chk("B1", "标题切到「编辑工作任务」", d.get("title") == "编辑工作任务", d.get("title"), "编辑工作任务")
chk("B1", "is-edit 标记已加（隐藏「保存并继续创建」用）", d.get("isEdit") is True, d.get("isEdit"), True)

print("-" * 118)
print("4c. 底栏：与创建态同结构，仅隐藏「保存并继续创建」，主按钮文案 → 保存")
d = g("B2")
btns = d.get("btns") or []
by_tx = {}
for b in btns:
    by_tx[b.get("tx")] = b
chk("B2", "底栏高 56", d.get("h") == "56px", d.get("h"), "56px")
chk("B2", "左右内距 24", d.get("pad") == "0px 24px", d.get("pad"), "0px 24px")
chk("B2", "三按钮齐全（取消 / 保存并继续创建 / 保存）",
    sorted(by_tx.keys()) == ["保存", "保存并继续创建", "取消"], sorted(by_tx.keys()), "3 个")
chk("B2", "「保存并继续创建」隐藏", by_tx.get("保存并继续创建", {}).get("disp") == "none" and d.get("keepDisp") == "none",
    [by_tx.get("保存并继续创建", {}).get("disp"), d.get("keepDisp")], "none")
chk("B2", "「取消」为主要按钮之一（secondary）",
    "giencoder-btn-secondary" in (by_tx.get("取消", {}).get("cls") or ""), by_tx.get("取消", {}).get("cls"), "含 -secondary")
chk("B2", "主按钮「保存」为 primary", "giencoder-btn-primary" in (by_tx.get("保存", {}).get("cls") or ""),
    by_tx.get("保存", {}).get("cls"), "含 -primary")
chk("B2", "按钮尺寸 = 78×32（与看板同档）",
    by_tx.get("保存", {}).get("rect", [0, 0, 0, 0])[2:] == [78, 32], by_tx.get("保存", {}).get("rect"), "[x, y, 78, 32]")

print("-" * 118)
print("4d. 数据预填（同一个创建表单，只是填了当前需求的数据）")
d = g("B3")
ty = d.get("type") or {}
chk("B3", "任务类型已填：拆分需求项", ty.get("val") == "拆分需求项" and ty.get("hasValue") is True,
    [ty.get("val"), ty.get("hasValue")], ["拆分需求项", True])
chk("B3", "类型下拉内该选项为选中态", ty.get("selected") == "拆分需求项", ty.get("selected"), "拆分需求项")
want_rows = [
    ("状态", "进行中"), ("优先级", "高"), ("关联需求", "端到端流程初始化"),
    ("前置任务", "端到端流程初始化"), ("责任人", "邵禹铭"),
]
got_rows = [(r.get("lbl"), r.get("val")) for r in (d.get("rows") or [])]
for lbl, want in want_rows:
    found = [v for l, v in got_rows if l and l.startswith(lbl)]
    chk("B3", "属性「%s」已填" % lbl, bool(found) and (found[0] or "").startswith(want),
        found[0] if found else None, want + "…")
chk("B3", "属性行数 = 6", len(got_rows) == 6, len(got_rows), 6)
chk("B3", "标题已填且为需求标题",
    (d.get("titleVal") or "").startswith("端到端流程初始化") and len(d.get("titleVal") or "") > 10,
    d.get("titleVal"), "端到端流程初始化：…")
chk("B3", "描述已填（多行正文）", (d.get("descLen") or 0) > 30 and "作为研发负责人" in (d.get("descHead") or ""),
    [d.get("descLen"), d.get("descHead")], ">30 且含「作为研发负责人」")
chk("B3", "预期完成日期已填", d.get("dateVal") == "2026/08/20", d.get("dateVal"), "2026/08/20")
chk("B3", "日历面板同步点亮 20 号", d.get("calSel") == "20", d.get("calSel"), "20")
chk("B3", "附件 3 条（与看板创建态同结构）", d.get("upCount") == 3, d.get("upCount"), 3)

print("-" * 118)
print("4e. 主体分栏与 aside 表单行（main : aside = 88% : 320 固定栏）")
d = g("B4")
chk("B4", "头部 48 高", d.get("headH") == "48px", d.get("headH"), "48px")
chk("B4", "aside 宽 320（min-width 主导）", (d.get("aside") or [0, 0, 0])[2] == 320, (d.get("aside") or [0, 0, 0])[2], 320)
chk("B4", "main + aside = dialog 宽", near((d.get("main") or [0, 0, 0])[2] + (d.get("aside") or [0, 0, 0])[2],
                                          d.get("dialogW"), 1.5),
    [(d.get("main") or [0, 0, 0])[2], (d.get("aside") or [0, 0, 0])[2]], d.get("dialogW"))
chk("B4", "属性行数 = 6", d.get("rows") == 6, d.get("rows"), 6)
chk("B4", "行内 label 80 + 控件填满剩余", (d.get("lbl") or [0, 0, 0])[2] == 80 and
    near((d.get("fld") or [0, 0, 0, 0])[2] + 80, (d.get("row0") or [0, 0, 0, 0])[2], 2),
    [(d.get("lbl") or [0, 0, 0])[2], (d.get("fld") or [0, 0, 0, 0])[2], (d.get("row0") or [0, 0, 0, 0])[2]],
    "[80, x, 272]")

print("-" * 118)
print("4f. 表单控件真的可交互（用的是 DS Select 契约结构）")
d = g("B5")
chk("B5", "点视图后 popup 打开（.giencoder-popup-open）", d.get("open") is True and d.get("display") == "block",
    [d.get("open"), d.get("display")], [True, "block"])
chk("B5", "触发器 aria-expanded=true", d.get("aria") == "true", d.get("aria"), "true")
chk("B5", "该 popup 内选项数 > 1", (d.get("optCount") or 0) > 1, d.get("optCount"), ">1")
d = g("B5b")
chk("B5b", "选中后视图文案更新且浮层收起", bool(d.get("val")) and d.get("popOpen") is False,
    [d.get("val"), d.get("popOpen")], "[非空, False]")

print("-" * 118)
print("4g. 关闭与提交")
d = g("B6")
chk("B6", "Esc（焦点在 input 内）可关闭", d.get("hidden") is True and d.get("flag") is False and d.get("aria") == "false",
    [d.get("hidden"), d.get("flag"), d.get("aria")], [True, False, "false"])
d = g("B7")
chk("B7", "点「保存」→ 弹窗关闭", d.get("hidden") is True and d.get("flag") is False,
    [d.get("hidden"), d.get("flag")], [True, False])
chk("B7", "提示走 DS Message（role=status）", d.get("msgCls") == "giencoder-message" and d.get("msgRole") == "status",
    [d.get("msgCls"), d.get("msgRole")], ["giencoder-message", "status"])
chk("B7", "提示文案 = 任务已保存", d.get("msgText") == "任务已保存", d.get("msgText"), "任务已保存")
d = g("B8")
chk("B8", "清空标题后保存 → 仍在弹窗（未提交）", d.get("modalHidden") is False, d.get("modalHidden"), False)
chk("B8", "显示「任务标题」校验消息（DS Message）",
    d.get("msgsHidden") is False and d.get("errTitleHidden") is False and d.get("errRole") == "status",
    [d.get("msgsHidden"), d.get("errTitleHidden"), d.get("errRole")], [False, False, "status"])
chk("B8", "文案 = 「任务标题」不能为空", d.get("errText") == "「任务标题」不能为空", d.get("errText"), "「任务标题」不能为空")
chk("B8", "标题控件进入 error 态", d.get("inputErr") is True, d.get("inputErr"), True)

# ============================ 第 5 项：base 去弥散 ============================
print("=" * 118)
print("5. base.html main：去掉彩色弥散、只留波点")
d = g("D1")
chk("D1", "background-image 只剩 1 层", d.get("bgImgLayers") == 1, d.get("bgImgLayers"), 1)
chk("D1", "该层是波点（primary 6 号 10%）", d.get("hasDot") is True, d.get("hasDot"), True)
chk("D1", "无任何一种彩色弥散", d.get("diffusion") == [], d.get("diffusion"), "[]")
chk("D1", "波点平铺 20px 20px / repeat", d.get("bgSize") == "20px 20px" and d.get("bgRepeat") == "repeat",
    [d.get("bgSize"), d.get("bgRepeat")], ["20px 20px", "repeat"])
d = g("D2")
diff = [x for x in (d.get("list") or []) if x.get("layers", 0) > 1]
chk("D2", "main 子树内没有多层渐变元素", diff == [], diff, "[]")

# ============================ 第 6 项：看板虚线 + hover ============================
print("=" * 118)
print("6a. 看板「进行中」首卡橙色虚线降两级")
d = g("C2")
chk("C2", "找到虚线卡", d.get("found") is True, d.get("found"), True)
chk("C2", "位于「进行中」泳道", d.get("lane") == "进行中", d.get("lane"), "进行中")
chk("C2", "是该泳道第 1 张（orderInCol=0）", d.get("orderInCol") == 0, d.get("orderInCol"), 0)
chk("C2", "★ --color-warning-4 已定义（本轮补进内联 :root）", (d.get("w4") or "") != "", d.get("w4"), "非空")
chk("C2", "★ 虚线 stroke 已解析（不再 none）", (d.get("stroke") or "none") != "none", d.get("stroke"), "非 none")
chk("C2", "虚线色 = warning-4 = #FFB65D", rgb_tuple(d.get("stroke")) == WARN4, d.get("stroke"), "rgb(255, 182, 93)")
chk("C2", "= --color-warning-4（降两级后的档位）", same_rgb(d.get("stroke"), d.get("w4")), [d.get("stroke"), d.get("w4")], "相等")
chk("C2", "≠ --color-warning-6（原色 #FF7D00，确实降了）", not same_rgb(d.get("stroke"), d.get("w6")),
    [d.get("stroke"), d.get("w6")], "不相等")
chk("C2", "线型仍是虚线 4/3", (d.get("dash") or "").replace(" ", "") == "4px,3px", d.get("dash"), "4px, 3px")

print("-" * 118)
print("6b. 卡片 hover 时标题转中粗 500（且不换行、不改变卡高）")
d = g("C3")
rest = d.get("rest") or []
ncards = d.get("n") or 0
chk("C3", "rest 态标题字重 = 400", all(x.get("fw") == "400" for x in rest) and len(rest) > 0,
    sorted(set(x.get("fw") for x in rest)), "400")
d = g("C4")
chk("C4", "虚线卡 hover 字重 = 500", d.get("fw") == "500", d.get("fw"), "500")
chk("C4", "虚线卡 hover 卡高 = rest 卡高（不换行）",
    near(d.get("h"), (g("C2") or {}).get("restH"), 0.6), d.get("h"), (g("C2") or {}).get("restH"))
chk("C4", "hover 不改变虚线颜色", rgb_tuple(d.get("stroke")) == WARN4, d.get("stroke"), "rgb(255, 182, 93)")
hover = []
for i in range(ncards):
    x = g("C6_%d" % i)
    hover.append((i, x.get("fw"), x.get("cardH"), x.get("i")))
chk("C6", "逐张 hover 覆盖全部卡片（%d 张）" % ncards, len(hover) == ncards and all(h[3] == h[0] for h in hover),
    len(hover), ncards)
bad_fw = [h[0] for h in hover if h[1] != "500"]
chk("C6", "每张卡 hover 标题字重都是 500", bad_fw == [], bad_fw, "[]")
bad_h = [h[0] for h in hover if not near(h[2], rest[h[0]].get("h") if h[0] < len(rest) else None, 0.6)]
chk("C6", "每张卡 hover 后高度 = rest 高度（无需为 500 字重留出换行位移）", bad_h == [], bad_h, "[]")

print("-" * 118)
print("6c. 看板「创建任务」弹窗基准（供第 4 项比对）")
d = g("C1")
chk("C1", "dialog = 1138×794（151, 49）",
    [(d.get("dlg") or [])[0], (d.get("dlg") or [])[1], (d.get("dlg") or [])[2], (d.get("dlg") or [])[3]] == [151, 49, 1138, 794],
    d.get("dlg"), [151, 49, 1138, 794])
chk("C1", "头部 48 / 底栏 56", [d.get("headH"), d.get("footH")] == ["48px", "56px"],
    [d.get("headH"), d.get("footH")], ["48px", "56px"])
chk("C1", "创建态「保存并继续创建」可见（对照编辑态）", d.get("keepDisp") == "flex", d.get("keepDisp"), "flex")

# ============================ 静态自检 ============================
print("=" * 118)
print("S. 静态自检：CSS 注释完整性 + 内联 token 与 DS 对齐 + 弹窗结构同源")


def strip_comments(css):
    """按 CSS 规则剥注释（注释不可嵌套：第一个 */ 即闭合），返回 (去注释正文, 问题列表)"""
    out, issues, i = [], [], 0
    while i < len(css):
        j = css.find("/*", i)
        if j < 0:
            out.append(css[i:])
            break
        out.append(css[i:j])
        k = css.find("*/", j + 2)
        if k < 0:
            issues.append("注释未闭合 @%d" % j)
            break
        i = k + 2
    body = "".join(out)
    if "*/" in body:
        issues.append("游离的 */（会把紧随其后的规则吞成野规则的声明块）")
    return body, issues


def cjk_in_prelude(css):
    """规则前奏（{ 之前、上一处 } / ; 之后）出现**裸的**非 ASCII
    → 说明注释被提前闭合、中文残渣被当成了选择器。
    注意：属性选择器里的引号字符串是合法 CSS（如 [aria-label="数字分身"]），先剥掉引号串。"""
    hits = []
    for m in re.finditer(r"\{", css):
        start = max(css.rfind("}", 0, m.start()), css.rfind(";", 0, m.start()))
        pre = css[start + 1:m.start()]
        pre = re.sub(r'"[^"]*"', '""', pre)
        pre = re.sub(r"'[^']*'", "''", pre)
        if any(ord(c) > 127 for c in pre):
            hits.append(pre.strip()[:48])
    return hits


src = io.open(PAGE, encoding="utf-8").read()
kbs = io.open(KANBAN, encoding="utf-8").read()

styles = re.findall(r"<style[^>]*>(.*?)</style>", src, re.S)
all_issues, all_cjk = [], []
for i, s in enumerate(styles):
    body, iss = strip_comments(s)
    all_issues += ["block#%d %s" % (i, x) for x in iss]
    all_cjk += ["block#%d %r" % (i, x) for x in cjk_in_prelude(body)][:3]
chk("S1", "所有 <style> 块：注释成对、无游离 */", all_issues == [], all_issues, "[]")
chk("S1c", "所有 <style> 块：无「注释提前闭合」残渣（规则前奏必须是 ASCII 选择器）",
    all_cjk == [], all_cjk, "[]")
chk("S1b", "已移除会提前闭合注释的那句旧注释",
    "`/* r15-create-modal-css */`" not in src, "`/* r15-create-modal-css */`" in src, False)
i_crt = src.find(".kb-crt {")
chk("S2", ".kb-crt 规则存在且其前一个注释已闭合（回归点）", i_crt > 0 and src.rfind("*/", 0, i_crt) > 0,
    i_crt, "> 0")
chk("S2b", ".kb-crt-dialog 与看板同源（构建期抽取）",
    "由 build-detail.py 在构建期从 pages/kanban.html 抽取" in src, True, True)

# 内联 :root 与 DS 对齐：warning 全档
ds = io.open("giencoder-design-system/colors_and_type.css", encoding="utf-8").read()
miss = [n for n in range(1, 11) if "--color-warning-%d:" % n not in src]
chk("S3", "页面内联 --color-warning-1..10 与 DS 全档对齐", miss == [], miss, "[]")
chk("S3b", "看板内联 --color-warning-4: 已补", "--color-warning-4:" in kbs, "--color-warning-4:" in kbs, True)
chk("S3c", "DS 源文件 warning 全档", all("--color-warning-%d:" % n in ds for n in range(1, 11)), True, True)

# 弹窗结构同源：KB_HTML 在页内是 JS 字符串数组，引号被转义
for tok, esc in [
    ('<div class="kb-crt" hidden>', '<div class=\\"kb-crt\\" hidden>'),
    ('class="giencoder-modal kb-crt-dialog"', 'class=\\"giencoder-modal kb-crt-dialog\\"'),
    ('data-crt-keep="1"', 'data-crt-keep=\\"1\\"'),
    ('data-crt-submit="1"', 'data-crt-submit=\\"1\\"'),
    ('kb-crt-msgs', 'kb-crt-msgs'),
    ('kb-crt-aside-body', 'kb-crt-aside-body'),
]:
    chk("S4", "详情页含看板同源结构 %s" % tok, esc in src, esc in src, True)

khtml = io.open(KANBAN, encoding="utf-8").read()
chk("S4b", "看板里同一份结构也仍在", all(e in khtml for e in
    ['<div class=\\"kb-crt\\" hidden>', 'data-crt-submit=\\"1\\"']), True, True)

print("=" * 118)
print("PASS %d / FAIL %d" % (len(OK), len(BAD)))
if BAD:
    print("失败项：")
    for b in BAD:
        print("   ✗ %-6s %-50s got=%s want=%s" % b)
print("RESULT:", "ALL_OK" if not BAD else "HAS_FAIL")

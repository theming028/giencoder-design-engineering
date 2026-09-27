# -*- coding: utf-8 -*-
"""第32轮断言器（第 1/2/3/4 项）：读 mg-work/r32/probe32.jsonl。
设计稿真值来源：mg-work/r32/design/coop.*（第 5 项）；第 1/2/3/4 项真值见下。
"""
import io
import json
import re
import sys

PROBE = "mg-work/r32/probe32.jsonl"
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
    print("  %s %-6s %-42s got=%s  want=%s" % ("✓" if cond else "✗ FAIL", step, name, got, want))


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


def rgb(v):
    if v is None:
        return None
    s = str(v).replace("rgba(", "").replace("rgb(", "").replace(")", "")
    try:
        p = [float(x.strip()) for x in s.split(",")]
        return tuple(int(round(x)) for x in p[:3])
    except Exception:
        return None


print("=" * 112)
print("2a. 基线几何")
d = g("2a")
chk("2a", "左栏 [8,48,936,844]", d.get("left") == [8, 48, 936, 844], d.get("left"), [8, 48, 936, 844])
chk("2a", "右栏 x952 w480", near((d.get("right") or [0])[0], 952) and near((d.get("right") or [0])[2], 480), d.get("right"), "[952,48,480,844]")
chk("2a", "拖动条宽 8", near((d.get("gutter") or [0])[2], 8), d.get("gutter"), "w=8")
chk("2a", "CSS --td-left-min = 480px（第4项）", d.get("leftMinCss") == "480px", d.get("leftMinCss"), "480px")
chk("2a", "跟手限幅 = 中心距×28%", near(d.get("capExpect"), round((d.get("gap") or 0) * 0.28), 1), [d.get("gap"), d.get("capExpect")], "cap=round(gap*0.28)")

print("=" * 112)
print("2b. 拖动跟手（1:1 区放宽后）")
CAP = (g("2a").get("capExpect") or 200)
d = g("2b20")
chk("2b", "进入拖动态 is-xdrag", d.get("moved") is True, d.get("moved"), True)
chk("2b", "+20px → tx=20（严格 1:1）", near(d.get("panelTx"), 20), d.get("panelTx"), 20)
chk("2b", "让位栏反向 14% → tx=-3", near(d.get("peerTx"), -round(20 * 0.14), 1), d.get("peerTx"), -round(20 * 0.14))
chk("2b", "★ 位移不含 scale（矩阵 m11 = 1，第2项去重栅格化）", near(d.get("scale"), 1.0, 0.0011), d.get("scale"), 1.0)
chk("2b", "transform 纯平移（matrix(1, 0, 0, 1, tx, 0)）", (d.get("transform") or "").startswith("matrix(1, 0, 0, 1,"), d.get("transform"), "matrix(1, 0, 0, 1, tx, 0)")
d = g("2b120")
chk("2b", "+120px → tx=120（旧版仅 104，已放宽）", near(d.get("panelTx"), 120), d.get("panelTx"), 120)
chk("2b", "+120px 已过阈值 → is-xarmed", d.get("armed") is True, d.get("armed"), True)
d = g("2b400")
exp400 = round(CAP + (400 - CAP) * 0.28)
chk("2b", "+400px → 橡皮筋 tx=%d（cap + 超出×0.28）" % exp400, near(d.get("panelTx"), exp400, 1), d.get("panelTx"), exp400)
chk("2b", "位移仍无 scale", near(d.get("scale"), 1.0, 0.0011), d.get("scale"), 1.0)
chk("2b", "主动栏「拎起来」加深投影（含 8px 24px 0.1）", "8px 24px" in (d.get("panelShadow") or ""), d.get("panelShadow"), "含 8px 24px")
d = g("2b_back")
chk("2b", "反向拖回 +20 → tx=20（反向同样 1:1）", near(d.get("panelTx"), 20), d.get("panelTx"), 20)
d = g("2c")
chk("2c", "未达阈值松手 → 未换位", d.get("swapped") is False, d.get("swapped"), False)
chk("2c", "左栏回到原位 x=8", near((d.get("leftRect") or [0])[0], 8), (d.get("leftRect") or [None])[0], 8)
chk("2c", "回弹结束清掉内联 transform", d.get("panelTransform") == "none" and not d.get("inlinePanel"), [d.get("panelTransform"), d.get("inlinePanel")], "transform 已复位")

print("=" * 112)
print("2d/2e. 连发位移终值 + 换位回归")
d = g("2d")
exp210 = round(min(210, CAP) + max(0, 210 - CAP) * 0.28)
chk("2d", "连发 6 帧后终值 = 末次位移的跟手值 %d（rAF 合并不丢帧）" % exp210, near(d.get("panelTx"), exp210, 1), d.get("panelTx"), exp210)
d = g("2e_mid")
chk("2e", "朝对方方向超过阈值 → is-xarmed", d.get("armed") is True, d.get("armed"), True)
d = g("2e")
chk("2e", "松手后换位（is-swapped）", d.get("swapped") is True, d.get("swapped"), True)
chk("2e", "换位后左栏 x=496 / 右栏 x=8", near((d.get("left") or [0])[0], 496) and near((d.get("right") or [0])[0], 8), [d.get("left"), d.get("right")], "[496.., 8..]")
d = g("2e_reset")
chk("2e", "重载后复位为默认（swapped=False / 936+480）", d.get("swapped") is False and near((d.get("left") or [0])[2], 936, 1) and near((d.get("right") or [0])[2], 480, 1), [d.get("swapped"), d.get("left"), d.get("right")], "[False, 936, 480]")

print("=" * 112)
print("1a. 转派浮窗投影 = Select 弹层投影（第1项）")
d = g("1a")
sh = d.get("shadow") or ""
chk("1a", "浮窗存在且已打开", d.get("exists") is True, d.get("exists"), True)
chk("1a", "投影 = 0 8px 20px rgba(0,0,0,.1)", "0px 8px 20px" in sh and "0.1" in sh, sh, "含 0px 8px 20px / 0.1")
chk("1a", "等于 --shadow3-down token", "8px 20px" in (d.get("shadow3tok") or ""), d.get("shadow3tok"), "0 8px 20px")
chk("1a", "已不再是 --shadow2-down(0 4px 10px)", "0px 4px 10px" not in sh, sh, "不含 0px 4px 10px")

print("=" * 112)
print("3a/3b. AI 文件卡 与 「3个AI产物」卡 = 同一组件（第3项）")
d = g("3a")
ai, pr = d.get("ai") or {}, d.get("prod") or {}
chk("3a", "同为 <a> 元素（可点、有链接语义）", ai.get("tag") == "A" and pr.get("tag") == "A", [ai.get("tag"), pr.get("tag")], ["A", "A"])
chk("3a", "类名完全相同（td-file td-file--lg）", ai.get("cls") == pr.get("cls"), [ai.get("cls"), pr.get("cls")], "两者相等")
chk("3a", "尺寸相同（294×56）", ai.get("rect") and pr.get("rect") and near(ai["rect"][2], 294, 1) and near(ai["rect"][3], 56, 1) and near(pr["rect"][2], 294, 1), [ai.get("rect"), pr.get("rect")], "均 294×56")
chk("3a", "底色相同 #F7F7F7", rgb(ai.get("bg")) == rgb(pr.get("bg")) == (247, 247, 247), [ai.get("bg"), pr.get("bg")], "rgb(247, 247, 247) 两者相同")
chk("3a", "圆角相同 8px", ai.get("radius") == pr.get("radius") == "8px", [ai.get("radius"), pr.get("radius")], "8px 两者相同")
chk("3a", "图标盒同 24×24 / 同色", ai.get("icoRect") and near(ai["icoRect"][2], 24) and ai.get("icoColor") == pr.get("icoColor"), [ai.get("icoRect"), ai.get("icoColor"), pr.get("icoColor")], "24×24 / 同色")
chk("3a", "竖分隔线同为 1×24 同色", ai.get("sepRect") and near(ai["sepRect"][2], 1) and near(ai["sepRect"][3], 24) and ai.get("sepColor") == pr.get("sepColor"), [ai.get("sepRect"), ai.get("sepColor")], "1×24 同色")
chk("3a", "文案块同为 column 布局", ai.get("bodyDisplay") == pr.get("bodyDisplay") == "flex", [ai.get("bodyDisplay"), pr.get("bodyDisplay")], "flex 两者相同")
chk("3a", "标题字号/字重相同", ai.get("txFs") == pr.get("txFs") and ai.get("txFw") == pr.get("txFw"), [ai.get("txFs"), ai.get("txFw"), pr.get("txFs"), pr.get("txFw")], "14px/500")
chk("3a", "副行（大小）字号/色相同", ai.get("sizeFs") == pr.get("sizeFs") and ai.get("sizeColor") == pr.get("sizeColor"), [ai.get("sizeFs"), ai.get("sizeColor"), pr.get("sizeFs"), pr.get("sizeColor")], "12px/同色")
chk("3a", "内部子节点类名序列完全相同", ai.get("kids") == pr.get("kids"), [ai.get("kids"), pr.get("kids")], "两者相同")
d = g("3b_ai")
a_bg = d.get("bg")
d2 = g("3b_prod")
p_bg = d2.get("bg")
chk("3b", "hover 底色相同且 = fill-2 #F2F2F2", rgb(a_bg) == rgb(p_bg) == (242, 242, 242), [a_bg, p_bg], "rgb(242, 242, 242) 两者相同")
chk("3b", "hover 光标同为 pointer", g("3b_ai").get("cursor") == "pointer" and g("3b_prod").get("cursor") == "pointer", [g("3b_ai").get("cursor"), g("3b_prod").get("cursor")], "pointer 两者")

print("=" * 112)
print("4a/4b. 左栏拖窄下限 480（第4项）")
d = g("4a")
chk("4a", "★ 拉到极限后左栏恰为 480 宽", near((d.get("left") or [0])[2], 480, 1), d.get("left"), "[*,*,480,*]")
chk("4a", "右栏同时达到最大 936", near((d.get("right") or [0])[2], 936, 1), d.get("right"), "[*,*,936,*]")
chk("4a", "--td-right-w 写入 936px", d.get("rightWvar") == "936px", d.get("rightWvar"), "936px")
chk("4a", "两栏 + 拖动条不溢出容器（原先会超 8px）", d.get("noOverflow") is True and d.get("rootScrollW") == d.get("rootClientW"), [d.get("noOverflow"), d.get("rootScrollW"), d.get("rootClientW")], "不溢出")
d = g("4a_reset")
chk("4a", "拖回中位 → 右栏 480 / 左栏 936", near((d.get("right") or [0])[2], 480, 1) and near((d.get("left") or [0])[2], 936, 1), [d.get("right"), d.get("left")], "480 / 936")
d = g("4b_mid")
chk("4b", "反向拖到极右 → 实时折叠右栏", d.get("collapsed") is True, d.get("collapsed"), True)
d = g("4b")
chk("4b", "松手后处于折叠态", d.get("collapsed") is True and d.get("rightW") == "48px", [d.get("collapsed"), d.get("rightW")], [True, "48px"])
d = g("4b_reset")
chk("4b", "点击折叠条恢复 480", d.get("collapsed") is False and near((d.get("right") or [0])[2], 480, 1), [d.get("collapsed"), d.get("right")], "[False, 480]")

print("=" * 112)
print("静态检查：DS 源文件里两个弹层的投影声明")
sel = io.open("giencoder-design-system/components.css", encoding="utf-8").read()
pop = io.open("giencoder-design-system/gienx-templates/ui-controls.css", encoding="utf-8").read()
m = re.search(r"\.giencoder-select-popup\s*\{[^}]*\}", sel, re.S)
chk("1a", "components.css .giencoder-select-popup 用 --shadow3-down", m and "var(--shadow3-down)" in m.group(0), (m.group(0).splitlines()[-2].strip() if m else None), "var(--shadow3-down)")
m2 = re.search(r"\.giencoder-popover\s*\{[^}]*\}", pop, re.S)
chk("1a", "ui-controls.css .giencoder-popover 用 --shadow3-down", m2 and "var(--shadow3-down)" in m2.group(0), (m2.group(0).splitlines()[-1].strip() if m2 else None), "var(--shadow3-down)")
c1 = io.open("giencoder-design-system/components/select.json", encoding="utf-8").read()
c2 = io.open("giencoder-design-system/components/popover.json", encoding="utf-8").read()
chk("1a", "select.json 契约 token 同步为 --shadow3-down", '"--shadow3-down"' in c1 and '"--shadow2-down"' not in c1, "--shadow3-down" if '"--shadow3-down"' in c1 else "--shadow2-down", "--shadow3-down")
chk("1a", "popover.json 契约 token 同步为 --shadow3-down", '"--shadow3-down"' in c2 and '"--shadow2-down"' not in c2, "--shadow3-down" if '"--shadow3-down"' in c2 else "--shadow2-down", "--shadow3-down")

print("=" * 112)
print("总断言 %d 项：PASS %d / FAIL %d" % (len(OK) + len(BAD), len(OK), len(BAD)))
if BAD:
    print("失败明细：")
    for s, n, got, want in BAD:
        print("  [%s] %s  got=%s want=%s" % (s, n, got, want))
    print("RESULT: HAS_FAIL")
    sys.exit(1)
print("RESULT: ALL_OK")

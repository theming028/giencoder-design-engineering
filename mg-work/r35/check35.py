# -*- coding: utf-8 -*-
"""第 35 轮第 1 项断言器：任务详情页「左右分栏互换 + 栏宽 + 折叠」的布局记忆。

输入：
  · pages/task-detail.html   —— 静态结构（记忆模块 / 落盘时机 / 钳位 / 双击出口）
  · mg-work/r21/build-detail.py —— 唯一生成源
  · mg-work/r35/probe35.jsonl   —— 实测探针（拖动 → 刷新 → 钳位 → 复位）

用法：C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe mg-work/r35/check35.py
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
        print("  x %s %s  %s" % (tag, desc, detail))


def load_jsonl(p):
    out = {}
    for ln in io.open(os.path.join(ROOT, p), encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        d = json.loads(ln)
        out[d["step"]] = d["data"]
    return out


P = load_jsonl("mg-work/r35/probe35.jsonl")
TD = io.open(os.path.join(ROOT, "pages", "task-detail.html"), encoding="utf-8").read()
SRC = io.open(os.path.join(ROOT, "mg-work", "r21", "build-detail.py"), encoding="utf-8").read()

KEY = "giencoder:td-cols:v1"

# ══════════════════════════ 1. 静态：记忆模块 ══════════════════════════
chk("1a", "生成源与产物都带版本化键名 %s" % KEY, SRC.count(KEY) == 1 and TD.count(KEY) == 1)
for tag, fn in (("1b1", "function loadLayout"), ("1b2", "function saveLayout"),
                ("1b3", "function clearLayout"), ("1b4", "function persistLayout"),
                ("1b5", "function restoreLayout"), ("1b6", "function clampNow")):
    chk(tag, "记忆模块函数存在且唯一：%s" % fn, TD.count(fn) == 1)

chk("1c", "loadLayout 对坏数据/隐私模式有 try-catch 兜底",
    re.search(r"function loadLayout\(\)\s*\{[^}]*try\s*\{[^}]*JSON\.parse", TD, re.S) is not None)

# 落盘时机：localStorage.setItem 只能出现在 saveLayout 内（persistLayout 经它间接落盘）
body = TD[TD.find("var LAYOUT_KEY"):TD.find("function restoreLayout")]
chk("1d", "整个记忆模块里 localStorage.setItem 只出现 1 次（集中在 saveLayout）",
    body.count("localStorage.setItem") == 1 and "function saveLayout" in body)
# 拖动过程中绝不落盘：pointermove 处理块内不得出现 persistLayout
pm = TD[TD.find("gutter.addEventListener('pointermove'"):TD.find("function endDrag")]
chk("1e", "pointermove 处理器内不写记忆（同步 IO 会拖卡拖动）", "persistLayout" not in pm,
    "pointermove 段含 persistLayout")
ed = TD[TD.find("function endDrag"):TD.find("gutter.addEventListener('pointerup'")]
chk("1f", "endDrag（拖动结束）才落盘", "persistLayout();" in ed)
chk("1g", "collapse / expand 各自落盘（折叠与展开都是一次「用户选择」）",
    TD.count("      persistLayout();\n    }") >= 2)
chk("1h", "换位判定后落盘（endSwap 内 persistLayout）",
    re.search(r"function endSwap\([\s\S]{0,2500}?persistLayout\(\);", TD) is not None)

# 钳位：恢复时必须用 maxRightW() 夹住，否则换显示器后旧值放不下
rl = TD[TD.find("function restoreLayout"):TD.find("function setWidth")]
chk("1i", "restoreLayout 用 maxRightW() 对记忆宽度做钳位",
    "maxRightW()" in rl and "Math.min(d.rightW, m)" in rl)
chk("1j", "恢复过程用 layoutRestoring 标志防止回写覆盖原始记忆",
    "layoutRestoring = true" in rl and "if (layoutRestoring) return;" in TD)
chk("1k", "布局恢复在所有绑定之后、首次绘制前调用（实测容器宽可读）",
    re.search(r"if \(root\.getBoundingClientRect\(\)\.width > 0\) restoreLayout\(\);\s*\n\s*else requestAnimationFrame\(restoreLayout\);", TD) is not None)

# 运行期改变视口也要重新钳位（第 35 轮实测暴露：1440→1100 时右栏 644 溢出容器 1084）
cn = TD[TD.find("function clampNow"):TD.find("window.addEventListener('resize'")]
chk("1l", "clampNow 在运行期按 loadLayout() 的原始意图宽度重新钳位",
    "loadLayout()" in cn and "maxRightW()" in cn and "setWidth(next)" in cn)
chk("1m", "resize 监听器存在且用 rAF 合并（避免拖窗时高频重排）",
    "window.addEventListener('resize'" in TD and "requestAnimationFrame(function () { clampRaf = 0; clampNow(); })" in TD)
chk("1n", "clampNow 不落盘（钳位值写回会让窗口变宽后无法复原）",
    "persistLayout" not in cn and "saveLayout" not in cn and "setItem" not in cn)

# 双击出口
chk("1o", "拖动条有 dblclick「恢复默认布局」出口，且先回默认再清记忆",
    re.search(r"gutter\.addEventListener\('dblclick'[\s\S]{0,400}?expand\(DEFAULT_W\);[\s\S]{0,200}?clearLayout\(\);", TD) is not None)
chk("1p", "拖动条带 title 提示（可发现性）",
    "拖动调整栏宽 · 双击恢复默认布局" in TD)

# 幂等 / 未破坏既有结构
chk("1q", "拖动条与两栏根容器结构仍在（未因加记忆而改结构）",
    'data-td-gutter' in TD and 'class=\\"td-root\\"' in TD)

# ══════════════════════════ 2. 实测：拖动 → 刷新保持 ══════════════════════════
need = ["baseline", "afterSwap", "reload1", "swapBack", "reload2",
        "afterWidth", "reload3", "narrow", "narrowReload", "wideBack",
        "afterReset", "reload4"]
missing = [s for s in need if s not in P]
chk("2a", "实测探针齐全（%d 步）" % len(need), not missing, "缺 %s" % missing)
if missing:
    print()
    print("=" * 74)
    print("PASS %d / FAIL %d" % (len(PASS), len(FAIL)))
    for f in FAIL:
        print("  FAIL  " + f)
    print("HAS_FAIL")
    raise SystemExit(0)


def store(step):
    s = P[step].get("store")
    return json.loads(s) if s else None


def rootw(step):
    return P[step]["root"][2]


chk("2b", "基线：无记忆（localStorage 为空）、右栏 480 @ x952",
    store("baseline") is None and P["baseline"]["rightW"] == "480px"
    and P["baseline"]["right"][0] == 952)

# --- 互换记忆 ---
st = store("afterSwap")
chk("2c", "拖标题栏互换后 is-swapped=true 且右栏跑到左侧 x8",
    P["afterSwap"]["swapped"] is True and P["afterSwap"]["right"][0] == 8)
chk("2d", "互换结果已落盘（swapped=true）", st is not None and st.get("swapped") is True)
chk("2e", "★ 刷新后互换被记住（reload1 仍 is-swapped，右栏 x8）",
    P["reload1"]["swapped"] is True and P["reload1"]["right"][0] == 8
    and P["reload1"]["left"][0] == 496)
chk("2f", "再拖回原布局 → 状态与记忆同步翻转为 false",
    P["swapBack"]["swapped"] is False and store("swapBack").get("swapped") is False)
chk("2g", "★ 刷新后仍未交换（记忆是可逆的，不是单向锁死）",
    P["reload2"]["swapped"] is False and P["reload2"]["right"][0] == 952)

# --- 栏宽记忆 ---
chk("2h", "拖拖动条后右栏变宽 480 → 644，左栏同步变窄",
    P["afterWidth"]["rightW"] == "644px" and P["afterWidth"]["left"][2] == 772)
chk("2i", "栏宽已落盘", store("afterWidth").get("rightW") == 644)
chk("2j", "★ 刷新后栏宽被记住（reload3 仍 644px）",
    P["reload3"]["rightW"] == "644px" and P["reload3"]["right"][2] == 644)

# --- 窄视口钳位 ---
n = P["narrow"]
chk("2k", "★ 视口 1440→1100 时右栏被重新钳位（644 → 容器宽 − 拖动条 − 左栏保底）",
    n["rightW"] == "596px", "实测 %s" % n["rightW"])
chk("2l", "钳位算式可复算：root宽 − gutter宽 − LEFT_MIN(480) == 钳位值",
    rootw("narrow") - n["gutter"][2] - 480 == int(n["rightW"].replace("px", "")),
    "%d - %d - 480 != %s" % (rootw("narrow"), n["gutter"][2], n["rightW"]))
chk("2m", "钳位后两栏不溢出容器（右栏右边界 ≤ 容器右边界）",
    n["right"][0] + n["right"][2] <= n["root"][0] + n["root"][2],
    "right右=%d root右=%d" % (n["right"][0] + n["right"][2], n["root"][0] + n["root"][2]))
chk("2n", "★ 钳位值不落盘：narrow 时记忆里仍是用户选的 644",
    store("narrow").get("rightW") == 644)
chk("2o", "刷新后（窄视口）仍按钳位值渲染，且记忆未被改写",
    P["narrowReload"]["rightW"] == "596px" and store("narrowReload").get("rightW") == 644)
chk("2p", "★ 视口变回 1440 后，记忆里的 644 原样复原（可恢复性）",
    P["wideBack"]["rightW"] == "644px" and P["wideBack"]["root"][2] == 1424,
    "实测 %s / root %s" % (P["wideBack"]["rightW"], P["wideBack"]["root"]))

# --- 双击复位 ---
chk("2q", "★ 双击拖动条 → 宽度回默认 480、互换解除",
    P["afterReset"]["rightW"] == "480px" and P["afterReset"]["swapped"] is False
    and P["afterReset"]["right"][0] == 952)
chk("2r", "★ 双击后记忆被清空（store=null，下次打开是全新默认态）", store("afterReset") is None)
chk("2s", "★ 刷新后仍是默认布局、且记忆仍为空（清空是真持久）",
    P["reload4"]["rightW"] == "480px" and store("reload4") is None)

print()
print("=" * 74)
print("PASS %d / FAIL %d" % (len(PASS), len(FAIL)))
for f in FAIL:
    print("  FAIL  " + f)
print("ALL_OK" if not FAIL else "HAS_FAIL")

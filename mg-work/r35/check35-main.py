# -*- coding: utf-8 -*-
"""第 35 轮第 2 项断言器：数字分身主内容还原（设计稿节点 1345:18487，内容宽 860px）。

输入：
  · pages/avatar.html                 —— 产物（React bundle 已换壳 + AV-MAIN 注入段）
  · mg-work/r35/build-avatar-main.py   —— 唯一生成源（CONTENT 全量文案 / 适配层 CSS / 挂载 JS）
  · mg-work/r35/probe-main.jsonl       —— agent-browser 实测（几何 / 视觉 / 抽屉联动 / 1920 视口）

断言分组：
  A*  静态：bundle 换壳、注入段结构、契约类合规、文案齐全、CSS 只走 token、生成源完整
  B*  实测：几何逐项 = 设计稿、内容宽 860、视觉值、抽屉联动、宽视口不溢出
  C*  幂等：复跑生成源页面内容零变化

用法：C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe mg-work/r35/check35-main.py
"""
import ast
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = "C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
PASS, FAIL = [], []


def chk(tag, desc, cond, detail=""):
    (PASS if cond else FAIL).append("%s %s" % (tag, desc))
    if not cond:
        print("  x %s %s  %s" % (tag, desc, detail))


def rd(p):
    return io.open(os.path.join(ROOT, p), encoding="utf-8").read()


def load_jsonl(p):
    out = {}
    for ln in rd(p).splitlines():
        ln = ln.strip()
        if ln:
            d = json.loads(ln)
            out[d["step"]] = d["data"]
    return out


def strip_c(s):
    """去掉 CSS 注释（注释里引用过 token 真值 hex，不参与硬编码判定）。"""
    return re.sub(r"/\*.*?\*/", "", s, flags=re.S)


def match_block(src, start_mark, open_ch="{", close_ch="}"):
    """从 start_mark 起做括号配平，返回整段源码。"""
    i = src.find(start_mark)
    assert i >= 0, "找不到 %s" % start_mark
    k = src.find(open_ch, i)
    depth = 0
    while k < len(src):
        if src[k] == open_ch:
            depth += 1
        elif src[k] == close_ch:
            depth -= 1
            if depth == 0:
                break
        k += 1
    return i, k + 1, src[i:k + 1]


AV = rd("pages/avatar.html")
BUILD = rd("mg-work/r35/build-avatar-main.py")
P = load_jsonl("mg-work/r35/probe-main.jsonl")

# ── 从生成源抽出 CONTENT（保证断言文案与生成源同源，不会各自漂移） ──
_i, _j, _seg = match_block(BUILD, "CONTENT = {")
CONTENT = ast.literal_eval(_seg[len("CONTENT = "):])

# ── 注入段 / 模板段定位 ──
START = "<!-- AV-MAIN"
END = "<!-- /AV-MAIN -->"
I_CSS = AV.find('<style id="av-main-css">')
I_TPL = AV.find('<template id="av-main-tpl">')
I_JS = AV.find('<script id="av-main-js">')
I_END = AV.find(END)
I_BODY = AV.rfind("</body>")
CSS = strip_c(AV[I_CSS:AV.find("</style>", I_CSS)])
TPL = AV[I_TPL:AV.find("</template>", I_TPL)]

# ════════════════════════════════════════════════════ A. 静态 ════════════════════════════════
# A1 注入段标记成对且唯一，且落在 </body> 之前
chk("A1", "AV-MAIN 注入段标记成对且唯一（START/END 各 1 次）",
    AV.count(START) == 1 and AV.count(END) == 1,
    "START=%d END=%d" % (AV.count(START), AV.count(END)))
chk("A2", "注入段位于 </body> 之前，且内部顺序为 CSS → template → script → END",
    -1 < I_CSS < I_TPL < I_JS < I_END < I_BODY,
    "css=%d tpl=%d js=%d end=%d body=%d" % (I_CSS, I_TPL, I_JS, I_END, I_BODY))

# A3 React bundle 已换壳（Dt() 渲染体 = <div class="av-main">）
DT_MARK = 'className:`av-main`,id:`av-main`'
DT_OLD = 'className:`mx-auto flex w-full max-w-3xl flex-col gap-5`'
chk("A3", "bundle 里 Dt() 渲染体已换成 av-main 空壳（标记唯一）",
    AV.count(DT_MARK) == 1, "DT_MARK=%d" % AV.count(DT_MARK))
chk("A4", "旧列表页容器 max-w-3xl 不再作为 class 使用（仅留 Tailwind 定义）",
    DT_OLD not in AV
    and re.search(r'class=\\?"[^"\\]*max-w-3xl', AV) is None
    and AV.count("max-w-3xl") == 1,
    "count=%d" % AV.count("max-w-3xl"))
chk("A5", "旧列表页文案已移除（去 CSS/JS 注释后仍出现即失败）",
    "新建分身" not in strip_c(re.sub(r"(?<![:/])//[^\n]*", "", AV)),
    "去注释后仍含「新建分身」")

# A6 三个 id 唯一
for tag, i in (("A6a", "av-main-css"), ("A6b", "av-main-tpl"), ("A6c", "av-main-js")):
    chk(tag, "锚点 id 唯一：%s" % i, AV.count('id="%s"' % i) == 1)

# A7 契约类名零虚构（复用 r30 的类名自检，覆盖 task-detail + avatar）
try:
    r = subprocess.run([PY, os.path.join(ROOT, "mg-work", "r30", "check-classes.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"), timeout=180)
    out = (r.stdout or "") + (r.stderr or "")
    chk("A7", "两页 giencoder-* 类名差集全部为空（无自造同义类）",
        out.count("虚构类名差集: NONE") == 2 and "ALL_OK" in out,
        "NONE=%d ALL_OK=%s" % (out.count("虚构类名差集: NONE"), "ALL_OK" in out))
except Exception as e:
    chk("A7", "两页 giencoder-* 类名差集全部为空（无自造同义类）", False, str(e))

# A8 必备契约类真的被用上（组件复用铁律）
REQ = ["giencoder-card", "giencoder-card-header", "giencoder-card-header-title",
       "giencoder-card-header-extra", "giencoder-card-body",
       "giencoder-avatar", "giencoder-avatar-square", "giencoder-tag",
       "giencoder-btn", "giencoder-btn-secondary", "giencoder-btn-size-default"]
missing = [c for c in REQ if ('"%s' % c) not in AV and not re.search(r'class="[^"]*\b%s\b' % c, AV)]
chk("A8", "11 个必备 DS 契约类全部落在产物里", not missing, "缺: %s" % missing)

# A9 适配层类名一律 av- 前缀，且都有定义（无裸类）
av_used = set(re.findall(r'class="[^"]*\b(av-[A-Za-z0-9_-]+)', AV))
# 定义域取全页 CSS（含第 34 轮抽屉适配层）；HOOK 是纯语义勾子类，视觉由契约类承载
av_def = set(re.findall(r"\.(av-[A-Za-z0-9_-]+)", AV))
HOOK = {"av-main-edit"}
undef = sorted(c for c in av_used if c not in av_def and c not in HOOK)
chk("A9", "适配层 %d 个 av-* 类名全部有样式定义（%d 个语义勾子类例外）" % (len(av_used), len(HOOK)),
    not undef, "未定义: %s" % undef)

# A10 模板结构计数（与实测 B1 互证）
n_card = TPL.count('class="giencoder-card av-card"')
n_row = TPL.count('class="giencoder-card av-row"')
n_link = len(re.findall(r'class="av-link[" ]', TPL))
chk("A10", "模板内 4 卡 / 3 行卡 / 8 链接（含 4 卡头 + 4 行卡链接）",
    n_card == 4 and n_row == 3 and n_link == 8,
    "cards=%d rows=%d links=%d" % (n_card, n_row, n_link))

# A11 文案逐条存在（同源于生成源 CONTENT）
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


texts = [CONTENT["name"], CONTENT["pill"], CONTENT["created"], CONTENT["desc"],
         CONTENT["edit"], CONTENT["trigger"], CONTENT["foot"]]
for k in ("cardA", "cardB", "cardC", "cardD"):
    c = CONTENT[k]
    texts += [c["title"], c["link"]]
    if "para" in c:
        texts.append(c["para"])
    for gp in c.get("groups", []):
        texts.append(gp["title"])
        texts += gp["lines"]
    for t, d in c.get("items", []):
        texts += [t, d]
for r0 in CONTENT["rows"]:
    texts += [r0["title"], r0["sub"], r0["meta"]] + r0["links"]
texts = sorted(set(texts))
lost = [t for t in texts if esc(t) not in AV]
chk("A11", "设计稿文案 %d 条全部落在产物里（含卡片/行卡标题、副标题、元信息、链接文案）" % len(texts),
    not lost, "缺 %d 条: %s" % (len(lost), lost[:6]))

# A12 适配层 CSS：硬编码 hex 仅限设计稿真值白名单 + 颜色一律走 token
HEX_OK = {"#6B6B6B", "#A9A9A9", "#fff", "#8FA9F2", "#4F68CE", "#7C82C7"}
hexes = set(re.findall(r"#[0-9A-Fa-f]{3,8}", CSS))
chk("A12", "适配层 CSS 硬编码色仅 6 个已收敛的设计稿真值（无散落 hex）",
    hexes <= HEX_OK, "越界: %s" % sorted(hexes - HEX_OK))
sizes = [s.strip() for s in re.findall(r"font-size:\s*([^;]+);", CSS)]
SZ_OK = {"40px"}   # 头像 emoji 装饰字号（设计稿真值，token 表最大档 title-3=24 无对应）
bad_sz = [s for s in sizes if not s.startswith("var(--font-size-") and s not in SZ_OK]
chk("A13", "全部 %d 处 font-size 走 --font-size-* token（仅头像 emoji 40px 例外）" % len(sizes),
    not bad_sz, "越界: %s" % bad_sz)
chk("A14", "非 token 色收敛为局部变量（--av-ink-2 / --av-ink-4 定义 + 被引用）",
    "--av-ink-2: #6B6B6B" in CSS and "--av-ink-4: #A9A9A9" in CSS
    and "var(--av-ink-2)" in CSS and "var(--av-ink-4)" in CSS)

# A15 几何关键值写在 CSS 里（设计稿逐项）
GEO = [("内容宽 860", "max-width: 860px"), ("卡片最小高 292", "min-height: 292px"),
       ("行卡高 118", "height: 118px"), ("两列等宽网格", "repeat(2, minmax(0, 1fr))"),
       ("页脚宽 240", "width: 240px"), ("头部头像 104", "width: 104px; height: 104px;")]
bad_geo = [n for n, s in GEO if s not in CSS]
chk("A15", "适配层写明全部 6 项设计稿几何关键值", not bad_geo, "缺: %s" % bad_geo)

# A16 生成源完整（唯一入口 + 幂等机制 + 不硬编码 bundle 结构）
for tag, s in (("A16a", "DT_NEW"), ("A16b", "DT_MARK"), ("A16c", "DT_OLD_MARK"),
               ("A16d", "def find_dt"), ("A16e", "MAIN_HTML"), ("A16f", "CSS_TMPL"),
               ("A16g", "JS_TMPL"), ("A16h", "幂等自检失败")):
    chk(tag, "生成源含 %s" % s, s in BUILD)

# A17 挂载脚本：ready 标记 + MutationObserver 兜底 React 首帧时序
chk("A17", "挂载脚本带 data-av-main-ready 幂等标记 + MutationObserver 兜底",
    "data-av-main-ready" in AV and "MutationObserver" in AV
    and "host.innerHTML = HTML" in AV)

# A18 token 铁律：适配层引用的每个 var(--x) 都能在本页内联 :root / 局部变量里解析
_rt = re.search(r"(?<![\w.\-#]):root\s*\{(.*?)\}", AV, re.S)
root_def = set(re.findall(r"(--[A-Za-z0-9_-]+)\s*:", _rt.group(1) if _rt else ""))
local_def = set(re.findall(r"(--av-[A-Za-z0-9_-]+)\s*:", CSS))
used_var = set(re.findall(r"var\((--[A-Za-z0-9_-]+)", CSS))
unresolved = sorted(v for v in used_var if v not in root_def and v not in local_def)
chk("A18", "适配层引用 %d 个 CSS 变量全部可解析（页内 :root %d 个 token + %d 个局部变量）"
    % (len(used_var), len(root_def), len(local_def)), not unresolved, "未解析: %s" % unresolved)

# A19 组件复用铁律：适配层只做后代组合，不改写契约类本体
sels = re.findall(r"([^{}]+)\{", CSS)
bare = []
for s in sels:
    for part in s.split(","):
        p = part.strip()
        if re.fullmatch(r"\.giencoder-[A-Za-z0-9_-]+", p):
            bare.append(p)
chk("A19", "适配层无「裸 .giencoder-* 选择器」（只允许 .av-x .giencoder-y 后代组合）",
    not bare, "改写本体: %s" % bare)
chk("A20", "适配层不含 !important（不靠权重硬压组件样式）", "!important" not in CSS)

# ════════════════════════════════════════════════════ B. 实测 ════════════════════════════════
for step in ("mounted", "boxes", "rel", "avail", "css", "drawer", "drawerClosed", "wide"):
    chk("B0-%s" % step, "实测步骤 %s 已采集且无解析错误" % step,
        step in P and "__parse_error__" not in P[step])

M = P["mounted"]
chk("B1", "主内容已挂载：host/ready/4 卡/3 行卡/8 链接/抽屉触发器齐备",
    M["host"] and M["ready"] == "1" and M["cards"] == 4 and M["rows"] == 3
    and M["links"] == 8 and M["trigger"],
    json.dumps(M, ensure_ascii=False))

R = P["rel"]
chk("B2", "内容宽 860px（用户要求）+ 整页高 1200（= 设计稿整页）",
    R["main"] == [0, 0, 860, 1200], "main=%s" % R["main"])
chk("B3", "头部容器 860×110（设计 110）", R["head"] == [0, 0, 860, 110], "head=%s" % R["head"])
chk("B4", "页分隔线 y130 高 1（设计 y130）", R["rule"] == [0, 130, 860, 1], "rule=%s" % R["rule"])
chk("B5", "卡片网格 y150 高 600（2×292 + 行距 16）", R["grid"] == [0, 150, 860, 600], "grid=%s" % R["grid"])
chk("B6", "底部三行卡 y766 高 386（3×118 + 2×16）", R["rows"] == [0, 766, 860, 386], "rows=%s" % R["rows"])
chk("B7", "页脚 y1184 高 16 宽 240（设计 y1184）", R["foot"] == [310, 1184, 240, 16], "foot=%s" % R["foot"])
chk("B8", "四张卡 422×292，列距 16 / 行距 16（y150 与 y458 两行）",
    R["cards"] == [[0, 150, 422, 292], [438, 150, 422, 292],
                   [0, 458, 422, 292], [438, 458, 422, 292]],
    "cards=%s" % R["cards"])
chk("B9", "三张行卡 y766 / y900 / y1034 各 118 高（间距 16）",
    R["rowboxes"] == [[0, 766, 860, 118], [0, 900, 860, 118], [0, 1034, 860, 118]],
    "rowboxes=%s" % R["rowboxes"])
chk("B10", "卡头紧贴卡体（卡体 y = 卡头 y + 卡头高；卡头 36~37 含 DS 1px 底纹）",
    R["h1"][1] == 151 and R["h1"][3] in (36, 37) and R["b1"][1] == R["h1"][1] + R["h1"][3],
    "h1=%s b1=%s" % (R["h1"], R["b1"]))
chk("B11", "第二列卡头与第一列同 y（两列等高对齐）",
    R["h2"][1] == R["h1"][1] and R["h2"][3] == R["h1"][3], "h2=%s" % R["h2"])

BX = P["boxes"]
chk("B12", "头部右侧动作区右贴齐内容右边界，且头像是 104×104",
    BX["actions"][0] + BX["actions"][2] == BX["main"][0] + BX["main"][2]
    and BX["avatar"][2] == 104 and BX["avatar"][3] == 104,
    "actions=%s main=%s avatar=%s" % (BX["actions"], BX["main"], BX["avatar"]))
chk("B13", "头部文案区左边界 = 头像右边界 + gap 20（104+20=124）",
    BX["nameRow"][0] - BX["main"][0] == 124, "d=%d" % (BX["nameRow"][0] - BX["main"][0]))

C = P["css"]
chk("B14", "实测计算样式：max-width 860px / 实宽 860 / 白底 / 圆角 4 / 描边 #F2F2F2",
    C["maxWidth"] == "860px" and C["width"] == 860
    and C["bgCard"] == "rgb(255, 255, 255)" and C["radiusCard"] == "4px"
    and C["cardBorder"] == "rgb(242, 242, 242)",
    json.dumps(C, ensure_ascii=False))
chk("B15", "容器可用宽 860 不溢出外壳（外壳宽 %d，左右内边距 24）" % P["avail"]["parentW"],
    P["avail"]["mainW"] == 860 and P["avail"]["parentW"] >= 860,
    json.dumps(P["avail"], ensure_ascii=False))

D = P["drawer"]
chk("B16", "头部触发器可唤起右侧对话抽屉，且与详情页右栏同盒 [952,48,480,844]",
    D["open"] is True and D["box"] == [952, 48, 480, 844], json.dumps(D, ensure_ascii=False))
chk("B17", "Esc 可关闭抽屉", P["drawerClosed"]["open"] is False)

W = P["wide"]
chk("B18", "1920 宽视口下内容仍为 860（max-width 生效、不随视口拉伸）",
    W["main"][2] == 860 and W["grid"][2] == 860 and W["rows"][2] == 860,
    json.dumps(W, ensure_ascii=False))

# ════════════════════════════════════════════════════ C. 幂等 ════════════════════════════════
before = rd("pages/avatar.html")
try:
    pr = subprocess.run([PY, os.path.join(ROOT, "mg-work", "r35", "build-avatar-main.py")],
                        capture_output=True, text=True, encoding="utf-8", errors="replace",
                        env=dict(os.environ, PYTHONIOENCODING="utf-8"), timeout=300)
    after = rd("pages/avatar.html")
    chk("C1", "复跑生成源幂等（页面内容零变化，可升级/可重放）",
        pr.returncode == 0 and before == after,
        "rc=%s len %d→%d" % (pr.returncode, len(before), len(after)))
except Exception as e:
    chk("C1", "复跑生成源幂等（页面内容零变化，可升级/可重放）", False, str(e))

# ════════════════════════════════════════════════════ 汇总 ════════════════════════════════
print("=" * 96)
print("pages/avatar.html  %d chars" % len(AV))
print("PASS %d / TOTAL %d" % (len(PASS), len(PASS) + len(FAIL)))
if FAIL:
    for f in FAIL:
        print("  FAIL %s" % f)
print("RESULT: %s" % ("ALL_OK" if not FAIL else "HAS_FAIL(%d)" % len(FAIL)))
print("=" * 96)
sys.exit(0 if not FAIL else 1)

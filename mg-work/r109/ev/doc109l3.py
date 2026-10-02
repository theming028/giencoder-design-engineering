# -*- coding: utf-8 -*-
u"""r109 第三拍收尾：把「邵先生三条」同步进记忆文档。

范围（同步的是「已落地未提交」态，不是「已推送」态）：
  1) .workbuddy/memory/HANDOFF.md   —— L4 时间戳 + 顶部插入「最新一拍 = r109 第三拍」块（第二拍降级为
                                      「上一拍（同代）」）+ §二·i 标题改「共三拍」+ §二·i 追加「第三拍」节
                                      + §六 加 53~57 + §七 状态行改「第一 / 二 / 三拍」+ §八 回滚段补 E10 与主题层
  2) .workbuddy/memory/PAGES.md     —— P3.11i 标题 + 固定事实表追加 4 行 + 必看清单追加 32~37
  3) .workbuddy/memory/PLAYBOOK.md  —— 附录前插入 **P3.58**（九条新教训）+ 附录标题「106 条」→「115 条」
                                      + 附录追加 107~115 九条
  4) .workbuddy/memory/MEMORY.md    —— 追加 r109 第三拍段
  5) 两份当日日志 **2026-10-02.md**（仓库内 + 工作区）—— 追加 r109 第三拍段
  6) .workbuddy/memory/MEMORY.md（**工作区**那份，3000 字符限额）—— 在限额内更新「最近拍」+ 两处计数

★ 幂等设计：**mark 一律取 new**（`new` 天然「改后才存在」）。
★ 「mark 歧义」硬断言：mark 与 old **同时**存在 ⇒ 只可能 mark 不唯一 ⇒ `sys.exit`；
  豁免位判据 = `old in new`。
★ `old` 允许是 **编译后的正则**（用于「整行替换」这类锚点太长的场景）。
★ 用法： python mg-work/r109/ev/doc109l3.py           # 写（连跑两遍验幂等：第二遍应「应用 0 / 跳过 N」）
        python mg-work/r109/ev/doc109l3.py --check    # 只校验锚点命中数 + 工作区字符预算（不写）
⚠ 正文里有百分号 / 花括号 / 反斜杠 这类字符 ⇒ 不用百分号格式化 / .format()，改用 @WHEN@ 占位符替换。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

WHEN = u'2026-10-02 11:5x'

MEMDIR = os.path.join(REPO, '.workbuddy', 'memory')
HOF = os.path.join(MEMDIR, 'HANDOFF.md')
PAG = os.path.join(MEMDIR, 'PAGES.md')
PBK = os.path.join(MEMDIR, 'PLAYBOOK.md')
MEM = os.path.join(MEMDIR, 'MEMORY.md')
LOG_REPO = os.path.join(MEMDIR, '2026-10-02.md')
LOG_WS = os.path.join(WS, '.workbuddy', 'memory', '2026-10-02.md')
WSMEM = os.path.join(WS, '.workbuddy', 'memory', 'MEMORY.md')

WSMEM_BUDGET = 3000          # ★ 工作区 MEMORY.md 限额（超了会被截断注入 ⇒ 等于没写）

APPLIED, SKIPPED, BAD = [], [], []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = u'\r\n' if u'\r\n' in raw else u'\n'
    return raw.replace(u'\r\n', u'\n'), nl


def wr(p, t, nl):
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(p, 'wb').write(t.replace(u'\n', nl).encode('utf-8'))


def subst(s):
    return s.replace(u'@WHEN@', WHEN)


def _hit(t, old):
    """old 可以是 str 或编译后的正则；返回 (命中次数, 待替换显示串)。"""
    if isinstance(old, re.Pattern):
        ms = old.findall(t)
        return len(ms), (ms[0] if ms else u'')
    return t.count(old), old


def _rep(t, old, new):
    if isinstance(old, re.Pattern):
        return old.sub(lambda m: new, t, count=1)
    return t.replace(old, new, 1)


def patch(p, steps, label):
    u"""steps = [(old, new, sub)]；old=None ⇒ 尾部追加（文件不存在则新建）。"""
    if not os.path.exists(p):
        if CHECK:
            BAD.append(u'%s：文件不存在' % label)
            return
        wr(p, u'', u'\n')
    t, nl = rd(p)
    for step in steps:
        old, new, sub = step[0], step[1], step[2]
        new = subst(new)
        mark = new                       # ★ mark == new（唯一来源，不手抄）
        keep_anchor = (old is not None) and (not isinstance(old, re.Pattern)) and (old in new)
        if CHECK:
            if old is not None:
                n, _ = _hit(t, old)
                if n != 1:
                    BAD.append(u'%s · %s → 锚点命中 %d 次' % (label, sub, n))
            continue
        if mark and mark in t:
            n_old, _ = _hit(t, old) if old is not None else (0, u'')
            if (not keep_anchor) and n_old:
                sys.exit(u'!! %s · %s：mark 歧义 —— `old` 与 `mark` 同时存在（mark 不唯一）' % (label, sub))
            SKIPPED.append(u'%s · %s' % (label, sub))
            print(u'   跳过  %s · %s（已应用）' % (label, sub))
            continue
        if old is None:
            t = t + new
        else:
            n, shown = _hit(t, old)
            if n != 1:
                sys.exit(u'!! %s · %s：锚点命中 %d 次（应 1 次）\n   old=%r'
                         % (label, sub, n, (shown if len(str(shown)) < 300 else str(shown)[:300])))
            t = _rep(t, old, new)
        APPLIED.append(u'%s · %s' % (label, sub))
        print(u'   %s  %s · %s' % (u'校验' if CHECK else u'应用', label, sub))
    if t is not None and not CHECK:
        wr(p, t, nl)


# ============================================================ 公共文案

R109_L3_TOP = u"""> 🚧 **最新一拍 = r109 第三拍（邵先生三条：批注原点 / 卡片两端对齐 / 全站暗色 · ★★ 同代就地返工 —— 第一 / 二拍尚未提交 ⇒ 按硬规则就地改 `ev/patch109l3.py` 与 `ev/theme/*.py`）** —— **🚫 未提交**（判据 `git status`：10 页 ` M` + `?? mg-work/r109/`）：
> 本拍 = **① 批注「在哪里点就在哪里落」+ 编辑态文案「保存」** / **② `.r93-card` 两端对齐** / **③ 全站暗色（机制层 10 页 + 适配层「基础工作台 5 页」）**。
> ① **唯一原点 = `noteAt`**（本次**真实点击点**、`.td-view` 内容坐标）：锚点 24×24 的**中心**咬住它、气泡**左边缘**对齐它；
>   「**预览批注**」时原点 = **锚点自己**；`noteCtrl()` 收口「编辑态 ⇒ **保存**」。
>   真机（**全真鼠标**）：点击 `880,349` ⇒ **气泡左 − 点击点 = 0**、提交后**锚点中心 = 880,349**、编辑态按钮 =「**保存**」、`taValue` 原文回填。
> ② **`ev/make109.py` 的 EDITS 表新增 E9**：`.r93-card` 的 `width: calc(100% - 18px); margin-left: 18px` ⇒ `width: 100%; margin-left: 0`。
>   真机**全量 12 张** `r93-card`（含 4 张 `--edge`）的 `dLeft` / `marginLeft` **全 0**。
> ③ **暗色**：底座 = DS **早就写好**的 `[giencoder-theme='dark']` 暗色档（已内联 10 页）⇒ 切主题 = 在 `<html>` 上挂/摘一个属性。
>   · **③-a 机制层** `ev/theme/apply-theme.py`（**全站 10 页**）：档位 `light/dark/auto` 存 `localStorage['gi-ui-theme']`、**默认 `auto`（跟随系统）**、首帧前执行、顺带补 `color-scheme`。
>   · **③-b 设置页「外观」接线**：捕获阶段接 `.r85-seg > .giencoder-btn` + 回填 `aria-pressed`。真机七步（**三枚按钮全真鼠标**）：点「深色」⇒ `attr=dark` / `bg1=#17171a` / 外壳 `rgb(23,23,26)`；点「跟随系统」+ `set media dark` ⇒ **自动跟随系统**；reload 后档位保留。
>   · **③-c 适配层** `ev/theme/apply-dark.py`（**基础工作台 5 页**）：收敛五类「不吃 token 的硬值」——① 第二套 shadcn HSL token 层（它排在 DS 之后、**同特异性** ⇒ 它胜出，满屏文字都从 body 继承）② React 写死内联 + 尾风字面色（只能靠 `!important` 压）③ 页面自定义变量（用 **DS 阶梯镜像**：`--gray-N` 浅暗互镜）④ 亮色 hover（暗下会闪白）⑤ 顶栏浅色位图（改 DS token 现画点阵）。
>   · **★★ 护栏**：机制层全局、适配层只有 5 页 ⇒ 机制层读 `<html data-gi-dark="1">`，没有就一律按浅色渲染（**杜绝半暗半亮**；逐页实测 5 页 `supported=True`、另 5 页**即便被请求 dark 也不变**）。
>   · 像素级验收：暗色档亮像素比 **0.9% ~ 3.6%**（浅色档 97.9% ~ 99.3%），残留全部落实到身份（主按钮 = `--giencoderblue-6` 暗档、顶栏点阵 = `--gray-2` 暗档、黄灯点 / 白圆钮 / 滑块刻度 = 刻意保留）。
>   · ★ 页面**自带**的那套非 DS 灰阶 `.dark{}` 块**刻意未用**（邵先生要求色值只来自 DS）。
> ★★ **收尾排障发现并修掉一条真缺陷**：`apply109.py` 的净底自检要求「剥块后不得再出现注入块 id」，而我在暗色块**注释**里写了 `r101-hdr-css` 字面 ⇒ **整条 apply 链断掉**；修好后又暴露第二条：`<html … data-gi-dark="1">` 让它的**逐字** `<html lang="zh-CN">` 锚点失配（还会把护栏**外溢**给 conversation）⇒ 新增 **E10**（属性宽容 + 摘护栏）。详见 `acceptance.md` **二十九节**。
> **门禁**：`check-syntax` **10/10**；`verify-design` 汇总 **76 不变**（差异只有「5 页各 +2 渐变」+ 行号偏移）；`scan-flatten` **仍 2 条**；`patch109l3` 幂等（0/12）；`apply-theme` 10/10、`apply-dark` 5/5 幂等；★★ **整链固定点**：按改序连跑两轮 quickhash 一致，且 `apply109` + 越界清扫往返 **md5 逐字节还原**。
> **产物**：`base.html` **487942**（HEAD +15792）· `avatar` **583882** · `automation` **377488** · `skills` **377375** · `settings` **475014**（各 +15792 = 机制层 4824 + 适配层 10951 + 护栏 17）· `conversation` **1054348**（+29523）· `dev/kanban/req-kanban/task-detail` 各 **+4824**（仅机制层）。
> 逐条实测见 `mg-work/r109/acceptance.md`（**十九 ~ 二十九节**）；机制级教训见 PLAYBOOK **P3.58**；本页固定事实见 PAGES **P3.11i**。
> 🚫 未 commit / 未 push。
> ▸ **上一拍（同代 · 第二拍）= r109 第二拍（五条 + 一条配套 · ★★ 同代就地返工 —— 第一拍尚未提交 ⇒ 按硬规则就地改 `ev/patch109l2.py`）** —— **🚫 未提交**（判据 `git status` 仍是 ` M pages/conversation.html`）："""

# ★ 顶部那行是「整行替换」（锚点太长 ⇒ 用正则）
RE_HOF_TOP2 = re.compile(u'^> 🚧 \\*\\*最新一拍 = r109 第二拍.*$', re.M)

SEC2I_L3 = u"""### 第三拍（r109 第三层补丁 · 邵先生三条 · 2026-10-02 10:2x · **就地返工 `ev/patch109l3.py` + 新建 `ev/theme/*.py`**）

> 需求逐字：①「添加批注的点击触发点与输入批注的容器 "td-elnote" 没有在一个原点，位置漂移太远，需要做到**在哪里点击就在哪里添加**，
> 包括**预览批注**的也是一样，另外**编辑态**时原来的"添加"文案需变为"**保存**"」；②「对话内容中的类似 "r93-card r93-card--edge"
> 这样的容器前面的**缩进都取消**，两端都对齐吧」；③「我需要支持**全局 UI 界面（基础工作台和研发工作台）的暗色模式**，
> 用户可以在**设置页面的"外观"里**去选择…**所有的色值全部要来自 giencoder 设计系统的色彩系统**」。
> ★ 唯一追问（三条决策）：③ 的落地范围 ⇒「**机制层 + 基础工作台 5 页**」；首次进入默认档 ⇒「**跟随系统**」；色值收敛尺度 ⇒「**按需收敛**」。

**落地面**：`part109/panel.js` 84643 → **88077**；`part109/panel.css` **84764（未动）**；`part109/browse.html` **106685（0）**；
`ev/patch109l3.py` 25098 → **29068**；`ev/make109.py` 7629 → **10681**（**+E9 +E10**）；`apply109.py` 191131 → **192105**（3676 行 / **10 处替换**）；
**新建** `ev/theme/apply-theme.py` **9549** / `ev/theme/apply-dark.py` **25406**。
**改序（7 步）**：`part109/panel.js` → `ev/make109.py` → `ev/splice109.py` → `ev/make109.py` → `apply109.py` → `ev/theme/apply-theme.py` → `ev/theme/apply-dark.py`
（★ 后两条**必须最后跑**：`apply109.py` 会从 `base.html` 的净底**重建** `conversation.html`）。

**① 唯一原点**：`noteAt` = 本次**真实点击点**（`.td-view` 内容坐标）；锚点 **24×24 的中心**咬住它、气泡**左边缘**对齐它（水平方向也补了可视带夹取）；
「预览批注」时原点 = 锚点自己；`noteCtrl()` 收口「编辑态 ⇒ **保存**」。
真机（全真鼠标）：点击 `880,349` ⇒ **气泡左 − 点击点 = 0**、提交后**锚点中心 = 880,349**；编辑态按钮 =「**保存**」、`taValue` 原文回填、气泡顶 − 锚点底 = 8。

**② 两端对齐**：E9 只动宽度两项（`calc(100% - 18px)` + `margin-left:18px` ⇒ `100%` + `0`）。
真机**全量 12 张** `r93-card`（含 4 张 `--edge`、1 张 `--quiz`、1 张 `--ctx`）的 `dLeft` / `marginLeft` **全 0**。

**③ 暗色**：底座 = DS 早写好的 `[giencoder-theme='dark']`（已内联 10 页）⇒ 切主题 = 在 `<html>` 上挂/摘属性。
③-a 机制层 10 页、③-b 设置页「外观」接线、③-c 适配层 5 页（「机制层做了、页面却不变色」的**五类真根因**见 `acceptance.md` §22）。
★★ 护栏 = `<html data-gi-dark="1">`（与适配块**同进同出**）⇒ 未适配页即便被请求 dark 也**一律浅色**。
★ 页面自带的非 DS 灰阶 `.dark{}` 块**刻意未用**（邵先生要求色值只来自 DS）。

**门禁**：`check-syntax` 10/10｜`verify-design` 76 不变（差异仅「5 页各 +2 渐变」+ 行号偏移）｜`scan-flatten` 仍 2 条｜
`patch109l3` 0/12｜`apply-theme` 10/10 · `apply-dark` 5/5｜★★ **整链固定点**（连跑两轮 quickhash 一致）+ **往返 md5 逐字节还原**。

**取证资产**：`ev/theme/{scan-dark2.sh, scan-guard.sh, probe-appearance.py, probe-l3.py, chk-net.py}` +
`ev/theme/{p-guard.js, p-verify.js, p-seg.js, p-state.js, p-l3{a,b,c,d}.js}` + `raw/theme/{light,dark}/*.png`。

"""

ITEM53 = u"""53. ★★ **给 `<html>` 加属性会打断下游的「逐字锚点」** —— `apply109.py` 用 `HTML_OLD = '<html lang="zh-CN">'` 逐字匹配；
    护栏写成 `<html lang="zh-CN" data-gi-dark="1">` ⇒ 命中 **0** 次；更危险的是**护栏会随净底外溢**到
    从 base 重建出来的 conversation（未适配页拿到护栏 = 半暗半亮）。
    修法 = **E10**（认文档里**第一个** `<html` 开标签 + 落标记前摘 `data-gi-dark`）。见 `acceptance.md` §29.2。
54. ★★★ **往产物里写注释时，先想「有没有别的层拿这个 token 当判据」** —— `apply109.py` 的净底自检要求剥块后
    不得再出现 `r101-hdr-css` 等注入块 id 的**字面**；我在暗色块**注释**里写了它 ⇒ **整条 apply 链当场退出**。见 §29.1。
55. ★★ **机制层与适配层覆盖范围不同 ⇒ 必须设护栏** —— 机制层全局、适配层只有 5 页 ⇒ 未适配页切暗会「token 翻暗、外壳仍浅」。
    护栏取 **`<html>` 属性**（**不是**去查 DOM 里的样式块：`<head>` 内**同步执行**时那张表还没解析）。见 §29.3。
56. ★★ **DS 原始色阶浅暗档是严格镜像的**（`--gray-N` 浅 ↔ `--gray-(11−N)` 暗，本拍逐值核实 10 对）⇒ 页面里踩在某个阶梯步上的
    **字面值**，暗色档写 `rgb(var(--gray-N))` 就自动得到同一步阶的镜像亮度：可证、可核、浅色零风险。见 §25.1。
57. ★★ **`agent-browser` 的输出绝不能接管道**（CLI 把 stdout 交给常驻守护进程 ⇒ 管道永不 EOF ⇒ 命令「挂死」）；
    一律 `subprocess` + **重定向到文件**。另：**注释里的裸 `<` + `style` 会撑破 `check-syntax.py`**（纯文本正则）。见 §29.4 / §29.5。

"""

ITEM53_ANCHOR = u"""    **稿子只给了锚点长相、没给落点** ⇒ 取通行读法（Figma 批注同款）。想换左/右下只需改 `noteDrop()` 的两个 `−12`。
"""

# ---- PLAYBOOK P3.58 ----
PBK_P358 = u"""## P3.58 ★★ r109 第三拍（邵先生三条：批注原点 / 卡片两端对齐 / 全站暗色 · 2026-10-02 10:2x）—— ★★ 九条新教训

**★ 判据速查（本轮实测值）**：① 真鼠标点击 `880,349` ⇒ 气泡左 − 点击点 = **0**、提交后锚点中心 = `880,349`、编辑态按钮 =「保存」；
② 全量 12 张 `r93-card` 的 `dLeft` / `marginLeft` **全 0**；③ 暗色亮像素比 **0.9% ~ 3.6%**（浅色 97.9% ~ 99.3%）；
护栏：5 页 `supported=True` + `attr=dark` + `bg1=#17171a` + 外壳 `rgb(23,23,26)`，另 5 页 `supported=False` 且**底色不变**；
设置页七步：点「深色」⇒ `attr=dark` / `shell=rgb(23,23,26)`；`auto` + `set media dark` ⇒ **自动跟随系统**；reload 后档位保留。

1. ★★★ **`applyNNN.py` 的净底自检盯的是「注入块 id 的**字面**」⇒ 产物里的**注释**也受它管** ——
   往块注释里写 `r101-hdr-css` 这类 id，会让「剥块后不得残留」这条自检炸掉、**整条 apply 链直接退出**（自愈能力归零）。
   ⇒ 写注释时改用「第 92 / 101 两代顶栏装饰块」这种**不含 token 的说法**。
2. ★★★ **同一个陷阱的正则版**：`<html[^>]*>` 这种「全串正则」会被**自己注释里**的 `<html>` 字面命中（本拍报「命中 8 次」）。
   ⇒ 要定位「文档级的唯一节点」，用 **`find` + 位置上限断言**（`_i <= 200`），别用全串正则。
3. ★★★ **给根元素加属性 ⇒ 先查下游有没有「逐字匹配 `<html …>`」的锚点** —— 有 ⇒ 那个锚点会失配，
   而且**新属性会随净底外溢**到从它重建出来的页面（本拍差点把「已适配」护栏外溢给 conversation = 半暗半亮）。
   修法 = 锚点改**属性宽容** + 落自己的标记前**先摘掉外来属性**。见 `acceptance.md` §29.2。
4. ★★★ **机制层与适配层覆盖范围不同 ⇒ 必须设护栏** —— 未适配页切暗会「token 翻暗、外壳仍浅」
   （外壳颜色来自 React 内联 + 尾风字面类，**都不吃 token**）⇒ 近白文字压浅底。
   护栏取 **`<html>` 属性**：`<head>` 内**同步执行**时查不到后面的样式块；夹 `<meta>` 又会破坏邻接剥离正则。
5. ★★ **DS 原始色阶浅暗档是严格镜像的**（`--gray-N` 浅 ↔ `--gray-(11−N)` 暗）
   ⇒ 页面里踩在某个阶梯步上的字面值，暗色档写 `rgb(var(--gray-N))` 即得同一步阶亮度：可证、可核、浅色零风险。
6. ★★ **「第二套 token 层」是最隐蔽的暗色元凶** —— 页面除 DS 外还内联一套 shadcn HSL token，
   其 `body{background-color:hsl(var(--background))}` 与 DS 的**同特异性**且**排在后面** ⇒ 它胜出，
   满屏文字都从 body 继承 ⇒ **只翻 DS token 等于没翻**。修法 = 把这套 token 在暗色档**重指**到 DS 暗色 token（写 HSL 三元组）。
7. ★★ **内联样式只输给「样式表里的 `!important`」** ⇒ React 写死的 `background: rgb(244,245,246)` 这类，
   唯一覆盖手段是 `[style*="…"]` 属性选择器 + `!important`。
   ⚠ 尾风任意类的**真实转义**是 `.hover\\:\\!bg-\\[\\#E9ECEE\\]:hover`（**`!bg` 不是 `bg`**）。
8. ★★★ **给「谁被改了」留一个能被工具独立数出来的特征** —— 本拍 `verify-design.py` 的**逐页渐变计数**
   精准地只在被注入的那 5 页各 **+2**（我新增 1 组 `linear-gradient` + 1 组 `radial-gradient`）
   ⇒ 用它给「适配层只落 5 页」做了**第二次独立证明**。比只靠自己的探针可信。
9. ★★ **幂等的判据要给「链」而不是给「单步」** —— 本拍 `apply109` **单独**不是固定点（每轮都会把适配块从
   base 的净底带进 conversation），但**改序的整链**是固定点（连跑两轮 quickhash 一致），
   且末步的**越界清扫**让「适配块只存在于被适配页」恒成立、往返**逐字节无损**（md5 还原）。
   ⇒ 文档里必须写清「**固定点属于哪一段**」。

**★ 门禁（本轮）**：`check-syntax` **10/10**；`verify-design` 汇总 **76 不变**；`scan-flatten` **仍 2 条**；
`patch109l3` 幂等（0/12）；`apply-theme` 10/10、`apply-dark` 5/5；★★ 整链固定点 + 往返 md5 逐字节还原。

"""

# ---- PAGES ----
PAGES_ROWS = u"""| **`.td-anchor` / `.td-elnote` 的「原点」** | ★★★ **r109 第三拍 ①**：唯一原点 = **`noteAt`**（本次**真实点击点**、`.td-view` 内容坐标）。锚点 24×24 的**中心**咬住它；气泡**左边缘**对齐它（水平方向也要做**可视带夹取**）；**「预览批注」时原点 = 锚点自己**。真机（真鼠标）：点击 `880,349` ⇒ 气泡左 − 点击点 = **0**、提交后锚点中心 = **`880,349`**。 |
| **`.td-elnote-ok` 的文案（新增 vs 编辑）** | ★★ **r109 第三拍 ①**：`noteCtrl(on)` 里**统一收口** —— `noteCur` 查得到（= 编辑态）⇒ 恒为「**保存**」。⚠ 别只在 `noteEdit()` 里写一次，否则「编辑态下按一下 Ctrl」会翻回「添加」。真机：真鼠标点开已存在锚点 ⇒ 按钮 =「保存」、`cancel` display = `flex`。 |
| **`.r93-card` 的宽度（★ 已两端对齐）** | ★★ **r109 第三拍 ②**：`width: 100%; margin-left: 0`（原 `calc(100% - 18px)` + `18px`）。★★ 落点 = **`ev/make109.py` 的 `EDITS` 表 E9**（`apply109.py` 是生成物）。⚠ 只动宽度两项；`.r93-card--full` 保留（显式满宽的语义声明）。真机**全量 12 张** `dLeft` / `marginLeft` **全 0**。 |
| **全站暗色：机制层 / 适配层 / 护栏** | ★★★ **r109 第三拍 ③**：机制层 `ev/theme/apply-theme.py`（**10 页**，档位 `light/dark/auto` 存 `localStorage['gi-ui-theme']`、**默认 auto**）；适配层 `ev/theme/apply-dark.py`（**基础工作台 5 页**，作用域 `html[giencoder-theme='dark']:not([data-r93-page])`）；**护栏 = `<html data-gi-dark="1">`**（与适配块同进同出）⇒ 未适配页即便被请求 dark 也**一律浅色**。★ 页面自带的**非 DS 灰阶** `.dark{}` 块**刻意未用**。 |
"""

PAGES_MUST = u"""
32. ★★★ **往产物里写注释前，先想「有没有别的层拿这个 token 当判据」** —— r109 在暗色块注释里写了注入块 id 的**字面**，
    `apply109.py` 的净底自检当场判「残留标记」并退出，**整条 apply 链断掉**。见 PLAYBOOK **P3.58①**。
33. ★★★ **给根元素（`<html>`）加属性 ⇒ 先查下游有没有「逐字匹配 `<html …>`」的锚点** —— 有 ⇒ 那个锚点会失配，
    且新属性会**随净底外溢**到从它重建的页面（r109：差点把「已适配」护栏外溢给 conversation = 半暗半亮）。见 **P3.58③**。
34. ★★★ **机制层与适配层覆盖范围不同 ⇒ 必须设护栏**（未适配页切暗会「token 翻暗、外壳仍浅」）；护栏取 **`<html>` 属性**
    （`<head>` 内同步执行时查不到后面的样式块；夹 `<meta>` 会破坏邻接剥离正则）。见 **P3.58④**。
35. ★★ **DS 原始色阶浅暗档严格镜像**（`--gray-N` 浅 ↔ `--gray-(11−N)` 暗）⇒ 踩在阶梯步上的字面值直接写 `rgb(var(--gray-N))`。见 **P3.58⑤**。
36. ★★ **「第二套 token 层」是最隐蔽的暗色元凶**：与 DS 的 `body{}` **同特异性**且**排在后面** ⇒ 它胜出，满屏文字都从 body 继承。见 **P3.58⑥**。
37. ★★ **幂等的判据要给「链」不给「单步」** —— r109 的 `apply109` 单独不是固定点，但**改序整链**是（连跑两轮 quickhash 一致），
    且末步越界清扫让「适配块只存在于被适配页」恒成立、往返 md5 逐字节还原。见 **P3.58⑨**。
"""

PAGES_MUST_ANCHOR = u"""26. ★★ **改「`--ui-fs` 杠杆下要跟着变的尺寸」时**"""

# ---- MEMORY.md（仓库）----
MEM_L3 = u"""
### r109 第三拍（邵先生三条：批注原点 / 卡片两端对齐 / 全站暗色 · 同日 10:2x · **就地返工 `ev/patch109l3.py` + 新建 `ev/theme/*.py`**）—— 🚫 未提交

> ① **批注「在哪里点就在哪里落」**：唯一原点 = `noteAt`（本次**真实点击点**、`.td-view` 内容坐标）；锚点 **24×24 的中心**咬住它、
>   气泡**左边缘**对齐它（水平方向也补了可视带夹取）；**预览批注**时原点 = 锚点自己；`noteCtrl()` 收口「编辑态 ⇒ **保存**」。
>   真机（全真鼠标）：点击 `880,349` ⇒ **气泡左 − 点击点 = 0**、提交后**锚点中心 = 880,349**、编辑态按钮 =「保存」、`taValue` 原文回填。
> ② **`.r93-card` 两端对齐**：E9（落点 = `ev/make109.py` 的 `EDITS` 表）只动宽度两项 ⇒ 真机**全量 12 张** `dLeft` / `marginLeft` **全 0**。
> ③ **全站暗色**：底座 = DS 早写好的 `[giencoder-theme='dark']`（已内联 10 页）⇒ 切主题 = 在 `<html>` 挂/摘属性。
>   ③-a 机制层（10 页 / 档位 `light,dark,auto` / **默认 auto 跟随系统** / 补 `color-scheme`）；③-b 设置页「外观」接线（捕获阶段 + 回填 `aria-pressed`，真机七步全过）；
>   ③-c 适配层（**基础工作台 5 页**）收敛五类「不吃 token 的硬值」：第二套 shadcn HSL 层 / React 内联 + 尾风字面色 / 页面自定义变量（**DS 阶梯镜像**）/ 亮色 hover / 顶栏浅色位图。
>   ★★ **护栏** `<html data-gi-dark="1">`（与适配块同进同出）⇒ 未适配页即便被请求 dark 也**一律浅色**（逐页实测 5 真 / 5 否）。
>   ★ 页面自带的**非 DS 灰阶** `.dark{}` 块**刻意未用**（邵先生要求色值只来自 DS）。像素级：暗色亮像素 **0.9% ~ 3.6%**、残留全部落实身份。
> ★★ **收尾排障修掉一条真缺陷**：暗色块**注释**里的 `r101-hdr-css` 字面撑破了 `apply109.py` 的净底自检 ⇒ **整条 apply 链断掉**；
>   修好后又暴露 `<html … data-gi-dark="1">` 打断它的**逐字** `<html lang="zh-CN">` 锚点（且护栏会**外溢**给 conversation）⇒ 新增 **E10**（属性宽容 + 摘护栏）。
> **九条坑** = **P3.58**。**门禁**：`check-syntax` 10/10｜`verify-design` **76 不变**（差异仅「5 页各 +2 渐变」）｜`scan-flatten` 仍 2 条｜
>   `patch109l3` 0/12｜`apply-theme` 10/10 · `apply-dark` 5/5｜★★ **整链固定点**（连跑两轮 quickhash 一致）+ **往返 md5 逐字节还原**。
> **产物**：`base` **487942** · `avatar` **583882** · `automation` **377488** · `skills` **377375** · `settings` **475014**（各 +15792）
>   · `conversation` **1054348**（+29523）· `dev/kanban/req-kanban/task-detail` 各 +4824；`acceptance.md` **二十九节**。
> 🚫 未 commit / 未 push。
"""

# ---- 当日日志 ----
LOG_L3_REPO = u"""
### r109 第三拍（邵先生三条 · 10:2x · 就地返工 `ev/patch109l3.py` + 新建 `ev/theme/*.py`）—— 🚫 未提交

- 三条全部落地 + 真机取证：① 批注**唯一原点** `noteAt`（本次真实点击点）—— 锚点中心咬它、气泡左边缘对齐它、预览态以锚点为原点、
  编辑态文案「保存」；真机（真鼠标）点击 `880,349` ⇒ `气泡左−点击点 = 0`、提交后锚点中心 `880,349`。
  ② `.r93-card` 取消 18px 左缩进 ⇒ 两端对齐（E9，落点 = `ev/make109.py` 的 EDITS 表）；真机**全量 12 张** `dLeft`/`marginLeft` 全 0。
  ③ **全站暗色**（邵先生定范围 = 机制层 + 基础工作台 5 页、默认档 = 跟随系统、尺度 = 按需收敛）：
  机制层 `ev/theme/apply-theme.py`（10 页）+ 设置页「外观」接线 + 适配层 `ev/theme/apply-dark.py`（5 页，收敛五类硬值）。
- ★★ **护栏** `<html data-gi-dark="1">`（与适配块同进同出）⇒ 未适配页即便被请求 dark 也一律浅色（逐页实测 5 真 / 5 否）；
  ★ 页面自带的**非 DS 灰阶** `.dark{}` 块刻意未用（色值只来自 DS）。像素级：暗色亮像素 **0.9% ~ 3.6%**（浅色 97.9% ~ 99.3%）。
- ★★ **收尾排障修掉一条真缺陷**：暗色块**注释**里的 `r101-hdr-css` 字面撑破 `apply109.py` 的净底自检 ⇒ **整条 apply 链断掉**；
  修好后暴露第二条：`<html … data-gi-dark="1">` 打断它的逐字 `<html lang="zh-CN">` 锚点、且护栏会**外溢**给 conversation
  ⇒ 新增 **E10**（属性宽容 + 落标记前摘护栏）。往返 md5 **逐字节还原**（`55a1f9a3135e3522c8fe0b893a791367`）。
- 门禁：`check-syntax` 10/10｜`verify-design` **76 不变**（差异仅「5 页各 +2 渐变」+ 行号偏移）｜`scan-flatten` 仍 2 条｜
  `patch109l3` 幂等 0/12｜`apply-theme` 10/10 · `apply-dark` 5/5｜★★ **整链固定点**（连跑两轮 quickhash 一致）。
- 产物：`part109/panel.js` **88077** / `panel.css` **84764（未动）** / `browse.html` **106685（0）** / `ev/make109.py` **10681** /
  `apply109.py` **192105**（3676 行 / 10 处替换）/ `ev/theme/apply-theme.py` **9549** / `apply-dark.py` **25406**。
  `pages/`：base **487942** · avatar **583882** · automation **377488** · skills **377375** · settings **475014**（各 +15792）
  · conversation **1054348**（+29523）· dev/kanban/req-kanban/task-detail 各 +4824。
- 九条机制级教训沉淀为 PLAYBOOK **P3.58**；固定事实进 PAGES **P3.11i**（+4 行 + 必看 32~37）；`acceptance.md` 续到 **二十九节**。
- 记忆同步脚本 = `mg-work/r109/ev/doc109l3.py`。🚫 未 commit / 未 push。
"""

LOG_L3_WS = u"""
## r109 第三拍（10:2x · 就地返工 `ev/patch109l3.py` + 新建 `ev/theme/*.py`）—— 🚫 未提交

三条全部落地并真机取证：① 批注**唯一原点** `noteAt`（真实点击点）—— 气泡左边缘对齐它、锚点中心咬它、编辑态文案「保存」；
② `.r93-card` 两端对齐（E9 = `ev/make109.py` 的 EDITS 表；全量 12 张 dLeft/marginLeft 全 0）；
③ **全站暗色**：机制层 10 页（档位 light/dark/**auto 默认跟随系统**）+ 设置页「外观」接线 + 适配层 5 页（收敛五类不吃 token 的硬值）。
★★ 护栏 `<html data-gi-dark="1">` ⇒ 未适配页即便被请求 dark 也一律浅色；★ 页面自带的非 DS 灰阶 `.dark{}` 刻意未用。
像素级：暗色亮像素 **0.9% ~ 3.6%**（浅色 97.9% ~ 99.3%）。
★★ 收尾修掉一条真缺陷：暗色块注释里的 `r101-hdr-css` 字面撑破 `apply109.py` 的净底自检 ⇒ 整条 apply 链断掉；
再加 `<html … data-gi-dark="1">` 打断它的逐字锚点 + 护栏外溢 ⇒ 新增 **E10**。往返 md5 逐字节还原。
门禁全绿（10/10 · verify-design 76 不变 · scan-flatten 仍 2 条 · 整链固定点两轮一致）。
产物 `conversation.html` **1054348**（+29523）。教训沉淀 PLAYBOOK **P3.58**；`acceptance.md` **二十九节**。🚫 未 commit。
"""

# ---- 工作区 MEMORY.md ----
WSMEM_OLD = u"""## 三、最近拍

- **r107**＝`e9c9498`；**r108 十二 ~ 十九拍**＝✅ `172e580`（已封板 ⇒ 再改右栏须新建 r109）。
- **r109 一 / 二拍**（🚫 未提交 · 右栏批注链路）：一拍＝删灰带 / 标注条贴顶 / 批注钮转红 / `td-elnote` 三稿逐像素。二拍＝右栏展开 ⇒ `zd-host` 折胶囊（盯 `.av-browse-on`）· 终端全 **13px** · `regen` 图标重画（落点 = **`make109.py` 的 `EDITS` 表**）· 锚点**点开 = 编辑态详情 / 可任意拖**（拖到底角 ⇒ 补气泡可视带夹取）。产物 **1045713 字符**；`acceptance.md` **十八节**。
- 新红线：**归零判据先剥三类注释**；**`sticky top` 只在滚动容器首子件之前才追得上**；**隐藏元素量不出几何**；**`applyNNN.py` 是生成物 ⇒ 图标类改动落 `makeNNN.py` 的 `EDITS` 表**；**反解判据看坏格数、不看总 err**；**加可拖件必查祖先 `overflow`**。
"""

WSMEM_NEW = u"""## 三、最近拍

- **r107**＝`e9c9498`；**r108 十二 ~ 十九拍**＝✅ `172e580`（已封板 ⇒ 再改右栏须新建 r109）。
- **r109 一 / 二 / 三拍**（🚫 未提交）：右栏批注链路已完成；三拍＝批注**唯一原点 `noteAt`**（编辑态文案「保存」）· `.r93-card` **两端对齐**（E9）· **全站暗色**（`ev/theme`：机制 10 页 / 适配 5 页 + 护栏；默认**跟随系统**）。产物 `conversation` **1054348**；`acceptance.md` **二十九节**。
- 新红线：**归零判据先剥三类注释**；**`sticky top` 只在滚动容器首子件之前才追得上**；**隐藏元素量不出几何**；**`applyNNN.py` 是生成物 ⇒ 改动落 `makeNNN.py` 的 `EDITS` 表**；**反解判据看坏格数、不看总 err**；**加可拖件必查祖先 `overflow`**；★★ **产物注释也受「别的层」判据管**（写注入块 id 字面 ⇒ 下游净底自检炸）；**根元素加属性会打断下游逐字锚点、随净底外溢**；**机制 / 适配层覆盖不同 ⇒ 必须设护栏**；**`agent-browser` 输出禁接管道**。
"""

# ★ 3000 字符限额的腾位压缩（「最近拍」块长了不少 ⇒ 必须从别处等量腾出）。
#   ⚠ 只删冗余字词 / 只删「HANDOFF·PLAYBOOK 里有全文」的复述，**不动任何一条判断口径**；
#     判据 = 脚本末尾的限额硬断言（`WSMEM_BUDGET`）。
#   ⚠⚠ 压缩项**不允许 new=''**：`patch()` 的幂等判据 = `new in t`，空串永远「未应用」⇒ 第二遍必炸。
#   ⚠⚠ 压缩项**不允许 `new` 是 `old` 的子串**：`patch()` 会判「mark 与 old 同时存在 ⇒ mark 歧义」并
#      `sys.exit`（本拍真踩：`两者都污染工作区` → `都污染工作区`）⇒ 这类只能整行重写。
#   ⚠ 「最近拍」那两行的压缩**已并入 `WSMEM_NEW`**（整块替换），**不要**再写成逐行压缩项：
#      逐行项要按 `WSMEM_NEW.split('\n')[i]` 取索引 ⇒ 极易数错行（本拍真踩：漏看了 r107 行，
#      把 r107 行覆盖掉、红线行变两行）⇒ **长块一律整块替换 + 肉眼核行数**。
WSMEM_TIGHTEN = [
    # —— 零碎腾位（口径一字不动，只删冗余字词）
    (u'> 本文件限额 **3000 字符** ⇒ 只留 Windows 速记 + 红线索引 + 最近拍。',
     u'> 限额 **3000 字符** ⇒ 仅 Windows 速记 + 红线索引 + 最近拍。'),
    (u'blob 存 LF、工作区落 CRLF', u'blob LF / 工作区 CRLF'),
    (u'- ⚠ `agent-browser` **不在 PATH** ⇒ 走绝对路径（P3.21）；', u'- ⚠ `agent-browser` **不在 PATH** ⇒ 绝对路径；'),
    (u'★★ **输出禁接管道**（会挂死）⇒ 重定向到文件。', u'★★ **输出禁接管道** ⇒ 重定向到文件。'),
    (u'（用 Python 打片段）', u'（Python 打片段）'),
]

# ---- 工作区 MEMORY.md 的两处计数 ----
WSMEM_HDR_OLD = u"> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.57** + 附录「工作区速览 106 条」·"
WSMEM_HDR_NEW = u"> `HANDOFF.md` 状态/待办（**新会话先读**，每轮覆盖）· `PLAYBOOK.md` 铁律 **P3.1→P3.58** + 附录「工作区速览 115 条」·"
WSMEM_SEC_OLD = u"## 二、红线索引（完整 106 条见仓库 PLAYBOOK 附录）"
WSMEM_SEC_NEW = u"## 二、红线索引（完整 115 条见仓库 PLAYBOOK 附录）"


# ---------------------------------------------------------------- 各文件

def do_handoff():
    print(u'== HANDOFF.md ==')
    patch(HOF, [
        (u'> 最后更新：2026-10-02 10:2x（**★ r109 第二拍已落地',
         u'> 最后更新：@WHEN@（**★ r109 第三拍已落地',
         u'L4 时间戳'),
        (RE_HOF_TOP2, R109_L3_TOP, u'顶部：插入第三拍块 + 第二拍降级'),
        (u'## 二·i ★★ r109（会话详情页右栏「批注链路四件重做」+ 第二拍「五条 + 一条配套」· 2026-10-02 08:5x 起 · **共两拍**）—— **🚫 未提交**',
         u'## 二·i ★★ r109（会话详情页右栏「批注链路四件重做」+ 第二拍「五条 + 一条配套」+ 第三拍「批注原点 / 卡片对齐 / 全站暗色」· 2026-10-02 08:5x 起 · **共三拍**）—— **🚫 未提交**',
         u'§二·i 标题'),
        (u'## 三、r88 ~ r92 做了什么（前情提要）',
         SEC2I_L3 + u'## 三、r88 ~ r92 做了什么（前情提要）',
         u'§二·i 追加第三拍'),
        (u'### r109 新增（5 条，均需邵先生点头）',
         u'### r109 新增（10 条，均需邵先生点头）',
         u'§六 标题计数'),
        (ITEM53_ANCHOR, ITEM53_ANCHOR + ITEM53, u'§六 追加 53~57'),
        (u'   **`r109` 第一 / 二拍 —— 🚫 未提交**（`git status` = ` M pages/conversation.html` + `?? mg-work/r109/`）。',
         u'   **`r109` 第一 / 二 / 三拍 —— 🚫 未提交**（`git status` = 10 页 ` M` + `?? mg-work/r109/`）。',
         u'§七 状态行'),
        (u'# ★ 第二拍（r109-l2）回滚：重跑 ev/patch109l2.py 前的 ev/bak-l2/{panel.css,panel.js}.before（连跑两遍验幂等）',
         u'# ★ 第二拍（r109-l2）回滚：重跑 ev/patch109l2.py 前的 ev/bak-l2/{panel.css,panel.js}.before（连跑两遍验幂等）\n'
         u'# ★ 第三拍（r109-l3 / 主题层）回滚：\n'
         u'#   （a）会话详情页那条：重跑 ev/patch109l3.py 前的 ev/bak-l3/{panel.js,make109.py,patch109l2.py}.before（连跑两遍验幂等）\n'
         u'#   （b）主题层（全站 10 页）：python mg-work/r109/ev/theme/apply-dark.py --revert && python mg-work/r109/ev/theme/apply-theme.py --revert\n'
         u'#   ⚠ 主题层是本代新增的**正交**一条链（只碰产物、不走 make109 的 EDITS 表）\n'
         u'#   ⚠ E10 改了生成器 ⇒ 回滚后必须重跑 ev/make109.py 再跑 apply109.py',
         u'§八 回滚段'),
    ], u'HANDOFF')


def do_pages():
    print(u'== PAGES.md ==')
    patch(PAG, [
        (u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 ~ 十九拍** + **r109 第一拍「批注链路四件重做」** + **r109 第二拍「五条 + 一条配套」** · 复刻 Codex 右栏 · 2026-10-01 / 10-02 · **共二十一拍**）',
         u'### P3.11i ★★ 会话详情页「侧栏模块标签化」（r107 十一拍 + **r108 十二 ~ 十九拍** + **r109 第一拍「批注链路四件重做」** + **r109 第二拍「五条 + 一条配套」** + **r109 第三拍「批注原点 / 卡片对齐 / 全站暗色」** · 复刻 Codex 右栏 · 2026-10-01 / 10-02 · **共二十二拍**）',
         u'P3.11i 标题'),
        (u'**⚠ 改这一块之前必看**',
         PAGES_ROWS + u'**⚠ 改这一块之前必看**',
         u'固定事实表 +4 行'),
        (PAGES_MUST_ANCHOR,
         PAGES_MUST + u'\n' + PAGES_MUST_ANCHOR,
         u'必看清单 32~37'),
    ], u'PAGES')


def do_playbook():
    print(u'== PLAYBOOK.md ==')
    patch(PBK, [
        (u'## 附：工作区速览 106 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         PBK_P358 + u'## 附：工作区速览 115 条（原 `E:/GienCoder/.workbuddy/memory/MEMORY.md` 的一行版）',
         u'插入 P3.58 + 附录计数'),
        (None,
         u"""
107. ★★★ **`applyNNN.py` 的净底自检盯的是「注入块 id 的**字面**」⇒ 产物里的注释也受它管** —— 往块注释里写 `r101-hdr-css` 这类 id，会让「剥块后不得残留」自检炸掉、**整条 apply 链退出**（r109 真踩）。改用「第 92 / 101 两代顶栏装饰块」这种不含 token 的说法。
108. ★★★ **「文档级唯一节点」要定位就用 `find` + 位置上限断言，别用全串正则** —— `<html[^>]*>` 会被**自己注释里**的 `<html>` 字面命中（r109 报「命中 8 次」）。
109. ★★★ **给根元素加属性 ⇒ 先查下游的「逐字 `<html …>` 锚点」** —— 会失配，且新属性会**随净底外溢**（r109：差点把「已适配」护栏外溢给 conversation）。修法 = 锚点属性宽容 + 落自己标记前先摘外来属性。
110. ★★★ **机制层与适配层覆盖不同 ⇒ 必须设护栏** —— 未适配页切暗 =「token 翻暗、外壳仍浅」（外壳用 React 内联 + 尾风字面类，都不吃 token）；护栏取 `<html>` 属性（`<head>` 内同步执行查不到后面的样式块）。
111. ★★ **DS 原始色阶浅暗档严格镜像**（`--gray-N` 浅 ↔ `--gray-(11−N)` 暗）⇒ 踩在阶梯步上的字面值写 `rgb(var(--gray-N))` 即得镜像亮度，可证、浅色零风险。
112. ★★ **「第二套 token 层」是最隐蔽的暗色元凶** —— 与 DS 的 `body{}` 同特异性且排在其后 ⇒ 它胜出，满屏文字都从 body 继承 ⇒ 只翻 DS token 等于没翻。
113. ★★ **内联样式只输给「样式表里的 `!important`」** ⇒ React 写死的颜色只能靠 `[style*="…"]` + `!important` 压。⚠ 尾风任意类的真实转义是 `.hover\\:\\!bg-\\[\\#E9ECEE\\]:hover`（**`!bg` 不是 `bg`**）。
114. ★★★ **给「谁被改了」留一个能被工具独立数出来的特征** —— r109 靠 `verify-design.py` 的**逐页渐变计数**（只在被注入的 5 页各 +2）给「适配层只落 5 页」做了第二次独立证明。
115. ★★ **幂等的判据要给「链」不给「单步」** —— r109 的 `apply109` 单独不是固定点（每轮把适配块带进 conversation），但**改序整链**是（连跑两轮 quickhash 一致），末步越界清扫保证可核契约恒成立、往返 md5 逐字节还原。
""",
         u'附录 +9 条'),
    ], u'PLAYBOOK')


def do_mem():
    print(u'== MEMORY.md（仓库）==')
    patch(MEM, [(None, MEM_L3, u'追加 r109 第三拍段')], u'MEMORY')


def do_logs():
    print(u'== 当日日志 ==')
    patch(LOG_REPO, [(None, LOG_L3_REPO, u'追加 r109 第三拍')], u'日志(仓库)')
    patch(LOG_WS, [(None, LOG_L3_WS, u'追加 r109 第三拍')], u'日志(工作区)')


def do_wsmem():
    print(u'== MEMORY.md（工作区 · 3000 限额）==')
    steps = [
        (WSMEM_HDR_OLD, WSMEM_HDR_NEW, u'头部计数'),
        (WSMEM_SEC_OLD, WSMEM_SEC_NEW, u'红线索引计数'),
        (WSMEM_OLD, WSMEM_NEW, u'最近拍'),
    ]
    for i, (o, n) in enumerate(WSMEM_TIGHTEN, start=1):
        steps.append((o, n, u'腾位压缩 %d' % i))
    patch(WSMEM, steps, u'工作区 MEMORY')
    if not CHECK:
        t, _ = rd(WSMEM)
        if len(t) > WSMEM_BUDGET:
            sys.exit(u'!! 工作区 MEMORY.md = %d 字符 > 限额 %d —— 必须再压' % (len(t), WSMEM_BUDGET))
        print(u'   工作区 MEMORY.md = %d / %d 字符 ✓' % (len(t), WSMEM_BUDGET))


def main():
    do_handoff()
    do_pages()
    do_playbook()
    do_mem()
    do_logs()
    do_wsmem()
    print()
    if CHECK:
        if BAD:
            print(u'!! 锚点校验失败 %d 条：' % len(BAD))
            for b in BAD:
                print(u'   - ' + b)
            sys.exit(1)
        print(u'锚点校验全部通过 ✓（本模式未写入）')
        return
    print(u'应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for s in SKIPPED:
        print(u'   跳过  ' + s)


if __name__ == '__main__':
    main()

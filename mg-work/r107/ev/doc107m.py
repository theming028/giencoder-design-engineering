# -*- coding: utf-8 -*-
u"""r107 交付收尾：把「🚫 未提交」同步成「已推送 e9c9498」。

背景：2026-10-01 14:2x 邵先生发话「commit and push」⇒ 提交 `e9c9498`
（r106 4d081ba + Codex 调研 f13b3bf + r107 十一拍，一次推上去，`de396d0..e9c9498`）。

只动「状态描述」，不回填 acceptance 的当拍体位记录（历史惯例：现场记录保留原样）。

★ 幂等设计（本文件首版连错两次后定的规矩 —— 手抄 mark 必漏字）：
  **mark 不再手写，一律 = new**（`new` 天然只可能「改后才存在」）。
  于是步骤 = 3 元组 `(old, new, sub)`；`old=None` 表示尾部追加。
用法： python ev/doc107m.py            # 写
      python ev/doc107m.py --check    # 只校验锚点命中数（不写）
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
WS = os.path.abspath(os.path.join(REPO, '..'))
CHECK = '--check' in sys.argv

SHA = u'e9c9498'
WHEN = u'2026-10-01 14:2x'

APPLIED, SKIPPED, BAD = [], [], []


def rd(p):
    raw = io.open(p, 'rb').read().decode('utf-8')
    nl = u'\r\n' if u'\r\n' in raw else u'\n'
    return raw.replace(u'\r\n', u'\n'), nl


def wr(p, t, nl):
    io.open(p, 'wb').write(t.replace(u'\n', nl).encode('utf-8'))


def patch(p, steps, label):
    """steps = [(old, new, sub)]；old=None ⇒ 尾部追加；mark 自动取 new。"""
    t, nl = rd(p)
    n0 = len(t)
    for old, new, sub in steps:
        mark = new                       # ★ mark == new（唯一来源）
        if CHECK:
            if old is not None and t.count(old) != 1:
                BAD.append(u'%s · %s → 锚点命中 %d 次' % (label, sub, t.count(old)))
            continue
        if mark and mark in t:
            SKIPPED.append(label + u' · ' + sub)
            continue
        if old is None:                  # 追加
            APPLIED.append(label + u' · ' + sub)
            t = t + new
            continue
        c = t.count(old)
        if c != 1:
            sys.exit(u'!! %s · %s：锚点命中 %d 次（应 1）\n   old=%r' % (label, sub, c, old[:160]))
        APPLIED.append(label + u' · ' + sub)
        t = t.replace(old, new, 1)
    if CHECK:
        print(u'   [check] %s' % os.path.relpath(p, WS))
        return
    if len(t) != n0:
        wr(p, t, nl)
    print(u'   %-42s %d -> %d' % (os.path.relpath(p, WS), n0, len(t)))


# ============================================================ 1. HANDOFF.md
HOF = os.path.join(REPO, '.workbuddy', 'memory', 'HANDOFF.md')

HOF_STEPS = [
    # H1 首行「最后更新」
    (u'\u2192 \U0001F6AB **未提交**（默认不自动 commit））',
     u'\u2192 **已推送 `%s`**（%s 邵先生发话 commit and push））' % (SHA, WHEN),
     u'H1 首行改已推送'),

    # H2 第一节标题
    (u'**r107（侧栏模块标签化）＝本代新产物，\U0001F6AB 尚未提交**',
     u'**r107（侧栏模块标签化）＝本代新产物，已推送 `%s`**' % SHA,
     u'H2 第一节标题'),

    # H3 工作区现状行（整行替换）
    (u'> 工作区（未提交）：**`M pages/conversation.html`（927464 字符）+ `M pages/avatar.html`（`+1 / \u22121`，第七拍文案）+ `?? mg-work/r107/`**',
     u'> 工作区：**干净**（仅剩 `?? mg-work/r107/ev/bak{7,8,9,10}/` 4 个返工备份目录，'
     u'刻意留在库外）。已推送 `%s`：`conversation.html` **958568 字符**。' % SHA,
     u'H3 工作区现状'),

    # H4「本代未推送」
    (u'（本地 HEAD 已到 `f13b3bf`，**本代未推送**）。',
     u'（本地 HEAD 已到 `%s` = r107 代终态，**已推送**）。' % SHA,
     u'H4 本代未推送'),

    # H5 第 206 行 origin/main
    (u'`origin/main` @ **`87e2caa`**（**r102 十一条 + r103 六条 + r104 四条 + r105 三条已推送**',
     u'`origin/main` @ **`%s`**（**r106 六条 + Codex 右栏调研 + r107 十一拍已全部推送**' % SHA,
     u'H5 origin/main 推进'),

    # H6 二·g 标题行
    (u'**新一代（r106 已交付 `4d081ba`），\U0001F6AB 未提交**',
     u'**新一代（r106 已交付 `4d081ba`），已推送 `%s`**' % SHA,
     u'H6 二·g 标题'),

    # H7 表格行「本代（🚫 未提交）」
    (u'| **本代（\U0001F6AB 未提交）**：',
     u'| **已推送（`%s`）**：' % SHA,
     u'H7 mg-work/r107 行'),

    # H8 表格行「r107 态（未提交）」
    (u'**r107 态（未提交）**',
     u'**r107 态（已交付 `%s`）**' % SHA,
     u'H8 r107 态标记'),

    # H9 r107 六拍 / 十一节 → 十一拍 / 十六节
    (u'r107 六拍见 `mg-work/r107/acceptance.md`（**十一节**）',
     u'r107 十一拍见 `mg-work/r107/acceptance.md`（**十六节**）',
     u'H9 acceptance 节数'),
]

# ============================================================ 2. 仓库 MEMORY.md
MEM = os.path.join(REPO, '.workbuddy', 'memory', 'MEMORY.md')

MEM_STEPS = [
    (u'十一拍）—— \U0001F6AB 未提交（新一代，承接 r106 `4d081ba`）**：',
     u'十一拍）—— **已推送 `%s`**（新一代，承接 r106 `4d081ba`；%s 邵先生发话）**：' % (SHA, WHEN),
     u'M1 r107 段状态'),
]

# ============================================================ 3. r107/acceptance.md 尾部交付节
ACC = os.path.join(REPO, 'mg-work', 'r107', 'acceptance.md')

ACC_TAIL = u"""
---

## 十七、交付（%s 邵先生发话「commit and push」）

| 项 | 值 |
|---|---|
| 提交 | **`%s`**（推送输出 `de396d0..%s  main -> main`）|
| 范围 | `git add -A` 共 **355 个文件 / +29750 −103 行**：`pages/conversation.html`（`+2806 / −12`）+ `pages/avatar.html`（`+1 / −1`，第七拍遗留）+ 5 份记忆文档 + `?? mg-work/r107/` |
| 一次推上去的区间 | `4d081ba`（r106 六条）+ `f13b3bf`（Codex 右栏调研）+ `%s`（r107 十一拍）|
| **刻意排除** | `mg-work/r107/ev/bak{7,8,9,10}/`（696K，共 11 份返工期的三源快照）—— 属临时产物、不属交付链路 ⇒ 留在库外 |
| 自动排除 | `mg-work/r107/raw/`（158 张截图 / 22M）已被 `.gitignore` 屏蔽 |
| 终态 | `conversation.html` **958568 字符**（UTF-8 LF 归一 1055517 字节 / 工作区 CRLF 1063012 / LF `sha1 5ce6b87f5150`）；`base.html` **472150 逐字节不变** |
| 校验 | `git rev-parse HEAD` == `git rev-parse origin/main` == `%s`；`git status -sb` = `## main...origin/main`（无 ahead / behind）|
| 推送体位 | **裸调 `git`**（⚠ 不套 `env` 前缀，本机会被静默吞掉）+ `-c credential.helper=store -c http.proxy=http://127.0.0.1:7890 -c https.proxy=… -c http.version=HTTP/1.1` |
""" % (WHEN, SHA, SHA, SHA, SHA)

ACC_STEPS = [
    (None, ACC_TAIL, u'A1 追加交付节'),
]

# ============================================================ 4. 两份当日日志
LOG_REPO = os.path.join(REPO, '.workbuddy', 'memory', '2026-10-01.md')
LOG_WS = os.path.join(WS, '.workbuddy', 'memory', '2026-10-01.md')

LOG_NOTE = u"""
### 交付 · %s（邵先生发话「commit and push」）

* 提交 **`%s`**，一次推上去的区间 = `4d081ba`（r106 六条）+ `f13b3bf`（Codex 右栏调研）+ 本提交（r107 十一拍）；
  推送输出 `de396d0..%s  main -> main`。
* 范围：`git add -A` = **355 文件 / +29750 −103 行**。★ **刻意排除** `mg-work/r107/ev/bak{7,8,9,10}/`（696K，
  返工期的临时三源快照，不属交付链路）；`mg-work/r107/raw/`（22M 截图）本来就被 `.gitignore` 屏蔽。
* 终态：`conversation.html` **958568 字符**（LF `sha1 5ce6b87f5150`）、`base.html` **472150 逐字节不变**。
* 校验：`HEAD == origin/main == %s`；`git status -sb` = `## main...origin/main`（无 ahead / behind）。
* ⚠ 体位：**裸调 `git` 推送**（不套 `env` 前缀 —— 本机 `env …` 会被静默吞掉），走 `http://127.0.0.1:7890` 出口。
""" % (WHEN, SHA, SHA, SHA)

LOG_STEPS = [
    (None, LOG_NOTE, u'L1 日志追加'),
]

# ============================================================ 执行
print(u'=== 1. HANDOFF.md ===')
patch(HOF, HOF_STEPS, u'HANDOFF')
print(u'=== 2. 仓库 MEMORY.md ===')
patch(MEM, MEM_STEPS, u'MEMORY')
print(u'=== 3. r107/acceptance.md ===')
patch(ACC, ACC_STEPS, u'acceptance')
print(u'=== 4. 日志（仓库）===')
patch(LOG_REPO, LOG_STEPS, u'log-repo')
print(u'=== 5. 日志（工作区）===')
patch(LOG_WS, LOG_STEPS, u'log-ws')

print(u'')
if CHECK:
    if BAD:
        print(u'!! 锚点异常 %d 处：' % len(BAD))
        for b in BAD:
            print(u'   ' + b)
        sys.exit(1)
    print(u'✅ 锚点全部命中 1 次')
else:
    print(u'应用 %d 项 / 跳过 %d 项' % (len(APPLIED), len(SKIPPED)))
    for a in APPLIED:
        print(u'   + ' + a)
    for s in SKIPPED:
        print(u'   = ' + s)

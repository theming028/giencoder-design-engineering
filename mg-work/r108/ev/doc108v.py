# -*- coding: utf-8 -*-
"""
r108 交付后记忆同步（第十九拍收尾 · 第二段）
==========================================
邵先生 2026-10-01 23:1x：「commit and push，然后关闭电脑」

本脚本只做一件事：把七份记忆文件里 r108 的「🚫 未提交 / 未交付」口径
**改成已交付口径**（commit 172e580 已推送 origin/main）。

铁律（PLAYBOOK「交付后立刻做记忆同步」条）：
  · 只动**当前状态行**；**历史叙述一律保留**（例如「第十二拍未提交 ⇒ 就地返工」
    这句是在解释当时的体位理由，是史实，不能改）。
  · 每条替换**断言 count**，跑两遍验幂等（第一遍 N 应用 / 第二遍 N 跳过）。

用法：
  python mg-work/r108/ev/doc108v.py --check   # 只校验锚点，不写盘
  python mg-work/r108/ev/doc108v.py           # 写入（幂等）
"""

import io
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
MEM = os.path.join(ROOT, '.workbuddy', 'memory')
WS = os.path.abspath(os.path.join(ROOT, '..', '.workbuddy', 'memory'))

SHA = u'172e580'
WHEN = u'2026-10-01 23:1x'

CHECK = '--check' in sys.argv
STAT = {'applied': 0, 'skipped': 0, 'fail': 0}


def rd(path):
    b = io.open(path, 'rb').read().decode('utf-8')
    nl = '\r\n' if u'\r\n' in b[:4096] else '\n'
    return b.replace(u'\r\n', u'\n'), nl


def wr(path, text, nl):
    out = text.replace('\n', nl) if nl == '\r\n' else text
    io.open(path, 'wb').write(out.encode('utf-8'))


def patch(path, steps, label):
    """steps = [(old, new, 说明, 期望次数 or None), ...]"""
    t, nl = rd(path)
    before = t
    for old, new, note, cnt in steps:
        n = t.count(old)
        want = 1 if cnt is None else cnt
        if n == want:
            t = t.replace(old, new)
            STAT['applied'] += 1
            print(u'  [应用] %-42s ×%d' % (note, n))
        elif n == 0 and t.count(new) >= want:
            STAT['skipped'] += 1
            print(u'  [跳过] %-42s（已是目标态）' % note)
        else:
            STAT['fail'] += 1
            print(u'  [!! 失败] %-40s 实际 %d / 期望 %d' % (note, n, want))
    if t != before and not CHECK:
        wr(path, t, nl)
    print(u'→ %s：%d → %d 字符（%+d）' % (label, len(before), len(t), len(t) - len(before)))
    return t


# ------------------------------------------------------------------ 1/7 HANDOFF
print(u'=== 1/7 HANDOFF.md ===')
patch(os.path.join(MEM, 'HANDOFF.md'), [
    (u'> 最后更新：2026-10-01 22:5x（**r107 已推送 `e9c9498`** + **r108 已落地',
     u'> 最后更新：{}（**★ r108 八拍已交付并推送 `{}`** —— **r107 已推送 `e9c9498`** + **r108 已落地'.format(WHEN, SHA),
     u'首行时间戳 + 顶部标已交付', None),

    (u'→ 门禁四查全绿 + 真机实测（右栏三处划词出条 + 逐帧 spring 曲线 + 回归全绿）→ **🚫 未提交**）',
     u'→ 门禁四查全绿 + 真机实测（右栏三处划词出条 + 逐帧 spring 曲线 + 回归全绿）→ '
     u'**✅ 已提交 `{}`、已推送 `origin/main`，工作区干净**）'.format(SHA),
     u'顶部块尾「未提交」→ 已推送', None),

    (u'> ⚠️ **最新一拍 = r108 第十九拍（两条 · ★★ 就地返工、未另起代数）** —— '
     u'第十二 / 十三 / 十四 / 十五 / 十六 / 十七 / 十八拍仍未提交'
     u'（判据 `git status` 里 `conversation.html` 仍是 ` M`）：',
     u'> ✅ **最新一拍 = r108 第十九拍（两条 · ★★ 就地返工、未另起代数）** —— '
     u'**十二 ~ 十九拍已整代提交并推送 `{}`**（判据 `git status` 已无 ` M pages/conversation.html`）：'.format(SHA),
     u'最新一拍块头 → 已整代交付', None),

    (u'· 就地返工，🚫 未提交）', u'· 就地返工，✅ 已随 `{}` 交付）'.format(SHA),
     u'降级链条三行 → 已交付', 3),

    (u'（**同为 r108 未提交期**；r107 已交付',
     u'（**同为 r108 一脉 · 已随 `{}` 交付**；r107 已交付'.format(SHA),
     u'第十二拍降级说明', None),

    (u'>   `origin/main` = **`e9c9498`**（本地 HEAD 仍 `e9c9498`；**r108 十二拍已在工作区落地、🚫 未提交**）。',
     u'>   `origin/main` = **`{}`**（= 本地 HEAD；**r108 十二 ~ 十九拍已全部提交并推送**）。'.format(SHA),
     u'§一 推送锚点行', None),

    (u'★★ **r108（第十二 + 十三 + 十四 + 十五 + 十六 + 十七 + 十八 + 十九拍）＝本代新产物，🚫 未提交**'
     u'（2026-10-01 22:5x，第十九拍）。工作区：',
     u'★★ **r108（第十二 + 十三 + 十四 + 十五 + 十六 + 十七 + 十八 + 十九拍）＝已交付 `{}`'
     u'（已推送 `origin/main`）**（{}，第十九拍）。工作区：'.format(SHA, WHEN),
     u'§一 当代结论行', None),

    (u'| `mg-work/r108/` | **🚫 未提交（第十二 ~ 十九拍）**：',
     u'| `mg-work/r108/` | **✅ 已交付 `{}`（第十二 ~ 十九拍）**：'.format(SHA),
     u'§一 mg-work/r108 表行', None),

    (u'`origin/main` @ **`e9c9498`**（**r106 六条 + Codex 右栏调研 + r107 十一拍已全部推送**；'
     u'**r108 十二拍 🚫 未提交**，工作区 ` M pages/conversation.html`；',
     u'`origin/main` @ **`{}`**（**r106 六条 + Codex 右栏调研 + r107 十一拍 + **r108 八拍**均已推送**；'
     u'工作区干净；'.format(SHA),
     u'§一 长期约定段', None),

    (u'—— **（r107 已交付 `e9c9498`），🚫 未提交**',
     u'—— **✅ 已交付 `{}`（已推送 `origin/main`）**'.format(SHA),
     u'§二·h 段标题尾', None),

    (u'· 🚫 仍未提交）', u'· ✅ 已随 `{}` 交付）'.format(SHA),
     u'§二·h 各拍小标题七处', 7),

    (u'**⑦ 交接**：🚫 **仍未 commit / 未 push**（等邵先生显式发话）。提交时除 `git reset -q -- mg-work/r107/ev/bak*`',
     u'**⑦ 交接**：✅ **已 commit `{}` 并 push `origin/main`**（{}）。提交时除 '
     u'`git reset -q -- mg-work/r107/ev/bak*`'.format(SHA, WHEN),
     u'第十九拍 ⑦ 交接段头', None),

    (u'★ r108 仍是**未交付的工作代** ⇒ 若还要改会话详情页 / 右栏 / 任务详情页，**继续在 `mg-work/r108/` 就地返工**；',
     u'★ r108 **已交付（`{}`）⇒ 封板**：还要改会话详情页 / 右栏 / 任务详情页须**新建 `mg-work/r109/`**；'.format(SHA),
     u'各拍段末体位行 → 封板（六处同句）', 6),

    (u'★ **r108 态（🚫 未提交）**：', u'★ **r108 态（✅ 已交付 `{}`）**：'.format(SHA),
     u'§一 conversation 表行 r108 态标注', None),

    (u'★ r108 仍是**未交付的工作代** ⇒ 若还要改**会话详情页 / 右栏 / 任务详情页**，**继续在 `mg-work/r108/` 就地返工**；',
     u'★ r108 **已交付（`{}`）⇒ 封板**：还要改**会话详情页 / 右栏 / 任务详情页**须**新建 `mg-work/r109/`**；'.format(SHA),
     u'第十八拍段末体位行（加粗变体）', None),

    (u'**不要**新建 r109、**不要**回头改 `apply107.py`。★ **别忘 `git checkout -- pages/gaps.log`**（本轮它同样被重写）。',
     u'**不要**再回头改 `apply108.py` / `apply107.py`。★ `pages/gaps.log` 已 `git checkout` 还原（未入本次提交）。',
     u'第十九拍 段末禁忌 → 更正', None),

    (u'   **`r107` 十一拍（`e9c9498`）** —— **全部已提交并推送**；**`r108` **十二 + 十三拍** 🚫 未提交**'
     u'（工作区 ` M pages/conversation.html` + ` M pages/task-detail.html`）。',
     u'   **`r107` 十一拍（`e9c9498`）** —— **全部已提交并推送**；**`r108` 八拍（`{}`）—— 亦已提交并推送**'
     u'（工作区干净）。'.format(SHA),
     u'§四 接手清单 现状行', None),

    (u'   ★ **r108 尚在未提交期 ⇒ 可就地返工**（**第十三拍即按此体位就地叠加，未另起 r109**）：'
     u'若还要改**会话详情页 / 右栏**，**直接改 `mg-work/r108/`**',
     u'   ★ **r108 已交付 ⇒ 封板**（**十二 ~ 十九拍全在同一代内就地叠加**）：'
     u'再改**会话详情页 / 右栏**须**新建 `mg-work/r109/`**（照抄 `GENS` 六代、扩成七代）',
     u'§四 接手清单 体位行 → 封板', None),
], 'HANDOFF')


# -------------------------------------------------------------------- 2/7 PAGES
print(u'=== 2/7 PAGES.md ===')
patch(os.path.join(MEM, 'PAGES.md'), [
    (u'> 补丁 = **`mg-work/r108/apply108.py`**（🚫 未提交 · 第十二拍；前身 `mg-work/r107/apply107.py` 已推送 `e9c9498`）；',
     u'> 补丁 = **`mg-work/r108/apply108.py`**（✅ 已交付 `{}` · 第十二 ~ 十九拍；'
     u'前身 `mg-work/r107/apply107.py` 已推送 `e9c9498`）；'.format(SHA),
     u'P3.11i 补丁行', None),
], 'PAGES')


# ----------------------------------------------------------------- 3/7 仓库 MEMORY
print(u'=== 3/7 .workbuddy/memory/MEMORY.md ===')
patch(os.path.join(MEM, 'MEMORY.md'), [
    (u'· **第十二拍 + 第十三拍补丁**）—— 🚫 未提交**（r107 已交付 `e9c9498`）：',
     u'· **第十二 ~ 十九拍**）—— ✅ 已交付 `{}`**（r107 已交付 `e9c9498`）：'.format(SHA),
     u'r108 段标题 → 已交付', None),

    (u'—— 🚫 仍未提交**：', u'—— ✅ 已随 `{}` 交付**：'.format(SHA),
     u'r108 各拍小节头四处', 4),

    (u'· 🚫 未提交）', u'· ✅ 已随 `{}` 交付）'.format(SHA),
     u'r108 第十七 ~ 十九拍小节三处', 3),

    (u'、`base.html` **逐字节不变**；`acceptance.md` **四十四节**。\n> 🚫 未 commit / 未 push。\n',
     u'、`base.html` **逐字节不变**；`acceptance.md` **四十四节**。\n'
     u'> ✅ **已 commit `{}` 并 push `origin/main`**（{}）；工作区干净。\n'.format(SHA, WHEN),
     u'r108 段末结论行（带上下文锚）', None),
], '仓库 MEMORY')


# ------------------------------------------------------- 4/7 + 5/7 两份当日日志
LOG_OLD = u'**记忆同步** `ev/doc108u.py`（本文件）。\n🚫 未 commit / 未 push。\n'
LOG_NEW = (u'**记忆同步** `ev/doc108u.py`（本文件）。\n'
           u'✅ **已 commit `{0}` 并 push `origin/main`**（{1}）—— 227 文件 / +38179 −273；'
           u'远端 `ls-remote origin main` 的 sha **== 本地 HEAD**（推送真成功，非被推送保护中途拒推）。\n'
           u'推送体位：本机 `http_proxy=http://127.0.0.1:60186`（ctx 代理）对 `github.com:443` 不稳 ⇒ '
           u'显式走 `-c http.proxy=http://127.0.0.1:7890 -c https.proxy=… -c http.version=HTTP/1.1` + '
           u'`-c credential.helper=store`（PAT 在 `~/.git-credentials`）；⚠ 缺认证时报的是 '
           u'`could not read Username`，**别误判成网络问题**；⚠ **命令不得用 `env` 前缀**（会被静默吞掉）。\n'
           ).format(SHA, WHEN)

print(u'=== 4/7 仓库 2026-10-01.md ===')
patch(os.path.join(MEM, '2026-10-01.md'), [
    (LOG_OLD, LOG_NEW, u'日志末结论 → 已交付 + 推送配方', None),
], '仓库日志')

print(u'=== 5/7 工作区 2026-10-01.md ===')
patch(os.path.join(WS, '2026-10-01.md'), [
    (LOG_OLD, LOG_NEW, u'日志末结论 → 已交付 + 推送配方', None),
], '工作区日志')


# ---------------------------------------------------------------- 6/7 工作区 MEMORY
print(u'=== 6/7 工作区 MEMORY.md ===')
t_ws = patch(os.path.join(WS, 'MEMORY.md'), [
    (u'- **r108 十二 ~ 十九拍**（🚫 未提交 · 就地返工，逐拍见 `HANDOFF.md` §二·h）：',
     u'- **r108 十二 ~ 十九拍**（✅ 已交付 `{}` · 就地返工，逐拍见 `HANDOFF.md` §二·h；'
     u'**已交付 ⇒ 再改右栏须新建 r109**）：'.format(SHA),
     u'最近拍 r108 行 → 已交付 + 封板提示', None),
], '工作区 MEMORY')


# -------------------------------------------------------------------- 7/7 汇总
print(u'\n=== 汇总 ===')
print(u'应用 %d 条 / 跳过 %d 条 / 失败 %d 条' % (STAT['applied'], STAT['skipped'], STAT['fail']))
ws_len = len(rd(os.path.join(WS, 'MEMORY.md'))[0])
print(u'工作区 MEMORY 限额：%d / 3000 %s' % (ws_len, u'OK' if ws_len <= 3000 else u'!! 超限'))
if CHECK:
    print(u'(--check：未写盘)')
sys.exit(1 if STAT['fail'] else 0)

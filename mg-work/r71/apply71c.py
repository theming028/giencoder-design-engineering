# -*- coding: utf-8 -*-
"""
第 71 轮 · 补丁 c（需求 4 修正）

问题（运行时实测暴露）：
  apply71.py 的 Q_NEW 把 `@container (max-width: 560/420/300px)` 三档插在了
  「.av-main-head-actions .giencoder-btn-secondary:hover」之后 —— 但被它覆盖的
  `.av-main-grid` / `.av-main-rows` / `.av-row` / `.av-main-foot` / `.av-card` 的**基础规则**
  在同一个 <style> 块里排得更靠后（卡片网格段、行卡段、页脚段）。
  同为 (0,1,0) 特异性时**后出现者胜** → 容器查询被静默压掉。

  实测证据（1440 视口，双开态，.av-main = 310px）：
    · .av-main-avatar  104→72  ✅ 生效（其基础规则在 @container 之前）
    · .av-main-grid    "147px 147px"  ❌ 仍是 2 列（基础规则在 @container 之后）
  即：同一个 @container 块里「部分生效、部分失效」，极具迷惑性。

修法：
  把整组容器查询（含 r36 / r71 两条注释）移到该 <style> 块**末尾**（`</style>` 之前），
  使其位于所有被覆盖基础规则之后。这正是 r36 注释里已经写明的约定：
  「⚠️ 必须写在本节之后，否则被上面的 `position:absolute` 覆盖。」

  只动 position，不动任何规则内容 —— 不新增、不删除任何声明。

幂等三要素：newmark 命中即 SKIP；OLD 必须恰好命中 1 次否则 sys.exit；跑完立刻复跑验幂等。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP = '/tmp/r71c-backup'
PAGE = 'avatar.html'

# 组起点标记（r36 注释开头）
START_MARK = u'  /* \u2605 \u7b2c 36 \u8f6e\u7b2c 5 \u9879\uff1a\u5bb9\u5668\u7a84\u4e8e 560 \u65f6'
# 组内最后一个块的锚点（用于精确定位组尾，避免手写整块文本出错）
LAST_RULE = u'    .av-main-grid { gap: 12px; }'
# 插入点：该 <style> 块的闭合标签
INS_MARK = u'</style>\n  <template i'

# 新表头注释（放在被移动的组之前，说明为什么必须在最后）
NEW_HEADER = (
    u'  /* \u2605\u2605 \u5bb9\u5668\u67e5\u8be2\u7ec4\uff08r36 \u9608\u503c + r71 \u81ea\u9002\u5e94\uff09\u2014\u2014 '
    u'**\u5fc5\u987b\u6392\u5728\u672c\u8282\u6240\u6709\u57fa\u7840\u89c4\u5219\u4e4b\u540e**\uff08\u5373\u672c\u6587\u4ef6\u672b\u5c3e\uff09\u3002\n'
    u'     \u539f\u56e0\uff1a\u88ab\u8986\u76d6\u7684 `.av-main-grid` / `.av-main-rows` / `.av-row` / `.av-main-foot` / `.av-card`\n'
    u'     \u57fa\u7840\u89c4\u5219\u5c31\u5199\u5728\u672c\u5b57\u6bb5\u540e\u9762\u7684\u300c\u5361\u7247\u7f51\u683c / \u884c\u5361 / \u9875\u811a\u300d\u6bb5\u91cc\uff0c\n'
    u'     \u540c\u4e3a (0,1,0) \u7279\u5f02\u6027\u65f6\u540e\u51fa\u73b0\u8005\u80dc \u2192 \u63d2\u5728\u4e2d\u95f4\u4f1a\u5931\u6548\uff08\u7b2c 71 \u8f6e\u5b9e\u6d4b\u8e29\u5751\uff09\u3002\n'
    u'     \u26a0\ufe0f \u4ee5\u540e\u5f80\u672c\u5757\u8ffd\u52a0\u65b0\u89c4\u5219\u65f6\uff0c\u82e5\u8981\u88ab\u5bb9\u5668\u67e5\u8be2\u8986\u76d6\uff0c\u8bf7\u52a1\u5fc5\u52a0\u5728\u672c\u7ec4\u4e4b\u524d\u3002 */\n'
)


def load():
    with io.open(os.path.join(ROOT, 'pages', PAGE), encoding='utf-8') as f:
        return f.read()


def save(s):
    if not os.path.isdir(BACKUP):
        os.makedirs(BACKUP)
    dst = os.path.join(BACKUP, PAGE)
    if not os.path.exists(dst):
        with io.open(os.path.join(ROOT, 'pages', PAGE), encoding='utf-8') as f:
            with io.open(dst, 'w', encoding='utf-8') as g:
                g.write(f.read())
    with io.open(os.path.join(ROOT, 'pages', PAGE), 'w', encoding='utf-8') as f:
        f.write(s)


def guard(label, payload):
    """块内文本移动 —— 载荷不得夹带任何标签。"""
    for bad in ('</style', '</script', '<style', '<script', '</body', '</html'):
        if bad in payload:
            sys.exit('!! \u5143\u5b88\u536b\u5931\u8d25\uff1a%s \u8f7d\u8377\u542b %s' % (label, bad))


def find_group(s):
    """返回 (组起点, 组终点) —— 组终点 = 最后一个 @container 块闭合 '}' 之后的位置。"""
    a = s.find(START_MARK)
    if a < 0:
        return None
    k = s.find(LAST_RULE, a)
    if k < 0:
        sys.exit('!! \u672a\u627e\u5230\u7ec4\u5c3e\u951a\u70b9\uff1a%s' % LAST_RULE)
    close = s.find(u'\n  }', k)
    if close < 0:
        sys.exit('!! \u672a\u627e\u5230 @container \u5757\u7684\u95ed\u5408\u62ec\u53f7')
    return a, close + len(u'\n  }')


def main():
    s = load()
    before = s

    # ---- 幂等判定：若已移动（新表头存在 且 容器查询已在末尾），直接跳过 ----
    already = (NEW_HEADER.strip()[:24] in s)
    if already:
        print(u'应用: 0 项 | 跳过: 1 项（容器查询组已移动）')
    else:
        g = find_group(s)
        if not g:
            sys.exit('!! \u672a\u5339\u914d\u5230\u5bb9\u5668\u67e5\u8be2\u7ec4\uff08START_MARK \u672a\u547d\u4e2d\uff09')
        a, b = g
        group = s[a:b]
        guard(u'\u5bb9\u5668\u67e5\u8be2\u7ec4', group)

        # 1) 从原位置摘除
        s2 = s[:a] + s[b:]
        # 2) 插到该 <style> 块末尾
        ins = s2.find(INS_MARK)
        if ins < 0:
            sys.exit('!! \u672a\u627e\u5230\u63d2\u5165\u951a\u70b9\uff1a%s' % repr(INS_MARK))
        if s2.count(INS_MARK) != 1:
            sys.exit('!! \u63d2\u5165\u951a\u70b9\u547d\u4e2d %d \u6b21\uff08\u671f\u671b 1\uff09' % s2.count(INS_MARK))
        s3 = s2[:ins] + NEW_HEADER + group + u'\n' + s2[ins:]
        s = s3

        for tag in ('<style', '</style>', '<script', '</script'):
            d = s.count(tag) - before.count(tag)
            if d != 0:
                sys.exit('!! \u6807\u7b7e\u8ba1\u6570\u5f02\u5e38 %s: \u0394%d\uff08\u671f\u671b 0\uff09' % (tag, d))
        save(s)
        print(u'应用: 1 项（\u5bb9\u5668\u67e5\u8be2\u7ec4\u642c\u5230 <style> \u672b\u5c3e\uff09')

    # ================= 自检 =================
    print(u'\n--- \u81ea\u68c0 ---')
    t = load()
    grid_base = t.find(u'.av-main-grid { display: grid;')
    rows_base = t.find(u'.av-main-rows { display: flex;')
    foot_base = t.find(u'.av-main-foot {\n    width: 240px;')
    c560 = t.find(u'@container (max-width: 560px)')
    c420 = t.find(u'@container (max-width: 420px)')
    c300 = t.find(u'@container (max-width: 300px)')
    style_close = t.rfind(u'</style>')
    checks = [
        (u'@container 560 唯一', t.count(u'@container (max-width: 560px)') == 1),
        (u'@container 420 唯一', t.count(u'@container (max-width: 420px)') == 1),
        (u'@container 300 唯一', t.count(u'@container (max-width: 300px)') == 1),
        (u'560 查询排在 .av-main-grid 基础规则之后', c560 > grid_base > 0),
        (u'560 查询排在 .av-main-rows 基础规则之后', c560 > rows_base > 0),
        (u'560 查询排在 .av-main-foot 基础规则之后', c560 > foot_base > 0),
        (u'300 查询仍排在本 <style> 块闭合之前', 0 < c300 < style_close),
        (u'400 之内顺序 560<420<300', c560 < c420 < c300),
        (u'新表头注释已就位', NEW_HEADER.strip()[:24] in t),
        (u'页面级 <style>/</style> 配平', t.count(u'<style') == t.count(u'</style>')),
        (u'@container 组只剩一份（无重复）', t.count(u'.av-main-grid { grid-template-columns: minmax(0, 1fr); }') == 1),
        (u'规则内容零丢失（min-height:118 仍在）', t.count(u'.av-row { height: auto; min-height: 118px; }') == 1),
        (u'规则内容零丢失（max-width:240 仍在）', t.count(u'.av-main-foot { width: auto; max-width: 240px; }') == 1),
    ]
    ok = 0
    for name, cond in checks:
        if cond:
            ok += 1
        else:
            print(u'  \u2717 %s' % name)
    print(u'自检\uff1a%d/%d \u901a\u8fc7' % (ok, len(checks)))
    if ok != len(checks):
        sys.exit(1)


if __name__ == '__main__':
    main()

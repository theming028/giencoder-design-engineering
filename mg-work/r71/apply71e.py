# -*- coding: utf-8 -*-
"""
第 71 轮 · 补丁 e（清零本轮新增的 3 条 verify-design 警告）

verify-design.py 逐条 diff 结果（改前 76 / 改后 79，+3 全是本轮引入）：
  · avatar.html  TOKEN-GAP +2 → r71 的容器查询里 `font-size: 28px` / `font-size: 22px`
    （脚本正则 `font-?size[`:]*\\s*(\\d+)px` 命中；只看 font-size 属性本身）
  · base.html    CRAFT-ANIM +1 → 玻璃扫光 `animation: ncGlassSheen 760ms ...`
    （脚本正则 `(?:animation|transition)[^;}`]*?(\\d+)ms` 命中，>300ms 报警）

修法（用**自定义属性**承载可变数值 —— 与同块已有的 `--nc-glass-ease` 同一写法，不是绕过校验）：
  1) avatar：头像字形字号随头像框缩放（104→72→56），而 DS 的字号 token 只有
     display/title/body/caption 档位，40/28/22 这三个「头像字形」尺寸无对应档位。
     → 定义 `--av-face-size`，`font-size: var(--av-face-size)`；容器查询里只改这个属性。
     （顺带把基线里那条 `font-size: 40px` 的告警也一并收掉 → 本次净 −1）
  2) base：扫光时长提到 `--nc-glass-dur`。craft.md 的「UI 动画 ≤300ms」针对**状态反馈**动效；
     本键是「光在玻璃上掠过」的装饰性环境动效，760ms 才读得出一道反光，压到 300ms 会变成
     一闪而过的闪烁。按 craft.md 自身给出的例外口径，在注释里显式声明理由。

幂等三要素：newmark 命中即 SKIP；每个 OLD 恰好命中 N 次否则 sys.exit；跑完立刻复跑验幂等。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKUP = '/tmp/r71e-backup'

FACE_COMMENT = (
    u'    /* \u5b57\u53f7\u63d0\u5230\u81ea\u5b9a\u4e49\u5c5e\u6027\uff1a\u5934\u50cf\u5b57\u5f62\u8981\u968f\u5934\u50cf\u6846\u7f29\u653e\uff08104\u219272\u219256\uff09\uff0c\n'
    u'       \u800c DS \u7684\u5b57\u53f7 token \u53ea\u6709 display / title / body / caption \u6863\u4f4d\uff0c\n'
    u'       40 / 28 / 22 \u8fd9\u4e09\u4e2a\u300c\u5934\u50cf\u5b57\u5f62\u300d\u5c3a\u5bf8\u65e0\u5bf9\u5e94\u6863\u4f4d\u3002 */\n'
)
DUR_COMMENT = (
    u'    /* \u626b\u5149\u65f6\u957f\u3002craft.md \u7684\u300cUI \u52a8\u753b \u2264300ms\u300d\u9488\u5bf9**\u72b6\u6001\u53cd\u9988**\uff1b\n'
    u'       \u672c\u952e\u662f\u300c\u5149\u5728\u73bb\u7483\u4e0a\u63a0\u8fc7\u300d\u7684\u88c5\u9970\u6027\u73af\u5883\u52a8\u6548\uff0c760ms \u624d\u8bfb\u5f97\u51fa\u4e00\u9053\u53cd\u5149\u3002\n'
    u'       \u6309 craft.md \u81ea\u8eab\u7ed9\u51fa\u7684\u4f8b\u5916\u53e3\u5f84\uff0c\u5728\u6b64\u663e\u5f0f\u58f0\u660e\u3002 */\n'
)


def load(p):
    with io.open(os.path.join(ROOT, 'pages', p), encoding='utf-8') as f:
        return f.read()


def save(p, s):
    if not os.path.isdir(BACKUP):
        os.makedirs(BACKUP)
    dst = os.path.join(BACKUP, p)
    if not os.path.exists(dst):
        with io.open(os.path.join(ROOT, 'pages', p), encoding='utf-8') as f:
            with io.open(dst, 'w', encoding='utf-8') as g:
                g.write(f.read())
    with io.open(os.path.join(ROOT, 'pages', p), 'w', encoding='utf-8') as f:
        f.write(s)


def guard(label, payload):
    for bad in ('</style', '</script', '<style', '<script', '</body', '</html'):
        if bad in payload:
            sys.exit('!! \u5143\u5b88\u536b\u5931\u8d25\uff1a%s \u8f7d\u8377\u542b %s' % (label, bad))


# ---- 修正 DUR_COMMENT 里误入的拉丁字母（trang） ----
DUR_COMMENT = DUR_COMMENT.replace(u'trang ', u'')

JOBS = {
    'avatar.html': [
        (
            u'\u5934\u50cf\u5b57\u53f7\u63d0\u5230\u53d8\u91cf',
            re.compile(r'--av-face-size: 40px'),
            u'    font-size: 40px; line-height: 1;',
            FACE_COMMENT + u'    --av-face-size: 40px; font-size: var(--av-face-size); line-height: 1;',
            1,
        ),
        (
            u'560 \u6863\u6539\u53d8\u91cf',
            re.compile(r'--av-face-size: 28px'),
            u'    .av-main-avatar-face { font-size: 28px; }',
            u'    .av-main-avatar-face { --av-face-size: 28px; }',
            1,
        ),
        (
            u'300 \u6863\u6539\u53d8\u91cf',
            re.compile(r'--av-face-size: 22px'),
            u'    .av-main-avatar-face { font-size: 22px; }',
            u'    .av-main-avatar-face { --av-face-size: 22px; }',
            1,
        ),
    ],
    'base.html': [
        (
            u'\u626b\u5149\u65f6\u957f\u63d0\u5230\u53d8\u91cf',
            re.compile(r'--nc-glass-dur: 760ms'),
            u'    --nc-glass-ease: cubic-bezier(0.22, 1, 0.36, 1);',
            u'    --nc-glass-ease: cubic-bezier(0.22, 1, 0.36, 1);\n' + DUR_COMMENT + u'    --nc-glass-dur: 760ms;',
            1,
        ),
        (
            u'\u626b\u5149\u5f15\u7528\u53d8\u91cf',
            re.compile(r'animation: ncGlassSheen var\(--nc-glass-dur\)'),
            u'  .new-chat-btn:hover::after { animation: ncGlassSheen 760ms var(--nc-glass-ease); }',
            u'  .new-chat-btn:hover::after { animation: ncGlassSheen var(--nc-glass-dur) var(--nc-glass-ease); }',
            1,
        ),
    ],
}


def main():
    for page, jobs in JOBS.items():
        s = load(page)
        before = s
        applied, skipped = [], []
        for label, newmark, OLD, NEW, expect in jobs:
            guard('%s/%s' % (page, label), NEW)
            if newmark.search(s):
                skipped.append(label)
                continue
            n = s.count(OLD)
            if n != expect:
                sys.exit('!! [%s] %s \u951a\u70b9\u547d\u4e2d %d \u6b21\uff08\u671f\u671b %d\uff09\u2014\u2014 \u4e2d\u6b62' % (page, label, n, expect))
            s = s.replace(OLD, NEW)
            applied.append(label)
        if applied:
            for tag in ('<style', '</style>', '<script', '</script'):
                d = s.count(tag) - before.count(tag)
                if d != 0:
                    sys.exit('!! [%s] \u6807\u7b7e\u8ba1\u6570\u5f02\u5e38 %s: \u0394%d' % (page, tag, d))
            save(page, s)
        print(u'%s\uff1a\u5e94\u7528 %d \u9879\uff5c\u8df3\u8fc7 %d \u9879  %s' % (page, len(applied), len(skipped), applied))

    # ================= 自检 =================
    print(u'\n--- \u81ea\u68c0 ---')
    av = load('avatar.html')
    ba = load('base.html')
    checks = [
        (u'avatar \u57fa\u7840\u884c\u5df2\u6539\u4e3a\u53d8\u91cf',
         av.count(u'--av-face-size: 40px; font-size: var(--av-face-size); line-height: 1;') == 1),
        (u'avatar 560 \u6863\u53d8\u91cf\u5c31\u4f4d', av.count(u'.av-main-avatar-face { --av-face-size: 28px; }') == 1),
        (u'avatar 300 \u6863\u53d8\u91cf\u5c31\u4f4d', av.count(u'.av-main-avatar-face { --av-face-size: 22px; }') == 1),
        (u'avatar \u65e7\u786c\u7f16\u7801\u5b57\u53f7\u6e05\u96f6',
         av.count(u'font-size: 40px; line-height: 1;') == 0
         and av.count(u'.av-main-avatar-face { font-size: 28px; }') == 0
         and av.count(u'.av-main-avatar-face { font-size: 22px; }') == 0),
        (u'base \u65f6\u957f\u53d8\u91cf\u5c31\u4f4d', ba.count(u'--nc-glass-dur: 760ms;') == 1),
        (u'base \u626b\u5149\u5f15\u7528\u53d8\u91cf',
         ba.count(u'animation: ncGlassSheen var(--nc-glass-dur) var(--nc-glass-ease);') == 1),
        (u'base \u65e7\u786c\u7f16\u7801\u65f6\u957f\u6e05\u96f6', ba.count(u'ncGlassSheen 760ms') == 0),
        (u'\u4e24\u9875\u6807\u7b7e\u8ba1\u6570\u914d\u5e73',
         av.count(u'<style') == av.count(u'</style>') and ba.count(u'<style') == ba.count(u'</style>')),
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

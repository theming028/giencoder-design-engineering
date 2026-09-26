# -*- coding: utf-8 -*-
"""round12 / base.html
1) main 容器背景：波点/点阵 + 弥散渐变（mesh gradient，参考 wanxiaozhi.aliyun.com）
2) 对话框（composer，w-[800px]）默认宽度 → 860px
幂等。
"""
import io, sys

P = r'E:\GienCoder\giencoder-design-engineering\pages\base.html'
s = io.open(P, encoding='utf-8').read()
orig = len(s)

# ---------------------------------------------------------------- 1. dot-bg
OLD = ('.dot-bg{background-image:radial-gradient(circle, rgba(55, 112, 247, 0.1) 1.5px, transparent 1.5px);'
       'background-size:20px 20px;}')
GRAD = ('radial-gradient(42% 46% at 6% 0%, rgba(var(--giencoderblue-5), 0.20) 0%, rgba(var(--giencoderblue-5), 0) 62%),'
        'radial-gradient(36% 40% at 94% 4%, rgba(var(--purple-4), 0.18) 0%, rgba(var(--purple-4), 0) 60%),'
        'radial-gradient(46% 50% at 86% 100%, rgba(var(--cyan-4), 0.16) 0%, rgba(var(--cyan-4), 0) 64%),'
        'radial-gradient(40% 44% at 10% 96%, rgba(var(--pinkpurple-4), 0.13) 0%, rgba(var(--pinkpurple-4), 0) 60%)')
GRAD_DARK = ('radial-gradient(42% 46% at 6% 0%, rgba(var(--giencoderblue-5), 0.30) 0%, rgba(var(--giencoderblue-5), 0) 62%),'
             'radial-gradient(36% 40% at 94% 4%, rgba(var(--purple-5), 0.24) 0%, rgba(var(--purple-5), 0) 60%),'
             'radial-gradient(46% 50% at 86% 100%, rgba(var(--cyan-5), 0.20) 0%, rgba(var(--cyan-5), 0) 64%),'
             'radial-gradient(40% 44% at 10% 96%, rgba(var(--pinkpurple-5), 0.16) 0%, rgba(var(--pinkpurple-5), 0) 60%)')
DOTS = 'radial-gradient(circle, rgba(55, 112, 247, 0.1) 1.5px, rgba(0,0,0,0) 1.5px)'
SIZE = 'background-size:20px 20px,100% 100%,100% 100%,100% 100%,100% 100%;'
REPEAT = 'background-repeat:repeat,no-repeat,no-repeat,no-repeat,no-repeat;}'

NEW = ('/* r12: main 容器背景 = 波点/点阵 + 弥散渐变（mesh gradient）\n'
       '   5 层 background-image：点阵在最上层，其下 4 个大半径软色团互相叠合形成弥散色雾；\n'
       '   全部取 Token 三元组（--giencoderblue/--purple/--cyan/--pinkpurple），不硬编码色值 */\n'
       '.dot-bg{background-image:' + DOTS + ',' + GRAD + ';' + SIZE + REPEAT + '\n'
       "[giencoder-theme='dark'] .dot-bg{background-image:" + DOTS + ',' + GRAD_DARK + ';' + SIZE + REPEAT)

if 'r12: main 容器背景' in s:
    print('[1] dot-bg already patched, skip')
elif OLD in s:
    s = s.replace(OLD, NEW, 1)
    print('[1] dot-bg patched')
else:
    print('[1] !! dot-bg anchor not found'); sys.exit(1)

# ---------------------------------------------------------------- 2. 对话框 860
C860 = ('/* r12: 基础工作台对话框（composer）默认宽度 860px（原 w-[800px]；属性选择器匹配 class token，\n'
        '   避免 Tailwind 方括号类名的转义问题，特异性 0-1-1 高于 .w-\\[800px\\] 的 0-1-0） */\n'
        'main [class~="w-[800px]"]{width:860px;}\n')
if '默认宽度 860px' in s:
    print('[2] dialog width already patched, skip')
else:
    anchor = '</style>\n  </head>'
    if anchor not in s:
        anchor = '</style>  </head>'
    if anchor not in s:
        print('[2] !! head style end anchor not found'); sys.exit(1)
    s = s.replace(anchor, C860 + anchor, 1)
    print('[2] dialog width 860px inserted')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('DONE  %d -> %d chars' % (orig, len(s)))

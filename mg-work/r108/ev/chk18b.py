# -*- coding: utf-8 -*-
import io, os, re
R = r'E:/GienCoder/giencoder-design-engineering'
P = os.path.join(R, 'mg-work/r108/part108')

def rd(p):
    return io.open(p, 'rb').read().decode('utf-8').replace('\r\n', '\n')

pc = rd(os.path.join(P, 'panel.css'))
pj = rd(os.path.join(P, 'panel.js'))
mods = rd(os.path.join(P, '_mods.html'))
head = rd(os.path.join(P, '_head.html'))
conv = rd(os.path.join(R, 'pages/conversation.html'))

print('panel.css  /* %d  */ %d' % (pc.count('/*'), pc.count('*/')))
print('panel.js   /* %d  */ %d' % (pj.count('/*'), pj.count('*/')))
print()
def n(label, s, pat):
    print('%-52s %d' % (label, len(re.findall(pat, s))))
n('conv  r108-l7', conv, r'r108-l7')
n('conv  r108-l6', conv, r'r108-l6')
n('conv  data-td-prev-save', conv, r'data-td-prev-save')
n('conv  data-td-prev-reveal', conv, r'data-td-prev-reveal')
n('conv  data-td-prev-open', conv, r'data-td-prev-open')
n('conv  flex:none 规则', conv, re.escape('.td-rv-body > .td-diff { flex: none; }'))
n('conv  aria-label=最大化侧栏', conv, re.escape('aria-label="最大化侧栏"'))
n('conv  data-td-max', conv, r'data-td-max')
n('conv  td-rv-body > .td-diff', conv, re.escape('.td-rv-body > .td-diff'))
print()
print('head  菜单顺序:', re.findall(r'data-td-open-mod="([a-z]+)"', head))
print('head  最大化按钮:', head.count('aria-label="最大化侧栏"'), ' 收起按钮:', head.count('aria-label="收起侧栏"'))
print('mods  prev-save/reveal/open:', mods.count('data-td-prev-save'), mods.count('data-td-prev-reveal'), mods.count('data-td-prev-open'))
print()
# 工作区 MEMORY 字符数
wsm = rd(r'E:/GienCoder/.workbuddy/memory/MEMORY.md')
print('ws MEMORY chars =', len(wsm))
# 仓库 MEMORY/LOG、两份 log
for rel in ['.workbuddy/memory/MEMORY.md', '.workbuddy/memory/2026-10-01.md']:
    print('%-40s chars=%d' % (rel, len(rd(os.path.join(R, rel)))))
print('%-40s chars=%d' % ('ws 2026-10-01.md', len(rd(r'E:/GienCoder/.workbuddy/memory/2026-10-01.md'))))
# PLAYBOOK 附录条数
pbk = rd(os.path.join(R, '.workbuddy/memory/PLAYBOOK.md'))
print()
print('PLAYBOOK 附录条数 =', len(re.findall(r'(?m)^\d+\. ', pbk.split('## 附：工作区速览')[1])))

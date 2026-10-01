# -*- coding: utf-8 -*-
import io, os, re
R = r'E:/GienCoder/giencoder-design-engineering'
M = os.path.join(R, '.workbuddy/memory')

def rd(p):
    return io.open(p, 'rb').read().decode('utf-8').replace('\r\n', '\n')

hof = rd(os.path.join(M, 'HANDOFF.md'))
pag = rd(os.path.join(M, 'PAGES.md'))
pbk = rd(os.path.join(M, 'PLAYBOOK.md'))
mem = rd(os.path.join(M, 'MEMORY.md'))
lr = rd(os.path.join(M, '2026-10-01.md'))
lw = rd(r'E:/GienCoder/.workbuddy/memory/2026-10-01.md')
wsm = rd(r'E:/GienCoder/.workbuddy/memory/MEMORY.md')

print('== HANDOFF ==')
for k in [u'第十八拍', u'本拍九条坑', u'P3.54', u'共**十二 ~ 十八拍**', u'**三十九节**',
          u'P3.48 ~ P3.54', u'1022257', u'1141453', u'f3e0bcc1a8e2', u'9227', u'84142']:
    print(u'  %-24s %d' % (k, hof.count(k)))
print(u'  末段 head 行:', [l for l in hof.split('\n') if l.startswith('### 第十八拍')])
print(u'  l7 接回句:', hof.count(u'patch108l8.py'), u'/ r108-l7 接回:', hof.count(u'/* r108-l7 */'))
print(u'  §一 状态段:', [l[:60] for l in hof.split('\n') if l.startswith(u'★★ **r108（第十二')])

print('== PAGES ==')
print(u'  共十八拍:', pag.count(u'**共十八拍**'), u'/ ⑯ 段:', pag.count(u'**⑯ r108 第十八拍'))
print(u'  ⑯ 在 ⑮ 前:', pag.index(u'**⑯ r108 第十八拍') < pag.index(u'**⑮ r108 第十七拍'))

print('== PLAYBOOK ==')
app = pbk.split(u'## 附：工作区速览')[1]
nums = [int(x) for x in re.findall(r'(?m)^(\d+)\. ', app)]
print(u'  附录条数 %d，最大编号 %d，缺号 %r' % (len(nums), max(nums), sorted(set(range(1, max(nums) + 1)) - set(nums))))
print(u'  P3.54:', pbk.count(u'## P3.54'), u'/ 86 条标题:', pbk.count(u'## 附：工作区速览 86 条'))
print(u'  78~86:', [pbk.count(u'\n%d. ' % i) for i in range(78, 87)])
print(u'  实测字符数引用:', re.findall(u'工作区实测 \\*\\*(\\d+) 字符\\*\\*', pbk))

print('== MEMORY / LOG ==')
print(u'  repo MEMORY 第十八拍:', mem.count(u'### 第十八拍'), u'/ P3.54:', mem.count(u'P3.54'))
print(u'  log-repo:', lr.count(u'### 第十八拍'), u'/ log-ws:', lw.count(u'### 第十八拍'))
print(u'  ws MEMORY chars =', len(wsm), u'/ P3.54:', wsm.count(u'P3.54'), u'/ 86 条:', wsm.count(u'86 条'),
      u'/ 七类:', wsm.count(u'七类'))
print(u'  ws MEMORY 残留 P3.53/77 条:', wsm.count(u'P3.53'), wsm.count(u'77 条'))

print('== 工作区状态 ==')
print(u'  ws MEMORY 末尾:', repr(wsm[-60:]))

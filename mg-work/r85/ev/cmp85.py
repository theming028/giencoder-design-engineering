# -*- coding: utf-8 -*-
"""r85 设计稿 ↔ 实机 逐项对照。

设计基准：节点 1389:18725 = 840×919，坐标原点 = 内容盒左上角。
实机基准：探针 p85b.js 的 .r85-page（同原点）。
所有坐标均为「逻辑 px」，来自设计稿 2x PNG 的逐像素扫描 + 结构树，非目测。
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
o = json.loads(io.open(os.path.join(HERE, 'p85b.json'), encoding='utf-8').read())

rows = []          # (区, 项, 期望, 实测, 说明)
def chk(sec, item, exp, got, note=''):
    rows.append((sec, item, exp, got, note))

# ---------------- 页面 / 标题 ----------------
chk('页面', '内容盒 w×h', (840, 919), tuple(o['page']), '设计 919；差 −1 = 卡片2 底内距 16（见下）')
t = o['title']
chk('标题', 'y / h', (0, 28), (t['box'][1], t['box'][3]))
chk('标题', 'font-size', '20px', t['fs'])
chk('标题', 'line-height', '28px', t['lh'])

# ---------------- 卡片 ----------------
DESIGN_CARDS = [(0, 52, 840, 230), (0, 298, 840, 448), (0, 763, 840, 156)]
for i, (c, exp) in enumerate(zip(o['cards'], DESIGN_CARDS)):
    chk('卡片%d' % (i + 1), 'box (x,y,w,h)', exp, tuple(c['box']),
        '' if i != 1 else '设计框高 448 = 内容 452 − 4（底内距 16 而非 20）')
    chk('卡片%d' % (i + 1), '内描边', 'solid 1px -1px  border:0px', c['outline'] + '  border:' + c['borderW'])

# ---------------- 行 ----------------
DESIGN_ROW_Y = [[20, 94, 168], [20, 94, 168, 242, 316, 390], [20, 94]]
DESIGN_ROW_T = [
    ['Agent 预设', '权限', '繁忙时 Enter 键行为'],
    ['保持系统唤醒', '桌面通知', '声音通知', '语言', '字号', '外观'],
    ['版本更新', '账号'],
]
bad = []
for ci, c in enumerate(o['cards']):
    cy = DESIGN_CARDS[ci][1]
    for ri, r in enumerate(c['rows']):
        y, ry = r['box'][1], c['box'][1]
        exp_y = cy + DESIGN_ROW_Y[ci][ri]
        if abs(y - (ry + DESIGN_ROW_Y[ci][ri])) > 1:            # 行在卡内的相对位（卡本身容差 ±1）
            bad.append('卡片%d行%d 卡内 y=%d 期望 %d' % (ci + 1, ri, y - ry, DESIGN_ROW_Y[ci][ri]))
        if abs(y - exp_y) > 1:
            bad.append('卡片%d行%d 绝对 y=%d 期望 %d' % (ci + 1, ri, y, exp_y))
        if r['box'][0] != 20 or r['box'][2] != 800 or r['box'][3] != 42:
            bad.append('卡片%d行%d box %s' % (ci + 1, ri, r['box']))
        if [r['ic'][0] - r['box'][0], r['ic'][1] - y, r['ic'][2], r['ic'][3]] != [0, 1, 40, 40]:
            bad.append('卡片%d行%d 图标行内位 %s' % (ci + 1, ri, [r['ic'][0] - r['box'][0], r['ic'][1] - y, r['ic'][2], r['ic'][3]]))
        exp_tx = 76 if ci == 2 else 72                       # 行内 56 / 52 + 内容盒左缘 20
        if r['tx'][0] != exp_tx:
            bad.append('卡片%d行%d 文字左缘 %d 期望 %d' % (ci + 1, ri, r['tx'][0], exp_tx))
        if r['tBox'][3] != 22 or r['dBox'][3] != 16:
            bad.append('卡片%d行%d 文字高 t=%d d=%d' % (ci + 1, ri, r['tBox'][3], r['dBox'][3]))
        if r['tBox'][1] - y != 2 or r['dBox'][1] - y != 24:
            bad.append('卡片%d行%d 标题/描述行内 y=%d/%d 期望 2/24' % (ci + 1, ri, r['tBox'][1] - y, r['dBox'][1] - y))
chk('行 × 11', '卡内 y / x20 w800 h42 / 图标行内(0,1)40×40 / 文字左缘 72或76 / 标题 2..24 描述 24..40',
    '全部命中', ('全部命中' if not bad else '%d 项偏差' % len(bad)),
    ('；'.join(bad[:6]) if bad else '11 行逐项一致'))

# ---------------- 控件 ----------------
sl = o['slider']
sl_y = DESIGN_CARDS[1][1] + 316            # 卡片2 第 5 行 (字号) 行顶 + 3
chk('滑块', '容器 box', (568, sl_y + 3, 252, 36), tuple(sl['box']))
chk('滑块', '轨道 (rel)', (6, 6, 240, 1), tuple(sl['track']))
chk('滑块', '已选段 (rel)', (6, 6, 48, 1), tuple(sl['done']))
chk('滑块', '拇指 (rel)', (52, 0, 4, 12), tuple(sl['thumb']))
tick_x = [t[0][0] for t in sl['ticks']]
chk('滑块', '刻度 rel x', [6, 54, 102, 150, 198, 246], tick_x)
chk('滑块', '刻度 rel y/h', (2, 8), (sl['ticks'][0][0][1], sl['ticks'][0][0][3]))
chk('滑块', '首刻度色（is-on）', 'rgb(31, 31, 31)', sl['ticks'][0][1])
chk('滑块', '标签中心 rel x', [6, 54, 246],
    [(l[1][0] + l[1][2] / 2.0) for l in sl['lbls']])
chk('滑块', '标签文字', ['小', '默认', '大'], [l[0] for l in sl['lbls']])

sw = o['switch']                            # 保持系统唤醒 / 桌面通知 / 声音通知
SW_Y = [DESIGN_CARDS[1][1] + y + 9 for y in (20, 94, 168)]
SW_BG = ['rgb(59, 179, 70)', 'rgb(107, 107, 107)', 'rgb(59, 179, 70)']   # 开 / 关 / 开
for i, s in enumerate(sw):
    chk('开关%d' % (i + 1), 'box', (780, SW_Y[i], 40, 24), tuple(s['box']))
    chk('开关%d' % (i + 1), '底色', SW_BG[i], s['bg'])
    chk('开关%d' % (i + 1), '圆角', '12px', s['r'])
    chk('开关%d' % (i + 1), '手柄 rel', (2, 2, 20, 20) if i == 1 else (18, 2, 20, 20), tuple(s['handle']))

c3row0 = DESIGN_CARDS[2][1] + 20            # 卡片3 行0 行顶
m = o['cbMask']
chk('复选框遮罩', 'box 14×14', (516, c3row0 + 14, 14, 14), tuple(m['box']))
chk('复选框遮罩', '底色', 'rgb(55, 112, 247)', m['bg'])

SEG_Y = DESIGN_CARDS[1][1] + 390 + 1
for i, b in enumerate(o['segs']):
    chk('外观按钮%d' % (i + 1), 'box', (420 + i * 136, SEG_Y, 128, 40), tuple(b['box']))
    chk('外观按钮%d' % (i + 1), '描边', 'dashed 2px' if i == 0 else 'solid 1px', '%s %s' % (b['bd'], b['bw']))

# ---------------- 选择器（右侧靠齐行右缘 820） ----------------
DESIGN_SEL = [
    (0, 0, 98, 'Agent 预设'), (0, 1, 154, '权限'), (0, 2, 98, '繁忙时 Enter 键行为'),
    (1, 3, 70, '语言'),
]
for ci, ri, sw_, nm in DESIGN_SEL:
    r = o['cards'][ci]['rows'][ri]
    y = DESIGN_CARDS[ci][1] + DESIGN_ROW_Y[ci][ri] + 5
    got = r['kids'][0]['box'] if r['kids'] else None
    chk('选择器', '%s %d×32' % (nm, sw_), (820 - sw_, y, sw_, 32), tuple(got) if got else None)

# 卡片3 行0 控件组：复选框 76 + 12 + 更新日志 104 + 8 + 检查更新 104
c3 = o['cards'][2]['rows'][0]
c3y = DESIGN_CARDS[2][1] + 20 + 5
kids = [(k['c'], tuple(k['box'])) for k in c3['kids']]
chk('卡片3行0 控件组', '复选框 box', (516, c3row0 + 10, 76, 22), kids[0][1] if kids else None)
seq = [('更新日志/检查更新', (604 + i * 112, c3row0 + 5, 104, 32)) for i in range(2)]
for i, (nm, exp) in enumerate(seq):
    chk('卡片3行0 控件组', '按钮%d box' % (i + 1), exp, kids[1 + i][1] if len(kids) > 1 + i else None)
c3b = o['cards'][2]['rows'][1]['kids']
chk('卡片3行1', '退出登录 box', (716, DESIGN_CARDS[2][1] + 94 + 5, 104, 32),
    tuple(c3b[0]['box']) if c3b else None)
_ = c3y

# ---------------- 导航 ----------------
n = o['nav']
chk('导航', '盒 w×h', (232, 268), tuple(n['wh']))
DESIGN_NAV = [('系统设置', 76, 'rgb(236, 238, 242)'), ('模型', 114, 'rgb(247, 247, 247)'),
              ('连接器', 152, 'rgb(247, 247, 247)'), ('已归档任务', 232, 'rgb(247, 247, 247)')]
for it, (nm, y, bg) in zip(n['items'], DESIGN_NAV):
    chk('导航', '%s box' % nm, (0, y, 232, 36), tuple(it['box']))
    chk('导航', '%s 底色' % nm, bg, it['bg'])
    chk('导航', '%s 图标 rel' % nm, (12, y + 10, 16, 16), tuple(it['ic']))
    chk('导航', '%s 图标色' % nm, 'rgb(55, 112, 247)' if nm == '系统设置' else 'rgb(31, 31, 31)', it['icColor'])
for g, (nm, exp) in zip(n['groups'], [('通用', (0, 52)), ('已归档', (0, 208))]):
    chk('导航', '分组标题「%s」y' % nm, exp[1], g[1][1])

# ---------------- 输出 ----------------
def fmt(v):
    if isinstance(v, tuple): return '(' + ', '.join(str(x) for x in v) + ')'
    if isinstance(v, list):  return '[' + ', '.join(('%g' % x) if isinstance(x, (int, float)) else str(x) for x in v) + ']'
    return str(v)

def same(e, g):
    if isinstance(e, (int, float)) and isinstance(g, (int, float)):
        return abs(e - g) <= 1
    if isinstance(e, (tuple, list)) and isinstance(g, (tuple, list)) and len(e) == len(g):
        return all(same(a, b) for a, b in zip(e, g))
    return e == g

w = [0, 0, 0, 0]
for r in rows:
    for i, v in enumerate(r[:4]):
        w[i] = max(w[i], len(fmt(v)))
nbad = 0
print('%-*s %-*s %-*s %-*s %s' % (w[0], '区', w[1], '项', w[2], '设计稿', w[3], '实机', '判定'))
print('-' * (sum(w) + 20))
for sec, item, exp, got, note in rows:
    ok = same(exp, got)
    if not ok: nbad += 1
    print('%-*s %-*s %-*s %-*s %s%s' % (w[0], sec, w[1], item, w[2], fmt(exp), w[3], fmt(got),
          '✓' if ok else '✗',
          ('   ← ' + note) if note else ''))
print('-' * (sum(w) + 20))
print('共 %d 项，%d 项偏差（容差 ±1px）' % (len(rows), nbad))
sys.exit(1 if nbad else 0)

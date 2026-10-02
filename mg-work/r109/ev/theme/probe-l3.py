# -*- coding: utf-8 -*-
u"""r109 第三拍 ①②：真机取证（① 唯一原点 + 编辑态「保存」；② 卡片两端对齐）。

★ 铁律：agent-browser 的 stdout 绝不能接管道 ⇒ 一律 subprocess + 重定向到文件。
★ ① 的判据必须用**真鼠标**点击（合成 click 没有可信的 clientX/clientY，
  而且合成事件绕过 pointerdown ⇒ 会污染手势分流，见 P3.57⑧）。
"""
import io
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EV = HERE
RAW = os.path.join(REPO, 'mg-work', 'r109', 'raw')
LOG = os.path.join(EV, 'l3-origin.log')
NODE = 'C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe'
CLI = ('C:/Users/Administrator/.workbuddy/binaries/node/workspace/'
       'node_modules/agent-browser/bin/agent-browser.js')
URL = 'file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html'

_lf = io.open(LOG, 'wb')
_n = [0]


def log(s):
    _lf.write((s + '\n').encode('utf-8'))
    _lf.flush()
    print(s)


def run(*a):
    _n[0] += 1
    tmp = os.path.join(EV, 'tmp')
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    p = os.path.join(tmp, 'l3-%d.txt' % _n[0])
    with io.open(p, 'wb') as f:
        subprocess.run([NODE, CLI] + list(a), stdout=f, stderr=subprocess.STDOUT)
    return io.open(p, encoding='utf-8', errors='replace').read()


def ev(jsfile, out=None):
    t = run('eval', io.open(os.path.join(EV, jsfile), encoding='utf-8').read())
    if out:
        io.open(os.path.join(EV, out), 'wb').write(t.encode('utf-8'))
    try:
        return json.loads(json.loads(t.strip()))
    except Exception as e:
        return {'__err': str(e), '__raw': t[:500]}


def click(x, y):
    run('mouse', 'move', str(x), str(y))
    run('mouse', 'down')
    run('mouse', 'up')


def main():
    log('=== r109 第三拍 ①② 真机取证 ===')
    run('close', '--all')
    run('set', 'viewport', '1440', '900')
    run('open', URL + '?v=%d' % (time.time() * 1000))
    run('wait', '4400')

    a = ev('p-l3a.js', 'l3-a.json')
    log('【预备】目标块 = %s' % a.get('target'))
    log('        isAnnotating=%s  已有锚点=%s' % (a.get('isAnnotating'), a.get('existingAnchors')))
    log('        targetBox=%s' % json.dumps(a.get('targetBox')))
    log('        目标块中心 = %s' % json.dumps(a.get('targetCenter')))
    log('        ★ 真实点击点 = %s   （= 目标块左起 56 / 上起 22）' % json.dumps(a.get('click')))
    cx, cy = a['click']['x'], a['click']['y']

    click(cx, cy)
    run('wait', '700')
    run('eval', 'window.__CLICK={x:%d,y:%d};"ok"' % (cx, cy))
    b = ev('p-l3b.js', 'l3-b.json')
    log('')
    log('【① 唯一原点（提交前 · 只有气泡）】')
    log('        anchorCount=%s  elnoteHidden=%s' % (b.get('anchorCount'), b.get('elnoteHidden')))
    log('        真实点击点(视口) = %s' % json.dumps(b.get('clickViewport')))
    log('        真实点击点(内容坐标) = %s' % json.dumps(b.get('clickContent')))
    log('        气泡(内容坐标) l=%s t=%s  尺寸 %sx%s  css left=%s'
        % (b.get('bubble', {}).get('l'), b.get('bubble', {}).get('t'),
           b.get('bubbleSize', {}).get('w'), b.get('bubbleSize', {}).get('h'), b.get('bubbleCssLeft')))
    log('        ★ 气泡左 − 点击点 = %s   （期望 ≈ 0：气泡**左边缘**钉在点击点上）' % b.get('dLeft'))
    log('        新增态按钮 = 「%s」 / 「%s」(display=%s)  hint display=%s  pin=%s(is-done=%s)'
        % (b.get('okText'), b.get('cancelText'), b.get('cancelDisplay'), b.get('hintDisplay'),
           b.get('pin'), b.get('pinDone')))
    log('        占位符 = %r' % b.get('taPlaceholder'))

    c = ev('p-l3c.js', 'l3-c.json')
    log('')
    log('【① 提交】提交前 okText=「%s」  提交前锚点数=%s'
        % (c.get('okTextBeforeCommit'), c.get('beforeCommit', {}).get('anchorCount')))
    log('        提交后锚点数=%s  elnoteHidden=%s  left/top=%s/%s'
        % (c.get('afterCommit', {}).get('anchorCount'), c.get('afterCommit', {}).get('elnoteHidden'),
           c.get('afterCommit', {}).get('styleLeft'), c.get('afterCommit', {}).get('styleTop')))
    log('        锚点中心(视口) = %s' % json.dumps(c.get('anchorCenter')))

    ac = c.get('anchorCenter') or {}
    if ac.get('x'):
        click(ac['x'], ac['y'])                     # ★ 真鼠标点开锚点
        run('wait', '700')
        d = ev('p-l3d.js', 'l3-d.json')
        log('')
        log('【① 编辑态（真鼠标点开已存在锚点）】')
        log('        elnoteHidden=%s  按钮 = 「%s」 / cancel display=%s'
            % (d.get('elnoteHidden'), d.get('okText'), d.get('cancelDisplay')))
        log('        pin=%s is-done=%s okDisabled=%s  taValue=%r'
            % (d.get('pin'), d.get('pinDone'), d.get('okDisabled'), d.get('taValue')))
        log('        气泡顶 − 锚点底 = %s   气泡左 − 锚点左 = %s   锚点数=%s'
            % (d.get('bubbleDTop'), d.get('bubbleLeftDx'), d.get('anchorCount')))
        run('screenshot', ' ' + os.path.join(RAW, 'l3-note-edit.png'))

    log('')
    log('【② 卡片两端对齐】')
    log('        %s' % json.dumps(c.get('card'), ensure_ascii=False)[:600])
    log('        r93-card 全量 dLeft/marginLeft 抽查：')
    for r in (c.get('cardsAll') or []):
        log('          dLeft=%-8s ml=%-8s %s' % (r['dLeft'], r['ml'], r['cls'][:70]))

    run('close', '--all')
    log('=== 完成 ===')
    return 0


if __name__ == '__main__':
    sys.exit(main())

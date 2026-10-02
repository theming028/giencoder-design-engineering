# -*- coding: utf-8 -*-
u"""r109 第三拍 ③-b：设置页「外观」三档的**真机点击**取证（★ 一律真鼠标）。

为什么必须真鼠标：交互类判据不能用合成 click —— 合成 `el.click()` 不经过 `pointerdown`，
会绕过任何手势分流（P3.57⑧）。这里 3 枚按钮全部用 `mouse move/down/up`。

★ 铁律：agent-browser 的 stdout **绝不能接管道**（CLI 把 stdout 交给常驻守护进程 ⇒ 管道永不 EOF）。
  本脚本一律 `subprocess` + **stdout 重定向到文件**，跑完再读文件。

覆盖：
  A 初始态（未点）            —— 默认档 auto + `aria-pressed` 回填正确
  B 点「深色」                —— attr=dark / stored=dark / 外壳底色翻暗
  C 点「浅色」                —— attr 摘掉 / stored=light / 外壳底色回浅
  D 点「跟随系统」            —— stored=auto
  E `set media dark` 后       —— ★ auto 真的跟随系统（MQ change 事件驱动）
  F `set media light` 后      —— 跟随回来
  G reload 后                 —— 档位持久化 + pressed 回填（不会「显示浅色、实际 auto」）

产出：ev/theme/a-pressed.log（全过程）+ ev/theme/s-*.json（每步状态）
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
RAW = os.path.join(REPO, 'mg-work', 'r109', 'raw', 'theme')
LOG = os.path.join(EV, 'a-pressed.log')

NODE = 'C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe'
CLI = ('C:/Users/Administrator/.workbuddy/binaries/node/workspace/'
       'node_modules/agent-browser/bin/agent-browser.js')
PAGE = 'file:///E:/GienCoder/giencoder-design-engineering/pages/settings.html'

_lf = io.open(LOG, 'wb')


def log(s):
    _lf.write((s + '\n').encode('utf-8'))
    _lf.flush()
    print(s.encode('utf-8', 'replace').decode('utf-8'))


def run(*args):
    u"""★ 全程重定向到文件（绝不用管道）。返回 (exit, 文件内容)。"""
    tag = args[0].replace('/', '_')[:24]
    tmp = os.path.join(EV, 'tmp')
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    p = os.path.join(tmp, 'ab-%s-%d.txt' % (tag, int(time.time() * 1000) % 100000))
    with io.open(p, 'wb') as f:
        r = subprocess.run([NODE, CLI] + list(args), stdout=f, stderr=subprocess.STDOUT)
    return r.returncode, io.open(p, encoding='utf-8', errors='replace').read()


def ev(jsfile, out=None):
    js = io.open(os.path.join(EV, jsfile), encoding='utf-8').read()
    rc, out_txt = run('eval', js)
    if out is not None:
        io.open(os.path.join(EV, out), 'wb').write(out_txt.encode('utf-8'))
    try:
        return json.loads(json.loads(out_txt.strip()))
    except Exception as e:
        return {'__parse_error': str(e), '__raw': out_txt[:400]}


def click(x, y):
    run('mouse', 'move', str(x), str(y))
    run('mouse', 'down')
    run('mouse', 'up')


def brief(tag, s):
    log('  %-22s mode=%-5s attr=%-5s data=%-5s stored=%-5s pressed=%-18s bg1=%-9s shell=%s'
        % (tag, s.get('mode'), str(s.get('attr')), str(s.get('dataAttr')),
           str(s.get('stored')), str(s.get('pressed')), str(s.get('bg1')), str(s.get('shellBg'))))


def main():
    log('=== r109 ③-b 设置页「外观」真机取证（全真鼠标）===')
    run('close', '--all')
    run('set', 'viewport', '1440', '900')
    run('set', 'media', 'light')                    # 系统档先归浅，保证 auto 的基线可读
    run('open', PAGE + '?v=%d' % (time.time() * 1000))
    run('wait', '5500')

    seg = ev('p-seg.js', 's-seg.json')
    log('  分段控件：%s' % json.dumps(seg, ensure_ascii=False)[:400])
    if not seg.get('ok'):
        log('!! 找不到 .r85-seg，终止')
        return 1
    items = seg['items']
    labels = [it['label'] for it in items]
    log('  文案 = %s' % json.dumps(labels, ensure_ascii=False))
    if labels[:3] != [u'浅色', u'深色', u'跟随系统']:
        log('!! 文案与预期不符（应 [浅色, 深色, 跟随系统]）')

    # 面板可能在折线以下 ⇒ 先滚进来，再重量一次坐标
    run('scrollintoview', '.r85-seg')
    run('wait', '600')
    seg = ev('p-seg.js', 's-seg2.json')
    items = seg['items']

    st = ev('p-state.js', 's-A-initial.json')
    brief('A 初始', st)

    click(items[1]['cx'], items[1]['cy'])           # 深色
    run('wait', '900')
    brief('B 点「深色」', ev('p-state.js', 's-B-dark.json'))
    run('wait', '1500')
    run('screenshot', os.path.join(RAW, 'dark', 'settings-appearance.png'))

    click(items[0]['cx'], items[0]['cy'])           # 浅色
    run('wait', '900')
    brief('C 点「浅色」', ev('p-state.js', 's-C-light.json'))

    click(items[2]['cx'], items[2]['cy'])           # 跟随系统
    run('wait', '900')
    brief('D 点「跟随系统」', ev('p-state.js', 's-D-auto.json'))

    run('set', 'media', 'dark')
    run('wait', '1200')
    brief('E 系统转暗', ev('p-state.js', 's-E-auto-sysdark.json'))

    run('set', 'media', 'light')
    run('wait', '1200')
    brief('F 系统转浅', ev('p-state.js', 's-F-auto-syslight.json'))

    run('reload')
    run('wait', '5500')
    brief('G reload 后', ev('p-state.js', 's-G-reload.json'))

    run('close', '--all')
    log('=== 完成 ===')
    return 0


if __name__ == '__main__':
    sys.exit(main())

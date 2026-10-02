# -*- coding: utf-8 -*-
u"""r109 第三拍 ③-b 补图：把设置页「外观」滚进视口 → 切暗色 → 定向截图（含分段控件）。"""
import io
import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
RAW = os.path.join(REPO, 'mg-work', 'r109', 'raw', 'theme')
NODE = 'C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe'
CLI = ('C:/Users/Administrator/.workbuddy/binaries/node/workspace/'
       'node_modules/agent-browser/bin/agent-browser.js')
PAGE = 'file:///E:/GienCoder/giencoder-design-engineering/pages/settings.html'
LG = os.path.join(HERE, 'pb-shot.log')
_lf = io.open(LG, 'wb')


_n = [0]


def run(*a):
    _n[0] += 1
    p = os.path.join(HERE, 'tmp', 'x%d.txt' % _n[0])
    with io.open(p, 'wb') as f:
        subprocess.run([NODE, CLI] + list(a), stdout=f, stderr=subprocess.STDOUT)
    return io.open(p, encoding='utf-8', errors='replace').read()


run('close', '--all')
run('set', 'viewport', '1440', '900')
run('set', 'media', 'light')
run('open', PAGE + '?v=%d' % (time.time() * 1000))
run('wait', '5500')
run('scrollintoview', '.r85-seg')
run('wait', '800')
out = run('eval', io.open(os.path.join(HERE, 'p-seg.js'), encoding='utf-8').read())
s = json.loads(json.loads(out.strip()))
_lf.write(('滚动后 .r85-seg: ' + json.dumps(s, ensure_ascii=False) + '\n').encode('utf-8'))
run('eval', "document.querySelector('.r85-seg').closest('[class*=rounded]').getBoundingClientRect().toJSON()"
    " + '|' + window.scrollY")
panel = run('eval', "JSON.stringify({sy:window.scrollY,box:(function(){var e=document.querySelector("
           "'.r85-seg');var r=e.getBoundingClientRect();return [r.left,r.top,r.width,r.height];})()})")
_lf.write(('panel: ' + panel.strip()[:300] + '\n').encode('utf-8'))
run('eval', "window.__giTheme.set('dark')")
run('wait', '1600')
run('screenshot', os.path.join(RAW, 'dark', 'settings-appearance.png'))
_lf.flush()
print(io.open(LG, encoding='utf-8').read())
print('---')
print(s)

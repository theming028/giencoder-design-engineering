# -*- coding: utf-8 -*-
u"""r109 第四拍 · 侦察驱动：**逐子屏**跑暗色「亮面元素」探针。

★★ 铁律：agent-browser 的 stdout 绝不能接管道（CLI 把写端交给常驻守护进程 ⇒ 管道永不 EOF
   ⇒ 命令挂死）⇒ 一律 subprocess + 重定向到文件。

用法： python mg-work/r109/ev/theme/probe-subscreens.py [页面...]
"""
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EV = os.path.join(REPO, 'mg-work', 'r109', 'ev', 'theme')
OUT = os.path.join(REPO, 'mg-work', 'r109', 'raw', 'mix4')
NODE = u'C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe'
CLI = u'C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js'

DEFAULT = ['base', 'avatar', 'automation', 'skills', 'settings']


def run(*args):
    u"""⚠⚠ `stdout=PIPE` 会**永久挂死**：CLI 把写端交给它 fork 的常驻守护进程 ⇒ 管道永不 EOF。
       ⇒ 只引导向 DEVNULL / 文件。"""
    subprocess.run([NODE, CLI] + list(args), stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, cwd=REPO)


def runto(path, *args):
    with io.open(path, 'wb') as f:
        subprocess.run([NODE, CLI] + list(args), stdout=f, stderr=subprocess.STDOUT, cwd=REPO)
    raw = io.open(path, encoding='utf-8', errors='replace').read().strip()
    try:
        v = json.loads(raw)
        while isinstance(v, str):
            v = json.loads(v)
        return v
    except Exception:
        return None


def js(name):
    return io.open(os.path.join(EV, name), encoding='utf-8').read()


def click(x, y):
    run('mouse', 'move', str(x), str(y))
    run('mouse', 'down')
    run('mouse', 'up')


def main():
    pages = sys.argv[1:] or DEFAULT
    os.makedirs(OUT, exist_ok=True)
    run('close', '--all')
    run('set', 'viewport', '1440', '900')
    report = {}
    for pg in pages:
        url = u'file:///E:/GienCoder/giencoder-design-engineering/pages/%s.html?v=%d' % (pg, os.getpid())
        runto(os.path.join(EV, 'ps-open-%s.log' % pg), 'open', url)
        run('wait', '4200')
        nav = runto(os.path.join(OUT, 'clicks-%s.json' % pg), 'eval', js('p-clicks.js')) or {}
        items = nav.get('items', [])
        print(u'== %s：%d 个子屏 ==' % (pg, len(items)))
        rows = []
        for k, it in enumerate(items):
            if k:
                click(it['x'], it['y'])
                run('wait', '1400')
            r = runto(os.path.join(OUT, 'sub-%s-%d.json' % (pg, k)), 'eval', js('p-mix.js'))
            if not r:
                print(u'   ! %s 探针无返回' % it['label'])
                continue
            rows.append((it['label'], r))
            run('eval', "var e=document.getElementById('probe-notrans'); if(e) e.remove(); 'ok'")
            san = r.get('sanity', {})
            print(u'   · %-10s 亮面 %-28s 合计 %-3d  自证 bg1=%s bodyBg=%s'
                  % (it['label'], str(r.get('counts')), r.get('total', 0), san.get('bg1'), san.get('bodyBg')))
            for x in r.get('items', [])[:8]:
                print(u'        %-6s %-19s %sx%s @%s,%s %s | %s'
                      % (x['k'], x['v'], x['w'], x['h'], x['x'], x['y'], x['sel'][-48:], x['txt']))
        report[pg] = rows
    run('close', '--all')
    io.open(os.path.join(OUT, 'subscreens.json'), 'w', encoding='utf-8').write(
        json.dumps(report, ensure_ascii=False, indent=1))
    print(u'\n→ %s' % os.path.join(OUT, 'subscreens.json'))


if __name__ == '__main__':
    main()

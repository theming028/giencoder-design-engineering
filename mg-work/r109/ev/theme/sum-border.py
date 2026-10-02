# -*- coding: utf-8 -*-
"""解析 scan-border.sh 的产物（JSON 套 JSON），打成浅/暗对照表。"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
OUT = os.path.join(ROOT, 'mg-work', 'r109', 'raw', 'bd10')

KEYS = ['--gray-1', '--gray-2', '--gray-3', '--gray-4',
        '--color-border-1', '--color-border-2', '--color-border-3']


def load(p):
    raw = io.open(p, encoding='utf-8').read().strip()
    try:
        d = json.loads(raw)
    except Exception:
        return None
    if isinstance(d, str):
        try:
            d = json.loads(d)
        except Exception:
            return None
    return d


import io  # noqa: E402

rows = []
for f in sorted(glob.glob(os.path.join(OUT, '*-light.json'))):
    pg = os.path.basename(f).replace('-light.json', '')
    dl = load(f)
    dd = load(os.path.join(OUT, pg + '-dark.json'))
    if not dl or not dd:
        rows.append((pg, None, None))
        continue
    rows.append((pg, dl, dd))

print('页           档     theme     块   ' + ''.join('%16s' % k.replace('--color-', '').replace('--', '') for k in KEYS))
print('-' * (38 + 16 * len(KEYS)))
for pg, dl, dd in rows:
    if dl is None:
        print('%-12s  解析失败' % pg)
        continue
    for tag, d in (('浅', dl), ('暗', dd)):
        v = d.get('v', {})
        print('%-12s  %-4s  %-8s %-3s ' % (pg, tag, str(d.get('theme'))[:8],
                                           'Y' if d.get('hasBlock') else 'N')
              + ''.join('%16s' % str(v.get(k, '?'))[:15] for k in KEYS))
print()
for pg, dl, dd in rows:
    if dl is None:
        continue
    s = dl.get('sample')
    s2 = dd.get('sample')
    print('%-12s 实测元素  浅 %s / 暗 %s'
          % (pg, (s['bc'] if s else '无'), (s2['bc'] if s2 else '无')))

# -*- coding: utf-8 -*-
"""扫「会被 apply88b.converge 压平」的规则。

模拟 apply88b 的往返（unscale → scale_block），逐规则报告：
  规则体里有 `line-height/height/min-height: calc(Npx * var(--ui-fs-ratio))`
  但**体里没有 `var(--font-size-*)` token** ⇒ unscale 会把它还原成裸 Npx，
  而 scale_block 只在体含 token 时才重派生 ⇒ **声明被永久压平**，`--ui-fs` 杠杆失效。
"""
import io, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

RATIO = r'var\(--ui-fs-ratio\)'
RE_SCALED_H2 = re.compile(r'(?<![-\w])height:\s*calc\((\d+(?:\.\d+)?)px \* ' + RATIO + r'\);\s*'
                          r'min-height:\s*calc\((\d+(?:\.\d+)?)px \* ' + RATIO + r'\)')
RE_SCALED_MH = re.compile(r'min-height:\s*calc\((\d+(?:\.\d+)?)px \* ' + RATIO + r'\)')
RE_SCALED_LH = re.compile(r'line-height:\s*calc\((\d+(?:\.\d+)?)px \* ' + RATIO + r'\)')
RE_HAS_FS = re.compile(r'var\(--font-size-[a-z0-9-]+\)')
RE_PLAIN = re.compile(r'(?<![-\w])(line-height|height|min-height):\s*(\d+(?:\.\d+)?)px')

for rel in sys.argv[1:]:
    p = os.path.join(ROOT, rel)
    s = io.open(p, 'rb').read().decode('utf-8')
    stripped = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    hits = []
    for m in re.finditer(r'([^{}]*)\{([^{}]*)\}', stripped):
        sel, body = m.group(1).strip(), m.group(2)
        if not RE_SCALED_LH.search(body) and not RE_SCALED_H2.search(body) and not RE_SCALED_MH.search(body):
            continue
        if RE_HAS_FS.search(body):
            continue                                  # 体含 token ⇒ scale 会重派生，自愈
        flat = []
        if RE_SCALED_LH.search(body):
            flat.append('line-height')
        if RE_SCALED_H2.search(body) or RE_SCALED_MH.search(body):
            flat.append('height/min-height')
        hits.append((sel.splitlines()[-1].strip()[:70] if sel else '(?)', ', '.join(flat),
                     ' '.join(body.split())[:120]))
    print('===== %s → %d 条会被压平' % (rel, len(hits)))
    for sel, props, body in hits:
        print('  >>> %s\n      [%s]  %s' % (sel, props, body))

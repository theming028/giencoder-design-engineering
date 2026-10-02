# -*- coding: utf-8 -*-
u"""apply-tokens.py 的**落盘前干跑**：把替换后的页面写到 `tmp/dry/`，并把每个
`<script>` 块单独导出成 `.mjs` / `.cjs`，交给 `node --check` 验语法。

为什么必须做这一步：
  批次三/四是**纯文本替换**，目标里含着 229~324KB 的**编译产物**。一旦把字面换成了
  会破坏 JS 语法的东西（多引号、断字符串、坏模板字面），页面只会**白屏**，
  而 `check-syntax.py` / `verify-design.py` 都查不出来（它们看的是 HTML 骨架与颜色 token）。
  ⇒ 判据 = **`node --check` 逐块通过**（比截图更早、更便宜）。
"""
import importlib.util
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NODE = r'C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe'

spec = importlib.util.spec_from_file_location('at', os.path.join(HERE, 'apply-tokens.py'))
at = importlib.util.module_from_spec(spec)
spec.loader.exec_module(at)

OUT = os.path.join(HERE, 'tmp', 'dry')
if not os.path.isdir(OUT):
    os.makedirs(OUT)

scripts = []          # (标签, 路径)
for pg in at.ALL:
    p = os.path.join(at.PAGES, pg + '.html')
    t, nl = at.rd(p)
    sink = []
    parts = []
    last = 0
    changed = 0
    prev_end = 0
    # ★★ 必须与 `apply-tokens.py` 的 `main()` 用**同一套分段**（`segs`，含 HTML 静态区伪块），
    #    否则干跑出来的字节数与真跑的落盘结果对不上 ⇒ 这一步就失去意义。
    for bid, tag, s, e, body in at.segs(t):
        assert s >= prev_end, (pg, bid, s, prev_end)
        prev_end = e
        if bid in at.SKIP_BID:
            continue
        if tag == 'html':                       # 第七批·C：静态内联 style 属性
            nb, k = at.rewrite_inline(body, sink)
        elif tag == 'style':
            if bid == u'(anon)' and at.DS_FINGERPRINT in body:
                continue
            nb, k = at.rewrite_body(tag, body, sink)
        else:
            nb, k = at.rewrite_scripts(body, sink)
        if k:
            parts.append(t[last:s])
            parts.append(nb)
            last = e
            changed += k
    parts.append(t[last:])
    t2 = u''.join(parts)
    dst = os.path.join(OUT, pg + '.html')
    io.open(dst, 'wb').write(t2.replace(u'\n', nl).encode('utf-8'))
    print(u'%-13s 原 %7d → 新 %7d（Δ%+6d） 替换 %d 处'
          % (pg, len(t), len(t2), len(t2) - len(t), changed))
    # 导出每个 script 块（替换后的版本）
    for i, (bid, tag, s, e, body) in enumerate(at.blocks(t2)):
        if tag != 'script':
            continue
        fn = os.path.join(OUT, u'%s-s%02d.mjs' % (pg, i))
        io.open(fn, 'wb').write(body.encode('utf-8'))
        scripts.append((u'%s#%d(%s,%d)' % (pg, i, bid[:14], e - s), fn))

print(u'\n── node --check（%d 块）──' % len(scripts))
bad = 0
for label, fn in scripts:
    r = subprocess.run([NODE, '--check', fn], stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    if r.returncode != 0:
        # 退一步：当成 CommonJS 再试（classic script）
        fn2 = fn[:-4] + u'.cjs'
        io.open(fn2, 'wb').write(io.open(fn, 'rb').read())
        r2 = subprocess.run([NODE, '--check', fn2], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
        if r2.returncode != 0:
            bad += 1
            print(u'   ✗ %-34s %s' % (label, r2.stdout.decode('utf-8', 'replace')[:200].replace(u'\n', u' | ')))
print(u'   node --check：%d/%d 通过' % (len(scripts) - bad, len(scripts)))
sys.exit(1 if bad else 0)

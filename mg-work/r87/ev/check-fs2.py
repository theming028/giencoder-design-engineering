import re, io, glob, os

SC = r'calc\(\d+(?:\.\d+)?px \* var\(--ui-fs-ratio\)\)'
pat_h = re.compile(r'(?<![-\w])height:\s*%s;\s*min-height:\s*%s' % (SC, SC))
pat_lh = re.compile(r'line-height:\s*%s' % SC)

print('---- settings.html 里被派生的规则（选择器 + 属性） ----')
s = io.open('pages/settings.html', encoding='utf-8').read()
for m in re.finditer(r'([^{}]{1,120})\{([^{}]*)\}', s):
    body = m.group(2)
    if 'var(--ui-fs-ratio)' not in body:
        continue
    hits = pat_h.findall(body) + pat_lh.findall(body)
    if hits:
        sel = m.group(1).strip().split('\n')[-1]
        props = re.findall(r'(?:line-height|(?<![-\w])height):\s*calc\([^;]*?\)', body)
        print('   %-42s %s' % (sel[-42:], props))

print()
print('---- 各页派生计数（修正后的正则） ----')
for f in sorted(glob.glob('pages/*.html')):
    t = io.open(f, encoding='utf-8', errors='ignore').read()
    print('  %-20s lh=%-4d h=%-4d' % (os.path.basename(f), len(pat_lh.findall(t)), len(pat_h.findall(t))))

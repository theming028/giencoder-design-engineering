import re, io, glob, os, collections
print('regex self-test:')
for p in [r'height:\s*\d+(?:\.\d+)?px', r'(?<![-\w])height:\s*\d+(?:\.\d+)?px']:
    print('  ', p, '->', bool(re.search(p, 'height:32px')))


def rules(css):
    out = []
    i = 0
    n = len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0:
            break
        k = css.find('}', j)
        if k < 0:
            break
        out.append((css[i:j], css[j + 1:k]))
        i = k + 1
    return out


agg = collections.Counter()
for f in sorted(glob.glob('pages/*.html')):
    s = io.open(f, encoding='utf-8', errors='ignore').read()
    for css in re.findall(r'<style[^>]*>(.*?)</style>', s, re.S):
        for sel, body in rules(css):
            if re.search(r'(?<![-\w])height:\s*\d+(?:\.\d+)?px', body):
                agg[sel.strip()[-70:]] += 1
print('含 height:px 的规则 %d 条：' % len(agg))
for k in sorted(agg):
    print('  ', k)

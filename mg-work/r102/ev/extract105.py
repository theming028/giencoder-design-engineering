import io, os, re, sys, hashlib

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
A = os.path.join(REPO, 'pages', 'avatar.html')
t = io.open(A, encoding='utf-8').read()

start = t.find('AV-BROWSE-SLOT v1')
print('marker idx', start)
end = t.find('<script id="av-chat-js">', start)
print('chat-js idx', end)
blob = t[start-20:end]
print('blob len', len(blob))
print('blob head:', repr(blob[:200]))
print('blob tail:', repr(blob[-200:]))

m_css = re.search(r'<style id="av-browse-css">\n(.*?)\n</style>', blob, re.S)
m_js = re.search(r'<script id="av-browse-js">\n(.*?)\n</script>\n*$', blob, re.S)
print('css match', bool(m_css), 'js match', bool(m_js))
css = m_css.group(1)
js = m_js.group(1)
# HTML 居中段
i_css_end = m_css.end()
i_js_start = m_js.start()
html = blob[i_css_end:i_js_start]
print('html len', len(html), 'head', repr(html[:160]), 'tail', repr(html[-160:]))

out = os.path.join(REPO, 'mg-work', 'r102', 'part105')
os.makedirs(out, exist_ok=True)
io.open(os.path.join(out, 'browse.css'), 'w', encoding='utf-8', newline='').write(css)
io.open(os.path.join(out, 'browse.html'), 'w', encoding='utf-8', newline='').write(html)
io.open(os.path.join(out, 'browse.js'), 'w', encoding='utf-8', newline='').write(js)

for name, cur in (('part-css.css', css), ('part-html.txt', html), ('part-ctrl.js', js)):
    old = io.open(os.path.join(REPO, 'mg-work/r69', name), encoding='utf-8').read()
    print('%-14s  r69=%-7d avatar=%-7d  %s' % (
        name, len(old), len(cur),
        'IDENTICAL' if old == cur else 'DIFF'))

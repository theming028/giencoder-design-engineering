# -*- coding: utf-8 -*-
import io, re
s = io.open('pages/avatar.html', encoding='utf-8').read()
css = "\n".join(re.findall(r'<style[^>]*>(.*?)</style>', s, re.S))
print("style 块数:", [len(x) for x in re.findall(r'<style[^>]*>(.*?)</style>', s, re.S)])
cls = ['.select-view-ghost', '.giencoder-select-popup', '.giencoder-popup-open',
       '.giencoder-select-view', '.giencoder-select-option', '.giencoder-btn-secondary',
       '.avatar-wrap', '.avatar-tooltip', '.td-right', '.td-file',
       '.select-view-ghost{', '.giencoder-select-popup.giencoder-popup-open{']
for c in cls:
    print("  %-42s inCSS=%d  inPage=%d" % (c, css.count(c), s.count(c)))
print("\n--- token 定义检查 ---")
toks = ['--color-primary-light-2', '--border-radius-medium', '--border-radius-large',
        '--font-size-body-1', '--font-size-body-3', '--transition-timing-function-standard',
        '--color-fill-3', '--color-bg-5', '--color-border-2', '--color-text-4', '--color-text-2',
        '--shadow2-down', '--border-radius-xl', '--color-fill-1', '--color-fill-2']
for t in toks:
    print("  %-40s defined=%s" % (t, bool(re.search(re.escape(t) + r'\s*:', css))))

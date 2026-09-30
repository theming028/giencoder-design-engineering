import re, io

s = io.open('giencoder-design-system/components.css', encoding='utf-8').read()
for cls in ['.giencoder-input-wrapper', '.giencoder-input', '.giencoder-btn-size-default',
            '.giencoder-select-view', '.giencoder-textarea']:
    out = []
    for m in re.finditer(r'([^{}]{0,200})' + re.escape(cls) + r'([^{}]{0,120})\{([^}]*)\}', s):
        body = m.group(3)
        if re.search(r'(?<![-\w])height:', body) or 'min-height' in body:
            out.append((m.group(1).strip()[-40:] + cls + m.group(2).strip(),
                        [x for x in body.split(';') if 'height' in x]))
    print('==', cls)
    for sel, h in out[:6]:
        print('   ', sel[:90], '->', h)

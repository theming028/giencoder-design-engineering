import re, io, glob, os

for f in sorted(glob.glob('pages/*.html')):
    s = io.open(f, encoding='utf-8', errors='ignore').read()
    head_end = s.find('</head>')
    # 所有 style/script 块的起始位置
    blocks = [(m.start(), m.group(1), m.group(2))
              for m in re.finditer(r'<(style|script)([^>]*)>', s)]
    token_root = s.find('--font-size-body-3')
    print('%-20s head_end=%d  token_root=%d  token在head内=%s'
          % (os.path.basename(f), head_end, token_root, token_root < head_end))
    # body 区的 style 块里是否重定义了 --font-size-*
    for pos, tag, attrs in blocks:
        if tag != 'style':
            continue
        end = s.find('</style>', pos)
        blk = s[pos:end]
        if pos < head_end:
            continue
        redecl = re.findall(r'--font-size-[a-z0-9-]+\s*:', blk)
        m = re.search(r'id="([^"]+)"', attrs)
        print('      BODY-STYLE id=%-14s len=%-6d 重定义字号token=%s'
              % (m.group(1) if m else '(无)', len(blk), redecl if redecl else '无'))

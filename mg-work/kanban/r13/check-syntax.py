import re, io, os, subprocess, sys
NODE = r'C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe'
path = sys.argv[1]
s = io.open(path, encoding='utf-8').read()
blocks = re.findall(r'<script[^>]*>(.*?)</script>', s, re.S)
os.makedirs('mg-work/kanban/r13/chk', exist_ok=True)
ok = True
for i, b in enumerate(blocks):
    f = 'mg-work/kanban/r13/chk/%s-%d.js' % (os.path.basename(path).replace('.html',''), i)
    io.open(f, 'w', encoding='utf-8').write(b)
    r = subprocess.run([NODE, '--check', f], capture_output=True, text=True)
    status = 'OK' if r.returncode == 0 else 'FAIL'
    if r.returncode != 0:
        ok = False
    print('%s  block#%d  %d chars' % (status, i, len(b)))
    if r.returncode != 0:
        print(r.stderr[:800])
print('ALL_OK' if ok else 'HAS_FAIL')

import re, io, glob, os, collections

s = io.open('pages/skills.html', encoding='utf-8').read()
print('ui-fs-ratio 出现次数:', s.count('var(--ui-fs-ratio)'))
print('r87-ui-css 存在:', 'id="r87-ui-css"' in s)
print('r87-ui-js  存在:', 'id="r87-ui-js"' in s)
i = s.find('<style id="r87-ui-css">')
print('---- 注入块 ----')
print(s[i:s.find('</style>', i) + 8])

print('\n---- 行高派生样本 ----')
for m in list(re.finditer(r'line-height:calc\([^)]*\)[^;}]*', s))[:8]:
    print('  ', m.group(0))

print('\n---- 高度派生样本 ----')
for m in list(re.finditer(r'(?<![-\w])height:calc\([^)]*\);min-height:calc\([^)]*\)', s))[:8]:
    print('  ', m.group(0))
print('  height+min-height 派生总数:', len(re.findall(r'(?<![-\w])height:calc\([^)]*\);min-height:calc\([^)]*\)', s)))
print('  行高派生总数:', len(re.findall(r'line-height:calc\(', s)))

print('\n---- 各页派生规模 ----')
for f in sorted(glob.glob('pages/*.html')):
    t = io.open(f, encoding='utf-8', errors='ignore').read()
    print('  %-20s lh=%-4d h=%-4d ratio=%d'
          % (os.path.basename(f),
             len(re.findall(r'line-height:calc\(', t)),
             len(re.findall(r'(?<![-\w])height:calc\([^)]*\);min-height:calc\([^)]*\)', t)),
             t.count('var(--ui-fs-ratio)')))

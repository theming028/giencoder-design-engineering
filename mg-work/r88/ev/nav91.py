import os
from PIL import Image, ImageDraw

RAW = 'mg-work/r88/raw'

# aside 元素截图原点 = aside 左上角（实测 aside 视口 y=48，nav 在 aside 内 y=0）
#   back      aside-local y  0.. 32   ⇒ 净区 y 16
#   system    aside-local y 76..112   ⇒ 净区 y 94   （选中态）
#   model     aside-local y114..150   ⇒ 净区 y132   （未选中）
#   connector aside-local y152..188   ⇒ 净区 y170
#   archived  aside-local y232..268   ⇒ 净区 y250
X = 230  # 远离图标(16px@12)与文字，落在项内空白处

d = Image.open(os.path.join(RAW, 'web-nav-r91-def@1x.png')).convert('RGB')
b = Image.open(os.path.join(RAW, 'web-nav-r91-backhover@1x.png')).convert('RGB')
h = Image.open(os.path.join(RAW, 'web-nav-r91-navihover@1x.png')).convert('RGB')


def g(im, y):
    return im.getpixel((X, y))


print('=== aside 底 / 各控件底色（x=%d） ===' % X)
print('%-24s %-20s %-20s %s' % ('位置', '默认态', 'hover返回钮', 'hover菜单项(模型)'))
rows = [('空闲区 y64', 64), ('返回钮 y16', 16), ('选中 system y94', 94),
        ('未选中 model y132', 132), ('未选中 connector y170', 170), ('未选中 archived y250', 250)]
for label, y in rows:
    print('%-24s %-20s %-20s %s' % (label, g(d, y), g(b, y), g(h, y)))

print()
print('=== 断言 ===')
print('  返回钮 hover 底 =', g(b, 16), '  菜单项 hover 底 =', g(h, 132), '  选中态底 =', g(d, 94))
print('  三者一致 :', g(b, 16) == g(h, 132) == g(d, 94))
print('  菜单默认底(= aside 底 #F4F5F6 即"无底") :', g(d, 132) == g(d, 64), g(d, 132))
print('  返回钮默认底(= aside 底) :', g(d, 16) == g(d, 64), g(d, 16))

# ---- 三联并排 ----
Z = 2
imgs = [('default', d), ('hover BACK', b), ('hover MENU item', h)]
crops = []
for name, im in imgs:
    c = im.crop((0, 0, 256, 290))
    crops.append((name, c.resize((c.width * Z, c.height * Z), Image.NEAREST)))
GAP = 10
W = sum(c.width for _, c in crops) + GAP * (len(crops) - 1)
H = crops[0][1].height
cv = Image.new('RGB', (W, H + 20), (255, 0, 255))
dr = ImageDraw.Draw(cv)
x = 0
for name, c in crops:
    cv.paste(c, (x, 20))
    dr.text((x + 4, 5), name, fill=(255, 255, 255))
    x += c.width + GAP
cv.save(os.path.join(RAW, 'nav91-triple.png'))
print('\nsaved nav91-triple.png', cv.size)

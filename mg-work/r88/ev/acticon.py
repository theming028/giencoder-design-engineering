import os
from PIL import Image, ImageDraw

RAW = 'mg-work/r88/raw'
# 聚焦第 1 行右侧两个图标钮（design px）：x 736..840, y 150..186
BOX = (736, 150, 840, 186)
Z = 5

design = Image.open(os.path.join(RAW, 'arch@2x_rgb.png')).convert('RGB')
design = design.resize((840, 658), Image.LANCZOS)          # 1680x1316 → 840x658
r90 = Image.open(os.path.join(RAW, 'web-arch-r90@1x.png')).convert('RGB')
r91 = Image.open(os.path.join(RAW, 'web-arch-r91@1x.png')).convert('RGB')

panels = [('design', design), ('before r90', r90), ('after r91', r91)]
crops = []
for name, im in panels:
    c = im.crop(BOX)
    crops.append((name, c.resize((c.width * Z, c.height * Z), Image.NEAREST)))

GAP = 12
W = sum(c.width for _, c in crops) + GAP * (len(crops) - 1)
H = crops[0][1].height
cv = Image.new('RGB', (W, H + 22), (255, 0, 255))
dr = ImageDraw.Draw(cv)
x = 0
for name, c in crops:
    cv.paste(c, (x, 22))
    dr.text((x + 4, 6), name, fill=(255, 255, 255))
    x += c.width + GAP
cv.save(os.path.join(RAW, 'acticon-90-91.png'))
print('saved acticon-90-91.png', cv.size)

# 取图标最暗像素做数值对照
def darkest(im, box):
    best = (255, 255, 255)
    for y in range(box[1], box[3]):
        for x in range(box[0], box[2]):
            p = im.getpixel((x, y))
            if sum(p) < sum(best):
                best = p
    return best

for name, im in panels:
    print('%-11s 图标最暗像素 = %s  #%02X%02X%02X' % (name, darkest(im, BOX), *darkest(im, BOX)))

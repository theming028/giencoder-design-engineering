"""r65 量测（二）：文字/图标墨迹 + 按钮 —— 设计稿 2x 截图 → CSS px"""
from PIL import Image
from measure import load, CX, CY, OX, OY, SC, alpha_bounds, ink

R = '/Users/shaoyuming/.mgmcp/resources/screenshots/193158744355579/958-18307/'

TARGETS = {
    '容器-165_1350-18230.png': {
        'title':        (24, 14, 200, 48),
        'close':        (430, 14, 470, 48),
        'subtitle':     (24, 48, 460, 76),
        'cardLabel':    (40, 100, 200, 126),
        'cardText':     (40, 124, 450, 182),
        'dividerText':  (180, 206, 300, 244),
        'placeholder':  (36, 254, 200, 290),
        'helper':       (24, 338, 340, 372),
        'btnCancel':    (296, 394, 366, 434),
        'btnOk':        (364, 394, 460, 434),
    },
    '容器-171_1350-18236.png': {
        'title':        (24, 14, 200, 48),
        'close':        (430, 14, 470, 48),
        'subtitle':     (24, 48, 460, 76),
        'cardLabel':    (40, 100, 200, 126),
        'cardText':     (40, 124, 450, 162),
        'dividerText':  (180, 168, 300, 206),
        'placeholder':  (36, 216, 200, 252),
        'helper':       (24, 300, 340, 334),
        'btnCancel':    (296, 356, 366, 396),
        'btnOk':        (364, 356, 460, 396),
    },
}

for name, t in TARGETS.items():
    im = load(name)
    print('=' * 74)
    print('###', name)
    for k, box in t.items():
        b = ink(im, *box)
        if b is None:
            print(f'  {k:12} (无墨迹)')
        else:
            print(f'  {k:12} ink CSS=({b[0]:6.1f},{b[1]:6.1f}) - ({b[2]:6.1f},{b[3]:6.1f})  宽={b[2]-b[0]+0.5:6.1f} 高={b[3]-b[1]+0.5:5.1f}')
    # 取色
    print('  --- 取色 ---')
    pts = {
        'card 底(内部)': (200, 140 if '165' in name else 128),
        'card 描边(上边)': (200, 90.2),
        'divider 线': (100, 224.5 if '165' in name else 186.5),
        'textarea 底': (200, 300 if '165' in name else 250),
        'textarea 描边(上边)': (200, 248.2 if '165' in name else 210.2),
    }
    for k, (cx, cy) in pts.items():
        x = int(round(OX + cx * SC)); y = int(round(OY + cy * SC))
        print(f'    {k:18} rgb={im.getpixel((x, y))}')

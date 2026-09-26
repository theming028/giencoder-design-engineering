from PIL import Image
for name in ['crt-open','design']:
    im = Image.open('mg-work/r15/%s.png' % name).convert('RGB')
    print(name, im.size)

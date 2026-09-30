# -*- coding: utf-8 -*-
"""从 MasterGo 本地 HTTP 取设计稿截图（base64 JSON）→ 落盘 PNG。

用法：
  python fetch-mg.py <documentId> <documentPageId> <targetNodeId> [scale] [out.png]

⚠ 该接口**只返回当前画布选中的节点**（传别的节点仍回选中页）。
⚠ 首次约 21s、缓存 0.4s；**必须 GET + query**（POST 400）。
"""
import io
import json
import os
import sys
import base64
import urllib.request

API = 'http://127.0.0.1:30678/api/getScreenshot'


def fetch(doc, page, node, scale=2, timeout=120):
    url = '%s?documentId=%s&documentPageId=%s&targetNodeId=%s&scale=%s' % (
        API, doc, page, node, scale)
    req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    d = json.loads(raw.decode('utf-8'))
    if not d.get('success'):
        raise SystemExit('接口 success=false：%s' % raw[:300])
    imgs = d.get('images') or []
    if not imgs:
        raise SystemExit('接口无 images 字段：%s' % raw[:300])
    im = imgs[0]
    if not im.get('success'):
        raise SystemExit('节点 %s 导出失败' % im.get('nodeId'))
    return base64.b64decode(im['base64']), im.get('nodeId'), im.get('byteLength')


def main():
    a = sys.argv[1:]
    if len(a) < 3:
        raise SystemExit(__doc__)
    doc, page, node = a[0], a[1], a[2]
    scale = a[3] if len(a) > 3 else '2'
    out = a[4] if len(a) > 4 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'mg-%s@%sx.png' % (node.replace(':', '-'), scale))
    data, nid, bl = fetch(doc, page, node, scale)
    io.open(out, 'wb').write(data)
    # 尺寸
    try:
        from PIL import Image
        with Image.open(io.BytesIO(data)) as im:
            print('OK  node=%s  %s  %s  bytes=%d' % (nid, im.size, im.mode, len(data)))
    except Exception as e:
        print('OK  node=%s  bytes=%d  (PIL 读失败 %s)' % (nid, len(data), e))
    print('保存 →', out)


if __name__ == '__main__':
    main()

#!/usr/bin/env bash
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
URL="http://127.0.0.1:8866/pages/task-detail.html"
$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.8
echo "=== 当前 overflow / 祖先链 ==="
$AB eval "JSON.stringify((function(){var r=document.querySelector('.td-root'),m=document.querySelector('main'),w=r.parentElement;return {main:{ov:getComputedStyle(m).overflow,rect:[Math.round(m.getBoundingClientRect().left),Math.round(m.getBoundingClientRect().right)]},wrap:{ov:getComputedStyle(w).overflow},root:{ov:getComputedStyle(r).overflow,rect:[Math.round(r.getBoundingClientRect().left),Math.round(r.getBoundingClientRect().right)]}};})())"
echo "=== 实验：放开 root / wrap / main 的 overflow ==="
$AB eval "(function(){var r=document.querySelector('.td-root');r.style.overflow='visible';r.parentElement.style.overflow='visible';document.querySelector('main').style.overflow='visible';return 1;})()" >/dev/null 2>&1
sleep 0.4
echo "  scrollbar: docScrollW=$($AB eval "document.documentElement.scrollWidth") clientW=$($AB eval "document.documentElement.clientWidth") bodyH=$($AB eval "document.body.scrollHeight") winH=$($AB eval "window.innerHeight")"
$AB screenshot "mg-work/r24/r24-shadow-exp.png" >/dev/null 2>&1
$PY - <<'PY'
from PIL import Image
im = Image.open('mg-work/r24/r24-shadow-exp.png').convert('RGB'); px = im.load()
bg = px[2, 400]
print('  bg =', bg)
for y in (200, 400):
    print('  y=%d 左缘: %s' % (y, '  '.join('%d:%s' % (x, px[x, y]) for x in range(3, 12))))
print('  左栏上缘 x=400:', '  '.join('y%d:%s' % (y, px[400, y]) for y in range(44, 52)))
print('  左栏下缘 x=400:', '  '.join('y%d:%s' % (y, px[400, y]) for y in range(888, 900)))
print('  两栏间隙 y=400:', '  '.join('%d:%s' % (x, px[x, 400]) for x in range(942, 956)))
PY

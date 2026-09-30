#!/usr/bin/env bash
# r105 ③ 文件预览栏自身交互：右键菜单 / 关闭 / 拖拽 / 文件树开合选中
cd /e/GienCoder/giencoder-design-engineering || exit 1
NODE=/c/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe
AB=/c/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js
R=mg-work/r102/raw
V=$(date +%s)

"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$V" >/dev/null 2>&1
"$NODE" "$AB" wait 2600 >/dev/null 2>&1

echo "=== 打开预览栏 ==="
"$NODE" "$AB" eval "(function(){document.querySelector('[data-r93-browse]').click();return 'clicked';})()" 2>&1
"$NODE" "$AB" wait 1000 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){
  var s=document.getElementById('av-browse-slot');
  return JSON.stringify({ctxBound:s?s.getAttribute('data-td-ctx-bound'):null,
    files:document.querySelectorAll('.td-bf').length,
    active:document.querySelectorAll('.td-bf.is-active').length,
    crumb:(document.querySelector('.td-browse-crumb-path')||{}).textContent,
    close:!!document.querySelector('[data-td-browse-close]'),
    treeTgl:!!document.querySelector('[data-td-tree-toggle]'),
    openBtn:!!document.querySelector('[data-td-open-browser]')});
})()" 2>&1

echo
echo "=== 文件树：点一个目录（开合） ==="
"$NODE" "$AB" eval "(function(){var d=document.querySelectorAll('.td-bf.is-dir');for(var i=0;i<d.length;i++){if(!d[i].classList.contains('is-closed')){d[i].setAttribute('data-p105j','1');return 'tagged '+i;}}return 'none';})()" 2>&1
"$NODE" "$AB" click '[data-p105j="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 400 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var d=document.querySelector('[data-p105j=\"1\"]');return JSON.stringify({closed:d.classList.contains('is-closed'), hidden:[].slice.call(document.querySelectorAll('.td-bf')).filter(function(r){return r.classList.contains('is-hidden')}).length});})()" 2>&1

echo
echo "=== 文件树：点一个文件（选中） ==="
"$NODE" "$AB" eval "(function(){var f=document.querySelectorAll('.td-bf.is-file');var t=null;for(var i=0;i<f.length;i++){if(!f[i].classList.contains('is-hidden')){f[i].setAttribute('data-p105k','1');t=f[i];break;}}return t?(t.querySelector('.td-bf-name')||{}).textContent:'none';})()" 2>&1
"$NODE" "$AB" click '[data-p105k="1"]' >/dev/null 2>&1
"$NODE" "$AB" wait 400 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var a=document.querySelector('.td-bf.is-active');return JSON.stringify({activeName:a?(a.querySelector('.td-bf-name')||{}).textContent:null, activeBefore:getComputedStyle(a||document.body).backgroundColor});})()" 2>&1

echo
echo "=== 右击文件（上下文菜单） ==="
"$NODE" "$AB" eval "(function(){var a=document.querySelector('.td-bf.is-active');if(!a)return 'no-active';a.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:1000,clientY:400,button:2}));return 'dispatched';})()" 2>&1
"$NODE" "$AB" wait 500 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var m=document.querySelector('.td-ctx');var r=m?m.getBoundingClientRect():null;return JSON.stringify({exists:!!m, open:m?m.classList.contains('giencoder-popup-open'):null, rect:r?[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]:null, items:document.querySelectorAll('.td-ctx .giencoder-dropdown-item').length, ctxOpenAttr:document.documentElement.hasAttribute('data-td-ctx-open')});})()" 2>&1
"$NODE" "$AB" screenshot "" "$R/x105-4-ctx.png" >/dev/null 2>&1
echo "  shot x105-4-ctx.png"

echo
echo "=== Esc 关菜单（预览栏应仍在） ==="
"$NODE" "$AB" press Escape >/dev/null 2>&1
"$NODE" "$AB" wait 500 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var m=document.querySelector('.td-ctx');return JSON.stringify({ctxOpen:m?m.classList.contains('giencoder-popup-open'):null, browseOn:!!document.querySelector('.av-browse-on')});})()" 2>&1

echo
echo "=== 拖拽分栏条（宽 641 → 加大） ==="
"$NODE" "$AB" eval "(function(){
  var sp=document.getElementById('av-browse-split');
  var r=sp.getBoundingClientRect();
  var x=Math.round(r.left+r.width/2), y=Math.round(r.top+r.height/2);
  window.__w0=getComputedStyle(document.getElementById('av-browse-slot')).flexBasis;
  sp.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true,clientX:x,clientY:y,button:0,pointerId:1}));
  sp.dispatchEvent(new PointerEvent('pointermove',{bubbles:true,cancelable:true,clientX:x-60,clientY:y,button:0,pointerId:1}));
  sp.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,cancelable:true,clientX:x-60,clientY:y,button:0,pointerId:1}));
  window.__w1=getComputedStyle(document.getElementById('av-browse-slot')).flexBasis;
  return JSON.stringify({w0:window.__w0,w1:window.__w1});
})()" 2>&1
"$NODE" "$AB" wait 500 >/dev/null 2>&1
"$NODE" "$AB" eval "getComputedStyle(document.getElementById('av-browse-slot')).flexBasis" 2>&1
"$NODE" "$AB" eval "localStorage.getItem('giencoder:r105-browse:v1')" 2>&1

echo
echo "=== 关闭按钮 ==="
"$NODE" "$AB" eval "(function(){document.querySelector('[data-td-browse-close]').click();return 'clicked';})()" 2>&1
"$NODE" "$AB" wait 800 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){return JSON.stringify({browseOn:!!document.querySelector('.av-browse-on'), asideW:Math.round(document.querySelector('aside').getBoundingClientRect().width), mainW:Math.round(document.querySelector('main').getBoundingClientRect().width)});})()" 2>&1

#!/usr/bin/env bash
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
W="${1:-1440}"; H="${2:-900}"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport "$W" "$H" >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 2600 >/dev/null 2>&1

echo "===== E1) 聚焦 composer → 基线截图 ====="
"$NODE" "$AB" click "textarea" >/dev/null 2>&1
"$NODE" "$AB" wait 500 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/e1-base.png" >/dev/null 2>&1
echo "  shot e1-base.png"

echo "===== E1b) 宿主 overflow:visible ====="
"$NODE" "$AB" eval "(function(){var h=document.querySelector('.r93-conv-host');h.style.overflow='visible';return 'ok';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 300 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/e1-ovf.png" >/dev/null 2>&1
echo "  shot e1-ovf.png"

echo "===== E1c) 宿主 display:none ====="
"$NODE" "$AB" eval "(function(){var h=document.querySelector('.r93-conv-host');h.style.overflow='';h.style.display='none';return 'ok';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 300 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/e1-none.png" >/dev/null 2>&1
echo "  shot e1-none.png"

echo "===== E1d) 宿主 position:static ====="
"$NODE" "$AB" eval "(function(){var h=document.querySelector('.r93-conv-host');h.style.display='';h.style.position='static';return 'ok';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 300 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/e1-pos.png" >/dev/null 2>&1
echo "  shot e1-pos.png"

echo "===== E1e) hero 加 z-index:5 ====="
"$NODE" "$AB" eval "(function(){var h=document.querySelector('.r93-conv-host');h.style.position='';var hero=document.querySelector('main > div > div.flex-1.justify-center');hero.style.position='relative';hero.style.zIndex='5';return 'ok';})()" >/dev/null 2>&1
"$NODE" "$AB" wait 300 >/dev/null 2>&1
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/e1-z5.png" >/dev/null 2>&1
echo "  shot e1-z5.png"

echo "===== E2) 折叠逐帧（顶层 fold#0 / 嵌套 fold#11 / 大块 fold#10） ====="
"$NODE" "$AB" eval "(function(){var hero=document.querySelector('main > div > div.flex-1.justify-center');hero.style.position='';hero.style.zIndex='';
  var res={};
  window.__run=function(idx,key){
    var fs=document.querySelectorAll('.r93-fold'); var f=fs[idx]; if(!f) return 'no fold '+idx;
    var h=f.querySelector(':scope > .r93-fh'); if(!h) return 'no fh';
    h.scrollIntoView({block:'center'});
    var fb=f.querySelector(':scope > .r93-fb');
    var rec=[]; var t0=performance.now();
    function tick(){ var t=performance.now()-t0; var c=getComputedStyle(fb);
      rec.push([Math.round(t), Math.round(fb.getBoundingClientRect().height), c.maxHeight, c.opacity, c.transform, c.overflow, document.getAnimations().length]);
      if(t<620) requestAnimationFrame(tick); else { window.__rec[key]=rec; } }
    requestAnimationFrame(tick);
    setTimeout(function(){ h.click(); }, 40);
    return 'started '+key+' open='+f.getAttribute('data-open');
  };
  return JSON.stringify({folds:document.querySelectorAll('.r93-fold').length});
})()"
"$NODE" "$AB" eval "window.__run(0,'f0')"
"$NODE" "$AB" wait 1100 >/dev/null 2>&1
"$NODE" "$AB" eval "window.__run(11,'f11')"
"$NODE" "$AB" wait 1100 >/dev/null 2>&1
"$NODE" "$AB" eval "window.__run(10,'f10')"
"$NODE" "$AB" wait 1100 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){var o={};['f0','f11','f10'].forEach(function(k){o[k]=(window.__rec[k]||[]).length;});return JSON.stringify(o);})()"
"$NODE" "$AB" eval "JSON.stringify(window.__rec, null, 0)"

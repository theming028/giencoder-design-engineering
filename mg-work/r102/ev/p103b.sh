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

echo "===== B1) composer 几何与祖先链（未聚焦） ====="
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p103b.js)"
echo
echo "===== B2) 聚焦后（.focus()） ====="
"$NODE" "$AB" eval "(function(){var ce=document.querySelector('[contenteditable]');if(ce){ce.focus();}return ce?('focused '+ce.tagName):'no ce';})()"
"$NODE" "$AB" wait 400 >/dev/null 2>&1
"$NODE" "$AB" eval "$(cat mg-work/r102/ev/p103b.js)"
echo
echo "===== B3) 真鼠标点击 composer ====="
"$NODE" "$AB" click "[contenteditable]" >/dev/null 2>&1
"$NODE" "$AB" wait 500 >/dev/null 2>&1
"$NODE" "$AB" eval "(function(){
  function R(el){var r=el.getBoundingClientRect();return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom)};}
  function cls(el){return (el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||'';}
  var ce=document.querySelector('[contenteditable]');
  if(!ce) return 'no ce';
  var res={active:document.activeElement?document.activeElement.tagName+'.'+cls(document.activeElement).slice(0,60):null, chain:[]};
  var n=ce;
  while(n && n!==document.body){
    var c=getComputedStyle(n);
    res.chain.push({t:n.tagName,c:cls(n).slice(0,80),r:R(n),ov:c.overflow,sh:c.boxShadow,bd:c.borderTopWidth+' '+c.borderTopColor+' | '+c.borderBottomWidth+' '+c.borderBottomColor,outline:c.outline,br:c.borderRadius});
    n=n.parentElement;
  }
  return JSON.stringify(res,null,1);
})()"
echo
"$NODE" "$AB" screenshot "" "mg-work/r102/raw/p103b-focus-${W}.png" >/dev/null 2>&1
echo "  shot p103b-focus-${W}.png"

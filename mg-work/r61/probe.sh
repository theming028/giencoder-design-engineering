#!/bin/zsh
# r61 运行时验收：图标尺寸 + 「取消任务」红色系 hover（:hover 与 .is-hover 两条路径）
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
NODE=/Users/shaoyuming/.workbuddy/binaries/node/versions/22.22.2-3/bin/node
MJS=/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r61/hover-menu.mjs
EV=/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r61/ev
mkdir -p "$EV"

$AB open "file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/task-detail.html" > /dev/null
$AB set viewport 1440 900 > /dev/null
sleep 0.5

echo "### 1) 打开「更多操作」菜单，并读出两项的静态几何"
$AB eval '(function(){
  var b=document.querySelector("[data-td-more]");
  if(b.getAttribute("aria-expanded")!=="true") b.click();
  var m=document.querySelector(".td-more");
  if(!m) return "菜单未生成";
  var out=["menu="+Math.round(m.getBoundingClientRect().width)+"x"+Math.round(m.getBoundingClientRect().height)];
  Array.prototype.forEach.call(m.querySelectorAll(".giencoder-dropdown-item"),function(r){
    var ic=r.querySelector(".td-more-ico"), sv=ic?ic.querySelector("svg"):null, lb=r.querySelector(".td-more-label");
    var mr=m.getBoundingClientRect();
    out.push("  ["+r.className+"] \""+r.textContent.trim()+"\" iconBox="+Math.round(ic.getBoundingClientRect().width)+"x"+Math.round(ic.getBoundingClientRect().height)
      +" svg="+Math.round(sv.getBoundingClientRect().width)+"x"+Math.round(sv.getBoundingClientRect().height)
      +" labelLeftOffset="+Math.round(lb.getBoundingClientRect().left-mr.left)
      +" itemBg="+getComputedStyle(r).backgroundColor+" itemColor="+getComputedStyle(r).color
      +" icoColor="+getComputedStyle(ic).color);
  });
  var rows=m.querySelectorAll(".giencoder-dropdown-item");
  var r=rows[1].getBoundingClientRect();
  out.push("CANCEL_XY="+(r.left+r.width/2)+","+(r.top+r.height/2));
  return out.join("\n");
})()'

echo ""
echo "### 2) 【:hover 真实鼠标】CDP 悬停「取消任务」"
CDP=$($AB get cdp-url 2>/dev/null | tail -1 | tr -d '"')
XY=$($AB eval '(function(){var m=document.querySelector(".td-more");var r=m.querySelectorAll(".giencoder-dropdown-item")[1].getBoundingClientRect();return Math.round(r.left+r.width/2)+","+Math.round(r.top+r.height/2)})()' | tail -1 | tr -d '"')
echo "  目标坐标: $XY"
$NODE "$MJS" "$CDP" "pages/task-detail.html" ${XY%,*} ${XY#*,}

echo ""
echo "### 3) 【.is-hover 键盘虚拟焦点】↑ 移到「取消任务」"
$AB eval '(function(){
  document.querySelector("[data-td-more]").focus();
  return "focused";
})()' > /dev/null
$AB eval '(function(){
  var ev=new KeyboardEvent("keydown",{key:"ArrowDown",bubbles:true});
  document.querySelector("[data-td-more]").dispatchEvent(ev);
  document.dispatchEvent(new KeyboardEvent("keydown",{key:"ArrowDown",bubbles:true}));
  var m=document.querySelector(".td-more");
  return Array.prototype.map.call(m.querySelectorAll(".giencoder-dropdown-item"),function(r){
    return "["+r.textContent.trim()+"] cls="+r.className+" bg="+getComputedStyle(r).backgroundColor+" color="+getComputedStyle(r).color
      +" icoColor="+getComputedStyle(r.querySelector(".td-more-ico")).color;
  }).join("\n");
})()'

echo ""
echo "### 4) 关闭菜单（Esc）+ 复位"
$AB eval '(function(){document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape",bubbles:true}));return "esc"})()' > /dev/null
sleep 0.4
$AB eval '(function(){var m=document.querySelector(".td-more");return "menu display="+(m?getComputedStyle(m).display:"-")+" aria-expanded="+document.querySelector("[data-td-more]").getAttribute("aria-expanded")})()'

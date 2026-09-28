#!/bin/zsh
# r62 运行时验收：「执行中」卡片标题的文字流光（Text Shimmer）
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r62/ev
mkdir -p "$EV"

$AB open "file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/kanban.html" > /dev/null
$AB set viewport 1440 900 > /dev/null
sleep 1.0

echo "### 1) 命中检查 + 计算样式全量"
$AB eval '(function(){
  var cards=document.querySelectorAll(".kb-card");
  var run=null;
  Array.prototype.forEach.call(cards,function(c){ if(c.querySelector(".kb-running")) run=c; });
  if(!run) return "NO RUNNING CARD";
  var t=run.querySelector(".kb-card-title");
  var cs=getComputedStyle(t);
  var others=Array.prototype.map.call(document.querySelectorAll(".kb-card-title"),function(e){
    var c=getComputedStyle(e);
    return "   "+(c.animationName==="kb-title-shimmer"?"[流光]":"[静置]")+" \""+String(e.textContent).slice(0,10)+"\" anim="+c.animationName;
  });
  var r=t.getBoundingClientRect();
  return [
    "命中卡片标题: \""+t.textContent+"\"  字数="+t.textContent.length,
    "内联 --kb-shimmer-spread = "+t.style.getPropertyValue("--kb-shimmer-spread")+"   (期望 "+(t.textContent.length*2)+"px)",
    "backgroundImage    = "+cs.backgroundImage,
    "backgroundSize     = "+cs.backgroundSize,
    "backgroundRepeat   = "+cs.backgroundRepeat,
    "backgroundClip     = "+cs.backgroundClip,
    "color              = "+cs.color,
    "-webkit-text-fill  = "+cs.webkitTextFillColor,
    "animation          = "+cs.animationName+" | "+cs.animationDuration+" | "+cs.animationIterationCount+" | "+cs.animationTimingFunction,
    "titleRect          = ("+Math.round(r.left)+","+Math.round(r.top)+") "+Math.round(r.width)+"x"+Math.round(r.height),
    "全页卡片标题状态:",
    others.join("\n")
  ].join("\n");
})()'

echo ""
echo "### 2) 四相位采样（证明 background-position 真的在动）+ 抓帧"
for i in 1 2 3 4; do
  P=$($AB eval '(function(){var c=document.querySelector(".kb-card:has(.kb-running)");return getComputedStyle(c.querySelector(".kb-card-title")).backgroundPosition})()' | tail -1 | tr -d '"')
  echo "  phase$i  backgroundPosition = $P"
  $AB screenshot "$EV/1$i-kanban-phase$i-1440.png" > /dev/null
  sleep 0.5
done
echo "  已存 4 张相位截图"

echo ""
echo "### 3) 静置卡片对照（同页另一张卡的标题，应完全无流光）"
$AB eval '(function(){
  var t=Array.prototype.filter.call(document.querySelectorAll(".kb-card-title"),function(e){return getComputedStyle(e).animationName!=="kb-title-shimmer"})[0];
  var cs=getComputedStyle(t);
  return "对照卡 \""+String(t.textContent).slice(0,10)+"\" backgroundImage="+cs.backgroundImage+" animation="+cs.animationName+" color="+cs.color;
})()'

echo ""
echo "### 4) 整页截图（看板全貌）"
$AB screenshot "$EV/20-kanban-full-1440.png" > /dev/null
echo "saved 20-kanban-full-1440.png"

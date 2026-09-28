#!/bin/zsh
# r63 运行时验收：进行中泳道字重 + 流光新配色（DOM 断言）
set -e
cd /Users/shaoyuming/Documents/GienCoderDesignEngineering
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser

$AB open "file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/kanban.html" >/dev/null
$AB set viewport 1440 900 >/dev/null
sleep 1.0

echo "=== ① 各泳道标题字重（base 态）==="
$AB eval '(function(){
  var out=[];
  ["kb-col--todo","kb-col--doing","kb-col--stop","kb-col--done"].forEach(function(c){
    var col=document.querySelector("."+c);
    if(!col){out.push(c+" (缺失)");return;}
    var ts=col.querySelectorAll(".kb-card-title");
    var fw=[];Array.prototype.forEach.call(ts,function(t){fw.push(getComputedStyle(t).fontWeight)});
    out.push(col.querySelector(".kb-col-name").textContent.trim()+" ("+c+") 卡="+ts.length+" 字重=["+fw.join(",")+"]");
  });
  return out.join("\n");
})()'

echo ""
echo "=== ② hover 态字重（CDP 前先用 JS 模拟 :hover 不可行，此处量 .is-hover 无关；改为读规则命中）==="
$AB eval '(function(){
  var out=[];
  var t=document.querySelector(".kb-col--todo .kb-card-title");
  out.push("待开始首卡 base 字重 = "+getComputedStyle(t).fontWeight);
  var d=document.querySelector(".kb-col--doing .kb-card-title");
  out.push("进行中首卡 base 字重 = "+getComputedStyle(d).fontWeight);
  return out.join("\n");
})()'

echo ""
echo "=== ③ 流光新配色（命中卡）==="
$AB eval '(function(){
  var t=document.querySelector(".kb-card:has(.kb-running) .kb-card-title");
  if(!t) return "!! 未命中流光卡";
  var cs=getComputedStyle(t);
  return [
    "文字内容 = \""+t.textContent+"\"（"+t.textContent.length+" 字）",
    "font-weight = "+cs.fontWeight,
    "backgroundImage = "+cs.backgroundImage,
    "backgroundSize = "+cs.backgroundSize,
    "animationName = "+cs.animationName+" / duration "+cs.animationDuration+" / "+cs.animationIterationCount,
    "color = "+cs.color+" / -webkit-text-fill-color = "+cs.webkitTextFillColor,
    "--kb-shimmer-spread = "+t.style.getPropertyValue("--kb-shimmer-spread")
  ].join("\n");
})()'

echo ""
echo "=== ④ 全页流光命中数（应恰好 1）==="
$AB eval '(function(){
  var all=document.querySelectorAll(".kb-card-title"),n=0,names=[];
  Array.prototype.forEach.call(all,function(e){
    if(getComputedStyle(e).animationName==="kb-title-shimmer"){n++;names.push(e.textContent.slice(0,12));}
  });
  return "全页标题="+all.length+" | 流光命中="+n+" | "+names.join(" / ");
})()'

echo ""
echo "=== ⑤ 几何与溢出（进行中列）==="
$AB eval '(function(){
  var col=document.querySelector(".kb-col--doing");
  var t=document.querySelector(".kb-card:has(.kb-running) .kb-card-title");
  var card=t.closest(".kb-card");
  var cr=card.getBoundingClientRect(), tr=t.getBoundingClientRect();
  var out=["列宽="+Math.round(col.getBoundingClientRect().width),
           "卡片="+Math.round(cr.width)+" (内宽 "+card.clientWidth+")",
           "流光标题盒="+Math.round(tr.width)+"x"+Math.round(tr.height)+" @ x"+Math.round(tr.left),
           "标题盒占卡片内宽 "+(Math.round(tr.width/card.clientWidth*1000)/10)+"%"];
  var bad=[];
  Array.prototype.forEach.call(col.querySelectorAll("*"),function(e){
    var cs=getComputedStyle(e);
    if(e.scrollWidth>e.clientWidth+1 && cs.overflowX!=="visible"){
      var cls=String(e.className||"");
      bad.push("<"+e.tagName.toLowerCase()+"."+cls+"> clientW="+e.clientWidth+" scrollW="+e.scrollWidth+" ovX="+cs.overflowX);
    }
  });
  out.push("内层溢出节点="+bad.length+(bad.length?"\n  "+bad.join("\n  "):""));
  return out.join("\n");
})()'

echo ""
echo "=== ⑥ 其它列标题盒几何（应与改前一致：块级撑满）==="
$AB eval '(function(){
  var out=[];
  ["kb-col--todo","kb-col--stop","kb-col--done"].forEach(function(c){
    var t=document.querySelector("."+c+" .kb-card-title");
    var card=t.closest(".kb-card");
    out.push(c+" 标题盒宽="+Math.round(t.getBoundingClientRect().width)+" 卡片内宽="+card.clientWidth+" 字重="+getComputedStyle(t).fontWeight);
  });
  return out.join("\n");
})()'

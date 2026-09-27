#!/usr/bin/env bash
# 第23轮实测：外壳研发工作台态 / 右栏标题字重 / 卡片链接 hover / 顶栏标题 16-500 /
#              顶栏右侧补间隔线与双按钮 / 信息列底部补创建者信息
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/task-detail.html"
KB="http://127.0.0.1:8866/pages/kanban.html"

$AB open "$URL" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 2.8

$AB eval "
(function(){
  var r=document.querySelector('.td-root');
  var shell=document.querySelector('div.flex.h-dvh');
  var hd=shell.querySelector('header');
  var row=shell.querySelector(':scope > div');
  var tl=document.querySelector('[role=tablist]');
  var ind=tl?tl.querySelector(':scope > span[aria-hidden]'):null;
  var base=tl?tl.querySelector('[data-tab=base]'):null;
  var dev=tl?tl.querySelector('[data-tab=dev]'):null;
  var cs=function(e){return e?getComputedStyle(e):{};};
  var bt=document.querySelector('.td-bar-title');
  var rt=document.querySelector('.td-right-title');
  var acts=document.querySelector('.td-bar-actions');
  var sep=document.querySelector('.td-bar-sep');
  var navs=document.querySelectorAll('.td-bar-nav .giencoder-btn');
  var more=document.querySelector('[aria-label=\"更多操作\"]');
  var cards=document.querySelectorAll('.td-file');
  var foot=document.querySelector('.td-side-foot');
  var side=r.querySelector('.td-side');
  var G=function(e){var b=e.getBoundingClientRect();return {l:Math.round(b.left),t:Math.round(b.top),w:Math.round(b.width),h:Math.round(b.height),r:Math.round(b.right)};};
  return JSON.stringify({
    '1_shell': {
      shellBg: cs(shell).backgroundColor,
      headerBg: cs(hd).backgroundColor,
      rowBg: cs(row).backgroundColor,
      rowPad: cs(row).paddingLeft+' / '+cs(row).paddingRight,
      asideDisp: cs(shell.querySelector(':scope > div > aside')).display,
      tabs: Array.from(document.querySelectorAll('[role=tab]')).map(function(b){return b.dataset.tab+':'+b.getAttribute('aria-selected')}).join(','),
      indLeft: ind?cs(ind).left:null, indWidth: ind?cs(ind).width:null,
      baseColor: base?cs(base).color:null, devColor: dev?cs(dev).color:null,
      mainBorder: cs(document.querySelector('main')).borderTopWidth,
      rootBg: cs(r).backgroundColor
    },
    '2_rightTitle': { fs: cs(rt).fontSize, fw: cs(rt).fontWeight },
    '4_barTitle': { fs: cs(bt).fontSize, fw: cs(bt).fontWeight, lh: cs(bt).lineHeight },
    '5_barActions': {
      count: acts.querySelectorAll('.giencoder-btn').length,
      more: more?G(more):null,
      sep: sep?G(sep):null,
      sepBg: sep?cs(sep).backgroundColor:null,
      navs: Array.from(navs).map(function(b){return {label:b.getAttribute('aria-label'),box:G(b),fw:cs(b).fontWeight};})
    },
    '6_sideFoot': {
      exists: !!foot,
      box: foot?G(foot):null,
      borderTop: foot?cs(foot).borderTop:null,
      padTop: foot?cs(foot).paddingTop:null,
      mt: foot?cs(foot).marginTop:null,
      rows: foot?Array.from(foot.querySelectorAll('.td-attr-row')).map(function(x){return {k:x.querySelector('.td-attr-k').textContent,v:x.querySelector('.td-attr-v').textContent,box:G(x)};}):null,
      sideBox: G(side)
    },
    '3_cards': {
      n: cards.length,
      tags: Array.from(cards).map(function(c){return c.tagName;}).join(','),
      hrefs: Array.from(cards).map(function(c){return c.getAttribute('href');}).join(','),
      bg: cards.length?cs(cards[0]).backgroundColor:null,
      cursor: cards.length?cs(cards[0]).cursor:null
    },
    '0_geometry': { left: G(r.querySelector('.td-left')), right: G(r.querySelector('.td-right')), side: G(side) }
  },null,0);
})()
" 2>&1

echo "=== 3_cards hover 实测 ==="
$AB eval "getComputedStyle(document.querySelector('.td-file')).backgroundColor" 2>&1
$AB hover ".td-file" >/dev/null 2>&1; sleep 0.5
echo "  hover 后 .td-file[0] bg = $($AB eval "getComputedStyle(document.querySelector('.td-file')).backgroundColor")"
$AB hover ".td-file--lg" >/dev/null 2>&1; sleep 0.5
echo "  hover 后 .td-file--lg[0] bg = $($AB eval "getComputedStyle(document.querySelector('.td-file--lg')).backgroundColor")"
echo "  hover 期间 .td-file[0] bg（应已复位）= $($AB eval "getComputedStyle(document.querySelector('.td-file')).backgroundColor")"

echo "=== 6 信息列底部是否在滚动容器底部 ==="
$AB eval "
(function(){
  var s=document.querySelector('.td-side'), f=document.querySelector('.td-side-foot');
  var sb=s.getBoundingClientRect(), fb=f.getBoundingClientRect();
  return JSON.stringify({sideBottom:Math.round(sb.bottom),footBottom:Math.round(fb.bottom),gapScroll:Math.round(sb.bottom-fb.bottom),scrollH:s.scrollHeight,clientH:s.clientHeight});
})()" 2>&1

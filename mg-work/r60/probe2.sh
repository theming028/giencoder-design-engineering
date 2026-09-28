#!/bin/zsh
# r60 边界压测：左栏被自动收窄后，正文列（.td-side 已隐藏）是否仍不横向溢出
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
URL="file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/task-detail.html"
EV=/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r60/ev

SNAP='(function(){var r=document.querySelector(".td-root"),L=document.querySelector(".td-left"),M=document.querySelector(".td-main"),S=document.querySelector(".td-side"),B=document.querySelector(".td-right"),P=document.querySelector(".td-browse-slot");function w(e){return e?Math.round(e.getBoundingClientRect().width):-1}var sd=S?getComputedStyle(S).display:"-";var bad=0;if(M)Array.prototype.forEach.call(M.querySelectorAll("*"),function(e){if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflowX!=="visible")bad++});return "viewport->left="+w(L)+" sideDisplay="+sd+" main="+w(M)+" mainClientW="+M.clientWidth+" overflowX="+(M.scrollWidth>M.clientWidth+1)+" 内层溢出节点数="+bad+" right="+w(B)+" browse="+w(P)})()'

$AB open "$URL" > /dev/null

for W in 1650 1700 1920 2560; do
  echo ""
  echo "=========== viewport ${W} ==========="
  $AB set viewport $W 1080 > /dev/null
  sleep 0.3
  $AB eval '(function(){var r=document.querySelector(".td-root");if(!r.classList.contains("is-browse")){document.querySelector("[data-td-browse-toggle]").click();return "opened"}return "already"})()' > /dev/null
  sleep 0.5
  echo "  浏览态: $($AB eval "$SNAP")"
  $AB eval '(function(){var r=document.querySelector(".td-root");if(r.classList.contains("is-browse")){document.querySelector("[data-td-browse-toggle]").click()}return "closed"})()' > /dev/null
  sleep 0.6
  echo "  普通态: $($AB eval "$SNAP")"
done

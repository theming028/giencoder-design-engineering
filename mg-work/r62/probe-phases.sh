#!/bin/zsh
# r62 确定性相位取证：用 Web Animations API 直接给动画设定 currentTime 并暂停
#   · animation-delay 只能定「相对」相位（绝对相位还叠了动画已运行的时长，不可复现）
#   · getAnimations()[0].currentTime = T 才能钉死绝对相位：同一 T 永远同一张图
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r62/ev
mkdir -p "$EV"

$AB open "file:///Users/shaoyuming/Documents/GienCoderDesignEngineering/pages/kanban.html" > /dev/null
$AB set viewport 1440 900 > /dev/null
sleep 1.0

# 6 个绝对相位（周期 2s）：0 / 350 / 700 / 1050 / 1400 / 1750 ms
i=0
for T in 0 350 700 1050 1400 1750; do
  i=$((i+1))
  INFO=$($AB eval "(function(){
    var c=document.querySelector('.kb-card:has(.kb-running)');
    var t=c.querySelector('.kb-card-title');
    var a=t.getAnimations()[0];
    a.pause();
    a.currentTime = ${T};
    return a.currentTime + 'ms | ' + getComputedStyle(t).backgroundPosition.split(',')[0].trim();
  })()" | tail -1 | tr -d '"')
  $AB screenshot "$EV/4$i-ph$(printf '%02d' $i)-1440.png" > /dev/null
  echo "  ph$i  currentTime=$INFO"
done

# 复位：恢复播放，避免污染后续任何取证
$AB eval '(function(){var t=document.querySelector(".kb-card:has(.kb-running) .kb-card-title");var a=t.getAnimations()[0];a.play();return "restored currentTime="+a.currentTime})()' > /dev/null
echo "已存 6 张确定性相位截图"

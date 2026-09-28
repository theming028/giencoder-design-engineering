#!/bin/zsh
# r63 确定性相位取证（同 r62 口径）：Web Animations API 钉死绝对相位再抓帧。
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
EV=/Users/shaoyuming/Documents/GienCoderDesignEngineering/mg-work/r63/ev
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
    return a.currentTime + 'ms | bp=' + getComputedStyle(t).backgroundPosition.split(',')[0].trim();
  })()" | tail -1 | tr -d '"')
  $AB screenshot "$EV/4$i-ph$(printf '%02d' $i)-1440.png" > /dev/null
  echo "  ph$i  $INFO"
done

# 复位
$AB eval '(function(){var t=document.querySelector(".kb-card:has(.kb-running) .kb-card-title");var a=t.getAnimations()[0];a.play();return "restored"})()' > /dev/null
echo "已存 6 张确定性相位截图 -> $EV"

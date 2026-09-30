#!/usr/bin/env bash
# r101 第②批 · Run C：骨架屏（临时把退场延时改成 60s 后取证）
set -u
cd /e/GienCoder/giencoder-design-engineering
NODE="C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2-3/node.exe"
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/agent-browser/bin/agent-browser.js"
TS=$(date +%s)
"$NODE" "$AB" close --all >/dev/null 2>&1
"$NODE" "$AB" set viewport 1440 900 >/dev/null 2>&1
"$NODE" "$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/conversation.html?v=$TS" >/dev/null 2>&1
"$NODE" "$AB" wait 1400 >/dev/null 2>&1
echo "=== 骨架屏读数 ==="
"$NODE" "$AB" eval "(function(){var H=document.querySelector('.r93-conv-host');var sk=H.querySelector('.r93-sk');if(!sk)return 'no sk';var R=function(e){if(!e)return null;var b=e.getBoundingClientRect();return [Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)];};var card=sk.querySelector('.r93-sk-card');var cs=card?getComputedStyle(card):null;s=sk.querySelector('.r93-sk-in');return JSON.stringify({sk:R(sk),z:getComputedStyle(sk).zIndex,bg:getComputedStyle(sk).backgroundColor,skIn:R(s),padTop:getComputedStyle(s).paddingTop,firstKid:R(s.firstElementChild),lines:sk.querySelectorAll('.giencoder-skeleton-line').length,titles:sk.querySelectorAll('.giencoder-skeleton-title').length,avs:sk.querySelectorAll('.giencoder-skeleton-avatar').length,card:R(card),cardBg:cs?cs.backgroundColor:null,cardBgImg:cs?cs.backgroundImage.slice(0,30):null,cardPad:cs?cs.padding:null,cardRadius:cs?cs.borderRadius:null,cardShadow:cs?cs.boxShadow:null,cardKids:card?[].map.call(card.children,function(k){return R(k).join(',');}):null,body3:R(sk.querySelectorAll('.r93-sk-body > .giencoder-skeleton-line')[0]),firstReal:R(H.querySelector('.r93-wrap > *'))});})()"
"$NODE" "$AB" screenshot "" "mg-work/r101/raw/r101-sk2.png" >/dev/null 2>&1
echo "   （已截 r101-sk2.png）"

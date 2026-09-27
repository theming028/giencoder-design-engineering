#!/usr/bin/env bash
set -u
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
P="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
BASE="http://127.0.0.1:8866/pages"; OUT="mg-work/r34/cmp2.jsonl"; : > "$OUT"
EXP='JSON.stringify((function(){var Q=function(s){return document.querySelector(s)},R=function(e){if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]},CS=function(e,p){return e?getComputedStyle(e)[p]:null};var t=Q(".td-composer textarea"),tb=Q(".td-composer .mt-auto");return{rightPanel:R(Q(".td-right")),card:R(Q(".td-composer > div")),ta:R(t),taMinH:CS(t,"minHeight"),toolbar:R(tb),sw:tb?tb.scrollWidth:null,cw:tb?tb.clientWidth:null,avatar:R(Q(".td-composer [aria-label=\"数字分身\"]")),bar:R(Q(".td-right-bar"))};})())'
$AB open "$BASE/task-detail.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.0
echo -n "DETAIL: "; D=$($AB eval "$EXP" 2>&1 | tail -1); echo "$D"; echo "{\"step\":\"detail\",\"data\":$D}" >> mg-work/r34/cmp2.jsonl
$AB open "$BASE/avatar.html" >/dev/null 2>&1
$AB set viewport 1440 900 >/dev/null 2>&1
sleep 4.5
$AB click ".av-chat-trigger" >/dev/null 2>&1
sleep 0.8
echo -n "AVATAR: "; A=$($AB eval "$EXP" 2>&1 | tail -1); echo "$A"; echo "{\"step\":\"avatar\",\"data\":$A}" >> mg-work/r34/cmp2.jsonl

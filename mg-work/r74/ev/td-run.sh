#!/bin/zsh
AB=/Users/shaoyuming/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser
D=/Users/shaoyuming/Documents/GienCoderDesignEngineering
$AB open "file://$D/pages/task-detail.html" >/dev/null 2>&1
$AB set viewport 1920 1080 >/dev/null 2>&1
sleep 2.5
$AB eval --stdin < "$D/mg-work/r74/ev/td-sample.js"

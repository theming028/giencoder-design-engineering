#!/usr/bin/env bash
# Round 20 实测：5 项调整
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
OUT="mg-work/r20"
mkdir -p "$OUT"

"$AB" set viewport 1440 900 >/dev/null 2>&1
"$AB" open "$URL" >/dev/null 2>&1
sleep 2

echo "############ 5. 创建任务卡 hover ############"
echo -n "默认: "
"$AB" eval "(function(){var e=document.querySelector('.kb-create');var c=getComputedStyle(e);return 'bg='+c.backgroundColor+' border='+c.borderTopColor+' shadow='+c.boxShadow;})()"
"$AB" hover ".kb-create" >/dev/null 2>&1
sleep 1
echo -n "hover: "
"$AB" eval "(function(){var e=document.querySelector('.kb-create');var c=getComputedStyle(e);return 'bg='+c.backgroundColor+' border='+c.borderTopColor+' shadow='+c.boxShadow;})()"
"$AB" screenshot "" "$OUT/hover-create.png" >/dev/null 2>&1
echo

echo "############ 打开创建任务弹窗 ############"
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 2

echo "############ 4. 编辑器容器边框色 ############"
"$AB" eval "(function(){var e=document.querySelector('.kb-crt-editor');var c=getComputedStyle(e);return 'borderTop='+c.borderTopColor+' width='+c.borderTopWidth;})()"

echo "############ 2. 上传中卡：标题与进度条间距 ############"
"$AB" eval "(function(){
  var info=document.querySelector('.kb-crt-uplist .kb-crt-upinfo');
  var nm=info.querySelector('.kb-crt-upname'); var pr=info.querySelector('.kb-crt-upprog');
  var a=nm.getBoundingClientRect(), b=pr.getBoundingClientRect();
  return 'gap='+getComputedStyle(info).gap+' 实测序号间距='+(b.top-a.bottom).toFixed(2)+'px  (标题底 '+a.bottom.toFixed(1)+' -> 进度条顶 '+b.top.toFixed(1)+')';
})()"

echo "############ 3. 附件卡 hover ############"
echo -n "默认: "
"$AB" eval "(function(){var e=document.querySelector('.kb-crt-uplist .kb-crt-upitem');return getComputedStyle(e).backgroundColor;})()"
"$AB" hover ".kb-crt-uplist .kb-crt-upitem" >/dev/null 2>&1
sleep 1
echo -n "hover: "
"$AB" eval "(function(){var e=document.querySelector('.kb-crt-uplist .kb-crt-upitem');return getComputedStyle(e).backgroundColor;})()"
echo

echo "############ 1. 弹窗边缘（截图供像素分析） ############"
"$AB" eval "(function(){var d=document.querySelector('.kb-crt-dialog');var b=d.getBoundingClientRect();return JSON.stringify({left:b.left,top:b.top,right:b.right,bottom:b.bottom});})()"
"$AB" screenshot "" "$OUT/r20-1440.png" >/dev/null 2>&1
echo DONE

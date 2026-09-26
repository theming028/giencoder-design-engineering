#!/usr/bin/env bash
# Round 15 / item 2 —— 设计稿画布尺寸（1440x900）下的高保真实测 + 上传区复测
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
OUT="mg-work/r15"
mkdir -p "$OUT"

echo "=== 0. 设置视口 1440x900（设计稿画布）==="
"$AB" set viewport 1440 900 >/dev/null 2>&1
"$AB" open "$URL" >/dev/null 2>&1
sleep 2
"$AB" eval "(function(){return JSON.stringify({vw:innerWidth,vh:innerHeight});})()"

echo
echo "=== A. 弹窗与设计稿尺寸逐项比对（设计稿：面板 1280x820）==="
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){
  var R=function(s){var e=document.querySelector(s);if(!e)return null;var r=e.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height)];};
  var d=document.querySelector('.kb-crt-dialog'),dr=d.getBoundingClientRect();
  var rowTops=[];
  document.querySelectorAll('.kb-crt-aside-body .kb-crt-row').forEach(function(e){rowTops.push(Math.round(e.getBoundingClientRect().top-dr.top));});
  var lhs=document.querySelector('.kb-crt-type').getBoundingClientRect();
  var ths=document.querySelector('.kb-crt-title').getBoundingClientRect();
  var ehs=document.querySelector('.kb-crt-editor').getBoundingClientRect();
  var ahs=document.querySelector('.kb-crt-attach').getBoundingClientRect();
  return JSON.stringify({
    dialog:R('.kb-crt-dialog'),
    head:R('.kb-crt-head'),
    type:R('.kb-crt-type .giencoder-select-view'),
    title:R('.kb-crt-title'),
    editor:R('.kb-crt-editor'),
    toolbar:R('.kb-crt-toolbar'),
    upbtn:R('.kb-crt-upbtn'),
    aside:R('.kb-crt-aside'),
    asideHead:R('.kb-crt-aside-head'),
    fld:R('.kb-crt-fld'),
    foot:R('.kb-crt-foot'),
    off_type:Math.round(lhs.top-dr.top),
    off_title:Math.round(ths.top-dr.top),
    off_editor:Math.round(ehs.top-dr.top),
    off_attach:Math.round(ahs.top-dr.top),
    rowTops:rowTops
  });})()"
"$AB" screenshot "" "$OUT/crt-1440.png" >/dev/null 2>&1

echo
echo "=== B. 错误提示条位置（设计稿：顶距面板顶约 16）==="
"$AB" eval "(function(){document.querySelector('[data-crt-submit]').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var d=document.querySelector('.kb-crt-dialog').getBoundingClientRect();var m=document.querySelector('.kb-crt-msgs').getBoundingClientRect();var c=document.querySelector('.kb-crt-msg').getBoundingClientRect();return JSON.stringify({msgsTop:Math.round(m.top-d.top),msgsH:Math.round(m.height),msgH:Math.round(c.height),msgW:Math.round(c.width),shown:document.querySelectorAll('.kb-crt-msgs .giencoder-message:not([hidden])').length});})()"
"$AB" screenshot "" "$OUT/crt-1440-error.png" >/dev/null 2>&1

echo
echo "=== C. 上传文件列表（删除按钮应为 SVG 图标）==="
"$AB" eval "(function(){var d=document.querySelector('.kb-crt-mask');d.click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
sleep 1
"$AB" eval "(function(){var inp=document.querySelector('.kb-crt-file');var f1=new File(['a'],'需求文档.md',{type:'text/markdown'});var f2=new File(['b'],'接口定义.yaml',{type:'text/yaml'});var dt=new DataTransfer();dt.items.add(f1);dt.items.add(f2);inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));var it=document.querySelectorAll('.kb-crt-upitem');var nm=[];it.forEach(function(e){var n=e.querySelector('.kb-crt-upname');nm.push(n?n.textContent:null);});var svg=document.querySelector('.kb-crt-uprm svg');var rm=document.querySelector('.kb-crt-uprm');return JSON.stringify({count:it.length,names:nm,itemH:Math.round(it[0].getBoundingClientRect().height),rmHasSvg:!!svg,rmText:rm.textContent,rmBox:[Math.round(rm.getBoundingClientRect().width),Math.round(rm.getBoundingClientRect().height)]});})()"
"$AB" screenshot "" "$OUT/crt-1440-upload.png" >/dev/null 2>&1
echo DONE

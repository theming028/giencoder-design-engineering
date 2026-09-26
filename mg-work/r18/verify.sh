#!/usr/bin/env bash
# Round 18 实测：标题/编辑器宽度自适应 + main:aside = 8:2
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
OUT="mg-work/r18"
mkdir -p "$OUT"

probe() {
  "$AB" eval "(function(){
    var q=function(s){var e=document.querySelector(s);if(!e)return null;var r=e.getBoundingClientRect();return {w:Math.round(r.width),left:Math.round(r.left)};};
    var m=q('.kb-crt-main'),a=q('.kb-crt-aside'),t=q('.kb-crt-title'),e=q('.kb-crt-editor');
    var body=q('.kb-crt-body');
    var ratio = (m&&a)? (m.w/a.w).toFixed(3) : null;
    var pct = (m&&a)? [Math.round(m.w/(m.w+a.w)*1000)/10, Math.round(a.w/(m.w+a.w)*1000)/10] : null;
    var f=q('.kb-crt-fld'), dt=q('.kb-crt-date');
    var ov=[];document.querySelectorAll('.kb-crt-aside-body .giencoder-select-view, .kb-crt-aside-body .giencoder-input-wrapper').forEach(function(el){
      if(el.scrollWidth>el.clientWidth+1) ov.push(el.className.split(' ')[0]+':'+el.scrollWidth+'>'+el.clientWidth);
    });
    return JSON.stringify({dialog:q('.kb-crt-dialog'),body:body,main:m,aside:a,title:t,editor:e,
      mainToAside:ratio, pct: pct, fldW: f?f.w:null, dateW: dt?dt.w:null,
      titleEqMainContent: (m&&t)? (t.w === m.w-80) : null,
      overflow: ov});
  })()"
}

for VP in "1440 900" "1920 1080"; do
  W=$(echo $VP | cut -d' ' -f1); H=$(echo $VP | cut -d' ' -f2)
  echo "############ 视口 ${W}x${H} ############"
  "$AB" set viewport $W $H >/dev/null 2>&1
  "$AB" open "$URL" >/dev/null 2>&1
  sleep 2
  "$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
  sleep 1
  probe
  "$AB" screenshot "" "$OUT/crt-${W}.png" >/dev/null 2>&1
  echo
done
echo DONE

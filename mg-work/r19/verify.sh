#!/usr/bin/env bash
# Round 19 实测：5 项调整
AB="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules/.bin/agent-browser"
URL="http://127.0.0.1:8866/pages/kanban.html"
OUT="mg-work/r19"
mkdir -p "$OUT"

echo "############ 1. 五张统计卡宽度 ############"
"$AB" set viewport 1440 900 >/dev/null 2>&1
"$AB" open "$URL" >/dev/null 2>&1
sleep 2
"$AB" eval "(function(){
  var out=[];
  document.querySelectorAll('.kb-stats > *').forEach(function(el){
    var b=el.getBoundingClientRect();
    var lbl=el.querySelector('.kb-stat-label');
    var nm=el.classList.contains('kb-create')?'创建任务':(lbl?lbl.textContent.trim():el.className);
    out.push(nm+' = '+b.width.toFixed(2));
  });
  return out.join(' | ');
})()"
echo

echo "############ 2-5. 弹窗内（1440 / 1920） ############"
for VP in "1440 900" "1920 1080"; do
  W=$(echo $VP | cut -d' ' -f1); H=$(echo $VP | cut -d' ' -f2)
  echo "---- 视口 ${W}x${H} ----"
  "$AB" set viewport $W $H >/dev/null 2>&1
  "$AB" open "$URL" >/dev/null 2>&1
  sleep 2
  "$AB" eval "(function(){document.querySelector('.kb-create').click();return 1;})()" >/dev/null 2>&1
  sleep 1
  # 触发校验 -> 显示 message
  "$AB" eval "(function(){var b=document.querySelector('[data-crt-submit]');if(b)b.click();return 1;})()" >/dev/null 2>&1
  sleep 1
  "$AB" eval "(function(){
    var r=function(e){if(!e)return null;var b=e.getBoundingClientRect();return {w:Math.round(b.width*100)/100,h:Math.round(b.height*100)/100,x:Math.round(b.left),y:Math.round(b.top)};};
    var m=r(document.querySelector('.kb-crt-main')), a=r(document.querySelector('.kb-crt-aside'));
    var pct=(m&&a)?[Math.round(m.w/(m.w+a.w)*1000)/10,Math.round(a.w/(m.w+a.w)*1000)/10]:null;
    /* 六字段可视框 */
    var flds=[];
    document.querySelectorAll('.kb-crt-aside-body .kb-crt-row').forEach(function(row){
      var lbl=row.querySelector('.kb-crt-lbl');
      var vis=row.querySelector('.giencoder-select-view')||row.querySelector('.giencoder-input-wrapper');
      if(!vis)return;
      var cs=getComputedStyle(vis);
      flds.push((lbl?lbl.textContent.trim():'?')+':'+r(vis).w+'/minW='+cs.minWidth);
    });
    /* message */
    var msg=document.querySelector('.kb-crt-msgs .giencoder-message');
    var msgInfo=null,cls=null;
    if(msg){var cs=getComputedStyle(msg);msgInfo={w:r(msg).w,h:r(msg).h,pad:cs.paddingTop+' '+cs.paddingRight,radius:cs.borderRadius,bg:cs.backgroundColor};}
    cls=msg?msg.className:null;
    var iconColor=msg&&msg.querySelector('.giencoder-message-icon')?getComputedStyle(msg.querySelector('.giencoder-message-icon')).color:null;
    var contentCls=msg&&msg.querySelector('.giencoder-message-content')?msg.querySelector('.giencoder-message-content').className:null;
    /* 附件卡 */
    var ups=[];
    document.querySelectorAll('.kb-crt-uplist .kb-crt-upitem').forEach(function(el){
      var cs=getComputedStyle(el);
      var hasProg=!!el.querySelector('.kb-crt-upprog');
      var meta=el.querySelector('.kb-crt-upmeta');
      var file=el.querySelector('.kb-crt-upfile');
      ups.push({w:r(el).w,h:r(el).h,bg:cs.backgroundColor,radius:cs.borderRadius,file:file?r(file).w:'-',state:hasProg?'上传中':(meta?meta.textContent:'-')});
    });
    var list=document.querySelector('.kb-crt-uplist');
    return JSON.stringify({main:m,aside:a,pct:pct,fields:flds,
      msgCls:cls,msg:msgInfo,msgIconColor:iconColor,msgContentCls:contentCls,
      ups:ups, upListW:list?r(list).w:null},null,1);
  })()"
  "$AB" screenshot "" "$OUT/r19-${W}.png" >/dev/null 2>&1
  echo
done
echo DONE

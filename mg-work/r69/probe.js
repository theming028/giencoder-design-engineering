(()=>{
const Q=s=>document.querySelector(s);
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();return[Math.round(r.width),Math.round(r.height)]};
const S=(e,p)=>e?getComputedStyle(e,p):null;
const PW=e=>e?S(e,'::before').width:null;
const PH=e=>e?S(e,'::before').height:null;
const SW=e=>{if(!e)return null;const g=e.querySelector('svg');return g?R(g):null};
const pane=Q('.td-browse');
if(!pane)return 'no pane';
const P=pane.getBoundingClientRect();
const L=e=>e?Math.round(e.getBoundingClientRect().left-P.left):null;
const bar=Q('.td-browse-bar'),tab=Q('.td-browse-tab'),add=Q('.td-browse-add'),ico=Q('.td-browse-ico'),sep=Q('.td-browse-sep');
const body=Q('.td-browse-body'),tree=Q('.td-browse-tree'),tt=Q('.td-browse-tree-title'),srch=Q('.td-browse-search'),files=Q('.td-browse-files');
const rows=files?[...files.querySelectorAll('.td-bf')]:[];
const r0=rows[0]||null,r1=rows[1]||null;
const chev=r0?r0.querySelector('.td-bf-arrow'):null,ico0=r0?r0.querySelector('.td-bf-ico'):null,nm0=r0?r0.querySelector('.td-bf-name'):null,guide=r0?r0.querySelector('.td-bf-guide'):null;
const act=Q('.td-bf.is-active')||rows.find(r=>r.classList.contains('is-file'))||null;
const code=Q('.td-browse-code'),crumb=Q('.td-browse-crumb'),cp=Q('.td-browse-crumb-path'),pre=Q('.td-browse-pre');
const c0=Q('.td-code'),no0=Q('.td-code-no'),k=Q('.td-code-k'),s0=Q('.td-code-s'),n0=Q('.td-code-n');
const csp=S(pane);
return JSON.stringify({
 panel:{"w":Math.round(P.width),"h":Math.round(P.height),"bg":csp.backgroundColor,"border":csp.borderTopWidth+" "+csp.borderTopColor,"radius":csp.borderRadius},
 bar:{"size":R(bar),"pad":S(bar)&&S(bar).padding,"gap":S(bar)&&S(bar).gap,"bg":S(bar)&&S(bar).backgroundColor,"borderB":S(bar)?(S(bar).borderBottomWidth+" "+S(bar).borderBottomColor):null},
 tab:{"size":R(tab),"font":S(tab)?(S(tab).fontSize+"/"+S(tab).fontWeight):null,"color":S(tab)&&S(tab).color,"gap":S(tab)&&S(tab).gap,"svg":SW(tab)},
 add:{"size":R(add),"svg":SW(add),"radius":S(add)&&S(add).borderRadius},
 closeIco:{"size":R(ico),"svg":SW(ico)},
 sep:{"size":R(sep),"bg":S(sep)&&S(sep).backgroundColor},
 body:{"pad":S(body)&&S(body).padding,"gap":S(body)&&S(body).gap},
 tree:{"w":tree?Math.round(tree.getBoundingClientRect().width):null,"pad":S(tree)&&S(tree).padding,"borderR":S(tree)?(S(tree).borderRightWidth+" "+S(tree).borderRightColor):null,"gap":S(tree)&&S(tree).gap},
 treeTitle:{"font":S(tt)?(S(tt).fontSize+"/"+S(tt).fontWeight):null,"color":S(tt)&&S(tt).color,"mb":S(tt)&&S(tt).marginBottom,"h":tt?Math.round(tt.getBoundingClientRect().height):null},
 search:{"size":R(srch),"border":S(srch)?(S(srch).borderTopWidth+" "+S(srch).borderTopColor):null,"radius":S(srch)&&S(srch).borderRadius,"bg":S(srch)&&S(srch).backgroundColor,"ph":srch&&srch.querySelector('input')?srch.querySelector('input').placeholder:null},
 files:{"w":files?Math.round(files.getBoundingClientRect().width):null,"pad":S(files)&&S(files).padding,"gap":S(files)&&S(files).gap},
 row:{"size":R(r0),"pad":S(r0)&&S(r0).paddingLeft,"radius":S(r0)&&S(r0).borderRadius,"font":S(nm0)&&S(nm0).fontSize,"color":S(nm0)&&S(nm0).color,"lineH":S(r0)&&S(r0).lineHeight,"indent":L(nm0)},
 chevron:{"box":R(chev),"left":L(chev),"before":PW(chev)+" x "+PH(chev),"svg":SW(chev)},
 ico0:{"box":R(ico0),"left":L(ico0),"before":PW(ico0)+" x "+PH(ico0),"svg":SW(ico0)},
 guide:{"before":guide?(PW(guide)+" x "+PH(guide)):null,"bg":guide?S(guide,'::before').backgroundColor:null,"left":L(guide)},
 active:{"bg":act?S(act,'::before').backgroundColor:null,"radius":act?S(act,'::before').borderRadius:null,"border":act?(S(act,'::before').borderTopWidth+" "+S(act,'::before').borderTopColor):null,"cls":act?act.className:null},
 code:{"w":code?Math.round(code.getBoundingClientRect().width):null,"pad":S(code)&&S(code).padding},
 crumb:{"size":R(crumb),"pad":S(crumb)&&S(crumb).padding,"font":S(crumb)&&S(crumb).fontSize,"color":S(crumb)&&S(crumb).color,"borderB":S(crumb)?(S(crumb).borderBottomWidth+" "+S(crumb).borderBottomColor):null,"pathColor":S(cp)&&S(cp).color},
 pre:{"pad":S(pre)&&S(pre).padding,"font":S(pre)&&S(pre).fontFamily.slice(0,24),"fontSize":S(pre)&&S(pre).fontSize,"lineH":S(pre)&&S(pre).lineHeight},
 cline:{"h":c0?Math.round(c0.getBoundingClientRect().height):null,"pad":S(c0)&&S(c0).padding,"gap":S(c0)&&S(c0).gap},
 cno:{"w":no0?Math.round(no0.getBoundingClientRect().width):null,"color":S(no0)&&S(no0).color},
 syn:{"k":S(k)&&S(k).color,"s":S(s0)&&S(s0).color,"n":S(n0)&&S(n0).color},
 nRows:rows.length,nCode:document.querySelectorAll('.td-code').length,
 nFiles:document.querySelectorAll('.td-file').length
})})()

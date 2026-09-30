JSON.stringify((function(){
  var tr=document.querySelector('.ws-dropdown-hover:has(.lucide-lock)');
  if(!tr) return {err:'no perm trigger'};
  var txt=tr.querySelector('.giencoder-select-view-text');
  var ico=tr.querySelector('svg');
  return {
    text:txt?txt.textContent:null,
    textCol:txt?getComputedStyle(txt).color:null,
    textInline:txt?txt.getAttribute('style'):null,
    icoCol:ico?getComputedStyle(ico).color:null,
    icoCls:ico?ico.getAttribute('class'):null,
    expanded:tr.getAttribute('aria-expanded'),
    menuOpen:!!document.querySelector('[role="listbox"][aria-label="权限选择"]'),
    /* 顺带把「工作目录」那一支也读出来，作为「没有误伤」的反证 */
    workdirTextCol:(function(){var w=document.querySelectorAll('.ws-dropdown-hover')[0];var t=w?w.querySelector('.giencoder-select-view-text'):null;return t?getComputedStyle(t).color:null;})()
  };
})())

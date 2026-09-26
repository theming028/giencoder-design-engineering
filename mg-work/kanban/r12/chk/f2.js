
(function(){
  var SKILL_DATA=[
    {n:"systematic-debugging",d:"一个用于调试软件问题的结构化方法，强制要求在提出修复方案前进行根本原因分析。",t:"预置"},
    {n:"writing-skills",d:"将测试驱动开发方法应用于Claude技能文档创建。",t:"预置"},
    {n:"create-ex",d:"Distill an ex-partner into an AI Skill. Import WeChat history, photos, social media posts, generate...",t:"预置"},
    {n:"nuwa-skill",d:"女娲（Nuwa）：输入任何人的名字，自动调研 → 提取思维框架 → 生成可运行的视角技能。",t:"自有"},
    {n:"subagent-driven-development",d:"将实施计划分解为独立任务的工作流，每个任务由新的AI子代理处理，并经过规...",t:"自有"}
  ];
  var SKILL_ICON="M24.186728,2.622206C25.384614,4.213191,25.259206,6.484126,23.810502,7.932686C22.690121,9.053067,21.078116,9.381961,19.669023,8.919509L15.722592,12.86594C15.543845,13.044685,15.254133,13.044685,15.075387,12.86594L13.13406,10.924469C12.955313,10.745724,12.955313,10.456011,13.13406,10.277266L17.080348,6.330977C16.617896,4.921884,16.946789,3.309879,18.067171,2.189497C19.515873,0.740794,21.786666,0.615386,23.37765,1.813272L20.957998,4.233068L21.766933,5.042002L24.186728,2.622206ZM23.86384,4.517631L23.85812,4.487745L22.090392,6.255331C21.911646,6.434078,21.621934,6.434078,21.443188,6.255331L19.744525,4.55667C19.565779,4.377923,19.565779,4.088211,19.744525,3.909465L21.512254,2.141736L21.482368,2.136016C20.561468,1.966136,19.579794,2.235113,18.867382,2.926647L18.835637,2.957963C18.041717,3.751882,17.770881,4.909586,18.102777,5.960186L18.113072,5.991931L18.321419,6.626838L14.347389,10.600867L15.398989,11.652467L19.373019,7.67858L20.007926,7.886927C21.066962,8.234553,22.239965,7.966291,23.042036,7.16422C23.756736,6.449521,24.036295,5.452117,23.86384,4.517631Z";
  var GOAL_ICON="M7.260587,0.644581C6.87263,0.450718,6.416301,0.732967,6.416504,1.166665L6.416504,7.583331C6.416504,7.905497,6.677672,8.166664,6.999837,8.166664C7.322004,8.166664,7.58317,7.905498,7.583171,7.583331L7.583171,6.193247L11.927254,4.02208C12.125246,3.923402,12.250381,3.721217,12.250381,3.499997C12.250381,3.278777,12.125246,3.076592,11.927254,2.977914L7.260587,0.644581ZM7.583171,2.109914L10.362171,3.499998L7.583171,4.890081L7.583171,2.109914ZM4.860295,2.324009C4.713676,2.274406,4.553353,2.285108,4.414628,2.353759C-0.024539,4.548843,0.172045,11.034927,4.735462,12.958759C9.298296,14.882011,14.076962,10.493592,12.548628,5.783759C12.449556,5.476926,12.120346,5.308662,11.813628,5.408093C11.507028,5.507411,11.339064,5.836544,11.438544,6.143093C12.685128,9.984926,8.908628,13.451676,5.187544,11.883093C1.465877,10.31451,1.311877,5.189926,4.932044,3.399676C5.220919,3.256842,5.339245,2.906827,5.196294,2.618009C5.127712,2.47933,5.00685,2.373575,4.860295,2.324009ZM4.20155,5.480991C4.294503,5.357728,4.43253,5.276338,4.585384,5.254659C4.738845,5.232536,4.894799,5.272417,5.0188,5.365493C5.27596,5.559329,5.327399,5.924884,5.133717,6.182159C4.097611,7.5315,4.820449,9.500094,6.48355,9.858326C8.138589,10.252957,9.640309,8.788727,9.287634,7.124243C9.224664,6.808747,9.429013,6.501833,9.744383,6.438242C10.06008,6.374911,10.367386,6.579347,10.430967,6.894992C10.926217,9.361326,8.678051,11.553492,6.225134,10.996992C3.772217,10.439909,2.690717,7.492325,4.20155,5.480991Z";
  var CLOSE_ICON="M7.490717,10.487117L2.965129,10.487117L1.833361,10.487117C1.771554,10.487117,1.716368,10.469081,1.664863,10.442951C1.557415,10.455818,1.445555,10.426761,1.363147,10.344354L0.845842,9.826678C0.703079,9.683902,0.703079,9.45246,0.845842,9.309349L3.293322,6.108695C3.436086,5.965968,3.667888,5.965968,3.810652,6.108695L4.327981,6.626036C4.470708,6.769135,4.470708,7.000973,4.327981,7.143689L2.923913,8.980075L6.860016,8.980075C8.010204,8.918245,8.927127,8.004297,8.983788,6.858569L8.983788,4.08214C8.983788,3.873866,9.152273,3.705392,9.36056,3.705392L10.12214,3.705392C10.330415,3.705392,10.4989,3.873866,10.4989,4.08214L10.4989,4.475809L10.4989,7.115747L10.4989,7.496561C10.4989,9.148201,9.152274,10.487117,7.490717,10.487117Z";

  function buildSkillsPopup(){
    var overlay=document.createElement('div');
    overlay.className='skills-popup-overlay';
    overlay.id='skills-popup';

    var bg=document.createElement('div');
    bg.className='skills-popup-bg';
    overlay.appendChild(bg);

    // 头部
    var header=document.createElement('div');
    header.className='skills-popup-header';
    bg.appendChild(header);

    var closeBtn=document.createElement('span');
    closeBtn.className='skills-popup-close';
    closeBtn.innerHTML='<svg viewBox="0.7 3.71 9.8 6.78" width="12" height="12" fill="none"><path d="'+CLOSE_ICON+'" fill="#A9A9A9"/></svg>';
    closeBtn.onclick=function(){overlay.remove()};
    bg.appendChild(closeBtn);

    var goalIcon=document.createElement('span');
    goalIcon.className='skills-popup-goal-icon';
    goalIcon.innerHTML='<svg viewBox="-0.02 0.45 14.1 14.43" width="14" height="14" fill="none"><path d="'+GOAL_ICON+'" fill="#7766FD"/></svg>';
    bg.appendChild(goalIcon);

    var goalTitle=document.createElement('span');
    goalTitle.className='skills-popup-goal-title';
    goalTitle.textContent='Goal';
    bg.appendChild(goalTitle);

    var goalDesc=document.createElement('span');
    goalDesc.className='skills-popup-goal-desc';
    goalDesc.textContent='构建一个以实现目标为结果的任务，持续运行直到全部完成。';
    bg.appendChild(goalDesc);

    // 标签
    var label=document.createElement('span');
    label.className='skills-popup-label';
    label.textContent='技能 Skills';
    bg.appendChild(label);

    // 5 行技能
    for(var i=0;i<SKILL_DATA.length;i++){
      var s=SKILL_DATA[i];
      var y=84+i*34;
      var row=document.createElement('div');
      row.className='skills-popup-row skill-row';
      row.style.top=y+'px';

      var icon=document.createElement('span');
      icon.className='skills-popup-row-icon';
      icon.innerHTML='<svg viewBox="0 0 14 14" width="14" height="14" fill="none"><path d="'+SKILL_ICON+'" fill="#6B6B6B" transform="matrix(-1,0,0,1,26,0)"/></svg>';
      row.appendChild(icon);

      var tag=document.createElement('span');
      tag.className='skills-popup-row-tag';
      tag.innerHTML='<span style="font:400 var(--font-size-body-1)/20px var(--font-family);color:var(--color-text-3)">'+s.t+'</span>';
      row.appendChild(tag);

      var name=document.createElement('span');
      name.className='skills-popup-row-name';
      name.textContent=s.n;
      row.appendChild(name);

      var desc=document.createElement('span');
      desc.className='skills-popup-row-desc';
      desc.style.position='absolute';
      desc.style.left=(34+s.n.length*7.5+12)+'px';
      desc.style.top='5px';
      desc.textContent=s.d;
      row.appendChild(desc);

      bg.appendChild(row);
    }

    // 分隔线
    var div=document.createElement('div');
    div.className='skills-popup-divider';
    bg.appendChild(div);

    // 按钮
    var btns=document.createElement('div');
    btns.className='skills-popup-buttons';
    var btn1=document.createElement('button');
    btn1.className='skills-popup-btn';
    btn1.textContent='安装技能';btn1.onclick=function(){window.location.href='skills.html'};
    btns.appendChild(btn1);
    var btn2=document.createElement('button');
    btn2.className='skills-popup-btn';
    btn2.textContent='管理技能';
    btns.appendChild(btn2);
    bg.appendChild(btns);

    document.body.appendChild(overlay);
  }

  // 监听 "@" 输入触发弹窗
  var observer=new MutationObserver(function(){
    // 检查是否有输入框内容包含 @
  });
  observer.observe(document.body,{childList:true,subtree:true});

  // 暴露到全局，方便测试
  window.__showSkillsPopup=buildSkillsPopup;
})();

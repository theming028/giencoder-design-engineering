/* ================================================================================
   ★ 第 69 轮：文件预览栏（.td-browse）—— 从「研发工作台 › 任务详情页」全要素移植
   三件套：① 同源 HTML（#av-browse-slot，含顶栏 / 文件目录树 / 代码预览 / 两条分栏条）
           ② 同源 CSS（#av-browse-css）
           ③ 同源 JS：右键菜单 bindBrowseContextMenu（逐字移植）+ 本控制器（按本页布局改写）
   与详情页的布局差异（决定了控制器为何要重写，而非照搬）：
     · 数字分身没有 .td-root 三栏；AI 会话栏是本页自己的 .av-chat-drawer（宽度走 --av-chat-w），
       预览栏插在它右侧，成为 shell flex 行（div:has(> main)）的最后一个子项；
     · 「让位对象」不是详情页的 .td-left，而是 shell 自己的「左导航 aside」（React 内联宽 256px）
       → 用 .av-browse-on 收宽度（200ms，沿用外壳自带 transition-all）；
     · 预览栏宽度走**本页独立变量** --av-browse-w（默认 641 = 树 240 + 分栏条 1 + 代码 400），
       不与详情页的 --td-browse-right-w 混用，避免布局记忆串味。
   本脚本必须插在 #av-chat-js **之前**：Esc 裁决靠注册顺序，预览栏要能先吃掉这一层。
   ================================================================================ */

/* ---------- 轻提示：DS Message（与详情页 tdToast 同构造，元素名沿用 .td-dp-msg） ---------- */
var AV_MSG_SVG = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true">' +
  '<circle cx="7" cy="7" r="6.2" fill="currentColor"/>' +
  '<path d="M4.3 7.2l1.9 1.9 3.5-3.7" stroke="var(--color-white)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

function avToast(text) {
  var box = document.querySelector('.td-dp-msg');
  if (!box) {
    box = document.createElement('div');
    box.className = 'td-dp-msg';
    box.innerHTML = '<div class="giencoder-message" role="status">' +
      '<span class="giencoder-message-icon" aria-hidden="true">' + AV_MSG_SVG + '</span>' +
      '<span class="giencoder-message-content"></span></div>';
    box.hidden = true;
    document.body.appendChild(box);
  }
  box.querySelector('.giencoder-message-content').textContent = text;
  box.hidden = false;
  clearTimeout(box._t);
  box._t = setTimeout(function () { box.hidden = true; }, 2400);
}

/* 右键菜单段用它判断「浏览态是否打开」—— 直接查类名，与该段原来的 .td-root.is-browse 等价 */
function avBrowseOpen() { return !!document.querySelector('.av-browse-on'); }

  function bindBrowseContextMenu() {
    var root = document.querySelector('.td-browse-slot');
    if (!root || root.getAttribute('data-td-ctx-bound') === '1') return;
    root.setAttribute('data-td-ctx-bound', '1');

    var ICON = {
      file: '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15.6 3.2H5.6a2 2 0 0 0-2 2v13.6a2 2 0 0 0 2 2h12.8a2 2 0 0 0 2-2V8.4z"/><path d="M8.6 10.8h7.6"/><path d="M8.6 14.6h4.2"/></svg>',
      folder: '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.1 3.8H9.2a1.6 1.6 0 0 1 1.6 1.6v0.8h8.5a1.6 1.6 0 0 1 1.6 1.6v11.5a1.6 1.6 0 0 1-1.6 1.6H4.1a1.6 1.6 0 0 1-1.6-1.6V5.4a1.6 1.6 0 0 1 1.6-1.6Z"/><path d="M2.5 11.3h18.9"/></svg>',
      message: '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 21.2V12.2A8.2 8.2 0 0 1 12.2 4h1.6a8.2 8.2 0 0 1 8.2 8.2v0.8a8.2 8.2 0 0 1-8.2 8.2z"/><path d="M8 11.5h8"/><path d="M8 15.3h4"/></svg>',
      brand: '<svg viewBox="0 0 14 14" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M11.812715011920929,3.386497311920929C12.044085011920929,3.083182911920929,11.834289011920928,2.749894211920929,11.62450701192093,2.5089274119209293C11.393401011920929,2.255956011920929,11.136255011920928,2.028110011920929,10.85729401192093,1.8291742119209289C8.180274311920929,-0.1715373980790711,4.41684251192093,0.21306953192092898,2.199793511920929,2.713929711920929C2.771062911920929,2.294303211920929,3.431602511920929,2.012423011920929,4.129799211920929,1.890314411920929C5.220866011920929,1.7100947119209289,6.340480111920929,1.922474711920929,7.289765611920929,2.4897480119209288C7.596643311920929,2.673177311920929,7.867575511920929,2.905751311920929,8.174451211920928,3.089180311920929C8.80152211192093,3.4599131119209288,9.506140511920929,3.679879211920929,10.23273541192093,3.731761511920929C10.61182001192093,3.770784711920929,10.994809011920928,3.743202311920929,11.36437201192093,3.650245711920929C11.537337011920929,3.610378311920929,11.69384801192093,3.518305811920929,11.812715011920929,3.386497311920929ZM13.204496011920929,5.964040111920929C13.308039011920929,6.203388011920929,13.37786801192093,6.455964911920929,13.41178301192093,6.714521711920929C13.436837011920929,6.9236405119209286,13.436033011920928,7.135023411920929,13.409468011920929,7.343931011920929C13.34379301192093,7.897807411920929,13.092739011920928,8.407185411920928,12.70547801192093,8.79408051192093C12.079658011920928,7.796718411920929,10.98494501192093,7.191249711920929,9.807498711920928,7.191249711920929C8.84493241192093,7.191249711920929,7.926897811920929,7.596736211920929,7.278597211920929,8.30823881192093L5.794902611920929,7.837869011920929Q4.54460051192093,7.439836311920929,3.290682411920929,7.051414311920929C3.108942111920929,6.991391011920929,2.924064911920929,6.941370811920929,2.736852011920929,6.901542511920929C2.3088937119209287,6.818829311920929,1.8150065119209289,6.841611211920929,1.432596201920929,7.068199011920929C1.0778479019209288,7.269458111920929,0.836193501920929,7.623557411920929,0.778067811920929,8.027285911920929C0.7111728019209289,7.872332911920929,0.657828451920929,7.711885711920929,0.618632435920929,7.547737411920929C0.42727268192092893,6.740241811920929,0.6415674309209289,5.890162311920929,1.192841411920929,5.269903011920929C1.4361915019209288,5.001285411920929,1.7409777119209289,4.795612111920929,2.081129411920929,4.670472911920929C2.457155211920929,4.540559311920929,2.862039411920929,4.518547611920929,3.249928311920929,4.606933911920929C3.468435611920929,4.656951711920929,3.684115711920929,4.718580111920929,3.896061711920929,4.791560011920929L4.907823811920929,5.111653111920929L7.974271111920929,6.074336311920929Q9.303697411920929,6.499929211920929,10.63795301192093,6.913548811920929C10.820187011920929,6.969887511920929,11.00231701192093,7.037025311920929,11.189380011920928,7.0789755119209286C11.62327501192093,7.174900811920929,12.13404601192093,7.159314411920929,12.52839501192093,6.935123311920929C12.894467011920929,6.736387111920929,13.145127011920929,6.376361711920929,13.204496011920929,5.964040111920929ZM12.624997011920929,10.61249901192093C12.624997011920929,12.168561011920929,11.363557011920928,13.429999011920929,9.807498711920928,13.429999011920929C8.25143701192093,13.429999011920929,6.989996711920929,12.168561011920929,6.989996711920929,10.61249901192093C6.989996711920929,9.056437311920929,8.25143701192093,7.794999411920929,9.807498711920928,7.794999411920929C11.363557011920928,7.794999411920929,12.624997011920929,9.056437311920929,12.624997011920929,10.61249901192093ZM9.016871311920928,9.203749511920929L7.593747411920929,10.61249901192093L9.016871311920928,12.021250011920928L9.60193901192093,11.598622011920929L8.60575081192093,10.612498011920929L9.60193901192093,9.626373111920929L9.016871311920928,9.203749511920929ZM10.59812001192093,9.203749511920929L10.01305471192093,9.626373111920929L11.00924301192093,10.612498011920929L10.01305471192093,11.598622011920929L10.59812001192093,12.021250011920928L12.021247011920929,10.61249901192093L10.59812001192093,9.203749511920929ZM7.792590911920929,13.377477011920929C7.116531711920929,12.88481501192093,6.644395211920929,12.161533011920929,6.465446311920929,11.344374011920928C6.247283311920929,11.193953011920929,6.038835311920929,11.03024901192093,5.810488511920929,10.89376101192093C5.183414711920929,10.523033011920928,4.478796511920929,10.30305371192093,3.752206111920929,10.25117191192093C3.373121311920929,10.212150411920929,2.990139111920929,10.239740211920928,2.620563611920929,10.332694811920929C2.4466323119209292,10.371808811920928,2.289135911920929,10.46396711192093,2.1698266119209286,10.596444011920928C1.938463511920929,10.89975701192093,2.1482491119209293,11.233040011920929,2.358033611920929,11.47401801192093C2.589444211920929,11.726658011920929,2.846572011920929,11.95447201192093,3.125242311920929,12.153769011920929C4.484981811920929,13.167788011920928,6.163141511920929,13.58699601192093,7.792590911920929,13.377477011920929Z" fill-rule="evenodd" fill-opacity="1"/></svg>',
      copy: '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6.5 6.8V5.7a2.6 2.6 0 0 1 2.6-2.6h9.4a2.6 2.6 0 0 1 2.6 2.6v9.4a2.6 2.6 0 0 1-2.6 2.6h-0.8"/><rect x="2.3" y="6.5" width="14.6" height="14.6" rx="2.6"/></svg>',
      apps: '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.65" y="3.65" width="6.55" height="6.55" rx="1.6"/><rect x="13.8" y="3.65" width="6.55" height="6.55" rx="1.6"/><rect x="3.65" y="13.8" width="6.55" height="6.55" rx="1.6"/><rect x="13.8" y="13.8" width="6.55" height="6.55" rx="1.6"/></svg>',
      right: '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9.5 5.6 15.9 12l-6.4 6.4"/></svg>'
    };
    var OPEN_WITH = [
      { id: 'vscode',   label: 'VS Code',         svg: '<svg viewBox="0 0 14 14" width="14" height="14" fill="currentColor" aria-hidden="true"><g><path d="M10.20231631875,1.397796630859375L5.28318331875,5.920730130859375L2.5340962187500002,3.848589930859375L1.3979493522644,4.509856730859375L4.10778931875,6.999943230859375L1.39794921875,9.490029330859375L2.5340959187500003,10.153256430859376L5.28318241875,8.081162930859374L10.20231531875,12.602137630859374L12.60210221875,11.436591630859375L12.60210221875,2.5633899308593753L10.20231631875,1.397796630859375ZM10.20231631875,4.372516630859375L10.20231631875,9.627182930859375L6.71542981875,6.999756330859375L10.20231631875,4.372516630859375Z" fill="#2196F3" fill-opacity="1"/></g></svg>' },
      { id: 'trae',     label: 'Trae',            svg: '<svg viewBox="0 0 14 14" width="14" height="14" fill="currentColor" aria-hidden="true"><g><path d="M14,11.98225500234375L1.9996666,11.98225500234375L1.9996666,9.98375420234375L0,9.98375420234375L0,1.98333740234375L14,1.98333740234375L14,11.98167040234375L14,11.98225500234375ZM1.9996666,9.98375420234375L12.000334,9.98375420234375L12.000334,3.9824207023437497L1.9996666,3.9824207023437497L1.9996666,9.98375420234375ZM7.0005832,6.95275350234375L5.5859995,8.36675360234375L4.1719995,6.95275350234375L5.5859995,5.53875400234375L7.0005832,6.95275350234375ZM11.0005,6.95217040234375L9.5865002,8.36558720234375L8.171916,6.95217040234375L9.5865002,5.53758690234375L11.0005,6.95217040234375Z" fill="#00CB60" fill-opacity="1"/></g></svg>' },
      { id: 'chrome',   label: 'Google Chrome',   svg: '<svg viewBox="0 0 14 14" width="14" height="14" fill="currentColor" aria-hidden="true"><g><path d="M1.6905517578125,2.438328523046875C4.9443848578125,-1.348088176953125,10.9783849578125,-0.600838126953125,13.2335517578125,3.823745223046875L7.8126354578125,3.823745223046875C6.8361353578125,3.823745223046875,6.2055516578125,3.801578523046875,5.5224685578125,4.160912023046875C4.7198018578125005,4.583828423046875,4.1143016578125,5.367245223046875,3.9025521578125,6.287161823046875L1.6905517578125,2.438911923046875L1.6905517578125,2.438328523046875Z" fill="#EA4335" fill-opacity="1"/><path d="M4.67138671875,6.9999854515625C4.67138671875,8.2833189515625,5.71497001875,9.3274855515625,6.99771971875,9.3274855515625C8.28105331875,9.3274855515625,9.32405331875,8.2833189515625,9.32405331875,6.9999854515625C9.32405331875,5.7166517515625,8.28047011875,4.6724853515625,6.99771971875,4.6724853515625C5.71438631875,4.6724853515625,4.67138618469238,5.7166517515625,4.67138671875,6.9999854515625Z" fill="#4285F4" fill-opacity="1"/><path d="M7.9006548,10.0467557671875C6.5945711,10.434672867187501,5.0668211,10.0041723671875,4.2297378,8.559255567187499C3.5904047,7.4567556671875,1.9022381,4.5155893671875,1.1351548,3.1785888671875C-1.5522618,7.2969217671875,0.76415479,12.9103383671875,5.6425714,13.8681718671875L7.9000711,10.0467557671875L7.9006548,10.0467557671875Z" fill="#34A853" fill-opacity="1"/><path d="M9.158279696875,4.672488708518125C10.241158496875,5.683395117578125,10.484791296875,7.307126317578125,9.746279196875001,8.591322417578125C9.191528996875,9.547989417578126,7.419945656875,12.538155517578126,6.561279296875,13.985988617578125C11.587862496875001,14.295739217578125,15.252945896875,9.369489217578124,13.597446896874999,4.671905517578125L9.158279696875,4.671905517578125L9.158279696875,4.672488708518125Z" fill="#FBBC05" fill-opacity="1"/></g></svg>' },
      { id: 'edge',     label: 'Microsoft Edge',  svg: '<svg viewBox="0 0 14 14" width="14" height="14" fill="currentColor" aria-hidden="true"><g><path d="M12.6286916453125,10.4146718796875C12.4435930453125,10.513641379687499,12.2517776453125,10.5995015796875,12.0546598453125,10.671619879687501C11.4270362453125,10.906760179687499,10.7622447453125,11.0271258796875,10.0920186453125,11.0269732796875C7.5061430453125,11.0269732796875,5.2537527453125,9.2502083796875,5.2537522453125,6.9650163796874995C5.259201745312501,6.3415612596875,5.602470845312499,5.7701431196875,6.1503350453125005,5.4725341796875C3.8104729653125,5.5709396376875,3.2091064453125,8.0092069796875,3.2091064453125,9.4360861796875C3.2091064453125,13.4761752796875,6.9321115453125,13.8861980796875,7.7357554453125,13.8861980796875C8.1676454453125,13.8861980796875,8.818215345312499,13.7604570796875,9.2118372453125,13.6347179796875L9.2829074453125,13.6128501796875C10.7899155453125,13.0934385796875,12.0744285453125,12.0750856796875,12.9239082453125,10.7262911796875C12.9882049453125,10.625032879687499,12.9589347453125,10.4908818796875,12.8583049453125,10.4256081796875C12.7891969453125,10.3812665796875,12.7016992453125,10.3771009796875,12.6286916453125,10.4146718796875Z" fill="#0F5197" fill-opacity="1"/><path d="M5.7786336234375,13.197344353515625C5.2922559234375,12.894782353515625,4.8705015234375,12.499038653515624,4.5376320234375,12.032879853515626C2.9212365234375,9.819769853515625,3.6921274234375,6.683941353515625,6.1503877234375,5.472518953515625C6.4107265234375,5.331455453515625,6.7016797234375,5.256371253515625,6.9977679234375,5.253839953515625C7.5510549234375,5.259719853515625,8.0702076234375,5.522326253515625,8.4027786234375,5.964545753515625C8.6236629234375,6.260231453515625,8.7460556234375,6.617847653515625,8.7526645234375,6.986868853515625C8.7526645234375,6.975934953515625,10.0920720234375,2.635162353515625,4.3790898234375,2.635162353515625C1.9790911234375,2.635162353515625,0.0055158728475,4.914887953515625,0.0055158728475,6.910330753515625C-0.0036279344624999994,7.967249353515625,0.2223243734375,9.012979053515625,0.6670188934375,9.971833253515625C2.1751220234375,13.185309353515626,5.8494196234375,14.761686353515625,9.2173567234375,13.640168353515625C8.0614967234375,14.002358353515625,6.8050227234375,13.840555353515626,5.7786336234375,13.197344353515625Z" fill="#0C88DA" fill-opacity="1"/><path d="M8.3261919,8.1404066C8.2824564,8.1950769,8.1457815,8.2770815,8.1457815,8.4520245C8.1457815,8.5941648,8.2387199,8.7308397,8.402729,8.8456459C9.1899729,9.3923435,10.67152,9.3212719,10.676988,9.3212719C11.259742,9.320488,11.831676,9.1638203,12.333479,8.8675137C13.361939,8.2672482,13.994617,7.1663055,13.995437,5.9754872C14.011838,4.7508869,13.558081,3.9363086,13.37767,3.5754886C13.082328,2.9984438,12.69576,2.4728665,12.232886,2.0190427C11.665668,1.4654787,11.005375,1.0161538,10.282272,0.69166297C9.2489815,0.23042263,8.1292667,-0.0053362763,6.9977183,0.000091847658C3.1710913,-0.00028636304,0.053812437,3.0731559,0,6.899405C0.027334835,4.9039617,2.0118442,3.2912061,4.3735743,3.2912061C4.564918,3.2912061,5.6583118,3.3076072,6.6697001,3.84337C7.5608163,4.313529,8.0309753,4.876627,8.3535261,5.4397244C8.6924782,6.0246902,8.752615,6.7572641,8.752615,7.0524797C8.752615,7.3476954,8.6050062,7.7795863,8.3261919,8.1404066Z" fill="#2CC3D5" fill-opacity="1"/><path d="M8.8805651021875,0.206756591796875C8.8805651021875,0.206756591796875,13.975231642187499,5.472540391796875,8.2168751541875,8.317549691796875C8.2168751541875,8.317549691796875,7.8445745121875,8.935864491796876,9.6229794421875,9.255680991796876C9.6229794421875,9.255680991796876,12.5691285421875,9.895863491796876,13.7581939421875,7.307254291796875C13.997647242187501,6.495409991796875,14.2108593421875,5.237460591796875,13.5777840421875,3.837369891796875C13.3129372421875,3.266012891796875,12.957566742187499,2.741171591796875,12.5253925421875,2.283111291796875C12.0709202421875,1.783691391796875,11.5508303421875,1.348198491796875,10.9793341421875,0.988533381796875C10.0433895421875,0.510173651796875,8.8805651021875,0.206756958961475,8.8805651021875,0.206756591796875Z" fill="#49D668" fill-opacity="1"/></g></svg>' },
      { id: 'notes',    label: 'Notes',           svg: '<svg viewBox="0 0 14 14" width="14" height="14" fill="currentColor" aria-hidden="true"><g><path d="M9.916667,13.41664698828125L4.0833333,13.41664698828125C2.7946688,13.41664698828125,1.75,12.37197698828125,1.75,11.08331298828125L1.75,2.91664628828125C1.74999973297119,1.62798178828125,2.7946686,0.583313055038452,4.0833333,0.58331298828125L9.916667,0.58331298828125C11.2053318,0.58331365585326,12.25,1.62798218828125,12.25,2.91664628828125L12.25,11.08331298828125C12.249999,12.37197698828125,11.2053308,13.41664498828125,9.916667,13.41664698828125ZM8.4583335,8.16664648828125C8.055892499999999,8.167289688281251,7.7298093,8.49337248828125,7.729167,8.89581298828125L7.729167,10.06247898828125C7.7294888,10.46505358828125,8.0557594,10.79132498828125,8.4583335,10.79164698828125L9.625,10.79164698828125C10.0273476,10.79132498828125,10.3535242,10.46541018828125,10.354167,10.06306168828125L10.354167,8.89639658828125C10.3538465,8.49372668828125,10.027669,8.167288288281249,9.625,8.16664598828125L8.4583335,8.16664648828125ZM4.156250200000001,5.98906278828125C3.8743548,5.98906278828125,3.6458335,6.21758408828125,3.6458335,6.49947928828125C3.6458335,6.78137488828125,3.8743548,7.00989628828125,4.156250200000001,7.00989628828125L6.78125,7.00989628828125C7.0631452,7.00989628828125,7.291667,6.78137488828125,7.291667,6.49947928828125C7.291667,6.21758408828125,7.0631452,5.98906278828125,6.78125,5.98906278828125L4.156250200000001,5.98906278828125ZM4.156250200000001,3.64522958828125C3.8809106,3.65453818828125,3.6625164,3.88044098828125,3.6625164,4.15593788828125C3.6625164,4.43143458828125,3.8809111,4.65733718828125,4.156250200000001,4.66664598828125L8.96875,4.66664598828125C9.2508063,4.66664598828125,9.4794588,4.437993988281249,9.4794588,4.15593768828125C9.4794588,3.87388138828125,9.2508063,3.64522938828125,8.96875,3.64522938828125L4.156250200000001,3.64522958828125Z" fill="#F9A01E" fill-opacity="1"/></g></svg>' },
      { id: 'explorer', label: '文件资源管理器',    svg: '<svg viewBox="0 0 14 14" width="14" height="14" fill="currentColor" aria-hidden="true"><g><path d="M12.6054934140625,12.44825461953125L1.3945556840625,12.44825461953125C1.0951416040625,12.44825461953125,0.8531494140625,12.20626261953125,0.8531494140625,11.90684791953125L0.8531494140625,3.06661378953125C0.8531494140625,2.76719970953125,1.0951416040625,2.52520751953125,1.3945556840625,2.52520751953125L12.6054934140625,2.52520751953125C12.9049074140625,2.52520751953125,13.1468994140625,2.76719970953125,13.1468994140625,3.06661378953125L13.1468994140625,11.90684791953125C13.1468994140625,12.20489501953125,12.9035394140625,12.44825461953125,12.6054934140625,12.44825461953125Z" fill="#FFA000" fill-opacity="1"/><path d="M7.0000243140625,4.8521485124999995L0.8531494140625,4.8521485124999995L0.8531494140625,2.0931640825C0.8531494140625,1.7937500025,1.0951416040625,1.5517578125,1.3945556840625,1.5517578125L5.6013918140625,1.5517578125C5.8406496140625,1.5517578125,6.0511961140625,1.7076171924999999,6.1195555140625,1.9373046725L7.0000243140625,4.8521485124999995Z" fill="#FFA000" fill-opacity="1"/><path d="M11.4875441,12L2.51116568,12C2.22847556,12,2,11.770205,2,11.485881299999999L2,4.5140956C2,4.22977237,2.22845247,4,2.5111425499999998,4L11.4888115,4C11.7715015,4,11.9999542,4.22977237,11.9999542,4.5140956L12,11.485881299999999C12,11.768906099999999,11.7702332,12,11.4875441,12Z" fill="#FFFFFF" fill-opacity="1"/><path d="M12.6054934140625,12.4482421625L1.3945556840625,12.4482421625C1.0951416040625,12.4482421625,0.8531494140625,12.2062501625,0.8531494140625,11.9068360625L0.8531494140625,5.9095459025C0.8531494140625,5.6101318625,1.0951171640625,5.3681640625,1.3945312540625001,5.3681640625L12.6054684140625,5.3681640625C12.9048824140625,5.3681640625,13.1468504140625,5.6101318625,13.1468504140625,5.9095459025L13.1468994140625,11.9068360625C13.1468994140625,12.204882662500001,12.9035394140625,12.4482421625,12.6054934140625,12.4482421625Z" fill="#F7C015" fill-opacity="1"/></g></svg>' }
    ];
    var MENU = [
      { id: 'open',     label: '打开',            svg: ICON.file },
      { id: 'reveal',   label: '打开所在文件夹',    svg: ICON.folder },
      { id: 'chat',     label: '添加到对话',       svg: ICON.message },
      { id: 'brand',    label: '添加到 GienCoder', svg: ICON.brand },
      { id: 'path',     label: '复制路径',         svg: ICON.copy },
      { divider: true },
      { id: 'openwith', label: '打开方式',         svg: ICON.apps, children: OPEN_WITH }
    ];

    var tree = root.querySelector('.td-browse-files');
    var pre = root.querySelector('.td-browse-pre');
    var crumb = root.querySelector('.td-browse-crumb-path');
    if (!tree && !pre) return;

    var menu = null, sub = null, subRow = null, open = false, cur = -1, rows = [], target = null;

    function build(items) {
      var box = document.createElement('div');
      box.className = 'giencoder-dropdown-popup td-ctx';
      box.setAttribute('role', 'menu');
      items.forEach(function (it) {
        if (it.divider) {
          var d = document.createElement('div');
          d.className = 'giencoder-dropdown-divider';
          d.setAttribute('role', 'separator');
          box.appendChild(d);
          return;
        }
        var row = document.createElement('div');
        row.className = 'giencoder-dropdown-item' + (it.children ? ' giencoder-dropdown-submenu' : '');
        row.setAttribute('role', 'menuitem');
        row.setAttribute('tabindex', '-1');
        row.setAttribute('data-ctx-id', it.id);
        if (it.children) row.setAttribute('aria-haspopup', 'menu');
        row.innerHTML = '<span class="td-ctx-ico" aria-hidden="true">' + it.svg + '</span>' +
                        '<span class="td-ctx-label"></span>' +
                        (it.children
                          ? '<span class="giencoder-dropdown-arrow" aria-hidden="true">' + ICON.right + '</span>'
                          : '');
        row.querySelector('.td-ctx-label').textContent = it.label;
        box.appendChild(row);
      });
      return box;
    }

    function ensure() {
      if (menu) return;
      menu = build(MENU);
      menu.style.display = 'none';
      document.body.appendChild(menu);
      sub = build(OPEN_WITH);
      sub.classList.add('giencoder-dropdown-submenu-popup');
      sub.style.display = 'none';
      document.body.appendChild(sub);
      rows = Array.prototype.slice.call(menu.querySelectorAll('.giencoder-dropdown-item'));

      menu.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
      menu.addEventListener('click', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.giencoder-dropdown-item') : null;
        if (!row) return;
        if (row.getAttribute('data-ctx-id') === 'openwith') { toggleSub(row); return; }
        run(row.getAttribute('data-ctx-id'));
      });
      /* 悬停切换：主菜单里移到别的项就收子菜单；指向「打开方式」本身或子菜单则保留 */
      menu.addEventListener('pointerover', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.giencoder-dropdown-item') : null;
        if (!row) return;
        if (row.getAttribute('data-ctx-id') === 'openwith') { openSub(row); return; }
        if (subRow && subRow !== row) closeSub();
      });
      sub.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
      sub.addEventListener('click', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.giencoder-dropdown-item') : null;
        if (row) run(row.getAttribute('data-ctx-id'));
      });
      sub.addEventListener('pointerover', function () { if (subRow) subRow.classList.add('is-hover'); });
      sub.addEventListener('pointerleave', function () { closeSub(); });
    }

    function openSub(row) {
      ensure();
      if (subRow === row && sub.classList.contains('giencoder-popup-open')) return;
      closeSub();
      subRow = row;
      row.classList.add('is-hover');
      var r = row.getBoundingClientRect();
      sub.style.display = 'flex';
      sub.style.visibility = 'hidden';
      var w = sub.offsetWidth, h = sub.offsetHeight;
      var left = r.right + 4, top = r.top;   /* DS 契约 submenu-popup: left calc(100%+4px) / top 0 */
      if (left + w > window.innerWidth - 8) left = Math.max(8, r.left - 4 - w);
      if (top + h > window.innerHeight - 8) top = Math.max(8, window.innerHeight - 8 - h);
      if (top < 8) top = 8;
      sub.style.left = left + 'px';
      sub.style.top = top + 'px';
      sub.style.visibility = '';
      sub.classList.add('giencoder-popup-open');
    }

    function closeSub() {
      if (!sub || !subRow) { return; }
      subRow.classList.remove('is-hover');
      subRow = null;
      cur = -1;
      sub.classList.remove('giencoder-popup-open');
      setTimeout(function () {
        if (!subRow && sub) sub.style.display = 'none';
      }, 200);
    }

    function toggleSub(row) {
      if (subRow === row && sub.classList.contains('giencoder-popup-open')) closeSub();
      else openSub(row);
    }

    /* 结果回执一律走 DS Message（第 19 轮全局约定），不另造提示 */
    function run(id) {
      var name = (target && target.name) || '';
      var path = (target && target.path) || '';
      close();
      if (id === 'path') {
        try { if (navigator.clipboard && path) navigator.clipboard.writeText(path); } catch (er) {}
        avToast(path ? '已复制路径：' + path : '已复制路径');
        return;
      }
      var plain = { open: '打开', reveal: '打开所在文件夹', chat: '添加到对话', brand: '添加到 GienCoder' };
      if (plain[id]) { avToast(plain[id] + '：' + name); return; }
      for (var i = 0; i < OPEN_WITH.length; i++) {
        if (OPEN_WITH[i].id === id) { avToast('已用 ' + OPEN_WITH[i].label + ' 打开：' + name); return; }
      }
    }

    function flag(on) {
      if (on) document.documentElement.setAttribute('data-td-ctx-open', '');
      else document.documentElement.removeAttribute('data-td-ctx-open');
    }

    function place(x, y) {
      menu.style.display = 'flex';
      menu.style.visibility = 'hidden';
      var w = menu.offsetWidth, h = menu.offsetHeight;
      var left = x, top = y;
      if (left + w > window.innerWidth - 8) left = Math.max(8, window.innerWidth - 8 - w);
      if (top + h > window.innerHeight - 8) top = Math.max(8, window.innerHeight - 8 - h);
      menu.style.left = left + 'px';
      menu.style.top = top + 'px';
      /* 缩放原点落在光标上 —— 契约的「轻微位移展开」就有了方向感 */
      menu.style.transformOrigin = (x - left) + 'px ' + (y - top) + 'px';
      menu.style.visibility = '';
    }

    function show(x, y, t) {
      ensure();
      closeSub();
      target = t;
      place(x, y);
      void menu.offsetHeight;                 /* 强制回流，让开合过渡生效 */
      menu.classList.add('giencoder-popup-open');
      open = true;
      cur = -1;
      rows.forEach(function (r) { r.classList.remove('is-hover'); });
      flag(true);
    }

    function close() {
      if (!menu || !open) return;
      open = false;
      closeSub();
      menu.classList.remove('giencoder-popup-open');
      setTimeout(function () { if (!open && menu) menu.style.display = 'none'; }, 200);
      flag(false);
    }

    function focusRow(i) {
      if (!rows.length) return;
      cur = (i + rows.length) % rows.length;
      rows.forEach(function (r, k) { r.classList.toggle('is-hover', k === cur); });
      if (rows[cur].getAttribute('data-ctx-id') === 'openwith') openSub(rows[cur]);
      else if (subRow) closeSub();
    }

    /* ---- 触发：树行 / 代码预览区 ---- */
    function hit(e) {
      var t = e.target;
      if (!t || !t.closest) return null;
      var base = crumb ? crumb.textContent.replace(/\s*\/\s*/g, '/').replace(/\/[^/]*$/, '') : '';
      var row = t.closest('.td-bf');
      if (row && tree && tree.contains(row)) {
        var nm = row.querySelector('.td-bf-name');
        var name = nm ? nm.textContent : '';
        return { name: name, path: (base ? base + '/' : '') + name };
      }
      if (pre && pre.contains(t)) {
        var p = crumb ? crumb.textContent.replace(/\s*\/\s*/g, '/') : '';
        return { name: p.split('/').pop() || 'index.html', path: p };
      }
      return null;
    }

    root.addEventListener('contextmenu', function (e) {
      if (!avBrowseOpen()) return;
      var t = hit(e);
      if (!t) return;
      e.preventDefault();
      var row = e.target && e.target.closest ? e.target.closest('.td-bf') : null;
      if (row && row.classList.contains('is-file')) {
        var old = root.querySelector('.td-bf.is-active');
        if (old) { old.classList.remove('is-active'); old.setAttribute('aria-selected', 'false'); }
        row.classList.add('is-active');
        row.setAttribute('aria-selected', 'true');
      }
      show(e.clientX, e.clientY, t);
    });

    /* ---- 关闭途径（契约 clickOutsideClose / escClose） ---- */
    document.addEventListener('pointerdown', function (e) {
      if (!open) return;
      if (e.button === 2) return;                       /* 右键交给 contextmenu 分支重开 */
      if (menu.contains(e.target) || sub.contains(e.target)) return;
      close();
    }, true);
    window.addEventListener('blur', close);
    window.addEventListener('resize', close);
    root.addEventListener('scroll', function () { if (open) close(); }, true);
    document.addEventListener('wheel', function () { if (open) close(); }, { passive: true });
    document.addEventListener('td:close-ctx', close);
    document.addEventListener('td:close-popovers', close);

    /* ---- 键盘（契约 keyboard 清单） ---- */
    document.addEventListener('keydown', function (e) {
      if (!open) return;
      /* 先打事件标记（与浏览侧栏的独立 Esc 监听共用，见 r56 说明），再 close() 清理状态位 */
      if (e.key === 'Escape') { e.__tdCtxHandled = true; e.stopPropagation(); close(); return; }
      if (e.key === 'ArrowDown') { e.preventDefault(); focusRow(cur + 1); return; }
      if (e.key === 'ArrowUp') { e.preventDefault(); focusRow(cur - 1); return; }
      if (e.key === 'ArrowRight') {
        if (cur >= 0 && rows[cur].getAttribute('data-ctx-id') === 'openwith') {
          e.preventDefault(); openSub(rows[cur]);
        }
        return;
      }
      if (e.key === 'ArrowLeft') { if (subRow) { e.preventDefault(); closeSub(); } return; }
      if (e.key === 'Enter' || e.key === ' ') {
        if (cur < 0) return;
        e.preventDefault();
        var id = rows[cur].getAttribute('data-ctx-id');
        if (id === 'openwith') toggleSub(rows[cur]); else run(id);
      }
    });
  }

(function () {
  var KEY = 'giencoder:av-browse:v1';
  var GAP = 8;                                   /* 与 .av-chat-gutter 净占位同值 */
  /* ★ 第 71 轮第 4 项：预览栏不再死守 641px —— 空间不够时先让预览栏，直到 main 拿到 MAIN_MIN。
     默认宽仍是 641；MIN_PANEL 由 641 修正为 561 = 文件树 MIN_TREE(240) + 分栏条 1 + 代码区 MIN_CODE(320)
     —— 原来的 641 与「内部两栏最小宽之和」本来就自相矛盾，等于把面板钉死在默认值上。
     MAIN_MIN 240 → 380：main 重排后的舒适下限（配合 @container 单列布局）。 */
  var DEF_PANEL = 641, MIN_PANEL = 561, MAIN_MIN = 380;
  var DEF_TREE = 296, MIN_TREE = 240, MIN_CODE = 320;

  var slot = document.getElementById('av-browse-slot');
  if (!slot) return;
  var pane = null, splitMain = null;
  var hostRow = null, hostMain = null, gutter = null, drawer = null;
  /* 生效宽：每次由期望宽 + 当前可用宽重钳，可被临时压缩 */
  var panelW = DEF_PANEL, treeW = DEF_TREE;
  /* ★ 期望宽（用户意图）：仅由「恢复记忆 / 拖动 / 键盘 / 双击复位」改写。
     clampNow / setOpen 一律从它重钳 → 视口变大时生效宽会自动长回来，避免「一缩到底」的棘轮。 */
  var wantPanel = DEF_PANEL, wantTree = DEF_TREE;
  var bound = false, ctxBound = false;

  function readStore() {
    try { return JSON.parse(localStorage.getItem(KEY) || 'null') || {}; } catch (e) { return {}; }
  }
  function writeStore(patch) {
    var d = readStore();
    for (var k in patch) { if (Object.prototype.hasOwnProperty.call(patch, k)) d[k] = patch[k]; }
    try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {}
  }
  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  /* ==================== 挂载：shell flex 行的最后一个子项 ====================
     行的 DOM 顺序由抽屉脚本先建立：… <main> → .av-chat-gutter → <aside 抽屉>；
     本脚本再往后接 [分栏条 td-split="main"] → [预览栏 slot]。
     抽屉脚本不认识本节点，故两边各挂一个常驻 MutationObserver；place() 命中即早退、不产生新变更，
     不会互激。 */
  function place() {
    if (hostRow && hostRow.isConnected
        && drawer && drawer.parentElement === hostRow
        && splitMain && splitMain.parentElement === hostRow
        && slot.parentElement === hostRow
        && splitMain.previousElementSibling === drawer
        && slot.previousElementSibling === splitMain) return true;
    hostRow = document.querySelector('div:has(> main)');
    if (!hostRow) return false;
    hostMain = hostRow.querySelector(':scope > main') || hostRow.querySelector('main');
    if (!hostMain) return false;
    gutter = hostRow.querySelector('.av-chat-gutter');
    drawer = document.getElementById('av-chat-drawer');
    if (!gutter || !drawer || drawer.parentElement !== hostRow) return false;   /* 等抽屉脚本先挂好 */
    splitMain = document.getElementById('av-browse-split');
    pane = slot.querySelector('.td-browse');
    if (!splitMain || !pane) return false;
    hostRow.insertBefore(splitMain, drawer.nextSibling);
    hostRow.insertBefore(slot, splitMain.nextSibling);
    slot.classList.add('av-slot-placed');   /* ★ 第 70 轮第 2 项：挂进 flex 行后才渲染 */
    bindAll();
    clampNow();
    return true;
  }

  /* ==================== 宽度：① 预览栏 ② 文件目录 ==================== */
  /* 可分配给 main + gutter + 抽屉 + 分栏条 + 预览栏 的总宽 = 行内容宽 − 其它 flex 子项（左导航等） */
  function freeW() {
    if (!hostRow) return 0;
    var cs = getComputedStyle(hostRow);
    var w = hostRow.clientWidth - parseFloat(cs.paddingLeft || 0) - parseFloat(cs.paddingRight || 0);
    Array.prototype.forEach.call(hostRow.children, function (c) {
      if (c === hostMain || c === gutter || c === drawer || c === splitMain || c === slot) return;
      w -= c.getBoundingClientRect().width;
    });
    return w;
  }
  function chatW() {
    var v = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--av-chat-w'));
    return isNaN(v) ? 480 : v;
  }
  function maxPanelW() { return Math.max(MIN_PANEL, Math.round(freeW() - chatW() - GAP - MAIN_MIN)); }
  function setPanelW(w, persist) {
    wantPanel = Math.round(w);
    panelW = Math.round(clamp(wantPanel, MIN_PANEL, maxPanelW()));
    slot.style.setProperty('--av-browse-w', panelW + 'px');
    if (splitMain) {
      splitMain.setAttribute('aria-valuenow', String(panelW));
      splitMain.setAttribute('aria-valuemin', String(MIN_PANEL));
      splitMain.setAttribute('title', '拖动调整文件预览栏宽度（最小 ' + MIN_PANEL + 'px）· 双击复位');
    }
    if (persist) writeStore({ panelW: wantPanel });
    return panelW;
  }
  function maxTree() {
    var sw = slot.getBoundingClientRect().width || panelW;
    return Math.max(MIN_TREE, Math.round(sw - 1 - MIN_CODE));
  }
  function setTree(w, persist) {
    wantTree = Math.round(w);
    treeW = Math.round(clamp(wantTree, MIN_TREE, maxTree()));
    pane.style.setProperty('--td-browse-tree-w', treeW + 'px');
    var st = pane.querySelector('[data-td-split="tree"]');
    if (st) {
      st.setAttribute('aria-valuenow', String(treeW));
      st.setAttribute('aria-valuemin', String(MIN_TREE));
      st.setAttribute('title', '拖动调整文件目录宽度（最小 ' + MIN_TREE + 'px）· 双击复位');
    }
    if (persist) writeStore({ treeW: wantTree });
    return treeW;
  }
  function clampNow() {
    if (!hostRow) return;
    setPanelW(wantPanel, false);
    setTree(wantTree, false);
  }
  /* 让 AI 会话栏脚本按新的可用宽重算钳位（它监听 window resize 并做 rAF 节流；此处不改它的代码） */
  function syncLayout() { try { window.dispatchEvent(new Event('resize')); } catch (e) {} }

  /* ==================== 展开 / 收起（含微动效，与详情页同款） ==================== */
  function setOpen(on) {
    if (!place()) return;
    var isOn = hostRow.classList.contains('av-browse-on');
    if (on === isOn && !pane.classList.contains('is-closing')) return;
    var btn = drawer.querySelector('[data-td-browse-toggle]');
    if (on) {
      if (pane._browseT) { clearTimeout(pane._browseT); pane._browseT = null; }
      pane.classList.remove('is-closing');
      hostRow.classList.add('av-browse-on');
      if (btn) btn.setAttribute('aria-pressed', 'true');
      setPanelW(wantPanel, false);
      setTree(wantTree, false);
      syncLayout();
      setTimeout(syncLayout, 260);              /* 左导航 200ms 收拢结束、可用宽定型后再校一次 */
      return;
    }
    if (pane.classList.contains('is-closing')) return;
    /* ★ 第 70 轮第 2 项：收起不再播 keyframes —— 摘掉状态类后由 .td-browse-slot 的
       flex-basis 过渡自然收拢（与左导航同款）。is-closing 只作 JS 防抖标记，无对应 CSS；
       期间再点开会在上方分支里清掉定时器并平滑反向。 */
    pane.classList.add('is-closing');
    hostRow.classList.remove('av-browse-on');
    if (btn) btn.setAttribute('aria-pressed', 'false');
    pane._browseT = setTimeout(function () {
      pane._browseT = null;
      pane.classList.remove('is-closing');
      syncLayout();
    }, 220);
    syncLayout();
  }

  /* ==================== 一次性绑定 ==================== */
  function bindSplit(el, kind) {
    if (!el) return;
    var dragging = false, startX = 0, startPanel = 0, startTree = 0;
    el.addEventListener('pointerdown', function (e) {
      if (!avBrowseOpen() || e.button !== 0) return;
      dragging = true;
      startX = e.clientX; startPanel = panelW; startTree = treeW;
      el.classList.add('is-dragging');
      hostRow.classList.add('is-col-dragging');
      if (el.setPointerCapture) { try { el.setPointerCapture(e.pointerId); } catch (err) {} }
      e.preventDefault();
    });
    el.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      if (kind === 'panel') setPanelW(startPanel - (e.clientX - startX), false);
      else setTree(startTree + (e.clientX - startX), false);
    });
    function end() {
      if (!dragging) return;
      dragging = false;
      el.classList.remove('is-dragging');
      hostRow.classList.remove('is-col-dragging');
      writeStore(kind === 'panel' ? { panelW: wantPanel } : { treeW: wantTree });
    }
    el.addEventListener('pointerup', end);
    el.addEventListener('pointercancel', end);
    el.addEventListener('dblclick', function () {
      if (kind === 'panel') setPanelW(DEF_PANEL, true); else setTree(DEF_TREE, true);
    });
    el.addEventListener('keydown', function (e) {
      var step = e.shiftKey ? 48 : 16;
      if (e.key === 'ArrowLeft') { e.preventDefault(); if (kind === 'panel') setPanelW(panelW + step, true); else setTree(treeW - step, true); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); if (kind === 'panel') setPanelW(panelW - step, true); else setTree(treeW + step, true); }
    });
  }

  function bindAll() {
    if (bound) return;
    bound = true;

    var btn = drawer.querySelector('[data-td-browse-toggle]');
    if (btn) btn.addEventListener('click', function () { setOpen(!avBrowseOpen()); });
    var close = pane.querySelector('[data-td-browse-close]');
    if (close) close.addEventListener('click', function () { setOpen(false); });

    bindSplit(splitMain, 'panel');
    bindSplit(pane.querySelector('[data-td-split="tree"]'), 'tree');

    /* ---------- crumb 右侧两按钮（与详情页同款） ---------- */
    var body = pane.querySelector('.td-browse-body');
    var tgl = pane.querySelector('[data-td-tree-toggle]');
    if (tgl && body) {
      tgl.addEventListener('click', function () {
        var hidden = body.classList.toggle('is-no-tree');
        tgl.setAttribute('aria-pressed', hidden ? 'false' : 'true');
        var label = hidden ? '显示文件目录' : '隐藏文件目录';
        tgl.setAttribute('aria-label', label);
        tgl.setAttribute('title', label);
        if (!hidden) setTree(wantTree, false);
      });
    }
    var openBtn = pane.querySelector('[data-td-open-browser]');
    var crumb = pane.querySelector('.td-browse-crumb-path');
    if (openBtn) {
      openBtn.addEventListener('click', function () {
        var name = crumb && crumb.textContent ? crumb.textContent.split('/').pop().trim() : '';
        if (!name) return;
        /* 与详情页同口径：映射到仓库根的同名文件（本页在 pages/ 下）→ ../index.html 真实存在。
           ⚠️ 内置 http 预览里 ../ 会落到 static-html 根 —— file:// 直开是标准用法。 */
        window.open(new URL('../' + name, location.href).href, '_blank', 'noopener');
      });
    }

    /* ---------- 文件树：展开/折叠 + 选中 ---------- */
    function refresh() {
      var rows = pane.querySelectorAll('.td-bf'), i;
      for (i = 0; i < rows.length; i++) {
        var p = rows[i].dataset.parent || '', ok = true;
        while (p) {
          var pr = pane.querySelector('.td-bf[data-node="' + p + '"]');
          if (!pr || pr.classList.contains('is-closed')) { ok = false; break; }
          p = pr.dataset.parent || '';
        }
        rows[i].classList.toggle('is-hidden', !ok);
      }
    }
    function toggleDir(row) {
      var closed = row.classList.toggle('is-closed');
      row.setAttribute('aria-expanded', closed ? 'false' : 'true');
      refresh();
    }
    function selectFile(row) {
      var old = pane.querySelector('.td-bf.is-active');
      if (old) { old.classList.remove('is-active'); old.setAttribute('aria-selected', 'false'); }
      row.classList.add('is-active');
      row.setAttribute('aria-selected', 'true');
    }
    var files = pane.querySelector('.td-browse-files');
    if (files) {
      files.addEventListener('click', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.td-bf') : null;
        if (!row) return;
        if (row.classList.contains('is-dir')) toggleDir(row); else selectFile(row);
      });
      files.addEventListener('keydown', function (e) {
        var row = e.target && e.target.closest ? e.target.closest('.td-bf') : null;
        if (!row || row !== e.target) return;
        var isDir = row.classList.contains('is-dir'), closed = row.classList.contains('is-closed');
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          if (isDir) toggleDir(row); else selectFile(row);
        } else if (e.key === 'ArrowRight' && isDir && closed) { e.preventDefault(); toggleDir(row); }
        else if (e.key === 'ArrowLeft' && isDir && !closed) { e.preventDefault(); toggleDir(row); }
      });
    }

    /* ---------- 恢复本页布局记忆 ---------- */
    var d = readStore();
    if (typeof d.panelW === 'number') { panelW = d.panelW; wantPanel = d.panelW; }
    if (typeof d.treeW === 'number') { treeW = d.treeW; wantTree = d.treeW; }
    clampNow();

    if (!ctxBound) {
      ctxBound = true;
      try { bindBrowseContextMenu(); } catch (e) {}
    }
  }

  /* ==================== Esc 裁决（捕获段，注册在抽屉脚本之前 → 先吃一层） ====================
     顺序：① 右键菜单 → ② 预览栏。自己吃掉即 stopImmediatePropagation，避免一次 Esc 把 AI 会话栏也收掉。 */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (document.documentElement.hasAttribute('data-td-ctx-open')) {
      e.preventDefault(); e.stopImmediatePropagation();
      document.dispatchEvent(new CustomEvent('td:close-ctx'));
      return;
    }
    if (avBrowseOpen()) {
      e.preventDefault(); e.stopImmediatePropagation();
      setOpen(false);
    }
  }, true);

  /* AI 会话栏收起时，预览栏一并收起（否则会留下一块孤立的文件预览） */
  new MutationObserver(function () {
    if (!document.documentElement.hasAttribute('data-av-chat-open') && avBrowseOpen()) setOpen(false);
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-av-chat-open'] });

  /* 视口变化重钳位 */
  var raf = 0;
  window.addEventListener('resize', function () {
    if (raf) cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function () { raf = 0; if (avBrowseOpen()) clampNow(); });
  });

  if (!place()) {
    var mo0 = new MutationObserver(function () { if (place()) mo0.disconnect(); });
    mo0.observe(document.body, { childList: true, subtree: true });
  }
  var moKeep = new MutationObserver(function () { place(); });
  moKeep.observe(document.body, { childList: true, subtree: true });
})();

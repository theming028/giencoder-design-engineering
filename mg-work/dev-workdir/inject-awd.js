const fs = require('fs');
const path = require('path');

const root = 'C:/Users/Administrator/Documents/Qoder/2026-09-24/0bfb1ccc/giencoder-design-engineering';
const icons = path.join(root, 'mg-work/dev-workdir/asset/icons');

const read = (f) => fs.readFileSync(path.join(icons, f), 'utf8').trim();

const frameSvg = read('svg_f6f9f697.svg');
const folderSvg = read('svg_eab17d9c.svg');
const plusSvg = read('svg_9a260fed.svg').replace('fill="#6B6B6B"', 'fill="currentColor"');
const lineSvg = read('svg_848f7e68.svg').replace('fill="#E5E5E5"', 'fill="currentColor"');

const markup =
`<div class="awd-root" data-node-id="1331:18125" data-name="容器 3">
  <div class="awd-card" data-node-id="1331:18124" data-name="容器 2">
    <div class="awd-card-bg" data-node-id="817:18556" data-name="矩形 494"></div>
    <div class="awd-card-frame" data-node-id="817:18698" data-name="矩形 495">${frameSvg}</div>
    <div class="awd-card-center" data-node-id="1331:18122" data-name="容器 1">
      <div class="awd-link" data-node-id="817:18561" data-name="Link">
        <span class="awd-link-icon">${plusSvg}</span>
        <span class="awd-link-text" data-node-id="817:18561/7:2495" data-name="文字链接">选择文件夹</span>
      </div>
      <div class="awd-illustration" data-node-id="817:18674" data-name="project-empty.f889c5e8">${folderSvg}</div>
    </div>
  </div>
  <div class="awd-divider" data-node-id="817:18722" data-name="divider">
    <span class="awd-divider-line">${lineSvg}</span>
    <div class="awd-divider-text" data-node-id="817:18722/1204:47623" data-name="text/text">
      <span data-node-id="817:18722/ip148:12469/6:287" data-name="中电金信">首次使用，请先添加你的工作目录</span>
    </div>
    <span class="awd-divider-line">${lineSvg}</span>
  </div>
  <div class="awd-button" data-node-id="817:18740" data-name="Button">
    <span class="awd-button-text" data-node-id="817:18740/ip148:12980" data-name="保存">进入研发工作台</span>
  </div>
</div>`;

const css =
`<style>
.awd-stage{width:100%;height:100%;display:flex;align-items:center;justify-content:center;}
.awd-root{width:500px;height:318px;position:relative;}
.awd-card{width:500px;height:200px;position:absolute;left:0;top:54px;z-index:0;}
.awd-card-bg{width:500px;height:200px;background:var(--color-fill-1);border-radius:24px;position:absolute;left:0;top:0;z-index:0;}
.awd-card-frame{position:absolute;left:16px;top:16px;z-index:1;line-height:0;}
.awd-card-center{width:122px;height:120px;position:absolute;left:189px;top:40px;z-index:2;}
.awd-link{width:122px;height:32px;display:flex;justify-content:flex-start;align-items:center;gap:6px;padding:5px 16px;background:var(--color-fill-1);border-radius:32px;position:absolute;left:0;top:88px;z-index:0;overflow:hidden;cursor:pointer;}
.awd-link-icon{width:14px;height:14px;color:var(--color-neutral-7);line-height:0;flex:none;}
.awd-link-icon svg{width:14px;height:14px;display:block;}
.awd-link-text{color:var(--color-text-1);font-size:14px;line-height:22px;white-space:nowrap;}
.awd-illustration{position:absolute;left:11px;top:0;z-index:1;line-height:0;}
.awd-divider{width:400px;height:22px;display:flex;justify-content:center;align-items:center;gap:16px;position:absolute;left:50px;top:0;z-index:1;overflow:hidden;}
.awd-divider-line{width:79px;height:1px;color:var(--color-border-2);line-height:0;flex:none;}
.awd-divider-line svg{width:79px;height:1px;display:block;}
.awd-divider-text{display:flex;justify-content:center;align-items:flex-start;flex-direction:column;overflow:hidden;}
.awd-divider-text span{color:var(--color-text-1);font-size:14px;line-height:22px;white-space:nowrap;}
.awd-button{width:468px;height:40px;display:flex;justify-content:center;align-items:center;gap:4px;padding:7px 20px;background:var(--color-primary-light-2);border-radius:8px;position:absolute;left:16px;top:278px;z-index:2;overflow:hidden;}
.awd-button-text{color:var(--color-white);font-size:14px;font-weight:500;line-height:22px;white-space:nowrap;}
</style>`;

const script =
`<script>
(function(){
  var AWD_HTML=${JSON.stringify(markup)};
  function inject(){
    var main=document.querySelector('main');
    if(!main||main.querySelector('.awd-stage'))return false;
    var wrap=document.createElement('div');
    wrap.className='awd-stage';
    wrap.innerHTML=AWD_HTML;
    main.appendChild(wrap);
    return true;
  }
  if(!inject()){
    var mo=new MutationObserver(function(){if(inject())mo.disconnect();});
    mo.observe(document.body,{childList:true,subtree:true});
  }
})();
</script>`;

const devPath = path.join(root, 'pages/dev.html');
let html = fs.readFileSync(devPath, 'utf8');
const anchor = '  </body>';
if (!html.includes(anchor)) { console.error('anchor not found'); process.exit(1); }
if (html.includes('awd-stage')) { console.error('already injected'); process.exit(1); }
html = html.replace(anchor, css + '\r\n' + script + '\r\n' + anchor);
fs.writeFileSync(devPath, html);
console.log('injected OK, new size =', html.length);

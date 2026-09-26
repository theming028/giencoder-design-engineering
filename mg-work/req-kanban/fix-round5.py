# -*- coding: utf-8 -*-
"""第 5 轮修复（8 项）：
1) 研发工作台「进入研发工作台」按钮改为正常态（可点击主色实心）
2) 研发工作台 awd-card-frame 整卡可点选择本地文件夹；hover 时 awd-link 变蓝底白字
3) 需求看板 rq-bh-controls 改为居左（与任务看板一致）
4) rq-stat hover 不改边框色，只显投影
5) 表格行 hover 时需求标题变蓝
6) 表格「需求子条目」标签着色
7) 表头加浅灰底色（对照设计稿）
8) 页码栏「共 256 条需求」与表格左对齐，分页按钮与表格右对齐
"""
import io, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
REQ = os.path.join(ROOT, 'pages', 'req-kanban.html')
KB = os.path.join(ROOT, 'pages', 'kanban.html')
DEV = os.path.join(ROOT, 'pages', 'dev.html')


def load(p):
    return io.open(p, encoding='utf-8').read()


def save(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


def rep(s, old, new, name):
    n = s.count(old)
    if n:
        s = s.replace(old, new)
    print(('OK  ' if n else 'MISS') + ' %-38s x%d' % (name, n), file=sys.stderr)
    return s, n


# ==================== 1 & 2) 研发工作台 dev.html ====================
print('########## dev.html ##########', file=sys.stderr)
d = load(DEV)

# 1) 按钮改为正常态：主色实心 + hover 加深
d, _ = rep(d,
           '.awd-button{width:468px;height:40px;display:flex;justify-content:center;align-items:center;gap:4px;'
           'padding:7px 20px;background:var(--color-primary-light-2);border-radius:8px;'
           'position:absolute;left:16px;top:278px;z-index:2;overflow:hidden;cursor:pointer;transition:filter .15s;}',
           '.awd-button{width:468px;height:40px;display:flex;justify-content:center;align-items:center;gap:4px;'
           'padding:7px 20px;background:var(--color-primary-6);border-radius:8px;'
           'position:absolute;left:16px;top:278px;z-index:2;overflow:hidden;cursor:pointer;'
           'transition:background .15s, box-shadow .15s;}',
           'awd-button -> primary-6')

# 2) 卡片：虚线框 + 整卡可点 + hover 效果
d, _ = rep(d,
           '.awd-card-frame{position:absolute;left:16px;top:16px;z-index:1;line-height:0;}',
           '.awd-card-frame{position:absolute;left:16px;top:16px;z-index:1;line-height:0;'
           'width:468px;height:168px;border:1px dashed var(--color-border-2);border-radius:12px;'
           'background:var(--color-bg-1);cursor:pointer;'
           'transition:border-color .15s, background .15s;}'
           '.awd-card-frame:hover{border-color:var(--color-primary-6);background:var(--color-primary-light-1);}'
           '.awd-card-frame:focus-visible{outline:2px solid var(--color-primary-6);outline-offset:2px;}',
           'awd-card-frame dashed + clickable')

# hover 时 awd-link 变蓝底白字
d, _ = rep(d,
           '.awd-link{width:122px;height:32px;display:flex;justify-content:flex-start;align-items:center;gap:6px;'
           'padding:5px 16px;background:var(--color-fill-1);border-radius:32px;position:absolute;left:0;top:88px;'
           'z-index:0;overflow:hidden;cursor:pointer;}',
           '.awd-link{width:122px;height:32px;display:flex;justify-content:center;align-items:center;gap:6px;'
           'padding:5px 16px;background:var(--color-fill-1);border-radius:32px;position:absolute;left:0;top:88px;'
           'z-index:1;overflow:hidden;cursor:pointer;pointer-events:none;'
           'transition:background .15s;}'
           '.awd-card-frame:hover .awd-link{background:var(--color-primary-6);}'
           '.awd-card-frame:hover .awd-link .awd-link-text{color:var(--color-white);}'
           '.awd-card-frame:hover .awd-link .awd-link-icon{color:var(--color-white);}'
           '.awd-card-frame:hover .awd-link .awd-link-icon svg path{fill:currentColor;}',
           'awd-link hover blue/white')

# 交互：整卡点击 + 选中后启用按钮
if 'function bindAwdCard' not in d:
    d, _ = rep(d,
               "    wrap.querySelector('.awd-button').addEventListener('click',function(){location.href='kanban.html';});\n    return true;",
               "    bindAwdCard(wrap);\n    return true;",
               'inject -> bindAwdCard')
    d, _ = rep(d,
               "  function inject(){",
               """  // 整卡可点：选择本地工作目录；选中后解锁「进入研发工作台」
  function bindAwdCard(wrap){
    var frame=wrap.querySelector('.awd-card-frame');
    var btn=wrap.querySelector('.awd-button');
    var btnText=wrap.querySelector('.awd-button-text');
    var dirEl=wrap.querySelector('.awd-divider-text span');
    var lock=(btn&&btn.getAttribute('data-locked')!=='false');
    function setLocked(v){
      lock=v;
      if(!btn)return;
      btn.setAttribute('data-locked',v?'true':'false');
      btn.style.background=v?'var(--color-primary-light-2)':'var(--color-primary-6)';
      btn.style.cursor=v?'not-allowed':'pointer';
      btn.style.opacity=v?'0.65':'1';
    }
    function pickDir(){
      var inp=document.createElement('input');
      inp.type='file'; inp.webkitdirectory=true; inp.multiple=true;
      inp.style.cssText='position:fixed;left:-9999px;top:-9999px;';
      document.body.appendChild(inp);
      inp.addEventListener('change',function(){
        var f=inp.files&&inp.files[0];
        var name='';
        if(f&&f.webkitRelativePath)name=f.webkitRelativePath.split('/')[0];
        else if(f&&f.name)name=f.name;
        if(!name)name='已选择工作目录';
        if(dirEl)dirEl.textContent=name;
        if(btnText)btnText.textContent='进入研发工作台';
        setLocked(false);
        inp.remove();
      });
      inp.click();
    }
    // 初始化：按设计稿先置为禁用态，选择目录后解锁
    setLocked(true);
    if(frame){
      frame.setAttribute('role','button');
      frame.setAttribute('tabindex','0');
      frame.setAttribute('aria-label','选择本地文件夹作为工作目录');
      frame.addEventListener('click',pickDir);
      frame.addEventListener('keydown',function(e){
        if(e.key==='Enter'||e.key===' '){e.preventDefault();pickDir();}
      });
    }
    if(btn){
      btn.addEventListener('click',function(){
        if(lock)return;
        location.href='kanban.html';
      });
    }
  }
  function inject(){""",
               'bindAwdCard implementation')

save(DEV, d)
d = load(DEV)
print('primary-6=%d locked=%d bindAwdCard=%d' % (
    d.count('background:var(--color-primary-6);'),
    d.count('data-locked'), d.count('function bindAwdCard')), file=sys.stderr)

# ==================== 3~8) 需求看板 req-kanban.html ====================
print('########## req-kanban.html ##########', file=sys.stderr)
s = load(REQ)

# 3) rq-bh-controls 居左（与任务看板一致：绝对定位 left:120px）
s, _ = rep(s,
           '.rq-bh-controls { display: flex; align-items: center; gap: 12px; margin-left: auto; }',
           '.rq-bh-controls { display: flex; align-items: center; gap: 8px; margin-left: 12px; }',
           'rq-bh-controls margin-left auto -> 12px')

# 4) rq-stat hover 不改边框色，只显投影
s, _ = rep(s,
           '.rq-stat:hover { border-color: var(--color-border-3); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }',
           '.rq-stat:hover { border-color: var(--color-border-2); box-shadow: 0 1px 8px rgba(0, 0, 0, 0.06); }',
           'rq-stat hover no border change')

# 5) 行 hover 时标题变蓝
s, _ = rep(s,
           '      .rq-link:hover { color: var(--color-primary-6); }',
           '      .rq-link:hover { color: var(--color-primary-6); }\n'
           '      /* 行 hover 时需求标题也转蓝，提示可点击 */\n'
           '      .rq-table tbody .giencoder-table-tr:hover .rq-link { color: var(--color-primary-6); }',
           'row hover -> link blue')

# 6) 需求子条目着色（青色系）
if '.rq-type--sub' not in s:
    s, _ = rep(s,
               '      .rq-type--entry { background: #FFECD9; color: #F3881E; }',
               '      .rq-type--entry { background: #FFECD9; color: #F3881E; }\n'
               '      .rq-type--sub { background: #E0F5F2; color: #0FA79A; }',
               'rq-type--sub colors')
s, _ = rep(s, '<span class=\\"rq-type\\">需求子条目</span>',
           '<span class=\\"rq-type rq-type--sub\\">需求子条目</span>',
           'type=需求子条目 -> sub')

# 7) 表头加浅灰底色（设计稿 #FAFAFA）
s, _ = rep(s,
           '.rq-table .giencoder-table-th { height: 32px; padding: 6px 12px; background: transparent; font-size: var(--font-size-body-1); border-top: none; }',
           '.rq-table .giencoder-table-th { height: 32px; padding: 6px 12px; font-size: var(--font-size-body-1); border-top: none;\n'
           '        /* 设计稿：表头浅灰底 #FAFAFA */\n'
           '        background: #FAFAFA; }',
           'th background #FAFAFA')
s, _ = rep(s,
           '.rq-table.giencoder-table-borderless .giencoder-table-th {\n        background: transparent; border-bottom: 1px solid var(--color-border-2);\n      }',
           '.rq-table.giencoder-table-borderless .giencoder-table-th {\n        background: #FAFAFA; border-bottom: 1px solid var(--color-border-2);\n      }',
           'borderless th #FAFAFA')

# 8) 页码栏左统计 / 右按钮，与表格两端对齐
s, _ = rep(s,
           '      .rq-pager {\n'
           '        flex: none; display: flex; align-items: center; justify-content: center; height: 48px;\n'
           '        padding: 0 16px; background: var(--color-bg-1); border-top: none;\n'
           '      }',
           '      /* 页码栏：左统计 / 右按钮，与表格两端对齐（表格 margin 20px） */\n'
           '      .rq-pager {\n'
           '        flex: none; display: flex; align-items: center; height: 48px;\n'
           '        margin: 0 20px; background: var(--color-bg-1); border-top: none;\n'
           '      }',
           'pager margin 20px + left align')
s, _ = rep(s,
           '      .rq-pager .giencoder-pagination { flex: none; }',
           '      .rq-pager .giencoder-pagination { flex: 1; justify-content: flex-end; }',
           'pagination flex:1 right')

save(REQ, s)
s = load(REQ)
print('bh-controls=%d sub=%d thFa=%d pagerMargin=%d' % (
    s.count('margin-left: 12px; }'), s.count('rq-type--sub'),
    s.count('background: #FAFAFA; }'), s.count('margin: 0 20px;')), file=sys.stderr)

print('DONE')

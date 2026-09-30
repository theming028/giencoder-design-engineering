#!/bin/bash
# r86 交互测试：真鼠标 hover/click/press（不用程序化 el.click()）
set -u
cd /e/GienCoder/giencoder-design-engineering
AB="/c/Users/Administrator/AppData/Local/npm-cache/_npx/ba0727cbf2d10686/node_modules/.bin/agent-browser"
O=mg-work/r86/ev
PICK='.giencoder-select-option:nth-child(3)'

"$AB" set viewport 1600 1100 >/dev/null 2>&1
"$AB" open "file:///E:/GienCoder/giencoder-design-engineering/pages/settings.html?v=$(date +%s%N)" >/dev/null 2>&1
"$AB" wait 1300 >/dev/null 2>&1

# ---------- A. hover 触发框：ds has-value ⇒ 箭头让位给清除 X，背景转 fill-1 ----------
"$AB" hover ".giencoder-select-view" >/dev/null 2>&1
"$AB" wait 350 >/dev/null 2>&1
"$AB" eval 'JSON.stringify({hasValue:document.querySelector(".giencoder-select").classList.contains("giencoder-select-has-value"),arrowDisplay:getComputedStyle(document.querySelector(".giencoder-select-arrow")).display,clearDisplay:getComputedStyle(document.querySelector(".giencoder-select-clear")).display,viewBg:getComputedStyle(document.querySelector(".giencoder-select-view")).backgroundColor,viewShadow:getComputedStyle(document.querySelector(".giencoder-select-view")).boxShadow})' > "$O/i1_hover.txt" 2>&1

# ---------- B. 点击展开：.giencoder-popup-open + aria-expanded + 面板几何 ----------
"$AB" click ".giencoder-select-view" >/dev/null 2>&1
"$AB" wait 500 >/dev/null 2>&1
"$AB" eval 'JSON.stringify({expanded:document.querySelector(".giencoder-select-view").getAttribute("aria-expanded"),openCls:document.querySelector(".giencoder-select-popup").classList.contains("giencoder-popup-open"),visibility:getComputedStyle(document.querySelector(".giencoder-select-popup")).visibility,opacity:getComputedStyle(document.querySelector(".giencoder-select-popup")).opacity,viewBorder:getComputedStyle(document.querySelector(".giencoder-select-view")).borderTopColor,popupBox:(function(b){return [+b.x.toFixed(1),+b.y.toFixed(1),+b.width.toFixed(1),+b.height.toFixed(1)]})(document.querySelector(".giencoder-select-popup").getBoundingClientRect()),optH:(function(b){return +b.height.toFixed(1)})(document.querySelector(".giencoder-select-option").getBoundingClientRect())})' > "$O/i2_open.txt" 2>&1

# ---------- C. 点选第 3 项：文本同步 / selected 互斥 / 面板收起 ----------
"$AB" click "$PICK" >/dev/null 2>&1
"$AB" wait 500 >/dev/null 2>&1
"$AB" eval 'JSON.stringify({text:document.querySelector(".giencoder-select-view-text").textContent,selTexts:[].slice.call(document.querySelectorAll(".giencoder-select")).map(function(s){var o=s.querySelector(".giencoder-select-option-selected");return o?o.textContent:null}),openCls:document.querySelector(".giencoder-select-popup").classList.contains("giencoder-popup-open"),expanded:document.querySelector(".giencoder-select-view").getAttribute("aria-expanded")})' > "$O/i3_pick.txt" 2>&1

# ---------- D. 键盘：focus → ArrowDown ×2 → Enter ----------
"$AB" focus ".giencoder-select-view" >/dev/null 2>&1
"$AB" press "ArrowDown" >/dev/null 2>&1
"$AB" wait 150 >/dev/null 2>&1
"$AB" eval 'JSON.stringify({afterDown1:{open:document.querySelector(".giencoder-select-popup").classList.contains("giencoder-popup-open"),active:document.activeElement.textContent,activeCls:document.activeElement.className,ae:document.querySelector(".giencoder-select-view").getAttribute("aria-activedescendant"),focusBg:getComputedStyle(document.activeElement).backgroundColor}})' > "$O/i4a_kb.txt" 2>&1
"$AB" press "ArrowDown" >/dev/null 2>&1
"$AB" wait 150 >/dev/null 2>&1
"$AB" eval 'JSON.stringify({afterDown2:{active:document.activeElement.textContent}})' > "$O/i4b_kb.txt" 2>&1
"$AB" press "Enter" >/dev/null 2>&1
"$AB" wait 400 >/dev/null 2>&1
"$AB" eval 'JSON.stringify({afterEnter:{text:document.querySelector(".giencoder-select-view-text").textContent,open:document.querySelector(".giencoder-select-popup").classList.contains("giencoder-popup-open")}})' > "$O/i4c_kb.txt" 2>&1

# ---------- E. Esc 关闭 ----------
"$AB" click ".giencoder-select-view" >/dev/null 2>&1
"$AB" wait 350 >/dev/null 2>&1
"$AB" press "Escape" >/dev/null 2>&1
"$AB" wait 350 >/dev/null 2>&1
"$AB" eval 'JSON.stringify({open:document.querySelector(".giencoder-select-popup").classList.contains("giencoder-popup-open"),ae:document.querySelector(".giencoder-select-view").getAttribute("aria-expanded")})' > "$O/i5_esc.txt" 2>&1

# ---------- F. 点外部关闭 ----------
"$AB" click ".giencoder-select-view" >/dev/null 2>&1
"$AB" wait 350 >/dev/null 2>&1
"$AB" click "main" >/dev/null 2>&1
"$AB" wait 350 >/dev/null 2>&1
"$AB" eval 'JSON.stringify({open:document.querySelector(".giencoder-select-popup").classList.contains("giencoder-popup-open"),ae:document.querySelector(".giencoder-select-view").getAttribute("aria-expanded")})' > "$O/i6_outside.txt" 2>&1

# ---------- G. 一次只开一个 ----------
"$AB" eval 'JSON.stringify((function(){var s=document.querySelectorAll(".giencoder-select");s[0].querySelector(".giencoder-select-view").click();s[1].querySelector(".giencoder-select-view").click();return {s0:s[0].querySelector(".giencoder-select-popup").classList.contains("giencoder-popup-open"),s1:s[1].querySelector(".giencoder-select-popup").classList.contains("giencoder-popup-open")};})())' > "$O/i7_single.txt" 2>&1
"$AB" wait 300 >/dev/null 2>&1
"$AB" eval 'JSON.stringify({note:"closeAll"})' >/dev/null 2>&1

# ---------- H. 拖拽尝试（把手坐标 mousedown + mousemove）→ aside 宽度必须不变 ----------
"$AB" eval 'JSON.stringify((function(){var a=document.querySelector("aside"),sep=document.querySelector("[role=\"separator\"][aria-label=\"调整菜单宽度\"]");var w0=a.getBoundingClientRect().width;if(sep){sep.dispatchEvent(new MouseEvent("mousedown",{bubbles:true,clientX:265,clientY:500}));document.dispatchEvent(new MouseEvent("mousemove",{bubbles:true,clientX:500,clientY:500}));document.dispatchEvent(new MouseEvent("mouseup",{bubbles:true,clientX:500,clientY:500}));}return {wBefore:w0,wAfter:a.getBoundingClientRect().width,inlineW:a.style.width,sepDisplay:sep?getComputedStyle(sep).display:"none"};})())' > "$O/i8_drag.txt" 2>&1

echo "ALL STEPS DONE"
ls "$O"/i*.txt | wc -l

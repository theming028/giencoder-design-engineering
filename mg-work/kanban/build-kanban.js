const fs = require('fs');
const path = require('path');

const BASE = 'C:\\Users\\Administrator\\Documents\\Qoder\\2026-09-24\\0bfb1ccc\\giencoder-design-engineering';
const KB = path.join(BASE, 'mg-work', 'kanban');
const TEMPLATE = path.join(KB, 'kanban-template.html');
const OUT = path.join(BASE, 'pages', 'kanban.html');

// Monochrome icons: replace fill="#hex" -> currentColor. Raw icons keep verbatim colors.
const RAW = new Set(['svg_186b82ab']);

// Build basename -> first full path map across all nXX/asset/icons
const iconMap = {};
for (const d of fs.readdirSync(KB)) {
  if (!/^n\d\d$/.test(d)) continue;
  const dir = path.join(KB, d, 'asset', 'icons');
  if (!fs.existsSync(dir)) continue;
  for (const f of fs.readdirSync(dir)) {
    if (f.endsWith('.svg') && !iconMap[f]) iconMap[f] = path.join(dir, f);
  }
}

let uid = 0;
function processSvg(file, useCurrentColor) {
  let s = fs.readFileSync(iconMap[file], 'utf8').trim();
  if (useCurrentColor) s = s.replace(/fill="#[0-9A-Fa-f]{6}"/g, 'fill="currentColor"');
  // unique-ify ids (clipPath/filter references) per insertion
  const n = ++uid;
  s = s.replace(/id="([^"]+)"/g, (_m, id) => 'id="' + id + '_u' + n + '"');
  s = s.replace(/url\(#([^)]+)\)/g, (_m, id) => 'url(#' + id + '_u' + n + ')');
  return s;
}

let html = fs.readFileSync(TEMPLATE, 'utf8');
let missing = [];
html = html.replace(/\{\{(ICONRAW|ICON):([a-z0-9_]+)\}\}/g, (_m, kind, name) => {
  const file = name + '.svg';
  if (!iconMap[file]) { missing.push(file); return '<!-- missing ' + file + ' -->'; }
  return processSvg(file, kind === 'ICON');
});

if (missing.length) { console.error('MISSING SVGs:', missing.join(', ')); }
fs.writeFileSync(OUT, html, 'utf8');
console.log('Wrote ' + OUT + ' (' + Buffer.byteLength(html) + 'B), ' + uid + ' svg instances inlined, missing=' + missing.length);

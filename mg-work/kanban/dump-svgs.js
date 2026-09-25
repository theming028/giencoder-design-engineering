const fs = require('fs');
const path = require('path');
const base = 'C:\\Users\\Administrator\\Documents\\Qoder\\2026-09-24\\0bfb1ccc\\giencoder-design-engineering\\mg-work\\kanban';
const dirs = fs.readdirSync(base).filter(d => /^n\d\d$/.test(d));
const seen = new Set();
let out = '';
for (const d of dirs.sort()) {
  const iconDir = path.join(base, d, 'asset', 'icons');
  if (!fs.existsSync(iconDir)) continue;
  for (const f of fs.readdirSync(iconDir).sort()) {
    if (seen.has(f)) continue;
    seen.add(f);
    const p = path.join(iconDir, f);
    out += '\n===== ' + f + ' (' + fs.statSync(p).size + 'B) =====\n';
    out += fs.readFileSync(p, 'utf8').trim() + '\n';
  }
}
fs.writeFileSync(path.join(base, 'all-svgs.txt'), out, 'utf8');
console.log('wrote all-svgs.txt, unique svgs:', seen.size);

// Save crop dataURLs (passed via JSON file) to png files.
const fs = require('fs');
const inp = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
for (const k in inp) {
  const b64 = inp[k].split(',')[1];
  fs.writeFileSync('mg-work/kanban/root/crop-' + k + '.png', Buffer.from(b64, 'base64'));
  console.log('crop-' + k + '.png');
}

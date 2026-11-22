// chụp từng slide 1280x720 -> out/png/uN/NN.png ; báo slide bị tràn
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const units = process.argv.slice(2).length ? process.argv.slice(2) : Array.from({ length: 15 }, (_, i) => String(i + 1));
const dsf = Number(process.env.DSF || 1.5);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: dsf });
  await p.goto('file://' + path.join(__dirname, 'render', 'index.html')); await p.waitForTimeout(300);
  const over = [];
  for (const u of units) {
    const key = 'avcn2-u' + u, dir = path.join(__dirname, 'out', 'png', 'u' + u); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const n = await p.evaluate(k => AVS_DECKS[k].length, key);
    for (let i = 0; i < n; i++) {
      const r = await p.evaluate(([k, i]) => show(k, i), [key, i]);
      if (r.h > 722) over.push(`u${u} #${i + 1} cao ${r.h}`);
      await p.locator('#f').screenshot({ path: path.join(dir, String(i + 1).padStart(2, '0') + '.png') });
    }
    console.log('u' + u, n, 'slide');
  }
  console.log('TRÀN:', over.length ? over.join(', ') : 'không');
  await b.close();
})();

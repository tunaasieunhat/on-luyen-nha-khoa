// node shot.js <key> <dir>  : chụp mọi slide (bản web) 1280x720
const { chromium } = require('playwright'); const [, , K, OUT] = process.argv;
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto('file:///home/claude/dl/sl/render/index.html'); await p.waitForTimeout(150);
  const n = await p.evaluate(k => DLS_DECKS[k].length, K);
  for (let i = 0; i < n; i++) { const r = await p.evaluate(([k, i]) => show(k, i), [K, i]); await p.waitForTimeout(60);
    await p.screenshot({ path: `${OUT}/${String(i + 1).padStart(2, '0')}.png`, clip: { x: 0, y: 0, width: 1280, height: 720 } }); if (r.shrink) console.log(i + 1, 'shrink', r.shrink, r.h); }
  await b.close(); })();

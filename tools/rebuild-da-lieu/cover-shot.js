const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 600, height: 850 }, deviceScaleFactor: 2 });
  await p.goto('file:///home/claude/dl/cover/cover.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: '/home/claude/dl/cover/cover2x.png' }); await b.close(); })();

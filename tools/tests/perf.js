const { chromium } = require('playwright');
const MODE = process.argv[2] || 'base';
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2.75 });
  const p = await ctx.newPage();
  await ctx.route(/fonts\.(googleapis|gstatic)\.com|onesignal/, r => r.abort());
  const cdp = await ctx.newCDPSession(p);
  await p.goto('http://localhost:8792/on-luyen-nha-khoa/index.html'); await p.waitForTimeout(1500);
  await p.click('#intro-go'); await p.waitForTimeout(600); if (await p.isVisible('#v1-ok')) await p.click('#v1-ok');
  await p.fill('#in-name', 'Lan'); await p.fill('#in-school', 'DNC'); await p.click('#start-form button[type=submit]'); await p.waitForTimeout(1200);
  if (await p.isVisible('#go-learn')) await p.click('#go-learn');
  await p.click('#go-theory'); await p.waitForTimeout(600); await p.click('[data-thsub="avcn2"]'); await p.waitForTimeout(400);
  if (MODE === 'noanim') await p.addStyleTag({ content: '#bg *{animation:none!important} #bg .bg-snow{display:none}' });
  if (MODE === 'nobg') await p.addStyleTag({ content: '#bg{display:none!important}' });
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 6 });
  const run = async (label) => {
    await p.evaluate(() => { window.scrollTo(0, 0); window.__f = []; let last = performance.now(); const tick = t => { window.__f.push(t - last); last = t; if (window.__go) requestAnimationFrame(tick); }; window.__go = 1; requestAnimationFrame(tick); });
    for (let i = 0; i < 25; i++) { await p.mouse.wheel(0, 180); await p.waitForTimeout(60); }
    const f = await p.evaluate(() => { window.__go = 0; return window.__f.slice(3); });
    const s = f.slice().sort((a, b) => a - b), avg = f.reduce((a, b) => a + b, 0) / f.length;
    console.log(MODE, label, 'frames', f.length, 'avg', avg.toFixed(1), 'p90', s[Math.floor(s.length * .9)].toFixed(1), 'max', s[s.length - 1].toFixed(1), 'jank>50', f.filter(x => x > 50).length);
  };
  await run('list');
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 1 });
  await p.click('#th-list [data-thread="avcn2-u5"]'); await p.waitForTimeout(800);
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 6 });
  await run('lesson');
  console.log('dom', await p.evaluate(() => document.getElementsByTagName('*').length), 'bg', await p.evaluate(() => document.querySelectorAll('#bg *').length));
  await b.close();
})();

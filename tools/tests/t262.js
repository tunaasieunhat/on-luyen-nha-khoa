const { chromium } = require('playwright');
const SHOT = '/tmp/claude-0/-home-claude/1c724e9b-fcd3-53c8-b63a-63ce5b775ad4/scratchpad/';
(async () => {
  const b = await chromium.launch();
  for (const [name, vp] of [['m', { width: 390, height: 844, isMobile: true, hasTouch: true }], ['d', { width: 1360, height: 900 }]]) {
    const p = await b.newPage({ viewport: { width: vp.width, height: vp.height }, isMobile: !!vp.isMobile, hasTouch: !!vp.hasTouch });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.route(/fonts\.(googleapis|gstatic)\.com|onesignal|github/, r => r.abort());
    await p.goto('http://localhost:8792/index.html'); await p.waitForTimeout(1200);
    await p.click('#intro-go'); await p.waitForTimeout(600); if (await p.isVisible('#v1-ok')) { console.log('v1', (await p.textContent('#v1-title'))); if (name==='m') await p.screenshot({ path: SHOT + 'v1.png' }); await p.click('#v1-ok'); }
    await p.fill('#in-name', 'Lan'); await p.fill('#in-school', 'DNC'); await p.click('#start-form button[type=submit]'); await p.waitForTimeout(1200);
    if (await p.isVisible('#go-learn')) await p.click('#go-learn');
    await p.waitForTimeout(1200); await p.click("#go-theory"); await p.waitForTimeout(1200); await p.click('[data-thsub="vat-lieu-nha-khoa"]'); await p.waitForTimeout(300);
    console.log('vd buttons', await p.locator('[data-thvd]').count());
    await p.click('[data-thvd="vlnk-bai-1"]'); await p.waitForTimeout(1500);
    console.log('tab', await p.evaluate(() => [document.getElementById('th-vd').hidden, document.getElementById('th-tab-vd').hidden, document.getElementById('th-tab-vd-n').textContent, document.getElementById('vd-meta').textContent]));
    await p.click('[data-vdto="3"]'); await p.waitForTimeout(2500);
    console.log('t', JSON.stringify(await p.evaluate(() => { const v = document.getElementById('vd-video'); return [v.currentTime, v.paused, v.readyState, v.textTracks[0] && v.textTracks[0].mode, v.textTracks[0] && v.textTracks[0].cues && v.textTracks[0].cues.length, document.getElementById('vd-now').textContent, v.error && v.error.code]; })));
    await p.evaluate(() => document.getElementById('vd-video').pause());
    await p.locator('#th-vd').scrollIntoViewIfNeeded();
    await p.screenshot({ path: SHOT + `vd-${name}.png`, fullPage: false });
    await p.click('[data-vdrate="1.25"]'); await p.click('#vd-cc');
    console.log('rate/cc', await p.evaluate(() => { const v = document.getElementById('vd-video'); return [v.playbackRate, v.textTracks[0].mode]; }));
    await p.click('[data-thtab="sum"]'); console.log('paused after tab', await p.evaluate(() => document.getElementById('vd-video').paused));
    console.log('errors', errs); await p.close();
  }
  await b.close();
})();

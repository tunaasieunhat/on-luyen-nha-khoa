const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(() => { window.__said = []; window.AndroidApp = { saveFile: () => 'saved', appVersion: () => '2.6.1', speak: (t, r) => { window.__said.push([t, r]); return true; } }; });
  await p.route(/fonts\.(googleapis|gstatic)\.com|onesignal|github/, r => r.abort());
  await p.goto('http://localhost:8791/on-luyen-nha-khoa/android/app/src/main/assets/www/index.html'); await p.waitForTimeout(1200);
  await p.click('#intro-go'); await p.waitForTimeout(600); if (await p.isVisible('#v1-ok')) { console.log('v1', (await p.textContent('#v1-title'))); await p.click('#v1-ok'); }
  await p.fill('#in-name', 'Lan'); await p.fill('#in-school', 'DNC'); await p.click('#start-form button[type=submit]'); await p.waitForTimeout(1200);
  if (await p.isVisible('#go-learn')) await p.click('#go-learn');
  await p.click('#go-theory'); await p.waitForTimeout(600); await p.click('[data-thsub="avcn2"]');
  await p.click('#th-list [data-vt="2"]'); await p.waitForTimeout(600);
  console.log('said', JSON.stringify(await p.evaluate(() => window.__said)));
  console.log('back', await p.evaluate(() => window.__androidBack && window.__androidBack()), 'hidden', await p.evaluate(() => document.getElementById('vt').hidden));
  console.log('errors', errs); await b.close();
})();

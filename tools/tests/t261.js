const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const vp of [{ width: 390, height: 844, m: 1, n: 'm' }, { width: 1280, height: 860, n: 'd' }]) {
    const ctx = await b.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: !!vp.m, hasTouch: !!vp.m });
    const p = await ctx.newPage(); const errs = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('c:' + m.text()); });
    await ctx.route(/fonts\.(googleapis|gstatic)\.com|onesignal/, r => r.abort());
    await p.addInitScript(() => { window.__said = []; const S = window.speechSynthesis; if (S) { S.speak = u => window.__said.push(u.text); } });
    await p.goto('http://localhost:8791/on-luyen-nha-khoa/index.html'); await p.waitForTimeout(1500);
    await p.click('#intro-go'); await p.waitForTimeout(800);
    if (await p.isVisible('#v1-ok')) { await p.screenshot({ path: `shots/v1-${vp.n}.png` }); await p.click('#v1-ok'); }
    await p.fill('#in-name', 'Lan'); await p.fill('#in-school', 'DNC'); await p.click('#start-form button[type=submit]'); await p.waitForTimeout(1500);
    if (await p.isVisible('#go-learn')) { await p.click('#go-learn'); await p.waitForTimeout(300); }
    await p.click('#go-theory'); await p.waitForTimeout(1000);
    await p.click('[data-thsub="avcn2"]'); await p.waitForTimeout(500);
    console.log(vp.n, 'list', await p.$$eval('#th-list .lesson', l => l.slice(0, 4).map(x => x.querySelector('.lesson-no').textContent + '|' + x.querySelector('strong').textContent)));
    console.log(vp.n, 'vt btns', await p.$$eval('#th-list [data-vt]', l => l.length), 'book', await p.textContent('#th-book .tb-info p'));
    await p.screenshot({ path: `shots/list-${vp.n}.png`, fullPage: false });
    await p.click('#th-list [data-thread="avcn2-u1"]'); await p.waitForTimeout(800);
    console.log(vp.n, 'cards', await p.$$eval('#th-body .vw', l => l.length), 'toc', await p.$$eval('#th-toc-list a', l => l.map(a => a.textContent).join(' / ')));
    await p.locator('#th-body .vw').first().scrollIntoViewIfNeeded(); await p.screenshot({ path: `shots/card-${vp.n}.png` });
    await p.click('#th-body .vw .vw-say >> nth=0'); await p.waitForTimeout(200);
    console.log(vp.n, 'said', await p.evaluate(() => window.__said));
    await p.click('#th-body [data-vt="1"]'); await p.waitForTimeout(500);
    await p.screenshot({ path: `shots/vt0-${vp.n}.png` });
    let n = 0;
    for (let i = 0; i < 30; i++) {
      if (await p.isVisible('.vt-end')) break;
      const ans = await p.evaluate(() => __vt.VT.run.q[__vt.VT.run.i].ans);
      const pick = (i % 4 === 3) ? (ans + 1) % 4 : ans;
      await p.click(`#vt [data-vtopt="${pick}"]`); await p.waitForTimeout(80);
      if (i === 1) await p.screenshot({ path: `shots/vt1-${vp.n}.png` });
      await p.click('#vt-next'); await p.waitForTimeout(80); n++;
    }
    await p.screenshot({ path: `shots/vtend-${vp.n}.png` });
    console.log(vp.n, 'answered', n, 'end', await p.textContent('.vt-score'), JSON.stringify(await p.evaluate(() => __vt.stats(1))));
    await p.keyboard.press('Escape'); await p.waitForTimeout(300);
    console.log(vp.n, 'closed', await p.evaluate(() => document.getElementById('vt').hidden), 'prog', await p.textContent('#th-body .vt-prog'));
    // second session -> question types should advance
    await p.click('#th-body [data-vt="1"]'); await p.waitForTimeout(300);
    console.log(vp.n, 'types', await p.evaluate(() => __vt.VT.run.q.map(q => q.type).join('')));
    await p.keyboard.press('Escape');
    for (const id of ['avcn2-u0', 'avcn2-ugoc', 'avcn2-u11']) {
      await p.evaluate(id => __vt.open(id), id); await p.waitForTimeout(300);
      console.log(vp.n, id, await p.textContent('#th-title'), await p.$$eval('#th-toc-list a', l => l.length));
    }
    await p.evaluate(() => __vt.open('avcn2-u0')); await p.waitForTimeout(300); await p.screenshot({ path: `shots/u0-${vp.n}.png`, fullPage: true });
    const r = await p.evaluate(async () => { const out = {}; for (const f of ['pdf/AVCN2-Bang-tu-tom-tat.pdf', 'pdf/AVCN2-U00-Bat-dau-tu-day.pdf', 'pdf/GiaoTrinh-Anh-van-chuyen-nganh-2.pdf']) out[f] = (await fetch(f)).status; return out; });
    console.log(vp.n, 'pdf', JSON.stringify(r), 'errors', errs);
    await ctx.close();
  }
  await b.close();
})();

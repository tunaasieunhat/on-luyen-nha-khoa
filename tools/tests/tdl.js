// Kiểm thử bản dựng lại: môn Da Liễu (giáo trình, slide), không còn sơ đồ tư duy / video. Máy chủ: rserve.py <repo> 8796
const { chromium } = require('playwright');
const SHOT = process.env.SHOT || '/tmp/sh/';
(async () => {
  const b = await chromium.launch();
  for (const [name, vp] of [['m', { width: 390, height: 844, mob: true }], ['d', { width: 1360, height: 900 }]]) {
    const p = await b.newPage({ viewport: { width: vp.width, height: vp.height }, isMobile: !!vp.mob, hasTouch: !!vp.mob });
    const errs = [], bad = []; p.on('pageerror', e => errs.push(e.message)); p.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });
    await p.route(/fonts\.(googleapis|gstatic)\.com|onesignal|github/, r => r.abort());
    await p.goto('http://localhost:8796/index.html'); await p.waitForTimeout(1200);
    await p.click('#intro-go'); await p.waitForTimeout(600); if (await p.isVisible('#v1-ok')) await p.click('#v1-ok');
    await p.fill('#in-name', 'Lan'); await p.fill('#in-school', 'DNC'); await p.click('#start-form button[type=submit]'); await p.waitForTimeout(1500);
    if (await p.isVisible('#go-learn')) await p.click('#go-learn'); await p.waitForTimeout(1000);
    await p.click('#go-theory'); await p.waitForTimeout(1000);
    console.log(name, 'môn:', await p.$$eval('#th-subjects [data-thsub]', a => a.map(x => x.dataset.thsub + ' ' + x.innerText.replace(/\n/g, ' | '))));
    console.log(name, 'nút sơ đồ/video còn lại:', await p.locator('[data-thmm],[data-thvd]').count());
    await p.click('[data-thsub="vat-lieu-nha-khoa"]'); await p.waitForTimeout(300);
    console.log(name, 'VLNK nút sơ đồ/video:', await p.locator('[data-thmm],[data-thvd]').count(), 'slide:', await p.locator('[data-thsl]').count());
    const dk = await p.$eval('#th-subjects', el => [...el.querySelectorAll('[data-thsub]')].map(x => x.dataset.thsub).find(k => /da-li/.test(k)));
    await p.click(`[data-thsub="${dk}"]`); await p.waitForTimeout(500);
    console.log(name, 'Da Liễu bài:', await p.locator('#th-list li.lesson.has').count(), 'slide:', await p.locator('[data-thsl^="dl-bai-"]').count(), 'pdf:', await p.locator('[data-thpdf^="dl-bai-"]').count());
    await p.screenshot({ path: SHOT + `dl-list-${name}.png`, fullPage: true });
    await p.click('#th-list [data-thread="dl-bai-10"]'); await p.waitForTimeout(1200);
    console.log(name, 'bài 10:', await p.textContent('#th-title'), '| mục:', await p.locator('#th-toc-list li').count(), '| tab mm ẩn', await p.$eval('#th-tab-mm', e => e.hidden), 'vd ẩn', await p.$eval('#th-tab-vd', e => e.hidden), 'sl hiện', !(await p.$eval('#th-tab-sl', e => e.hidden)));
    await p.evaluate(() => document.querySelectorAll('#th-body img').forEach(i => { i.loading = 'eager'; i.scrollIntoView(); })); await p.waitForTimeout(1500);
    console.log(name, 'hình:', await p.$$eval('#th-body img', a => a.map(i => i.naturalWidth > 0).join(',')));
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.click('[data-thtab="sl"]'); await p.waitForTimeout(600);
    console.log(name, 'slide:', await p.textContent('#sl-count'), await p.textContent('#th-tab-sl-n'), 'thumbs', await p.locator('#sl-thumbs button.tx').count());
    await p.click('[data-slto="5"]'); await p.waitForTimeout(800); await p.locator('#sl-stage').scrollIntoViewIfNeeded();
    console.log(name, 'hình slide:', await p.$$eval('#sl-html img', a => a.map(i => i.complete && i.naturalWidth)));
    await p.screenshot({ path: SHOT + `dl-slide-${name}.png` });
    const qi = await p.evaluate(() => __dls.decks['dl-bai-10'].findIndex(s => s.k === 'quiz'));
    await p.click(`[data-slto="${qi}"]`); await p.waitForTimeout(300);
    const ans = await p.evaluate(i => __dls.decks['dl-bai-10'][i].q.map(q => q.a), qi);
    await p.click(`#sl-html [data-avsq="0"] [data-avso="${ans[0]}"]`); await p.click(`#sl-html [data-avsq="1"] [data-avso="${(ans[1] + 1) % 4}"]`); await p.click(`#sl-html [data-avsq="2"] [data-avso="${ans[2]}"]`);
    console.log(name, 'điểm:', await p.textContent('#sl-html .score'));
    await p.locator('#sl-stage').scrollIntoViewIfNeeded(); await p.screenshot({ path: SHOT + `dl-quiz-${name}.png` });
    await p.keyboard.press('ArrowRight'); console.log(name, 'sau →', await p.textContent('#sl-count'));
    // AVCN2 vẫn chạy
    console.log(name, 'AVCN2 slide 1:', await p.evaluate(() => { const d = __avs.decks['avcn2-u1']; return d && d.length; }));
    // file tải
    const files = await p.evaluate(async () => { const out = []; for (const u of ['pdf/DL-Bai-10-Giang-Mai.pdf', 'pdf/GiaoTrinh-Da-lieu.pdf', 'slides/da-lieu/DL-Slide-Bai-10-Giang-Mai.pptx', 'slides/da-lieu/DL-Slide-Bai-10-Giang-Mai-BanIn.pdf']) { const r = await fetch(u, { method: 'HEAD' }); out.push(r.status); } return out; });
    console.log(name, 'file:', files);
    console.log(name, 'lỗi', errs, bad.filter(x => !/fonts|onesignal|github/.test(x))); await p.close();
  }
  await b.close();
})();

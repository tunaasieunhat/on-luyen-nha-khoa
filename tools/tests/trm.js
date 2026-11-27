// Kiểm thử bản dựng lại: không còn Mô phỏng / Sơ đồ / Video, Flashcard tạm khoá, các phần khác vẫn chạy. Máy chủ: rserve.py <repo> 8796
const { chromium } = require('playwright');
const SHOT = process.env.SHOT || '/tmp/sh/';
(async () => {
  const b = await chromium.launch();
  for (const [name, vp] of [['m', { width: 390, height: 844, mob: true }], ['d', { width: 1360, height: 900 }]]) {
    const p = await b.newPage({ viewport: { width: vp.width, height: vp.height }, isMobile: !!vp.mob, hasTouch: !!vp.mob });
    const learn = async () => { if (await p.isVisible('#go-learn')) await p.click('#go-learn'); await p.waitForTimeout(300); };
    const errs = [], bad = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); }); p.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });
    await p.route(/fonts\.(googleapis|gstatic)\.com|onesignal|github/, r => r.abort());
    await p.goto('http://localhost:8796/index.html'); await p.waitForTimeout(1200);
    await p.click('#intro-go'); await p.waitForTimeout(600); if (await p.isVisible('#v1-ok')) await p.click('#v1-ok');
    await p.fill('#in-name', 'Lan'); await p.fill('#in-school', 'DNC'); await p.click('#start-form button[type=submit]'); await p.waitForTimeout(1500);
    console.log(name, 'menu chính:', await p.$$eval('#menu-main button', a => a.map(x => x.id)), '| có scr-sim:', await p.locator('#scr-sim').count());
    await p.screenshot({ path: SHOT + `rm-lobby-${name}.png` });
    await p.click('#go-learn'); await p.waitForTimeout(500);
    console.log(name, 'menu ôn luyện:', await p.$$eval('#menu-learn button.menu-btn', a => a.map(x => x.id + (x.classList.contains('locked') ? '(khoá)' : ''))));
    await p.screenshot({ path: SHOT + `rm-learn-${name}.png` });
    await p.click('#go-flash', { force: true }); await p.waitForTimeout(800);
    console.log(name, 'bấm flashcard → màn:', await p.evaluate(() => document.body.dataset.scr), '| toast:', (await p.textContent('#toast').catch(() => '')).trim().slice(0, 60));
    // cài đặt
    if (await p.isVisible('#learn-back')) await p.click('#learn-back'); await p.waitForTimeout(300);
    await p.click('#go-settings'); await p.waitForTimeout(500);
    console.log(name, 'cài đặt:', await p.$$eval('#set-body h3', a => a.map(x => x.textContent.trim())));
    await p.keyboard.press('Escape'); await p.waitForTimeout(300);
    // làm bài
    await learn(); await p.click('#go-quiz'); await p.waitForTimeout(1800);
    console.log(name, 'màn làm bài:', await p.evaluate(() => document.body.dataset.scr));
    await p.click('[data-back]:visible'); await p.waitForTimeout(600);
    // phòng thi
    await learn(); await p.click('#go-exam'); await p.waitForTimeout(1800);
    console.log(name, 'phòng thi:', await p.evaluate(() => document.body.dataset.scr));
    await p.click('[data-back]:visible'); await p.waitForTimeout(600);
    // lý thuyết VLNK
    await learn(); await p.click('#go-theory'); await p.waitForTimeout(1500);
    await p.click('[data-thsub="vat-lieu-nha-khoa"]'); await p.waitForTimeout(300);
    console.log(name, 'VLNK nút:', await p.$$eval('#th-list li.has:first-child .lesson-act button', a => a.map(x => x.textContent.trim())));
    await p.click('#th-list [data-thsl="vlnk-bai-1"]'); await p.waitForTimeout(800);
    console.log(name, 'tab:', await p.$$eval('#th-read [data-thtab]', a => a.filter(x => !x.hidden).map(x => x.textContent.trim())), '| slide:', await p.textContent('#sl-count'));
    await p.click('[data-thtab="sum"]'); await p.waitForTimeout(300); await p.click('#th-close'); await p.waitForTimeout(400);
    console.log(name, 'lỗi', errs, bad.filter(x => !/fonts|onesignal|github/.test(x))); await p.close();
  }
  await b.close();
})();

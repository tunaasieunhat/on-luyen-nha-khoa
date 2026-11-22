const { chromium } = require('playwright');
const SHOT = '/tmp/claude-0/-home-claude/1c724e9b-fcd3-53c8-b63a-63ce5b775ad4/scratchpad/';
(async () => {
  const b = await chromium.launch();
  for (const [name, vp] of [['m', { width: 390, height: 844, mob: true }], ['d', { width: 1360, height: 900 }]]) {
    const p = await b.newPage({ viewport: { width: vp.width, height: vp.height }, isMobile: !!vp.mob, hasTouch: !!vp.mob });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.addInitScript(() => { window.__said = []; Object.defineProperty(window, 'speechSynthesis', { value: { cancel() {}, speak(u) { window.__said.push(u.text); }, getVoices() { return []; }, addEventListener() {} }, configurable: true }); window.SpeechSynthesisUtterance = function (t) { this.text = t; }; });
    await p.route(/fonts\.(googleapis|gstatic)\.com|onesignal|github/, r => r.abort());
    await p.goto('http://localhost:8796/index.html'); await p.waitForTimeout(1200);
    await p.click('#intro-go'); await p.waitForTimeout(600); if (await p.isVisible('#v1-ok')) { if (name === 'm') await p.screenshot({ path: SHOT + 'v263.png' }); await p.click('#v1-ok'); }
    await p.fill('#in-name', 'Lan'); await p.fill('#in-school', 'DNC'); await p.click('#start-form button[type=submit]'); await p.waitForTimeout(1500);
    if (await p.isVisible('#go-learn')) await p.click('#go-learn'); await p.waitForTimeout(1000);
    await p.click('#go-theory'); await p.waitForTimeout(1000); await p.click('[data-thsub="avcn2"]'); await p.waitForTimeout(400);
    console.log(name, 'nút slide AVCN2:', await p.locator('[data-thsl^="avcn2-"]').count());
    await p.click('[data-thsl="avcn2-u1"]'); await p.waitForTimeout(800);
    console.log(name, 'tab', await p.evaluate(() => [document.getElementById('th-sl').hidden, document.getElementById('th-tab-sl-n').textContent, document.getElementById('sl-count').textContent, document.getElementById('sl-stage').className, document.querySelectorAll('#sl-thumbs button.tx').length]));
    // tới slide từ đầu tiên
    await p.click('[data-slto="3"]'); await p.waitForTimeout(300);
    await p.locator('#th-sl').scrollIntoViewIfNeeded();
    await p.click('#sl-html [data-avsay]'); console.log(name, 'đọc:', await p.evaluate(() => window.__said));
    await p.screenshot({ path: SHOT + `avs-word-${name}.png`, fullPage: false });
    // trắc nghiệm nhanh 1
    const qi = await p.evaluate(() => __avs.decks['avcn2-u1'].findIndex(s => s.k === 'quiz'));
    await p.click(`[data-slto="${qi}"]`); await p.waitForTimeout(300);
    const ans = await p.evaluate(i => __avs.decks['avcn2-u1'][i].q.map(q => q.a), qi);
    await p.click(`#sl-html [data-avsq="0"] [data-avso="${ans[0]}"]`);
    await p.click(`#sl-html [data-avsq="1"] [data-avso="${(ans[1] + 1) % 4}"]`);
    await p.click(`#sl-html [data-avsq="2"] [data-avso="${ans[2]}"]`);
    console.log(name, 'điểm:', await p.textContent('#sl-html .score'), '| slide còn ở', await p.textContent('#sl-count'));
    await p.locator('#sl-stage').scrollIntoViewIfNeeded();
    await p.screenshot({ path: SHOT + `avs-quiz-${name}.png`, fullPage: false });
    // vuốt / phím
    await p.keyboard.press('ArrowRight'); console.log(name, 'sau →', await p.textContent('#sl-count'));
    await p.click('#sl-full'); await p.waitForTimeout(300); await p.screenshot({ path: SHOT + `avs-full-${name}.png` }); await p.click('#sl-full');
    // tab VLNK vẫn dùng ảnh
    console.log(name, 'tải pptx url:', await p.evaluate(() => { return document.querySelector('[data-sldl=pptx]') ? 'ok' : 'x'; }));
    console.log(name, 'lỗi', errs); await p.close();
  }
  await b.close();
})();

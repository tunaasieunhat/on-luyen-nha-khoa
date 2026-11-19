// mỗi slide một trang PDF 1280x720 (chữ vector): node slidepdf.js <unit> <ra.pdf>
const { chromium } = require('playwright');
const [, , U, OUT] = process.argv;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto('file:///home/claude/work262s/render/index.html'); await p.waitForTimeout(200);
  await p.evaluate(u => {
    const S = AVS_DECKS['avcn2-u' + u];
    const st = document.createElement('style');
    st.textContent = '@page{size:1280px 720px;margin:0}#f{display:none}.pgx{width:1280px;height:720px;overflow:hidden;container-type:inline-size;background:#FCFEFD;break-after:page;position:relative}.pgx .avs{min-height:720px}';
    document.head.appendChild(st);
    document.body.insertAdjacentHTML('beforeend', S.map((_, i) => `<div class="pgx" data-i="${i}"></div>`).join(''));
    document.querySelectorAll('.pgx').forEach(fr => {
      fr.innerHTML = avsSlide(S, Number(fr.dataset.i), true);
      const a = fr.querySelector('.avs'); let f = parseFloat(getComputedStyle(a).fontSize), t = 0;
      while (a.scrollHeight > 720 && t < 30) { f -= .5; a.style.setProperty('--fs', f + 'px'); t++; }
    });
  }, U);
  await p.emulateMedia({ media: 'screen' });
  await p.pdf({ path: OUT, width: '1280px', height: '720px', printBackground: true, preferCSSPageSize: false });
  await b.close();
})();

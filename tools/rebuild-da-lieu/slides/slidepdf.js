// mỗi slide (bản in, có slide đáp án) một trang 1280x720: node slidepdf.js <key> <ra.pdf>
const { chromium } = require('playwright'); const [, , K, OUT] = process.argv;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto('file:///home/claude/dl/sl/render/index.html'); await p.waitForTimeout(200);
  await p.evaluate(k => {
    const S = DLS_PRINT[k]; const st = document.createElement('style');
    st.textContent = '@page{size:1280px 720px;margin:0}#f{display:none}.pgx{width:1280px;height:720px;overflow:hidden;container-type:inline-size;background:#FFFCFD;break-after:page;position:relative}.pgx .avs{min-height:720px}';
    document.head.appendChild(st);
    document.body.insertAdjacentHTML('beforeend', S.map((_, i) => `<div class="pgx" data-i="${i}"></div>`).join(''));
    document.querySelectorAll('.pgx').forEach(fr => { fr.innerHTML = dlsSlide(S, Number(fr.dataset.i), true);
      fr.querySelectorAll('img').forEach(i => { i.src = i.src.replace('/fig/', '/figj/').replace('.webp', '.jpg'); }); const a = fr.querySelector('.avs'); let f = parseFloat(getComputedStyle(a).fontSize), t = 0;
      while (a.scrollHeight > 720 && t < 30) { f -= .5; a.style.setProperty('--fs', f + 'px'); t++; } });
  }, K);
  await p.waitForLoadState('networkidle');
  await p.emulateMedia({ media: 'screen' });
  await p.pdf({ path: OUT, width: '1280px', height: '720px', printBackground: true });
  await b.close();
})();

// Bản in 4 slide/trang (A4 ngang), chữ dạng vector: node handout2.js <unit> <ra.pdf> "<tiêu đề>"
const { chromium } = require('playwright'); const path = require('path');
const [, , U, OUT, TITLE] = process.argv;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file:///home/claude/work262s/render/index.html'); await p.waitForTimeout(200);
  await p.evaluate(([u, title]) => {
    const S = AVS_DECKS['avcn2-u' + u], n = S.length, pages = Math.ceil(n / 4);
    const st = document.createElement('style');
    st.textContent = `@page{size:A4 landscape;margin:0}body{margin:0;font-family:Carlito,sans-serif;color:#12332E}#f{display:none}
.pg{width:297mm;height:210mm;padding:9mm 11mm 8mm;display:flex;flex-direction:column;gap:4mm;page-break-after:always;box-sizing:border-box}
.hd{display:flex;justify-content:space-between;font-size:9.5pt;border-bottom:.4mm solid #CFE3DC;padding-bottom:2mm}.hd b{color:#0B544C}
.gr{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:5mm 8mm}
.c{display:flex;flex-direction:column;gap:1.2mm;min-height:0}.c span{font-size:8pt;color:#4F6D69}
.cell{width:100%;aspect-ratio:16/9;border:.3mm solid #9DBFB6;border-radius:1.5mm;overflow:hidden;position:relative}
.cell .frame{position:absolute;left:0;top:0;transform-origin:0 0}`;
    document.head.appendChild(st);
    let html = '';
    for (let k = 0; k < pages; k++) {
      html += `<div class="pg"><div class="hd"><b>${title}</b><span>Ôn Luyện Nha Khoa · trang ${k + 1}/${pages}</span></div><div class="gr">`;
      for (let i = k * 4; i < Math.min(n, k * 4 + 4); i++) html += `<div class="c"><div class="cell"><div class="frame" data-i="${i}"></div></div><span>Slide ${i + 1}</span></div>`;
      html += '</div></div>';
    }
    document.body.insertAdjacentHTML('beforeend', html);
    document.querySelectorAll('.frame[data-i]').forEach(fr => {
      fr.innerHTML = avsSlide(S, Number(fr.dataset.i), true);
      const a = fr.querySelector('.avs'); let f = parseFloat(getComputedStyle(a).fontSize), t = 0;
      while (a.scrollHeight > 720 && t < 30) { f -= .5; a.style.setProperty('--fs', f + 'px'); t++; }
      fr.style.transform = `scale(${fr.parentNode.clientWidth / 1280})`;
    });
  }, [U, TITLE]);
  await p.emulateMedia({ media: 'screen' });
  await p.pdf({ path: OUT, preferCSSPageSize: true, printBackground: true }); await b.close();
  console.log(path.basename(OUT));
})();

// Bản in 4 slide/trang (A4 ngang) từ ảnh slide: node handout.js <thư mục png> <ra.pdf> "<tiêu đề>"
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const [, , DIR, OUT, TITLE] = process.argv;
const imgs = fs.readdirSync(DIR).filter(f => f.endsWith('.png')).sort();
const pages = []; for (let i = 0; i < imgs.length; i += 4) pages.push(imgs.slice(i, i + 4));
const esc = s => s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c]);
const html = `<!doctype html><meta charset="utf-8"><style>
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Inter,sans-serif;color:#12332E}
.pg{width:297mm;height:210mm;padding:9mm 11mm 8mm;display:flex;flex-direction:column;gap:4mm;page-break-after:always}
.hd{display:flex;justify-content:space-between;font-size:9.5pt;border-bottom:.4mm solid #CFE3DC;padding-bottom:2mm}.hd b{color:#0B544C}
.gr{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:5mm 8mm}
.c{display:flex;flex-direction:column;gap:1.2mm;min-height:0}.c img{width:100%;aspect-ratio:16/9;border:.3mm solid #9DBFB6;border-radius:1.5mm;display:block}
.c span{font-size:8pt;color:#4F6D69}</style>` + pages.map((p, k) => `<div class="pg"><div class="hd"><b>${esc(TITLE)}</b><span>Ôn Luyện Nha Khoa · trang ${k + 1}/${pages.length}</span></div><div class="gr">` +
  p.map(f => `<div class="c"><img src="file://${path.join(DIR, f)}"><span>Slide ${Number(f.slice(0, 2))}</span></div>`).join('') + '</div></div>').join('');
(async () => {
  const tmp = OUT + '.html'; fs.writeFileSync(tmp, html);
  const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + tmp); await p.waitForTimeout(300);
  await p.pdf({ path: OUT, preferCSSPageSize: true, printBackground: true }); await b.close(); fs.unlinkSync(tmp);
  console.log(path.basename(OUT), pages.length, 'trang');
})();

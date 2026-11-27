// In PDF: node print261.js <jobs.json>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch(); const p = await b.newPage();
  for (const j of jobs) {
    await p.goto('file://' + j.html, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts && document.fonts.ready);
    const foot = j.footer ? `<div style="font-family:Carlito,sans-serif;font-size:7.5px;color:#4F6D69;width:100%;padding:0 14mm;display:flex;justify-content:space-between"><span>${j.footer}</span><span>Trang <span class="pageNumber"></span>/<span class="totalPages"></span></span></div>` : '<span></span>';
    await p.pdf({ path: j.pdf, format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: !!j.footer, headerTemplate: '<span></span>', footerTemplate: foot });
    console.log(path.basename(j.pdf), fs.statSync(j.pdf).size);
  }
  await b.close();
})();

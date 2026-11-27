// Slide Da Liễu -> PowerPoint (sửa được, có ghi chú người trình bày): node pptx_dl.js <thư mục ra> [bài...]
const pptxgen = require('/opt/npm-tools/node_modules/pptxgenjs');
const { applyTheme } = require(process.env.PPTX_SKILL + '/scripts/apply_theme.js');
const fs = require('fs'), path = require('path');
const [, , OUT, ...only] = process.argv;
const D = __dirname, F = JSON.parse(fs.readFileSync(D + '/out/decks.json', 'utf8'));
const META = Object.fromEntries(JSON.parse(fs.readFileSync(D + '/../meta.json', 'utf8')).map(m => [m.b, m]));
const C = { ink: '2B1F24', rose: 'A8455D', roseD: '7A2E41', roseS: 'F7E3E8', line: 'EBCBD2', mut: '7A5C64', lamp: 'E0B23C', lampS: 'FFF4D1', lampD: '7A5600', teal: '3F8C83', tealS: 'EAF5F2', bad: 'CF4C64', badS: 'FCE4E8', ok: '1C8A5C', okS: 'DDF4E9', bg: 'FFFCFD' };
const THEME = { name: 'On Luyen Da Lieu', headFontFace: 'Calibri', bodyFontFace: 'Calibri',
  colors: { dk1: C.ink, lt1: 'FFFFFF', dk2: C.roseD, lt2: C.roseS, accent1: C.rose, accent2: C.teal, accent3: C.lamp, accent4: C.ok, accent5: C.bad, accent6: C.mut, hlink: C.rose, folHlink: C.roseD } };
const plain = s => s.replace(/\*\*/g, '');
function runs(s, base, boldColor) {
  const out = []; s.split(/(\*\*.+?\*\*)/).forEach(p => { if (!p) return; const b = p.startsWith('**'); out.push({ text: b ? p.slice(2, -2) : p, options: { ...base, ...(b ? { bold: true, color: boldColor || C.roseD } : {}) } }); });
  return out;
}
function para(t, ch, pp, last, bc) {
  const r = runs(t, ch, bc);
  r[0].options = { ...r[0].options, ...pp };
  if (!last) r[r.length - 1].options = { ...r[r.length - 1].options, breakLine: true };
  return r;
}
const lines = (txt, w, pt) => Math.max(1, Math.ceil(plain(txt).length / Math.max(8, (w * 72) / (pt * 0.48))));
function deck(key) {
  const S = F[key], b = S[0].b, title = META[b].title;
  const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Ôn Luyện Nha Khoa'; pres.title = `Da Liễu – Bài ${b}. ${title}`;
  pres.theme = { headFontFace: 'Calibri', bodyFontFace: 'Calibri' };
  pres.defineSlideMaster({ title: 'DL', background: { color: C.bg },
    objects: [{ text: { text: 'Da Liễu · Ôn Luyện Nha Khoa', options: { x: 0.4, y: 5.28, w: 6, h: 0.25, fontSize: 8, color: C.mut, fontFace: 'Calibri', margin: 0 } } }],
    slideNumber: { x: 9.05, y: 5.25, w: 0.55, h: 0.28, fontSize: 9, color: C.mut, align: 'right' } });
  pres.addSection({ title: `Bài ${b}` });
  const add = () => pres.addSlide({ masterName: 'DL', sectionTitle: `Bài ${b}` });
  const tag = (sl, t) => sl.addText([{ text: ` BÀI ${b} `, options: { bold: true, color: 'FFFFFF', highlight: C.rose } }, { text: '   ' + t.toUpperCase(), options: { color: C.mut, bold: true } }], { x: 0.4, y: 0.22, w: 9.2, h: 0.3, fontSize: 9, charSpacing: 1, margin: 0, isTextBox: true });
  const head = (sl, h) => sl.addText(h, { x: 0.4, y: 0.58, w: 9.2, h: 0.55, fontSize: 24, bold: true, color: C.roseD, margin: 0, isTextBox: true, valign: 'top' });
  const box = (fill, line) => ({ fill: { color: fill }, line: { color: line, width: 1.25 }, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08 });
  const S2 = []; S.forEach(s => { S2.push(s); if (s.k === 'quiz') S2.push({ ...s, k: 'ans', title: 'Đáp án · ' + s.title.split(': ').pop() }); });
  for (const s of S2) {
    const sl = add();
    if (s.k === 'title') {
      sl.addShape(pres.shapes.OVAL, { x: 7.3, y: -1.2, w: 3.6, h: 3.6, fill: { color: C.roseS }, line: { color: C.roseS } });
      sl.addText('DA LIỄU · ÔN LUYỆN NHA KHOA', { x: 0.5, y: 1.0, w: 7, h: 0.3, fontSize: 10, bold: true, color: C.roseD, charSpacing: 2, margin: 0, isTextBox: true });
      sl.addText([{ text: `Bài ${b}`, options: { fontSize: 80, bold: true, color: C.rose } }, { text: ' /11', options: { fontSize: 26, bold: true, color: C.mut } }], { x: 0.45, y: 1.3, w: 7, h: 1.4, margin: 0, isTextBox: true, valign: 'bottom' });
      sl.addText(title, { x: 0.5, y: 2.85, w: 9, h: 0.9, fontSize: title.length > 30 ? 32 : 38, bold: true, color: C.ink, margin: 0, isTextBox: true, valign: 'top' });
      sl.addText(`${s.n} slide   ·   Khoảng ${s.mins} phút   ·   ${s.nq} câu trắc nghiệm`, { x: 0.5, y: 4.2, w: 9, h: 0.4, fontSize: 13, color: C.lampD, bold: true, margin: 0, isTextBox: true });
      sl.addNotes(`Bài ${b}: ${title}. Giới thiệu mục tiêu bài học, sau đó đi lần lượt các phần. Có ${s.nq} câu trắc nghiệm kèm slide đáp án.`);
    } else if (s.k === 'goal' || s.k === 'recap') {
      tag(sl, s.k === 'goal' ? 'Mục tiêu' : 'Tổng kết'); head(sl, s.k === 'goal' ? 'Học xong bài này, bạn cần' : 'Ghi nhớ cả bài');
      const n = s.items.length, pt = n > 5 ? 15 : 17;
      const r = []; s.items.forEach(([t], k) => r.push(...para(t, { fontSize: pt, color: C.ink }, { bullet: s.k === 'goal' ? { type: 'number' } : true, paraSpaceAfter: 8 }, k === n - 1)));
      sl.addText(r, { x: 0.4, y: 1.3, w: 9.2, h: 3.8, margin: 12, valign: 'top', isTextBox: true, ...(s.k === 'recap' ? box(C.roseS, C.rose) : {}) });
      sl.addNotes(s.items.map(([t]) => '• ' + plain(t)).join('\n'));
    } else if (s.k === 'c') {
      tag(sl, s.sec); head(sl, s.h);
      const W = s.fig ? 5.5 : 9.2, top = 1.25, bottom = 5.1;
      const noteH = s.note ? 0.25 + lines(s.note.lab + s.note.t, W - 0.3, 12) * 0.22 : 0;
      let pt = 16, layout;
      const tblH = (p) => s.rows ? s.rows.reduce((a, r) => a + 0.12 + Math.max(...r.map(c => lines(c, (W / r.length) - 0.1, p))) * p * 1.2 / 72, 0) : 0;
      const itH = (p) => s.items ? s.items.reduce((a, [t, l]) => a + lines(t, W - 0.4 - l * 0.3, p) * p * 1.25 / 72 + 0.07, 0) + 0.1 : 0;
      for (; pt > 10; pt -= 0.5) { layout = { it: itH(pt), tb: tblH(pt - 2) }; if (layout.it + layout.tb + noteH + (s.items && s.rows ? 0.1 : 0) + (s.note ? 0.12 : 0) <= bottom - top) break; }
      let y = top;
      const putItems = () => { if (!s.items) return; const r = [];
        s.items.forEach(([t, l], k) => r.push(...para(t, { fontSize: l ? pt - 1.5 : pt, color: C.ink }, { bullet: l ? { indent: 14 } : true, indentLevel: l, paraSpaceAfter: 5 }, k === s.items.length - 1)));
        sl.addText(r, { x: 0.4, y, w: W, h: layout.it, margin: [2, 4, 2, 4], valign: 'top', isTextBox: true }); y += layout.it + 0.1; };
      const putTable = () => { if (!s.rows) return; const tp = pt - 2;
        sl.addTable(s.rows.map((r, i) => r.map(c => ({ text: runs(c, { fontSize: tp, color: i ? C.ink : C.roseD, bold: !i }), options: { fill: { color: i ? 'FFFFFF' : C.roseS } } }))),
          { x: 0.4, y, w: W, fontSize: tp, border: { type: 'solid', pt: 0.75, color: C.line }, margin: 3, valign: 'top' }); y += layout.tb + 0.1; };
      if (s.tfirst) { putTable(); putItems(); } else { putItems(); putTable(); }
      if (s.note) { const nc = { tip: [C.lampS, C.lamp, C.lampD], why: [C.tealS, C.teal, C.teal], warn: [C.badS, C.bad, C.bad], key: [C.roseS, C.rose, C.roseD] }[s.note.kind];
        sl.addText([{ text: s.note.lab.toUpperCase(), options: { fontSize: 8.5, bold: true, color: nc[2], breakLine: true } }, ...runs(s.note.t, { fontSize: 12, color: C.ink })],
          { x: 0.4, y: Math.min(y + 0.02, bottom - noteH), w: W, h: noteH, margin: 6, valign: 'top', isTextBox: true, ...box(nc[0], nc[1]) }); }
      if (s.fig) { const fw = 3.55, fh0 = fw * s.fig.h / s.fig.w, fh = Math.min(fh0, 3.3), w2 = fh * s.fig.w / s.fig.h;
        sl.addImage({ path: path.join(D, 'figj', s.fig.src.replace('.webp', '.jpg')), x: 6.05 + (fw - w2) / 2, y: 1.3, w: w2, h: fh, altText: s.fig.cap });
        sl.addText(s.fig.cap, { x: 6.05, y: 1.35 + fh, w: fw, h: 0.4, fontSize: 9, color: C.mut, align: 'center', valign: 'top', margin: 0, isTextBox: true }); }
      sl.addNotes([s.h, ...(s.items || []).map(([t, l]) => (l ? '   – ' : '• ') + plain(t)), ...(s.rows || []).map(r => r.map(plain).join(' | ')), s.note ? `${s.note.lab}: ${plain(s.note.t)}` : ''].filter(Boolean).join('\n'));
    } else if (s.k === 'quiz' || s.k === 'ans') {
      tag(sl, s.title);
      const n = s.q.length, gap = 0.12, top = 0.62, h = (4.55 - gap * (n - 1)) / n;
      s.q.forEach((q, k) => { const y = top + k * (h + gap);
        if (s.k === 'quiz') {
          sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.4, y, w: 9.2, h, fill: { color: 'FFFFFF' }, line: { color: C.line, width: 1.25 }, rectRadius: 0.08 });
          sl.addText([{ text: ` ${k + 1} `, options: { bold: true, color: 'FFFFFF', highlight: C.rose, fontSize: 12 } }, { text: '   ' + q.lab.toUpperCase(), options: { fontSize: 8.5, bold: true, color: C.mut, breakLine: true } }, { text: q.p, options: { fontSize: 14, bold: true, color: C.ink } }], { x: 0.55, y: y + 0.05, w: 8.9, h: h * 0.55, margin: 0, valign: 'top', isTextBox: true });
          const oh = Math.min(0.45, h * 0.36), ow = (8.9 - 3 * 0.1) / 4, oy = y + h - oh - 0.07;
          q.o.forEach((o, j) => sl.addText([{ text: 'ABCD'[j] + '  ', options: { bold: true, color: C.rose } }, { text: o, options: { color: C.ink } }], { x: 0.55 + j * (ow + 0.1), y: oy, w: ow, h: oh, fontSize: o.length > 30 ? 9.5 : o.length > 18 ? 10.5 : 12, margin: 4, valign: 'middle', isTextBox: true, ...box(C.bg, C.line) }));
        } else sl.addText([{ text: ` ${k + 1} `, options: { bold: true, color: 'FFFFFF', highlight: C.ok, fontSize: 13 } }, { text: `  ${'ABCD'[q.a]}. ${q.o[q.a]}`, options: { bold: true, color: C.ok, fontSize: 15, breakLine: true } }, { text: q.why, options: { color: C.mut, fontSize: 13 } }], { x: 0.4, y, w: 9.2, h, margin: 4, valign: 'top', isTextBox: true });
      });
      sl.addNotes(s.k === 'quiz' ? 'Cho người học tự chọn đáp án, rồi chuyển slide sau để xem đáp án.' : s.q.map((q, k) => `Câu ${k + 1}: ${'ABCD'[q.a]}. ${q.o[q.a]} – ${q.why}`).join('\n'));
    } else if (s.k === 'end') {
      tag(sl, 'Hoàn thành');
      sl.addText(`Xong Bài ${b} rồi!`, { x: 0.4, y: 0.9, w: 9, h: 0.9, fontSize: 40, bold: true, color: C.roseD, margin: 0, isTextBox: true });
      sl.addText([{ text: 'ÔN CHO NHỚ LÂU', options: { fontSize: 9, bold: true, color: C.roseD, breakLine: true, paraSpaceAfter: 4 } },
        ...['Mở tab Giáo trình của bài này trong app, đọc lại các khung Mẹo nhớ.', 'Ngày mai mở slide Tổng kết, che lại và tự nói các ý chính.', 'Làm lại các slide Kiểm tra nhanh sau 3 ngày.'].map((t, k) => ({ text: t, options: { bullet: { type: 'number' }, fontSize: 14, color: C.ink, breakLine: k < 2, paraSpaceAfter: 6 } }))],
        { x: 0.4, y: 2.0, w: 5.2, h: 2.4, margin: 10, valign: 'top', isTextBox: true, ...box(C.roseS, C.rose) });
      sl.addText(s.next ? [{ text: 'BÀI TIẾP THEO', options: { fontSize: 9, bold: true, color: C.mut, breakLine: true, paraSpaceAfter: 4 } }, { text: `Bài ${b + 1} · ${s.next}`, options: { fontSize: 15, bold: true, color: C.ink } }]
        : [{ text: 'CHÚC MỪNG', options: { fontSize: 9, bold: true, color: C.mut, breakLine: true, paraSpaceAfter: 4 } }, { text: 'Bạn đã học hết 11 bài Da Liễu.', options: { fontSize: 14, color: C.ink } }],
        { x: 5.8, y: 2.0, w: 3.8, h: 2.4, margin: 10, valign: 'top', isTextBox: true, ...box('FFFFFF', C.line) });
      sl.addNotes('Kết thúc bài. Nhắc người học ôn lại bằng tab Giáo trình và slide Tổng kết.');
    }
  }
  return pres;
}
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  for (const k of Object.keys(F).filter(k => !only.length || only.includes(k.replace('dl-bai-', '')))) {
    const b = Number(k.replace('dl-bai-', '')), file = path.join(OUT, META[b].file.replace('DL-Bai-', 'DL-Slide-Bai-').replace('.pdf', '.pptx'));
    await deck(k).writeFile({ fileName: file }); await applyTheme(file, THEME); console.log(path.basename(file));
  }
})();

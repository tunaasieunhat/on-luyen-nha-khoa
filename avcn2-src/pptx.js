// Slide Anh văn chuyên ngành 2 -> PowerPoint (chỉnh sửa được, có ghi chú người trình bày)
// node pptx.js <decks.json> <thư mục ra> [unit...]
const pptxgen = require('pptxgenjs');
const { applyTheme } = require(process.env.PPTX_SKILL + '/scripts/apply_theme.js');
const fs = require('fs'), path = require('path');
const [, , SRC, OUT, ...only] = process.argv;
const F = JSON.parse(fs.readFileSync(SRC, 'utf8'));
const THEME = { name: 'On Luyen AVCN2', headFontFace: 'Calibri', bodyFontFace: 'Calibri',
  colors: { dk1: '12332E', lt1: 'FFFFFF', dk2: '0B544C', lt2: 'F3FAF7', accent1: '127B70', accent2: 'B83A54', accent3: 'FFD66B', accent4: '1C8A5C', accent5: 'C9402F', accent6: '4F6D69', hlink: '127B70', folHlink: '0B544C' } };
const C = { ink: '12332E', teal: '127B70', tealD: '0B544C', tealS: 'D7F1EB', gum: 'B83A54', gumS: 'FCE4E8', gumL: 'F2B8C4', lamp: 'FFD66B', lampS: 'FFF4D1', lampD: '7A5600', mut: '4F6D69', line: 'CFE3DC', ok: '1C8A5C', okS: 'DDF4E9', bg: 'FCFEFD' };
const TITLES = { 1: 'The dentist – Nha sĩ và nghề nha', 2: 'Dental specialties – Các chuyên khoa', 3: 'The dental office – Khu vực phòng khám', 4: 'Dental staff – Nhân sự phòng khám', 5: 'Dental instruments – Dụng cụ nha khoa', 6: 'The mouth – Khoang miệng', 7: 'Tooth anatomy – Cấu tạo răng', 8: 'Types of teeth – Các loại răng', 9: 'Infection control – Kiểm soát lây nhiễm', 10: 'Dental technology – Công nghệ nha khoa', 11: 'Appointments – Lịch hẹn', 12: 'Payment and insurance – Thanh toán, bảo hiểm', 13: 'Patient communication – Giao tiếp bệnh nhân', 14: 'Oral hygiene – Vệ sinh răng miệng', 15: 'Teeth cleaning – Làm sạch răng' };
// cỡ chữ theo độ dài
const fit = (len, steps) => { for (const [max, pt] of steps) if (len <= max) return pt; return steps[steps.length - 1][1]; };
// tô nổi từ khóa trong câu: trả về mảng run
function runs(term, s, base) {
  const re = new RegExp('(^|[^A-Za-z])(' + term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')(?![A-Za-z])', 'gi');
  const out = []; let last = 0, m;
  while ((m = re.exec(s))) {
    const st = m.index + m[1].length;
    if (st > last) out.push({ text: s.slice(last, st), options: { ...base } });
    out.push({ text: m[2], options: { ...base, bold: true, highlight: C.lamp } });
    last = st + m[2].length;
  }
  if (last < s.length) out.push({ text: s.slice(last), options: { ...base } });
  return out;
}
function unitPptx(key) {
  const S = F[key], u = S[0].u;
  const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9';
  pres.author = 'Ôn Luyện Nha Khoa'; pres.title = `Anh văn chuyên ngành 2 – Unit ${u}`;
  pres.theme = { headFontFace: 'Calibri', bodyFontFace: 'Calibri' };
  pres.defineSlideMaster({ title: 'AVCN2', background: { color: C.bg },
    objects: [{ text: { text: 'Anh văn chuyên ngành 2 · Ôn Luyện Nha Khoa', options: { x: 0.4, y: 5.28, w: 6, h: 0.25, fontSize: 8, color: C.mut, fontFace: 'Calibri', margin: 0 } } }],
    slideNumber: { x: 9.05, y: 5.25, w: 0.55, h: 0.28, fontSize: 9, color: C.mut, align: 'right' } });
  pres.addSection({ title: `Unit ${u}` });
  const add = () => pres.addSlide({ masterName: 'AVCN2', sectionTitle: `Unit ${u}` });
  const tag = (sl, txt, right) => {
    sl.addText([{ text: `UNIT ${u}`, options: { bold: true, color: 'FFFFFF', highlight: C.teal } }, { text: '   ' + txt.toUpperCase(), options: { color: C.mut, bold: true } }],
      { x: 0.4, y: 0.22, w: 6.8, h: 0.3, fontSize: 9, charSpacing: 1, margin: 0, isTextBox: true });
    if (right) sl.addText(right, { x: 6.6, y: 0.22, w: 3.0, h: 0.3, fontSize: 9, color: C.mut, align: 'right', margin: 0, isTextBox: true });
  };
  const words = S.filter(s => s.k === 'word');
  for (const s of S) {
    const sl = add();
    if (s.k === 'title') {
      sl.addShape(pres.shapes.OVAL, { x: 7.3, y: -1.2, w: 3.6, h: 3.6, fill: { color: C.tealS }, line: { color: C.tealS } });
      sl.addText('ANH VĂN CHUYÊN NGÀNH 2 · ÔN LUYỆN NHA KHOA', { x: 0.5, y: 0.9, w: 7, h: 0.3, fontSize: 10, bold: true, color: C.tealD, charSpacing: 2, margin: 0, isTextBox: true });
      sl.addText([{ text: `U${u}`, options: { fontSize: 96, bold: true, color: C.teal } }, { text: ' /15', options: { fontSize: 28, bold: true, color: C.mut } }], { x: 0.45, y: 1.2, w: 6, h: 1.45, margin: 0, isTextBox: true, valign: 'bottom' });
      sl.addText(s.en, { x: 0.5, y: 2.75, w: 9, h: 0.8, fontSize: 40, bold: true, color: C.ink, margin: 0, isTextBox: true });
      sl.addText(s.vi, { x: 0.5, y: 3.55, w: 9, h: 0.5, fontSize: 22, color: C.gum, bold: true, margin: 0, isTextBox: true });
      sl.addText(`${s.n} từ mới   ·   Khoảng ${s.mins} phút   ·   Trắc nghiệm sau mỗi 4 từ`, { x: 0.5, y: 4.25, w: 9, h: 0.4, fontSize: 13, color: C.lampD, bold: true, margin: 0, isTextBox: true });
      sl.addNotes(`Mở đầu Unit ${u}: ${s.en} (${s.vi}). Unit có ${s.n} từ. Học mỗi từ: nghe đọc, đọc theo 3 lần, đọc ví dụ, đọc câu định nghĩa.`);
    } else if (s.k === 'intro') {
      tag(sl, 'Bắt đầu');
      sl.addText('Unit này nói về gì?', { x: 0.4, y: 0.62, w: 9, h: 0.6, fontSize: 28, bold: true, color: C.tealD, margin: 0, isTextBox: true });
      sl.addText(s.intro, { x: 0.4, y: 1.4, w: 4.4, h: 3.6, fontSize: fit(s.intro.length, [[260, 15], [360, 13], [9999, 12]]), color: C.ink, fill: { color: C.tealS }, line: { color: C.teal, width: 1.5 }, margin: 10, valign: 'top', rectRadius: 0.1, shape: pres.shapes.ROUNDED_RECTANGLE, isTextBox: true });
      sl.addText([{ text: 'HỌC MỖI TỪ THEO 4 BƯỚC', options: { fontSize: 9, bold: true, color: C.mut, breakLine: true, paraSpaceAfter: 6 } },
        ...s.how.map((h, k) => ({ text: h, options: { bullet: { type: 'number' }, fontSize: 14, color: C.ink, breakLine: k < s.how.length - 1, paraSpaceAfter: 6 } }))],
        { x: 5.0, y: 1.4, w: 4.6, h: 3.6, margin: 10, valign: 'top', fill: { color: 'FFFFFF' }, line: { color: C.line, width: 1.5 }, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, isTextBox: true });
      sl.addNotes(s.intro);
    } else if (s.k === 'map') {
      tag(sl, 'Danh sách từ', `${s.words.length} từ`);
      sl.addText(`Hôm nay mình học ${s.words.length} từ này`, { x: 0.4, y: 0.62, w: 9, h: 0.6, fontSize: 26, bold: true, color: C.tealD, margin: 0, isTextBox: true });
      const n = s.words.length, cols = n > 12 ? 4 : 3, rows = Math.ceil(n / cols), cw = (9.2 - (cols - 1) * 0.12) / cols, rh = Math.min(0.78, (3.85 - (rows - 1) * 0.1) / rows);
      s.words.forEach((w, k) => {
        const c = k % cols, r = Math.floor(k / cols);
        sl.addText([{ text: `${k + 1}  `, options: { color: C.mut, fontSize: 10 } }, { text: w[0], options: { bold: true, color: C.tealD, fontSize: 14, breakLine: true } }, { text: w[1], options: { color: C.mut, fontSize: 11 } }],
          { x: 0.4 + c * (cw + 0.12), y: 1.35 + r * (rh + 0.1), w: cw, h: rh, margin: 6, valign: 'middle', fill: { color: 'FFFFFF' }, line: { color: C.line, width: 1 }, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, isTextBox: true });
      });
      sl.addNotes('Đọc lướt danh sách: từ tiếng Anh và nghĩa. Chưa cần nhớ ngay.');
    } else if (s.k === 'word') {
      const wn = words.indexOf(s) + 1;
      tag(sl, `Từ ${wn} / ${words.length}`, s.pos);
      sl.addText(s.t, { x: 0.4, y: 0.6, w: 4.4, h: s.t.length > 13 ? 1.25 : 0.85, fontSize: fit(s.t.length, [[9, 48], [13, 40], [16, 32], [99, 28]]), bold: true, color: C.ink, margin: 0, valign: 'top', isTextBox: true });
      let y = 0.6 + (s.t.length > 13 ? 1.3 : 0.9);
      sl.addText([{ text: s.ipa + '   ', options: { color: C.mut, fontFace: 'Segoe UI' } }, { text: 'Đọc gần giống: ', options: { color: C.tealD, fontSize: 11 } }, { text: s.say, options: { color: C.tealD, bold: true } }],
        { x: 0.4, y, w: 4.4, h: 0.55, fontSize: 15, margin: 0, valign: 'top', isTextBox: true });
      y += 0.6;
      sl.addText(s.m, { x: 0.4, y, w: 4.4, h: 0.65, fontSize: fit(s.m.length, [[22, 24], [32, 20], [99, 17]]), bold: true, color: C.gum, margin: 0, valign: 'top', isTextBox: true });
      y += 0.72;
      sl.addText([{ text: 'MẸO NHỚ', options: { fontSize: 9, bold: true, color: C.lampD, breakLine: true } }, { text: s.hook, options: { fontSize: fit(s.hook.length, [[90, 14], [125, 12.5], [999, 11.5]]), color: C.ink } }],
        { x: 0.4, y, w: 4.4, h: Math.max(1.0, 5.15 - y), margin: 8, valign: 'top', fill: { color: C.lampS }, line: { color: C.lamp, width: 1.5 }, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, isTextBox: true });
      const exLen = s.ex.reduce((a, e) => a + e[0].length + e[1].length, 0), exPt = fit(exLen, [[200, 13.5], [260, 12.5], [999, 11.5]]);
      const ex = [{ text: 'VÍ DỤ', options: { fontSize: 9, bold: true, color: C.mut, breakLine: true, paraSpaceAfter: 2 } }];
      s.ex.forEach((e, k) => { ex.push({ text: `${k + 1}. `, options: { fontSize: exPt, color: C.teal, bold: true } }, ...runs(s.t, e[0], { fontSize: exPt, color: C.ink }), { text: '', options: { breakLine: true } }, { text: '    ' + e[1], options: { fontSize: exPt - 1.5, color: C.mut, breakLine: k < 2, paraSpaceAfter: 5 } }); });
      sl.addText(ex, { x: 5.0, y: 0.6, w: 4.6, h: 2.25, margin: 2, valign: 'top', isTextBox: true });
      const dLen = s.def.length + s.defv.length, dPt = fit(dLen, [[230, 12.5], [330, 11], [420, 10], [999, 9]]);
      sl.addText([{ text: 'CÂU ĐỊNH NGHĨA TRONG ĐỀ', options: { fontSize: 9, bold: true, color: C.gum, breakLine: true, paraSpaceAfter: 2 } },
        ...runs(s.t, s.def, { fontSize: dPt, color: C.ink }), { text: '', options: { breakLine: true } },
        { text: s.defv, options: { fontSize: dPt - 1, color: C.mut, breakLine: !!s.kw, paraSpaceBefore: 3 } },
        ...(s.kw ? [{ text: 'Chữ khóa: ', options: { fontSize: dPt - 1, color: C.tealD } }, { text: s.kw, options: { fontSize: dPt - 1, color: C.tealD, bold: true } }] : [])],
        { x: 5.0, y: 2.95, w: 4.6, h: 2.2, margin: 8, valign: 'top', fill: { color: C.gumS }, line: { color: C.gumL, width: 1.5 }, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, isTextBox: true });
      sl.addNotes(`${s.t} ${s.ipa} (đọc gần giống: ${s.say}) = ${s.m}.\nMẹo nhớ: ${s.hook}\nCho người học đọc to từ 3 lần, đọc 3 câu ví dụ, rồi đọc câu định nghĩa. Hỏi: chữ nào trong định nghĩa giúp nhận ra từ này?`);
    } else if (s.k === 'quiz' || s.k === 'ans') {
      tag(sl, s.title, s.k === 'quiz' ? (s.sub || '') : '');
      const n = s.q.length, gap = 0.12, top = 0.62, h = (4.55 - gap * (n - 1)) / n;
      s.q.forEach((q, k) => {
        const y = top + k * (h + gap), no = (s.base || 0) + k + 1;
        if (s.k === 'quiz') {
          // chọn cỡ chữ để câu hỏi vừa phần trên của ô (ước lượng 0.5 em mỗi ký tự)
          let pPt = 14; const room = h * 0.56 - 0.24;
          while (pPt > 8.5 && Math.ceil(q.p.length / ((8.9 * 72) / (pPt * 0.5))) * pPt * 1.22 / 72 > room) pPt -= 0.5;
          sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.4, y, w: 9.2, h, fill: { color: 'FFFFFF' }, line: { color: C.line, width: 1.25 }, rectRadius: 0.08 });
          sl.addText([{ text: ` ${no} `, options: { bold: true, color: 'FFFFFF', highlight: C.teal, fontSize: 12 } }, { text: '   ' + q.lab.toUpperCase(), options: { fontSize: 8.5, bold: true, color: C.mut } }, { text: '', options: { breakLine: true } },
            { text: q.p, options: { fontSize: pPt, bold: true, color: C.ink } }], { x: 0.55, y: y + 0.05, w: 8.9, h: h * 0.56, margin: 0, valign: 'top', isTextBox: true });
          const oh = Math.min(0.42, h * 0.34), ow = (8.9 - 3 * 0.1) / 4, oy = y + h - oh - 0.06;
          q.o.forEach((o, j) => sl.addText([{ text: 'ABCD'[j] + '  ', options: { bold: true, color: C.teal } }, { text: o, options: { color: C.ink } }],
            { x: 0.55 + j * (ow + 0.1), y: oy, w: ow, h: oh, fontSize: fit(o.length, [[18, 12], [28, 10.5], [99, 9.5]]), margin: 4, valign: 'middle', fill: { color: C.bg }, line: { color: C.line, width: 1 }, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, isTextBox: true }));
        } else {
          sl.addText([{ text: ` ${no} `, options: { bold: true, color: 'FFFFFF', highlight: C.ok, fontSize: 13 } }, { text: `  ${'ABCD'[q.a]}. ${q.o[q.a]}`, options: { bold: true, color: C.ok, fontSize: 14, breakLine: true } },
            { text: q.why, options: { color: C.mut, fontSize: fit(q.why.length, [[120, 12], [200, 11], [999, 10]]) } }], { x: 0.4, y, w: 9.2, h, margin: 4, valign: 'top', isTextBox: true });
        }
      });
      sl.addNotes(s.k === 'quiz' ? 'Cho người học tự chọn đáp án rồi chuyển sang slide sau để xem đáp án.' : s.q.map((q, k) => `Câu ${(s.base || 0) + k + 1}: ${'ABCD'[q.a]}. ${q.o[q.a]} – ${q.why}`).join('\n'));
    } else if (s.k === 'recap') {
      tag(sl, 'Tổng kết');
      sl.addText(`Ôn lại ${s.words.length} từ của Unit ${u}`, { x: 0.4, y: 0.6, w: 9, h: 0.55, fontSize: 24, bold: true, color: C.tealD, margin: 0, isTextBox: true });
      const half = Math.ceil(s.words.length / 2), pt = s.words.length > 12 ? 10 : 11.5;
      [s.words.slice(0, half), s.words.slice(half)].forEach((part, c) => {
        sl.addTable(part.map(w => [{ text: w[0], options: { bold: true, color: C.tealD } }, { text: w[1], options: { color: C.mut, fontFace: 'Segoe UI' } }, { text: w[2], options: { color: C.ink } }]),
          { x: 0.4 + c * 4.7, y: 1.3, w: 4.5, colW: [1.45, 1.35, 1.7], fontSize: pt, border: { type: 'solid', pt: 0.75, color: C.line }, margin: 3, valign: 'middle' });
      });
      sl.addNotes('Che cột nghĩa và tự nói nghĩa của từng từ. Sau đó che cột từ và nói lại từ tiếng Anh.');
    } else if (s.k === 'end') {
      tag(sl, 'Hoàn thành');
      sl.addText(`Xong Unit ${u} rồi!`, { x: 0.4, y: 0.9, w: 9, h: 0.9, fontSize: 40, bold: true, color: C.tealD, margin: 0, isTextBox: true });
      sl.addText([{ text: 'ÔN CHO NHỚ LÂU', options: { fontSize: 9, bold: true, color: C.tealD, breakLine: true, paraSpaceAfter: 4 } },
        ...[`Bấm Luyện từ 5 bậc ở bài Unit ${u} trong app.`, 'Ngày mai mở lại slide Tổng kết, che cột nghĩa và tự nói nghĩa.', 'Làm lại bài Kiểm tra cuối Unit sau 3 ngày.'].map((t, k) => ({ text: t, options: { bullet: { type: 'number' }, fontSize: 14, color: C.ink, breakLine: k < 2, paraSpaceAfter: 6 } }))],
        { x: 0.4, y: 2.0, w: 5.2, h: 2.4, margin: 10, valign: 'top', fill: { color: C.tealS }, line: { color: C.teal, width: 1.5 }, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, isTextBox: true });
      sl.addText(s.next ? [{ text: 'UNIT TIẾP THEO', options: { fontSize: 9, bold: true, color: C.mut, breakLine: true, paraSpaceAfter: 4 } }, { text: `U${u + 1} · ${s.next}`, options: { fontSize: 15, bold: true, color: C.ink } }]
        : [{ text: 'CHÚC MỪNG', options: { fontSize: 9, bold: true, color: C.mut, breakLine: true, paraSpaceAfter: 4 } }, { text: 'Bạn đã đi hết 15 Unit. Hãy làm đề thi thử trong app.', options: { fontSize: 14, color: C.ink } }],
        { x: 5.8, y: 2.0, w: 3.8, h: 2.4, margin: 10, valign: 'top', fill: { color: 'FFFFFF' }, line: { color: C.line, width: 1.5 }, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, isTextBox: true });
      sl.addNotes('Kết thúc Unit. Nhắc người học ôn lại bằng Luyện từ 5 bậc trong app.');
    }
  }
  return pres;
}
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const keys = Object.keys(F).filter(k => !only.length || only.includes(k.replace('avcn2-u', '')));
  for (const k of keys) {
    const u = Number(k.replace('avcn2-u', '')), slug = TITLES[u].split(' – ')[0].replace(/[^A-Za-z0-9]+/g, '-').replace(/^-|-$/g, '');
    const file = path.join(OUT, `AVCN2-Slide-Unit-${String(u).padStart(2, '0')}-${slug}.pptx`);
    await unitPptx(k).writeFile({ fileName: file });
    await applyTheme(file, THEME);
    console.log(path.basename(file));
  }
})();

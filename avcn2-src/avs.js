/* @@AVS-JS: slide Anh văn chuyên ngành 2 vẽ bằng HTML (Version 2.6.3) */
var AVS_DECKS = __AVS_DATA__;
const AVS_SPK = '<svg viewBox="0 0 24 24"><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z"/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11"/></svg>';
const avsEsc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
function avsMark(term, s) {
  const e = avsEsc(s), t = avsEsc(term).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return e.replace(new RegExp('(^|[^A-Za-z])(' + t + ')(?![A-Za-z])', 'gi'), '$1<mark>$2</mark>');
}
const avsBlank = s => avsEsc(s).replace(/_____/g, '<span style="letter-spacing:.06em">_______</span>');
function avsSlide(S, i, print) {
  const s = S[i], U = `<b>Unit ${s.u}</b>`, cls = `avs k-${s.k}${print ? ' print' : ''}`;
  const words = S.filter(x => x.k === 'word'), wn = words.indexOf(s) + 1;
  const spk = (t, sm) => `<button class="spk${sm ? ' sm' : ''}" type="button" data-avsay="${avsEsc(t)}" aria-label="Nghe đọc ${avsEsc(t)}">${AVS_SPK}</button>`;
  if (s.k === 'title') return `<div class="${cls}"><span class="course">Anh văn chuyên ngành 2 · Ôn Luyện Nha Khoa</span>
    <div class="big-u">U${s.u}<small>/15</small></div><h2>${avsEsc(s.en)}</h2><div class="vi">${avsEsc(s.vi)}</div>
    <div class="meta"><span>${s.n} từ mới</span><span>Khoảng ${s.mins} phút</span><span>Trắc nghiệm sau mỗi 4 từ</span></div></div>`;
  if (s.k === 'intro') return `<div class="${cls}"><div class="top">${U}<span>Bắt đầu</span></div><h2 class="h">Unit này nói về gì?</h2>
    <div class="two"><div class="box teal">${avsEsc(s.intro)}</div><div class="box"><span class="lbl">Học mỗi từ theo 4 bước</span><ol class="steps">${s.how.map(h => `<li>${avsEsc(h)}</li>`).join('')}</ol></div></div></div>`;
  if (s.k === 'map') return `<div class="${cls}"><div class="top">${U}<span>Danh sách từ</span><span class="r">${s.words.length} từ</span></div><h2 class="h">Hôm nay mình học ${s.words.length} từ này</h2>
    <div class="map">${s.words.map(w => `<div><b>${avsEsc(w[0])}</b><span>${avsEsc(w[1])}</span></div>`).join('')}</div></div>`;
  if (s.k === 'word') return `<div class="${cls}"><div class="top">${U}<span>Từ ${wn} / ${words.length}</span><span class="r pill">${avsEsc(s.pos)}</span></div>
    <div class="two w"><div class="col">
      <div class="wt"><h2>${avsEsc(s.t)}</h2>${spk(s.t)}</div>
      <div class="ipa-l"><span class="ipa">${avsEsc(s.ipa)}</span><span class="say"><small>Đọc gần giống</small>${avsEsc(s.say)}</span></div>
      <div class="mean">${avsEsc(s.m)}</div>
      <div class="box lamp"><span class="lbl">Mẹo nhớ</span>${avsEsc(s.hook)}</div>
    </div><div class="col">
      <div><span class="lbl">Ví dụ</span><ol class="exs">${s.ex.map((e, k) => `<li><span class="n">${k + 1}</span><span class="en">${avsMark(s.t, e[0])}</span><span class="vi">${avsEsc(e[1])}</span></li>`).join('')}</ol></div>
      <div class="box gum def"><span class="lbl">Câu định nghĩa trong đề</span><div class="en">${avsMark(s.t, s.def)}</div><div class="vi">${avsEsc(s.defv)}</div>${s.kw ? `<div class="kw">Chữ khóa: <b>${avsEsc(s.kw)}</b></div>` : ''}</div>
    </div></div></div>`;
  if (s.k === 'quiz') {
    const b = s.base || 0;
    return `<div class="${cls}"><div class="top">${U}<span>${avsEsc(s.title)}</span><span class="r">${avsEsc(s.sub || '')}</span></div>
    <div class="qs${s.q.length > 3 ? ' c2' : ''}">${s.q.map((q, k) => `<div class="q" data-avsq="${k}"><div class="qh"><span class="qn">${b + k + 1}</span><span class="ql">${avsEsc(q.lab)}</span></div>
      <div class="qp">${avsBlank(q.p)}</div><div class="opts">${q.o.map((o, j) => `<button class="opt" type="button" data-avso="${j}"><i>${'ABCD'[j]}</i><span>${avsEsc(o)}</span></button>`).join('')}</div>
      <div class="why" hidden></div></div>`).join('')}</div>${print ? '' : '<div class="score" aria-live="polite"></div>'}</div>`;
  }
  if (s.k === 'ans') {
    const b = s.base || 0;
    return `<div class="${cls}"><div class="top">${U}<span>${avsEsc(s.title)}</span></div>
    <div class="ans">${s.q.map((q, k) => `<div><b class="n">${b + k + 1}</b><strong>${'ABCD'[q.a]}. ${avsEsc(q.o[q.a])}</strong><span>${avsEsc(q.why)}</span></div>`).join('')}</div></div>`;
  }
  if (s.k === 'recap') {
    const h = Math.ceil(s.words.length / 2), row = w => `<tr><td>${avsEsc(w[0])}</td><td class="ipa">${avsEsc(w[1])}</td><td>${avsEsc(w[2])}</td></tr>`;
    return `<div class="${cls}"><div class="top">${U}<span>Tổng kết</span></div><h2 class="h">Ôn lại ${s.words.length} từ của Unit ${s.u}</h2>
    <div class="rc-wrap"><table class="rc"><tbody>${s.words.slice(0, h).map(row).join('')}</tbody></table><table class="rc"><tbody>${s.words.slice(h).map(row).join('')}</tbody></table></div></div>`;
  }
  if (s.k === 'end') return `<div class="${cls}"><div class="top">${U}<span>Hoàn thành</span></div><h2>Xong Unit ${s.u} rồi!</h2>
    <div class="two"><div class="box teal"><span class="lbl">Ôn cho nhớ lâu</span><ol class="steps"><li>Bấm <b>Luyện từ 5 bậc</b> ở bài Unit ${s.u} để luyện nghe, nghĩa và định nghĩa.</li><li>Ngày mai mở lại slide Tổng kết, che cột nghĩa và tự nói nghĩa.</li><li>Làm lại bài Kiểm tra cuối Unit sau 3 ngày.</li></ol></div>
    ${s.next ? `<div class="box"><span class="lbl">Unit tiếp theo</span><b>U${s.u + 1} · ${avsEsc(s.next)}</b></div>` : '<div class="box"><span class="lbl">Chúc mừng</span>Bạn đã đi hết 15 Unit. Hãy làm đề thi thử trong app để kiểm tra.</div>'}</div></div>`;
  return `<div class="${cls}"></div>`;
}
function avsThumb(s, i) {
  const lab = s.k === 'word' ? s.t : s.k === 'quiz' ? s.title : ({ title: 'Mở đầu', intro: 'Unit này nói về gì?', map: 'Danh sách từ', recap: 'Tổng kết', end: 'Hoàn thành' })[s.k] || '';
  const c = s.k === 'word' ? 'w' : s.k === 'quiz' ? 'q' : '';
  const kind = s.k === 'word' ? 'Từ' : s.k === 'quiz' ? 'Trắc nghiệm' : 'Slide';
  return { c, html: `<i>${kind}</i>${avsEsc(lab)}` };
}
function avsAnswer(root, S, i, qi, oj) {
  const s = S[i]; if (!s || s.k !== 'quiz') return;
  const q = s.q[qi], box = root.querySelector(`[data-avsq="${qi}"]`); if (!q || !box || box.dataset.done) return;
  box.dataset.done = oj === q.a ? 'ok' : 'no';
  box.querySelectorAll('.opt').forEach((b, j) => { b.disabled = true; if (j === q.a) b.classList.add('ok'); else if (j === oj) b.classList.add('no'); });
  const why = box.querySelector('.why'); why.hidden = false;
  why.innerHTML = `<b>${oj === q.a ? 'Đúng rồi!' : `Chưa đúng. Đáp án: ${'ABCD'[q.a]}. ${avsEsc(q.o[q.a])}`}</b> ${avsEsc(q.why)}`;
  const done = root.querySelectorAll('[data-avsq][data-done]'), ok = root.querySelectorAll('[data-avsq][data-done="ok"]');
  const sc = root.querySelector('.score');
  if (sc) sc.textContent = done.length === s.q.length ? `Bạn đúng ${ok.length}/${s.q.length} câu. ${ok.length === s.q.length ? 'Tuyệt vời!' : 'Xem lại các từ chưa đúng rồi làm lại nhé.'}` : `Đã làm ${done.length}/${s.q.length} câu`;
}
var AVS_META = __AVS_META__;
(function () {
  if (typeof SLIDES !== 'object' || !SLIDES) return;
  window.__avs = { decks: AVS_DECKS };
  for (const k in AVS_DECKS) SLIDES[k] = { n: AVS_DECKS[k].length, deck: true, base: 'slides/avcn2', pptx: AVS_META[k].pptx, print: AVS_META[k].print };
  const box = document.getElementById('sl-html'); if (!box) return;
  box.addEventListener('click', e => {
    const sp = e.target.closest('[data-avsay]');
    if (sp) { if (typeof vtSpeak === 'function') vtSpeak(sp.dataset.avsay); return; }
    const o = e.target.closest('[data-avso]'), q = o && o.closest('[data-avsq]');
    if (o && q) avsAnswer(box, AVS_DECKS[SL.id], SL.i, Number(q.dataset.avsq), Number(o.dataset.avso));
  });
})();
/* @@AVS-JS-END */
